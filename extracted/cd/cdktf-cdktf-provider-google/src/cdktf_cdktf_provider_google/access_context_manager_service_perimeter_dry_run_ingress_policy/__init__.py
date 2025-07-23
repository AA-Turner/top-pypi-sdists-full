r'''
# `google_access_context_manager_service_perimeter_dry_run_ingress_policy`

Refer to the Terraform Registry for docs: [`google_access_context_manager_service_perimeter_dry_run_ingress_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy).
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


class AccessContextManagerServicePerimeterDryRunIngressPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy google_access_context_manager_service_perimeter_dry_run_ingress_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        perimeter: builtins.str,
        id: typing.Optional[builtins.str] = None,
        ingress_from: typing.Optional[typing.Union["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        ingress_to: typing.Optional[typing.Union["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy google_access_context_manager_service_perimeter_dry_run_ingress_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param perimeter: The name of the Service Perimeter to add this resource to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#perimeter AccessContextManagerServicePerimeterDryRunIngressPolicy#perimeter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#id AccessContextManagerServicePerimeterDryRunIngressPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingress_from: ingress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#ingress_from AccessContextManagerServicePerimeterDryRunIngressPolicy#ingress_from}
        :param ingress_to: ingress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#ingress_to AccessContextManagerServicePerimeterDryRunIngressPolicy#ingress_to}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#timeouts AccessContextManagerServicePerimeterDryRunIngressPolicy#timeouts}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#title AccessContextManagerServicePerimeterDryRunIngressPolicy#title}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23fdef3d5ceca15bd81300d90361cefabaca5afd1e3aae3257b606c79bf0138b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessContextManagerServicePerimeterDryRunIngressPolicyConfig(
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
        '''Generates CDKTF code for importing a AccessContextManagerServicePerimeterDryRunIngressPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AccessContextManagerServicePerimeterDryRunIngressPolicy to import.
        :param import_from_id: The id of the existing AccessContextManagerServicePerimeterDryRunIngressPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AccessContextManagerServicePerimeterDryRunIngressPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b36f5070b809882ec5a74a7eccf7c6889d4f113f646a37f05feecc111dfdfb)
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
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: Identities can be an individual user, service account, Google group, or third-party identity. For third-party identity, only single identities are supported and other identity types are not supported.The v1 identities that have the prefix user, group and serviceAccount in https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#identities AccessContextManagerServicePerimeterDryRunIngressPolicy#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#identity_type AccessContextManagerServicePerimeterDryRunIngressPolicy#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#sources AccessContextManagerServicePerimeterDryRunIngressPolicy#sources}
        '''
        value = AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom(
            identities=identities, identity_type=identity_type, sources=sources
        )

        return typing.cast(None, jsii.invoke(self, "putIngressFrom", [value]))

    @jsii.member(jsii_name="putIngressTo")
    def put_ingress_to(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#operations AccessContextManagerServicePerimeterDryRunIngressPolicy#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#resources AccessContextManagerServicePerimeterDryRunIngressPolicy#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#roles AccessContextManagerServicePerimeterDryRunIngressPolicy#roles}
        '''
        value = AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#create AccessContextManagerServicePerimeterDryRunIngressPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#delete AccessContextManagerServicePerimeterDryRunIngressPolicy#delete}.
        '''
        value = AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts(
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
    ) -> "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromOutputReference":
        return typing.cast("AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromOutputReference", jsii.get(self, "ingressFrom"))

    @builtins.property
    @jsii.member(jsii_name="ingressTo")
    def ingress_to(
        self,
    ) -> "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOutputReference":
        return typing.cast("AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOutputReference", jsii.get(self, "ingressTo"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "AccessContextManagerServicePerimeterDryRunIngressPolicyTimeoutsOutputReference":
        return typing.cast("AccessContextManagerServicePerimeterDryRunIngressPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressFromInput")
    def ingress_from_input(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom"]:
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom"], jsii.get(self, "ingressFromInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressToInput")
    def ingress_to_input(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo"]:
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo"], jsii.get(self, "ingressToInput"))

    @builtins.property
    @jsii.member(jsii_name="perimeterInput")
    def perimeter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "perimeterInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3b105a490eeee316293ef12a621b67c80f29dba81928b5ec16d2be5935328adf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="perimeter")
    def perimeter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "perimeter"))

    @perimeter.setter
    def perimeter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f2278e6b574e088335af3cea3c63c3938a96ea81b0654584ff3eea8422f648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perimeter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0b5b308e16fc0c0852e9d8a1beddcbe2e1381391441a40256ba65b3ab6ad392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyConfig",
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
class AccessContextManagerServicePerimeterDryRunIngressPolicyConfig(
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
        ingress_from: typing.Optional[typing.Union["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        ingress_to: typing.Optional[typing.Union["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param perimeter: The name of the Service Perimeter to add this resource to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#perimeter AccessContextManagerServicePerimeterDryRunIngressPolicy#perimeter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#id AccessContextManagerServicePerimeterDryRunIngressPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingress_from: ingress_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#ingress_from AccessContextManagerServicePerimeterDryRunIngressPolicy#ingress_from}
        :param ingress_to: ingress_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#ingress_to AccessContextManagerServicePerimeterDryRunIngressPolicy#ingress_to}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#timeouts AccessContextManagerServicePerimeterDryRunIngressPolicy#timeouts}
        :param title: Human readable title. Must be unique within the perimeter. Does not affect behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#title AccessContextManagerServicePerimeterDryRunIngressPolicy#title}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(ingress_from, dict):
            ingress_from = AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom(**ingress_from)
        if isinstance(ingress_to, dict):
            ingress_to = AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo(**ingress_to)
        if isinstance(timeouts, dict):
            timeouts = AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553323c1307ee585e0e68ec74dfd3e2755b75a44dcccb786224092b4b57b2c94)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#perimeter AccessContextManagerServicePerimeterDryRunIngressPolicy#perimeter}
        '''
        result = self._values.get("perimeter")
        assert result is not None, "Required property 'perimeter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#id AccessContextManagerServicePerimeterDryRunIngressPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingress_from(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom"]:
        '''ingress_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#ingress_from AccessContextManagerServicePerimeterDryRunIngressPolicy#ingress_from}
        '''
        result = self._values.get("ingress_from")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom"], result)

    @builtins.property
    def ingress_to(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo"]:
        '''ingress_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#ingress_to AccessContextManagerServicePerimeterDryRunIngressPolicy#ingress_to}
        '''
        result = self._values.get("ingress_to")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#timeouts AccessContextManagerServicePerimeterDryRunIngressPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Human readable title. Must be unique within the perimeter. Does not affect behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#title AccessContextManagerServicePerimeterDryRunIngressPolicy#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterDryRunIngressPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom",
    jsii_struct_bases=[],
    name_mapping={
        "identities": "identities",
        "identity_type": "identityType",
        "sources": "sources",
    },
)
class AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom:
    def __init__(
        self,
        *,
        identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_type: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param identities: Identities can be an individual user, service account, Google group, or third-party identity. For third-party identity, only single identities are supported and other identity types are not supported.The v1 identities that have the prefix user, group and serviceAccount in https://cloud.google.com/iam/docs/principal-identifiers#v1 are supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#identities AccessContextManagerServicePerimeterDryRunIngressPolicy#identities}
        :param identity_type: Specifies the type of identities that are allowed access from outside the perimeter. If left unspecified, then members of 'identities' field will be allowed access. Possible values: ["ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#identity_type AccessContextManagerServicePerimeterDryRunIngressPolicy#identity_type}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#sources AccessContextManagerServicePerimeterDryRunIngressPolicy#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98c1b9f033988096c89dd9631d3bc5122a653ca783238f15ff1afd668e11b89)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#identities AccessContextManagerServicePerimeterDryRunIngressPolicy#identities}
        '''
        result = self._values.get("identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of identities that are allowed access from outside the perimeter.

        If left unspecified, then members of 'identities' field will be
        allowed access. Possible values: ["ANY_IDENTITY", "ANY_USER_ACCOUNT", "ANY_SERVICE_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#identity_type AccessContextManagerServicePerimeterDryRunIngressPolicy#identity_type}
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#sources AccessContextManagerServicePerimeterDryRunIngressPolicy#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adb92257b1c405c37a3372a0215c21d81b98c5fb3ffc76b389f8526ad458c22c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06effcd3e77ef5975715c6d66291e3b3ae1f4a59bea6bb32534f7921917601b8)
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
    ) -> "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSourcesList":
        return typing.cast("AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSourcesList", jsii.get(self, "sources"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="identities")
    def identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identities"))

    @identities.setter
    def identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9055fa227767ffee1fd09771e2fb8bc9f6e3fdec8ae6b8af342e62ad487cc39e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityType")
    def identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityType"))

    @identity_type.setter
    def identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b2998f13b1c3a1be83db7c6094b739609151482d84fc4cd17fa040666f110fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ae3e7ee85fe8a7b5521869d98415f0407bf1e0c8f59db8329222e8892be4069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "resource": "resource"},
)
class AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: An 'AccessLevel' resource name that allow resources within the 'ServicePerimeters' to be accessed from the internet. 'AccessLevels' listed must be in the same policy as this 'ServicePerimeter'. Referencing a nonexistent 'AccessLevel' will cause an error. If no 'AccessLevel' names are listed, resources within the perimeter can only be accessed via Google Cloud calls with request origins within the perimeter. Example 'accessPolicies/MY_POLICY/accessLevels/MY_LEVEL.' If * is specified, then all IngressSources will be allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#access_level AccessContextManagerServicePerimeterDryRunIngressPolicy#access_level}
        :param resource: A Google Cloud resource that is allowed to ingress the perimeter. Requests from these resources will be allowed to access perimeter data. Currently only projects are allowed. Format 'projects/{project_number}' The project may be in any Google Cloud organization, not just the organization that the perimeter is defined in. '*' is not allowed, the case of allowing all Google Cloud resources only is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#resource AccessContextManagerServicePerimeterDryRunIngressPolicy#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5b8d769884c3a5d178ca836f7d0da45c30b059b2c60bae3795b38a39f4d60b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#access_level AccessContextManagerServicePerimeterDryRunIngressPolicy#access_level}
        '''
        result = self._values.get("access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''A Google Cloud resource that is allowed to ingress the perimeter.

        Requests from these resources will be allowed to access perimeter data.
        Currently only projects are allowed. Format 'projects/{project_number}'
        The project may be in any Google Cloud organization, not just the
        organization that the perimeter is defined in. '*' is not allowed, the case
        of allowing all Google Cloud resources only is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#resource AccessContextManagerServicePerimeterDryRunIngressPolicy#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9858f4c9c258a34ccb12a71cb91ed8330eec573f84927f326908a79b9116a20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12fcafa7bbeadca27cde353b6f6565be84b5a0b7e83642d7068ecd6b8aa0b8a7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__151202e9b27cac8879ecfa1f5abf0c5a479ef73bc53f505571115bba76476827)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb9aa50a135601422139281e2ef01fdc249e3fac9728e434a51b2144438b479e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f94e5a743779ecc5019cc62f903b438704d168864ad50af1311b21470274a1c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dbaf1b609d1a79e53254e26355ff4109aff9a872455eb982f87f38e1dde8fda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f28f260737117c7c76309b4d2ec8ef0f7107dcf4370c561b62fd59b9b74a466d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8addb1fb04f826c524ea125f2cc1397284ab97783297a6b38c7d3aa3fb069477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4023d7bb2c637b51bb92f0edc1037cfddd54584876cfa1059cfe4f4c420e93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e895ea151daa448601c6de8ef282fa30feb44af9d48acbf91a918b3ed4a3a968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo",
    jsii_struct_bases=[],
    name_mapping={
        "operations": "operations",
        "resources": "resources",
        "roles": "roles",
    },
)
class AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo:
    def __init__(
        self,
        *,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#operations AccessContextManagerServicePerimeterDryRunIngressPolicy#operations}
        :param resources: A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'. A request matches if it contains a resource in this list. If '*' is specified for resources, then this 'IngressTo' rule will authorize access to all resources inside the perimeter, provided that the request also matches the 'operations' field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#resources AccessContextManagerServicePerimeterDryRunIngressPolicy#resources}
        :param roles: A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#roles AccessContextManagerServicePerimeterDryRunIngressPolicy#roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5252d007d42441ffb29444d40ad92162c643e277580c43f2da7febf4bd20ece0)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#operations AccessContextManagerServicePerimeterDryRunIngressPolicy#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations"]]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resources, currently only projects in the form 'projects/', protected by this 'ServicePerimeter' that are allowed to be accessed by sources defined in the corresponding 'IngressFrom'.

        A request matches if it contains
        a resource in this list. If '*' is specified for resources,
        then this 'IngressTo' rule will authorize access to all
        resources inside the perimeter, provided that the request
        also matches the 'operations' field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#resources AccessContextManagerServicePerimeterDryRunIngressPolicy#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IAM roles that represent the set of operations that the sources specified in the corresponding 'IngressFrom' are allowed to perform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#roles AccessContextManagerServicePerimeterDryRunIngressPolicy#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "method_selectors": "methodSelectors",
        "service_name": "serviceName",
    },
)
class AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations:
    def __init__(
        self,
        *,
        method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method_selectors: method_selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#method_selectors AccessContextManagerServicePerimeterDryRunIngressPolicy#method_selectors}
        :param service_name: The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow. A single 'ApiOperation' with 'serviceName' field set to '*' will allow all methods AND permissions for all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#service_name AccessContextManagerServicePerimeterDryRunIngressPolicy#service_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c50bb942bd38f823812ce8d7cffa7fa5368899dcf6b3239be6faac45ed108294)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors"]]]:
        '''method_selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#method_selectors AccessContextManagerServicePerimeterDryRunIngressPolicy#method_selectors}
        '''
        result = self._values.get("method_selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors"]]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the API whose methods or permissions the 'IngressPolicy' or 'EgressPolicy' want to allow.

        A single 'ApiOperation' with 'serviceName'
        field set to '*' will allow all methods AND permissions for all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#service_name AccessContextManagerServicePerimeterDryRunIngressPolicy#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a61047d43e006fe93301f4ad88a26ef81595e31ae53c4af8029431278ccd5fad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__409e73c5bc8cd8ffa9a9f44dfb4746f336639cb7d2c4c7fc184f1674698e8577)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c3ad5d4786e9540bd3b45c262c1bc3a67db4bfb534e093979e4f0fd2f80137)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a5eefecd60fc7a0f6f9c2d070eeafc6eebd913eb6199663f0f353d7efd8c314)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f563b59659837793e11073772b49003c2b03113112dbf3e0a808a5a9e71e9bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31297842a7b5c4bfdd363ca8850f097a03a7c41395ea44c1ace28d56d7df3694)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "permission": "permission"},
)
class AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors:
    def __init__(
        self,
        *,
        method: typing.Optional[builtins.str] = None,
        permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param method: Value for method should be a valid method name for the corresponding serviceName in 'ApiOperation'. If '*' used as value for 'method', then ALL methods and permissions are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#method AccessContextManagerServicePerimeterDryRunIngressPolicy#method}
        :param permission: Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#permission AccessContextManagerServicePerimeterDryRunIngressPolicy#permission}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9f562b4f7af87dbe52bcbc8736a0f12f8c6bd006fc2256423b9e3b6807e012)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#method AccessContextManagerServicePerimeterDryRunIngressPolicy#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''Value for permission should be a valid Cloud IAM permission for the corresponding 'serviceName' in 'ApiOperation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#permission AccessContextManagerServicePerimeterDryRunIngressPolicy#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43ea0fbc40f1adf17605da6b830397481a7aca585737689f4d7591081dcd610e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abb888483d1dcf21088aca2b7ab8859f7159cc79a033a0ab08cf58370f712d4f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373727d96ebc36f152c247603b3332661887414998af91d5969a0467ac255300)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e638b8ac5f3662ddd070116588497e2c3e602b24eac58da6d202b60fb36211dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbe399f92d8b78c1e7ac32f163db8654f18429485a249d9592a25c06e57afb5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cac2a70fdf819b6071fe2bb671b0866ec899ecd7eb8ce0059693a5f76cb42c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc0bd47b748175a58e0e85662d933f4d496f2d54a52b2c972cdde1612615ec8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__202a7f71bbecd60ae83d6b334cc92b6139f24b2807dd91dfa2da61f7fdf64b3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permission"))

    @permission.setter
    def permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90a187fb7839355c57c9938b9e2b599bf6dc3370b66692e8071261098800dd71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f9d2c2d533433122b44a47c6906dea46a4af584a8e4d4941424ba76a07fafc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__693bb9408b88979562e0d68548949b021651da8f8cc1537e359332d584c1e9c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethodSelectors")
    def put_method_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55ea437b08c2b4fe67894cf35f2d292d67728afb101a11c8237600aab6e5977)
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
    ) -> AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectorsList:
        return typing.cast(AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectorsList, jsii.get(self, "methodSelectors"))

    @builtins.property
    @jsii.member(jsii_name="methodSelectorsInput")
    def method_selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors]]], jsii.get(self, "methodSelectorsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c2d8e960540f53a111621dd8f6a7d233d09e386a22fe7cc83f2a39ec4b9bb076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2fcc185387b63a0c4a84533636f52fe9f3b7dc581c72dd0052a819c7e1aa56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57770bfe1068a7d55cba5c4fc82f16dcf29b97b19606f33f7ebd3787185885cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8878a18c49cc7d6912ebe20bfa084200a8d66da214955695a3d25c096dbaee00)
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
    ) -> AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsList:
        return typing.cast(AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations]]], jsii.get(self, "operationsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e177dc249c2c94f5b0e2a4b0e5c2cb0832bc833599e8e45d5b4f9e660c2098cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__135e5ae90d2a3d46d455f7b8568587fc67ff3d4fd1bf7c959f342731f09e951f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo]:
        return typing.cast(typing.Optional[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b4ad29c9a330840cd083dcf3d4751c8233ef531a3fe14bcd5681214d27bfb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#create AccessContextManagerServicePerimeterDryRunIngressPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#delete AccessContextManagerServicePerimeterDryRunIngressPolicy#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc591caed462948d65fc63690df32b55c860f84744f5cd67cbec8e45e7fea24)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#create AccessContextManagerServicePerimeterDryRunIngressPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_service_perimeter_dry_run_ingress_policy#delete AccessContextManagerServicePerimeterDryRunIngressPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerServicePerimeterDryRunIngressPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerServicePerimeterDryRunIngressPolicy.AccessContextManagerServicePerimeterDryRunIngressPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c87f126ab82276b26806c34fc89ee4a51d5a5da85f8b80aa539a7c27280218c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__530a492e44bde8a085aee6eba6ea03a3ecea22c66076768fd53bcd36b483f243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5ceed5761e91f839919c04d490a20eadd96e925592f58e4dbcedb3e2975d51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e55cbec02710825c0d024bcc2bf8a3e3b6f02b76ac6c58e53ab686a7aa51f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AccessContextManagerServicePerimeterDryRunIngressPolicy",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyConfig",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromOutputReference",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSourcesList",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSourcesOutputReference",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsList",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectorsList",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectorsOutputReference",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsOutputReference",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOutputReference",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts",
    "AccessContextManagerServicePerimeterDryRunIngressPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__23fdef3d5ceca15bd81300d90361cefabaca5afd1e3aae3257b606c79bf0138b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    perimeter: builtins.str,
    id: typing.Optional[builtins.str] = None,
    ingress_from: typing.Optional[typing.Union[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    ingress_to: typing.Optional[typing.Union[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d8b36f5070b809882ec5a74a7eccf7c6889d4f113f646a37f05feecc111dfdfb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b105a490eeee316293ef12a621b67c80f29dba81928b5ec16d2be5935328adf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f2278e6b574e088335af3cea3c63c3938a96ea81b0654584ff3eea8422f648(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b5b308e16fc0c0852e9d8a1beddcbe2e1381391441a40256ba65b3ab6ad392(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553323c1307ee585e0e68ec74dfd3e2755b75a44dcccb786224092b4b57b2c94(
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
    ingress_from: typing.Optional[typing.Union[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    ingress_to: typing.Optional[typing.Union[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98c1b9f033988096c89dd9631d3bc5122a653ca783238f15ff1afd668e11b89(
    *,
    identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_type: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb92257b1c405c37a3372a0215c21d81b98c5fb3ffc76b389f8526ad458c22c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06effcd3e77ef5975715c6d66291e3b3ae1f4a59bea6bb32534f7921917601b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9055fa227767ffee1fd09771e2fb8bc9f6e3fdec8ae6b8af342e62ad487cc39e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2998f13b1c3a1be83db7c6094b739609151482d84fc4cd17fa040666f110fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae3e7ee85fe8a7b5521869d98415f0407bf1e0c8f59db8329222e8892be4069(
    value: typing.Optional[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5b8d769884c3a5d178ca836f7d0da45c30b059b2c60bae3795b38a39f4d60b(
    *,
    access_level: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9858f4c9c258a34ccb12a71cb91ed8330eec573f84927f326908a79b9116a20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12fcafa7bbeadca27cde353b6f6565be84b5a0b7e83642d7068ecd6b8aa0b8a7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151202e9b27cac8879ecfa1f5abf0c5a479ef73bc53f505571115bba76476827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9aa50a135601422139281e2ef01fdc249e3fac9728e434a51b2144438b479e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94e5a743779ecc5019cc62f903b438704d168864ad50af1311b21470274a1c4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dbaf1b609d1a79e53254e26355ff4109aff9a872455eb982f87f38e1dde8fda(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28f260737117c7c76309b4d2ec8ef0f7107dcf4370c561b62fd59b9b74a466d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8addb1fb04f826c524ea125f2cc1397284ab97783297a6b38c7d3aa3fb069477(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4023d7bb2c637b51bb92f0edc1037cfddd54584876cfa1059cfe4f4c420e93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e895ea151daa448601c6de8ef282fa30feb44af9d48acbf91a918b3ed4a3a968(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyIngressFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5252d007d42441ffb29444d40ad92162c643e277580c43f2da7febf4bd20ece0(
    *,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50bb942bd38f823812ce8d7cffa7fa5368899dcf6b3239be6faac45ed108294(
    *,
    method_selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a61047d43e006fe93301f4ad88a26ef81595e31ae53c4af8029431278ccd5fad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409e73c5bc8cd8ffa9a9f44dfb4746f336639cb7d2c4c7fc184f1674698e8577(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c3ad5d4786e9540bd3b45c262c1bc3a67db4bfb534e093979e4f0fd2f80137(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5eefecd60fc7a0f6f9c2d070eeafc6eebd913eb6199663f0f353d7efd8c314(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f563b59659837793e11073772b49003c2b03113112dbf3e0a808a5a9e71e9bc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31297842a7b5c4bfdd363ca8850f097a03a7c41395ea44c1ace28d56d7df3694(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9f562b4f7af87dbe52bcbc8736a0f12f8c6bd006fc2256423b9e3b6807e012(
    *,
    method: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ea0fbc40f1adf17605da6b830397481a7aca585737689f4d7591081dcd610e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb888483d1dcf21088aca2b7ab8859f7159cc79a033a0ab08cf58370f712d4f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373727d96ebc36f152c247603b3332661887414998af91d5969a0467ac255300(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e638b8ac5f3662ddd070116588497e2c3e602b24eac58da6d202b60fb36211dd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe399f92d8b78c1e7ac32f163db8654f18429485a249d9592a25c06e57afb5f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cac2a70fdf819b6071fe2bb671b0866ec899ecd7eb8ce0059693a5f76cb42c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0bd47b748175a58e0e85662d933f4d496f2d54a52b2c972cdde1612615ec8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202a7f71bbecd60ae83d6b334cc92b6139f24b2807dd91dfa2da61f7fdf64b3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a187fb7839355c57c9938b9e2b599bf6dc3370b66692e8071261098800dd71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f9d2c2d533433122b44a47c6906dea46a4af584a8e4d4941424ba76a07fafc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693bb9408b88979562e0d68548949b021651da8f8cc1537e359332d584c1e9c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55ea437b08c2b4fe67894cf35f2d292d67728afb101a11c8237600aab6e5977(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperationsMethodSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d8e960540f53a111621dd8f6a7d233d09e386a22fe7cc83f2a39ec4b9bb076(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2fcc185387b63a0c4a84533636f52fe9f3b7dc581c72dd0052a819c7e1aa56(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57770bfe1068a7d55cba5c4fc82f16dcf29b97b19606f33f7ebd3787185885cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8878a18c49cc7d6912ebe20bfa084200a8d66da214955695a3d25c096dbaee00(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e177dc249c2c94f5b0e2a4b0e5c2cb0832bc833599e8e45d5b4f9e660c2098cc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135e5ae90d2a3d46d455f7b8568587fc67ff3d4fd1bf7c959f342731f09e951f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b4ad29c9a330840cd083dcf3d4751c8233ef531a3fe14bcd5681214d27bfb7(
    value: typing.Optional[AccessContextManagerServicePerimeterDryRunIngressPolicyIngressTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc591caed462948d65fc63690df32b55c860f84744f5cd67cbec8e45e7fea24(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c87f126ab82276b26806c34fc89ee4a51d5a5da85f8b80aa539a7c27280218c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530a492e44bde8a085aee6eba6ea03a3ecea22c66076768fd53bcd36b483f243(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5ceed5761e91f839919c04d490a20eadd96e925592f58e4dbcedb3e2975d51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e55cbec02710825c0d024bcc2bf8a3e3b6f02b76ac6c58e53ab686a7aa51f24(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerServicePerimeterDryRunIngressPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

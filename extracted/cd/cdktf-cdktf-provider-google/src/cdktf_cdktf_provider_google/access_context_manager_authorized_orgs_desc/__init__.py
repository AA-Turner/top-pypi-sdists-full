r'''
# `google_access_context_manager_authorized_orgs_desc`

Refer to the Terraform Registry for docs: [`google_access_context_manager_authorized_orgs_desc`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc).
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


class AccessContextManagerAuthorizedOrgsDesc(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAuthorizedOrgsDesc.AccessContextManagerAuthorizedOrgsDesc",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc google_access_context_manager_authorized_orgs_desc}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        parent: builtins.str,
        asset_type: typing.Optional[builtins.str] = None,
        authorization_direction: typing.Optional[builtins.str] = None,
        authorization_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        orgs: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerAuthorizedOrgsDescTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc google_access_context_manager_authorized_orgs_desc} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Resource name for the 'AuthorizedOrgsDesc'. Format: 'accessPolicies/{access_policy}/authorizedOrgsDescs/{authorized_orgs_desc}'. The 'authorized_orgs_desc' component must begin with a letter, followed by alphanumeric characters or '_'. After you create an 'AuthorizedOrgsDesc', you cannot change its 'name'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#name AccessContextManagerAuthorizedOrgsDesc#name}
        :param parent: Required. Resource name for the access policy which owns this 'AuthorizedOrgsDesc'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#parent AccessContextManagerAuthorizedOrgsDesc#parent}
        :param asset_type: The type of entities that need to use the authorization relationship during evaluation, such as a device. Valid values are "ASSET_TYPE_DEVICE" and "ASSET_TYPE_CREDENTIAL_STRENGTH". Possible values: ["ASSET_TYPE_DEVICE", "ASSET_TYPE_CREDENTIAL_STRENGTH"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#asset_type AccessContextManagerAuthorizedOrgsDesc#asset_type}
        :param authorization_direction: The direction of the authorization relationship between this organization and the organizations listed in the "orgs" field. The valid values for this field include the following: AUTHORIZATION_DIRECTION_FROM: Allows this organization to evaluate traffic in the organizations listed in the 'orgs' field. AUTHORIZATION_DIRECTION_TO: Allows the organizations listed in the 'orgs' field to evaluate the traffic in this organization. For the authorization relationship to take effect, all of the organizations must authorize and specify the appropriate relationship direction. For example, if organization A authorized organization B and C to evaluate its traffic, by specifying "AUTHORIZATION_DIRECTION_TO" as the authorization direction, organizations B and C must specify "AUTHORIZATION_DIRECTION_FROM" as the authorization direction in their "AuthorizedOrgsDesc" resource. Possible values: ["AUTHORIZATION_DIRECTION_TO", "AUTHORIZATION_DIRECTION_FROM"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#authorization_direction AccessContextManagerAuthorizedOrgsDesc#authorization_direction}
        :param authorization_type: A granular control type for authorization levels. Valid value is "AUTHORIZATION_TYPE_TRUST". Possible values: ["AUTHORIZATION_TYPE_TRUST"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#authorization_type AccessContextManagerAuthorizedOrgsDesc#authorization_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#id AccessContextManagerAuthorizedOrgsDesc#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param orgs: The list of organization ids in this AuthorizedOrgsDesc. Format: 'organizations/<org_number>' Example: 'organizations/123456'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#orgs AccessContextManagerAuthorizedOrgsDesc#orgs}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#timeouts AccessContextManagerAuthorizedOrgsDesc#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a569035c24ca11d59143abfc60cc05ac4b6c62a7fed8fe9013113da07e2aafe9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessContextManagerAuthorizedOrgsDescConfig(
            name=name,
            parent=parent,
            asset_type=asset_type,
            authorization_direction=authorization_direction,
            authorization_type=authorization_type,
            id=id,
            orgs=orgs,
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
        '''Generates CDKTF code for importing a AccessContextManagerAuthorizedOrgsDesc resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AccessContextManagerAuthorizedOrgsDesc to import.
        :param import_from_id: The id of the existing AccessContextManagerAuthorizedOrgsDesc that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AccessContextManagerAuthorizedOrgsDesc to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3504422642e5782c37e876da83cba122e68fdc7b7b3e1df22f216d192f631182)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#create AccessContextManagerAuthorizedOrgsDesc#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#delete AccessContextManagerAuthorizedOrgsDesc#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#update AccessContextManagerAuthorizedOrgsDesc#update}.
        '''
        value = AccessContextManagerAuthorizedOrgsDescTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAssetType")
    def reset_asset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssetType", []))

    @jsii.member(jsii_name="resetAuthorizationDirection")
    def reset_authorization_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizationDirection", []))

    @jsii.member(jsii_name="resetAuthorizationType")
    def reset_authorization_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizationType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOrgs")
    def reset_orgs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgs", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "AccessContextManagerAuthorizedOrgsDescTimeoutsOutputReference":
        return typing.cast("AccessContextManagerAuthorizedOrgsDescTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="assetTypeInput")
    def asset_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assetTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationDirectionInput")
    def authorization_direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationDirectionInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationTypeInput")
    def authorization_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orgsInput")
    def orgs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "orgsInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessContextManagerAuthorizedOrgsDescTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessContextManagerAuthorizedOrgsDescTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="assetType")
    def asset_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assetType"))

    @asset_type.setter
    def asset_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1871ddbf8b7e1e54558c40d7ff7631179662e68bc17a82e9f8f092a4072b3a56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authorizationDirection")
    def authorization_direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationDirection"))

    @authorization_direction.setter
    def authorization_direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1790c728edab5ddab4037fd4e31592431b38f4d028e08e9c07251c63e491acf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationDirection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authorizationType")
    def authorization_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationType"))

    @authorization_type.setter
    def authorization_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ed9cfd543a37b1605200aa8aa05ee7896b3a8c2c77c302c78261a9ff213023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034bbe8a42234169bf6bffbe23a9b913d420c155f2d3abe25175153c0fdc7f89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf0c9bb1d52c9351b352aeda1e079ea0eea2bb61d476d290551e8440ad906dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgs")
    def orgs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "orgs"))

    @orgs.setter
    def orgs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8173563f3faef9fb291a2c2bf3cc2fdec8a5b23b1f7a530dffc831207583c93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198268f17cb779d2132235aeca41a88fd74f50d9ea2695c8d71f670a53650fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAuthorizedOrgsDesc.AccessContextManagerAuthorizedOrgsDescConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "parent": "parent",
        "asset_type": "assetType",
        "authorization_direction": "authorizationDirection",
        "authorization_type": "authorizationType",
        "id": "id",
        "orgs": "orgs",
        "timeouts": "timeouts",
    },
)
class AccessContextManagerAuthorizedOrgsDescConfig(
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
        name: builtins.str,
        parent: builtins.str,
        asset_type: typing.Optional[builtins.str] = None,
        authorization_direction: typing.Optional[builtins.str] = None,
        authorization_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        orgs: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerAuthorizedOrgsDescTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Resource name for the 'AuthorizedOrgsDesc'. Format: 'accessPolicies/{access_policy}/authorizedOrgsDescs/{authorized_orgs_desc}'. The 'authorized_orgs_desc' component must begin with a letter, followed by alphanumeric characters or '_'. After you create an 'AuthorizedOrgsDesc', you cannot change its 'name'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#name AccessContextManagerAuthorizedOrgsDesc#name}
        :param parent: Required. Resource name for the access policy which owns this 'AuthorizedOrgsDesc'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#parent AccessContextManagerAuthorizedOrgsDesc#parent}
        :param asset_type: The type of entities that need to use the authorization relationship during evaluation, such as a device. Valid values are "ASSET_TYPE_DEVICE" and "ASSET_TYPE_CREDENTIAL_STRENGTH". Possible values: ["ASSET_TYPE_DEVICE", "ASSET_TYPE_CREDENTIAL_STRENGTH"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#asset_type AccessContextManagerAuthorizedOrgsDesc#asset_type}
        :param authorization_direction: The direction of the authorization relationship between this organization and the organizations listed in the "orgs" field. The valid values for this field include the following: AUTHORIZATION_DIRECTION_FROM: Allows this organization to evaluate traffic in the organizations listed in the 'orgs' field. AUTHORIZATION_DIRECTION_TO: Allows the organizations listed in the 'orgs' field to evaluate the traffic in this organization. For the authorization relationship to take effect, all of the organizations must authorize and specify the appropriate relationship direction. For example, if organization A authorized organization B and C to evaluate its traffic, by specifying "AUTHORIZATION_DIRECTION_TO" as the authorization direction, organizations B and C must specify "AUTHORIZATION_DIRECTION_FROM" as the authorization direction in their "AuthorizedOrgsDesc" resource. Possible values: ["AUTHORIZATION_DIRECTION_TO", "AUTHORIZATION_DIRECTION_FROM"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#authorization_direction AccessContextManagerAuthorizedOrgsDesc#authorization_direction}
        :param authorization_type: A granular control type for authorization levels. Valid value is "AUTHORIZATION_TYPE_TRUST". Possible values: ["AUTHORIZATION_TYPE_TRUST"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#authorization_type AccessContextManagerAuthorizedOrgsDesc#authorization_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#id AccessContextManagerAuthorizedOrgsDesc#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param orgs: The list of organization ids in this AuthorizedOrgsDesc. Format: 'organizations/<org_number>' Example: 'organizations/123456'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#orgs AccessContextManagerAuthorizedOrgsDesc#orgs}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#timeouts AccessContextManagerAuthorizedOrgsDesc#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = AccessContextManagerAuthorizedOrgsDescTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4699621d622e0cc1caccd07d92439276287ca4db01d54df32b4ff9b90e7c73e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument asset_type", value=asset_type, expected_type=type_hints["asset_type"])
            check_type(argname="argument authorization_direction", value=authorization_direction, expected_type=type_hints["authorization_direction"])
            check_type(argname="argument authorization_type", value=authorization_type, expected_type=type_hints["authorization_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument orgs", value=orgs, expected_type=type_hints["orgs"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "parent": parent,
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
        if asset_type is not None:
            self._values["asset_type"] = asset_type
        if authorization_direction is not None:
            self._values["authorization_direction"] = authorization_direction
        if authorization_type is not None:
            self._values["authorization_type"] = authorization_type
        if id is not None:
            self._values["id"] = id
        if orgs is not None:
            self._values["orgs"] = orgs
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
    def name(self) -> builtins.str:
        '''Resource name for the 'AuthorizedOrgsDesc'.

        Format:
        'accessPolicies/{access_policy}/authorizedOrgsDescs/{authorized_orgs_desc}'.
        The 'authorized_orgs_desc' component must begin with a letter, followed by
        alphanumeric characters or '_'.
        After you create an 'AuthorizedOrgsDesc', you cannot change its 'name'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#name AccessContextManagerAuthorizedOrgsDesc#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''Required. Resource name for the access policy which owns this 'AuthorizedOrgsDesc'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#parent AccessContextManagerAuthorizedOrgsDesc#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_type(self) -> typing.Optional[builtins.str]:
        '''The type of entities that need to use the authorization relationship during evaluation, such as a device.

        Valid values are "ASSET_TYPE_DEVICE" and
        "ASSET_TYPE_CREDENTIAL_STRENGTH". Possible values: ["ASSET_TYPE_DEVICE", "ASSET_TYPE_CREDENTIAL_STRENGTH"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#asset_type AccessContextManagerAuthorizedOrgsDesc#asset_type}
        '''
        result = self._values.get("asset_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorization_direction(self) -> typing.Optional[builtins.str]:
        '''The direction of the authorization relationship between this organization and the organizations listed in the "orgs" field.

        The valid values for this
        field include the following:

        AUTHORIZATION_DIRECTION_FROM: Allows this organization to evaluate traffic
        in the organizations listed in the 'orgs' field.

        AUTHORIZATION_DIRECTION_TO: Allows the organizations listed in the 'orgs'
        field to evaluate the traffic in this organization.

        For the authorization relationship to take effect, all of the organizations
        must authorize and specify the appropriate relationship direction. For
        example, if organization A authorized organization B and C to evaluate its
        traffic, by specifying "AUTHORIZATION_DIRECTION_TO" as the authorization
        direction, organizations B and C must specify
        "AUTHORIZATION_DIRECTION_FROM" as the authorization direction in their
        "AuthorizedOrgsDesc" resource. Possible values: ["AUTHORIZATION_DIRECTION_TO", "AUTHORIZATION_DIRECTION_FROM"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#authorization_direction AccessContextManagerAuthorizedOrgsDesc#authorization_direction}
        '''
        result = self._values.get("authorization_direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorization_type(self) -> typing.Optional[builtins.str]:
        '''A granular control type for authorization levels. Valid value is "AUTHORIZATION_TYPE_TRUST". Possible values: ["AUTHORIZATION_TYPE_TRUST"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#authorization_type AccessContextManagerAuthorizedOrgsDesc#authorization_type}
        '''
        result = self._values.get("authorization_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#id AccessContextManagerAuthorizedOrgsDesc#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def orgs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of organization ids in this AuthorizedOrgsDesc. Format: 'organizations/<org_number>' Example: 'organizations/123456'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#orgs AccessContextManagerAuthorizedOrgsDesc#orgs}
        '''
        result = self._values.get("orgs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["AccessContextManagerAuthorizedOrgsDescTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#timeouts AccessContextManagerAuthorizedOrgsDesc#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AccessContextManagerAuthorizedOrgsDescTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAuthorizedOrgsDescConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAuthorizedOrgsDesc.AccessContextManagerAuthorizedOrgsDescTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class AccessContextManagerAuthorizedOrgsDescTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#create AccessContextManagerAuthorizedOrgsDesc#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#delete AccessContextManagerAuthorizedOrgsDesc#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#update AccessContextManagerAuthorizedOrgsDesc#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f43f64c08c7000e84a077f8bd29833740f18e836ad1d1f986636655712cc037d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#create AccessContextManagerAuthorizedOrgsDesc#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#delete AccessContextManagerAuthorizedOrgsDesc#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_authorized_orgs_desc#update AccessContextManagerAuthorizedOrgsDesc#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAuthorizedOrgsDescTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerAuthorizedOrgsDescTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAuthorizedOrgsDesc.AccessContextManagerAuthorizedOrgsDescTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1495895b82239c25c585d2fcb185761ac15fc2729022d6e808a7158cd3f00394)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b59b2391cbe8853651255f8bb21176c90098ded6a0e6c8750d7f83c103dbc7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff16b03d4b389bbcacc1bff6950a519a3cba9225660b6ebfdb6ee8c228b3cd28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ef68bca7efe132798dd99891bd2a94dbe60135c568f7adf62faa3f505269d9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAuthorizedOrgsDescTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAuthorizedOrgsDescTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAuthorizedOrgsDescTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c776a7cf55bf731108f2880536ce0306198df8ce3dda9be11ccc149c12b5033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AccessContextManagerAuthorizedOrgsDesc",
    "AccessContextManagerAuthorizedOrgsDescConfig",
    "AccessContextManagerAuthorizedOrgsDescTimeouts",
    "AccessContextManagerAuthorizedOrgsDescTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a569035c24ca11d59143abfc60cc05ac4b6c62a7fed8fe9013113da07e2aafe9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    parent: builtins.str,
    asset_type: typing.Optional[builtins.str] = None,
    authorization_direction: typing.Optional[builtins.str] = None,
    authorization_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    orgs: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerAuthorizedOrgsDescTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3504422642e5782c37e876da83cba122e68fdc7b7b3e1df22f216d192f631182(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1871ddbf8b7e1e54558c40d7ff7631179662e68bc17a82e9f8f092a4072b3a56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1790c728edab5ddab4037fd4e31592431b38f4d028e08e9c07251c63e491acf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ed9cfd543a37b1605200aa8aa05ee7896b3a8c2c77c302c78261a9ff213023(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034bbe8a42234169bf6bffbe23a9b913d420c155f2d3abe25175153c0fdc7f89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf0c9bb1d52c9351b352aeda1e079ea0eea2bb61d476d290551e8440ad906dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8173563f3faef9fb291a2c2bf3cc2fdec8a5b23b1f7a530dffc831207583c93(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198268f17cb779d2132235aeca41a88fd74f50d9ea2695c8d71f670a53650fe3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4699621d622e0cc1caccd07d92439276287ca4db01d54df32b4ff9b90e7c73e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    parent: builtins.str,
    asset_type: typing.Optional[builtins.str] = None,
    authorization_direction: typing.Optional[builtins.str] = None,
    authorization_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    orgs: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerAuthorizedOrgsDescTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f43f64c08c7000e84a077f8bd29833740f18e836ad1d1f986636655712cc037d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1495895b82239c25c585d2fcb185761ac15fc2729022d6e808a7158cd3f00394(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b59b2391cbe8853651255f8bb21176c90098ded6a0e6c8750d7f83c103dbc7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff16b03d4b389bbcacc1bff6950a519a3cba9225660b6ebfdb6ee8c228b3cd28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef68bca7efe132798dd99891bd2a94dbe60135c568f7adf62faa3f505269d9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c776a7cf55bf731108f2880536ce0306198df8ce3dda9be11ccc149c12b5033(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerAuthorizedOrgsDescTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

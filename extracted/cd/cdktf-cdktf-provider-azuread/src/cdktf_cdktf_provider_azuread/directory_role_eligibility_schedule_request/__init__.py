r'''
# `azuread_directory_role_eligibility_schedule_request`

Refer to the Terraform Registry for docs: [`azuread_directory_role_eligibility_schedule_request`](https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request).
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


class DirectoryRoleEligibilityScheduleRequest(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.directoryRoleEligibilityScheduleRequest.DirectoryRoleEligibilityScheduleRequest",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request azuread_directory_role_eligibility_schedule_request}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        directory_scope_id: builtins.str,
        justification: builtins.str,
        principal_id: builtins.str,
        role_definition_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DirectoryRoleEligibilityScheduleRequestTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request azuread_directory_role_eligibility_schedule_request} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param directory_scope_id: Identifier of the directory object representing the scope of the role eligibility schedule request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#directory_scope_id DirectoryRoleEligibilityScheduleRequest#directory_scope_id}
        :param justification: Justification for why the role is assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#justification DirectoryRoleEligibilityScheduleRequest#justification}
        :param principal_id: The object ID of the member principal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#principal_id DirectoryRoleEligibilityScheduleRequest#principal_id}
        :param role_definition_id: The object ID of the directory role for this role eligibility schedule request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#role_definition_id DirectoryRoleEligibilityScheduleRequest#role_definition_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#id DirectoryRoleEligibilityScheduleRequest#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#timeouts DirectoryRoleEligibilityScheduleRequest#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e14bccd2b2e81bf3b1dc3217f43e60c65195ee6394f17b9250bde030b4b6bde9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DirectoryRoleEligibilityScheduleRequestConfig(
            directory_scope_id=directory_scope_id,
            justification=justification,
            principal_id=principal_id,
            role_definition_id=role_definition_id,
            id=id,
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
        '''Generates CDKTF code for importing a DirectoryRoleEligibilityScheduleRequest resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DirectoryRoleEligibilityScheduleRequest to import.
        :param import_from_id: The id of the existing DirectoryRoleEligibilityScheduleRequest that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DirectoryRoleEligibilityScheduleRequest to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__162a7098edf40bffd8ca7bb40917f8986b552c2e1b85a73ac76f5b9349c9c7b4)
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
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#create DirectoryRoleEligibilityScheduleRequest#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#delete DirectoryRoleEligibilityScheduleRequest#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#read DirectoryRoleEligibilityScheduleRequest#read}.
        '''
        value = DirectoryRoleEligibilityScheduleRequestTimeouts(
            create=create, delete=delete, read=read
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "DirectoryRoleEligibilityScheduleRequestTimeoutsOutputReference":
        return typing.cast("DirectoryRoleEligibilityScheduleRequestTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="directoryScopeIdInput")
    def directory_scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryScopeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="justificationInput")
    def justification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "justificationInput"))

    @builtins.property
    @jsii.member(jsii_name="principalIdInput")
    def principal_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalIdInput"))

    @builtins.property
    @jsii.member(jsii_name="roleDefinitionIdInput")
    def role_definition_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleDefinitionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DirectoryRoleEligibilityScheduleRequestTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DirectoryRoleEligibilityScheduleRequestTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="directoryScopeId")
    def directory_scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directoryScopeId"))

    @directory_scope_id.setter
    def directory_scope_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c21d29f6397b903abaf484a113b269bbed3855904f56125cb90fd6068f249b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryScopeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__491fbbd37fcabc32e54ad98c2225594c72e8f64613149bb170e38d5f70d56c08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="justification")
    def justification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "justification"))

    @justification.setter
    def justification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f422ceaa8c1cde74b75d1763f30f10f9e7b9676d18fbca8c344d9ad300df51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "justification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @principal_id.setter
    def principal_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce142f5620d7bc8c1c0a4dc933780c042dbc4df9bc02362b74764f673937c54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principalId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleDefinitionId")
    def role_definition_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleDefinitionId"))

    @role_definition_id.setter
    def role_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57cc820150f4056da63df63bab31b7d12d5b20d6ea8f29861e88f3334b1c3e10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleDefinitionId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.directoryRoleEligibilityScheduleRequest.DirectoryRoleEligibilityScheduleRequestConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "directory_scope_id": "directoryScopeId",
        "justification": "justification",
        "principal_id": "principalId",
        "role_definition_id": "roleDefinitionId",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class DirectoryRoleEligibilityScheduleRequestConfig(
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
        directory_scope_id: builtins.str,
        justification: builtins.str,
        principal_id: builtins.str,
        role_definition_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DirectoryRoleEligibilityScheduleRequestTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param directory_scope_id: Identifier of the directory object representing the scope of the role eligibility schedule request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#directory_scope_id DirectoryRoleEligibilityScheduleRequest#directory_scope_id}
        :param justification: Justification for why the role is assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#justification DirectoryRoleEligibilityScheduleRequest#justification}
        :param principal_id: The object ID of the member principal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#principal_id DirectoryRoleEligibilityScheduleRequest#principal_id}
        :param role_definition_id: The object ID of the directory role for this role eligibility schedule request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#role_definition_id DirectoryRoleEligibilityScheduleRequest#role_definition_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#id DirectoryRoleEligibilityScheduleRequest#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#timeouts DirectoryRoleEligibilityScheduleRequest#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DirectoryRoleEligibilityScheduleRequestTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed7048b7fd09bd946c08e9b142d394dbca2f505c8c63afbb88a2b5fbb1265b7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument directory_scope_id", value=directory_scope_id, expected_type=type_hints["directory_scope_id"])
            check_type(argname="argument justification", value=justification, expected_type=type_hints["justification"])
            check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
            check_type(argname="argument role_definition_id", value=role_definition_id, expected_type=type_hints["role_definition_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "directory_scope_id": directory_scope_id,
            "justification": justification,
            "principal_id": principal_id,
            "role_definition_id": role_definition_id,
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
    def directory_scope_id(self) -> builtins.str:
        '''Identifier of the directory object representing the scope of the role eligibility schedule request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#directory_scope_id DirectoryRoleEligibilityScheduleRequest#directory_scope_id}
        '''
        result = self._values.get("directory_scope_id")
        assert result is not None, "Required property 'directory_scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def justification(self) -> builtins.str:
        '''Justification for why the role is assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#justification DirectoryRoleEligibilityScheduleRequest#justification}
        '''
        result = self._values.get("justification")
        assert result is not None, "Required property 'justification' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def principal_id(self) -> builtins.str:
        '''The object ID of the member principal.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#principal_id DirectoryRoleEligibilityScheduleRequest#principal_id}
        '''
        result = self._values.get("principal_id")
        assert result is not None, "Required property 'principal_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_definition_id(self) -> builtins.str:
        '''The object ID of the directory role for this role eligibility schedule request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#role_definition_id DirectoryRoleEligibilityScheduleRequest#role_definition_id}
        '''
        result = self._values.get("role_definition_id")
        assert result is not None, "Required property 'role_definition_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#id DirectoryRoleEligibilityScheduleRequest#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DirectoryRoleEligibilityScheduleRequestTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#timeouts DirectoryRoleEligibilityScheduleRequest#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DirectoryRoleEligibilityScheduleRequestTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DirectoryRoleEligibilityScheduleRequestConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.directoryRoleEligibilityScheduleRequest.DirectoryRoleEligibilityScheduleRequestTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class DirectoryRoleEligibilityScheduleRequestTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#create DirectoryRoleEligibilityScheduleRequest#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#delete DirectoryRoleEligibilityScheduleRequest#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#read DirectoryRoleEligibilityScheduleRequest#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394357d980d1a0136df5d54936c5263a9bdf4c9266f443b0085af3f3dd42eac0)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#create DirectoryRoleEligibilityScheduleRequest#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#delete DirectoryRoleEligibilityScheduleRequest#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/directory_role_eligibility_schedule_request#read DirectoryRoleEligibilityScheduleRequest#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DirectoryRoleEligibilityScheduleRequestTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DirectoryRoleEligibilityScheduleRequestTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.directoryRoleEligibilityScheduleRequest.DirectoryRoleEligibilityScheduleRequestTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f026ce34062056f7ed3c71943cf34b2ad00d4ad27b0ca090ef34b097fcc69487)
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
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff7e50c1f3ac1236105663ad24696acb6aced9ed617f474d4462478296aeff67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74fc20582cf7f969d3171b05cd146b0c4162e59c0f164d41ea13771a6805fc8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff1fe00b4c7463488ab8807ca50ff4f5535113d9faed1ca0bb6146819d8e0d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DirectoryRoleEligibilityScheduleRequestTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DirectoryRoleEligibilityScheduleRequestTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DirectoryRoleEligibilityScheduleRequestTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc2de96e59f016070807b525c8c664e20431465faccd18fd601803fe37565681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DirectoryRoleEligibilityScheduleRequest",
    "DirectoryRoleEligibilityScheduleRequestConfig",
    "DirectoryRoleEligibilityScheduleRequestTimeouts",
    "DirectoryRoleEligibilityScheduleRequestTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e14bccd2b2e81bf3b1dc3217f43e60c65195ee6394f17b9250bde030b4b6bde9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    directory_scope_id: builtins.str,
    justification: builtins.str,
    principal_id: builtins.str,
    role_definition_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DirectoryRoleEligibilityScheduleRequestTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__162a7098edf40bffd8ca7bb40917f8986b552c2e1b85a73ac76f5b9349c9c7b4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c21d29f6397b903abaf484a113b269bbed3855904f56125cb90fd6068f249b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491fbbd37fcabc32e54ad98c2225594c72e8f64613149bb170e38d5f70d56c08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f422ceaa8c1cde74b75d1763f30f10f9e7b9676d18fbca8c344d9ad300df51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce142f5620d7bc8c1c0a4dc933780c042dbc4df9bc02362b74764f673937c54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57cc820150f4056da63df63bab31b7d12d5b20d6ea8f29861e88f3334b1c3e10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed7048b7fd09bd946c08e9b142d394dbca2f505c8c63afbb88a2b5fbb1265b7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    directory_scope_id: builtins.str,
    justification: builtins.str,
    principal_id: builtins.str,
    role_definition_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DirectoryRoleEligibilityScheduleRequestTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394357d980d1a0136df5d54936c5263a9bdf4c9266f443b0085af3f3dd42eac0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f026ce34062056f7ed3c71943cf34b2ad00d4ad27b0ca090ef34b097fcc69487(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7e50c1f3ac1236105663ad24696acb6aced9ed617f474d4462478296aeff67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fc20582cf7f969d3171b05cd146b0c4162e59c0f164d41ea13771a6805fc8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1fe00b4c7463488ab8807ca50ff4f5535113d9faed1ca0bb6146819d8e0d6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2de96e59f016070807b525c8c664e20431465faccd18fd601803fe37565681(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DirectoryRoleEligibilityScheduleRequestTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

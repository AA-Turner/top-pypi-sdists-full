r'''
# `data_google_privileged_access_manager_entitlement`

Refer to the Terraform Registry for docs: [`data_google_privileged_access_manager_entitlement`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement).
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


class DataGooglePrivilegedAccessManagerEntitlement(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlement",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement google_privileged_access_manager_entitlement}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        entitlement_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement google_privileged_access_manager_entitlement} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param entitlement_id: The ID to use for this Entitlement. This will become the last part of the resource name. This value should be 4-63 characters, and valid characters are "[a-z]", "[0-9]", and "-". The first character should be from [a-z]. This value should be unique among all other Entitlements under the specified 'parent'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement#entitlement_id DataGooglePrivilegedAccessManagerEntitlement#entitlement_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement#id DataGooglePrivilegedAccessManagerEntitlement#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The region of the Entitlement resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement#location DataGooglePrivilegedAccessManagerEntitlement#location}
        :param parent: Format: projects/{project-id|project-number} or organizations/{organization-number} or folders/{folder-number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement#parent DataGooglePrivilegedAccessManagerEntitlement#parent}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ed0cc5e4bde137a83ca41abc264c8a72911f5f76efccb540f6959121f496ba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataGooglePrivilegedAccessManagerEntitlementConfig(
            entitlement_id=entitlement_id,
            id=id,
            location=location,
            parent=parent,
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
        '''Generates CDKTF code for importing a DataGooglePrivilegedAccessManagerEntitlement resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataGooglePrivilegedAccessManagerEntitlement to import.
        :param import_from_id: The id of the existing DataGooglePrivilegedAccessManagerEntitlement that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataGooglePrivilegedAccessManagerEntitlement to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c08873871e78d8871af0cbd6f0366ce9cce4e879732ab8298a17c6ab8a478310)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetEntitlementId")
    def reset_entitlement_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntitlementId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetParent")
    def reset_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParent", []))

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
    @jsii.member(jsii_name="additionalNotificationTargets")
    def additional_notification_targets(
        self,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargetsList":
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargetsList", jsii.get(self, "additionalNotificationTargets"))

    @builtins.property
    @jsii.member(jsii_name="approvalWorkflow")
    def approval_workflow(
        self,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowList":
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowList", jsii.get(self, "approvalWorkflow"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="eligibleUsers")
    def eligible_users(
        self,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementEligibleUsersList":
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementEligibleUsersList", jsii.get(self, "eligibleUsers"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="maxRequestDuration")
    def max_request_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxRequestDuration"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="privilegedAccess")
    def privileged_access(
        self,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessList":
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessList", jsii.get(self, "privilegedAccess"))

    @builtins.property
    @jsii.member(jsii_name="requesterJustificationConfig")
    def requester_justification_config(
        self,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigList":
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigList", jsii.get(self, "requesterJustificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="entitlementIdInput")
    def entitlement_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entitlementIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="entitlementId")
    def entitlement_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entitlementId"))

    @entitlement_id.setter
    def entitlement_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb23b0eacf2d654b8c819426e70d29b663b101b71149e3d87d08184ded5ff3f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entitlementId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b4aebb0eeed77e204a9816f94d7fab1c5b4b174daec7f8c19b282f1433526e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1354de511b56a81334d8ceb3983f5a6cc587ce817e72d4626b23d6b389795a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3be8cf52891b286e1f7dce74da624d37dfc4832a0b35834584d4b51bf4111e0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__941c8ff1c3bb180062d86511e418be544825e2f8937e0d01f2a482524e34ad64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3776ec3b3bdd969734f49f38dd5d7398a80770020fe5b814b8053b14664f96e1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43828d83e28b66f0501a4b5974d576649b6273e70859e5da102e98149d233ca6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02bdcfa330e84b235d60a12e8ddedc30a8481c5ef312d86bf5f91bdcf83c1d2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0e8aa5038d852b28b46a2d05fc533a5cdb19da0b62f9541c1f63a179c6c0978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7641d48e40b45a85509a8f0d95772af27c1154adf800e3442240e13892d462f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="adminEmailRecipients")
    def admin_email_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "adminEmailRecipients"))

    @builtins.property
    @jsii.member(jsii_name="requesterEmailRecipients")
    def requester_email_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requesterEmailRecipients"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets]:
        return typing.cast(typing.Optional[DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd2268d31c5a84dd2fec3e49d97a8722cc0e50fc71645bdc0efd42c3f0303e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflow",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflow:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__802c44f7e672d947c3ca465f9dd1a3ae33de30e8d84411cbd4b47812ee98bb32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2a94b350d1fba7bf231086cfbba291411ed25507b8c00b914ee4acab9f821d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68f29fe0d5c5312f8a9b485a269f02b3fabab5f1883a19dd8a35f68eda44a70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4971ab80cd31c516d74dc60ddc01918ff767d39be075b4ec9bc062d3cc10b250)
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
            type_hints = typing.get_type_hints(_typecheckingstub__029833f8df4c0ea30e100e95f4a7cabbb4dfd9b20f8a39bd7337cbb5c185da46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46be2034e47cf95805f5b6c286b07d021f905af544c7dd096f162d8723d450bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf305660ba62fe281595e1f8f7613cd48b0080b11d7a05bf29149af48fb558e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3954e3ff265d0f0a95e7ea4be18c169c413019a4e7cd017ca1edac75cba34d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b75f6b4a4f5ef3242baf5f7809e1745c3d2cec23dc5e6175737dceb511fe7973)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac3fe12a9313192ce2676733d03b32a759ffc7e19a012e732f75395826d962e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f4da97414b80e53936663470af48bfdc39f19ce017fbef8d8bcb604f3cd286f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="requireApproverJustification")
    def require_approver_justification(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "requireApproverJustification"))

    @builtins.property
    @jsii.member(jsii_name="steps")
    def steps(
        self,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsList":
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsList", jsii.get(self, "steps"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals]:
        return typing.cast(typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0048cf3f6fdfd91861c41a1c7e803bf4fb8e900178541283170684e66adfd959)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__005d61e0a830ad1c3701d24dc73ca36dd16d8afcd6fd2cf7fb3e0482083d8a9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f0b9a06f978b422201b1150e93b6c8833f453c998a523fbc621e0f4535da122)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c9962130f6b217cd4ab962778cbffce21d7042a1dc397b793ececc78dcbd7f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b313d2cb4829b8adac648a5d16cc14ab2eb6bfcbea7550835ee06cb12849cdde)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3656d0d3dfda6aa4060d1f86e8bfe84bc70be7568630c9bf0fc857804026125e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae4ee18d5c4143b846b0a11cfbb6b820a5690f11ff3935c584394a1c005d7e17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "principals"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers]:
        return typing.cast(typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce803a03a23e918fde43f0242097995040a47155636549fbd2bb5f8522a28d7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f248de9a09153f49a910d6bb50e943e1dd231744a4230bc51d4e12bc30e2e378)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce3b6ae2de6a5fe9aa86ab792149a5c3809299cf15f3b4a3d880533803370d5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc87775c76aa26a8cea7b6765278c1e2a5826d9e298e1e15ed5338a65be39ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__497e9a3f7840a26d3e47c8931e9af558e759be3ae9449ee38122e88bb9f423fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9043f1939b82846a23e563dd294a3b14d484ff2f2f6e178180627cfc08626ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b51d9a1cc6ddadf23f8a047430b59a5d68e6f31a58925e15c53de24a04711826)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="approvalsNeeded")
    def approvals_needed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "approvalsNeeded"))

    @builtins.property
    @jsii.member(jsii_name="approverEmailRecipients")
    def approver_email_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "approverEmailRecipients"))

    @builtins.property
    @jsii.member(jsii_name="approvers")
    def approvers(
        self,
    ) -> DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversList:
        return typing.cast(DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversList, jsii.get(self, "approvers"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]:
        return typing.cast(typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e706086e6a94231d11cd9dbe1f402d781507ea6ef46aef445b46114932341ee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ef9a90c0b8b07ab7b7bede09d8bd792eba5d07c032af6cb92fd14156610b9ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="manualApprovals")
    def manual_approvals(
        self,
    ) -> DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsList:
        return typing.cast(DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsList, jsii.get(self, "manualApprovals"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflow]:
        return typing.cast(typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__945e8e4afbb5645d9cd84da4a8a334e5e10f8fb627619641839722e8afc09d5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "entitlement_id": "entitlementId",
        "id": "id",
        "location": "location",
        "parent": "parent",
    },
)
class DataGooglePrivilegedAccessManagerEntitlementConfig(
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
        entitlement_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param entitlement_id: The ID to use for this Entitlement. This will become the last part of the resource name. This value should be 4-63 characters, and valid characters are "[a-z]", "[0-9]", and "-". The first character should be from [a-z]. This value should be unique among all other Entitlements under the specified 'parent'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement#entitlement_id DataGooglePrivilegedAccessManagerEntitlement#entitlement_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement#id DataGooglePrivilegedAccessManagerEntitlement#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The region of the Entitlement resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement#location DataGooglePrivilegedAccessManagerEntitlement#location}
        :param parent: Format: projects/{project-id|project-number} or organizations/{organization-number} or folders/{folder-number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement#parent DataGooglePrivilegedAccessManagerEntitlement#parent}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb3074812f13b66471ac99534631dac6b21a1fe5b0d594746933c532f01d330b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument entitlement_id", value=entitlement_id, expected_type=type_hints["entitlement_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if entitlement_id is not None:
            self._values["entitlement_id"] = entitlement_id
        if id is not None:
            self._values["id"] = id
        if location is not None:
            self._values["location"] = location
        if parent is not None:
            self._values["parent"] = parent

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
    def entitlement_id(self) -> typing.Optional[builtins.str]:
        '''The ID to use for this Entitlement.

        This will become the last part of the resource name.
        This value should be 4-63 characters, and valid characters are "[a-z]", "[0-9]", and "-". The first character should be from [a-z].
        This value should be unique among all other Entitlements under the specified 'parent'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement#entitlement_id DataGooglePrivilegedAccessManagerEntitlement#entitlement_id}
        '''
        result = self._values.get("entitlement_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement#id DataGooglePrivilegedAccessManagerEntitlement#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The region of the Entitlement resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement#location DataGooglePrivilegedAccessManagerEntitlement#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''Format: projects/{project-id|project-number} or organizations/{organization-number} or folders/{folder-number}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/privileged_access_manager_entitlement#parent DataGooglePrivilegedAccessManagerEntitlement#parent}
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGooglePrivilegedAccessManagerEntitlementConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementEligibleUsers",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGooglePrivilegedAccessManagerEntitlementEligibleUsers:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGooglePrivilegedAccessManagerEntitlementEligibleUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGooglePrivilegedAccessManagerEntitlementEligibleUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementEligibleUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f553619351fc7c3494972a2d0de6aea311ba46b90f7f4c9329be37b5c7ec71b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementEligibleUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a68bfc18aef3c6f4543530125fb2abd0f548b2517d659a7ce2033ddda72bef11)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementEligibleUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae696c3f7ac5ca6d8f33a5705d5616f4f323e4b9e41e0c366fdcaaaa74b8f6a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8248416cbc3b1092517f993633c03a8b0177831cc97eff44a429a420e6a6db6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aec0ecbd6234445194ebe4d845585b4b4d9bac659f12b0be31362949ad3f3405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGooglePrivilegedAccessManagerEntitlementEligibleUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementEligibleUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__016b204ec50609c48eb8678de1c7a8ff66262e8dc7c43ac2db2b74f5cbcd9fe2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "principals"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGooglePrivilegedAccessManagerEntitlementEligibleUsers]:
        return typing.cast(typing.Optional[DataGooglePrivilegedAccessManagerEntitlementEligibleUsers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementEligibleUsers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f95575dd9d167bf2133eae882eb1a92d7dde31ba2897daec4b2631849392e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccess",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccess:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb50742e9536cb687c5f815a4f81fc8284a67e15e66f73723be5c67835e45554)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2de8e30ae6aa1913c3149f1ebab46f93ea7b1d2bd4522087192294330056cb7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__469f1ae75942e88e30d9d36c779d3d087f7aed03d5e35fc26f832fbd2feccc42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8bf8d04951b87d8de8a093e1d2f8cdf2627a466753a71d39d039b5666cef21b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__788e105e4220719ea0a78fea92c51581a0bea00aac76688e90d06beac539aaea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d59ab6b7818e114057e743559641f301458b9ab71304be82f4cea882b45d986)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @builtins.property
    @jsii.member(jsii_name="roleBindings")
    def role_bindings(
        self,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsList":
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsList", jsii.get(self, "roleBindings"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess]:
        return typing.cast(typing.Optional[DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43406ee48883c307cb5d42c07a2d5489a20919bdd7da5c4d8c0a34cc88866aed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__744c90e40b1c3327a3940090558e6231639716d4b13608f1e8dffe6534db8e64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e27a7831a3fa735ea54f9857631e71168ad200fb12c01d8dd997e217bb003c1e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f828a41aac91af194078983f02943d8d667c7767f88089763875f9493bf38f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80fe40e7d2aa60dd834792a30c1cafe7638e61aa49b81057289637a32b81c9b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__852d17734b0b5d611f7b20071f12ae3c98a805a6bbf4c41dcb66d69cae9d5c68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfef3c037c8f492d411b56c49cd68ee91d6fe2828dbb25c3dcae5e9f24814fc9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditionExpression")
    def condition_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conditionExpression"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]:
        return typing.cast(typing.Optional[DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9daa71be9905bb58eda6ea774adb68cca7e0c8208ad23921676a2b3f97ddfc84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b62e59b3b1ef531186c5be078d4c729e74093c68b243d34888a1bb0b6e6452d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeef9a8281c5dfde8a3ac8cdad7f94d4fa4d50ebf2a2e21d794116cd8a85c72b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f8f5721ad645107843b491cab56e86be2a6d5bc995325e9104b65e3dbaa380)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba7dfe48ecd40edbe39bea0396ed4ef8681a909ff26a9e35a7ca32d0c0454428)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0539c985349484127b4de26cbbe6b0d0003465e224b7bccd718a06660f8ea92d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2d5fc3bdd1991bba149517a04048666aaa49f3153c41339b938ae99ae0b6883)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="gcpIamAccess")
    def gcp_iam_access(
        self,
    ) -> DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessList:
        return typing.cast(DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessList, jsii.get(self, "gcpIamAccess"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccess]:
        return typing.cast(typing.Optional[DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da4fdebea978337f939d69948e633186fc88bafcfc978f66843b36c48822810e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a01321a7abedadae73b1bbf21cb7fc50abd0f30e871c027db45801b25f244ea1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f273bc0b870443659cb7f9b16f1fbde8439b2b20fadafd2b9df3cd10010f185)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4128a98a2c7816ba2118689d09b854b0926f0c99029464843ec9c18b2681671f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d894f380948be8dafe108e73db663791f07ba6eb0b583c86a25815c948595be6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce89da60c3d48dc813784727c4e6e1137bdd2692a3f454b970e9cd4740216b61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8465771ff0bcb49c23cf85e7faf0b429c150eb22663fb0eb0693dc1247d58e7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9592e1583df7f5d4087e3ff473e171b92db4a671d975f286411e9dbd49df467d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5792d5fbaab0a2315bfca77d55f1eccf12022e50267c5ad0e1da1f7af48b6e81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__346fef3e74f2beb0db0aaa48c64af0181fc77baeb943447bdb607b887a4f0931)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b67a9265daaa3f67cee67b211f9ffecb3bc1d365a265ce5260f6c47d642c69c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a65a1f9fd35299c0621d35a39d0372b68af4686a7e6660f549926a8ad1d997ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory]:
        return typing.cast(typing.Optional[DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58bd1d7207da5626c1fdd9ea80d21db70a6ecc647f357e23d914c2bae54848f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0e50d820c6df1be554ae08a6e7276222e46e3c081598e15c8da71c7f6650465)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="notMandatory")
    def not_mandatory(
        self,
    ) -> DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryList:
        return typing.cast(DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryList, jsii.get(self, "notMandatory"))

    @builtins.property
    @jsii.member(jsii_name="unstructured")
    def unstructured(
        self,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredList":
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredList", jsii.get(self, "unstructured"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig]:
        return typing.cast(typing.Optional[DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b871422578c326ec294dce829fd2cf0a2a68a8e140925b74ec25534475d2cf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6da9e6cd221405789035bb3cb11e2c5f0198acf02fac8b968204a47bfba70d53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8ecee121032e1eee524d53f38e7033e0f6cd7b0e962fc15ba1095ee8101fdbb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afbc5aedc66d6c972d1bbaaa12109416cec09f5ca348dea46a8c247fa519fa1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48ad93fc75db0bf10e14d25efc330f984af891e020d1645b546b08b4836e501c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71337f4ae9bb2b3df3fa1c75c3f4a59356a000547c8ddbe0b2cb45e8b9ce8d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGooglePrivilegedAccessManagerEntitlement.DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6aa1df2672b7d16ee522f249bace84e5158b99191ceaf4d9a1bc7c3b4d73ca07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured]:
        return typing.cast(typing.Optional[DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3249fcc8c46354587ccd111d41a3700bbe87a376d345f0bd114fcc1cff0501d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataGooglePrivilegedAccessManagerEntitlement",
    "DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets",
    "DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargetsList",
    "DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargetsOutputReference",
    "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflow",
    "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowList",
    "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals",
    "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsList",
    "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsOutputReference",
    "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps",
    "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers",
    "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversList",
    "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversOutputReference",
    "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsList",
    "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsOutputReference",
    "DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowOutputReference",
    "DataGooglePrivilegedAccessManagerEntitlementConfig",
    "DataGooglePrivilegedAccessManagerEntitlementEligibleUsers",
    "DataGooglePrivilegedAccessManagerEntitlementEligibleUsersList",
    "DataGooglePrivilegedAccessManagerEntitlementEligibleUsersOutputReference",
    "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccess",
    "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess",
    "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessList",
    "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessOutputReference",
    "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings",
    "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsList",
    "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsOutputReference",
    "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessList",
    "DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessOutputReference",
    "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig",
    "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigList",
    "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory",
    "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryList",
    "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryOutputReference",
    "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigOutputReference",
    "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured",
    "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredList",
    "DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredOutputReference",
]

publication.publish()

def _typecheckingstub__44ed0cc5e4bde137a83ca41abc264c8a72911f5f76efccb540f6959121f496ba(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    entitlement_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__c08873871e78d8871af0cbd6f0366ce9cce4e879732ab8298a17c6ab8a478310(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb23b0eacf2d654b8c819426e70d29b663b101b71149e3d87d08184ded5ff3f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4aebb0eeed77e204a9816f94d7fab1c5b4b174daec7f8c19b282f1433526e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1354de511b56a81334d8ceb3983f5a6cc587ce817e72d4626b23d6b389795a33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be8cf52891b286e1f7dce74da624d37dfc4832a0b35834584d4b51bf4111e0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941c8ff1c3bb180062d86511e418be544825e2f8937e0d01f2a482524e34ad64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3776ec3b3bdd969734f49f38dd5d7398a80770020fe5b814b8053b14664f96e1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43828d83e28b66f0501a4b5974d576649b6273e70859e5da102e98149d233ca6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02bdcfa330e84b235d60a12e8ddedc30a8481c5ef312d86bf5f91bdcf83c1d2d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e8aa5038d852b28b46a2d05fc533a5cdb19da0b62f9541c1f63a179c6c0978(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7641d48e40b45a85509a8f0d95772af27c1154adf800e3442240e13892d462f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd2268d31c5a84dd2fec3e49d97a8722cc0e50fc71645bdc0efd42c3f0303e9(
    value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802c44f7e672d947c3ca465f9dd1a3ae33de30e8d84411cbd4b47812ee98bb32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2a94b350d1fba7bf231086cfbba291411ed25507b8c00b914ee4acab9f821d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68f29fe0d5c5312f8a9b485a269f02b3fabab5f1883a19dd8a35f68eda44a70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4971ab80cd31c516d74dc60ddc01918ff767d39be075b4ec9bc062d3cc10b250(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029833f8df4c0ea30e100e95f4a7cabbb4dfd9b20f8a39bd7337cbb5c185da46(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46be2034e47cf95805f5b6c286b07d021f905af544c7dd096f162d8723d450bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf305660ba62fe281595e1f8f7613cd48b0080b11d7a05bf29149af48fb558e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3954e3ff265d0f0a95e7ea4be18c169c413019a4e7cd017ca1edac75cba34d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75f6b4a4f5ef3242baf5f7809e1745c3d2cec23dc5e6175737dceb511fe7973(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3fe12a9313192ce2676733d03b32a759ffc7e19a012e732f75395826d962e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4da97414b80e53936663470af48bfdc39f19ce017fbef8d8bcb604f3cd286f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0048cf3f6fdfd91861c41a1c7e803bf4fb8e900178541283170684e66adfd959(
    value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005d61e0a830ad1c3701d24dc73ca36dd16d8afcd6fd2cf7fb3e0482083d8a9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0b9a06f978b422201b1150e93b6c8833f453c998a523fbc621e0f4535da122(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9962130f6b217cd4ab962778cbffce21d7042a1dc397b793ececc78dcbd7f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b313d2cb4829b8adac648a5d16cc14ab2eb6bfcbea7550835ee06cb12849cdde(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3656d0d3dfda6aa4060d1f86e8bfe84bc70be7568630c9bf0fc857804026125e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4ee18d5c4143b846b0a11cfbb6b820a5690f11ff3935c584394a1c005d7e17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce803a03a23e918fde43f0242097995040a47155636549fbd2bb5f8522a28d7e(
    value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f248de9a09153f49a910d6bb50e943e1dd231744a4230bc51d4e12bc30e2e378(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce3b6ae2de6a5fe9aa86ab792149a5c3809299cf15f3b4a3d880533803370d5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc87775c76aa26a8cea7b6765278c1e2a5826d9e298e1e15ed5338a65be39ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497e9a3f7840a26d3e47c8931e9af558e759be3ae9449ee38122e88bb9f423fe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9043f1939b82846a23e563dd294a3b14d484ff2f2f6e178180627cfc08626ec9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51d9a1cc6ddadf23f8a047430b59a5d68e6f31a58925e15c53de24a04711826(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e706086e6a94231d11cd9dbe1f402d781507ea6ef46aef445b46114932341ee0(
    value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef9a90c0b8b07ab7b7bede09d8bd792eba5d07c032af6cb92fd14156610b9ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945e8e4afbb5645d9cd84da4a8a334e5e10f8fb627619641839722e8afc09d5b(
    value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementApprovalWorkflow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3074812f13b66471ac99534631dac6b21a1fe5b0d594746933c532f01d330b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    entitlement_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f553619351fc7c3494972a2d0de6aea311ba46b90f7f4c9329be37b5c7ec71b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68bfc18aef3c6f4543530125fb2abd0f548b2517d659a7ce2033ddda72bef11(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae696c3f7ac5ca6d8f33a5705d5616f4f323e4b9e41e0c366fdcaaaa74b8f6a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8248416cbc3b1092517f993633c03a8b0177831cc97eff44a429a420e6a6db6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec0ecbd6234445194ebe4d845585b4b4d9bac659f12b0be31362949ad3f3405(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016b204ec50609c48eb8678de1c7a8ff66262e8dc7c43ac2db2b74f5cbcd9fe2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f95575dd9d167bf2133eae882eb1a92d7dde31ba2897daec4b2631849392e2(
    value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementEligibleUsers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb50742e9536cb687c5f815a4f81fc8284a67e15e66f73723be5c67835e45554(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2de8e30ae6aa1913c3149f1ebab46f93ea7b1d2bd4522087192294330056cb7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469f1ae75942e88e30d9d36c779d3d087f7aed03d5e35fc26f832fbd2feccc42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8bf8d04951b87d8de8a093e1d2f8cdf2627a466753a71d39d039b5666cef21b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788e105e4220719ea0a78fea92c51581a0bea00aac76688e90d06beac539aaea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d59ab6b7818e114057e743559641f301458b9ab71304be82f4cea882b45d986(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43406ee48883c307cb5d42c07a2d5489a20919bdd7da5c4d8c0a34cc88866aed(
    value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744c90e40b1c3327a3940090558e6231639716d4b13608f1e8dffe6534db8e64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27a7831a3fa735ea54f9857631e71168ad200fb12c01d8dd997e217bb003c1e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f828a41aac91af194078983f02943d8d667c7767f88089763875f9493bf38f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80fe40e7d2aa60dd834792a30c1cafe7638e61aa49b81057289637a32b81c9b6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852d17734b0b5d611f7b20071f12ae3c98a805a6bbf4c41dcb66d69cae9d5c68(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfef3c037c8f492d411b56c49cd68ee91d6fe2828dbb25c3dcae5e9f24814fc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9daa71be9905bb58eda6ea774adb68cca7e0c8208ad23921676a2b3f97ddfc84(
    value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62e59b3b1ef531186c5be078d4c729e74093c68b243d34888a1bb0b6e6452d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeef9a8281c5dfde8a3ac8cdad7f94d4fa4d50ebf2a2e21d794116cd8a85c72b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f8f5721ad645107843b491cab56e86be2a6d5bc995325e9104b65e3dbaa380(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7dfe48ecd40edbe39bea0396ed4ef8681a909ff26a9e35a7ca32d0c0454428(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0539c985349484127b4de26cbbe6b0d0003465e224b7bccd718a06660f8ea92d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d5fc3bdd1991bba149517a04048666aaa49f3153c41339b938ae99ae0b6883(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da4fdebea978337f939d69948e633186fc88bafcfc978f66843b36c48822810e(
    value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementPrivilegedAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01321a7abedadae73b1bbf21cb7fc50abd0f30e871c027db45801b25f244ea1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f273bc0b870443659cb7f9b16f1fbde8439b2b20fadafd2b9df3cd10010f185(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4128a98a2c7816ba2118689d09b854b0926f0c99029464843ec9c18b2681671f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d894f380948be8dafe108e73db663791f07ba6eb0b583c86a25815c948595be6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce89da60c3d48dc813784727c4e6e1137bdd2692a3f454b970e9cd4740216b61(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8465771ff0bcb49c23cf85e7faf0b429c150eb22663fb0eb0693dc1247d58e7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9592e1583df7f5d4087e3ff473e171b92db4a671d975f286411e9dbd49df467d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5792d5fbaab0a2315bfca77d55f1eccf12022e50267c5ad0e1da1f7af48b6e81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__346fef3e74f2beb0db0aaa48c64af0181fc77baeb943447bdb607b887a4f0931(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b67a9265daaa3f67cee67b211f9ffecb3bc1d365a265ce5260f6c47d642c69c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65a1f9fd35299c0621d35a39d0372b68af4686a7e6660f549926a8ad1d997ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58bd1d7207da5626c1fdd9ea80d21db70a6ecc647f357e23d914c2bae54848f(
    value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0e50d820c6df1be554ae08a6e7276222e46e3c081598e15c8da71c7f6650465(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b871422578c326ec294dce829fd2cf0a2a68a8e140925b74ec25534475d2cf6(
    value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da9e6cd221405789035bb3cb11e2c5f0198acf02fac8b968204a47bfba70d53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ecee121032e1eee524d53f38e7033e0f6cd7b0e962fc15ba1095ee8101fdbb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afbc5aedc66d6c972d1bbaaa12109416cec09f5ca348dea46a8c247fa519fa1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ad93fc75db0bf10e14d25efc330f984af891e020d1645b546b08b4836e501c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71337f4ae9bb2b3df3fa1c75c3f4a59356a000547c8ddbe0b2cb45e8b9ce8d97(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa1df2672b7d16ee522f249bace84e5158b99191ceaf4d9a1bc7c3b4d73ca07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3249fcc8c46354587ccd111d41a3700bbe87a376d345f0bd114fcc1cff0501d6(
    value: typing.Optional[DataGooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `azuread_group`

Refer to the Terraform Registry for docs: [`azuread_group`](https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group).
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


class Group(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.group.Group",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group azuread_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        administrative_unit_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        assignable_to_role: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_subscribe_new_members: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        behaviors: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamic_membership: typing.Optional[typing.Union["GroupDynamicMembership", typing.Dict[builtins.str, typing.Any]]] = None,
        external_senders_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_from_address_lists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_from_outlook_clients: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        mail_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mail_nickname: typing.Optional[builtins.str] = None,
        members: typing.Optional[typing.Sequence[builtins.str]] = None,
        onpremises_group_type: typing.Optional[builtins.str] = None,
        owners: typing.Optional[typing.Sequence[builtins.str]] = None,
        prevent_duplicate_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        provisioning_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        theme: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
        visibility: typing.Optional[builtins.str] = None,
        writeback_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group azuread_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The display name for the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#display_name Group#display_name}
        :param administrative_unit_ids: The administrative unit IDs in which the group should be. If empty, the group will be created at the tenant level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#administrative_unit_ids Group#administrative_unit_ids}
        :param assignable_to_role: Indicates whether this group can be assigned to an Azure Active Directory role. This property can only be ``true`` for security-enabled groups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#assignable_to_role Group#assignable_to_role}
        :param auto_subscribe_new_members: Indicates whether new members added to the group will be auto-subscribed to receive email notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#auto_subscribe_new_members Group#auto_subscribe_new_members}
        :param behaviors: The group behaviours for a Microsoft 365 group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#behaviors Group#behaviors}
        :param description: The description for the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#description Group#description}
        :param dynamic_membership: dynamic_membership block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#dynamic_membership Group#dynamic_membership}
        :param external_senders_allowed: Indicates whether people external to the organization can send messages to the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#external_senders_allowed Group#external_senders_allowed}
        :param hide_from_address_lists: Indicates whether the group is displayed in certain parts of the Outlook user interface: in the Address Book, in address lists for selecting message recipients, and in the Browse Groups dialog for searching groups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#hide_from_address_lists Group#hide_from_address_lists}
        :param hide_from_outlook_clients: Indicates whether the group is displayed in Outlook clients, such as Outlook for Windows and Outlook on the web. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#hide_from_outlook_clients Group#hide_from_outlook_clients}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#id Group#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mail_enabled: Whether the group is a mail enabled, with a shared group mailbox. At least one of ``mail_enabled`` or ``security_enabled`` must be specified. A group can be mail enabled *and* security enabled Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#mail_enabled Group#mail_enabled}
        :param mail_nickname: The mail alias for the group, unique in the organisation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#mail_nickname Group#mail_nickname}
        :param members: A set of members who should be present in this group. Supported object types are Users, Groups or Service Principals Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#members Group#members}
        :param onpremises_group_type: Indicates the target on-premise group type the group will be written back as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#onpremises_group_type Group#onpremises_group_type}
        :param owners: A set of owners who own this group. Supported object types are Users or Service Principals. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#owners Group#owners}
        :param prevent_duplicate_names: If ``true``, will return an error if an existing group is found with the same name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#prevent_duplicate_names Group#prevent_duplicate_names}
        :param provisioning_options: The group provisioning options for a Microsoft 365 group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#provisioning_options Group#provisioning_options}
        :param security_enabled: Whether the group is a security group for controlling access to in-app resources. At least one of ``security_enabled`` or ``mail_enabled`` must be specified. A group can be security enabled *and* mail enabled Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#security_enabled Group#security_enabled}
        :param theme: The colour theme for a Microsoft 365 group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#theme Group#theme}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#timeouts Group#timeouts}
        :param types: A set of group types to configure for the group. ``Unified`` specifies a Microsoft 365 group. Required when ``mail_enabled`` is true Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#types Group#types}
        :param visibility: Specifies the group join policy and group content visibility. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#visibility Group#visibility}
        :param writeback_enabled: Whether this group should be synced from Azure AD to the on-premises directory when Azure AD Connect is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#writeback_enabled Group#writeback_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57cec1dff8bf4b59beeaf8d356d64549966d579c4f31b5278225aa0f1eab6299)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GroupConfig(
            display_name=display_name,
            administrative_unit_ids=administrative_unit_ids,
            assignable_to_role=assignable_to_role,
            auto_subscribe_new_members=auto_subscribe_new_members,
            behaviors=behaviors,
            description=description,
            dynamic_membership=dynamic_membership,
            external_senders_allowed=external_senders_allowed,
            hide_from_address_lists=hide_from_address_lists,
            hide_from_outlook_clients=hide_from_outlook_clients,
            id=id,
            mail_enabled=mail_enabled,
            mail_nickname=mail_nickname,
            members=members,
            onpremises_group_type=onpremises_group_type,
            owners=owners,
            prevent_duplicate_names=prevent_duplicate_names,
            provisioning_options=provisioning_options,
            security_enabled=security_enabled,
            theme=theme,
            timeouts=timeouts,
            types=types,
            visibility=visibility,
            writeback_enabled=writeback_enabled,
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
        '''Generates CDKTF code for importing a Group resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Group to import.
        :param import_from_id: The id of the existing Group that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Group to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bdd9713f6d0cc38429007886dda974dfab08b41cf8a3f0bffe81b30860ebbe2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDynamicMembership")
    def put_dynamic_membership(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        rule: builtins.str,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#enabled Group#enabled}.
        :param rule: Rule to determine members for a dynamic group. Required when ``group_types`` contains 'DynamicMembership'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#rule Group#rule}
        '''
        value = GroupDynamicMembership(enabled=enabled, rule=rule)

        return typing.cast(None, jsii.invoke(self, "putDynamicMembership", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#create Group#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#delete Group#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#read Group#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#update Group#update}.
        '''
        value = GroupTimeouts(create=create, delete=delete, read=read, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdministrativeUnitIds")
    def reset_administrative_unit_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministrativeUnitIds", []))

    @jsii.member(jsii_name="resetAssignableToRole")
    def reset_assignable_to_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssignableToRole", []))

    @jsii.member(jsii_name="resetAutoSubscribeNewMembers")
    def reset_auto_subscribe_new_members(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoSubscribeNewMembers", []))

    @jsii.member(jsii_name="resetBehaviors")
    def reset_behaviors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBehaviors", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDynamicMembership")
    def reset_dynamic_membership(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicMembership", []))

    @jsii.member(jsii_name="resetExternalSendersAllowed")
    def reset_external_senders_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalSendersAllowed", []))

    @jsii.member(jsii_name="resetHideFromAddressLists")
    def reset_hide_from_address_lists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHideFromAddressLists", []))

    @jsii.member(jsii_name="resetHideFromOutlookClients")
    def reset_hide_from_outlook_clients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHideFromOutlookClients", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMailEnabled")
    def reset_mail_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMailEnabled", []))

    @jsii.member(jsii_name="resetMailNickname")
    def reset_mail_nickname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMailNickname", []))

    @jsii.member(jsii_name="resetMembers")
    def reset_members(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembers", []))

    @jsii.member(jsii_name="resetOnpremisesGroupType")
    def reset_onpremises_group_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnpremisesGroupType", []))

    @jsii.member(jsii_name="resetOwners")
    def reset_owners(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwners", []))

    @jsii.member(jsii_name="resetPreventDuplicateNames")
    def reset_prevent_duplicate_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreventDuplicateNames", []))

    @jsii.member(jsii_name="resetProvisioningOptions")
    def reset_provisioning_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisioningOptions", []))

    @jsii.member(jsii_name="resetSecurityEnabled")
    def reset_security_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityEnabled", []))

    @jsii.member(jsii_name="resetTheme")
    def reset_theme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTheme", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTypes")
    def reset_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypes", []))

    @jsii.member(jsii_name="resetVisibility")
    def reset_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibility", []))

    @jsii.member(jsii_name="resetWritebackEnabled")
    def reset_writeback_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWritebackEnabled", []))

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
    @jsii.member(jsii_name="dynamicMembership")
    def dynamic_membership(self) -> "GroupDynamicMembershipOutputReference":
        return typing.cast("GroupDynamicMembershipOutputReference", jsii.get(self, "dynamicMembership"))

    @builtins.property
    @jsii.member(jsii_name="mail")
    def mail(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mail"))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesDomainName")
    def onpremises_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onpremisesDomainName"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesNetbiosName")
    def onpremises_netbios_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onpremisesNetbiosName"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesSamAccountName")
    def onpremises_sam_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onpremisesSamAccountName"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesSecurityIdentifier")
    def onpremises_security_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onpremisesSecurityIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesSyncEnabled")
    def onpremises_sync_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "onpremisesSyncEnabled"))

    @builtins.property
    @jsii.member(jsii_name="preferredLanguage")
    def preferred_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferredLanguage"))

    @builtins.property
    @jsii.member(jsii_name="proxyAddresses")
    def proxy_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "proxyAddresses"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GroupTimeoutsOutputReference":
        return typing.cast("GroupTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="administrativeUnitIdsInput")
    def administrative_unit_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "administrativeUnitIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="assignableToRoleInput")
    def assignable_to_role_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "assignableToRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="autoSubscribeNewMembersInput")
    def auto_subscribe_new_members_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoSubscribeNewMembersInput"))

    @builtins.property
    @jsii.member(jsii_name="behaviorsInput")
    def behaviors_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "behaviorsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicMembershipInput")
    def dynamic_membership_input(self) -> typing.Optional["GroupDynamicMembership"]:
        return typing.cast(typing.Optional["GroupDynamicMembership"], jsii.get(self, "dynamicMembershipInput"))

    @builtins.property
    @jsii.member(jsii_name="externalSendersAllowedInput")
    def external_senders_allowed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "externalSendersAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="hideFromAddressListsInput")
    def hide_from_address_lists_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hideFromAddressListsInput"))

    @builtins.property
    @jsii.member(jsii_name="hideFromOutlookClientsInput")
    def hide_from_outlook_clients_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hideFromOutlookClientsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mailEnabledInput")
    def mail_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mailEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="mailNicknameInput")
    def mail_nickname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mailNicknameInput"))

    @builtins.property
    @jsii.member(jsii_name="membersInput")
    def members_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "membersInput"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesGroupTypeInput")
    def onpremises_group_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onpremisesGroupTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ownersInput")
    def owners_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ownersInput"))

    @builtins.property
    @jsii.member(jsii_name="preventDuplicateNamesInput")
    def prevent_duplicate_names_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preventDuplicateNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="provisioningOptionsInput")
    def provisioning_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "provisioningOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityEnabledInput")
    def security_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "securityEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="themeInput")
    def theme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "themeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GroupTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GroupTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typesInput")
    def types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "typesInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="writebackEnabledInput")
    def writeback_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "writebackEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="administrativeUnitIds")
    def administrative_unit_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "administrativeUnitIds"))

    @administrative_unit_ids.setter
    def administrative_unit_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95cc40902601a8f4b4a6558057bffac91b0f66757554ec097cf992176e60ae53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administrativeUnitIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="assignableToRole")
    def assignable_to_role(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "assignableToRole"))

    @assignable_to_role.setter
    def assignable_to_role(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ca6823fa793ae00ce3b24c0e490a0b6c466b769134c80687e92a4af48aabe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assignableToRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoSubscribeNewMembers")
    def auto_subscribe_new_members(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoSubscribeNewMembers"))

    @auto_subscribe_new_members.setter
    def auto_subscribe_new_members(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f1957ee095250beadb8841afcbb3ceea40fd53427eb13444b60ee8c14d9ee70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSubscribeNewMembers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="behaviors")
    def behaviors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "behaviors"))

    @behaviors.setter
    def behaviors(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__757a30022db9bdd170273b21b7b7353c9a4d7ee7da5131d5fb3f2320644e2391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behaviors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664cc6e4dd953d28933e44a96f626c1eb760c7e354ef449ae05ef47362c67ab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0447a33c1cb8d859fde6243fec1240db78dee5252ee7f93af1128202eb6608a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalSendersAllowed")
    def external_senders_allowed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "externalSendersAllowed"))

    @external_senders_allowed.setter
    def external_senders_allowed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e3265a22278c4a6c2a1c1164c48eb227fe551a8711dec2d264dd7f7b8ca165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalSendersAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hideFromAddressLists")
    def hide_from_address_lists(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hideFromAddressLists"))

    @hide_from_address_lists.setter
    def hide_from_address_lists(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ea48eb2e737720b6a5ebc911420a07c2bee0127cea3b2fedf02c7aeefb0eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hideFromAddressLists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hideFromOutlookClients")
    def hide_from_outlook_clients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hideFromOutlookClients"))

    @hide_from_outlook_clients.setter
    def hide_from_outlook_clients(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d5496381be878625580ef03b239e4c48f80e3b4546143384f6a57e451d884c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hideFromOutlookClients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1461fcd50393688909bb398627d907b2b4d76e0592e56f1bf75e681d0a645491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mailEnabled")
    def mail_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mailEnabled"))

    @mail_enabled.setter
    def mail_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d747361375c46f2767410a04ed742f793c4f75a5368eb336cbba3822d0f9405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mailEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mailNickname")
    def mail_nickname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mailNickname"))

    @mail_nickname.setter
    def mail_nickname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6c3939d89cc82e887dfce18ff16f07619c58b5aa555edc0fee191cc2fdb3e34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mailNickname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="members")
    def members(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "members"))

    @members.setter
    def members(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b262a67fbb284a8d5b748d0d6b57e4862e547efaa86bbd5823d43a4e5a44d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "members", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onpremisesGroupType")
    def onpremises_group_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onpremisesGroupType"))

    @onpremises_group_type.setter
    def onpremises_group_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3784016360ceb15900b6f36bfc18d6bcf06c7629d554adf72514b0df0d5f2e42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onpremisesGroupType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="owners")
    def owners(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "owners"))

    @owners.setter
    def owners(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63991d9fcd1a9966b00b5ca504e2271c355d87bff16871c81cd20dba7a7f0e3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owners", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preventDuplicateNames")
    def prevent_duplicate_names(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preventDuplicateNames"))

    @prevent_duplicate_names.setter
    def prevent_duplicate_names(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__143e4ebfa2770d3cc5dc1556a57d6f7138760293b2f02985b42b946b7d09a8c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventDuplicateNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisioningOptions")
    def provisioning_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "provisioningOptions"))

    @provisioning_options.setter
    def provisioning_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd10f3df7fe6f4f9bf7db5b06610f32fb8726d691e06d4e0782715383bf3c97e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityEnabled")
    def security_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "securityEnabled"))

    @security_enabled.setter
    def security_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0f107c34ba8792187c509f6b527379876bb037165d4029e6ea239c1b94d5639)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="theme")
    def theme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "theme"))

    @theme.setter
    def theme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d16a16ceb68f91f902c89feda6adb5c62d8ab94df8cb6eeba106244b97536f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "theme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "types"))

    @types.setter
    def types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47df827a3e35e7ef8b9a364ddc6562c9a500d5db8823e4864b2508c34b1cddc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "types", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6eee3d246ce0c9fadbcd29f564ef0f2d3667a88c0ea3fad2b9329729c71f344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writebackEnabled")
    def writeback_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "writebackEnabled"))

    @writeback_enabled.setter
    def writeback_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b37268e93f02d1bf64bc382309efb235f636ad3bf36e49197cd3c9550f0957)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writebackEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.group.GroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "administrative_unit_ids": "administrativeUnitIds",
        "assignable_to_role": "assignableToRole",
        "auto_subscribe_new_members": "autoSubscribeNewMembers",
        "behaviors": "behaviors",
        "description": "description",
        "dynamic_membership": "dynamicMembership",
        "external_senders_allowed": "externalSendersAllowed",
        "hide_from_address_lists": "hideFromAddressLists",
        "hide_from_outlook_clients": "hideFromOutlookClients",
        "id": "id",
        "mail_enabled": "mailEnabled",
        "mail_nickname": "mailNickname",
        "members": "members",
        "onpremises_group_type": "onpremisesGroupType",
        "owners": "owners",
        "prevent_duplicate_names": "preventDuplicateNames",
        "provisioning_options": "provisioningOptions",
        "security_enabled": "securityEnabled",
        "theme": "theme",
        "timeouts": "timeouts",
        "types": "types",
        "visibility": "visibility",
        "writeback_enabled": "writebackEnabled",
    },
)
class GroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        administrative_unit_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        assignable_to_role: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_subscribe_new_members: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        behaviors: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamic_membership: typing.Optional[typing.Union["GroupDynamicMembership", typing.Dict[builtins.str, typing.Any]]] = None,
        external_senders_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_from_address_lists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_from_outlook_clients: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        mail_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mail_nickname: typing.Optional[builtins.str] = None,
        members: typing.Optional[typing.Sequence[builtins.str]] = None,
        onpremises_group_type: typing.Optional[builtins.str] = None,
        owners: typing.Optional[typing.Sequence[builtins.str]] = None,
        prevent_duplicate_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        provisioning_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        theme: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
        visibility: typing.Optional[builtins.str] = None,
        writeback_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The display name for the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#display_name Group#display_name}
        :param administrative_unit_ids: The administrative unit IDs in which the group should be. If empty, the group will be created at the tenant level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#administrative_unit_ids Group#administrative_unit_ids}
        :param assignable_to_role: Indicates whether this group can be assigned to an Azure Active Directory role. This property can only be ``true`` for security-enabled groups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#assignable_to_role Group#assignable_to_role}
        :param auto_subscribe_new_members: Indicates whether new members added to the group will be auto-subscribed to receive email notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#auto_subscribe_new_members Group#auto_subscribe_new_members}
        :param behaviors: The group behaviours for a Microsoft 365 group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#behaviors Group#behaviors}
        :param description: The description for the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#description Group#description}
        :param dynamic_membership: dynamic_membership block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#dynamic_membership Group#dynamic_membership}
        :param external_senders_allowed: Indicates whether people external to the organization can send messages to the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#external_senders_allowed Group#external_senders_allowed}
        :param hide_from_address_lists: Indicates whether the group is displayed in certain parts of the Outlook user interface: in the Address Book, in address lists for selecting message recipients, and in the Browse Groups dialog for searching groups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#hide_from_address_lists Group#hide_from_address_lists}
        :param hide_from_outlook_clients: Indicates whether the group is displayed in Outlook clients, such as Outlook for Windows and Outlook on the web. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#hide_from_outlook_clients Group#hide_from_outlook_clients}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#id Group#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mail_enabled: Whether the group is a mail enabled, with a shared group mailbox. At least one of ``mail_enabled`` or ``security_enabled`` must be specified. A group can be mail enabled *and* security enabled Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#mail_enabled Group#mail_enabled}
        :param mail_nickname: The mail alias for the group, unique in the organisation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#mail_nickname Group#mail_nickname}
        :param members: A set of members who should be present in this group. Supported object types are Users, Groups or Service Principals Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#members Group#members}
        :param onpremises_group_type: Indicates the target on-premise group type the group will be written back as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#onpremises_group_type Group#onpremises_group_type}
        :param owners: A set of owners who own this group. Supported object types are Users or Service Principals. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#owners Group#owners}
        :param prevent_duplicate_names: If ``true``, will return an error if an existing group is found with the same name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#prevent_duplicate_names Group#prevent_duplicate_names}
        :param provisioning_options: The group provisioning options for a Microsoft 365 group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#provisioning_options Group#provisioning_options}
        :param security_enabled: Whether the group is a security group for controlling access to in-app resources. At least one of ``security_enabled`` or ``mail_enabled`` must be specified. A group can be security enabled *and* mail enabled Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#security_enabled Group#security_enabled}
        :param theme: The colour theme for a Microsoft 365 group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#theme Group#theme}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#timeouts Group#timeouts}
        :param types: A set of group types to configure for the group. ``Unified`` specifies a Microsoft 365 group. Required when ``mail_enabled`` is true Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#types Group#types}
        :param visibility: Specifies the group join policy and group content visibility. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#visibility Group#visibility}
        :param writeback_enabled: Whether this group should be synced from Azure AD to the on-premises directory when Azure AD Connect is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#writeback_enabled Group#writeback_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dynamic_membership, dict):
            dynamic_membership = GroupDynamicMembership(**dynamic_membership)
        if isinstance(timeouts, dict):
            timeouts = GroupTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47b7233356d26eaf49aa543fb81be0a3612fed53e3db84c23edb8b4664cf46e9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument administrative_unit_ids", value=administrative_unit_ids, expected_type=type_hints["administrative_unit_ids"])
            check_type(argname="argument assignable_to_role", value=assignable_to_role, expected_type=type_hints["assignable_to_role"])
            check_type(argname="argument auto_subscribe_new_members", value=auto_subscribe_new_members, expected_type=type_hints["auto_subscribe_new_members"])
            check_type(argname="argument behaviors", value=behaviors, expected_type=type_hints["behaviors"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dynamic_membership", value=dynamic_membership, expected_type=type_hints["dynamic_membership"])
            check_type(argname="argument external_senders_allowed", value=external_senders_allowed, expected_type=type_hints["external_senders_allowed"])
            check_type(argname="argument hide_from_address_lists", value=hide_from_address_lists, expected_type=type_hints["hide_from_address_lists"])
            check_type(argname="argument hide_from_outlook_clients", value=hide_from_outlook_clients, expected_type=type_hints["hide_from_outlook_clients"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mail_enabled", value=mail_enabled, expected_type=type_hints["mail_enabled"])
            check_type(argname="argument mail_nickname", value=mail_nickname, expected_type=type_hints["mail_nickname"])
            check_type(argname="argument members", value=members, expected_type=type_hints["members"])
            check_type(argname="argument onpremises_group_type", value=onpremises_group_type, expected_type=type_hints["onpremises_group_type"])
            check_type(argname="argument owners", value=owners, expected_type=type_hints["owners"])
            check_type(argname="argument prevent_duplicate_names", value=prevent_duplicate_names, expected_type=type_hints["prevent_duplicate_names"])
            check_type(argname="argument provisioning_options", value=provisioning_options, expected_type=type_hints["provisioning_options"])
            check_type(argname="argument security_enabled", value=security_enabled, expected_type=type_hints["security_enabled"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
            check_type(argname="argument writeback_enabled", value=writeback_enabled, expected_type=type_hints["writeback_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
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
        if administrative_unit_ids is not None:
            self._values["administrative_unit_ids"] = administrative_unit_ids
        if assignable_to_role is not None:
            self._values["assignable_to_role"] = assignable_to_role
        if auto_subscribe_new_members is not None:
            self._values["auto_subscribe_new_members"] = auto_subscribe_new_members
        if behaviors is not None:
            self._values["behaviors"] = behaviors
        if description is not None:
            self._values["description"] = description
        if dynamic_membership is not None:
            self._values["dynamic_membership"] = dynamic_membership
        if external_senders_allowed is not None:
            self._values["external_senders_allowed"] = external_senders_allowed
        if hide_from_address_lists is not None:
            self._values["hide_from_address_lists"] = hide_from_address_lists
        if hide_from_outlook_clients is not None:
            self._values["hide_from_outlook_clients"] = hide_from_outlook_clients
        if id is not None:
            self._values["id"] = id
        if mail_enabled is not None:
            self._values["mail_enabled"] = mail_enabled
        if mail_nickname is not None:
            self._values["mail_nickname"] = mail_nickname
        if members is not None:
            self._values["members"] = members
        if onpremises_group_type is not None:
            self._values["onpremises_group_type"] = onpremises_group_type
        if owners is not None:
            self._values["owners"] = owners
        if prevent_duplicate_names is not None:
            self._values["prevent_duplicate_names"] = prevent_duplicate_names
        if provisioning_options is not None:
            self._values["provisioning_options"] = provisioning_options
        if security_enabled is not None:
            self._values["security_enabled"] = security_enabled
        if theme is not None:
            self._values["theme"] = theme
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if types is not None:
            self._values["types"] = types
        if visibility is not None:
            self._values["visibility"] = visibility
        if writeback_enabled is not None:
            self._values["writeback_enabled"] = writeback_enabled

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
    def display_name(self) -> builtins.str:
        '''The display name for the group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#display_name Group#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def administrative_unit_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The administrative unit IDs in which the group should be.

        If empty, the group will be created at the tenant level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#administrative_unit_ids Group#administrative_unit_ids}
        '''
        result = self._values.get("administrative_unit_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def assignable_to_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether this group can be assigned to an Azure Active Directory role.

        This property can only be ``true`` for security-enabled groups.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#assignable_to_role Group#assignable_to_role}
        '''
        result = self._values.get("assignable_to_role")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_subscribe_new_members(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether new members added to the group will be auto-subscribed to receive email notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#auto_subscribe_new_members Group#auto_subscribe_new_members}
        '''
        result = self._values.get("auto_subscribe_new_members")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def behaviors(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The group behaviours for a Microsoft 365 group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#behaviors Group#behaviors}
        '''
        result = self._values.get("behaviors")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#description Group#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamic_membership(self) -> typing.Optional["GroupDynamicMembership"]:
        '''dynamic_membership block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#dynamic_membership Group#dynamic_membership}
        '''
        result = self._values.get("dynamic_membership")
        return typing.cast(typing.Optional["GroupDynamicMembership"], result)

    @builtins.property
    def external_senders_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether people external to the organization can send messages to the group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#external_senders_allowed Group#external_senders_allowed}
        '''
        result = self._values.get("external_senders_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hide_from_address_lists(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the group is displayed in certain parts of the Outlook user interface: in the Address Book, in address lists for selecting message recipients, and in the Browse Groups dialog for searching groups.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#hide_from_address_lists Group#hide_from_address_lists}
        '''
        result = self._values.get("hide_from_address_lists")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hide_from_outlook_clients(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the group is displayed in Outlook clients, such as Outlook for Windows and Outlook on the web.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#hide_from_outlook_clients Group#hide_from_outlook_clients}
        '''
        result = self._values.get("hide_from_outlook_clients")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#id Group#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mail_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the group is a mail enabled, with a shared group mailbox.

        At least one of ``mail_enabled`` or ``security_enabled`` must be specified. A group can be mail enabled *and* security enabled

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#mail_enabled Group#mail_enabled}
        '''
        result = self._values.get("mail_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mail_nickname(self) -> typing.Optional[builtins.str]:
        '''The mail alias for the group, unique in the organisation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#mail_nickname Group#mail_nickname}
        '''
        result = self._values.get("mail_nickname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def members(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of members who should be present in this group.

        Supported object types are Users, Groups or Service Principals

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#members Group#members}
        '''
        result = self._values.get("members")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def onpremises_group_type(self) -> typing.Optional[builtins.str]:
        '''Indicates the target on-premise group type the group will be written back as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#onpremises_group_type Group#onpremises_group_type}
        '''
        result = self._values.get("onpremises_group_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owners(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of owners who own this group. Supported object types are Users or Service Principals.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#owners Group#owners}
        '''
        result = self._values.get("owners")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def prevent_duplicate_names(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true``, will return an error if an existing group is found with the same name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#prevent_duplicate_names Group#prevent_duplicate_names}
        '''
        result = self._values.get("prevent_duplicate_names")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def provisioning_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The group provisioning options for a Microsoft 365 group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#provisioning_options Group#provisioning_options}
        '''
        result = self._values.get("provisioning_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the group is a security group for controlling access to in-app resources.

        At least one of ``security_enabled`` or ``mail_enabled`` must be specified. A group can be security enabled *and* mail enabled

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#security_enabled Group#security_enabled}
        '''
        result = self._values.get("security_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def theme(self) -> typing.Optional[builtins.str]:
        '''The colour theme for a Microsoft 365 group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#theme Group#theme}
        '''
        result = self._values.get("theme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GroupTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#timeouts Group#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GroupTimeouts"], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of group types to configure for the group.

        ``Unified`` specifies a Microsoft 365 group. Required when ``mail_enabled`` is true

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#types Group#types}
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''Specifies the group join policy and group content visibility.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#visibility Group#visibility}
        '''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def writeback_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this group should be synced from Azure AD to the on-premises directory when Azure AD Connect is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#writeback_enabled Group#writeback_enabled}
        '''
        result = self._values.get("writeback_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.group.GroupDynamicMembership",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "rule": "rule"},
)
class GroupDynamicMembership:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        rule: builtins.str,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#enabled Group#enabled}.
        :param rule: Rule to determine members for a dynamic group. Required when ``group_types`` contains 'DynamicMembership'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#rule Group#rule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5baeb9ccec25f32937fbf82a07c8ca7906b4e85dda0c59207893b6b6df2efc30)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "rule": rule,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#enabled Group#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def rule(self) -> builtins.str:
        '''Rule to determine members for a dynamic group. Required when ``group_types`` contains 'DynamicMembership'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#rule Group#rule}
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupDynamicMembership(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupDynamicMembershipOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.group.GroupDynamicMembershipOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__807a57e1627e164255c24844cc3f538b35969fe1b59a4ed6a67af98611fde474)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4efdf723d3800a0cc06af05f321d7ba326f928853938861288303c42195a6993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rule"))

    @rule.setter
    def rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4feeb4f47c5b14c111568a83df688aa82c369b8e2a0291125d5d594bbc2d0796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GroupDynamicMembership]:
        return typing.cast(typing.Optional[GroupDynamicMembership], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GroupDynamicMembership]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd534d6e756dceabb6a2b8a1bcf1ebf92e9ac67eef04f3996b75fa74cc71eec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.group.GroupTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class GroupTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#create Group#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#delete Group#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#read Group#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#update Group#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c6893784a70c7186c61a3c690ade07b0de0888dd4171356f1786b696c995b80)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#create Group#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#delete Group#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#read Group#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group#update Group#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.group.GroupTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fcba0b138bb740dadf556e7123820597b5a289447e7996600e27e48b3687574)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceb0d1afe9e41f7b8521c1d0c625ccda2fb9305ef0accd7247ea0456dfd550a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cbfcd66e569a0bc1f1c08ac664ab539bf2298b28a9fb3cede35562eadf03c0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109d1a69f7abd68da445bb361c3aa53ab8abb72eef190ce5d423400e3b3db8ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e5ed34c7bd003cf6a3672174d11be73cd1a9196a5ec52279bd3509620a3ff5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e339815097411c1c96de3d10d4572fda9d8a58947a373c5b513dea8e544cfb44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Group",
    "GroupConfig",
    "GroupDynamicMembership",
    "GroupDynamicMembershipOutputReference",
    "GroupTimeouts",
    "GroupTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__57cec1dff8bf4b59beeaf8d356d64549966d579c4f31b5278225aa0f1eab6299(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    administrative_unit_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    assignable_to_role: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_subscribe_new_members: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    behaviors: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamic_membership: typing.Optional[typing.Union[GroupDynamicMembership, typing.Dict[builtins.str, typing.Any]]] = None,
    external_senders_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_from_address_lists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_from_outlook_clients: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    mail_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mail_nickname: typing.Optional[builtins.str] = None,
    members: typing.Optional[typing.Sequence[builtins.str]] = None,
    onpremises_group_type: typing.Optional[builtins.str] = None,
    owners: typing.Optional[typing.Sequence[builtins.str]] = None,
    prevent_duplicate_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    provisioning_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    theme: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
    visibility: typing.Optional[builtins.str] = None,
    writeback_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__4bdd9713f6d0cc38429007886dda974dfab08b41cf8a3f0bffe81b30860ebbe2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95cc40902601a8f4b4a6558057bffac91b0f66757554ec097cf992176e60ae53(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ca6823fa793ae00ce3b24c0e490a0b6c466b769134c80687e92a4af48aabe9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1957ee095250beadb8841afcbb3ceea40fd53427eb13444b60ee8c14d9ee70(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757a30022db9bdd170273b21b7b7353c9a4d7ee7da5131d5fb3f2320644e2391(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664cc6e4dd953d28933e44a96f626c1eb760c7e354ef449ae05ef47362c67ab7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0447a33c1cb8d859fde6243fec1240db78dee5252ee7f93af1128202eb6608a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e3265a22278c4a6c2a1c1164c48eb227fe551a8711dec2d264dd7f7b8ca165(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ea48eb2e737720b6a5ebc911420a07c2bee0127cea3b2fedf02c7aeefb0eb6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d5496381be878625580ef03b239e4c48f80e3b4546143384f6a57e451d884c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1461fcd50393688909bb398627d907b2b4d76e0592e56f1bf75e681d0a645491(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d747361375c46f2767410a04ed742f793c4f75a5368eb336cbba3822d0f9405(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c3939d89cc82e887dfce18ff16f07619c58b5aa555edc0fee191cc2fdb3e34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b262a67fbb284a8d5b748d0d6b57e4862e547efaa86bbd5823d43a4e5a44d2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3784016360ceb15900b6f36bfc18d6bcf06c7629d554adf72514b0df0d5f2e42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63991d9fcd1a9966b00b5ca504e2271c355d87bff16871c81cd20dba7a7f0e3c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143e4ebfa2770d3cc5dc1556a57d6f7138760293b2f02985b42b946b7d09a8c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd10f3df7fe6f4f9bf7db5b06610f32fb8726d691e06d4e0782715383bf3c97e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f107c34ba8792187c509f6b527379876bb037165d4029e6ea239c1b94d5639(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d16a16ceb68f91f902c89feda6adb5c62d8ab94df8cb6eeba106244b97536f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47df827a3e35e7ef8b9a364ddc6562c9a500d5db8823e4864b2508c34b1cddc2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6eee3d246ce0c9fadbcd29f564ef0f2d3667a88c0ea3fad2b9329729c71f344(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b37268e93f02d1bf64bc382309efb235f636ad3bf36e49197cd3c9550f0957(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47b7233356d26eaf49aa543fb81be0a3612fed53e3db84c23edb8b4664cf46e9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    administrative_unit_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    assignable_to_role: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_subscribe_new_members: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    behaviors: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamic_membership: typing.Optional[typing.Union[GroupDynamicMembership, typing.Dict[builtins.str, typing.Any]]] = None,
    external_senders_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_from_address_lists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_from_outlook_clients: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    mail_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mail_nickname: typing.Optional[builtins.str] = None,
    members: typing.Optional[typing.Sequence[builtins.str]] = None,
    onpremises_group_type: typing.Optional[builtins.str] = None,
    owners: typing.Optional[typing.Sequence[builtins.str]] = None,
    prevent_duplicate_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    provisioning_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    theme: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
    visibility: typing.Optional[builtins.str] = None,
    writeback_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5baeb9ccec25f32937fbf82a07c8ca7906b4e85dda0c59207893b6b6df2efc30(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    rule: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807a57e1627e164255c24844cc3f538b35969fe1b59a4ed6a67af98611fde474(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4efdf723d3800a0cc06af05f321d7ba326f928853938861288303c42195a6993(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4feeb4f47c5b14c111568a83df688aa82c369b8e2a0291125d5d594bbc2d0796(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd534d6e756dceabb6a2b8a1bcf1ebf92e9ac67eef04f3996b75fa74cc71eec(
    value: typing.Optional[GroupDynamicMembership],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6893784a70c7186c61a3c690ade07b0de0888dd4171356f1786b696c995b80(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fcba0b138bb740dadf556e7123820597b5a289447e7996600e27e48b3687574(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb0d1afe9e41f7b8521c1d0c625ccda2fb9305ef0accd7247ea0456dfd550a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbfcd66e569a0bc1f1c08ac664ab539bf2298b28a9fb3cede35562eadf03c0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109d1a69f7abd68da445bb361c3aa53ab8abb72eef190ce5d423400e3b3db8ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e5ed34c7bd003cf6a3672174d11be73cd1a9196a5ec52279bd3509620a3ff5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e339815097411c1c96de3d10d4572fda9d8a58947a373c5b513dea8e544cfb44(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `google_folder_access_approval_settings`

Refer to the Terraform Registry for docs: [`google_folder_access_approval_settings`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings).
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


class FolderAccessApprovalSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.folderAccessApprovalSettings.FolderAccessApprovalSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings google_folder_access_approval_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        enrolled_services: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FolderAccessApprovalSettingsEnrolledServices", typing.Dict[builtins.str, typing.Any]]]],
        folder_id: builtins.str,
        active_key_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        notification_emails: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["FolderAccessApprovalSettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings google_folder_access_approval_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enrolled_services: enrolled_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#enrolled_services FolderAccessApprovalSettings#enrolled_services}
        :param folder_id: ID of the folder of the access approval settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#folder_id FolderAccessApprovalSettings#folder_id}
        :param active_key_version: The asymmetric crypto key version to use for signing approval requests. Empty active_key_version indicates that a Google-managed key should be used for signing. This property will be ignored if set by an ancestor of the resource, and new non-empty values may not be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#active_key_version FolderAccessApprovalSettings#active_key_version}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#id FolderAccessApprovalSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_emails: A list of email addresses to which notifications relating to approval requests should be sent. Notifications relating to a resource will be sent to all emails in the settings of ancestor resources of that resource. A maximum of 50 email addresses are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#notification_emails FolderAccessApprovalSettings#notification_emails}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#timeouts FolderAccessApprovalSettings#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4f2804fafd90d3e37aa0ecbe21700fc00e04b70e3fa643e263d95b939a3eb80)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FolderAccessApprovalSettingsConfig(
            enrolled_services=enrolled_services,
            folder_id=folder_id,
            active_key_version=active_key_version,
            id=id,
            notification_emails=notification_emails,
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
        '''Generates CDKTF code for importing a FolderAccessApprovalSettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FolderAccessApprovalSettings to import.
        :param import_from_id: The id of the existing FolderAccessApprovalSettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FolderAccessApprovalSettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e839205d5aa0353383e86625d3bcb4637c609fdc3b2fd1130af7c212fd6c7574)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEnrolledServices")
    def put_enrolled_services(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FolderAccessApprovalSettingsEnrolledServices", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db30a91279084311d29e5b359e440f50f5b5303df4c231e334d511457b51f580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnrolledServices", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#create FolderAccessApprovalSettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#delete FolderAccessApprovalSettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#update FolderAccessApprovalSettings#update}.
        '''
        value = FolderAccessApprovalSettingsTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetActiveKeyVersion")
    def reset_active_key_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveKeyVersion", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotificationEmails")
    def reset_notification_emails(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationEmails", []))

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
    @jsii.member(jsii_name="ancestorHasActiveKeyVersion")
    def ancestor_has_active_key_version(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "ancestorHasActiveKeyVersion"))

    @builtins.property
    @jsii.member(jsii_name="enrolledAncestor")
    def enrolled_ancestor(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enrolledAncestor"))

    @builtins.property
    @jsii.member(jsii_name="enrolledServices")
    def enrolled_services(self) -> "FolderAccessApprovalSettingsEnrolledServicesList":
        return typing.cast("FolderAccessApprovalSettingsEnrolledServicesList", jsii.get(self, "enrolledServices"))

    @builtins.property
    @jsii.member(jsii_name="invalidKeyVersion")
    def invalid_key_version(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "invalidKeyVersion"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FolderAccessApprovalSettingsTimeoutsOutputReference":
        return typing.cast("FolderAccessApprovalSettingsTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="activeKeyVersionInput")
    def active_key_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activeKeyVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="enrolledServicesInput")
    def enrolled_services_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FolderAccessApprovalSettingsEnrolledServices"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FolderAccessApprovalSettingsEnrolledServices"]]], jsii.get(self, "enrolledServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="folderIdInput")
    def folder_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "folderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationEmailsInput")
    def notification_emails_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationEmailsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FolderAccessApprovalSettingsTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FolderAccessApprovalSettingsTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="activeKeyVersion")
    def active_key_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activeKeyVersion"))

    @active_key_version.setter
    def active_key_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb569e3eaf95ce1f2390993ad313d88c9fedb8ef0a375f204870b99ad2875486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeKeyVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="folderId")
    def folder_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folderId"))

    @folder_id.setter
    def folder_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79cafed7109157cf080d6696640781d8e359f3e51ff5028b495fcd4df373cbbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folderId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9006d20a64604c6d072aa895050164188df36e388c76a074e1d43ecb8b19b904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationEmails")
    def notification_emails(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notificationEmails"))

    @notification_emails.setter
    def notification_emails(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e14e70c0c558e71dfab3739b86b9779ccde21db4dc75ad7a181be5a1b8ac4ff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationEmails", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.folderAccessApprovalSettings.FolderAccessApprovalSettingsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "enrolled_services": "enrolledServices",
        "folder_id": "folderId",
        "active_key_version": "activeKeyVersion",
        "id": "id",
        "notification_emails": "notificationEmails",
        "timeouts": "timeouts",
    },
)
class FolderAccessApprovalSettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        enrolled_services: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FolderAccessApprovalSettingsEnrolledServices", typing.Dict[builtins.str, typing.Any]]]],
        folder_id: builtins.str,
        active_key_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        notification_emails: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["FolderAccessApprovalSettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param enrolled_services: enrolled_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#enrolled_services FolderAccessApprovalSettings#enrolled_services}
        :param folder_id: ID of the folder of the access approval settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#folder_id FolderAccessApprovalSettings#folder_id}
        :param active_key_version: The asymmetric crypto key version to use for signing approval requests. Empty active_key_version indicates that a Google-managed key should be used for signing. This property will be ignored if set by an ancestor of the resource, and new non-empty values may not be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#active_key_version FolderAccessApprovalSettings#active_key_version}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#id FolderAccessApprovalSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_emails: A list of email addresses to which notifications relating to approval requests should be sent. Notifications relating to a resource will be sent to all emails in the settings of ancestor resources of that resource. A maximum of 50 email addresses are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#notification_emails FolderAccessApprovalSettings#notification_emails}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#timeouts FolderAccessApprovalSettings#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = FolderAccessApprovalSettingsTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6925e0469e6c9e823a78c2cf449f0996bd2e4623c7bfa0674958e26dd4bc9045)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument enrolled_services", value=enrolled_services, expected_type=type_hints["enrolled_services"])
            check_type(argname="argument folder_id", value=folder_id, expected_type=type_hints["folder_id"])
            check_type(argname="argument active_key_version", value=active_key_version, expected_type=type_hints["active_key_version"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notification_emails", value=notification_emails, expected_type=type_hints["notification_emails"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enrolled_services": enrolled_services,
            "folder_id": folder_id,
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
        if active_key_version is not None:
            self._values["active_key_version"] = active_key_version
        if id is not None:
            self._values["id"] = id
        if notification_emails is not None:
            self._values["notification_emails"] = notification_emails
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
    def enrolled_services(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FolderAccessApprovalSettingsEnrolledServices"]]:
        '''enrolled_services block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#enrolled_services FolderAccessApprovalSettings#enrolled_services}
        '''
        result = self._values.get("enrolled_services")
        assert result is not None, "Required property 'enrolled_services' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FolderAccessApprovalSettingsEnrolledServices"]], result)

    @builtins.property
    def folder_id(self) -> builtins.str:
        '''ID of the folder of the access approval settings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#folder_id FolderAccessApprovalSettings#folder_id}
        '''
        result = self._values.get("folder_id")
        assert result is not None, "Required property 'folder_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active_key_version(self) -> typing.Optional[builtins.str]:
        '''The asymmetric crypto key version to use for signing approval requests.

        Empty active_key_version indicates that a Google-managed key should be used for signing.
        This property will be ignored if set by an ancestor of the resource, and new non-empty values may not be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#active_key_version FolderAccessApprovalSettings#active_key_version}
        '''
        result = self._values.get("active_key_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#id FolderAccessApprovalSettings#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_emails(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of email addresses to which notifications relating to approval requests should be sent.

        Notifications relating to a resource will be sent to all emails in the settings of ancestor
        resources of that resource. A maximum of 50 email addresses are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#notification_emails FolderAccessApprovalSettings#notification_emails}
        '''
        result = self._values.get("notification_emails")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FolderAccessApprovalSettingsTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#timeouts FolderAccessApprovalSettings#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FolderAccessApprovalSettingsTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FolderAccessApprovalSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.folderAccessApprovalSettings.FolderAccessApprovalSettingsEnrolledServices",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_product": "cloudProduct",
        "enrollment_level": "enrollmentLevel",
    },
)
class FolderAccessApprovalSettingsEnrolledServices:
    def __init__(
        self,
        *,
        cloud_product: builtins.str,
        enrollment_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_product: The product for which Access Approval will be enrolled. Allowed values are listed (case-sensitive): - all - App Engine - BigQuery - Cloud Bigtable - Cloud Key Management Service - Compute Engine - Cloud Dataflow - Cloud Identity and Access Management - Cloud Pub/Sub - Cloud Storage - Persistent Disk Note: These values are supported as input, but considered a legacy format: - all - appengine.googleapis.com - bigquery.googleapis.com - bigtable.googleapis.com - cloudkms.googleapis.com - compute.googleapis.com - dataflow.googleapis.com - iam.googleapis.com - pubsub.googleapis.com - storage.googleapis.com Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#cloud_product FolderAccessApprovalSettings#cloud_product}
        :param enrollment_level: The enrollment level of the service. Default value: "BLOCK_ALL" Possible values: ["BLOCK_ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#enrollment_level FolderAccessApprovalSettings#enrollment_level}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1981aecc8a85d171fa0719fe1117bc29887709eeaae7d307ae093290746ab41)
            check_type(argname="argument cloud_product", value=cloud_product, expected_type=type_hints["cloud_product"])
            check_type(argname="argument enrollment_level", value=enrollment_level, expected_type=type_hints["enrollment_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_product": cloud_product,
        }
        if enrollment_level is not None:
            self._values["enrollment_level"] = enrollment_level

    @builtins.property
    def cloud_product(self) -> builtins.str:
        '''The product for which Access Approval will be enrolled.

        Allowed values are listed (case-sensitive):

        - all
        - App Engine
        - BigQuery
        - Cloud Bigtable
        - Cloud Key Management Service
        - Compute Engine
        - Cloud Dataflow
        - Cloud Identity and Access Management
        - Cloud Pub/Sub
        - Cloud Storage
        - Persistent Disk

        Note: These values are supported as input, but considered a legacy format:

        - all
        - appengine.googleapis.com
        - bigquery.googleapis.com
        - bigtable.googleapis.com
        - cloudkms.googleapis.com
        - compute.googleapis.com
        - dataflow.googleapis.com
        - iam.googleapis.com
        - pubsub.googleapis.com
        - storage.googleapis.com

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#cloud_product FolderAccessApprovalSettings#cloud_product}
        '''
        result = self._values.get("cloud_product")
        assert result is not None, "Required property 'cloud_product' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enrollment_level(self) -> typing.Optional[builtins.str]:
        '''The enrollment level of the service. Default value: "BLOCK_ALL" Possible values: ["BLOCK_ALL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#enrollment_level FolderAccessApprovalSettings#enrollment_level}
        '''
        result = self._values.get("enrollment_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FolderAccessApprovalSettingsEnrolledServices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FolderAccessApprovalSettingsEnrolledServicesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.folderAccessApprovalSettings.FolderAccessApprovalSettingsEnrolledServicesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__050c18fb9ec5ca863db2197bae9282284eb193560811ab2ec3a16bbaa1787fa9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FolderAccessApprovalSettingsEnrolledServicesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88539a35d84c5df0a0bdf3ced82416d979ac8ba5c6463c99e581d0f901aef6be)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FolderAccessApprovalSettingsEnrolledServicesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de693cc541ae76e9923576706f83662c7d0f4c521550cf295bc9d09b445af6f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10889c81974aa51df8a42697eae8ad8767afb4a35c4b1e99e268b49e8f4eb387)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7114914c89e05892cf7412b3781886708c45d0f64f84a832f1c58d4a5df38d1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FolderAccessApprovalSettingsEnrolledServices]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FolderAccessApprovalSettingsEnrolledServices]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FolderAccessApprovalSettingsEnrolledServices]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae76acb3051e4c8bbc855eec71ed4876e324a8dedaf950e6e6f5a66ce91b5f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FolderAccessApprovalSettingsEnrolledServicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.folderAccessApprovalSettings.FolderAccessApprovalSettingsEnrolledServicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b3ecd098ce987cea21fe9e6f475a5187d182aa1722e09f651ab533d0984dc9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnrollmentLevel")
    def reset_enrollment_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnrollmentLevel", []))

    @builtins.property
    @jsii.member(jsii_name="cloudProductInput")
    def cloud_product_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudProductInput"))

    @builtins.property
    @jsii.member(jsii_name="enrollmentLevelInput")
    def enrollment_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enrollmentLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudProduct")
    def cloud_product(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudProduct"))

    @cloud_product.setter
    def cloud_product(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53fc20c378e3b62268760881a0a0bf789b89589df5f7010461dd29f092666613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudProduct", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enrollmentLevel")
    def enrollment_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enrollmentLevel"))

    @enrollment_level.setter
    def enrollment_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d2eae0cc78dfe7a19cebc85f9aaff8897973e0660b848357f4babd82a128b58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enrollmentLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FolderAccessApprovalSettingsEnrolledServices]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FolderAccessApprovalSettingsEnrolledServices]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FolderAccessApprovalSettingsEnrolledServices]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3e7edcafbdfb050b0afd6d62015cff6c983b27c0af9dbc6e145d80993addf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.folderAccessApprovalSettings.FolderAccessApprovalSettingsTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class FolderAccessApprovalSettingsTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#create FolderAccessApprovalSettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#delete FolderAccessApprovalSettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#update FolderAccessApprovalSettings#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f8f285101ff97151e2f885aef3047a833834a64bf886073f53a4126edb0b03)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#create FolderAccessApprovalSettings#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#delete FolderAccessApprovalSettings#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/folder_access_approval_settings#update FolderAccessApprovalSettings#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FolderAccessApprovalSettingsTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FolderAccessApprovalSettingsTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.folderAccessApprovalSettings.FolderAccessApprovalSettingsTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0401ff754d4365261244a521d73c876b5a97fdf87fb9fdc90aa38c2a86578a70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dab7076d4a960b2b149bff79e9f2dc73f197f46b81f087f07cf84cc6241e3393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9babd17e037fbf2ffab53ac515ca45ea981aef71fa4c2257385018c936db6be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b2a513555cd58fb59fc0ae1fb7db9168cc13a50e03a23465fad30afd4c174c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FolderAccessApprovalSettingsTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FolderAccessApprovalSettingsTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FolderAccessApprovalSettingsTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e7cbe30eb878e1bbea6a0e37d0d25d9b88a9f29718681e7a975912c9994e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FolderAccessApprovalSettings",
    "FolderAccessApprovalSettingsConfig",
    "FolderAccessApprovalSettingsEnrolledServices",
    "FolderAccessApprovalSettingsEnrolledServicesList",
    "FolderAccessApprovalSettingsEnrolledServicesOutputReference",
    "FolderAccessApprovalSettingsTimeouts",
    "FolderAccessApprovalSettingsTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b4f2804fafd90d3e37aa0ecbe21700fc00e04b70e3fa643e263d95b939a3eb80(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    enrolled_services: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FolderAccessApprovalSettingsEnrolledServices, typing.Dict[builtins.str, typing.Any]]]],
    folder_id: builtins.str,
    active_key_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    notification_emails: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[FolderAccessApprovalSettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e839205d5aa0353383e86625d3bcb4637c609fdc3b2fd1130af7c212fd6c7574(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db30a91279084311d29e5b359e440f50f5b5303df4c231e334d511457b51f580(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FolderAccessApprovalSettingsEnrolledServices, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb569e3eaf95ce1f2390993ad313d88c9fedb8ef0a375f204870b99ad2875486(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79cafed7109157cf080d6696640781d8e359f3e51ff5028b495fcd4df373cbbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9006d20a64604c6d072aa895050164188df36e388c76a074e1d43ecb8b19b904(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14e70c0c558e71dfab3739b86b9779ccde21db4dc75ad7a181be5a1b8ac4ff8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6925e0469e6c9e823a78c2cf449f0996bd2e4623c7bfa0674958e26dd4bc9045(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enrolled_services: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FolderAccessApprovalSettingsEnrolledServices, typing.Dict[builtins.str, typing.Any]]]],
    folder_id: builtins.str,
    active_key_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    notification_emails: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[FolderAccessApprovalSettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1981aecc8a85d171fa0719fe1117bc29887709eeaae7d307ae093290746ab41(
    *,
    cloud_product: builtins.str,
    enrollment_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050c18fb9ec5ca863db2197bae9282284eb193560811ab2ec3a16bbaa1787fa9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88539a35d84c5df0a0bdf3ced82416d979ac8ba5c6463c99e581d0f901aef6be(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de693cc541ae76e9923576706f83662c7d0f4c521550cf295bc9d09b445af6f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10889c81974aa51df8a42697eae8ad8767afb4a35c4b1e99e268b49e8f4eb387(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7114914c89e05892cf7412b3781886708c45d0f64f84a832f1c58d4a5df38d1d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae76acb3051e4c8bbc855eec71ed4876e324a8dedaf950e6e6f5a66ce91b5f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FolderAccessApprovalSettingsEnrolledServices]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3ecd098ce987cea21fe9e6f475a5187d182aa1722e09f651ab533d0984dc9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fc20c378e3b62268760881a0a0bf789b89589df5f7010461dd29f092666613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d2eae0cc78dfe7a19cebc85f9aaff8897973e0660b848357f4babd82a128b58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3e7edcafbdfb050b0afd6d62015cff6c983b27c0af9dbc6e145d80993addf5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FolderAccessApprovalSettingsEnrolledServices]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f8f285101ff97151e2f885aef3047a833834a64bf886073f53a4126edb0b03(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0401ff754d4365261244a521d73c876b5a97fdf87fb9fdc90aa38c2a86578a70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab7076d4a960b2b149bff79e9f2dc73f197f46b81f087f07cf84cc6241e3393(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9babd17e037fbf2ffab53ac515ca45ea981aef71fa4c2257385018c936db6be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b2a513555cd58fb59fc0ae1fb7db9168cc13a50e03a23465fad30afd4c174c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e7cbe30eb878e1bbea6a0e37d0d25d9b88a9f29718681e7a975912c9994e2d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FolderAccessApprovalSettingsTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

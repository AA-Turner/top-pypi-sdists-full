r'''
# `google_project_access_approval_settings`

Refer to the Terraform Registry for docs: [`google_project_access_approval_settings`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings).
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


class ProjectAccessApprovalSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.projectAccessApprovalSettings.ProjectAccessApprovalSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings google_project_access_approval_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        enrolled_services: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectAccessApprovalSettingsEnrolledServices", typing.Dict[builtins.str, typing.Any]]]],
        project_id: builtins.str,
        active_key_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        notification_emails: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ProjectAccessApprovalSettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings google_project_access_approval_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enrolled_services: enrolled_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#enrolled_services ProjectAccessApprovalSettings#enrolled_services}
        :param project_id: ID of the project of the access approval settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#project_id ProjectAccessApprovalSettings#project_id}
        :param active_key_version: The asymmetric crypto key version to use for signing approval requests. Empty active_key_version indicates that a Google-managed key should be used for signing. This property will be ignored if set by an ancestor of the resource, and new non-empty values may not be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#active_key_version ProjectAccessApprovalSettings#active_key_version}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#id ProjectAccessApprovalSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_emails: A list of email addresses to which notifications relating to approval requests should be sent. Notifications relating to a resource will be sent to all emails in the settings of ancestor resources of that resource. A maximum of 50 email addresses are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#notification_emails ProjectAccessApprovalSettings#notification_emails}
        :param project: Project id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#project ProjectAccessApprovalSettings#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#timeouts ProjectAccessApprovalSettings#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccdd13e8809c64632f7573b0d3fc9d3f5f2ac8984c7f74dd14fe0ab54c822bdc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ProjectAccessApprovalSettingsConfig(
            enrolled_services=enrolled_services,
            project_id=project_id,
            active_key_version=active_key_version,
            id=id,
            notification_emails=notification_emails,
            project=project,
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
        '''Generates CDKTF code for importing a ProjectAccessApprovalSettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ProjectAccessApprovalSettings to import.
        :param import_from_id: The id of the existing ProjectAccessApprovalSettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ProjectAccessApprovalSettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab4e60a3ac435b3736e5adde5df45ffa241ef7e58c917e6212f18f88b55e4f65)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEnrolledServices")
    def put_enrolled_services(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectAccessApprovalSettingsEnrolledServices", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8abc5c4e259588a54ca63dcb21274195b835124f9eabd9ed1d475e74a50bf3da)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#create ProjectAccessApprovalSettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#delete ProjectAccessApprovalSettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#update ProjectAccessApprovalSettings#update}.
        '''
        value = ProjectAccessApprovalSettingsTimeouts(
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

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    def enrolled_services(self) -> "ProjectAccessApprovalSettingsEnrolledServicesList":
        return typing.cast("ProjectAccessApprovalSettingsEnrolledServicesList", jsii.get(self, "enrolledServices"))

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
    def timeouts(self) -> "ProjectAccessApprovalSettingsTimeoutsOutputReference":
        return typing.cast("ProjectAccessApprovalSettingsTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="activeKeyVersionInput")
    def active_key_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activeKeyVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="enrolledServicesInput")
    def enrolled_services_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectAccessApprovalSettingsEnrolledServices"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectAccessApprovalSettingsEnrolledServices"]]], jsii.get(self, "enrolledServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationEmailsInput")
    def notification_emails_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationEmailsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ProjectAccessApprovalSettingsTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ProjectAccessApprovalSettingsTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="activeKeyVersion")
    def active_key_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activeKeyVersion"))

    @active_key_version.setter
    def active_key_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a25295da013d867fbe212dccaf9d17a0cef3b6e2973787c513ef4f231b9208bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeKeyVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d69fa7eb68a7338d34cfece0c40e55f097571fbb2267be4436c991bd1fe7a8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationEmails")
    def notification_emails(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notificationEmails"))

    @notification_emails.setter
    def notification_emails(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__807de479f33c7ef1fe469f47ed205b9b549e599b155890383d588091d02a6745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationEmails", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c5294ccd1895781568994e0811893f31b526f7bcc0b4fa68899d0696982cb5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5113509bcc746d4f4ab6e5008de9aff99b3e2df95e838189470af51117257bfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.projectAccessApprovalSettings.ProjectAccessApprovalSettingsConfig",
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
        "project_id": "projectId",
        "active_key_version": "activeKeyVersion",
        "id": "id",
        "notification_emails": "notificationEmails",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class ProjectAccessApprovalSettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        enrolled_services: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectAccessApprovalSettingsEnrolledServices", typing.Dict[builtins.str, typing.Any]]]],
        project_id: builtins.str,
        active_key_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        notification_emails: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ProjectAccessApprovalSettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param enrolled_services: enrolled_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#enrolled_services ProjectAccessApprovalSettings#enrolled_services}
        :param project_id: ID of the project of the access approval settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#project_id ProjectAccessApprovalSettings#project_id}
        :param active_key_version: The asymmetric crypto key version to use for signing approval requests. Empty active_key_version indicates that a Google-managed key should be used for signing. This property will be ignored if set by an ancestor of the resource, and new non-empty values may not be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#active_key_version ProjectAccessApprovalSettings#active_key_version}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#id ProjectAccessApprovalSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_emails: A list of email addresses to which notifications relating to approval requests should be sent. Notifications relating to a resource will be sent to all emails in the settings of ancestor resources of that resource. A maximum of 50 email addresses are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#notification_emails ProjectAccessApprovalSettings#notification_emails}
        :param project: Project id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#project ProjectAccessApprovalSettings#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#timeouts ProjectAccessApprovalSettings#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ProjectAccessApprovalSettingsTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c69ce7b1f68a12c1406794d81703d27602373c9c391478949d204f8f2153a5f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument enrolled_services", value=enrolled_services, expected_type=type_hints["enrolled_services"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument active_key_version", value=active_key_version, expected_type=type_hints["active_key_version"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notification_emails", value=notification_emails, expected_type=type_hints["notification_emails"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enrolled_services": enrolled_services,
            "project_id": project_id,
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
        if project is not None:
            self._values["project"] = project
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectAccessApprovalSettingsEnrolledServices"]]:
        '''enrolled_services block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#enrolled_services ProjectAccessApprovalSettings#enrolled_services}
        '''
        result = self._values.get("enrolled_services")
        assert result is not None, "Required property 'enrolled_services' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectAccessApprovalSettingsEnrolledServices"]], result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''ID of the project of the access approval settings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#project_id ProjectAccessApprovalSettings#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active_key_version(self) -> typing.Optional[builtins.str]:
        '''The asymmetric crypto key version to use for signing approval requests.

        Empty active_key_version indicates that a Google-managed key should be used for signing.
        This property will be ignored if set by an ancestor of the resource, and new non-empty values may not be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#active_key_version ProjectAccessApprovalSettings#active_key_version}
        '''
        result = self._values.get("active_key_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#id ProjectAccessApprovalSettings#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#notification_emails ProjectAccessApprovalSettings#notification_emails}
        '''
        result = self._values.get("notification_emails")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Project id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#project ProjectAccessApprovalSettings#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ProjectAccessApprovalSettingsTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#timeouts ProjectAccessApprovalSettings#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ProjectAccessApprovalSettingsTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectAccessApprovalSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.projectAccessApprovalSettings.ProjectAccessApprovalSettingsEnrolledServices",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_product": "cloudProduct",
        "enrollment_level": "enrollmentLevel",
    },
)
class ProjectAccessApprovalSettingsEnrolledServices:
    def __init__(
        self,
        *,
        cloud_product: builtins.str,
        enrollment_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_product: The product for which Access Approval will be enrolled. Allowed values are listed (case-sensitive): all appengine.googleapis.com bigquery.googleapis.com bigtable.googleapis.com cloudkms.googleapis.com compute.googleapis.com dataflow.googleapis.com iam.googleapis.com pubsub.googleapis.com storage.googleapis.com Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#cloud_product ProjectAccessApprovalSettings#cloud_product}
        :param enrollment_level: The enrollment level of the service. Default value: "BLOCK_ALL" Possible values: ["BLOCK_ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#enrollment_level ProjectAccessApprovalSettings#enrollment_level}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0650665416f289d9f0953754e6e123942e3152c34b87e70f64fe69ebf3b0d2a8)
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
        all
        appengine.googleapis.com
        bigquery.googleapis.com
        bigtable.googleapis.com
        cloudkms.googleapis.com
        compute.googleapis.com
        dataflow.googleapis.com
        iam.googleapis.com
        pubsub.googleapis.com
        storage.googleapis.com

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#cloud_product ProjectAccessApprovalSettings#cloud_product}
        '''
        result = self._values.get("cloud_product")
        assert result is not None, "Required property 'cloud_product' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enrollment_level(self) -> typing.Optional[builtins.str]:
        '''The enrollment level of the service. Default value: "BLOCK_ALL" Possible values: ["BLOCK_ALL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#enrollment_level ProjectAccessApprovalSettings#enrollment_level}
        '''
        result = self._values.get("enrollment_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectAccessApprovalSettingsEnrolledServices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectAccessApprovalSettingsEnrolledServicesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.projectAccessApprovalSettings.ProjectAccessApprovalSettingsEnrolledServicesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2d510a99169057c328fd5fdc91d87def8ce670735ee5de6f6b637f8950ee94b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ProjectAccessApprovalSettingsEnrolledServicesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b28fedeb558fcae5654fb071595a8c5dd55a2319cee4b59b4db6bcaeb8cb4fd8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProjectAccessApprovalSettingsEnrolledServicesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e83ea0dbd6450ce4c5643b0afed98cab2237ba7122b282f9d2d5aa811dc46363)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdfae05bd9005d537c467d11fef3cb2a9f1728a40fab87b385fd00054bfb7691)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d85148c37728157af76bf3cf07e22e96a17cd4de862581e7e0271ba41545908f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectAccessApprovalSettingsEnrolledServices]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectAccessApprovalSettingsEnrolledServices]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectAccessApprovalSettingsEnrolledServices]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1eac15cace9d6ca1b57171de53f40c6bef9fe1580a7d2d61467d98fbed5cd6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProjectAccessApprovalSettingsEnrolledServicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.projectAccessApprovalSettings.ProjectAccessApprovalSettingsEnrolledServicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77c826095a3ec0312956a11aee256964a513e3da93ea3c225f7545e472226e2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b930b48b32b33ae4d3548cffdbee675818d440ffca24a9bd2b21b002ad53eaca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudProduct", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enrollmentLevel")
    def enrollment_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enrollmentLevel"))

    @enrollment_level.setter
    def enrollment_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e17e5557fd540106b2dd087c3f9217060a0c6fb873ce871d54503a2493bb006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enrollmentLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectAccessApprovalSettingsEnrolledServices]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectAccessApprovalSettingsEnrolledServices]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectAccessApprovalSettingsEnrolledServices]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adb85b62fdfaae259a7915704173a1ec1992dbf87aa99e12d5008f8649512ac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.projectAccessApprovalSettings.ProjectAccessApprovalSettingsTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ProjectAccessApprovalSettingsTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#create ProjectAccessApprovalSettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#delete ProjectAccessApprovalSettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#update ProjectAccessApprovalSettings#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__706676d070addadb2861852ad9607acbfaa8bb9aa63f9b4784343b5879438a1d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#create ProjectAccessApprovalSettings#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#delete ProjectAccessApprovalSettings#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/project_access_approval_settings#update ProjectAccessApprovalSettings#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectAccessApprovalSettingsTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectAccessApprovalSettingsTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.projectAccessApprovalSettings.ProjectAccessApprovalSettingsTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b79e7df4f850c6ed724282878a0768925aed9ad378b007de82095a9d9af95262)
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
            type_hints = typing.get_type_hints(_typecheckingstub__637e1f6cd88a2363ac3c8a3b3f5f917eba0238695166766397208817245eac03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6e26b0cadb357d933a5d005c71680586ef7e3787c557bc606e9670fc1da09b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da49dd0b1795760da67022b054d69ea91b169db64011425c760536a9e8ee024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectAccessApprovalSettingsTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectAccessApprovalSettingsTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectAccessApprovalSettingsTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb40e0fe501ac315e73b77a46cb94d76c2a0005b519fe84dfd697ba7ed7f0bf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ProjectAccessApprovalSettings",
    "ProjectAccessApprovalSettingsConfig",
    "ProjectAccessApprovalSettingsEnrolledServices",
    "ProjectAccessApprovalSettingsEnrolledServicesList",
    "ProjectAccessApprovalSettingsEnrolledServicesOutputReference",
    "ProjectAccessApprovalSettingsTimeouts",
    "ProjectAccessApprovalSettingsTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ccdd13e8809c64632f7573b0d3fc9d3f5f2ac8984c7f74dd14fe0ab54c822bdc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    enrolled_services: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectAccessApprovalSettingsEnrolledServices, typing.Dict[builtins.str, typing.Any]]]],
    project_id: builtins.str,
    active_key_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    notification_emails: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ProjectAccessApprovalSettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ab4e60a3ac435b3736e5adde5df45ffa241ef7e58c917e6212f18f88b55e4f65(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8abc5c4e259588a54ca63dcb21274195b835124f9eabd9ed1d475e74a50bf3da(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectAccessApprovalSettingsEnrolledServices, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25295da013d867fbe212dccaf9d17a0cef3b6e2973787c513ef4f231b9208bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d69fa7eb68a7338d34cfece0c40e55f097571fbb2267be4436c991bd1fe7a8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807de479f33c7ef1fe469f47ed205b9b549e599b155890383d588091d02a6745(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5294ccd1895781568994e0811893f31b526f7bcc0b4fa68899d0696982cb5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5113509bcc746d4f4ab6e5008de9aff99b3e2df95e838189470af51117257bfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c69ce7b1f68a12c1406794d81703d27602373c9c391478949d204f8f2153a5f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enrolled_services: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectAccessApprovalSettingsEnrolledServices, typing.Dict[builtins.str, typing.Any]]]],
    project_id: builtins.str,
    active_key_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    notification_emails: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ProjectAccessApprovalSettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0650665416f289d9f0953754e6e123942e3152c34b87e70f64fe69ebf3b0d2a8(
    *,
    cloud_product: builtins.str,
    enrollment_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d510a99169057c328fd5fdc91d87def8ce670735ee5de6f6b637f8950ee94b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28fedeb558fcae5654fb071595a8c5dd55a2319cee4b59b4db6bcaeb8cb4fd8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83ea0dbd6450ce4c5643b0afed98cab2237ba7122b282f9d2d5aa811dc46363(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdfae05bd9005d537c467d11fef3cb2a9f1728a40fab87b385fd00054bfb7691(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85148c37728157af76bf3cf07e22e96a17cd4de862581e7e0271ba41545908f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1eac15cace9d6ca1b57171de53f40c6bef9fe1580a7d2d61467d98fbed5cd6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectAccessApprovalSettingsEnrolledServices]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c826095a3ec0312956a11aee256964a513e3da93ea3c225f7545e472226e2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b930b48b32b33ae4d3548cffdbee675818d440ffca24a9bd2b21b002ad53eaca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e17e5557fd540106b2dd087c3f9217060a0c6fb873ce871d54503a2493bb006(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb85b62fdfaae259a7915704173a1ec1992dbf87aa99e12d5008f8649512ac4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectAccessApprovalSettingsEnrolledServices]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__706676d070addadb2861852ad9607acbfaa8bb9aa63f9b4784343b5879438a1d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79e7df4f850c6ed724282878a0768925aed9ad378b007de82095a9d9af95262(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637e1f6cd88a2363ac3c8a3b3f5f917eba0238695166766397208817245eac03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6e26b0cadb357d933a5d005c71680586ef7e3787c557bc606e9670fc1da09b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da49dd0b1795760da67022b054d69ea91b169db64011425c760536a9e8ee024(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb40e0fe501ac315e73b77a46cb94d76c2a0005b519fe84dfd697ba7ed7f0bf7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectAccessApprovalSettingsTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

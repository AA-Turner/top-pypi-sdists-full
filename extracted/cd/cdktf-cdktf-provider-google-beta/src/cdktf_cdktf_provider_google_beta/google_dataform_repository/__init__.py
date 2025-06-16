r'''
# `google_dataform_repository`

Refer to the Terraform Registry for docs: [`google_dataform_repository`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository).
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


class GoogleDataformRepository(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepository",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository google_dataform_repository}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        deletion_policy: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        git_remote_settings: typing.Optional[typing.Union["GoogleDataformRepositoryGitRemoteSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        npmrc_environment_variables_secret_version: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataformRepositoryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workspace_compilation_overrides: typing.Optional[typing.Union["GoogleDataformRepositoryWorkspaceCompilationOverrides", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository google_dataform_repository} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The repository's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#name GoogleDataformRepository#name}
        :param deletion_policy: Policy to control how the repository and its child resources are deleted. When set to 'FORCE', any child resources of this repository will also be deleted. Possible values: 'DELETE', 'FORCE'. Defaults to 'DELETE'. Default value: "DELETE" Possible values: ["DELETE", "FORCE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#deletion_policy GoogleDataformRepository#deletion_policy}
        :param display_name: Optional. The repository's user-friendly name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#display_name GoogleDataformRepository#display_name}
        :param git_remote_settings: git_remote_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#git_remote_settings GoogleDataformRepository#git_remote_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#id GoogleDataformRepository#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: Optional. The reference to a KMS encryption key. If provided, it will be used to encrypt user data in the repository and all child resources. It is not possible to add or update the encryption key after the repository is created. Example projects/[kms_project_id]/locations/[region]/keyRings/[key_region]/cryptoKeys/[key] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#kms_key_name GoogleDataformRepository#kms_key_name}
        :param labels: Optional. Repository user labels. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#labels GoogleDataformRepository#labels}
        :param npmrc_environment_variables_secret_version: Optional. The name of the Secret Manager secret version to be used to interpolate variables into the .npmrc file for package installation operations. Must be in the format projects/* /secrets/* /versions/*. The file itself must be in a JSON format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#npmrc_environment_variables_secret_version GoogleDataformRepository#npmrc_environment_variables_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#project GoogleDataformRepository#project}.
        :param region: A reference to the region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#region GoogleDataformRepository#region}
        :param service_account: The service account to run workflow invocations under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#service_account GoogleDataformRepository#service_account}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#timeouts GoogleDataformRepository#timeouts}
        :param workspace_compilation_overrides: workspace_compilation_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#workspace_compilation_overrides GoogleDataformRepository#workspace_compilation_overrides}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2dbd824e559816fa9aa1a41d21f96fb5232e9bbae6a2495bc5c0d34376681af)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataformRepositoryConfig(
            name=name,
            deletion_policy=deletion_policy,
            display_name=display_name,
            git_remote_settings=git_remote_settings,
            id=id,
            kms_key_name=kms_key_name,
            labels=labels,
            npmrc_environment_variables_secret_version=npmrc_environment_variables_secret_version,
            project=project,
            region=region,
            service_account=service_account,
            timeouts=timeouts,
            workspace_compilation_overrides=workspace_compilation_overrides,
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
        '''Generates CDKTF code for importing a GoogleDataformRepository resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataformRepository to import.
        :param import_from_id: The id of the existing GoogleDataformRepository that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataformRepository to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4982b3250d3f8e3309c956a1e0230b848f9a370e78b482ff83448ba2fdf4f225)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putGitRemoteSettings")
    def put_git_remote_settings(
        self,
        *,
        default_branch: builtins.str,
        url: builtins.str,
        authentication_token_secret_version: typing.Optional[builtins.str] = None,
        ssh_authentication_config: typing.Optional[typing.Union["GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_branch: The Git remote's default branch name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#default_branch GoogleDataformRepository#default_branch}
        :param url: The Git remote's URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#url GoogleDataformRepository#url}
        :param authentication_token_secret_version: The name of the Secret Manager secret version to use as an authentication token for Git operations. This secret is for assigning with HTTPS only(for SSH use 'ssh_authentication_config'). Must be in the format projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#authentication_token_secret_version GoogleDataformRepository#authentication_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param ssh_authentication_config: ssh_authentication_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#ssh_authentication_config GoogleDataformRepository#ssh_authentication_config}
        '''
        value = GoogleDataformRepositoryGitRemoteSettings(
            default_branch=default_branch,
            url=url,
            authentication_token_secret_version=authentication_token_secret_version,
            ssh_authentication_config=ssh_authentication_config,
        )

        return typing.cast(None, jsii.invoke(self, "putGitRemoteSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#create GoogleDataformRepository#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#delete GoogleDataformRepository#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#update GoogleDataformRepository#update}.
        '''
        value = GoogleDataformRepositoryTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWorkspaceCompilationOverrides")
    def put_workspace_compilation_overrides(
        self,
        *,
        default_database: typing.Optional[builtins.str] = None,
        schema_suffix: typing.Optional[builtins.str] = None,
        table_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_database: The default database (Google Cloud project ID). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#default_database GoogleDataformRepository#default_database}
        :param schema_suffix: The suffix that should be appended to all schema (BigQuery dataset ID) names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#schema_suffix GoogleDataformRepository#schema_suffix}
        :param table_prefix: The prefix that should be prepended to all table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#table_prefix GoogleDataformRepository#table_prefix}
        '''
        value = GoogleDataformRepositoryWorkspaceCompilationOverrides(
            default_database=default_database,
            schema_suffix=schema_suffix,
            table_prefix=table_prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putWorkspaceCompilationOverrides", [value]))

    @jsii.member(jsii_name="resetDeletionPolicy")
    def reset_deletion_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionPolicy", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetGitRemoteSettings")
    def reset_git_remote_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitRemoteSettings", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetNpmrcEnvironmentVariablesSecretVersion")
    def reset_npmrc_environment_variables_secret_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNpmrcEnvironmentVariablesSecretVersion", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWorkspaceCompilationOverrides")
    def reset_workspace_compilation_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspaceCompilationOverrides", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="gitRemoteSettings")
    def git_remote_settings(
        self,
    ) -> "GoogleDataformRepositoryGitRemoteSettingsOutputReference":
        return typing.cast("GoogleDataformRepositoryGitRemoteSettingsOutputReference", jsii.get(self, "gitRemoteSettings"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDataformRepositoryTimeoutsOutputReference":
        return typing.cast("GoogleDataformRepositoryTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="workspaceCompilationOverrides")
    def workspace_compilation_overrides(
        self,
    ) -> "GoogleDataformRepositoryWorkspaceCompilationOverridesOutputReference":
        return typing.cast("GoogleDataformRepositoryWorkspaceCompilationOverridesOutputReference", jsii.get(self, "workspaceCompilationOverrides"))

    @builtins.property
    @jsii.member(jsii_name="deletionPolicyInput")
    def deletion_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deletionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gitRemoteSettingsInput")
    def git_remote_settings_input(
        self,
    ) -> typing.Optional["GoogleDataformRepositoryGitRemoteSettings"]:
        return typing.cast(typing.Optional["GoogleDataformRepositoryGitRemoteSettings"], jsii.get(self, "gitRemoteSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="npmrcEnvironmentVariablesSecretVersionInput")
    def npmrc_environment_variables_secret_version_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "npmrcEnvironmentVariablesSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataformRepositoryTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataformRepositoryTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceCompilationOverridesInput")
    def workspace_compilation_overrides_input(
        self,
    ) -> typing.Optional["GoogleDataformRepositoryWorkspaceCompilationOverrides"]:
        return typing.cast(typing.Optional["GoogleDataformRepositoryWorkspaceCompilationOverrides"], jsii.get(self, "workspaceCompilationOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionPolicy"))

    @deletion_policy.setter
    def deletion_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07326b944741ae02bed8b31803b8d3081fcdf06bbe48596cb70fcecd8b49cd9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa0b318c03a6cc27c4e41711801ac229fea4b454d657be5e9f62c5f749f34243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdab58a8336d3c636189858c8588a677dfbd052ab3c14cd40d8a49268abe669a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8674d45cd36b9f31a39b64074a76ee3997c0ad77dcb1a3d754bbdae5270095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c1846c3b2e08a8d69501f4154ace7bc32f940e3678fae0e8fd1b0b50a0dfb27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f4a057106a343e989703f7b4f95ba2b705fc513ca7ab7e2b71229b381e155b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="npmrcEnvironmentVariablesSecretVersion")
    def npmrc_environment_variables_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "npmrcEnvironmentVariablesSecretVersion"))

    @npmrc_environment_variables_secret_version.setter
    def npmrc_environment_variables_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d281090dfb6ba31c5295d851a626d13f4cf75a828fb0470ac5bec972d567fe6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "npmrcEnvironmentVariablesSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71eede5c5296a69640fb97de4b79bb9c672e8cf27c8ab290f2b532f6c87b7800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__744cc633499380c09cf18b996dc875cbfe006cccf23bcf66b03b1b203bb195b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4afafaf87a78ceeedf5f8ba317278784992d382db13f45b3188fe96a75388914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryConfig",
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
        "deletion_policy": "deletionPolicy",
        "display_name": "displayName",
        "git_remote_settings": "gitRemoteSettings",
        "id": "id",
        "kms_key_name": "kmsKeyName",
        "labels": "labels",
        "npmrc_environment_variables_secret_version": "npmrcEnvironmentVariablesSecretVersion",
        "project": "project",
        "region": "region",
        "service_account": "serviceAccount",
        "timeouts": "timeouts",
        "workspace_compilation_overrides": "workspaceCompilationOverrides",
    },
)
class GoogleDataformRepositoryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        deletion_policy: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        git_remote_settings: typing.Optional[typing.Union["GoogleDataformRepositoryGitRemoteSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        npmrc_environment_variables_secret_version: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataformRepositoryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workspace_compilation_overrides: typing.Optional[typing.Union["GoogleDataformRepositoryWorkspaceCompilationOverrides", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The repository's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#name GoogleDataformRepository#name}
        :param deletion_policy: Policy to control how the repository and its child resources are deleted. When set to 'FORCE', any child resources of this repository will also be deleted. Possible values: 'DELETE', 'FORCE'. Defaults to 'DELETE'. Default value: "DELETE" Possible values: ["DELETE", "FORCE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#deletion_policy GoogleDataformRepository#deletion_policy}
        :param display_name: Optional. The repository's user-friendly name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#display_name GoogleDataformRepository#display_name}
        :param git_remote_settings: git_remote_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#git_remote_settings GoogleDataformRepository#git_remote_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#id GoogleDataformRepository#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: Optional. The reference to a KMS encryption key. If provided, it will be used to encrypt user data in the repository and all child resources. It is not possible to add or update the encryption key after the repository is created. Example projects/[kms_project_id]/locations/[region]/keyRings/[key_region]/cryptoKeys/[key] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#kms_key_name GoogleDataformRepository#kms_key_name}
        :param labels: Optional. Repository user labels. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#labels GoogleDataformRepository#labels}
        :param npmrc_environment_variables_secret_version: Optional. The name of the Secret Manager secret version to be used to interpolate variables into the .npmrc file for package installation operations. Must be in the format projects/* /secrets/* /versions/*. The file itself must be in a JSON format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#npmrc_environment_variables_secret_version GoogleDataformRepository#npmrc_environment_variables_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#project GoogleDataformRepository#project}.
        :param region: A reference to the region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#region GoogleDataformRepository#region}
        :param service_account: The service account to run workflow invocations under. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#service_account GoogleDataformRepository#service_account}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#timeouts GoogleDataformRepository#timeouts}
        :param workspace_compilation_overrides: workspace_compilation_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#workspace_compilation_overrides GoogleDataformRepository#workspace_compilation_overrides}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(git_remote_settings, dict):
            git_remote_settings = GoogleDataformRepositoryGitRemoteSettings(**git_remote_settings)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataformRepositoryTimeouts(**timeouts)
        if isinstance(workspace_compilation_overrides, dict):
            workspace_compilation_overrides = GoogleDataformRepositoryWorkspaceCompilationOverrides(**workspace_compilation_overrides)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46292713426893130af4f48ca81b8e9914d1899beb7a04a7c673d8ef7571474b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument deletion_policy", value=deletion_policy, expected_type=type_hints["deletion_policy"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument git_remote_settings", value=git_remote_settings, expected_type=type_hints["git_remote_settings"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument npmrc_environment_variables_secret_version", value=npmrc_environment_variables_secret_version, expected_type=type_hints["npmrc_environment_variables_secret_version"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument workspace_compilation_overrides", value=workspace_compilation_overrides, expected_type=type_hints["workspace_compilation_overrides"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if deletion_policy is not None:
            self._values["deletion_policy"] = deletion_policy
        if display_name is not None:
            self._values["display_name"] = display_name
        if git_remote_settings is not None:
            self._values["git_remote_settings"] = git_remote_settings
        if id is not None:
            self._values["id"] = id
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if labels is not None:
            self._values["labels"] = labels
        if npmrc_environment_variables_secret_version is not None:
            self._values["npmrc_environment_variables_secret_version"] = npmrc_environment_variables_secret_version
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if service_account is not None:
            self._values["service_account"] = service_account
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if workspace_compilation_overrides is not None:
            self._values["workspace_compilation_overrides"] = workspace_compilation_overrides

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
        '''The repository's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#name GoogleDataformRepository#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deletion_policy(self) -> typing.Optional[builtins.str]:
        '''Policy to control how the repository and its child resources are deleted.

        When set to 'FORCE', any child resources of this repository will also be deleted. Possible values: 'DELETE', 'FORCE'. Defaults to 'DELETE'. Default value: "DELETE" Possible values: ["DELETE", "FORCE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#deletion_policy GoogleDataformRepository#deletion_policy}
        '''
        result = self._values.get("deletion_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Optional. The repository's user-friendly name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#display_name GoogleDataformRepository#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_remote_settings(
        self,
    ) -> typing.Optional["GoogleDataformRepositoryGitRemoteSettings"]:
        '''git_remote_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#git_remote_settings GoogleDataformRepository#git_remote_settings}
        '''
        result = self._values.get("git_remote_settings")
        return typing.cast(typing.Optional["GoogleDataformRepositoryGitRemoteSettings"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#id GoogleDataformRepository#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The reference to a KMS encryption key. If provided, it will be used to encrypt user data in the repository and all child resources.
        It is not possible to add or update the encryption key after the repository is created. Example projects/[kms_project_id]/locations/[region]/keyRings/[key_region]/cryptoKeys/[key]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#kms_key_name GoogleDataformRepository#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        Repository user labels.
        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#labels GoogleDataformRepository#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def npmrc_environment_variables_secret_version(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Optional.

        The name of the Secret Manager secret version to be used to interpolate variables into the .npmrc file for package installation operations. Must be in the format projects/* /secrets/* /versions/*. The file itself must be in a JSON format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#npmrc_environment_variables_secret_version GoogleDataformRepository#npmrc_environment_variables_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("npmrc_environment_variables_secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#project GoogleDataformRepository#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''A reference to the region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#region GoogleDataformRepository#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The service account to run workflow invocations under.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#service_account GoogleDataformRepository#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDataformRepositoryTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#timeouts GoogleDataformRepository#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataformRepositoryTimeouts"], result)

    @builtins.property
    def workspace_compilation_overrides(
        self,
    ) -> typing.Optional["GoogleDataformRepositoryWorkspaceCompilationOverrides"]:
        '''workspace_compilation_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#workspace_compilation_overrides GoogleDataformRepository#workspace_compilation_overrides}
        '''
        result = self._values.get("workspace_compilation_overrides")
        return typing.cast(typing.Optional["GoogleDataformRepositoryWorkspaceCompilationOverrides"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryGitRemoteSettings",
    jsii_struct_bases=[],
    name_mapping={
        "default_branch": "defaultBranch",
        "url": "url",
        "authentication_token_secret_version": "authenticationTokenSecretVersion",
        "ssh_authentication_config": "sshAuthenticationConfig",
    },
)
class GoogleDataformRepositoryGitRemoteSettings:
    def __init__(
        self,
        *,
        default_branch: builtins.str,
        url: builtins.str,
        authentication_token_secret_version: typing.Optional[builtins.str] = None,
        ssh_authentication_config: typing.Optional[typing.Union["GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_branch: The Git remote's default branch name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#default_branch GoogleDataformRepository#default_branch}
        :param url: The Git remote's URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#url GoogleDataformRepository#url}
        :param authentication_token_secret_version: The name of the Secret Manager secret version to use as an authentication token for Git operations. This secret is for assigning with HTTPS only(for SSH use 'ssh_authentication_config'). Must be in the format projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#authentication_token_secret_version GoogleDataformRepository#authentication_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param ssh_authentication_config: ssh_authentication_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#ssh_authentication_config GoogleDataformRepository#ssh_authentication_config}
        '''
        if isinstance(ssh_authentication_config, dict):
            ssh_authentication_config = GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig(**ssh_authentication_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c21af2bc6bfb3bab1f9bc417185401720314c52dbfc807d5870bf1320efd6dd)
            check_type(argname="argument default_branch", value=default_branch, expected_type=type_hints["default_branch"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument authentication_token_secret_version", value=authentication_token_secret_version, expected_type=type_hints["authentication_token_secret_version"])
            check_type(argname="argument ssh_authentication_config", value=ssh_authentication_config, expected_type=type_hints["ssh_authentication_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_branch": default_branch,
            "url": url,
        }
        if authentication_token_secret_version is not None:
            self._values["authentication_token_secret_version"] = authentication_token_secret_version
        if ssh_authentication_config is not None:
            self._values["ssh_authentication_config"] = ssh_authentication_config

    @builtins.property
    def default_branch(self) -> builtins.str:
        '''The Git remote's default branch name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#default_branch GoogleDataformRepository#default_branch}
        '''
        result = self._values.get("default_branch")
        assert result is not None, "Required property 'default_branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The Git remote's URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#url GoogleDataformRepository#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication_token_secret_version(self) -> typing.Optional[builtins.str]:
        '''The name of the Secret Manager secret version to use as an authentication token for Git operations.

        This secret is for assigning with HTTPS only(for SSH use 'ssh_authentication_config'). Must be in the format projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#authentication_token_secret_version GoogleDataformRepository#authentication_token_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("authentication_token_secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_authentication_config(
        self,
    ) -> typing.Optional["GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig"]:
        '''ssh_authentication_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#ssh_authentication_config GoogleDataformRepository#ssh_authentication_config}
        '''
        result = self._values.get("ssh_authentication_config")
        return typing.cast(typing.Optional["GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryGitRemoteSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataformRepositoryGitRemoteSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryGitRemoteSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97873d5926dd2154336fe47a5fbab943469af69a4d3b88ed9fd639545b49564c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSshAuthenticationConfig")
    def put_ssh_authentication_config(
        self,
        *,
        host_public_key: builtins.str,
        user_private_key_secret_version: builtins.str,
    ) -> None:
        '''
        :param host_public_key: Content of a public SSH key to verify an identity of a remote Git host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#host_public_key GoogleDataformRepository#host_public_key}
        :param user_private_key_secret_version: The name of the Secret Manager secret version to use as a ssh private key for Git operations. Must be in the format projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#user_private_key_secret_version GoogleDataformRepository#user_private_key_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig(
            host_public_key=host_public_key,
            user_private_key_secret_version=user_private_key_secret_version,
        )

        return typing.cast(None, jsii.invoke(self, "putSshAuthenticationConfig", [value]))

    @jsii.member(jsii_name="resetAuthenticationTokenSecretVersion")
    def reset_authentication_token_secret_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationTokenSecretVersion", []))

    @jsii.member(jsii_name="resetSshAuthenticationConfig")
    def reset_ssh_authentication_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshAuthenticationConfig", []))

    @builtins.property
    @jsii.member(jsii_name="sshAuthenticationConfig")
    def ssh_authentication_config(
        self,
    ) -> "GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfigOutputReference":
        return typing.cast("GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfigOutputReference", jsii.get(self, "sshAuthenticationConfig"))

    @builtins.property
    @jsii.member(jsii_name="tokenStatus")
    def token_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenStatus"))

    @builtins.property
    @jsii.member(jsii_name="authenticationTokenSecretVersionInput")
    def authentication_token_secret_version_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationTokenSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBranchInput")
    def default_branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="sshAuthenticationConfigInput")
    def ssh_authentication_config_input(
        self,
    ) -> typing.Optional["GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig"]:
        return typing.cast(typing.Optional["GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig"], jsii.get(self, "sshAuthenticationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationTokenSecretVersion")
    def authentication_token_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationTokenSecretVersion"))

    @authentication_token_secret_version.setter
    def authentication_token_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a229a599e9211b12b86b14f4f3bd35ccc1d537ccdd4e44035a0f1f4d6901538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultBranch")
    def default_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBranch"))

    @default_branch.setter
    def default_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783c7f3edbc4f113d3f2f8030f9e1b541eb9fcfe76ce3f354466f2be521fcea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c7efaa8f3af0f47c4c5aad5ec4ee382c3c57cb67dba3661479611d7a03c53a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataformRepositoryGitRemoteSettings]:
        return typing.cast(typing.Optional[GoogleDataformRepositoryGitRemoteSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataformRepositoryGitRemoteSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed0e9b2e2577a2ba5242aedfcdf814880d69c5bd7dc2f5ae13966b24bf118ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "host_public_key": "hostPublicKey",
        "user_private_key_secret_version": "userPrivateKeySecretVersion",
    },
)
class GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig:
    def __init__(
        self,
        *,
        host_public_key: builtins.str,
        user_private_key_secret_version: builtins.str,
    ) -> None:
        '''
        :param host_public_key: Content of a public SSH key to verify an identity of a remote Git host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#host_public_key GoogleDataformRepository#host_public_key}
        :param user_private_key_secret_version: The name of the Secret Manager secret version to use as a ssh private key for Git operations. Must be in the format projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#user_private_key_secret_version GoogleDataformRepository#user_private_key_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d53b6faccf7338eb4eb93627bac1a3fad25d30e48e8e26e847ee708ffaaf32)
            check_type(argname="argument host_public_key", value=host_public_key, expected_type=type_hints["host_public_key"])
            check_type(argname="argument user_private_key_secret_version", value=user_private_key_secret_version, expected_type=type_hints["user_private_key_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_public_key": host_public_key,
            "user_private_key_secret_version": user_private_key_secret_version,
        }

    @builtins.property
    def host_public_key(self) -> builtins.str:
        '''Content of a public SSH key to verify an identity of a remote Git host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#host_public_key GoogleDataformRepository#host_public_key}
        '''
        result = self._values.get("host_public_key")
        assert result is not None, "Required property 'host_public_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_private_key_secret_version(self) -> builtins.str:
        '''The name of the Secret Manager secret version to use as a ssh private key for Git operations.

        Must be in the format projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#user_private_key_secret_version GoogleDataformRepository#user_private_key_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("user_private_key_secret_version")
        assert result is not None, "Required property 'user_private_key_secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bea5f6b38c299ddf96759021c8e112bea7a2b2985a18dd7bd61c7902fbf19018)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="hostPublicKeyInput")
    def host_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="userPrivateKeySecretVersionInput")
    def user_private_key_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPrivateKeySecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="hostPublicKey")
    def host_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostPublicKey"))

    @host_public_key.setter
    def host_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58de4e5125fbad18c9b063b80a69cd7a6fb14a4201a8a5f40c84a09ecc837afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostPublicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPrivateKeySecretVersion")
    def user_private_key_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPrivateKeySecretVersion"))

    @user_private_key_secret_version.setter
    def user_private_key_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394b4efe48c14b2585d775b8deeb685c57e23f39a272e97511ff01cde8409663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPrivateKeySecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig]:
        return typing.cast(typing.Optional[GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa9d8d436a7318306b7e98a065f0f1381344b65910369de7e8b940ef1fd7ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataformRepositoryTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#create GoogleDataformRepository#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#delete GoogleDataformRepository#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#update GoogleDataformRepository#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2719976fd13de943c3167e1e6739094d2ed568298a0d57656b4f8c1ca35518d5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#create GoogleDataformRepository#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#delete GoogleDataformRepository#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#update GoogleDataformRepository#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataformRepositoryTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b7f381de35bc803a505908c5d40709d47da540ac9a4efa5c335cda31d3406ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__283b11723732b3f3229e899e367657cf2cfda342929ad3c7fdf312a3b32d204f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd561d679f0123739773decaee3123635124ce0ad6fb75979c5873452bf740d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091bbe88824867d0d2d464ac5c6f801cc11555cc988d1b11a03032491f5144b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b9b463fb2ecd020cf23c10f44bf1c90ac3e794ac611b652fc86faec64dab9c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryWorkspaceCompilationOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "default_database": "defaultDatabase",
        "schema_suffix": "schemaSuffix",
        "table_prefix": "tablePrefix",
    },
)
class GoogleDataformRepositoryWorkspaceCompilationOverrides:
    def __init__(
        self,
        *,
        default_database: typing.Optional[builtins.str] = None,
        schema_suffix: typing.Optional[builtins.str] = None,
        table_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_database: The default database (Google Cloud project ID). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#default_database GoogleDataformRepository#default_database}
        :param schema_suffix: The suffix that should be appended to all schema (BigQuery dataset ID) names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#schema_suffix GoogleDataformRepository#schema_suffix}
        :param table_prefix: The prefix that should be prepended to all table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#table_prefix GoogleDataformRepository#table_prefix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cecc5f15ece6202297d034039c369da9796c3f7977e6f14fe5b93e4673192496)
            check_type(argname="argument default_database", value=default_database, expected_type=type_hints["default_database"])
            check_type(argname="argument schema_suffix", value=schema_suffix, expected_type=type_hints["schema_suffix"])
            check_type(argname="argument table_prefix", value=table_prefix, expected_type=type_hints["table_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_database is not None:
            self._values["default_database"] = default_database
        if schema_suffix is not None:
            self._values["schema_suffix"] = schema_suffix
        if table_prefix is not None:
            self._values["table_prefix"] = table_prefix

    @builtins.property
    def default_database(self) -> typing.Optional[builtins.str]:
        '''The default database (Google Cloud project ID).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#default_database GoogleDataformRepository#default_database}
        '''
        result = self._values.get("default_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_suffix(self) -> typing.Optional[builtins.str]:
        '''The suffix that should be appended to all schema (BigQuery dataset ID) names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#schema_suffix GoogleDataformRepository#schema_suffix}
        '''
        result = self._values.get("schema_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix that should be prepended to all table names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataform_repository#table_prefix GoogleDataformRepository#table_prefix}
        '''
        result = self._values.get("table_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryWorkspaceCompilationOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataformRepositoryWorkspaceCompilationOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryWorkspaceCompilationOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6384b9c375c124f95f11e9336c92d5bbce4922619dd88f6973361b8d486f17b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDefaultDatabase")
    def reset_default_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultDatabase", []))

    @jsii.member(jsii_name="resetSchemaSuffix")
    def reset_schema_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaSuffix", []))

    @jsii.member(jsii_name="resetTablePrefix")
    def reset_table_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTablePrefix", []))

    @builtins.property
    @jsii.member(jsii_name="defaultDatabaseInput")
    def default_database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultDatabaseInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaSuffixInput")
    def schema_suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaSuffixInput"))

    @builtins.property
    @jsii.member(jsii_name="tablePrefixInput")
    def table_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tablePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultDatabase")
    def default_database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultDatabase"))

    @default_database.setter
    def default_database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3279c69ac87fdabe26cef05ed908210decd1e256ea1e9223654a0ba4312b54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultDatabase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemaSuffix")
    def schema_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaSuffix"))

    @schema_suffix.setter
    def schema_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fccd0e68cdb88b87f8196a96507981f3efad94bbc9e326994243901135833e1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaSuffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tablePrefix")
    def table_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tablePrefix"))

    @table_prefix.setter
    def table_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9267a09d91c0d74eeb9d655ce38bd621c37013c8a9480927bf7bb3da611c7446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tablePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataformRepositoryWorkspaceCompilationOverrides]:
        return typing.cast(typing.Optional[GoogleDataformRepositoryWorkspaceCompilationOverrides], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataformRepositoryWorkspaceCompilationOverrides],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee928fadd0462924fe5af73d22e3f1bfb274e58b7a913f0aea24dc0332f5ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataformRepository",
    "GoogleDataformRepositoryConfig",
    "GoogleDataformRepositoryGitRemoteSettings",
    "GoogleDataformRepositoryGitRemoteSettingsOutputReference",
    "GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig",
    "GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfigOutputReference",
    "GoogleDataformRepositoryTimeouts",
    "GoogleDataformRepositoryTimeoutsOutputReference",
    "GoogleDataformRepositoryWorkspaceCompilationOverrides",
    "GoogleDataformRepositoryWorkspaceCompilationOverridesOutputReference",
]

publication.publish()

def _typecheckingstub__b2dbd824e559816fa9aa1a41d21f96fb5232e9bbae6a2495bc5c0d34376681af(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    deletion_policy: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    git_remote_settings: typing.Optional[typing.Union[GoogleDataformRepositoryGitRemoteSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    npmrc_environment_variables_secret_version: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataformRepositoryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workspace_compilation_overrides: typing.Optional[typing.Union[GoogleDataformRepositoryWorkspaceCompilationOverrides, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4982b3250d3f8e3309c956a1e0230b848f9a370e78b482ff83448ba2fdf4f225(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07326b944741ae02bed8b31803b8d3081fcdf06bbe48596cb70fcecd8b49cd9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0b318c03a6cc27c4e41711801ac229fea4b454d657be5e9f62c5f749f34243(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdab58a8336d3c636189858c8588a677dfbd052ab3c14cd40d8a49268abe669a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8674d45cd36b9f31a39b64074a76ee3997c0ad77dcb1a3d754bbdae5270095(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c1846c3b2e08a8d69501f4154ace7bc32f940e3678fae0e8fd1b0b50a0dfb27(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f4a057106a343e989703f7b4f95ba2b705fc513ca7ab7e2b71229b381e155b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d281090dfb6ba31c5295d851a626d13f4cf75a828fb0470ac5bec972d567fe6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71eede5c5296a69640fb97de4b79bb9c672e8cf27c8ab290f2b532f6c87b7800(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744cc633499380c09cf18b996dc875cbfe006cccf23bcf66b03b1b203bb195b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4afafaf87a78ceeedf5f8ba317278784992d382db13f45b3188fe96a75388914(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46292713426893130af4f48ca81b8e9914d1899beb7a04a7c673d8ef7571474b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    deletion_policy: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    git_remote_settings: typing.Optional[typing.Union[GoogleDataformRepositoryGitRemoteSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    npmrc_environment_variables_secret_version: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataformRepositoryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workspace_compilation_overrides: typing.Optional[typing.Union[GoogleDataformRepositoryWorkspaceCompilationOverrides, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c21af2bc6bfb3bab1f9bc417185401720314c52dbfc807d5870bf1320efd6dd(
    *,
    default_branch: builtins.str,
    url: builtins.str,
    authentication_token_secret_version: typing.Optional[builtins.str] = None,
    ssh_authentication_config: typing.Optional[typing.Union[GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97873d5926dd2154336fe47a5fbab943469af69a4d3b88ed9fd639545b49564c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a229a599e9211b12b86b14f4f3bd35ccc1d537ccdd4e44035a0f1f4d6901538(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783c7f3edbc4f113d3f2f8030f9e1b541eb9fcfe76ce3f354466f2be521fcea9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7efaa8f3af0f47c4c5aad5ec4ee382c3c57cb67dba3661479611d7a03c53a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed0e9b2e2577a2ba5242aedfcdf814880d69c5bd7dc2f5ae13966b24bf118ce(
    value: typing.Optional[GoogleDataformRepositoryGitRemoteSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d53b6faccf7338eb4eb93627bac1a3fad25d30e48e8e26e847ee708ffaaf32(
    *,
    host_public_key: builtins.str,
    user_private_key_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea5f6b38c299ddf96759021c8e112bea7a2b2985a18dd7bd61c7902fbf19018(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58de4e5125fbad18c9b063b80a69cd7a6fb14a4201a8a5f40c84a09ecc837afa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394b4efe48c14b2585d775b8deeb685c57e23f39a272e97511ff01cde8409663(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa9d8d436a7318306b7e98a065f0f1381344b65910369de7e8b940ef1fd7ce9(
    value: typing.Optional[GoogleDataformRepositoryGitRemoteSettingsSshAuthenticationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2719976fd13de943c3167e1e6739094d2ed568298a0d57656b4f8c1ca35518d5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7f381de35bc803a505908c5d40709d47da540ac9a4efa5c335cda31d3406ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283b11723732b3f3229e899e367657cf2cfda342929ad3c7fdf312a3b32d204f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd561d679f0123739773decaee3123635124ce0ad6fb75979c5873452bf740d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091bbe88824867d0d2d464ac5c6f801cc11555cc988d1b11a03032491f5144b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9b463fb2ecd020cf23c10f44bf1c90ac3e794ac611b652fc86faec64dab9c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cecc5f15ece6202297d034039c369da9796c3f7977e6f14fe5b93e4673192496(
    *,
    default_database: typing.Optional[builtins.str] = None,
    schema_suffix: typing.Optional[builtins.str] = None,
    table_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6384b9c375c124f95f11e9336c92d5bbce4922619dd88f6973361b8d486f17b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3279c69ac87fdabe26cef05ed908210decd1e256ea1e9223654a0ba4312b54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccd0e68cdb88b87f8196a96507981f3efad94bbc9e326994243901135833e1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9267a09d91c0d74eeb9d655ce38bd621c37013c8a9480927bf7bb3da611c7446(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee928fadd0462924fe5af73d22e3f1bfb274e58b7a913f0aea24dc0332f5ee9(
    value: typing.Optional[GoogleDataformRepositoryWorkspaceCompilationOverrides],
) -> None:
    """Type checking stubs"""
    pass

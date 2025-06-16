r'''
# `google_cloudbuildv2_connection`

Refer to the Terraform Registry for docs: [`google_cloudbuildv2_connection`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection).
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


class GoogleCloudbuildv2Connection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2Connection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection google_cloudbuildv2_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bitbucket_cloud_config: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionBitbucketCloudConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        bitbucket_data_center_config: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        github_config: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionGithubConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        github_enterprise_config: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionGithubEnterpriseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gitlab_config: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionGitlabConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection google_cloudbuildv2_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#location GoogleCloudbuildv2Connection#location}
        :param name: Immutable. The resource name of the connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#name GoogleCloudbuildv2Connection#name}
        :param annotations: Allows clients to store small amounts of arbitrary data. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#annotations GoogleCloudbuildv2Connection#annotations}
        :param bitbucket_cloud_config: bitbucket_cloud_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#bitbucket_cloud_config GoogleCloudbuildv2Connection#bitbucket_cloud_config}
        :param bitbucket_data_center_config: bitbucket_data_center_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#bitbucket_data_center_config GoogleCloudbuildv2Connection#bitbucket_data_center_config}
        :param disabled: If disabled is set to true, functionality is disabled for this connection. Repository based API methods and webhooks processing for repositories in this connection will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#disabled GoogleCloudbuildv2Connection#disabled}
        :param github_config: github_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#github_config GoogleCloudbuildv2Connection#github_config}
        :param github_enterprise_config: github_enterprise_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#github_enterprise_config GoogleCloudbuildv2Connection#github_enterprise_config}
        :param gitlab_config: gitlab_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#gitlab_config GoogleCloudbuildv2Connection#gitlab_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#id GoogleCloudbuildv2Connection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#project GoogleCloudbuildv2Connection#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#timeouts GoogleCloudbuildv2Connection#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e069a18cb840344f24faba78ec5e819a19e02d050a8feaf02ecfd3ba746987bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleCloudbuildv2ConnectionConfig(
            location=location,
            name=name,
            annotations=annotations,
            bitbucket_cloud_config=bitbucket_cloud_config,
            bitbucket_data_center_config=bitbucket_data_center_config,
            disabled=disabled,
            github_config=github_config,
            github_enterprise_config=github_enterprise_config,
            gitlab_config=gitlab_config,
            id=id,
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
        '''Generates CDKTF code for importing a GoogleCloudbuildv2Connection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleCloudbuildv2Connection to import.
        :param import_from_id: The id of the existing GoogleCloudbuildv2Connection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleCloudbuildv2Connection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b932808800b0e66ffcdf628a2229859bc4f8948ab422aa04369a4ddf5e16c6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBitbucketCloudConfig")
    def put_bitbucket_cloud_config(
        self,
        *,
        authorizer_credential: typing.Union["GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        workspace: builtins.str,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#authorizer_credential GoogleCloudbuildv2Connection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#read_authorizer_credential GoogleCloudbuildv2Connection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#webhook_secret_secret_version GoogleCloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param workspace: The Bitbucket Cloud Workspace ID to be connected to Google Cloud Platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#workspace GoogleCloudbuildv2Connection#workspace}
        '''
        value = GoogleCloudbuildv2ConnectionBitbucketCloudConfig(
            authorizer_credential=authorizer_credential,
            read_authorizer_credential=read_authorizer_credential,
            webhook_secret_secret_version=webhook_secret_secret_version,
            workspace=workspace,
        )

        return typing.cast(None, jsii.invoke(self, "putBitbucketCloudConfig", [value]))

    @jsii.member(jsii_name="putBitbucketDataCenterConfig")
    def put_bitbucket_data_center_config(
        self,
        *,
        authorizer_credential: typing.Union["GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        host_uri: builtins.str,
        read_authorizer_credential: typing.Union["GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        service_directory_config: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#authorizer_credential GoogleCloudbuildv2Connection#authorizer_credential}
        :param host_uri: The URI of the Bitbucket Data Center host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#host_uri GoogleCloudbuildv2Connection#host_uri}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#read_authorizer_credential GoogleCloudbuildv2Connection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#webhook_secret_secret_version GoogleCloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service_directory_config GoogleCloudbuildv2Connection#service_directory_config}
        :param ssl_ca: SSL certificate to use for requests to the Bitbucket Data Center. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#ssl_ca GoogleCloudbuildv2Connection#ssl_ca}
        '''
        value = GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig(
            authorizer_credential=authorizer_credential,
            host_uri=host_uri,
            read_authorizer_credential=read_authorizer_credential,
            webhook_secret_secret_version=webhook_secret_secret_version,
            service_directory_config=service_directory_config,
            ssl_ca=ssl_ca,
        )

        return typing.cast(None, jsii.invoke(self, "putBitbucketDataCenterConfig", [value]))

    @jsii.member(jsii_name="putGithubConfig")
    def put_github_config(
        self,
        *,
        app_installation_id: typing.Optional[jsii.Number] = None,
        authorizer_credential: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param app_installation_id: GitHub App installation id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#app_installation_id GoogleCloudbuildv2Connection#app_installation_id}
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#authorizer_credential GoogleCloudbuildv2Connection#authorizer_credential}
        '''
        value = GoogleCloudbuildv2ConnectionGithubConfig(
            app_installation_id=app_installation_id,
            authorizer_credential=authorizer_credential,
        )

        return typing.cast(None, jsii.invoke(self, "putGithubConfig", [value]))

    @jsii.member(jsii_name="putGithubEnterpriseConfig")
    def put_github_enterprise_config(
        self,
        *,
        host_uri: builtins.str,
        app_id: typing.Optional[jsii.Number] = None,
        app_installation_id: typing.Optional[jsii.Number] = None,
        app_slug: typing.Optional[builtins.str] = None,
        private_key_secret_version: typing.Optional[builtins.str] = None,
        service_directory_config: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
        webhook_secret_secret_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_uri: Required. The URI of the GitHub Enterprise host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#host_uri GoogleCloudbuildv2Connection#host_uri}
        :param app_id: Id of the GitHub App created from the manifest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#app_id GoogleCloudbuildv2Connection#app_id}
        :param app_installation_id: ID of the installation of the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#app_installation_id GoogleCloudbuildv2Connection#app_installation_id}
        :param app_slug: The URL-friendly name of the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#app_slug GoogleCloudbuildv2Connection#app_slug}
        :param private_key_secret_version: SecretManager resource containing the private key of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#private_key_secret_version GoogleCloudbuildv2Connection#private_key_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service_directory_config GoogleCloudbuildv2Connection#service_directory_config}
        :param ssl_ca: SSL certificate to use for requests to GitHub Enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#ssl_ca GoogleCloudbuildv2Connection#ssl_ca}
        :param webhook_secret_secret_version: SecretManager resource containing the webhook secret of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#webhook_secret_secret_version GoogleCloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleCloudbuildv2ConnectionGithubEnterpriseConfig(
            host_uri=host_uri,
            app_id=app_id,
            app_installation_id=app_installation_id,
            app_slug=app_slug,
            private_key_secret_version=private_key_secret_version,
            service_directory_config=service_directory_config,
            ssl_ca=ssl_ca,
            webhook_secret_secret_version=webhook_secret_secret_version,
        )

        return typing.cast(None, jsii.invoke(self, "putGithubEnterpriseConfig", [value]))

    @jsii.member(jsii_name="putGitlabConfig")
    def put_gitlab_config(
        self,
        *,
        authorizer_credential: typing.Union["GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        host_uri: typing.Optional[builtins.str] = None,
        service_directory_config: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#authorizer_credential GoogleCloudbuildv2Connection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#read_authorizer_credential GoogleCloudbuildv2Connection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret of a GitLab Enterprise project, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#webhook_secret_secret_version GoogleCloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param host_uri: The URI of the GitLab Enterprise host this connection is for. If not specified, the default value is https://gitlab.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#host_uri GoogleCloudbuildv2Connection#host_uri}
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service_directory_config GoogleCloudbuildv2Connection#service_directory_config}
        :param ssl_ca: SSL certificate to use for requests to GitLab Enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#ssl_ca GoogleCloudbuildv2Connection#ssl_ca}
        '''
        value = GoogleCloudbuildv2ConnectionGitlabConfig(
            authorizer_credential=authorizer_credential,
            read_authorizer_credential=read_authorizer_credential,
            webhook_secret_secret_version=webhook_secret_secret_version,
            host_uri=host_uri,
            service_directory_config=service_directory_config,
            ssl_ca=ssl_ca,
        )

        return typing.cast(None, jsii.invoke(self, "putGitlabConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#create GoogleCloudbuildv2Connection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#delete GoogleCloudbuildv2Connection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#update GoogleCloudbuildv2Connection#update}.
        '''
        value = GoogleCloudbuildv2ConnectionTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetBitbucketCloudConfig")
    def reset_bitbucket_cloud_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBitbucketCloudConfig", []))

    @jsii.member(jsii_name="resetBitbucketDataCenterConfig")
    def reset_bitbucket_data_center_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBitbucketDataCenterConfig", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetGithubConfig")
    def reset_github_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithubConfig", []))

    @jsii.member(jsii_name="resetGithubEnterpriseConfig")
    def reset_github_enterprise_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithubEnterpriseConfig", []))

    @jsii.member(jsii_name="resetGitlabConfig")
    def reset_gitlab_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitlabConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="bitbucketCloudConfig")
    def bitbucket_cloud_config(
        self,
    ) -> "GoogleCloudbuildv2ConnectionBitbucketCloudConfigOutputReference":
        return typing.cast("GoogleCloudbuildv2ConnectionBitbucketCloudConfigOutputReference", jsii.get(self, "bitbucketCloudConfig"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketDataCenterConfig")
    def bitbucket_data_center_config(
        self,
    ) -> "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigOutputReference":
        return typing.cast("GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigOutputReference", jsii.get(self, "bitbucketDataCenterConfig"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="githubConfig")
    def github_config(
        self,
    ) -> "GoogleCloudbuildv2ConnectionGithubConfigOutputReference":
        return typing.cast("GoogleCloudbuildv2ConnectionGithubConfigOutputReference", jsii.get(self, "githubConfig"))

    @builtins.property
    @jsii.member(jsii_name="githubEnterpriseConfig")
    def github_enterprise_config(
        self,
    ) -> "GoogleCloudbuildv2ConnectionGithubEnterpriseConfigOutputReference":
        return typing.cast("GoogleCloudbuildv2ConnectionGithubEnterpriseConfigOutputReference", jsii.get(self, "githubEnterpriseConfig"))

    @builtins.property
    @jsii.member(jsii_name="gitlabConfig")
    def gitlab_config(
        self,
    ) -> "GoogleCloudbuildv2ConnectionGitlabConfigOutputReference":
        return typing.cast("GoogleCloudbuildv2ConnectionGitlabConfigOutputReference", jsii.get(self, "gitlabConfig"))

    @builtins.property
    @jsii.member(jsii_name="installationState")
    def installation_state(self) -> "GoogleCloudbuildv2ConnectionInstallationStateList":
        return typing.cast("GoogleCloudbuildv2ConnectionInstallationStateList", jsii.get(self, "installationState"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleCloudbuildv2ConnectionTimeoutsOutputReference":
        return typing.cast("GoogleCloudbuildv2ConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketCloudConfigInput")
    def bitbucket_cloud_config_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionBitbucketCloudConfig"]:
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionBitbucketCloudConfig"], jsii.get(self, "bitbucketCloudConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketDataCenterConfigInput")
    def bitbucket_data_center_config_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig"]:
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig"], jsii.get(self, "bitbucketDataCenterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="githubConfigInput")
    def github_config_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionGithubConfig"]:
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionGithubConfig"], jsii.get(self, "githubConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="githubEnterpriseConfigInput")
    def github_enterprise_config_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionGithubEnterpriseConfig"]:
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionGithubEnterpriseConfig"], jsii.get(self, "githubEnterpriseConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gitlabConfigInput")
    def gitlab_config_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionGitlabConfig"]:
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionGitlabConfig"], jsii.get(self, "gitlabConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudbuildv2ConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudbuildv2ConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caaa7a20f58e7e0953062a1c0b84a5c99c32dc28f002a96a1194eab8b35ebeb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c7c20470334e0b007159b4a84919f36f91be0e716e9fb3c1ad59140eca5911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a74cbb01716399ebb7120d52792cf3b1502db208cb7248b2a56444ee05e732e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e6cc99be65bd60a761dfcc8b4f4a25fb0144fb0ead3171ed690be73fa79029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adedb2733bbdec57df730333e12d4832acec5481f5df1036b2a23271e420a6c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b6c50da6e792d48e305143ad151beae1a7f11e7536421adf8f7d7580262dcfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionBitbucketCloudConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_credential": "authorizerCredential",
        "read_authorizer_credential": "readAuthorizerCredential",
        "webhook_secret_secret_version": "webhookSecretSecretVersion",
        "workspace": "workspace",
    },
)
class GoogleCloudbuildv2ConnectionBitbucketCloudConfig:
    def __init__(
        self,
        *,
        authorizer_credential: typing.Union["GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        workspace: builtins.str,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#authorizer_credential GoogleCloudbuildv2Connection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#read_authorizer_credential GoogleCloudbuildv2Connection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#webhook_secret_secret_version GoogleCloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param workspace: The Bitbucket Cloud Workspace ID to be connected to Google Cloud Platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#workspace GoogleCloudbuildv2Connection#workspace}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential(**authorizer_credential)
        if isinstance(read_authorizer_credential, dict):
            read_authorizer_credential = GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential(**read_authorizer_credential)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eba5c43495f346879f0121059dcb4cb9ed006b5a53949ee5354bfefaf998536c)
            check_type(argname="argument authorizer_credential", value=authorizer_credential, expected_type=type_hints["authorizer_credential"])
            check_type(argname="argument read_authorizer_credential", value=read_authorizer_credential, expected_type=type_hints["read_authorizer_credential"])
            check_type(argname="argument webhook_secret_secret_version", value=webhook_secret_secret_version, expected_type=type_hints["webhook_secret_secret_version"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorizer_credential": authorizer_credential,
            "read_authorizer_credential": read_authorizer_credential,
            "webhook_secret_secret_version": webhook_secret_secret_version,
            "workspace": workspace,
        }

    @builtins.property
    def authorizer_credential(
        self,
    ) -> "GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential":
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#authorizer_credential GoogleCloudbuildv2Connection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        assert result is not None, "Required property 'authorizer_credential' is missing"
        return typing.cast("GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential", result)

    @builtins.property
    def read_authorizer_credential(
        self,
    ) -> "GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential":
        '''read_authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#read_authorizer_credential GoogleCloudbuildv2Connection#read_authorizer_credential}
        '''
        result = self._values.get("read_authorizer_credential")
        assert result is not None, "Required property 'read_authorizer_credential' is missing"
        return typing.cast("GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential", result)

    @builtins.property
    def webhook_secret_secret_version(self) -> builtins.str:
        '''Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#webhook_secret_secret_version GoogleCloudbuildv2Connection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        assert result is not None, "Required property 'webhook_secret_secret_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace(self) -> builtins.str:
        '''The Bitbucket Cloud Workspace ID to be connected to Google Cloud Platform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#workspace GoogleCloudbuildv2Connection#workspace}
        '''
        result = self._values.get("workspace")
        assert result is not None, "Required property 'workspace' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionBitbucketCloudConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65b7f1d36cfadeb89014318f4461a7326b4efaef8910f8fe770570a9409751e5)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("user_token_secret_version")
        assert result is not None, "Required property 'user_token_secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0281720ed30272307478e90a0434d3005fc0b57340ec5c149141a808d995f883)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @builtins.property
    @jsii.member(jsii_name="userTokenSecretVersionInput")
    def user_token_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userTokenSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="userTokenSecretVersion")
    def user_token_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userTokenSecretVersion"))

    @user_token_secret_version.setter
    def user_token_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8fcc87fcf3f2afad7f4e4e89d5779ec26c7c66234c7538a9fc9eb0f0257434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd7b9d4c065a2129a4cae24743f065a2e5bd95ca18384cd9252e75f389a89fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildv2ConnectionBitbucketCloudConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionBitbucketCloudConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5bd52b092c970db6925428d497854dd90492c65d12da8fd1c59373b1b433b9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorizerCredential")
    def put_authorizer_credential(
        self,
        *,
        user_token_secret_version: builtins.str,
    ) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putAuthorizerCredential", [value]))

    @jsii.member(jsii_name="putReadAuthorizerCredential")
    def put_read_authorizer_credential(
        self,
        *,
        user_token_secret_version: builtins.str,
    ) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putReadAuthorizerCredential", [value]))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredential")
    def authorizer_credential(
        self,
    ) -> GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference:
        return typing.cast(GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredential")
    def read_authorizer_credential(
        self,
    ) -> "GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference":
        return typing.cast("GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference", jsii.get(self, "readAuthorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredentialInput")
    def read_authorizer_credential_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential"]:
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential"], jsii.get(self, "readAuthorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersionInput")
    def webhook_secret_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookSecretSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceInput")
    def workspace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretSecretVersion"))

    @webhook_secret_secret_version.setter
    def webhook_secret_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e85ce909a9b7e4eb0fda65c0406985b1892935a2827a2b39bd7bd1dfd5176c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspace")
    def workspace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspace"))

    @workspace.setter
    def workspace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9763eb3784d18f838a1bbd33cc8f1264129f511e082c8e193be3a421c9bf7867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfig]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e27400dce6562b011c6945503fcccfd4fc37c557253f5e0509bd5b438cd335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__657c8d1a190d5877d04ff17898b7b1270c8796a8708177ad6f1a2b2e18a5478b)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("user_token_secret_version")
        assert result is not None, "Required property 'user_token_secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc80687f9866a0d8b07c2270e09f0452b1d5ba36da9131abb23079b68358a93c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @builtins.property
    @jsii.member(jsii_name="userTokenSecretVersionInput")
    def user_token_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userTokenSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="userTokenSecretVersion")
    def user_token_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userTokenSecretVersion"))

    @user_token_secret_version.setter
    def user_token_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3870554a8e91b4b91e07425551442ae8d4102e0d34594a6fa9da5b152a84c55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a52db4a453b3639ec72bc715684ffe81ce3e7a2ae8b26bfc85735be18c30bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_credential": "authorizerCredential",
        "host_uri": "hostUri",
        "read_authorizer_credential": "readAuthorizerCredential",
        "webhook_secret_secret_version": "webhookSecretSecretVersion",
        "service_directory_config": "serviceDirectoryConfig",
        "ssl_ca": "sslCa",
    },
)
class GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig:
    def __init__(
        self,
        *,
        authorizer_credential: typing.Union["GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        host_uri: builtins.str,
        read_authorizer_credential: typing.Union["GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        service_directory_config: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#authorizer_credential GoogleCloudbuildv2Connection#authorizer_credential}
        :param host_uri: The URI of the Bitbucket Data Center host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#host_uri GoogleCloudbuildv2Connection#host_uri}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#read_authorizer_credential GoogleCloudbuildv2Connection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#webhook_secret_secret_version GoogleCloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service_directory_config GoogleCloudbuildv2Connection#service_directory_config}
        :param ssl_ca: SSL certificate to use for requests to the Bitbucket Data Center. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#ssl_ca GoogleCloudbuildv2Connection#ssl_ca}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential(**authorizer_credential)
        if isinstance(read_authorizer_credential, dict):
            read_authorizer_credential = GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential(**read_authorizer_credential)
        if isinstance(service_directory_config, dict):
            service_directory_config = GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig(**service_directory_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__169d3b0d8e901ddb96f98679f1a895528d0ca3ec6c2acefb7771eff1c98eabf2)
            check_type(argname="argument authorizer_credential", value=authorizer_credential, expected_type=type_hints["authorizer_credential"])
            check_type(argname="argument host_uri", value=host_uri, expected_type=type_hints["host_uri"])
            check_type(argname="argument read_authorizer_credential", value=read_authorizer_credential, expected_type=type_hints["read_authorizer_credential"])
            check_type(argname="argument webhook_secret_secret_version", value=webhook_secret_secret_version, expected_type=type_hints["webhook_secret_secret_version"])
            check_type(argname="argument service_directory_config", value=service_directory_config, expected_type=type_hints["service_directory_config"])
            check_type(argname="argument ssl_ca", value=ssl_ca, expected_type=type_hints["ssl_ca"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorizer_credential": authorizer_credential,
            "host_uri": host_uri,
            "read_authorizer_credential": read_authorizer_credential,
            "webhook_secret_secret_version": webhook_secret_secret_version,
        }
        if service_directory_config is not None:
            self._values["service_directory_config"] = service_directory_config
        if ssl_ca is not None:
            self._values["ssl_ca"] = ssl_ca

    @builtins.property
    def authorizer_credential(
        self,
    ) -> "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential":
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#authorizer_credential GoogleCloudbuildv2Connection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        assert result is not None, "Required property 'authorizer_credential' is missing"
        return typing.cast("GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential", result)

    @builtins.property
    def host_uri(self) -> builtins.str:
        '''The URI of the Bitbucket Data Center host this connection is for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#host_uri GoogleCloudbuildv2Connection#host_uri}
        '''
        result = self._values.get("host_uri")
        assert result is not None, "Required property 'host_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_authorizer_credential(
        self,
    ) -> "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential":
        '''read_authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#read_authorizer_credential GoogleCloudbuildv2Connection#read_authorizer_credential}
        '''
        result = self._values.get("read_authorizer_credential")
        assert result is not None, "Required property 'read_authorizer_credential' is missing"
        return typing.cast("GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential", result)

    @builtins.property
    def webhook_secret_secret_version(self) -> builtins.str:
        '''Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#webhook_secret_secret_version GoogleCloudbuildv2Connection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        assert result is not None, "Required property 'webhook_secret_secret_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_directory_config(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig"]:
        '''service_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service_directory_config GoogleCloudbuildv2Connection#service_directory_config}
        '''
        result = self._values.get("service_directory_config")
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig"], result)

    @builtins.property
    def ssl_ca(self) -> typing.Optional[builtins.str]:
        '''SSL certificate to use for requests to the Bitbucket Data Center.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#ssl_ca GoogleCloudbuildv2Connection#ssl_ca}
        '''
        result = self._values.get("ssl_ca")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f66417e3b6c264de1b6cd4e9c16f7cab6c1a7bfad7e3fb10e6b7faa20e7c735)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("user_token_secret_version")
        assert result is not None, "Required property 'user_token_secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df8d4daa36bc9d24f6785091b1f32931977380bed1287e48534cbc7498429908)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @builtins.property
    @jsii.member(jsii_name="userTokenSecretVersionInput")
    def user_token_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userTokenSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="userTokenSecretVersion")
    def user_token_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userTokenSecretVersion"))

    @user_token_secret_version.setter
    def user_token_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b588f63ad1c0be68831f497ea04950ad7d81af337b96bffbafd5602558803e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c427c792b88da1e65817836d113f19b2bcda4c7fe208fa9b3fa772e0f731f909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b518a4b14ffc844ffad988cfd420c440a247d0454bd4ba36f60e2802a80b1270)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorizerCredential")
    def put_authorizer_credential(
        self,
        *,
        user_token_secret_version: builtins.str,
    ) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putAuthorizerCredential", [value]))

    @jsii.member(jsii_name="putReadAuthorizerCredential")
    def put_read_authorizer_credential(
        self,
        *,
        user_token_secret_version: builtins.str,
    ) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putReadAuthorizerCredential", [value]))

    @jsii.member(jsii_name="putServiceDirectoryConfig")
    def put_service_directory_config(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service GoogleCloudbuildv2Connection#service}
        '''
        value = GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig(
            service=service
        )

        return typing.cast(None, jsii.invoke(self, "putServiceDirectoryConfig", [value]))

    @jsii.member(jsii_name="resetServiceDirectoryConfig")
    def reset_service_directory_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceDirectoryConfig", []))

    @jsii.member(jsii_name="resetSslCa")
    def reset_ssl_ca(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCa", []))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredential")
    def authorizer_credential(
        self,
    ) -> GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference:
        return typing.cast(GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredential")
    def read_authorizer_credential(
        self,
    ) -> "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference":
        return typing.cast("GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference", jsii.get(self, "readAuthorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="serverVersion")
    def server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverVersion"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfig")
    def service_directory_config(
        self,
    ) -> "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference":
        return typing.cast("GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference", jsii.get(self, "serviceDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="hostUriInput")
    def host_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostUriInput"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredentialInput")
    def read_authorizer_credential_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential"]:
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential"], jsii.get(self, "readAuthorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfigInput")
    def service_directory_config_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig"]:
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig"], jsii.get(self, "serviceDirectoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCaInput")
    def ssl_ca_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCaInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersionInput")
    def webhook_secret_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookSecretSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="hostUri")
    def host_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostUri"))

    @host_uri.setter
    def host_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d97c474cb2c19feac95cb42d4ae346ec5ace9586e91b5f393d8aed9c74cdc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCa")
    def ssl_ca(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCa"))

    @ssl_ca.setter
    def ssl_ca(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b86e90a8d36692e13a9431bb0223e184f2461e925089a93ce07ee4ccf9a0ac43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretSecretVersion"))

    @webhook_secret_secret_version.setter
    def webhook_secret_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99f59c78533befd6c11e277a4c00b64a76070589224c5407c78cde6f027e5246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c054f90d6216ec1019d0d70c246c8ee0d4941053ab4d47d89c9e395fcab32d1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f5b99fd9ecb368aef70ec7d4577a81984eb73187f0ed8772c8af7d6269cd458)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("user_token_secret_version")
        assert result is not None, "Required property 'user_token_secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1fe858d162d7ffcd40245d3b95f295c46b18744a860fda09d10ce07c6e8ae99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @builtins.property
    @jsii.member(jsii_name="userTokenSecretVersionInput")
    def user_token_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userTokenSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="userTokenSecretVersion")
    def user_token_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userTokenSecretVersion"))

    @user_token_secret_version.setter
    def user_token_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc879c122e44c8c93e987175b232ab4759655a23a0f33c9ccfe67e6bda7b978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__418b5a82ac0df96ca4536870b9ea96ed3c960180e88151145971c17b31363c59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"service": "service"},
)
class GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig:
    def __init__(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service GoogleCloudbuildv2Connection#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea77e746f1ee981caed971e51a152f9dceda1c9dcf3617cbfa9d6e5aa99279f8)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service GoogleCloudbuildv2Connection#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a16b643e1e67b108f070f98f5ca6d807d79c63373b2bc911689ceaa3903355e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1ce5a03d486b1ff28333b8c98fb4a9f1251958b4d167093d7c8a2364d0d0f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3fc1083dc53eb873d56275d9b026cbf651f55a1dfa0a30e31d1e1dda534efe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "annotations": "annotations",
        "bitbucket_cloud_config": "bitbucketCloudConfig",
        "bitbucket_data_center_config": "bitbucketDataCenterConfig",
        "disabled": "disabled",
        "github_config": "githubConfig",
        "github_enterprise_config": "githubEnterpriseConfig",
        "gitlab_config": "gitlabConfig",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleCloudbuildv2ConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bitbucket_cloud_config: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionBitbucketCloudConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        bitbucket_data_center_config: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        github_config: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionGithubConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        github_enterprise_config: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionGithubEnterpriseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gitlab_config: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionGitlabConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#location GoogleCloudbuildv2Connection#location}
        :param name: Immutable. The resource name of the connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#name GoogleCloudbuildv2Connection#name}
        :param annotations: Allows clients to store small amounts of arbitrary data. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#annotations GoogleCloudbuildv2Connection#annotations}
        :param bitbucket_cloud_config: bitbucket_cloud_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#bitbucket_cloud_config GoogleCloudbuildv2Connection#bitbucket_cloud_config}
        :param bitbucket_data_center_config: bitbucket_data_center_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#bitbucket_data_center_config GoogleCloudbuildv2Connection#bitbucket_data_center_config}
        :param disabled: If disabled is set to true, functionality is disabled for this connection. Repository based API methods and webhooks processing for repositories in this connection will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#disabled GoogleCloudbuildv2Connection#disabled}
        :param github_config: github_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#github_config GoogleCloudbuildv2Connection#github_config}
        :param github_enterprise_config: github_enterprise_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#github_enterprise_config GoogleCloudbuildv2Connection#github_enterprise_config}
        :param gitlab_config: gitlab_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#gitlab_config GoogleCloudbuildv2Connection#gitlab_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#id GoogleCloudbuildv2Connection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#project GoogleCloudbuildv2Connection#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#timeouts GoogleCloudbuildv2Connection#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bitbucket_cloud_config, dict):
            bitbucket_cloud_config = GoogleCloudbuildv2ConnectionBitbucketCloudConfig(**bitbucket_cloud_config)
        if isinstance(bitbucket_data_center_config, dict):
            bitbucket_data_center_config = GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig(**bitbucket_data_center_config)
        if isinstance(github_config, dict):
            github_config = GoogleCloudbuildv2ConnectionGithubConfig(**github_config)
        if isinstance(github_enterprise_config, dict):
            github_enterprise_config = GoogleCloudbuildv2ConnectionGithubEnterpriseConfig(**github_enterprise_config)
        if isinstance(gitlab_config, dict):
            gitlab_config = GoogleCloudbuildv2ConnectionGitlabConfig(**gitlab_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleCloudbuildv2ConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__970c626ee352f9a22331f448cf4401422335f5bcf1f5e07c355ffb9021ce672a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument bitbucket_cloud_config", value=bitbucket_cloud_config, expected_type=type_hints["bitbucket_cloud_config"])
            check_type(argname="argument bitbucket_data_center_config", value=bitbucket_data_center_config, expected_type=type_hints["bitbucket_data_center_config"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument github_config", value=github_config, expected_type=type_hints["github_config"])
            check_type(argname="argument github_enterprise_config", value=github_enterprise_config, expected_type=type_hints["github_enterprise_config"])
            check_type(argname="argument gitlab_config", value=gitlab_config, expected_type=type_hints["gitlab_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if bitbucket_cloud_config is not None:
            self._values["bitbucket_cloud_config"] = bitbucket_cloud_config
        if bitbucket_data_center_config is not None:
            self._values["bitbucket_data_center_config"] = bitbucket_data_center_config
        if disabled is not None:
            self._values["disabled"] = disabled
        if github_config is not None:
            self._values["github_config"] = github_config
        if github_enterprise_config is not None:
            self._values["github_enterprise_config"] = github_enterprise_config
        if gitlab_config is not None:
            self._values["gitlab_config"] = gitlab_config
        if id is not None:
            self._values["id"] = id
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
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#location GoogleCloudbuildv2Connection#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Immutable. The resource name of the connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#name GoogleCloudbuildv2Connection#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Allows clients to store small amounts of arbitrary data.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#annotations GoogleCloudbuildv2Connection#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bitbucket_cloud_config(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfig]:
        '''bitbucket_cloud_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#bitbucket_cloud_config GoogleCloudbuildv2Connection#bitbucket_cloud_config}
        '''
        result = self._values.get("bitbucket_cloud_config")
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfig], result)

    @builtins.property
    def bitbucket_data_center_config(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig]:
        '''bitbucket_data_center_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#bitbucket_data_center_config GoogleCloudbuildv2Connection#bitbucket_data_center_config}
        '''
        result = self._values.get("bitbucket_data_center_config")
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If disabled is set to true, functionality is disabled for this connection.

        Repository based API methods and webhooks processing for repositories in this connection will be disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#disabled GoogleCloudbuildv2Connection#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def github_config(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionGithubConfig"]:
        '''github_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#github_config GoogleCloudbuildv2Connection#github_config}
        '''
        result = self._values.get("github_config")
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionGithubConfig"], result)

    @builtins.property
    def github_enterprise_config(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionGithubEnterpriseConfig"]:
        '''github_enterprise_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#github_enterprise_config GoogleCloudbuildv2Connection#github_enterprise_config}
        '''
        result = self._values.get("github_enterprise_config")
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionGithubEnterpriseConfig"], result)

    @builtins.property
    def gitlab_config(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionGitlabConfig"]:
        '''gitlab_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#gitlab_config GoogleCloudbuildv2Connection#gitlab_config}
        '''
        result = self._values.get("gitlab_config")
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionGitlabConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#id GoogleCloudbuildv2Connection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#project GoogleCloudbuildv2Connection#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleCloudbuildv2ConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#timeouts GoogleCloudbuildv2Connection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGithubConfig",
    jsii_struct_bases=[],
    name_mapping={
        "app_installation_id": "appInstallationId",
        "authorizer_credential": "authorizerCredential",
    },
)
class GoogleCloudbuildv2ConnectionGithubConfig:
    def __init__(
        self,
        *,
        app_installation_id: typing.Optional[jsii.Number] = None,
        authorizer_credential: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param app_installation_id: GitHub App installation id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#app_installation_id GoogleCloudbuildv2Connection#app_installation_id}
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#authorizer_credential GoogleCloudbuildv2Connection#authorizer_credential}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential(**authorizer_credential)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5cacfab94b991720cacf086c133513e0d7939deb4b3b199e04e982000b40e4e)
            check_type(argname="argument app_installation_id", value=app_installation_id, expected_type=type_hints["app_installation_id"])
            check_type(argname="argument authorizer_credential", value=authorizer_credential, expected_type=type_hints["authorizer_credential"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_installation_id is not None:
            self._values["app_installation_id"] = app_installation_id
        if authorizer_credential is not None:
            self._values["authorizer_credential"] = authorizer_credential

    @builtins.property
    def app_installation_id(self) -> typing.Optional[jsii.Number]:
        '''GitHub App installation id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#app_installation_id GoogleCloudbuildv2Connection#app_installation_id}
        '''
        result = self._values.get("app_installation_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def authorizer_credential(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential"]:
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#authorizer_credential GoogleCloudbuildv2Connection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionGithubConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"oauth_token_secret_version": "oauthTokenSecretVersion"},
)
class GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential:
    def __init__(
        self,
        *,
        oauth_token_secret_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param oauth_token_secret_version: A SecretManager resource containing the OAuth token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#oauth_token_secret_version GoogleCloudbuildv2Connection#oauth_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f9be218d7e53fba891ad11b7510c24af31e5ae51394ac2052914c35b13617a)
            check_type(argname="argument oauth_token_secret_version", value=oauth_token_secret_version, expected_type=type_hints["oauth_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if oauth_token_secret_version is not None:
            self._values["oauth_token_secret_version"] = oauth_token_secret_version

    @builtins.property
    def oauth_token_secret_version(self) -> typing.Optional[builtins.str]:
        '''A SecretManager resource containing the OAuth token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#oauth_token_secret_version GoogleCloudbuildv2Connection#oauth_token_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("oauth_token_secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2544d63177fa1f66014824458a80a7267b98a1f280701f0595786795f7b095ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOauthTokenSecretVersion")
    def reset_oauth_token_secret_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthTokenSecretVersion", []))

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @builtins.property
    @jsii.member(jsii_name="oauthTokenSecretVersionInput")
    def oauth_token_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthTokenSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthTokenSecretVersion")
    def oauth_token_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthTokenSecretVersion"))

    @oauth_token_secret_version.setter
    def oauth_token_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c5ad1594c6884b8c2a4be47bb46d3bce7f8a9d89dabbcfc165e7c55cbeca61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37bb61ddca95c4bf43afef47e69f5952ad4e3d8c69648abe179ac344e110a02d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildv2ConnectionGithubConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGithubConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2082917c86b3a13aed4af5ba3821cb263e802d65b84a4ae2948d241bb5781bbb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorizerCredential")
    def put_authorizer_credential(
        self,
        *,
        oauth_token_secret_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param oauth_token_secret_version: A SecretManager resource containing the OAuth token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#oauth_token_secret_version GoogleCloudbuildv2Connection#oauth_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential(
            oauth_token_secret_version=oauth_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putAuthorizerCredential", [value]))

    @jsii.member(jsii_name="resetAppInstallationId")
    def reset_app_installation_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppInstallationId", []))

    @jsii.member(jsii_name="resetAuthorizerCredential")
    def reset_authorizer_credential(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizerCredential", []))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredential")
    def authorizer_credential(
        self,
    ) -> GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredentialOutputReference:
        return typing.cast(GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="appInstallationIdInput")
    def app_installation_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "appInstallationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="appInstallationId")
    def app_installation_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "appInstallationId"))

    @app_installation_id.setter
    def app_installation_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f8d4579927ec082663ad439f1fb77c0f918ff01702140d4c0d2e643ab11cdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appInstallationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionGithubConfig]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionGithubConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionGithubConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9cf4e6a91b7053ff9b29d42104b51095730dd5d11610127d8807893067aafbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGithubEnterpriseConfig",
    jsii_struct_bases=[],
    name_mapping={
        "host_uri": "hostUri",
        "app_id": "appId",
        "app_installation_id": "appInstallationId",
        "app_slug": "appSlug",
        "private_key_secret_version": "privateKeySecretVersion",
        "service_directory_config": "serviceDirectoryConfig",
        "ssl_ca": "sslCa",
        "webhook_secret_secret_version": "webhookSecretSecretVersion",
    },
)
class GoogleCloudbuildv2ConnectionGithubEnterpriseConfig:
    def __init__(
        self,
        *,
        host_uri: builtins.str,
        app_id: typing.Optional[jsii.Number] = None,
        app_installation_id: typing.Optional[jsii.Number] = None,
        app_slug: typing.Optional[builtins.str] = None,
        private_key_secret_version: typing.Optional[builtins.str] = None,
        service_directory_config: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
        webhook_secret_secret_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_uri: Required. The URI of the GitHub Enterprise host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#host_uri GoogleCloudbuildv2Connection#host_uri}
        :param app_id: Id of the GitHub App created from the manifest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#app_id GoogleCloudbuildv2Connection#app_id}
        :param app_installation_id: ID of the installation of the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#app_installation_id GoogleCloudbuildv2Connection#app_installation_id}
        :param app_slug: The URL-friendly name of the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#app_slug GoogleCloudbuildv2Connection#app_slug}
        :param private_key_secret_version: SecretManager resource containing the private key of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#private_key_secret_version GoogleCloudbuildv2Connection#private_key_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service_directory_config GoogleCloudbuildv2Connection#service_directory_config}
        :param ssl_ca: SSL certificate to use for requests to GitHub Enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#ssl_ca GoogleCloudbuildv2Connection#ssl_ca}
        :param webhook_secret_secret_version: SecretManager resource containing the webhook secret of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#webhook_secret_secret_version GoogleCloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if isinstance(service_directory_config, dict):
            service_directory_config = GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig(**service_directory_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f45ae368b8e1adbc6ea4fc9e7beeb45a55a83fd1c1e2ec77a2bd7caafe08c0)
            check_type(argname="argument host_uri", value=host_uri, expected_type=type_hints["host_uri"])
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument app_installation_id", value=app_installation_id, expected_type=type_hints["app_installation_id"])
            check_type(argname="argument app_slug", value=app_slug, expected_type=type_hints["app_slug"])
            check_type(argname="argument private_key_secret_version", value=private_key_secret_version, expected_type=type_hints["private_key_secret_version"])
            check_type(argname="argument service_directory_config", value=service_directory_config, expected_type=type_hints["service_directory_config"])
            check_type(argname="argument ssl_ca", value=ssl_ca, expected_type=type_hints["ssl_ca"])
            check_type(argname="argument webhook_secret_secret_version", value=webhook_secret_secret_version, expected_type=type_hints["webhook_secret_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_uri": host_uri,
        }
        if app_id is not None:
            self._values["app_id"] = app_id
        if app_installation_id is not None:
            self._values["app_installation_id"] = app_installation_id
        if app_slug is not None:
            self._values["app_slug"] = app_slug
        if private_key_secret_version is not None:
            self._values["private_key_secret_version"] = private_key_secret_version
        if service_directory_config is not None:
            self._values["service_directory_config"] = service_directory_config
        if ssl_ca is not None:
            self._values["ssl_ca"] = ssl_ca
        if webhook_secret_secret_version is not None:
            self._values["webhook_secret_secret_version"] = webhook_secret_secret_version

    @builtins.property
    def host_uri(self) -> builtins.str:
        '''Required. The URI of the GitHub Enterprise host this connection is for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#host_uri GoogleCloudbuildv2Connection#host_uri}
        '''
        result = self._values.get("host_uri")
        assert result is not None, "Required property 'host_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_id(self) -> typing.Optional[jsii.Number]:
        '''Id of the GitHub App created from the manifest.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#app_id GoogleCloudbuildv2Connection#app_id}
        '''
        result = self._values.get("app_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def app_installation_id(self) -> typing.Optional[jsii.Number]:
        '''ID of the installation of the GitHub App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#app_installation_id GoogleCloudbuildv2Connection#app_installation_id}
        '''
        result = self._values.get("app_installation_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def app_slug(self) -> typing.Optional[builtins.str]:
        '''The URL-friendly name of the GitHub App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#app_slug GoogleCloudbuildv2Connection#app_slug}
        '''
        result = self._values.get("app_slug")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_secret_version(self) -> typing.Optional[builtins.str]:
        '''SecretManager resource containing the private key of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#private_key_secret_version GoogleCloudbuildv2Connection#private_key_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("private_key_secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_directory_config(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig"]:
        '''service_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service_directory_config GoogleCloudbuildv2Connection#service_directory_config}
        '''
        result = self._values.get("service_directory_config")
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig"], result)

    @builtins.property
    def ssl_ca(self) -> typing.Optional[builtins.str]:
        '''SSL certificate to use for requests to GitHub Enterprise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#ssl_ca GoogleCloudbuildv2Connection#ssl_ca}
        '''
        result = self._values.get("ssl_ca")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webhook_secret_secret_version(self) -> typing.Optional[builtins.str]:
        '''SecretManager resource containing the webhook secret of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#webhook_secret_secret_version GoogleCloudbuildv2Connection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionGithubEnterpriseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildv2ConnectionGithubEnterpriseConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGithubEnterpriseConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60d68f05aaf1edeabf143ecbbc8b6de5e99feadf8fa2b006138aa25384982656)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putServiceDirectoryConfig")
    def put_service_directory_config(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service GoogleCloudbuildv2Connection#service}
        '''
        value = GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig(
            service=service
        )

        return typing.cast(None, jsii.invoke(self, "putServiceDirectoryConfig", [value]))

    @jsii.member(jsii_name="resetAppId")
    def reset_app_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppId", []))

    @jsii.member(jsii_name="resetAppInstallationId")
    def reset_app_installation_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppInstallationId", []))

    @jsii.member(jsii_name="resetAppSlug")
    def reset_app_slug(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppSlug", []))

    @jsii.member(jsii_name="resetPrivateKeySecretVersion")
    def reset_private_key_secret_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKeySecretVersion", []))

    @jsii.member(jsii_name="resetServiceDirectoryConfig")
    def reset_service_directory_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceDirectoryConfig", []))

    @jsii.member(jsii_name="resetSslCa")
    def reset_ssl_ca(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCa", []))

    @jsii.member(jsii_name="resetWebhookSecretSecretVersion")
    def reset_webhook_secret_secret_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebhookSecretSecretVersion", []))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfig")
    def service_directory_config(
        self,
    ) -> "GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference":
        return typing.cast("GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference", jsii.get(self, "serviceDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="appIdInput")
    def app_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "appIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appInstallationIdInput")
    def app_installation_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "appInstallationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appSlugInput")
    def app_slug_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appSlugInput"))

    @builtins.property
    @jsii.member(jsii_name="hostUriInput")
    def host_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostUriInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeySecretVersionInput")
    def private_key_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeySecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfigInput")
    def service_directory_config_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig"]:
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig"], jsii.get(self, "serviceDirectoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCaInput")
    def ssl_ca_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCaInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersionInput")
    def webhook_secret_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookSecretSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "appId"))

    @app_id.setter
    def app_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4be26ccc927f1d3352e0190f051b9436dd75898a4cabe70be85698b791e150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appInstallationId")
    def app_installation_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "appInstallationId"))

    @app_installation_id.setter
    def app_installation_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5cbf73a689de59491625dc557459c59edc0c058143b2c48ac0c3270e21817a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appInstallationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appSlug")
    def app_slug(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSlug"))

    @app_slug.setter
    def app_slug(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77755225d2de5b9c15f97bed3ca5690a5a27e4b6d517f1e9fa706bc7d85d2bab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSlug", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostUri")
    def host_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostUri"))

    @host_uri.setter
    def host_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bf62212919c7d76f7dbe583ea924db6c4df13d7f7061bc81ff1557f7821ba8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKeySecretVersion")
    def private_key_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKeySecretVersion"))

    @private_key_secret_version.setter
    def private_key_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab3c19a7f11d1a6a3087dec7228ed55edcce1a2a7a8c08dc850efabc485821bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeySecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCa")
    def ssl_ca(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCa"))

    @ssl_ca.setter
    def ssl_ca(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee4913548a67a2e3ea59985c6cf29e46984d4d216f118c80bb6abe044b44b2fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretSecretVersion"))

    @webhook_secret_secret_version.setter
    def webhook_secret_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87aca26015c0060fb398fe6a5b4a351c7dc320a5a665412da9512c1fa0e392fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionGithubEnterpriseConfig]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionGithubEnterpriseConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionGithubEnterpriseConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81eaf8d6f04bc2248d5f109ed44060703a37541770352b2b97f538ca749a8913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"service": "service"},
)
class GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig:
    def __init__(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service GoogleCloudbuildv2Connection#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fb23a7db6edbecef0f252ae73a0737459f906e99b1ba55dd5a2b622d826cad)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service GoogleCloudbuildv2Connection#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__022381ecd2584bf0f876eff2daf980c11c189319a75ee159fe390e4ba59dcef4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ca9526fbb25579d56bea11cc66b46e41d6833cbaee05cdb7b2db7f2d1eb94e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4505e3b89cf312a7e7a28de0887f89d4a86af14c9b6971dc85ba146bdecd0cab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGitlabConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_credential": "authorizerCredential",
        "read_authorizer_credential": "readAuthorizerCredential",
        "webhook_secret_secret_version": "webhookSecretSecretVersion",
        "host_uri": "hostUri",
        "service_directory_config": "serviceDirectoryConfig",
        "ssl_ca": "sslCa",
    },
)
class GoogleCloudbuildv2ConnectionGitlabConfig:
    def __init__(
        self,
        *,
        authorizer_credential: typing.Union["GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        host_uri: typing.Optional[builtins.str] = None,
        service_directory_config: typing.Optional[typing.Union["GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#authorizer_credential GoogleCloudbuildv2Connection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#read_authorizer_credential GoogleCloudbuildv2Connection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret of a GitLab Enterprise project, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#webhook_secret_secret_version GoogleCloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param host_uri: The URI of the GitLab Enterprise host this connection is for. If not specified, the default value is https://gitlab.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#host_uri GoogleCloudbuildv2Connection#host_uri}
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service_directory_config GoogleCloudbuildv2Connection#service_directory_config}
        :param ssl_ca: SSL certificate to use for requests to GitLab Enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#ssl_ca GoogleCloudbuildv2Connection#ssl_ca}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential(**authorizer_credential)
        if isinstance(read_authorizer_credential, dict):
            read_authorizer_credential = GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential(**read_authorizer_credential)
        if isinstance(service_directory_config, dict):
            service_directory_config = GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig(**service_directory_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035fb0be9ebae7ea7f424efec255832c9d9123ac1108ba33b1aba9c0107d8163)
            check_type(argname="argument authorizer_credential", value=authorizer_credential, expected_type=type_hints["authorizer_credential"])
            check_type(argname="argument read_authorizer_credential", value=read_authorizer_credential, expected_type=type_hints["read_authorizer_credential"])
            check_type(argname="argument webhook_secret_secret_version", value=webhook_secret_secret_version, expected_type=type_hints["webhook_secret_secret_version"])
            check_type(argname="argument host_uri", value=host_uri, expected_type=type_hints["host_uri"])
            check_type(argname="argument service_directory_config", value=service_directory_config, expected_type=type_hints["service_directory_config"])
            check_type(argname="argument ssl_ca", value=ssl_ca, expected_type=type_hints["ssl_ca"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorizer_credential": authorizer_credential,
            "read_authorizer_credential": read_authorizer_credential,
            "webhook_secret_secret_version": webhook_secret_secret_version,
        }
        if host_uri is not None:
            self._values["host_uri"] = host_uri
        if service_directory_config is not None:
            self._values["service_directory_config"] = service_directory_config
        if ssl_ca is not None:
            self._values["ssl_ca"] = ssl_ca

    @builtins.property
    def authorizer_credential(
        self,
    ) -> "GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential":
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#authorizer_credential GoogleCloudbuildv2Connection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        assert result is not None, "Required property 'authorizer_credential' is missing"
        return typing.cast("GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential", result)

    @builtins.property
    def read_authorizer_credential(
        self,
    ) -> "GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential":
        '''read_authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#read_authorizer_credential GoogleCloudbuildv2Connection#read_authorizer_credential}
        '''
        result = self._values.get("read_authorizer_credential")
        assert result is not None, "Required property 'read_authorizer_credential' is missing"
        return typing.cast("GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential", result)

    @builtins.property
    def webhook_secret_secret_version(self) -> builtins.str:
        '''Required. Immutable. SecretManager resource containing the webhook secret of a GitLab Enterprise project, formatted as 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#webhook_secret_secret_version GoogleCloudbuildv2Connection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        assert result is not None, "Required property 'webhook_secret_secret_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the GitLab Enterprise host this connection is for. If not specified, the default value is https://gitlab.com.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#host_uri GoogleCloudbuildv2Connection#host_uri}
        '''
        result = self._values.get("host_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_directory_config(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig"]:
        '''service_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service_directory_config GoogleCloudbuildv2Connection#service_directory_config}
        '''
        result = self._values.get("service_directory_config")
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig"], result)

    @builtins.property
    def ssl_ca(self) -> typing.Optional[builtins.str]:
        '''SSL certificate to use for requests to GitLab Enterprise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#ssl_ca GoogleCloudbuildv2Connection#ssl_ca}
        '''
        result = self._values.get("ssl_ca")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionGitlabConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f446c8007307f11d89241cea10acfd1936d926700a4515ca4148e23dbe9ac4)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("user_token_secret_version")
        assert result is not None, "Required property 'user_token_secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a78088d69592f6535b9924e678b963777293c68508ed93681132df95b98d7f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @builtins.property
    @jsii.member(jsii_name="userTokenSecretVersionInput")
    def user_token_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userTokenSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="userTokenSecretVersion")
    def user_token_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userTokenSecretVersion"))

    @user_token_secret_version.setter
    def user_token_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1762f1908d84c1de7ce903538d35660f26d3d7e5ee481458b61210e51a49eb8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f187f6d41860451b62923bb7df8164bc5945850725db43de76693d871303e984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildv2ConnectionGitlabConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGitlabConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97ff203d588326e8c12ca1cb9a25b0ed2627134e5e961633766fafb0500ee8d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorizerCredential")
    def put_authorizer_credential(
        self,
        *,
        user_token_secret_version: builtins.str,
    ) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putAuthorizerCredential", [value]))

    @jsii.member(jsii_name="putReadAuthorizerCredential")
    def put_read_authorizer_credential(
        self,
        *,
        user_token_secret_version: builtins.str,
    ) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putReadAuthorizerCredential", [value]))

    @jsii.member(jsii_name="putServiceDirectoryConfig")
    def put_service_directory_config(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service GoogleCloudbuildv2Connection#service}
        '''
        value = GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig(
            service=service
        )

        return typing.cast(None, jsii.invoke(self, "putServiceDirectoryConfig", [value]))

    @jsii.member(jsii_name="resetHostUri")
    def reset_host_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostUri", []))

    @jsii.member(jsii_name="resetServiceDirectoryConfig")
    def reset_service_directory_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceDirectoryConfig", []))

    @jsii.member(jsii_name="resetSslCa")
    def reset_ssl_ca(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCa", []))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredential")
    def authorizer_credential(
        self,
    ) -> GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredentialOutputReference:
        return typing.cast(GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredential")
    def read_authorizer_credential(
        self,
    ) -> "GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredentialOutputReference":
        return typing.cast("GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredentialOutputReference", jsii.get(self, "readAuthorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="serverVersion")
    def server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverVersion"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfig")
    def service_directory_config(
        self,
    ) -> "GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfigOutputReference":
        return typing.cast("GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfigOutputReference", jsii.get(self, "serviceDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="hostUriInput")
    def host_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostUriInput"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredentialInput")
    def read_authorizer_credential_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential"]:
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential"], jsii.get(self, "readAuthorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfigInput")
    def service_directory_config_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig"]:
        return typing.cast(typing.Optional["GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig"], jsii.get(self, "serviceDirectoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCaInput")
    def ssl_ca_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCaInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersionInput")
    def webhook_secret_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookSecretSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="hostUri")
    def host_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostUri"))

    @host_uri.setter
    def host_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8714ae767f469435966e2846fa51d4171c82f88bced8e887af10b3ee8055f5b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCa")
    def ssl_ca(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCa"))

    @ssl_ca.setter
    def ssl_ca(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc5f31d3cd5a192e2025830eb2afb5fa662cc63e2ff0eba11a7b92c31f52ac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretSecretVersion"))

    @webhook_secret_secret_version.setter
    def webhook_secret_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c9091946ddedcbf6af625042b55b8fb755b0b61775bad76e1cb0bd1a15ddd4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfig]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a742efc47ab5416fed096b34d6b0afcffa354bd2b7d12d4c6e258912a97a170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f81175bca87c872e75d29c1a157d152c48265d9f83a7f865d1661a5eb5b4413)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#user_token_secret_version GoogleCloudbuildv2Connection#user_token_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("user_token_secret_version")
        assert result is not None, "Required property 'user_token_secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dad533c49e6e7ce7ff0f2d5baa59c500837a61c07f35500c7c3cce52bbf9f2d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @builtins.property
    @jsii.member(jsii_name="userTokenSecretVersionInput")
    def user_token_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userTokenSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="userTokenSecretVersion")
    def user_token_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userTokenSecretVersion"))

    @user_token_secret_version.setter
    def user_token_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5af4f5ef950ebe7718f8f08d6c0fc167ddbaa42586ec9b16003d95e79d0658f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b59b03a49c5579aa2039b990c99553307a9e9998896476d5873300028b0569a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"service": "service"},
)
class GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig:
    def __init__(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service GoogleCloudbuildv2Connection#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d05ba80a816ee77c923e30e31a7dd628e6e64a0e9b9e2d6a91bf41c0b4a23b)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#service GoogleCloudbuildv2Connection#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb90768d5eb56d8b9702f218094a21dacf46048702b9c3eb1399b5077b0e377b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__227a485f0025543a171abf7539817e030f12fa4c6e262cfd1cf47e1de28f3597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__461da72f0e3e8c05d0d9ba4a50aeaaba8244d1efb3b7e958b4814ff20bb14f84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionInstallationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleCloudbuildv2ConnectionInstallationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionInstallationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildv2ConnectionInstallationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionInstallationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b136327cc062b286ca1d1712c785f89b73d6ea1d5ea4a7773730d8a982fac94c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudbuildv2ConnectionInstallationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91eed79453ba0f1db171422c75da6bf2206bb7fc4c99c496a8e8a4733a6f35c8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudbuildv2ConnectionInstallationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccbc235bcf3bbeec655da1cd91181b91b10a89410968a7ebf8c4d04722f9e422)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0647150ed6452ec2d200687c7a6f3912ab3c15937ad5b1168874c74426928e79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58a098d7799b6b8a8dce2a7bec9fa31f14825e6a61a7af0c0c47eac56cc487e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildv2ConnectionInstallationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionInstallationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3b805f09d1229bc765c5cf51b1821c2dff2b0336c40766513cba1cb94251f53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actionUri")
    def action_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionUri"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildv2ConnectionInstallationState]:
        return typing.cast(typing.Optional[GoogleCloudbuildv2ConnectionInstallationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildv2ConnectionInstallationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e0298b8410487cd64284c29ac95de6aca6e1ecbf15b33a81411d916b3a2ffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleCloudbuildv2ConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#create GoogleCloudbuildv2Connection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#delete GoogleCloudbuildv2Connection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#update GoogleCloudbuildv2Connection#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4870153579ead9434f4373e426bf7c32c813e19fd46b7da74b5b54d3872c3a3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#create GoogleCloudbuildv2Connection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#delete GoogleCloudbuildv2Connection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuildv2_connection#update GoogleCloudbuildv2Connection#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildv2ConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildv2ConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildv2Connection.GoogleCloudbuildv2ConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43642c85120d73804d0cbdbb37418a13ce1ffd823aa4ed62e670815bf592c1d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__533e7af9c1b177240695bc8ae676893e0281073de1c0302fa1436d5efe96bae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7693ba102d473f589e6bf376a517d30a4166d8485560a1ebb463762445855ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528ee8bc346b69a8ca2ccc6e27f3200c0682788b28f8b2e3b3bb75b75c798675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildv2ConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildv2ConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildv2ConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__577fe86e0e9d5dbdcc60cea712ac4a499a93bcf38da4ba8016a1792e258a3195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleCloudbuildv2Connection",
    "GoogleCloudbuildv2ConnectionBitbucketCloudConfig",
    "GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential",
    "GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference",
    "GoogleCloudbuildv2ConnectionBitbucketCloudConfigOutputReference",
    "GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential",
    "GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference",
    "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig",
    "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential",
    "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference",
    "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigOutputReference",
    "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential",
    "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference",
    "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig",
    "GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference",
    "GoogleCloudbuildv2ConnectionConfig",
    "GoogleCloudbuildv2ConnectionGithubConfig",
    "GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential",
    "GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredentialOutputReference",
    "GoogleCloudbuildv2ConnectionGithubConfigOutputReference",
    "GoogleCloudbuildv2ConnectionGithubEnterpriseConfig",
    "GoogleCloudbuildv2ConnectionGithubEnterpriseConfigOutputReference",
    "GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig",
    "GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference",
    "GoogleCloudbuildv2ConnectionGitlabConfig",
    "GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential",
    "GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredentialOutputReference",
    "GoogleCloudbuildv2ConnectionGitlabConfigOutputReference",
    "GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential",
    "GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredentialOutputReference",
    "GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig",
    "GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfigOutputReference",
    "GoogleCloudbuildv2ConnectionInstallationState",
    "GoogleCloudbuildv2ConnectionInstallationStateList",
    "GoogleCloudbuildv2ConnectionInstallationStateOutputReference",
    "GoogleCloudbuildv2ConnectionTimeouts",
    "GoogleCloudbuildv2ConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e069a18cb840344f24faba78ec5e819a19e02d050a8feaf02ecfd3ba746987bd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bitbucket_cloud_config: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionBitbucketCloudConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bitbucket_data_center_config: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    github_config: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionGithubConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    github_enterprise_config: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionGithubEnterpriseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gitlab_config: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionGitlabConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b6b932808800b0e66ffcdf628a2229859bc4f8948ab422aa04369a4ddf5e16c6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caaa7a20f58e7e0953062a1c0b84a5c99c32dc28f002a96a1194eab8b35ebeb9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c7c20470334e0b007159b4a84919f36f91be0e716e9fb3c1ad59140eca5911(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74cbb01716399ebb7120d52792cf3b1502db208cb7248b2a56444ee05e732e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e6cc99be65bd60a761dfcc8b4f4a25fb0144fb0ead3171ed690be73fa79029(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adedb2733bbdec57df730333e12d4832acec5481f5df1036b2a23271e420a6c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6c50da6e792d48e305143ad151beae1a7f11e7536421adf8f7d7580262dcfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba5c43495f346879f0121059dcb4cb9ed006b5a53949ee5354bfefaf998536c(
    *,
    authorizer_credential: typing.Union[GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    read_authorizer_credential: typing.Union[GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    webhook_secret_secret_version: builtins.str,
    workspace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b7f1d36cfadeb89014318f4461a7326b4efaef8910f8fe770570a9409751e5(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0281720ed30272307478e90a0434d3005fc0b57340ec5c149141a808d995f883(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8fcc87fcf3f2afad7f4e4e89d5779ec26c7c66234c7538a9fc9eb0f0257434(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd7b9d4c065a2129a4cae24743f065a2e5bd95ca18384cd9252e75f389a89fc(
    value: typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bd52b092c970db6925428d497854dd90492c65d12da8fd1c59373b1b433b9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e85ce909a9b7e4eb0fda65c0406985b1892935a2827a2b39bd7bd1dfd5176c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9763eb3784d18f838a1bbd33cc8f1264129f511e082c8e193be3a421c9bf7867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e27400dce6562b011c6945503fcccfd4fc37c557253f5e0509bd5b438cd335(
    value: typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657c8d1a190d5877d04ff17898b7b1270c8796a8708177ad6f1a2b2e18a5478b(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc80687f9866a0d8b07c2270e09f0452b1d5ba36da9131abb23079b68358a93c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3870554a8e91b4b91e07425551442ae8d4102e0d34594a6fa9da5b152a84c55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a52db4a453b3639ec72bc715684ffe81ce3e7a2ae8b26bfc85735be18c30bc6(
    value: typing.Optional[GoogleCloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169d3b0d8e901ddb96f98679f1a895528d0ca3ec6c2acefb7771eff1c98eabf2(
    *,
    authorizer_credential: typing.Union[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    host_uri: builtins.str,
    read_authorizer_credential: typing.Union[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    webhook_secret_secret_version: builtins.str,
    service_directory_config: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_ca: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f66417e3b6c264de1b6cd4e9c16f7cab6c1a7bfad7e3fb10e6b7faa20e7c735(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8d4daa36bc9d24f6785091b1f32931977380bed1287e48534cbc7498429908(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b588f63ad1c0be68831f497ea04950ad7d81af337b96bffbafd5602558803e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c427c792b88da1e65817836d113f19b2bcda4c7fe208fa9b3fa772e0f731f909(
    value: typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b518a4b14ffc844ffad988cfd420c440a247d0454bd4ba36f60e2802a80b1270(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d97c474cb2c19feac95cb42d4ae346ec5ace9586e91b5f393d8aed9c74cdc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86e90a8d36692e13a9431bb0223e184f2461e925089a93ce07ee4ccf9a0ac43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f59c78533befd6c11e277a4c00b64a76070589224c5407c78cde6f027e5246(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c054f90d6216ec1019d0d70c246c8ee0d4941053ab4d47d89c9e395fcab32d1d(
    value: typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5b99fd9ecb368aef70ec7d4577a81984eb73187f0ed8772c8af7d6269cd458(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1fe858d162d7ffcd40245d3b95f295c46b18744a860fda09d10ce07c6e8ae99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc879c122e44c8c93e987175b232ab4759655a23a0f33c9ccfe67e6bda7b978(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418b5a82ac0df96ca4536870b9ea96ed3c960180e88151145971c17b31363c59(
    value: typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea77e746f1ee981caed971e51a152f9dceda1c9dcf3617cbfa9d6e5aa99279f8(
    *,
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a16b643e1e67b108f070f98f5ca6d807d79c63373b2bc911689ceaa3903355e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1ce5a03d486b1ff28333b8c98fb4a9f1251958b4d167093d7c8a2364d0d0f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3fc1083dc53eb873d56275d9b026cbf651f55a1dfa0a30e31d1e1dda534efe3(
    value: typing.Optional[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970c626ee352f9a22331f448cf4401422335f5bcf1f5e07c355ffb9021ce672a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bitbucket_cloud_config: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionBitbucketCloudConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bitbucket_data_center_config: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionBitbucketDataCenterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    github_config: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionGithubConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    github_enterprise_config: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionGithubEnterpriseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gitlab_config: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionGitlabConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5cacfab94b991720cacf086c133513e0d7939deb4b3b199e04e982000b40e4e(
    *,
    app_installation_id: typing.Optional[jsii.Number] = None,
    authorizer_credential: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f9be218d7e53fba891ad11b7510c24af31e5ae51394ac2052914c35b13617a(
    *,
    oauth_token_secret_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2544d63177fa1f66014824458a80a7267b98a1f280701f0595786795f7b095ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c5ad1594c6884b8c2a4be47bb46d3bce7f8a9d89dabbcfc165e7c55cbeca61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37bb61ddca95c4bf43afef47e69f5952ad4e3d8c69648abe179ac344e110a02d(
    value: typing.Optional[GoogleCloudbuildv2ConnectionGithubConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2082917c86b3a13aed4af5ba3821cb263e802d65b84a4ae2948d241bb5781bbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f8d4579927ec082663ad439f1fb77c0f918ff01702140d4c0d2e643ab11cdc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9cf4e6a91b7053ff9b29d42104b51095730dd5d11610127d8807893067aafbe(
    value: typing.Optional[GoogleCloudbuildv2ConnectionGithubConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f45ae368b8e1adbc6ea4fc9e7beeb45a55a83fd1c1e2ec77a2bd7caafe08c0(
    *,
    host_uri: builtins.str,
    app_id: typing.Optional[jsii.Number] = None,
    app_installation_id: typing.Optional[jsii.Number] = None,
    app_slug: typing.Optional[builtins.str] = None,
    private_key_secret_version: typing.Optional[builtins.str] = None,
    service_directory_config: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_ca: typing.Optional[builtins.str] = None,
    webhook_secret_secret_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d68f05aaf1edeabf143ecbbc8b6de5e99feadf8fa2b006138aa25384982656(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4be26ccc927f1d3352e0190f051b9436dd75898a4cabe70be85698b791e150(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5cbf73a689de59491625dc557459c59edc0c058143b2c48ac0c3270e21817a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77755225d2de5b9c15f97bed3ca5690a5a27e4b6d517f1e9fa706bc7d85d2bab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bf62212919c7d76f7dbe583ea924db6c4df13d7f7061bc81ff1557f7821ba8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab3c19a7f11d1a6a3087dec7228ed55edcce1a2a7a8c08dc850efabc485821bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4913548a67a2e3ea59985c6cf29e46984d4d216f118c80bb6abe044b44b2fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87aca26015c0060fb398fe6a5b4a351c7dc320a5a665412da9512c1fa0e392fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81eaf8d6f04bc2248d5f109ed44060703a37541770352b2b97f538ca749a8913(
    value: typing.Optional[GoogleCloudbuildv2ConnectionGithubEnterpriseConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fb23a7db6edbecef0f252ae73a0737459f906e99b1ba55dd5a2b622d826cad(
    *,
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__022381ecd2584bf0f876eff2daf980c11c189319a75ee159fe390e4ba59dcef4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ca9526fbb25579d56bea11cc66b46e41d6833cbaee05cdb7b2db7f2d1eb94e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4505e3b89cf312a7e7a28de0887f89d4a86af14c9b6971dc85ba146bdecd0cab(
    value: typing.Optional[GoogleCloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035fb0be9ebae7ea7f424efec255832c9d9123ac1108ba33b1aba9c0107d8163(
    *,
    authorizer_credential: typing.Union[GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    read_authorizer_credential: typing.Union[GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    webhook_secret_secret_version: builtins.str,
    host_uri: typing.Optional[builtins.str] = None,
    service_directory_config: typing.Optional[typing.Union[GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_ca: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f446c8007307f11d89241cea10acfd1936d926700a4515ca4148e23dbe9ac4(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a78088d69592f6535b9924e678b963777293c68508ed93681132df95b98d7f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1762f1908d84c1de7ce903538d35660f26d3d7e5ee481458b61210e51a49eb8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f187f6d41860451b62923bb7df8164bc5945850725db43de76693d871303e984(
    value: typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ff203d588326e8c12ca1cb9a25b0ed2627134e5e961633766fafb0500ee8d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8714ae767f469435966e2846fa51d4171c82f88bced8e887af10b3ee8055f5b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc5f31d3cd5a192e2025830eb2afb5fa662cc63e2ff0eba11a7b92c31f52ac7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c9091946ddedcbf6af625042b55b8fb755b0b61775bad76e1cb0bd1a15ddd4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a742efc47ab5416fed096b34d6b0afcffa354bd2b7d12d4c6e258912a97a170(
    value: typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f81175bca87c872e75d29c1a157d152c48265d9f83a7f865d1661a5eb5b4413(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dad533c49e6e7ce7ff0f2d5baa59c500837a61c07f35500c7c3cce52bbf9f2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5af4f5ef950ebe7718f8f08d6c0fc167ddbaa42586ec9b16003d95e79d0658f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59b03a49c5579aa2039b990c99553307a9e9998896476d5873300028b0569a4(
    value: typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d05ba80a816ee77c923e30e31a7dd628e6e64a0e9b9e2d6a91bf41c0b4a23b(
    *,
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb90768d5eb56d8b9702f218094a21dacf46048702b9c3eb1399b5077b0e377b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__227a485f0025543a171abf7539817e030f12fa4c6e262cfd1cf47e1de28f3597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__461da72f0e3e8c05d0d9ba4a50aeaaba8244d1efb3b7e958b4814ff20bb14f84(
    value: typing.Optional[GoogleCloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b136327cc062b286ca1d1712c785f89b73d6ea1d5ea4a7773730d8a982fac94c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91eed79453ba0f1db171422c75da6bf2206bb7fc4c99c496a8e8a4733a6f35c8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccbc235bcf3bbeec655da1cd91181b91b10a89410968a7ebf8c4d04722f9e422(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0647150ed6452ec2d200687c7a6f3912ab3c15937ad5b1168874c74426928e79(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a098d7799b6b8a8dce2a7bec9fa31f14825e6a61a7af0c0c47eac56cc487e5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b805f09d1229bc765c5cf51b1821c2dff2b0336c40766513cba1cb94251f53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e0298b8410487cd64284c29ac95de6aca6e1ecbf15b33a81411d916b3a2ffe(
    value: typing.Optional[GoogleCloudbuildv2ConnectionInstallationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4870153579ead9434f4373e426bf7c32c813e19fd46b7da74b5b54d3872c3a3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43642c85120d73804d0cbdbb37418a13ce1ffd823aa4ed62e670815bf592c1d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533e7af9c1b177240695bc8ae676893e0281073de1c0302fa1436d5efe96bae6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7693ba102d473f589e6bf376a517d30a4166d8485560a1ebb463762445855ede(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528ee8bc346b69a8ca2ccc6e27f3200c0682788b28f8b2e3b3bb75b75c798675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__577fe86e0e9d5dbdcc60cea712ac4a499a93bcf38da4ba8016a1792e258a3195(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildv2ConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

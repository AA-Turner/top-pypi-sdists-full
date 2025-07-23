r'''
# `google_cloudbuildv2_connection`

Refer to the Terraform Registry for docs: [`google_cloudbuildv2_connection`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection).
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


class Cloudbuildv2Connection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2Connection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection google_cloudbuildv2_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bitbucket_cloud_config: typing.Optional[typing.Union["Cloudbuildv2ConnectionBitbucketCloudConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        bitbucket_data_center_config: typing.Optional[typing.Union["Cloudbuildv2ConnectionBitbucketDataCenterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        github_config: typing.Optional[typing.Union["Cloudbuildv2ConnectionGithubConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        github_enterprise_config: typing.Optional[typing.Union["Cloudbuildv2ConnectionGithubEnterpriseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gitlab_config: typing.Optional[typing.Union["Cloudbuildv2ConnectionGitlabConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["Cloudbuildv2ConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection google_cloudbuildv2_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#location Cloudbuildv2Connection#location}
        :param name: Immutable. The resource name of the connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#name Cloudbuildv2Connection#name}
        :param annotations: Allows clients to store small amounts of arbitrary data. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#annotations Cloudbuildv2Connection#annotations}
        :param bitbucket_cloud_config: bitbucket_cloud_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#bitbucket_cloud_config Cloudbuildv2Connection#bitbucket_cloud_config}
        :param bitbucket_data_center_config: bitbucket_data_center_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#bitbucket_data_center_config Cloudbuildv2Connection#bitbucket_data_center_config}
        :param disabled: If disabled is set to true, functionality is disabled for this connection. Repository based API methods and webhooks processing for repositories in this connection will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#disabled Cloudbuildv2Connection#disabled}
        :param github_config: github_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#github_config Cloudbuildv2Connection#github_config}
        :param github_enterprise_config: github_enterprise_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#github_enterprise_config Cloudbuildv2Connection#github_enterprise_config}
        :param gitlab_config: gitlab_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#gitlab_config Cloudbuildv2Connection#gitlab_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#id Cloudbuildv2Connection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#project Cloudbuildv2Connection#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#timeouts Cloudbuildv2Connection#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f327521b7ef91321641159e8e6dc2e7ac30ef31189ca3e3b8057808220c1de2d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Cloudbuildv2ConnectionConfig(
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
        '''Generates CDKTF code for importing a Cloudbuildv2Connection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Cloudbuildv2Connection to import.
        :param import_from_id: The id of the existing Cloudbuildv2Connection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Cloudbuildv2Connection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e298b50d4128d53271e2465f3e1e6240744a1d25a5986f80fe1cae9fc135d29f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBitbucketCloudConfig")
    def put_bitbucket_cloud_config(
        self,
        *,
        authorizer_credential: typing.Union["Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        workspace: builtins.str,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#authorizer_credential Cloudbuildv2Connection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#read_authorizer_credential Cloudbuildv2Connection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#webhook_secret_secret_version Cloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param workspace: The Bitbucket Cloud Workspace ID to be connected to Google Cloud Platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#workspace Cloudbuildv2Connection#workspace}
        '''
        value = Cloudbuildv2ConnectionBitbucketCloudConfig(
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
        authorizer_credential: typing.Union["Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        host_uri: builtins.str,
        read_authorizer_credential: typing.Union["Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        service_directory_config: typing.Optional[typing.Union["Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#authorizer_credential Cloudbuildv2Connection#authorizer_credential}
        :param host_uri: The URI of the Bitbucket Data Center host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#host_uri Cloudbuildv2Connection#host_uri}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#read_authorizer_credential Cloudbuildv2Connection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#webhook_secret_secret_version Cloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service_directory_config Cloudbuildv2Connection#service_directory_config}
        :param ssl_ca: SSL certificate to use for requests to the Bitbucket Data Center. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#ssl_ca Cloudbuildv2Connection#ssl_ca}
        '''
        value = Cloudbuildv2ConnectionBitbucketDataCenterConfig(
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
        authorizer_credential: typing.Optional[typing.Union["Cloudbuildv2ConnectionGithubConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param app_installation_id: GitHub App installation id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#app_installation_id Cloudbuildv2Connection#app_installation_id}
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#authorizer_credential Cloudbuildv2Connection#authorizer_credential}
        '''
        value = Cloudbuildv2ConnectionGithubConfig(
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
        service_directory_config: typing.Optional[typing.Union["Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
        webhook_secret_secret_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_uri: Required. The URI of the GitHub Enterprise host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#host_uri Cloudbuildv2Connection#host_uri}
        :param app_id: Id of the GitHub App created from the manifest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#app_id Cloudbuildv2Connection#app_id}
        :param app_installation_id: ID of the installation of the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#app_installation_id Cloudbuildv2Connection#app_installation_id}
        :param app_slug: The URL-friendly name of the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#app_slug Cloudbuildv2Connection#app_slug}
        :param private_key_secret_version: SecretManager resource containing the private key of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#private_key_secret_version Cloudbuildv2Connection#private_key_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service_directory_config Cloudbuildv2Connection#service_directory_config}
        :param ssl_ca: SSL certificate to use for requests to GitHub Enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#ssl_ca Cloudbuildv2Connection#ssl_ca}
        :param webhook_secret_secret_version: SecretManager resource containing the webhook secret of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#webhook_secret_secret_version Cloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = Cloudbuildv2ConnectionGithubEnterpriseConfig(
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
        authorizer_credential: typing.Union["Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        host_uri: typing.Optional[builtins.str] = None,
        service_directory_config: typing.Optional[typing.Union["Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#authorizer_credential Cloudbuildv2Connection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#read_authorizer_credential Cloudbuildv2Connection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret of a GitLab Enterprise project, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#webhook_secret_secret_version Cloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param host_uri: The URI of the GitLab Enterprise host this connection is for. If not specified, the default value is https://gitlab.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#host_uri Cloudbuildv2Connection#host_uri}
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service_directory_config Cloudbuildv2Connection#service_directory_config}
        :param ssl_ca: SSL certificate to use for requests to GitLab Enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#ssl_ca Cloudbuildv2Connection#ssl_ca}
        '''
        value = Cloudbuildv2ConnectionGitlabConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#create Cloudbuildv2Connection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#delete Cloudbuildv2Connection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#update Cloudbuildv2Connection#update}.
        '''
        value = Cloudbuildv2ConnectionTimeouts(
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
    ) -> "Cloudbuildv2ConnectionBitbucketCloudConfigOutputReference":
        return typing.cast("Cloudbuildv2ConnectionBitbucketCloudConfigOutputReference", jsii.get(self, "bitbucketCloudConfig"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketDataCenterConfig")
    def bitbucket_data_center_config(
        self,
    ) -> "Cloudbuildv2ConnectionBitbucketDataCenterConfigOutputReference":
        return typing.cast("Cloudbuildv2ConnectionBitbucketDataCenterConfigOutputReference", jsii.get(self, "bitbucketDataCenterConfig"))

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
    def github_config(self) -> "Cloudbuildv2ConnectionGithubConfigOutputReference":
        return typing.cast("Cloudbuildv2ConnectionGithubConfigOutputReference", jsii.get(self, "githubConfig"))

    @builtins.property
    @jsii.member(jsii_name="githubEnterpriseConfig")
    def github_enterprise_config(
        self,
    ) -> "Cloudbuildv2ConnectionGithubEnterpriseConfigOutputReference":
        return typing.cast("Cloudbuildv2ConnectionGithubEnterpriseConfigOutputReference", jsii.get(self, "githubEnterpriseConfig"))

    @builtins.property
    @jsii.member(jsii_name="gitlabConfig")
    def gitlab_config(self) -> "Cloudbuildv2ConnectionGitlabConfigOutputReference":
        return typing.cast("Cloudbuildv2ConnectionGitlabConfigOutputReference", jsii.get(self, "gitlabConfig"))

    @builtins.property
    @jsii.member(jsii_name="installationState")
    def installation_state(self) -> "Cloudbuildv2ConnectionInstallationStateList":
        return typing.cast("Cloudbuildv2ConnectionInstallationStateList", jsii.get(self, "installationState"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "Cloudbuildv2ConnectionTimeoutsOutputReference":
        return typing.cast("Cloudbuildv2ConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["Cloudbuildv2ConnectionBitbucketCloudConfig"]:
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionBitbucketCloudConfig"], jsii.get(self, "bitbucketCloudConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketDataCenterConfigInput")
    def bitbucket_data_center_config_input(
        self,
    ) -> typing.Optional["Cloudbuildv2ConnectionBitbucketDataCenterConfig"]:
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionBitbucketDataCenterConfig"], jsii.get(self, "bitbucketDataCenterConfigInput"))

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
    ) -> typing.Optional["Cloudbuildv2ConnectionGithubConfig"]:
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionGithubConfig"], jsii.get(self, "githubConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="githubEnterpriseConfigInput")
    def github_enterprise_config_input(
        self,
    ) -> typing.Optional["Cloudbuildv2ConnectionGithubEnterpriseConfig"]:
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionGithubEnterpriseConfig"], jsii.get(self, "githubEnterpriseConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gitlabConfigInput")
    def gitlab_config_input(
        self,
    ) -> typing.Optional["Cloudbuildv2ConnectionGitlabConfig"]:
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionGitlabConfig"], jsii.get(self, "gitlabConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "Cloudbuildv2ConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "Cloudbuildv2ConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab644863a8af6e48b4ed49e96e0ff41fb37e6904cb86809eac53bc04e42cd679)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bf69d29a1fa557d7fb3fa1b2d1b84c629c013b060c10a87c8fc9b19f3bfe650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7576007a13b4b0c968094f518ad6ef3cc481720ad44cb718b4e26baafa7a91a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c8d45e31b445e17142d1ef2c2d8e78dc0b3b292f586171ab08860d67fe9b5e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6abbc131ecc3747cd789d9e971b691402f711fc8464413009a72c6c31aeca00c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64eba0d4139c25f99a3f50274ede658998e2b6ca7d1142bbe0938f0e2adb987c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionBitbucketCloudConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_credential": "authorizerCredential",
        "read_authorizer_credential": "readAuthorizerCredential",
        "webhook_secret_secret_version": "webhookSecretSecretVersion",
        "workspace": "workspace",
    },
)
class Cloudbuildv2ConnectionBitbucketCloudConfig:
    def __init__(
        self,
        *,
        authorizer_credential: typing.Union["Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        workspace: builtins.str,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#authorizer_credential Cloudbuildv2Connection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#read_authorizer_credential Cloudbuildv2Connection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#webhook_secret_secret_version Cloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param workspace: The Bitbucket Cloud Workspace ID to be connected to Google Cloud Platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#workspace Cloudbuildv2Connection#workspace}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential(**authorizer_credential)
        if isinstance(read_authorizer_credential, dict):
            read_authorizer_credential = Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential(**read_authorizer_credential)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e4c76fb36a101559b16d43533f50f09366a2ca345e4c20a7b37886d36b06215)
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
    ) -> "Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential":
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#authorizer_credential Cloudbuildv2Connection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        assert result is not None, "Required property 'authorizer_credential' is missing"
        return typing.cast("Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential", result)

    @builtins.property
    def read_authorizer_credential(
        self,
    ) -> "Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential":
        '''read_authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#read_authorizer_credential Cloudbuildv2Connection#read_authorizer_credential}
        '''
        result = self._values.get("read_authorizer_credential")
        assert result is not None, "Required property 'read_authorizer_credential' is missing"
        return typing.cast("Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential", result)

    @builtins.property
    def webhook_secret_secret_version(self) -> builtins.str:
        '''Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#webhook_secret_secret_version Cloudbuildv2Connection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        assert result is not None, "Required property 'webhook_secret_secret_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace(self) -> builtins.str:
        '''The Bitbucket Cloud Workspace ID to be connected to Google Cloud Platform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#workspace Cloudbuildv2Connection#workspace}
        '''
        result = self._values.get("workspace")
        assert result is not None, "Required property 'workspace' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudbuildv2ConnectionBitbucketCloudConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d124b8ff2d5fd3589f1b94e31a543a8e8768783c2c3281b8990472cb2957eaf)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version}

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
        return "Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cef31e69ef97c45af00b121169aabda96e73f6d5d93649c9468d138b752104c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9badd1c82ad9b607f6aa08567acd00feaf5cb92c9a2d7343d68bcd5ec53ea75c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1f21eb585dc2b26d37e75fd6b755fc0f7fcf2f103ca580d2a3a12285931297c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Cloudbuildv2ConnectionBitbucketCloudConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionBitbucketCloudConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e197c9780fbf6015cafe17a40435d88f4e6cefe764ea002d472ff2a0721aed33)
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential(
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putReadAuthorizerCredential", [value]))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredential")
    def authorizer_credential(
        self,
    ) -> Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference:
        return typing.cast(Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredential")
    def read_authorizer_credential(
        self,
    ) -> "Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference":
        return typing.cast("Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference", jsii.get(self, "readAuthorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredentialInput")
    def read_authorizer_credential_input(
        self,
    ) -> typing.Optional["Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential"]:
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential"], jsii.get(self, "readAuthorizerCredentialInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ca28791024a33e87ae5d3f5a9e3cf11c9f707d4d197cabd405d270895db0f10d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspace")
    def workspace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspace"))

    @workspace.setter
    def workspace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62e16a1c725ada3d87cf476aeda6fc2a9ec41d9c589a99993aec8b246300fda0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfig]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b99bd227db1fe3aeb3db382125b2cde99d28ff0b33b76ac539ce5d9bc133a7fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dbb3e85738134313b363c4306face699da8a67652f40d7fd3e6463fb625066d)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version}

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
        return "Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b60f7f75bed739e3858ab9d48cda02187fad00592a3f239673e9ef0dfd15e675)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17d4ba2d0b166df101c754cfe150d93c4cd7584ecba8e8af3845242ef7f9592c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377668b18ab476b6628e64cb2dfa869619e94db457826944a1c3c53eb41e6670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionBitbucketDataCenterConfig",
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
class Cloudbuildv2ConnectionBitbucketDataCenterConfig:
    def __init__(
        self,
        *,
        authorizer_credential: typing.Union["Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        host_uri: builtins.str,
        read_authorizer_credential: typing.Union["Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        service_directory_config: typing.Optional[typing.Union["Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#authorizer_credential Cloudbuildv2Connection#authorizer_credential}
        :param host_uri: The URI of the Bitbucket Data Center host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#host_uri Cloudbuildv2Connection#host_uri}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#read_authorizer_credential Cloudbuildv2Connection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#webhook_secret_secret_version Cloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service_directory_config Cloudbuildv2Connection#service_directory_config}
        :param ssl_ca: SSL certificate to use for requests to the Bitbucket Data Center. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#ssl_ca Cloudbuildv2Connection#ssl_ca}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential(**authorizer_credential)
        if isinstance(read_authorizer_credential, dict):
            read_authorizer_credential = Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential(**read_authorizer_credential)
        if isinstance(service_directory_config, dict):
            service_directory_config = Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig(**service_directory_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088b8cc0d88b1dc312e77f8f5c6f1bf1c7d3050cd85657422c06daf5e19300a1)
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
    ) -> "Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential":
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#authorizer_credential Cloudbuildv2Connection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        assert result is not None, "Required property 'authorizer_credential' is missing"
        return typing.cast("Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential", result)

    @builtins.property
    def host_uri(self) -> builtins.str:
        '''The URI of the Bitbucket Data Center host this connection is for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#host_uri Cloudbuildv2Connection#host_uri}
        '''
        result = self._values.get("host_uri")
        assert result is not None, "Required property 'host_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_authorizer_credential(
        self,
    ) -> "Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential":
        '''read_authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#read_authorizer_credential Cloudbuildv2Connection#read_authorizer_credential}
        '''
        result = self._values.get("read_authorizer_credential")
        assert result is not None, "Required property 'read_authorizer_credential' is missing"
        return typing.cast("Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential", result)

    @builtins.property
    def webhook_secret_secret_version(self) -> builtins.str:
        '''Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#webhook_secret_secret_version Cloudbuildv2Connection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        assert result is not None, "Required property 'webhook_secret_secret_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_directory_config(
        self,
    ) -> typing.Optional["Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig"]:
        '''service_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service_directory_config Cloudbuildv2Connection#service_directory_config}
        '''
        result = self._values.get("service_directory_config")
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig"], result)

    @builtins.property
    def ssl_ca(self) -> typing.Optional[builtins.str]:
        '''SSL certificate to use for requests to the Bitbucket Data Center.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#ssl_ca Cloudbuildv2Connection#ssl_ca}
        '''
        result = self._values.get("ssl_ca")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudbuildv2ConnectionBitbucketDataCenterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35eab05d8caf6aa08d11ce48e4aa3e47d8e4fa3891c6d2a92d94610876f9254e)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version}

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
        return "Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eee3044a4d1077ef31e8281243dbd5719bd1f96f8562af526240adf5e92f2bd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b91b65ed6e0c7c53d74c39ef846b4c1788449d8f028093d1b58f7edccdb1817d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a990341d11caeea455dcf3df777b8cb549139af67b174f24ac98441ceb10ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Cloudbuildv2ConnectionBitbucketDataCenterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionBitbucketDataCenterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__515d56693c6946a90a67a8335766ed1b0f733dfe94e9cb39aec81a452f3ed2f9)
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential(
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putReadAuthorizerCredential", [value]))

    @jsii.member(jsii_name="putServiceDirectoryConfig")
    def put_service_directory_config(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service Cloudbuildv2Connection#service}
        '''
        value = Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig(
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
    ) -> Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference:
        return typing.cast(Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredential")
    def read_authorizer_credential(
        self,
    ) -> "Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference":
        return typing.cast("Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference", jsii.get(self, "readAuthorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="serverVersion")
    def server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverVersion"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfig")
    def service_directory_config(
        self,
    ) -> "Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference":
        return typing.cast("Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference", jsii.get(self, "serviceDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="hostUriInput")
    def host_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostUriInput"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredentialInput")
    def read_authorizer_credential_input(
        self,
    ) -> typing.Optional["Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential"]:
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential"], jsii.get(self, "readAuthorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfigInput")
    def service_directory_config_input(
        self,
    ) -> typing.Optional["Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig"]:
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig"], jsii.get(self, "serviceDirectoryConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c2669e5c7cf5840dee24c0ad8d79f8d0e96e9132e6df2b473bf312ac7e7ca24c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCa")
    def ssl_ca(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCa"))

    @ssl_ca.setter
    def ssl_ca(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9dd9d51afe261a8fd23e49636ee8c40d6cc5c261ef9c402db6f695f8a022c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretSecretVersion"))

    @webhook_secret_secret_version.setter
    def webhook_secret_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c544aa1530682d22a4003f502cd2567b19dd6eb7a7b4b5105b68ba7d6a897296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfig]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__278ecc24dfb1ab217cdb37108865ff9f4e4292d8fb2ac135ccd746ed2bf64b8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23caef4a4d843b0c19daa5933517f486c87d446c7d1be6d42c3e5099e7978e30)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version}

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
        return "Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__508aba201234b9de02374842db5f66349333c7474785153926113a49a2191aef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__567a0f242eae98dd2f90a17a6d54f64ae3d9d09b240b357c0d9ea4dd7a69500b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6548eb08cca7c6d10183ab1c5d4b951c3b1a5903bbcbec69610f3ea103c4f524)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"service": "service"},
)
class Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig:
    def __init__(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service Cloudbuildv2Connection#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fe2ab2612126d994c30e8b22e83b4195e859932fcbca28ea70f3ff653029643)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service Cloudbuildv2Connection#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f21c4c42ea25bb5eec36d994f8b5738eea5518a46a46eb072d0cf3acc1a56e07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f61f3eadd9700406ada31ab03ca0789f4ad2423dcc5fe8e54342fa87ad4e6a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__135d9afb3f4ea603e502b8ed3c747c02fb919938c79eb2e1d37dd99a1ee6522b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionConfig",
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
class Cloudbuildv2ConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bitbucket_cloud_config: typing.Optional[typing.Union[Cloudbuildv2ConnectionBitbucketCloudConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        bitbucket_data_center_config: typing.Optional[typing.Union[Cloudbuildv2ConnectionBitbucketDataCenterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        github_config: typing.Optional[typing.Union["Cloudbuildv2ConnectionGithubConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        github_enterprise_config: typing.Optional[typing.Union["Cloudbuildv2ConnectionGithubEnterpriseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gitlab_config: typing.Optional[typing.Union["Cloudbuildv2ConnectionGitlabConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["Cloudbuildv2ConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#location Cloudbuildv2Connection#location}
        :param name: Immutable. The resource name of the connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#name Cloudbuildv2Connection#name}
        :param annotations: Allows clients to store small amounts of arbitrary data. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#annotations Cloudbuildv2Connection#annotations}
        :param bitbucket_cloud_config: bitbucket_cloud_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#bitbucket_cloud_config Cloudbuildv2Connection#bitbucket_cloud_config}
        :param bitbucket_data_center_config: bitbucket_data_center_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#bitbucket_data_center_config Cloudbuildv2Connection#bitbucket_data_center_config}
        :param disabled: If disabled is set to true, functionality is disabled for this connection. Repository based API methods and webhooks processing for repositories in this connection will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#disabled Cloudbuildv2Connection#disabled}
        :param github_config: github_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#github_config Cloudbuildv2Connection#github_config}
        :param github_enterprise_config: github_enterprise_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#github_enterprise_config Cloudbuildv2Connection#github_enterprise_config}
        :param gitlab_config: gitlab_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#gitlab_config Cloudbuildv2Connection#gitlab_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#id Cloudbuildv2Connection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#project Cloudbuildv2Connection#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#timeouts Cloudbuildv2Connection#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bitbucket_cloud_config, dict):
            bitbucket_cloud_config = Cloudbuildv2ConnectionBitbucketCloudConfig(**bitbucket_cloud_config)
        if isinstance(bitbucket_data_center_config, dict):
            bitbucket_data_center_config = Cloudbuildv2ConnectionBitbucketDataCenterConfig(**bitbucket_data_center_config)
        if isinstance(github_config, dict):
            github_config = Cloudbuildv2ConnectionGithubConfig(**github_config)
        if isinstance(github_enterprise_config, dict):
            github_enterprise_config = Cloudbuildv2ConnectionGithubEnterpriseConfig(**github_enterprise_config)
        if isinstance(gitlab_config, dict):
            gitlab_config = Cloudbuildv2ConnectionGitlabConfig(**gitlab_config)
        if isinstance(timeouts, dict):
            timeouts = Cloudbuildv2ConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7a39d7c5bfe9d502648a40f0275f3c50c8785e852bc88e6a6af9087b24513d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#location Cloudbuildv2Connection#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Immutable. The resource name of the connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#name Cloudbuildv2Connection#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#annotations Cloudbuildv2Connection#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bitbucket_cloud_config(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfig]:
        '''bitbucket_cloud_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#bitbucket_cloud_config Cloudbuildv2Connection#bitbucket_cloud_config}
        '''
        result = self._values.get("bitbucket_cloud_config")
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfig], result)

    @builtins.property
    def bitbucket_data_center_config(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfig]:
        '''bitbucket_data_center_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#bitbucket_data_center_config Cloudbuildv2Connection#bitbucket_data_center_config}
        '''
        result = self._values.get("bitbucket_data_center_config")
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfig], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If disabled is set to true, functionality is disabled for this connection.

        Repository based API methods and webhooks processing for repositories in this connection will be disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#disabled Cloudbuildv2Connection#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def github_config(self) -> typing.Optional["Cloudbuildv2ConnectionGithubConfig"]:
        '''github_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#github_config Cloudbuildv2Connection#github_config}
        '''
        result = self._values.get("github_config")
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionGithubConfig"], result)

    @builtins.property
    def github_enterprise_config(
        self,
    ) -> typing.Optional["Cloudbuildv2ConnectionGithubEnterpriseConfig"]:
        '''github_enterprise_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#github_enterprise_config Cloudbuildv2Connection#github_enterprise_config}
        '''
        result = self._values.get("github_enterprise_config")
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionGithubEnterpriseConfig"], result)

    @builtins.property
    def gitlab_config(self) -> typing.Optional["Cloudbuildv2ConnectionGitlabConfig"]:
        '''gitlab_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#gitlab_config Cloudbuildv2Connection#gitlab_config}
        '''
        result = self._values.get("gitlab_config")
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionGitlabConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#id Cloudbuildv2Connection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#project Cloudbuildv2Connection#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["Cloudbuildv2ConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#timeouts Cloudbuildv2Connection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudbuildv2ConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGithubConfig",
    jsii_struct_bases=[],
    name_mapping={
        "app_installation_id": "appInstallationId",
        "authorizer_credential": "authorizerCredential",
    },
)
class Cloudbuildv2ConnectionGithubConfig:
    def __init__(
        self,
        *,
        app_installation_id: typing.Optional[jsii.Number] = None,
        authorizer_credential: typing.Optional[typing.Union["Cloudbuildv2ConnectionGithubConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param app_installation_id: GitHub App installation id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#app_installation_id Cloudbuildv2Connection#app_installation_id}
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#authorizer_credential Cloudbuildv2Connection#authorizer_credential}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = Cloudbuildv2ConnectionGithubConfigAuthorizerCredential(**authorizer_credential)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43a04979e49eeb0bd8f62e4c709d4674365694312eb10f7d7c8c3ca9c72f5ae)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#app_installation_id Cloudbuildv2Connection#app_installation_id}
        '''
        result = self._values.get("app_installation_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def authorizer_credential(
        self,
    ) -> typing.Optional["Cloudbuildv2ConnectionGithubConfigAuthorizerCredential"]:
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#authorizer_credential Cloudbuildv2Connection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionGithubConfigAuthorizerCredential"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudbuildv2ConnectionGithubConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGithubConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"oauth_token_secret_version": "oauthTokenSecretVersion"},
)
class Cloudbuildv2ConnectionGithubConfigAuthorizerCredential:
    def __init__(
        self,
        *,
        oauth_token_secret_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param oauth_token_secret_version: A SecretManager resource containing the OAuth token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#oauth_token_secret_version Cloudbuildv2Connection#oauth_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__903568966873c58e69c0d1770998500cf7dd80a01efe6f8c03b2b19a952080ef)
            check_type(argname="argument oauth_token_secret_version", value=oauth_token_secret_version, expected_type=type_hints["oauth_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if oauth_token_secret_version is not None:
            self._values["oauth_token_secret_version"] = oauth_token_secret_version

    @builtins.property
    def oauth_token_secret_version(self) -> typing.Optional[builtins.str]:
        '''A SecretManager resource containing the OAuth token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#oauth_token_secret_version Cloudbuildv2Connection#oauth_token_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("oauth_token_secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudbuildv2ConnectionGithubConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudbuildv2ConnectionGithubConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGithubConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe4daf7401842ca5996fa45a11a0f2ab25678ddafa7c5b5116c67386864bfa1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb50bd49d3fbf9d64a5be7b932ad2de376bff1b09df2510bd387d732c753d198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionGithubConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionGithubConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionGithubConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48cf0b26345a327d2ad3afa524cae0102345d2e5a63cde5ec1509cb42ec4d5b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Cloudbuildv2ConnectionGithubConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGithubConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d9ee4532cac6f89413f058d357435112e3d571338df522568bebc758a5f2951)
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
        :param oauth_token_secret_version: A SecretManager resource containing the OAuth token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#oauth_token_secret_version Cloudbuildv2Connection#oauth_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = Cloudbuildv2ConnectionGithubConfigAuthorizerCredential(
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
    ) -> Cloudbuildv2ConnectionGithubConfigAuthorizerCredentialOutputReference:
        return typing.cast(Cloudbuildv2ConnectionGithubConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="appInstallationIdInput")
    def app_installation_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "appInstallationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionGithubConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionGithubConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="appInstallationId")
    def app_installation_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "appInstallationId"))

    @app_installation_id.setter
    def app_installation_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc212c354bf816364689b637b8ee1be97fd4719e62f5677668d39c8dcd0f3f1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appInstallationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Cloudbuildv2ConnectionGithubConfig]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionGithubConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionGithubConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6ac16cec169d0d3ff5e9e00ab760384593d6a6d18598a85cc654b4e627b4c72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGithubEnterpriseConfig",
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
class Cloudbuildv2ConnectionGithubEnterpriseConfig:
    def __init__(
        self,
        *,
        host_uri: builtins.str,
        app_id: typing.Optional[jsii.Number] = None,
        app_installation_id: typing.Optional[jsii.Number] = None,
        app_slug: typing.Optional[builtins.str] = None,
        private_key_secret_version: typing.Optional[builtins.str] = None,
        service_directory_config: typing.Optional[typing.Union["Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
        webhook_secret_secret_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_uri: Required. The URI of the GitHub Enterprise host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#host_uri Cloudbuildv2Connection#host_uri}
        :param app_id: Id of the GitHub App created from the manifest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#app_id Cloudbuildv2Connection#app_id}
        :param app_installation_id: ID of the installation of the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#app_installation_id Cloudbuildv2Connection#app_installation_id}
        :param app_slug: The URL-friendly name of the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#app_slug Cloudbuildv2Connection#app_slug}
        :param private_key_secret_version: SecretManager resource containing the private key of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#private_key_secret_version Cloudbuildv2Connection#private_key_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service_directory_config Cloudbuildv2Connection#service_directory_config}
        :param ssl_ca: SSL certificate to use for requests to GitHub Enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#ssl_ca Cloudbuildv2Connection#ssl_ca}
        :param webhook_secret_secret_version: SecretManager resource containing the webhook secret of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#webhook_secret_secret_version Cloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if isinstance(service_directory_config, dict):
            service_directory_config = Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig(**service_directory_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286291dc21651914736822f99d786cb7b0e630b2cbd1056c3aa44bd53ad97a66)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#host_uri Cloudbuildv2Connection#host_uri}
        '''
        result = self._values.get("host_uri")
        assert result is not None, "Required property 'host_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_id(self) -> typing.Optional[jsii.Number]:
        '''Id of the GitHub App created from the manifest.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#app_id Cloudbuildv2Connection#app_id}
        '''
        result = self._values.get("app_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def app_installation_id(self) -> typing.Optional[jsii.Number]:
        '''ID of the installation of the GitHub App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#app_installation_id Cloudbuildv2Connection#app_installation_id}
        '''
        result = self._values.get("app_installation_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def app_slug(self) -> typing.Optional[builtins.str]:
        '''The URL-friendly name of the GitHub App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#app_slug Cloudbuildv2Connection#app_slug}
        '''
        result = self._values.get("app_slug")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_secret_version(self) -> typing.Optional[builtins.str]:
        '''SecretManager resource containing the private key of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#private_key_secret_version Cloudbuildv2Connection#private_key_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("private_key_secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_directory_config(
        self,
    ) -> typing.Optional["Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig"]:
        '''service_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service_directory_config Cloudbuildv2Connection#service_directory_config}
        '''
        result = self._values.get("service_directory_config")
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig"], result)

    @builtins.property
    def ssl_ca(self) -> typing.Optional[builtins.str]:
        '''SSL certificate to use for requests to GitHub Enterprise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#ssl_ca Cloudbuildv2Connection#ssl_ca}
        '''
        result = self._values.get("ssl_ca")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webhook_secret_secret_version(self) -> typing.Optional[builtins.str]:
        '''SecretManager resource containing the webhook secret of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#webhook_secret_secret_version Cloudbuildv2Connection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudbuildv2ConnectionGithubEnterpriseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudbuildv2ConnectionGithubEnterpriseConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGithubEnterpriseConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77ed0aff6bdbca9e1baec04d322288f9c6baef334dd276f63c1e19a7e8b6d642)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putServiceDirectoryConfig")
    def put_service_directory_config(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service Cloudbuildv2Connection#service}
        '''
        value = Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig(
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
    ) -> "Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference":
        return typing.cast("Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference", jsii.get(self, "serviceDirectoryConfig"))

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
    ) -> typing.Optional["Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig"]:
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig"], jsii.get(self, "serviceDirectoryConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__84ad9d014c896d4df8e535d8412cfa9242d0f7e7e69f2ad581f3bb19539b33bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appInstallationId")
    def app_installation_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "appInstallationId"))

    @app_installation_id.setter
    def app_installation_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e1daa5abf6e4ec61e87b95d3474b6781589397ec88fe22024d7fbbb723c47c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appInstallationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appSlug")
    def app_slug(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSlug"))

    @app_slug.setter
    def app_slug(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__297ff9887a88f7728ce3c9fbb7dff315489256524f4c6341331024b213e37354)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSlug", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostUri")
    def host_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostUri"))

    @host_uri.setter
    def host_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0794dac9766e961b4c9db842a53dd5ca92e5b776112690a87b95539b3a313433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKeySecretVersion")
    def private_key_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKeySecretVersion"))

    @private_key_secret_version.setter
    def private_key_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc681c8bee3fd36febbd57c57d09a98d1d52b444ea709f9d2de898c52a42e0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeySecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCa")
    def ssl_ca(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCa"))

    @ssl_ca.setter
    def ssl_ca(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0146d2c89802451d1552129ec07ad9251ae6ce2b51227169cd2caaf47c0cfed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretSecretVersion"))

    @webhook_secret_secret_version.setter
    def webhook_secret_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b595d2041b5326a0a36788297e79e4d8fe20f40aa43ed1657426e3cbf99b0b5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionGithubEnterpriseConfig]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionGithubEnterpriseConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionGithubEnterpriseConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e535edc8e0d395da42e401b8de833ab0b552a0f68e1a9d0e154766ef320698db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"service": "service"},
)
class Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig:
    def __init__(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service Cloudbuildv2Connection#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8a44d8613b48e6a5c5ee194c528ab6cef304bfb0c838ae282f4c138c176f93)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service Cloudbuildv2Connection#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57cc0a5d832db9956eb8e6cf169a115ab84646fcf975a60ffb4bc7d9380e4e08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e342ab4518d68f56d234def5a5298048f41a8823d77032ec468ef7ff876ef4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e14c28814a665437dc6ae1dc4bdab00b51178ab3284845eeeb70be32d687b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGitlabConfig",
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
class Cloudbuildv2ConnectionGitlabConfig:
    def __init__(
        self,
        *,
        authorizer_credential: typing.Union["Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        host_uri: typing.Optional[builtins.str] = None,
        service_directory_config: typing.Optional[typing.Union["Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#authorizer_credential Cloudbuildv2Connection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#read_authorizer_credential Cloudbuildv2Connection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret of a GitLab Enterprise project, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#webhook_secret_secret_version Cloudbuildv2Connection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param host_uri: The URI of the GitLab Enterprise host this connection is for. If not specified, the default value is https://gitlab.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#host_uri Cloudbuildv2Connection#host_uri}
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service_directory_config Cloudbuildv2Connection#service_directory_config}
        :param ssl_ca: SSL certificate to use for requests to GitLab Enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#ssl_ca Cloudbuildv2Connection#ssl_ca}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential(**authorizer_credential)
        if isinstance(read_authorizer_credential, dict):
            read_authorizer_credential = Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential(**read_authorizer_credential)
        if isinstance(service_directory_config, dict):
            service_directory_config = Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig(**service_directory_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd948762c360b6e92914b77d72ccba588d404a2abdf8b0845e9b8d188842beb)
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
    ) -> "Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential":
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#authorizer_credential Cloudbuildv2Connection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        assert result is not None, "Required property 'authorizer_credential' is missing"
        return typing.cast("Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential", result)

    @builtins.property
    def read_authorizer_credential(
        self,
    ) -> "Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential":
        '''read_authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#read_authorizer_credential Cloudbuildv2Connection#read_authorizer_credential}
        '''
        result = self._values.get("read_authorizer_credential")
        assert result is not None, "Required property 'read_authorizer_credential' is missing"
        return typing.cast("Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential", result)

    @builtins.property
    def webhook_secret_secret_version(self) -> builtins.str:
        '''Required. Immutable. SecretManager resource containing the webhook secret of a GitLab Enterprise project, formatted as 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#webhook_secret_secret_version Cloudbuildv2Connection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        assert result is not None, "Required property 'webhook_secret_secret_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the GitLab Enterprise host this connection is for. If not specified, the default value is https://gitlab.com.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#host_uri Cloudbuildv2Connection#host_uri}
        '''
        result = self._values.get("host_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_directory_config(
        self,
    ) -> typing.Optional["Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig"]:
        '''service_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service_directory_config Cloudbuildv2Connection#service_directory_config}
        '''
        result = self._values.get("service_directory_config")
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig"], result)

    @builtins.property
    def ssl_ca(self) -> typing.Optional[builtins.str]:
        '''SSL certificate to use for requests to GitLab Enterprise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#ssl_ca Cloudbuildv2Connection#ssl_ca}
        '''
        result = self._values.get("ssl_ca")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudbuildv2ConnectionGitlabConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7065fb1fba8dc2e536c87df3601f7acde035d54ab76247e453ed87fd982b0e29)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version}

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
        return "Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudbuildv2ConnectionGitlabConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGitlabConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bf4730d52820f8fad9cc9907df9e4996b7b0dab745ab100580fc632654ff44d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c362d6642316eab9c1449388919086af1eff07877b5c3091b14ac6b41888f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34caee6c631ae2ee019c4983b1ad171630cdb0ea0587d91aebf040ae09223885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Cloudbuildv2ConnectionGitlabConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGitlabConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb5a757af3f8ee684f1cc8b3cdfa8d4afa9e52f2c8823c5c09c6655c88728204)
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential(
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putReadAuthorizerCredential", [value]))

    @jsii.member(jsii_name="putServiceDirectoryConfig")
    def put_service_directory_config(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service Cloudbuildv2Connection#service}
        '''
        value = Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig(
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
    ) -> Cloudbuildv2ConnectionGitlabConfigAuthorizerCredentialOutputReference:
        return typing.cast(Cloudbuildv2ConnectionGitlabConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredential")
    def read_authorizer_credential(
        self,
    ) -> "Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredentialOutputReference":
        return typing.cast("Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredentialOutputReference", jsii.get(self, "readAuthorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="serverVersion")
    def server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverVersion"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfig")
    def service_directory_config(
        self,
    ) -> "Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfigOutputReference":
        return typing.cast("Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfigOutputReference", jsii.get(self, "serviceDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="hostUriInput")
    def host_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostUriInput"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredentialInput")
    def read_authorizer_credential_input(
        self,
    ) -> typing.Optional["Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential"]:
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential"], jsii.get(self, "readAuthorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfigInput")
    def service_directory_config_input(
        self,
    ) -> typing.Optional["Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig"]:
        return typing.cast(typing.Optional["Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig"], jsii.get(self, "serviceDirectoryConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__39d1cf8929b59a1f6d97063619ec2f0542fc5dc2e81a9998089de3082ac578a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCa")
    def ssl_ca(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCa"))

    @ssl_ca.setter
    def ssl_ca(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd94a22b1f64e9be284698d0e435beb59d24b6e78c0e67c4ff8f4c34c535ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretSecretVersion"))

    @webhook_secret_secret_version.setter
    def webhook_secret_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0e6d311df560f93c6c1315c527c9b4bd47f665b6161ff1724c6332bcce1a8a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Cloudbuildv2ConnectionGitlabConfig]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionGitlabConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionGitlabConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eaebbe83ec3a270b0fea820f2e0540fd51b55766351e27a9966f83f9907f397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e9a90b29d4541ddd7d78cb01963e31bae4465468eed93b0cb3ffee5174b3228)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#user_token_secret_version Cloudbuildv2Connection#user_token_secret_version}

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
        return "Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61c95e905b9c83f406ac750164a07607c14da0d8bdab22eb8d57d2f68fcf6fab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09039155c189f465e36867a099cd932e1b718ab8ed436647a5563ab832f8760c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980130c4a5432908dd2a653ebef87275f924efc57f9f9c02ef5060b02c2b3ccc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"service": "service"},
)
class Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig:
    def __init__(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service Cloudbuildv2Connection#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b734e2759c6f725dcb1f715f779ddec0a2664b6cf63c5c0d09557afd10f438)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#service Cloudbuildv2Connection#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6398bd4d1f5e1f75b8874d228f4da07f15858d771fc0c03a8a793629061a28b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b008f267beaab75be65a2d295ec68531564d6de95792fb96ea8e1de9bb7a95e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd58dada936e687cec350b0ed56f002d6a7574175827f4c9f267e38a229f3131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionInstallationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class Cloudbuildv2ConnectionInstallationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudbuildv2ConnectionInstallationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudbuildv2ConnectionInstallationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionInstallationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d33eebc558c44bf49b4a9c071b53c68c73750a488eecaf03280338924cf94970)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Cloudbuildv2ConnectionInstallationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d6c9ccdda3c5c68fd88c343bfecc89fd75cd92ea711cc197def732751b2e7e9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Cloudbuildv2ConnectionInstallationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55811fdf45ba32b2bf6d54e2b0db775ed552ffc4f9e5368c948787fef3a2146c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11920242b9feb033a3f6dfa46064f5d349158599a47f559cf7fe7f056a762fb8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__754a9476f28135e2d6ddd17a698c359bf276847780ca4f53e5f9203b6d9bef45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Cloudbuildv2ConnectionInstallationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionInstallationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__951f6a028737b10bf95143fb4251dfd6f68eb882132417a920af81f1e7a81a56)
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
    ) -> typing.Optional[Cloudbuildv2ConnectionInstallationState]:
        return typing.cast(typing.Optional[Cloudbuildv2ConnectionInstallationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Cloudbuildv2ConnectionInstallationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19cac2a4e9b99522c738ac5576267e28989a1f4352fbef06b906408055465693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class Cloudbuildv2ConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#create Cloudbuildv2Connection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#delete Cloudbuildv2Connection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#update Cloudbuildv2Connection#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05972f69886c116da3a983d2319b15a14e659e4db911cd496bd1b6308234cfed)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#create Cloudbuildv2Connection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#delete Cloudbuildv2Connection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuildv2_connection#update Cloudbuildv2Connection#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cloudbuildv2ConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cloudbuildv2ConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildv2Connection.Cloudbuildv2ConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__798682c14600e889b45fa3c7fce10645ba1a7791aae15aab0d2bd426963491b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efba59495c5a322839853341c73cafffd4269f2986d4959413e4ea8074e46403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73ccea5fe513bb91a3254cf1ed035bf7c5755578ab037abdf12f64aa80b466ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd76e52ee16812eacad9695de4080f3b58194ec35af2c347943d9de6f7a89109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudbuildv2ConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudbuildv2ConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudbuildv2ConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f43b9c3f2204374923d08a79790f976966b843b6f014250eb49dec23358824)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Cloudbuildv2Connection",
    "Cloudbuildv2ConnectionBitbucketCloudConfig",
    "Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential",
    "Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference",
    "Cloudbuildv2ConnectionBitbucketCloudConfigOutputReference",
    "Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential",
    "Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference",
    "Cloudbuildv2ConnectionBitbucketDataCenterConfig",
    "Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential",
    "Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference",
    "Cloudbuildv2ConnectionBitbucketDataCenterConfigOutputReference",
    "Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential",
    "Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference",
    "Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig",
    "Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference",
    "Cloudbuildv2ConnectionConfig",
    "Cloudbuildv2ConnectionGithubConfig",
    "Cloudbuildv2ConnectionGithubConfigAuthorizerCredential",
    "Cloudbuildv2ConnectionGithubConfigAuthorizerCredentialOutputReference",
    "Cloudbuildv2ConnectionGithubConfigOutputReference",
    "Cloudbuildv2ConnectionGithubEnterpriseConfig",
    "Cloudbuildv2ConnectionGithubEnterpriseConfigOutputReference",
    "Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig",
    "Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference",
    "Cloudbuildv2ConnectionGitlabConfig",
    "Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential",
    "Cloudbuildv2ConnectionGitlabConfigAuthorizerCredentialOutputReference",
    "Cloudbuildv2ConnectionGitlabConfigOutputReference",
    "Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential",
    "Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredentialOutputReference",
    "Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig",
    "Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfigOutputReference",
    "Cloudbuildv2ConnectionInstallationState",
    "Cloudbuildv2ConnectionInstallationStateList",
    "Cloudbuildv2ConnectionInstallationStateOutputReference",
    "Cloudbuildv2ConnectionTimeouts",
    "Cloudbuildv2ConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f327521b7ef91321641159e8e6dc2e7ac30ef31189ca3e3b8057808220c1de2d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bitbucket_cloud_config: typing.Optional[typing.Union[Cloudbuildv2ConnectionBitbucketCloudConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bitbucket_data_center_config: typing.Optional[typing.Union[Cloudbuildv2ConnectionBitbucketDataCenterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    github_config: typing.Optional[typing.Union[Cloudbuildv2ConnectionGithubConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    github_enterprise_config: typing.Optional[typing.Union[Cloudbuildv2ConnectionGithubEnterpriseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gitlab_config: typing.Optional[typing.Union[Cloudbuildv2ConnectionGitlabConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[Cloudbuildv2ConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e298b50d4128d53271e2465f3e1e6240744a1d25a5986f80fe1cae9fc135d29f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab644863a8af6e48b4ed49e96e0ff41fb37e6904cb86809eac53bc04e42cd679(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf69d29a1fa557d7fb3fa1b2d1b84c629c013b060c10a87c8fc9b19f3bfe650(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7576007a13b4b0c968094f518ad6ef3cc481720ad44cb718b4e26baafa7a91a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8d45e31b445e17142d1ef2c2d8e78dc0b3b292f586171ab08860d67fe9b5e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abbc131ecc3747cd789d9e971b691402f711fc8464413009a72c6c31aeca00c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64eba0d4139c25f99a3f50274ede658998e2b6ca7d1142bbe0938f0e2adb987c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4c76fb36a101559b16d43533f50f09366a2ca345e4c20a7b37886d36b06215(
    *,
    authorizer_credential: typing.Union[Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    read_authorizer_credential: typing.Union[Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    webhook_secret_secret_version: builtins.str,
    workspace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d124b8ff2d5fd3589f1b94e31a543a8e8768783c2c3281b8990472cb2957eaf(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef31e69ef97c45af00b121169aabda96e73f6d5d93649c9468d138b752104c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9badd1c82ad9b607f6aa08567acd00feaf5cb92c9a2d7343d68bcd5ec53ea75c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f21eb585dc2b26d37e75fd6b755fc0f7fcf2f103ca580d2a3a12285931297c(
    value: typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e197c9780fbf6015cafe17a40435d88f4e6cefe764ea002d472ff2a0721aed33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca28791024a33e87ae5d3f5a9e3cf11c9f707d4d197cabd405d270895db0f10d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e16a1c725ada3d87cf476aeda6fc2a9ec41d9c589a99993aec8b246300fda0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99bd227db1fe3aeb3db382125b2cde99d28ff0b33b76ac539ce5d9bc133a7fc(
    value: typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dbb3e85738134313b363c4306face699da8a67652f40d7fd3e6463fb625066d(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60f7f75bed739e3858ab9d48cda02187fad00592a3f239673e9ef0dfd15e675(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d4ba2d0b166df101c754cfe150d93c4cd7584ecba8e8af3845242ef7f9592c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377668b18ab476b6628e64cb2dfa869619e94db457826944a1c3c53eb41e6670(
    value: typing.Optional[Cloudbuildv2ConnectionBitbucketCloudConfigReadAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088b8cc0d88b1dc312e77f8f5c6f1bf1c7d3050cd85657422c06daf5e19300a1(
    *,
    authorizer_credential: typing.Union[Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    host_uri: builtins.str,
    read_authorizer_credential: typing.Union[Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    webhook_secret_secret_version: builtins.str,
    service_directory_config: typing.Optional[typing.Union[Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_ca: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35eab05d8caf6aa08d11ce48e4aa3e47d8e4fa3891c6d2a92d94610876f9254e(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee3044a4d1077ef31e8281243dbd5719bd1f96f8562af526240adf5e92f2bd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91b65ed6e0c7c53d74c39ef846b4c1788449d8f028093d1b58f7edccdb1817d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a990341d11caeea455dcf3df777b8cb549139af67b174f24ac98441ceb10ad(
    value: typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515d56693c6946a90a67a8335766ed1b0f733dfe94e9cb39aec81a452f3ed2f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2669e5c7cf5840dee24c0ad8d79f8d0e96e9132e6df2b473bf312ac7e7ca24c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9dd9d51afe261a8fd23e49636ee8c40d6cc5c261ef9c402db6f695f8a022c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c544aa1530682d22a4003f502cd2567b19dd6eb7a7b4b5105b68ba7d6a897296(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278ecc24dfb1ab217cdb37108865ff9f4e4292d8fb2ac135ccd746ed2bf64b8f(
    value: typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23caef4a4d843b0c19daa5933517f486c87d446c7d1be6d42c3e5099e7978e30(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__508aba201234b9de02374842db5f66349333c7474785153926113a49a2191aef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567a0f242eae98dd2f90a17a6d54f64ae3d9d09b240b357c0d9ea4dd7a69500b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6548eb08cca7c6d10183ab1c5d4b951c3b1a5903bbcbec69610f3ea103c4f524(
    value: typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfigReadAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe2ab2612126d994c30e8b22e83b4195e859932fcbca28ea70f3ff653029643(
    *,
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21c4c42ea25bb5eec36d994f8b5738eea5518a46a46eb072d0cf3acc1a56e07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f61f3eadd9700406ada31ab03ca0789f4ad2423dcc5fe8e54342fa87ad4e6a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135d9afb3f4ea603e502b8ed3c747c02fb919938c79eb2e1d37dd99a1ee6522b(
    value: typing.Optional[Cloudbuildv2ConnectionBitbucketDataCenterConfigServiceDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7a39d7c5bfe9d502648a40f0275f3c50c8785e852bc88e6a6af9087b24513d(
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
    bitbucket_cloud_config: typing.Optional[typing.Union[Cloudbuildv2ConnectionBitbucketCloudConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bitbucket_data_center_config: typing.Optional[typing.Union[Cloudbuildv2ConnectionBitbucketDataCenterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    github_config: typing.Optional[typing.Union[Cloudbuildv2ConnectionGithubConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    github_enterprise_config: typing.Optional[typing.Union[Cloudbuildv2ConnectionGithubEnterpriseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gitlab_config: typing.Optional[typing.Union[Cloudbuildv2ConnectionGitlabConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[Cloudbuildv2ConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43a04979e49eeb0bd8f62e4c709d4674365694312eb10f7d7c8c3ca9c72f5ae(
    *,
    app_installation_id: typing.Optional[jsii.Number] = None,
    authorizer_credential: typing.Optional[typing.Union[Cloudbuildv2ConnectionGithubConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903568966873c58e69c0d1770998500cf7dd80a01efe6f8c03b2b19a952080ef(
    *,
    oauth_token_secret_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4daf7401842ca5996fa45a11a0f2ab25678ddafa7c5b5116c67386864bfa1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb50bd49d3fbf9d64a5be7b932ad2de376bff1b09df2510bd387d732c753d198(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48cf0b26345a327d2ad3afa524cae0102345d2e5a63cde5ec1509cb42ec4d5b2(
    value: typing.Optional[Cloudbuildv2ConnectionGithubConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9ee4532cac6f89413f058d357435112e3d571338df522568bebc758a5f2951(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc212c354bf816364689b637b8ee1be97fd4719e62f5677668d39c8dcd0f3f1c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ac16cec169d0d3ff5e9e00ab760384593d6a6d18598a85cc654b4e627b4c72(
    value: typing.Optional[Cloudbuildv2ConnectionGithubConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286291dc21651914736822f99d786cb7b0e630b2cbd1056c3aa44bd53ad97a66(
    *,
    host_uri: builtins.str,
    app_id: typing.Optional[jsii.Number] = None,
    app_installation_id: typing.Optional[jsii.Number] = None,
    app_slug: typing.Optional[builtins.str] = None,
    private_key_secret_version: typing.Optional[builtins.str] = None,
    service_directory_config: typing.Optional[typing.Union[Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_ca: typing.Optional[builtins.str] = None,
    webhook_secret_secret_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ed0aff6bdbca9e1baec04d322288f9c6baef334dd276f63c1e19a7e8b6d642(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ad9d014c896d4df8e535d8412cfa9242d0f7e7e69f2ad581f3bb19539b33bd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e1daa5abf6e4ec61e87b95d3474b6781589397ec88fe22024d7fbbb723c47c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297ff9887a88f7728ce3c9fbb7dff315489256524f4c6341331024b213e37354(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0794dac9766e961b4c9db842a53dd5ca92e5b776112690a87b95539b3a313433(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc681c8bee3fd36febbd57c57d09a98d1d52b444ea709f9d2de898c52a42e0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0146d2c89802451d1552129ec07ad9251ae6ce2b51227169cd2caaf47c0cfed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b595d2041b5326a0a36788297e79e4d8fe20f40aa43ed1657426e3cbf99b0b5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e535edc8e0d395da42e401b8de833ab0b552a0f68e1a9d0e154766ef320698db(
    value: typing.Optional[Cloudbuildv2ConnectionGithubEnterpriseConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8a44d8613b48e6a5c5ee194c528ab6cef304bfb0c838ae282f4c138c176f93(
    *,
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57cc0a5d832db9956eb8e6cf169a115ab84646fcf975a60ffb4bc7d9380e4e08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e342ab4518d68f56d234def5a5298048f41a8823d77032ec468ef7ff876ef4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e14c28814a665437dc6ae1dc4bdab00b51178ab3284845eeeb70be32d687b6(
    value: typing.Optional[Cloudbuildv2ConnectionGithubEnterpriseConfigServiceDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd948762c360b6e92914b77d72ccba588d404a2abdf8b0845e9b8d188842beb(
    *,
    authorizer_credential: typing.Union[Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    read_authorizer_credential: typing.Union[Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    webhook_secret_secret_version: builtins.str,
    host_uri: typing.Optional[builtins.str] = None,
    service_directory_config: typing.Optional[typing.Union[Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_ca: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7065fb1fba8dc2e536c87df3601f7acde035d54ab76247e453ed87fd982b0e29(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bf4730d52820f8fad9cc9907df9e4996b7b0dab745ab100580fc632654ff44d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c362d6642316eab9c1449388919086af1eff07877b5c3091b14ac6b41888f72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34caee6c631ae2ee019c4983b1ad171630cdb0ea0587d91aebf040ae09223885(
    value: typing.Optional[Cloudbuildv2ConnectionGitlabConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb5a757af3f8ee684f1cc8b3cdfa8d4afa9e52f2c8823c5c09c6655c88728204(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d1cf8929b59a1f6d97063619ec2f0542fc5dc2e81a9998089de3082ac578a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd94a22b1f64e9be284698d0e435beb59d24b6e78c0e67c4ff8f4c34c535ecf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e6d311df560f93c6c1315c527c9b4bd47f665b6161ff1724c6332bcce1a8a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eaebbe83ec3a270b0fea820f2e0540fd51b55766351e27a9966f83f9907f397(
    value: typing.Optional[Cloudbuildv2ConnectionGitlabConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e9a90b29d4541ddd7d78cb01963e31bae4465468eed93b0cb3ffee5174b3228(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c95e905b9c83f406ac750164a07607c14da0d8bdab22eb8d57d2f68fcf6fab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09039155c189f465e36867a099cd932e1b718ab8ed436647a5563ab832f8760c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980130c4a5432908dd2a653ebef87275f924efc57f9f9c02ef5060b02c2b3ccc(
    value: typing.Optional[Cloudbuildv2ConnectionGitlabConfigReadAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b734e2759c6f725dcb1f715f779ddec0a2664b6cf63c5c0d09557afd10f438(
    *,
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6398bd4d1f5e1f75b8874d228f4da07f15858d771fc0c03a8a793629061a28b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b008f267beaab75be65a2d295ec68531564d6de95792fb96ea8e1de9bb7a95e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd58dada936e687cec350b0ed56f002d6a7574175827f4c9f267e38a229f3131(
    value: typing.Optional[Cloudbuildv2ConnectionGitlabConfigServiceDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d33eebc558c44bf49b4a9c071b53c68c73750a488eecaf03280338924cf94970(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d6c9ccdda3c5c68fd88c343bfecc89fd75cd92ea711cc197def732751b2e7e9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55811fdf45ba32b2bf6d54e2b0db775ed552ffc4f9e5368c948787fef3a2146c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11920242b9feb033a3f6dfa46064f5d349158599a47f559cf7fe7f056a762fb8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754a9476f28135e2d6ddd17a698c359bf276847780ca4f53e5f9203b6d9bef45(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951f6a028737b10bf95143fb4251dfd6f68eb882132417a920af81f1e7a81a56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19cac2a4e9b99522c738ac5576267e28989a1f4352fbef06b906408055465693(
    value: typing.Optional[Cloudbuildv2ConnectionInstallationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05972f69886c116da3a983d2319b15a14e659e4db911cd496bd1b6308234cfed(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798682c14600e889b45fa3c7fce10645ba1a7791aae15aab0d2bd426963491b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efba59495c5a322839853341c73cafffd4269f2986d4959413e4ea8074e46403(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ccea5fe513bb91a3254cf1ed035bf7c5755578ab037abdf12f64aa80b466ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd76e52ee16812eacad9695de4080f3b58194ec35af2c347943d9de6f7a89109(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f43b9c3f2204374923d08a79790f976966b843b6f014250eb49dec23358824(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Cloudbuildv2ConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

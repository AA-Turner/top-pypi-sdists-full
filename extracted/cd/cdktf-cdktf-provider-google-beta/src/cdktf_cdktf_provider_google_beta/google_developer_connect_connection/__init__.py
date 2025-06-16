r'''
# `google_developer_connect_connection`

Refer to the Terraform Registry for docs: [`google_developer_connect_connection`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection).
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


class GoogleDeveloperConnectConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection google_developer_connect_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        connection_id: builtins.str,
        location: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bitbucket_cloud_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionBitbucketCloudConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        bitbucket_data_center_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionBitbucketDataCenterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        crypto_key_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionCryptoKeyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        etag: typing.Optional[builtins.str] = None,
        github_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionGithubConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        github_enterprise_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionGithubEnterpriseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gitlab_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionGitlabConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gitlab_enterprise_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionGitlabEnterpriseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection google_developer_connect_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param connection_id: Required. Id of the requesting object If auto-generating Id server-side, remove this field and connection_id from the method_signature of Create RPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#connection_id GoogleDeveloperConnectConnection#connection_id}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#location GoogleDeveloperConnectConnection#location}
        :param annotations: Optional. Allows clients to store small amounts of arbitrary data. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#annotations GoogleDeveloperConnectConnection#annotations}
        :param bitbucket_cloud_config: bitbucket_cloud_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#bitbucket_cloud_config GoogleDeveloperConnectConnection#bitbucket_cloud_config}
        :param bitbucket_data_center_config: bitbucket_data_center_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#bitbucket_data_center_config GoogleDeveloperConnectConnection#bitbucket_data_center_config}
        :param crypto_key_config: crypto_key_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#crypto_key_config GoogleDeveloperConnectConnection#crypto_key_config}
        :param disabled: Optional. If disabled is set to true, functionality is disabled for this connection. Repository based API methods and webhooks processing for repositories in this connection will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#disabled GoogleDeveloperConnectConnection#disabled}
        :param etag: Optional. This checksum is computed by the server based on the value of other fields, and may be sent on update and delete requests to ensure the client has an up-to-date value before proceeding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#etag GoogleDeveloperConnectConnection#etag}
        :param github_config: github_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#github_config GoogleDeveloperConnectConnection#github_config}
        :param github_enterprise_config: github_enterprise_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#github_enterprise_config GoogleDeveloperConnectConnection#github_enterprise_config}
        :param gitlab_config: gitlab_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#gitlab_config GoogleDeveloperConnectConnection#gitlab_config}
        :param gitlab_enterprise_config: gitlab_enterprise_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#gitlab_enterprise_config GoogleDeveloperConnectConnection#gitlab_enterprise_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#id GoogleDeveloperConnectConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#labels GoogleDeveloperConnectConnection#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#project GoogleDeveloperConnectConnection#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#timeouts GoogleDeveloperConnectConnection#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d019c75242c0ef7adbf3e363b4c2ccc0d579eefa451f9b61effc57d67801f956)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDeveloperConnectConnectionConfig(
            connection_id=connection_id,
            location=location,
            annotations=annotations,
            bitbucket_cloud_config=bitbucket_cloud_config,
            bitbucket_data_center_config=bitbucket_data_center_config,
            crypto_key_config=crypto_key_config,
            disabled=disabled,
            etag=etag,
            github_config=github_config,
            github_enterprise_config=github_enterprise_config,
            gitlab_config=gitlab_config,
            gitlab_enterprise_config=gitlab_enterprise_config,
            id=id,
            labels=labels,
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
        '''Generates CDKTF code for importing a GoogleDeveloperConnectConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDeveloperConnectConnection to import.
        :param import_from_id: The id of the existing GoogleDeveloperConnectConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDeveloperConnectConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175f5cef411a2276d3371bd7225e1d3a20d48a0b8b38df544325338f1e54dd42)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBitbucketCloudConfig")
    def put_bitbucket_cloud_config(
        self,
        *,
        authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        workspace: builtins.str,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#authorizer_credential GoogleDeveloperConnectConnection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#read_authorizer_credential GoogleDeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate and create webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#webhook_secret_secret_version GoogleDeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param workspace: Required. The Bitbucket Cloud Workspace ID to be connected to Google Cloud Platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#workspace GoogleDeveloperConnectConnection#workspace}
        '''
        value = GoogleDeveloperConnectConnectionBitbucketCloudConfig(
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
        authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        host_uri: builtins.str,
        read_authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        service_directory_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca_certificate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#authorizer_credential GoogleDeveloperConnectConnection#authorizer_credential}
        :param host_uri: Required. The URI of the Bitbucket Data Center host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#host_uri GoogleDeveloperConnectConnection#host_uri}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#read_authorizer_credential GoogleDeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#webhook_secret_secret_version GoogleDeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service_directory_config GoogleDeveloperConnectConnection#service_directory_config}
        :param ssl_ca_certificate: Optional. SSL certificate authority to trust when making requests to Bitbucket Data Center. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#ssl_ca_certificate GoogleDeveloperConnectConnection#ssl_ca_certificate}
        '''
        value = GoogleDeveloperConnectConnectionBitbucketDataCenterConfig(
            authorizer_credential=authorizer_credential,
            host_uri=host_uri,
            read_authorizer_credential=read_authorizer_credential,
            webhook_secret_secret_version=webhook_secret_secret_version,
            service_directory_config=service_directory_config,
            ssl_ca_certificate=ssl_ca_certificate,
        )

        return typing.cast(None, jsii.invoke(self, "putBitbucketDataCenterConfig", [value]))

    @jsii.member(jsii_name="putCryptoKeyConfig")
    def put_crypto_key_config(self, *, key_reference: builtins.str) -> None:
        '''
        :param key_reference: Required. The name of the key which is used to encrypt/decrypt customer data. For key in Cloud KMS, the key should be in the format of 'projects/* /locations/* /keyRings/* /cryptoKeys/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#key_reference GoogleDeveloperConnectConnection#key_reference} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleDeveloperConnectConnectionCryptoKeyConfig(
            key_reference=key_reference
        )

        return typing.cast(None, jsii.invoke(self, "putCryptoKeyConfig", [value]))

    @jsii.member(jsii_name="putGithubConfig")
    def put_github_config(
        self,
        *,
        github_app: builtins.str,
        app_installation_id: typing.Optional[builtins.str] = None,
        authorizer_credential: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param github_app: Required. Immutable. The GitHub Application that was installed to the GitHub user or organization. Possible values: GIT_HUB_APP_UNSPECIFIED DEVELOPER_CONNECT FIREBASE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#github_app GoogleDeveloperConnectConnection#github_app}
        :param app_installation_id: Optional. GitHub App installation id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#app_installation_id GoogleDeveloperConnectConnection#app_installation_id}
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#authorizer_credential GoogleDeveloperConnectConnection#authorizer_credential}
        '''
        value = GoogleDeveloperConnectConnectionGithubConfig(
            github_app=github_app,
            app_installation_id=app_installation_id,
            authorizer_credential=authorizer_credential,
        )

        return typing.cast(None, jsii.invoke(self, "putGithubConfig", [value]))

    @jsii.member(jsii_name="putGithubEnterpriseConfig")
    def put_github_enterprise_config(
        self,
        *,
        host_uri: builtins.str,
        app_id: typing.Optional[builtins.str] = None,
        app_installation_id: typing.Optional[builtins.str] = None,
        private_key_secret_version: typing.Optional[builtins.str] = None,
        service_directory_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca_certificate: typing.Optional[builtins.str] = None,
        webhook_secret_secret_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_uri: Required. The URI of the GitHub Enterprise host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#host_uri GoogleDeveloperConnectConnection#host_uri}
        :param app_id: Optional. ID of the GitHub App created from the manifest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#app_id GoogleDeveloperConnectConnection#app_id}
        :param app_installation_id: Optional. ID of the installation of the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#app_installation_id GoogleDeveloperConnectConnection#app_installation_id}
        :param private_key_secret_version: Optional. SecretManager resource containing the private key of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#private_key_secret_version GoogleDeveloperConnectConnection#private_key_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service_directory_config GoogleDeveloperConnectConnection#service_directory_config}
        :param ssl_ca_certificate: Optional. SSL certificate to use for requests to GitHub Enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#ssl_ca_certificate GoogleDeveloperConnectConnection#ssl_ca_certificate}
        :param webhook_secret_secret_version: Optional. SecretManager resource containing the webhook secret of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#webhook_secret_secret_version GoogleDeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleDeveloperConnectConnectionGithubEnterpriseConfig(
            host_uri=host_uri,
            app_id=app_id,
            app_installation_id=app_installation_id,
            private_key_secret_version=private_key_secret_version,
            service_directory_config=service_directory_config,
            ssl_ca_certificate=ssl_ca_certificate,
            webhook_secret_secret_version=webhook_secret_secret_version,
        )

        return typing.cast(None, jsii.invoke(self, "putGithubEnterpriseConfig", [value]))

    @jsii.member(jsii_name="putGitlabConfig")
    def put_gitlab_config(
        self,
        *,
        authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#authorizer_credential GoogleDeveloperConnectConnection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#read_authorizer_credential GoogleDeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret of a GitLab project, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#webhook_secret_secret_version GoogleDeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleDeveloperConnectConnectionGitlabConfig(
            authorizer_credential=authorizer_credential,
            read_authorizer_credential=read_authorizer_credential,
            webhook_secret_secret_version=webhook_secret_secret_version,
        )

        return typing.cast(None, jsii.invoke(self, "putGitlabConfig", [value]))

    @jsii.member(jsii_name="putGitlabEnterpriseConfig")
    def put_gitlab_enterprise_config(
        self,
        *,
        authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        host_uri: builtins.str,
        read_authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        service_directory_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca_certificate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#authorizer_credential GoogleDeveloperConnectConnection#authorizer_credential}
        :param host_uri: Required. The URI of the GitLab Enterprise host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#host_uri GoogleDeveloperConnectConnection#host_uri}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#read_authorizer_credential GoogleDeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret of a GitLab project, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#webhook_secret_secret_version GoogleDeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service_directory_config GoogleDeveloperConnectConnection#service_directory_config}
        :param ssl_ca_certificate: Optional. SSL Certificate Authority certificate to use for requests to GitLab Enterprise instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#ssl_ca_certificate GoogleDeveloperConnectConnection#ssl_ca_certificate}
        '''
        value = GoogleDeveloperConnectConnectionGitlabEnterpriseConfig(
            authorizer_credential=authorizer_credential,
            host_uri=host_uri,
            read_authorizer_credential=read_authorizer_credential,
            webhook_secret_secret_version=webhook_secret_secret_version,
            service_directory_config=service_directory_config,
            ssl_ca_certificate=ssl_ca_certificate,
        )

        return typing.cast(None, jsii.invoke(self, "putGitlabEnterpriseConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#create GoogleDeveloperConnectConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#delete GoogleDeveloperConnectConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#update GoogleDeveloperConnectConnection#update}.
        '''
        value = GoogleDeveloperConnectConnectionTimeouts(
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

    @jsii.member(jsii_name="resetCryptoKeyConfig")
    def reset_crypto_key_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCryptoKeyConfig", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetEtag")
    def reset_etag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEtag", []))

    @jsii.member(jsii_name="resetGithubConfig")
    def reset_github_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithubConfig", []))

    @jsii.member(jsii_name="resetGithubEnterpriseConfig")
    def reset_github_enterprise_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithubEnterpriseConfig", []))

    @jsii.member(jsii_name="resetGitlabConfig")
    def reset_gitlab_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitlabConfig", []))

    @jsii.member(jsii_name="resetGitlabEnterpriseConfig")
    def reset_gitlab_enterprise_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitlabEnterpriseConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

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
    ) -> "GoogleDeveloperConnectConnectionBitbucketCloudConfigOutputReference":
        return typing.cast("GoogleDeveloperConnectConnectionBitbucketCloudConfigOutputReference", jsii.get(self, "bitbucketCloudConfig"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketDataCenterConfig")
    def bitbucket_data_center_config(
        self,
    ) -> "GoogleDeveloperConnectConnectionBitbucketDataCenterConfigOutputReference":
        return typing.cast("GoogleDeveloperConnectConnectionBitbucketDataCenterConfigOutputReference", jsii.get(self, "bitbucketDataCenterConfig"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyConfig")
    def crypto_key_config(
        self,
    ) -> "GoogleDeveloperConnectConnectionCryptoKeyConfigOutputReference":
        return typing.cast("GoogleDeveloperConnectConnectionCryptoKeyConfigOutputReference", jsii.get(self, "cryptoKeyConfig"))

    @builtins.property
    @jsii.member(jsii_name="deleteTime")
    def delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="githubConfig")
    def github_config(
        self,
    ) -> "GoogleDeveloperConnectConnectionGithubConfigOutputReference":
        return typing.cast("GoogleDeveloperConnectConnectionGithubConfigOutputReference", jsii.get(self, "githubConfig"))

    @builtins.property
    @jsii.member(jsii_name="githubEnterpriseConfig")
    def github_enterprise_config(
        self,
    ) -> "GoogleDeveloperConnectConnectionGithubEnterpriseConfigOutputReference":
        return typing.cast("GoogleDeveloperConnectConnectionGithubEnterpriseConfigOutputReference", jsii.get(self, "githubEnterpriseConfig"))

    @builtins.property
    @jsii.member(jsii_name="gitlabConfig")
    def gitlab_config(
        self,
    ) -> "GoogleDeveloperConnectConnectionGitlabConfigOutputReference":
        return typing.cast("GoogleDeveloperConnectConnectionGitlabConfigOutputReference", jsii.get(self, "gitlabConfig"))

    @builtins.property
    @jsii.member(jsii_name="gitlabEnterpriseConfig")
    def gitlab_enterprise_config(
        self,
    ) -> "GoogleDeveloperConnectConnectionGitlabEnterpriseConfigOutputReference":
        return typing.cast("GoogleDeveloperConnectConnectionGitlabEnterpriseConfigOutputReference", jsii.get(self, "gitlabEnterpriseConfig"))

    @builtins.property
    @jsii.member(jsii_name="installationState")
    def installation_state(
        self,
    ) -> "GoogleDeveloperConnectConnectionInstallationStateList":
        return typing.cast("GoogleDeveloperConnectConnectionInstallationStateList", jsii.get(self, "installationState"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDeveloperConnectConnectionTimeoutsOutputReference":
        return typing.cast("GoogleDeveloperConnectConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

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
    ) -> typing.Optional["GoogleDeveloperConnectConnectionBitbucketCloudConfig"]:
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionBitbucketCloudConfig"], jsii.get(self, "bitbucketCloudConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketDataCenterConfigInput")
    def bitbucket_data_center_config_input(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionBitbucketDataCenterConfig"]:
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionBitbucketDataCenterConfig"], jsii.get(self, "bitbucketDataCenterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionIdInput")
    def connection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyConfigInput")
    def crypto_key_config_input(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionCryptoKeyConfig"]:
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionCryptoKeyConfig"], jsii.get(self, "cryptoKeyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="etagInput")
    def etag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "etagInput"))

    @builtins.property
    @jsii.member(jsii_name="githubConfigInput")
    def github_config_input(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionGithubConfig"]:
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionGithubConfig"], jsii.get(self, "githubConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="githubEnterpriseConfigInput")
    def github_enterprise_config_input(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionGithubEnterpriseConfig"]:
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionGithubEnterpriseConfig"], jsii.get(self, "githubEnterpriseConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gitlabConfigInput")
    def gitlab_config_input(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionGitlabConfig"]:
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionGitlabConfig"], jsii.get(self, "gitlabConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gitlabEnterpriseConfigInput")
    def gitlab_enterprise_config_input(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionGitlabEnterpriseConfig"]:
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionGitlabEnterpriseConfig"], jsii.get(self, "gitlabEnterpriseConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDeveloperConnectConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDeveloperConnectConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35049cef196ec2e0479b080fe180ac82ab01ce8dec6b6489fca6147f02311cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionId")
    def connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionId"))

    @connection_id.setter
    def connection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87413ffcb34301a2a0f51b79f5fbaf988e6609740105fe6b6b58122d8a197489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionId", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__8ca15962991343397d2111e5c5ec22471ca5a53116cdc3c4112176517f7e7d1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @etag.setter
    def etag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbdce802dcf2989f8cb91e0520027d27e9c8c626c9c6304f6306b05dbeaeee3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "etag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c48fc18c4fecb6657bd76d647029ad4c36ff5104f6642df72c3265a66f58ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be7148525c7ab6813a3e0a20d76beeec9168abdd567345cdfc4af354ac57740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0397857237152162f5e49387eddfec93ef90c19139af70bf56a653bf31d1f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37b7c27e9ff53f7ee2fcfe298e857e916570b35871e9b321c22075b24e65450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionBitbucketCloudConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_credential": "authorizerCredential",
        "read_authorizer_credential": "readAuthorizerCredential",
        "webhook_secret_secret_version": "webhookSecretSecretVersion",
        "workspace": "workspace",
    },
)
class GoogleDeveloperConnectConnectionBitbucketCloudConfig:
    def __init__(
        self,
        *,
        authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        workspace: builtins.str,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#authorizer_credential GoogleDeveloperConnectConnection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#read_authorizer_credential GoogleDeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate and create webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#webhook_secret_secret_version GoogleDeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param workspace: Required. The Bitbucket Cloud Workspace ID to be connected to Google Cloud Platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#workspace GoogleDeveloperConnectConnection#workspace}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential(**authorizer_credential)
        if isinstance(read_authorizer_credential, dict):
            read_authorizer_credential = GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential(**read_authorizer_credential)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26c549b09009e83f7cacfe30df6be081b52b0af35ecae3724ab307afd940d1ad)
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
    ) -> "GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential":
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#authorizer_credential GoogleDeveloperConnectConnection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        assert result is not None, "Required property 'authorizer_credential' is missing"
        return typing.cast("GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential", result)

    @builtins.property
    def read_authorizer_credential(
        self,
    ) -> "GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential":
        '''read_authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#read_authorizer_credential GoogleDeveloperConnectConnection#read_authorizer_credential}
        '''
        result = self._values.get("read_authorizer_credential")
        assert result is not None, "Required property 'read_authorizer_credential' is missing"
        return typing.cast("GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential", result)

    @builtins.property
    def webhook_secret_secret_version(self) -> builtins.str:
        '''Required.

        Immutable. SecretManager resource containing the webhook secret used to verify webhook
        events, formatted as 'projects/* /secrets/* /versions/*'. This is used to
        validate and create webhooks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#webhook_secret_secret_version GoogleDeveloperConnectConnection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        assert result is not None, "Required property 'webhook_secret_secret_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace(self) -> builtins.str:
        '''Required. The Bitbucket Cloud Workspace ID to be connected to Google Cloud Platform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#workspace GoogleDeveloperConnectConnection#workspace}
        '''
        result = self._values.get("workspace")
        assert result is not None, "Required property 'workspace' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectConnectionBitbucketCloudConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4111cb853b65cd7cdf84d91dcebe6f4ecdb9009c5bacf88218d9dd51ba4a3c67)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version}

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
        return "GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3605158ffebdbfd267556edc5ebe24855364fcf0b8fd88f27b902f4ccb509e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cfacfec39994a310368f9e9e114eb827e179c128af481add3f5a3109445cdc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82ddd59a425e73d93a8672762ac88656959e9bbc12cd321ae1f15c89cbab23fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDeveloperConnectConnectionBitbucketCloudConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionBitbucketCloudConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2c15c8ac077c9cf02f0dcac95ea8a9c4392d5df6b663a4f58e82490f8641939)
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential(
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putReadAuthorizerCredential", [value]))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredential")
    def authorizer_credential(
        self,
    ) -> GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference:
        return typing.cast(GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredential")
    def read_authorizer_credential(
        self,
    ) -> "GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference":
        return typing.cast("GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference", jsii.get(self, "readAuthorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredentialInput")
    def read_authorizer_credential_input(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential"]:
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential"], jsii.get(self, "readAuthorizerCredentialInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2048aa99ba68876d0afe2b38dc2c6812dcc0a610891b95292a213487621685fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspace")
    def workspace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspace"))

    @workspace.setter
    def workspace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a80c8f006177d6c0de1d509a0b4678cb9299e06533626f7dbc7c6a841e4462b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfig]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e0457f800ba329580ca0af8c450a89a9cd15091940b78ad1db294222725411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56d84557df7fca3d700bc51acd0078ccbffcefee3037d163c638709bb5579e2f)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version}

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
        return "GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14ae572bc295cdb0590a44c81d5c30ce0d583f01d39f9f80f85f5201c255356d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4707295e69492af504194b6977d5a0b227dd9f9c326cedabaf444b3cb669508b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ecf4c659fcbb6c181c21e5d5c212fad958a8159ab740f27f67d933c6d836800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionBitbucketDataCenterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_credential": "authorizerCredential",
        "host_uri": "hostUri",
        "read_authorizer_credential": "readAuthorizerCredential",
        "webhook_secret_secret_version": "webhookSecretSecretVersion",
        "service_directory_config": "serviceDirectoryConfig",
        "ssl_ca_certificate": "sslCaCertificate",
    },
)
class GoogleDeveloperConnectConnectionBitbucketDataCenterConfig:
    def __init__(
        self,
        *,
        authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        host_uri: builtins.str,
        read_authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        service_directory_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca_certificate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#authorizer_credential GoogleDeveloperConnectConnection#authorizer_credential}
        :param host_uri: Required. The URI of the Bitbucket Data Center host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#host_uri GoogleDeveloperConnectConnection#host_uri}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#read_authorizer_credential GoogleDeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#webhook_secret_secret_version GoogleDeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service_directory_config GoogleDeveloperConnectConnection#service_directory_config}
        :param ssl_ca_certificate: Optional. SSL certificate authority to trust when making requests to Bitbucket Data Center. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#ssl_ca_certificate GoogleDeveloperConnectConnection#ssl_ca_certificate}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential(**authorizer_credential)
        if isinstance(read_authorizer_credential, dict):
            read_authorizer_credential = GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential(**read_authorizer_credential)
        if isinstance(service_directory_config, dict):
            service_directory_config = GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig(**service_directory_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__455e422c6ca1f6939e3f9f9c9f535f6ae38a5371fd23de0c4954f97f0b893ab3)
            check_type(argname="argument authorizer_credential", value=authorizer_credential, expected_type=type_hints["authorizer_credential"])
            check_type(argname="argument host_uri", value=host_uri, expected_type=type_hints["host_uri"])
            check_type(argname="argument read_authorizer_credential", value=read_authorizer_credential, expected_type=type_hints["read_authorizer_credential"])
            check_type(argname="argument webhook_secret_secret_version", value=webhook_secret_secret_version, expected_type=type_hints["webhook_secret_secret_version"])
            check_type(argname="argument service_directory_config", value=service_directory_config, expected_type=type_hints["service_directory_config"])
            check_type(argname="argument ssl_ca_certificate", value=ssl_ca_certificate, expected_type=type_hints["ssl_ca_certificate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorizer_credential": authorizer_credential,
            "host_uri": host_uri,
            "read_authorizer_credential": read_authorizer_credential,
            "webhook_secret_secret_version": webhook_secret_secret_version,
        }
        if service_directory_config is not None:
            self._values["service_directory_config"] = service_directory_config
        if ssl_ca_certificate is not None:
            self._values["ssl_ca_certificate"] = ssl_ca_certificate

    @builtins.property
    def authorizer_credential(
        self,
    ) -> "GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential":
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#authorizer_credential GoogleDeveloperConnectConnection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        assert result is not None, "Required property 'authorizer_credential' is missing"
        return typing.cast("GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential", result)

    @builtins.property
    def host_uri(self) -> builtins.str:
        '''Required. The URI of the Bitbucket Data Center host this connection is for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#host_uri GoogleDeveloperConnectConnection#host_uri}
        '''
        result = self._values.get("host_uri")
        assert result is not None, "Required property 'host_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_authorizer_credential(
        self,
    ) -> "GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential":
        '''read_authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#read_authorizer_credential GoogleDeveloperConnectConnection#read_authorizer_credential}
        '''
        result = self._values.get("read_authorizer_credential")
        assert result is not None, "Required property 'read_authorizer_credential' is missing"
        return typing.cast("GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential", result)

    @builtins.property
    def webhook_secret_secret_version(self) -> builtins.str:
        '''Required.

        Immutable. SecretManager resource containing the webhook secret used to verify webhook
        events, formatted as 'projects/* /secrets/* /versions/*'. This is used to
        validate webhooks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#webhook_secret_secret_version GoogleDeveloperConnectConnection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        assert result is not None, "Required property 'webhook_secret_secret_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_directory_config(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig"]:
        '''service_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service_directory_config GoogleDeveloperConnectConnection#service_directory_config}
        '''
        result = self._values.get("service_directory_config")
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig"], result)

    @builtins.property
    def ssl_ca_certificate(self) -> typing.Optional[builtins.str]:
        '''Optional. SSL certificate authority to trust when making requests to Bitbucket Data Center.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#ssl_ca_certificate GoogleDeveloperConnectConnection#ssl_ca_certificate}
        '''
        result = self._values.get("ssl_ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectConnectionBitbucketDataCenterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45de49c73c0e0f12c3c8faacf8f4358aec37f9bcfa8c77581c7fe026c7cd5f38)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version}

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
        return "GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d05c539797204f7faa5fa190d05e0fa6f75f1aadc87584fa687f7e9514b9111)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95ac794f8c3212f434e4eb67310f82889a7b04732b9c695c0059d9e7d79a369a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b5df574359c8907faeab074c5eb1b04bc9d881f974ed84b4d06f4fa0653f14b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDeveloperConnectConnectionBitbucketDataCenterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionBitbucketDataCenterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d245107a2ddc0c0d4455b7cb1a4d63db4cfab0891d422b2ab98daaed40e6969f)
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential(
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putReadAuthorizerCredential", [value]))

    @jsii.member(jsii_name="putServiceDirectoryConfig")
    def put_service_directory_config(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service GoogleDeveloperConnectConnection#service}
        '''
        value = GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig(
            service=service
        )

        return typing.cast(None, jsii.invoke(self, "putServiceDirectoryConfig", [value]))

    @jsii.member(jsii_name="resetServiceDirectoryConfig")
    def reset_service_directory_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceDirectoryConfig", []))

    @jsii.member(jsii_name="resetSslCaCertificate")
    def reset_ssl_ca_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCaCertificate", []))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredential")
    def authorizer_credential(
        self,
    ) -> GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference:
        return typing.cast(GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredential")
    def read_authorizer_credential(
        self,
    ) -> "GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference":
        return typing.cast("GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference", jsii.get(self, "readAuthorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="serverVersion")
    def server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverVersion"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfig")
    def service_directory_config(
        self,
    ) -> "GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference":
        return typing.cast("GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference", jsii.get(self, "serviceDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="hostUriInput")
    def host_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostUriInput"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredentialInput")
    def read_authorizer_credential_input(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential"]:
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential"], jsii.get(self, "readAuthorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfigInput")
    def service_directory_config_input(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig"]:
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig"], jsii.get(self, "serviceDirectoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCaCertificateInput")
    def ssl_ca_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCaCertificateInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6d521a9a2d108787e02410dec44d853b56ec92a20bc67dff8d9bc67b6d8aafaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCaCertificate")
    def ssl_ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCaCertificate"))

    @ssl_ca_certificate.setter
    def ssl_ca_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99293d6e2321e4cb56ce407d9397017f630edc75333b2bc9bfa38381915620bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCaCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretSecretVersion"))

    @webhook_secret_secret_version.setter
    def webhook_secret_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8ad6bb265faf0703e1517462210e96765ddc7483e1f2dfcb301a9324de24237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfig]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93894d37e8d3565ca41bfc7bc9539af45bdb0e6f7253d76e8a02c440e8833ed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9718c663adcf73a265a9ebd4c5f8d45c82c8064128beecd8833b515d1e07dba)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version}

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
        return "GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efb29c126d54344490ad472268d88c30718992b91d059dd4794a1323dac85939)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6560eb599d5c6b045d5053587526b0239422155b8da575863c9de4ad302a17f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b23e0b0393b233728c95d738b601278e828a71333ee00a3c820c8628d6d4c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"service": "service"},
)
class GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig:
    def __init__(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service GoogleDeveloperConnectConnection#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a21a099830f6d211e1e11ac86a64670102df7bca24bf6fb66178d7d6e9c977b)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service GoogleDeveloperConnectConnection#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fa19fcba78ccb66211188342f8a985ab1993aa07a7ac297a002069c23ac2c18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc9c3eedd024cb8b37930133f826cf7985a4c7e7bdc421c87de9576f216a7b99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3049d907a46ddc4507f0664dbedc271046fd27aa0346cd5de0f93ab0780ac983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "connection_id": "connectionId",
        "location": "location",
        "annotations": "annotations",
        "bitbucket_cloud_config": "bitbucketCloudConfig",
        "bitbucket_data_center_config": "bitbucketDataCenterConfig",
        "crypto_key_config": "cryptoKeyConfig",
        "disabled": "disabled",
        "etag": "etag",
        "github_config": "githubConfig",
        "github_enterprise_config": "githubEnterpriseConfig",
        "gitlab_config": "gitlabConfig",
        "gitlab_enterprise_config": "gitlabEnterpriseConfig",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleDeveloperConnectConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        connection_id: builtins.str,
        location: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bitbucket_cloud_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionBitbucketCloudConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        bitbucket_data_center_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionBitbucketDataCenterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        crypto_key_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionCryptoKeyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        etag: typing.Optional[builtins.str] = None,
        github_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionGithubConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        github_enterprise_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionGithubEnterpriseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gitlab_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionGitlabConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gitlab_enterprise_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionGitlabEnterpriseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param connection_id: Required. Id of the requesting object If auto-generating Id server-side, remove this field and connection_id from the method_signature of Create RPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#connection_id GoogleDeveloperConnectConnection#connection_id}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#location GoogleDeveloperConnectConnection#location}
        :param annotations: Optional. Allows clients to store small amounts of arbitrary data. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#annotations GoogleDeveloperConnectConnection#annotations}
        :param bitbucket_cloud_config: bitbucket_cloud_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#bitbucket_cloud_config GoogleDeveloperConnectConnection#bitbucket_cloud_config}
        :param bitbucket_data_center_config: bitbucket_data_center_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#bitbucket_data_center_config GoogleDeveloperConnectConnection#bitbucket_data_center_config}
        :param crypto_key_config: crypto_key_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#crypto_key_config GoogleDeveloperConnectConnection#crypto_key_config}
        :param disabled: Optional. If disabled is set to true, functionality is disabled for this connection. Repository based API methods and webhooks processing for repositories in this connection will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#disabled GoogleDeveloperConnectConnection#disabled}
        :param etag: Optional. This checksum is computed by the server based on the value of other fields, and may be sent on update and delete requests to ensure the client has an up-to-date value before proceeding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#etag GoogleDeveloperConnectConnection#etag}
        :param github_config: github_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#github_config GoogleDeveloperConnectConnection#github_config}
        :param github_enterprise_config: github_enterprise_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#github_enterprise_config GoogleDeveloperConnectConnection#github_enterprise_config}
        :param gitlab_config: gitlab_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#gitlab_config GoogleDeveloperConnectConnection#gitlab_config}
        :param gitlab_enterprise_config: gitlab_enterprise_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#gitlab_enterprise_config GoogleDeveloperConnectConnection#gitlab_enterprise_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#id GoogleDeveloperConnectConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#labels GoogleDeveloperConnectConnection#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#project GoogleDeveloperConnectConnection#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#timeouts GoogleDeveloperConnectConnection#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bitbucket_cloud_config, dict):
            bitbucket_cloud_config = GoogleDeveloperConnectConnectionBitbucketCloudConfig(**bitbucket_cloud_config)
        if isinstance(bitbucket_data_center_config, dict):
            bitbucket_data_center_config = GoogleDeveloperConnectConnectionBitbucketDataCenterConfig(**bitbucket_data_center_config)
        if isinstance(crypto_key_config, dict):
            crypto_key_config = GoogleDeveloperConnectConnectionCryptoKeyConfig(**crypto_key_config)
        if isinstance(github_config, dict):
            github_config = GoogleDeveloperConnectConnectionGithubConfig(**github_config)
        if isinstance(github_enterprise_config, dict):
            github_enterprise_config = GoogleDeveloperConnectConnectionGithubEnterpriseConfig(**github_enterprise_config)
        if isinstance(gitlab_config, dict):
            gitlab_config = GoogleDeveloperConnectConnectionGitlabConfig(**gitlab_config)
        if isinstance(gitlab_enterprise_config, dict):
            gitlab_enterprise_config = GoogleDeveloperConnectConnectionGitlabEnterpriseConfig(**gitlab_enterprise_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDeveloperConnectConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ce7e8e300158d9e7c6b7d5e65ab4d826261adc86b4648af314eee91707765a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument connection_id", value=connection_id, expected_type=type_hints["connection_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument bitbucket_cloud_config", value=bitbucket_cloud_config, expected_type=type_hints["bitbucket_cloud_config"])
            check_type(argname="argument bitbucket_data_center_config", value=bitbucket_data_center_config, expected_type=type_hints["bitbucket_data_center_config"])
            check_type(argname="argument crypto_key_config", value=crypto_key_config, expected_type=type_hints["crypto_key_config"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
            check_type(argname="argument github_config", value=github_config, expected_type=type_hints["github_config"])
            check_type(argname="argument github_enterprise_config", value=github_enterprise_config, expected_type=type_hints["github_enterprise_config"])
            check_type(argname="argument gitlab_config", value=gitlab_config, expected_type=type_hints["gitlab_config"])
            check_type(argname="argument gitlab_enterprise_config", value=gitlab_enterprise_config, expected_type=type_hints["gitlab_enterprise_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_id": connection_id,
            "location": location,
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
        if crypto_key_config is not None:
            self._values["crypto_key_config"] = crypto_key_config
        if disabled is not None:
            self._values["disabled"] = disabled
        if etag is not None:
            self._values["etag"] = etag
        if github_config is not None:
            self._values["github_config"] = github_config
        if github_enterprise_config is not None:
            self._values["github_enterprise_config"] = github_enterprise_config
        if gitlab_config is not None:
            self._values["gitlab_config"] = gitlab_config
        if gitlab_enterprise_config is not None:
            self._values["gitlab_enterprise_config"] = gitlab_enterprise_config
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
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
    def connection_id(self) -> builtins.str:
        '''Required. Id of the requesting object If auto-generating Id server-side, remove this field and connection_id from the method_signature of Create RPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#connection_id GoogleDeveloperConnectConnection#connection_id}
        '''
        result = self._values.get("connection_id")
        assert result is not None, "Required property 'connection_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#location GoogleDeveloperConnectConnection#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Allows clients to store small amounts of arbitrary data.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#annotations GoogleDeveloperConnectConnection#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bitbucket_cloud_config(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfig]:
        '''bitbucket_cloud_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#bitbucket_cloud_config GoogleDeveloperConnectConnection#bitbucket_cloud_config}
        '''
        result = self._values.get("bitbucket_cloud_config")
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfig], result)

    @builtins.property
    def bitbucket_data_center_config(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfig]:
        '''bitbucket_data_center_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#bitbucket_data_center_config GoogleDeveloperConnectConnection#bitbucket_data_center_config}
        '''
        result = self._values.get("bitbucket_data_center_config")
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfig], result)

    @builtins.property
    def crypto_key_config(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionCryptoKeyConfig"]:
        '''crypto_key_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#crypto_key_config GoogleDeveloperConnectConnection#crypto_key_config}
        '''
        result = self._values.get("crypto_key_config")
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionCryptoKeyConfig"], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        If disabled is set to true, functionality is disabled for this connection.
        Repository based API methods and webhooks processing for repositories in
        this connection will be disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#disabled GoogleDeveloperConnectConnection#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def etag(self) -> typing.Optional[builtins.str]:
        '''Optional.

        This checksum is computed by the server based on the value of other
        fields, and may be sent on update and delete requests to ensure the
        client has an up-to-date value before proceeding.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#etag GoogleDeveloperConnectConnection#etag}
        '''
        result = self._values.get("etag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_config(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionGithubConfig"]:
        '''github_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#github_config GoogleDeveloperConnectConnection#github_config}
        '''
        result = self._values.get("github_config")
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionGithubConfig"], result)

    @builtins.property
    def github_enterprise_config(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionGithubEnterpriseConfig"]:
        '''github_enterprise_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#github_enterprise_config GoogleDeveloperConnectConnection#github_enterprise_config}
        '''
        result = self._values.get("github_enterprise_config")
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionGithubEnterpriseConfig"], result)

    @builtins.property
    def gitlab_config(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionGitlabConfig"]:
        '''gitlab_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#gitlab_config GoogleDeveloperConnectConnection#gitlab_config}
        '''
        result = self._values.get("gitlab_config")
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionGitlabConfig"], result)

    @builtins.property
    def gitlab_enterprise_config(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionGitlabEnterpriseConfig"]:
        '''gitlab_enterprise_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#gitlab_enterprise_config GoogleDeveloperConnectConnection#gitlab_enterprise_config}
        '''
        result = self._values.get("gitlab_enterprise_config")
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionGitlabEnterpriseConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#id GoogleDeveloperConnectConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Labels as key value pairs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#labels GoogleDeveloperConnectConnection#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#project GoogleDeveloperConnectConnection#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDeveloperConnectConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#timeouts GoogleDeveloperConnectConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionCryptoKeyConfig",
    jsii_struct_bases=[],
    name_mapping={"key_reference": "keyReference"},
)
class GoogleDeveloperConnectConnectionCryptoKeyConfig:
    def __init__(self, *, key_reference: builtins.str) -> None:
        '''
        :param key_reference: Required. The name of the key which is used to encrypt/decrypt customer data. For key in Cloud KMS, the key should be in the format of 'projects/* /locations/* /keyRings/* /cryptoKeys/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#key_reference GoogleDeveloperConnectConnection#key_reference} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b51f6359f7eb4c6585278488f5d0fa933f50f6942b7427c6a9dab3b418ce89f)
            check_type(argname="argument key_reference", value=key_reference, expected_type=type_hints["key_reference"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_reference": key_reference,
        }

    @builtins.property
    def key_reference(self) -> builtins.str:
        '''Required.

        The name of the key which is used to encrypt/decrypt customer data. For key
        in Cloud KMS, the key should be in the format of
        'projects/* /locations/* /keyRings/* /cryptoKeys/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#key_reference GoogleDeveloperConnectConnection#key_reference}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("key_reference")
        assert result is not None, "Required property 'key_reference' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectConnectionCryptoKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionCryptoKeyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionCryptoKeyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__786c6997b04dce78f5705dd662c8a01debd58c99c51dd1b60bbdb15c3f86d78c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyReferenceInput")
    def key_reference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="keyReference")
    def key_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyReference"))

    @key_reference.setter
    def key_reference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96fefdd9d151186443ddc8d4556d5258ca1396e3524f418d21b3ad328026f66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyReference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionCryptoKeyConfig]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionCryptoKeyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionCryptoKeyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f97de144b51fbe99caf256ae82424aafdd34831694a64415256f481be5d63fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGithubConfig",
    jsii_struct_bases=[],
    name_mapping={
        "github_app": "githubApp",
        "app_installation_id": "appInstallationId",
        "authorizer_credential": "authorizerCredential",
    },
)
class GoogleDeveloperConnectConnectionGithubConfig:
    def __init__(
        self,
        *,
        github_app: builtins.str,
        app_installation_id: typing.Optional[builtins.str] = None,
        authorizer_credential: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param github_app: Required. Immutable. The GitHub Application that was installed to the GitHub user or organization. Possible values: GIT_HUB_APP_UNSPECIFIED DEVELOPER_CONNECT FIREBASE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#github_app GoogleDeveloperConnectConnection#github_app}
        :param app_installation_id: Optional. GitHub App installation id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#app_installation_id GoogleDeveloperConnectConnection#app_installation_id}
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#authorizer_credential GoogleDeveloperConnectConnection#authorizer_credential}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential(**authorizer_credential)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b4189844dadbcfccb8d6f4567fafec123fad3ecdd0560faf9f4a8e654676134)
            check_type(argname="argument github_app", value=github_app, expected_type=type_hints["github_app"])
            check_type(argname="argument app_installation_id", value=app_installation_id, expected_type=type_hints["app_installation_id"])
            check_type(argname="argument authorizer_credential", value=authorizer_credential, expected_type=type_hints["authorizer_credential"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "github_app": github_app,
        }
        if app_installation_id is not None:
            self._values["app_installation_id"] = app_installation_id
        if authorizer_credential is not None:
            self._values["authorizer_credential"] = authorizer_credential

    @builtins.property
    def github_app(self) -> builtins.str:
        '''Required. Immutable. The GitHub Application that was installed to the GitHub user or organization. Possible values: GIT_HUB_APP_UNSPECIFIED DEVELOPER_CONNECT FIREBASE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#github_app GoogleDeveloperConnectConnection#github_app}
        '''
        result = self._values.get("github_app")
        assert result is not None, "Required property 'github_app' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_installation_id(self) -> typing.Optional[builtins.str]:
        '''Optional. GitHub App installation id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#app_installation_id GoogleDeveloperConnectConnection#app_installation_id}
        '''
        result = self._values.get("app_installation_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorizer_credential(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential"]:
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#authorizer_credential GoogleDeveloperConnectConnection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectConnectionGithubConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"oauth_token_secret_version": "oauthTokenSecretVersion"},
)
class GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential:
    def __init__(self, *, oauth_token_secret_version: builtins.str) -> None:
        '''
        :param oauth_token_secret_version: Required. A SecretManager resource containing the OAuth token that authorizes the connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#oauth_token_secret_version GoogleDeveloperConnectConnection#oauth_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d2927a2c258b888f54bd0b4928853c1887c19a71850c919037399f80ce9c69)
            check_type(argname="argument oauth_token_secret_version", value=oauth_token_secret_version, expected_type=type_hints["oauth_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "oauth_token_secret_version": oauth_token_secret_version,
        }

    @builtins.property
    def oauth_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the OAuth token that authorizes the connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#oauth_token_secret_version GoogleDeveloperConnectConnection#oauth_token_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("oauth_token_secret_version")
        assert result is not None, "Required property 'oauth_token_secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcdcf33beacd04f1fb7a2e1f69a5734da0be6512add5f4103417cfff9c3d5ba2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__68b07364c1996acc2e9620584802a1d3f109b5d56973edb9c69c600e929ea81e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8a2d2b4198f3a5c8bf449bcb6d4c0df0100b7ca08263901521c00d93ac1d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDeveloperConnectConnectionGithubConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGithubConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3a93325c64e1956f28f145c554d67b73d1064449d94ab164ca4369b9b5cc624)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorizerCredential")
    def put_authorizer_credential(
        self,
        *,
        oauth_token_secret_version: builtins.str,
    ) -> None:
        '''
        :param oauth_token_secret_version: Required. A SecretManager resource containing the OAuth token that authorizes the connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#oauth_token_secret_version GoogleDeveloperConnectConnection#oauth_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential(
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
    ) -> GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredentialOutputReference:
        return typing.cast(GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="installationUri")
    def installation_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "installationUri"))

    @builtins.property
    @jsii.member(jsii_name="appInstallationIdInput")
    def app_installation_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appInstallationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="githubAppInput")
    def github_app_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "githubAppInput"))

    @builtins.property
    @jsii.member(jsii_name="appInstallationId")
    def app_installation_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appInstallationId"))

    @app_installation_id.setter
    def app_installation_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68b7d995fc8c59b04bc77c6b03383404ffd9330fc804b0213b8c613cb0e7e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appInstallationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="githubApp")
    def github_app(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "githubApp"))

    @github_app.setter
    def github_app(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf539e5d390a1c3ed05696f3b761aa5b1b818601915e292106d95ad646fea83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "githubApp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionGithubConfig]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionGithubConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionGithubConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55bb699c3f1ab3795f42753553bae53efb235854d9cc30d7fc439622b7f33eec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGithubEnterpriseConfig",
    jsii_struct_bases=[],
    name_mapping={
        "host_uri": "hostUri",
        "app_id": "appId",
        "app_installation_id": "appInstallationId",
        "private_key_secret_version": "privateKeySecretVersion",
        "service_directory_config": "serviceDirectoryConfig",
        "ssl_ca_certificate": "sslCaCertificate",
        "webhook_secret_secret_version": "webhookSecretSecretVersion",
    },
)
class GoogleDeveloperConnectConnectionGithubEnterpriseConfig:
    def __init__(
        self,
        *,
        host_uri: builtins.str,
        app_id: typing.Optional[builtins.str] = None,
        app_installation_id: typing.Optional[builtins.str] = None,
        private_key_secret_version: typing.Optional[builtins.str] = None,
        service_directory_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca_certificate: typing.Optional[builtins.str] = None,
        webhook_secret_secret_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_uri: Required. The URI of the GitHub Enterprise host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#host_uri GoogleDeveloperConnectConnection#host_uri}
        :param app_id: Optional. ID of the GitHub App created from the manifest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#app_id GoogleDeveloperConnectConnection#app_id}
        :param app_installation_id: Optional. ID of the installation of the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#app_installation_id GoogleDeveloperConnectConnection#app_installation_id}
        :param private_key_secret_version: Optional. SecretManager resource containing the private key of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#private_key_secret_version GoogleDeveloperConnectConnection#private_key_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service_directory_config GoogleDeveloperConnectConnection#service_directory_config}
        :param ssl_ca_certificate: Optional. SSL certificate to use for requests to GitHub Enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#ssl_ca_certificate GoogleDeveloperConnectConnection#ssl_ca_certificate}
        :param webhook_secret_secret_version: Optional. SecretManager resource containing the webhook secret of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#webhook_secret_secret_version GoogleDeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if isinstance(service_directory_config, dict):
            service_directory_config = GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig(**service_directory_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0711ace343d00a3d9f60e00bd62f75446114857b6297feded1e8d7497e4f9a5)
            check_type(argname="argument host_uri", value=host_uri, expected_type=type_hints["host_uri"])
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument app_installation_id", value=app_installation_id, expected_type=type_hints["app_installation_id"])
            check_type(argname="argument private_key_secret_version", value=private_key_secret_version, expected_type=type_hints["private_key_secret_version"])
            check_type(argname="argument service_directory_config", value=service_directory_config, expected_type=type_hints["service_directory_config"])
            check_type(argname="argument ssl_ca_certificate", value=ssl_ca_certificate, expected_type=type_hints["ssl_ca_certificate"])
            check_type(argname="argument webhook_secret_secret_version", value=webhook_secret_secret_version, expected_type=type_hints["webhook_secret_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_uri": host_uri,
        }
        if app_id is not None:
            self._values["app_id"] = app_id
        if app_installation_id is not None:
            self._values["app_installation_id"] = app_installation_id
        if private_key_secret_version is not None:
            self._values["private_key_secret_version"] = private_key_secret_version
        if service_directory_config is not None:
            self._values["service_directory_config"] = service_directory_config
        if ssl_ca_certificate is not None:
            self._values["ssl_ca_certificate"] = ssl_ca_certificate
        if webhook_secret_secret_version is not None:
            self._values["webhook_secret_secret_version"] = webhook_secret_secret_version

    @builtins.property
    def host_uri(self) -> builtins.str:
        '''Required. The URI of the GitHub Enterprise host this connection is for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#host_uri GoogleDeveloperConnectConnection#host_uri}
        '''
        result = self._values.get("host_uri")
        assert result is not None, "Required property 'host_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_id(self) -> typing.Optional[builtins.str]:
        '''Optional. ID of the GitHub App created from the manifest.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#app_id GoogleDeveloperConnectConnection#app_id}
        '''
        result = self._values.get("app_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_installation_id(self) -> typing.Optional[builtins.str]:
        '''Optional. ID of the installation of the GitHub App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#app_installation_id GoogleDeveloperConnectConnection#app_installation_id}
        '''
        result = self._values.get("app_installation_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_secret_version(self) -> typing.Optional[builtins.str]:
        '''Optional. SecretManager resource containing the private key of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#private_key_secret_version GoogleDeveloperConnectConnection#private_key_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("private_key_secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_directory_config(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig"]:
        '''service_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service_directory_config GoogleDeveloperConnectConnection#service_directory_config}
        '''
        result = self._values.get("service_directory_config")
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig"], result)

    @builtins.property
    def ssl_ca_certificate(self) -> typing.Optional[builtins.str]:
        '''Optional. SSL certificate to use for requests to GitHub Enterprise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#ssl_ca_certificate GoogleDeveloperConnectConnection#ssl_ca_certificate}
        '''
        result = self._values.get("ssl_ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webhook_secret_secret_version(self) -> typing.Optional[builtins.str]:
        '''Optional. SecretManager resource containing the webhook secret of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#webhook_secret_secret_version GoogleDeveloperConnectConnection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectConnectionGithubEnterpriseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionGithubEnterpriseConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGithubEnterpriseConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32dde5ae4249de958262b0570b30954224a9b3dd96dfbe00ef212c7602b69a28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putServiceDirectoryConfig")
    def put_service_directory_config(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service GoogleDeveloperConnectConnection#service}
        '''
        value = GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig(
            service=service
        )

        return typing.cast(None, jsii.invoke(self, "putServiceDirectoryConfig", [value]))

    @jsii.member(jsii_name="resetAppId")
    def reset_app_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppId", []))

    @jsii.member(jsii_name="resetAppInstallationId")
    def reset_app_installation_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppInstallationId", []))

    @jsii.member(jsii_name="resetPrivateKeySecretVersion")
    def reset_private_key_secret_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKeySecretVersion", []))

    @jsii.member(jsii_name="resetServiceDirectoryConfig")
    def reset_service_directory_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceDirectoryConfig", []))

    @jsii.member(jsii_name="resetSslCaCertificate")
    def reset_ssl_ca_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCaCertificate", []))

    @jsii.member(jsii_name="resetWebhookSecretSecretVersion")
    def reset_webhook_secret_secret_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebhookSecretSecretVersion", []))

    @builtins.property
    @jsii.member(jsii_name="appSlug")
    def app_slug(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSlug"))

    @builtins.property
    @jsii.member(jsii_name="installationUri")
    def installation_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "installationUri"))

    @builtins.property
    @jsii.member(jsii_name="serverVersion")
    def server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverVersion"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfig")
    def service_directory_config(
        self,
    ) -> "GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference":
        return typing.cast("GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference", jsii.get(self, "serviceDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="appIdInput")
    def app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appInstallationIdInput")
    def app_installation_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appInstallationIdInput"))

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
    ) -> typing.Optional["GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig"]:
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig"], jsii.get(self, "serviceDirectoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCaCertificateInput")
    def ssl_ca_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCaCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersionInput")
    def webhook_secret_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookSecretSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @app_id.setter
    def app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c350328d9ff49f779f19d1dd1f027b891d6cbda3f98eaa8e7672408e952c59ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appInstallationId")
    def app_installation_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appInstallationId"))

    @app_installation_id.setter
    def app_installation_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0cb80043108b11a455f37340a8a0b5c7ffa578498cc534ff4c23421041db21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appInstallationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostUri")
    def host_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostUri"))

    @host_uri.setter
    def host_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__935c51922788928a0442d5ba2a50995b48cec88b91801578045f947c4cbad760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKeySecretVersion")
    def private_key_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKeySecretVersion"))

    @private_key_secret_version.setter
    def private_key_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41beeaa1125759f5fa6dabb0891e9e24c53f45b5ddfaf5d30def02b9334e0c23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeySecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCaCertificate")
    def ssl_ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCaCertificate"))

    @ssl_ca_certificate.setter
    def ssl_ca_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eef177e7dc017b2efe32b4de0c40bfd1ffe74dde77e0d45807fffbb4b2fd298d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCaCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretSecretVersion"))

    @webhook_secret_secret_version.setter
    def webhook_secret_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673987f25820d83284584e362ca1730873282b13e2bf694206302e33dc227f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionGithubEnterpriseConfig]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionGithubEnterpriseConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionGithubEnterpriseConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df57b367c645591b7962f0dd6bdd12afff39e3d72df88f5f7e9d36647267ab4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"service": "service"},
)
class GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig:
    def __init__(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service GoogleDeveloperConnectConnection#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96002356503a7dc14e2f2912b3952d0d213335d966e1c9a2caef83088db353e)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service GoogleDeveloperConnectConnection#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8abccc8f3ccf3b5aafe4a2e3438986521ecb0c26b0c137baa57815e77b491312)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66b8d5e0cd4ba225115bc17e2b4dcc6cc2f909f9f58e9415e25bc9173642796a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a08aef6bbb709c540315d24412d18d2a4378506be9facb60b18a577bfd19f5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGitlabConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_credential": "authorizerCredential",
        "read_authorizer_credential": "readAuthorizerCredential",
        "webhook_secret_secret_version": "webhookSecretSecretVersion",
    },
)
class GoogleDeveloperConnectConnectionGitlabConfig:
    def __init__(
        self,
        *,
        authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#authorizer_credential GoogleDeveloperConnectConnection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#read_authorizer_credential GoogleDeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret of a GitLab project, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#webhook_secret_secret_version GoogleDeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential(**authorizer_credential)
        if isinstance(read_authorizer_credential, dict):
            read_authorizer_credential = GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential(**read_authorizer_credential)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187dafba38009887a98471a92d62200c6757cfd70717a7b24fc1f62cc2b809ad)
            check_type(argname="argument authorizer_credential", value=authorizer_credential, expected_type=type_hints["authorizer_credential"])
            check_type(argname="argument read_authorizer_credential", value=read_authorizer_credential, expected_type=type_hints["read_authorizer_credential"])
            check_type(argname="argument webhook_secret_secret_version", value=webhook_secret_secret_version, expected_type=type_hints["webhook_secret_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorizer_credential": authorizer_credential,
            "read_authorizer_credential": read_authorizer_credential,
            "webhook_secret_secret_version": webhook_secret_secret_version,
        }

    @builtins.property
    def authorizer_credential(
        self,
    ) -> "GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential":
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#authorizer_credential GoogleDeveloperConnectConnection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        assert result is not None, "Required property 'authorizer_credential' is missing"
        return typing.cast("GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential", result)

    @builtins.property
    def read_authorizer_credential(
        self,
    ) -> "GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential":
        '''read_authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#read_authorizer_credential GoogleDeveloperConnectConnection#read_authorizer_credential}
        '''
        result = self._values.get("read_authorizer_credential")
        assert result is not None, "Required property 'read_authorizer_credential' is missing"
        return typing.cast("GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential", result)

    @builtins.property
    def webhook_secret_secret_version(self) -> builtins.str:
        '''Required.

        Immutable. SecretManager resource containing the webhook secret of a GitLab project,
        formatted as 'projects/* /secrets/* /versions/*'. This is used to validate
        webhooks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#webhook_secret_secret_version GoogleDeveloperConnectConnection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        assert result is not None, "Required property 'webhook_secret_secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectConnectionGitlabConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de97011ec28bfd814426bc9afa0a8640f6a053a3b9e6fe63263613b20474d66b)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version}

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
        return "GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__426d11c409e7e1791c3fa94a28c85c8f93f3c4d9a6b5785cddc5a08c91d69744)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fb48418fce9a59b7f500edff01dd946b67ee5b9e070fa8ed2f46a4d3efb8289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af33b7e66c30770b4a7dcd9cec9b372b5f30512a351d71038e496209a2831e15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDeveloperConnectConnectionGitlabConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGitlabConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ead5c56276c13dfea38e2f50d5592dc015b7bc20c21edd13e6c816035d58cbdf)
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential(
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putReadAuthorizerCredential", [value]))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredential")
    def authorizer_credential(
        self,
    ) -> GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredentialOutputReference:
        return typing.cast(GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredential")
    def read_authorizer_credential(
        self,
    ) -> "GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredentialOutputReference":
        return typing.cast("GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredentialOutputReference", jsii.get(self, "readAuthorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredentialInput")
    def read_authorizer_credential_input(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential"]:
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential"], jsii.get(self, "readAuthorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersionInput")
    def webhook_secret_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookSecretSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretSecretVersion"))

    @webhook_secret_secret_version.setter
    def webhook_secret_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b577d9d50da59bd7cde9bf2f28be70a4c65db1ca3270573bb63c30538662adb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionGitlabConfig]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionGitlabConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionGitlabConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9434442b65ca87662ddb2559f6223cedd91b9aba539b972b5a3c36204026c780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89277e6aac60a177a2c265e5403ec2b7e0aaf38954a1e3e81c2b1784cf7dc6e2)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version}

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
        return "GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bd6d5efde02bf243c5bbc5973b023595b2876018818c2fc9ae9dcceb9a1ed6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__beae2c8acf6dbb7986dc9c7ad3e1fae0710b8649675520d3773bfcd6a19521c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13f61df495df30093bdd40c47861496af74e99e044d56067ac34789a44fabf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGitlabEnterpriseConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_credential": "authorizerCredential",
        "host_uri": "hostUri",
        "read_authorizer_credential": "readAuthorizerCredential",
        "webhook_secret_secret_version": "webhookSecretSecretVersion",
        "service_directory_config": "serviceDirectoryConfig",
        "ssl_ca_certificate": "sslCaCertificate",
    },
)
class GoogleDeveloperConnectConnectionGitlabEnterpriseConfig:
    def __init__(
        self,
        *,
        authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        host_uri: builtins.str,
        read_authorizer_credential: typing.Union["GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        service_directory_config: typing.Optional[typing.Union["GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca_certificate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#authorizer_credential GoogleDeveloperConnectConnection#authorizer_credential}
        :param host_uri: Required. The URI of the GitLab Enterprise host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#host_uri GoogleDeveloperConnectConnection#host_uri}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#read_authorizer_credential GoogleDeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret of a GitLab project, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#webhook_secret_secret_version GoogleDeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service_directory_config GoogleDeveloperConnectConnection#service_directory_config}
        :param ssl_ca_certificate: Optional. SSL Certificate Authority certificate to use for requests to GitLab Enterprise instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#ssl_ca_certificate GoogleDeveloperConnectConnection#ssl_ca_certificate}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential(**authorizer_credential)
        if isinstance(read_authorizer_credential, dict):
            read_authorizer_credential = GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential(**read_authorizer_credential)
        if isinstance(service_directory_config, dict):
            service_directory_config = GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig(**service_directory_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4e73eac78bb74fff8e6ed4801d874636f8c7cec312f0e04182815ccd8bef90)
            check_type(argname="argument authorizer_credential", value=authorizer_credential, expected_type=type_hints["authorizer_credential"])
            check_type(argname="argument host_uri", value=host_uri, expected_type=type_hints["host_uri"])
            check_type(argname="argument read_authorizer_credential", value=read_authorizer_credential, expected_type=type_hints["read_authorizer_credential"])
            check_type(argname="argument webhook_secret_secret_version", value=webhook_secret_secret_version, expected_type=type_hints["webhook_secret_secret_version"])
            check_type(argname="argument service_directory_config", value=service_directory_config, expected_type=type_hints["service_directory_config"])
            check_type(argname="argument ssl_ca_certificate", value=ssl_ca_certificate, expected_type=type_hints["ssl_ca_certificate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorizer_credential": authorizer_credential,
            "host_uri": host_uri,
            "read_authorizer_credential": read_authorizer_credential,
            "webhook_secret_secret_version": webhook_secret_secret_version,
        }
        if service_directory_config is not None:
            self._values["service_directory_config"] = service_directory_config
        if ssl_ca_certificate is not None:
            self._values["ssl_ca_certificate"] = ssl_ca_certificate

    @builtins.property
    def authorizer_credential(
        self,
    ) -> "GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential":
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#authorizer_credential GoogleDeveloperConnectConnection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        assert result is not None, "Required property 'authorizer_credential' is missing"
        return typing.cast("GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential", result)

    @builtins.property
    def host_uri(self) -> builtins.str:
        '''Required. The URI of the GitLab Enterprise host this connection is for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#host_uri GoogleDeveloperConnectConnection#host_uri}
        '''
        result = self._values.get("host_uri")
        assert result is not None, "Required property 'host_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_authorizer_credential(
        self,
    ) -> "GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential":
        '''read_authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#read_authorizer_credential GoogleDeveloperConnectConnection#read_authorizer_credential}
        '''
        result = self._values.get("read_authorizer_credential")
        assert result is not None, "Required property 'read_authorizer_credential' is missing"
        return typing.cast("GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential", result)

    @builtins.property
    def webhook_secret_secret_version(self) -> builtins.str:
        '''Required.

        Immutable. SecretManager resource containing the webhook secret of a GitLab project,
        formatted as 'projects/* /secrets/* /versions/*'. This is used to validate
        webhooks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#webhook_secret_secret_version GoogleDeveloperConnectConnection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        assert result is not None, "Required property 'webhook_secret_secret_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_directory_config(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig"]:
        '''service_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service_directory_config GoogleDeveloperConnectConnection#service_directory_config}
        '''
        result = self._values.get("service_directory_config")
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig"], result)

    @builtins.property
    def ssl_ca_certificate(self) -> typing.Optional[builtins.str]:
        '''Optional. SSL Certificate Authority certificate to use for requests to GitLab Enterprise instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#ssl_ca_certificate GoogleDeveloperConnectConnection#ssl_ca_certificate}
        '''
        result = self._values.get("ssl_ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectConnectionGitlabEnterpriseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fd10d042f1f3cd61de758b90d717c5362248367e9126de88a758c1b7dbf8f5c)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version}

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
        return "GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__361165bf70bdb5255656adfabca1002224b65f6d55d0dd457088d700c5c4c285)
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
            type_hints = typing.get_type_hints(_typecheckingstub__947295e4edcad27aa975485a94e77e40ca77a8b17c77c7763963cbd1f5890cf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6a1b6779eb808a704bcbc00551ee483acbfd3d7c50b14ddea4a03251897b4f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDeveloperConnectConnectionGitlabEnterpriseConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGitlabEnterpriseConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6d8b5f47fb8e09823e6b5ca259c2bdb04551aa9f651be9ddec7f21df0d1e02c)
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential(
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putReadAuthorizerCredential", [value]))

    @jsii.member(jsii_name="putServiceDirectoryConfig")
    def put_service_directory_config(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service GoogleDeveloperConnectConnection#service}
        '''
        value = GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig(
            service=service
        )

        return typing.cast(None, jsii.invoke(self, "putServiceDirectoryConfig", [value]))

    @jsii.member(jsii_name="resetServiceDirectoryConfig")
    def reset_service_directory_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceDirectoryConfig", []))

    @jsii.member(jsii_name="resetSslCaCertificate")
    def reset_ssl_ca_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCaCertificate", []))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredential")
    def authorizer_credential(
        self,
    ) -> GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredentialOutputReference:
        return typing.cast(GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredential")
    def read_authorizer_credential(
        self,
    ) -> "GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredentialOutputReference":
        return typing.cast("GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredentialOutputReference", jsii.get(self, "readAuthorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="serverVersion")
    def server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverVersion"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfig")
    def service_directory_config(
        self,
    ) -> "GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfigOutputReference":
        return typing.cast("GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfigOutputReference", jsii.get(self, "serviceDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="hostUriInput")
    def host_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostUriInput"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredentialInput")
    def read_authorizer_credential_input(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential"]:
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential"], jsii.get(self, "readAuthorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfigInput")
    def service_directory_config_input(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig"]:
        return typing.cast(typing.Optional["GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig"], jsii.get(self, "serviceDirectoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCaCertificateInput")
    def ssl_ca_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCaCertificateInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ef97a31c66b3a19c878f7d2caab6b6a68812dc10f6940b45d4c61acac0a3f9fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCaCertificate")
    def ssl_ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCaCertificate"))

    @ssl_ca_certificate.setter
    def ssl_ca_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081f1930ccc76141f981e0c7b0a4eb3de0bfbf68dac482d0baef102751dcc952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCaCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretSecretVersion"))

    @webhook_secret_secret_version.setter
    def webhook_secret_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2daa7002d43aea8c1d7a2e8ab48c587759ab9a41ae7ee22eb3f802e42ce7a666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfig]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da3b47d84c0e92d9c1e841456df46523c2f7fe46a10e39cce5e0ed2dad32f036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__368c89c9bd1ce169d8de2ebffa268e4ed42cb79957bb276d55c4980b40a928cb)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#user_token_secret_version GoogleDeveloperConnectConnection#user_token_secret_version}

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
        return "GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e06e1d33acc4ebcd6d742a70332a964ebe398d046309972f182e6768e58d69ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a861de1617668d012d21b047e8872b5cfe3b6b3f1a46285ff401f28f67d3bdc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf2e8e292e89c8a2b6768bb140633f00c721159c91ae1d9ba1fd51f89712331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"service": "service"},
)
class GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig:
    def __init__(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service GoogleDeveloperConnectConnection#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c91e09d97367ee9fd67cd5e1a22766519e887c1b71c27b7ef45943b9cee82b)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#service GoogleDeveloperConnectConnection#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7161192a06e1f97b9d2d49ce8bbc177a1efb92efcd959e0bf597c1ff4a2915b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63d6a50de478d347d95df5c8b8be7710bb252323829a45e61f9c96ffcbcb3505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fc80630fc756233bfc33c8b40b13cb2adc77552167839f133cc179cf1d16534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionInstallationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDeveloperConnectConnectionInstallationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectConnectionInstallationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionInstallationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionInstallationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80cd5f55f79c62cccdfa1cef3418dd1bd6bf87550c05ac98c2e09991bee9697c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDeveloperConnectConnectionInstallationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53076cfeb6b81faecaa314a060f725e98727296de71101800cdd0c9f947a23d7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDeveloperConnectConnectionInstallationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c370ef11b18d73b1938eafa458cef5c102f9f59b9bc1082fd8ec3fd23e1b7a3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__935924e8a7fa14fb83d02d4c82566f3f047ee49eb14d3886573a9b5abf2feb81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84911336ae4e9dff72518b493624145ca8e1296173a2db2737f6ce3dc46b3a5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDeveloperConnectConnectionInstallationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionInstallationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff76c75e7c25e828e8140071baa5e7481fcc33491728eded3d8dedea593c1215)
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
    ) -> typing.Optional[GoogleDeveloperConnectConnectionInstallationState]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectConnectionInstallationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectConnectionInstallationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e9a1f0cf7b858eb83fb706fa285d323caca6551a020aae305ed4c69107d87fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDeveloperConnectConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#create GoogleDeveloperConnectConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#delete GoogleDeveloperConnectConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#update GoogleDeveloperConnectConnection#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d913dab2045d439fadfd7c86d7a889b1dc39672efff644f6e152c422ee1ab32)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#create GoogleDeveloperConnectConnection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#delete GoogleDeveloperConnectConnection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_developer_connect_connection#update GoogleDeveloperConnectConnection#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectConnection.GoogleDeveloperConnectConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a06e0e3cc6b294cde513053e4c8340dedf57a78866d1ad9a930d22e7e24b9201)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b38d59778c3ad67d27c0f40488cd9e9e02e65ae5d4895e0aa560ce907ed3cd04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5b6d269daf98e9cb1240461a20c8002dde7e75576f6d71717c5c886f45ab17f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72479954d3fcc180413b6a891dbf2004abf52c889c2af08524cdffde90c787c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDeveloperConnectConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDeveloperConnectConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDeveloperConnectConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be936ca4febbcfeb71f9ebe4be0dff0b449707d3e07e31c762d7b8e6f23bfbed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDeveloperConnectConnection",
    "GoogleDeveloperConnectConnectionBitbucketCloudConfig",
    "GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential",
    "GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference",
    "GoogleDeveloperConnectConnectionBitbucketCloudConfigOutputReference",
    "GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential",
    "GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference",
    "GoogleDeveloperConnectConnectionBitbucketDataCenterConfig",
    "GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential",
    "GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference",
    "GoogleDeveloperConnectConnectionBitbucketDataCenterConfigOutputReference",
    "GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential",
    "GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference",
    "GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig",
    "GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference",
    "GoogleDeveloperConnectConnectionConfig",
    "GoogleDeveloperConnectConnectionCryptoKeyConfig",
    "GoogleDeveloperConnectConnectionCryptoKeyConfigOutputReference",
    "GoogleDeveloperConnectConnectionGithubConfig",
    "GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential",
    "GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredentialOutputReference",
    "GoogleDeveloperConnectConnectionGithubConfigOutputReference",
    "GoogleDeveloperConnectConnectionGithubEnterpriseConfig",
    "GoogleDeveloperConnectConnectionGithubEnterpriseConfigOutputReference",
    "GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig",
    "GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference",
    "GoogleDeveloperConnectConnectionGitlabConfig",
    "GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential",
    "GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredentialOutputReference",
    "GoogleDeveloperConnectConnectionGitlabConfigOutputReference",
    "GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential",
    "GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredentialOutputReference",
    "GoogleDeveloperConnectConnectionGitlabEnterpriseConfig",
    "GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential",
    "GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredentialOutputReference",
    "GoogleDeveloperConnectConnectionGitlabEnterpriseConfigOutputReference",
    "GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential",
    "GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredentialOutputReference",
    "GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig",
    "GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfigOutputReference",
    "GoogleDeveloperConnectConnectionInstallationState",
    "GoogleDeveloperConnectConnectionInstallationStateList",
    "GoogleDeveloperConnectConnectionInstallationStateOutputReference",
    "GoogleDeveloperConnectConnectionTimeouts",
    "GoogleDeveloperConnectConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d019c75242c0ef7adbf3e363b4c2ccc0d579eefa451f9b61effc57d67801f956(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    connection_id: builtins.str,
    location: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bitbucket_cloud_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionBitbucketCloudConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bitbucket_data_center_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionBitbucketDataCenterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    crypto_key_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionCryptoKeyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    etag: typing.Optional[builtins.str] = None,
    github_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionGithubConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    github_enterprise_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionGithubEnterpriseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gitlab_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionGitlabConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gitlab_enterprise_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionGitlabEnterpriseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__175f5cef411a2276d3371bd7225e1d3a20d48a0b8b38df544325338f1e54dd42(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35049cef196ec2e0479b080fe180ac82ab01ce8dec6b6489fca6147f02311cf2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87413ffcb34301a2a0f51b79f5fbaf988e6609740105fe6b6b58122d8a197489(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca15962991343397d2111e5c5ec22471ca5a53116cdc3c4112176517f7e7d1a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbdce802dcf2989f8cb91e0520027d27e9c8c626c9c6304f6306b05dbeaeee3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c48fc18c4fecb6657bd76d647029ad4c36ff5104f6642df72c3265a66f58ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be7148525c7ab6813a3e0a20d76beeec9168abdd567345cdfc4af354ac57740(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0397857237152162f5e49387eddfec93ef90c19139af70bf56a653bf31d1f74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37b7c27e9ff53f7ee2fcfe298e857e916570b35871e9b321c22075b24e65450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c549b09009e83f7cacfe30df6be081b52b0af35ecae3724ab307afd940d1ad(
    *,
    authorizer_credential: typing.Union[GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    read_authorizer_credential: typing.Union[GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    webhook_secret_secret_version: builtins.str,
    workspace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4111cb853b65cd7cdf84d91dcebe6f4ecdb9009c5bacf88218d9dd51ba4a3c67(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3605158ffebdbfd267556edc5ebe24855364fcf0b8fd88f27b902f4ccb509e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cfacfec39994a310368f9e9e114eb827e179c128af481add3f5a3109445cdc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ddd59a425e73d93a8672762ac88656959e9bbc12cd321ae1f15c89cbab23fc(
    value: typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c15c8ac077c9cf02f0dcac95ea8a9c4392d5df6b663a4f58e82490f8641939(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2048aa99ba68876d0afe2b38dc2c6812dcc0a610891b95292a213487621685fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a80c8f006177d6c0de1d509a0b4678cb9299e06533626f7dbc7c6a841e4462b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e0457f800ba329580ca0af8c450a89a9cd15091940b78ad1db294222725411(
    value: typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d84557df7fca3d700bc51acd0078ccbffcefee3037d163c638709bb5579e2f(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ae572bc295cdb0590a44c81d5c30ce0d583f01d39f9f80f85f5201c255356d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4707295e69492af504194b6977d5a0b227dd9f9c326cedabaf444b3cb669508b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ecf4c659fcbb6c181c21e5d5c212fad958a8159ab740f27f67d933c6d836800(
    value: typing.Optional[GoogleDeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455e422c6ca1f6939e3f9f9c9f535f6ae38a5371fd23de0c4954f97f0b893ab3(
    *,
    authorizer_credential: typing.Union[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    host_uri: builtins.str,
    read_authorizer_credential: typing.Union[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    webhook_secret_secret_version: builtins.str,
    service_directory_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_ca_certificate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45de49c73c0e0f12c3c8faacf8f4358aec37f9bcfa8c77581c7fe026c7cd5f38(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d05c539797204f7faa5fa190d05e0fa6f75f1aadc87584fa687f7e9514b9111(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ac794f8c3212f434e4eb67310f82889a7b04732b9c695c0059d9e7d79a369a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5df574359c8907faeab074c5eb1b04bc9d881f974ed84b4d06f4fa0653f14b(
    value: typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d245107a2ddc0c0d4455b7cb1a4d63db4cfab0891d422b2ab98daaed40e6969f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d521a9a2d108787e02410dec44d853b56ec92a20bc67dff8d9bc67b6d8aafaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99293d6e2321e4cb56ce407d9397017f630edc75333b2bc9bfa38381915620bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8ad6bb265faf0703e1517462210e96765ddc7483e1f2dfcb301a9324de24237(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93894d37e8d3565ca41bfc7bc9539af45bdb0e6f7253d76e8a02c440e8833ed7(
    value: typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9718c663adcf73a265a9ebd4c5f8d45c82c8064128beecd8833b515d1e07dba(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb29c126d54344490ad472268d88c30718992b91d059dd4794a1323dac85939(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6560eb599d5c6b045d5053587526b0239422155b8da575863c9de4ad302a17f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b23e0b0393b233728c95d738b601278e828a71333ee00a3c820c8628d6d4c1(
    value: typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a21a099830f6d211e1e11ac86a64670102df7bca24bf6fb66178d7d6e9c977b(
    *,
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa19fcba78ccb66211188342f8a985ab1993aa07a7ac297a002069c23ac2c18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9c3eedd024cb8b37930133f826cf7985a4c7e7bdc421c87de9576f216a7b99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3049d907a46ddc4507f0664dbedc271046fd27aa0346cd5de0f93ab0780ac983(
    value: typing.Optional[GoogleDeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ce7e8e300158d9e7c6b7d5e65ab4d826261adc86b4648af314eee91707765a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection_id: builtins.str,
    location: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bitbucket_cloud_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionBitbucketCloudConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bitbucket_data_center_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionBitbucketDataCenterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    crypto_key_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionCryptoKeyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    etag: typing.Optional[builtins.str] = None,
    github_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionGithubConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    github_enterprise_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionGithubEnterpriseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gitlab_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionGitlabConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gitlab_enterprise_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionGitlabEnterpriseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b51f6359f7eb4c6585278488f5d0fa933f50f6942b7427c6a9dab3b418ce89f(
    *,
    key_reference: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786c6997b04dce78f5705dd662c8a01debd58c99c51dd1b60bbdb15c3f86d78c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96fefdd9d151186443ddc8d4556d5258ca1396e3524f418d21b3ad328026f66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f97de144b51fbe99caf256ae82424aafdd34831694a64415256f481be5d63fa(
    value: typing.Optional[GoogleDeveloperConnectConnectionCryptoKeyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4189844dadbcfccb8d6f4567fafec123fad3ecdd0560faf9f4a8e654676134(
    *,
    github_app: builtins.str,
    app_installation_id: typing.Optional[builtins.str] = None,
    authorizer_credential: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d2927a2c258b888f54bd0b4928853c1887c19a71850c919037399f80ce9c69(
    *,
    oauth_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcdcf33beacd04f1fb7a2e1f69a5734da0be6512add5f4103417cfff9c3d5ba2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b07364c1996acc2e9620584802a1d3f109b5d56973edb9c69c600e929ea81e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8a2d2b4198f3a5c8bf449bcb6d4c0df0100b7ca08263901521c00d93ac1d41(
    value: typing.Optional[GoogleDeveloperConnectConnectionGithubConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a93325c64e1956f28f145c554d67b73d1064449d94ab164ca4369b9b5cc624(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68b7d995fc8c59b04bc77c6b03383404ffd9330fc804b0213b8c613cb0e7e13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf539e5d390a1c3ed05696f3b761aa5b1b818601915e292106d95ad646fea83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55bb699c3f1ab3795f42753553bae53efb235854d9cc30d7fc439622b7f33eec(
    value: typing.Optional[GoogleDeveloperConnectConnectionGithubConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0711ace343d00a3d9f60e00bd62f75446114857b6297feded1e8d7497e4f9a5(
    *,
    host_uri: builtins.str,
    app_id: typing.Optional[builtins.str] = None,
    app_installation_id: typing.Optional[builtins.str] = None,
    private_key_secret_version: typing.Optional[builtins.str] = None,
    service_directory_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_ca_certificate: typing.Optional[builtins.str] = None,
    webhook_secret_secret_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32dde5ae4249de958262b0570b30954224a9b3dd96dfbe00ef212c7602b69a28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c350328d9ff49f779f19d1dd1f027b891d6cbda3f98eaa8e7672408e952c59ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0cb80043108b11a455f37340a8a0b5c7ffa578498cc534ff4c23421041db21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__935c51922788928a0442d5ba2a50995b48cec88b91801578045f947c4cbad760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41beeaa1125759f5fa6dabb0891e9e24c53f45b5ddfaf5d30def02b9334e0c23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef177e7dc017b2efe32b4de0c40bfd1ffe74dde77e0d45807fffbb4b2fd298d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673987f25820d83284584e362ca1730873282b13e2bf694206302e33dc227f96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df57b367c645591b7962f0dd6bdd12afff39e3d72df88f5f7e9d36647267ab4f(
    value: typing.Optional[GoogleDeveloperConnectConnectionGithubEnterpriseConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96002356503a7dc14e2f2912b3952d0d213335d966e1c9a2caef83088db353e(
    *,
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8abccc8f3ccf3b5aafe4a2e3438986521ecb0c26b0c137baa57815e77b491312(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b8d5e0cd4ba225115bc17e2b4dcc6cc2f909f9f58e9415e25bc9173642796a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a08aef6bbb709c540315d24412d18d2a4378506be9facb60b18a577bfd19f5e(
    value: typing.Optional[GoogleDeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187dafba38009887a98471a92d62200c6757cfd70717a7b24fc1f62cc2b809ad(
    *,
    authorizer_credential: typing.Union[GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    read_authorizer_credential: typing.Union[GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    webhook_secret_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de97011ec28bfd814426bc9afa0a8640f6a053a3b9e6fe63263613b20474d66b(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426d11c409e7e1791c3fa94a28c85c8f93f3c4d9a6b5785cddc5a08c91d69744(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb48418fce9a59b7f500edff01dd946b67ee5b9e070fa8ed2f46a4d3efb8289(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af33b7e66c30770b4a7dcd9cec9b372b5f30512a351d71038e496209a2831e15(
    value: typing.Optional[GoogleDeveloperConnectConnectionGitlabConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead5c56276c13dfea38e2f50d5592dc015b7bc20c21edd13e6c816035d58cbdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b577d9d50da59bd7cde9bf2f28be70a4c65db1ca3270573bb63c30538662adb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9434442b65ca87662ddb2559f6223cedd91b9aba539b972b5a3c36204026c780(
    value: typing.Optional[GoogleDeveloperConnectConnectionGitlabConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89277e6aac60a177a2c265e5403ec2b7e0aaf38954a1e3e81c2b1784cf7dc6e2(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd6d5efde02bf243c5bbc5973b023595b2876018818c2fc9ae9dcceb9a1ed6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beae2c8acf6dbb7986dc9c7ad3e1fae0710b8649675520d3773bfcd6a19521c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13f61df495df30093bdd40c47861496af74e99e044d56067ac34789a44fabf6(
    value: typing.Optional[GoogleDeveloperConnectConnectionGitlabConfigReadAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4e73eac78bb74fff8e6ed4801d874636f8c7cec312f0e04182815ccd8bef90(
    *,
    authorizer_credential: typing.Union[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    host_uri: builtins.str,
    read_authorizer_credential: typing.Union[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    webhook_secret_secret_version: builtins.str,
    service_directory_config: typing.Optional[typing.Union[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_ca_certificate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd10d042f1f3cd61de758b90d717c5362248367e9126de88a758c1b7dbf8f5c(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361165bf70bdb5255656adfabca1002224b65f6d55d0dd457088d700c5c4c285(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947295e4edcad27aa975485a94e77e40ca77a8b17c77c7763963cbd1f5890cf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a1b6779eb808a704bcbc00551ee483acbfd3d7c50b14ddea4a03251897b4f4(
    value: typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6d8b5f47fb8e09823e6b5ca259c2bdb04551aa9f651be9ddec7f21df0d1e02c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef97a31c66b3a19c878f7d2caab6b6a68812dc10f6940b45d4c61acac0a3f9fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081f1930ccc76141f981e0c7b0a4eb3de0bfbf68dac482d0baef102751dcc952(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2daa7002d43aea8c1d7a2e8ab48c587759ab9a41ae7ee22eb3f802e42ce7a666(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3b47d84c0e92d9c1e841456df46523c2f7fe46a10e39cce5e0ed2dad32f036(
    value: typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__368c89c9bd1ce169d8de2ebffa268e4ed42cb79957bb276d55c4980b40a928cb(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06e1d33acc4ebcd6d742a70332a964ebe398d046309972f182e6768e58d69ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a861de1617668d012d21b047e8872b5cfe3b6b3f1a46285ff401f28f67d3bdc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf2e8e292e89c8a2b6768bb140633f00c721159c91ae1d9ba1fd51f89712331(
    value: typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c91e09d97367ee9fd67cd5e1a22766519e887c1b71c27b7ef45943b9cee82b(
    *,
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7161192a06e1f97b9d2d49ce8bbc177a1efb92efcd959e0bf597c1ff4a2915b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d6a50de478d347d95df5c8b8be7710bb252323829a45e61f9c96ffcbcb3505(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc80630fc756233bfc33c8b40b13cb2adc77552167839f133cc179cf1d16534(
    value: typing.Optional[GoogleDeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80cd5f55f79c62cccdfa1cef3418dd1bd6bf87550c05ac98c2e09991bee9697c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53076cfeb6b81faecaa314a060f725e98727296de71101800cdd0c9f947a23d7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c370ef11b18d73b1938eafa458cef5c102f9f59b9bc1082fd8ec3fd23e1b7a3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__935924e8a7fa14fb83d02d4c82566f3f047ee49eb14d3886573a9b5abf2feb81(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84911336ae4e9dff72518b493624145ca8e1296173a2db2737f6ce3dc46b3a5e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff76c75e7c25e828e8140071baa5e7481fcc33491728eded3d8dedea593c1215(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9a1f0cf7b858eb83fb706fa285d323caca6551a020aae305ed4c69107d87fd(
    value: typing.Optional[GoogleDeveloperConnectConnectionInstallationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d913dab2045d439fadfd7c86d7a889b1dc39672efff644f6e152c422ee1ab32(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06e0e3cc6b294cde513053e4c8340dedf57a78866d1ad9a930d22e7e24b9201(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38d59778c3ad67d27c0f40488cd9e9e02e65ae5d4895e0aa560ce907ed3cd04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b6d269daf98e9cb1240461a20c8002dde7e75576f6d71717c5c886f45ab17f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72479954d3fcc180413b6a891dbf2004abf52c889c2af08524cdffde90c787c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be936ca4febbcfeb71f9ebe4be0dff0b449707d3e07e31c762d7b8e6f23bfbed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDeveloperConnectConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

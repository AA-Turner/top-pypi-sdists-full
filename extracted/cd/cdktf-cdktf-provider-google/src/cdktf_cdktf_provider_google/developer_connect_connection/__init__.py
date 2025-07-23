r'''
# `google_developer_connect_connection`

Refer to the Terraform Registry for docs: [`google_developer_connect_connection`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection).
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


class DeveloperConnectConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection google_developer_connect_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        connection_id: builtins.str,
        location: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bitbucket_cloud_config: typing.Optional[typing.Union["DeveloperConnectConnectionBitbucketCloudConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        bitbucket_data_center_config: typing.Optional[typing.Union["DeveloperConnectConnectionBitbucketDataCenterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        crypto_key_config: typing.Optional[typing.Union["DeveloperConnectConnectionCryptoKeyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        etag: typing.Optional[builtins.str] = None,
        github_config: typing.Optional[typing.Union["DeveloperConnectConnectionGithubConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        github_enterprise_config: typing.Optional[typing.Union["DeveloperConnectConnectionGithubEnterpriseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gitlab_config: typing.Optional[typing.Union["DeveloperConnectConnectionGitlabConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gitlab_enterprise_config: typing.Optional[typing.Union["DeveloperConnectConnectionGitlabEnterpriseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DeveloperConnectConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection google_developer_connect_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param connection_id: Required. Id of the requesting object If auto-generating Id server-side, remove this field and connection_id from the method_signature of Create RPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#connection_id DeveloperConnectConnection#connection_id}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#location DeveloperConnectConnection#location}
        :param annotations: Optional. Allows clients to store small amounts of arbitrary data. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#annotations DeveloperConnectConnection#annotations}
        :param bitbucket_cloud_config: bitbucket_cloud_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#bitbucket_cloud_config DeveloperConnectConnection#bitbucket_cloud_config}
        :param bitbucket_data_center_config: bitbucket_data_center_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#bitbucket_data_center_config DeveloperConnectConnection#bitbucket_data_center_config}
        :param crypto_key_config: crypto_key_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#crypto_key_config DeveloperConnectConnection#crypto_key_config}
        :param disabled: Optional. If disabled is set to true, functionality is disabled for this connection. Repository based API methods and webhooks processing for repositories in this connection will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#disabled DeveloperConnectConnection#disabled}
        :param etag: Optional. This checksum is computed by the server based on the value of other fields, and may be sent on update and delete requests to ensure the client has an up-to-date value before proceeding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#etag DeveloperConnectConnection#etag}
        :param github_config: github_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#github_config DeveloperConnectConnection#github_config}
        :param github_enterprise_config: github_enterprise_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#github_enterprise_config DeveloperConnectConnection#github_enterprise_config}
        :param gitlab_config: gitlab_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#gitlab_config DeveloperConnectConnection#gitlab_config}
        :param gitlab_enterprise_config: gitlab_enterprise_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#gitlab_enterprise_config DeveloperConnectConnection#gitlab_enterprise_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#id DeveloperConnectConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#labels DeveloperConnectConnection#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#project DeveloperConnectConnection#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#timeouts DeveloperConnectConnection#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5f7c849e226382d29b1b843e7d2cd11820eda3e477fa8c7620f830fbdcecce)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DeveloperConnectConnectionConfig(
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
        '''Generates CDKTF code for importing a DeveloperConnectConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DeveloperConnectConnection to import.
        :param import_from_id: The id of the existing DeveloperConnectConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DeveloperConnectConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9092c814bc0a10a9ef3377908122c58f279135323e39c22f8a0ae2a2ac9090f1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBitbucketCloudConfig")
    def put_bitbucket_cloud_config(
        self,
        *,
        authorizer_credential: typing.Union["DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        workspace: builtins.str,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#authorizer_credential DeveloperConnectConnection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#read_authorizer_credential DeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate and create webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#webhook_secret_secret_version DeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param workspace: Required. The Bitbucket Cloud Workspace ID to be connected to Google Cloud Platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#workspace DeveloperConnectConnection#workspace}
        '''
        value = DeveloperConnectConnectionBitbucketCloudConfig(
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
        authorizer_credential: typing.Union["DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        host_uri: builtins.str,
        read_authorizer_credential: typing.Union["DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        service_directory_config: typing.Optional[typing.Union["DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca_certificate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#authorizer_credential DeveloperConnectConnection#authorizer_credential}
        :param host_uri: Required. The URI of the Bitbucket Data Center host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#host_uri DeveloperConnectConnection#host_uri}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#read_authorizer_credential DeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#webhook_secret_secret_version DeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service_directory_config DeveloperConnectConnection#service_directory_config}
        :param ssl_ca_certificate: Optional. SSL certificate authority to trust when making requests to Bitbucket Data Center. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#ssl_ca_certificate DeveloperConnectConnection#ssl_ca_certificate}
        '''
        value = DeveloperConnectConnectionBitbucketDataCenterConfig(
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
        :param key_reference: Required. The name of the key which is used to encrypt/decrypt customer data. For key in Cloud KMS, the key should be in the format of 'projects/* /locations/* /keyRings/* /cryptoKeys/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#key_reference DeveloperConnectConnection#key_reference} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = DeveloperConnectConnectionCryptoKeyConfig(key_reference=key_reference)

        return typing.cast(None, jsii.invoke(self, "putCryptoKeyConfig", [value]))

    @jsii.member(jsii_name="putGithubConfig")
    def put_github_config(
        self,
        *,
        github_app: builtins.str,
        app_installation_id: typing.Optional[builtins.str] = None,
        authorizer_credential: typing.Optional[typing.Union["DeveloperConnectConnectionGithubConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param github_app: Required. Immutable. The GitHub Application that was installed to the GitHub user or organization. Possible values: GIT_HUB_APP_UNSPECIFIED DEVELOPER_CONNECT FIREBASE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#github_app DeveloperConnectConnection#github_app}
        :param app_installation_id: Optional. GitHub App installation id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#app_installation_id DeveloperConnectConnection#app_installation_id}
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#authorizer_credential DeveloperConnectConnection#authorizer_credential}
        '''
        value = DeveloperConnectConnectionGithubConfig(
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
        service_directory_config: typing.Optional[typing.Union["DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca_certificate: typing.Optional[builtins.str] = None,
        webhook_secret_secret_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_uri: Required. The URI of the GitHub Enterprise host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#host_uri DeveloperConnectConnection#host_uri}
        :param app_id: Optional. ID of the GitHub App created from the manifest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#app_id DeveloperConnectConnection#app_id}
        :param app_installation_id: Optional. ID of the installation of the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#app_installation_id DeveloperConnectConnection#app_installation_id}
        :param private_key_secret_version: Optional. SecretManager resource containing the private key of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#private_key_secret_version DeveloperConnectConnection#private_key_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service_directory_config DeveloperConnectConnection#service_directory_config}
        :param ssl_ca_certificate: Optional. SSL certificate to use for requests to GitHub Enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#ssl_ca_certificate DeveloperConnectConnection#ssl_ca_certificate}
        :param webhook_secret_secret_version: Optional. SecretManager resource containing the webhook secret of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#webhook_secret_secret_version DeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = DeveloperConnectConnectionGithubEnterpriseConfig(
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
        authorizer_credential: typing.Union["DeveloperConnectConnectionGitlabConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#authorizer_credential DeveloperConnectConnection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#read_authorizer_credential DeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret of a GitLab project, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#webhook_secret_secret_version DeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = DeveloperConnectConnectionGitlabConfig(
            authorizer_credential=authorizer_credential,
            read_authorizer_credential=read_authorizer_credential,
            webhook_secret_secret_version=webhook_secret_secret_version,
        )

        return typing.cast(None, jsii.invoke(self, "putGitlabConfig", [value]))

    @jsii.member(jsii_name="putGitlabEnterpriseConfig")
    def put_gitlab_enterprise_config(
        self,
        *,
        authorizer_credential: typing.Union["DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        host_uri: builtins.str,
        read_authorizer_credential: typing.Union["DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        service_directory_config: typing.Optional[typing.Union["DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca_certificate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#authorizer_credential DeveloperConnectConnection#authorizer_credential}
        :param host_uri: Required. The URI of the GitLab Enterprise host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#host_uri DeveloperConnectConnection#host_uri}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#read_authorizer_credential DeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret of a GitLab project, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#webhook_secret_secret_version DeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service_directory_config DeveloperConnectConnection#service_directory_config}
        :param ssl_ca_certificate: Optional. SSL Certificate Authority certificate to use for requests to GitLab Enterprise instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#ssl_ca_certificate DeveloperConnectConnection#ssl_ca_certificate}
        '''
        value = DeveloperConnectConnectionGitlabEnterpriseConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#create DeveloperConnectConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#delete DeveloperConnectConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#update DeveloperConnectConnection#update}.
        '''
        value = DeveloperConnectConnectionTimeouts(
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
    ) -> "DeveloperConnectConnectionBitbucketCloudConfigOutputReference":
        return typing.cast("DeveloperConnectConnectionBitbucketCloudConfigOutputReference", jsii.get(self, "bitbucketCloudConfig"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketDataCenterConfig")
    def bitbucket_data_center_config(
        self,
    ) -> "DeveloperConnectConnectionBitbucketDataCenterConfigOutputReference":
        return typing.cast("DeveloperConnectConnectionBitbucketDataCenterConfigOutputReference", jsii.get(self, "bitbucketDataCenterConfig"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyConfig")
    def crypto_key_config(
        self,
    ) -> "DeveloperConnectConnectionCryptoKeyConfigOutputReference":
        return typing.cast("DeveloperConnectConnectionCryptoKeyConfigOutputReference", jsii.get(self, "cryptoKeyConfig"))

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
    def github_config(self) -> "DeveloperConnectConnectionGithubConfigOutputReference":
        return typing.cast("DeveloperConnectConnectionGithubConfigOutputReference", jsii.get(self, "githubConfig"))

    @builtins.property
    @jsii.member(jsii_name="githubEnterpriseConfig")
    def github_enterprise_config(
        self,
    ) -> "DeveloperConnectConnectionGithubEnterpriseConfigOutputReference":
        return typing.cast("DeveloperConnectConnectionGithubEnterpriseConfigOutputReference", jsii.get(self, "githubEnterpriseConfig"))

    @builtins.property
    @jsii.member(jsii_name="gitlabConfig")
    def gitlab_config(self) -> "DeveloperConnectConnectionGitlabConfigOutputReference":
        return typing.cast("DeveloperConnectConnectionGitlabConfigOutputReference", jsii.get(self, "gitlabConfig"))

    @builtins.property
    @jsii.member(jsii_name="gitlabEnterpriseConfig")
    def gitlab_enterprise_config(
        self,
    ) -> "DeveloperConnectConnectionGitlabEnterpriseConfigOutputReference":
        return typing.cast("DeveloperConnectConnectionGitlabEnterpriseConfigOutputReference", jsii.get(self, "gitlabEnterpriseConfig"))

    @builtins.property
    @jsii.member(jsii_name="installationState")
    def installation_state(self) -> "DeveloperConnectConnectionInstallationStateList":
        return typing.cast("DeveloperConnectConnectionInstallationStateList", jsii.get(self, "installationState"))

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
    def timeouts(self) -> "DeveloperConnectConnectionTimeoutsOutputReference":
        return typing.cast("DeveloperConnectConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["DeveloperConnectConnectionBitbucketCloudConfig"]:
        return typing.cast(typing.Optional["DeveloperConnectConnectionBitbucketCloudConfig"], jsii.get(self, "bitbucketCloudConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bitbucketDataCenterConfigInput")
    def bitbucket_data_center_config_input(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionBitbucketDataCenterConfig"]:
        return typing.cast(typing.Optional["DeveloperConnectConnectionBitbucketDataCenterConfig"], jsii.get(self, "bitbucketDataCenterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionIdInput")
    def connection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyConfigInput")
    def crypto_key_config_input(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionCryptoKeyConfig"]:
        return typing.cast(typing.Optional["DeveloperConnectConnectionCryptoKeyConfig"], jsii.get(self, "cryptoKeyConfigInput"))

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
    ) -> typing.Optional["DeveloperConnectConnectionGithubConfig"]:
        return typing.cast(typing.Optional["DeveloperConnectConnectionGithubConfig"], jsii.get(self, "githubConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="githubEnterpriseConfigInput")
    def github_enterprise_config_input(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionGithubEnterpriseConfig"]:
        return typing.cast(typing.Optional["DeveloperConnectConnectionGithubEnterpriseConfig"], jsii.get(self, "githubEnterpriseConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gitlabConfigInput")
    def gitlab_config_input(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionGitlabConfig"]:
        return typing.cast(typing.Optional["DeveloperConnectConnectionGitlabConfig"], jsii.get(self, "gitlabConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gitlabEnterpriseConfigInput")
    def gitlab_enterprise_config_input(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionGitlabEnterpriseConfig"]:
        return typing.cast(typing.Optional["DeveloperConnectConnectionGitlabEnterpriseConfig"], jsii.get(self, "gitlabEnterpriseConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DeveloperConnectConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DeveloperConnectConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c39f91af8ad2c207e75c1de1746d0a9671610b91853c4af3abe942656adadf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionId")
    def connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionId"))

    @connection_id.setter
    def connection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ed325842b3aafa7df12258113a78ad323bc2e1fdca9c52d7d3b59463056d11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb601dead08c5231ddfb31772e61392459124041663a04fdd80322a1fc004eb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @etag.setter
    def etag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3f59d638720f6f8425b75711296e1c4ebe4cec2bb01c499c0aa64fdc9a5bf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "etag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d2d8b7f47548661a7bf517f82512933e7ff382914e3f402f9be363f210cd678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55efd47c6672b55c0cd4b099254aaa69f6e6768420e7b258351ea862310f1454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36762e0e24fb0de2d3af85ab551b54e94b401b9ccbc62ae73579a3c60b05d9c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6aaa9d403ed34fe5395b556c8e8347d588523a4d659b6c51abd83877c36eba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionBitbucketCloudConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_credential": "authorizerCredential",
        "read_authorizer_credential": "readAuthorizerCredential",
        "webhook_secret_secret_version": "webhookSecretSecretVersion",
        "workspace": "workspace",
    },
)
class DeveloperConnectConnectionBitbucketCloudConfig:
    def __init__(
        self,
        *,
        authorizer_credential: typing.Union["DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        workspace: builtins.str,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#authorizer_credential DeveloperConnectConnection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#read_authorizer_credential DeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate and create webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#webhook_secret_secret_version DeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param workspace: Required. The Bitbucket Cloud Workspace ID to be connected to Google Cloud Platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#workspace DeveloperConnectConnection#workspace}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential(**authorizer_credential)
        if isinstance(read_authorizer_credential, dict):
            read_authorizer_credential = DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential(**read_authorizer_credential)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e087b6f89575451fdef2b1d290160045fceedb773c8839ac0c146b96b6a15a)
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
    ) -> "DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential":
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#authorizer_credential DeveloperConnectConnection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        assert result is not None, "Required property 'authorizer_credential' is missing"
        return typing.cast("DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential", result)

    @builtins.property
    def read_authorizer_credential(
        self,
    ) -> "DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential":
        '''read_authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#read_authorizer_credential DeveloperConnectConnection#read_authorizer_credential}
        '''
        result = self._values.get("read_authorizer_credential")
        assert result is not None, "Required property 'read_authorizer_credential' is missing"
        return typing.cast("DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential", result)

    @builtins.property
    def webhook_secret_secret_version(self) -> builtins.str:
        '''Required.

        Immutable. SecretManager resource containing the webhook secret used to verify webhook
        events, formatted as 'projects/* /secrets/* /versions/*'. This is used to
        validate and create webhooks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#webhook_secret_secret_version DeveloperConnectConnection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        assert result is not None, "Required property 'webhook_secret_secret_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace(self) -> builtins.str:
        '''Required. The Bitbucket Cloud Workspace ID to be connected to Google Cloud Platform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#workspace DeveloperConnectConnection#workspace}
        '''
        result = self._values.get("workspace")
        assert result is not None, "Required property 'workspace' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeveloperConnectConnectionBitbucketCloudConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcdfd51330728864840339013d6a8950dfd25129a206e29a662faf9ad8e0d2e7)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version}

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
        return "DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4edc2e9ffa25975258e69b9613e3d2ba0572762b378c42b09e50e45263b3e273)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73c4ae16f817125edb7e5956bffb39eae4c6635c8bf65e40a918b31efb69eda9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bde1051a82f13b4ffc531b176eaaf6b410fc0f2da43889188c3243649a2d7791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DeveloperConnectConnectionBitbucketCloudConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionBitbucketCloudConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ce74a69d88d740009bf3a09b95db7d62939c103102e5bbda87da6405e0431e4)
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential(
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putReadAuthorizerCredential", [value]))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredential")
    def authorizer_credential(
        self,
    ) -> DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference:
        return typing.cast(DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredential")
    def read_authorizer_credential(
        self,
    ) -> "DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference":
        return typing.cast("DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference", jsii.get(self, "readAuthorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredentialInput")
    def read_authorizer_credential_input(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential"]:
        return typing.cast(typing.Optional["DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential"], jsii.get(self, "readAuthorizerCredentialInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d93057caa9d69b7d95f3a763c72cec778d9a41c60696894666ca98c8c4810557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspace")
    def workspace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspace"))

    @workspace.setter
    def workspace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c9fcfd06fd2ac9c10541121874321454963012671c3cf1c7ed29d77a154af3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionBitbucketCloudConfig]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionBitbucketCloudConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionBitbucketCloudConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f212d90fc6860b6d9efee9d4e29fb24e0fe4c12a98442d1d64116cd7899e47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49436b5f0456064837b142664630b0d864c5b2683ff41cf600c4edd3cd0759c)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version}

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
        return "DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94a5a70f14f731ac0637365abe18c5694051e00aafe1f1efb47889be8241f3e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b2db4fd71461328dbcbbe83093cd8618236fcf1021d3debfb01853585f7b926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9972adb1d8c28d695082da85e8afaa14f7306fa7fc2d98ac74acb89893cfba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionBitbucketDataCenterConfig",
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
class DeveloperConnectConnectionBitbucketDataCenterConfig:
    def __init__(
        self,
        *,
        authorizer_credential: typing.Union["DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        host_uri: builtins.str,
        read_authorizer_credential: typing.Union["DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        service_directory_config: typing.Optional[typing.Union["DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca_certificate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#authorizer_credential DeveloperConnectConnection#authorizer_credential}
        :param host_uri: Required. The URI of the Bitbucket Data Center host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#host_uri DeveloperConnectConnection#host_uri}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#read_authorizer_credential DeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret used to verify webhook events, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#webhook_secret_secret_version DeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service_directory_config DeveloperConnectConnection#service_directory_config}
        :param ssl_ca_certificate: Optional. SSL certificate authority to trust when making requests to Bitbucket Data Center. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#ssl_ca_certificate DeveloperConnectConnection#ssl_ca_certificate}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential(**authorizer_credential)
        if isinstance(read_authorizer_credential, dict):
            read_authorizer_credential = DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential(**read_authorizer_credential)
        if isinstance(service_directory_config, dict):
            service_directory_config = DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig(**service_directory_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6138039f66db7c5a1445f64936d757ecfbf7ce7ec69a36b162dc3939f164704)
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
    ) -> "DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential":
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#authorizer_credential DeveloperConnectConnection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        assert result is not None, "Required property 'authorizer_credential' is missing"
        return typing.cast("DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential", result)

    @builtins.property
    def host_uri(self) -> builtins.str:
        '''Required. The URI of the Bitbucket Data Center host this connection is for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#host_uri DeveloperConnectConnection#host_uri}
        '''
        result = self._values.get("host_uri")
        assert result is not None, "Required property 'host_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_authorizer_credential(
        self,
    ) -> "DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential":
        '''read_authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#read_authorizer_credential DeveloperConnectConnection#read_authorizer_credential}
        '''
        result = self._values.get("read_authorizer_credential")
        assert result is not None, "Required property 'read_authorizer_credential' is missing"
        return typing.cast("DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential", result)

    @builtins.property
    def webhook_secret_secret_version(self) -> builtins.str:
        '''Required.

        Immutable. SecretManager resource containing the webhook secret used to verify webhook
        events, formatted as 'projects/* /secrets/* /versions/*'. This is used to
        validate webhooks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#webhook_secret_secret_version DeveloperConnectConnection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        assert result is not None, "Required property 'webhook_secret_secret_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_directory_config(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig"]:
        '''service_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service_directory_config DeveloperConnectConnection#service_directory_config}
        '''
        result = self._values.get("service_directory_config")
        return typing.cast(typing.Optional["DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig"], result)

    @builtins.property
    def ssl_ca_certificate(self) -> typing.Optional[builtins.str]:
        '''Optional. SSL certificate authority to trust when making requests to Bitbucket Data Center.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#ssl_ca_certificate DeveloperConnectConnection#ssl_ca_certificate}
        '''
        result = self._values.get("ssl_ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeveloperConnectConnectionBitbucketDataCenterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a603600345b15d889e3353a36940c7cab743d7dca01a9555f1864d42bfb9cb5)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version}

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
        return "DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a06d55c3f5549f093cc77c60dfe9b39379ce5c39d508b83494d5232a19f60b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__668c4bc11d8d68e58aa3e99fc63f59b9c59da48793eba60cd879ad57652891d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22056d9e5b8e9dc66a7ed9caa89fcfd1291b78863e7f30b6356dbf7eabd31c11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DeveloperConnectConnectionBitbucketDataCenterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionBitbucketDataCenterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f043487ef8a4303fb4bb652787d82fce29955a2b2c43b46e258bab3626b391a5)
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential(
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putReadAuthorizerCredential", [value]))

    @jsii.member(jsii_name="putServiceDirectoryConfig")
    def put_service_directory_config(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service DeveloperConnectConnection#service}
        '''
        value = DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig(
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
    ) -> DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference:
        return typing.cast(DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredential")
    def read_authorizer_credential(
        self,
    ) -> "DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference":
        return typing.cast("DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference", jsii.get(self, "readAuthorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="serverVersion")
    def server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverVersion"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfig")
    def service_directory_config(
        self,
    ) -> "DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference":
        return typing.cast("DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference", jsii.get(self, "serviceDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="hostUriInput")
    def host_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostUriInput"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredentialInput")
    def read_authorizer_credential_input(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential"]:
        return typing.cast(typing.Optional["DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential"], jsii.get(self, "readAuthorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfigInput")
    def service_directory_config_input(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig"]:
        return typing.cast(typing.Optional["DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig"], jsii.get(self, "serviceDirectoryConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0ab122fc2755b96e75b037d9c1c4ea726fc9d966e4fbb461f4b3df6554679b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCaCertificate")
    def ssl_ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCaCertificate"))

    @ssl_ca_certificate.setter
    def ssl_ca_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bacee05d30c2b80c54d94b2bd6e70a4e9925a125805e243204b3c94a542adf3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCaCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretSecretVersion"))

    @webhook_secret_secret_version.setter
    def webhook_secret_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31267240419529b2a5d13a013f8c56cf7be3dd5126c61bddd29db984d4f53bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfig]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__837e47937a03a735535e54006b765e8fe9e2724e6b7bdc0a6c7d63a382cf79bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34306204031fbf6ccfd2a91c8fab61a8951691561807fbcada866d30f65e7175)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version}

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
        return "DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3263b225171c8969bf3b977621450d30550fa7621431664b0e41ab4e1da29150)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7684c4dfb9d932aa499097ab3447f41d22a61f4bcb5198fa34945ece6e46a9db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016e759a3d570bf6acdfabd8f212c168c20a3d42b8349729a16fe46dfd5017da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"service": "service"},
)
class DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig:
    def __init__(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service DeveloperConnectConnection#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e8bcb1836923d65792df11fd2b60968de006bae3fc0ffce2a74a598bbc3d3ac)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service DeveloperConnectConnection#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2646778169c03fa9450468d471e197cfe7bd0f31f3ccc5d6e9de2d901c0445e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03ec0a3ac1066e9f3306f82902dcbaeabc7e45f376740fec29f2036be98c1c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80d7e9d2bbcbe8a504295a46a7927c1138bfdf4b64c316876fe9306514e7c469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionConfig",
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
class DeveloperConnectConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bitbucket_cloud_config: typing.Optional[typing.Union[DeveloperConnectConnectionBitbucketCloudConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        bitbucket_data_center_config: typing.Optional[typing.Union[DeveloperConnectConnectionBitbucketDataCenterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        crypto_key_config: typing.Optional[typing.Union["DeveloperConnectConnectionCryptoKeyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        etag: typing.Optional[builtins.str] = None,
        github_config: typing.Optional[typing.Union["DeveloperConnectConnectionGithubConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        github_enterprise_config: typing.Optional[typing.Union["DeveloperConnectConnectionGithubEnterpriseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gitlab_config: typing.Optional[typing.Union["DeveloperConnectConnectionGitlabConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gitlab_enterprise_config: typing.Optional[typing.Union["DeveloperConnectConnectionGitlabEnterpriseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DeveloperConnectConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param connection_id: Required. Id of the requesting object If auto-generating Id server-side, remove this field and connection_id from the method_signature of Create RPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#connection_id DeveloperConnectConnection#connection_id}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#location DeveloperConnectConnection#location}
        :param annotations: Optional. Allows clients to store small amounts of arbitrary data. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#annotations DeveloperConnectConnection#annotations}
        :param bitbucket_cloud_config: bitbucket_cloud_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#bitbucket_cloud_config DeveloperConnectConnection#bitbucket_cloud_config}
        :param bitbucket_data_center_config: bitbucket_data_center_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#bitbucket_data_center_config DeveloperConnectConnection#bitbucket_data_center_config}
        :param crypto_key_config: crypto_key_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#crypto_key_config DeveloperConnectConnection#crypto_key_config}
        :param disabled: Optional. If disabled is set to true, functionality is disabled for this connection. Repository based API methods and webhooks processing for repositories in this connection will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#disabled DeveloperConnectConnection#disabled}
        :param etag: Optional. This checksum is computed by the server based on the value of other fields, and may be sent on update and delete requests to ensure the client has an up-to-date value before proceeding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#etag DeveloperConnectConnection#etag}
        :param github_config: github_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#github_config DeveloperConnectConnection#github_config}
        :param github_enterprise_config: github_enterprise_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#github_enterprise_config DeveloperConnectConnection#github_enterprise_config}
        :param gitlab_config: gitlab_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#gitlab_config DeveloperConnectConnection#gitlab_config}
        :param gitlab_enterprise_config: gitlab_enterprise_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#gitlab_enterprise_config DeveloperConnectConnection#gitlab_enterprise_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#id DeveloperConnectConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#labels DeveloperConnectConnection#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#project DeveloperConnectConnection#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#timeouts DeveloperConnectConnection#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bitbucket_cloud_config, dict):
            bitbucket_cloud_config = DeveloperConnectConnectionBitbucketCloudConfig(**bitbucket_cloud_config)
        if isinstance(bitbucket_data_center_config, dict):
            bitbucket_data_center_config = DeveloperConnectConnectionBitbucketDataCenterConfig(**bitbucket_data_center_config)
        if isinstance(crypto_key_config, dict):
            crypto_key_config = DeveloperConnectConnectionCryptoKeyConfig(**crypto_key_config)
        if isinstance(github_config, dict):
            github_config = DeveloperConnectConnectionGithubConfig(**github_config)
        if isinstance(github_enterprise_config, dict):
            github_enterprise_config = DeveloperConnectConnectionGithubEnterpriseConfig(**github_enterprise_config)
        if isinstance(gitlab_config, dict):
            gitlab_config = DeveloperConnectConnectionGitlabConfig(**gitlab_config)
        if isinstance(gitlab_enterprise_config, dict):
            gitlab_enterprise_config = DeveloperConnectConnectionGitlabEnterpriseConfig(**gitlab_enterprise_config)
        if isinstance(timeouts, dict):
            timeouts = DeveloperConnectConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbc4944cb0b9799a6e96ded50817370b6b2b1d50e564c4b66838f400c3718533)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#connection_id DeveloperConnectConnection#connection_id}
        '''
        result = self._values.get("connection_id")
        assert result is not None, "Required property 'connection_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#location DeveloperConnectConnection#location}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#annotations DeveloperConnectConnection#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bitbucket_cloud_config(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionBitbucketCloudConfig]:
        '''bitbucket_cloud_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#bitbucket_cloud_config DeveloperConnectConnection#bitbucket_cloud_config}
        '''
        result = self._values.get("bitbucket_cloud_config")
        return typing.cast(typing.Optional[DeveloperConnectConnectionBitbucketCloudConfig], result)

    @builtins.property
    def bitbucket_data_center_config(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfig]:
        '''bitbucket_data_center_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#bitbucket_data_center_config DeveloperConnectConnection#bitbucket_data_center_config}
        '''
        result = self._values.get("bitbucket_data_center_config")
        return typing.cast(typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfig], result)

    @builtins.property
    def crypto_key_config(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionCryptoKeyConfig"]:
        '''crypto_key_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#crypto_key_config DeveloperConnectConnection#crypto_key_config}
        '''
        result = self._values.get("crypto_key_config")
        return typing.cast(typing.Optional["DeveloperConnectConnectionCryptoKeyConfig"], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        If disabled is set to true, functionality is disabled for this connection.
        Repository based API methods and webhooks processing for repositories in
        this connection will be disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#disabled DeveloperConnectConnection#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def etag(self) -> typing.Optional[builtins.str]:
        '''Optional.

        This checksum is computed by the server based on the value of other
        fields, and may be sent on update and delete requests to ensure the
        client has an up-to-date value before proceeding.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#etag DeveloperConnectConnection#etag}
        '''
        result = self._values.get("etag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_config(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionGithubConfig"]:
        '''github_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#github_config DeveloperConnectConnection#github_config}
        '''
        result = self._values.get("github_config")
        return typing.cast(typing.Optional["DeveloperConnectConnectionGithubConfig"], result)

    @builtins.property
    def github_enterprise_config(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionGithubEnterpriseConfig"]:
        '''github_enterprise_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#github_enterprise_config DeveloperConnectConnection#github_enterprise_config}
        '''
        result = self._values.get("github_enterprise_config")
        return typing.cast(typing.Optional["DeveloperConnectConnectionGithubEnterpriseConfig"], result)

    @builtins.property
    def gitlab_config(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionGitlabConfig"]:
        '''gitlab_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#gitlab_config DeveloperConnectConnection#gitlab_config}
        '''
        result = self._values.get("gitlab_config")
        return typing.cast(typing.Optional["DeveloperConnectConnectionGitlabConfig"], result)

    @builtins.property
    def gitlab_enterprise_config(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionGitlabEnterpriseConfig"]:
        '''gitlab_enterprise_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#gitlab_enterprise_config DeveloperConnectConnection#gitlab_enterprise_config}
        '''
        result = self._values.get("gitlab_enterprise_config")
        return typing.cast(typing.Optional["DeveloperConnectConnectionGitlabEnterpriseConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#id DeveloperConnectConnection#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#labels DeveloperConnectConnection#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#project DeveloperConnectConnection#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DeveloperConnectConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#timeouts DeveloperConnectConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DeveloperConnectConnectionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeveloperConnectConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionCryptoKeyConfig",
    jsii_struct_bases=[],
    name_mapping={"key_reference": "keyReference"},
)
class DeveloperConnectConnectionCryptoKeyConfig:
    def __init__(self, *, key_reference: builtins.str) -> None:
        '''
        :param key_reference: Required. The name of the key which is used to encrypt/decrypt customer data. For key in Cloud KMS, the key should be in the format of 'projects/* /locations/* /keyRings/* /cryptoKeys/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#key_reference DeveloperConnectConnection#key_reference} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd043c71f3920c80935370b7d4edbe7317c6e28c25afa603e412a4c694ea424)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#key_reference DeveloperConnectConnection#key_reference}

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
        return "DeveloperConnectConnectionCryptoKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionCryptoKeyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionCryptoKeyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7151c358a6ba2ba1d58edc3dc28cc02d9f0c200b952809ae87d49f59f3c9e9c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e802136bb02af16b19c2204c88d6cb6ba053213d94acc6eec1d78f5fb18c605f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyReference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionCryptoKeyConfig]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionCryptoKeyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionCryptoKeyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c185d85abc6df5f016399869eb3e0e2905aea96671be851d3a96e9b5ccdf9529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGithubConfig",
    jsii_struct_bases=[],
    name_mapping={
        "github_app": "githubApp",
        "app_installation_id": "appInstallationId",
        "authorizer_credential": "authorizerCredential",
    },
)
class DeveloperConnectConnectionGithubConfig:
    def __init__(
        self,
        *,
        github_app: builtins.str,
        app_installation_id: typing.Optional[builtins.str] = None,
        authorizer_credential: typing.Optional[typing.Union["DeveloperConnectConnectionGithubConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param github_app: Required. Immutable. The GitHub Application that was installed to the GitHub user or organization. Possible values: GIT_HUB_APP_UNSPECIFIED DEVELOPER_CONNECT FIREBASE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#github_app DeveloperConnectConnection#github_app}
        :param app_installation_id: Optional. GitHub App installation id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#app_installation_id DeveloperConnectConnection#app_installation_id}
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#authorizer_credential DeveloperConnectConnection#authorizer_credential}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = DeveloperConnectConnectionGithubConfigAuthorizerCredential(**authorizer_credential)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e47510a7d75a1275b5ced081cac1613f37b194a752269cce90afc384735739)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#github_app DeveloperConnectConnection#github_app}
        '''
        result = self._values.get("github_app")
        assert result is not None, "Required property 'github_app' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_installation_id(self) -> typing.Optional[builtins.str]:
        '''Optional. GitHub App installation id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#app_installation_id DeveloperConnectConnection#app_installation_id}
        '''
        result = self._values.get("app_installation_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorizer_credential(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionGithubConfigAuthorizerCredential"]:
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#authorizer_credential DeveloperConnectConnection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        return typing.cast(typing.Optional["DeveloperConnectConnectionGithubConfigAuthorizerCredential"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeveloperConnectConnectionGithubConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGithubConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"oauth_token_secret_version": "oauthTokenSecretVersion"},
)
class DeveloperConnectConnectionGithubConfigAuthorizerCredential:
    def __init__(self, *, oauth_token_secret_version: builtins.str) -> None:
        '''
        :param oauth_token_secret_version: Required. A SecretManager resource containing the OAuth token that authorizes the connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#oauth_token_secret_version DeveloperConnectConnection#oauth_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b35f4095d7f0bf91eec57da4deeb0b52cae3b8e615ac782df878f6be9ded4c6)
            check_type(argname="argument oauth_token_secret_version", value=oauth_token_secret_version, expected_type=type_hints["oauth_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "oauth_token_secret_version": oauth_token_secret_version,
        }

    @builtins.property
    def oauth_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the OAuth token that authorizes the connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#oauth_token_secret_version DeveloperConnectConnection#oauth_token_secret_version}

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
        return "DeveloperConnectConnectionGithubConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionGithubConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGithubConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbcbb2ca3318b1ac114136e0991d002b6f5b66c47f6c0caff667c041c291ba60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26cab7f30a80045003622f94b72c341c1a088feab1d88564032a3e6ec3ae574c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionGithubConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionGithubConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionGithubConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5f10d88c270de0cdb8b3b1475a0b4ed0cad8b5b2794c8645c4d24761fcd8ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DeveloperConnectConnectionGithubConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGithubConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3320adebc70b773f11a12fb768ae3e5858ba2d884901321dc8cc3d477a36fb62)
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
        :param oauth_token_secret_version: Required. A SecretManager resource containing the OAuth token that authorizes the connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#oauth_token_secret_version DeveloperConnectConnection#oauth_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = DeveloperConnectConnectionGithubConfigAuthorizerCredential(
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
    ) -> DeveloperConnectConnectionGithubConfigAuthorizerCredentialOutputReference:
        return typing.cast(DeveloperConnectConnectionGithubConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

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
    ) -> typing.Optional[DeveloperConnectConnectionGithubConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionGithubConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__34de131aca48787c75f3d9edf6e3f8a869adae73f24a09d1a642e3c39b3ab4c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appInstallationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="githubApp")
    def github_app(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "githubApp"))

    @github_app.setter
    def github_app(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9a3981d497fbfdffe20e74a2a9a006fd9279a51148b2249e9a4b56268c6bce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "githubApp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DeveloperConnectConnectionGithubConfig]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionGithubConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionGithubConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4458961ed29fa8a248752eedd2c632d2913562e97a20144932112696a721966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGithubEnterpriseConfig",
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
class DeveloperConnectConnectionGithubEnterpriseConfig:
    def __init__(
        self,
        *,
        host_uri: builtins.str,
        app_id: typing.Optional[builtins.str] = None,
        app_installation_id: typing.Optional[builtins.str] = None,
        private_key_secret_version: typing.Optional[builtins.str] = None,
        service_directory_config: typing.Optional[typing.Union["DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca_certificate: typing.Optional[builtins.str] = None,
        webhook_secret_secret_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_uri: Required. The URI of the GitHub Enterprise host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#host_uri DeveloperConnectConnection#host_uri}
        :param app_id: Optional. ID of the GitHub App created from the manifest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#app_id DeveloperConnectConnection#app_id}
        :param app_installation_id: Optional. ID of the installation of the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#app_installation_id DeveloperConnectConnection#app_installation_id}
        :param private_key_secret_version: Optional. SecretManager resource containing the private key of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#private_key_secret_version DeveloperConnectConnection#private_key_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service_directory_config DeveloperConnectConnection#service_directory_config}
        :param ssl_ca_certificate: Optional. SSL certificate to use for requests to GitHub Enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#ssl_ca_certificate DeveloperConnectConnection#ssl_ca_certificate}
        :param webhook_secret_secret_version: Optional. SecretManager resource containing the webhook secret of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#webhook_secret_secret_version DeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if isinstance(service_directory_config, dict):
            service_directory_config = DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig(**service_directory_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4b6f5f929aff03e75052965ab095c5968016807d1c847182d73047227b3cb2c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#host_uri DeveloperConnectConnection#host_uri}
        '''
        result = self._values.get("host_uri")
        assert result is not None, "Required property 'host_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_id(self) -> typing.Optional[builtins.str]:
        '''Optional. ID of the GitHub App created from the manifest.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#app_id DeveloperConnectConnection#app_id}
        '''
        result = self._values.get("app_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_installation_id(self) -> typing.Optional[builtins.str]:
        '''Optional. ID of the installation of the GitHub App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#app_installation_id DeveloperConnectConnection#app_installation_id}
        '''
        result = self._values.get("app_installation_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_secret_version(self) -> typing.Optional[builtins.str]:
        '''Optional. SecretManager resource containing the private key of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#private_key_secret_version DeveloperConnectConnection#private_key_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("private_key_secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_directory_config(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig"]:
        '''service_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service_directory_config DeveloperConnectConnection#service_directory_config}
        '''
        result = self._values.get("service_directory_config")
        return typing.cast(typing.Optional["DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig"], result)

    @builtins.property
    def ssl_ca_certificate(self) -> typing.Optional[builtins.str]:
        '''Optional. SSL certificate to use for requests to GitHub Enterprise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#ssl_ca_certificate DeveloperConnectConnection#ssl_ca_certificate}
        '''
        result = self._values.get("ssl_ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webhook_secret_secret_version(self) -> typing.Optional[builtins.str]:
        '''Optional. SecretManager resource containing the webhook secret of the GitHub App, formatted as 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#webhook_secret_secret_version DeveloperConnectConnection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeveloperConnectConnectionGithubEnterpriseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionGithubEnterpriseConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGithubEnterpriseConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aedf431d028cf6d551e7e4cfdf27bf85714160e1f4313dbc8e44c1ed055ddd6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putServiceDirectoryConfig")
    def put_service_directory_config(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service DeveloperConnectConnection#service}
        '''
        value = DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig(
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
    ) -> "DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference":
        return typing.cast("DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference", jsii.get(self, "serviceDirectoryConfig"))

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
    ) -> typing.Optional["DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig"]:
        return typing.cast(typing.Optional["DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig"], jsii.get(self, "serviceDirectoryConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__981afc9afdcd5c1bdba2003a3ab2a8f70e0e43fcad2509c49665936672627ca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appInstallationId")
    def app_installation_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appInstallationId"))

    @app_installation_id.setter
    def app_installation_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5099c5d3e43c727c535e4a05eb0f4521fc85699425f1395a8ef4d516c7544f41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appInstallationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostUri")
    def host_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostUri"))

    @host_uri.setter
    def host_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65880c4ab222a4b79727f8e17b1bf06423a165f455454fde71e216327821a9aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKeySecretVersion")
    def private_key_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKeySecretVersion"))

    @private_key_secret_version.setter
    def private_key_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89fa07f95795bcaea72d09d75ea7b45fd39f0db6514531253048f1b18b9688e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeySecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCaCertificate")
    def ssl_ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCaCertificate"))

    @ssl_ca_certificate.setter
    def ssl_ca_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4296e19a17a7924c23c2204b7569be5f3a1b6baa1be6be249003e1f884c4b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCaCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretSecretVersion"))

    @webhook_secret_secret_version.setter
    def webhook_secret_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ef6dc7f69f56e0d227d113abc0cf11592f0e76fbb49397f7a1bbd768f8c7766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionGithubEnterpriseConfig]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionGithubEnterpriseConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionGithubEnterpriseConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d7be3f6ddc8cda204df6cc96dce681a582835b2844bd647bf11b639be51f8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"service": "service"},
)
class DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig:
    def __init__(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service DeveloperConnectConnection#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdcc5fbd5c68abde04f469e08be68c41d3ee8b77cae8e10c0582c804d10ec1c0)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service DeveloperConnectConnection#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17b798649703d0d2171930757de6d64a7e8b2f78c5a1976fcee2e739a7c19096)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0732346470e83db13fe155b6337820d868e0746361e24c69062bffcd58ed5611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec4640cdccfe40c65a9ef1c2abd2226a66675a1c4d0fb12964b8b1d576a71c74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGitlabConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_credential": "authorizerCredential",
        "read_authorizer_credential": "readAuthorizerCredential",
        "webhook_secret_secret_version": "webhookSecretSecretVersion",
    },
)
class DeveloperConnectConnectionGitlabConfig:
    def __init__(
        self,
        *,
        authorizer_credential: typing.Union["DeveloperConnectConnectionGitlabConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        read_authorizer_credential: typing.Union["DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#authorizer_credential DeveloperConnectConnection#authorizer_credential}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#read_authorizer_credential DeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret of a GitLab project, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#webhook_secret_secret_version DeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = DeveloperConnectConnectionGitlabConfigAuthorizerCredential(**authorizer_credential)
        if isinstance(read_authorizer_credential, dict):
            read_authorizer_credential = DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential(**read_authorizer_credential)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d71d0dcee3e119858e57d7f1b38f77eabab8f189ac34e4be5d5716b50673edac)
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
    ) -> "DeveloperConnectConnectionGitlabConfigAuthorizerCredential":
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#authorizer_credential DeveloperConnectConnection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        assert result is not None, "Required property 'authorizer_credential' is missing"
        return typing.cast("DeveloperConnectConnectionGitlabConfigAuthorizerCredential", result)

    @builtins.property
    def read_authorizer_credential(
        self,
    ) -> "DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential":
        '''read_authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#read_authorizer_credential DeveloperConnectConnection#read_authorizer_credential}
        '''
        result = self._values.get("read_authorizer_credential")
        assert result is not None, "Required property 'read_authorizer_credential' is missing"
        return typing.cast("DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential", result)

    @builtins.property
    def webhook_secret_secret_version(self) -> builtins.str:
        '''Required.

        Immutable. SecretManager resource containing the webhook secret of a GitLab project,
        formatted as 'projects/* /secrets/* /versions/*'. This is used to validate
        webhooks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#webhook_secret_secret_version DeveloperConnectConnection#webhook_secret_secret_version}

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
        return "DeveloperConnectConnectionGitlabConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGitlabConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class DeveloperConnectConnectionGitlabConfigAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4cfbf1f205c1ce9a5cdc481dfcfed76495e011a41fb810f5911346c79617a22)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version}

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
        return "DeveloperConnectConnectionGitlabConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionGitlabConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGitlabConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df96e76bbd6f7a46af11921c311d9c2ae91d2bc9bfa16b85b3727623e963b6c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf1e1b78fda5487a6b8ef0649bdd5556de21b140627f467764d10eec04303fae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionGitlabConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionGitlabConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionGitlabConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8be2fcfb14e18de38bfe97098e1a4b19532597d12ad646c8ba772c2a05ceb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DeveloperConnectConnectionGitlabConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGitlabConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0e0d7d47c784391218144e5b0e0f06303f9ccb923432da2a78d70ae7b0a1afe)
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = DeveloperConnectConnectionGitlabConfigAuthorizerCredential(
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putReadAuthorizerCredential", [value]))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredential")
    def authorizer_credential(
        self,
    ) -> DeveloperConnectConnectionGitlabConfigAuthorizerCredentialOutputReference:
        return typing.cast(DeveloperConnectConnectionGitlabConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredential")
    def read_authorizer_credential(
        self,
    ) -> "DeveloperConnectConnectionGitlabConfigReadAuthorizerCredentialOutputReference":
        return typing.cast("DeveloperConnectConnectionGitlabConfigReadAuthorizerCredentialOutputReference", jsii.get(self, "readAuthorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionGitlabConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionGitlabConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredentialInput")
    def read_authorizer_credential_input(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential"]:
        return typing.cast(typing.Optional["DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential"], jsii.get(self, "readAuthorizerCredentialInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__acdae9c50867f37aa4d09b45929cd1d73bb6574b6afcca1ab773334675ae601c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DeveloperConnectConnectionGitlabConfig]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionGitlabConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionGitlabConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d833a45c6854b9f9ac36f02e0f93675b1e5ff2987f2cc357d5a4c894bf525712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b13c3272511f81508579bf34dd8b5174a29f7130210bfff134c6c281c13d15)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version}

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
        return "DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionGitlabConfigReadAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGitlabConfigReadAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7fac92a87d42a52c6dfbd13413133d6c16dac68079b7c3c304d9e07d70d1ced)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b45301e90895000ecaa0c20f09044f67298b7936fd0da9593d46c163f84f53ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b3f5be430940ee09f5bc90a122e6edde28dd50749eab179408ca29e4814551f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGitlabEnterpriseConfig",
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
class DeveloperConnectConnectionGitlabEnterpriseConfig:
    def __init__(
        self,
        *,
        authorizer_credential: typing.Union["DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        host_uri: builtins.str,
        read_authorizer_credential: typing.Union["DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential", typing.Dict[builtins.str, typing.Any]],
        webhook_secret_secret_version: builtins.str,
        service_directory_config: typing.Optional[typing.Union["DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_ca_certificate: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_credential: authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#authorizer_credential DeveloperConnectConnection#authorizer_credential}
        :param host_uri: Required. The URI of the GitLab Enterprise host this connection is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#host_uri DeveloperConnectConnection#host_uri}
        :param read_authorizer_credential: read_authorizer_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#read_authorizer_credential DeveloperConnectConnection#read_authorizer_credential}
        :param webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret of a GitLab project, formatted as 'projects/* /secrets/* /versions/*'. This is used to validate webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#webhook_secret_secret_version DeveloperConnectConnection#webhook_secret_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service_directory_config DeveloperConnectConnection#service_directory_config}
        :param ssl_ca_certificate: Optional. SSL Certificate Authority certificate to use for requests to GitLab Enterprise instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#ssl_ca_certificate DeveloperConnectConnection#ssl_ca_certificate}
        '''
        if isinstance(authorizer_credential, dict):
            authorizer_credential = DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential(**authorizer_credential)
        if isinstance(read_authorizer_credential, dict):
            read_authorizer_credential = DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential(**read_authorizer_credential)
        if isinstance(service_directory_config, dict):
            service_directory_config = DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig(**service_directory_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34804edb3f9b1a12c384d9752d82e6dc97810a1ed46dd50263fb474ee972d04f)
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
    ) -> "DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential":
        '''authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#authorizer_credential DeveloperConnectConnection#authorizer_credential}
        '''
        result = self._values.get("authorizer_credential")
        assert result is not None, "Required property 'authorizer_credential' is missing"
        return typing.cast("DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential", result)

    @builtins.property
    def host_uri(self) -> builtins.str:
        '''Required. The URI of the GitLab Enterprise host this connection is for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#host_uri DeveloperConnectConnection#host_uri}
        '''
        result = self._values.get("host_uri")
        assert result is not None, "Required property 'host_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_authorizer_credential(
        self,
    ) -> "DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential":
        '''read_authorizer_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#read_authorizer_credential DeveloperConnectConnection#read_authorizer_credential}
        '''
        result = self._values.get("read_authorizer_credential")
        assert result is not None, "Required property 'read_authorizer_credential' is missing"
        return typing.cast("DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential", result)

    @builtins.property
    def webhook_secret_secret_version(self) -> builtins.str:
        '''Required.

        Immutable. SecretManager resource containing the webhook secret of a GitLab project,
        formatted as 'projects/* /secrets/* /versions/*'. This is used to validate
        webhooks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#webhook_secret_secret_version DeveloperConnectConnection#webhook_secret_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("webhook_secret_secret_version")
        assert result is not None, "Required property 'webhook_secret_secret_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_directory_config(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig"]:
        '''service_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service_directory_config DeveloperConnectConnection#service_directory_config}
        '''
        result = self._values.get("service_directory_config")
        return typing.cast(typing.Optional["DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig"], result)

    @builtins.property
    def ssl_ca_certificate(self) -> typing.Optional[builtins.str]:
        '''Optional. SSL Certificate Authority certificate to use for requests to GitLab Enterprise instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#ssl_ca_certificate DeveloperConnectConnection#ssl_ca_certificate}
        '''
        result = self._values.get("ssl_ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeveloperConnectConnectionGitlabEnterpriseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38a276f4391993b3d67217fcce2108059cd138e1bb3ff9fa895a3c4b7ce5b85)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version}

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
        return "DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1647efb0c657d9f092eaf8a37337c3f2af5703c41387453be08e94b481179c07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__daf3165439903fd07b011a75cc0d558a6aabc842eb3bd1fe603572adfb89046b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e16cf2193390c05f3326797967890f9969d1717017ce45a75559e0a8621113a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DeveloperConnectConnectionGitlabEnterpriseConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGitlabEnterpriseConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dccc7d047947c6ffa047b4ad506c4d4a6f591712076719c13447df98a72d67e2)
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential(
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
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential(
            user_token_secret_version=user_token_secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putReadAuthorizerCredential", [value]))

    @jsii.member(jsii_name="putServiceDirectoryConfig")
    def put_service_directory_config(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service DeveloperConnectConnection#service}
        '''
        value = DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig(
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
    ) -> DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredentialOutputReference:
        return typing.cast(DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredentialOutputReference, jsii.get(self, "authorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredential")
    def read_authorizer_credential(
        self,
    ) -> "DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredentialOutputReference":
        return typing.cast("DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredentialOutputReference", jsii.get(self, "readAuthorizerCredential"))

    @builtins.property
    @jsii.member(jsii_name="serverVersion")
    def server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverVersion"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfig")
    def service_directory_config(
        self,
    ) -> "DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfigOutputReference":
        return typing.cast("DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfigOutputReference", jsii.get(self, "serviceDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialInput")
    def authorizer_credential_input(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential], jsii.get(self, "authorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="hostUriInput")
    def host_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostUriInput"))

    @builtins.property
    @jsii.member(jsii_name="readAuthorizerCredentialInput")
    def read_authorizer_credential_input(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential"]:
        return typing.cast(typing.Optional["DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential"], jsii.get(self, "readAuthorizerCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfigInput")
    def service_directory_config_input(
        self,
    ) -> typing.Optional["DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig"]:
        return typing.cast(typing.Optional["DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig"], jsii.get(self, "serviceDirectoryConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a55bd3bca07a2d04082b0eff0a4e6fb970e732e0dc518fd67d2acdc82591106d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCaCertificate")
    def ssl_ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCaCertificate"))

    @ssl_ca_certificate.setter
    def ssl_ca_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e7f6e589c9c13bd5e9220755eb6bc8c11a728d55c128027b63dc95ae5cf8e04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCaCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretSecretVersion"))

    @webhook_secret_secret_version.setter
    def webhook_secret_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1324d3a1ecad74e5e1c9106eb8e80ce60f8e4a96f2c0ca5221414f09669a51b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfig]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__869b1a6314a7c42a6b9e87e77c5974aa54eb93d09706ff609eab193a22ebb86f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential",
    jsii_struct_bases=[],
    name_mapping={"user_token_secret_version": "userTokenSecretVersion"},
)
class DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential:
    def __init__(self, *, user_token_secret_version: builtins.str) -> None:
        '''
        :param user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3559ba8cba72c54de84969fbefb68855c716dd68ae9e39819f889b7f7db47f14)
            check_type(argname="argument user_token_secret_version", value=user_token_secret_version, expected_type=type_hints["user_token_secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_token_secret_version": user_token_secret_version,
        }

    @builtins.property
    def user_token_secret_version(self) -> builtins.str:
        '''Required. A SecretManager resource containing the user token that authorizes the Developer Connect connection. Format: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#user_token_secret_version DeveloperConnectConnection#user_token_secret_version}

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
        return "DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07e8f5ba182847acbe7f1bbd0651b368e15860e66cd078237840b2800ddb47ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da3d78f96f2e1e4e47c7e8310ee4bdab2478d405f3c5ed406aa6ca9eb73a9346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b106675e973c2b82faead5cd303fcc26f38a40e2360b92d73afb5eb5412e06f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"service": "service"},
)
class DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig:
    def __init__(self, *, service: builtins.str) -> None:
        '''
        :param service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service DeveloperConnectConnection#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__986e224616be57c0a008bf9c48282a4c61539fb97aa27b8e3d554fd4539c3818)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#service DeveloperConnectConnection#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d8af218d7962fe9a299e09bded262b52b7a1812a409c5b5631aa08fbab562ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b653e1bb5608244deafb91aac54402e32c3b37c1bb7261aa89e28cdca91c061)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47d7a27409216a3620f3f261c4daab0d27ddd71ebc21968c8e8707682ca958a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionInstallationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class DeveloperConnectConnectionInstallationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeveloperConnectConnectionInstallationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionInstallationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionInstallationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1329087f4f9ebafd278e68e077b166326386b4a535f22dcec039458a162c81aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DeveloperConnectConnectionInstallationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__080c5fa579dabb44444410b531b0a6a6ba31bfef4eac6c1bfbe6249c19cce55a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DeveloperConnectConnectionInstallationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea43629b7b0b9b22c7ba4a5a6ecab6e527c2ee8a797e1a24ba2e99f439bdfb4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53ea89471d9c5948617383f735f25d1a4bbb19083f941a13e7837769e6cc01dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dcaec87ff7159c27445dd05d3ea7cca2850258d4c27415fcda252244402dc45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DeveloperConnectConnectionInstallationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionInstallationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1283477adfdef6cf70013758c7a2707ee9fe91f7c1ef8b7b2856434bfa87e89)
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
    ) -> typing.Optional[DeveloperConnectConnectionInstallationState]:
        return typing.cast(typing.Optional[DeveloperConnectConnectionInstallationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeveloperConnectConnectionInstallationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c7a10d1f00baad04e691ef2f2d4c861dd7d459afbf2afefb1a759efe85309c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DeveloperConnectConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#create DeveloperConnectConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#delete DeveloperConnectConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#update DeveloperConnectConnection#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d33d1bf1f3b9cd1475ba2a23db2337da1d7db69416963c74339f87a41b9d1a0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#create DeveloperConnectConnection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#delete DeveloperConnectConnection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/developer_connect_connection#update DeveloperConnectConnection#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeveloperConnectConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeveloperConnectConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.developerConnectConnection.DeveloperConnectConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4de8efb3be8a23de9ab5226d50406fe2494748acede7855370afcbec214eb0e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5169e9a4cdcf33a334b1d044df66a6f21a7fba566881052739e94213d81a5be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9396650952545563f93eeca3f3e54f6862742cc0809f772cd18be3add98e12c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d3340643134cec52d210f800cee3f93c3394cc600ddd0a4e986fd1cc92f1352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DeveloperConnectConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DeveloperConnectConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DeveloperConnectConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e56cd6584d3353472db80e8d36683dc1c07413be204506f1cb66a2c1a1ce698d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DeveloperConnectConnection",
    "DeveloperConnectConnectionBitbucketCloudConfig",
    "DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential",
    "DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredentialOutputReference",
    "DeveloperConnectConnectionBitbucketCloudConfigOutputReference",
    "DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential",
    "DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredentialOutputReference",
    "DeveloperConnectConnectionBitbucketDataCenterConfig",
    "DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential",
    "DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredentialOutputReference",
    "DeveloperConnectConnectionBitbucketDataCenterConfigOutputReference",
    "DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential",
    "DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredentialOutputReference",
    "DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig",
    "DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfigOutputReference",
    "DeveloperConnectConnectionConfig",
    "DeveloperConnectConnectionCryptoKeyConfig",
    "DeveloperConnectConnectionCryptoKeyConfigOutputReference",
    "DeveloperConnectConnectionGithubConfig",
    "DeveloperConnectConnectionGithubConfigAuthorizerCredential",
    "DeveloperConnectConnectionGithubConfigAuthorizerCredentialOutputReference",
    "DeveloperConnectConnectionGithubConfigOutputReference",
    "DeveloperConnectConnectionGithubEnterpriseConfig",
    "DeveloperConnectConnectionGithubEnterpriseConfigOutputReference",
    "DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig",
    "DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfigOutputReference",
    "DeveloperConnectConnectionGitlabConfig",
    "DeveloperConnectConnectionGitlabConfigAuthorizerCredential",
    "DeveloperConnectConnectionGitlabConfigAuthorizerCredentialOutputReference",
    "DeveloperConnectConnectionGitlabConfigOutputReference",
    "DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential",
    "DeveloperConnectConnectionGitlabConfigReadAuthorizerCredentialOutputReference",
    "DeveloperConnectConnectionGitlabEnterpriseConfig",
    "DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential",
    "DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredentialOutputReference",
    "DeveloperConnectConnectionGitlabEnterpriseConfigOutputReference",
    "DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential",
    "DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredentialOutputReference",
    "DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig",
    "DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfigOutputReference",
    "DeveloperConnectConnectionInstallationState",
    "DeveloperConnectConnectionInstallationStateList",
    "DeveloperConnectConnectionInstallationStateOutputReference",
    "DeveloperConnectConnectionTimeouts",
    "DeveloperConnectConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__df5f7c849e226382d29b1b843e7d2cd11820eda3e477fa8c7620f830fbdcecce(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    connection_id: builtins.str,
    location: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bitbucket_cloud_config: typing.Optional[typing.Union[DeveloperConnectConnectionBitbucketCloudConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bitbucket_data_center_config: typing.Optional[typing.Union[DeveloperConnectConnectionBitbucketDataCenterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    crypto_key_config: typing.Optional[typing.Union[DeveloperConnectConnectionCryptoKeyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    etag: typing.Optional[builtins.str] = None,
    github_config: typing.Optional[typing.Union[DeveloperConnectConnectionGithubConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    github_enterprise_config: typing.Optional[typing.Union[DeveloperConnectConnectionGithubEnterpriseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gitlab_config: typing.Optional[typing.Union[DeveloperConnectConnectionGitlabConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gitlab_enterprise_config: typing.Optional[typing.Union[DeveloperConnectConnectionGitlabEnterpriseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DeveloperConnectConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9092c814bc0a10a9ef3377908122c58f279135323e39c22f8a0ae2a2ac9090f1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c39f91af8ad2c207e75c1de1746d0a9671610b91853c4af3abe942656adadf(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ed325842b3aafa7df12258113a78ad323bc2e1fdca9c52d7d3b59463056d11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb601dead08c5231ddfb31772e61392459124041663a04fdd80322a1fc004eb0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3f59d638720f6f8425b75711296e1c4ebe4cec2bb01c499c0aa64fdc9a5bf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2d8b7f47548661a7bf517f82512933e7ff382914e3f402f9be363f210cd678(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55efd47c6672b55c0cd4b099254aaa69f6e6768420e7b258351ea862310f1454(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36762e0e24fb0de2d3af85ab551b54e94b401b9ccbc62ae73579a3c60b05d9c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6aaa9d403ed34fe5395b556c8e8347d588523a4d659b6c51abd83877c36eba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e087b6f89575451fdef2b1d290160045fceedb773c8839ac0c146b96b6a15a(
    *,
    authorizer_credential: typing.Union[DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    read_authorizer_credential: typing.Union[DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    webhook_secret_secret_version: builtins.str,
    workspace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcdfd51330728864840339013d6a8950dfd25129a206e29a662faf9ad8e0d2e7(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4edc2e9ffa25975258e69b9613e3d2ba0572762b378c42b09e50e45263b3e273(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c4ae16f817125edb7e5956bffb39eae4c6635c8bf65e40a918b31efb69eda9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde1051a82f13b4ffc531b176eaaf6b410fc0f2da43889188c3243649a2d7791(
    value: typing.Optional[DeveloperConnectConnectionBitbucketCloudConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce74a69d88d740009bf3a09b95db7d62939c103102e5bbda87da6405e0431e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93057caa9d69b7d95f3a763c72cec778d9a41c60696894666ca98c8c4810557(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c9fcfd06fd2ac9c10541121874321454963012671c3cf1c7ed29d77a154af3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f212d90fc6860b6d9efee9d4e29fb24e0fe4c12a98442d1d64116cd7899e47(
    value: typing.Optional[DeveloperConnectConnectionBitbucketCloudConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49436b5f0456064837b142664630b0d864c5b2683ff41cf600c4edd3cd0759c(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a5a70f14f731ac0637365abe18c5694051e00aafe1f1efb47889be8241f3e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2db4fd71461328dbcbbe83093cd8618236fcf1021d3debfb01853585f7b926(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9972adb1d8c28d695082da85e8afaa14f7306fa7fc2d98ac74acb89893cfba(
    value: typing.Optional[DeveloperConnectConnectionBitbucketCloudConfigReadAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6138039f66db7c5a1445f64936d757ecfbf7ce7ec69a36b162dc3939f164704(
    *,
    authorizer_credential: typing.Union[DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    host_uri: builtins.str,
    read_authorizer_credential: typing.Union[DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    webhook_secret_secret_version: builtins.str,
    service_directory_config: typing.Optional[typing.Union[DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_ca_certificate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a603600345b15d889e3353a36940c7cab743d7dca01a9555f1864d42bfb9cb5(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a06d55c3f5549f093cc77c60dfe9b39379ce5c39d508b83494d5232a19f60b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668c4bc11d8d68e58aa3e99fc63f59b9c59da48793eba60cd879ad57652891d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22056d9e5b8e9dc66a7ed9caa89fcfd1291b78863e7f30b6356dbf7eabd31c11(
    value: typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f043487ef8a4303fb4bb652787d82fce29955a2b2c43b46e258bab3626b391a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab122fc2755b96e75b037d9c1c4ea726fc9d966e4fbb461f4b3df6554679b1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bacee05d30c2b80c54d94b2bd6e70a4e9925a125805e243204b3c94a542adf3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31267240419529b2a5d13a013f8c56cf7be3dd5126c61bddd29db984d4f53bc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837e47937a03a735535e54006b765e8fe9e2724e6b7bdc0a6c7d63a382cf79bb(
    value: typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34306204031fbf6ccfd2a91c8fab61a8951691561807fbcada866d30f65e7175(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3263b225171c8969bf3b977621450d30550fa7621431664b0e41ab4e1da29150(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7684c4dfb9d932aa499097ab3447f41d22a61f4bcb5198fa34945ece6e46a9db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016e759a3d570bf6acdfabd8f212c168c20a3d42b8349729a16fe46dfd5017da(
    value: typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfigReadAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8bcb1836923d65792df11fd2b60968de006bae3fc0ffce2a74a598bbc3d3ac(
    *,
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2646778169c03fa9450468d471e197cfe7bd0f31f3ccc5d6e9de2d901c0445e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ec0a3ac1066e9f3306f82902dcbaeabc7e45f376740fec29f2036be98c1c4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d7e9d2bbcbe8a504295a46a7927c1138bfdf4b64c316876fe9306514e7c469(
    value: typing.Optional[DeveloperConnectConnectionBitbucketDataCenterConfigServiceDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc4944cb0b9799a6e96ded50817370b6b2b1d50e564c4b66838f400c3718533(
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
    bitbucket_cloud_config: typing.Optional[typing.Union[DeveloperConnectConnectionBitbucketCloudConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bitbucket_data_center_config: typing.Optional[typing.Union[DeveloperConnectConnectionBitbucketDataCenterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    crypto_key_config: typing.Optional[typing.Union[DeveloperConnectConnectionCryptoKeyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    etag: typing.Optional[builtins.str] = None,
    github_config: typing.Optional[typing.Union[DeveloperConnectConnectionGithubConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    github_enterprise_config: typing.Optional[typing.Union[DeveloperConnectConnectionGithubEnterpriseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gitlab_config: typing.Optional[typing.Union[DeveloperConnectConnectionGitlabConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gitlab_enterprise_config: typing.Optional[typing.Union[DeveloperConnectConnectionGitlabEnterpriseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DeveloperConnectConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd043c71f3920c80935370b7d4edbe7317c6e28c25afa603e412a4c694ea424(
    *,
    key_reference: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7151c358a6ba2ba1d58edc3dc28cc02d9f0c200b952809ae87d49f59f3c9e9c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e802136bb02af16b19c2204c88d6cb6ba053213d94acc6eec1d78f5fb18c605f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c185d85abc6df5f016399869eb3e0e2905aea96671be851d3a96e9b5ccdf9529(
    value: typing.Optional[DeveloperConnectConnectionCryptoKeyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e47510a7d75a1275b5ced081cac1613f37b194a752269cce90afc384735739(
    *,
    github_app: builtins.str,
    app_installation_id: typing.Optional[builtins.str] = None,
    authorizer_credential: typing.Optional[typing.Union[DeveloperConnectConnectionGithubConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b35f4095d7f0bf91eec57da4deeb0b52cae3b8e615ac782df878f6be9ded4c6(
    *,
    oauth_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbcbb2ca3318b1ac114136e0991d002b6f5b66c47f6c0caff667c041c291ba60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26cab7f30a80045003622f94b72c341c1a088feab1d88564032a3e6ec3ae574c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5f10d88c270de0cdb8b3b1475a0b4ed0cad8b5b2794c8645c4d24761fcd8ae(
    value: typing.Optional[DeveloperConnectConnectionGithubConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3320adebc70b773f11a12fb768ae3e5858ba2d884901321dc8cc3d477a36fb62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34de131aca48787c75f3d9edf6e3f8a869adae73f24a09d1a642e3c39b3ab4c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a3981d497fbfdffe20e74a2a9a006fd9279a51148b2249e9a4b56268c6bce3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4458961ed29fa8a248752eedd2c632d2913562e97a20144932112696a721966(
    value: typing.Optional[DeveloperConnectConnectionGithubConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b6f5f929aff03e75052965ab095c5968016807d1c847182d73047227b3cb2c(
    *,
    host_uri: builtins.str,
    app_id: typing.Optional[builtins.str] = None,
    app_installation_id: typing.Optional[builtins.str] = None,
    private_key_secret_version: typing.Optional[builtins.str] = None,
    service_directory_config: typing.Optional[typing.Union[DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_ca_certificate: typing.Optional[builtins.str] = None,
    webhook_secret_secret_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedf431d028cf6d551e7e4cfdf27bf85714160e1f4313dbc8e44c1ed055ddd6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981afc9afdcd5c1bdba2003a3ab2a8f70e0e43fcad2509c49665936672627ca4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5099c5d3e43c727c535e4a05eb0f4521fc85699425f1395a8ef4d516c7544f41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65880c4ab222a4b79727f8e17b1bf06423a165f455454fde71e216327821a9aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89fa07f95795bcaea72d09d75ea7b45fd39f0db6514531253048f1b18b9688e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4296e19a17a7924c23c2204b7569be5f3a1b6baa1be6be249003e1f884c4b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef6dc7f69f56e0d227d113abc0cf11592f0e76fbb49397f7a1bbd768f8c7766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d7be3f6ddc8cda204df6cc96dce681a582835b2844bd647bf11b639be51f8c(
    value: typing.Optional[DeveloperConnectConnectionGithubEnterpriseConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdcc5fbd5c68abde04f469e08be68c41d3ee8b77cae8e10c0582c804d10ec1c0(
    *,
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b798649703d0d2171930757de6d64a7e8b2f78c5a1976fcee2e739a7c19096(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0732346470e83db13fe155b6337820d868e0746361e24c69062bffcd58ed5611(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4640cdccfe40c65a9ef1c2abd2226a66675a1c4d0fb12964b8b1d576a71c74(
    value: typing.Optional[DeveloperConnectConnectionGithubEnterpriseConfigServiceDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d71d0dcee3e119858e57d7f1b38f77eabab8f189ac34e4be5d5716b50673edac(
    *,
    authorizer_credential: typing.Union[DeveloperConnectConnectionGitlabConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    read_authorizer_credential: typing.Union[DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    webhook_secret_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4cfbf1f205c1ce9a5cdc481dfcfed76495e011a41fb810f5911346c79617a22(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df96e76bbd6f7a46af11921c311d9c2ae91d2bc9bfa16b85b3727623e963b6c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf1e1b78fda5487a6b8ef0649bdd5556de21b140627f467764d10eec04303fae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8be2fcfb14e18de38bfe97098e1a4b19532597d12ad646c8ba772c2a05ceb4(
    value: typing.Optional[DeveloperConnectConnectionGitlabConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e0d7d47c784391218144e5b0e0f06303f9ccb923432da2a78d70ae7b0a1afe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acdae9c50867f37aa4d09b45929cd1d73bb6574b6afcca1ab773334675ae601c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d833a45c6854b9f9ac36f02e0f93675b1e5ff2987f2cc357d5a4c894bf525712(
    value: typing.Optional[DeveloperConnectConnectionGitlabConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b13c3272511f81508579bf34dd8b5174a29f7130210bfff134c6c281c13d15(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fac92a87d42a52c6dfbd13413133d6c16dac68079b7c3c304d9e07d70d1ced(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45301e90895000ecaa0c20f09044f67298b7936fd0da9593d46c163f84f53ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3f5be430940ee09f5bc90a122e6edde28dd50749eab179408ca29e4814551f(
    value: typing.Optional[DeveloperConnectConnectionGitlabConfigReadAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34804edb3f9b1a12c384d9752d82e6dc97810a1ed46dd50263fb474ee972d04f(
    *,
    authorizer_credential: typing.Union[DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    host_uri: builtins.str,
    read_authorizer_credential: typing.Union[DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential, typing.Dict[builtins.str, typing.Any]],
    webhook_secret_secret_version: builtins.str,
    service_directory_config: typing.Optional[typing.Union[DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_ca_certificate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38a276f4391993b3d67217fcce2108059cd138e1bb3ff9fa895a3c4b7ce5b85(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1647efb0c657d9f092eaf8a37337c3f2af5703c41387453be08e94b481179c07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf3165439903fd07b011a75cc0d558a6aabc842eb3bd1fe603572adfb89046b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16cf2193390c05f3326797967890f9969d1717017ce45a75559e0a8621113a8(
    value: typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfigAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dccc7d047947c6ffa047b4ad506c4d4a6f591712076719c13447df98a72d67e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55bd3bca07a2d04082b0eff0a4e6fb970e732e0dc518fd67d2acdc82591106d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7f6e589c9c13bd5e9220755eb6bc8c11a728d55c128027b63dc95ae5cf8e04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1324d3a1ecad74e5e1c9106eb8e80ce60f8e4a96f2c0ca5221414f09669a51b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__869b1a6314a7c42a6b9e87e77c5974aa54eb93d09706ff609eab193a22ebb86f(
    value: typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3559ba8cba72c54de84969fbefb68855c716dd68ae9e39819f889b7f7db47f14(
    *,
    user_token_secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e8f5ba182847acbe7f1bbd0651b368e15860e66cd078237840b2800ddb47ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3d78f96f2e1e4e47c7e8310ee4bdab2478d405f3c5ed406aa6ca9eb73a9346(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b106675e973c2b82faead5cd303fcc26f38a40e2360b92d73afb5eb5412e06f(
    value: typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfigReadAuthorizerCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__986e224616be57c0a008bf9c48282a4c61539fb97aa27b8e3d554fd4539c3818(
    *,
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8af218d7962fe9a299e09bded262b52b7a1812a409c5b5631aa08fbab562ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b653e1bb5608244deafb91aac54402e32c3b37c1bb7261aa89e28cdca91c061(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47d7a27409216a3620f3f261c4daab0d27ddd71ebc21968c8e8707682ca958a(
    value: typing.Optional[DeveloperConnectConnectionGitlabEnterpriseConfigServiceDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1329087f4f9ebafd278e68e077b166326386b4a535f22dcec039458a162c81aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080c5fa579dabb44444410b531b0a6a6ba31bfef4eac6c1bfbe6249c19cce55a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea43629b7b0b9b22c7ba4a5a6ecab6e527c2ee8a797e1a24ba2e99f439bdfb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ea89471d9c5948617383f735f25d1a4bbb19083f941a13e7837769e6cc01dd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dcaec87ff7159c27445dd05d3ea7cca2850258d4c27415fcda252244402dc45(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1283477adfdef6cf70013758c7a2707ee9fe91f7c1ef8b7b2856434bfa87e89(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c7a10d1f00baad04e691ef2f2d4c861dd7d459afbf2afefb1a759efe85309c(
    value: typing.Optional[DeveloperConnectConnectionInstallationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d33d1bf1f3b9cd1475ba2a23db2337da1d7db69416963c74339f87a41b9d1a0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de8efb3be8a23de9ab5226d50406fe2494748acede7855370afcbec214eb0e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5169e9a4cdcf33a334b1d044df66a6f21a7fba566881052739e94213d81a5be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9396650952545563f93eeca3f3e54f6862742cc0809f772cd18be3add98e12c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d3340643134cec52d210f800cee3f93c3394cc600ddd0a4e986fd1cc92f1352(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e56cd6584d3353472db80e8d36683dc1c07413be204506f1cb66a2c1a1ce698d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DeveloperConnectConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

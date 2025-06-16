r'''
# `google_cloudbuild_bitbucket_server_config`

Refer to the Terraform Registry for docs: [`google_cloudbuild_bitbucket_server_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config).
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


class GoogleCloudbuildBitbucketServerConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildBitbucketServerConfig.GoogleCloudbuildBitbucketServerConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config google_cloudbuild_bitbucket_server_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        api_key: builtins.str,
        config_id: builtins.str,
        host_uri: builtins.str,
        location: builtins.str,
        secrets: typing.Union["GoogleCloudbuildBitbucketServerConfigSecrets", typing.Dict[builtins.str, typing.Any]],
        username: builtins.str,
        connected_repositories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildBitbucketServerConfigConnectedRepositories", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        peered_network: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudbuildBitbucketServerConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config google_cloudbuild_bitbucket_server_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_key: Immutable. API Key that will be attached to webhook. Once this field has been set, it cannot be changed. Changing this field will result in deleting/ recreating the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#api_key GoogleCloudbuildBitbucketServerConfig#api_key}
        :param config_id: The ID to use for the BitbucketServerConfig, which will become the final component of the BitbucketServerConfig's resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#config_id GoogleCloudbuildBitbucketServerConfig#config_id}
        :param host_uri: Immutable. The URI of the Bitbucket Server host. Once this field has been set, it cannot be changed. If you need to change it, please create another BitbucketServerConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#host_uri GoogleCloudbuildBitbucketServerConfig#host_uri}
        :param location: The location of this bitbucket server config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#location GoogleCloudbuildBitbucketServerConfig#location}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#secrets GoogleCloudbuildBitbucketServerConfig#secrets}
        :param username: Username of the account Cloud Build will use on Bitbucket Server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#username GoogleCloudbuildBitbucketServerConfig#username}
        :param connected_repositories: connected_repositories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#connected_repositories GoogleCloudbuildBitbucketServerConfig#connected_repositories}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#id GoogleCloudbuildBitbucketServerConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param peered_network: The network to be used when reaching out to the Bitbucket Server instance. The VPC network must be enabled for private service connection. This should be set if the Bitbucket Server instance is hosted on-premises and not reachable by public internet. If this field is left empty, no network peering will occur and calls to the Bitbucket Server instance will be made over the public internet. Must be in the format projects/{project}/global/networks/{network}, where {project} is a project number or id and {network} is the name of a VPC network in the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#peered_network GoogleCloudbuildBitbucketServerConfig#peered_network}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#project GoogleCloudbuildBitbucketServerConfig#project}.
        :param ssl_ca: SSL certificate to use for requests to Bitbucket Server. The format should be PEM format but the extension can be one of .pem, .cer, or .crt. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#ssl_ca GoogleCloudbuildBitbucketServerConfig#ssl_ca}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#timeouts GoogleCloudbuildBitbucketServerConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__387cb9bf9b6d432beee83052b718b8380309b49b5bb2d1f981203e3d2d51f52f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleCloudbuildBitbucketServerConfigConfig(
            api_key=api_key,
            config_id=config_id,
            host_uri=host_uri,
            location=location,
            secrets=secrets,
            username=username,
            connected_repositories=connected_repositories,
            id=id,
            peered_network=peered_network,
            project=project,
            ssl_ca=ssl_ca,
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
        '''Generates CDKTF code for importing a GoogleCloudbuildBitbucketServerConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleCloudbuildBitbucketServerConfig to import.
        :param import_from_id: The id of the existing GoogleCloudbuildBitbucketServerConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleCloudbuildBitbucketServerConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef4b639ff0941beeb3f941edae771978c43f3e3ddb5ee7c320d79d200bb7794c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConnectedRepositories")
    def put_connected_repositories(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildBitbucketServerConfigConnectedRepositories", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2473c134ccfea39095dcf82ecbd774988695e4ff2ad99f3a2c668a7319abfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConnectedRepositories", [value]))

    @jsii.member(jsii_name="putSecrets")
    def put_secrets(
        self,
        *,
        admin_access_token_version_name: builtins.str,
        read_access_token_version_name: builtins.str,
        webhook_secret_version_name: builtins.str,
    ) -> None:
        '''
        :param admin_access_token_version_name: The resource name for the admin access token's secret version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#admin_access_token_version_name GoogleCloudbuildBitbucketServerConfig#admin_access_token_version_name}
        :param read_access_token_version_name: The resource name for the read access token's secret version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#read_access_token_version_name GoogleCloudbuildBitbucketServerConfig#read_access_token_version_name}
        :param webhook_secret_version_name: Immutable. The resource name for the webhook secret's secret version. Once this field has been set, it cannot be changed. Changing this field will result in deleting/ recreating the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#webhook_secret_version_name GoogleCloudbuildBitbucketServerConfig#webhook_secret_version_name}
        '''
        value = GoogleCloudbuildBitbucketServerConfigSecrets(
            admin_access_token_version_name=admin_access_token_version_name,
            read_access_token_version_name=read_access_token_version_name,
            webhook_secret_version_name=webhook_secret_version_name,
        )

        return typing.cast(None, jsii.invoke(self, "putSecrets", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#create GoogleCloudbuildBitbucketServerConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#delete GoogleCloudbuildBitbucketServerConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#update GoogleCloudbuildBitbucketServerConfig#update}.
        '''
        value = GoogleCloudbuildBitbucketServerConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetConnectedRepositories")
    def reset_connected_repositories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectedRepositories", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPeeredNetwork")
    def reset_peered_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeeredNetwork", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSslCa")
    def reset_ssl_ca(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCa", []))

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
    @jsii.member(jsii_name="connectedRepositories")
    def connected_repositories(
        self,
    ) -> "GoogleCloudbuildBitbucketServerConfigConnectedRepositoriesList":
        return typing.cast("GoogleCloudbuildBitbucketServerConfigConnectedRepositoriesList", jsii.get(self, "connectedRepositories"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> "GoogleCloudbuildBitbucketServerConfigSecretsOutputReference":
        return typing.cast("GoogleCloudbuildBitbucketServerConfigSecretsOutputReference", jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleCloudbuildBitbucketServerConfigTimeoutsOutputReference":
        return typing.cast("GoogleCloudbuildBitbucketServerConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="webhookKey")
    def webhook_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookKey"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="configIdInput")
    def config_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configIdInput"))

    @builtins.property
    @jsii.member(jsii_name="connectedRepositoriesInput")
    def connected_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildBitbucketServerConfigConnectedRepositories"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildBitbucketServerConfigConnectedRepositories"]]], jsii.get(self, "connectedRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="hostUriInput")
    def host_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostUriInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="peeredNetworkInput")
    def peered_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peeredNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="secretsInput")
    def secrets_input(
        self,
    ) -> typing.Optional["GoogleCloudbuildBitbucketServerConfigSecrets"]:
        return typing.cast(typing.Optional["GoogleCloudbuildBitbucketServerConfigSecrets"], jsii.get(self, "secretsInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCaInput")
    def ssl_ca_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCaInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudbuildBitbucketServerConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudbuildBitbucketServerConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65c5416997154b434ebb7dcf74885a46def328772d35c44dfb808aed2e9cc77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configId")
    def config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configId"))

    @config_id.setter
    def config_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8fec931b7a8e4bd0ebb85cbc017927fb06b5ce7aff2318a495a5b4861b08cd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostUri")
    def host_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostUri"))

    @host_uri.setter
    def host_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__251c346d45578b5a38733404f3d961e9f91a0c14ee2070f658f5545f06c234b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d6143c244e8f4cb3ce6bf8aa885374b05cd449b281807d738dd65ea8d95b73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553a51308f4c5e776c6ff50fd56994f2444883f34da61611893530261cef31c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peeredNetwork")
    def peered_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peeredNetwork"))

    @peered_network.setter
    def peered_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d2cd59e5eb56345b5248645c81a1dccaef5ec60c2b4fa93995ec31ba85de7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peeredNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417af527aba9db53907e0e6812a57994c716dc19bfae4173f0b620de4be1aa5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCa")
    def ssl_ca(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCa"))

    @ssl_ca.setter
    def ssl_ca(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11816457717d7cdeb929b320bfb6a320262627010f316eb53d3aa15d32058e92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b5eb208d9ffd0bfa0096c8ececa213b0086d3893eb00179c21f2803da1b2580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildBitbucketServerConfig.GoogleCloudbuildBitbucketServerConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "api_key": "apiKey",
        "config_id": "configId",
        "host_uri": "hostUri",
        "location": "location",
        "secrets": "secrets",
        "username": "username",
        "connected_repositories": "connectedRepositories",
        "id": "id",
        "peered_network": "peeredNetwork",
        "project": "project",
        "ssl_ca": "sslCa",
        "timeouts": "timeouts",
    },
)
class GoogleCloudbuildBitbucketServerConfigConfig(
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
        api_key: builtins.str,
        config_id: builtins.str,
        host_uri: builtins.str,
        location: builtins.str,
        secrets: typing.Union["GoogleCloudbuildBitbucketServerConfigSecrets", typing.Dict[builtins.str, typing.Any]],
        username: builtins.str,
        connected_repositories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudbuildBitbucketServerConfigConnectedRepositories", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        peered_network: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudbuildBitbucketServerConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_key: Immutable. API Key that will be attached to webhook. Once this field has been set, it cannot be changed. Changing this field will result in deleting/ recreating the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#api_key GoogleCloudbuildBitbucketServerConfig#api_key}
        :param config_id: The ID to use for the BitbucketServerConfig, which will become the final component of the BitbucketServerConfig's resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#config_id GoogleCloudbuildBitbucketServerConfig#config_id}
        :param host_uri: Immutable. The URI of the Bitbucket Server host. Once this field has been set, it cannot be changed. If you need to change it, please create another BitbucketServerConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#host_uri GoogleCloudbuildBitbucketServerConfig#host_uri}
        :param location: The location of this bitbucket server config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#location GoogleCloudbuildBitbucketServerConfig#location}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#secrets GoogleCloudbuildBitbucketServerConfig#secrets}
        :param username: Username of the account Cloud Build will use on Bitbucket Server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#username GoogleCloudbuildBitbucketServerConfig#username}
        :param connected_repositories: connected_repositories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#connected_repositories GoogleCloudbuildBitbucketServerConfig#connected_repositories}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#id GoogleCloudbuildBitbucketServerConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param peered_network: The network to be used when reaching out to the Bitbucket Server instance. The VPC network must be enabled for private service connection. This should be set if the Bitbucket Server instance is hosted on-premises and not reachable by public internet. If this field is left empty, no network peering will occur and calls to the Bitbucket Server instance will be made over the public internet. Must be in the format projects/{project}/global/networks/{network}, where {project} is a project number or id and {network} is the name of a VPC network in the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#peered_network GoogleCloudbuildBitbucketServerConfig#peered_network}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#project GoogleCloudbuildBitbucketServerConfig#project}.
        :param ssl_ca: SSL certificate to use for requests to Bitbucket Server. The format should be PEM format but the extension can be one of .pem, .cer, or .crt. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#ssl_ca GoogleCloudbuildBitbucketServerConfig#ssl_ca}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#timeouts GoogleCloudbuildBitbucketServerConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(secrets, dict):
            secrets = GoogleCloudbuildBitbucketServerConfigSecrets(**secrets)
        if isinstance(timeouts, dict):
            timeouts = GoogleCloudbuildBitbucketServerConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d509126af01f1e5d7ffd309734d504cd905bf220a417c31387b47b49ad65056f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument config_id", value=config_id, expected_type=type_hints["config_id"])
            check_type(argname="argument host_uri", value=host_uri, expected_type=type_hints["host_uri"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument connected_repositories", value=connected_repositories, expected_type=type_hints["connected_repositories"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument peered_network", value=peered_network, expected_type=type_hints["peered_network"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument ssl_ca", value=ssl_ca, expected_type=type_hints["ssl_ca"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
            "config_id": config_id,
            "host_uri": host_uri,
            "location": location,
            "secrets": secrets,
            "username": username,
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
        if connected_repositories is not None:
            self._values["connected_repositories"] = connected_repositories
        if id is not None:
            self._values["id"] = id
        if peered_network is not None:
            self._values["peered_network"] = peered_network
        if project is not None:
            self._values["project"] = project
        if ssl_ca is not None:
            self._values["ssl_ca"] = ssl_ca
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
    def api_key(self) -> builtins.str:
        '''Immutable.

        API Key that will be attached to webhook. Once this field has been set, it cannot be changed.
        Changing this field will result in deleting/ recreating the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#api_key GoogleCloudbuildBitbucketServerConfig#api_key}
        '''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config_id(self) -> builtins.str:
        '''The ID to use for the BitbucketServerConfig, which will become the final component of the BitbucketServerConfig's resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#config_id GoogleCloudbuildBitbucketServerConfig#config_id}
        '''
        result = self._values.get("config_id")
        assert result is not None, "Required property 'config_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_uri(self) -> builtins.str:
        '''Immutable.

        The URI of the Bitbucket Server host. Once this field has been set, it cannot be changed.
        If you need to change it, please create another BitbucketServerConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#host_uri GoogleCloudbuildBitbucketServerConfig#host_uri}
        '''
        result = self._values.get("host_uri")
        assert result is not None, "Required property 'host_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of this bitbucket server config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#location GoogleCloudbuildBitbucketServerConfig#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secrets(self) -> "GoogleCloudbuildBitbucketServerConfigSecrets":
        '''secrets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#secrets GoogleCloudbuildBitbucketServerConfig#secrets}
        '''
        result = self._values.get("secrets")
        assert result is not None, "Required property 'secrets' is missing"
        return typing.cast("GoogleCloudbuildBitbucketServerConfigSecrets", result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username of the account Cloud Build will use on Bitbucket Server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#username GoogleCloudbuildBitbucketServerConfig#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connected_repositories(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildBitbucketServerConfigConnectedRepositories"]]]:
        '''connected_repositories block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#connected_repositories GoogleCloudbuildBitbucketServerConfig#connected_repositories}
        '''
        result = self._values.get("connected_repositories")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudbuildBitbucketServerConfigConnectedRepositories"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#id GoogleCloudbuildBitbucketServerConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peered_network(self) -> typing.Optional[builtins.str]:
        '''The network to be used when reaching out to the Bitbucket Server instance.

        The VPC network must be enabled for private service connection.
        This should be set if the Bitbucket Server instance is hosted on-premises and not reachable by public internet. If this field is left empty,
        no network peering will occur and calls to the Bitbucket Server instance will be made over the public internet. Must be in the format
        projects/{project}/global/networks/{network}, where {project} is a project number or id and {network} is the name of a VPC network in the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#peered_network GoogleCloudbuildBitbucketServerConfig#peered_network}
        '''
        result = self._values.get("peered_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#project GoogleCloudbuildBitbucketServerConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_ca(self) -> typing.Optional[builtins.str]:
        '''SSL certificate to use for requests to Bitbucket Server.

        The format should be PEM format but the extension can be one of .pem, .cer, or .crt.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#ssl_ca GoogleCloudbuildBitbucketServerConfig#ssl_ca}
        '''
        result = self._values.get("ssl_ca")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleCloudbuildBitbucketServerConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#timeouts GoogleCloudbuildBitbucketServerConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleCloudbuildBitbucketServerConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildBitbucketServerConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildBitbucketServerConfig.GoogleCloudbuildBitbucketServerConfigConnectedRepositories",
    jsii_struct_bases=[],
    name_mapping={"project_key": "projectKey", "repo_slug": "repoSlug"},
)
class GoogleCloudbuildBitbucketServerConfigConnectedRepositories:
    def __init__(self, *, project_key: builtins.str, repo_slug: builtins.str) -> None:
        '''
        :param project_key: Identifier for the project storing the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#project_key GoogleCloudbuildBitbucketServerConfig#project_key}
        :param repo_slug: Identifier for the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#repo_slug GoogleCloudbuildBitbucketServerConfig#repo_slug}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__698558ef3351f88cd6a7ea995fdf035f7d93147f24a5e27e9ea90a402ffe38c1)
            check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            check_type(argname="argument repo_slug", value=repo_slug, expected_type=type_hints["repo_slug"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_key": project_key,
            "repo_slug": repo_slug,
        }

    @builtins.property
    def project_key(self) -> builtins.str:
        '''Identifier for the project storing the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#project_key GoogleCloudbuildBitbucketServerConfig#project_key}
        '''
        result = self._values.get("project_key")
        assert result is not None, "Required property 'project_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo_slug(self) -> builtins.str:
        '''Identifier for the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#repo_slug GoogleCloudbuildBitbucketServerConfig#repo_slug}
        '''
        result = self._values.get("repo_slug")
        assert result is not None, "Required property 'repo_slug' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildBitbucketServerConfigConnectedRepositories(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildBitbucketServerConfigConnectedRepositoriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildBitbucketServerConfig.GoogleCloudbuildBitbucketServerConfigConnectedRepositoriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79dd38bbde7975f60c46863826d518f2ac3b61e7db37229ea27381afd2d70562)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudbuildBitbucketServerConfigConnectedRepositoriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__096d947cb27c5ffbf22649c9e098b7d908b59179ff8fe9981eeb277dd99e882b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudbuildBitbucketServerConfigConnectedRepositoriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eed77ed6c90bb9945ad257d4a181e19eeef78c702ad2f8bfdf401ff796c49cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d62b44a5ba9c1dfa8b7169820d71a43e26f1b80b0037d83d8e977814f619650f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8c35dbdbd931faffb2368ba2aeee8d78a55fdc97965b806b90267edb496bfc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildBitbucketServerConfigConnectedRepositories]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildBitbucketServerConfigConnectedRepositories]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildBitbucketServerConfigConnectedRepositories]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c241c5e0118a53bae0eed2223fcc84ff2b44ea5c5b5b1523375fd02693c98f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudbuildBitbucketServerConfigConnectedRepositoriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildBitbucketServerConfig.GoogleCloudbuildBitbucketServerConfigConnectedRepositoriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d56515cb56ba240332e4a5121d29f3eeb6811a238147fc57f94804de58d7150)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="projectKeyInput")
    def project_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="repoSlugInput")
    def repo_slug_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repoSlugInput"))

    @builtins.property
    @jsii.member(jsii_name="projectKey")
    def project_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectKey"))

    @project_key.setter
    def project_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33536273ba61c965cf14185a415729c30f9637d1f9a2a16026001eae7b56cf30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoSlug")
    def repo_slug(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoSlug"))

    @repo_slug.setter
    def repo_slug(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f4177c64c99ca351f5b2b355afdd610b572c00ede3fb1dd8125d9a31145f97d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoSlug", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildBitbucketServerConfigConnectedRepositories]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildBitbucketServerConfigConnectedRepositories]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildBitbucketServerConfigConnectedRepositories]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05e063f86186c6b104d4bb813fc307764378ae80adbef4122294ccfd146c9b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildBitbucketServerConfig.GoogleCloudbuildBitbucketServerConfigSecrets",
    jsii_struct_bases=[],
    name_mapping={
        "admin_access_token_version_name": "adminAccessTokenVersionName",
        "read_access_token_version_name": "readAccessTokenVersionName",
        "webhook_secret_version_name": "webhookSecretVersionName",
    },
)
class GoogleCloudbuildBitbucketServerConfigSecrets:
    def __init__(
        self,
        *,
        admin_access_token_version_name: builtins.str,
        read_access_token_version_name: builtins.str,
        webhook_secret_version_name: builtins.str,
    ) -> None:
        '''
        :param admin_access_token_version_name: The resource name for the admin access token's secret version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#admin_access_token_version_name GoogleCloudbuildBitbucketServerConfig#admin_access_token_version_name}
        :param read_access_token_version_name: The resource name for the read access token's secret version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#read_access_token_version_name GoogleCloudbuildBitbucketServerConfig#read_access_token_version_name}
        :param webhook_secret_version_name: Immutable. The resource name for the webhook secret's secret version. Once this field has been set, it cannot be changed. Changing this field will result in deleting/ recreating the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#webhook_secret_version_name GoogleCloudbuildBitbucketServerConfig#webhook_secret_version_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7096a32f594525c76ae309427afe2d9492d4c71306b88994a759a3476f54ee6)
            check_type(argname="argument admin_access_token_version_name", value=admin_access_token_version_name, expected_type=type_hints["admin_access_token_version_name"])
            check_type(argname="argument read_access_token_version_name", value=read_access_token_version_name, expected_type=type_hints["read_access_token_version_name"])
            check_type(argname="argument webhook_secret_version_name", value=webhook_secret_version_name, expected_type=type_hints["webhook_secret_version_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_access_token_version_name": admin_access_token_version_name,
            "read_access_token_version_name": read_access_token_version_name,
            "webhook_secret_version_name": webhook_secret_version_name,
        }

    @builtins.property
    def admin_access_token_version_name(self) -> builtins.str:
        '''The resource name for the admin access token's secret version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#admin_access_token_version_name GoogleCloudbuildBitbucketServerConfig#admin_access_token_version_name}
        '''
        result = self._values.get("admin_access_token_version_name")
        assert result is not None, "Required property 'admin_access_token_version_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_access_token_version_name(self) -> builtins.str:
        '''The resource name for the read access token's secret version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#read_access_token_version_name GoogleCloudbuildBitbucketServerConfig#read_access_token_version_name}
        '''
        result = self._values.get("read_access_token_version_name")
        assert result is not None, "Required property 'read_access_token_version_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def webhook_secret_version_name(self) -> builtins.str:
        '''Immutable.

        The resource name for the webhook secret's secret version. Once this field has been set, it cannot be changed.
        Changing this field will result in deleting/ recreating the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#webhook_secret_version_name GoogleCloudbuildBitbucketServerConfig#webhook_secret_version_name}
        '''
        result = self._values.get("webhook_secret_version_name")
        assert result is not None, "Required property 'webhook_secret_version_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildBitbucketServerConfigSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildBitbucketServerConfigSecretsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildBitbucketServerConfig.GoogleCloudbuildBitbucketServerConfigSecretsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22a58e447ae0f0638629c82b96851a41006ae5ea24b6c92bf864f34f5a8a7445)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="adminAccessTokenVersionNameInput")
    def admin_access_token_version_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminAccessTokenVersionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="readAccessTokenVersionNameInput")
    def read_access_token_version_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readAccessTokenVersionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookSecretVersionNameInput")
    def webhook_secret_version_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookSecretVersionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="adminAccessTokenVersionName")
    def admin_access_token_version_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminAccessTokenVersionName"))

    @admin_access_token_version_name.setter
    def admin_access_token_version_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0199cc27490e13261083e87048a9c8367346782178f253885bc597411ac8c309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminAccessTokenVersionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readAccessTokenVersionName")
    def read_access_token_version_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readAccessTokenVersionName"))

    @read_access_token_version_name.setter
    def read_access_token_version_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c613b896aa89fd8f23568f568f2358ecdb8ddf9c1f3eb3c64fb44eb72a6db19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readAccessTokenVersionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookSecretVersionName")
    def webhook_secret_version_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretVersionName"))

    @webhook_secret_version_name.setter
    def webhook_secret_version_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c7f227de8a4c223567961cf0530ac6c0239a68bcf49b904121c622eeadd0e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretVersionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudbuildBitbucketServerConfigSecrets]:
        return typing.cast(typing.Optional[GoogleCloudbuildBitbucketServerConfigSecrets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudbuildBitbucketServerConfigSecrets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a25ba66c841ac388757a5ce396f79497cf33f64a394bbd11c6c85cad483797f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildBitbucketServerConfig.GoogleCloudbuildBitbucketServerConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleCloudbuildBitbucketServerConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#create GoogleCloudbuildBitbucketServerConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#delete GoogleCloudbuildBitbucketServerConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#update GoogleCloudbuildBitbucketServerConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c09c2d63847f552af39bed8dc183f9e05c6f7caefbc4e75dc3b58696d091801)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#create GoogleCloudbuildBitbucketServerConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#delete GoogleCloudbuildBitbucketServerConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloudbuild_bitbucket_server_config#update GoogleCloudbuildBitbucketServerConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudbuildBitbucketServerConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudbuildBitbucketServerConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudbuildBitbucketServerConfig.GoogleCloudbuildBitbucketServerConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac2af62e0c115a5e492995cf4c57090c1d55d860204ce8af7cf9e60adcd5fc66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c681f9e7927b3e530f22a7b8080334b451cd89a783b4f73d7b57645f512036b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb4010ddb1c1e77b27c89c28062a9f04f8cdcd2fda9798b3563d2797420d52b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f25fcfd26501d556222d9c2b35cb6664e6686ae7d19d4790277b7a02491850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildBitbucketServerConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildBitbucketServerConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildBitbucketServerConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43dba0489859ffdbef2a087271860861d9ab49691ecc7141ca1833a5ae7419a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleCloudbuildBitbucketServerConfig",
    "GoogleCloudbuildBitbucketServerConfigConfig",
    "GoogleCloudbuildBitbucketServerConfigConnectedRepositories",
    "GoogleCloudbuildBitbucketServerConfigConnectedRepositoriesList",
    "GoogleCloudbuildBitbucketServerConfigConnectedRepositoriesOutputReference",
    "GoogleCloudbuildBitbucketServerConfigSecrets",
    "GoogleCloudbuildBitbucketServerConfigSecretsOutputReference",
    "GoogleCloudbuildBitbucketServerConfigTimeouts",
    "GoogleCloudbuildBitbucketServerConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__387cb9bf9b6d432beee83052b718b8380309b49b5bb2d1f981203e3d2d51f52f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    api_key: builtins.str,
    config_id: builtins.str,
    host_uri: builtins.str,
    location: builtins.str,
    secrets: typing.Union[GoogleCloudbuildBitbucketServerConfigSecrets, typing.Dict[builtins.str, typing.Any]],
    username: builtins.str,
    connected_repositories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildBitbucketServerConfigConnectedRepositories, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    peered_network: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    ssl_ca: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudbuildBitbucketServerConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ef4b639ff0941beeb3f941edae771978c43f3e3ddb5ee7c320d79d200bb7794c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2473c134ccfea39095dcf82ecbd774988695e4ff2ad99f3a2c668a7319abfe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildBitbucketServerConfigConnectedRepositories, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65c5416997154b434ebb7dcf74885a46def328772d35c44dfb808aed2e9cc77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8fec931b7a8e4bd0ebb85cbc017927fb06b5ce7aff2318a495a5b4861b08cd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251c346d45578b5a38733404f3d961e9f91a0c14ee2070f658f5545f06c234b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d6143c244e8f4cb3ce6bf8aa885374b05cd449b281807d738dd65ea8d95b73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553a51308f4c5e776c6ff50fd56994f2444883f34da61611893530261cef31c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2cd59e5eb56345b5248645c81a1dccaef5ec60c2b4fa93995ec31ba85de7bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417af527aba9db53907e0e6812a57994c716dc19bfae4173f0b620de4be1aa5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11816457717d7cdeb929b320bfb6a320262627010f316eb53d3aa15d32058e92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b5eb208d9ffd0bfa0096c8ececa213b0086d3893eb00179c21f2803da1b2580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d509126af01f1e5d7ffd309734d504cd905bf220a417c31387b47b49ad65056f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    api_key: builtins.str,
    config_id: builtins.str,
    host_uri: builtins.str,
    location: builtins.str,
    secrets: typing.Union[GoogleCloudbuildBitbucketServerConfigSecrets, typing.Dict[builtins.str, typing.Any]],
    username: builtins.str,
    connected_repositories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudbuildBitbucketServerConfigConnectedRepositories, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    peered_network: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    ssl_ca: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudbuildBitbucketServerConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698558ef3351f88cd6a7ea995fdf035f7d93147f24a5e27e9ea90a402ffe38c1(
    *,
    project_key: builtins.str,
    repo_slug: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79dd38bbde7975f60c46863826d518f2ac3b61e7db37229ea27381afd2d70562(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__096d947cb27c5ffbf22649c9e098b7d908b59179ff8fe9981eeb277dd99e882b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eed77ed6c90bb9945ad257d4a181e19eeef78c702ad2f8bfdf401ff796c49cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62b44a5ba9c1dfa8b7169820d71a43e26f1b80b0037d83d8e977814f619650f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c35dbdbd931faffb2368ba2aeee8d78a55fdc97965b806b90267edb496bfc7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c241c5e0118a53bae0eed2223fcc84ff2b44ea5c5b5b1523375fd02693c98f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudbuildBitbucketServerConfigConnectedRepositories]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d56515cb56ba240332e4a5121d29f3eeb6811a238147fc57f94804de58d7150(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33536273ba61c965cf14185a415729c30f9637d1f9a2a16026001eae7b56cf30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4177c64c99ca351f5b2b355afdd610b572c00ede3fb1dd8125d9a31145f97d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05e063f86186c6b104d4bb813fc307764378ae80adbef4122294ccfd146c9b3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildBitbucketServerConfigConnectedRepositories]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7096a32f594525c76ae309427afe2d9492d4c71306b88994a759a3476f54ee6(
    *,
    admin_access_token_version_name: builtins.str,
    read_access_token_version_name: builtins.str,
    webhook_secret_version_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a58e447ae0f0638629c82b96851a41006ae5ea24b6c92bf864f34f5a8a7445(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0199cc27490e13261083e87048a9c8367346782178f253885bc597411ac8c309(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c613b896aa89fd8f23568f568f2358ecdb8ddf9c1f3eb3c64fb44eb72a6db19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c7f227de8a4c223567961cf0530ac6c0239a68bcf49b904121c622eeadd0e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25ba66c841ac388757a5ce396f79497cf33f64a394bbd11c6c85cad483797f1(
    value: typing.Optional[GoogleCloudbuildBitbucketServerConfigSecrets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c09c2d63847f552af39bed8dc183f9e05c6f7caefbc4e75dc3b58696d091801(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2af62e0c115a5e492995cf4c57090c1d55d860204ce8af7cf9e60adcd5fc66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c681f9e7927b3e530f22a7b8080334b451cd89a783b4f73d7b57645f512036b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb4010ddb1c1e77b27c89c28062a9f04f8cdcd2fda9798b3563d2797420d52b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f25fcfd26501d556222d9c2b35cb6664e6686ae7d19d4790277b7a02491850(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43dba0489859ffdbef2a087271860861d9ab49691ecc7141ca1833a5ae7419a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudbuildBitbucketServerConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

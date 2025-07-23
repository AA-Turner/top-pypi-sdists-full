r'''
# `google_cloudbuild_bitbucket_server_config`

Refer to the Terraform Registry for docs: [`google_cloudbuild_bitbucket_server_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config).
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


class CloudbuildBitbucketServerConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildBitbucketServerConfig.CloudbuildBitbucketServerConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config google_cloudbuild_bitbucket_server_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        api_key: builtins.str,
        config_id: builtins.str,
        host_uri: builtins.str,
        location: builtins.str,
        secrets: typing.Union["CloudbuildBitbucketServerConfigSecrets", typing.Dict[builtins.str, typing.Any]],
        username: builtins.str,
        connected_repositories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildBitbucketServerConfigConnectedRepositories", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        peered_network: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CloudbuildBitbucketServerConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config google_cloudbuild_bitbucket_server_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_key: Immutable. API Key that will be attached to webhook. Once this field has been set, it cannot be changed. Changing this field will result in deleting/ recreating the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#api_key CloudbuildBitbucketServerConfig#api_key}
        :param config_id: The ID to use for the BitbucketServerConfig, which will become the final component of the BitbucketServerConfig's resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#config_id CloudbuildBitbucketServerConfig#config_id}
        :param host_uri: Immutable. The URI of the Bitbucket Server host. Once this field has been set, it cannot be changed. If you need to change it, please create another BitbucketServerConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#host_uri CloudbuildBitbucketServerConfig#host_uri}
        :param location: The location of this bitbucket server config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#location CloudbuildBitbucketServerConfig#location}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#secrets CloudbuildBitbucketServerConfig#secrets}
        :param username: Username of the account Cloud Build will use on Bitbucket Server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#username CloudbuildBitbucketServerConfig#username}
        :param connected_repositories: connected_repositories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#connected_repositories CloudbuildBitbucketServerConfig#connected_repositories}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#id CloudbuildBitbucketServerConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param peered_network: The network to be used when reaching out to the Bitbucket Server instance. The VPC network must be enabled for private service connection. This should be set if the Bitbucket Server instance is hosted on-premises and not reachable by public internet. If this field is left empty, no network peering will occur and calls to the Bitbucket Server instance will be made over the public internet. Must be in the format projects/{project}/global/networks/{network}, where {project} is a project number or id and {network} is the name of a VPC network in the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#peered_network CloudbuildBitbucketServerConfig#peered_network}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#project CloudbuildBitbucketServerConfig#project}.
        :param ssl_ca: SSL certificate to use for requests to Bitbucket Server. The format should be PEM format but the extension can be one of .pem, .cer, or .crt. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#ssl_ca CloudbuildBitbucketServerConfig#ssl_ca}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#timeouts CloudbuildBitbucketServerConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e280400f0b3a4e11d10d7bb12022d773cfb91fc280754a56308bc0c82edcce4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudbuildBitbucketServerConfigConfig(
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
        '''Generates CDKTF code for importing a CloudbuildBitbucketServerConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudbuildBitbucketServerConfig to import.
        :param import_from_id: The id of the existing CloudbuildBitbucketServerConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudbuildBitbucketServerConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab5c9c7550d3ee99e4afc581ab257dae4902867e516e8879fd4dcf319d8345c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConnectedRepositories")
    def put_connected_repositories(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildBitbucketServerConfigConnectedRepositories", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9aacfbf9869c890e2806c14db9b9088bc21db527f8f686da9b1bd229f08448e)
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
        :param admin_access_token_version_name: The resource name for the admin access token's secret version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#admin_access_token_version_name CloudbuildBitbucketServerConfig#admin_access_token_version_name}
        :param read_access_token_version_name: The resource name for the read access token's secret version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#read_access_token_version_name CloudbuildBitbucketServerConfig#read_access_token_version_name}
        :param webhook_secret_version_name: Immutable. The resource name for the webhook secret's secret version. Once this field has been set, it cannot be changed. Changing this field will result in deleting/ recreating the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#webhook_secret_version_name CloudbuildBitbucketServerConfig#webhook_secret_version_name}
        '''
        value = CloudbuildBitbucketServerConfigSecrets(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#create CloudbuildBitbucketServerConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#delete CloudbuildBitbucketServerConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#update CloudbuildBitbucketServerConfig#update}.
        '''
        value = CloudbuildBitbucketServerConfigTimeouts(
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
    ) -> "CloudbuildBitbucketServerConfigConnectedRepositoriesList":
        return typing.cast("CloudbuildBitbucketServerConfigConnectedRepositoriesList", jsii.get(self, "connectedRepositories"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> "CloudbuildBitbucketServerConfigSecretsOutputReference":
        return typing.cast("CloudbuildBitbucketServerConfigSecretsOutputReference", jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudbuildBitbucketServerConfigTimeoutsOutputReference":
        return typing.cast("CloudbuildBitbucketServerConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildBitbucketServerConfigConnectedRepositories"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildBitbucketServerConfigConnectedRepositories"]]], jsii.get(self, "connectedRepositoriesInput"))

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
    ) -> typing.Optional["CloudbuildBitbucketServerConfigSecrets"]:
        return typing.cast(typing.Optional["CloudbuildBitbucketServerConfigSecrets"], jsii.get(self, "secretsInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCaInput")
    def ssl_ca_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCaInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudbuildBitbucketServerConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudbuildBitbucketServerConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__11e5660e4f625365f7feb1113eb60fbad1dd346cd478dd3fac6c2c8d97233bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configId")
    def config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configId"))

    @config_id.setter
    def config_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ccc1bd02a3c70e3bd27b36811f60c0cea84188bfbd54c6c8c9206791c457df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostUri")
    def host_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostUri"))

    @host_uri.setter
    def host_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e53d0aff7c47b0e8a63f095907125c4748fb7d99a67c903f9674bf1ce10d2e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84998a766f1a0b107460f4f7f647bc870e6774d7543b804995e1cb40fe3a7d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c262385af387eb8d98e553a9848f56dbd70b3b4cc964f5a6f1b504055499e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peeredNetwork")
    def peered_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peeredNetwork"))

    @peered_network.setter
    def peered_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d087ccba6089970422b97e16d089c1abe6fd89dea020f6dfe4872cc4cbb7d7de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peeredNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077cae5c6913a3fb1dc78e335377e2a9aa09cf7cfe1d34635c604c8071952ea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCa")
    def ssl_ca(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCa"))

    @ssl_ca.setter
    def ssl_ca(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ff5acdd1c47caa53ebd88ad991daded0f31bf2481ac2279a20b9e79168fa5fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1cab3f3591ccc6cc6884e28f8adc8d64169bae8c41d25fede2906233a5619e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildBitbucketServerConfig.CloudbuildBitbucketServerConfigConfig",
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
class CloudbuildBitbucketServerConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        secrets: typing.Union["CloudbuildBitbucketServerConfigSecrets", typing.Dict[builtins.str, typing.Any]],
        username: builtins.str,
        connected_repositories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudbuildBitbucketServerConfigConnectedRepositories", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        peered_network: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        ssl_ca: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CloudbuildBitbucketServerConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_key: Immutable. API Key that will be attached to webhook. Once this field has been set, it cannot be changed. Changing this field will result in deleting/ recreating the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#api_key CloudbuildBitbucketServerConfig#api_key}
        :param config_id: The ID to use for the BitbucketServerConfig, which will become the final component of the BitbucketServerConfig's resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#config_id CloudbuildBitbucketServerConfig#config_id}
        :param host_uri: Immutable. The URI of the Bitbucket Server host. Once this field has been set, it cannot be changed. If you need to change it, please create another BitbucketServerConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#host_uri CloudbuildBitbucketServerConfig#host_uri}
        :param location: The location of this bitbucket server config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#location CloudbuildBitbucketServerConfig#location}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#secrets CloudbuildBitbucketServerConfig#secrets}
        :param username: Username of the account Cloud Build will use on Bitbucket Server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#username CloudbuildBitbucketServerConfig#username}
        :param connected_repositories: connected_repositories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#connected_repositories CloudbuildBitbucketServerConfig#connected_repositories}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#id CloudbuildBitbucketServerConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param peered_network: The network to be used when reaching out to the Bitbucket Server instance. The VPC network must be enabled for private service connection. This should be set if the Bitbucket Server instance is hosted on-premises and not reachable by public internet. If this field is left empty, no network peering will occur and calls to the Bitbucket Server instance will be made over the public internet. Must be in the format projects/{project}/global/networks/{network}, where {project} is a project number or id and {network} is the name of a VPC network in the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#peered_network CloudbuildBitbucketServerConfig#peered_network}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#project CloudbuildBitbucketServerConfig#project}.
        :param ssl_ca: SSL certificate to use for requests to Bitbucket Server. The format should be PEM format but the extension can be one of .pem, .cer, or .crt. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#ssl_ca CloudbuildBitbucketServerConfig#ssl_ca}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#timeouts CloudbuildBitbucketServerConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(secrets, dict):
            secrets = CloudbuildBitbucketServerConfigSecrets(**secrets)
        if isinstance(timeouts, dict):
            timeouts = CloudbuildBitbucketServerConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b189642c3ec5143d70a1af84e088b8770d10889d8d8dc20eb9dd4f2a5e482b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#api_key CloudbuildBitbucketServerConfig#api_key}
        '''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config_id(self) -> builtins.str:
        '''The ID to use for the BitbucketServerConfig, which will become the final component of the BitbucketServerConfig's resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#config_id CloudbuildBitbucketServerConfig#config_id}
        '''
        result = self._values.get("config_id")
        assert result is not None, "Required property 'config_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_uri(self) -> builtins.str:
        '''Immutable.

        The URI of the Bitbucket Server host. Once this field has been set, it cannot be changed.
        If you need to change it, please create another BitbucketServerConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#host_uri CloudbuildBitbucketServerConfig#host_uri}
        '''
        result = self._values.get("host_uri")
        assert result is not None, "Required property 'host_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of this bitbucket server config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#location CloudbuildBitbucketServerConfig#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secrets(self) -> "CloudbuildBitbucketServerConfigSecrets":
        '''secrets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#secrets CloudbuildBitbucketServerConfig#secrets}
        '''
        result = self._values.get("secrets")
        assert result is not None, "Required property 'secrets' is missing"
        return typing.cast("CloudbuildBitbucketServerConfigSecrets", result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username of the account Cloud Build will use on Bitbucket Server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#username CloudbuildBitbucketServerConfig#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connected_repositories(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildBitbucketServerConfigConnectedRepositories"]]]:
        '''connected_repositories block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#connected_repositories CloudbuildBitbucketServerConfig#connected_repositories}
        '''
        result = self._values.get("connected_repositories")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudbuildBitbucketServerConfigConnectedRepositories"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#id CloudbuildBitbucketServerConfig#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#peered_network CloudbuildBitbucketServerConfig#peered_network}
        '''
        result = self._values.get("peered_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#project CloudbuildBitbucketServerConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_ca(self) -> typing.Optional[builtins.str]:
        '''SSL certificate to use for requests to Bitbucket Server.

        The format should be PEM format but the extension can be one of .pem, .cer, or .crt.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#ssl_ca CloudbuildBitbucketServerConfig#ssl_ca}
        '''
        result = self._values.get("ssl_ca")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudbuildBitbucketServerConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#timeouts CloudbuildBitbucketServerConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudbuildBitbucketServerConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildBitbucketServerConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildBitbucketServerConfig.CloudbuildBitbucketServerConfigConnectedRepositories",
    jsii_struct_bases=[],
    name_mapping={"project_key": "projectKey", "repo_slug": "repoSlug"},
)
class CloudbuildBitbucketServerConfigConnectedRepositories:
    def __init__(self, *, project_key: builtins.str, repo_slug: builtins.str) -> None:
        '''
        :param project_key: Identifier for the project storing the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#project_key CloudbuildBitbucketServerConfig#project_key}
        :param repo_slug: Identifier for the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#repo_slug CloudbuildBitbucketServerConfig#repo_slug}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2540ec0963632517ef07eba6e3063f60f2028dc947ef1444cd58d341e591d7)
            check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            check_type(argname="argument repo_slug", value=repo_slug, expected_type=type_hints["repo_slug"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_key": project_key,
            "repo_slug": repo_slug,
        }

    @builtins.property
    def project_key(self) -> builtins.str:
        '''Identifier for the project storing the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#project_key CloudbuildBitbucketServerConfig#project_key}
        '''
        result = self._values.get("project_key")
        assert result is not None, "Required property 'project_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo_slug(self) -> builtins.str:
        '''Identifier for the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#repo_slug CloudbuildBitbucketServerConfig#repo_slug}
        '''
        result = self._values.get("repo_slug")
        assert result is not None, "Required property 'repo_slug' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildBitbucketServerConfigConnectedRepositories(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildBitbucketServerConfigConnectedRepositoriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildBitbucketServerConfig.CloudbuildBitbucketServerConfigConnectedRepositoriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0ceb07b95c7eaa6ad50ee24d8a7194b03701e7da7b0df079db6cd177518ac07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudbuildBitbucketServerConfigConnectedRepositoriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__302781587c954cde916d405efe12c640e8331668bb9a3ae031918cd0f3495321)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudbuildBitbucketServerConfigConnectedRepositoriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d7ca748863b53d3c82f2d9e5444509776962f479dc5d74bc64ab92e41f820d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b05788b71eedb010538e878b1718933297e32f1c78a7dd922d77b00e0f0e6f51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f378cdf19958e3f0c26b1c499024594f563c7ba97fda6c76838fa9a00790e08d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildBitbucketServerConfigConnectedRepositories]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildBitbucketServerConfigConnectedRepositories]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildBitbucketServerConfigConnectedRepositories]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ded030f0dd81d0a305ecd1be1693d7d63659751c58e971bf67a291970bc9908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudbuildBitbucketServerConfigConnectedRepositoriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildBitbucketServerConfig.CloudbuildBitbucketServerConfigConnectedRepositoriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a5e3d36dd4933ac8c2227dce08bce907fe20b6b21ffdacf43ef3170a0f61937)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ffaac03484e3669ab3e1bb2f6f668e9bc5156269abf131b0bb4669b000aa0dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoSlug")
    def repo_slug(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoSlug"))

    @repo_slug.setter
    def repo_slug(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30177c50cf162610d4fd9ef159d6b65243ac0315cf64f58053a661c1430b2504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoSlug", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildBitbucketServerConfigConnectedRepositories]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildBitbucketServerConfigConnectedRepositories]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildBitbucketServerConfigConnectedRepositories]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__815982f45205082377998043947499e4c44495df8cbc47587350ff416b79083c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildBitbucketServerConfig.CloudbuildBitbucketServerConfigSecrets",
    jsii_struct_bases=[],
    name_mapping={
        "admin_access_token_version_name": "adminAccessTokenVersionName",
        "read_access_token_version_name": "readAccessTokenVersionName",
        "webhook_secret_version_name": "webhookSecretVersionName",
    },
)
class CloudbuildBitbucketServerConfigSecrets:
    def __init__(
        self,
        *,
        admin_access_token_version_name: builtins.str,
        read_access_token_version_name: builtins.str,
        webhook_secret_version_name: builtins.str,
    ) -> None:
        '''
        :param admin_access_token_version_name: The resource name for the admin access token's secret version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#admin_access_token_version_name CloudbuildBitbucketServerConfig#admin_access_token_version_name}
        :param read_access_token_version_name: The resource name for the read access token's secret version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#read_access_token_version_name CloudbuildBitbucketServerConfig#read_access_token_version_name}
        :param webhook_secret_version_name: Immutable. The resource name for the webhook secret's secret version. Once this field has been set, it cannot be changed. Changing this field will result in deleting/ recreating the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#webhook_secret_version_name CloudbuildBitbucketServerConfig#webhook_secret_version_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5c7cdcf5387ae77e9a7501d6ce16c44957486ea90a310d208826629d640c92)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#admin_access_token_version_name CloudbuildBitbucketServerConfig#admin_access_token_version_name}
        '''
        result = self._values.get("admin_access_token_version_name")
        assert result is not None, "Required property 'admin_access_token_version_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_access_token_version_name(self) -> builtins.str:
        '''The resource name for the read access token's secret version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#read_access_token_version_name CloudbuildBitbucketServerConfig#read_access_token_version_name}
        '''
        result = self._values.get("read_access_token_version_name")
        assert result is not None, "Required property 'read_access_token_version_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def webhook_secret_version_name(self) -> builtins.str:
        '''Immutable.

        The resource name for the webhook secret's secret version. Once this field has been set, it cannot be changed.
        Changing this field will result in deleting/ recreating the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#webhook_secret_version_name CloudbuildBitbucketServerConfig#webhook_secret_version_name}
        '''
        result = self._values.get("webhook_secret_version_name")
        assert result is not None, "Required property 'webhook_secret_version_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildBitbucketServerConfigSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildBitbucketServerConfigSecretsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildBitbucketServerConfig.CloudbuildBitbucketServerConfigSecretsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbe431dc2ae5ea731e41528fb44bb969a3b2cb8b6c9356f06684eb703064b22f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2863bd6e90bd97606166b2f0c61d214fca3dea28efc102075cf54603435a0ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminAccessTokenVersionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readAccessTokenVersionName")
    def read_access_token_version_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readAccessTokenVersionName"))

    @read_access_token_version_name.setter
    def read_access_token_version_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f5459268769725fc38bbe4d4ddabc6cf909474cb33a44214649658ac15234a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readAccessTokenVersionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookSecretVersionName")
    def webhook_secret_version_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookSecretVersionName"))

    @webhook_secret_version_name.setter
    def webhook_secret_version_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506ed4319969bef32a8391c7fd5dae7317a491c6ed1de02eeec45a2033192e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookSecretVersionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudbuildBitbucketServerConfigSecrets]:
        return typing.cast(typing.Optional[CloudbuildBitbucketServerConfigSecrets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudbuildBitbucketServerConfigSecrets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d94f1e6c9571ad24e728acf8e31bb79a7e39c94b7cbcc7b3e9983ab7e99a7db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudbuildBitbucketServerConfig.CloudbuildBitbucketServerConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudbuildBitbucketServerConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#create CloudbuildBitbucketServerConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#delete CloudbuildBitbucketServerConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#update CloudbuildBitbucketServerConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ffe91adfb7f760eded5d6e1d77251af89a8490c813c6463dd11c58c6536c603)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#create CloudbuildBitbucketServerConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#delete CloudbuildBitbucketServerConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudbuild_bitbucket_server_config#update CloudbuildBitbucketServerConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudbuildBitbucketServerConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudbuildBitbucketServerConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudbuildBitbucketServerConfig.CloudbuildBitbucketServerConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a333b181701a5c1efdbbbb875ad66c755338937146f6538d20eed4738b796cd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ebf8b1cbf17125c9d4ee66e887d94a1c7319d16f108b88e240230a2de69a9a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb959e2b014a8e1aa7a6b47d133c535bbfed33b2669fbd74c7c74a58e49ff1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539c970a3c078e4ea66b310c60728ebde3d48a3025ea5c736fb2271ea91702de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildBitbucketServerConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildBitbucketServerConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildBitbucketServerConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78c337b13aaa82c981980219f90ff755f8026c894b03adb1df5a015593c94a6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudbuildBitbucketServerConfig",
    "CloudbuildBitbucketServerConfigConfig",
    "CloudbuildBitbucketServerConfigConnectedRepositories",
    "CloudbuildBitbucketServerConfigConnectedRepositoriesList",
    "CloudbuildBitbucketServerConfigConnectedRepositoriesOutputReference",
    "CloudbuildBitbucketServerConfigSecrets",
    "CloudbuildBitbucketServerConfigSecretsOutputReference",
    "CloudbuildBitbucketServerConfigTimeouts",
    "CloudbuildBitbucketServerConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3e280400f0b3a4e11d10d7bb12022d773cfb91fc280754a56308bc0c82edcce4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    api_key: builtins.str,
    config_id: builtins.str,
    host_uri: builtins.str,
    location: builtins.str,
    secrets: typing.Union[CloudbuildBitbucketServerConfigSecrets, typing.Dict[builtins.str, typing.Any]],
    username: builtins.str,
    connected_repositories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildBitbucketServerConfigConnectedRepositories, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    peered_network: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    ssl_ca: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CloudbuildBitbucketServerConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9ab5c9c7550d3ee99e4afc581ab257dae4902867e516e8879fd4dcf319d8345c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9aacfbf9869c890e2806c14db9b9088bc21db527f8f686da9b1bd229f08448e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildBitbucketServerConfigConnectedRepositories, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e5660e4f625365f7feb1113eb60fbad1dd346cd478dd3fac6c2c8d97233bd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ccc1bd02a3c70e3bd27b36811f60c0cea84188bfbd54c6c8c9206791c457df2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e53d0aff7c47b0e8a63f095907125c4748fb7d99a67c903f9674bf1ce10d2e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84998a766f1a0b107460f4f7f647bc870e6774d7543b804995e1cb40fe3a7d35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c262385af387eb8d98e553a9848f56dbd70b3b4cc964f5a6f1b504055499e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d087ccba6089970422b97e16d089c1abe6fd89dea020f6dfe4872cc4cbb7d7de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077cae5c6913a3fb1dc78e335377e2a9aa09cf7cfe1d34635c604c8071952ea3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff5acdd1c47caa53ebd88ad991daded0f31bf2481ac2279a20b9e79168fa5fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1cab3f3591ccc6cc6884e28f8adc8d64169bae8c41d25fede2906233a5619e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b189642c3ec5143d70a1af84e088b8770d10889d8d8dc20eb9dd4f2a5e482b(
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
    secrets: typing.Union[CloudbuildBitbucketServerConfigSecrets, typing.Dict[builtins.str, typing.Any]],
    username: builtins.str,
    connected_repositories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudbuildBitbucketServerConfigConnectedRepositories, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    peered_network: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    ssl_ca: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CloudbuildBitbucketServerConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2540ec0963632517ef07eba6e3063f60f2028dc947ef1444cd58d341e591d7(
    *,
    project_key: builtins.str,
    repo_slug: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ceb07b95c7eaa6ad50ee24d8a7194b03701e7da7b0df079db6cd177518ac07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__302781587c954cde916d405efe12c640e8331668bb9a3ae031918cd0f3495321(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d7ca748863b53d3c82f2d9e5444509776962f479dc5d74bc64ab92e41f820d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05788b71eedb010538e878b1718933297e32f1c78a7dd922d77b00e0f0e6f51(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f378cdf19958e3f0c26b1c499024594f563c7ba97fda6c76838fa9a00790e08d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ded030f0dd81d0a305ecd1be1693d7d63659751c58e971bf67a291970bc9908(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudbuildBitbucketServerConfigConnectedRepositories]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5e3d36dd4933ac8c2227dce08bce907fe20b6b21ffdacf43ef3170a0f61937(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ffaac03484e3669ab3e1bb2f6f668e9bc5156269abf131b0bb4669b000aa0dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30177c50cf162610d4fd9ef159d6b65243ac0315cf64f58053a661c1430b2504(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815982f45205082377998043947499e4c44495df8cbc47587350ff416b79083c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildBitbucketServerConfigConnectedRepositories]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5c7cdcf5387ae77e9a7501d6ce16c44957486ea90a310d208826629d640c92(
    *,
    admin_access_token_version_name: builtins.str,
    read_access_token_version_name: builtins.str,
    webhook_secret_version_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe431dc2ae5ea731e41528fb44bb969a3b2cb8b6c9356f06684eb703064b22f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2863bd6e90bd97606166b2f0c61d214fca3dea28efc102075cf54603435a0ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f5459268769725fc38bbe4d4ddabc6cf909474cb33a44214649658ac15234a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506ed4319969bef32a8391c7fd5dae7317a491c6ed1de02eeec45a2033192e50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d94f1e6c9571ad24e728acf8e31bb79a7e39c94b7cbcc7b3e9983ab7e99a7db(
    value: typing.Optional[CloudbuildBitbucketServerConfigSecrets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ffe91adfb7f760eded5d6e1d77251af89a8490c813c6463dd11c58c6536c603(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a333b181701a5c1efdbbbb875ad66c755338937146f6538d20eed4738b796cd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ebf8b1cbf17125c9d4ee66e887d94a1c7319d16f108b88e240230a2de69a9a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb959e2b014a8e1aa7a6b47d133c535bbfed33b2669fbd74c7c74a58e49ff1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539c970a3c078e4ea66b310c60728ebde3d48a3025ea5c736fb2271ea91702de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c337b13aaa82c981980219f90ff755f8026c894b03adb1df5a015593c94a6c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudbuildBitbucketServerConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

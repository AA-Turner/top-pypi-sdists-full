r'''
# `google_apigee_environment`

Refer to the Terraform Registry for docs: [`google_apigee_environment`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment).
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


class GoogleApigeeEnvironment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeEnvironment.GoogleApigeeEnvironment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment google_apigee_environment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        org_id: builtins.str,
        api_proxy_type: typing.Optional[builtins.str] = None,
        client_ip_resolution_config: typing.Optional[typing.Union["GoogleApigeeEnvironmentClientIpResolutionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        forward_proxy_uri: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        node_config: typing.Optional[typing.Union["GoogleApigeeEnvironmentNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Union["GoogleApigeeEnvironmentProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeEnvironmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment google_apigee_environment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The resource ID of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#name GoogleApigeeEnvironment#name}
        :param org_id: The Apigee Organization associated with the Apigee environment, in the format 'organizations/{{org_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#org_id GoogleApigeeEnvironment#org_id}
        :param api_proxy_type: Optional. API Proxy type supported by the environment. The type can be set when creating the Environment and cannot be changed. Possible values: ["API_PROXY_TYPE_UNSPECIFIED", "PROGRAMMABLE", "CONFIGURABLE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#api_proxy_type GoogleApigeeEnvironment#api_proxy_type}
        :param client_ip_resolution_config: client_ip_resolution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#client_ip_resolution_config GoogleApigeeEnvironment#client_ip_resolution_config}
        :param deployment_type: Optional. Deployment type supported by the environment. The deployment type can be set when creating the environment and cannot be changed. When you enable archive deployment, you will be prevented from performing a subset of actions within the environment, including: Managing the deployment of API proxy or shared flow revisions; Creating, updating, or deleting resource files; Creating, updating, or deleting target servers. Possible values: ["DEPLOYMENT_TYPE_UNSPECIFIED", "PROXY", "ARCHIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#deployment_type GoogleApigeeEnvironment#deployment_type}
        :param description: Description of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#description GoogleApigeeEnvironment#description}
        :param display_name: Display name of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#display_name GoogleApigeeEnvironment#display_name}
        :param forward_proxy_uri: Optional. URI of the forward proxy to be applied to the runtime instances in this environment. Must be in the format of {scheme}://{hostname}:{port}. Note that the scheme must be one of "http" or "https", and the port must be supplied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#forward_proxy_uri GoogleApigeeEnvironment#forward_proxy_uri}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#id GoogleApigeeEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#node_config GoogleApigeeEnvironment#node_config}
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#properties GoogleApigeeEnvironment#properties}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#timeouts GoogleApigeeEnvironment#timeouts}
        :param type: Types that can be selected for an Environment. Each of the types are limited by capability and capacity. Refer to Apigee's public documentation to understand about each of these types in details. An Apigee org can support heterogeneous Environments. Possible values: ["ENVIRONMENT_TYPE_UNSPECIFIED", "BASE", "INTERMEDIATE", "COMPREHENSIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#type GoogleApigeeEnvironment#type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc229540176c799051ab83314c246b0d7b10ccfddf834fc7f47c376be6f71fa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleApigeeEnvironmentConfig(
            name=name,
            org_id=org_id,
            api_proxy_type=api_proxy_type,
            client_ip_resolution_config=client_ip_resolution_config,
            deployment_type=deployment_type,
            description=description,
            display_name=display_name,
            forward_proxy_uri=forward_proxy_uri,
            id=id,
            node_config=node_config,
            properties=properties,
            timeouts=timeouts,
            type=type,
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
        '''Generates CDKTF code for importing a GoogleApigeeEnvironment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleApigeeEnvironment to import.
        :param import_from_id: The id of the existing GoogleApigeeEnvironment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleApigeeEnvironment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b8b5b9255d8bb9ad208889b6fec1af55a6816ae7d5a3dcf8882a40b62e722b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putClientIpResolutionConfig")
    def put_client_ip_resolution_config(
        self,
        *,
        header_index_algorithm: typing.Optional[typing.Union["GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param header_index_algorithm: header_index_algorithm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#header_index_algorithm GoogleApigeeEnvironment#header_index_algorithm}
        '''
        value = GoogleApigeeEnvironmentClientIpResolutionConfig(
            header_index_algorithm=header_index_algorithm
        )

        return typing.cast(None, jsii.invoke(self, "putClientIpResolutionConfig", [value]))

    @jsii.member(jsii_name="putNodeConfig")
    def put_node_config(
        self,
        *,
        max_node_count: typing.Optional[builtins.str] = None,
        min_node_count: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_node_count: The maximum total number of gateway nodes that the is reserved for all instances that has the specified environment. If not specified, the default is determined by the recommended maximum number of nodes for that gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#max_node_count GoogleApigeeEnvironment#max_node_count}
        :param min_node_count: The minimum total number of gateway nodes that the is reserved for all instances that has the specified environment. If not specified, the default is determined by the recommended minimum number of nodes for that gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#min_node_count GoogleApigeeEnvironment#min_node_count}
        '''
        value = GoogleApigeeEnvironmentNodeConfig(
            max_node_count=max_node_count, min_node_count=min_node_count
        )

        return typing.cast(None, jsii.invoke(self, "putNodeConfig", [value]))

    @jsii.member(jsii_name="putProperties")
    def put_properties(
        self,
        *,
        property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeEnvironmentPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param property: property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#property GoogleApigeeEnvironment#property}
        '''
        value = GoogleApigeeEnvironmentProperties(property=property)

        return typing.cast(None, jsii.invoke(self, "putProperties", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#create GoogleApigeeEnvironment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#delete GoogleApigeeEnvironment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#update GoogleApigeeEnvironment#update}.
        '''
        value = GoogleApigeeEnvironmentTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetApiProxyType")
    def reset_api_proxy_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiProxyType", []))

    @jsii.member(jsii_name="resetClientIpResolutionConfig")
    def reset_client_ip_resolution_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientIpResolutionConfig", []))

    @jsii.member(jsii_name="resetDeploymentType")
    def reset_deployment_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentType", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetForwardProxyUri")
    def reset_forward_proxy_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardProxyUri", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNodeConfig")
    def reset_node_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeConfig", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="clientIpResolutionConfig")
    def client_ip_resolution_config(
        self,
    ) -> "GoogleApigeeEnvironmentClientIpResolutionConfigOutputReference":
        return typing.cast("GoogleApigeeEnvironmentClientIpResolutionConfigOutputReference", jsii.get(self, "clientIpResolutionConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(self) -> "GoogleApigeeEnvironmentNodeConfigOutputReference":
        return typing.cast("GoogleApigeeEnvironmentNodeConfigOutputReference", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> "GoogleApigeeEnvironmentPropertiesOutputReference":
        return typing.cast("GoogleApigeeEnvironmentPropertiesOutputReference", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleApigeeEnvironmentTimeoutsOutputReference":
        return typing.cast("GoogleApigeeEnvironmentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="apiProxyTypeInput")
    def api_proxy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiProxyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIpResolutionConfigInput")
    def client_ip_resolution_config_input(
        self,
    ) -> typing.Optional["GoogleApigeeEnvironmentClientIpResolutionConfig"]:
        return typing.cast(typing.Optional["GoogleApigeeEnvironmentClientIpResolutionConfig"], jsii.get(self, "clientIpResolutionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentTypeInput")
    def deployment_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardProxyUriInput")
    def forward_proxy_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardProxyUriInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigInput")
    def node_config_input(self) -> typing.Optional["GoogleApigeeEnvironmentNodeConfig"]:
        return typing.cast(typing.Optional["GoogleApigeeEnvironmentNodeConfig"], jsii.get(self, "nodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="orgIdInput")
    def org_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgIdInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(self) -> typing.Optional["GoogleApigeeEnvironmentProperties"]:
        return typing.cast(typing.Optional["GoogleApigeeEnvironmentProperties"], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeEnvironmentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeEnvironmentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="apiProxyType")
    def api_proxy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiProxyType"))

    @api_proxy_type.setter
    def api_proxy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1685eb760562e23b2ad8db817d9ab14e81be9ac69a6b56cacfd0d073608dfb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiProxyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentType")
    def deployment_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentType"))

    @deployment_type.setter
    def deployment_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5cb2a5460e1c69b4cd86003adbd1b991526ac204803309885ec04b761d85c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc645b061b4a35ad8761634c568bd131a48ed5e439f2c9dbf393423cd33a863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f4c49a80bee3f95285cb739ef55a71ad7bea287cf20d3a95d916fced4052e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardProxyUri")
    def forward_proxy_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardProxyUri"))

    @forward_proxy_uri.setter
    def forward_proxy_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d95f942a5122042687d0d1118d408a70a906c3f621f10d1354aa82b783ce76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardProxyUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d129cf7ec82c3e06bb7b32f06410ae575c245f4f0facb60685f214cac4dfbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c65201fbba5cbeae5520844a9acb42dcdc5b3f649e2d705ad995207cbef426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @org_id.setter
    def org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a09578d2728632935747cdbb554f7c14a7d85600382d4cbd62924aa511b319aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506311c403c8da86b06dcb5b02287378f948845d64bab47a4df384acd5d4da72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeEnvironment.GoogleApigeeEnvironmentClientIpResolutionConfig",
    jsii_struct_bases=[],
    name_mapping={"header_index_algorithm": "headerIndexAlgorithm"},
)
class GoogleApigeeEnvironmentClientIpResolutionConfig:
    def __init__(
        self,
        *,
        header_index_algorithm: typing.Optional[typing.Union["GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param header_index_algorithm: header_index_algorithm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#header_index_algorithm GoogleApigeeEnvironment#header_index_algorithm}
        '''
        if isinstance(header_index_algorithm, dict):
            header_index_algorithm = GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm(**header_index_algorithm)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a35caf397f165e71d3495a4d44ce9c84d38784e8ac710682c08cb81a9e882f5)
            check_type(argname="argument header_index_algorithm", value=header_index_algorithm, expected_type=type_hints["header_index_algorithm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_index_algorithm is not None:
            self._values["header_index_algorithm"] = header_index_algorithm

    @builtins.property
    def header_index_algorithm(
        self,
    ) -> typing.Optional["GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm"]:
        '''header_index_algorithm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#header_index_algorithm GoogleApigeeEnvironment#header_index_algorithm}
        '''
        result = self._values.get("header_index_algorithm")
        return typing.cast(typing.Optional["GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeEnvironmentClientIpResolutionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeEnvironment.GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm",
    jsii_struct_bases=[],
    name_mapping={
        "ip_header_index": "ipHeaderIndex",
        "ip_header_name": "ipHeaderName",
    },
)
class GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm:
    def __init__(
        self,
        *,
        ip_header_index: jsii.Number,
        ip_header_name: builtins.str,
    ) -> None:
        '''
        :param ip_header_index: The index of the ip in the header. Positive indices 0, 1, 2, 3 chooses indices from the left (first ips). Negative indices -1, -2, -3 chooses indices from the right (last ips). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#ip_header_index GoogleApigeeEnvironment#ip_header_index}
        :param ip_header_name: The name of the header to extract the client ip from. We are currently only supporting the X-Forwarded-For header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#ip_header_name GoogleApigeeEnvironment#ip_header_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269e028193115b8fc075c36f12363f7a0f0a690f92b86b35ee2d6dc2d4504c77)
            check_type(argname="argument ip_header_index", value=ip_header_index, expected_type=type_hints["ip_header_index"])
            check_type(argname="argument ip_header_name", value=ip_header_name, expected_type=type_hints["ip_header_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_header_index": ip_header_index,
            "ip_header_name": ip_header_name,
        }

    @builtins.property
    def ip_header_index(self) -> jsii.Number:
        '''The index of the ip in the header.

        Positive indices 0, 1, 2, 3 chooses indices from the left (first ips). Negative indices -1, -2, -3 chooses indices from the right (last ips).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#ip_header_index GoogleApigeeEnvironment#ip_header_index}
        '''
        result = self._values.get("ip_header_index")
        assert result is not None, "Required property 'ip_header_index' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def ip_header_name(self) -> builtins.str:
        '''The name of the header to extract the client ip from. We are currently only supporting the X-Forwarded-For header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#ip_header_name GoogleApigeeEnvironment#ip_header_name}
        '''
        result = self._values.get("ip_header_name")
        assert result is not None, "Required property 'ip_header_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeEnvironment.GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__783000f33c677b9568b18bb0df018bad5f69bbcab9c4d59b8028621983cf5625)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ipHeaderIndexInput")
    def ip_header_index_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ipHeaderIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="ipHeaderNameInput")
    def ip_header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipHeaderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipHeaderIndex")
    def ip_header_index(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ipHeaderIndex"))

    @ip_header_index.setter
    def ip_header_index(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a3aa706081c627d1cadc21f7911c7710145d531a8cc9ce008f41443fa53a8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipHeaderIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipHeaderName")
    def ip_header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipHeaderName"))

    @ip_header_name.setter
    def ip_header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b28795cf50487c5c5b9f37bed834eaa2ffbc47e359901f4459b43cf967ad63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm]:
        return typing.cast(typing.Optional[GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492fd241cecc06af9c3047604be4b3f71a0db990de1de7c35a755d7ac9bae99c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeEnvironmentClientIpResolutionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeEnvironment.GoogleApigeeEnvironmentClientIpResolutionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__636d5c7d87558f54b26708267839f908dd04fa11417e18bc3a049855208387df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaderIndexAlgorithm")
    def put_header_index_algorithm(
        self,
        *,
        ip_header_index: jsii.Number,
        ip_header_name: builtins.str,
    ) -> None:
        '''
        :param ip_header_index: The index of the ip in the header. Positive indices 0, 1, 2, 3 chooses indices from the left (first ips). Negative indices -1, -2, -3 chooses indices from the right (last ips). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#ip_header_index GoogleApigeeEnvironment#ip_header_index}
        :param ip_header_name: The name of the header to extract the client ip from. We are currently only supporting the X-Forwarded-For header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#ip_header_name GoogleApigeeEnvironment#ip_header_name}
        '''
        value = GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm(
            ip_header_index=ip_header_index, ip_header_name=ip_header_name
        )

        return typing.cast(None, jsii.invoke(self, "putHeaderIndexAlgorithm", [value]))

    @jsii.member(jsii_name="resetHeaderIndexAlgorithm")
    def reset_header_index_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderIndexAlgorithm", []))

    @builtins.property
    @jsii.member(jsii_name="headerIndexAlgorithm")
    def header_index_algorithm(
        self,
    ) -> GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithmOutputReference:
        return typing.cast(GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithmOutputReference, jsii.get(self, "headerIndexAlgorithm"))

    @builtins.property
    @jsii.member(jsii_name="headerIndexAlgorithmInput")
    def header_index_algorithm_input(
        self,
    ) -> typing.Optional[GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm]:
        return typing.cast(typing.Optional[GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm], jsii.get(self, "headerIndexAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeEnvironmentClientIpResolutionConfig]:
        return typing.cast(typing.Optional[GoogleApigeeEnvironmentClientIpResolutionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeEnvironmentClientIpResolutionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c74dd2533da22392a87375f9350701348c4e5ec735b534b51ab4429cc96d4d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeEnvironment.GoogleApigeeEnvironmentConfig",
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
        "org_id": "orgId",
        "api_proxy_type": "apiProxyType",
        "client_ip_resolution_config": "clientIpResolutionConfig",
        "deployment_type": "deploymentType",
        "description": "description",
        "display_name": "displayName",
        "forward_proxy_uri": "forwardProxyUri",
        "id": "id",
        "node_config": "nodeConfig",
        "properties": "properties",
        "timeouts": "timeouts",
        "type": "type",
    },
)
class GoogleApigeeEnvironmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        org_id: builtins.str,
        api_proxy_type: typing.Optional[builtins.str] = None,
        client_ip_resolution_config: typing.Optional[typing.Union[GoogleApigeeEnvironmentClientIpResolutionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        forward_proxy_uri: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        node_config: typing.Optional[typing.Union["GoogleApigeeEnvironmentNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Union["GoogleApigeeEnvironmentProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeEnvironmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The resource ID of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#name GoogleApigeeEnvironment#name}
        :param org_id: The Apigee Organization associated with the Apigee environment, in the format 'organizations/{{org_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#org_id GoogleApigeeEnvironment#org_id}
        :param api_proxy_type: Optional. API Proxy type supported by the environment. The type can be set when creating the Environment and cannot be changed. Possible values: ["API_PROXY_TYPE_UNSPECIFIED", "PROGRAMMABLE", "CONFIGURABLE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#api_proxy_type GoogleApigeeEnvironment#api_proxy_type}
        :param client_ip_resolution_config: client_ip_resolution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#client_ip_resolution_config GoogleApigeeEnvironment#client_ip_resolution_config}
        :param deployment_type: Optional. Deployment type supported by the environment. The deployment type can be set when creating the environment and cannot be changed. When you enable archive deployment, you will be prevented from performing a subset of actions within the environment, including: Managing the deployment of API proxy or shared flow revisions; Creating, updating, or deleting resource files; Creating, updating, or deleting target servers. Possible values: ["DEPLOYMENT_TYPE_UNSPECIFIED", "PROXY", "ARCHIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#deployment_type GoogleApigeeEnvironment#deployment_type}
        :param description: Description of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#description GoogleApigeeEnvironment#description}
        :param display_name: Display name of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#display_name GoogleApigeeEnvironment#display_name}
        :param forward_proxy_uri: Optional. URI of the forward proxy to be applied to the runtime instances in this environment. Must be in the format of {scheme}://{hostname}:{port}. Note that the scheme must be one of "http" or "https", and the port must be supplied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#forward_proxy_uri GoogleApigeeEnvironment#forward_proxy_uri}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#id GoogleApigeeEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#node_config GoogleApigeeEnvironment#node_config}
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#properties GoogleApigeeEnvironment#properties}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#timeouts GoogleApigeeEnvironment#timeouts}
        :param type: Types that can be selected for an Environment. Each of the types are limited by capability and capacity. Refer to Apigee's public documentation to understand about each of these types in details. An Apigee org can support heterogeneous Environments. Possible values: ["ENVIRONMENT_TYPE_UNSPECIFIED", "BASE", "INTERMEDIATE", "COMPREHENSIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#type GoogleApigeeEnvironment#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(client_ip_resolution_config, dict):
            client_ip_resolution_config = GoogleApigeeEnvironmentClientIpResolutionConfig(**client_ip_resolution_config)
        if isinstance(node_config, dict):
            node_config = GoogleApigeeEnvironmentNodeConfig(**node_config)
        if isinstance(properties, dict):
            properties = GoogleApigeeEnvironmentProperties(**properties)
        if isinstance(timeouts, dict):
            timeouts = GoogleApigeeEnvironmentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608c9cfb3d3d2d95732ed87959bb69e0eb41568b98851e08c05067e53aaada82)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument org_id", value=org_id, expected_type=type_hints["org_id"])
            check_type(argname="argument api_proxy_type", value=api_proxy_type, expected_type=type_hints["api_proxy_type"])
            check_type(argname="argument client_ip_resolution_config", value=client_ip_resolution_config, expected_type=type_hints["client_ip_resolution_config"])
            check_type(argname="argument deployment_type", value=deployment_type, expected_type=type_hints["deployment_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument forward_proxy_uri", value=forward_proxy_uri, expected_type=type_hints["forward_proxy_uri"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument node_config", value=node_config, expected_type=type_hints["node_config"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "org_id": org_id,
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
        if api_proxy_type is not None:
            self._values["api_proxy_type"] = api_proxy_type
        if client_ip_resolution_config is not None:
            self._values["client_ip_resolution_config"] = client_ip_resolution_config
        if deployment_type is not None:
            self._values["deployment_type"] = deployment_type
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if forward_proxy_uri is not None:
            self._values["forward_proxy_uri"] = forward_proxy_uri
        if id is not None:
            self._values["id"] = id
        if node_config is not None:
            self._values["node_config"] = node_config
        if properties is not None:
            self._values["properties"] = properties
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type is not None:
            self._values["type"] = type

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
        '''The resource ID of the environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#name GoogleApigeeEnvironment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def org_id(self) -> builtins.str:
        '''The Apigee Organization associated with the Apigee environment, in the format 'organizations/{{org_name}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#org_id GoogleApigeeEnvironment#org_id}
        '''
        result = self._values.get("org_id")
        assert result is not None, "Required property 'org_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_proxy_type(self) -> typing.Optional[builtins.str]:
        '''Optional.

        API Proxy type supported by the environment. The type can be set when creating
        the Environment and cannot be changed. Possible values: ["API_PROXY_TYPE_UNSPECIFIED", "PROGRAMMABLE", "CONFIGURABLE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#api_proxy_type GoogleApigeeEnvironment#api_proxy_type}
        '''
        result = self._values.get("api_proxy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_ip_resolution_config(
        self,
    ) -> typing.Optional[GoogleApigeeEnvironmentClientIpResolutionConfig]:
        '''client_ip_resolution_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#client_ip_resolution_config GoogleApigeeEnvironment#client_ip_resolution_config}
        '''
        result = self._values.get("client_ip_resolution_config")
        return typing.cast(typing.Optional[GoogleApigeeEnvironmentClientIpResolutionConfig], result)

    @builtins.property
    def deployment_type(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Deployment type supported by the environment. The deployment type can be
        set when creating the environment and cannot be changed. When you enable archive
        deployment, you will be prevented from performing a subset of actions within the
        environment, including:
        Managing the deployment of API proxy or shared flow revisions;
        Creating, updating, or deleting resource files;
        Creating, updating, or deleting target servers. Possible values: ["DEPLOYMENT_TYPE_UNSPECIFIED", "PROXY", "ARCHIVE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#deployment_type GoogleApigeeEnvironment#deployment_type}
        '''
        result = self._values.get("deployment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#description GoogleApigeeEnvironment#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Display name of the environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#display_name GoogleApigeeEnvironment#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forward_proxy_uri(self) -> typing.Optional[builtins.str]:
        '''Optional.

        URI of the forward proxy to be applied to the runtime instances in this environment. Must be in the format of {scheme}://{hostname}:{port}. Note that the scheme must be one of "http" or "https", and the port must be supplied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#forward_proxy_uri GoogleApigeeEnvironment#forward_proxy_uri}
        '''
        result = self._values.get("forward_proxy_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#id GoogleApigeeEnvironment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_config(self) -> typing.Optional["GoogleApigeeEnvironmentNodeConfig"]:
        '''node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#node_config GoogleApigeeEnvironment#node_config}
        '''
        result = self._values.get("node_config")
        return typing.cast(typing.Optional["GoogleApigeeEnvironmentNodeConfig"], result)

    @builtins.property
    def properties(self) -> typing.Optional["GoogleApigeeEnvironmentProperties"]:
        '''properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#properties GoogleApigeeEnvironment#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional["GoogleApigeeEnvironmentProperties"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleApigeeEnvironmentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#timeouts GoogleApigeeEnvironment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleApigeeEnvironmentTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Types that can be selected for an Environment.

        Each of the types are
        limited by capability and capacity. Refer to Apigee's public documentation
        to understand about each of these types in details.
        An Apigee org can support heterogeneous Environments. Possible values: ["ENVIRONMENT_TYPE_UNSPECIFIED", "BASE", "INTERMEDIATE", "COMPREHENSIVE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#type GoogleApigeeEnvironment#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeEnvironment.GoogleApigeeEnvironmentNodeConfig",
    jsii_struct_bases=[],
    name_mapping={"max_node_count": "maxNodeCount", "min_node_count": "minNodeCount"},
)
class GoogleApigeeEnvironmentNodeConfig:
    def __init__(
        self,
        *,
        max_node_count: typing.Optional[builtins.str] = None,
        min_node_count: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_node_count: The maximum total number of gateway nodes that the is reserved for all instances that has the specified environment. If not specified, the default is determined by the recommended maximum number of nodes for that gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#max_node_count GoogleApigeeEnvironment#max_node_count}
        :param min_node_count: The minimum total number of gateway nodes that the is reserved for all instances that has the specified environment. If not specified, the default is determined by the recommended minimum number of nodes for that gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#min_node_count GoogleApigeeEnvironment#min_node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__419c6bee219e3a8bc962bf8f375d5b6b430d5d038c07580bcab95ec8fa9e9739)
            check_type(argname="argument max_node_count", value=max_node_count, expected_type=type_hints["max_node_count"])
            check_type(argname="argument min_node_count", value=min_node_count, expected_type=type_hints["min_node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_node_count is not None:
            self._values["max_node_count"] = max_node_count
        if min_node_count is not None:
            self._values["min_node_count"] = min_node_count

    @builtins.property
    def max_node_count(self) -> typing.Optional[builtins.str]:
        '''The maximum total number of gateway nodes that the is reserved for all instances that has the specified environment.

        If not specified, the default is determined by the
        recommended maximum number of nodes for that gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#max_node_count GoogleApigeeEnvironment#max_node_count}
        '''
        result = self._values.get("max_node_count")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_node_count(self) -> typing.Optional[builtins.str]:
        '''The minimum total number of gateway nodes that the is reserved for all instances that has the specified environment.

        If not specified, the default is determined by the
        recommended minimum number of nodes for that gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#min_node_count GoogleApigeeEnvironment#min_node_count}
        '''
        result = self._values.get("min_node_count")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeEnvironmentNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeEnvironmentNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeEnvironment.GoogleApigeeEnvironmentNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76f4839f8c91d71377f4560e1dede8f89d3cb80f36d4778cbee73a4b2e72a34b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxNodeCount")
    def reset_max_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxNodeCount", []))

    @jsii.member(jsii_name="resetMinNodeCount")
    def reset_min_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinNodeCount", []))

    @builtins.property
    @jsii.member(jsii_name="currentAggregateNodeCount")
    def current_aggregate_node_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "currentAggregateNodeCount"))

    @builtins.property
    @jsii.member(jsii_name="maxNodeCountInput")
    def max_node_count_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodeCountInput")
    def min_node_count_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNodeCount")
    def max_node_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxNodeCount"))

    @max_node_count.setter
    def max_node_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adaa05409bdb142e7ee3580bb5edc79ce324f629bd7526de3e24cf3f19c7cb42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac0b28733b451898c59902676c4ce8a687e3253eeee41b70827ba43daf6baa04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleApigeeEnvironmentNodeConfig]:
        return typing.cast(typing.Optional[GoogleApigeeEnvironmentNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeEnvironmentNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1865638991698951fb52402efb4cc9d9edb2257985a3794a673ca98cecb4459)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeEnvironment.GoogleApigeeEnvironmentProperties",
    jsii_struct_bases=[],
    name_mapping={"property": "property"},
)
class GoogleApigeeEnvironmentProperties:
    def __init__(
        self,
        *,
        property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeEnvironmentPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param property: property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#property GoogleApigeeEnvironment#property}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f3cb6c5ce4c1eee575211a0641913dd4a590ce3a2d5d4d302b34f25cdf42ff)
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if property is not None:
            self._values["property"] = property

    @builtins.property
    def property(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeEnvironmentPropertiesProperty"]]]:
        '''property block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#property GoogleApigeeEnvironment#property}
        '''
        result = self._values.get("property")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeEnvironmentPropertiesProperty"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeEnvironmentProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeEnvironmentPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeEnvironment.GoogleApigeeEnvironmentPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22ae018ec4840c71c376ea946aaf31c3670ecae5e9bd19f8683e872b09cb276f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProperty")
    def put_property(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeEnvironmentPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c6c279a7d0c1f4c41acd5a9e27f7959c081ad15bfd37e222033357facaad25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProperty", [value]))

    @jsii.member(jsii_name="resetProperty")
    def reset_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperty", []))

    @builtins.property
    @jsii.member(jsii_name="property")
    def property(self) -> "GoogleApigeeEnvironmentPropertiesPropertyList":
        return typing.cast("GoogleApigeeEnvironmentPropertiesPropertyList", jsii.get(self, "property"))

    @builtins.property
    @jsii.member(jsii_name="propertyInput")
    def property_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeEnvironmentPropertiesProperty"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeEnvironmentPropertiesProperty"]]], jsii.get(self, "propertyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleApigeeEnvironmentProperties]:
        return typing.cast(typing.Optional[GoogleApigeeEnvironmentProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeEnvironmentProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b0ff91ab8141b03021a1def8806678e7161e6e3fc725559d1ec23661932f76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeEnvironment.GoogleApigeeEnvironmentPropertiesProperty",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleApigeeEnvironmentPropertiesProperty:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The property key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#name GoogleApigeeEnvironment#name}
        :param value: The property value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#value GoogleApigeeEnvironment#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b627d3a12d5499ce2db6ce787d7c45df3a5534036d8f91beb622413129466a01)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The property key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#name GoogleApigeeEnvironment#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The property value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#value GoogleApigeeEnvironment#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeEnvironmentPropertiesProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeEnvironmentPropertiesPropertyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeEnvironment.GoogleApigeeEnvironmentPropertiesPropertyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__166dd0e23f8addf0f60ef1521a09c54ee567bf37f976898ed2d8bd442f430fe2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApigeeEnvironmentPropertiesPropertyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cad7bc21a99ca0431b57341d8498edccdac15949e758b7fa24f2b4d57f0fd7b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApigeeEnvironmentPropertiesPropertyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ec024560bcda4bacfd2487e31e3cff21683d836ef637b2f09925968a795c92)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e56a1401d1a9da7ac45fbe1c444de0738d66fbf7697555878f112a5426efefed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ad79a5e80cdb3d897be990407f684427defa65d235ea4addb7e746ce2ab0efa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeEnvironmentPropertiesProperty]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeEnvironmentPropertiesProperty]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeEnvironmentPropertiesProperty]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e178289401e06d08bc4b34cbe0661ff59320180e583e882f95b1aaa9e2fac6be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeEnvironmentPropertiesPropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeEnvironment.GoogleApigeeEnvironmentPropertiesPropertyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0453585c201490aca94fd72737cf4165098e79cf14dc50102087fd512210b4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__027ccca41b476bc85882124f5500b8c326a21fa9b341b88002755aef7ba98d42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b0beb5e342155619c39fa8fe19e7ba0f3423ce64350076e1311f4edf1963b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeEnvironmentPropertiesProperty]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeEnvironmentPropertiesProperty]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeEnvironmentPropertiesProperty]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__613cdd3666d95d2fe68a2fd9d27618d28802ee1915d2ba26f6aa45ee17dd4073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeEnvironment.GoogleApigeeEnvironmentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleApigeeEnvironmentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#create GoogleApigeeEnvironment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#delete GoogleApigeeEnvironment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#update GoogleApigeeEnvironment#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d80cf1891bc570563ab62c6caab70aa24c2abb605c18776e8ab839bdadb79827)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#create GoogleApigeeEnvironment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#delete GoogleApigeeEnvironment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_environment#update GoogleApigeeEnvironment#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeEnvironmentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeEnvironmentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeEnvironment.GoogleApigeeEnvironmentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee74c3345af536a5ae0bd39e1e4a21f205da5d11ecbb3d0242d04fa3a13b0a58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0668a20e1872afc1a6b8797ab28d0ec1cff6794753809d648eb9b2050a7e4b9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94bcabd02bcc1aa1aa9d03daf2ca577014716570028fb45617c0bd87b71033c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__527508aac9795eeac563eee20d76d9fdf4ff761b9636465013525057d0c37277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeEnvironmentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeEnvironmentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeEnvironmentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84baeb07bdcc88cc99b675330fc20f29346b9d0c4882c7b7312fae03f9160e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleApigeeEnvironment",
    "GoogleApigeeEnvironmentClientIpResolutionConfig",
    "GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm",
    "GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithmOutputReference",
    "GoogleApigeeEnvironmentClientIpResolutionConfigOutputReference",
    "GoogleApigeeEnvironmentConfig",
    "GoogleApigeeEnvironmentNodeConfig",
    "GoogleApigeeEnvironmentNodeConfigOutputReference",
    "GoogleApigeeEnvironmentProperties",
    "GoogleApigeeEnvironmentPropertiesOutputReference",
    "GoogleApigeeEnvironmentPropertiesProperty",
    "GoogleApigeeEnvironmentPropertiesPropertyList",
    "GoogleApigeeEnvironmentPropertiesPropertyOutputReference",
    "GoogleApigeeEnvironmentTimeouts",
    "GoogleApigeeEnvironmentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0cc229540176c799051ab83314c246b0d7b10ccfddf834fc7f47c376be6f71fa(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    org_id: builtins.str,
    api_proxy_type: typing.Optional[builtins.str] = None,
    client_ip_resolution_config: typing.Optional[typing.Union[GoogleApigeeEnvironmentClientIpResolutionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    forward_proxy_uri: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    node_config: typing.Optional[typing.Union[GoogleApigeeEnvironmentNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    properties: typing.Optional[typing.Union[GoogleApigeeEnvironmentProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeEnvironmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__63b8b5b9255d8bb9ad208889b6fec1af55a6816ae7d5a3dcf8882a40b62e722b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1685eb760562e23b2ad8db817d9ab14e81be9ac69a6b56cacfd0d073608dfb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5cb2a5460e1c69b4cd86003adbd1b991526ac204803309885ec04b761d85c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc645b061b4a35ad8761634c568bd131a48ed5e439f2c9dbf393423cd33a863(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f4c49a80bee3f95285cb739ef55a71ad7bea287cf20d3a95d916fced4052e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d95f942a5122042687d0d1118d408a70a906c3f621f10d1354aa82b783ce76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d129cf7ec82c3e06bb7b32f06410ae575c245f4f0facb60685f214cac4dfbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c65201fbba5cbeae5520844a9acb42dcdc5b3f649e2d705ad995207cbef426(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a09578d2728632935747cdbb554f7c14a7d85600382d4cbd62924aa511b319aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506311c403c8da86b06dcb5b02287378f948845d64bab47a4df384acd5d4da72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a35caf397f165e71d3495a4d44ce9c84d38784e8ac710682c08cb81a9e882f5(
    *,
    header_index_algorithm: typing.Optional[typing.Union[GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269e028193115b8fc075c36f12363f7a0f0a690f92b86b35ee2d6dc2d4504c77(
    *,
    ip_header_index: jsii.Number,
    ip_header_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783000f33c677b9568b18bb0df018bad5f69bbcab9c4d59b8028621983cf5625(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a3aa706081c627d1cadc21f7911c7710145d531a8cc9ce008f41443fa53a8a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b28795cf50487c5c5b9f37bed834eaa2ffbc47e359901f4459b43cf967ad63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492fd241cecc06af9c3047604be4b3f71a0db990de1de7c35a755d7ac9bae99c(
    value: typing.Optional[GoogleApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636d5c7d87558f54b26708267839f908dd04fa11417e18bc3a049855208387df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74dd2533da22392a87375f9350701348c4e5ec735b534b51ab4429cc96d4d79(
    value: typing.Optional[GoogleApigeeEnvironmentClientIpResolutionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608c9cfb3d3d2d95732ed87959bb69e0eb41568b98851e08c05067e53aaada82(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    org_id: builtins.str,
    api_proxy_type: typing.Optional[builtins.str] = None,
    client_ip_resolution_config: typing.Optional[typing.Union[GoogleApigeeEnvironmentClientIpResolutionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    forward_proxy_uri: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    node_config: typing.Optional[typing.Union[GoogleApigeeEnvironmentNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    properties: typing.Optional[typing.Union[GoogleApigeeEnvironmentProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeEnvironmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__419c6bee219e3a8bc962bf8f375d5b6b430d5d038c07580bcab95ec8fa9e9739(
    *,
    max_node_count: typing.Optional[builtins.str] = None,
    min_node_count: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f4839f8c91d71377f4560e1dede8f89d3cb80f36d4778cbee73a4b2e72a34b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adaa05409bdb142e7ee3580bb5edc79ce324f629bd7526de3e24cf3f19c7cb42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac0b28733b451898c59902676c4ce8a687e3253eeee41b70827ba43daf6baa04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1865638991698951fb52402efb4cc9d9edb2257985a3794a673ca98cecb4459(
    value: typing.Optional[GoogleApigeeEnvironmentNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f3cb6c5ce4c1eee575211a0641913dd4a590ce3a2d5d4d302b34f25cdf42ff(
    *,
    property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeEnvironmentPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ae018ec4840c71c376ea946aaf31c3670ecae5e9bd19f8683e872b09cb276f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c6c279a7d0c1f4c41acd5a9e27f7959c081ad15bfd37e222033357facaad25(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeEnvironmentPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b0ff91ab8141b03021a1def8806678e7161e6e3fc725559d1ec23661932f76(
    value: typing.Optional[GoogleApigeeEnvironmentProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b627d3a12d5499ce2db6ce787d7c45df3a5534036d8f91beb622413129466a01(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__166dd0e23f8addf0f60ef1521a09c54ee567bf37f976898ed2d8bd442f430fe2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cad7bc21a99ca0431b57341d8498edccdac15949e758b7fa24f2b4d57f0fd7b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ec024560bcda4bacfd2487e31e3cff21683d836ef637b2f09925968a795c92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e56a1401d1a9da7ac45fbe1c444de0738d66fbf7697555878f112a5426efefed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad79a5e80cdb3d897be990407f684427defa65d235ea4addb7e746ce2ab0efa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e178289401e06d08bc4b34cbe0661ff59320180e583e882f95b1aaa9e2fac6be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeEnvironmentPropertiesProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0453585c201490aca94fd72737cf4165098e79cf14dc50102087fd512210b4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__027ccca41b476bc85882124f5500b8c326a21fa9b341b88002755aef7ba98d42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b0beb5e342155619c39fa8fe19e7ba0f3423ce64350076e1311f4edf1963b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613cdd3666d95d2fe68a2fd9d27618d28802ee1915d2ba26f6aa45ee17dd4073(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeEnvironmentPropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d80cf1891bc570563ab62c6caab70aa24c2abb605c18776e8ab839bdadb79827(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee74c3345af536a5ae0bd39e1e4a21f205da5d11ecbb3d0242d04fa3a13b0a58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0668a20e1872afc1a6b8797ab28d0ec1cff6794753809d648eb9b2050a7e4b9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94bcabd02bcc1aa1aa9d03daf2ca577014716570028fb45617c0bd87b71033c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527508aac9795eeac563eee20d76d9fdf4ff761b9636465013525057d0c37277(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84baeb07bdcc88cc99b675330fc20f29346b9d0c4882c7b7312fae03f9160e75(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeEnvironmentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

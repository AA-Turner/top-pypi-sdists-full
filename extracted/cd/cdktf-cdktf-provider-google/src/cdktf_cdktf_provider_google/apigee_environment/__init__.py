r'''
# `google_apigee_environment`

Refer to the Terraform Registry for docs: [`google_apigee_environment`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment).
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


class ApigeeEnvironment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeEnvironment.ApigeeEnvironment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment google_apigee_environment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        org_id: builtins.str,
        api_proxy_type: typing.Optional[builtins.str] = None,
        client_ip_resolution_config: typing.Optional[typing.Union["ApigeeEnvironmentClientIpResolutionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        forward_proxy_uri: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        node_config: typing.Optional[typing.Union["ApigeeEnvironmentNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Union["ApigeeEnvironmentProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ApigeeEnvironmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment google_apigee_environment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The resource ID of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#name ApigeeEnvironment#name}
        :param org_id: The Apigee Organization associated with the Apigee environment, in the format 'organizations/{{org_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#org_id ApigeeEnvironment#org_id}
        :param api_proxy_type: Optional. API Proxy type supported by the environment. The type can be set when creating the Environment and cannot be changed. Possible values: ["API_PROXY_TYPE_UNSPECIFIED", "PROGRAMMABLE", "CONFIGURABLE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#api_proxy_type ApigeeEnvironment#api_proxy_type}
        :param client_ip_resolution_config: client_ip_resolution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#client_ip_resolution_config ApigeeEnvironment#client_ip_resolution_config}
        :param deployment_type: Optional. Deployment type supported by the environment. The deployment type can be set when creating the environment and cannot be changed. When you enable archive deployment, you will be prevented from performing a subset of actions within the environment, including: Managing the deployment of API proxy or shared flow revisions; Creating, updating, or deleting resource files; Creating, updating, or deleting target servers. Possible values: ["DEPLOYMENT_TYPE_UNSPECIFIED", "PROXY", "ARCHIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#deployment_type ApigeeEnvironment#deployment_type}
        :param description: Description of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#description ApigeeEnvironment#description}
        :param display_name: Display name of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#display_name ApigeeEnvironment#display_name}
        :param forward_proxy_uri: Optional. URI of the forward proxy to be applied to the runtime instances in this environment. Must be in the format of {scheme}://{hostname}:{port}. Note that the scheme must be one of "http" or "https", and the port must be supplied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#forward_proxy_uri ApigeeEnvironment#forward_proxy_uri}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#id ApigeeEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#node_config ApigeeEnvironment#node_config}
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#properties ApigeeEnvironment#properties}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#timeouts ApigeeEnvironment#timeouts}
        :param type: Types that can be selected for an Environment. Each of the types are limited by capability and capacity. Refer to Apigee's public documentation to understand about each of these types in details. An Apigee org can support heterogeneous Environments. Possible values: ["ENVIRONMENT_TYPE_UNSPECIFIED", "BASE", "INTERMEDIATE", "COMPREHENSIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#type ApigeeEnvironment#type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea40fd31858cddb5d1fe77fda8ff1648ead93d911063b38b92c8655585d84048)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApigeeEnvironmentConfig(
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
        '''Generates CDKTF code for importing a ApigeeEnvironment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApigeeEnvironment to import.
        :param import_from_id: The id of the existing ApigeeEnvironment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApigeeEnvironment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e1cb8b9709aa97edb7af63f3ae4c0334305a722dd36c555e209e0e8a60744f5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putClientIpResolutionConfig")
    def put_client_ip_resolution_config(
        self,
        *,
        header_index_algorithm: typing.Optional[typing.Union["ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param header_index_algorithm: header_index_algorithm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#header_index_algorithm ApigeeEnvironment#header_index_algorithm}
        '''
        value = ApigeeEnvironmentClientIpResolutionConfig(
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
        :param max_node_count: The maximum total number of gateway nodes that the is reserved for all instances that has the specified environment. If not specified, the default is determined by the recommended maximum number of nodes for that gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#max_node_count ApigeeEnvironment#max_node_count}
        :param min_node_count: The minimum total number of gateway nodes that the is reserved for all instances that has the specified environment. If not specified, the default is determined by the recommended minimum number of nodes for that gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#min_node_count ApigeeEnvironment#min_node_count}
        '''
        value = ApigeeEnvironmentNodeConfig(
            max_node_count=max_node_count, min_node_count=min_node_count
        )

        return typing.cast(None, jsii.invoke(self, "putNodeConfig", [value]))

    @jsii.member(jsii_name="putProperties")
    def put_properties(
        self,
        *,
        property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeEnvironmentPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param property: property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#property ApigeeEnvironment#property}
        '''
        value = ApigeeEnvironmentProperties(property=property)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#create ApigeeEnvironment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#delete ApigeeEnvironment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#update ApigeeEnvironment#update}.
        '''
        value = ApigeeEnvironmentTimeouts(create=create, delete=delete, update=update)

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
    ) -> "ApigeeEnvironmentClientIpResolutionConfigOutputReference":
        return typing.cast("ApigeeEnvironmentClientIpResolutionConfigOutputReference", jsii.get(self, "clientIpResolutionConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(self) -> "ApigeeEnvironmentNodeConfigOutputReference":
        return typing.cast("ApigeeEnvironmentNodeConfigOutputReference", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> "ApigeeEnvironmentPropertiesOutputReference":
        return typing.cast("ApigeeEnvironmentPropertiesOutputReference", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApigeeEnvironmentTimeoutsOutputReference":
        return typing.cast("ApigeeEnvironmentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="apiProxyTypeInput")
    def api_proxy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiProxyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIpResolutionConfigInput")
    def client_ip_resolution_config_input(
        self,
    ) -> typing.Optional["ApigeeEnvironmentClientIpResolutionConfig"]:
        return typing.cast(typing.Optional["ApigeeEnvironmentClientIpResolutionConfig"], jsii.get(self, "clientIpResolutionConfigInput"))

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
    def node_config_input(self) -> typing.Optional["ApigeeEnvironmentNodeConfig"]:
        return typing.cast(typing.Optional["ApigeeEnvironmentNodeConfig"], jsii.get(self, "nodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="orgIdInput")
    def org_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgIdInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(self) -> typing.Optional["ApigeeEnvironmentProperties"]:
        return typing.cast(typing.Optional["ApigeeEnvironmentProperties"], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeEnvironmentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeEnvironmentTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c93877eb500997420989ea9411ad5e6f4d2c4925647525d0ac5f81c3377a96ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiProxyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentType")
    def deployment_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentType"))

    @deployment_type.setter
    def deployment_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27cf9464dfb610d11ebef6abf029c8283b874bf7020b5da3f42ea5b9f1bb0312)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac76252e9c60f16d9f557c75242b6e1fb8f14b1ce9c88b6e2c60e3b57d8a251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb09040be2fcdfa8569782a9ec69a6451a27b3a7ccd243f7d69a7bf404aa4b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardProxyUri")
    def forward_proxy_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardProxyUri"))

    @forward_proxy_uri.setter
    def forward_proxy_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b06dfd999fa12b03f0d198d75b4b1e9afab2f06b00d8bfa5678a6208458a4dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardProxyUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c282aa2880eab71bf50704657706615733980ad25a353c0045216062ed3c55ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14f5243bd6e710e6138dc8044e94e6a54c54ea058d3e4de2ee823726351f44f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @org_id.setter
    def org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__375b29c2909509123d38f426b52dc31d2e0aae4b5d97a9b74467fdeb13fd4d25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ee83fd149c306745fcb0902da78d3bedd7359a6051972b1f3a571071321f11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeEnvironment.ApigeeEnvironmentClientIpResolutionConfig",
    jsii_struct_bases=[],
    name_mapping={"header_index_algorithm": "headerIndexAlgorithm"},
)
class ApigeeEnvironmentClientIpResolutionConfig:
    def __init__(
        self,
        *,
        header_index_algorithm: typing.Optional[typing.Union["ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param header_index_algorithm: header_index_algorithm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#header_index_algorithm ApigeeEnvironment#header_index_algorithm}
        '''
        if isinstance(header_index_algorithm, dict):
            header_index_algorithm = ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm(**header_index_algorithm)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99cb417c890e51b89a693ce0858aac7fb6a0fc31474c0480ad87b948e2f1f9fd)
            check_type(argname="argument header_index_algorithm", value=header_index_algorithm, expected_type=type_hints["header_index_algorithm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_index_algorithm is not None:
            self._values["header_index_algorithm"] = header_index_algorithm

    @builtins.property
    def header_index_algorithm(
        self,
    ) -> typing.Optional["ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm"]:
        '''header_index_algorithm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#header_index_algorithm ApigeeEnvironment#header_index_algorithm}
        '''
        result = self._values.get("header_index_algorithm")
        return typing.cast(typing.Optional["ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeEnvironmentClientIpResolutionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeEnvironment.ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm",
    jsii_struct_bases=[],
    name_mapping={
        "ip_header_index": "ipHeaderIndex",
        "ip_header_name": "ipHeaderName",
    },
)
class ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm:
    def __init__(
        self,
        *,
        ip_header_index: jsii.Number,
        ip_header_name: builtins.str,
    ) -> None:
        '''
        :param ip_header_index: The index of the ip in the header. Positive indices 0, 1, 2, 3 chooses indices from the left (first ips). Negative indices -1, -2, -3 chooses indices from the right (last ips). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#ip_header_index ApigeeEnvironment#ip_header_index}
        :param ip_header_name: The name of the header to extract the client ip from. We are currently only supporting the X-Forwarded-For header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#ip_header_name ApigeeEnvironment#ip_header_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6cea53c655efefd2839c6fb3e8b234c046e973c7c6c9555fed5e51bd8fce4c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#ip_header_index ApigeeEnvironment#ip_header_index}
        '''
        result = self._values.get("ip_header_index")
        assert result is not None, "Required property 'ip_header_index' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def ip_header_name(self) -> builtins.str:
        '''The name of the header to extract the client ip from. We are currently only supporting the X-Forwarded-For header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#ip_header_name ApigeeEnvironment#ip_header_name}
        '''
        result = self._values.get("ip_header_name")
        assert result is not None, "Required property 'ip_header_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeEnvironment.ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83255040095d9af6e5e37608a954361c832b9d8017cd0ec33a8ffff3820d587b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74fefb2c67ca92cc916b2186e82b0257e401eb40d6c21094da5426748d27edff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipHeaderIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipHeaderName")
    def ip_header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipHeaderName"))

    @ip_header_name.setter
    def ip_header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e23cb9e01669f0ce079dcee741f91771ff942a4432348a4d5af2688d8ddf6ec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm]:
        return typing.cast(typing.Optional[ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e405f97e3f54c63be5ee65bb8540764e6bafd0af3138230870f53e94ab003c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeEnvironmentClientIpResolutionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeEnvironment.ApigeeEnvironmentClientIpResolutionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f32c6732ccd6f3cdd7098c9ed641eaa1088ce1ea5aaad0296db4d2fe42f9611)
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
        :param ip_header_index: The index of the ip in the header. Positive indices 0, 1, 2, 3 chooses indices from the left (first ips). Negative indices -1, -2, -3 chooses indices from the right (last ips). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#ip_header_index ApigeeEnvironment#ip_header_index}
        :param ip_header_name: The name of the header to extract the client ip from. We are currently only supporting the X-Forwarded-For header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#ip_header_name ApigeeEnvironment#ip_header_name}
        '''
        value = ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm(
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
    ) -> ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithmOutputReference:
        return typing.cast(ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithmOutputReference, jsii.get(self, "headerIndexAlgorithm"))

    @builtins.property
    @jsii.member(jsii_name="headerIndexAlgorithmInput")
    def header_index_algorithm_input(
        self,
    ) -> typing.Optional[ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm]:
        return typing.cast(typing.Optional[ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm], jsii.get(self, "headerIndexAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApigeeEnvironmentClientIpResolutionConfig]:
        return typing.cast(typing.Optional[ApigeeEnvironmentClientIpResolutionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeEnvironmentClientIpResolutionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e58b2c542e180d95b79bb3f2e14b8b2b523a72c7f7bd94110872d76e8eb980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeEnvironment.ApigeeEnvironmentConfig",
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
class ApigeeEnvironmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        client_ip_resolution_config: typing.Optional[typing.Union[ApigeeEnvironmentClientIpResolutionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        forward_proxy_uri: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        node_config: typing.Optional[typing.Union["ApigeeEnvironmentNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Union["ApigeeEnvironmentProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ApigeeEnvironmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: The resource ID of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#name ApigeeEnvironment#name}
        :param org_id: The Apigee Organization associated with the Apigee environment, in the format 'organizations/{{org_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#org_id ApigeeEnvironment#org_id}
        :param api_proxy_type: Optional. API Proxy type supported by the environment. The type can be set when creating the Environment and cannot be changed. Possible values: ["API_PROXY_TYPE_UNSPECIFIED", "PROGRAMMABLE", "CONFIGURABLE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#api_proxy_type ApigeeEnvironment#api_proxy_type}
        :param client_ip_resolution_config: client_ip_resolution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#client_ip_resolution_config ApigeeEnvironment#client_ip_resolution_config}
        :param deployment_type: Optional. Deployment type supported by the environment. The deployment type can be set when creating the environment and cannot be changed. When you enable archive deployment, you will be prevented from performing a subset of actions within the environment, including: Managing the deployment of API proxy or shared flow revisions; Creating, updating, or deleting resource files; Creating, updating, or deleting target servers. Possible values: ["DEPLOYMENT_TYPE_UNSPECIFIED", "PROXY", "ARCHIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#deployment_type ApigeeEnvironment#deployment_type}
        :param description: Description of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#description ApigeeEnvironment#description}
        :param display_name: Display name of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#display_name ApigeeEnvironment#display_name}
        :param forward_proxy_uri: Optional. URI of the forward proxy to be applied to the runtime instances in this environment. Must be in the format of {scheme}://{hostname}:{port}. Note that the scheme must be one of "http" or "https", and the port must be supplied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#forward_proxy_uri ApigeeEnvironment#forward_proxy_uri}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#id ApigeeEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#node_config ApigeeEnvironment#node_config}
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#properties ApigeeEnvironment#properties}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#timeouts ApigeeEnvironment#timeouts}
        :param type: Types that can be selected for an Environment. Each of the types are limited by capability and capacity. Refer to Apigee's public documentation to understand about each of these types in details. An Apigee org can support heterogeneous Environments. Possible values: ["ENVIRONMENT_TYPE_UNSPECIFIED", "BASE", "INTERMEDIATE", "COMPREHENSIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#type ApigeeEnvironment#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(client_ip_resolution_config, dict):
            client_ip_resolution_config = ApigeeEnvironmentClientIpResolutionConfig(**client_ip_resolution_config)
        if isinstance(node_config, dict):
            node_config = ApigeeEnvironmentNodeConfig(**node_config)
        if isinstance(properties, dict):
            properties = ApigeeEnvironmentProperties(**properties)
        if isinstance(timeouts, dict):
            timeouts = ApigeeEnvironmentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f606507ccdfee0f97787f22694fe38b5b722ab3d633647d75847a2aa1654b58)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#name ApigeeEnvironment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def org_id(self) -> builtins.str:
        '''The Apigee Organization associated with the Apigee environment, in the format 'organizations/{{org_name}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#org_id ApigeeEnvironment#org_id}
        '''
        result = self._values.get("org_id")
        assert result is not None, "Required property 'org_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_proxy_type(self) -> typing.Optional[builtins.str]:
        '''Optional.

        API Proxy type supported by the environment. The type can be set when creating
        the Environment and cannot be changed. Possible values: ["API_PROXY_TYPE_UNSPECIFIED", "PROGRAMMABLE", "CONFIGURABLE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#api_proxy_type ApigeeEnvironment#api_proxy_type}
        '''
        result = self._values.get("api_proxy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_ip_resolution_config(
        self,
    ) -> typing.Optional[ApigeeEnvironmentClientIpResolutionConfig]:
        '''client_ip_resolution_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#client_ip_resolution_config ApigeeEnvironment#client_ip_resolution_config}
        '''
        result = self._values.get("client_ip_resolution_config")
        return typing.cast(typing.Optional[ApigeeEnvironmentClientIpResolutionConfig], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#deployment_type ApigeeEnvironment#deployment_type}
        '''
        result = self._values.get("deployment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#description ApigeeEnvironment#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Display name of the environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#display_name ApigeeEnvironment#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forward_proxy_uri(self) -> typing.Optional[builtins.str]:
        '''Optional.

        URI of the forward proxy to be applied to the runtime instances in this environment. Must be in the format of {scheme}://{hostname}:{port}. Note that the scheme must be one of "http" or "https", and the port must be supplied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#forward_proxy_uri ApigeeEnvironment#forward_proxy_uri}
        '''
        result = self._values.get("forward_proxy_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#id ApigeeEnvironment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_config(self) -> typing.Optional["ApigeeEnvironmentNodeConfig"]:
        '''node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#node_config ApigeeEnvironment#node_config}
        '''
        result = self._values.get("node_config")
        return typing.cast(typing.Optional["ApigeeEnvironmentNodeConfig"], result)

    @builtins.property
    def properties(self) -> typing.Optional["ApigeeEnvironmentProperties"]:
        '''properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#properties ApigeeEnvironment#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional["ApigeeEnvironmentProperties"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApigeeEnvironmentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#timeouts ApigeeEnvironment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApigeeEnvironmentTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Types that can be selected for an Environment.

        Each of the types are
        limited by capability and capacity. Refer to Apigee's public documentation
        to understand about each of these types in details.
        An Apigee org can support heterogeneous Environments. Possible values: ["ENVIRONMENT_TYPE_UNSPECIFIED", "BASE", "INTERMEDIATE", "COMPREHENSIVE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#type ApigeeEnvironment#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeEnvironment.ApigeeEnvironmentNodeConfig",
    jsii_struct_bases=[],
    name_mapping={"max_node_count": "maxNodeCount", "min_node_count": "minNodeCount"},
)
class ApigeeEnvironmentNodeConfig:
    def __init__(
        self,
        *,
        max_node_count: typing.Optional[builtins.str] = None,
        min_node_count: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_node_count: The maximum total number of gateway nodes that the is reserved for all instances that has the specified environment. If not specified, the default is determined by the recommended maximum number of nodes for that gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#max_node_count ApigeeEnvironment#max_node_count}
        :param min_node_count: The minimum total number of gateway nodes that the is reserved for all instances that has the specified environment. If not specified, the default is determined by the recommended minimum number of nodes for that gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#min_node_count ApigeeEnvironment#min_node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a95ec9ecc2d1bb7caf18c1be31f3afbe226f3021885101ae2dc107a30f851ff)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#max_node_count ApigeeEnvironment#max_node_count}
        '''
        result = self._values.get("max_node_count")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_node_count(self) -> typing.Optional[builtins.str]:
        '''The minimum total number of gateway nodes that the is reserved for all instances that has the specified environment.

        If not specified, the default is determined by the
        recommended minimum number of nodes for that gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#min_node_count ApigeeEnvironment#min_node_count}
        '''
        result = self._values.get("min_node_count")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeEnvironmentNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeEnvironmentNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeEnvironment.ApigeeEnvironmentNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b040eec67a46b48ac2027d313bbecef9283f6356fef82bb183e146a40e09c203)
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
            type_hints = typing.get_type_hints(_typecheckingstub__830f99cdde4f34ec17c60de93022421c02b796d057b8b6e9e4fcba9d77a61a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff66f199dd6f353b49ebd56c185da2ff06094a33dd19c1aca937650e6046e05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigeeEnvironmentNodeConfig]:
        return typing.cast(typing.Optional[ApigeeEnvironmentNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeEnvironmentNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a8eb2e0ec05f871b7711144c0b12ec55c84290b15a9973bf9bae6aeb8c33ca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeEnvironment.ApigeeEnvironmentProperties",
    jsii_struct_bases=[],
    name_mapping={"property": "property"},
)
class ApigeeEnvironmentProperties:
    def __init__(
        self,
        *,
        property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeEnvironmentPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param property: property block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#property ApigeeEnvironment#property}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69eb44385d1ce4142ef861a0866da18fbb39b1846206d37036722d7567d31656)
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if property is not None:
            self._values["property"] = property

    @builtins.property
    def property(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeEnvironmentPropertiesProperty"]]]:
        '''property block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#property ApigeeEnvironment#property}
        '''
        result = self._values.get("property")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeEnvironmentPropertiesProperty"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeEnvironmentProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeEnvironmentPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeEnvironment.ApigeeEnvironmentPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f1991b84bb951977262412b0444bc2aaa3e4931faff6c11cdc102909a6e6b69)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProperty")
    def put_property(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeEnvironmentPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa503384d2900c1bbb6d31f7e4b12a83f4701392bf3064da63675c6c66dfa7e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProperty", [value]))

    @jsii.member(jsii_name="resetProperty")
    def reset_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperty", []))

    @builtins.property
    @jsii.member(jsii_name="property")
    def property(self) -> "ApigeeEnvironmentPropertiesPropertyList":
        return typing.cast("ApigeeEnvironmentPropertiesPropertyList", jsii.get(self, "property"))

    @builtins.property
    @jsii.member(jsii_name="propertyInput")
    def property_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeEnvironmentPropertiesProperty"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeEnvironmentPropertiesProperty"]]], jsii.get(self, "propertyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigeeEnvironmentProperties]:
        return typing.cast(typing.Optional[ApigeeEnvironmentProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeEnvironmentProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c391549e911b7339c6199b06948481808fcee71f739e9340f28e95b7bc19e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeEnvironment.ApigeeEnvironmentPropertiesProperty",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ApigeeEnvironmentPropertiesProperty:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The property key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#name ApigeeEnvironment#name}
        :param value: The property value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#value ApigeeEnvironment#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35daf95d822c812562b40f8442c102b44af8de1635982f166d2f3aa29debbfce)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#name ApigeeEnvironment#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The property value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#value ApigeeEnvironment#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeEnvironmentPropertiesProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeEnvironmentPropertiesPropertyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeEnvironment.ApigeeEnvironmentPropertiesPropertyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb5159c98a2467ffa6e6992628e975c4c7c012476e81f0d54af210d68a2d96f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigeeEnvironmentPropertiesPropertyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc28fc33e5a0fb3884ef83a638b9f92ff996c082b65c91dffc62909ab896103b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigeeEnvironmentPropertiesPropertyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7984117201b20f0dc4b2df2268acdd0ea2025ccd2ab7b57e552d86829c7d9c88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ed7eaa13f9f5ea72c1d146df2428ea6699bd2fd0ca85efb553b3724fff934c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27e24591bef24f260ecb0d42240c8e28ad2c2e8aa56e96df081885d211fbbca6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeEnvironmentPropertiesProperty]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeEnvironmentPropertiesProperty]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeEnvironmentPropertiesProperty]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da02e24f3146db6ccb9c259633c9076e6cf8f01b84fec386f2a2e5dc59c2c88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeEnvironmentPropertiesPropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeEnvironment.ApigeeEnvironmentPropertiesPropertyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af591c178019e22130cae8e079f989d540276f37fae5d840187a565a3e49f5ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0772be1f0d8eb52e98e29bd27b4cbca89f980f7187a9f20e98b78c01cef5cd9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d440cc1d26c442e5377fb75dec86e1d78c13350d404eedcddb787159c1d2e155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeEnvironmentPropertiesProperty]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeEnvironmentPropertiesProperty]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeEnvironmentPropertiesProperty]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4196551d279c10022f370a4c14c2c8c8c323149906a6690710ba7467fbd5d301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeEnvironment.ApigeeEnvironmentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ApigeeEnvironmentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#create ApigeeEnvironment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#delete ApigeeEnvironment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#update ApigeeEnvironment#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cbc1abd5c6ec607e51a9d7dc1f434de3d78e2bac53745e33bce355bd0c23e0c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#create ApigeeEnvironment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#delete ApigeeEnvironment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_environment#update ApigeeEnvironment#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeEnvironmentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeEnvironmentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeEnvironment.ApigeeEnvironmentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9c087ff0fe7f805a16436503d9957ca9c6f403282fc3a635dfd547871f305a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__008baed70f93e7e9e6de872d8f7dc286c1c0b00f3822b4ab225b272927b89a3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014a2de760b6ca4279ab22a064c6020da252e8f9bec7c70e06e48807a6a2bd9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72eb5f1d75880a365b599503de3788fe2cc4a0df9f26639f7d57dc26ba991a9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeEnvironmentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeEnvironmentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeEnvironmentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aceb5a3cf1a7326b21d5d7ed8fd33ac1d049c6040f6dd11ba52ee8facec5135c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApigeeEnvironment",
    "ApigeeEnvironmentClientIpResolutionConfig",
    "ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm",
    "ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithmOutputReference",
    "ApigeeEnvironmentClientIpResolutionConfigOutputReference",
    "ApigeeEnvironmentConfig",
    "ApigeeEnvironmentNodeConfig",
    "ApigeeEnvironmentNodeConfigOutputReference",
    "ApigeeEnvironmentProperties",
    "ApigeeEnvironmentPropertiesOutputReference",
    "ApigeeEnvironmentPropertiesProperty",
    "ApigeeEnvironmentPropertiesPropertyList",
    "ApigeeEnvironmentPropertiesPropertyOutputReference",
    "ApigeeEnvironmentTimeouts",
    "ApigeeEnvironmentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ea40fd31858cddb5d1fe77fda8ff1648ead93d911063b38b92c8655585d84048(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    org_id: builtins.str,
    api_proxy_type: typing.Optional[builtins.str] = None,
    client_ip_resolution_config: typing.Optional[typing.Union[ApigeeEnvironmentClientIpResolutionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    forward_proxy_uri: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    node_config: typing.Optional[typing.Union[ApigeeEnvironmentNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    properties: typing.Optional[typing.Union[ApigeeEnvironmentProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ApigeeEnvironmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6e1cb8b9709aa97edb7af63f3ae4c0334305a722dd36c555e209e0e8a60744f5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c93877eb500997420989ea9411ad5e6f4d2c4925647525d0ac5f81c3377a96ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27cf9464dfb610d11ebef6abf029c8283b874bf7020b5da3f42ea5b9f1bb0312(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac76252e9c60f16d9f557c75242b6e1fb8f14b1ce9c88b6e2c60e3b57d8a251(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb09040be2fcdfa8569782a9ec69a6451a27b3a7ccd243f7d69a7bf404aa4b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b06dfd999fa12b03f0d198d75b4b1e9afab2f06b00d8bfa5678a6208458a4dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c282aa2880eab71bf50704657706615733980ad25a353c0045216062ed3c55ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14f5243bd6e710e6138dc8044e94e6a54c54ea058d3e4de2ee823726351f44f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375b29c2909509123d38f426b52dc31d2e0aae4b5d97a9b74467fdeb13fd4d25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ee83fd149c306745fcb0902da78d3bedd7359a6051972b1f3a571071321f11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99cb417c890e51b89a693ce0858aac7fb6a0fc31474c0480ad87b948e2f1f9fd(
    *,
    header_index_algorithm: typing.Optional[typing.Union[ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6cea53c655efefd2839c6fb3e8b234c046e973c7c6c9555fed5e51bd8fce4c(
    *,
    ip_header_index: jsii.Number,
    ip_header_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83255040095d9af6e5e37608a954361c832b9d8017cd0ec33a8ffff3820d587b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fefb2c67ca92cc916b2186e82b0257e401eb40d6c21094da5426748d27edff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e23cb9e01669f0ce079dcee741f91771ff942a4432348a4d5af2688d8ddf6ec3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e405f97e3f54c63be5ee65bb8540764e6bafd0af3138230870f53e94ab003c3(
    value: typing.Optional[ApigeeEnvironmentClientIpResolutionConfigHeaderIndexAlgorithm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f32c6732ccd6f3cdd7098c9ed641eaa1088ce1ea5aaad0296db4d2fe42f9611(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e58b2c542e180d95b79bb3f2e14b8b2b523a72c7f7bd94110872d76e8eb980(
    value: typing.Optional[ApigeeEnvironmentClientIpResolutionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f606507ccdfee0f97787f22694fe38b5b722ab3d633647d75847a2aa1654b58(
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
    client_ip_resolution_config: typing.Optional[typing.Union[ApigeeEnvironmentClientIpResolutionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    forward_proxy_uri: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    node_config: typing.Optional[typing.Union[ApigeeEnvironmentNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    properties: typing.Optional[typing.Union[ApigeeEnvironmentProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ApigeeEnvironmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a95ec9ecc2d1bb7caf18c1be31f3afbe226f3021885101ae2dc107a30f851ff(
    *,
    max_node_count: typing.Optional[builtins.str] = None,
    min_node_count: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b040eec67a46b48ac2027d313bbecef9283f6356fef82bb183e146a40e09c203(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830f99cdde4f34ec17c60de93022421c02b796d057b8b6e9e4fcba9d77a61a6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff66f199dd6f353b49ebd56c185da2ff06094a33dd19c1aca937650e6046e05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8eb2e0ec05f871b7711144c0b12ec55c84290b15a9973bf9bae6aeb8c33ca1(
    value: typing.Optional[ApigeeEnvironmentNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69eb44385d1ce4142ef861a0866da18fbb39b1846206d37036722d7567d31656(
    *,
    property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeEnvironmentPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1991b84bb951977262412b0444bc2aaa3e4931faff6c11cdc102909a6e6b69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa503384d2900c1bbb6d31f7e4b12a83f4701392bf3064da63675c6c66dfa7e5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeEnvironmentPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c391549e911b7339c6199b06948481808fcee71f739e9340f28e95b7bc19e0(
    value: typing.Optional[ApigeeEnvironmentProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35daf95d822c812562b40f8442c102b44af8de1635982f166d2f3aa29debbfce(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5159c98a2467ffa6e6992628e975c4c7c012476e81f0d54af210d68a2d96f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc28fc33e5a0fb3884ef83a638b9f92ff996c082b65c91dffc62909ab896103b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7984117201b20f0dc4b2df2268acdd0ea2025ccd2ab7b57e552d86829c7d9c88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed7eaa13f9f5ea72c1d146df2428ea6699bd2fd0ca85efb553b3724fff934c9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e24591bef24f260ecb0d42240c8e28ad2c2e8aa56e96df081885d211fbbca6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da02e24f3146db6ccb9c259633c9076e6cf8f01b84fec386f2a2e5dc59c2c88(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeEnvironmentPropertiesProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af591c178019e22130cae8e079f989d540276f37fae5d840187a565a3e49f5ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0772be1f0d8eb52e98e29bd27b4cbca89f980f7187a9f20e98b78c01cef5cd9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d440cc1d26c442e5377fb75dec86e1d78c13350d404eedcddb787159c1d2e155(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4196551d279c10022f370a4c14c2c8c8c323149906a6690710ba7467fbd5d301(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeEnvironmentPropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbc1abd5c6ec607e51a9d7dc1f434de3d78e2bac53745e33bce355bd0c23e0c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c087ff0fe7f805a16436503d9957ca9c6f403282fc3a635dfd547871f305a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008baed70f93e7e9e6de872d8f7dc286c1c0b00f3822b4ab225b272927b89a3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014a2de760b6ca4279ab22a064c6020da252e8f9bec7c70e06e48807a6a2bd9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72eb5f1d75880a365b599503de3788fe2cc4a0df9f26639f7d57dc26ba991a9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aceb5a3cf1a7326b21d5d7ed8fd33ac1d049c6040f6dd11ba52ee8facec5135c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeEnvironmentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

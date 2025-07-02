r'''
# `azurerm_spring_cloud_gateway`

Refer to the Terraform Registry for docs: [`azurerm_spring_cloud_gateway`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway).
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


class SpringCloudGateway(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGateway",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway azurerm_spring_cloud_gateway}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        spring_cloud_service_id: builtins.str,
        api_metadata: typing.Optional[typing.Union["SpringCloudGatewayApiMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        application_performance_monitoring_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        application_performance_monitoring_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_authorization: typing.Optional[typing.Union["SpringCloudGatewayClientAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        cors: typing.Optional[typing.Union["SpringCloudGatewayCors", typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_count: typing.Optional[jsii.Number] = None,
        local_response_cache_per_instance: typing.Optional[typing.Union["SpringCloudGatewayLocalResponseCachePerInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        local_response_cache_per_route: typing.Optional[typing.Union["SpringCloudGatewayLocalResponseCachePerRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        quota: typing.Optional[typing.Union["SpringCloudGatewayQuota", typing.Dict[builtins.str, typing.Any]]] = None,
        sensitive_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        sso: typing.Optional[typing.Union["SpringCloudGatewaySso", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["SpringCloudGatewayTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway azurerm_spring_cloud_gateway} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#name SpringCloudGateway#name}.
        :param spring_cloud_service_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#spring_cloud_service_id SpringCloudGateway#spring_cloud_service_id}.
        :param api_metadata: api_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#api_metadata SpringCloudGateway#api_metadata}
        :param application_performance_monitoring_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#application_performance_monitoring_ids SpringCloudGateway#application_performance_monitoring_ids}.
        :param application_performance_monitoring_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#application_performance_monitoring_types SpringCloudGateway#application_performance_monitoring_types}.
        :param client_authorization: client_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#client_authorization SpringCloudGateway#client_authorization}
        :param cors: cors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#cors SpringCloudGateway#cors}
        :param environment_variables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#environment_variables SpringCloudGateway#environment_variables}.
        :param https_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#https_only SpringCloudGateway#https_only}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#id SpringCloudGateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#instance_count SpringCloudGateway#instance_count}.
        :param local_response_cache_per_instance: local_response_cache_per_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#local_response_cache_per_instance SpringCloudGateway#local_response_cache_per_instance}
        :param local_response_cache_per_route: local_response_cache_per_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#local_response_cache_per_route SpringCloudGateway#local_response_cache_per_route}
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#public_network_access_enabled SpringCloudGateway#public_network_access_enabled}.
        :param quota: quota block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#quota SpringCloudGateway#quota}
        :param sensitive_environment_variables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#sensitive_environment_variables SpringCloudGateway#sensitive_environment_variables}.
        :param sso: sso block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#sso SpringCloudGateway#sso}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#timeouts SpringCloudGateway#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ea5c4c43f390c11649d0036d926660ddca068892f161b3d0babd6df0e9a2d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SpringCloudGatewayConfig(
            name=name,
            spring_cloud_service_id=spring_cloud_service_id,
            api_metadata=api_metadata,
            application_performance_monitoring_ids=application_performance_monitoring_ids,
            application_performance_monitoring_types=application_performance_monitoring_types,
            client_authorization=client_authorization,
            cors=cors,
            environment_variables=environment_variables,
            https_only=https_only,
            id=id,
            instance_count=instance_count,
            local_response_cache_per_instance=local_response_cache_per_instance,
            local_response_cache_per_route=local_response_cache_per_route,
            public_network_access_enabled=public_network_access_enabled,
            quota=quota,
            sensitive_environment_variables=sensitive_environment_variables,
            sso=sso,
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
        '''Generates CDKTF code for importing a SpringCloudGateway resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SpringCloudGateway to import.
        :param import_from_id: The id of the existing SpringCloudGateway that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SpringCloudGateway to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d9cf08bbcd04001b6e33f3dd34a02e77f83cada8990785011daaa0c6fcd4a1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putApiMetadata")
    def put_api_metadata(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        documentation_url: typing.Optional[builtins.str] = None,
        server_url: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#description SpringCloudGateway#description}.
        :param documentation_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#documentation_url SpringCloudGateway#documentation_url}.
        :param server_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#server_url SpringCloudGateway#server_url}.
        :param title: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#title SpringCloudGateway#title}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#version SpringCloudGateway#version}.
        '''
        value = SpringCloudGatewayApiMetadata(
            description=description,
            documentation_url=documentation_url,
            server_url=server_url,
            title=title,
            version=version,
        )

        return typing.cast(None, jsii.invoke(self, "putApiMetadata", [value]))

    @jsii.member(jsii_name="putClientAuthorization")
    def put_client_authorization(
        self,
        *,
        certificate_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        verification_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param certificate_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#certificate_ids SpringCloudGateway#certificate_ids}.
        :param verification_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#verification_enabled SpringCloudGateway#verification_enabled}.
        '''
        value = SpringCloudGatewayClientAuthorization(
            certificate_ids=certificate_ids, verification_enabled=verification_enabled
        )

        return typing.cast(None, jsii.invoke(self, "putClientAuthorization", [value]))

    @jsii.member(jsii_name="putCors")
    def put_cors(
        self,
        *,
        allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_origin_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        credentials_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exposed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_age_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allowed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#allowed_headers SpringCloudGateway#allowed_headers}.
        :param allowed_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#allowed_methods SpringCloudGateway#allowed_methods}.
        :param allowed_origin_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#allowed_origin_patterns SpringCloudGateway#allowed_origin_patterns}.
        :param allowed_origins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#allowed_origins SpringCloudGateway#allowed_origins}.
        :param credentials_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#credentials_allowed SpringCloudGateway#credentials_allowed}.
        :param exposed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#exposed_headers SpringCloudGateway#exposed_headers}.
        :param max_age_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#max_age_seconds SpringCloudGateway#max_age_seconds}.
        '''
        value = SpringCloudGatewayCors(
            allowed_headers=allowed_headers,
            allowed_methods=allowed_methods,
            allowed_origin_patterns=allowed_origin_patterns,
            allowed_origins=allowed_origins,
            credentials_allowed=credentials_allowed,
            exposed_headers=exposed_headers,
            max_age_seconds=max_age_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putCors", [value]))

    @jsii.member(jsii_name="putLocalResponseCachePerInstance")
    def put_local_response_cache_per_instance(
        self,
        *,
        size: typing.Optional[builtins.str] = None,
        time_to_live: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#size SpringCloudGateway#size}.
        :param time_to_live: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#time_to_live SpringCloudGateway#time_to_live}.
        '''
        value = SpringCloudGatewayLocalResponseCachePerInstance(
            size=size, time_to_live=time_to_live
        )

        return typing.cast(None, jsii.invoke(self, "putLocalResponseCachePerInstance", [value]))

    @jsii.member(jsii_name="putLocalResponseCachePerRoute")
    def put_local_response_cache_per_route(
        self,
        *,
        size: typing.Optional[builtins.str] = None,
        time_to_live: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#size SpringCloudGateway#size}.
        :param time_to_live: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#time_to_live SpringCloudGateway#time_to_live}.
        '''
        value = SpringCloudGatewayLocalResponseCachePerRoute(
            size=size, time_to_live=time_to_live
        )

        return typing.cast(None, jsii.invoke(self, "putLocalResponseCachePerRoute", [value]))

    @jsii.member(jsii_name="putQuota")
    def put_quota(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#cpu SpringCloudGateway#cpu}.
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#memory SpringCloudGateway#memory}.
        '''
        value = SpringCloudGatewayQuota(cpu=cpu, memory=memory)

        return typing.cast(None, jsii.invoke(self, "putQuota", [value]))

    @jsii.member(jsii_name="putSso")
    def put_sso(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        issuer_uri: typing.Optional[builtins.str] = None,
        scope: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#client_id SpringCloudGateway#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#client_secret SpringCloudGateway#client_secret}.
        :param issuer_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#issuer_uri SpringCloudGateway#issuer_uri}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#scope SpringCloudGateway#scope}.
        '''
        value = SpringCloudGatewaySso(
            client_id=client_id,
            client_secret=client_secret,
            issuer_uri=issuer_uri,
            scope=scope,
        )

        return typing.cast(None, jsii.invoke(self, "putSso", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#create SpringCloudGateway#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#delete SpringCloudGateway#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#read SpringCloudGateway#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#update SpringCloudGateway#update}.
        '''
        value = SpringCloudGatewayTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetApiMetadata")
    def reset_api_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiMetadata", []))

    @jsii.member(jsii_name="resetApplicationPerformanceMonitoringIds")
    def reset_application_performance_monitoring_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationPerformanceMonitoringIds", []))

    @jsii.member(jsii_name="resetApplicationPerformanceMonitoringTypes")
    def reset_application_performance_monitoring_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationPerformanceMonitoringTypes", []))

    @jsii.member(jsii_name="resetClientAuthorization")
    def reset_client_authorization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientAuthorization", []))

    @jsii.member(jsii_name="resetCors")
    def reset_cors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCors", []))

    @jsii.member(jsii_name="resetEnvironmentVariables")
    def reset_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentVariables", []))

    @jsii.member(jsii_name="resetHttpsOnly")
    def reset_https_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsOnly", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceCount")
    def reset_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceCount", []))

    @jsii.member(jsii_name="resetLocalResponseCachePerInstance")
    def reset_local_response_cache_per_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalResponseCachePerInstance", []))

    @jsii.member(jsii_name="resetLocalResponseCachePerRoute")
    def reset_local_response_cache_per_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalResponseCachePerRoute", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetQuota")
    def reset_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuota", []))

    @jsii.member(jsii_name="resetSensitiveEnvironmentVariables")
    def reset_sensitive_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitiveEnvironmentVariables", []))

    @jsii.member(jsii_name="resetSso")
    def reset_sso(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSso", []))

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
    @jsii.member(jsii_name="apiMetadata")
    def api_metadata(self) -> "SpringCloudGatewayApiMetadataOutputReference":
        return typing.cast("SpringCloudGatewayApiMetadataOutputReference", jsii.get(self, "apiMetadata"))

    @builtins.property
    @jsii.member(jsii_name="clientAuthorization")
    def client_authorization(
        self,
    ) -> "SpringCloudGatewayClientAuthorizationOutputReference":
        return typing.cast("SpringCloudGatewayClientAuthorizationOutputReference", jsii.get(self, "clientAuthorization"))

    @builtins.property
    @jsii.member(jsii_name="cors")
    def cors(self) -> "SpringCloudGatewayCorsOutputReference":
        return typing.cast("SpringCloudGatewayCorsOutputReference", jsii.get(self, "cors"))

    @builtins.property
    @jsii.member(jsii_name="localResponseCachePerInstance")
    def local_response_cache_per_instance(
        self,
    ) -> "SpringCloudGatewayLocalResponseCachePerInstanceOutputReference":
        return typing.cast("SpringCloudGatewayLocalResponseCachePerInstanceOutputReference", jsii.get(self, "localResponseCachePerInstance"))

    @builtins.property
    @jsii.member(jsii_name="localResponseCachePerRoute")
    def local_response_cache_per_route(
        self,
    ) -> "SpringCloudGatewayLocalResponseCachePerRouteOutputReference":
        return typing.cast("SpringCloudGatewayLocalResponseCachePerRouteOutputReference", jsii.get(self, "localResponseCachePerRoute"))

    @builtins.property
    @jsii.member(jsii_name="quota")
    def quota(self) -> "SpringCloudGatewayQuotaOutputReference":
        return typing.cast("SpringCloudGatewayQuotaOutputReference", jsii.get(self, "quota"))

    @builtins.property
    @jsii.member(jsii_name="sso")
    def sso(self) -> "SpringCloudGatewaySsoOutputReference":
        return typing.cast("SpringCloudGatewaySsoOutputReference", jsii.get(self, "sso"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SpringCloudGatewayTimeoutsOutputReference":
        return typing.cast("SpringCloudGatewayTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="apiMetadataInput")
    def api_metadata_input(self) -> typing.Optional["SpringCloudGatewayApiMetadata"]:
        return typing.cast(typing.Optional["SpringCloudGatewayApiMetadata"], jsii.get(self, "apiMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationPerformanceMonitoringIdsInput")
    def application_performance_monitoring_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "applicationPerformanceMonitoringIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationPerformanceMonitoringTypesInput")
    def application_performance_monitoring_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "applicationPerformanceMonitoringTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientAuthorizationInput")
    def client_authorization_input(
        self,
    ) -> typing.Optional["SpringCloudGatewayClientAuthorization"]:
        return typing.cast(typing.Optional["SpringCloudGatewayClientAuthorization"], jsii.get(self, "clientAuthorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="corsInput")
    def cors_input(self) -> typing.Optional["SpringCloudGatewayCors"]:
        return typing.cast(typing.Optional["SpringCloudGatewayCors"], jsii.get(self, "corsInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentVariablesInput")
    def environment_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsOnlyInput")
    def https_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "httpsOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceCountInput")
    def instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="localResponseCachePerInstanceInput")
    def local_response_cache_per_instance_input(
        self,
    ) -> typing.Optional["SpringCloudGatewayLocalResponseCachePerInstance"]:
        return typing.cast(typing.Optional["SpringCloudGatewayLocalResponseCachePerInstance"], jsii.get(self, "localResponseCachePerInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="localResponseCachePerRouteInput")
    def local_response_cache_per_route_input(
        self,
    ) -> typing.Optional["SpringCloudGatewayLocalResponseCachePerRoute"]:
        return typing.cast(typing.Optional["SpringCloudGatewayLocalResponseCachePerRoute"], jsii.get(self, "localResponseCachePerRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabledInput")
    def public_network_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicNetworkAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaInput")
    def quota_input(self) -> typing.Optional["SpringCloudGatewayQuota"]:
        return typing.cast(typing.Optional["SpringCloudGatewayQuota"], jsii.get(self, "quotaInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitiveEnvironmentVariablesInput")
    def sensitive_environment_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "sensitiveEnvironmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="springCloudServiceIdInput")
    def spring_cloud_service_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "springCloudServiceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ssoInput")
    def sso_input(self) -> typing.Optional["SpringCloudGatewaySso"]:
        return typing.cast(typing.Optional["SpringCloudGatewaySso"], jsii.get(self, "ssoInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpringCloudGatewayTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpringCloudGatewayTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationPerformanceMonitoringIds")
    def application_performance_monitoring_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "applicationPerformanceMonitoringIds"))

    @application_performance_monitoring_ids.setter
    def application_performance_monitoring_ids(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c5b35b99c77c8d1f49f2e923a01db9b2d1e5b3542c49edd410c051465ec84de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationPerformanceMonitoringIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationPerformanceMonitoringTypes")
    def application_performance_monitoring_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "applicationPerformanceMonitoringTypes"))

    @application_performance_monitoring_types.setter
    def application_performance_monitoring_types(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc373ac40e261600f82442aa5b469b40a70a45bfe49bd7259f87a45b4cbfc11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationPerformanceMonitoringTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environmentVariables")
    def environment_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environmentVariables"))

    @environment_variables.setter
    def environment_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3ac9779dad8286db43091bcfc4015056ac54d7dad23875222d52481c5fb12ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsOnly")
    def https_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "httpsOnly"))

    @https_only.setter
    def https_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e355deaa490fb58fe156b3b8f66d98cd4ea24e82499ba96e25e19eb781ab61a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e22dfd456ab89b680fdc3c1ebb99e905f5700673a6b0e8b46180868f45df998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceCount")
    def instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceCount"))

    @instance_count.setter
    def instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d764d7e680fe5b6a4615b77d020fdf8a9885b610e9ebb59670a902715db525c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb228f34a54fa7dde443d7277fdd9e1c976a4542447d9ff42b18c7956ccdfd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabled")
    def public_network_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicNetworkAccessEnabled"))

    @public_network_access_enabled.setter
    def public_network_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca6b634ae39a9094f9b3f2bbc37f07488a07dca11676ac12f148d617d4d76f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sensitiveEnvironmentVariables")
    def sensitive_environment_variables(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "sensitiveEnvironmentVariables"))

    @sensitive_environment_variables.setter
    def sensitive_environment_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f008bebbd01d7234e2cec52dc1db44339e4041f2bf97fd31963230fecde4d6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sensitiveEnvironmentVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="springCloudServiceId")
    def spring_cloud_service_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "springCloudServiceId"))

    @spring_cloud_service_id.setter
    def spring_cloud_service_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d80c74833ea1ecb700fe36a39933bc180456e27792f45e7b844fa8ed290c97e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "springCloudServiceId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewayApiMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "documentation_url": "documentationUrl",
        "server_url": "serverUrl",
        "title": "title",
        "version": "version",
    },
)
class SpringCloudGatewayApiMetadata:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        documentation_url: typing.Optional[builtins.str] = None,
        server_url: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#description SpringCloudGateway#description}.
        :param documentation_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#documentation_url SpringCloudGateway#documentation_url}.
        :param server_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#server_url SpringCloudGateway#server_url}.
        :param title: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#title SpringCloudGateway#title}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#version SpringCloudGateway#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b2191202d948787f215561fb8d229efe74117a0ce6f4750e6a0284a59b9d40)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument documentation_url", value=documentation_url, expected_type=type_hints["documentation_url"])
            check_type(argname="argument server_url", value=server_url, expected_type=type_hints["server_url"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if documentation_url is not None:
            self._values["documentation_url"] = documentation_url
        if server_url is not None:
            self._values["server_url"] = server_url
        if title is not None:
            self._values["title"] = title
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#description SpringCloudGateway#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def documentation_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#documentation_url SpringCloudGateway#documentation_url}.'''
        result = self._values.get("documentation_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#server_url SpringCloudGateway#server_url}.'''
        result = self._values.get("server_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#title SpringCloudGateway#title}.'''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#version SpringCloudGateway#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudGatewayApiMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudGatewayApiMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewayApiMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7d620e7c5e5b919030523947472abc1a184a4a9a619340f783e5d40cae95d5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDocumentationUrl")
    def reset_documentation_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentationUrl", []))

    @jsii.member(jsii_name="resetServerUrl")
    def reset_server_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerUrl", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="documentationUrlInput")
    def documentation_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentationUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="serverUrlInput")
    def server_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0bf16de631f61b934d066320f2e10db2e169e32950643948af795972970cbc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentationUrl")
    def documentation_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentationUrl"))

    @documentation_url.setter
    def documentation_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffc2eabf235eab52592cdc684ef0477cabcca1dbc1d71c21f81cd85aea5a4d3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentationUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverUrl"))

    @server_url.setter
    def server_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ede059f6cf36ced443911d51b2b2b2f00987169786816b33139a10472761b4b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0acdfde898f18729447fa4f03117fa1a513d3f2b9dbb26595206d16ba58a8fc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eef3839e83670879c2bd888665495db18b6b0bd7a2cd417d1b3e7a33bfde299e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SpringCloudGatewayApiMetadata]:
        return typing.cast(typing.Optional[SpringCloudGatewayApiMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpringCloudGatewayApiMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a972b9b07ebca2e1bb4ac437248f2b6cf59f36d2a8cf1eb535bfa69dbe2cdab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewayClientAuthorization",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_ids": "certificateIds",
        "verification_enabled": "verificationEnabled",
    },
)
class SpringCloudGatewayClientAuthorization:
    def __init__(
        self,
        *,
        certificate_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        verification_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param certificate_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#certificate_ids SpringCloudGateway#certificate_ids}.
        :param verification_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#verification_enabled SpringCloudGateway#verification_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f4efc04a5be5be02dc8304b59eaf0f210b88fee369da8f8c9c09d3f8239bcd7)
            check_type(argname="argument certificate_ids", value=certificate_ids, expected_type=type_hints["certificate_ids"])
            check_type(argname="argument verification_enabled", value=verification_enabled, expected_type=type_hints["verification_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_ids is not None:
            self._values["certificate_ids"] = certificate_ids
        if verification_enabled is not None:
            self._values["verification_enabled"] = verification_enabled

    @builtins.property
    def certificate_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#certificate_ids SpringCloudGateway#certificate_ids}.'''
        result = self._values.get("certificate_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def verification_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#verification_enabled SpringCloudGateway#verification_enabled}.'''
        result = self._values.get("verification_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudGatewayClientAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudGatewayClientAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewayClientAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7accb34208514c59f0ac64501e8a5816b9412a160ba1821992ce778691cb43c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCertificateIds")
    def reset_certificate_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateIds", []))

    @jsii.member(jsii_name="resetVerificationEnabled")
    def reset_verification_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerificationEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="certificateIdsInput")
    def certificate_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "certificateIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="verificationEnabledInput")
    def verification_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verificationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateIds")
    def certificate_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "certificateIds"))

    @certificate_ids.setter
    def certificate_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29e0c7cdc310140607f0ba33c7a496186ea74a773f48258d56a560418272daa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verificationEnabled")
    def verification_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verificationEnabled"))

    @verification_enabled.setter
    def verification_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a42e3fb016c85ad3545a75b51b75d7b0a6990e656e507e619ba4cb39330ac39d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verificationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SpringCloudGatewayClientAuthorization]:
        return typing.cast(typing.Optional[SpringCloudGatewayClientAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpringCloudGatewayClientAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06d54adea6603da117a3053e8cd982c36f3a47247b37deb3de8a4ad712c33f1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewayConfig",
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
        "spring_cloud_service_id": "springCloudServiceId",
        "api_metadata": "apiMetadata",
        "application_performance_monitoring_ids": "applicationPerformanceMonitoringIds",
        "application_performance_monitoring_types": "applicationPerformanceMonitoringTypes",
        "client_authorization": "clientAuthorization",
        "cors": "cors",
        "environment_variables": "environmentVariables",
        "https_only": "httpsOnly",
        "id": "id",
        "instance_count": "instanceCount",
        "local_response_cache_per_instance": "localResponseCachePerInstance",
        "local_response_cache_per_route": "localResponseCachePerRoute",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "quota": "quota",
        "sensitive_environment_variables": "sensitiveEnvironmentVariables",
        "sso": "sso",
        "timeouts": "timeouts",
    },
)
class SpringCloudGatewayConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        spring_cloud_service_id: builtins.str,
        api_metadata: typing.Optional[typing.Union[SpringCloudGatewayApiMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
        application_performance_monitoring_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        application_performance_monitoring_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_authorization: typing.Optional[typing.Union[SpringCloudGatewayClientAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        cors: typing.Optional[typing.Union["SpringCloudGatewayCors", typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_count: typing.Optional[jsii.Number] = None,
        local_response_cache_per_instance: typing.Optional[typing.Union["SpringCloudGatewayLocalResponseCachePerInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        local_response_cache_per_route: typing.Optional[typing.Union["SpringCloudGatewayLocalResponseCachePerRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        quota: typing.Optional[typing.Union["SpringCloudGatewayQuota", typing.Dict[builtins.str, typing.Any]]] = None,
        sensitive_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        sso: typing.Optional[typing.Union["SpringCloudGatewaySso", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["SpringCloudGatewayTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#name SpringCloudGateway#name}.
        :param spring_cloud_service_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#spring_cloud_service_id SpringCloudGateway#spring_cloud_service_id}.
        :param api_metadata: api_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#api_metadata SpringCloudGateway#api_metadata}
        :param application_performance_monitoring_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#application_performance_monitoring_ids SpringCloudGateway#application_performance_monitoring_ids}.
        :param application_performance_monitoring_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#application_performance_monitoring_types SpringCloudGateway#application_performance_monitoring_types}.
        :param client_authorization: client_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#client_authorization SpringCloudGateway#client_authorization}
        :param cors: cors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#cors SpringCloudGateway#cors}
        :param environment_variables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#environment_variables SpringCloudGateway#environment_variables}.
        :param https_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#https_only SpringCloudGateway#https_only}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#id SpringCloudGateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#instance_count SpringCloudGateway#instance_count}.
        :param local_response_cache_per_instance: local_response_cache_per_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#local_response_cache_per_instance SpringCloudGateway#local_response_cache_per_instance}
        :param local_response_cache_per_route: local_response_cache_per_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#local_response_cache_per_route SpringCloudGateway#local_response_cache_per_route}
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#public_network_access_enabled SpringCloudGateway#public_network_access_enabled}.
        :param quota: quota block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#quota SpringCloudGateway#quota}
        :param sensitive_environment_variables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#sensitive_environment_variables SpringCloudGateway#sensitive_environment_variables}.
        :param sso: sso block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#sso SpringCloudGateway#sso}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#timeouts SpringCloudGateway#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(api_metadata, dict):
            api_metadata = SpringCloudGatewayApiMetadata(**api_metadata)
        if isinstance(client_authorization, dict):
            client_authorization = SpringCloudGatewayClientAuthorization(**client_authorization)
        if isinstance(cors, dict):
            cors = SpringCloudGatewayCors(**cors)
        if isinstance(local_response_cache_per_instance, dict):
            local_response_cache_per_instance = SpringCloudGatewayLocalResponseCachePerInstance(**local_response_cache_per_instance)
        if isinstance(local_response_cache_per_route, dict):
            local_response_cache_per_route = SpringCloudGatewayLocalResponseCachePerRoute(**local_response_cache_per_route)
        if isinstance(quota, dict):
            quota = SpringCloudGatewayQuota(**quota)
        if isinstance(sso, dict):
            sso = SpringCloudGatewaySso(**sso)
        if isinstance(timeouts, dict):
            timeouts = SpringCloudGatewayTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958760e128879532c937531a9910df138d3deeca5d0c7b621fd14c7bb1144ec3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument spring_cloud_service_id", value=spring_cloud_service_id, expected_type=type_hints["spring_cloud_service_id"])
            check_type(argname="argument api_metadata", value=api_metadata, expected_type=type_hints["api_metadata"])
            check_type(argname="argument application_performance_monitoring_ids", value=application_performance_monitoring_ids, expected_type=type_hints["application_performance_monitoring_ids"])
            check_type(argname="argument application_performance_monitoring_types", value=application_performance_monitoring_types, expected_type=type_hints["application_performance_monitoring_types"])
            check_type(argname="argument client_authorization", value=client_authorization, expected_type=type_hints["client_authorization"])
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument https_only", value=https_only, expected_type=type_hints["https_only"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
            check_type(argname="argument local_response_cache_per_instance", value=local_response_cache_per_instance, expected_type=type_hints["local_response_cache_per_instance"])
            check_type(argname="argument local_response_cache_per_route", value=local_response_cache_per_route, expected_type=type_hints["local_response_cache_per_route"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument quota", value=quota, expected_type=type_hints["quota"])
            check_type(argname="argument sensitive_environment_variables", value=sensitive_environment_variables, expected_type=type_hints["sensitive_environment_variables"])
            check_type(argname="argument sso", value=sso, expected_type=type_hints["sso"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "spring_cloud_service_id": spring_cloud_service_id,
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
        if api_metadata is not None:
            self._values["api_metadata"] = api_metadata
        if application_performance_monitoring_ids is not None:
            self._values["application_performance_monitoring_ids"] = application_performance_monitoring_ids
        if application_performance_monitoring_types is not None:
            self._values["application_performance_monitoring_types"] = application_performance_monitoring_types
        if client_authorization is not None:
            self._values["client_authorization"] = client_authorization
        if cors is not None:
            self._values["cors"] = cors
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if https_only is not None:
            self._values["https_only"] = https_only
        if id is not None:
            self._values["id"] = id
        if instance_count is not None:
            self._values["instance_count"] = instance_count
        if local_response_cache_per_instance is not None:
            self._values["local_response_cache_per_instance"] = local_response_cache_per_instance
        if local_response_cache_per_route is not None:
            self._values["local_response_cache_per_route"] = local_response_cache_per_route
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if quota is not None:
            self._values["quota"] = quota
        if sensitive_environment_variables is not None:
            self._values["sensitive_environment_variables"] = sensitive_environment_variables
        if sso is not None:
            self._values["sso"] = sso
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#name SpringCloudGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spring_cloud_service_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#spring_cloud_service_id SpringCloudGateway#spring_cloud_service_id}.'''
        result = self._values.get("spring_cloud_service_id")
        assert result is not None, "Required property 'spring_cloud_service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_metadata(self) -> typing.Optional[SpringCloudGatewayApiMetadata]:
        '''api_metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#api_metadata SpringCloudGateway#api_metadata}
        '''
        result = self._values.get("api_metadata")
        return typing.cast(typing.Optional[SpringCloudGatewayApiMetadata], result)

    @builtins.property
    def application_performance_monitoring_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#application_performance_monitoring_ids SpringCloudGateway#application_performance_monitoring_ids}.'''
        result = self._values.get("application_performance_monitoring_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def application_performance_monitoring_types(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#application_performance_monitoring_types SpringCloudGateway#application_performance_monitoring_types}.'''
        result = self._values.get("application_performance_monitoring_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def client_authorization(
        self,
    ) -> typing.Optional[SpringCloudGatewayClientAuthorization]:
        '''client_authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#client_authorization SpringCloudGateway#client_authorization}
        '''
        result = self._values.get("client_authorization")
        return typing.cast(typing.Optional[SpringCloudGatewayClientAuthorization], result)

    @builtins.property
    def cors(self) -> typing.Optional["SpringCloudGatewayCors"]:
        '''cors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#cors SpringCloudGateway#cors}
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional["SpringCloudGatewayCors"], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#environment_variables SpringCloudGateway#environment_variables}.'''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def https_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#https_only SpringCloudGateway#https_only}.'''
        result = self._values.get("https_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#id SpringCloudGateway#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#instance_count SpringCloudGateway#instance_count}.'''
        result = self._values.get("instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def local_response_cache_per_instance(
        self,
    ) -> typing.Optional["SpringCloudGatewayLocalResponseCachePerInstance"]:
        '''local_response_cache_per_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#local_response_cache_per_instance SpringCloudGateway#local_response_cache_per_instance}
        '''
        result = self._values.get("local_response_cache_per_instance")
        return typing.cast(typing.Optional["SpringCloudGatewayLocalResponseCachePerInstance"], result)

    @builtins.property
    def local_response_cache_per_route(
        self,
    ) -> typing.Optional["SpringCloudGatewayLocalResponseCachePerRoute"]:
        '''local_response_cache_per_route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#local_response_cache_per_route SpringCloudGateway#local_response_cache_per_route}
        '''
        result = self._values.get("local_response_cache_per_route")
        return typing.cast(typing.Optional["SpringCloudGatewayLocalResponseCachePerRoute"], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#public_network_access_enabled SpringCloudGateway#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def quota(self) -> typing.Optional["SpringCloudGatewayQuota"]:
        '''quota block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#quota SpringCloudGateway#quota}
        '''
        result = self._values.get("quota")
        return typing.cast(typing.Optional["SpringCloudGatewayQuota"], result)

    @builtins.property
    def sensitive_environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#sensitive_environment_variables SpringCloudGateway#sensitive_environment_variables}.'''
        result = self._values.get("sensitive_environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def sso(self) -> typing.Optional["SpringCloudGatewaySso"]:
        '''sso block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#sso SpringCloudGateway#sso}
        '''
        result = self._values.get("sso")
        return typing.cast(typing.Optional["SpringCloudGatewaySso"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SpringCloudGatewayTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#timeouts SpringCloudGateway#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SpringCloudGatewayTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudGatewayConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewayCors",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_headers": "allowedHeaders",
        "allowed_methods": "allowedMethods",
        "allowed_origin_patterns": "allowedOriginPatterns",
        "allowed_origins": "allowedOrigins",
        "credentials_allowed": "credentialsAllowed",
        "exposed_headers": "exposedHeaders",
        "max_age_seconds": "maxAgeSeconds",
    },
)
class SpringCloudGatewayCors:
    def __init__(
        self,
        *,
        allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_origin_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        credentials_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exposed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_age_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allowed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#allowed_headers SpringCloudGateway#allowed_headers}.
        :param allowed_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#allowed_methods SpringCloudGateway#allowed_methods}.
        :param allowed_origin_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#allowed_origin_patterns SpringCloudGateway#allowed_origin_patterns}.
        :param allowed_origins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#allowed_origins SpringCloudGateway#allowed_origins}.
        :param credentials_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#credentials_allowed SpringCloudGateway#credentials_allowed}.
        :param exposed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#exposed_headers SpringCloudGateway#exposed_headers}.
        :param max_age_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#max_age_seconds SpringCloudGateway#max_age_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66857bab341a8d9196a0c571c7e5b36dbbc6c4a0688c306bb5648bc936f464ea)
            check_type(argname="argument allowed_headers", value=allowed_headers, expected_type=type_hints["allowed_headers"])
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument allowed_origin_patterns", value=allowed_origin_patterns, expected_type=type_hints["allowed_origin_patterns"])
            check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
            check_type(argname="argument credentials_allowed", value=credentials_allowed, expected_type=type_hints["credentials_allowed"])
            check_type(argname="argument exposed_headers", value=exposed_headers, expected_type=type_hints["exposed_headers"])
            check_type(argname="argument max_age_seconds", value=max_age_seconds, expected_type=type_hints["max_age_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_headers is not None:
            self._values["allowed_headers"] = allowed_headers
        if allowed_methods is not None:
            self._values["allowed_methods"] = allowed_methods
        if allowed_origin_patterns is not None:
            self._values["allowed_origin_patterns"] = allowed_origin_patterns
        if allowed_origins is not None:
            self._values["allowed_origins"] = allowed_origins
        if credentials_allowed is not None:
            self._values["credentials_allowed"] = credentials_allowed
        if exposed_headers is not None:
            self._values["exposed_headers"] = exposed_headers
        if max_age_seconds is not None:
            self._values["max_age_seconds"] = max_age_seconds

    @builtins.property
    def allowed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#allowed_headers SpringCloudGateway#allowed_headers}.'''
        result = self._values.get("allowed_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#allowed_methods SpringCloudGateway#allowed_methods}.'''
        result = self._values.get("allowed_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_origin_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#allowed_origin_patterns SpringCloudGateway#allowed_origin_patterns}.'''
        result = self._values.get("allowed_origin_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_origins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#allowed_origins SpringCloudGateway#allowed_origins}.'''
        result = self._values.get("allowed_origins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def credentials_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#credentials_allowed SpringCloudGateway#credentials_allowed}.'''
        result = self._values.get("credentials_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exposed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#exposed_headers SpringCloudGateway#exposed_headers}.'''
        result = self._values.get("exposed_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_age_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#max_age_seconds SpringCloudGateway#max_age_seconds}.'''
        result = self._values.get("max_age_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudGatewayCors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudGatewayCorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewayCorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95a069eab0ee657d0d5d5e17d0abc3b8bcdb741494d70a507e26653d9ba5b565)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedHeaders")
    def reset_allowed_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedHeaders", []))

    @jsii.member(jsii_name="resetAllowedMethods")
    def reset_allowed_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedMethods", []))

    @jsii.member(jsii_name="resetAllowedOriginPatterns")
    def reset_allowed_origin_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedOriginPatterns", []))

    @jsii.member(jsii_name="resetAllowedOrigins")
    def reset_allowed_origins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedOrigins", []))

    @jsii.member(jsii_name="resetCredentialsAllowed")
    def reset_credentials_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialsAllowed", []))

    @jsii.member(jsii_name="resetExposedHeaders")
    def reset_exposed_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExposedHeaders", []))

    @jsii.member(jsii_name="resetMaxAgeSeconds")
    def reset_max_age_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAgeSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="allowedHeadersInput")
    def allowed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedOriginPatternsInput")
    def allowed_origin_patterns_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOriginPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedOriginsInput")
    def allowed_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsAllowedInput")
    def credentials_allowed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "credentialsAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="exposedHeadersInput")
    def exposed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exposedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeSecondsInput")
    def max_age_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAgeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedHeaders")
    def allowed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedHeaders"))

    @allowed_headers.setter
    def allowed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6519100ca651e374518209e8619aa97ec3bbd68b4db819ceee4b9242552ad02e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMethods"))

    @allowed_methods.setter
    def allowed_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2e301ab3ed3aac6ba624843e6f5556337e26cf423d3acde596d4c8f03e04503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedOriginPatterns")
    def allowed_origin_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOriginPatterns"))

    @allowed_origin_patterns.setter
    def allowed_origin_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3991504329cfc02f4bdf6ce92ffd25912bc55f7fc1c49f8424490c7d7333a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOriginPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOrigins"))

    @allowed_origins.setter
    def allowed_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a50c5b9b1d5c7000fd795aad6a69d24b637e9335d636cef5014eb405fd509d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOrigins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="credentialsAllowed")
    def credentials_allowed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "credentialsAllowed"))

    @credentials_allowed.setter
    def credentials_allowed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24cb8153e899f847b3d54911e939b0f318841b03d65d047c9b5dd295b803710a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialsAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exposedHeaders")
    def exposed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exposedHeaders"))

    @exposed_headers.setter
    def exposed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b94318106aa7d11df6bb1aa9cf03cf18590dbbb27f1d2eb9733c2a709e6bf03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAgeSeconds")
    def max_age_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAgeSeconds"))

    @max_age_seconds.setter
    def max_age_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a77de9357d8cdeed75ae58d375a3ae39d531eed11c94442f3c159fa8dae64e99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAgeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SpringCloudGatewayCors]:
        return typing.cast(typing.Optional[SpringCloudGatewayCors], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SpringCloudGatewayCors]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9c0965dfc044d14233b2b5d1cd7289af913284b67200754cc3e2b024b79cb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewayLocalResponseCachePerInstance",
    jsii_struct_bases=[],
    name_mapping={"size": "size", "time_to_live": "timeToLive"},
)
class SpringCloudGatewayLocalResponseCachePerInstance:
    def __init__(
        self,
        *,
        size: typing.Optional[builtins.str] = None,
        time_to_live: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#size SpringCloudGateway#size}.
        :param time_to_live: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#time_to_live SpringCloudGateway#time_to_live}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc165033d8460ef3b275ef4f32f28e1d6e5d350e452c939c72466cc3b251e27)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument time_to_live", value=time_to_live, expected_type=type_hints["time_to_live"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if size is not None:
            self._values["size"] = size
        if time_to_live is not None:
            self._values["time_to_live"] = time_to_live

    @builtins.property
    def size(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#size SpringCloudGateway#size}.'''
        result = self._values.get("size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_to_live(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#time_to_live SpringCloudGateway#time_to_live}.'''
        result = self._values.get("time_to_live")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudGatewayLocalResponseCachePerInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudGatewayLocalResponseCachePerInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewayLocalResponseCachePerInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d41d5f3d16ef2b6e11da5f61927edc706e40ad319349c969b63c73916ce65fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @jsii.member(jsii_name="resetTimeToLive")
    def reset_time_to_live(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeToLive", []))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeToLiveInput")
    def time_to_live_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeToLiveInput"))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "size"))

    @size.setter
    def size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b196910b25410b040431c8fa03abd70a19919214e1089307ab84000f3075c0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeToLive")
    def time_to_live(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeToLive"))

    @time_to_live.setter
    def time_to_live(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ae58794683f5d677d601962d7c7c23f889cd5135538960c3564c9c09b76d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeToLive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpringCloudGatewayLocalResponseCachePerInstance]:
        return typing.cast(typing.Optional[SpringCloudGatewayLocalResponseCachePerInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpringCloudGatewayLocalResponseCachePerInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19ba10e2ce8974894ae93fdb8d2e50aaf8d05eb76f7f419c1828dc83729c8136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewayLocalResponseCachePerRoute",
    jsii_struct_bases=[],
    name_mapping={"size": "size", "time_to_live": "timeToLive"},
)
class SpringCloudGatewayLocalResponseCachePerRoute:
    def __init__(
        self,
        *,
        size: typing.Optional[builtins.str] = None,
        time_to_live: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#size SpringCloudGateway#size}.
        :param time_to_live: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#time_to_live SpringCloudGateway#time_to_live}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac71c986cca371eb3bde34cf65c4a58dca8bf2aa55b683b8465433cd5e63637)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument time_to_live", value=time_to_live, expected_type=type_hints["time_to_live"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if size is not None:
            self._values["size"] = size
        if time_to_live is not None:
            self._values["time_to_live"] = time_to_live

    @builtins.property
    def size(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#size SpringCloudGateway#size}.'''
        result = self._values.get("size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_to_live(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#time_to_live SpringCloudGateway#time_to_live}.'''
        result = self._values.get("time_to_live")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudGatewayLocalResponseCachePerRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudGatewayLocalResponseCachePerRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewayLocalResponseCachePerRouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2a7085c399cfbcf71ab536b412c8d28c9d29d82a00bc3015c2c5d2f25a2a021)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @jsii.member(jsii_name="resetTimeToLive")
    def reset_time_to_live(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeToLive", []))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeToLiveInput")
    def time_to_live_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeToLiveInput"))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "size"))

    @size.setter
    def size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa5d15c43ee127ece82936018fb21cc165f9358ff5ecf34d4703997197ec0b67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeToLive")
    def time_to_live(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeToLive"))

    @time_to_live.setter
    def time_to_live(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a10e00486dba4ad882fe75b48f1b42221d7bc46bf80c3bd9fd846d7848e06ebe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeToLive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpringCloudGatewayLocalResponseCachePerRoute]:
        return typing.cast(typing.Optional[SpringCloudGatewayLocalResponseCachePerRoute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpringCloudGatewayLocalResponseCachePerRoute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df89dcb91d73d525e5c27430f4655c1e93ee36f7747213a89e86632c3369a35f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewayQuota",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory"},
)
class SpringCloudGatewayQuota:
    def __init__(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#cpu SpringCloudGateway#cpu}.
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#memory SpringCloudGateway#memory}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c5564cda6208a8a285528193188313d8eb896104c4f80506036d8e1d077582)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory is not None:
            self._values["memory"] = memory

    @builtins.property
    def cpu(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#cpu SpringCloudGateway#cpu}.'''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#memory SpringCloudGateway#memory}.'''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudGatewayQuota(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudGatewayQuotaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewayQuotaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecda1bcd54b4b57ce647c4fe1ce586ae9eab95aa976f72c10bf674bac80fa6e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d7150302512da26b02c9b49f6e07004fd4b0981eb2f7c6d00b48cf0e1edf653)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ae25ab8c647db3e3c0e2e4befed55885fbb6914dabd1f81c5423cfd33668c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SpringCloudGatewayQuota]:
        return typing.cast(typing.Optional[SpringCloudGatewayQuota], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SpringCloudGatewayQuota]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__303940ed0df19b817ef7b14fb45a70d17457a137ee5efde2f4018f0df19f6ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewaySso",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "issuer_uri": "issuerUri",
        "scope": "scope",
    },
)
class SpringCloudGatewaySso:
    def __init__(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        issuer_uri: typing.Optional[builtins.str] = None,
        scope: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#client_id SpringCloudGateway#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#client_secret SpringCloudGateway#client_secret}.
        :param issuer_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#issuer_uri SpringCloudGateway#issuer_uri}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#scope SpringCloudGateway#scope}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608e5df39a8558e29df7ec802a2975d2be9295274a64233c9f58f93d08266d3b)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument issuer_uri", value=issuer_uri, expected_type=type_hints["issuer_uri"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if issuer_uri is not None:
            self._values["issuer_uri"] = issuer_uri
        if scope is not None:
            self._values["scope"] = scope

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#client_id SpringCloudGateway#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#client_secret SpringCloudGateway#client_secret}.'''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#issuer_uri SpringCloudGateway#issuer_uri}.'''
        result = self._values.get("issuer_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#scope SpringCloudGateway#scope}.'''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudGatewaySso(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudGatewaySsoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewaySsoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__160b79fc76395a16a0dea901fca9b007471bae3e02ca5e1e79b069adec9e3885)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetIssuerUri")
    def reset_issuer_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuerUri", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerUriInput")
    def issuer_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerUriInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d777decc74edd6aa42154bedbc3e74ce23a92511b954ed764c04f4737c708c21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b4df3738a6290ea0c1affcf4d87a4142e876a91fbdd384c4c0c9504f941108)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuerUri")
    def issuer_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUri"))

    @issuer_uri.setter
    def issuer_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__973f609ba1a2c5aa706d450cfb29f5b44a065f28fb7fc275a419d5e34a361f1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc8e5d3dd3b230cb2be66579b54797163d9c1fa2c62af5cf5d2e71847e88b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SpringCloudGatewaySso]:
        return typing.cast(typing.Optional[SpringCloudGatewaySso], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SpringCloudGatewaySso]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c44ab4105908faf70db5d5718e44cf278d831b861787dbe1f6476a39c39a9db6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewayTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SpringCloudGatewayTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#create SpringCloudGateway#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#delete SpringCloudGateway#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#read SpringCloudGateway#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#update SpringCloudGateway#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d210a8cf9328eaf0a9a63ad7e472ab3d32923fd3cbae74830ac509fb946ee3c6)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#create SpringCloudGateway#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#delete SpringCloudGateway#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#read SpringCloudGateway#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_gateway#update SpringCloudGateway#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudGatewayTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudGatewayTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudGateway.SpringCloudGatewayTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f8c32948f107fa513436da50d3555df24c845f885777248f972315e19d9ab67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c71c08496f5d580eaa474bef171ffe5ab37de17877a3b6de9010c33486074d17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab7c00a9cc9e685a9770d451062b3d4aced4ec47f0011a4cf01c6b7d53c9730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e92ca612a1881303ee30bd61db3077d2559278ae8799d4a6d6bf98b544dc77a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__559ef810fdc66d3cec108ab2f0554ff6e307089cade64dddea4cca8de21083bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudGatewayTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudGatewayTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudGatewayTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8736c180ba9ba41a0a5c6b2e36994c9ac36e7ceed99057e54226a611e8f8648f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SpringCloudGateway",
    "SpringCloudGatewayApiMetadata",
    "SpringCloudGatewayApiMetadataOutputReference",
    "SpringCloudGatewayClientAuthorization",
    "SpringCloudGatewayClientAuthorizationOutputReference",
    "SpringCloudGatewayConfig",
    "SpringCloudGatewayCors",
    "SpringCloudGatewayCorsOutputReference",
    "SpringCloudGatewayLocalResponseCachePerInstance",
    "SpringCloudGatewayLocalResponseCachePerInstanceOutputReference",
    "SpringCloudGatewayLocalResponseCachePerRoute",
    "SpringCloudGatewayLocalResponseCachePerRouteOutputReference",
    "SpringCloudGatewayQuota",
    "SpringCloudGatewayQuotaOutputReference",
    "SpringCloudGatewaySso",
    "SpringCloudGatewaySsoOutputReference",
    "SpringCloudGatewayTimeouts",
    "SpringCloudGatewayTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__76ea5c4c43f390c11649d0036d926660ddca068892f161b3d0babd6df0e9a2d8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    spring_cloud_service_id: builtins.str,
    api_metadata: typing.Optional[typing.Union[SpringCloudGatewayApiMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    application_performance_monitoring_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    application_performance_monitoring_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_authorization: typing.Optional[typing.Union[SpringCloudGatewayClientAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    cors: typing.Optional[typing.Union[SpringCloudGatewayCors, typing.Dict[builtins.str, typing.Any]]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_count: typing.Optional[jsii.Number] = None,
    local_response_cache_per_instance: typing.Optional[typing.Union[SpringCloudGatewayLocalResponseCachePerInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    local_response_cache_per_route: typing.Optional[typing.Union[SpringCloudGatewayLocalResponseCachePerRoute, typing.Dict[builtins.str, typing.Any]]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    quota: typing.Optional[typing.Union[SpringCloudGatewayQuota, typing.Dict[builtins.str, typing.Any]]] = None,
    sensitive_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    sso: typing.Optional[typing.Union[SpringCloudGatewaySso, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[SpringCloudGatewayTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e8d9cf08bbcd04001b6e33f3dd34a02e77f83cada8990785011daaa0c6fcd4a1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5b35b99c77c8d1f49f2e923a01db9b2d1e5b3542c49edd410c051465ec84de(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc373ac40e261600f82442aa5b469b40a70a45bfe49bd7259f87a45b4cbfc11(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ac9779dad8286db43091bcfc4015056ac54d7dad23875222d52481c5fb12ba(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e355deaa490fb58fe156b3b8f66d98cd4ea24e82499ba96e25e19eb781ab61a2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e22dfd456ab89b680fdc3c1ebb99e905f5700673a6b0e8b46180868f45df998(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d764d7e680fe5b6a4615b77d020fdf8a9885b610e9ebb59670a902715db525c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb228f34a54fa7dde443d7277fdd9e1c976a4542447d9ff42b18c7956ccdfd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca6b634ae39a9094f9b3f2bbc37f07488a07dca11676ac12f148d617d4d76f0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f008bebbd01d7234e2cec52dc1db44339e4041f2bf97fd31963230fecde4d6f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d80c74833ea1ecb700fe36a39933bc180456e27792f45e7b844fa8ed290c97e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b2191202d948787f215561fb8d229efe74117a0ce6f4750e6a0284a59b9d40(
    *,
    description: typing.Optional[builtins.str] = None,
    documentation_url: typing.Optional[builtins.str] = None,
    server_url: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d620e7c5e5b919030523947472abc1a184a4a9a619340f783e5d40cae95d5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0bf16de631f61b934d066320f2e10db2e169e32950643948af795972970cbc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc2eabf235eab52592cdc684ef0477cabcca1dbc1d71c21f81cd85aea5a4d3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede059f6cf36ced443911d51b2b2b2f00987169786816b33139a10472761b4b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0acdfde898f18729447fa4f03117fa1a513d3f2b9dbb26595206d16ba58a8fc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef3839e83670879c2bd888665495db18b6b0bd7a2cd417d1b3e7a33bfde299e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a972b9b07ebca2e1bb4ac437248f2b6cf59f36d2a8cf1eb535bfa69dbe2cdab(
    value: typing.Optional[SpringCloudGatewayApiMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4efc04a5be5be02dc8304b59eaf0f210b88fee369da8f8c9c09d3f8239bcd7(
    *,
    certificate_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    verification_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7accb34208514c59f0ac64501e8a5816b9412a160ba1821992ce778691cb43c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e0c7cdc310140607f0ba33c7a496186ea74a773f48258d56a560418272daa0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a42e3fb016c85ad3545a75b51b75d7b0a6990e656e507e619ba4cb39330ac39d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06d54adea6603da117a3053e8cd982c36f3a47247b37deb3de8a4ad712c33f1f(
    value: typing.Optional[SpringCloudGatewayClientAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958760e128879532c937531a9910df138d3deeca5d0c7b621fd14c7bb1144ec3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    spring_cloud_service_id: builtins.str,
    api_metadata: typing.Optional[typing.Union[SpringCloudGatewayApiMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    application_performance_monitoring_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    application_performance_monitoring_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_authorization: typing.Optional[typing.Union[SpringCloudGatewayClientAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    cors: typing.Optional[typing.Union[SpringCloudGatewayCors, typing.Dict[builtins.str, typing.Any]]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_count: typing.Optional[jsii.Number] = None,
    local_response_cache_per_instance: typing.Optional[typing.Union[SpringCloudGatewayLocalResponseCachePerInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    local_response_cache_per_route: typing.Optional[typing.Union[SpringCloudGatewayLocalResponseCachePerRoute, typing.Dict[builtins.str, typing.Any]]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    quota: typing.Optional[typing.Union[SpringCloudGatewayQuota, typing.Dict[builtins.str, typing.Any]]] = None,
    sensitive_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    sso: typing.Optional[typing.Union[SpringCloudGatewaySso, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[SpringCloudGatewayTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66857bab341a8d9196a0c571c7e5b36dbbc6c4a0688c306bb5648bc936f464ea(
    *,
    allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_origin_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
    credentials_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exposed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_age_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a069eab0ee657d0d5d5e17d0abc3b8bcdb741494d70a507e26653d9ba5b565(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6519100ca651e374518209e8619aa97ec3bbd68b4db819ceee4b9242552ad02e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e301ab3ed3aac6ba624843e6f5556337e26cf423d3acde596d4c8f03e04503(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3991504329cfc02f4bdf6ce92ffd25912bc55f7fc1c49f8424490c7d7333a2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a50c5b9b1d5c7000fd795aad6a69d24b637e9335d636cef5014eb405fd509d3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24cb8153e899f847b3d54911e939b0f318841b03d65d047c9b5dd295b803710a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b94318106aa7d11df6bb1aa9cf03cf18590dbbb27f1d2eb9733c2a709e6bf03(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77de9357d8cdeed75ae58d375a3ae39d531eed11c94442f3c159fa8dae64e99(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9c0965dfc044d14233b2b5d1cd7289af913284b67200754cc3e2b024b79cb1(
    value: typing.Optional[SpringCloudGatewayCors],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc165033d8460ef3b275ef4f32f28e1d6e5d350e452c939c72466cc3b251e27(
    *,
    size: typing.Optional[builtins.str] = None,
    time_to_live: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d41d5f3d16ef2b6e11da5f61927edc706e40ad319349c969b63c73916ce65fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b196910b25410b040431c8fa03abd70a19919214e1089307ab84000f3075c0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ae58794683f5d677d601962d7c7c23f889cd5135538960c3564c9c09b76d6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ba10e2ce8974894ae93fdb8d2e50aaf8d05eb76f7f419c1828dc83729c8136(
    value: typing.Optional[SpringCloudGatewayLocalResponseCachePerInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac71c986cca371eb3bde34cf65c4a58dca8bf2aa55b683b8465433cd5e63637(
    *,
    size: typing.Optional[builtins.str] = None,
    time_to_live: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a7085c399cfbcf71ab536b412c8d28c9d29d82a00bc3015c2c5d2f25a2a021(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa5d15c43ee127ece82936018fb21cc165f9358ff5ecf34d4703997197ec0b67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10e00486dba4ad882fe75b48f1b42221d7bc46bf80c3bd9fd846d7848e06ebe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df89dcb91d73d525e5c27430f4655c1e93ee36f7747213a89e86632c3369a35f(
    value: typing.Optional[SpringCloudGatewayLocalResponseCachePerRoute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c5564cda6208a8a285528193188313d8eb896104c4f80506036d8e1d077582(
    *,
    cpu: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecda1bcd54b4b57ce647c4fe1ce586ae9eab95aa976f72c10bf674bac80fa6e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7150302512da26b02c9b49f6e07004fd4b0981eb2f7c6d00b48cf0e1edf653(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ae25ab8c647db3e3c0e2e4befed55885fbb6914dabd1f81c5423cfd33668c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303940ed0df19b817ef7b14fb45a70d17457a137ee5efde2f4018f0df19f6ca9(
    value: typing.Optional[SpringCloudGatewayQuota],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608e5df39a8558e29df7ec802a2975d2be9295274a64233c9f58f93d08266d3b(
    *,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    issuer_uri: typing.Optional[builtins.str] = None,
    scope: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160b79fc76395a16a0dea901fca9b007471bae3e02ca5e1e79b069adec9e3885(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d777decc74edd6aa42154bedbc3e74ce23a92511b954ed764c04f4737c708c21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b4df3738a6290ea0c1affcf4d87a4142e876a91fbdd384c4c0c9504f941108(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973f609ba1a2c5aa706d450cfb29f5b44a065f28fb7fc275a419d5e34a361f1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc8e5d3dd3b230cb2be66579b54797163d9c1fa2c62af5cf5d2e71847e88b41(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44ab4105908faf70db5d5718e44cf278d831b861787dbe1f6476a39c39a9db6(
    value: typing.Optional[SpringCloudGatewaySso],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d210a8cf9328eaf0a9a63ad7e472ab3d32923fd3cbae74830ac509fb946ee3c6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8c32948f107fa513436da50d3555df24c845f885777248f972315e19d9ab67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c71c08496f5d580eaa474bef171ffe5ab37de17877a3b6de9010c33486074d17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab7c00a9cc9e685a9770d451062b3d4aced4ec47f0011a4cf01c6b7d53c9730(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e92ca612a1881303ee30bd61db3077d2559278ae8799d4a6d6bf98b544dc77a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__559ef810fdc66d3cec108ab2f0554ff6e307089cade64dddea4cca8de21083bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8736c180ba9ba41a0a5c6b2e36994c9ac36e7ceed99057e54226a611e8f8648f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudGatewayTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

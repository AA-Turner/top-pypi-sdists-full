r'''
# `opentelekomcloud_css_configuration_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_css_configuration_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1).
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


class CssConfigurationV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssConfigurationV1.CssConfigurationV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1 opentelekomcloud_css_configuration_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_id: builtins.str,
        auto_create_index: typing.Optional[builtins.str] = None,
        http_cors_allow_credentials: typing.Optional[builtins.str] = None,
        http_cors_allow_headers: typing.Optional[builtins.str] = None,
        http_cors_allow_methods: typing.Optional[builtins.str] = None,
        http_cors_allow_origin: typing.Optional[builtins.str] = None,
        http_cors_enabled: typing.Optional[builtins.str] = None,
        http_cors_max_age: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        indices_queries_cache_size: typing.Optional[builtins.str] = None,
        reindex_remote_whitelist: typing.Optional[builtins.str] = None,
        thread_pool_force_merge_size: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CssConfigurationV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1 opentelekomcloud_css_configuration_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_id: The CSS cluster ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#cluster_id CssConfigurationV1#cluster_id}
        :param auto_create_index: Whether to auto-create index. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#auto_create_index CssConfigurationV1#auto_create_index}
        :param http_cors_allow_credentials: Whether to return the Access-Control-Allow-Credentials of the header during cross-domain access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_allow_credentials CssConfigurationV1#http_cors_allow_credentials}
        :param http_cors_allow_headers: Headers allowed for cross-domain access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_allow_headers CssConfigurationV1#http_cors_allow_headers}
        :param http_cors_allow_methods: Methods allowed for cross-domain access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_allow_methods CssConfigurationV1#http_cors_allow_methods}
        :param http_cors_allow_origin: Origin IP address allowed for cross-domain access, for example, **122.122.122.122:9200**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_allow_origin CssConfigurationV1#http_cors_allow_origin}
        :param http_cors_enabled: Whether to allow cross-domain access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_enabled CssConfigurationV1#http_cors_enabled}
        :param http_cors_max_age: Cache duration of the browser. The cache is automatically cleared after the time range you specify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_max_age CssConfigurationV1#http_cors_max_age}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#id CssConfigurationV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param indices_queries_cache_size: Cache size in the query phase. Value range: **1** to **100**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#indices_queries_cache_size CssConfigurationV1#indices_queries_cache_size}
        :param reindex_remote_whitelist: Configured for migrating data from the current cluster to the target cluster through the reindex API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#reindex_remote_whitelist CssConfigurationV1#reindex_remote_whitelist}
        :param thread_pool_force_merge_size: Queue size in the force merge thread pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#thread_pool_force_merge_size CssConfigurationV1#thread_pool_force_merge_size}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#timeouts CssConfigurationV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e28e69e84af295ae9ab80f04ab8f0cc3a0869ad2247f2c001613a365cf7a5e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CssConfigurationV1Config(
            cluster_id=cluster_id,
            auto_create_index=auto_create_index,
            http_cors_allow_credentials=http_cors_allow_credentials,
            http_cors_allow_headers=http_cors_allow_headers,
            http_cors_allow_methods=http_cors_allow_methods,
            http_cors_allow_origin=http_cors_allow_origin,
            http_cors_enabled=http_cors_enabled,
            http_cors_max_age=http_cors_max_age,
            id=id,
            indices_queries_cache_size=indices_queries_cache_size,
            reindex_remote_whitelist=reindex_remote_whitelist,
            thread_pool_force_merge_size=thread_pool_force_merge_size,
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
        '''Generates CDKTF code for importing a CssConfigurationV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CssConfigurationV1 to import.
        :param import_from_id: The id of the existing CssConfigurationV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CssConfigurationV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73dd4b3a922fbe2682d4f405ac0273229b8b3e6233062bb799a0d5598597bc8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#create CssConfigurationV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#delete CssConfigurationV1#delete}.
        '''
        value = CssConfigurationV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoCreateIndex")
    def reset_auto_create_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoCreateIndex", []))

    @jsii.member(jsii_name="resetHttpCorsAllowCredentials")
    def reset_http_cors_allow_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpCorsAllowCredentials", []))

    @jsii.member(jsii_name="resetHttpCorsAllowHeaders")
    def reset_http_cors_allow_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpCorsAllowHeaders", []))

    @jsii.member(jsii_name="resetHttpCorsAllowMethods")
    def reset_http_cors_allow_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpCorsAllowMethods", []))

    @jsii.member(jsii_name="resetHttpCorsAllowOrigin")
    def reset_http_cors_allow_origin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpCorsAllowOrigin", []))

    @jsii.member(jsii_name="resetHttpCorsEnabled")
    def reset_http_cors_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpCorsEnabled", []))

    @jsii.member(jsii_name="resetHttpCorsMaxAge")
    def reset_http_cors_max_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpCorsMaxAge", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIndicesQueriesCacheSize")
    def reset_indices_queries_cache_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndicesQueriesCacheSize", []))

    @jsii.member(jsii_name="resetReindexRemoteWhitelist")
    def reset_reindex_remote_whitelist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReindexRemoteWhitelist", []))

    @jsii.member(jsii_name="resetThreadPoolForceMergeSize")
    def reset_thread_pool_force_merge_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreadPoolForceMergeSize", []))

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
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CssConfigurationV1TimeoutsOutputReference":
        return typing.cast("CssConfigurationV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoCreateIndexInput")
    def auto_create_index_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoCreateIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="httpCorsAllowCredentialsInput")
    def http_cors_allow_credentials_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpCorsAllowCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpCorsAllowHeadersInput")
    def http_cors_allow_headers_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpCorsAllowHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="httpCorsAllowMethodsInput")
    def http_cors_allow_methods_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpCorsAllowMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpCorsAllowOriginInput")
    def http_cors_allow_origin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpCorsAllowOriginInput"))

    @builtins.property
    @jsii.member(jsii_name="httpCorsEnabledInput")
    def http_cors_enabled_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpCorsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="httpCorsMaxAgeInput")
    def http_cors_max_age_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpCorsMaxAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="indicesQueriesCacheSizeInput")
    def indices_queries_cache_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indicesQueriesCacheSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="reindexRemoteWhitelistInput")
    def reindex_remote_whitelist_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reindexRemoteWhitelistInput"))

    @builtins.property
    @jsii.member(jsii_name="threadPoolForceMergeSizeInput")
    def thread_pool_force_merge_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "threadPoolForceMergeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CssConfigurationV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CssConfigurationV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoCreateIndex")
    def auto_create_index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoCreateIndex"))

    @auto_create_index.setter
    def auto_create_index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466cdc801c84520e32316a3ac02aa86e6470b6a9cf6fe3b74ba5eb40762ce5d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoCreateIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d2a400852d31e1568bc629a37592ece1dc2e2d6d6459fca417c273f63a13d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpCorsAllowCredentials")
    def http_cors_allow_credentials(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpCorsAllowCredentials"))

    @http_cors_allow_credentials.setter
    def http_cors_allow_credentials(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac3d71a4ff70772930032667138225ce278b18735033eb9ccd7d12e8e4b76862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpCorsAllowCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpCorsAllowHeaders")
    def http_cors_allow_headers(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpCorsAllowHeaders"))

    @http_cors_allow_headers.setter
    def http_cors_allow_headers(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e83190ec0c3df624dcf74203b33541f873dcda544c9fc216591742c56769e1ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpCorsAllowHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpCorsAllowMethods")
    def http_cors_allow_methods(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpCorsAllowMethods"))

    @http_cors_allow_methods.setter
    def http_cors_allow_methods(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd30efc751cb834a0ae9722c703ec808f17685680539f2c44e4fd1babd56ee0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpCorsAllowMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpCorsAllowOrigin")
    def http_cors_allow_origin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpCorsAllowOrigin"))

    @http_cors_allow_origin.setter
    def http_cors_allow_origin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce45464359d20755f7ef9ba02bb92951b7d6f3b84349effa4e72718fdfeb0e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpCorsAllowOrigin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpCorsEnabled")
    def http_cors_enabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpCorsEnabled"))

    @http_cors_enabled.setter
    def http_cors_enabled(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e727764788278927e02d921f39caac2a1e4a38979315e843aa057ddfc7f2289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpCorsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpCorsMaxAge")
    def http_cors_max_age(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpCorsMaxAge"))

    @http_cors_max_age.setter
    def http_cors_max_age(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65b878a20c9d9a6e73f8271ed0e178e5962cc674347f78b77fca6a964b810d9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpCorsMaxAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dda29e62d65741c6f891aacd9e3a654f4606ae29981f5d913e6ba812d08bc79d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indicesQueriesCacheSize")
    def indices_queries_cache_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indicesQueriesCacheSize"))

    @indices_queries_cache_size.setter
    def indices_queries_cache_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c5594aedf722db5bd2df89931b2c113fb0e04e3662c30a677c4c6d266af5af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indicesQueriesCacheSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reindexRemoteWhitelist")
    def reindex_remote_whitelist(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reindexRemoteWhitelist"))

    @reindex_remote_whitelist.setter
    def reindex_remote_whitelist(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f549061fbedd8b4173e956f992e9ce6fc29640a7bd13f0d3b613683639c42746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reindexRemoteWhitelist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threadPoolForceMergeSize")
    def thread_pool_force_merge_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "threadPoolForceMergeSize"))

    @thread_pool_force_merge_size.setter
    def thread_pool_force_merge_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b113c4bb4118199e1142a6af3b8831fe799d372f8684ba284eea0e8600f7f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threadPoolForceMergeSize", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cssConfigurationV1.CssConfigurationV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_id": "clusterId",
        "auto_create_index": "autoCreateIndex",
        "http_cors_allow_credentials": "httpCorsAllowCredentials",
        "http_cors_allow_headers": "httpCorsAllowHeaders",
        "http_cors_allow_methods": "httpCorsAllowMethods",
        "http_cors_allow_origin": "httpCorsAllowOrigin",
        "http_cors_enabled": "httpCorsEnabled",
        "http_cors_max_age": "httpCorsMaxAge",
        "id": "id",
        "indices_queries_cache_size": "indicesQueriesCacheSize",
        "reindex_remote_whitelist": "reindexRemoteWhitelist",
        "thread_pool_force_merge_size": "threadPoolForceMergeSize",
        "timeouts": "timeouts",
    },
)
class CssConfigurationV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster_id: builtins.str,
        auto_create_index: typing.Optional[builtins.str] = None,
        http_cors_allow_credentials: typing.Optional[builtins.str] = None,
        http_cors_allow_headers: typing.Optional[builtins.str] = None,
        http_cors_allow_methods: typing.Optional[builtins.str] = None,
        http_cors_allow_origin: typing.Optional[builtins.str] = None,
        http_cors_enabled: typing.Optional[builtins.str] = None,
        http_cors_max_age: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        indices_queries_cache_size: typing.Optional[builtins.str] = None,
        reindex_remote_whitelist: typing.Optional[builtins.str] = None,
        thread_pool_force_merge_size: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CssConfigurationV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_id: The CSS cluster ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#cluster_id CssConfigurationV1#cluster_id}
        :param auto_create_index: Whether to auto-create index. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#auto_create_index CssConfigurationV1#auto_create_index}
        :param http_cors_allow_credentials: Whether to return the Access-Control-Allow-Credentials of the header during cross-domain access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_allow_credentials CssConfigurationV1#http_cors_allow_credentials}
        :param http_cors_allow_headers: Headers allowed for cross-domain access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_allow_headers CssConfigurationV1#http_cors_allow_headers}
        :param http_cors_allow_methods: Methods allowed for cross-domain access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_allow_methods CssConfigurationV1#http_cors_allow_methods}
        :param http_cors_allow_origin: Origin IP address allowed for cross-domain access, for example, **122.122.122.122:9200**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_allow_origin CssConfigurationV1#http_cors_allow_origin}
        :param http_cors_enabled: Whether to allow cross-domain access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_enabled CssConfigurationV1#http_cors_enabled}
        :param http_cors_max_age: Cache duration of the browser. The cache is automatically cleared after the time range you specify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_max_age CssConfigurationV1#http_cors_max_age}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#id CssConfigurationV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param indices_queries_cache_size: Cache size in the query phase. Value range: **1** to **100**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#indices_queries_cache_size CssConfigurationV1#indices_queries_cache_size}
        :param reindex_remote_whitelist: Configured for migrating data from the current cluster to the target cluster through the reindex API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#reindex_remote_whitelist CssConfigurationV1#reindex_remote_whitelist}
        :param thread_pool_force_merge_size: Queue size in the force merge thread pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#thread_pool_force_merge_size CssConfigurationV1#thread_pool_force_merge_size}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#timeouts CssConfigurationV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = CssConfigurationV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7df2e29547f1bce4d0eaacac53ba2658df81b6a8b0dd0e751c2199925e3dbf0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument auto_create_index", value=auto_create_index, expected_type=type_hints["auto_create_index"])
            check_type(argname="argument http_cors_allow_credentials", value=http_cors_allow_credentials, expected_type=type_hints["http_cors_allow_credentials"])
            check_type(argname="argument http_cors_allow_headers", value=http_cors_allow_headers, expected_type=type_hints["http_cors_allow_headers"])
            check_type(argname="argument http_cors_allow_methods", value=http_cors_allow_methods, expected_type=type_hints["http_cors_allow_methods"])
            check_type(argname="argument http_cors_allow_origin", value=http_cors_allow_origin, expected_type=type_hints["http_cors_allow_origin"])
            check_type(argname="argument http_cors_enabled", value=http_cors_enabled, expected_type=type_hints["http_cors_enabled"])
            check_type(argname="argument http_cors_max_age", value=http_cors_max_age, expected_type=type_hints["http_cors_max_age"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument indices_queries_cache_size", value=indices_queries_cache_size, expected_type=type_hints["indices_queries_cache_size"])
            check_type(argname="argument reindex_remote_whitelist", value=reindex_remote_whitelist, expected_type=type_hints["reindex_remote_whitelist"])
            check_type(argname="argument thread_pool_force_merge_size", value=thread_pool_force_merge_size, expected_type=type_hints["thread_pool_force_merge_size"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_id": cluster_id,
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
        if auto_create_index is not None:
            self._values["auto_create_index"] = auto_create_index
        if http_cors_allow_credentials is not None:
            self._values["http_cors_allow_credentials"] = http_cors_allow_credentials
        if http_cors_allow_headers is not None:
            self._values["http_cors_allow_headers"] = http_cors_allow_headers
        if http_cors_allow_methods is not None:
            self._values["http_cors_allow_methods"] = http_cors_allow_methods
        if http_cors_allow_origin is not None:
            self._values["http_cors_allow_origin"] = http_cors_allow_origin
        if http_cors_enabled is not None:
            self._values["http_cors_enabled"] = http_cors_enabled
        if http_cors_max_age is not None:
            self._values["http_cors_max_age"] = http_cors_max_age
        if id is not None:
            self._values["id"] = id
        if indices_queries_cache_size is not None:
            self._values["indices_queries_cache_size"] = indices_queries_cache_size
        if reindex_remote_whitelist is not None:
            self._values["reindex_remote_whitelist"] = reindex_remote_whitelist
        if thread_pool_force_merge_size is not None:
            self._values["thread_pool_force_merge_size"] = thread_pool_force_merge_size
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
    def cluster_id(self) -> builtins.str:
        '''The CSS cluster ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#cluster_id CssConfigurationV1#cluster_id}
        '''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_create_index(self) -> typing.Optional[builtins.str]:
        '''Whether to auto-create index.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#auto_create_index CssConfigurationV1#auto_create_index}
        '''
        result = self._values.get("auto_create_index")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_cors_allow_credentials(self) -> typing.Optional[builtins.str]:
        '''Whether to return the Access-Control-Allow-Credentials of the header during cross-domain access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_allow_credentials CssConfigurationV1#http_cors_allow_credentials}
        '''
        result = self._values.get("http_cors_allow_credentials")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_cors_allow_headers(self) -> typing.Optional[builtins.str]:
        '''Headers allowed for cross-domain access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_allow_headers CssConfigurationV1#http_cors_allow_headers}
        '''
        result = self._values.get("http_cors_allow_headers")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_cors_allow_methods(self) -> typing.Optional[builtins.str]:
        '''Methods allowed for cross-domain access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_allow_methods CssConfigurationV1#http_cors_allow_methods}
        '''
        result = self._values.get("http_cors_allow_methods")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_cors_allow_origin(self) -> typing.Optional[builtins.str]:
        '''Origin IP address allowed for cross-domain access, for example, **122.122.122.122:9200**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_allow_origin CssConfigurationV1#http_cors_allow_origin}
        '''
        result = self._values.get("http_cors_allow_origin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_cors_enabled(self) -> typing.Optional[builtins.str]:
        '''Whether to allow cross-domain access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_enabled CssConfigurationV1#http_cors_enabled}
        '''
        result = self._values.get("http_cors_enabled")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_cors_max_age(self) -> typing.Optional[builtins.str]:
        '''Cache duration of the browser. The cache is automatically cleared after the time range you specify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#http_cors_max_age CssConfigurationV1#http_cors_max_age}
        '''
        result = self._values.get("http_cors_max_age")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#id CssConfigurationV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def indices_queries_cache_size(self) -> typing.Optional[builtins.str]:
        '''Cache size in the query phase. Value range: **1** to **100**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#indices_queries_cache_size CssConfigurationV1#indices_queries_cache_size}
        '''
        result = self._values.get("indices_queries_cache_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reindex_remote_whitelist(self) -> typing.Optional[builtins.str]:
        '''Configured for migrating data from the current cluster to the target cluster through the reindex API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#reindex_remote_whitelist CssConfigurationV1#reindex_remote_whitelist}
        '''
        result = self._values.get("reindex_remote_whitelist")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def thread_pool_force_merge_size(self) -> typing.Optional[builtins.str]:
        '''Queue size in the force merge thread pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#thread_pool_force_merge_size CssConfigurationV1#thread_pool_force_merge_size}
        '''
        result = self._values.get("thread_pool_force_merge_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CssConfigurationV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#timeouts CssConfigurationV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CssConfigurationV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssConfigurationV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cssConfigurationV1.CssConfigurationV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class CssConfigurationV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#create CssConfigurationV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#delete CssConfigurationV1#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e07a6a522ea6c641d224b49bbc76ed4990726a672a2966ca55171f2b2ea651)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#create CssConfigurationV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_configuration_v1#delete CssConfigurationV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssConfigurationV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CssConfigurationV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssConfigurationV1.CssConfigurationV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6820367e54d28cec5c97db37eb9b04f3c9043521a70348044700e25728458ac7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9642ab39c4955a1238d0c5489626077982014521dbdc205715e632bf2699be7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c5e1723561b0e5f77fe2c757cfb480a313266a7311b12669d7a52afade883c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CssConfigurationV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CssConfigurationV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CssConfigurationV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e86706dd8c57928d461c23fbd005ef4904fb947ed1a06de87e56163e902ab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CssConfigurationV1",
    "CssConfigurationV1Config",
    "CssConfigurationV1Timeouts",
    "CssConfigurationV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d5e28e69e84af295ae9ab80f04ab8f0cc3a0869ad2247f2c001613a365cf7a5e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_id: builtins.str,
    auto_create_index: typing.Optional[builtins.str] = None,
    http_cors_allow_credentials: typing.Optional[builtins.str] = None,
    http_cors_allow_headers: typing.Optional[builtins.str] = None,
    http_cors_allow_methods: typing.Optional[builtins.str] = None,
    http_cors_allow_origin: typing.Optional[builtins.str] = None,
    http_cors_enabled: typing.Optional[builtins.str] = None,
    http_cors_max_age: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    indices_queries_cache_size: typing.Optional[builtins.str] = None,
    reindex_remote_whitelist: typing.Optional[builtins.str] = None,
    thread_pool_force_merge_size: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CssConfigurationV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c73dd4b3a922fbe2682d4f405ac0273229b8b3e6233062bb799a0d5598597bc8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466cdc801c84520e32316a3ac02aa86e6470b6a9cf6fe3b74ba5eb40762ce5d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d2a400852d31e1568bc629a37592ece1dc2e2d6d6459fca417c273f63a13d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3d71a4ff70772930032667138225ce278b18735033eb9ccd7d12e8e4b76862(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83190ec0c3df624dcf74203b33541f873dcda544c9fc216591742c56769e1ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd30efc751cb834a0ae9722c703ec808f17685680539f2c44e4fd1babd56ee0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce45464359d20755f7ef9ba02bb92951b7d6f3b84349effa4e72718fdfeb0e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e727764788278927e02d921f39caac2a1e4a38979315e843aa057ddfc7f2289(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b878a20c9d9a6e73f8271ed0e178e5962cc674347f78b77fca6a964b810d9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dda29e62d65741c6f891aacd9e3a654f4606ae29981f5d913e6ba812d08bc79d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c5594aedf722db5bd2df89931b2c113fb0e04e3662c30a677c4c6d266af5af9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f549061fbedd8b4173e956f992e9ce6fc29640a7bd13f0d3b613683639c42746(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b113c4bb4118199e1142a6af3b8831fe799d372f8684ba284eea0e8600f7f5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7df2e29547f1bce4d0eaacac53ba2658df81b6a8b0dd0e751c2199925e3dbf0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_id: builtins.str,
    auto_create_index: typing.Optional[builtins.str] = None,
    http_cors_allow_credentials: typing.Optional[builtins.str] = None,
    http_cors_allow_headers: typing.Optional[builtins.str] = None,
    http_cors_allow_methods: typing.Optional[builtins.str] = None,
    http_cors_allow_origin: typing.Optional[builtins.str] = None,
    http_cors_enabled: typing.Optional[builtins.str] = None,
    http_cors_max_age: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    indices_queries_cache_size: typing.Optional[builtins.str] = None,
    reindex_remote_whitelist: typing.Optional[builtins.str] = None,
    thread_pool_force_merge_size: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CssConfigurationV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e07a6a522ea6c641d224b49bbc76ed4990726a672a2966ca55171f2b2ea651(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6820367e54d28cec5c97db37eb9b04f3c9043521a70348044700e25728458ac7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9642ab39c4955a1238d0c5489626077982014521dbdc205715e632bf2699be7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c5e1723561b0e5f77fe2c757cfb480a313266a7311b12669d7a52afade883c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e86706dd8c57928d461c23fbd005ef4904fb947ed1a06de87e56163e902ab8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CssConfigurationV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

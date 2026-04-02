r'''
# `google_apigee_api_product`

Refer to the Terraform Registry for docs: [`google_apigee_api_product`](https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product).
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


class GoogleApigeeApiProduct(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProduct",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product google_apigee_api_product}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        name: builtins.str,
        org_id: builtins.str,
        api_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        approval_type: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeApiProductAttributes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        environments: typing.Optional[typing.Sequence[builtins.str]] = None,
        graphql_operation_group: typing.Optional[typing.Union["GoogleApigeeApiProductGraphqlOperationGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_operation_group: typing.Optional[typing.Union["GoogleApigeeApiProductGrpcOperationGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        operation_group: typing.Optional[typing.Union["GoogleApigeeApiProductOperationGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
        quota: typing.Optional[builtins.str] = None,
        quota_counter_scope: typing.Optional[builtins.str] = None,
        quota_interval: typing.Optional[builtins.str] = None,
        quota_time_unit: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        space: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeApiProductTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product google_apigee_api_product} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Name displayed in the UI or developer portal to developers registering for API access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#display_name GoogleApigeeApiProduct#display_name}
        :param name: Internal name of the API product. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#name GoogleApigeeApiProduct#name}
        :param org_id: The Apigee Organization associated with the Apigee API product, in the format 'organizations/{{org_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#org_id GoogleApigeeApiProduct#org_id}
        :param api_resources: Comma-separated list of API resources to be bundled in the API product. By default, the resource paths are mapped from the proxy.pathsuffix variable. The proxy path suffix is defined as the URI fragment following the ProxyEndpoint base path. For example, if the apiResources element is defined to be /forecastrss and the base path defined for the API proxy is /weather, then only requests to /weather/forecastrss are permitted by the API product. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#api_resources GoogleApigeeApiProduct#api_resources}
        :param approval_type: Flag that specifies how API keys are approved to access the APIs defined by the API product. Valid values are 'auto' or 'manual'. Possible values: ["auto", "manual"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#approval_type GoogleApigeeApiProduct#approval_type}
        :param attributes: attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#attributes GoogleApigeeApiProduct#attributes}
        :param description: Description of the API product. Include key information about the API product that is not captured by other fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#description GoogleApigeeApiProduct#description}
        :param environments: Comma-separated list of environment names to which the API product is bound. Requests to environments that are not listed are rejected. By specifying one or more environments, you can bind the resources listed in the API product to a specific environment, preventing developers from accessing those resources through API proxies deployed in another environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#environments GoogleApigeeApiProduct#environments}
        :param graphql_operation_group: graphql_operation_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#graphql_operation_group GoogleApigeeApiProduct#graphql_operation_group}
        :param grpc_operation_group: grpc_operation_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#grpc_operation_group GoogleApigeeApiProduct#grpc_operation_group}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#id GoogleApigeeApiProduct#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param operation_group: operation_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_group GoogleApigeeApiProduct#operation_group}
        :param proxies: Comma-separated list of API proxy names to which this API product is bound. By specifying API proxies, you can associate resources in the API product with specific API proxies, preventing developers from accessing those resources through other API proxies. Apigee rejects requests to API proxies that are not listed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#proxies GoogleApigeeApiProduct#proxies}
        :param quota: Number of request messages permitted per app by this API product for the specified quotaInterval and quotaTimeUnit. For example, a quota of 50, for a quotaInterval of 12 and a quotaTimeUnit of hours means 50 requests are allowed every 12 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota GoogleApigeeApiProduct#quota}
        :param quota_counter_scope: Scope of the quota decides how the quota counter gets applied and evaluate for quota violation. If the Scope is set as PROXY, then all the operations defined for the APIproduct that are associated with the same proxy will share the same quota counter set at the APIproduct level, making it a global counter at a proxy level. If the Scope is set as OPERATION, then each operations get the counter set at the API product dedicated, making it a local counter. Note that, the QuotaCounterScope applies only when an operation does not have dedicated quota set for itself. Possible values: ["QUOTA_COUNTER_SCOPE_UNSPECIFIED", "PROXY", "OPERATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota_counter_scope GoogleApigeeApiProduct#quota_counter_scope}
        :param quota_interval: Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota_interval GoogleApigeeApiProduct#quota_interval}
        :param quota_time_unit: Time unit defined for the quotaInterval. Valid values include second, minute, hour, day, month or year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota_time_unit GoogleApigeeApiProduct#quota_time_unit}
        :param scopes: Comma-separated list of OAuth scopes that are validated at runtime. Apigee validates that the scopes in any access token presented match the scopes defined in the OAuth policy associated with the API product. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#scopes GoogleApigeeApiProduct#scopes}
        :param space: Optional. The resource ID of the parent Space. If not set, the parent resource will be the Organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#space GoogleApigeeApiProduct#space}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#timeouts GoogleApigeeApiProduct#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33fee3793f5c7cfdf853bc7f94cf2fdda03d5a3ebce935e173face88980d4c28)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleApigeeApiProductConfig(
            display_name=display_name,
            name=name,
            org_id=org_id,
            api_resources=api_resources,
            approval_type=approval_type,
            attributes=attributes,
            description=description,
            environments=environments,
            graphql_operation_group=graphql_operation_group,
            grpc_operation_group=grpc_operation_group,
            id=id,
            operation_group=operation_group,
            proxies=proxies,
            quota=quota,
            quota_counter_scope=quota_counter_scope,
            quota_interval=quota_interval,
            quota_time_unit=quota_time_unit,
            scopes=scopes,
            space=space,
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
        '''Generates CDKTF code for importing a GoogleApigeeApiProduct resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleApigeeApiProduct to import.
        :param import_from_id: The id of the existing GoogleApigeeApiProduct that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleApigeeApiProduct to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c7775c8d793754dd087a8269e81d7caae77155cd08b12ae7aa224c8ae74704)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAttributes")
    def put_attributes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeApiProductAttributes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a481cd3d3ab4b2120e39f468208e4fe489a8904333aed23ab5d1d602e7143af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAttributes", [value]))

    @jsii.member(jsii_name="putGraphqlOperationGroup")
    def put_graphql_operation_group(
        self,
        *,
        operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operation_config_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operation_configs: operation_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_configs GoogleApigeeApiProduct#operation_configs}
        :param operation_config_type: Flag that specifes whether the configuration is for Apigee API proxy or a remote service. Valid values include proxy or remoteservice. Defaults to proxy. Set to proxy when Apigee API proxies are associated with the API product. Set to remoteservice when non-Apigee proxies like Istio-Envoy are associated with the API product. Possible values: ["proxy", "remoteservice"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_config_type GoogleApigeeApiProduct#operation_config_type}
        '''
        value = GoogleApigeeApiProductGraphqlOperationGroup(
            operation_configs=operation_configs,
            operation_config_type=operation_config_type,
        )

        return typing.cast(None, jsii.invoke(self, "putGraphqlOperationGroup", [value]))

    @jsii.member(jsii_name="putGrpcOperationGroup")
    def put_grpc_operation_group(
        self,
        *,
        operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeApiProductGrpcOperationGroupOperationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param operation_configs: operation_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_configs GoogleApigeeApiProduct#operation_configs}
        '''
        value = GoogleApigeeApiProductGrpcOperationGroup(
            operation_configs=operation_configs
        )

        return typing.cast(None, jsii.invoke(self, "putGrpcOperationGroup", [value]))

    @jsii.member(jsii_name="putOperationGroup")
    def put_operation_group(
        self,
        *,
        operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeApiProductOperationGroupOperationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operation_config_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operation_configs: operation_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_configs GoogleApigeeApiProduct#operation_configs}
        :param operation_config_type: Flag that specifes whether the configuration is for Apigee API proxy or a remote service. Valid values include proxy or remoteservice. Defaults to proxy. Set to proxy when Apigee API proxies are associated with the API product. Set to remoteservice when non-Apigee proxies like Istio-Envoy are associated with the API product. Possible values: ["proxy", "remoteservice"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_config_type GoogleApigeeApiProduct#operation_config_type}
        '''
        value = GoogleApigeeApiProductOperationGroup(
            operation_configs=operation_configs,
            operation_config_type=operation_config_type,
        )

        return typing.cast(None, jsii.invoke(self, "putOperationGroup", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#create GoogleApigeeApiProduct#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#delete GoogleApigeeApiProduct#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#update GoogleApigeeApiProduct#update}.
        '''
        value = GoogleApigeeApiProductTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetApiResources")
    def reset_api_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiResources", []))

    @jsii.member(jsii_name="resetApprovalType")
    def reset_approval_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprovalType", []))

    @jsii.member(jsii_name="resetAttributes")
    def reset_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributes", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnvironments")
    def reset_environments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironments", []))

    @jsii.member(jsii_name="resetGraphqlOperationGroup")
    def reset_graphql_operation_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGraphqlOperationGroup", []))

    @jsii.member(jsii_name="resetGrpcOperationGroup")
    def reset_grpc_operation_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpcOperationGroup", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOperationGroup")
    def reset_operation_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationGroup", []))

    @jsii.member(jsii_name="resetProxies")
    def reset_proxies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxies", []))

    @jsii.member(jsii_name="resetQuota")
    def reset_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuota", []))

    @jsii.member(jsii_name="resetQuotaCounterScope")
    def reset_quota_counter_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuotaCounterScope", []))

    @jsii.member(jsii_name="resetQuotaInterval")
    def reset_quota_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuotaInterval", []))

    @jsii.member(jsii_name="resetQuotaTimeUnit")
    def reset_quota_time_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuotaTimeUnit", []))

    @jsii.member(jsii_name="resetScopes")
    def reset_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopes", []))

    @jsii.member(jsii_name="resetSpace")
    def reset_space(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpace", []))

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
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> "GoogleApigeeApiProductAttributesList":
        return typing.cast("GoogleApigeeApiProductAttributesList", jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="graphqlOperationGroup")
    def graphql_operation_group(
        self,
    ) -> "GoogleApigeeApiProductGraphqlOperationGroupOutputReference":
        return typing.cast("GoogleApigeeApiProductGraphqlOperationGroupOutputReference", jsii.get(self, "graphqlOperationGroup"))

    @builtins.property
    @jsii.member(jsii_name="grpcOperationGroup")
    def grpc_operation_group(
        self,
    ) -> "GoogleApigeeApiProductGrpcOperationGroupOutputReference":
        return typing.cast("GoogleApigeeApiProductGrpcOperationGroupOutputReference", jsii.get(self, "grpcOperationGroup"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedAt")
    def last_modified_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifiedAt"))

    @builtins.property
    @jsii.member(jsii_name="operationGroup")
    def operation_group(self) -> "GoogleApigeeApiProductOperationGroupOutputReference":
        return typing.cast("GoogleApigeeApiProductOperationGroupOutputReference", jsii.get(self, "operationGroup"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleApigeeApiProductTimeoutsOutputReference":
        return typing.cast("GoogleApigeeApiProductTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="apiResourcesInput")
    def api_resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "apiResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalTypeInput")
    def approval_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "approvalTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductAttributes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductAttributes"]]], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentsInput")
    def environments_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "environmentsInput"))

    @builtins.property
    @jsii.member(jsii_name="graphqlOperationGroupInput")
    def graphql_operation_group_input(
        self,
    ) -> typing.Optional["GoogleApigeeApiProductGraphqlOperationGroup"]:
        return typing.cast(typing.Optional["GoogleApigeeApiProductGraphqlOperationGroup"], jsii.get(self, "graphqlOperationGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcOperationGroupInput")
    def grpc_operation_group_input(
        self,
    ) -> typing.Optional["GoogleApigeeApiProductGrpcOperationGroup"]:
        return typing.cast(typing.Optional["GoogleApigeeApiProductGrpcOperationGroup"], jsii.get(self, "grpcOperationGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="operationGroupInput")
    def operation_group_input(
        self,
    ) -> typing.Optional["GoogleApigeeApiProductOperationGroup"]:
        return typing.cast(typing.Optional["GoogleApigeeApiProductOperationGroup"], jsii.get(self, "operationGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="orgIdInput")
    def org_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgIdInput"))

    @builtins.property
    @jsii.member(jsii_name="proxiesInput")
    def proxies_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "proxiesInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaCounterScopeInput")
    def quota_counter_scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quotaCounterScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaInput")
    def quota_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quotaInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaIntervalInput")
    def quota_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quotaIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaTimeUnitInput")
    def quota_time_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quotaTimeUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="spaceInput")
    def space_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spaceInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeApiProductTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeApiProductTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="apiResources")
    def api_resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apiResources"))

    @api_resources.setter
    def api_resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__669868253939cebc06f197fca4fb2a0661b1d00a170ff984fa0c830c09dbd49b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="approvalType")
    def approval_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "approvalType"))

    @approval_type.setter
    def approval_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947853c0faaedc690d9885bcc4ca79b878fa16523d4eec7e122d3469c210ac3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approvalType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__188e0508c0888e679ad5166b0cd28d645f905a35ffcb3036ff59d6468d83c2ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b25cdef51640a4d0aa77efd6be11cfa8fcb7151d95078a847e596729f5b529e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environments")
    def environments(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "environments"))

    @environments.setter
    def environments(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__012fe2165426c8a6dc38fed5b39dafe54eaf175f9e73a4add9c9690ef28b3d3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2a6453e3acd476b4887236155f8b5924330244fd5fc1b28473252360f5fc2e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dff35e929574f73ec4df769bdd7e2690f9cc806f661d588a18afd634ee3bb44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @org_id.setter
    def org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__152812118ffd3b3360686624727b460d8506b82db44cb52c07a4a90ae4305e42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxies")
    def proxies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "proxies"))

    @proxies.setter
    def proxies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78aa7aac21e055b917672c2b238c776f6c59dda915e504e90074e4ada8da8c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quota")
    def quota(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quota"))

    @quota.setter
    def quota(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__595ee6f4f65602c7bc5ef5b9fe8e9514620af5b2c4dd41fa4b213eb6f201157b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quota", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quotaCounterScope")
    def quota_counter_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quotaCounterScope"))

    @quota_counter_scope.setter
    def quota_counter_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__875fd5f1e8c485e6d033f428cf5c002412b4a66e4b1ab7e30d1e750c761ac622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotaCounterScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quotaInterval")
    def quota_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quotaInterval"))

    @quota_interval.setter
    def quota_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98be399cf02c8821ce3c8e9bcd996595698181804b13f08dd709e20385f1252a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotaInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quotaTimeUnit")
    def quota_time_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quotaTimeUnit"))

    @quota_time_unit.setter
    def quota_time_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec44498a65b86b553b4c9654ccbe0ab09108288bc8ce1efd494de2066442eb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotaTimeUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6cb2ad432efad35dc4a22171c5c7752790986d7d64479c7e3dea337a56b55e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="space")
    def space(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "space"))

    @space.setter
    def space(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377297d908886bde0706f12aba2eff3c254361ef1bc27abba371fc600078c687)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "space", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductAttributes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleApigeeApiProductAttributes:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Key of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#name GoogleApigeeApiProduct#name}
        :param value: Value of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#value GoogleApigeeApiProduct#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a3ee76430cda167fd930af908d589889c36308eac05d5b36c33a30fceb2edc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Key of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#name GoogleApigeeApiProduct#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#value GoogleApigeeApiProduct#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeApiProductAttributesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductAttributesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1358ca9e99b4b62203ada4ab5634f0138921898e3edee94a8465535795708bd5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApigeeApiProductAttributesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecfe13f870ba930d1ae54493244694c308435008dfe13f5275a7dd73410f64a8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApigeeApiProductAttributesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__048bdad59d5b0fc352b431a7096ea2890c28a6df44f5ad2f151a0f750e268de4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c47e2a54b40975e6d9411ed9b040977bbb1538f250b3d3e12a492773fa67dc68)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d39ca2277e587f7ac7bcb5bcd2b159001f418405752e65061a99aa7c8aeb882)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductAttributes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductAttributes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ec9ae86291a6873d6bfb579da6a04c31be2b36f6ec6ce39251723bf080462ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeApiProductAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductAttributesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fcda4a05dcd04361f070e4aa3ec176f5a21913437ff8b251fffb6d16eb2db3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bde72aabea3785af439489b6ae9182a309f5b05e69665355d150a2464db0844b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6589392c2a3b5c971b3e8a51e5065252e5ff6b0a26f8075f8411e1aff736bc20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__803e640ae55d649303c75a95457371f8fb80b0c742d6961991f4b00186d714d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "name": "name",
        "org_id": "orgId",
        "api_resources": "apiResources",
        "approval_type": "approvalType",
        "attributes": "attributes",
        "description": "description",
        "environments": "environments",
        "graphql_operation_group": "graphqlOperationGroup",
        "grpc_operation_group": "grpcOperationGroup",
        "id": "id",
        "operation_group": "operationGroup",
        "proxies": "proxies",
        "quota": "quota",
        "quota_counter_scope": "quotaCounterScope",
        "quota_interval": "quotaInterval",
        "quota_time_unit": "quotaTimeUnit",
        "scopes": "scopes",
        "space": "space",
        "timeouts": "timeouts",
    },
)
class GoogleApigeeApiProductConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        name: builtins.str,
        org_id: builtins.str,
        api_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        approval_type: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductAttributes, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        environments: typing.Optional[typing.Sequence[builtins.str]] = None,
        graphql_operation_group: typing.Optional[typing.Union["GoogleApigeeApiProductGraphqlOperationGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_operation_group: typing.Optional[typing.Union["GoogleApigeeApiProductGrpcOperationGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        operation_group: typing.Optional[typing.Union["GoogleApigeeApiProductOperationGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
        quota: typing.Optional[builtins.str] = None,
        quota_counter_scope: typing.Optional[builtins.str] = None,
        quota_interval: typing.Optional[builtins.str] = None,
        quota_time_unit: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        space: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeApiProductTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Name displayed in the UI or developer portal to developers registering for API access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#display_name GoogleApigeeApiProduct#display_name}
        :param name: Internal name of the API product. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#name GoogleApigeeApiProduct#name}
        :param org_id: The Apigee Organization associated with the Apigee API product, in the format 'organizations/{{org_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#org_id GoogleApigeeApiProduct#org_id}
        :param api_resources: Comma-separated list of API resources to be bundled in the API product. By default, the resource paths are mapped from the proxy.pathsuffix variable. The proxy path suffix is defined as the URI fragment following the ProxyEndpoint base path. For example, if the apiResources element is defined to be /forecastrss and the base path defined for the API proxy is /weather, then only requests to /weather/forecastrss are permitted by the API product. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#api_resources GoogleApigeeApiProduct#api_resources}
        :param approval_type: Flag that specifies how API keys are approved to access the APIs defined by the API product. Valid values are 'auto' or 'manual'. Possible values: ["auto", "manual"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#approval_type GoogleApigeeApiProduct#approval_type}
        :param attributes: attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#attributes GoogleApigeeApiProduct#attributes}
        :param description: Description of the API product. Include key information about the API product that is not captured by other fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#description GoogleApigeeApiProduct#description}
        :param environments: Comma-separated list of environment names to which the API product is bound. Requests to environments that are not listed are rejected. By specifying one or more environments, you can bind the resources listed in the API product to a specific environment, preventing developers from accessing those resources through API proxies deployed in another environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#environments GoogleApigeeApiProduct#environments}
        :param graphql_operation_group: graphql_operation_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#graphql_operation_group GoogleApigeeApiProduct#graphql_operation_group}
        :param grpc_operation_group: grpc_operation_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#grpc_operation_group GoogleApigeeApiProduct#grpc_operation_group}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#id GoogleApigeeApiProduct#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param operation_group: operation_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_group GoogleApigeeApiProduct#operation_group}
        :param proxies: Comma-separated list of API proxy names to which this API product is bound. By specifying API proxies, you can associate resources in the API product with specific API proxies, preventing developers from accessing those resources through other API proxies. Apigee rejects requests to API proxies that are not listed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#proxies GoogleApigeeApiProduct#proxies}
        :param quota: Number of request messages permitted per app by this API product for the specified quotaInterval and quotaTimeUnit. For example, a quota of 50, for a quotaInterval of 12 and a quotaTimeUnit of hours means 50 requests are allowed every 12 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota GoogleApigeeApiProduct#quota}
        :param quota_counter_scope: Scope of the quota decides how the quota counter gets applied and evaluate for quota violation. If the Scope is set as PROXY, then all the operations defined for the APIproduct that are associated with the same proxy will share the same quota counter set at the APIproduct level, making it a global counter at a proxy level. If the Scope is set as OPERATION, then each operations get the counter set at the API product dedicated, making it a local counter. Note that, the QuotaCounterScope applies only when an operation does not have dedicated quota set for itself. Possible values: ["QUOTA_COUNTER_SCOPE_UNSPECIFIED", "PROXY", "OPERATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota_counter_scope GoogleApigeeApiProduct#quota_counter_scope}
        :param quota_interval: Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota_interval GoogleApigeeApiProduct#quota_interval}
        :param quota_time_unit: Time unit defined for the quotaInterval. Valid values include second, minute, hour, day, month or year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota_time_unit GoogleApigeeApiProduct#quota_time_unit}
        :param scopes: Comma-separated list of OAuth scopes that are validated at runtime. Apigee validates that the scopes in any access token presented match the scopes defined in the OAuth policy associated with the API product. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#scopes GoogleApigeeApiProduct#scopes}
        :param space: Optional. The resource ID of the parent Space. If not set, the parent resource will be the Organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#space GoogleApigeeApiProduct#space}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#timeouts GoogleApigeeApiProduct#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(graphql_operation_group, dict):
            graphql_operation_group = GoogleApigeeApiProductGraphqlOperationGroup(**graphql_operation_group)
        if isinstance(grpc_operation_group, dict):
            grpc_operation_group = GoogleApigeeApiProductGrpcOperationGroup(**grpc_operation_group)
        if isinstance(operation_group, dict):
            operation_group = GoogleApigeeApiProductOperationGroup(**operation_group)
        if isinstance(timeouts, dict):
            timeouts = GoogleApigeeApiProductTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2fe238bad8f79212011b4d6ccf5d59058f8633ef027389548fe335ea4549299)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument org_id", value=org_id, expected_type=type_hints["org_id"])
            check_type(argname="argument api_resources", value=api_resources, expected_type=type_hints["api_resources"])
            check_type(argname="argument approval_type", value=approval_type, expected_type=type_hints["approval_type"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environments", value=environments, expected_type=type_hints["environments"])
            check_type(argname="argument graphql_operation_group", value=graphql_operation_group, expected_type=type_hints["graphql_operation_group"])
            check_type(argname="argument grpc_operation_group", value=grpc_operation_group, expected_type=type_hints["grpc_operation_group"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument operation_group", value=operation_group, expected_type=type_hints["operation_group"])
            check_type(argname="argument proxies", value=proxies, expected_type=type_hints["proxies"])
            check_type(argname="argument quota", value=quota, expected_type=type_hints["quota"])
            check_type(argname="argument quota_counter_scope", value=quota_counter_scope, expected_type=type_hints["quota_counter_scope"])
            check_type(argname="argument quota_interval", value=quota_interval, expected_type=type_hints["quota_interval"])
            check_type(argname="argument quota_time_unit", value=quota_time_unit, expected_type=type_hints["quota_time_unit"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument space", value=space, expected_type=type_hints["space"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
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
        if api_resources is not None:
            self._values["api_resources"] = api_resources
        if approval_type is not None:
            self._values["approval_type"] = approval_type
        if attributes is not None:
            self._values["attributes"] = attributes
        if description is not None:
            self._values["description"] = description
        if environments is not None:
            self._values["environments"] = environments
        if graphql_operation_group is not None:
            self._values["graphql_operation_group"] = graphql_operation_group
        if grpc_operation_group is not None:
            self._values["grpc_operation_group"] = grpc_operation_group
        if id is not None:
            self._values["id"] = id
        if operation_group is not None:
            self._values["operation_group"] = operation_group
        if proxies is not None:
            self._values["proxies"] = proxies
        if quota is not None:
            self._values["quota"] = quota
        if quota_counter_scope is not None:
            self._values["quota_counter_scope"] = quota_counter_scope
        if quota_interval is not None:
            self._values["quota_interval"] = quota_interval
        if quota_time_unit is not None:
            self._values["quota_time_unit"] = quota_time_unit
        if scopes is not None:
            self._values["scopes"] = scopes
        if space is not None:
            self._values["space"] = space
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
    def display_name(self) -> builtins.str:
        '''Name displayed in the UI or developer portal to developers registering for API access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#display_name GoogleApigeeApiProduct#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Internal name of the API product.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#name GoogleApigeeApiProduct#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def org_id(self) -> builtins.str:
        '''The Apigee Organization associated with the Apigee API product, in the format 'organizations/{{org_name}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#org_id GoogleApigeeApiProduct#org_id}
        '''
        result = self._values.get("org_id")
        assert result is not None, "Required property 'org_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Comma-separated list of API resources to be bundled in the API product.

        By default, the resource paths are mapped from the proxy.pathsuffix variable.
        The proxy path suffix is defined as the URI fragment following the ProxyEndpoint base path. For example, if the apiResources element is defined to be /forecastrss and the base path defined for the API proxy is /weather, then only requests to /weather/forecastrss are permitted by the API product.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#api_resources GoogleApigeeApiProduct#api_resources}
        '''
        result = self._values.get("api_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def approval_type(self) -> typing.Optional[builtins.str]:
        '''Flag that specifies how API keys are approved to access the APIs defined by the API product.

        Valid values are 'auto' or 'manual'. Possible values: ["auto", "manual"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#approval_type GoogleApigeeApiProduct#approval_type}
        '''
        result = self._values.get("approval_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductAttributes]]]:
        '''attributes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#attributes GoogleApigeeApiProduct#attributes}
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductAttributes]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the API product. Include key information about the API product that is not captured by other fields.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#description GoogleApigeeApiProduct#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environments(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Comma-separated list of environment names to which the API product is bound.

        Requests to environments that are not listed are rejected.
        By specifying one or more environments, you can bind the resources listed in the API product to a specific environment, preventing developers from accessing those resources through API proxies deployed in another environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#environments GoogleApigeeApiProduct#environments}
        '''
        result = self._values.get("environments")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def graphql_operation_group(
        self,
    ) -> typing.Optional["GoogleApigeeApiProductGraphqlOperationGroup"]:
        '''graphql_operation_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#graphql_operation_group GoogleApigeeApiProduct#graphql_operation_group}
        '''
        result = self._values.get("graphql_operation_group")
        return typing.cast(typing.Optional["GoogleApigeeApiProductGraphqlOperationGroup"], result)

    @builtins.property
    def grpc_operation_group(
        self,
    ) -> typing.Optional["GoogleApigeeApiProductGrpcOperationGroup"]:
        '''grpc_operation_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#grpc_operation_group GoogleApigeeApiProduct#grpc_operation_group}
        '''
        result = self._values.get("grpc_operation_group")
        return typing.cast(typing.Optional["GoogleApigeeApiProductGrpcOperationGroup"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#id GoogleApigeeApiProduct#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operation_group(
        self,
    ) -> typing.Optional["GoogleApigeeApiProductOperationGroup"]:
        '''operation_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_group GoogleApigeeApiProduct#operation_group}
        '''
        result = self._values.get("operation_group")
        return typing.cast(typing.Optional["GoogleApigeeApiProductOperationGroup"], result)

    @builtins.property
    def proxies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Comma-separated list of API proxy names to which this API product is bound.

        By specifying API proxies, you can associate resources in the API product with specific API proxies, preventing developers from accessing those resources through other API proxies.
        Apigee rejects requests to API proxies that are not listed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#proxies GoogleApigeeApiProduct#proxies}
        '''
        result = self._values.get("proxies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def quota(self) -> typing.Optional[builtins.str]:
        '''Number of request messages permitted per app by this API product for the specified quotaInterval and quotaTimeUnit.

        For example, a quota of 50, for a quotaInterval of 12 and a quotaTimeUnit of hours means 50 requests are allowed every 12 hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota GoogleApigeeApiProduct#quota}
        '''
        result = self._values.get("quota")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quota_counter_scope(self) -> typing.Optional[builtins.str]:
        '''Scope of the quota decides how the quota counter gets applied and evaluate for quota violation.

        If the Scope is set as PROXY, then all the operations defined for the APIproduct that are associated with the same proxy will share the same quota counter set at the APIproduct level, making it a global counter at a proxy level. If the Scope is set as OPERATION, then each operations get the counter set at the API product dedicated, making it a local counter. Note that, the QuotaCounterScope applies only when an operation does not have dedicated quota set for itself. Possible values: ["QUOTA_COUNTER_SCOPE_UNSPECIFIED", "PROXY", "OPERATION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota_counter_scope GoogleApigeeApiProduct#quota_counter_scope}
        '''
        result = self._values.get("quota_counter_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quota_interval(self) -> typing.Optional[builtins.str]:
        '''Time interval over which the number of request messages is calculated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota_interval GoogleApigeeApiProduct#quota_interval}
        '''
        result = self._values.get("quota_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quota_time_unit(self) -> typing.Optional[builtins.str]:
        '''Time unit defined for the quotaInterval. Valid values include second, minute, hour, day, month or year.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota_time_unit GoogleApigeeApiProduct#quota_time_unit}
        '''
        result = self._values.get("quota_time_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Comma-separated list of OAuth scopes that are validated at runtime.

        Apigee validates that the scopes in any access token presented match the scopes defined in the OAuth policy associated with the API product.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#scopes GoogleApigeeApiProduct#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def space(self) -> typing.Optional[builtins.str]:
        '''Optional. The resource ID of the parent Space. If not set, the parent resource will be the Organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#space GoogleApigeeApiProduct#space}
        '''
        result = self._values.get("space")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleApigeeApiProductTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#timeouts GoogleApigeeApiProduct#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleApigeeApiProductTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGraphqlOperationGroup",
    jsii_struct_bases=[],
    name_mapping={
        "operation_configs": "operationConfigs",
        "operation_config_type": "operationConfigType",
    },
)
class GoogleApigeeApiProductGraphqlOperationGroup:
    def __init__(
        self,
        *,
        operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operation_config_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operation_configs: operation_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_configs GoogleApigeeApiProduct#operation_configs}
        :param operation_config_type: Flag that specifes whether the configuration is for Apigee API proxy or a remote service. Valid values include proxy or remoteservice. Defaults to proxy. Set to proxy when Apigee API proxies are associated with the API product. Set to remoteservice when non-Apigee proxies like Istio-Envoy are associated with the API product. Possible values: ["proxy", "remoteservice"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_config_type GoogleApigeeApiProduct#operation_config_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__facd936e205ac6ca654567899d9381d47de9cbef1f6434dd3ed055382b049069)
            check_type(argname="argument operation_configs", value=operation_configs, expected_type=type_hints["operation_configs"])
            check_type(argname="argument operation_config_type", value=operation_config_type, expected_type=type_hints["operation_config_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operation_configs is not None:
            self._values["operation_configs"] = operation_configs
        if operation_config_type is not None:
            self._values["operation_config_type"] = operation_config_type

    @builtins.property
    def operation_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs"]]]:
        '''operation_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_configs GoogleApigeeApiProduct#operation_configs}
        '''
        result = self._values.get("operation_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs"]]], result)

    @builtins.property
    def operation_config_type(self) -> typing.Optional[builtins.str]:
        '''Flag that specifes whether the configuration is for Apigee API proxy or a remote service.

        Valid values include proxy or remoteservice. Defaults to proxy. Set to proxy when Apigee API proxies are associated with the API product. Set to remoteservice when non-Apigee proxies like Istio-Envoy are associated with the API product. Possible values: ["proxy", "remoteservice"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_config_type GoogleApigeeApiProduct#operation_config_type}
        '''
        result = self._values.get("operation_config_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductGraphqlOperationGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "api_source": "apiSource",
        "attributes": "attributes",
        "operations": "operations",
        "quota": "quota",
    },
)
class GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs:
    def __init__(
        self,
        *,
        api_source: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        quota: typing.Optional[typing.Union["GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param api_source: Required. Name of the API proxy endpoint or remote service with which the GraphQL operation and quota are associated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#api_source GoogleApigeeApiProduct#api_source}
        :param attributes: attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#attributes GoogleApigeeApiProduct#attributes}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operations GoogleApigeeApiProduct#operations}
        :param quota: quota block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota GoogleApigeeApiProduct#quota}
        '''
        if isinstance(quota, dict):
            quota = GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota(**quota)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d392294de9959a6146c288ebd5a21d45b637bdb4a6e355502b4e12dc3788107c)
            check_type(argname="argument api_source", value=api_source, expected_type=type_hints["api_source"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument quota", value=quota, expected_type=type_hints["quota"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_source is not None:
            self._values["api_source"] = api_source
        if attributes is not None:
            self._values["attributes"] = attributes
        if operations is not None:
            self._values["operations"] = operations
        if quota is not None:
            self._values["quota"] = quota

    @builtins.property
    def api_source(self) -> typing.Optional[builtins.str]:
        '''Required. Name of the API proxy endpoint or remote service with which the GraphQL operation and quota are associated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#api_source GoogleApigeeApiProduct#api_source}
        '''
        result = self._values.get("api_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes"]]]:
        '''attributes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#attributes GoogleApigeeApiProduct#attributes}
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes"]]], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operations GoogleApigeeApiProduct#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations"]]], result)

    @builtins.property
    def quota(
        self,
    ) -> typing.Optional["GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota"]:
        '''quota block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota GoogleApigeeApiProduct#quota}
        '''
        result = self._values.get("quota")
        return typing.cast(typing.Optional["GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Key of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#name GoogleApigeeApiProduct#name}
        :param value: Value of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#value GoogleApigeeApiProduct#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a67a50d837580ecc9b5582c9c97ab724a528a55ed44a3db5d0a1d9e6be9bb96)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Key of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#name GoogleApigeeApiProduct#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#value GoogleApigeeApiProduct#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bf9915ea4783070e5764ca479b92cb935ef3b21a3f3e30804676afc2f337d01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6b8fe31c8ea3ba902bcb1b5943364018b29b94682791fbf119776c289cd75e8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35935a50dd2f9ee78a064c1fbf4c171032a8ba0c24a94937b3b20550df6b159)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c375fa0b978d56a03ee6dd7ba72afdcb2c0aa03088066a183329b9f1f60ed8a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a705c7f21c9c9c950bfd7e0ea520ffc0404182038997c96282a2aa9c9e6a90ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0829670015ca4b8b826e9c91fc6c9d36b00e770a86b5857e9ec8697ccec25f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b78b130339a9066db0d7ebb43151b2d30130ad62651302bc6b755e09635fac4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c2615aa9087d7817166fe93cf956d5f5ccd44a875e4619c5f98622537d38c3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d239b3fa1417fee916ac421dbe08107f4b320c85200e89b72b0d6124912386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec7499becca61b70ccb266552a84695ca016b59b8eeb45c7b115f55fac5265d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18fca154422b7f308577ff595c1920635eed59ecc22b7ef87e075fedc9d50896)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ca76a96fff2d7723782deb849797c2872fd996a87b08e73f8428c3085a986c4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb234c7f5321600c26579b8a4802b09fbd452e65a9c6998c75e5a371ec6e198)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6af4d2885c1132cec80c8274d0abe365666c72b9e1bb416052521f454445c12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d89c17305012b2c71fe5dd5e419b21b1eec1359d560b7b9af57cc52a91a71366)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75ae4e2acc76066c4337b108cd2b72c5bdf590521d1baa1e7ca7caeb21f675c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations",
    jsii_struct_bases=[],
    name_mapping={"operation": "operation", "operation_types": "operationTypes"},
)
class GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations:
    def __init__(
        self,
        *,
        operation: typing.Optional[builtins.str] = None,
        operation_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operation: GraphQL operation name. The name and operation type will be used to apply quotas. If no name is specified, the quota will be applied to all GraphQL operations irrespective of their operation names in the payload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation GoogleApigeeApiProduct#operation}
        :param operation_types: Required. GraphQL operation types. Valid values include query or mutation. Note: Apigee does not currently support subscription types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_types GoogleApigeeApiProduct#operation_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b884935aa4274f0b0c5ac63c552855b24852912dfcd4a37e9f48298dd5d379)
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
            check_type(argname="argument operation_types", value=operation_types, expected_type=type_hints["operation_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operation is not None:
            self._values["operation"] = operation
        if operation_types is not None:
            self._values["operation_types"] = operation_types

    @builtins.property
    def operation(self) -> typing.Optional[builtins.str]:
        '''GraphQL operation name.

        The name and operation type will be used to apply quotas. If no name is specified, the quota will be applied to all GraphQL operations irrespective of their operation names in the payload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation GoogleApigeeApiProduct#operation}
        '''
        result = self._values.get("operation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operation_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Required. GraphQL operation types. Valid values include query or mutation. Note: Apigee does not currently support subscription types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_types GoogleApigeeApiProduct#operation_types}
        '''
        result = self._values.get("operation_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0b1a7ff5cc469e4fd3a7b5feb67f0e9447fbd405a27e212cabca25c9734a458)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0137c2945d963690aa5cba53b1c664aab786b192daea9901160123f62cc62ac4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9253c65455581aeeaff86a00a385ae1cd8480d719246b94a26099fc3ddfa6937)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e916a507ae2d2308d8eebe4ecc294ba1571e5d653795c1036af934c86d6afba0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0d0e375b152d089660d63c5696339b30ba4b5092ef880cd80617c55e660ba46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e785bdce038fabdcf5ff2c1d8ace863279fdb2e90ed3a975dfc211a6a3fce588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4381f29e9ad20144cd7546a20b63ec957f2dad5d32147e00b7c1279d01e088ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOperation")
    def reset_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperation", []))

    @jsii.member(jsii_name="resetOperationTypes")
    def reset_operation_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationTypes", []))

    @builtins.property
    @jsii.member(jsii_name="operationInput")
    def operation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationInput"))

    @builtins.property
    @jsii.member(jsii_name="operationTypesInput")
    def operation_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "operationTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operation"))

    @operation.setter
    def operation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__683c93021062825525f7868ff9d640706b5024ea93fc253b345a19248d9e9a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operationTypes")
    def operation_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "operationTypes"))

    @operation_types.setter
    def operation_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c54e2ffea0b9772f482f60cfb474d17a500170bea2246757f7af2e0f7f53d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4683a24798af1f521f2dcc6cb0561f31b301d0ef3f345136507d5b463007b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__931ab05734b7e17f80acb5c2816162cece98bbc0354e621d50865ac37fdc6e53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAttributes")
    def put_attributes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51e3eb33251d705f591de3642c09b07c0f95abf089d1a6a4709ab1bad016fc09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAttributes", [value]))

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc95bdab1e7b70fecd0de08e744f37c803cfd7f0be78ad9d3cf34e1e06dd466)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperations", [value]))

    @jsii.member(jsii_name="putQuota")
    def put_quota(
        self,
        *,
        interval: typing.Optional[builtins.str] = None,
        limit: typing.Optional[builtins.str] = None,
        time_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interval: Required. Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#interval GoogleApigeeApiProduct#interval}
        :param limit: Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#limit GoogleApigeeApiProduct#limit}
        :param time_unit: Time unit defined for the interval. Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#time_unit GoogleApigeeApiProduct#time_unit}
        '''
        value = GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota(
            interval=interval, limit=limit, time_unit=time_unit
        )

        return typing.cast(None, jsii.invoke(self, "putQuota", [value]))

    @jsii.member(jsii_name="resetApiSource")
    def reset_api_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiSource", []))

    @jsii.member(jsii_name="resetAttributes")
    def reset_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributes", []))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @jsii.member(jsii_name="resetQuota")
    def reset_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuota", []))

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesList:
        return typing.cast(GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesList, jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(
        self,
    ) -> GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsList:
        return typing.cast(GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="quota")
    def quota(
        self,
    ) -> "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuotaOutputReference":
        return typing.cast("GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuotaOutputReference", jsii.get(self, "quota"))

    @builtins.property
    @jsii.member(jsii_name="apiSourceInput")
    def api_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]]], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaInput")
    def quota_input(
        self,
    ) -> typing.Optional["GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota"]:
        return typing.cast(typing.Optional["GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota"], jsii.get(self, "quotaInput"))

    @builtins.property
    @jsii.member(jsii_name="apiSource")
    def api_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiSource"))

    @api_source.setter
    def api_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b892a3dc3c187f839fea215bcbefcb3652d6cc3a64537160db73cd9dee235bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3dfa5ef550f1057c9978f3f617e7fcfcd5a33690239af73390a0012459aa6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "limit": "limit", "time_unit": "timeUnit"},
)
class GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota:
    def __init__(
        self,
        *,
        interval: typing.Optional[builtins.str] = None,
        limit: typing.Optional[builtins.str] = None,
        time_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interval: Required. Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#interval GoogleApigeeApiProduct#interval}
        :param limit: Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#limit GoogleApigeeApiProduct#limit}
        :param time_unit: Time unit defined for the interval. Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#time_unit GoogleApigeeApiProduct#time_unit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796bb2d846ef922e179a147065886cf48369bdf83f74b08a9af6cb6ee07f4b0e)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument time_unit", value=time_unit, expected_type=type_hints["time_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if interval is not None:
            self._values["interval"] = interval
        if limit is not None:
            self._values["limit"] = limit
        if time_unit is not None:
            self._values["time_unit"] = time_unit

    @builtins.property
    def interval(self) -> typing.Optional[builtins.str]:
        '''Required. Time interval over which the number of request messages is calculated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#interval GoogleApigeeApiProduct#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit(self) -> typing.Optional[builtins.str]:
        '''Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#limit GoogleApigeeApiProduct#limit}
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_unit(self) -> typing.Optional[builtins.str]:
        '''Time unit defined for the interval.

        Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#time_unit GoogleApigeeApiProduct#time_unit}
        '''
        result = self._values.get("time_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuotaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuotaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b85692d0e7ad5458932c904cb42dcd36b6d6bf23aea1ca77d14522202f3b8590)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetLimit")
    def reset_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimit", []))

    @jsii.member(jsii_name="resetTimeUnit")
    def reset_time_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeUnit", []))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="timeUnitInput")
    def time_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e112509e6546379dc0587869410bc2c85444d79144efe23f2e13de42e4062586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a990a7fcb1784fe09511b5de39bf41149800c2effc37c7b8f57d7dc03ef5f5f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeUnit")
    def time_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeUnit"))

    @time_unit.setter
    def time_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf98e935ffbba8c85f49a61373ed2a8bbe7cfb171c054d93a44171fa9e9f6804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota]:
        return typing.cast(typing.Optional[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df3985b4ff95ea0a141982c28547bc249362f25b23a579eb209ea4c4de8a380)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeApiProductGraphqlOperationGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGraphqlOperationGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a6e0ed84649194a62c621bae30e52e6226f6b72a2dc147a4fc9cda5fa0a73c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperationConfigs")
    def put_operation_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e60d245e99dfc43de94c86309d43f1f52db922ee17a8bc23d1352896934f936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperationConfigs", [value]))

    @jsii.member(jsii_name="resetOperationConfigs")
    def reset_operation_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationConfigs", []))

    @jsii.member(jsii_name="resetOperationConfigType")
    def reset_operation_config_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationConfigType", []))

    @builtins.property
    @jsii.member(jsii_name="operationConfigs")
    def operation_configs(
        self,
    ) -> GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsList:
        return typing.cast(GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsList, jsii.get(self, "operationConfigs"))

    @builtins.property
    @jsii.member(jsii_name="operationConfigsInput")
    def operation_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs]]], jsii.get(self, "operationConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="operationConfigTypeInput")
    def operation_config_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationConfigTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="operationConfigType")
    def operation_config_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationConfigType"))

    @operation_config_type.setter
    def operation_config_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66506e86e7e8a4ced93eea7da9fa4491a2c774e2b6d2ba784304a3db784c30ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationConfigType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeApiProductGraphqlOperationGroup]:
        return typing.cast(typing.Optional[GoogleApigeeApiProductGraphqlOperationGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeApiProductGraphqlOperationGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b4abaee9caf9cbe66e8eba33f8327318ceb3d3e9771298dade3e42a35073d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGrpcOperationGroup",
    jsii_struct_bases=[],
    name_mapping={"operation_configs": "operationConfigs"},
)
class GoogleApigeeApiProductGrpcOperationGroup:
    def __init__(
        self,
        *,
        operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeApiProductGrpcOperationGroupOperationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param operation_configs: operation_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_configs GoogleApigeeApiProduct#operation_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81cb8713b7c8a5f78d0be231f57a96a0ead13d502326c68fb8e2ffd1cfacc76e)
            check_type(argname="argument operation_configs", value=operation_configs, expected_type=type_hints["operation_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operation_configs is not None:
            self._values["operation_configs"] = operation_configs

    @builtins.property
    def operation_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductGrpcOperationGroupOperationConfigs"]]]:
        '''operation_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_configs GoogleApigeeApiProduct#operation_configs}
        '''
        result = self._values.get("operation_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductGrpcOperationGroupOperationConfigs"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductGrpcOperationGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGrpcOperationGroupOperationConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "api_source": "apiSource",
        "attributes": "attributes",
        "methods": "methods",
        "quota": "quota",
        "service": "service",
    },
)
class GoogleApigeeApiProductGrpcOperationGroupOperationConfigs:
    def __init__(
        self,
        *,
        api_source: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        quota: typing.Optional[typing.Union["GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota", typing.Dict[builtins.str, typing.Any]]] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_source: Required. Name of the API proxy with which the gRPC operation and quota are associated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#api_source GoogleApigeeApiProduct#api_source}
        :param attributes: attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#attributes GoogleApigeeApiProduct#attributes}
        :param methods: List of unqualified gRPC method names for the proxy to which quota will be applied. If this field is empty, the Quota will apply to all operations on the gRPC service defined on the proxy. Example: Given a proxy that is configured to serve com.petstore.PetService, the methods com.petstore.PetService.ListPets and com.petstore.PetService.GetPet would be specified here as simply ["ListPets", "GetPet"]. Note: Currently, you can specify only a single GraphQLOperation. Specifying more than one will cause the operation to fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#methods GoogleApigeeApiProduct#methods}
        :param quota: quota block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota GoogleApigeeApiProduct#quota}
        :param service: Required. gRPC Service name associated to be associated with the API proxy, on which quota rules can be applied upon. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#service GoogleApigeeApiProduct#service}
        '''
        if isinstance(quota, dict):
            quota = GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota(**quota)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e692c41cd188a4315b626fc74e61a879c35a11a4f7c90db98f64386a1c130514)
            check_type(argname="argument api_source", value=api_source, expected_type=type_hints["api_source"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument methods", value=methods, expected_type=type_hints["methods"])
            check_type(argname="argument quota", value=quota, expected_type=type_hints["quota"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_source is not None:
            self._values["api_source"] = api_source
        if attributes is not None:
            self._values["attributes"] = attributes
        if methods is not None:
            self._values["methods"] = methods
        if quota is not None:
            self._values["quota"] = quota
        if service is not None:
            self._values["service"] = service

    @builtins.property
    def api_source(self) -> typing.Optional[builtins.str]:
        '''Required. Name of the API proxy with which the gRPC operation and quota are associated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#api_source GoogleApigeeApiProduct#api_source}
        '''
        result = self._values.get("api_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes"]]]:
        '''attributes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#attributes GoogleApigeeApiProduct#attributes}
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes"]]], result)

    @builtins.property
    def methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of unqualified gRPC method names for the proxy to which quota will be applied.

        If this field is empty, the Quota will apply to all operations on the gRPC service defined on the proxy.

        Example: Given a proxy that is configured to serve com.petstore.PetService, the methods com.petstore.PetService.ListPets and com.petstore.PetService.GetPet would be specified here as simply ["ListPets", "GetPet"].

        Note: Currently, you can specify only a single GraphQLOperation. Specifying more than one will cause the operation to fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#methods GoogleApigeeApiProduct#methods}
        '''
        result = self._values.get("methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def quota(
        self,
    ) -> typing.Optional["GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota"]:
        '''quota block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota GoogleApigeeApiProduct#quota}
        '''
        result = self._values.get("quota")
        return typing.cast(typing.Optional["GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota"], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Required.

        gRPC Service name associated to be associated with the API proxy, on which quota rules can be applied upon.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#service GoogleApigeeApiProduct#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductGrpcOperationGroupOperationConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Key of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#name GoogleApigeeApiProduct#name}
        :param value: Value of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#value GoogleApigeeApiProduct#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e0a84ce479265e1dd8695028a001e855434c17cee3b7d794ac2efde8f6da0a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Key of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#name GoogleApigeeApiProduct#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#value GoogleApigeeApiProduct#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89e109872b36820fdd1dd3fe5bf2114d16b34bcf2714892cfb9fa6ae3019159c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4472e14062911d32d52e23e2a693e3ee3a265198c9318f081d33916075811b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22bbb49ec8095fadf2910775b267e29fc61870ca6f1fe7ff255df655e5b7b5d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62459ffc38cd265784c783218a4e17d6252823a049714e91a853fbd6a169bb5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8079fb86623f88db0b83912b4aa4fe882a0a05ee47abc647329706ecadb8247e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9374e951e9d05e5506682ebecb45fed7d6b83e65c86f4d51010482004ed930c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57e57448d3ecceeb5b371ba9d7f1fab6c1f867daf04bb2151a8f802b6e5dd8cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__670eecb10a80dc8caf5b0aaf8f785bfca3fa64b305abf1803bfd09ad4067a539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c9b29166235334843950c4521e0f68d8fa32d6015e2eed56102b0eb7a92439)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0006e1b163f820ee21991cb0beadd783678bc4134d663759b016f4c705eb43f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeApiProductGrpcOperationGroupOperationConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGrpcOperationGroupOperationConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5264048c7f6c4f205d624bf8f660d7f01bd3c03fdd2f6cfc3a9665db1298804)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApigeeApiProductGrpcOperationGroupOperationConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b6d8d53f734dd475bbbe059f3c8be2ada98b8be339c8b126300c47cbe1235a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApigeeApiProductGrpcOperationGroupOperationConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ef7930b29d87f9cc245c68412afaf8cb574daa3c4d42ce15b08d493291f244)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2123accdcaf188654bc2bda050575ee87c45c8b90ac0751247dfe3c170d191ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__509e9f1692dda76c7fbbb13c27c07649dcec8a6b2c4f9ee4625752a457382608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGrpcOperationGroupOperationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGrpcOperationGroupOperationConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGrpcOperationGroupOperationConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__689bf1db81520114497b4823ff65707deb229ccba976a51398af4148eecb1df7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeApiProductGrpcOperationGroupOperationConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGrpcOperationGroupOperationConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36a7c09c17f7f03156f9ab3fcc2457e0b997c07585e58f8f1ba3dac81df735d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAttributes")
    def put_attributes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d513929c04a59b590948dac8c0232199344621376e734ef2db8b0f47f140dc68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAttributes", [value]))

    @jsii.member(jsii_name="putQuota")
    def put_quota(
        self,
        *,
        interval: typing.Optional[builtins.str] = None,
        limit: typing.Optional[builtins.str] = None,
        time_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interval: Required. Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#interval GoogleApigeeApiProduct#interval}
        :param limit: Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#limit GoogleApigeeApiProduct#limit}
        :param time_unit: Time unit defined for the interval. Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#time_unit GoogleApigeeApiProduct#time_unit}
        '''
        value = GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota(
            interval=interval, limit=limit, time_unit=time_unit
        )

        return typing.cast(None, jsii.invoke(self, "putQuota", [value]))

    @jsii.member(jsii_name="resetApiSource")
    def reset_api_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiSource", []))

    @jsii.member(jsii_name="resetAttributes")
    def reset_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributes", []))

    @jsii.member(jsii_name="resetMethods")
    def reset_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethods", []))

    @jsii.member(jsii_name="resetQuota")
    def reset_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuota", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributesList:
        return typing.cast(GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributesList, jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="quota")
    def quota(
        self,
    ) -> "GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuotaOutputReference":
        return typing.cast("GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuotaOutputReference", jsii.get(self, "quota"))

    @builtins.property
    @jsii.member(jsii_name="apiSourceInput")
    def api_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]]], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="methodsInput")
    def methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "methodsInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaInput")
    def quota_input(
        self,
    ) -> typing.Optional["GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota"]:
        return typing.cast(typing.Optional["GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota"], jsii.get(self, "quotaInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="apiSource")
    def api_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiSource"))

    @api_source.setter
    def api_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d09c3c06f7d3ad33c3927781eb9562b326751a25c5536aa0f4f07dcd7fe804b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="methods")
    def methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "methods"))

    @methods.setter
    def methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ea3f913ad2f23eb3ccb66f89e357c592fc74841075df9d725f93658c086c21d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55b7fc3cc14b85a3bc42c48b2a14d7c653c32a92225d281f89cf9d74de47688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGrpcOperationGroupOperationConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGrpcOperationGroupOperationConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGrpcOperationGroupOperationConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__143dafb423f9ef77e4a1841253eb3d02c0fe2724e1293ce24a73ba445c0cfbb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "limit": "limit", "time_unit": "timeUnit"},
)
class GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota:
    def __init__(
        self,
        *,
        interval: typing.Optional[builtins.str] = None,
        limit: typing.Optional[builtins.str] = None,
        time_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interval: Required. Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#interval GoogleApigeeApiProduct#interval}
        :param limit: Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#limit GoogleApigeeApiProduct#limit}
        :param time_unit: Time unit defined for the interval. Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#time_unit GoogleApigeeApiProduct#time_unit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b6980e74e721c848b9e81c243a53f4f5c11d70799e4c8cdcf0699af2bb2b25)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument time_unit", value=time_unit, expected_type=type_hints["time_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if interval is not None:
            self._values["interval"] = interval
        if limit is not None:
            self._values["limit"] = limit
        if time_unit is not None:
            self._values["time_unit"] = time_unit

    @builtins.property
    def interval(self) -> typing.Optional[builtins.str]:
        '''Required. Time interval over which the number of request messages is calculated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#interval GoogleApigeeApiProduct#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit(self) -> typing.Optional[builtins.str]:
        '''Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#limit GoogleApigeeApiProduct#limit}
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_unit(self) -> typing.Optional[builtins.str]:
        '''Time unit defined for the interval.

        Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#time_unit GoogleApigeeApiProduct#time_unit}
        '''
        result = self._values.get("time_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuotaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuotaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78812791e4975c43ec45c9c3afbf9d37a95b6fa54d06dd59a3beb9a1dc7fde81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetLimit")
    def reset_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimit", []))

    @jsii.member(jsii_name="resetTimeUnit")
    def reset_time_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeUnit", []))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="timeUnitInput")
    def time_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721b9f6f11b7522d559847dc6097dc536684bc71ad0d4af5646351a543837af2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ce656a3f84f2c9053e5525e6ede7aa0e43987a4a1f399e8ad614bf7f08ce15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeUnit")
    def time_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeUnit"))

    @time_unit.setter
    def time_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c06b087afa8a03b882727935418b87b4383705356049bcef5dc80fb487dba00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota]:
        return typing.cast(typing.Optional[GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccfbd666000d562aa7e25388e7d6d42cb0bb055becd5339d638df98fe2e5c3ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeApiProductGrpcOperationGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductGrpcOperationGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3bcc2e37f8f6edceb8608c7602a74fbeef55a5cf8db778f6ec98cc2dfc31ade)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperationConfigs")
    def put_operation_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductGrpcOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b5d2ac8259fe848324be33a67e99dd734f5bbb02e175dfb1b7a437dbcaad09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperationConfigs", [value]))

    @jsii.member(jsii_name="resetOperationConfigs")
    def reset_operation_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationConfigs", []))

    @builtins.property
    @jsii.member(jsii_name="operationConfigs")
    def operation_configs(
        self,
    ) -> GoogleApigeeApiProductGrpcOperationGroupOperationConfigsList:
        return typing.cast(GoogleApigeeApiProductGrpcOperationGroupOperationConfigsList, jsii.get(self, "operationConfigs"))

    @builtins.property
    @jsii.member(jsii_name="operationConfigsInput")
    def operation_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGrpcOperationGroupOperationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGrpcOperationGroupOperationConfigs]]], jsii.get(self, "operationConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeApiProductGrpcOperationGroup]:
        return typing.cast(typing.Optional[GoogleApigeeApiProductGrpcOperationGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeApiProductGrpcOperationGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48fd6db39ef2771d7badf2d7697aa5d7e80c55a06b7401c93fc612755ad31f53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductOperationGroup",
    jsii_struct_bases=[],
    name_mapping={
        "operation_configs": "operationConfigs",
        "operation_config_type": "operationConfigType",
    },
)
class GoogleApigeeApiProductOperationGroup:
    def __init__(
        self,
        *,
        operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeApiProductOperationGroupOperationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operation_config_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operation_configs: operation_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_configs GoogleApigeeApiProduct#operation_configs}
        :param operation_config_type: Flag that specifes whether the configuration is for Apigee API proxy or a remote service. Valid values include proxy or remoteservice. Defaults to proxy. Set to proxy when Apigee API proxies are associated with the API product. Set to remoteservice when non-Apigee proxies like Istio-Envoy are associated with the API product. Possible values: ["proxy", "remoteservice"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_config_type GoogleApigeeApiProduct#operation_config_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de0cb1db0c453431ba2c99fc61dd9786f24e72baff8b739fc88c374f4c6a6c5)
            check_type(argname="argument operation_configs", value=operation_configs, expected_type=type_hints["operation_configs"])
            check_type(argname="argument operation_config_type", value=operation_config_type, expected_type=type_hints["operation_config_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operation_configs is not None:
            self._values["operation_configs"] = operation_configs
        if operation_config_type is not None:
            self._values["operation_config_type"] = operation_config_type

    @builtins.property
    def operation_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductOperationGroupOperationConfigs"]]]:
        '''operation_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_configs GoogleApigeeApiProduct#operation_configs}
        '''
        result = self._values.get("operation_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductOperationGroupOperationConfigs"]]], result)

    @builtins.property
    def operation_config_type(self) -> typing.Optional[builtins.str]:
        '''Flag that specifes whether the configuration is for Apigee API proxy or a remote service.

        Valid values include proxy or remoteservice. Defaults to proxy. Set to proxy when Apigee API proxies are associated with the API product. Set to remoteservice when non-Apigee proxies like Istio-Envoy are associated with the API product. Possible values: ["proxy", "remoteservice"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operation_config_type GoogleApigeeApiProduct#operation_config_type}
        '''
        result = self._values.get("operation_config_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductOperationGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductOperationGroupOperationConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "api_source": "apiSource",
        "attributes": "attributes",
        "operations": "operations",
        "quota": "quota",
    },
)
class GoogleApigeeApiProductOperationGroupOperationConfigs:
    def __init__(
        self,
        *,
        api_source: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeApiProductOperationGroupOperationConfigsAttributes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeApiProductOperationGroupOperationConfigsOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        quota: typing.Optional[typing.Union["GoogleApigeeApiProductOperationGroupOperationConfigsQuota", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param api_source: Required. Name of the API proxy or remote service with which the resources, methods, and quota are associated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#api_source GoogleApigeeApiProduct#api_source}
        :param attributes: attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#attributes GoogleApigeeApiProduct#attributes}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operations GoogleApigeeApiProduct#operations}
        :param quota: quota block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota GoogleApigeeApiProduct#quota}
        '''
        if isinstance(quota, dict):
            quota = GoogleApigeeApiProductOperationGroupOperationConfigsQuota(**quota)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cda39321c7977b50b65dd2d9f4f1bfbe2205740519d43055439a669e759fc11)
            check_type(argname="argument api_source", value=api_source, expected_type=type_hints["api_source"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument quota", value=quota, expected_type=type_hints["quota"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_source is not None:
            self._values["api_source"] = api_source
        if attributes is not None:
            self._values["attributes"] = attributes
        if operations is not None:
            self._values["operations"] = operations
        if quota is not None:
            self._values["quota"] = quota

    @builtins.property
    def api_source(self) -> typing.Optional[builtins.str]:
        '''Required. Name of the API proxy or remote service with which the resources, methods, and quota are associated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#api_source GoogleApigeeApiProduct#api_source}
        '''
        result = self._values.get("api_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductOperationGroupOperationConfigsAttributes"]]]:
        '''attributes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#attributes GoogleApigeeApiProduct#attributes}
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductOperationGroupOperationConfigsAttributes"]]], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductOperationGroupOperationConfigsOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#operations GoogleApigeeApiProduct#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeApiProductOperationGroupOperationConfigsOperations"]]], result)

    @builtins.property
    def quota(
        self,
    ) -> typing.Optional["GoogleApigeeApiProductOperationGroupOperationConfigsQuota"]:
        '''quota block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#quota GoogleApigeeApiProduct#quota}
        '''
        result = self._values.get("quota")
        return typing.cast(typing.Optional["GoogleApigeeApiProductOperationGroupOperationConfigsQuota"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductOperationGroupOperationConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductOperationGroupOperationConfigsAttributes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleApigeeApiProductOperationGroupOperationConfigsAttributes:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Key of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#name GoogleApigeeApiProduct#name}
        :param value: Value of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#value GoogleApigeeApiProduct#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603fd5dfb91ffbef1ea19f9f58a79f5a794da73147648eeaad115cc6bdf6a34c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Key of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#name GoogleApigeeApiProduct#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#value GoogleApigeeApiProduct#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductOperationGroupOperationConfigsAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeApiProductOperationGroupOperationConfigsAttributesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductOperationGroupOperationConfigsAttributesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4918ad440eb5bfdc3d3921736bdd2a86fb3d2eb474839d48c51baf323c6da88b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApigeeApiProductOperationGroupOperationConfigsAttributesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3102dc9e93b0a9e8479d468052f3bfb348e6f365b2381cc627ff2d4ebcfd2266)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApigeeApiProductOperationGroupOperationConfigsAttributesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__879ac236ecf5f9576855dc6eee36a6dc9089bcc24cafb5a6317f8de47ca5b57f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73e133cb6d49cdd9e8db9c59c499e7caf7dce01ac064cde2033c09e44202a358)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5958ab6f5ccc8c6a4bf56aa6b33f986734fab836677c3fca156fde057ede3a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigsAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigsAttributes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigsAttributes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae6e08b518d00c37cc8150556fde6d49d69d41c789290bee590cba985851e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeApiProductOperationGroupOperationConfigsAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductOperationGroupOperationConfigsAttributesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5159732ab9e27bd49211ac841bd4cc5360e2623bdc4cdc84086226b6b4fc04f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6fba974e1cf6d9c5fb731a76ff04a85c3e1a94e25449031961c3806f46db893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__276eb26bb42106753cf1a621736b8b750874da8838548be7b0dccc067dc5afb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductOperationGroupOperationConfigsAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductOperationGroupOperationConfigsAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductOperationGroupOperationConfigsAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3900ebec2a1e13c226f056483cc6734b4a40bed3cf1559a581720ff56983ae84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeApiProductOperationGroupOperationConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductOperationGroupOperationConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec1fd025e040a95f35f4722c5025908434ad246479bba3377110af7c79883159)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApigeeApiProductOperationGroupOperationConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f614756148fb519b1648a6d0c1a29f38df88bdb3a052c7c0f96e6a0186f20a3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApigeeApiProductOperationGroupOperationConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84873bd41b029f7930c1d44a56c580d1171946cb0fb2d229000e72229565106a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e0c59f4633080ae05666412e18ffa818b8b9aeaee75d964e62b90bcb1c3ba15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f32735597ac56373d6440faff14403f0e3560813176474542260ddbcd0f1e98a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9829f6556a130aae1875d27893f9195c9d67a8f49f87dcd62f2a05c30f68bdb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductOperationGroupOperationConfigsOperations",
    jsii_struct_bases=[],
    name_mapping={"methods": "methods", "resource": "resource"},
)
class GoogleApigeeApiProductOperationGroupOperationConfigsOperations:
    def __init__(
        self,
        *,
        methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param methods: Methods refers to the REST verbs, when none specified, all verb types are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#methods GoogleApigeeApiProduct#methods}
        :param resource: Required. REST resource path associated with the API proxy or remote service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#resource GoogleApigeeApiProduct#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb9bc7ac2528419272341aa16eab08e2ee1ce859499244f27d622e8b42d1cf0)
            check_type(argname="argument methods", value=methods, expected_type=type_hints["methods"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if methods is not None:
            self._values["methods"] = methods
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Methods refers to the REST verbs, when none specified, all verb types are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#methods GoogleApigeeApiProduct#methods}
        '''
        result = self._values.get("methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''Required. REST resource path associated with the API proxy or remote service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#resource GoogleApigeeApiProduct#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductOperationGroupOperationConfigsOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeApiProductOperationGroupOperationConfigsOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductOperationGroupOperationConfigsOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f57bb4dce96fb3eee4830fae5533728dc5405195af817300c7f29ee6b2504473)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApigeeApiProductOperationGroupOperationConfigsOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa704971f29cbf5676420407b8f907492e8aa968a8417345c7c3c324b0fec4a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApigeeApiProductOperationGroupOperationConfigsOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ba71b960ca8d6280d61604327b7848dace8cf3cd575b168888d7add54d2e3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d95f53a8fefa267b153b3fe22300eabbd0241610d900578ee7f9dd8420bedaee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6147d9887f17664af25d1affb53e17c35b9b4a7edefc68237ed80005b3cbe51f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigsOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigsOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigsOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__453e310ec73a37feea9aacf0760a05865e289d7e8cdabce2c93cc4846ebc9a6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeApiProductOperationGroupOperationConfigsOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductOperationGroupOperationConfigsOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a90e6bb0755fa7ae81d7b45b70256cca82c2dcbfca2efed9dd09e37be1c44ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMethods")
    def reset_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethods", []))

    @jsii.member(jsii_name="resetResource")
    def reset_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResource", []))

    @builtins.property
    @jsii.member(jsii_name="methodsInput")
    def methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "methodsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="methods")
    def methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "methods"))

    @methods.setter
    def methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed365088a181a493923786dc7651c13a4d3a7a5d6c6709fc784eb18f7c7a9794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3b0783cb35a670c36a063e1e2d5725a59470d03763de68750db795fca1b35e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductOperationGroupOperationConfigsOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductOperationGroupOperationConfigsOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductOperationGroupOperationConfigsOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f13e366530941adc3be2efbb8b4934e5411a579759a7360835d6644265b7e396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeApiProductOperationGroupOperationConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductOperationGroupOperationConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b87d82aa57beae463bf0446120ebc3b07bd7f62f05740bac3b37ece3e41868d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAttributes")
    def put_attributes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83482e4aef2eeaf591fc69d0be4466e28c265fa42ee36d940784b5b5d2836ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAttributes", [value]))

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductOperationGroupOperationConfigsOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf15cca150b26cfded3aa1ce75ba6e4df165be6765d4312a19f9fed96ceb652f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperations", [value]))

    @jsii.member(jsii_name="putQuota")
    def put_quota(
        self,
        *,
        interval: typing.Optional[builtins.str] = None,
        limit: typing.Optional[builtins.str] = None,
        time_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interval: Required. Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#interval GoogleApigeeApiProduct#interval}
        :param limit: Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#limit GoogleApigeeApiProduct#limit}
        :param time_unit: Time unit defined for the interval. Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#time_unit GoogleApigeeApiProduct#time_unit}
        '''
        value = GoogleApigeeApiProductOperationGroupOperationConfigsQuota(
            interval=interval, limit=limit, time_unit=time_unit
        )

        return typing.cast(None, jsii.invoke(self, "putQuota", [value]))

    @jsii.member(jsii_name="resetApiSource")
    def reset_api_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiSource", []))

    @jsii.member(jsii_name="resetAttributes")
    def reset_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributes", []))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @jsii.member(jsii_name="resetQuota")
    def reset_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuota", []))

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> GoogleApigeeApiProductOperationGroupOperationConfigsAttributesList:
        return typing.cast(GoogleApigeeApiProductOperationGroupOperationConfigsAttributesList, jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(
        self,
    ) -> GoogleApigeeApiProductOperationGroupOperationConfigsOperationsList:
        return typing.cast(GoogleApigeeApiProductOperationGroupOperationConfigsOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="quota")
    def quota(
        self,
    ) -> "GoogleApigeeApiProductOperationGroupOperationConfigsQuotaOutputReference":
        return typing.cast("GoogleApigeeApiProductOperationGroupOperationConfigsQuotaOutputReference", jsii.get(self, "quota"))

    @builtins.property
    @jsii.member(jsii_name="apiSourceInput")
    def api_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigsAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigsAttributes]]], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigsOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigsOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaInput")
    def quota_input(
        self,
    ) -> typing.Optional["GoogleApigeeApiProductOperationGroupOperationConfigsQuota"]:
        return typing.cast(typing.Optional["GoogleApigeeApiProductOperationGroupOperationConfigsQuota"], jsii.get(self, "quotaInput"))

    @builtins.property
    @jsii.member(jsii_name="apiSource")
    def api_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiSource"))

    @api_source.setter
    def api_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a49f7d1b2f52352164c0ac073ff63d6f82bf662f757bada6a5b7564108b70d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductOperationGroupOperationConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductOperationGroupOperationConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductOperationGroupOperationConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59d898d098b7bc8d50a5578f2bd96511d1b7fc88bd827b18ec8948af0f14a888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductOperationGroupOperationConfigsQuota",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "limit": "limit", "time_unit": "timeUnit"},
)
class GoogleApigeeApiProductOperationGroupOperationConfigsQuota:
    def __init__(
        self,
        *,
        interval: typing.Optional[builtins.str] = None,
        limit: typing.Optional[builtins.str] = None,
        time_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interval: Required. Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#interval GoogleApigeeApiProduct#interval}
        :param limit: Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#limit GoogleApigeeApiProduct#limit}
        :param time_unit: Time unit defined for the interval. Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#time_unit GoogleApigeeApiProduct#time_unit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e00e7a69e29f4f579eed5f9dfa12ef03fbde8afe0ae3d32a6406fd1815874a)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument time_unit", value=time_unit, expected_type=type_hints["time_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if interval is not None:
            self._values["interval"] = interval
        if limit is not None:
            self._values["limit"] = limit
        if time_unit is not None:
            self._values["time_unit"] = time_unit

    @builtins.property
    def interval(self) -> typing.Optional[builtins.str]:
        '''Required. Time interval over which the number of request messages is calculated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#interval GoogleApigeeApiProduct#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit(self) -> typing.Optional[builtins.str]:
        '''Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#limit GoogleApigeeApiProduct#limit}
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_unit(self) -> typing.Optional[builtins.str]:
        '''Time unit defined for the interval.

        Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#time_unit GoogleApigeeApiProduct#time_unit}
        '''
        result = self._values.get("time_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductOperationGroupOperationConfigsQuota(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeApiProductOperationGroupOperationConfigsQuotaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductOperationGroupOperationConfigsQuotaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8407ec046c98065da928378303b9744f73e3ebf2e84408c4c368a034124ec73c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetLimit")
    def reset_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimit", []))

    @jsii.member(jsii_name="resetTimeUnit")
    def reset_time_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeUnit", []))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="timeUnitInput")
    def time_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4bfcad8b958cef0364481ffe4af48782024af46f46278a24074d917661aa94e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9778a30215e9904141402e6d600ebdb51aa8f3397d125b91f95faa418ebc1f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeUnit")
    def time_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeUnit"))

    @time_unit.setter
    def time_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed1c0eb3abcb91700c03f3889dba9c90123a590b0db1ef67e0648da18bf2ece3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeApiProductOperationGroupOperationConfigsQuota]:
        return typing.cast(typing.Optional[GoogleApigeeApiProductOperationGroupOperationConfigsQuota], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeApiProductOperationGroupOperationConfigsQuota],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9020d103b8cb24107802ea4bee7040f46e19b4bcf4f8cae1f867426b67e009d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeApiProductOperationGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductOperationGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d04276c8fb8a1f654d207a427ff4b350ae39ba8923d9d46c9c3223b61d6b6e9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperationConfigs")
    def put_operation_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f886e3701a980a8d88df9b2d9d40316edc8508a82585acdd100f7d5ca99f4819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperationConfigs", [value]))

    @jsii.member(jsii_name="resetOperationConfigs")
    def reset_operation_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationConfigs", []))

    @jsii.member(jsii_name="resetOperationConfigType")
    def reset_operation_config_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationConfigType", []))

    @builtins.property
    @jsii.member(jsii_name="operationConfigs")
    def operation_configs(
        self,
    ) -> GoogleApigeeApiProductOperationGroupOperationConfigsList:
        return typing.cast(GoogleApigeeApiProductOperationGroupOperationConfigsList, jsii.get(self, "operationConfigs"))

    @builtins.property
    @jsii.member(jsii_name="operationConfigsInput")
    def operation_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigs]]], jsii.get(self, "operationConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="operationConfigTypeInput")
    def operation_config_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationConfigTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="operationConfigType")
    def operation_config_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationConfigType"))

    @operation_config_type.setter
    def operation_config_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5200cf795ae6c292faf388ecc16457f062ac48986a33ea9c56c4d5e414f16e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationConfigType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleApigeeApiProductOperationGroup]:
        return typing.cast(typing.Optional[GoogleApigeeApiProductOperationGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeApiProductOperationGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9461181b514f9dc207f9df1ddd77ce7928df8620613ff445a92a4a5337af883e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleApigeeApiProductTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#create GoogleApigeeApiProduct#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#delete GoogleApigeeApiProduct#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#update GoogleApigeeApiProduct#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c0b2c9cda19f2c47074155d32c33ab78d316c3e87b659aafc66becd33eb58a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#create GoogleApigeeApiProduct#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#delete GoogleApigeeApiProduct#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_api_product#update GoogleApigeeApiProduct#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeApiProductTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeApiProductTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeApiProduct.GoogleApigeeApiProductTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28beb99966cc561b7a10f1315e854818a7b37a93b6f02fc884c3de528440c1ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20edc9be6d506f5559680877ec4a63a4067a6237ce5e511eda9a37b2e1e66b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab4cd89c3538bbdd43df7dc7cef0aa43b18e6b9a080537b8b81709898fdd8ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0079a949cdaeed8c95c14545f8afce57651acb009b2bea9ff6e801ba619caebe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1165c9e1c0170f2ccb5e578ec21a5679afdd4378353c5efcfc250ee1639a99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleApigeeApiProduct",
    "GoogleApigeeApiProductAttributes",
    "GoogleApigeeApiProductAttributesList",
    "GoogleApigeeApiProductAttributesOutputReference",
    "GoogleApigeeApiProductConfig",
    "GoogleApigeeApiProductGraphqlOperationGroup",
    "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs",
    "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes",
    "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesList",
    "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesOutputReference",
    "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsList",
    "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations",
    "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsList",
    "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsOutputReference",
    "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOutputReference",
    "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota",
    "GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuotaOutputReference",
    "GoogleApigeeApiProductGraphqlOperationGroupOutputReference",
    "GoogleApigeeApiProductGrpcOperationGroup",
    "GoogleApigeeApiProductGrpcOperationGroupOperationConfigs",
    "GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes",
    "GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributesList",
    "GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributesOutputReference",
    "GoogleApigeeApiProductGrpcOperationGroupOperationConfigsList",
    "GoogleApigeeApiProductGrpcOperationGroupOperationConfigsOutputReference",
    "GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota",
    "GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuotaOutputReference",
    "GoogleApigeeApiProductGrpcOperationGroupOutputReference",
    "GoogleApigeeApiProductOperationGroup",
    "GoogleApigeeApiProductOperationGroupOperationConfigs",
    "GoogleApigeeApiProductOperationGroupOperationConfigsAttributes",
    "GoogleApigeeApiProductOperationGroupOperationConfigsAttributesList",
    "GoogleApigeeApiProductOperationGroupOperationConfigsAttributesOutputReference",
    "GoogleApigeeApiProductOperationGroupOperationConfigsList",
    "GoogleApigeeApiProductOperationGroupOperationConfigsOperations",
    "GoogleApigeeApiProductOperationGroupOperationConfigsOperationsList",
    "GoogleApigeeApiProductOperationGroupOperationConfigsOperationsOutputReference",
    "GoogleApigeeApiProductOperationGroupOperationConfigsOutputReference",
    "GoogleApigeeApiProductOperationGroupOperationConfigsQuota",
    "GoogleApigeeApiProductOperationGroupOperationConfigsQuotaOutputReference",
    "GoogleApigeeApiProductOperationGroupOutputReference",
    "GoogleApigeeApiProductTimeouts",
    "GoogleApigeeApiProductTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__33fee3793f5c7cfdf853bc7f94cf2fdda03d5a3ebce935e173face88980d4c28(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    name: builtins.str,
    org_id: builtins.str,
    api_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    approval_type: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductAttributes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    environments: typing.Optional[typing.Sequence[builtins.str]] = None,
    graphql_operation_group: typing.Optional[typing.Union[GoogleApigeeApiProductGraphqlOperationGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_operation_group: typing.Optional[typing.Union[GoogleApigeeApiProductGrpcOperationGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    operation_group: typing.Optional[typing.Union[GoogleApigeeApiProductOperationGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
    quota: typing.Optional[builtins.str] = None,
    quota_counter_scope: typing.Optional[builtins.str] = None,
    quota_interval: typing.Optional[builtins.str] = None,
    quota_time_unit: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    space: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeApiProductTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__23c7775c8d793754dd087a8269e81d7caae77155cd08b12ae7aa224c8ae74704(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a481cd3d3ab4b2120e39f468208e4fe489a8904333aed23ab5d1d602e7143af6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductAttributes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__669868253939cebc06f197fca4fb2a0661b1d00a170ff984fa0c830c09dbd49b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947853c0faaedc690d9885bcc4ca79b878fa16523d4eec7e122d3469c210ac3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188e0508c0888e679ad5166b0cd28d645f905a35ffcb3036ff59d6468d83c2ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b25cdef51640a4d0aa77efd6be11cfa8fcb7151d95078a847e596729f5b529e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__012fe2165426c8a6dc38fed5b39dafe54eaf175f9e73a4add9c9690ef28b3d3a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a6453e3acd476b4887236155f8b5924330244fd5fc1b28473252360f5fc2e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dff35e929574f73ec4df769bdd7e2690f9cc806f661d588a18afd634ee3bb44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152812118ffd3b3360686624727b460d8506b82db44cb52c07a4a90ae4305e42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78aa7aac21e055b917672c2b238c776f6c59dda915e504e90074e4ada8da8c20(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595ee6f4f65602c7bc5ef5b9fe8e9514620af5b2c4dd41fa4b213eb6f201157b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__875fd5f1e8c485e6d033f428cf5c002412b4a66e4b1ab7e30d1e750c761ac622(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98be399cf02c8821ce3c8e9bcd996595698181804b13f08dd709e20385f1252a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec44498a65b86b553b4c9654ccbe0ab09108288bc8ce1efd494de2066442eb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6cb2ad432efad35dc4a22171c5c7752790986d7d64479c7e3dea337a56b55e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377297d908886bde0706f12aba2eff3c254361ef1bc27abba371fc600078c687(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a3ee76430cda167fd930af908d589889c36308eac05d5b36c33a30fceb2edc(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1358ca9e99b4b62203ada4ab5634f0138921898e3edee94a8465535795708bd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecfe13f870ba930d1ae54493244694c308435008dfe13f5275a7dd73410f64a8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048bdad59d5b0fc352b431a7096ea2890c28a6df44f5ad2f151a0f750e268de4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47e2a54b40975e6d9411ed9b040977bbb1538f250b3d3e12a492773fa67dc68(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d39ca2277e587f7ac7bcb5bcd2b159001f418405752e65061a99aa7c8aeb882(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec9ae86291a6873d6bfb579da6a04c31be2b36f6ec6ce39251723bf080462ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductAttributes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fcda4a05dcd04361f070e4aa3ec176f5a21913437ff8b251fffb6d16eb2db3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde72aabea3785af439489b6ae9182a309f5b05e69665355d150a2464db0844b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6589392c2a3b5c971b3e8a51e5065252e5ff6b0a26f8075f8411e1aff736bc20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__803e640ae55d649303c75a95457371f8fb80b0c742d6961991f4b00186d714d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2fe238bad8f79212011b4d6ccf5d59058f8633ef027389548fe335ea4549299(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    name: builtins.str,
    org_id: builtins.str,
    api_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    approval_type: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductAttributes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    environments: typing.Optional[typing.Sequence[builtins.str]] = None,
    graphql_operation_group: typing.Optional[typing.Union[GoogleApigeeApiProductGraphqlOperationGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_operation_group: typing.Optional[typing.Union[GoogleApigeeApiProductGrpcOperationGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    operation_group: typing.Optional[typing.Union[GoogleApigeeApiProductOperationGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
    quota: typing.Optional[builtins.str] = None,
    quota_counter_scope: typing.Optional[builtins.str] = None,
    quota_interval: typing.Optional[builtins.str] = None,
    quota_time_unit: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    space: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeApiProductTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__facd936e205ac6ca654567899d9381d47de9cbef1f6434dd3ed055382b049069(
    *,
    operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operation_config_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d392294de9959a6146c288ebd5a21d45b637bdb4a6e355502b4e12dc3788107c(
    *,
    api_source: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    quota: typing.Optional[typing.Union[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a67a50d837580ecc9b5582c9c97ab724a528a55ed44a3db5d0a1d9e6be9bb96(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf9915ea4783070e5764ca479b92cb935ef3b21a3f3e30804676afc2f337d01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b8fe31c8ea3ba902bcb1b5943364018b29b94682791fbf119776c289cd75e8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35935a50dd2f9ee78a064c1fbf4c171032a8ba0c24a94937b3b20550df6b159(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c375fa0b978d56a03ee6dd7ba72afdcb2c0aa03088066a183329b9f1f60ed8a9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a705c7f21c9c9c950bfd7e0ea520ffc0404182038997c96282a2aa9c9e6a90ab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0829670015ca4b8b826e9c91fc6c9d36b00e770a86b5857e9ec8697ccec25f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b78b130339a9066db0d7ebb43151b2d30130ad62651302bc6b755e09635fac4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2615aa9087d7817166fe93cf956d5f5ccd44a875e4619c5f98622537d38c3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d239b3fa1417fee916ac421dbe08107f4b320c85200e89b72b0d6124912386(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec7499becca61b70ccb266552a84695ca016b59b8eeb45c7b115f55fac5265d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fca154422b7f308577ff595c1920635eed59ecc22b7ef87e075fedc9d50896(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ca76a96fff2d7723782deb849797c2872fd996a87b08e73f8428c3085a986c4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb234c7f5321600c26579b8a4802b09fbd452e65a9c6998c75e5a371ec6e198(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6af4d2885c1132cec80c8274d0abe365666c72b9e1bb416052521f454445c12(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d89c17305012b2c71fe5dd5e419b21b1eec1359d560b7b9af57cc52a91a71366(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75ae4e2acc76066c4337b108cd2b72c5bdf590521d1baa1e7ca7caeb21f675c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b884935aa4274f0b0c5ac63c552855b24852912dfcd4a37e9f48298dd5d379(
    *,
    operation: typing.Optional[builtins.str] = None,
    operation_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b1a7ff5cc469e4fd3a7b5feb67f0e9447fbd405a27e212cabca25c9734a458(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0137c2945d963690aa5cba53b1c664aab786b192daea9901160123f62cc62ac4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9253c65455581aeeaff86a00a385ae1cd8480d719246b94a26099fc3ddfa6937(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e916a507ae2d2308d8eebe4ecc294ba1571e5d653795c1036af934c86d6afba0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0d0e375b152d089660d63c5696339b30ba4b5092ef880cd80617c55e660ba46(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e785bdce038fabdcf5ff2c1d8ace863279fdb2e90ed3a975dfc211a6a3fce588(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4381f29e9ad20144cd7546a20b63ec957f2dad5d32147e00b7c1279d01e088ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__683c93021062825525f7868ff9d640706b5024ea93fc253b345a19248d9e9a18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c54e2ffea0b9772f482f60cfb474d17a500170bea2246757f7af2e0f7f53d0b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4683a24798af1f521f2dcc6cb0561f31b301d0ef3f345136507d5b463007b35(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931ab05734b7e17f80acb5c2816162cece98bbc0354e621d50865ac37fdc6e53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e3eb33251d705f591de3642c09b07c0f95abf089d1a6a4709ab1bad016fc09(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc95bdab1e7b70fecd0de08e744f37c803cfd7f0be78ad9d3cf34e1e06dd466(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b892a3dc3c187f839fea215bcbefcb3652d6cc3a64537160db73cd9dee235bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3dfa5ef550f1057c9978f3f617e7fcfcd5a33690239af73390a0012459aa6c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796bb2d846ef922e179a147065886cf48369bdf83f74b08a9af6cb6ee07f4b0e(
    *,
    interval: typing.Optional[builtins.str] = None,
    limit: typing.Optional[builtins.str] = None,
    time_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85692d0e7ad5458932c904cb42dcd36b6d6bf23aea1ca77d14522202f3b8590(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e112509e6546379dc0587869410bc2c85444d79144efe23f2e13de42e4062586(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a990a7fcb1784fe09511b5de39bf41149800c2effc37c7b8f57d7dc03ef5f5f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf98e935ffbba8c85f49a61373ed2a8bbe7cfb171c054d93a44171fa9e9f6804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df3985b4ff95ea0a141982c28547bc249362f25b23a579eb209ea4c4de8a380(
    value: typing.Optional[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigsQuota],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6e0ed84649194a62c621bae30e52e6226f6b72a2dc147a4fc9cda5fa0a73c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e60d245e99dfc43de94c86309d43f1f52db922ee17a8bc23d1352896934f936(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductGraphqlOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66506e86e7e8a4ced93eea7da9fa4491a2c774e2b6d2ba784304a3db784c30ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b4abaee9caf9cbe66e8eba33f8327318ceb3d3e9771298dade3e42a35073d4(
    value: typing.Optional[GoogleApigeeApiProductGraphqlOperationGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81cb8713b7c8a5f78d0be231f57a96a0ead13d502326c68fb8e2ffd1cfacc76e(
    *,
    operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductGrpcOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e692c41cd188a4315b626fc74e61a879c35a11a4f7c90db98f64386a1c130514(
    *,
    api_source: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    quota: typing.Optional[typing.Union[GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota, typing.Dict[builtins.str, typing.Any]]] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e0a84ce479265e1dd8695028a001e855434c17cee3b7d794ac2efde8f6da0a(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e109872b36820fdd1dd3fe5bf2114d16b34bcf2714892cfb9fa6ae3019159c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4472e14062911d32d52e23e2a693e3ee3a265198c9318f081d33916075811b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22bbb49ec8095fadf2910775b267e29fc61870ca6f1fe7ff255df655e5b7b5d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62459ffc38cd265784c783218a4e17d6252823a049714e91a853fbd6a169bb5d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8079fb86623f88db0b83912b4aa4fe882a0a05ee47abc647329706ecadb8247e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9374e951e9d05e5506682ebecb45fed7d6b83e65c86f4d51010482004ed930c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e57448d3ecceeb5b371ba9d7f1fab6c1f867daf04bb2151a8f802b6e5dd8cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670eecb10a80dc8caf5b0aaf8f785bfca3fa64b305abf1803bfd09ad4067a539(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c9b29166235334843950c4521e0f68d8fa32d6015e2eed56102b0eb7a92439(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0006e1b163f820ee21991cb0beadd783678bc4134d663759b016f4c705eb43f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5264048c7f6c4f205d624bf8f660d7f01bd3c03fdd2f6cfc3a9665db1298804(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b6d8d53f734dd475bbbe059f3c8be2ada98b8be339c8b126300c47cbe1235a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ef7930b29d87f9cc245c68412afaf8cb574daa3c4d42ce15b08d493291f244(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2123accdcaf188654bc2bda050575ee87c45c8b90ac0751247dfe3c170d191ee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509e9f1692dda76c7fbbb13c27c07649dcec8a6b2c4f9ee4625752a457382608(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689bf1db81520114497b4823ff65707deb229ccba976a51398af4148eecb1df7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductGrpcOperationGroupOperationConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a7c09c17f7f03156f9ab3fcc2457e0b997c07585e58f8f1ba3dac81df735d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d513929c04a59b590948dac8c0232199344621376e734ef2db8b0f47f140dc68(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductGrpcOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09c3c06f7d3ad33c3927781eb9562b326751a25c5536aa0f4f07dcd7fe804b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ea3f913ad2f23eb3ccb66f89e357c592fc74841075df9d725f93658c086c21d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55b7fc3cc14b85a3bc42c48b2a14d7c653c32a92225d281f89cf9d74de47688(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143dafb423f9ef77e4a1841253eb3d02c0fe2724e1293ce24a73ba445c0cfbb4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductGrpcOperationGroupOperationConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b6980e74e721c848b9e81c243a53f4f5c11d70799e4c8cdcf0699af2bb2b25(
    *,
    interval: typing.Optional[builtins.str] = None,
    limit: typing.Optional[builtins.str] = None,
    time_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78812791e4975c43ec45c9c3afbf9d37a95b6fa54d06dd59a3beb9a1dc7fde81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721b9f6f11b7522d559847dc6097dc536684bc71ad0d4af5646351a543837af2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ce656a3f84f2c9053e5525e6ede7aa0e43987a4a1f399e8ad614bf7f08ce15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c06b087afa8a03b882727935418b87b4383705356049bcef5dc80fb487dba00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccfbd666000d562aa7e25388e7d6d42cb0bb055becd5339d638df98fe2e5c3ff(
    value: typing.Optional[GoogleApigeeApiProductGrpcOperationGroupOperationConfigsQuota],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3bcc2e37f8f6edceb8608c7602a74fbeef55a5cf8db778f6ec98cc2dfc31ade(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b5d2ac8259fe848324be33a67e99dd734f5bbb02e175dfb1b7a437dbcaad09(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductGrpcOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48fd6db39ef2771d7badf2d7697aa5d7e80c55a06b7401c93fc612755ad31f53(
    value: typing.Optional[GoogleApigeeApiProductGrpcOperationGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de0cb1db0c453431ba2c99fc61dd9786f24e72baff8b739fc88c374f4c6a6c5(
    *,
    operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operation_config_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cda39321c7977b50b65dd2d9f4f1bfbe2205740519d43055439a669e759fc11(
    *,
    api_source: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductOperationGroupOperationConfigsOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    quota: typing.Optional[typing.Union[GoogleApigeeApiProductOperationGroupOperationConfigsQuota, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603fd5dfb91ffbef1ea19f9f58a79f5a794da73147648eeaad115cc6bdf6a34c(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4918ad440eb5bfdc3d3921736bdd2a86fb3d2eb474839d48c51baf323c6da88b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3102dc9e93b0a9e8479d468052f3bfb348e6f365b2381cc627ff2d4ebcfd2266(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879ac236ecf5f9576855dc6eee36a6dc9089bcc24cafb5a6317f8de47ca5b57f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e133cb6d49cdd9e8db9c59c499e7caf7dce01ac064cde2033c09e44202a358(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5958ab6f5ccc8c6a4bf56aa6b33f986734fab836677c3fca156fde057ede3a8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae6e08b518d00c37cc8150556fde6d49d69d41c789290bee590cba985851e85(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigsAttributes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5159732ab9e27bd49211ac841bd4cc5360e2623bdc4cdc84086226b6b4fc04f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6fba974e1cf6d9c5fb731a76ff04a85c3e1a94e25449031961c3806f46db893(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__276eb26bb42106753cf1a621736b8b750874da8838548be7b0dccc067dc5afb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3900ebec2a1e13c226f056483cc6734b4a40bed3cf1559a581720ff56983ae84(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductOperationGroupOperationConfigsAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1fd025e040a95f35f4722c5025908434ad246479bba3377110af7c79883159(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f614756148fb519b1648a6d0c1a29f38df88bdb3a052c7c0f96e6a0186f20a3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84873bd41b029f7930c1d44a56c580d1171946cb0fb2d229000e72229565106a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0c59f4633080ae05666412e18ffa818b8b9aeaee75d964e62b90bcb1c3ba15(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32735597ac56373d6440faff14403f0e3560813176474542260ddbcd0f1e98a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9829f6556a130aae1875d27893f9195c9d67a8f49f87dcd62f2a05c30f68bdb0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb9bc7ac2528419272341aa16eab08e2ee1ce859499244f27d622e8b42d1cf0(
    *,
    methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57bb4dce96fb3eee4830fae5533728dc5405195af817300c7f29ee6b2504473(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa704971f29cbf5676420407b8f907492e8aa968a8417345c7c3c324b0fec4a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ba71b960ca8d6280d61604327b7848dace8cf3cd575b168888d7add54d2e3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d95f53a8fefa267b153b3fe22300eabbd0241610d900578ee7f9dd8420bedaee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6147d9887f17664af25d1affb53e17c35b9b4a7edefc68237ed80005b3cbe51f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__453e310ec73a37feea9aacf0760a05865e289d7e8cdabce2c93cc4846ebc9a6c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeApiProductOperationGroupOperationConfigsOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a90e6bb0755fa7ae81d7b45b70256cca82c2dcbfca2efed9dd09e37be1c44ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed365088a181a493923786dc7651c13a4d3a7a5d6c6709fc784eb18f7c7a9794(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3b0783cb35a670c36a063e1e2d5725a59470d03763de68750db795fca1b35e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13e366530941adc3be2efbb8b4934e5411a579759a7360835d6644265b7e396(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductOperationGroupOperationConfigsOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87d82aa57beae463bf0446120ebc3b07bd7f62f05740bac3b37ece3e41868d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83482e4aef2eeaf591fc69d0be4466e28c265fa42ee36d940784b5b5d2836ab(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf15cca150b26cfded3aa1ce75ba6e4df165be6765d4312a19f9fed96ceb652f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductOperationGroupOperationConfigsOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a49f7d1b2f52352164c0ac073ff63d6f82bf662f757bada6a5b7564108b70d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d898d098b7bc8d50a5578f2bd96511d1b7fc88bd827b18ec8948af0f14a888(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductOperationGroupOperationConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e00e7a69e29f4f579eed5f9dfa12ef03fbde8afe0ae3d32a6406fd1815874a(
    *,
    interval: typing.Optional[builtins.str] = None,
    limit: typing.Optional[builtins.str] = None,
    time_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8407ec046c98065da928378303b9744f73e3ebf2e84408c4c368a034124ec73c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4bfcad8b958cef0364481ffe4af48782024af46f46278a24074d917661aa94e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9778a30215e9904141402e6d600ebdb51aa8f3397d125b91f95faa418ebc1f4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed1c0eb3abcb91700c03f3889dba9c90123a590b0db1ef67e0648da18bf2ece3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9020d103b8cb24107802ea4bee7040f46e19b4bcf4f8cae1f867426b67e009d(
    value: typing.Optional[GoogleApigeeApiProductOperationGroupOperationConfigsQuota],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04276c8fb8a1f654d207a427ff4b350ae39ba8923d9d46c9c3223b61d6b6e9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f886e3701a980a8d88df9b2d9d40316edc8508a82585acdd100f7d5ca99f4819(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeApiProductOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5200cf795ae6c292faf388ecc16457f062ac48986a33ea9c56c4d5e414f16e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9461181b514f9dc207f9df1ddd77ce7928df8620613ff445a92a4a5337af883e(
    value: typing.Optional[GoogleApigeeApiProductOperationGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c0b2c9cda19f2c47074155d32c33ab78d316c3e87b659aafc66becd33eb58a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28beb99966cc561b7a10f1315e854818a7b37a93b6f02fc884c3de528440c1ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20edc9be6d506f5559680877ec4a63a4067a6237ce5e511eda9a37b2e1e66b1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab4cd89c3538bbdd43df7dc7cef0aa43b18e6b9a080537b8b81709898fdd8ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0079a949cdaeed8c95c14545f8afce57651acb009b2bea9ff6e801ba619caebe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1165c9e1c0170f2ccb5e578ec21a5679afdd4378353c5efcfc250ee1639a99(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeApiProductTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

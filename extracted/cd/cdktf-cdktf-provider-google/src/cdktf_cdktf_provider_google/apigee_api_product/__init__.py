r'''
# `google_apigee_api_product`

Refer to the Terraform Registry for docs: [`google_apigee_api_product`](https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product).
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


class ApigeeApiProduct(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProduct",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product google_apigee_api_product}.'''

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
        attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeApiProductAttributes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        environments: typing.Optional[typing.Sequence[builtins.str]] = None,
        graphql_operation_group: typing.Optional[typing.Union["ApigeeApiProductGraphqlOperationGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_operation_group: typing.Optional[typing.Union["ApigeeApiProductGrpcOperationGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        operation_group: typing.Optional[typing.Union["ApigeeApiProductOperationGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
        quota: typing.Optional[builtins.str] = None,
        quota_counter_scope: typing.Optional[builtins.str] = None,
        quota_interval: typing.Optional[builtins.str] = None,
        quota_time_unit: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        space: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApigeeApiProductTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product google_apigee_api_product} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Name displayed in the UI or developer portal to developers registering for API access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#display_name ApigeeApiProduct#display_name}
        :param name: Internal name of the API product. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#name ApigeeApiProduct#name}
        :param org_id: The Apigee Organization associated with the Apigee API product, in the format 'organizations/{{org_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#org_id ApigeeApiProduct#org_id}
        :param api_resources: Comma-separated list of API resources to be bundled in the API product. By default, the resource paths are mapped from the proxy.pathsuffix variable. The proxy path suffix is defined as the URI fragment following the ProxyEndpoint base path. For example, if the apiResources element is defined to be /forecastrss and the base path defined for the API proxy is /weather, then only requests to /weather/forecastrss are permitted by the API product. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#api_resources ApigeeApiProduct#api_resources}
        :param approval_type: Flag that specifies how API keys are approved to access the APIs defined by the API product. Valid values are 'auto' or 'manual'. Possible values: ["auto", "manual"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#approval_type ApigeeApiProduct#approval_type}
        :param attributes: attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#attributes ApigeeApiProduct#attributes}
        :param description: Description of the API product. Include key information about the API product that is not captured by other fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#description ApigeeApiProduct#description}
        :param environments: Comma-separated list of environment names to which the API product is bound. Requests to environments that are not listed are rejected. By specifying one or more environments, you can bind the resources listed in the API product to a specific environment, preventing developers from accessing those resources through API proxies deployed in another environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#environments ApigeeApiProduct#environments}
        :param graphql_operation_group: graphql_operation_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#graphql_operation_group ApigeeApiProduct#graphql_operation_group}
        :param grpc_operation_group: grpc_operation_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#grpc_operation_group ApigeeApiProduct#grpc_operation_group}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#id ApigeeApiProduct#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param operation_group: operation_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_group ApigeeApiProduct#operation_group}
        :param proxies: Comma-separated list of API proxy names to which this API product is bound. By specifying API proxies, you can associate resources in the API product with specific API proxies, preventing developers from accessing those resources through other API proxies. Apigee rejects requests to API proxies that are not listed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#proxies ApigeeApiProduct#proxies}
        :param quota: Number of request messages permitted per app by this API product for the specified quotaInterval and quotaTimeUnit. For example, a quota of 50, for a quotaInterval of 12 and a quotaTimeUnit of hours means 50 requests are allowed every 12 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota ApigeeApiProduct#quota}
        :param quota_counter_scope: Scope of the quota decides how the quota counter gets applied and evaluate for quota violation. If the Scope is set as PROXY, then all the operations defined for the APIproduct that are associated with the same proxy will share the same quota counter set at the APIproduct level, making it a global counter at a proxy level. If the Scope is set as OPERATION, then each operations get the counter set at the API product dedicated, making it a local counter. Note that, the QuotaCounterScope applies only when an operation does not have dedicated quota set for itself. Possible values: ["QUOTA_COUNTER_SCOPE_UNSPECIFIED", "PROXY", "OPERATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota_counter_scope ApigeeApiProduct#quota_counter_scope}
        :param quota_interval: Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota_interval ApigeeApiProduct#quota_interval}
        :param quota_time_unit: Time unit defined for the quotaInterval. Valid values include second, minute, hour, day, month or year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota_time_unit ApigeeApiProduct#quota_time_unit}
        :param scopes: Comma-separated list of OAuth scopes that are validated at runtime. Apigee validates that the scopes in any access token presented match the scopes defined in the OAuth policy associated with the API product. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#scopes ApigeeApiProduct#scopes}
        :param space: Optional. The resource ID of the parent Space. If not set, the parent resource will be the Organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#space ApigeeApiProduct#space}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#timeouts ApigeeApiProduct#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6017f2ef836cffb7756622ee18bc7a751d71525d2d6a456afced6a4f65a7d9e7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApigeeApiProductConfig(
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
        '''Generates CDKTF code for importing a ApigeeApiProduct resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApigeeApiProduct to import.
        :param import_from_id: The id of the existing ApigeeApiProduct that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApigeeApiProduct to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc8f7f8d7117a2b85f604d31211389200a7c549b5ea10827780fb2029712b9c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAttributes")
    def put_attributes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeApiProductAttributes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79702e0506ab5070baaab0dcdcf03c462e0316b5d05cb579bff5eb8008d608f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAttributes", [value]))

    @jsii.member(jsii_name="putGraphqlOperationGroup")
    def put_graphql_operation_group(
        self,
        *,
        operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeApiProductGraphqlOperationGroupOperationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operation_config_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operation_configs: operation_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_configs ApigeeApiProduct#operation_configs}
        :param operation_config_type: Flag that specifes whether the configuration is for Apigee API proxy or a remote service. Valid values include proxy or remoteservice. Defaults to proxy. Set to proxy when Apigee API proxies are associated with the API product. Set to remoteservice when non-Apigee proxies like Istio-Envoy are associated with the API product. Possible values: ["proxy", "remoteservice"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_config_type ApigeeApiProduct#operation_config_type}
        '''
        value = ApigeeApiProductGraphqlOperationGroup(
            operation_configs=operation_configs,
            operation_config_type=operation_config_type,
        )

        return typing.cast(None, jsii.invoke(self, "putGraphqlOperationGroup", [value]))

    @jsii.member(jsii_name="putGrpcOperationGroup")
    def put_grpc_operation_group(
        self,
        *,
        operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeApiProductGrpcOperationGroupOperationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param operation_configs: operation_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_configs ApigeeApiProduct#operation_configs}
        '''
        value = ApigeeApiProductGrpcOperationGroup(operation_configs=operation_configs)

        return typing.cast(None, jsii.invoke(self, "putGrpcOperationGroup", [value]))

    @jsii.member(jsii_name="putOperationGroup")
    def put_operation_group(
        self,
        *,
        operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeApiProductOperationGroupOperationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operation_config_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operation_configs: operation_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_configs ApigeeApiProduct#operation_configs}
        :param operation_config_type: Flag that specifes whether the configuration is for Apigee API proxy or a remote service. Valid values include proxy or remoteservice. Defaults to proxy. Set to proxy when Apigee API proxies are associated with the API product. Set to remoteservice when non-Apigee proxies like Istio-Envoy are associated with the API product. Possible values: ["proxy", "remoteservice"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_config_type ApigeeApiProduct#operation_config_type}
        '''
        value = ApigeeApiProductOperationGroup(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#create ApigeeApiProduct#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#delete ApigeeApiProduct#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#update ApigeeApiProduct#update}.
        '''
        value = ApigeeApiProductTimeouts(create=create, delete=delete, update=update)

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
    def attributes(self) -> "ApigeeApiProductAttributesList":
        return typing.cast("ApigeeApiProductAttributesList", jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="graphqlOperationGroup")
    def graphql_operation_group(
        self,
    ) -> "ApigeeApiProductGraphqlOperationGroupOutputReference":
        return typing.cast("ApigeeApiProductGraphqlOperationGroupOutputReference", jsii.get(self, "graphqlOperationGroup"))

    @builtins.property
    @jsii.member(jsii_name="grpcOperationGroup")
    def grpc_operation_group(
        self,
    ) -> "ApigeeApiProductGrpcOperationGroupOutputReference":
        return typing.cast("ApigeeApiProductGrpcOperationGroupOutputReference", jsii.get(self, "grpcOperationGroup"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedAt")
    def last_modified_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifiedAt"))

    @builtins.property
    @jsii.member(jsii_name="operationGroup")
    def operation_group(self) -> "ApigeeApiProductOperationGroupOutputReference":
        return typing.cast("ApigeeApiProductOperationGroupOutputReference", jsii.get(self, "operationGroup"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApigeeApiProductTimeoutsOutputReference":
        return typing.cast("ApigeeApiProductTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductAttributes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductAttributes"]]], jsii.get(self, "attributesInput"))

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
    ) -> typing.Optional["ApigeeApiProductGraphqlOperationGroup"]:
        return typing.cast(typing.Optional["ApigeeApiProductGraphqlOperationGroup"], jsii.get(self, "graphqlOperationGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcOperationGroupInput")
    def grpc_operation_group_input(
        self,
    ) -> typing.Optional["ApigeeApiProductGrpcOperationGroup"]:
        return typing.cast(typing.Optional["ApigeeApiProductGrpcOperationGroup"], jsii.get(self, "grpcOperationGroupInput"))

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
    ) -> typing.Optional["ApigeeApiProductOperationGroup"]:
        return typing.cast(typing.Optional["ApigeeApiProductOperationGroup"], jsii.get(self, "operationGroupInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeApiProductTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeApiProductTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="apiResources")
    def api_resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apiResources"))

    @api_resources.setter
    def api_resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a73089ff50086d83ebab1878798b0c50fa01a4ec70c44487975653a2d7efd4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="approvalType")
    def approval_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "approvalType"))

    @approval_type.setter
    def approval_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25fd7b4f6955a67fd6096599326b43604db58f645487f80a07f303c382c223f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approvalType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18a98241211097f49b30842a8dd1ac4723941f7a2358c0e8a2ded6096a8c22c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b32a897237394e498329c3691bd7a329aca2526bda86ba99812ba6dc2a94e8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environments")
    def environments(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "environments"))

    @environments.setter
    def environments(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8999c9c7bcc61c0316da3da70f18b6e2a4f42232e1edab3214ce3e9d21ffafa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff7d4c2a87bcc4b5c47c38997f5346924b80fada2cf3d91aa907cdf85cdbe88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7a7a085f717dc7a16fa939ad65a43289578f5f3ddaf0d105e6b0d1da5f88d90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @org_id.setter
    def org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4acfafbfb881e7da63f5862ffc3bd4e3e81e23cd1ae0b4a24f751e889a9631d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxies")
    def proxies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "proxies"))

    @proxies.setter
    def proxies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26b59b8fb15fb2cfe14916512a2ca84ffe425ea7496a2385cd250801ec60c80b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quota")
    def quota(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quota"))

    @quota.setter
    def quota(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0800a65ba72d147ab0331e0d1e1c4832565c7d8cd41dfeeed3445caaf94cfe59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quota", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quotaCounterScope")
    def quota_counter_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quotaCounterScope"))

    @quota_counter_scope.setter
    def quota_counter_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f7c1b282c570e32b54e45cae3e1c35fbd5ca8308d4c21ccd6a843b6e2c41ec8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotaCounterScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quotaInterval")
    def quota_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quotaInterval"))

    @quota_interval.setter
    def quota_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6035ba9a1606ba288fa3b58c5d302aee4e1190aabcd2c2ddab744edca5b1d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotaInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quotaTimeUnit")
    def quota_time_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quotaTimeUnit"))

    @quota_time_unit.setter
    def quota_time_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4fdda4a2381c6c3b80b489c3e84aeb17050e11c187b5edd8556c52a14f96a13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotaTimeUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78c6efbae0fa3632955b2eda586c2424c13e32ad9a11c4ad2e75f80caf8f3745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="space")
    def space(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "space"))

    @space.setter
    def space(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109e98e14f4841657bf40a875664f2d6e396fc5458fbfb1e2138b22aceca43a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "space", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductAttributes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ApigeeApiProductAttributes:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Key of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#name ApigeeApiProduct#name}
        :param value: Value of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#value ApigeeApiProduct#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467c0062a6e51f011a34630f9cbc45299cb006d4d0f748ce4497cb5403750213)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#name ApigeeApiProduct#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#value ApigeeApiProduct#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeApiProductAttributesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductAttributesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d72f76c50ddbf685a33609badeef751bd4ea26d10d50e8b7a55d514998bbe8eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApigeeApiProductAttributesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__928a3ec9bbdd76f4e40342cc61b848e3eab0cbf1ae4880de47d8783f21aa454c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigeeApiProductAttributesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6071175010546a31d2420a67720a1bf36bb3be8d343ddcd0c50fda2cd1995e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__376e62e854f96837dedbe3ce27778827f67b4b457b304ca4819bdf93d9aa32fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a14c8682a5a6e5f04c670314d8c13c2c6671bc0d0ff130d4df7b687570171b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductAttributes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductAttributes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9bcf3ce9017729c2f4200fd8c1a48d22cb9d67335dba08127a70e1bf8898ec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeApiProductAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductAttributesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__242f551e17faa9a3a97357870b2c97183eb49a6c94565a16f27ec7f220d34090)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b84f26c11e14ec9975224b66353b5dba7a5b7e7ef81f3ef9accde1a48cc016c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83213f33c1c7c89814c62ae1378f859c667a3bf1d137517df90b0dc47c355912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0630fb2b6175f8239a9256364ac90022d1f4996362dd268720476c03169c5f83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductConfig",
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
class ApigeeApiProductConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductAttributes, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        environments: typing.Optional[typing.Sequence[builtins.str]] = None,
        graphql_operation_group: typing.Optional[typing.Union["ApigeeApiProductGraphqlOperationGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_operation_group: typing.Optional[typing.Union["ApigeeApiProductGrpcOperationGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        operation_group: typing.Optional[typing.Union["ApigeeApiProductOperationGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
        quota: typing.Optional[builtins.str] = None,
        quota_counter_scope: typing.Optional[builtins.str] = None,
        quota_interval: typing.Optional[builtins.str] = None,
        quota_time_unit: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        space: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApigeeApiProductTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Name displayed in the UI or developer portal to developers registering for API access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#display_name ApigeeApiProduct#display_name}
        :param name: Internal name of the API product. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#name ApigeeApiProduct#name}
        :param org_id: The Apigee Organization associated with the Apigee API product, in the format 'organizations/{{org_name}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#org_id ApigeeApiProduct#org_id}
        :param api_resources: Comma-separated list of API resources to be bundled in the API product. By default, the resource paths are mapped from the proxy.pathsuffix variable. The proxy path suffix is defined as the URI fragment following the ProxyEndpoint base path. For example, if the apiResources element is defined to be /forecastrss and the base path defined for the API proxy is /weather, then only requests to /weather/forecastrss are permitted by the API product. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#api_resources ApigeeApiProduct#api_resources}
        :param approval_type: Flag that specifies how API keys are approved to access the APIs defined by the API product. Valid values are 'auto' or 'manual'. Possible values: ["auto", "manual"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#approval_type ApigeeApiProduct#approval_type}
        :param attributes: attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#attributes ApigeeApiProduct#attributes}
        :param description: Description of the API product. Include key information about the API product that is not captured by other fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#description ApigeeApiProduct#description}
        :param environments: Comma-separated list of environment names to which the API product is bound. Requests to environments that are not listed are rejected. By specifying one or more environments, you can bind the resources listed in the API product to a specific environment, preventing developers from accessing those resources through API proxies deployed in another environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#environments ApigeeApiProduct#environments}
        :param graphql_operation_group: graphql_operation_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#graphql_operation_group ApigeeApiProduct#graphql_operation_group}
        :param grpc_operation_group: grpc_operation_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#grpc_operation_group ApigeeApiProduct#grpc_operation_group}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#id ApigeeApiProduct#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param operation_group: operation_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_group ApigeeApiProduct#operation_group}
        :param proxies: Comma-separated list of API proxy names to which this API product is bound. By specifying API proxies, you can associate resources in the API product with specific API proxies, preventing developers from accessing those resources through other API proxies. Apigee rejects requests to API proxies that are not listed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#proxies ApigeeApiProduct#proxies}
        :param quota: Number of request messages permitted per app by this API product for the specified quotaInterval and quotaTimeUnit. For example, a quota of 50, for a quotaInterval of 12 and a quotaTimeUnit of hours means 50 requests are allowed every 12 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota ApigeeApiProduct#quota}
        :param quota_counter_scope: Scope of the quota decides how the quota counter gets applied and evaluate for quota violation. If the Scope is set as PROXY, then all the operations defined for the APIproduct that are associated with the same proxy will share the same quota counter set at the APIproduct level, making it a global counter at a proxy level. If the Scope is set as OPERATION, then each operations get the counter set at the API product dedicated, making it a local counter. Note that, the QuotaCounterScope applies only when an operation does not have dedicated quota set for itself. Possible values: ["QUOTA_COUNTER_SCOPE_UNSPECIFIED", "PROXY", "OPERATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota_counter_scope ApigeeApiProduct#quota_counter_scope}
        :param quota_interval: Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota_interval ApigeeApiProduct#quota_interval}
        :param quota_time_unit: Time unit defined for the quotaInterval. Valid values include second, minute, hour, day, month or year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota_time_unit ApigeeApiProduct#quota_time_unit}
        :param scopes: Comma-separated list of OAuth scopes that are validated at runtime. Apigee validates that the scopes in any access token presented match the scopes defined in the OAuth policy associated with the API product. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#scopes ApigeeApiProduct#scopes}
        :param space: Optional. The resource ID of the parent Space. If not set, the parent resource will be the Organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#space ApigeeApiProduct#space}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#timeouts ApigeeApiProduct#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(graphql_operation_group, dict):
            graphql_operation_group = ApigeeApiProductGraphqlOperationGroup(**graphql_operation_group)
        if isinstance(grpc_operation_group, dict):
            grpc_operation_group = ApigeeApiProductGrpcOperationGroup(**grpc_operation_group)
        if isinstance(operation_group, dict):
            operation_group = ApigeeApiProductOperationGroup(**operation_group)
        if isinstance(timeouts, dict):
            timeouts = ApigeeApiProductTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073dc733d0d05b808d75d23bc661bc8c187d4c00fe992c0f62bb6274974d55d6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#display_name ApigeeApiProduct#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Internal name of the API product.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#name ApigeeApiProduct#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def org_id(self) -> builtins.str:
        '''The Apigee Organization associated with the Apigee API product, in the format 'organizations/{{org_name}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#org_id ApigeeApiProduct#org_id}
        '''
        result = self._values.get("org_id")
        assert result is not None, "Required property 'org_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Comma-separated list of API resources to be bundled in the API product.

        By default, the resource paths are mapped from the proxy.pathsuffix variable.
        The proxy path suffix is defined as the URI fragment following the ProxyEndpoint base path. For example, if the apiResources element is defined to be /forecastrss and the base path defined for the API proxy is /weather, then only requests to /weather/forecastrss are permitted by the API product.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#api_resources ApigeeApiProduct#api_resources}
        '''
        result = self._values.get("api_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def approval_type(self) -> typing.Optional[builtins.str]:
        '''Flag that specifies how API keys are approved to access the APIs defined by the API product.

        Valid values are 'auto' or 'manual'. Possible values: ["auto", "manual"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#approval_type ApigeeApiProduct#approval_type}
        '''
        result = self._values.get("approval_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductAttributes]]]:
        '''attributes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#attributes ApigeeApiProduct#attributes}
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductAttributes]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the API product. Include key information about the API product that is not captured by other fields.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#description ApigeeApiProduct#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environments(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Comma-separated list of environment names to which the API product is bound.

        Requests to environments that are not listed are rejected.
        By specifying one or more environments, you can bind the resources listed in the API product to a specific environment, preventing developers from accessing those resources through API proxies deployed in another environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#environments ApigeeApiProduct#environments}
        '''
        result = self._values.get("environments")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def graphql_operation_group(
        self,
    ) -> typing.Optional["ApigeeApiProductGraphqlOperationGroup"]:
        '''graphql_operation_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#graphql_operation_group ApigeeApiProduct#graphql_operation_group}
        '''
        result = self._values.get("graphql_operation_group")
        return typing.cast(typing.Optional["ApigeeApiProductGraphqlOperationGroup"], result)

    @builtins.property
    def grpc_operation_group(
        self,
    ) -> typing.Optional["ApigeeApiProductGrpcOperationGroup"]:
        '''grpc_operation_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#grpc_operation_group ApigeeApiProduct#grpc_operation_group}
        '''
        result = self._values.get("grpc_operation_group")
        return typing.cast(typing.Optional["ApigeeApiProductGrpcOperationGroup"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#id ApigeeApiProduct#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operation_group(self) -> typing.Optional["ApigeeApiProductOperationGroup"]:
        '''operation_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_group ApigeeApiProduct#operation_group}
        '''
        result = self._values.get("operation_group")
        return typing.cast(typing.Optional["ApigeeApiProductOperationGroup"], result)

    @builtins.property
    def proxies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Comma-separated list of API proxy names to which this API product is bound.

        By specifying API proxies, you can associate resources in the API product with specific API proxies, preventing developers from accessing those resources through other API proxies.
        Apigee rejects requests to API proxies that are not listed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#proxies ApigeeApiProduct#proxies}
        '''
        result = self._values.get("proxies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def quota(self) -> typing.Optional[builtins.str]:
        '''Number of request messages permitted per app by this API product for the specified quotaInterval and quotaTimeUnit.

        For example, a quota of 50, for a quotaInterval of 12 and a quotaTimeUnit of hours means 50 requests are allowed every 12 hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota ApigeeApiProduct#quota}
        '''
        result = self._values.get("quota")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quota_counter_scope(self) -> typing.Optional[builtins.str]:
        '''Scope of the quota decides how the quota counter gets applied and evaluate for quota violation.

        If the Scope is set as PROXY, then all the operations defined for the APIproduct that are associated with the same proxy will share the same quota counter set at the APIproduct level, making it a global counter at a proxy level. If the Scope is set as OPERATION, then each operations get the counter set at the API product dedicated, making it a local counter. Note that, the QuotaCounterScope applies only when an operation does not have dedicated quota set for itself. Possible values: ["QUOTA_COUNTER_SCOPE_UNSPECIFIED", "PROXY", "OPERATION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota_counter_scope ApigeeApiProduct#quota_counter_scope}
        '''
        result = self._values.get("quota_counter_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quota_interval(self) -> typing.Optional[builtins.str]:
        '''Time interval over which the number of request messages is calculated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota_interval ApigeeApiProduct#quota_interval}
        '''
        result = self._values.get("quota_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quota_time_unit(self) -> typing.Optional[builtins.str]:
        '''Time unit defined for the quotaInterval. Valid values include second, minute, hour, day, month or year.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota_time_unit ApigeeApiProduct#quota_time_unit}
        '''
        result = self._values.get("quota_time_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Comma-separated list of OAuth scopes that are validated at runtime.

        Apigee validates that the scopes in any access token presented match the scopes defined in the OAuth policy associated with the API product.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#scopes ApigeeApiProduct#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def space(self) -> typing.Optional[builtins.str]:
        '''Optional. The resource ID of the parent Space. If not set, the parent resource will be the Organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#space ApigeeApiProduct#space}
        '''
        result = self._values.get("space")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApigeeApiProductTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#timeouts ApigeeApiProduct#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApigeeApiProductTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGraphqlOperationGroup",
    jsii_struct_bases=[],
    name_mapping={
        "operation_configs": "operationConfigs",
        "operation_config_type": "operationConfigType",
    },
)
class ApigeeApiProductGraphqlOperationGroup:
    def __init__(
        self,
        *,
        operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeApiProductGraphqlOperationGroupOperationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operation_config_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operation_configs: operation_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_configs ApigeeApiProduct#operation_configs}
        :param operation_config_type: Flag that specifes whether the configuration is for Apigee API proxy or a remote service. Valid values include proxy or remoteservice. Defaults to proxy. Set to proxy when Apigee API proxies are associated with the API product. Set to remoteservice when non-Apigee proxies like Istio-Envoy are associated with the API product. Possible values: ["proxy", "remoteservice"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_config_type ApigeeApiProduct#operation_config_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__936a1dceac7b48558ec2c38069d20dc17c9ead77276b3100598007b32c10b4f3)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductGraphqlOperationGroupOperationConfigs"]]]:
        '''operation_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_configs ApigeeApiProduct#operation_configs}
        '''
        result = self._values.get("operation_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductGraphqlOperationGroupOperationConfigs"]]], result)

    @builtins.property
    def operation_config_type(self) -> typing.Optional[builtins.str]:
        '''Flag that specifes whether the configuration is for Apigee API proxy or a remote service.

        Valid values include proxy or remoteservice. Defaults to proxy. Set to proxy when Apigee API proxies are associated with the API product. Set to remoteservice when non-Apigee proxies like Istio-Envoy are associated with the API product. Possible values: ["proxy", "remoteservice"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_config_type ApigeeApiProduct#operation_config_type}
        '''
        result = self._values.get("operation_config_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductGraphqlOperationGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGraphqlOperationGroupOperationConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "api_source": "apiSource",
        "attributes": "attributes",
        "operations": "operations",
        "quota": "quota",
    },
)
class ApigeeApiProductGraphqlOperationGroupOperationConfigs:
    def __init__(
        self,
        *,
        api_source: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        quota: typing.Optional[typing.Union["ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param api_source: Required. Name of the API proxy endpoint or remote service with which the GraphQL operation and quota are associated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#api_source ApigeeApiProduct#api_source}
        :param attributes: attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#attributes ApigeeApiProduct#attributes}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operations ApigeeApiProduct#operations}
        :param quota: quota block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota ApigeeApiProduct#quota}
        '''
        if isinstance(quota, dict):
            quota = ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota(**quota)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd41f2aad16e0416bc5d294e091e1fa3c9fdca1b15b6560514b92301bc1e3b2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#api_source ApigeeApiProduct#api_source}
        '''
        result = self._values.get("api_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes"]]]:
        '''attributes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#attributes ApigeeApiProduct#attributes}
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes"]]], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operations ApigeeApiProduct#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations"]]], result)

    @builtins.property
    def quota(
        self,
    ) -> typing.Optional["ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota"]:
        '''quota block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota ApigeeApiProduct#quota}
        '''
        result = self._values.get("quota")
        return typing.cast(typing.Optional["ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductGraphqlOperationGroupOperationConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Key of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#name ApigeeApiProduct#name}
        :param value: Value of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#value ApigeeApiProduct#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6e04f9876bfbe81a6af66d8a8ea6a0f715b7aab2265ee801267bb94700833d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#name ApigeeApiProduct#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#value ApigeeApiProduct#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__056205aa8090c2350ab44a887d93c16c4ea198fbc50a24bc347b4e5c0515b9ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13b63a351e947f0ad6165e9fb4d644144de78e880a1fc46cc3b94cc909e330f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13405e28c0cda98bb24873d16894b86ff63e331676abe896c691152bd7ab2b87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80ed97afdfeed43f645b1a06c8a10ec1d439c26b89dec77554f270dd2484c82a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02eb632defd58096edb44b2909231ab7f21d4a956091b559dd487d75bb6ff6e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bdd20fd66a475c98258026bf286727aa28fdcbe492f2cba3de6725b8c929ad2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7f1ee47bdbebdf747e2b9e6572076b0493bdb439f7b41c7f6bf401a81ce125a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__966c469d6d8fa8b86af330aa8296ee1e090e61ad72161b7a195436ce3d2a86a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b698d7475776ec2240223391c415de99ca41cf21ebc6dd7313f84c382e6b1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab5748d9a24615fae534b5c2fd54673109d908b7a7ec9df3a17194ddf241446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeApiProductGraphqlOperationGroupOperationConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGraphqlOperationGroupOperationConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9222c31b95619127768e4cc6b4067d08ab5ebc76c0e3f1dfad7d4d1ee978a976)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigeeApiProductGraphqlOperationGroupOperationConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__875a6640f26f23ac97792a133ae56a0b53502b327433cb2e1ca74b8249c47bd6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigeeApiProductGraphqlOperationGroupOperationConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed578be78884ade4eb2b01b902fb75c04d484305af46b965476a6eb46b3e3fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1448f7225e2724541089d1ea96ccd150301eb16db9c6de4453eb56785a476f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eacd67aea2d9db4462f92b33f5d4d47bc506f0e45be758bc527f60be8f9d95ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d872d48a84c4f3d8af5639e660cd7281a0c689b413010d0919c0b0a060dfd8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations",
    jsii_struct_bases=[],
    name_mapping={"operation": "operation", "operation_types": "operationTypes"},
)
class ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations:
    def __init__(
        self,
        *,
        operation: typing.Optional[builtins.str] = None,
        operation_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param operation: GraphQL operation name. The name and operation type will be used to apply quotas. If no name is specified, the quota will be applied to all GraphQL operations irrespective of their operation names in the payload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation ApigeeApiProduct#operation}
        :param operation_types: Required. GraphQL operation types. Valid values include query or mutation. Note: Apigee does not currently support subscription types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_types ApigeeApiProduct#operation_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a39200f71531fd8b55b92b5e28809318f1df9f2ff24223acd502bd3ad6abf46)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation ApigeeApiProduct#operation}
        '''
        result = self._values.get("operation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operation_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Required. GraphQL operation types. Valid values include query or mutation. Note: Apigee does not currently support subscription types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_types ApigeeApiProduct#operation_types}
        '''
        result = self._values.get("operation_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1b8a68119223723f75449da5197dac471bea5ef58df37a112ee53b48c7dcd53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbfe1f1b47d2543a6ab1188f0330fef663facc829471681e9c9f3177dea38f08)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e99197b411a8bea206b47e7255bdc3e12b2d9eeb817cea16419b0e5d47166cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__819a90e7c2b13fbafef1fbae70f9ab7cd02588d44f923d3c5a3e48add3a77314)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e07fb6bf0d9969882e3fd91766defd68e7367b7ef84aa88234b97e168b9f721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4463a4ced1221c252a9b8db787eef5d95f122fdb3eae0e9c42c1a9daab8d6877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9038e6cf7c19d7ddcaa80abf412d38e7b86c0b8437cc6a44ecf062cdb1608117)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48ce91a5a54704417cc444187f62f1c1ccf8b1404711fe23fa8b588d31fd959d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operationTypes")
    def operation_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "operationTypes"))

    @operation_types.setter
    def operation_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d05cca40fe8bbd4c7d5e2fc25b94b2cf103a114b92298b427a589e559b1afd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da81e8648b1843f49d215092ac1045bc75e32e299ed68b1795ae4e8349b04268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeApiProductGraphqlOperationGroupOperationConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGraphqlOperationGroupOperationConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5a8aa92a12d16ba62f9e9e2723b7980e56e1a0e4b36ff7a8fc81c9ebfc7df96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAttributes")
    def put_attributes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49557b437c98d27f1ad6fb3967944d4e42926e122aadbc8b6592f78dc49db76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAttributes", [value]))

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e29175a5ba0abe9f024001f5d6b26138368af6946f8d424e82caf120118170d)
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
        :param interval: Required. Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#interval ApigeeApiProduct#interval}
        :param limit: Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#limit ApigeeApiProduct#limit}
        :param time_unit: Time unit defined for the interval. Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#time_unit ApigeeApiProduct#time_unit}
        '''
        value = ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota(
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
    ) -> ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesList:
        return typing.cast(ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesList, jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(
        self,
    ) -> ApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsList:
        return typing.cast(ApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="quota")
    def quota(
        self,
    ) -> "ApigeeApiProductGraphqlOperationGroupOperationConfigsQuotaOutputReference":
        return typing.cast("ApigeeApiProductGraphqlOperationGroupOperationConfigsQuotaOutputReference", jsii.get(self, "quota"))

    @builtins.property
    @jsii.member(jsii_name="apiSourceInput")
    def api_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]]], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaInput")
    def quota_input(
        self,
    ) -> typing.Optional["ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota"]:
        return typing.cast(typing.Optional["ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota"], jsii.get(self, "quotaInput"))

    @builtins.property
    @jsii.member(jsii_name="apiSource")
    def api_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiSource"))

    @api_source.setter
    def api_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1fad066bd6ca994c2421a9aa08066fa0462159724e6c1969aa64eabcf862c71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGraphqlOperationGroupOperationConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGraphqlOperationGroupOperationConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGraphqlOperationGroupOperationConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed34ee0ff08b4d830ddfdf55b1f19db2a3237ef54a6bc00f72a95e1c5a6e02e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "limit": "limit", "time_unit": "timeUnit"},
)
class ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota:
    def __init__(
        self,
        *,
        interval: typing.Optional[builtins.str] = None,
        limit: typing.Optional[builtins.str] = None,
        time_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interval: Required. Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#interval ApigeeApiProduct#interval}
        :param limit: Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#limit ApigeeApiProduct#limit}
        :param time_unit: Time unit defined for the interval. Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#time_unit ApigeeApiProduct#time_unit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c9f898f73550f91a2148c4c3005e8d3f3e0fb8da5a467bfbc60cea5fdb6099a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#interval ApigeeApiProduct#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit(self) -> typing.Optional[builtins.str]:
        '''Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#limit ApigeeApiProduct#limit}
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_unit(self) -> typing.Optional[builtins.str]:
        '''Time unit defined for the interval.

        Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#time_unit ApigeeApiProduct#time_unit}
        '''
        result = self._values.get("time_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeApiProductGraphqlOperationGroupOperationConfigsQuotaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGraphqlOperationGroupOperationConfigsQuotaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5178f44ff6095a04a871112fc463aeec21717e6dd5a438e6020b4e13912c61d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd4a5e28489b9ad01461674de5fc5b40b552985318c54819a55b10ec5ce51f88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31cbbae1760ed655567a37a8e9ec86251ebde9e449c493541b1ece7910695e87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeUnit")
    def time_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeUnit"))

    @time_unit.setter
    def time_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4d1dc0d845d3cb36a5356e3ca3cdc46799cbbcc4f9b01fadfcd45c6c496214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota]:
        return typing.cast(typing.Optional[ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d788dd05ce24d3e482bd10e20f9fb898f446bbf3a57122cd45303b64067270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeApiProductGraphqlOperationGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGraphqlOperationGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2669f51c450559c4d63f039af6de08fa46002eb671f1a41650692304a1b76102)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperationConfigs")
    def put_operation_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductGraphqlOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a7c8e4f51ee55409c09d5e4a8146b1445906232cdd021730a611596320b80e)
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
    ) -> ApigeeApiProductGraphqlOperationGroupOperationConfigsList:
        return typing.cast(ApigeeApiProductGraphqlOperationGroupOperationConfigsList, jsii.get(self, "operationConfigs"))

    @builtins.property
    @jsii.member(jsii_name="operationConfigsInput")
    def operation_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigs]]], jsii.get(self, "operationConfigsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__787a5ae7a476f9b21a088051b6b2f3c953d3884b6fc9b6511834d0d614d09cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationConfigType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigeeApiProductGraphqlOperationGroup]:
        return typing.cast(typing.Optional[ApigeeApiProductGraphqlOperationGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeApiProductGraphqlOperationGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc168cfa8a77125df368ff08eb66e0637e1e56eba35360d059ebe184e4b3c6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGrpcOperationGroup",
    jsii_struct_bases=[],
    name_mapping={"operation_configs": "operationConfigs"},
)
class ApigeeApiProductGrpcOperationGroup:
    def __init__(
        self,
        *,
        operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeApiProductGrpcOperationGroupOperationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param operation_configs: operation_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_configs ApigeeApiProduct#operation_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec100a1e8f2a89dac2a24026ae8910e5869080d2674afbf1dd76a6a0e7be8ac)
            check_type(argname="argument operation_configs", value=operation_configs, expected_type=type_hints["operation_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operation_configs is not None:
            self._values["operation_configs"] = operation_configs

    @builtins.property
    def operation_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductGrpcOperationGroupOperationConfigs"]]]:
        '''operation_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_configs ApigeeApiProduct#operation_configs}
        '''
        result = self._values.get("operation_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductGrpcOperationGroupOperationConfigs"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductGrpcOperationGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGrpcOperationGroupOperationConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "api_source": "apiSource",
        "attributes": "attributes",
        "methods": "methods",
        "quota": "quota",
        "service": "service",
    },
)
class ApigeeApiProductGrpcOperationGroupOperationConfigs:
    def __init__(
        self,
        *,
        api_source: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        quota: typing.Optional[typing.Union["ApigeeApiProductGrpcOperationGroupOperationConfigsQuota", typing.Dict[builtins.str, typing.Any]]] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_source: Required. Name of the API proxy with which the gRPC operation and quota are associated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#api_source ApigeeApiProduct#api_source}
        :param attributes: attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#attributes ApigeeApiProduct#attributes}
        :param methods: List of unqualified gRPC method names for the proxy to which quota will be applied. If this field is empty, the Quota will apply to all operations on the gRPC service defined on the proxy. Example: Given a proxy that is configured to serve com.petstore.PetService, the methods com.petstore.PetService.ListPets and com.petstore.PetService.GetPet would be specified here as simply ["ListPets", "GetPet"]. Note: Currently, you can specify only a single GraphQLOperation. Specifying more than one will cause the operation to fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#methods ApigeeApiProduct#methods}
        :param quota: quota block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota ApigeeApiProduct#quota}
        :param service: Required. gRPC Service name associated to be associated with the API proxy, on which quota rules can be applied upon. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#service ApigeeApiProduct#service}
        '''
        if isinstance(quota, dict):
            quota = ApigeeApiProductGrpcOperationGroupOperationConfigsQuota(**quota)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a2c433f4ad5ea8e96c2b1df20f7cd8a92dc8369639b215460687e16954a479b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#api_source ApigeeApiProduct#api_source}
        '''
        result = self._values.get("api_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes"]]]:
        '''attributes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#attributes ApigeeApiProduct#attributes}
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes"]]], result)

    @builtins.property
    def methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of unqualified gRPC method names for the proxy to which quota will be applied.

        If this field is empty, the Quota will apply to all operations on the gRPC service defined on the proxy.

        Example: Given a proxy that is configured to serve com.petstore.PetService, the methods com.petstore.PetService.ListPets and com.petstore.PetService.GetPet would be specified here as simply ["ListPets", "GetPet"].

        Note: Currently, you can specify only a single GraphQLOperation. Specifying more than one will cause the operation to fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#methods ApigeeApiProduct#methods}
        '''
        result = self._values.get("methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def quota(
        self,
    ) -> typing.Optional["ApigeeApiProductGrpcOperationGroupOperationConfigsQuota"]:
        '''quota block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota ApigeeApiProduct#quota}
        '''
        result = self._values.get("quota")
        return typing.cast(typing.Optional["ApigeeApiProductGrpcOperationGroupOperationConfigsQuota"], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Required.

        gRPC Service name associated to be associated with the API proxy, on which quota rules can be applied upon.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#service ApigeeApiProduct#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductGrpcOperationGroupOperationConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Key of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#name ApigeeApiProduct#name}
        :param value: Value of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#value ApigeeApiProduct#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__601bf900e21075f8141cedd9003f5c0b47a88cf4f7c11227b0920844eb501623)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#name ApigeeApiProduct#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#value ApigeeApiProduct#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeApiProductGrpcOperationGroupOperationConfigsAttributesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGrpcOperationGroupOperationConfigsAttributesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2afb9449327e271d962164d698a94ac5406339fb46a0c1e76ac238ac8654270d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigeeApiProductGrpcOperationGroupOperationConfigsAttributesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__655787b549237b4aa98f835ba09ddcac10fe5498d7f6d513226de7450ab6e14b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigeeApiProductGrpcOperationGroupOperationConfigsAttributesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7b65dd3b5d25f5578df41282ad768b6e07607731b9e2fb5b17af04d9677a9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__782758d40d5a448639542228f2e0e117b501cbbb3992d0d27887e33369f82384)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5eed00447dea24d9ff9e0498573132fe6d509ef3aef674b37252b3c2ce72ae29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf49f2dee3d9a24145c1b00a83cc7c49475abd86728e0d0ecd03d39fb1fd641a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeApiProductGrpcOperationGroupOperationConfigsAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGrpcOperationGroupOperationConfigsAttributesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ac5791323ea0849613e2a3495aacc1cf8e1791b68fbbee1fc71ffd60bf0c54a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77d891ac2aa8ed44d187758f6738e88e3799dbd9e2e2db51d258529d043bd450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14acf5680e8d2e5b03e4c35132e51f63120768d46b8836037a05bb18069a4144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1ce17d5f3937df746d76420c64b8aef7965a3c00a8fbc829a5642c998797ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeApiProductGrpcOperationGroupOperationConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGrpcOperationGroupOperationConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e8bc42e40dc6e7f38869f36610781889ae9174c9bdfd6411cb8bdc652bdacfe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigeeApiProductGrpcOperationGroupOperationConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1add584600c76fef31cd6a09cdffe500e38b038afcd86f92acd1b291250c1d8c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigeeApiProductGrpcOperationGroupOperationConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d245048b37c162f28bc104244d6f87da3d65802b346da2d6c98c2cf8d2dd9531)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50aab66c49c8fc3997e41044dcd4c33dd9fda01cd55fac8db8ec6622304ba797)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ed4c1bd876627455c2114f6c3e26e24880f527ac7e925c18de20e3b0ce0bec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGrpcOperationGroupOperationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGrpcOperationGroupOperationConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGrpcOperationGroupOperationConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a40cd5d6afd79e2a78865cbf856a4a529735d0d012acdc1d7418ddbd8cbeca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeApiProductGrpcOperationGroupOperationConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGrpcOperationGroupOperationConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__647327c943999326dfe29b1b82f113d6a476fce4ac56a4e9bd8f0423fbeaad27)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAttributes")
    def put_attributes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9667e3ac69ad2e85bcf70642ae6d2678290f1cc3793749e3c84f449228738d2b)
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
        :param interval: Required. Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#interval ApigeeApiProduct#interval}
        :param limit: Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#limit ApigeeApiProduct#limit}
        :param time_unit: Time unit defined for the interval. Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#time_unit ApigeeApiProduct#time_unit}
        '''
        value = ApigeeApiProductGrpcOperationGroupOperationConfigsQuota(
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
    ) -> ApigeeApiProductGrpcOperationGroupOperationConfigsAttributesList:
        return typing.cast(ApigeeApiProductGrpcOperationGroupOperationConfigsAttributesList, jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="quota")
    def quota(
        self,
    ) -> "ApigeeApiProductGrpcOperationGroupOperationConfigsQuotaOutputReference":
        return typing.cast("ApigeeApiProductGrpcOperationGroupOperationConfigsQuotaOutputReference", jsii.get(self, "quota"))

    @builtins.property
    @jsii.member(jsii_name="apiSourceInput")
    def api_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]]], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="methodsInput")
    def methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "methodsInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaInput")
    def quota_input(
        self,
    ) -> typing.Optional["ApigeeApiProductGrpcOperationGroupOperationConfigsQuota"]:
        return typing.cast(typing.Optional["ApigeeApiProductGrpcOperationGroupOperationConfigsQuota"], jsii.get(self, "quotaInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f6a0d460e54d898d40c1618805e401e82ce51fdf1b81e1fe61a49c5c7efa9718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="methods")
    def methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "methods"))

    @methods.setter
    def methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9aa5713e405b411d0c0a00bed03332c9ee4aab52c19bf2453e0f58dcad7dd7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cefb94f4a7fb52db7b36851d7db0725c4faafd9a38cc5c0d41a300df995f6184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGrpcOperationGroupOperationConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGrpcOperationGroupOperationConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGrpcOperationGroupOperationConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc1c5548f046ffb41e75fab3f12e4da09a8916c63eb822bf8d355bc4b669b3df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGrpcOperationGroupOperationConfigsQuota",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "limit": "limit", "time_unit": "timeUnit"},
)
class ApigeeApiProductGrpcOperationGroupOperationConfigsQuota:
    def __init__(
        self,
        *,
        interval: typing.Optional[builtins.str] = None,
        limit: typing.Optional[builtins.str] = None,
        time_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interval: Required. Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#interval ApigeeApiProduct#interval}
        :param limit: Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#limit ApigeeApiProduct#limit}
        :param time_unit: Time unit defined for the interval. Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#time_unit ApigeeApiProduct#time_unit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5558828c844edcf5368a2cb72168af726e3b6b838a92d8243acf854e62eeb702)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#interval ApigeeApiProduct#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit(self) -> typing.Optional[builtins.str]:
        '''Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#limit ApigeeApiProduct#limit}
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_unit(self) -> typing.Optional[builtins.str]:
        '''Time unit defined for the interval.

        Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#time_unit ApigeeApiProduct#time_unit}
        '''
        result = self._values.get("time_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductGrpcOperationGroupOperationConfigsQuota(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeApiProductGrpcOperationGroupOperationConfigsQuotaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGrpcOperationGroupOperationConfigsQuotaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4cf774e457892f77b9e624e96d7a15511fd5041285fff4952c6a7b55c727360)
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
            type_hints = typing.get_type_hints(_typecheckingstub__214de5a83a973e8fac88ec13f3a38c5764836ea9f00e953a9d2912dc99ff89b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f272107ff8179896cf102efdd67a2b0452c061363739a77d64c073fdeb8de67a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeUnit")
    def time_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeUnit"))

    @time_unit.setter
    def time_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c992f79f829cf244f03b5f0df2c0ecada78849a7ad8e3e48b371dc4bb1f2d2f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApigeeApiProductGrpcOperationGroupOperationConfigsQuota]:
        return typing.cast(typing.Optional[ApigeeApiProductGrpcOperationGroupOperationConfigsQuota], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeApiProductGrpcOperationGroupOperationConfigsQuota],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0440a3f40d8eba462573ea301b16ba2bbf6534a6f3879980bdee71b509677c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeApiProductGrpcOperationGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductGrpcOperationGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c82075a25ddc718d868d4772259067f2db2f9d452c5e3a7c5ae73cfcbae3edfe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperationConfigs")
    def put_operation_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductGrpcOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d7e3a4e70ff0d676fbf783de0517f393efcd14e9e95a0f3868019cfa425f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperationConfigs", [value]))

    @jsii.member(jsii_name="resetOperationConfigs")
    def reset_operation_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationConfigs", []))

    @builtins.property
    @jsii.member(jsii_name="operationConfigs")
    def operation_configs(
        self,
    ) -> ApigeeApiProductGrpcOperationGroupOperationConfigsList:
        return typing.cast(ApigeeApiProductGrpcOperationGroupOperationConfigsList, jsii.get(self, "operationConfigs"))

    @builtins.property
    @jsii.member(jsii_name="operationConfigsInput")
    def operation_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGrpcOperationGroupOperationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGrpcOperationGroupOperationConfigs]]], jsii.get(self, "operationConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigeeApiProductGrpcOperationGroup]:
        return typing.cast(typing.Optional[ApigeeApiProductGrpcOperationGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeApiProductGrpcOperationGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3917c97f4fa79147575e4a05d835a5bc7d5aba193021824ad361911a22ee811f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductOperationGroup",
    jsii_struct_bases=[],
    name_mapping={
        "operation_configs": "operationConfigs",
        "operation_config_type": "operationConfigType",
    },
)
class ApigeeApiProductOperationGroup:
    def __init__(
        self,
        *,
        operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeApiProductOperationGroupOperationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operation_config_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operation_configs: operation_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_configs ApigeeApiProduct#operation_configs}
        :param operation_config_type: Flag that specifes whether the configuration is for Apigee API proxy or a remote service. Valid values include proxy or remoteservice. Defaults to proxy. Set to proxy when Apigee API proxies are associated with the API product. Set to remoteservice when non-Apigee proxies like Istio-Envoy are associated with the API product. Possible values: ["proxy", "remoteservice"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_config_type ApigeeApiProduct#operation_config_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26eb1ee29407550ff4f2557b537d7281fae97cf477ea41439692dcf4bb5e2493)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductOperationGroupOperationConfigs"]]]:
        '''operation_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_configs ApigeeApiProduct#operation_configs}
        '''
        result = self._values.get("operation_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductOperationGroupOperationConfigs"]]], result)

    @builtins.property
    def operation_config_type(self) -> typing.Optional[builtins.str]:
        '''Flag that specifes whether the configuration is for Apigee API proxy or a remote service.

        Valid values include proxy or remoteservice. Defaults to proxy. Set to proxy when Apigee API proxies are associated with the API product. Set to remoteservice when non-Apigee proxies like Istio-Envoy are associated with the API product. Possible values: ["proxy", "remoteservice"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operation_config_type ApigeeApiProduct#operation_config_type}
        '''
        result = self._values.get("operation_config_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductOperationGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductOperationGroupOperationConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "api_source": "apiSource",
        "attributes": "attributes",
        "operations": "operations",
        "quota": "quota",
    },
)
class ApigeeApiProductOperationGroupOperationConfigs:
    def __init__(
        self,
        *,
        api_source: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeApiProductOperationGroupOperationConfigsAttributes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeApiProductOperationGroupOperationConfigsOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        quota: typing.Optional[typing.Union["ApigeeApiProductOperationGroupOperationConfigsQuota", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param api_source: Required. Name of the API proxy or remote service with which the resources, methods, and quota are associated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#api_source ApigeeApiProduct#api_source}
        :param attributes: attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#attributes ApigeeApiProduct#attributes}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operations ApigeeApiProduct#operations}
        :param quota: quota block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota ApigeeApiProduct#quota}
        '''
        if isinstance(quota, dict):
            quota = ApigeeApiProductOperationGroupOperationConfigsQuota(**quota)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5248ed6ae22745adb6639a72dc0271cdf33d91e16ff2b210b61d350c40e15f9e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#api_source ApigeeApiProduct#api_source}
        '''
        result = self._values.get("api_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductOperationGroupOperationConfigsAttributes"]]]:
        '''attributes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#attributes ApigeeApiProduct#attributes}
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductOperationGroupOperationConfigsAttributes"]]], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductOperationGroupOperationConfigsOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#operations ApigeeApiProduct#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeApiProductOperationGroupOperationConfigsOperations"]]], result)

    @builtins.property
    def quota(
        self,
    ) -> typing.Optional["ApigeeApiProductOperationGroupOperationConfigsQuota"]:
        '''quota block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#quota ApigeeApiProduct#quota}
        '''
        result = self._values.get("quota")
        return typing.cast(typing.Optional["ApigeeApiProductOperationGroupOperationConfigsQuota"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductOperationGroupOperationConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductOperationGroupOperationConfigsAttributes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ApigeeApiProductOperationGroupOperationConfigsAttributes:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Key of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#name ApigeeApiProduct#name}
        :param value: Value of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#value ApigeeApiProduct#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee0d3430197d6047b67b96b2cf7db554a25d048ad386fa494ceffcc698f5c8b1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#name ApigeeApiProduct#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#value ApigeeApiProduct#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductOperationGroupOperationConfigsAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeApiProductOperationGroupOperationConfigsAttributesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductOperationGroupOperationConfigsAttributesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db8c30419ff6f5c4fabee74da9d3aa977e86ca06c6ea6e4d6b78f87a3d018635)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigeeApiProductOperationGroupOperationConfigsAttributesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20134b6bded694cb1f54ca300b44585dc8aea3537956d893322602d4c8d20670)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigeeApiProductOperationGroupOperationConfigsAttributesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a29e1889d07b8d3c1020032a3ea7c41476ef0c56f23fba365e27faa27b6c7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4adc63497575f3ba14b550cee613ee69a8158e14e4e8691a57cfc55d1bd8f22d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54086698f65b314cb95d18c848d98d5780788cf7cd62fe575e2dde076fdb77f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigsAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigsAttributes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigsAttributes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08097196cb8e3a221e2282b0c07d9503ed8c726e404d23fb26c51130c3d64e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeApiProductOperationGroupOperationConfigsAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductOperationGroupOperationConfigsAttributesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e0e71919f7d2543739a1db3b0a9e7d139c0f5ad9fbaa5efad466e7c642c2966)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e56486c7ac75544cd32dd56f0785bc0f70e9897ab8f2b470a4212d97f66833d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa3d993bfc186ebcdf6bfd233c80b51322b05c5b2ad5cf590fe0169efd61ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductOperationGroupOperationConfigsAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductOperationGroupOperationConfigsAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductOperationGroupOperationConfigsAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab6bedf1f327bfe730eaa698f4c29ae9678c26731386665792a2ab036416130d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeApiProductOperationGroupOperationConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductOperationGroupOperationConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dc8071582ea615fc56b4d7d2ee2a61464b9c3c302c6944873f6fbf2119d2aaf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigeeApiProductOperationGroupOperationConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6831b751c136b60aba1fab6ae3f50964eb8e5210cf09146bb34a1f506ed9306b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigeeApiProductOperationGroupOperationConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe9a4621a2dad44564bd90b6a122b2c45eea34870f3c7503706cc0c7b70285e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ecc62b7c023a022dcac8f0d93e4c479f14cea4e763e627a8d9f303e4453bb46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09054ce24701c8a8beaaf4c60ac8114c35d3114c7addd7731b7191e44c71ed73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10e975ef5405dd33fc20576e4472ee6d85209d51dc8ea209a1102d90274405c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductOperationGroupOperationConfigsOperations",
    jsii_struct_bases=[],
    name_mapping={"methods": "methods", "resource": "resource"},
)
class ApigeeApiProductOperationGroupOperationConfigsOperations:
    def __init__(
        self,
        *,
        methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param methods: Methods refers to the REST verbs, when none specified, all verb types are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#methods ApigeeApiProduct#methods}
        :param resource: Required. REST resource path associated with the API proxy or remote service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#resource ApigeeApiProduct#resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82c5aaf235e8e1f05ba0bab1490b394ba6cf256faf89ac69132f6c87dc489c82)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#methods ApigeeApiProduct#methods}
        '''
        result = self._values.get("methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''Required. REST resource path associated with the API proxy or remote service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#resource ApigeeApiProduct#resource}
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductOperationGroupOperationConfigsOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeApiProductOperationGroupOperationConfigsOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductOperationGroupOperationConfigsOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bd4c23b02fe3cb5acc4ab7ff155ef5987466ba25af6182a1b691413db365947)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigeeApiProductOperationGroupOperationConfigsOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4776f8bf34274643dde9023ac8b335f2081efdaa1863ae8992505092f388c68c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigeeApiProductOperationGroupOperationConfigsOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ae523d47bfb4d29fa760c98a5641b869a44e0476339ceb9904cb7fbfb43291)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd10c862c668513ba36308a9ca689be144ee0cf6af1d09f86524655ebf3548fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f1cb64aca4950c7453780bf30ffe2e9320c62324ab6014de9005d897cba6327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigsOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigsOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigsOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2170efe0c7a621502e715ed8f7069a11d26fdd0f93c7e21fd9154c52cdb75998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeApiProductOperationGroupOperationConfigsOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductOperationGroupOperationConfigsOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b6558ca3cafe9c2a7ea7d94c461170bd9df03048dee9ca52f162eb0cafae788)
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
            type_hints = typing.get_type_hints(_typecheckingstub__292a389a71dd4ac17588a87ae6af241531fcbf9bc4aae8c3f78cd4fddb6730b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c32fd160a4dbed1aa135058dd7678bce60af7f8d7b1b290da6ded5a3241138)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductOperationGroupOperationConfigsOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductOperationGroupOperationConfigsOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductOperationGroupOperationConfigsOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ba728397a668f6b2ff04b6aa7179b2e1b56b2873d53da80c1b2cb88d83e719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeApiProductOperationGroupOperationConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductOperationGroupOperationConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d35c96c60ae54086ec925ad9d77f74bba7bc805de15768ee320742e3d3fc0ddc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAttributes")
    def put_attributes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5701139ee0aad43836dfe1beb2587a319308710318f73ddb77489f0d566cc2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAttributes", [value]))

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductOperationGroupOperationConfigsOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__163002afe8aeb6d2f748d46d650582f4fbba44543e920f71c49a14d27b6e003d)
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
        :param interval: Required. Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#interval ApigeeApiProduct#interval}
        :param limit: Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#limit ApigeeApiProduct#limit}
        :param time_unit: Time unit defined for the interval. Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#time_unit ApigeeApiProduct#time_unit}
        '''
        value = ApigeeApiProductOperationGroupOperationConfigsQuota(
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
    ) -> ApigeeApiProductOperationGroupOperationConfigsAttributesList:
        return typing.cast(ApigeeApiProductOperationGroupOperationConfigsAttributesList, jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(
        self,
    ) -> ApigeeApiProductOperationGroupOperationConfigsOperationsList:
        return typing.cast(ApigeeApiProductOperationGroupOperationConfigsOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="quota")
    def quota(
        self,
    ) -> "ApigeeApiProductOperationGroupOperationConfigsQuotaOutputReference":
        return typing.cast("ApigeeApiProductOperationGroupOperationConfigsQuotaOutputReference", jsii.get(self, "quota"))

    @builtins.property
    @jsii.member(jsii_name="apiSourceInput")
    def api_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigsAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigsAttributes]]], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigsOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigsOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaInput")
    def quota_input(
        self,
    ) -> typing.Optional["ApigeeApiProductOperationGroupOperationConfigsQuota"]:
        return typing.cast(typing.Optional["ApigeeApiProductOperationGroupOperationConfigsQuota"], jsii.get(self, "quotaInput"))

    @builtins.property
    @jsii.member(jsii_name="apiSource")
    def api_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiSource"))

    @api_source.setter
    def api_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ca74020039d95a75df41d5bbe8a8af8dd82c0749592d984ba374ca53ed8041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductOperationGroupOperationConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductOperationGroupOperationConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductOperationGroupOperationConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a1fd58d825abe17f11160c93240b5d057a410b715b6cc1cada293d12d0520f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductOperationGroupOperationConfigsQuota",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "limit": "limit", "time_unit": "timeUnit"},
)
class ApigeeApiProductOperationGroupOperationConfigsQuota:
    def __init__(
        self,
        *,
        interval: typing.Optional[builtins.str] = None,
        limit: typing.Optional[builtins.str] = None,
        time_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interval: Required. Time interval over which the number of request messages is calculated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#interval ApigeeApiProduct#interval}
        :param limit: Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#limit ApigeeApiProduct#limit}
        :param time_unit: Time unit defined for the interval. Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#time_unit ApigeeApiProduct#time_unit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c02f3fb00fa1dbf8e1723857cc084ce7232766790eb382170510ff14bb972fb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#interval ApigeeApiProduct#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit(self) -> typing.Optional[builtins.str]:
        '''Required. Upper limit allowed for the time interval and time unit specified. Requests exceeding this limit will be rejected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#limit ApigeeApiProduct#limit}
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_unit(self) -> typing.Optional[builtins.str]:
        '''Time unit defined for the interval.

        Valid values include second, minute, hour, day, month or year. If limit and interval are valid, the default value is hour; otherwise, the default is null.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#time_unit ApigeeApiProduct#time_unit}
        '''
        result = self._values.get("time_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductOperationGroupOperationConfigsQuota(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeApiProductOperationGroupOperationConfigsQuotaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductOperationGroupOperationConfigsQuotaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d724eb96c8f4869e21873553bc6990ace00962fb024d5ea4d7bd3662162a741d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__206abd9c744e7678a17ae76bb130c09fe9fe36f92204fa7e223610cde333b30a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74ca023a2d51b8659e24e6235c98bbfed8753df403665c3f5f10ed080bf282f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeUnit")
    def time_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeUnit"))

    @time_unit.setter
    def time_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299c769d64c9d1f7e746fdf627a299b6e1fd3fb5f1a51849efb8a2ae7ef6774a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApigeeApiProductOperationGroupOperationConfigsQuota]:
        return typing.cast(typing.Optional[ApigeeApiProductOperationGroupOperationConfigsQuota], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeApiProductOperationGroupOperationConfigsQuota],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be63cfff3170e2a1329c854f79de81747581512b752bdf51bdb820a88ed58c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeApiProductOperationGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductOperationGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1066b9d1294de1e99e9f7ebdc5cf7766803f96b9c1100f4ab0b268897d6706ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOperationConfigs")
    def put_operation_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6b4863813329a85a5938edbf46e24ec09f21d97b14d97d41ce090229cca11d8)
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
    def operation_configs(self) -> ApigeeApiProductOperationGroupOperationConfigsList:
        return typing.cast(ApigeeApiProductOperationGroupOperationConfigsList, jsii.get(self, "operationConfigs"))

    @builtins.property
    @jsii.member(jsii_name="operationConfigsInput")
    def operation_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigs]]], jsii.get(self, "operationConfigsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7e63e992dd05cc117cddac4b3b0703f6744d8359aa85ef646e959434cf1a202e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationConfigType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigeeApiProductOperationGroup]:
        return typing.cast(typing.Optional[ApigeeApiProductOperationGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeApiProductOperationGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cb35f2d4517ad6b4331358139e596af43c415f76d1095ca36c6e1f9277d47e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ApigeeApiProductTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#create ApigeeApiProduct#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#delete ApigeeApiProduct#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#update ApigeeApiProduct#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__290d6a86ce0df70f7f4a693a4c2570b98a95557457a9f52463ba8709f15fba1b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#create ApigeeApiProduct#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#delete ApigeeApiProduct#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/apigee_api_product#update ApigeeApiProduct#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeApiProductTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeApiProductTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeApiProduct.ApigeeApiProductTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ab6945228d3466f1e5fac4bf3dbb215f93a7df614dc227cdedd27462e38206e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fc6b79e6c47c9b9c6ec64f7a49cceec2d37c51b28aeaff84f415533a402a725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a880a1978b617b6a264e03f7e12e1e412384a3ad8f7665e3551fa3136e80c4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a8291be84e975b941510d299cd5d5529c7676cc86ec51dcbdfa19013e5ac1d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f99ca7eefc72b5e92dd1f4dcbc05a7e545d6d9df5711e9b6eb6f05aa7fa2b67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApigeeApiProduct",
    "ApigeeApiProductAttributes",
    "ApigeeApiProductAttributesList",
    "ApigeeApiProductAttributesOutputReference",
    "ApigeeApiProductConfig",
    "ApigeeApiProductGraphqlOperationGroup",
    "ApigeeApiProductGraphqlOperationGroupOperationConfigs",
    "ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes",
    "ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesList",
    "ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributesOutputReference",
    "ApigeeApiProductGraphqlOperationGroupOperationConfigsList",
    "ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations",
    "ApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsList",
    "ApigeeApiProductGraphqlOperationGroupOperationConfigsOperationsOutputReference",
    "ApigeeApiProductGraphqlOperationGroupOperationConfigsOutputReference",
    "ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota",
    "ApigeeApiProductGraphqlOperationGroupOperationConfigsQuotaOutputReference",
    "ApigeeApiProductGraphqlOperationGroupOutputReference",
    "ApigeeApiProductGrpcOperationGroup",
    "ApigeeApiProductGrpcOperationGroupOperationConfigs",
    "ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes",
    "ApigeeApiProductGrpcOperationGroupOperationConfigsAttributesList",
    "ApigeeApiProductGrpcOperationGroupOperationConfigsAttributesOutputReference",
    "ApigeeApiProductGrpcOperationGroupOperationConfigsList",
    "ApigeeApiProductGrpcOperationGroupOperationConfigsOutputReference",
    "ApigeeApiProductGrpcOperationGroupOperationConfigsQuota",
    "ApigeeApiProductGrpcOperationGroupOperationConfigsQuotaOutputReference",
    "ApigeeApiProductGrpcOperationGroupOutputReference",
    "ApigeeApiProductOperationGroup",
    "ApigeeApiProductOperationGroupOperationConfigs",
    "ApigeeApiProductOperationGroupOperationConfigsAttributes",
    "ApigeeApiProductOperationGroupOperationConfigsAttributesList",
    "ApigeeApiProductOperationGroupOperationConfigsAttributesOutputReference",
    "ApigeeApiProductOperationGroupOperationConfigsList",
    "ApigeeApiProductOperationGroupOperationConfigsOperations",
    "ApigeeApiProductOperationGroupOperationConfigsOperationsList",
    "ApigeeApiProductOperationGroupOperationConfigsOperationsOutputReference",
    "ApigeeApiProductOperationGroupOperationConfigsOutputReference",
    "ApigeeApiProductOperationGroupOperationConfigsQuota",
    "ApigeeApiProductOperationGroupOperationConfigsQuotaOutputReference",
    "ApigeeApiProductOperationGroupOutputReference",
    "ApigeeApiProductTimeouts",
    "ApigeeApiProductTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6017f2ef836cffb7756622ee18bc7a751d71525d2d6a456afced6a4f65a7d9e7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    name: builtins.str,
    org_id: builtins.str,
    api_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    approval_type: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductAttributes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    environments: typing.Optional[typing.Sequence[builtins.str]] = None,
    graphql_operation_group: typing.Optional[typing.Union[ApigeeApiProductGraphqlOperationGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_operation_group: typing.Optional[typing.Union[ApigeeApiProductGrpcOperationGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    operation_group: typing.Optional[typing.Union[ApigeeApiProductOperationGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
    quota: typing.Optional[builtins.str] = None,
    quota_counter_scope: typing.Optional[builtins.str] = None,
    quota_interval: typing.Optional[builtins.str] = None,
    quota_time_unit: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    space: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApigeeApiProductTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bcc8f7f8d7117a2b85f604d31211389200a7c549b5ea10827780fb2029712b9c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79702e0506ab5070baaab0dcdcf03c462e0316b5d05cb579bff5eb8008d608f0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductAttributes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a73089ff50086d83ebab1878798b0c50fa01a4ec70c44487975653a2d7efd4d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25fd7b4f6955a67fd6096599326b43604db58f645487f80a07f303c382c223f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18a98241211097f49b30842a8dd1ac4723941f7a2358c0e8a2ded6096a8c22c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b32a897237394e498329c3691bd7a329aca2526bda86ba99812ba6dc2a94e8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8999c9c7bcc61c0316da3da70f18b6e2a4f42232e1edab3214ce3e9d21ffafa6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff7d4c2a87bcc4b5c47c38997f5346924b80fada2cf3d91aa907cdf85cdbe88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a7a085f717dc7a16fa939ad65a43289578f5f3ddaf0d105e6b0d1da5f88d90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4acfafbfb881e7da63f5862ffc3bd4e3e81e23cd1ae0b4a24f751e889a9631d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b59b8fb15fb2cfe14916512a2ca84ffe425ea7496a2385cd250801ec60c80b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0800a65ba72d147ab0331e0d1e1c4832565c7d8cd41dfeeed3445caaf94cfe59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7c1b282c570e32b54e45cae3e1c35fbd5ca8308d4c21ccd6a843b6e2c41ec8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6035ba9a1606ba288fa3b58c5d302aee4e1190aabcd2c2ddab744edca5b1d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4fdda4a2381c6c3b80b489c3e84aeb17050e11c187b5edd8556c52a14f96a13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c6efbae0fa3632955b2eda586c2424c13e32ad9a11c4ad2e75f80caf8f3745(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109e98e14f4841657bf40a875664f2d6e396fc5458fbfb1e2138b22aceca43a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467c0062a6e51f011a34630f9cbc45299cb006d4d0f748ce4497cb5403750213(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d72f76c50ddbf685a33609badeef751bd4ea26d10d50e8b7a55d514998bbe8eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__928a3ec9bbdd76f4e40342cc61b848e3eab0cbf1ae4880de47d8783f21aa454c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6071175010546a31d2420a67720a1bf36bb3be8d343ddcd0c50fda2cd1995e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376e62e854f96837dedbe3ce27778827f67b4b457b304ca4819bdf93d9aa32fd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a14c8682a5a6e5f04c670314d8c13c2c6671bc0d0ff130d4df7b687570171b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9bcf3ce9017729c2f4200fd8c1a48d22cb9d67335dba08127a70e1bf8898ec1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductAttributes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242f551e17faa9a3a97357870b2c97183eb49a6c94565a16f27ec7f220d34090(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84f26c11e14ec9975224b66353b5dba7a5b7e7ef81f3ef9accde1a48cc016c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83213f33c1c7c89814c62ae1378f859c667a3bf1d137517df90b0dc47c355912(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0630fb2b6175f8239a9256364ac90022d1f4996362dd268720476c03169c5f83(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073dc733d0d05b808d75d23bc661bc8c187d4c00fe992c0f62bb6274974d55d6(
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
    attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductAttributes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    environments: typing.Optional[typing.Sequence[builtins.str]] = None,
    graphql_operation_group: typing.Optional[typing.Union[ApigeeApiProductGraphqlOperationGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_operation_group: typing.Optional[typing.Union[ApigeeApiProductGrpcOperationGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    operation_group: typing.Optional[typing.Union[ApigeeApiProductOperationGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
    quota: typing.Optional[builtins.str] = None,
    quota_counter_scope: typing.Optional[builtins.str] = None,
    quota_interval: typing.Optional[builtins.str] = None,
    quota_time_unit: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    space: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApigeeApiProductTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936a1dceac7b48558ec2c38069d20dc17c9ead77276b3100598007b32c10b4f3(
    *,
    operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductGraphqlOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operation_config_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd41f2aad16e0416bc5d294e091e1fa3c9fdca1b15b6560514b92301bc1e3b2(
    *,
    api_source: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    quota: typing.Optional[typing.Union[ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6e04f9876bfbe81a6af66d8a8ea6a0f715b7aab2265ee801267bb94700833d(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056205aa8090c2350ab44a887d93c16c4ea198fbc50a24bc347b4e5c0515b9ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13b63a351e947f0ad6165e9fb4d644144de78e880a1fc46cc3b94cc909e330f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13405e28c0cda98bb24873d16894b86ff63e331676abe896c691152bd7ab2b87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ed97afdfeed43f645b1a06c8a10ec1d439c26b89dec77554f270dd2484c82a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02eb632defd58096edb44b2909231ab7f21d4a956091b559dd487d75bb6ff6e7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bdd20fd66a475c98258026bf286727aa28fdcbe492f2cba3de6725b8c929ad2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f1ee47bdbebdf747e2b9e6572076b0493bdb439f7b41c7f6bf401a81ce125a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966c469d6d8fa8b86af330aa8296ee1e090e61ad72161b7a195436ce3d2a86a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b698d7475776ec2240223391c415de99ca41cf21ebc6dd7313f84c382e6b1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab5748d9a24615fae534b5c2fd54673109d908b7a7ec9df3a17194ddf241446(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9222c31b95619127768e4cc6b4067d08ab5ebc76c0e3f1dfad7d4d1ee978a976(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__875a6640f26f23ac97792a133ae56a0b53502b327433cb2e1ca74b8249c47bd6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed578be78884ade4eb2b01b902fb75c04d484305af46b965476a6eb46b3e3fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1448f7225e2724541089d1ea96ccd150301eb16db9c6de4453eb56785a476f4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eacd67aea2d9db4462f92b33f5d4d47bc506f0e45be758bc527f60be8f9d95ff(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d872d48a84c4f3d8af5639e660cd7281a0c689b413010d0919c0b0a060dfd8d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a39200f71531fd8b55b92b5e28809318f1df9f2ff24223acd502bd3ad6abf46(
    *,
    operation: typing.Optional[builtins.str] = None,
    operation_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b8a68119223723f75449da5197dac471bea5ef58df37a112ee53b48c7dcd53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbfe1f1b47d2543a6ab1188f0330fef663facc829471681e9c9f3177dea38f08(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e99197b411a8bea206b47e7255bdc3e12b2d9eeb817cea16419b0e5d47166cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819a90e7c2b13fbafef1fbae70f9ab7cd02588d44f923d3c5a3e48add3a77314(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e07fb6bf0d9969882e3fd91766defd68e7367b7ef84aa88234b97e168b9f721(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4463a4ced1221c252a9b8db787eef5d95f122fdb3eae0e9c42c1a9daab8d6877(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9038e6cf7c19d7ddcaa80abf412d38e7b86c0b8437cc6a44ecf062cdb1608117(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ce91a5a54704417cc444187f62f1c1ccf8b1404711fe23fa8b588d31fd959d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d05cca40fe8bbd4c7d5e2fc25b94b2cf103a114b92298b427a589e559b1afd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da81e8648b1843f49d215092ac1045bc75e32e299ed68b1795ae4e8349b04268(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a8aa92a12d16ba62f9e9e2723b7980e56e1a0e4b36ff7a8fc81c9ebfc7df96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49557b437c98d27f1ad6fb3967944d4e42926e122aadbc8b6592f78dc49db76(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductGraphqlOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e29175a5ba0abe9f024001f5d6b26138368af6946f8d424e82caf120118170d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductGraphqlOperationGroupOperationConfigsOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1fad066bd6ca994c2421a9aa08066fa0462159724e6c1969aa64eabcf862c71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed34ee0ff08b4d830ddfdf55b1f19db2a3237ef54a6bc00f72a95e1c5a6e02e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGraphqlOperationGroupOperationConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c9f898f73550f91a2148c4c3005e8d3f3e0fb8da5a467bfbc60cea5fdb6099a(
    *,
    interval: typing.Optional[builtins.str] = None,
    limit: typing.Optional[builtins.str] = None,
    time_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5178f44ff6095a04a871112fc463aeec21717e6dd5a438e6020b4e13912c61d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd4a5e28489b9ad01461674de5fc5b40b552985318c54819a55b10ec5ce51f88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31cbbae1760ed655567a37a8e9ec86251ebde9e449c493541b1ece7910695e87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4d1dc0d845d3cb36a5356e3ca3cdc46799cbbcc4f9b01fadfcd45c6c496214(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d788dd05ce24d3e482bd10e20f9fb898f446bbf3a57122cd45303b64067270(
    value: typing.Optional[ApigeeApiProductGraphqlOperationGroupOperationConfigsQuota],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2669f51c450559c4d63f039af6de08fa46002eb671f1a41650692304a1b76102(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a7c8e4f51ee55409c09d5e4a8146b1445906232cdd021730a611596320b80e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductGraphqlOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787a5ae7a476f9b21a088051b6b2f3c953d3884b6fc9b6511834d0d614d09cb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc168cfa8a77125df368ff08eb66e0637e1e56eba35360d059ebe184e4b3c6f(
    value: typing.Optional[ApigeeApiProductGraphqlOperationGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec100a1e8f2a89dac2a24026ae8910e5869080d2674afbf1dd76a6a0e7be8ac(
    *,
    operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductGrpcOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2c433f4ad5ea8e96c2b1df20f7cd8a92dc8369639b215460687e16954a479b(
    *,
    api_source: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    quota: typing.Optional[typing.Union[ApigeeApiProductGrpcOperationGroupOperationConfigsQuota, typing.Dict[builtins.str, typing.Any]]] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601bf900e21075f8141cedd9003f5c0b47a88cf4f7c11227b0920844eb501623(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afb9449327e271d962164d698a94ac5406339fb46a0c1e76ac238ac8654270d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655787b549237b4aa98f835ba09ddcac10fe5498d7f6d513226de7450ab6e14b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7b65dd3b5d25f5578df41282ad768b6e07607731b9e2fb5b17af04d9677a9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782758d40d5a448639542228f2e0e117b501cbbb3992d0d27887e33369f82384(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eed00447dea24d9ff9e0498573132fe6d509ef3aef674b37252b3c2ce72ae29(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf49f2dee3d9a24145c1b00a83cc7c49475abd86728e0d0ecd03d39fb1fd641a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac5791323ea0849613e2a3495aacc1cf8e1791b68fbbee1fc71ffd60bf0c54a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d891ac2aa8ed44d187758f6738e88e3799dbd9e2e2db51d258529d043bd450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14acf5680e8d2e5b03e4c35132e51f63120768d46b8836037a05bb18069a4144(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1ce17d5f3937df746d76420c64b8aef7965a3c00a8fbc829a5642c998797ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e8bc42e40dc6e7f38869f36610781889ae9174c9bdfd6411cb8bdc652bdacfe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1add584600c76fef31cd6a09cdffe500e38b038afcd86f92acd1b291250c1d8c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d245048b37c162f28bc104244d6f87da3d65802b346da2d6c98c2cf8d2dd9531(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50aab66c49c8fc3997e41044dcd4c33dd9fda01cd55fac8db8ec6622304ba797(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed4c1bd876627455c2114f6c3e26e24880f527ac7e925c18de20e3b0ce0bec9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a40cd5d6afd79e2a78865cbf856a4a529735d0d012acdc1d7418ddbd8cbeca2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductGrpcOperationGroupOperationConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647327c943999326dfe29b1b82f113d6a476fce4ac56a4e9bd8f0423fbeaad27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9667e3ac69ad2e85bcf70642ae6d2678290f1cc3793749e3c84f449228738d2b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductGrpcOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a0d460e54d898d40c1618805e401e82ce51fdf1b81e1fe61a49c5c7efa9718(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9aa5713e405b411d0c0a00bed03332c9ee4aab52c19bf2453e0f58dcad7dd7a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cefb94f4a7fb52db7b36851d7db0725c4faafd9a38cc5c0d41a300df995f6184(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1c5548f046ffb41e75fab3f12e4da09a8916c63eb822bf8d355bc4b669b3df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductGrpcOperationGroupOperationConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5558828c844edcf5368a2cb72168af726e3b6b838a92d8243acf854e62eeb702(
    *,
    interval: typing.Optional[builtins.str] = None,
    limit: typing.Optional[builtins.str] = None,
    time_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4cf774e457892f77b9e624e96d7a15511fd5041285fff4952c6a7b55c727360(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214de5a83a973e8fac88ec13f3a38c5764836ea9f00e953a9d2912dc99ff89b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f272107ff8179896cf102efdd67a2b0452c061363739a77d64c073fdeb8de67a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c992f79f829cf244f03b5f0df2c0ecada78849a7ad8e3e48b371dc4bb1f2d2f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0440a3f40d8eba462573ea301b16ba2bbf6534a6f3879980bdee71b509677c20(
    value: typing.Optional[ApigeeApiProductGrpcOperationGroupOperationConfigsQuota],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82075a25ddc718d868d4772259067f2db2f9d452c5e3a7c5ae73cfcbae3edfe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d7e3a4e70ff0d676fbf783de0517f393efcd14e9e95a0f3868019cfa425f7c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductGrpcOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3917c97f4fa79147575e4a05d835a5bc7d5aba193021824ad361911a22ee811f(
    value: typing.Optional[ApigeeApiProductGrpcOperationGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26eb1ee29407550ff4f2557b537d7281fae97cf477ea41439692dcf4bb5e2493(
    *,
    operation_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operation_config_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5248ed6ae22745adb6639a72dc0271cdf33d91e16ff2b210b61d350c40e15f9e(
    *,
    api_source: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductOperationGroupOperationConfigsOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    quota: typing.Optional[typing.Union[ApigeeApiProductOperationGroupOperationConfigsQuota, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0d3430197d6047b67b96b2cf7db554a25d048ad386fa494ceffcc698f5c8b1(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db8c30419ff6f5c4fabee74da9d3aa977e86ca06c6ea6e4d6b78f87a3d018635(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20134b6bded694cb1f54ca300b44585dc8aea3537956d893322602d4c8d20670(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a29e1889d07b8d3c1020032a3ea7c41476ef0c56f23fba365e27faa27b6c7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4adc63497575f3ba14b550cee613ee69a8158e14e4e8691a57cfc55d1bd8f22d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54086698f65b314cb95d18c848d98d5780788cf7cd62fe575e2dde076fdb77f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08097196cb8e3a221e2282b0c07d9503ed8c726e404d23fb26c51130c3d64e8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigsAttributes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0e71919f7d2543739a1db3b0a9e7d139c0f5ad9fbaa5efad466e7c642c2966(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e56486c7ac75544cd32dd56f0785bc0f70e9897ab8f2b470a4212d97f66833d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa3d993bfc186ebcdf6bfd233c80b51322b05c5b2ad5cf590fe0169efd61ee7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab6bedf1f327bfe730eaa698f4c29ae9678c26731386665792a2ab036416130d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductOperationGroupOperationConfigsAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc8071582ea615fc56b4d7d2ee2a61464b9c3c302c6944873f6fbf2119d2aaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6831b751c136b60aba1fab6ae3f50964eb8e5210cf09146bb34a1f506ed9306b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe9a4621a2dad44564bd90b6a122b2c45eea34870f3c7503706cc0c7b70285e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ecc62b7c023a022dcac8f0d93e4c479f14cea4e763e627a8d9f303e4453bb46(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09054ce24701c8a8beaaf4c60ac8114c35d3114c7addd7731b7191e44c71ed73(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10e975ef5405dd33fc20576e4472ee6d85209d51dc8ea209a1102d90274405c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c5aaf235e8e1f05ba0bab1490b394ba6cf256faf89ac69132f6c87dc489c82(
    *,
    methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd4c23b02fe3cb5acc4ab7ff155ef5987466ba25af6182a1b691413db365947(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4776f8bf34274643dde9023ac8b335f2081efdaa1863ae8992505092f388c68c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ae523d47bfb4d29fa760c98a5641b869a44e0476339ceb9904cb7fbfb43291(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd10c862c668513ba36308a9ca689be144ee0cf6af1d09f86524655ebf3548fd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f1cb64aca4950c7453780bf30ffe2e9320c62324ab6014de9005d897cba6327(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2170efe0c7a621502e715ed8f7069a11d26fdd0f93c7e21fd9154c52cdb75998(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeApiProductOperationGroupOperationConfigsOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6558ca3cafe9c2a7ea7d94c461170bd9df03048dee9ca52f162eb0cafae788(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292a389a71dd4ac17588a87ae6af241531fcbf9bc4aae8c3f78cd4fddb6730b5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c32fd160a4dbed1aa135058dd7678bce60af7f8d7b1b290da6ded5a3241138(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ba728397a668f6b2ff04b6aa7179b2e1b56b2873d53da80c1b2cb88d83e719(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductOperationGroupOperationConfigsOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35c96c60ae54086ec925ad9d77f74bba7bc805de15768ee320742e3d3fc0ddc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5701139ee0aad43836dfe1beb2587a319308710318f73ddb77489f0d566cc2f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductOperationGroupOperationConfigsAttributes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__163002afe8aeb6d2f748d46d650582f4fbba44543e920f71c49a14d27b6e003d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductOperationGroupOperationConfigsOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ca74020039d95a75df41d5bbe8a8af8dd82c0749592d984ba374ca53ed8041(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a1fd58d825abe17f11160c93240b5d057a410b715b6cc1cada293d12d0520f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductOperationGroupOperationConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c02f3fb00fa1dbf8e1723857cc084ce7232766790eb382170510ff14bb972fb(
    *,
    interval: typing.Optional[builtins.str] = None,
    limit: typing.Optional[builtins.str] = None,
    time_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d724eb96c8f4869e21873553bc6990ace00962fb024d5ea4d7bd3662162a741d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__206abd9c744e7678a17ae76bb130c09fe9fe36f92204fa7e223610cde333b30a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74ca023a2d51b8659e24e6235c98bbfed8753df403665c3f5f10ed080bf282f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299c769d64c9d1f7e746fdf627a299b6e1fd3fb5f1a51849efb8a2ae7ef6774a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be63cfff3170e2a1329c854f79de81747581512b752bdf51bdb820a88ed58c5(
    value: typing.Optional[ApigeeApiProductOperationGroupOperationConfigsQuota],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1066b9d1294de1e99e9f7ebdc5cf7766803f96b9c1100f4ab0b268897d6706ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b4863813329a85a5938edbf46e24ec09f21d97b14d97d41ce090229cca11d8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeApiProductOperationGroupOperationConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e63e992dd05cc117cddac4b3b0703f6744d8359aa85ef646e959434cf1a202e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb35f2d4517ad6b4331358139e596af43c415f76d1095ca36c6e1f9277d47e4(
    value: typing.Optional[ApigeeApiProductOperationGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290d6a86ce0df70f7f4a693a4c2570b98a95557457a9f52463ba8709f15fba1b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab6945228d3466f1e5fac4bf3dbb215f93a7df614dc227cdedd27462e38206e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc6b79e6c47c9b9c6ec64f7a49cceec2d37c51b28aeaff84f415533a402a725(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a880a1978b617b6a264e03f7e12e1e412384a3ad8f7665e3551fa3136e80c4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a8291be84e975b941510d299cd5d5529c7676cc86ec51dcbdfa19013e5ac1d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f99ca7eefc72b5e92dd1f4dcbc05a7e545d6d9df5711e9b6eb6f05aa7fa2b67(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeApiProductTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

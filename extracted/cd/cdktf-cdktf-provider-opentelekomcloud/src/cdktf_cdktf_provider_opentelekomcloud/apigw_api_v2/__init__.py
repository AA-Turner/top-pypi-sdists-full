r'''
# `opentelekomcloud_apigw_api_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_apigw_api_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2).
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


class ApigwApiV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2 opentelekomcloud_apigw_api_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        gateway_id: builtins.str,
        group_id: builtins.str,
        name: builtins.str,
        request_method: builtins.str,
        request_protocol: builtins.str,
        request_uri: builtins.str,
        type: builtins.str,
        authorizer_id: typing.Optional[builtins.str] = None,
        backend_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2BackendParams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        body_description: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        failure_response: typing.Optional[builtins.str] = None,
        func_graph: typing.Optional[typing.Union["ApigwApiV2FuncGraph", typing.Dict[builtins.str, typing.Any]]] = None,
        func_graph_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2FuncGraphPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http: typing.Optional[typing.Union["ApigwApiV2Http", typing.Dict[builtins.str, typing.Any]]] = None,
        http_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2HttpPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        match_mode: typing.Optional[builtins.str] = None,
        mock: typing.Optional[typing.Union["ApigwApiV2Mock", typing.Dict[builtins.str, typing.Any]]] = None,
        mock_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2MockPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        request_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2RequestParams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_id: typing.Optional[builtins.str] = None,
        security_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_authentication_type: typing.Optional[builtins.str] = None,
        success_response: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2 opentelekomcloud_apigw_api_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#gateway_id ApigwApiV2#gateway_id}.
        :param group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#group_id ApigwApiV2#group_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.
        :param request_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_method ApigwApiV2#request_method}.
        :param request_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_protocol ApigwApiV2#request_protocol}.
        :param request_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_uri ApigwApiV2#request_uri}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.
        :param authorizer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.
        :param backend_params: backend_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#backend_params ApigwApiV2#backend_params}
        :param body_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#body_description ApigwApiV2#body_description}.
        :param cors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#cors ApigwApiV2#cors}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.
        :param failure_response: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#failure_response ApigwApiV2#failure_response}.
        :param func_graph: func_graph block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#func_graph ApigwApiV2#func_graph}
        :param func_graph_policy: func_graph_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#func_graph_policy ApigwApiV2#func_graph_policy}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#http ApigwApiV2#http}
        :param http_policy: http_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#http_policy ApigwApiV2#http_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#id ApigwApiV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param match_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#match_mode ApigwApiV2#match_mode}.
        :param mock: mock block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#mock ApigwApiV2#mock}
        :param mock_policy: mock_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#mock_policy ApigwApiV2#mock_policy}
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#region ApigwApiV2#region}.
        :param request_params: request_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_params ApigwApiV2#request_params}
        :param response_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#response_id ApigwApiV2#response_id}.
        :param security_authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#security_authentication_enabled ApigwApiV2#security_authentication_enabled}.
        :param security_authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#security_authentication_type ApigwApiV2#security_authentication_type}.
        :param success_response: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#success_response ApigwApiV2#success_response}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#tags ApigwApiV2#tags}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#version ApigwApiV2#version}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c6d591787b72ced60a28d7fd2c09ded0ef5bb28ba58cbb19861e0dda0f601f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApigwApiV2Config(
            gateway_id=gateway_id,
            group_id=group_id,
            name=name,
            request_method=request_method,
            request_protocol=request_protocol,
            request_uri=request_uri,
            type=type,
            authorizer_id=authorizer_id,
            backend_params=backend_params,
            body_description=body_description,
            cors=cors,
            description=description,
            failure_response=failure_response,
            func_graph=func_graph,
            func_graph_policy=func_graph_policy,
            http=http,
            http_policy=http_policy,
            id=id,
            match_mode=match_mode,
            mock=mock,
            mock_policy=mock_policy,
            region=region,
            request_params=request_params,
            response_id=response_id,
            security_authentication_enabled=security_authentication_enabled,
            security_authentication_type=security_authentication_type,
            success_response=success_response,
            tags=tags,
            version=version,
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
        '''Generates CDKTF code for importing a ApigwApiV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApigwApiV2 to import.
        :param import_from_id: The id of the existing ApigwApiV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApigwApiV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b2583d77120eb9a486bc84646f2b47db3afb1310f702e8197b45ba61fa44dc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackendParams")
    def put_backend_params(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2BackendParams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c0594e84901cd906cf0b083c60563c4cdc4434b100784e09b1d88456d5fa75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackendParams", [value]))

    @jsii.member(jsii_name="putFuncGraph")
    def put_func_graph(
        self,
        *,
        function_urn: builtins.str,
        authorizer_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        invocation_type: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param function_urn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#function_urn ApigwApiV2#function_urn}.
        :param authorizer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.
        :param invocation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#invocation_type ApigwApiV2#invocation_type}.
        :param network_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#network_type ApigwApiV2#network_type}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#timeout ApigwApiV2#timeout}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#version ApigwApiV2#version}.
        '''
        value = ApigwApiV2FuncGraph(
            function_urn=function_urn,
            authorizer_id=authorizer_id,
            description=description,
            invocation_type=invocation_type,
            network_type=network_type,
            timeout=timeout,
            version=version,
        )

        return typing.cast(None, jsii.invoke(self, "putFuncGraph", [value]))

    @jsii.member(jsii_name="putFuncGraphPolicy")
    def put_func_graph_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2FuncGraphPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac4d558f77573ac6f6535eaaf9cac46b96dfacb7b0f3cc030b98e3d3206c476a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFuncGraphPolicy", [value]))

    @jsii.member(jsii_name="putHttp")
    def put_http(
        self,
        *,
        request_method: builtins.str,
        request_uri: builtins.str,
        authorizer_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        request_protocol: typing.Optional[builtins.str] = None,
        retry_count: typing.Optional[jsii.Number] = None,
        ssl_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        url_domain: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        vpc_channel_id: typing.Optional[builtins.str] = None,
        vpc_channel_proxy_host: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param request_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_method ApigwApiV2#request_method}.
        :param request_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_uri ApigwApiV2#request_uri}.
        :param authorizer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.
        :param request_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_protocol ApigwApiV2#request_protocol}.
        :param retry_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#retry_count ApigwApiV2#retry_count}.
        :param ssl_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#ssl_enable ApigwApiV2#ssl_enable}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#timeout ApigwApiV2#timeout}.
        :param url_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#url_domain ApigwApiV2#url_domain}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#version ApigwApiV2#version}.
        :param vpc_channel_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#vpc_channel_id ApigwApiV2#vpc_channel_id}.
        :param vpc_channel_proxy_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#vpc_channel_proxy_host ApigwApiV2#vpc_channel_proxy_host}.
        '''
        value = ApigwApiV2Http(
            request_method=request_method,
            request_uri=request_uri,
            authorizer_id=authorizer_id,
            description=description,
            request_protocol=request_protocol,
            retry_count=retry_count,
            ssl_enable=ssl_enable,
            timeout=timeout,
            url_domain=url_domain,
            version=version,
            vpc_channel_id=vpc_channel_id,
            vpc_channel_proxy_host=vpc_channel_proxy_host,
        )

        return typing.cast(None, jsii.invoke(self, "putHttp", [value]))

    @jsii.member(jsii_name="putHttpPolicy")
    def put_http_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2HttpPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3317766a38b0d92e6c884aaf8838795367b7da2f96c58da1f1e685427748d59b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpPolicy", [value]))

    @jsii.member(jsii_name="putMock")
    def put_mock(
        self,
        *,
        authorizer_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        response: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.
        :param response: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#response ApigwApiV2#response}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#version ApigwApiV2#version}.
        '''
        value = ApigwApiV2Mock(
            authorizer_id=authorizer_id,
            description=description,
            response=response,
            version=version,
        )

        return typing.cast(None, jsii.invoke(self, "putMock", [value]))

    @jsii.member(jsii_name="putMockPolicy")
    def put_mock_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2MockPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c114ec1361094937e51477539c398a0d6041f508d0769b8de2ed7a4d5cc6aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMockPolicy", [value]))

    @jsii.member(jsii_name="putRequestParams")
    def put_request_params(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2RequestParams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dee2ee99a829667c54c5c46ca5d6ea86221a8d94f291f75f4b01d344b25d1d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestParams", [value]))

    @jsii.member(jsii_name="resetAuthorizerId")
    def reset_authorizer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizerId", []))

    @jsii.member(jsii_name="resetBackendParams")
    def reset_backend_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendParams", []))

    @jsii.member(jsii_name="resetBodyDescription")
    def reset_body_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBodyDescription", []))

    @jsii.member(jsii_name="resetCors")
    def reset_cors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCors", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFailureResponse")
    def reset_failure_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureResponse", []))

    @jsii.member(jsii_name="resetFuncGraph")
    def reset_func_graph(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFuncGraph", []))

    @jsii.member(jsii_name="resetFuncGraphPolicy")
    def reset_func_graph_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFuncGraphPolicy", []))

    @jsii.member(jsii_name="resetHttp")
    def reset_http(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp", []))

    @jsii.member(jsii_name="resetHttpPolicy")
    def reset_http_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpPolicy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMatchMode")
    def reset_match_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchMode", []))

    @jsii.member(jsii_name="resetMock")
    def reset_mock(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMock", []))

    @jsii.member(jsii_name="resetMockPolicy")
    def reset_mock_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMockPolicy", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRequestParams")
    def reset_request_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestParams", []))

    @jsii.member(jsii_name="resetResponseId")
    def reset_response_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseId", []))

    @jsii.member(jsii_name="resetSecurityAuthenticationEnabled")
    def reset_security_authentication_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityAuthenticationEnabled", []))

    @jsii.member(jsii_name="resetSecurityAuthenticationType")
    def reset_security_authentication_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityAuthenticationType", []))

    @jsii.member(jsii_name="resetSuccessResponse")
    def reset_success_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessResponse", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

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
    @jsii.member(jsii_name="backendParams")
    def backend_params(self) -> "ApigwApiV2BackendParamsList":
        return typing.cast("ApigwApiV2BackendParamsList", jsii.get(self, "backendParams"))

    @builtins.property
    @jsii.member(jsii_name="funcGraph")
    def func_graph(self) -> "ApigwApiV2FuncGraphOutputReference":
        return typing.cast("ApigwApiV2FuncGraphOutputReference", jsii.get(self, "funcGraph"))

    @builtins.property
    @jsii.member(jsii_name="funcGraphPolicy")
    def func_graph_policy(self) -> "ApigwApiV2FuncGraphPolicyList":
        return typing.cast("ApigwApiV2FuncGraphPolicyList", jsii.get(self, "funcGraphPolicy"))

    @builtins.property
    @jsii.member(jsii_name="http")
    def http(self) -> "ApigwApiV2HttpOutputReference":
        return typing.cast("ApigwApiV2HttpOutputReference", jsii.get(self, "http"))

    @builtins.property
    @jsii.member(jsii_name="httpPolicy")
    def http_policy(self) -> "ApigwApiV2HttpPolicyList":
        return typing.cast("ApigwApiV2HttpPolicyList", jsii.get(self, "httpPolicy"))

    @builtins.property
    @jsii.member(jsii_name="mock")
    def mock(self) -> "ApigwApiV2MockOutputReference":
        return typing.cast("ApigwApiV2MockOutputReference", jsii.get(self, "mock"))

    @builtins.property
    @jsii.member(jsii_name="mockPolicy")
    def mock_policy(self) -> "ApigwApiV2MockPolicyList":
        return typing.cast("ApigwApiV2MockPolicyList", jsii.get(self, "mockPolicy"))

    @builtins.property
    @jsii.member(jsii_name="registeredAt")
    def registered_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registeredAt"))

    @builtins.property
    @jsii.member(jsii_name="requestParams")
    def request_params(self) -> "ApigwApiV2RequestParamsList":
        return typing.cast("ApigwApiV2RequestParamsList", jsii.get(self, "requestParams"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="authorizerIdInput")
    def authorizer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="backendParamsInput")
    def backend_params_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2BackendParams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2BackendParams"]]], jsii.get(self, "backendParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyDescriptionInput")
    def body_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="corsInput")
    def cors_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "corsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="failureResponseInput")
    def failure_response_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "failureResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="funcGraphInput")
    def func_graph_input(self) -> typing.Optional["ApigwApiV2FuncGraph"]:
        return typing.cast(typing.Optional["ApigwApiV2FuncGraph"], jsii.get(self, "funcGraphInput"))

    @builtins.property
    @jsii.member(jsii_name="funcGraphPolicyInput")
    def func_graph_policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2FuncGraphPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2FuncGraphPolicy"]]], jsii.get(self, "funcGraphPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayIdInput")
    def gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="httpInput")
    def http_input(self) -> typing.Optional["ApigwApiV2Http"]:
        return typing.cast(typing.Optional["ApigwApiV2Http"], jsii.get(self, "httpInput"))

    @builtins.property
    @jsii.member(jsii_name="httpPolicyInput")
    def http_policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2HttpPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2HttpPolicy"]]], jsii.get(self, "httpPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="matchModeInput")
    def match_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="mockInput")
    def mock_input(self) -> typing.Optional["ApigwApiV2Mock"]:
        return typing.cast(typing.Optional["ApigwApiV2Mock"], jsii.get(self, "mockInput"))

    @builtins.property
    @jsii.member(jsii_name="mockPolicyInput")
    def mock_policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2MockPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2MockPolicy"]]], jsii.get(self, "mockPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestMethodInput")
    def request_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="requestParamsInput")
    def request_params_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2RequestParams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2RequestParams"]]], jsii.get(self, "requestParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="requestProtocolInput")
    def request_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="requestUriInput")
    def request_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestUriInput"))

    @builtins.property
    @jsii.member(jsii_name="responseIdInput")
    def response_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseIdInput"))

    @builtins.property
    @jsii.member(jsii_name="securityAuthenticationEnabledInput")
    def security_authentication_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "securityAuthenticationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="securityAuthenticationTypeInput")
    def security_authentication_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityAuthenticationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="successResponseInput")
    def success_response_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "successResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizerId"))

    @authorizer_id.setter
    def authorizer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c741f67b1cd739916dffb8140c837a0a5925808a554cf752938fddafea12d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bodyDescription")
    def body_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bodyDescription"))

    @body_description.setter
    def body_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37bc815a2cd221075c00316e48b4e52d6316fc75a6a635a736953b875d41a7f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bodyDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cors")
    def cors(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cors"))

    @cors.setter
    def cors(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7659527498d3a621a45e14361d1c1cd2167d12ae9157baae3a911533158bd6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dbcf6c3885f855e4297a226dff953daf8b433277c0833f3d5f12e8f2e102d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failureResponse")
    def failure_response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failureResponse"))

    @failure_response.setter
    def failure_response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48618b4e21107d6d7836b97e2774fb9e575ce41bdd9e908913c9dd2348b49012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureResponse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gatewayId")
    def gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayId"))

    @gateway_id.setter
    def gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c3b2c8f2cf969201fc6698ba42111382e233836f385078dc0e9a9c19fa0529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__435879ffc3a2e06ce9a4e3419108647af9f22750987194763c8a269f63789e68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d16972e248b07868a0f2428bceb84fedb6b82997e8225ce9030f39724bf4e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchMode")
    def match_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchMode"))

    @match_mode.setter
    def match_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__453954931077f4e1616cf1482a8f5368c9c691095419caf6ba8aa738b9cd58af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f88b327fd5b03ad09fbcd6c93635a939851786e5cc5b6cb4f201b0d9dcafbbb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ccdc9cb5dcd17252fd8035ae961224a78b1ebfd1ff7e7ec9752cc1bf69efcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestMethod")
    def request_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestMethod"))

    @request_method.setter
    def request_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c948d54d75957099e366a1a758abbc470db418e7838f29c3977417f4d97537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestProtocol")
    def request_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestProtocol"))

    @request_protocol.setter
    def request_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7d8392ef836b2f36360e3d2cac8ba3eee0b70ddd2caceb696857e5a67b1a83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestUri")
    def request_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestUri"))

    @request_uri.setter
    def request_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66af1a0912254692405948cb42d75e5ba3eb0df03c3fefea0c75d48501a20281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseId")
    def response_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseId"))

    @response_id.setter
    def response_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ced327dcdf101c7016e05c9735eb40b3c8686418af0d17c3e22d1ffd9e8faf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityAuthenticationEnabled")
    def security_authentication_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "securityAuthenticationEnabled"))

    @security_authentication_enabled.setter
    def security_authentication_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36cf44897c72b51d4946e2d96703d7a9d0ae882a7fff92e317b2b59ad560fa48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityAuthenticationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityAuthenticationType")
    def security_authentication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityAuthenticationType"))

    @security_authentication_type.setter
    def security_authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5c83eacfae9d8dcabc02114eec78a0229d4e76f6b74642ab2641492df77447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityAuthenticationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successResponse")
    def success_response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "successResponse"))

    @success_response.setter
    def success_response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54fdaf6e13149df6273f1aa01f7e06bf650644468ca63433ec0a1441785304c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successResponse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ebf3bd12a423a5b817076b47fecf8ad4991c7a286e09a3179eda79d19cd82b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a2b681587a43f32ef796a3741300e2d3f2de39ea06b24568177814fda28696e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__477de151aa89463f855b00d5d454180ae8d65b55890c393d74372a5cc96e4b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2BackendParams",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "name": "name",
        "type": "type",
        "value": "value",
        "description": "description",
        "system_param_type": "systemParamType",
    },
)
class ApigwApiV2BackendParams:
    def __init__(
        self,
        *,
        location: builtins.str,
        name: builtins.str,
        type: builtins.str,
        value: builtins.str,
        description: typing.Optional[builtins.str] = None,
        system_param_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#location ApigwApiV2#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#value ApigwApiV2#value}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.
        :param system_param_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#system_param_type ApigwApiV2#system_param_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5272ad308f2177cd178a354a08f1b48dd06aab6ac5dbd7a7ad3c353c117b6e04)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument system_param_type", value=system_param_type, expected_type=type_hints["system_param_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "type": type,
            "value": value,
        }
        if description is not None:
            self._values["description"] = description
        if system_param_type is not None:
            self._values["system_param_type"] = system_param_type

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#location ApigwApiV2#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#value ApigwApiV2#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_param_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#system_param_type ApigwApiV2#system_param_type}.'''
        result = self._values.get("system_param_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwApiV2BackendParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwApiV2BackendParamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2BackendParamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5938eaf406a44d0524ab5511c5d4595fcb781b0b4153f23b3c84fd9817907a2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApigwApiV2BackendParamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f123697d071cb30e265348fa3b51bc4f50ede0ebd6d99f64a3f25e3863d3eb51)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigwApiV2BackendParamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09215e036466ccfecf0551124d0ad20c2286eea6579a5dcfdd8226a83bd25d84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4636aa5a6a64b2ae8350965dc722679dd80dd85185f21945744fd07c9d8cd9c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3337aa79b166173e4ad013677c14ffae9cb8288db2b2a32df82e5ec7228e28d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2BackendParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2BackendParams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2BackendParams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e83e455e2ee524117c1c89af2519bc92b63418ded636dc664452567554235b84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwApiV2BackendParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2BackendParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21e1e3888ebc2f245610cfebd313f80d8df4e429e575903433aa01238de47978)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetSystemParamType")
    def reset_system_param_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemParamType", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="systemParamTypeInput")
    def system_param_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemParamTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0181a2baca96237f3e3243a07ecfc67076014c94fd7e764c48d694a7e367e5d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f55ae9c306e450f2e19a45809aec9f6f2a89dff629d7dffed2e7f258ca24eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebe816b3399b0f02af16cfe5ee572ee94bd23fefe422e13c8c3cc9b239b5fb72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemParamType")
    def system_param_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemParamType"))

    @system_param_type.setter
    def system_param_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11e8020cbf83675b61c48058f29cba9e1fe5634634c7f0e2299e4c1412c0dbcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemParamType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8493ee9684b43715f8f6ea84dce348a383e5d2300b1852188ae0fa84bd8bba90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__312549a66ae7c8539b3c2bdc21b0aec81ce58d46254d815719ea6913e1508e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2BackendParams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2BackendParams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2BackendParams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89d76bceab190c521b5f3464fe1e9ff68efc42f82e70ff7268df5a977a45dd90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "gateway_id": "gatewayId",
        "group_id": "groupId",
        "name": "name",
        "request_method": "requestMethod",
        "request_protocol": "requestProtocol",
        "request_uri": "requestUri",
        "type": "type",
        "authorizer_id": "authorizerId",
        "backend_params": "backendParams",
        "body_description": "bodyDescription",
        "cors": "cors",
        "description": "description",
        "failure_response": "failureResponse",
        "func_graph": "funcGraph",
        "func_graph_policy": "funcGraphPolicy",
        "http": "http",
        "http_policy": "httpPolicy",
        "id": "id",
        "match_mode": "matchMode",
        "mock": "mock",
        "mock_policy": "mockPolicy",
        "region": "region",
        "request_params": "requestParams",
        "response_id": "responseId",
        "security_authentication_enabled": "securityAuthenticationEnabled",
        "security_authentication_type": "securityAuthenticationType",
        "success_response": "successResponse",
        "tags": "tags",
        "version": "version",
    },
)
class ApigwApiV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        gateway_id: builtins.str,
        group_id: builtins.str,
        name: builtins.str,
        request_method: builtins.str,
        request_protocol: builtins.str,
        request_uri: builtins.str,
        type: builtins.str,
        authorizer_id: typing.Optional[builtins.str] = None,
        backend_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2BackendParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
        body_description: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        failure_response: typing.Optional[builtins.str] = None,
        func_graph: typing.Optional[typing.Union["ApigwApiV2FuncGraph", typing.Dict[builtins.str, typing.Any]]] = None,
        func_graph_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2FuncGraphPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http: typing.Optional[typing.Union["ApigwApiV2Http", typing.Dict[builtins.str, typing.Any]]] = None,
        http_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2HttpPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        match_mode: typing.Optional[builtins.str] = None,
        mock: typing.Optional[typing.Union["ApigwApiV2Mock", typing.Dict[builtins.str, typing.Any]]] = None,
        mock_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2MockPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        request_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2RequestParams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_id: typing.Optional[builtins.str] = None,
        security_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_authentication_type: typing.Optional[builtins.str] = None,
        success_response: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#gateway_id ApigwApiV2#gateway_id}.
        :param group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#group_id ApigwApiV2#group_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.
        :param request_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_method ApigwApiV2#request_method}.
        :param request_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_protocol ApigwApiV2#request_protocol}.
        :param request_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_uri ApigwApiV2#request_uri}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.
        :param authorizer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.
        :param backend_params: backend_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#backend_params ApigwApiV2#backend_params}
        :param body_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#body_description ApigwApiV2#body_description}.
        :param cors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#cors ApigwApiV2#cors}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.
        :param failure_response: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#failure_response ApigwApiV2#failure_response}.
        :param func_graph: func_graph block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#func_graph ApigwApiV2#func_graph}
        :param func_graph_policy: func_graph_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#func_graph_policy ApigwApiV2#func_graph_policy}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#http ApigwApiV2#http}
        :param http_policy: http_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#http_policy ApigwApiV2#http_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#id ApigwApiV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param match_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#match_mode ApigwApiV2#match_mode}.
        :param mock: mock block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#mock ApigwApiV2#mock}
        :param mock_policy: mock_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#mock_policy ApigwApiV2#mock_policy}
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#region ApigwApiV2#region}.
        :param request_params: request_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_params ApigwApiV2#request_params}
        :param response_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#response_id ApigwApiV2#response_id}.
        :param security_authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#security_authentication_enabled ApigwApiV2#security_authentication_enabled}.
        :param security_authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#security_authentication_type ApigwApiV2#security_authentication_type}.
        :param success_response: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#success_response ApigwApiV2#success_response}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#tags ApigwApiV2#tags}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#version ApigwApiV2#version}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(func_graph, dict):
            func_graph = ApigwApiV2FuncGraph(**func_graph)
        if isinstance(http, dict):
            http = ApigwApiV2Http(**http)
        if isinstance(mock, dict):
            mock = ApigwApiV2Mock(**mock)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f99146ae80425ff18102abd92c0a20f2d969194859e001830dc1039c6243a1f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument gateway_id", value=gateway_id, expected_type=type_hints["gateway_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument request_method", value=request_method, expected_type=type_hints["request_method"])
            check_type(argname="argument request_protocol", value=request_protocol, expected_type=type_hints["request_protocol"])
            check_type(argname="argument request_uri", value=request_uri, expected_type=type_hints["request_uri"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument authorizer_id", value=authorizer_id, expected_type=type_hints["authorizer_id"])
            check_type(argname="argument backend_params", value=backend_params, expected_type=type_hints["backend_params"])
            check_type(argname="argument body_description", value=body_description, expected_type=type_hints["body_description"])
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument failure_response", value=failure_response, expected_type=type_hints["failure_response"])
            check_type(argname="argument func_graph", value=func_graph, expected_type=type_hints["func_graph"])
            check_type(argname="argument func_graph_policy", value=func_graph_policy, expected_type=type_hints["func_graph_policy"])
            check_type(argname="argument http", value=http, expected_type=type_hints["http"])
            check_type(argname="argument http_policy", value=http_policy, expected_type=type_hints["http_policy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument match_mode", value=match_mode, expected_type=type_hints["match_mode"])
            check_type(argname="argument mock", value=mock, expected_type=type_hints["mock"])
            check_type(argname="argument mock_policy", value=mock_policy, expected_type=type_hints["mock_policy"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument request_params", value=request_params, expected_type=type_hints["request_params"])
            check_type(argname="argument response_id", value=response_id, expected_type=type_hints["response_id"])
            check_type(argname="argument security_authentication_enabled", value=security_authentication_enabled, expected_type=type_hints["security_authentication_enabled"])
            check_type(argname="argument security_authentication_type", value=security_authentication_type, expected_type=type_hints["security_authentication_type"])
            check_type(argname="argument success_response", value=success_response, expected_type=type_hints["success_response"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway_id": gateway_id,
            "group_id": group_id,
            "name": name,
            "request_method": request_method,
            "request_protocol": request_protocol,
            "request_uri": request_uri,
            "type": type,
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
        if authorizer_id is not None:
            self._values["authorizer_id"] = authorizer_id
        if backend_params is not None:
            self._values["backend_params"] = backend_params
        if body_description is not None:
            self._values["body_description"] = body_description
        if cors is not None:
            self._values["cors"] = cors
        if description is not None:
            self._values["description"] = description
        if failure_response is not None:
            self._values["failure_response"] = failure_response
        if func_graph is not None:
            self._values["func_graph"] = func_graph
        if func_graph_policy is not None:
            self._values["func_graph_policy"] = func_graph_policy
        if http is not None:
            self._values["http"] = http
        if http_policy is not None:
            self._values["http_policy"] = http_policy
        if id is not None:
            self._values["id"] = id
        if match_mode is not None:
            self._values["match_mode"] = match_mode
        if mock is not None:
            self._values["mock"] = mock
        if mock_policy is not None:
            self._values["mock_policy"] = mock_policy
        if region is not None:
            self._values["region"] = region
        if request_params is not None:
            self._values["request_params"] = request_params
        if response_id is not None:
            self._values["response_id"] = response_id
        if security_authentication_enabled is not None:
            self._values["security_authentication_enabled"] = security_authentication_enabled
        if security_authentication_type is not None:
            self._values["security_authentication_type"] = security_authentication_type
        if success_response is not None:
            self._values["success_response"] = success_response
        if tags is not None:
            self._values["tags"] = tags
        if version is not None:
            self._values["version"] = version

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
    def gateway_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#gateway_id ApigwApiV2#gateway_id}.'''
        result = self._values.get("gateway_id")
        assert result is not None, "Required property 'gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#group_id ApigwApiV2#group_id}.'''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_method(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_method ApigwApiV2#request_method}.'''
        result = self._values.get("request_method")
        assert result is not None, "Required property 'request_method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_protocol ApigwApiV2#request_protocol}.'''
        result = self._values.get("request_protocol")
        assert result is not None, "Required property 'request_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_uri ApigwApiV2#request_uri}.'''
        result = self._values.get("request_uri")
        assert result is not None, "Required property 'request_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorizer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.'''
        result = self._values.get("authorizer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backend_params(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2BackendParams]]]:
        '''backend_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#backend_params ApigwApiV2#backend_params}
        '''
        result = self._values.get("backend_params")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2BackendParams]]], result)

    @builtins.property
    def body_description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#body_description ApigwApiV2#body_description}.'''
        result = self._values.get("body_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#cors ApigwApiV2#cors}.'''
        result = self._values.get("cors")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_response(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#failure_response ApigwApiV2#failure_response}.'''
        result = self._values.get("failure_response")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def func_graph(self) -> typing.Optional["ApigwApiV2FuncGraph"]:
        '''func_graph block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#func_graph ApigwApiV2#func_graph}
        '''
        result = self._values.get("func_graph")
        return typing.cast(typing.Optional["ApigwApiV2FuncGraph"], result)

    @builtins.property
    def func_graph_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2FuncGraphPolicy"]]]:
        '''func_graph_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#func_graph_policy ApigwApiV2#func_graph_policy}
        '''
        result = self._values.get("func_graph_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2FuncGraphPolicy"]]], result)

    @builtins.property
    def http(self) -> typing.Optional["ApigwApiV2Http"]:
        '''http block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#http ApigwApiV2#http}
        '''
        result = self._values.get("http")
        return typing.cast(typing.Optional["ApigwApiV2Http"], result)

    @builtins.property
    def http_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2HttpPolicy"]]]:
        '''http_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#http_policy ApigwApiV2#http_policy}
        '''
        result = self._values.get("http_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2HttpPolicy"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#id ApigwApiV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#match_mode ApigwApiV2#match_mode}.'''
        result = self._values.get("match_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mock(self) -> typing.Optional["ApigwApiV2Mock"]:
        '''mock block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#mock ApigwApiV2#mock}
        '''
        result = self._values.get("mock")
        return typing.cast(typing.Optional["ApigwApiV2Mock"], result)

    @builtins.property
    def mock_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2MockPolicy"]]]:
        '''mock_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#mock_policy ApigwApiV2#mock_policy}
        '''
        result = self._values.get("mock_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2MockPolicy"]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#region ApigwApiV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_params(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2RequestParams"]]]:
        '''request_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_params ApigwApiV2#request_params}
        '''
        result = self._values.get("request_params")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2RequestParams"]]], result)

    @builtins.property
    def response_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#response_id ApigwApiV2#response_id}.'''
        result = self._values.get("response_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_authentication_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#security_authentication_enabled ApigwApiV2#security_authentication_enabled}.'''
        result = self._values.get("security_authentication_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security_authentication_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#security_authentication_type ApigwApiV2#security_authentication_type}.'''
        result = self._values.get("security_authentication_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success_response(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#success_response ApigwApiV2#success_response}.'''
        result = self._values.get("success_response")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#tags ApigwApiV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#version ApigwApiV2#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwApiV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2FuncGraph",
    jsii_struct_bases=[],
    name_mapping={
        "function_urn": "functionUrn",
        "authorizer_id": "authorizerId",
        "description": "description",
        "invocation_type": "invocationType",
        "network_type": "networkType",
        "timeout": "timeout",
        "version": "version",
    },
)
class ApigwApiV2FuncGraph:
    def __init__(
        self,
        *,
        function_urn: builtins.str,
        authorizer_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        invocation_type: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param function_urn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#function_urn ApigwApiV2#function_urn}.
        :param authorizer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.
        :param invocation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#invocation_type ApigwApiV2#invocation_type}.
        :param network_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#network_type ApigwApiV2#network_type}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#timeout ApigwApiV2#timeout}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#version ApigwApiV2#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ec5573ceee1551a8adae90ba07dc4a693257f0075b9f39bbc4d20f5f36408d)
            check_type(argname="argument function_urn", value=function_urn, expected_type=type_hints["function_urn"])
            check_type(argname="argument authorizer_id", value=authorizer_id, expected_type=type_hints["authorizer_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_urn": function_urn,
        }
        if authorizer_id is not None:
            self._values["authorizer_id"] = authorizer_id
        if description is not None:
            self._values["description"] = description
        if invocation_type is not None:
            self._values["invocation_type"] = invocation_type
        if network_type is not None:
            self._values["network_type"] = network_type
        if timeout is not None:
            self._values["timeout"] = timeout
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def function_urn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#function_urn ApigwApiV2#function_urn}.'''
        result = self._values.get("function_urn")
        assert result is not None, "Required property 'function_urn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorizer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.'''
        result = self._values.get("authorizer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invocation_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#invocation_type ApigwApiV2#invocation_type}.'''
        result = self._values.get("invocation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#network_type ApigwApiV2#network_type}.'''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#timeout ApigwApiV2#timeout}.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#version ApigwApiV2#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwApiV2FuncGraph(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwApiV2FuncGraphOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2FuncGraphOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11ea7b9eed3785099ddaf2caf63434f6345ac95ea042f5d63c848519f8387fe7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthorizerId")
    def reset_authorizer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizerId", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetInvocationType")
    def reset_invocation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvocationType", []))

    @jsii.member(jsii_name="resetNetworkType")
    def reset_network_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkType", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="authorizerIdInput")
    def authorizer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="functionUrnInput")
    def function_urn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionUrnInput"))

    @builtins.property
    @jsii.member(jsii_name="invocationTypeInput")
    def invocation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "invocationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTypeInput")
    def network_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizerId"))

    @authorizer_id.setter
    def authorizer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1acca9cf786fab79e31ed948bc6328f58d1171b5d48eff2d71ba2e1a4b7bb0d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97e12613cd4f82bf0cf5c25868b125a0abe71db52df1f04fd98130726e95b36c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionUrn")
    def function_urn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionUrn"))

    @function_urn.setter
    def function_urn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d46f543a7a16f30dccf7913e94afe676c29e458047dc4d4ab6b4263014e784cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionUrn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invocationType")
    def invocation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "invocationType"))

    @invocation_type.setter
    def invocation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e2b826b0a29775c7a349be71e30286f3c9e6dbe02f522e558902a2241ceaa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invocationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkType")
    def network_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkType"))

    @network_type.setter
    def network_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9a4ec350f7adc96c676f8df7d4597ce278a09814e1b22d40f62b5b4e76e4c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12746fa66408ac1bba58911fe43633f8d2781f9104367cc877695524bfdbdfcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db44af16030471d8dcbbc8a347f0e27ea0e6b62b1484331e2cc58ccb808f564b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigwApiV2FuncGraph]:
        return typing.cast(typing.Optional[ApigwApiV2FuncGraph], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApigwApiV2FuncGraph]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b01ec7a384251f9785dca4327c73b0bad98d84615d691f36d4a5ebeb1be35b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2FuncGraphPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "conditions": "conditions",
        "function_urn": "functionUrn",
        "name": "name",
        "authorizer_id": "authorizerId",
        "backend_params": "backendParams",
        "effective_mode": "effectiveMode",
        "invocation_type": "invocationType",
        "network_type": "networkType",
        "timeout": "timeout",
        "version": "version",
    },
)
class ApigwApiV2FuncGraphPolicy:
    def __init__(
        self,
        *,
        conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2FuncGraphPolicyConditions", typing.Dict[builtins.str, typing.Any]]]],
        function_urn: builtins.str,
        name: builtins.str,
        authorizer_id: typing.Optional[builtins.str] = None,
        backend_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2FuncGraphPolicyBackendParams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        effective_mode: typing.Optional[builtins.str] = None,
        invocation_type: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#conditions ApigwApiV2#conditions}
        :param function_urn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#function_urn ApigwApiV2#function_urn}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.
        :param authorizer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.
        :param backend_params: backend_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#backend_params ApigwApiV2#backend_params}
        :param effective_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#effective_mode ApigwApiV2#effective_mode}.
        :param invocation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#invocation_type ApigwApiV2#invocation_type}.
        :param network_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#network_type ApigwApiV2#network_type}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#timeout ApigwApiV2#timeout}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#version ApigwApiV2#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d0982cdbb0aab92bd59fb512b00424b2806f9c6ce0ac31ca8c4ee7e5b564226)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument function_urn", value=function_urn, expected_type=type_hints["function_urn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument authorizer_id", value=authorizer_id, expected_type=type_hints["authorizer_id"])
            check_type(argname="argument backend_params", value=backend_params, expected_type=type_hints["backend_params"])
            check_type(argname="argument effective_mode", value=effective_mode, expected_type=type_hints["effective_mode"])
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "conditions": conditions,
            "function_urn": function_urn,
            "name": name,
        }
        if authorizer_id is not None:
            self._values["authorizer_id"] = authorizer_id
        if backend_params is not None:
            self._values["backend_params"] = backend_params
        if effective_mode is not None:
            self._values["effective_mode"] = effective_mode
        if invocation_type is not None:
            self._values["invocation_type"] = invocation_type
        if network_type is not None:
            self._values["network_type"] = network_type
        if timeout is not None:
            self._values["timeout"] = timeout
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def conditions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2FuncGraphPolicyConditions"]]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#conditions ApigwApiV2#conditions}
        '''
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2FuncGraphPolicyConditions"]], result)

    @builtins.property
    def function_urn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#function_urn ApigwApiV2#function_urn}.'''
        result = self._values.get("function_urn")
        assert result is not None, "Required property 'function_urn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorizer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.'''
        result = self._values.get("authorizer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backend_params(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2FuncGraphPolicyBackendParams"]]]:
        '''backend_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#backend_params ApigwApiV2#backend_params}
        '''
        result = self._values.get("backend_params")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2FuncGraphPolicyBackendParams"]]], result)

    @builtins.property
    def effective_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#effective_mode ApigwApiV2#effective_mode}.'''
        result = self._values.get("effective_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invocation_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#invocation_type ApigwApiV2#invocation_type}.'''
        result = self._values.get("invocation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#network_type ApigwApiV2#network_type}.'''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#timeout ApigwApiV2#timeout}.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#version ApigwApiV2#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwApiV2FuncGraphPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2FuncGraphPolicyBackendParams",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "name": "name",
        "type": "type",
        "value": "value",
        "description": "description",
        "system_param_type": "systemParamType",
    },
)
class ApigwApiV2FuncGraphPolicyBackendParams:
    def __init__(
        self,
        *,
        location: builtins.str,
        name: builtins.str,
        type: builtins.str,
        value: builtins.str,
        description: typing.Optional[builtins.str] = None,
        system_param_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#location ApigwApiV2#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#value ApigwApiV2#value}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.
        :param system_param_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#system_param_type ApigwApiV2#system_param_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f7fb1c878a9f4625795561a5bc987762bda08a5de974ee2e2af1b1e2996eff)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument system_param_type", value=system_param_type, expected_type=type_hints["system_param_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "type": type,
            "value": value,
        }
        if description is not None:
            self._values["description"] = description
        if system_param_type is not None:
            self._values["system_param_type"] = system_param_type

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#location ApigwApiV2#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#value ApigwApiV2#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_param_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#system_param_type ApigwApiV2#system_param_type}.'''
        result = self._values.get("system_param_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwApiV2FuncGraphPolicyBackendParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwApiV2FuncGraphPolicyBackendParamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2FuncGraphPolicyBackendParamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de83c4fdbc27b6e299ab04f80c42db39bc87d91d816c1187dd73f257bc5e5367)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigwApiV2FuncGraphPolicyBackendParamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__734b81e155e0ca84cd9722f42c212b6ddf4a41f331f370734ff0f9b172a95cfc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigwApiV2FuncGraphPolicyBackendParamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090d78e29e041ac0bd5225fed6cb7ed91bfe78c5750c83df69a50a420d6e0e77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecacf16a974a6fc66174dbf064a4462676c6f42ddf45324c8556714ab7bfef45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__018af445eff1a63eef854065d5f675ed98c91d1f2e9878611800d2578ef8cc6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicyBackendParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicyBackendParams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicyBackendParams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b1ad7a28346e6bcdc0f9161053a6169fe63bb2ba773b99556df8e8b3397c43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwApiV2FuncGraphPolicyBackendParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2FuncGraphPolicyBackendParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abb406034ed69a22d84ac85ee820b04fa472671910a69c14c4cd10a0f54e0d50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetSystemParamType")
    def reset_system_param_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemParamType", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="systemParamTypeInput")
    def system_param_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemParamTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b03debde1a1a827cb8f26126867470e12f49cfbe9900e5e95aa381a09d91b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__561cb35908a4a71341a1a06b3dc529b466f2be0cddadd65f21d53a276e7fa119)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c63da0b80bf78ead13bf43b1ea28ff6f4559d61a7ec734d08fc6a670f3dbb04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemParamType")
    def system_param_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemParamType"))

    @system_param_type.setter
    def system_param_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47de248f66711e1efa4f694bfab0145dde9719b70aea39973951c5bbdf691ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemParamType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71726c41e480a7c8ec3fc44c6523c66cccb4e18c79eb30f0449a7a6be20f0586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4831e7f1f2758a7c308a793de3c884c1c42bcde8f7b41eef7206accce5812dd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2FuncGraphPolicyBackendParams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2FuncGraphPolicyBackendParams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2FuncGraphPolicyBackendParams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58da4f3e2ed2215521ad2be2148c0303892fcf6df193033acf57b768043b7ab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2FuncGraphPolicyConditions",
    jsii_struct_bases=[],
    name_mapping={
        "value": "value",
        "origin": "origin",
        "param_name": "paramName",
        "type": "type",
    },
)
class ApigwApiV2FuncGraphPolicyConditions:
    def __init__(
        self,
        *,
        value: builtins.str,
        origin: typing.Optional[builtins.str] = None,
        param_name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#value ApigwApiV2#value}.
        :param origin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#origin ApigwApiV2#origin}.
        :param param_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#param_name ApigwApiV2#param_name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c3dd59dbd6dc7434e413a5c321489a7ea4bb039baa126f261ad14fc4c308c44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            check_type(argname="argument param_name", value=param_name, expected_type=type_hints["param_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if origin is not None:
            self._values["origin"] = origin
        if param_name is not None:
            self._values["param_name"] = param_name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#value ApigwApiV2#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#origin ApigwApiV2#origin}.'''
        result = self._values.get("origin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def param_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#param_name ApigwApiV2#param_name}.'''
        result = self._values.get("param_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwApiV2FuncGraphPolicyConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwApiV2FuncGraphPolicyConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2FuncGraphPolicyConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e5556468a4356eafc445d57642ca1c8896a0099b2b3d548511663adc59f0fc7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigwApiV2FuncGraphPolicyConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5813bbdb2de271a8df8b847998418a4549dd986f75e64867ef454cad891fba4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigwApiV2FuncGraphPolicyConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce951b14f517ec2c3ac9790775c036bffd27cc6632523042f7f77ddfbb57928)
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
            type_hints = typing.get_type_hints(_typecheckingstub__862c01aa1684d0986e8523509b320836d1124c6d8d08f75e0b76c59043fc75cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ee503e9b6caa8319ba789863538a7eb10204fad1ad0d6e80f8e5d72cc721dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicyConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicyConditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicyConditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1ab1386ac423e687458ba3b60d5f65a56c737d72fd4a28ce313f76f492c91a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwApiV2FuncGraphPolicyConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2FuncGraphPolicyConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31686c48c5232284dab3d7b024f73738e661b470fea874bbddec7b15414063aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOrigin")
    def reset_origin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrigin", []))

    @jsii.member(jsii_name="resetParamName")
    def reset_param_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParamName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="originInput")
    def origin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originInput"))

    @builtins.property
    @jsii.member(jsii_name="paramNameInput")
    def param_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "paramNameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="origin")
    def origin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "origin"))

    @origin.setter
    def origin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a57b9286945b66b6d86ddd011d254be81d197ca7e1072fdd5b3cdcc538b008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "origin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paramName")
    def param_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "paramName"))

    @param_name.setter
    def param_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466db76d7ad98da7c981afb2ff6a0d46100cf1c7d0eae9b64fa82ce834f7c662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paramName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__471ea9f86ae84e64f466b3304ec7e1ecb5dd47b39b098c28579a40c36c59f31c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39cc0cc1f7e8bb6c7ff29eec8e89c161c5f793db64f8e1a243e170bbb874b4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2FuncGraphPolicyConditions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2FuncGraphPolicyConditions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2FuncGraphPolicyConditions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6376a7ecbf10cfc8cb612049a565dfe558ac30b15b55cd1e678312f54850a515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwApiV2FuncGraphPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2FuncGraphPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1244d71f50a2d8ef54d72620e5bb8ea524522b5763e21a3e3ba8c329765cc528)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApigwApiV2FuncGraphPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f1c731a632b6fdb056400b2c25b2ecdda17a5d2b5d4ccbeebf11ad4faa5b54f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigwApiV2FuncGraphPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ea3b97c4f5e3fb482a989d3c7c049677d660e8b0c669f6f0c44df7dee0d4a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce07850942a95fb3a90b62055f679026bb97d68faa4cd839eb61df79a6efb432)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4160410f3fa8a63c8e090d2687f8b6d1235c04d3701b7e39df724651ea724aa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa9ebe92c771cac42cc1a42921bc6a4f4f8683b3b253ce81450b0541010db58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwApiV2FuncGraphPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2FuncGraphPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fbf05484d4a79ba255e4e41ea42c8b3c557ce86a07c91c10310285b991d4585)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBackendParams")
    def put_backend_params(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2FuncGraphPolicyBackendParams, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb8a5dd6819ebdf8f11b936f6bdf76fbc1386bdd3f4bb59413af5ed209a32e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackendParams", [value]))

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2FuncGraphPolicyConditions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52a3aa0f38c9543ecb50e33cdd94a2f1695bf3cda257affcf7b59d6648301ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="resetAuthorizerId")
    def reset_authorizer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizerId", []))

    @jsii.member(jsii_name="resetBackendParams")
    def reset_backend_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendParams", []))

    @jsii.member(jsii_name="resetEffectiveMode")
    def reset_effective_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffectiveMode", []))

    @jsii.member(jsii_name="resetInvocationType")
    def reset_invocation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvocationType", []))

    @jsii.member(jsii_name="resetNetworkType")
    def reset_network_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkType", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="backendParams")
    def backend_params(self) -> ApigwApiV2FuncGraphPolicyBackendParamsList:
        return typing.cast(ApigwApiV2FuncGraphPolicyBackendParamsList, jsii.get(self, "backendParams"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> ApigwApiV2FuncGraphPolicyConditionsList:
        return typing.cast(ApigwApiV2FuncGraphPolicyConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="authorizerIdInput")
    def authorizer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="backendParamsInput")
    def backend_params_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicyBackendParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicyBackendParams]]], jsii.get(self, "backendParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicyConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicyConditions]]], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="effectiveModeInput")
    def effective_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectiveModeInput"))

    @builtins.property
    @jsii.member(jsii_name="functionUrnInput")
    def function_urn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionUrnInput"))

    @builtins.property
    @jsii.member(jsii_name="invocationTypeInput")
    def invocation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "invocationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTypeInput")
    def network_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizerId"))

    @authorizer_id.setter
    def authorizer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f9ac70d20317549e1df74812f61c783b3f464a026392eb4fa297156dae24c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="effectiveMode")
    def effective_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveMode"))

    @effective_mode.setter
    def effective_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cfb177beb2b264f119d5118e1c565dbea793daf44fce5169aae96bb6c414199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectiveMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionUrn")
    def function_urn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionUrn"))

    @function_urn.setter
    def function_urn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827d692f3e6f411995c3d3c06315e0b73ecb62326d29a27e475d9930b5c61d43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionUrn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invocationType")
    def invocation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "invocationType"))

    @invocation_type.setter
    def invocation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8943f9352ccf55c8c56c1bb5cb64b45f599c4aed27a517a51c1ee1b886794c63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invocationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11b4fb7701d26bbc7182107d269e28c1e182b91ca333b250f00c7d64a133021b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkType")
    def network_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkType"))

    @network_type.setter
    def network_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20bcedb80fde4354fc0ff80c56c0cd7390aa89d7ed837ea6cb79b5dc7b5f42b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c99222a518c0bafba788ce2fc227ec56c1c3cfeba52d2cdce8b5c891cab45b47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0351a6158fb019c298a9e068374ed45a5d13712a696d7beca9d404ef979af3b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2FuncGraphPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2FuncGraphPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2FuncGraphPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cb37c3602efcd17eb7f549184b3da81060b3c86d23c83059b526401f084b0d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2Http",
    jsii_struct_bases=[],
    name_mapping={
        "request_method": "requestMethod",
        "request_uri": "requestUri",
        "authorizer_id": "authorizerId",
        "description": "description",
        "request_protocol": "requestProtocol",
        "retry_count": "retryCount",
        "ssl_enable": "sslEnable",
        "timeout": "timeout",
        "url_domain": "urlDomain",
        "version": "version",
        "vpc_channel_id": "vpcChannelId",
        "vpc_channel_proxy_host": "vpcChannelProxyHost",
    },
)
class ApigwApiV2Http:
    def __init__(
        self,
        *,
        request_method: builtins.str,
        request_uri: builtins.str,
        authorizer_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        request_protocol: typing.Optional[builtins.str] = None,
        retry_count: typing.Optional[jsii.Number] = None,
        ssl_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        url_domain: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        vpc_channel_id: typing.Optional[builtins.str] = None,
        vpc_channel_proxy_host: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param request_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_method ApigwApiV2#request_method}.
        :param request_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_uri ApigwApiV2#request_uri}.
        :param authorizer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.
        :param request_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_protocol ApigwApiV2#request_protocol}.
        :param retry_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#retry_count ApigwApiV2#retry_count}.
        :param ssl_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#ssl_enable ApigwApiV2#ssl_enable}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#timeout ApigwApiV2#timeout}.
        :param url_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#url_domain ApigwApiV2#url_domain}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#version ApigwApiV2#version}.
        :param vpc_channel_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#vpc_channel_id ApigwApiV2#vpc_channel_id}.
        :param vpc_channel_proxy_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#vpc_channel_proxy_host ApigwApiV2#vpc_channel_proxy_host}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0385464ccdb348a212f5d6f27a1fd87676e1c83ed335f21348e5029d3c8737f3)
            check_type(argname="argument request_method", value=request_method, expected_type=type_hints["request_method"])
            check_type(argname="argument request_uri", value=request_uri, expected_type=type_hints["request_uri"])
            check_type(argname="argument authorizer_id", value=authorizer_id, expected_type=type_hints["authorizer_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument request_protocol", value=request_protocol, expected_type=type_hints["request_protocol"])
            check_type(argname="argument retry_count", value=retry_count, expected_type=type_hints["retry_count"])
            check_type(argname="argument ssl_enable", value=ssl_enable, expected_type=type_hints["ssl_enable"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument url_domain", value=url_domain, expected_type=type_hints["url_domain"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument vpc_channel_id", value=vpc_channel_id, expected_type=type_hints["vpc_channel_id"])
            check_type(argname="argument vpc_channel_proxy_host", value=vpc_channel_proxy_host, expected_type=type_hints["vpc_channel_proxy_host"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "request_method": request_method,
            "request_uri": request_uri,
        }
        if authorizer_id is not None:
            self._values["authorizer_id"] = authorizer_id
        if description is not None:
            self._values["description"] = description
        if request_protocol is not None:
            self._values["request_protocol"] = request_protocol
        if retry_count is not None:
            self._values["retry_count"] = retry_count
        if ssl_enable is not None:
            self._values["ssl_enable"] = ssl_enable
        if timeout is not None:
            self._values["timeout"] = timeout
        if url_domain is not None:
            self._values["url_domain"] = url_domain
        if version is not None:
            self._values["version"] = version
        if vpc_channel_id is not None:
            self._values["vpc_channel_id"] = vpc_channel_id
        if vpc_channel_proxy_host is not None:
            self._values["vpc_channel_proxy_host"] = vpc_channel_proxy_host

    @builtins.property
    def request_method(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_method ApigwApiV2#request_method}.'''
        result = self._values.get("request_method")
        assert result is not None, "Required property 'request_method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_uri ApigwApiV2#request_uri}.'''
        result = self._values.get("request_uri")
        assert result is not None, "Required property 'request_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorizer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.'''
        result = self._values.get("authorizer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_protocol ApigwApiV2#request_protocol}.'''
        result = self._values.get("request_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#retry_count ApigwApiV2#retry_count}.'''
        result = self._values.get("retry_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ssl_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#ssl_enable ApigwApiV2#ssl_enable}.'''
        result = self._values.get("ssl_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#timeout ApigwApiV2#timeout}.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def url_domain(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#url_domain ApigwApiV2#url_domain}.'''
        result = self._values.get("url_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#version ApigwApiV2#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_channel_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#vpc_channel_id ApigwApiV2#vpc_channel_id}.'''
        result = self._values.get("vpc_channel_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_channel_proxy_host(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#vpc_channel_proxy_host ApigwApiV2#vpc_channel_proxy_host}.'''
        result = self._values.get("vpc_channel_proxy_host")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwApiV2Http(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwApiV2HttpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2HttpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f43e4664e2030889bca2add08bdfc515fd64f4331c497d34dc020275f6b43d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthorizerId")
    def reset_authorizer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizerId", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetRequestProtocol")
    def reset_request_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestProtocol", []))

    @jsii.member(jsii_name="resetRetryCount")
    def reset_retry_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryCount", []))

    @jsii.member(jsii_name="resetSslEnable")
    def reset_ssl_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslEnable", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetUrlDomain")
    def reset_url_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlDomain", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @jsii.member(jsii_name="resetVpcChannelId")
    def reset_vpc_channel_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcChannelId", []))

    @jsii.member(jsii_name="resetVpcChannelProxyHost")
    def reset_vpc_channel_proxy_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcChannelProxyHost", []))

    @builtins.property
    @jsii.member(jsii_name="authorizerIdInput")
    def authorizer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestMethodInput")
    def request_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="requestProtocolInput")
    def request_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="requestUriInput")
    def request_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestUriInput"))

    @builtins.property
    @jsii.member(jsii_name="retryCountInput")
    def retry_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryCountInput"))

    @builtins.property
    @jsii.member(jsii_name="sslEnableInput")
    def ssl_enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sslEnableInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="urlDomainInput")
    def url_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcChannelIdInput")
    def vpc_channel_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcChannelIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcChannelProxyHostInput")
    def vpc_channel_proxy_host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcChannelProxyHostInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizerId"))

    @authorizer_id.setter
    def authorizer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7fd8a32c8952a5738ff992f105f3fc4613f42ecc3695510dc80f33263bdc7ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f31487c8e6f4296e1758310698d47c15aec8ec5bb8f33ad48e102375a116986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestMethod")
    def request_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestMethod"))

    @request_method.setter
    def request_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d02381f797e70f63a0c948b0afd739f791c63767e8ebe588ce8abcdf2def74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestProtocol")
    def request_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestProtocol"))

    @request_protocol.setter
    def request_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e822fd6f658d0ebe14ea4982f11f617872b06b622bd58ed4c3bdc209f6530b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestUri")
    def request_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestUri"))

    @request_uri.setter
    def request_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d00b2ba527d28d76699f73f79a574dd29c18adccab33c54a29798327b94a97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryCount")
    def retry_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryCount"))

    @retry_count.setter
    def retry_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a2d8cd4643e508cd5c9c16695bd9a0f6e3904d5c743c3910673bdb27a9c2ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslEnable")
    def ssl_enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sslEnable"))

    @ssl_enable.setter
    def ssl_enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e02e8855bafcb003277a732af70b871cf36b12093067a87945cb5dcfa28747)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslEnable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c732dbada4fe58b11ba8ecbb1fd2be9938644a0fd4ffdcb067f812986a69b811)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlDomain")
    def url_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlDomain"))

    @url_domain.setter
    def url_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325acbad61f6f5380ed6e855458781db5937a3afffe7c63660ba2bf331a0a30c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e35b364083469479825d8da27694c548b262c87a929e0e35c9cc94ee2632d26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcChannelId")
    def vpc_channel_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcChannelId"))

    @vpc_channel_id.setter
    def vpc_channel_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aaa4b6748cc829578c24dfc826facbf637e3ca99397385ef6f57abe4e69c8d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcChannelId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcChannelProxyHost")
    def vpc_channel_proxy_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcChannelProxyHost"))

    @vpc_channel_proxy_host.setter
    def vpc_channel_proxy_host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f2414bd1becd3f4b4b44d599121d755355a042695a7ece1046a14f5c8fc05ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcChannelProxyHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigwApiV2Http]:
        return typing.cast(typing.Optional[ApigwApiV2Http], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApigwApiV2Http]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc47b491fa0051f9e3d643bac4f3b6d8b52c3861f3f0a87049c2e1ecba707db9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2HttpPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "conditions": "conditions",
        "name": "name",
        "request_method": "requestMethod",
        "request_uri": "requestUri",
        "authorizer_id": "authorizerId",
        "backend_params": "backendParams",
        "effective_mode": "effectiveMode",
        "request_protocol": "requestProtocol",
        "retry_count": "retryCount",
        "timeout": "timeout",
        "url_domain": "urlDomain",
        "vpc_channel_id": "vpcChannelId",
        "vpc_channel_proxy_host": "vpcChannelProxyHost",
    },
)
class ApigwApiV2HttpPolicy:
    def __init__(
        self,
        *,
        conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2HttpPolicyConditions", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        request_method: builtins.str,
        request_uri: builtins.str,
        authorizer_id: typing.Optional[builtins.str] = None,
        backend_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2HttpPolicyBackendParams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        effective_mode: typing.Optional[builtins.str] = None,
        request_protocol: typing.Optional[builtins.str] = None,
        retry_count: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[jsii.Number] = None,
        url_domain: typing.Optional[builtins.str] = None,
        vpc_channel_id: typing.Optional[builtins.str] = None,
        vpc_channel_proxy_host: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#conditions ApigwApiV2#conditions}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.
        :param request_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_method ApigwApiV2#request_method}.
        :param request_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_uri ApigwApiV2#request_uri}.
        :param authorizer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.
        :param backend_params: backend_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#backend_params ApigwApiV2#backend_params}
        :param effective_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#effective_mode ApigwApiV2#effective_mode}.
        :param request_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_protocol ApigwApiV2#request_protocol}.
        :param retry_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#retry_count ApigwApiV2#retry_count}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#timeout ApigwApiV2#timeout}.
        :param url_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#url_domain ApigwApiV2#url_domain}.
        :param vpc_channel_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#vpc_channel_id ApigwApiV2#vpc_channel_id}.
        :param vpc_channel_proxy_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#vpc_channel_proxy_host ApigwApiV2#vpc_channel_proxy_host}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4d0cae3e4c7aad1f5dc7044f8921394f4badb235752e79d0b31b2dc41d3f59)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument request_method", value=request_method, expected_type=type_hints["request_method"])
            check_type(argname="argument request_uri", value=request_uri, expected_type=type_hints["request_uri"])
            check_type(argname="argument authorizer_id", value=authorizer_id, expected_type=type_hints["authorizer_id"])
            check_type(argname="argument backend_params", value=backend_params, expected_type=type_hints["backend_params"])
            check_type(argname="argument effective_mode", value=effective_mode, expected_type=type_hints["effective_mode"])
            check_type(argname="argument request_protocol", value=request_protocol, expected_type=type_hints["request_protocol"])
            check_type(argname="argument retry_count", value=retry_count, expected_type=type_hints["retry_count"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument url_domain", value=url_domain, expected_type=type_hints["url_domain"])
            check_type(argname="argument vpc_channel_id", value=vpc_channel_id, expected_type=type_hints["vpc_channel_id"])
            check_type(argname="argument vpc_channel_proxy_host", value=vpc_channel_proxy_host, expected_type=type_hints["vpc_channel_proxy_host"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "conditions": conditions,
            "name": name,
            "request_method": request_method,
            "request_uri": request_uri,
        }
        if authorizer_id is not None:
            self._values["authorizer_id"] = authorizer_id
        if backend_params is not None:
            self._values["backend_params"] = backend_params
        if effective_mode is not None:
            self._values["effective_mode"] = effective_mode
        if request_protocol is not None:
            self._values["request_protocol"] = request_protocol
        if retry_count is not None:
            self._values["retry_count"] = retry_count
        if timeout is not None:
            self._values["timeout"] = timeout
        if url_domain is not None:
            self._values["url_domain"] = url_domain
        if vpc_channel_id is not None:
            self._values["vpc_channel_id"] = vpc_channel_id
        if vpc_channel_proxy_host is not None:
            self._values["vpc_channel_proxy_host"] = vpc_channel_proxy_host

    @builtins.property
    def conditions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2HttpPolicyConditions"]]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#conditions ApigwApiV2#conditions}
        '''
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2HttpPolicyConditions"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_method(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_method ApigwApiV2#request_method}.'''
        result = self._values.get("request_method")
        assert result is not None, "Required property 'request_method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_uri ApigwApiV2#request_uri}.'''
        result = self._values.get("request_uri")
        assert result is not None, "Required property 'request_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorizer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.'''
        result = self._values.get("authorizer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backend_params(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2HttpPolicyBackendParams"]]]:
        '''backend_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#backend_params ApigwApiV2#backend_params}
        '''
        result = self._values.get("backend_params")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2HttpPolicyBackendParams"]]], result)

    @builtins.property
    def effective_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#effective_mode ApigwApiV2#effective_mode}.'''
        result = self._values.get("effective_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#request_protocol ApigwApiV2#request_protocol}.'''
        result = self._values.get("request_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#retry_count ApigwApiV2#retry_count}.'''
        result = self._values.get("retry_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#timeout ApigwApiV2#timeout}.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def url_domain(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#url_domain ApigwApiV2#url_domain}.'''
        result = self._values.get("url_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_channel_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#vpc_channel_id ApigwApiV2#vpc_channel_id}.'''
        result = self._values.get("vpc_channel_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_channel_proxy_host(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#vpc_channel_proxy_host ApigwApiV2#vpc_channel_proxy_host}.'''
        result = self._values.get("vpc_channel_proxy_host")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwApiV2HttpPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2HttpPolicyBackendParams",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "name": "name",
        "type": "type",
        "value": "value",
        "description": "description",
        "system_param_type": "systemParamType",
    },
)
class ApigwApiV2HttpPolicyBackendParams:
    def __init__(
        self,
        *,
        location: builtins.str,
        name: builtins.str,
        type: builtins.str,
        value: builtins.str,
        description: typing.Optional[builtins.str] = None,
        system_param_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#location ApigwApiV2#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#value ApigwApiV2#value}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.
        :param system_param_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#system_param_type ApigwApiV2#system_param_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__522cf78c24bdfe5661b3ab5479c54138886841f1f4e83aee23485e99348882c2)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument system_param_type", value=system_param_type, expected_type=type_hints["system_param_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "type": type,
            "value": value,
        }
        if description is not None:
            self._values["description"] = description
        if system_param_type is not None:
            self._values["system_param_type"] = system_param_type

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#location ApigwApiV2#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#value ApigwApiV2#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_param_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#system_param_type ApigwApiV2#system_param_type}.'''
        result = self._values.get("system_param_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwApiV2HttpPolicyBackendParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwApiV2HttpPolicyBackendParamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2HttpPolicyBackendParamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f47552ef548408b3fa47f9ca9c3cc8f678967882d5374da6bc6617b9fa1ec083)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigwApiV2HttpPolicyBackendParamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f0e75ca94718e88ab3715aaf220221a193c2cdd24a79c934988acf31257ab6d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigwApiV2HttpPolicyBackendParamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e21f006ed2cc135bded700d9c3a52bd1b5b459c9f36dc9d5c2bfa06659a08b34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13fca870eb4fb2b46c1ac24fdebaee68b9c6401a4c4fba467fe6b6e380ea64ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5074bc7ad611696ffcffeebd24d8bc5b85efeefe09026d5f944e0d85654f14d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicyBackendParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicyBackendParams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicyBackendParams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0890f43f5c258f7913d28cf59b7f48923cc24b10e1a38897075052ed48b4bd89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwApiV2HttpPolicyBackendParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2HttpPolicyBackendParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7389b11642351758ab952a4c8578d46d2809980bb9ad9bb0904139dbaedf15f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetSystemParamType")
    def reset_system_param_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemParamType", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="systemParamTypeInput")
    def system_param_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemParamTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716b07fd935475ba36cb86eba88cef4fe732bf130473ecc5d44d7becf22fbd60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39705b94f1280e24b8808360808cac39fbbfc984af79919dfaf3f85ed8f41c27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70afb42cadcd3b3e22fc2f73bbad37c4b07ab7ba204364fd7ac12f872e8d39d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemParamType")
    def system_param_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemParamType"))

    @system_param_type.setter
    def system_param_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb01f21f757363da5e2a2d0d0a1e29bac8e8dee91a2767c49ce8bd5decab2760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemParamType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56b95576c126dd2e1f493c1dd4463e471b56cc014dfc3cd14b592e56e1ce1405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcaabcbc44272984e8976d00771987012df2c7356bd4f62185a351aa1fb04d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2HttpPolicyBackendParams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2HttpPolicyBackendParams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2HttpPolicyBackendParams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70c04cec34fe56f6683a6aad50b74cea8631440816f2d461b587b7daeea8b6d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2HttpPolicyConditions",
    jsii_struct_bases=[],
    name_mapping={
        "value": "value",
        "origin": "origin",
        "param_name": "paramName",
        "type": "type",
    },
)
class ApigwApiV2HttpPolicyConditions:
    def __init__(
        self,
        *,
        value: builtins.str,
        origin: typing.Optional[builtins.str] = None,
        param_name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#value ApigwApiV2#value}.
        :param origin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#origin ApigwApiV2#origin}.
        :param param_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#param_name ApigwApiV2#param_name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc0530b1efdf3e1705d23b346fedc8d5b8d4049c23f595b3fbae19f573ec322b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            check_type(argname="argument param_name", value=param_name, expected_type=type_hints["param_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if origin is not None:
            self._values["origin"] = origin
        if param_name is not None:
            self._values["param_name"] = param_name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#value ApigwApiV2#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#origin ApigwApiV2#origin}.'''
        result = self._values.get("origin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def param_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#param_name ApigwApiV2#param_name}.'''
        result = self._values.get("param_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwApiV2HttpPolicyConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwApiV2HttpPolicyConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2HttpPolicyConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdd370eac994d897a35450758f72a6318166a35a9d7061094fa0d4f9f1c60e01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigwApiV2HttpPolicyConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6bbc5d7b0f334550197be6155d91f04f5c0c4df7c4d0736166e43f9d58930bb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigwApiV2HttpPolicyConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__260cc7384f9a757539635fc7e9c1677fd99a5eca74535f8ba0cf617cd800ec0f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5622175bcd379e75bc8243388820ae8e87b6c69ee5f7ed58d30899e8e0575795)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80141b8b10f364423194a7d69453cec08a1c0f8995ebbfa9640545ae163a84f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicyConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicyConditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicyConditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a225d5fb51c5b2b09a82431afec06b29ae5c3e67b2634514ef8b5315f67be31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwApiV2HttpPolicyConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2HttpPolicyConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8155b4f0d3a9a4a6c372cad9e0afe16a6d56c2289a950cd3eea24bd3825e0182)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOrigin")
    def reset_origin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrigin", []))

    @jsii.member(jsii_name="resetParamName")
    def reset_param_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParamName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="originInput")
    def origin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originInput"))

    @builtins.property
    @jsii.member(jsii_name="paramNameInput")
    def param_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "paramNameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="origin")
    def origin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "origin"))

    @origin.setter
    def origin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__295ec024c2e888d579344ddda33fa121bfb51c9927c5b9fad8ca278aca61dd2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "origin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paramName")
    def param_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "paramName"))

    @param_name.setter
    def param_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__242d7fcd31a6c9b2f464658290f84cb0f80f4b801f047a0582a0d2552931d349)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paramName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eedb5aca2b9049442eeb34d5f26b32d8080d67038156a0599cc520bc8a7f463d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25f07f3bd7ac3ba2d1292780ca7b914808da3b4dfa995fa42e8a1c715fce57cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2HttpPolicyConditions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2HttpPolicyConditions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2HttpPolicyConditions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eabba317efdfa8d4610e0b67862bebb1c3a328e0bdfc26551cc7f70abbb732c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwApiV2HttpPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2HttpPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aff780ed5b554c13aaf3f9a57336d1805ab056201a056c7e5cc2d76d469496b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApigwApiV2HttpPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5646ca144ff73a39d76be7043cbebf6011c560c23442de5d7fb747e519d1ca82)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigwApiV2HttpPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7956f9a42996cd77e489b51b8de76f45568f06c2303b5d9832b3696cc699b517)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9454bcc5209ea5a438d71a06e481f3e7fac9e1c3330c6116dd2e153e44cfab95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3618fb618feda5d750819f6c17a4a6b1a12c65a74ef9e2dfc2ca08ecd5421f9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225fb858d733cf10827647ab3fe5fc5bdea7966b7fd5208d5d7918992207d081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwApiV2HttpPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2HttpPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d7edcaf8dc4420f766d8f70283badba073e5cdfcaf65a0548e46bb5aa8b2ac0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBackendParams")
    def put_backend_params(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2HttpPolicyBackendParams, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552a8dc86d3fd1a1e12170283902da79b68ae71f56b59dad58dbca36e353b7fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackendParams", [value]))

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2HttpPolicyConditions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec4e93afdb989b837bbafff3a18ced142f194474ac12e0183c74e0ba9ac7a6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="resetAuthorizerId")
    def reset_authorizer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizerId", []))

    @jsii.member(jsii_name="resetBackendParams")
    def reset_backend_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendParams", []))

    @jsii.member(jsii_name="resetEffectiveMode")
    def reset_effective_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffectiveMode", []))

    @jsii.member(jsii_name="resetRequestProtocol")
    def reset_request_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestProtocol", []))

    @jsii.member(jsii_name="resetRetryCount")
    def reset_retry_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryCount", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetUrlDomain")
    def reset_url_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlDomain", []))

    @jsii.member(jsii_name="resetVpcChannelId")
    def reset_vpc_channel_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcChannelId", []))

    @jsii.member(jsii_name="resetVpcChannelProxyHost")
    def reset_vpc_channel_proxy_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcChannelProxyHost", []))

    @builtins.property
    @jsii.member(jsii_name="backendParams")
    def backend_params(self) -> ApigwApiV2HttpPolicyBackendParamsList:
        return typing.cast(ApigwApiV2HttpPolicyBackendParamsList, jsii.get(self, "backendParams"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> ApigwApiV2HttpPolicyConditionsList:
        return typing.cast(ApigwApiV2HttpPolicyConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="authorizerIdInput")
    def authorizer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="backendParamsInput")
    def backend_params_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicyBackendParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicyBackendParams]]], jsii.get(self, "backendParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicyConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicyConditions]]], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="effectiveModeInput")
    def effective_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectiveModeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="requestMethodInput")
    def request_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="requestProtocolInput")
    def request_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="requestUriInput")
    def request_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestUriInput"))

    @builtins.property
    @jsii.member(jsii_name="retryCountInput")
    def retry_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryCountInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="urlDomainInput")
    def url_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcChannelIdInput")
    def vpc_channel_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcChannelIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcChannelProxyHostInput")
    def vpc_channel_proxy_host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcChannelProxyHostInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizerId"))

    @authorizer_id.setter
    def authorizer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d67c4742aaf8f1078aea28eaf64fb16492dbe2833613f758c7b931b872dae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="effectiveMode")
    def effective_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveMode"))

    @effective_mode.setter
    def effective_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89de32e1f0439932541da57db36bd8c9e39f578fccc3d15e0f4a1453f8f88f67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectiveMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b91dd79a87e3973be62a2e436159ee492f32f2e7a5d11c328a6378172d5b6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestMethod")
    def request_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestMethod"))

    @request_method.setter
    def request_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff2add9c0461d38988504365b3d454560cd0a564f8231cdbd077971608058763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestProtocol")
    def request_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestProtocol"))

    @request_protocol.setter
    def request_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077c981087a3e01c52a2284708147cad49be5afaf2daf5deb50bb873e0bc1750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestUri")
    def request_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestUri"))

    @request_uri.setter
    def request_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecee390c6a90262927c35d81c96d3c9173d3ddbade5a0ab43e831ee6f237f22c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryCount")
    def retry_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryCount"))

    @retry_count.setter
    def retry_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999bea44ddb68d517c3ea5d02736738321ca6ed9ade36a280200a6f878d04c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c77d1fa4a65f7a10a7bc0cf8080bcacade2886eb54abd2140dc6ae849d382d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlDomain")
    def url_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlDomain"))

    @url_domain.setter
    def url_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d076dbd0f15ff2f9f2b31918b7259a002e53f790555925900e220df50e2916c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcChannelId")
    def vpc_channel_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcChannelId"))

    @vpc_channel_id.setter
    def vpc_channel_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef3aca9fe000cc2bac2ab0a93d42279144c64b558d45dcd94bf5456f28a0014b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcChannelId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcChannelProxyHost")
    def vpc_channel_proxy_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcChannelProxyHost"))

    @vpc_channel_proxy_host.setter
    def vpc_channel_proxy_host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be10bc62066ff4d97787ec58cc285aec2e48b7c9f08dc7570613c9a7c7c7df99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcChannelProxyHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2HttpPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2HttpPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2HttpPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__612944840153b8443ed9cfcc1f4f245df91355295bf52203140b6981c1b75407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2Mock",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_id": "authorizerId",
        "description": "description",
        "response": "response",
        "version": "version",
    },
)
class ApigwApiV2Mock:
    def __init__(
        self,
        *,
        authorizer_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        response: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.
        :param response: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#response ApigwApiV2#response}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#version ApigwApiV2#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0886d4fd7625ac26691bc62dc111cb3fc16d530271e7fb01db391c060c66fda)
            check_type(argname="argument authorizer_id", value=authorizer_id, expected_type=type_hints["authorizer_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument response", value=response, expected_type=type_hints["response"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorizer_id is not None:
            self._values["authorizer_id"] = authorizer_id
        if description is not None:
            self._values["description"] = description
        if response is not None:
            self._values["response"] = response
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def authorizer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.'''
        result = self._values.get("authorizer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#response ApigwApiV2#response}.'''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#version ApigwApiV2#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwApiV2Mock(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwApiV2MockOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2MockOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e4c1250dd2bebad73898ca9ef93d6fb6fc84d4e80703065ca6f09c1e71be347)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthorizerId")
    def reset_authorizer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizerId", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetResponse")
    def reset_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponse", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="authorizerIdInput")
    def authorizer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="responseInput")
    def response_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizerId"))

    @authorizer_id.setter
    def authorizer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0afcbb390f978c5c4449352ef830ad4adadc03e970514950dfcc28d68a1475c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17279539694b334d980f7bc79011a87709b66ccaf0c4c127e142bf871354629b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b54e39ff34b4cd3f86578b39957c16418dcec0fc2f07d1af1e11bef23ea85b72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85324bb4808fff1be1b30e13c40b1e5b54a20f02d2a7c2f1498a1454d09478cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigwApiV2Mock]:
        return typing.cast(typing.Optional[ApigwApiV2Mock], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApigwApiV2Mock]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d73fd0a87b0f3c2c3684b62b41e0615155b9f77ec0f1296a7c9fb9beba570fb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2MockPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "conditions": "conditions",
        "name": "name",
        "authorizer_id": "authorizerId",
        "backend_params": "backendParams",
        "effective_mode": "effectiveMode",
        "response": "response",
    },
)
class ApigwApiV2MockPolicy:
    def __init__(
        self,
        *,
        conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2MockPolicyConditions", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        authorizer_id: typing.Optional[builtins.str] = None,
        backend_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwApiV2MockPolicyBackendParams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        effective_mode: typing.Optional[builtins.str] = None,
        response: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#conditions ApigwApiV2#conditions}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.
        :param authorizer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.
        :param backend_params: backend_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#backend_params ApigwApiV2#backend_params}
        :param effective_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#effective_mode ApigwApiV2#effective_mode}.
        :param response: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#response ApigwApiV2#response}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59d3eb1e46a9e3ad5bfc64ef0f4349f50e716969d25fa6e406bbc354fa3ed7d5)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument authorizer_id", value=authorizer_id, expected_type=type_hints["authorizer_id"])
            check_type(argname="argument backend_params", value=backend_params, expected_type=type_hints["backend_params"])
            check_type(argname="argument effective_mode", value=effective_mode, expected_type=type_hints["effective_mode"])
            check_type(argname="argument response", value=response, expected_type=type_hints["response"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "conditions": conditions,
            "name": name,
        }
        if authorizer_id is not None:
            self._values["authorizer_id"] = authorizer_id
        if backend_params is not None:
            self._values["backend_params"] = backend_params
        if effective_mode is not None:
            self._values["effective_mode"] = effective_mode
        if response is not None:
            self._values["response"] = response

    @builtins.property
    def conditions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2MockPolicyConditions"]]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#conditions ApigwApiV2#conditions}
        '''
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2MockPolicyConditions"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorizer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#authorizer_id ApigwApiV2#authorizer_id}.'''
        result = self._values.get("authorizer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backend_params(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2MockPolicyBackendParams"]]]:
        '''backend_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#backend_params ApigwApiV2#backend_params}
        '''
        result = self._values.get("backend_params")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwApiV2MockPolicyBackendParams"]]], result)

    @builtins.property
    def effective_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#effective_mode ApigwApiV2#effective_mode}.'''
        result = self._values.get("effective_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#response ApigwApiV2#response}.'''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwApiV2MockPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2MockPolicyBackendParams",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "name": "name",
        "type": "type",
        "value": "value",
        "description": "description",
        "system_param_type": "systemParamType",
    },
)
class ApigwApiV2MockPolicyBackendParams:
    def __init__(
        self,
        *,
        location: builtins.str,
        name: builtins.str,
        type: builtins.str,
        value: builtins.str,
        description: typing.Optional[builtins.str] = None,
        system_param_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#location ApigwApiV2#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#value ApigwApiV2#value}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.
        :param system_param_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#system_param_type ApigwApiV2#system_param_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5edea3f4928c0c9dc1ad430e3c01f2e8ace1af7df2db8131513657ef35487b37)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument system_param_type", value=system_param_type, expected_type=type_hints["system_param_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "type": type,
            "value": value,
        }
        if description is not None:
            self._values["description"] = description
        if system_param_type is not None:
            self._values["system_param_type"] = system_param_type

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#location ApigwApiV2#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#value ApigwApiV2#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_param_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#system_param_type ApigwApiV2#system_param_type}.'''
        result = self._values.get("system_param_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwApiV2MockPolicyBackendParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwApiV2MockPolicyBackendParamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2MockPolicyBackendParamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e3060d669a9fe60eb180e5d452069a4385ced297df11796ee53f4cc47e18b00)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigwApiV2MockPolicyBackendParamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ceeb27b6f5ee7a389cec074127d5ac18b47deebba88698a3e06bece1c89674)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigwApiV2MockPolicyBackendParamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__462040fd6921beba93862362fa699c721e78176fed141a29196d3111803f1110)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1801a261140c923227295c143f3f96a0aae8b78ced4dad3ac895d586b6b3839f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f94e8650c166b4bc34f61a9c570ff5265fe7bd08febedee0fe39664e39a7f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicyBackendParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicyBackendParams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicyBackendParams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dda8d92b6f9f9f9a925b2c842f4178f33a36f5d1aa1c9ae58fb686dab07380e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwApiV2MockPolicyBackendParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2MockPolicyBackendParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d6165bf5cbda001e9cfcef3ea9f51598b2e61424f3994214d3c4eb127a5d372)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetSystemParamType")
    def reset_system_param_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemParamType", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="systemParamTypeInput")
    def system_param_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemParamTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__089760d58721a57ae2664aa4357739bd39051e67cfe5ea1188fa2a75d4bf8d68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8596e04d63675f2a2b2ff1e3a9b92efbf340347f0f6624229d9f4abc2aed0969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e080105a535f1b3acc4a7330c75c90c75ca727313284f142093a8fbc0e17408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemParamType")
    def system_param_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemParamType"))

    @system_param_type.setter
    def system_param_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__314a1590e6a41b584502d5f1d3b7b8a9cb58d4ec195368d4ba782e246add16d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemParamType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a78ca8d31bbbaa2a850963a802e1bb75a5010aab4ac556fcb4a52df3bd2dc05e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c4e828a0e326b48da61a7f3895b275512ed90735545f1ba940926b9a63421e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2MockPolicyBackendParams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2MockPolicyBackendParams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2MockPolicyBackendParams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d784d91c83a8a0ef02ec43a3d2dcb63ee4c738911b35fc3cf8d7d5d4d1ae2f2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2MockPolicyConditions",
    jsii_struct_bases=[],
    name_mapping={
        "value": "value",
        "origin": "origin",
        "param_name": "paramName",
        "type": "type",
    },
)
class ApigwApiV2MockPolicyConditions:
    def __init__(
        self,
        *,
        value: builtins.str,
        origin: typing.Optional[builtins.str] = None,
        param_name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#value ApigwApiV2#value}.
        :param origin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#origin ApigwApiV2#origin}.
        :param param_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#param_name ApigwApiV2#param_name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__208c2dc27284be917c71c2d4c279618770f0eb8366b0e257200e4126164687aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            check_type(argname="argument param_name", value=param_name, expected_type=type_hints["param_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if origin is not None:
            self._values["origin"] = origin
        if param_name is not None:
            self._values["param_name"] = param_name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#value ApigwApiV2#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#origin ApigwApiV2#origin}.'''
        result = self._values.get("origin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def param_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#param_name ApigwApiV2#param_name}.'''
        result = self._values.get("param_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwApiV2MockPolicyConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwApiV2MockPolicyConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2MockPolicyConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8a96c9dbd581761011dd9a467389573958e34baae10daa8d2dbcc2fbef67846)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigwApiV2MockPolicyConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f715900c476cb3e260a9e8713d3ee6a935fe153004bc88622f02c096cc12e50d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigwApiV2MockPolicyConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a7b0c1f21efc95d80d89ca4c7b601616ca8495f41687008d5a20cd99f2df6cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__113c0a666d9743c1a1eb4f45b885877d7d8796fa0433808b2683aa4bc58d7344)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1298e1e5f1eaf304e4b33033ee5eb6bbd1781ef9b8f6123949f62cce8d567918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicyConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicyConditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicyConditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b8cc5ed21ae3f4bfa4e630794936dcfec8b94c6bc252d224ccdf114d1850a4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwApiV2MockPolicyConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2MockPolicyConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a90cf05f8cce9563a2327ed2f902921a181d11a72aff4ed68848df2782c0ab2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOrigin")
    def reset_origin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrigin", []))

    @jsii.member(jsii_name="resetParamName")
    def reset_param_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParamName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="originInput")
    def origin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originInput"))

    @builtins.property
    @jsii.member(jsii_name="paramNameInput")
    def param_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "paramNameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="origin")
    def origin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "origin"))

    @origin.setter
    def origin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22559387adcd61b01e8bc5f892d63eaa2abde6d5bf6039932ef79315cee7cccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "origin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paramName")
    def param_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "paramName"))

    @param_name.setter
    def param_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a23d41af9bb8c84037b029ed7122e6295bad07aff398561e750364647d2c40ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paramName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77bf6bd8170882adb26cd1da4b5fc51160960f4fe579984a908da6b1b8c52f41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c8519b2215f38b497fcae29918d76e6e1279c776b826ba10f7441154129959)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2MockPolicyConditions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2MockPolicyConditions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2MockPolicyConditions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86eff74f34109aedacda209c7f12d0dd6929c9b1c632b7c091855994c470097d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwApiV2MockPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2MockPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__687adc94ddbcca1cba88ebf3928323a333633ab44e54e673e623bc25e5e33f40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApigwApiV2MockPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed504668a80f68e450bb5e09a118eda6a5f8cf7f570ab56aa99cf37dfe63b29a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigwApiV2MockPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8fd586d051647a127363fbd15f86139e508a96eec96417e1f55d07b72eb0e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2507bdd8023b9b23d4d9d48a7e049ea77484c5ed7dcbb4e4f663f11b7b5adb34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3576735318a9840c38d0cde73e49bdecea6fc64b8f197520c7c5514685cf459)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d4757ea11d812dd9f713bb3d141f3c42a0dee5b45610b02ae0c056de4fe4d99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwApiV2MockPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2MockPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac7ff6ea0ff12b66e8e179bf2403182bdb7a6d8492337fd13d451ba7cbe7a19d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBackendParams")
    def put_backend_params(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2MockPolicyBackendParams, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d90add921ca472a22bb2d3ddc9127b649af00dabdf0546239c21867566796b18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackendParams", [value]))

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2MockPolicyConditions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__270528180ec17df945058bc0b16a81ea48eedd4dbd71321a0be986d94c9ee91f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="resetAuthorizerId")
    def reset_authorizer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizerId", []))

    @jsii.member(jsii_name="resetBackendParams")
    def reset_backend_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendParams", []))

    @jsii.member(jsii_name="resetEffectiveMode")
    def reset_effective_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffectiveMode", []))

    @jsii.member(jsii_name="resetResponse")
    def reset_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponse", []))

    @builtins.property
    @jsii.member(jsii_name="backendParams")
    def backend_params(self) -> ApigwApiV2MockPolicyBackendParamsList:
        return typing.cast(ApigwApiV2MockPolicyBackendParamsList, jsii.get(self, "backendParams"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> ApigwApiV2MockPolicyConditionsList:
        return typing.cast(ApigwApiV2MockPolicyConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="authorizerIdInput")
    def authorizer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="backendParamsInput")
    def backend_params_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicyBackendParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicyBackendParams]]], jsii.get(self, "backendParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicyConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicyConditions]]], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="effectiveModeInput")
    def effective_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectiveModeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="responseInput")
    def response_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizerId"))

    @authorizer_id.setter
    def authorizer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61c70db185226d4543b6d8afe3a75f11d65d2e7d82c87e2631d620bba8fb5ca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="effectiveMode")
    def effective_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveMode"))

    @effective_mode.setter
    def effective_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af98e0f5b94abec146487d46663e726d38ee284dd7e890e77139e6c237f256b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectiveMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed0508d4f22842dd9360f498d67646e487589f79ef37496980760fa05afa726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce11ecdfa62669a3d791409b01e5b9160732666dad299a098a5392aa4ea6890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2MockPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2MockPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2MockPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6352e8f2144cebda73a68c1ad02f67e62db4311267ee12bd143da5d69a61299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2RequestParams",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "default": "default",
        "description": "description",
        "enumeration": "enumeration",
        "location": "location",
        "maximum": "maximum",
        "minimum": "minimum",
        "passthrough": "passthrough",
        "required": "required",
        "sample": "sample",
        "type": "type",
        "validity_check": "validityCheck",
    },
)
class ApigwApiV2RequestParams:
    def __init__(
        self,
        *,
        name: builtins.str,
        default: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enumeration: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        maximum: typing.Optional[jsii.Number] = None,
        minimum: typing.Optional[jsii.Number] = None,
        passthrough: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sample: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        validity_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#default ApigwApiV2#default}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.
        :param enumeration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#enumeration ApigwApiV2#enumeration}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#location ApigwApiV2#location}.
        :param maximum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#maximum ApigwApiV2#maximum}.
        :param minimum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#minimum ApigwApiV2#minimum}.
        :param passthrough: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#passthrough ApigwApiV2#passthrough}.
        :param required: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#required ApigwApiV2#required}.
        :param sample: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#sample ApigwApiV2#sample}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.
        :param validity_check: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#validity_check ApigwApiV2#validity_check}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__392fc4acf6a9c4ebf36224fb588decd0ef1366df0c96512dc53081ae78900023)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enumeration", value=enumeration, expected_type=type_hints["enumeration"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument maximum", value=maximum, expected_type=type_hints["maximum"])
            check_type(argname="argument minimum", value=minimum, expected_type=type_hints["minimum"])
            check_type(argname="argument passthrough", value=passthrough, expected_type=type_hints["passthrough"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            check_type(argname="argument sample", value=sample, expected_type=type_hints["sample"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument validity_check", value=validity_check, expected_type=type_hints["validity_check"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if default is not None:
            self._values["default"] = default
        if description is not None:
            self._values["description"] = description
        if enumeration is not None:
            self._values["enumeration"] = enumeration
        if location is not None:
            self._values["location"] = location
        if maximum is not None:
            self._values["maximum"] = maximum
        if minimum is not None:
            self._values["minimum"] = minimum
        if passthrough is not None:
            self._values["passthrough"] = passthrough
        if required is not None:
            self._values["required"] = required
        if sample is not None:
            self._values["sample"] = sample
        if type is not None:
            self._values["type"] = type
        if validity_check is not None:
            self._values["validity_check"] = validity_check

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#name ApigwApiV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#default ApigwApiV2#default}.'''
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#description ApigwApiV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enumeration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#enumeration ApigwApiV2#enumeration}.'''
        result = self._values.get("enumeration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#location ApigwApiV2#location}.'''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maximum(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#maximum ApigwApiV2#maximum}.'''
        result = self._values.get("maximum")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#minimum ApigwApiV2#minimum}.'''
        result = self._values.get("minimum")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def passthrough(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#passthrough ApigwApiV2#passthrough}.'''
        result = self._values.get("passthrough")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#required ApigwApiV2#required}.'''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sample(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#sample ApigwApiV2#sample}.'''
        result = self._values.get("sample")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#type ApigwApiV2#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validity_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_api_v2#validity_check ApigwApiV2#validity_check}.'''
        result = self._values.get("validity_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwApiV2RequestParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwApiV2RequestParamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2RequestParamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49e6cfe466fd18ed11e1d2d2921b3083e613dea2d93432cd2f92af8686946c88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApigwApiV2RequestParamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4f197546f8a6a4adc41de6ecd94865dfcc1154628723d4bae021d1a2fcb4d77)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigwApiV2RequestParamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74866b128025a2ea1285224af8d7249e3000fc5466441dd4e456edf36ab693b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__880ad7a2db8fdf588287916a7ed659b21867743ea4a8753324c3edd6a1ddd474)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a1673b472440aaa141289a73d71f8db8a0eda3bbbd9caa57f6656fadd80f9fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2RequestParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2RequestParams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2RequestParams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618cee9c564fb1c1a9b9f998d0c5cecc415115b37ef1f4d2e86833389f2cbd60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwApiV2RequestParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwApiV2.ApigwApiV2RequestParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__761d9e0251a2ef4706884267238a58d9e6051198686b181f515305f98d707feb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDefault")
    def reset_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefault", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnumeration")
    def reset_enumeration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnumeration", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetMaximum")
    def reset_maximum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximum", []))

    @jsii.member(jsii_name="resetMinimum")
    def reset_minimum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimum", []))

    @jsii.member(jsii_name="resetPassthrough")
    def reset_passthrough(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassthrough", []))

    @jsii.member(jsii_name="resetRequired")
    def reset_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequired", []))

    @jsii.member(jsii_name="resetSample")
    def reset_sample(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSample", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValidityCheck")
    def reset_validity_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidityCheck", []))

    @builtins.property
    @jsii.member(jsii_name="defaultInput")
    def default_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enumerationInput")
    def enumeration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enumerationInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumInput")
    def maximum_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumInput")
    def minimum_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passthroughInput")
    def passthrough_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passthroughInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredInput")
    def required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleInput")
    def sample_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sampleInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="validityCheckInput")
    def validity_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "validityCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @default.setter
    def default(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e1a61e432e49d6b38d1d767af203caa510df46b85184de951af705a8cc3a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a795a18740dbbf644a6e2f7c6214f63f735c97d5dceb830961de331fb1e75eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enumeration")
    def enumeration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enumeration"))

    @enumeration.setter
    def enumeration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6078c179c6abc6dcde88a0c2c8f954d5002dc4b3b16b65d43ef4bcde3aa0fa7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enumeration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0b8b1f0c8400813c41038d6ef093e961a8d55ae9c5a43b9304952dd1cb3922d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximum")
    def maximum(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximum"))

    @maximum.setter
    def maximum(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c36e7932defd16b53184fd650695690a545d481ab009815194b3de899ee12365)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimum")
    def minimum(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimum"))

    @minimum.setter
    def minimum(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39329a8d809a2f1fc1cc61931fcdbe6c40b4cc0711c5abba5ff68b8319c95a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc1fd3973482d4c800fcb9c82efb77d30cd62322500b7271933a60f763b8c544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passthrough")
    def passthrough(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passthrough"))

    @passthrough.setter
    def passthrough(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38abca2e6ea9655389182d1696b703eedb9d9f4b8513d6779cb9ad9db246099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passthrough", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="required")
    def required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "required"))

    @required.setter
    def required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e94e6afaceeaf1f43bce0bd767d41d8c820ef50be58b6f00917727d74a596deb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sample")
    def sample(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sample"))

    @sample.setter
    def sample(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9051e71c5c5ac8d56fe7c881e8a4b3a215786839cb81ff750f856358c8a745b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sample", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c72dd37cca3601977a8d1408ab29b04913bfbb9812d8bbf5a9b779c1baecec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validityCheck")
    def validity_check(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "validityCheck"))

    @validity_check.setter
    def validity_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a70f76d986f9fe6166e3fe98f552a9638d4a6fcd377c1bdc2bff8e8ae5563e1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validityCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2RequestParams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2RequestParams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2RequestParams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a82162af30d9e1e50e100dcdec3814cd85042dfb2321146e0ccf8e558cad95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApigwApiV2",
    "ApigwApiV2BackendParams",
    "ApigwApiV2BackendParamsList",
    "ApigwApiV2BackendParamsOutputReference",
    "ApigwApiV2Config",
    "ApigwApiV2FuncGraph",
    "ApigwApiV2FuncGraphOutputReference",
    "ApigwApiV2FuncGraphPolicy",
    "ApigwApiV2FuncGraphPolicyBackendParams",
    "ApigwApiV2FuncGraphPolicyBackendParamsList",
    "ApigwApiV2FuncGraphPolicyBackendParamsOutputReference",
    "ApigwApiV2FuncGraphPolicyConditions",
    "ApigwApiV2FuncGraphPolicyConditionsList",
    "ApigwApiV2FuncGraphPolicyConditionsOutputReference",
    "ApigwApiV2FuncGraphPolicyList",
    "ApigwApiV2FuncGraphPolicyOutputReference",
    "ApigwApiV2Http",
    "ApigwApiV2HttpOutputReference",
    "ApigwApiV2HttpPolicy",
    "ApigwApiV2HttpPolicyBackendParams",
    "ApigwApiV2HttpPolicyBackendParamsList",
    "ApigwApiV2HttpPolicyBackendParamsOutputReference",
    "ApigwApiV2HttpPolicyConditions",
    "ApigwApiV2HttpPolicyConditionsList",
    "ApigwApiV2HttpPolicyConditionsOutputReference",
    "ApigwApiV2HttpPolicyList",
    "ApigwApiV2HttpPolicyOutputReference",
    "ApigwApiV2Mock",
    "ApigwApiV2MockOutputReference",
    "ApigwApiV2MockPolicy",
    "ApigwApiV2MockPolicyBackendParams",
    "ApigwApiV2MockPolicyBackendParamsList",
    "ApigwApiV2MockPolicyBackendParamsOutputReference",
    "ApigwApiV2MockPolicyConditions",
    "ApigwApiV2MockPolicyConditionsList",
    "ApigwApiV2MockPolicyConditionsOutputReference",
    "ApigwApiV2MockPolicyList",
    "ApigwApiV2MockPolicyOutputReference",
    "ApigwApiV2RequestParams",
    "ApigwApiV2RequestParamsList",
    "ApigwApiV2RequestParamsOutputReference",
]

publication.publish()

def _typecheckingstub__b7c6d591787b72ced60a28d7fd2c09ded0ef5bb28ba58cbb19861e0dda0f601f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    gateway_id: builtins.str,
    group_id: builtins.str,
    name: builtins.str,
    request_method: builtins.str,
    request_protocol: builtins.str,
    request_uri: builtins.str,
    type: builtins.str,
    authorizer_id: typing.Optional[builtins.str] = None,
    backend_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2BackendParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    body_description: typing.Optional[builtins.str] = None,
    cors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    failure_response: typing.Optional[builtins.str] = None,
    func_graph: typing.Optional[typing.Union[ApigwApiV2FuncGraph, typing.Dict[builtins.str, typing.Any]]] = None,
    func_graph_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2FuncGraphPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http: typing.Optional[typing.Union[ApigwApiV2Http, typing.Dict[builtins.str, typing.Any]]] = None,
    http_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2HttpPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    match_mode: typing.Optional[builtins.str] = None,
    mock: typing.Optional[typing.Union[ApigwApiV2Mock, typing.Dict[builtins.str, typing.Any]]] = None,
    mock_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2MockPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    request_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2RequestParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    response_id: typing.Optional[builtins.str] = None,
    security_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_authentication_type: typing.Optional[builtins.str] = None,
    success_response: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__74b2583d77120eb9a486bc84646f2b47db3afb1310f702e8197b45ba61fa44dc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c0594e84901cd906cf0b083c60563c4cdc4434b100784e09b1d88456d5fa75(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2BackendParams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4d558f77573ac6f6535eaaf9cac46b96dfacb7b0f3cc030b98e3d3206c476a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2FuncGraphPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3317766a38b0d92e6c884aaf8838795367b7da2f96c58da1f1e685427748d59b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2HttpPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c114ec1361094937e51477539c398a0d6041f508d0769b8de2ed7a4d5cc6aa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2MockPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dee2ee99a829667c54c5c46ca5d6ea86221a8d94f291f75f4b01d344b25d1d1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2RequestParams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c741f67b1cd739916dffb8140c837a0a5925808a554cf752938fddafea12d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37bc815a2cd221075c00316e48b4e52d6316fc75a6a635a736953b875d41a7f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7659527498d3a621a45e14361d1c1cd2167d12ae9157baae3a911533158bd6e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dbcf6c3885f855e4297a226dff953daf8b433277c0833f3d5f12e8f2e102d23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48618b4e21107d6d7836b97e2774fb9e575ce41bdd9e908913c9dd2348b49012(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c3b2c8f2cf969201fc6698ba42111382e233836f385078dc0e9a9c19fa0529(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435879ffc3a2e06ce9a4e3419108647af9f22750987194763c8a269f63789e68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d16972e248b07868a0f2428bceb84fedb6b82997e8225ce9030f39724bf4e23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__453954931077f4e1616cf1482a8f5368c9c691095419caf6ba8aa738b9cd58af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88b327fd5b03ad09fbcd6c93635a939851786e5cc5b6cb4f201b0d9dcafbbb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ccdc9cb5dcd17252fd8035ae961224a78b1ebfd1ff7e7ec9752cc1bf69efcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c948d54d75957099e366a1a758abbc470db418e7838f29c3977417f4d97537(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7d8392ef836b2f36360e3d2cac8ba3eee0b70ddd2caceb696857e5a67b1a83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66af1a0912254692405948cb42d75e5ba3eb0df03c3fefea0c75d48501a20281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ced327dcdf101c7016e05c9735eb40b3c8686418af0d17c3e22d1ffd9e8faf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36cf44897c72b51d4946e2d96703d7a9d0ae882a7fff92e317b2b59ad560fa48(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5c83eacfae9d8dcabc02114eec78a0229d4e76f6b74642ab2641492df77447(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54fdaf6e13149df6273f1aa01f7e06bf650644468ca63433ec0a1441785304c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ebf3bd12a423a5b817076b47fecf8ad4991c7a286e09a3179eda79d19cd82b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2b681587a43f32ef796a3741300e2d3f2de39ea06b24568177814fda28696e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477de151aa89463f855b00d5d454180ae8d65b55890c393d74372a5cc96e4b06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5272ad308f2177cd178a354a08f1b48dd06aab6ac5dbd7a7ad3c353c117b6e04(
    *,
    location: builtins.str,
    name: builtins.str,
    type: builtins.str,
    value: builtins.str,
    description: typing.Optional[builtins.str] = None,
    system_param_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5938eaf406a44d0524ab5511c5d4595fcb781b0b4153f23b3c84fd9817907a2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f123697d071cb30e265348fa3b51bc4f50ede0ebd6d99f64a3f25e3863d3eb51(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09215e036466ccfecf0551124d0ad20c2286eea6579a5dcfdd8226a83bd25d84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4636aa5a6a64b2ae8350965dc722679dd80dd85185f21945744fd07c9d8cd9c7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3337aa79b166173e4ad013677c14ffae9cb8288db2b2a32df82e5ec7228e28d7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83e455e2ee524117c1c89af2519bc92b63418ded636dc664452567554235b84(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2BackendParams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e1e3888ebc2f245610cfebd313f80d8df4e429e575903433aa01238de47978(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0181a2baca96237f3e3243a07ecfc67076014c94fd7e764c48d694a7e367e5d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f55ae9c306e450f2e19a45809aec9f6f2a89dff629d7dffed2e7f258ca24eea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe816b3399b0f02af16cfe5ee572ee94bd23fefe422e13c8c3cc9b239b5fb72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e8020cbf83675b61c48058f29cba9e1fe5634634c7f0e2299e4c1412c0dbcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8493ee9684b43715f8f6ea84dce348a383e5d2300b1852188ae0fa84bd8bba90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312549a66ae7c8539b3c2bdc21b0aec81ce58d46254d815719ea6913e1508e8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d76bceab190c521b5f3464fe1e9ff68efc42f82e70ff7268df5a977a45dd90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2BackendParams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f99146ae80425ff18102abd92c0a20f2d969194859e001830dc1039c6243a1f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gateway_id: builtins.str,
    group_id: builtins.str,
    name: builtins.str,
    request_method: builtins.str,
    request_protocol: builtins.str,
    request_uri: builtins.str,
    type: builtins.str,
    authorizer_id: typing.Optional[builtins.str] = None,
    backend_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2BackendParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    body_description: typing.Optional[builtins.str] = None,
    cors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    failure_response: typing.Optional[builtins.str] = None,
    func_graph: typing.Optional[typing.Union[ApigwApiV2FuncGraph, typing.Dict[builtins.str, typing.Any]]] = None,
    func_graph_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2FuncGraphPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http: typing.Optional[typing.Union[ApigwApiV2Http, typing.Dict[builtins.str, typing.Any]]] = None,
    http_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2HttpPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    match_mode: typing.Optional[builtins.str] = None,
    mock: typing.Optional[typing.Union[ApigwApiV2Mock, typing.Dict[builtins.str, typing.Any]]] = None,
    mock_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2MockPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    request_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2RequestParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    response_id: typing.Optional[builtins.str] = None,
    security_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_authentication_type: typing.Optional[builtins.str] = None,
    success_response: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ec5573ceee1551a8adae90ba07dc4a693257f0075b9f39bbc4d20f5f36408d(
    *,
    function_urn: builtins.str,
    authorizer_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    invocation_type: typing.Optional[builtins.str] = None,
    network_type: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[jsii.Number] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ea7b9eed3785099ddaf2caf63434f6345ac95ea042f5d63c848519f8387fe7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1acca9cf786fab79e31ed948bc6328f58d1171b5d48eff2d71ba2e1a4b7bb0d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e12613cd4f82bf0cf5c25868b125a0abe71db52df1f04fd98130726e95b36c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46f543a7a16f30dccf7913e94afe676c29e458047dc4d4ab6b4263014e784cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e2b826b0a29775c7a349be71e30286f3c9e6dbe02f522e558902a2241ceaa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9a4ec350f7adc96c676f8df7d4597ce278a09814e1b22d40f62b5b4e76e4c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12746fa66408ac1bba58911fe43633f8d2781f9104367cc877695524bfdbdfcf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db44af16030471d8dcbbc8a347f0e27ea0e6b62b1484331e2cc58ccb808f564b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b01ec7a384251f9785dca4327c73b0bad98d84615d691f36d4a5ebeb1be35b6(
    value: typing.Optional[ApigwApiV2FuncGraph],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d0982cdbb0aab92bd59fb512b00424b2806f9c6ce0ac31ca8c4ee7e5b564226(
    *,
    conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2FuncGraphPolicyConditions, typing.Dict[builtins.str, typing.Any]]]],
    function_urn: builtins.str,
    name: builtins.str,
    authorizer_id: typing.Optional[builtins.str] = None,
    backend_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2FuncGraphPolicyBackendParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    effective_mode: typing.Optional[builtins.str] = None,
    invocation_type: typing.Optional[builtins.str] = None,
    network_type: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[jsii.Number] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f7fb1c878a9f4625795561a5bc987762bda08a5de974ee2e2af1b1e2996eff(
    *,
    location: builtins.str,
    name: builtins.str,
    type: builtins.str,
    value: builtins.str,
    description: typing.Optional[builtins.str] = None,
    system_param_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de83c4fdbc27b6e299ab04f80c42db39bc87d91d816c1187dd73f257bc5e5367(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__734b81e155e0ca84cd9722f42c212b6ddf4a41f331f370734ff0f9b172a95cfc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090d78e29e041ac0bd5225fed6cb7ed91bfe78c5750c83df69a50a420d6e0e77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecacf16a974a6fc66174dbf064a4462676c6f42ddf45324c8556714ab7bfef45(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__018af445eff1a63eef854065d5f675ed98c91d1f2e9878611800d2578ef8cc6a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b1ad7a28346e6bcdc0f9161053a6169fe63bb2ba773b99556df8e8b3397c43(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicyBackendParams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb406034ed69a22d84ac85ee820b04fa472671910a69c14c4cd10a0f54e0d50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b03debde1a1a827cb8f26126867470e12f49cfbe9900e5e95aa381a09d91b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561cb35908a4a71341a1a06b3dc529b466f2be0cddadd65f21d53a276e7fa119(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c63da0b80bf78ead13bf43b1ea28ff6f4559d61a7ec734d08fc6a670f3dbb04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47de248f66711e1efa4f694bfab0145dde9719b70aea39973951c5bbdf691ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71726c41e480a7c8ec3fc44c6523c66cccb4e18c79eb30f0449a7a6be20f0586(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4831e7f1f2758a7c308a793de3c884c1c42bcde8f7b41eef7206accce5812dd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58da4f3e2ed2215521ad2be2148c0303892fcf6df193033acf57b768043b7ab2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2FuncGraphPolicyBackendParams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3dd59dbd6dc7434e413a5c321489a7ea4bb039baa126f261ad14fc4c308c44(
    *,
    value: builtins.str,
    origin: typing.Optional[builtins.str] = None,
    param_name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e5556468a4356eafc445d57642ca1c8896a0099b2b3d548511663adc59f0fc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5813bbdb2de271a8df8b847998418a4549dd986f75e64867ef454cad891fba4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce951b14f517ec2c3ac9790775c036bffd27cc6632523042f7f77ddfbb57928(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862c01aa1684d0986e8523509b320836d1124c6d8d08f75e0b76c59043fc75cf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee503e9b6caa8319ba789863538a7eb10204fad1ad0d6e80f8e5d72cc721dfc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1ab1386ac423e687458ba3b60d5f65a56c737d72fd4a28ce313f76f492c91a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicyConditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31686c48c5232284dab3d7b024f73738e661b470fea874bbddec7b15414063aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a57b9286945b66b6d86ddd011d254be81d197ca7e1072fdd5b3cdcc538b008(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466db76d7ad98da7c981afb2ff6a0d46100cf1c7d0eae9b64fa82ce834f7c662(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471ea9f86ae84e64f466b3304ec7e1ecb5dd47b39b098c28579a40c36c59f31c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39cc0cc1f7e8bb6c7ff29eec8e89c161c5f793db64f8e1a243e170bbb874b4d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6376a7ecbf10cfc8cb612049a565dfe558ac30b15b55cd1e678312f54850a515(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2FuncGraphPolicyConditions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1244d71f50a2d8ef54d72620e5bb8ea524522b5763e21a3e3ba8c329765cc528(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1c731a632b6fdb056400b2c25b2ecdda17a5d2b5d4ccbeebf11ad4faa5b54f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ea3b97c4f5e3fb482a989d3c7c049677d660e8b0c669f6f0c44df7dee0d4a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce07850942a95fb3a90b62055f679026bb97d68faa4cd839eb61df79a6efb432(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4160410f3fa8a63c8e090d2687f8b6d1235c04d3701b7e39df724651ea724aa8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa9ebe92c771cac42cc1a42921bc6a4f4f8683b3b253ce81450b0541010db58(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2FuncGraphPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fbf05484d4a79ba255e4e41ea42c8b3c557ce86a07c91c10310285b991d4585(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb8a5dd6819ebdf8f11b936f6bdf76fbc1386bdd3f4bb59413af5ed209a32e6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2FuncGraphPolicyBackendParams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a3aa0f38c9543ecb50e33cdd94a2f1695bf3cda257affcf7b59d6648301ef6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2FuncGraphPolicyConditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f9ac70d20317549e1df74812f61c783b3f464a026392eb4fa297156dae24c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cfb177beb2b264f119d5118e1c565dbea793daf44fce5169aae96bb6c414199(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827d692f3e6f411995c3d3c06315e0b73ecb62326d29a27e475d9930b5c61d43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8943f9352ccf55c8c56c1bb5cb64b45f599c4aed27a517a51c1ee1b886794c63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b4fb7701d26bbc7182107d269e28c1e182b91ca333b250f00c7d64a133021b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bcedb80fde4354fc0ff80c56c0cd7390aa89d7ed837ea6cb79b5dc7b5f42b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c99222a518c0bafba788ce2fc227ec56c1c3cfeba52d2cdce8b5c891cab45b47(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0351a6158fb019c298a9e068374ed45a5d13712a696d7beca9d404ef979af3b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb37c3602efcd17eb7f549184b3da81060b3c86d23c83059b526401f084b0d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2FuncGraphPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0385464ccdb348a212f5d6f27a1fd87676e1c83ed335f21348e5029d3c8737f3(
    *,
    request_method: builtins.str,
    request_uri: builtins.str,
    authorizer_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    request_protocol: typing.Optional[builtins.str] = None,
    retry_count: typing.Optional[jsii.Number] = None,
    ssl_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    url_domain: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    vpc_channel_id: typing.Optional[builtins.str] = None,
    vpc_channel_proxy_host: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f43e4664e2030889bca2add08bdfc515fd64f4331c497d34dc020275f6b43d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7fd8a32c8952a5738ff992f105f3fc4613f42ecc3695510dc80f33263bdc7ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f31487c8e6f4296e1758310698d47c15aec8ec5bb8f33ad48e102375a116986(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d02381f797e70f63a0c948b0afd739f791c63767e8ebe588ce8abcdf2def74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e822fd6f658d0ebe14ea4982f11f617872b06b622bd58ed4c3bdc209f6530b40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d00b2ba527d28d76699f73f79a574dd29c18adccab33c54a29798327b94a97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a2d8cd4643e508cd5c9c16695bd9a0f6e3904d5c743c3910673bdb27a9c2ed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e02e8855bafcb003277a732af70b871cf36b12093067a87945cb5dcfa28747(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c732dbada4fe58b11ba8ecbb1fd2be9938644a0fd4ffdcb067f812986a69b811(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325acbad61f6f5380ed6e855458781db5937a3afffe7c63660ba2bf331a0a30c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e35b364083469479825d8da27694c548b262c87a929e0e35c9cc94ee2632d26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aaa4b6748cc829578c24dfc826facbf637e3ca99397385ef6f57abe4e69c8d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f2414bd1becd3f4b4b44d599121d755355a042695a7ece1046a14f5c8fc05ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc47b491fa0051f9e3d643bac4f3b6d8b52c3861f3f0a87049c2e1ecba707db9(
    value: typing.Optional[ApigwApiV2Http],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4d0cae3e4c7aad1f5dc7044f8921394f4badb235752e79d0b31b2dc41d3f59(
    *,
    conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2HttpPolicyConditions, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    request_method: builtins.str,
    request_uri: builtins.str,
    authorizer_id: typing.Optional[builtins.str] = None,
    backend_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2HttpPolicyBackendParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    effective_mode: typing.Optional[builtins.str] = None,
    request_protocol: typing.Optional[builtins.str] = None,
    retry_count: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[jsii.Number] = None,
    url_domain: typing.Optional[builtins.str] = None,
    vpc_channel_id: typing.Optional[builtins.str] = None,
    vpc_channel_proxy_host: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522cf78c24bdfe5661b3ab5479c54138886841f1f4e83aee23485e99348882c2(
    *,
    location: builtins.str,
    name: builtins.str,
    type: builtins.str,
    value: builtins.str,
    description: typing.Optional[builtins.str] = None,
    system_param_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f47552ef548408b3fa47f9ca9c3cc8f678967882d5374da6bc6617b9fa1ec083(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0e75ca94718e88ab3715aaf220221a193c2cdd24a79c934988acf31257ab6d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21f006ed2cc135bded700d9c3a52bd1b5b459c9f36dc9d5c2bfa06659a08b34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fca870eb4fb2b46c1ac24fdebaee68b9c6401a4c4fba467fe6b6e380ea64ad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5074bc7ad611696ffcffeebd24d8bc5b85efeefe09026d5f944e0d85654f14d1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0890f43f5c258f7913d28cf59b7f48923cc24b10e1a38897075052ed48b4bd89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicyBackendParams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7389b11642351758ab952a4c8578d46d2809980bb9ad9bb0904139dbaedf15f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716b07fd935475ba36cb86eba88cef4fe732bf130473ecc5d44d7becf22fbd60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39705b94f1280e24b8808360808cac39fbbfc984af79919dfaf3f85ed8f41c27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70afb42cadcd3b3e22fc2f73bbad37c4b07ab7ba204364fd7ac12f872e8d39d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb01f21f757363da5e2a2d0d0a1e29bac8e8dee91a2767c49ce8bd5decab2760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b95576c126dd2e1f493c1dd4463e471b56cc014dfc3cd14b592e56e1ce1405(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcaabcbc44272984e8976d00771987012df2c7356bd4f62185a351aa1fb04d1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c04cec34fe56f6683a6aad50b74cea8631440816f2d461b587b7daeea8b6d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2HttpPolicyBackendParams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0530b1efdf3e1705d23b346fedc8d5b8d4049c23f595b3fbae19f573ec322b(
    *,
    value: builtins.str,
    origin: typing.Optional[builtins.str] = None,
    param_name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd370eac994d897a35450758f72a6318166a35a9d7061094fa0d4f9f1c60e01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6bbc5d7b0f334550197be6155d91f04f5c0c4df7c4d0736166e43f9d58930bb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__260cc7384f9a757539635fc7e9c1677fd99a5eca74535f8ba0cf617cd800ec0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5622175bcd379e75bc8243388820ae8e87b6c69ee5f7ed58d30899e8e0575795(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80141b8b10f364423194a7d69453cec08a1c0f8995ebbfa9640545ae163a84f9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a225d5fb51c5b2b09a82431afec06b29ae5c3e67b2634514ef8b5315f67be31(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicyConditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8155b4f0d3a9a4a6c372cad9e0afe16a6d56c2289a950cd3eea24bd3825e0182(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295ec024c2e888d579344ddda33fa121bfb51c9927c5b9fad8ca278aca61dd2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242d7fcd31a6c9b2f464658290f84cb0f80f4b801f047a0582a0d2552931d349(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eedb5aca2b9049442eeb34d5f26b32d8080d67038156a0599cc520bc8a7f463d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f07f3bd7ac3ba2d1292780ca7b914808da3b4dfa995fa42e8a1c715fce57cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eabba317efdfa8d4610e0b67862bebb1c3a328e0bdfc26551cc7f70abbb732c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2HttpPolicyConditions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff780ed5b554c13aaf3f9a57336d1805ab056201a056c7e5cc2d76d469496b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5646ca144ff73a39d76be7043cbebf6011c560c23442de5d7fb747e519d1ca82(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7956f9a42996cd77e489b51b8de76f45568f06c2303b5d9832b3696cc699b517(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9454bcc5209ea5a438d71a06e481f3e7fac9e1c3330c6116dd2e153e44cfab95(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3618fb618feda5d750819f6c17a4a6b1a12c65a74ef9e2dfc2ca08ecd5421f9f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225fb858d733cf10827647ab3fe5fc5bdea7966b7fd5208d5d7918992207d081(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2HttpPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7edcaf8dc4420f766d8f70283badba073e5cdfcaf65a0548e46bb5aa8b2ac0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552a8dc86d3fd1a1e12170283902da79b68ae71f56b59dad58dbca36e353b7fe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2HttpPolicyBackendParams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec4e93afdb989b837bbafff3a18ced142f194474ac12e0183c74e0ba9ac7a6b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2HttpPolicyConditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d67c4742aaf8f1078aea28eaf64fb16492dbe2833613f758c7b931b872dae8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89de32e1f0439932541da57db36bd8c9e39f578fccc3d15e0f4a1453f8f88f67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b91dd79a87e3973be62a2e436159ee492f32f2e7a5d11c328a6378172d5b6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff2add9c0461d38988504365b3d454560cd0a564f8231cdbd077971608058763(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077c981087a3e01c52a2284708147cad49be5afaf2daf5deb50bb873e0bc1750(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecee390c6a90262927c35d81c96d3c9173d3ddbade5a0ab43e831ee6f237f22c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999bea44ddb68d517c3ea5d02736738321ca6ed9ade36a280200a6f878d04c3f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c77d1fa4a65f7a10a7bc0cf8080bcacade2886eb54abd2140dc6ae849d382d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d076dbd0f15ff2f9f2b31918b7259a002e53f790555925900e220df50e2916c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef3aca9fe000cc2bac2ab0a93d42279144c64b558d45dcd94bf5456f28a0014b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be10bc62066ff4d97787ec58cc285aec2e48b7c9f08dc7570613c9a7c7c7df99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__612944840153b8443ed9cfcc1f4f245df91355295bf52203140b6981c1b75407(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2HttpPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0886d4fd7625ac26691bc62dc111cb3fc16d530271e7fb01db391c060c66fda(
    *,
    authorizer_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    response: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4c1250dd2bebad73898ca9ef93d6fb6fc84d4e80703065ca6f09c1e71be347(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0afcbb390f978c5c4449352ef830ad4adadc03e970514950dfcc28d68a1475c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17279539694b334d980f7bc79011a87709b66ccaf0c4c127e142bf871354629b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54e39ff34b4cd3f86578b39957c16418dcec0fc2f07d1af1e11bef23ea85b72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85324bb4808fff1be1b30e13c40b1e5b54a20f02d2a7c2f1498a1454d09478cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73fd0a87b0f3c2c3684b62b41e0615155b9f77ec0f1296a7c9fb9beba570fb2(
    value: typing.Optional[ApigwApiV2Mock],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d3eb1e46a9e3ad5bfc64ef0f4349f50e716969d25fa6e406bbc354fa3ed7d5(
    *,
    conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2MockPolicyConditions, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    authorizer_id: typing.Optional[builtins.str] = None,
    backend_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2MockPolicyBackendParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    effective_mode: typing.Optional[builtins.str] = None,
    response: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5edea3f4928c0c9dc1ad430e3c01f2e8ace1af7df2db8131513657ef35487b37(
    *,
    location: builtins.str,
    name: builtins.str,
    type: builtins.str,
    value: builtins.str,
    description: typing.Optional[builtins.str] = None,
    system_param_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3060d669a9fe60eb180e5d452069a4385ced297df11796ee53f4cc47e18b00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ceeb27b6f5ee7a389cec074127d5ac18b47deebba88698a3e06bece1c89674(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462040fd6921beba93862362fa699c721e78176fed141a29196d3111803f1110(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1801a261140c923227295c143f3f96a0aae8b78ced4dad3ac895d586b6b3839f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f94e8650c166b4bc34f61a9c570ff5265fe7bd08febedee0fe39664e39a7f7f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dda8d92b6f9f9f9a925b2c842f4178f33a36f5d1aa1c9ae58fb686dab07380e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicyBackendParams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6165bf5cbda001e9cfcef3ea9f51598b2e61424f3994214d3c4eb127a5d372(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089760d58721a57ae2664aa4357739bd39051e67cfe5ea1188fa2a75d4bf8d68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8596e04d63675f2a2b2ff1e3a9b92efbf340347f0f6624229d9f4abc2aed0969(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e080105a535f1b3acc4a7330c75c90c75ca727313284f142093a8fbc0e17408(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314a1590e6a41b584502d5f1d3b7b8a9cb58d4ec195368d4ba782e246add16d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a78ca8d31bbbaa2a850963a802e1bb75a5010aab4ac556fcb4a52df3bd2dc05e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4e828a0e326b48da61a7f3895b275512ed90735545f1ba940926b9a63421e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d784d91c83a8a0ef02ec43a3d2dcb63ee4c738911b35fc3cf8d7d5d4d1ae2f2d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2MockPolicyBackendParams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208c2dc27284be917c71c2d4c279618770f0eb8366b0e257200e4126164687aa(
    *,
    value: builtins.str,
    origin: typing.Optional[builtins.str] = None,
    param_name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a96c9dbd581761011dd9a467389573958e34baae10daa8d2dbcc2fbef67846(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f715900c476cb3e260a9e8713d3ee6a935fe153004bc88622f02c096cc12e50d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a7b0c1f21efc95d80d89ca4c7b601616ca8495f41687008d5a20cd99f2df6cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113c0a666d9743c1a1eb4f45b885877d7d8796fa0433808b2683aa4bc58d7344(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1298e1e5f1eaf304e4b33033ee5eb6bbd1781ef9b8f6123949f62cce8d567918(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8cc5ed21ae3f4bfa4e630794936dcfec8b94c6bc252d224ccdf114d1850a4e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicyConditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a90cf05f8cce9563a2327ed2f902921a181d11a72aff4ed68848df2782c0ab2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22559387adcd61b01e8bc5f892d63eaa2abde6d5bf6039932ef79315cee7cccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23d41af9bb8c84037b029ed7122e6295bad07aff398561e750364647d2c40ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77bf6bd8170882adb26cd1da4b5fc51160960f4fe579984a908da6b1b8c52f41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c8519b2215f38b497fcae29918d76e6e1279c776b826ba10f7441154129959(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86eff74f34109aedacda209c7f12d0dd6929c9b1c632b7c091855994c470097d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2MockPolicyConditions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687adc94ddbcca1cba88ebf3928323a333633ab44e54e673e623bc25e5e33f40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed504668a80f68e450bb5e09a118eda6a5f8cf7f570ab56aa99cf37dfe63b29a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8fd586d051647a127363fbd15f86139e508a96eec96417e1f55d07b72eb0e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2507bdd8023b9b23d4d9d48a7e049ea77484c5ed7dcbb4e4f663f11b7b5adb34(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3576735318a9840c38d0cde73e49bdecea6fc64b8f197520c7c5514685cf459(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d4757ea11d812dd9f713bb3d141f3c42a0dee5b45610b02ae0c056de4fe4d99(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2MockPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7ff6ea0ff12b66e8e179bf2403182bdb7a6d8492337fd13d451ba7cbe7a19d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90add921ca472a22bb2d3ddc9127b649af00dabdf0546239c21867566796b18(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2MockPolicyBackendParams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270528180ec17df945058bc0b16a81ea48eedd4dbd71321a0be986d94c9ee91f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwApiV2MockPolicyConditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c70db185226d4543b6d8afe3a75f11d65d2e7d82c87e2631d620bba8fb5ca3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af98e0f5b94abec146487d46663e726d38ee284dd7e890e77139e6c237f256b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed0508d4f22842dd9360f498d67646e487589f79ef37496980760fa05afa726(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce11ecdfa62669a3d791409b01e5b9160732666dad299a098a5392aa4ea6890(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6352e8f2144cebda73a68c1ad02f67e62db4311267ee12bd143da5d69a61299(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2MockPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392fc4acf6a9c4ebf36224fb588decd0ef1366df0c96512dc53081ae78900023(
    *,
    name: builtins.str,
    default: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enumeration: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    maximum: typing.Optional[jsii.Number] = None,
    minimum: typing.Optional[jsii.Number] = None,
    passthrough: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sample: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    validity_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e6cfe466fd18ed11e1d2d2921b3083e613dea2d93432cd2f92af8686946c88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f197546f8a6a4adc41de6ecd94865dfcc1154628723d4bae021d1a2fcb4d77(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74866b128025a2ea1285224af8d7249e3000fc5466441dd4e456edf36ab693b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880ad7a2db8fdf588287916a7ed659b21867743ea4a8753324c3edd6a1ddd474(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1673b472440aaa141289a73d71f8db8a0eda3bbbd9caa57f6656fadd80f9fa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618cee9c564fb1c1a9b9f998d0c5cecc415115b37ef1f4d2e86833389f2cbd60(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwApiV2RequestParams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761d9e0251a2ef4706884267238a58d9e6051198686b181f515305f98d707feb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e1a61e432e49d6b38d1d767af203caa510df46b85184de951af705a8cc3a3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a795a18740dbbf644a6e2f7c6214f63f735c97d5dceb830961de331fb1e75eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6078c179c6abc6dcde88a0c2c8f954d5002dc4b3b16b65d43ef4bcde3aa0fa7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b8b1f0c8400813c41038d6ef093e961a8d55ae9c5a43b9304952dd1cb3922d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36e7932defd16b53184fd650695690a545d481ab009815194b3de899ee12365(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39329a8d809a2f1fc1cc61931fcdbe6c40b4cc0711c5abba5ff68b8319c95a3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc1fd3973482d4c800fcb9c82efb77d30cd62322500b7271933a60f763b8c544(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38abca2e6ea9655389182d1696b703eedb9d9f4b8513d6779cb9ad9db246099(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e94e6afaceeaf1f43bce0bd767d41d8c820ef50be58b6f00917727d74a596deb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9051e71c5c5ac8d56fe7c881e8a4b3a215786839cb81ff750f856358c8a745b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c72dd37cca3601977a8d1408ab29b04913bfbb9812d8bbf5a9b779c1baecec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70f76d986f9fe6166e3fe98f552a9638d4a6fcd377c1bdc2bff8e8ae5563e1a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a82162af30d9e1e50e100dcdec3814cd85042dfb2321146e0ccf8e558cad95(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwApiV2RequestParams]],
) -> None:
    """Type checking stubs"""
    pass

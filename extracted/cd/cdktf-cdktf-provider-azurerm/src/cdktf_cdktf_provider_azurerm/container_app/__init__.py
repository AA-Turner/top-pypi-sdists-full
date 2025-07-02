r'''
# `azurerm_container_app`

Refer to the Terraform Registry for docs: [`azurerm_container_app`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app).
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


class ContainerApp(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerApp",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app azurerm_container_app}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        container_app_environment_id: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        revision_mode: builtins.str,
        template: typing.Union["ContainerAppTemplate", typing.Dict[builtins.str, typing.Any]],
        dapr: typing.Optional[typing.Union["ContainerAppDapr", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ContainerAppIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        ingress: typing.Optional[typing.Union["ContainerAppIngress", typing.Dict[builtins.str, typing.Any]]] = None,
        max_inactive_revisions: typing.Optional[jsii.Number] = None,
        registry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppRegistry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppSecret", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ContainerAppTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_profile_name: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app azurerm_container_app} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param container_app_environment_id: The ID of the Container App Environment to host this Container App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#container_app_environment_id ContainerApp#container_app_environment_id}
        :param name: The name for this Container App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#resource_group_name ContainerApp#resource_group_name}.
        :param revision_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#revision_mode ContainerApp#revision_mode}.
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#template ContainerApp#template}
        :param dapr: dapr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#dapr ContainerApp#dapr}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#id ContainerApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#identity ContainerApp#identity}
        :param ingress: ingress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#ingress ContainerApp#ingress}
        :param max_inactive_revisions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#max_inactive_revisions ContainerApp#max_inactive_revisions}.
        :param registry: registry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#registry ContainerApp#registry}
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#secret ContainerApp#secret}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#tags ContainerApp#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#timeouts ContainerApp#timeouts}
        :param workload_profile_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#workload_profile_name ContainerApp#workload_profile_name}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab6e515acad25b2aee6c2cd5a6f19f3af4da1e8d8d0e1f5b7b0afd9bd733d52)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ContainerAppConfig(
            container_app_environment_id=container_app_environment_id,
            name=name,
            resource_group_name=resource_group_name,
            revision_mode=revision_mode,
            template=template,
            dapr=dapr,
            id=id,
            identity=identity,
            ingress=ingress,
            max_inactive_revisions=max_inactive_revisions,
            registry=registry,
            secret=secret,
            tags=tags,
            timeouts=timeouts,
            workload_profile_name=workload_profile_name,
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
        '''Generates CDKTF code for importing a ContainerApp resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContainerApp to import.
        :param import_from_id: The id of the existing ContainerApp that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContainerApp to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13015e1fcd408ee164f209e0e79d89a04279d8ee058ce736d8f1828ac9d98d9c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDapr")
    def put_dapr(
        self,
        *,
        app_id: builtins.str,
        app_port: typing.Optional[jsii.Number] = None,
        app_protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param app_id: The Dapr Application Identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#app_id ContainerApp#app_id}
        :param app_port: The port which the application is listening on. This is the same as the ``ingress`` port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#app_port ContainerApp#app_port}
        :param app_protocol: The protocol for the app. Possible values include ``http`` and ``grpc``. Defaults to ``http``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#app_protocol ContainerApp#app_protocol}
        '''
        value = ContainerAppDapr(
            app_id=app_id, app_port=app_port, app_protocol=app_protocol
        )

        return typing.cast(None, jsii.invoke(self, "putDapr", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#type ContainerApp#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#identity_ids ContainerApp#identity_ids}.
        '''
        value = ContainerAppIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putIngress")
    def put_ingress(
        self,
        *,
        target_port: jsii.Number,
        traffic_weight: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppIngressTrafficWeight", typing.Dict[builtins.str, typing.Any]]]],
        allow_insecure_connections: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_certificate_mode: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Union["ContainerAppIngressCors", typing.Dict[builtins.str, typing.Any]]] = None,
        exposed_port: typing.Optional[jsii.Number] = None,
        external_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_security_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppIngressIpSecurityRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        transport: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_port: The target port on the container for the Ingress traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#target_port ContainerApp#target_port}
        :param traffic_weight: traffic_weight block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#traffic_weight ContainerApp#traffic_weight}
        :param allow_insecure_connections: Should this ingress allow insecure connections? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#allow_insecure_connections ContainerApp#allow_insecure_connections}
        :param client_certificate_mode: Client certificate mode for mTLS authentication. Ignore indicates server drops client certificate on forwarding. Accept indicates server forwards client certificate but does not require a client certificate. Require indicates server requires a client certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#client_certificate_mode ContainerApp#client_certificate_mode}
        :param cors: cors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#cors ContainerApp#cors}
        :param exposed_port: The exposed port on the container for the Ingress traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#exposed_port ContainerApp#exposed_port}
        :param external_enabled: Is this an external Ingress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#external_enabled ContainerApp#external_enabled}
        :param ip_security_restriction: ip_security_restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#ip_security_restriction ContainerApp#ip_security_restriction}
        :param transport: The transport method for the Ingress. Possible values include ``auto``, ``http``, and ``http2``, ``tcp``. Defaults to ``auto``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#transport ContainerApp#transport}
        '''
        value = ContainerAppIngress(
            target_port=target_port,
            traffic_weight=traffic_weight,
            allow_insecure_connections=allow_insecure_connections,
            client_certificate_mode=client_certificate_mode,
            cors=cors,
            exposed_port=exposed_port,
            external_enabled=external_enabled,
            ip_security_restriction=ip_security_restriction,
            transport=transport,
        )

        return typing.cast(None, jsii.invoke(self, "putIngress", [value]))

    @jsii.member(jsii_name="putRegistry")
    def put_registry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppRegistry", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b76c868c6a43d7ef249c63c011803112d33f07c873b5ebac32de3043143547d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRegistry", [value]))

    @jsii.member(jsii_name="putSecret")
    def put_secret(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppSecret", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__366314372c1d2fca5a222833acf6f59c8353fc8c66b0e01d588463ebdf75d584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecret", [value]))

    @jsii.member(jsii_name="putTemplate")
    def put_template(
        self,
        *,
        container: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateContainer", typing.Dict[builtins.str, typing.Any]]]],
        azure_queue_scale_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateAzureQueueScaleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_scale_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateCustomScaleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http_scale_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateHttpScaleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        init_container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateInitContainer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_replicas: typing.Optional[jsii.Number] = None,
        min_replicas: typing.Optional[jsii.Number] = None,
        revision_suffix: typing.Optional[builtins.str] = None,
        tcp_scale_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateTcpScaleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        termination_grace_period_seconds: typing.Optional[jsii.Number] = None,
        volume: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateVolume", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#container ContainerApp#container}
        :param azure_queue_scale_rule: azure_queue_scale_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#azure_queue_scale_rule ContainerApp#azure_queue_scale_rule}
        :param custom_scale_rule: custom_scale_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#custom_scale_rule ContainerApp#custom_scale_rule}
        :param http_scale_rule: http_scale_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#http_scale_rule ContainerApp#http_scale_rule}
        :param init_container: init_container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#init_container ContainerApp#init_container}
        :param max_replicas: The maximum number of replicas for this container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#max_replicas ContainerApp#max_replicas}
        :param min_replicas: The minimum number of replicas for this container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#min_replicas ContainerApp#min_replicas}
        :param revision_suffix: The suffix for the revision. This value must be unique for the lifetime of the Resource. If omitted the service will use a hash function to create one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#revision_suffix ContainerApp#revision_suffix}
        :param tcp_scale_rule: tcp_scale_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#tcp_scale_rule ContainerApp#tcp_scale_rule}
        :param termination_grace_period_seconds: The time in seconds after the container is sent the termination signal before the process if forcibly killed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#termination_grace_period_seconds ContainerApp#termination_grace_period_seconds}
        :param volume: volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#volume ContainerApp#volume}
        '''
        value = ContainerAppTemplate(
            container=container,
            azure_queue_scale_rule=azure_queue_scale_rule,
            custom_scale_rule=custom_scale_rule,
            http_scale_rule=http_scale_rule,
            init_container=init_container,
            max_replicas=max_replicas,
            min_replicas=min_replicas,
            revision_suffix=revision_suffix,
            tcp_scale_rule=tcp_scale_rule,
            termination_grace_period_seconds=termination_grace_period_seconds,
            volume=volume,
        )

        return typing.cast(None, jsii.invoke(self, "putTemplate", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#create ContainerApp#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#delete ContainerApp#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#read ContainerApp#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#update ContainerApp#update}.
        '''
        value = ContainerAppTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDapr")
    def reset_dapr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDapr", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetIngress")
    def reset_ingress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngress", []))

    @jsii.member(jsii_name="resetMaxInactiveRevisions")
    def reset_max_inactive_revisions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInactiveRevisions", []))

    @jsii.member(jsii_name="resetRegistry")
    def reset_registry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistry", []))

    @jsii.member(jsii_name="resetSecret")
    def reset_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecret", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWorkloadProfileName")
    def reset_workload_profile_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadProfileName", []))

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
    @jsii.member(jsii_name="customDomainVerificationId")
    def custom_domain_verification_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customDomainVerificationId"))

    @builtins.property
    @jsii.member(jsii_name="dapr")
    def dapr(self) -> "ContainerAppDaprOutputReference":
        return typing.cast("ContainerAppDaprOutputReference", jsii.get(self, "dapr"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "ContainerAppIdentityOutputReference":
        return typing.cast("ContainerAppIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="ingress")
    def ingress(self) -> "ContainerAppIngressOutputReference":
        return typing.cast("ContainerAppIngressOutputReference", jsii.get(self, "ingress"))

    @builtins.property
    @jsii.member(jsii_name="latestRevisionFqdn")
    def latest_revision_fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "latestRevisionFqdn"))

    @builtins.property
    @jsii.member(jsii_name="latestRevisionName")
    def latest_revision_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "latestRevisionName"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="outboundIpAddresses")
    def outbound_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outboundIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="registry")
    def registry(self) -> "ContainerAppRegistryList":
        return typing.cast("ContainerAppRegistryList", jsii.get(self, "registry"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> "ContainerAppSecretList":
        return typing.cast("ContainerAppSecretList", jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> "ContainerAppTemplateOutputReference":
        return typing.cast("ContainerAppTemplateOutputReference", jsii.get(self, "template"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ContainerAppTimeoutsOutputReference":
        return typing.cast("ContainerAppTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="containerAppEnvironmentIdInput")
    def container_app_environment_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerAppEnvironmentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="daprInput")
    def dapr_input(self) -> typing.Optional["ContainerAppDapr"]:
        return typing.cast(typing.Optional["ContainerAppDapr"], jsii.get(self, "daprInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["ContainerAppIdentity"]:
        return typing.cast(typing.Optional["ContainerAppIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressInput")
    def ingress_input(self) -> typing.Optional["ContainerAppIngress"]:
        return typing.cast(typing.Optional["ContainerAppIngress"], jsii.get(self, "ingressInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInactiveRevisionsInput")
    def max_inactive_revisions_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInactiveRevisionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="registryInput")
    def registry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppRegistry"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppRegistry"]]], jsii.get(self, "registryInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="revisionModeInput")
    def revision_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "revisionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppSecret"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppSecret"]]], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional["ContainerAppTemplate"]:
        return typing.cast(typing.Optional["ContainerAppTemplate"], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAppTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAppTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadProfileNameInput")
    def workload_profile_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workloadProfileNameInput"))

    @builtins.property
    @jsii.member(jsii_name="containerAppEnvironmentId")
    def container_app_environment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerAppEnvironmentId"))

    @container_app_environment_id.setter
    def container_app_environment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ecf9c4acb19649ee7830a966f9c532410c371b02e782688376a5324f76ead72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerAppEnvironmentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3de8247276175bc52f83edd51ad3ab7db2bd115d679dafa22eeed55d63903d9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxInactiveRevisions")
    def max_inactive_revisions(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInactiveRevisions"))

    @max_inactive_revisions.setter
    def max_inactive_revisions(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f547c012f9b9d264667faebb7804fcffa90f1681d339dfebd5010a1eb66d9a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInactiveRevisions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19705745af8b888c3d739bd9b7eeb7389b5e21c16d1f809ab2499ef58d16a7ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d2adf02e4e89dfe65b73fe8e1f4715a397935a8716dd4caeaf599568d327b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revisionMode")
    def revision_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revisionMode"))

    @revision_mode.setter
    def revision_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7856a6d4bc92d97d87c36fb71213c28702b60f012957d1009f599de3034ede3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revisionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b25142a32a2e7f01ac4b76de05ad599d2e2ded49a998c0a9b86a0714898e98a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadProfileName")
    def workload_profile_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadProfileName"))

    @workload_profile_name.setter
    def workload_profile_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006e0877e9a3afe591122cd91de4a5f9513c42b96de19c5a39321972ff27bcf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadProfileName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "container_app_environment_id": "containerAppEnvironmentId",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "revision_mode": "revisionMode",
        "template": "template",
        "dapr": "dapr",
        "id": "id",
        "identity": "identity",
        "ingress": "ingress",
        "max_inactive_revisions": "maxInactiveRevisions",
        "registry": "registry",
        "secret": "secret",
        "tags": "tags",
        "timeouts": "timeouts",
        "workload_profile_name": "workloadProfileName",
    },
)
class ContainerAppConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        container_app_environment_id: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        revision_mode: builtins.str,
        template: typing.Union["ContainerAppTemplate", typing.Dict[builtins.str, typing.Any]],
        dapr: typing.Optional[typing.Union["ContainerAppDapr", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ContainerAppIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        ingress: typing.Optional[typing.Union["ContainerAppIngress", typing.Dict[builtins.str, typing.Any]]] = None,
        max_inactive_revisions: typing.Optional[jsii.Number] = None,
        registry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppRegistry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppSecret", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ContainerAppTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_profile_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param container_app_environment_id: The ID of the Container App Environment to host this Container App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#container_app_environment_id ContainerApp#container_app_environment_id}
        :param name: The name for this Container App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#resource_group_name ContainerApp#resource_group_name}.
        :param revision_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#revision_mode ContainerApp#revision_mode}.
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#template ContainerApp#template}
        :param dapr: dapr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#dapr ContainerApp#dapr}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#id ContainerApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#identity ContainerApp#identity}
        :param ingress: ingress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#ingress ContainerApp#ingress}
        :param max_inactive_revisions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#max_inactive_revisions ContainerApp#max_inactive_revisions}.
        :param registry: registry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#registry ContainerApp#registry}
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#secret ContainerApp#secret}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#tags ContainerApp#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#timeouts ContainerApp#timeouts}
        :param workload_profile_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#workload_profile_name ContainerApp#workload_profile_name}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(template, dict):
            template = ContainerAppTemplate(**template)
        if isinstance(dapr, dict):
            dapr = ContainerAppDapr(**dapr)
        if isinstance(identity, dict):
            identity = ContainerAppIdentity(**identity)
        if isinstance(ingress, dict):
            ingress = ContainerAppIngress(**ingress)
        if isinstance(timeouts, dict):
            timeouts = ContainerAppTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef4933c6f7b389cb1316d1608a878808a652469c82fb2ff9fc03059bb6b7639)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument container_app_environment_id", value=container_app_environment_id, expected_type=type_hints["container_app_environment_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument revision_mode", value=revision_mode, expected_type=type_hints["revision_mode"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument dapr", value=dapr, expected_type=type_hints["dapr"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument ingress", value=ingress, expected_type=type_hints["ingress"])
            check_type(argname="argument max_inactive_revisions", value=max_inactive_revisions, expected_type=type_hints["max_inactive_revisions"])
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument workload_profile_name", value=workload_profile_name, expected_type=type_hints["workload_profile_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_app_environment_id": container_app_environment_id,
            "name": name,
            "resource_group_name": resource_group_name,
            "revision_mode": revision_mode,
            "template": template,
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
        if dapr is not None:
            self._values["dapr"] = dapr
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if ingress is not None:
            self._values["ingress"] = ingress
        if max_inactive_revisions is not None:
            self._values["max_inactive_revisions"] = max_inactive_revisions
        if registry is not None:
            self._values["registry"] = registry
        if secret is not None:
            self._values["secret"] = secret
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if workload_profile_name is not None:
            self._values["workload_profile_name"] = workload_profile_name

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
    def container_app_environment_id(self) -> builtins.str:
        '''The ID of the Container App Environment to host this Container App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#container_app_environment_id ContainerApp#container_app_environment_id}
        '''
        result = self._values.get("container_app_environment_id")
        assert result is not None, "Required property 'container_app_environment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for this Container App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#resource_group_name ContainerApp#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def revision_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#revision_mode ContainerApp#revision_mode}.'''
        result = self._values.get("revision_mode")
        assert result is not None, "Required property 'revision_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template(self) -> "ContainerAppTemplate":
        '''template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#template ContainerApp#template}
        '''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast("ContainerAppTemplate", result)

    @builtins.property
    def dapr(self) -> typing.Optional["ContainerAppDapr"]:
        '''dapr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#dapr ContainerApp#dapr}
        '''
        result = self._values.get("dapr")
        return typing.cast(typing.Optional["ContainerAppDapr"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#id ContainerApp#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["ContainerAppIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#identity ContainerApp#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["ContainerAppIdentity"], result)

    @builtins.property
    def ingress(self) -> typing.Optional["ContainerAppIngress"]:
        '''ingress block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#ingress ContainerApp#ingress}
        '''
        result = self._values.get("ingress")
        return typing.cast(typing.Optional["ContainerAppIngress"], result)

    @builtins.property
    def max_inactive_revisions(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#max_inactive_revisions ContainerApp#max_inactive_revisions}.'''
        result = self._values.get("max_inactive_revisions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def registry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppRegistry"]]]:
        '''registry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#registry ContainerApp#registry}
        '''
        result = self._values.get("registry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppRegistry"]]], result)

    @builtins.property
    def secret(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppSecret"]]]:
        '''secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#secret ContainerApp#secret}
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppSecret"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#tags ContainerApp#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContainerAppTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#timeouts ContainerApp#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContainerAppTimeouts"], result)

    @builtins.property
    def workload_profile_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#workload_profile_name ContainerApp#workload_profile_name}.'''
        result = self._values.get("workload_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppDapr",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "app_port": "appPort",
        "app_protocol": "appProtocol",
    },
)
class ContainerAppDapr:
    def __init__(
        self,
        *,
        app_id: builtins.str,
        app_port: typing.Optional[jsii.Number] = None,
        app_protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param app_id: The Dapr Application Identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#app_id ContainerApp#app_id}
        :param app_port: The port which the application is listening on. This is the same as the ``ingress`` port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#app_port ContainerApp#app_port}
        :param app_protocol: The protocol for the app. Possible values include ``http`` and ``grpc``. Defaults to ``http``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#app_protocol ContainerApp#app_protocol}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55ba1fd3395176bcd35feadafa390baf247798b5b00082cde7728f8b1c017a57)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument app_port", value=app_port, expected_type=type_hints["app_port"])
            check_type(argname="argument app_protocol", value=app_protocol, expected_type=type_hints["app_protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_id": app_id,
        }
        if app_port is not None:
            self._values["app_port"] = app_port
        if app_protocol is not None:
            self._values["app_protocol"] = app_protocol

    @builtins.property
    def app_id(self) -> builtins.str:
        '''The Dapr Application Identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#app_id ContainerApp#app_id}
        '''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_port(self) -> typing.Optional[jsii.Number]:
        '''The port which the application is listening on. This is the same as the ``ingress`` port.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#app_port ContainerApp#app_port}
        '''
        result = self._values.get("app_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def app_protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol for the app. Possible values include ``http`` and ``grpc``. Defaults to ``http``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#app_protocol ContainerApp#app_protocol}
        '''
        result = self._values.get("app_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppDapr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppDaprOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppDaprOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68503c60b1a85ece06eb0e212f000726c80dbb50bd098848c31325c955b30187)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAppPort")
    def reset_app_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppPort", []))

    @jsii.member(jsii_name="resetAppProtocol")
    def reset_app_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppProtocol", []))

    @builtins.property
    @jsii.member(jsii_name="appIdInput")
    def app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appPortInput")
    def app_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "appPortInput"))

    @builtins.property
    @jsii.member(jsii_name="appProtocolInput")
    def app_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @app_id.setter
    def app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f85e61f40595e3e2abbadf713d291d55fdbb82c3cedec0e295c7fc3bad8548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appPort")
    def app_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "appPort"))

    @app_port.setter
    def app_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cf79021921548e02f28bc46ddc8af7fa682cbcaf0e81dd872661a0cd88b804f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appProtocol")
    def app_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appProtocol"))

    @app_protocol.setter
    def app_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__815ddaffbfe627317ffcc1e9e507f5ad5e97a508b4000d1f7ca977bedff8b327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAppDapr]:
        return typing.cast(typing.Optional[ContainerAppDapr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ContainerAppDapr]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1dde5021f995755fa83765b01e33ea8bfd3e5adf5441ec8ed9ac5b454627b37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class ContainerAppIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#type ContainerApp#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#identity_ids ContainerApp#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b7d9b8b8f67c98f8f7fc137b1cb5d845fbfde889dcdf557745980564cee9f97)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#type ContainerApp#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#identity_ids ContainerApp#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04f11a6cfdc4e7a1c4041786626cd9d7200f55540e1e53b249d893fdd8cb6c4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdentityIds")
    def reset_identity_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityIds", []))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370a9e729757c0174b86b7a1b57bb075ea0685b78b541f7c0cf062d1da0d42ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bce3f953abd635b059574972b28ca915ab3af243924d6fd99be3df7554edbf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAppIdentity]:
        return typing.cast(typing.Optional[ContainerAppIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ContainerAppIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015d8afcbdc1afefa72c56098a612418a92afa16d055ceb4e2ed18866ca335d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppIngress",
    jsii_struct_bases=[],
    name_mapping={
        "target_port": "targetPort",
        "traffic_weight": "trafficWeight",
        "allow_insecure_connections": "allowInsecureConnections",
        "client_certificate_mode": "clientCertificateMode",
        "cors": "cors",
        "exposed_port": "exposedPort",
        "external_enabled": "externalEnabled",
        "ip_security_restriction": "ipSecurityRestriction",
        "transport": "transport",
    },
)
class ContainerAppIngress:
    def __init__(
        self,
        *,
        target_port: jsii.Number,
        traffic_weight: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppIngressTrafficWeight", typing.Dict[builtins.str, typing.Any]]]],
        allow_insecure_connections: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_certificate_mode: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Union["ContainerAppIngressCors", typing.Dict[builtins.str, typing.Any]]] = None,
        exposed_port: typing.Optional[jsii.Number] = None,
        external_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_security_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppIngressIpSecurityRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        transport: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_port: The target port on the container for the Ingress traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#target_port ContainerApp#target_port}
        :param traffic_weight: traffic_weight block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#traffic_weight ContainerApp#traffic_weight}
        :param allow_insecure_connections: Should this ingress allow insecure connections? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#allow_insecure_connections ContainerApp#allow_insecure_connections}
        :param client_certificate_mode: Client certificate mode for mTLS authentication. Ignore indicates server drops client certificate on forwarding. Accept indicates server forwards client certificate but does not require a client certificate. Require indicates server requires a client certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#client_certificate_mode ContainerApp#client_certificate_mode}
        :param cors: cors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#cors ContainerApp#cors}
        :param exposed_port: The exposed port on the container for the Ingress traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#exposed_port ContainerApp#exposed_port}
        :param external_enabled: Is this an external Ingress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#external_enabled ContainerApp#external_enabled}
        :param ip_security_restriction: ip_security_restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#ip_security_restriction ContainerApp#ip_security_restriction}
        :param transport: The transport method for the Ingress. Possible values include ``auto``, ``http``, and ``http2``, ``tcp``. Defaults to ``auto``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#transport ContainerApp#transport}
        '''
        if isinstance(cors, dict):
            cors = ContainerAppIngressCors(**cors)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e16fa4bf221e40e688f48b83977355c89e9b8bfaf159d1118170ee21489c209)
            check_type(argname="argument target_port", value=target_port, expected_type=type_hints["target_port"])
            check_type(argname="argument traffic_weight", value=traffic_weight, expected_type=type_hints["traffic_weight"])
            check_type(argname="argument allow_insecure_connections", value=allow_insecure_connections, expected_type=type_hints["allow_insecure_connections"])
            check_type(argname="argument client_certificate_mode", value=client_certificate_mode, expected_type=type_hints["client_certificate_mode"])
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument exposed_port", value=exposed_port, expected_type=type_hints["exposed_port"])
            check_type(argname="argument external_enabled", value=external_enabled, expected_type=type_hints["external_enabled"])
            check_type(argname="argument ip_security_restriction", value=ip_security_restriction, expected_type=type_hints["ip_security_restriction"])
            check_type(argname="argument transport", value=transport, expected_type=type_hints["transport"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_port": target_port,
            "traffic_weight": traffic_weight,
        }
        if allow_insecure_connections is not None:
            self._values["allow_insecure_connections"] = allow_insecure_connections
        if client_certificate_mode is not None:
            self._values["client_certificate_mode"] = client_certificate_mode
        if cors is not None:
            self._values["cors"] = cors
        if exposed_port is not None:
            self._values["exposed_port"] = exposed_port
        if external_enabled is not None:
            self._values["external_enabled"] = external_enabled
        if ip_security_restriction is not None:
            self._values["ip_security_restriction"] = ip_security_restriction
        if transport is not None:
            self._values["transport"] = transport

    @builtins.property
    def target_port(self) -> jsii.Number:
        '''The target port on the container for the Ingress traffic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#target_port ContainerApp#target_port}
        '''
        result = self._values.get("target_port")
        assert result is not None, "Required property 'target_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def traffic_weight(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppIngressTrafficWeight"]]:
        '''traffic_weight block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#traffic_weight ContainerApp#traffic_weight}
        '''
        result = self._values.get("traffic_weight")
        assert result is not None, "Required property 'traffic_weight' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppIngressTrafficWeight"]], result)

    @builtins.property
    def allow_insecure_connections(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should this ingress allow insecure connections?

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#allow_insecure_connections ContainerApp#allow_insecure_connections}
        '''
        result = self._values.get("allow_insecure_connections")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_certificate_mode(self) -> typing.Optional[builtins.str]:
        '''Client certificate mode for mTLS authentication.

        Ignore indicates server drops client certificate on forwarding. Accept indicates server forwards client certificate but does not require a client certificate. Require indicates server requires a client certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#client_certificate_mode ContainerApp#client_certificate_mode}
        '''
        result = self._values.get("client_certificate_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors(self) -> typing.Optional["ContainerAppIngressCors"]:
        '''cors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#cors ContainerApp#cors}
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional["ContainerAppIngressCors"], result)

    @builtins.property
    def exposed_port(self) -> typing.Optional[jsii.Number]:
        '''The exposed port on the container for the Ingress traffic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#exposed_port ContainerApp#exposed_port}
        '''
        result = self._values.get("exposed_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def external_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Is this an external Ingress.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#external_enabled ContainerApp#external_enabled}
        '''
        result = self._values.get("external_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip_security_restriction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppIngressIpSecurityRestriction"]]]:
        '''ip_security_restriction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#ip_security_restriction ContainerApp#ip_security_restriction}
        '''
        result = self._values.get("ip_security_restriction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppIngressIpSecurityRestriction"]]], result)

    @builtins.property
    def transport(self) -> typing.Optional[builtins.str]:
        '''The transport method for the Ingress. Possible values include ``auto``, ``http``, and ``http2``, ``tcp``. Defaults to ``auto``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#transport ContainerApp#transport}
        '''
        result = self._values.get("transport")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppIngress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppIngressCors",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_origins": "allowedOrigins",
        "allow_credentials_enabled": "allowCredentialsEnabled",
        "allowed_headers": "allowedHeaders",
        "allowed_methods": "allowedMethods",
        "exposed_headers": "exposedHeaders",
        "max_age_in_seconds": "maxAgeInSeconds",
    },
)
class ContainerAppIngressCors:
    def __init__(
        self,
        *,
        allowed_origins: typing.Sequence[builtins.str],
        allow_credentials_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        exposed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_age_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allowed_origins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#allowed_origins ContainerApp#allowed_origins}.
        :param allow_credentials_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#allow_credentials_enabled ContainerApp#allow_credentials_enabled}.
        :param allowed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#allowed_headers ContainerApp#allowed_headers}.
        :param allowed_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#allowed_methods ContainerApp#allowed_methods}.
        :param exposed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#exposed_headers ContainerApp#exposed_headers}.
        :param max_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#max_age_in_seconds ContainerApp#max_age_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__929902f62516e315f66d416f1c5eeeb6711138aca1d29b6fc4c5905bcc20c69c)
            check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
            check_type(argname="argument allow_credentials_enabled", value=allow_credentials_enabled, expected_type=type_hints["allow_credentials_enabled"])
            check_type(argname="argument allowed_headers", value=allowed_headers, expected_type=type_hints["allowed_headers"])
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument exposed_headers", value=exposed_headers, expected_type=type_hints["exposed_headers"])
            check_type(argname="argument max_age_in_seconds", value=max_age_in_seconds, expected_type=type_hints["max_age_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_origins": allowed_origins,
        }
        if allow_credentials_enabled is not None:
            self._values["allow_credentials_enabled"] = allow_credentials_enabled
        if allowed_headers is not None:
            self._values["allowed_headers"] = allowed_headers
        if allowed_methods is not None:
            self._values["allowed_methods"] = allowed_methods
        if exposed_headers is not None:
            self._values["exposed_headers"] = exposed_headers
        if max_age_in_seconds is not None:
            self._values["max_age_in_seconds"] = max_age_in_seconds

    @builtins.property
    def allowed_origins(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#allowed_origins ContainerApp#allowed_origins}.'''
        result = self._values.get("allowed_origins")
        assert result is not None, "Required property 'allowed_origins' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allow_credentials_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#allow_credentials_enabled ContainerApp#allow_credentials_enabled}.'''
        result = self._values.get("allow_credentials_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allowed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#allowed_headers ContainerApp#allowed_headers}.'''
        result = self._values.get("allowed_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#allowed_methods ContainerApp#allowed_methods}.'''
        result = self._values.get("allowed_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exposed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#exposed_headers ContainerApp#exposed_headers}.'''
        result = self._values.get("exposed_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_age_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#max_age_in_seconds ContainerApp#max_age_in_seconds}.'''
        result = self._values.get("max_age_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppIngressCors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppIngressCorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppIngressCorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de22ca49ca645fd1e7eff774a19b8f8128d4f73ff32dff01281728b257583a7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowCredentialsEnabled")
    def reset_allow_credentials_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowCredentialsEnabled", []))

    @jsii.member(jsii_name="resetAllowedHeaders")
    def reset_allowed_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedHeaders", []))

    @jsii.member(jsii_name="resetAllowedMethods")
    def reset_allowed_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedMethods", []))

    @jsii.member(jsii_name="resetExposedHeaders")
    def reset_exposed_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExposedHeaders", []))

    @jsii.member(jsii_name="resetMaxAgeInSeconds")
    def reset_max_age_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAgeInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="allowCredentialsEnabledInput")
    def allow_credentials_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowCredentialsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedHeadersInput")
    def allowed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedOriginsInput")
    def allowed_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="exposedHeadersInput")
    def exposed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exposedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeInSecondsInput")
    def max_age_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAgeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowCredentialsEnabled")
    def allow_credentials_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowCredentialsEnabled"))

    @allow_credentials_enabled.setter
    def allow_credentials_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc993b968193f5b04f24121ded13cb3e65397110ae2df401b468b3a528acaa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowCredentialsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedHeaders")
    def allowed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedHeaders"))

    @allowed_headers.setter
    def allowed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d862ea58b945b1a07bc03cfbe128b33d4275d51ce0df62f47946740bde1edb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMethods"))

    @allowed_methods.setter
    def allowed_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e700ec7aa7c7e2a781ed7da85b54423cbfcaf8c41ddaf105e8a35ddc10f3cdae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOrigins"))

    @allowed_origins.setter
    def allowed_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad8dc761ef267116369ba39749e210ba1f510a7d8780df1ac5684a0a0559e6f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOrigins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exposedHeaders")
    def exposed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exposedHeaders"))

    @exposed_headers.setter
    def exposed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca75d93b8865d3e2409f58692a0378e38978b34faa2224801a1f56603f11dc92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAgeInSeconds")
    def max_age_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAgeInSeconds"))

    @max_age_in_seconds.setter
    def max_age_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693111cb8900bab6587f6a5d1ec3d06fbb2051867df5ecdf9d5125321b5ada6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAgeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAppIngressCors]:
        return typing.cast(typing.Optional[ContainerAppIngressCors], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ContainerAppIngressCors]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__766269472b1d717025edd63e9c9c252529d4695b685bfa6a4ba50f34214c4a12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppIngressCustomDomain",
    jsii_struct_bases=[],
    name_mapping={},
)
class ContainerAppIngressCustomDomain:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppIngressCustomDomain(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppIngressCustomDomainList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppIngressCustomDomainList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2ae1fb6c5b09a9d0551b7eec17d739e092eb03d9e90865a5c97e4f13900c8d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppIngressCustomDomainOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6434e8b28ded9df2424d0635cb1ca8a51dd28a9da278c79e304878d1a9f2473)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppIngressCustomDomainOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7daccfd746887f648f239cd41c619d9d4f506ba71efc7c2e1e2a605230d372)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f784ff4f75bd60aaf9e857d7a680f76b88f16e8d964e562ee4de48bcab56c62e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7715c239aee3d74639db328903558946cf29d1d37aa68cb84bef6216d2d909bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ContainerAppIngressCustomDomainOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppIngressCustomDomainOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f24a79c79db45167303cec3cf04dfbdef12ea603bfd1fb3fd1e792eaa116967b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="certificateBindingType")
    def certificate_binding_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateBindingType"))

    @builtins.property
    @jsii.member(jsii_name="certificateId")
    def certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateId"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAppIngressCustomDomain]:
        return typing.cast(typing.Optional[ContainerAppIngressCustomDomain], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAppIngressCustomDomain],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40fbe6d43f2f4426bb668ebb0123547e883398fc4293d8a810bc53f8f6ce7adb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppIngressIpSecurityRestriction",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "ip_address_range": "ipAddressRange",
        "name": "name",
        "description": "description",
    },
)
class ContainerAppIngressIpSecurityRestriction:
    def __init__(
        self,
        *,
        action: builtins.str,
        ip_address_range: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: The action. Allow or Deny. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#action ContainerApp#action}
        :param ip_address_range: The incoming IP address or range of IP addresses (in CIDR notation). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#ip_address_range ContainerApp#ip_address_range}
        :param name: Name for the IP restriction rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        :param description: Describe the IP restriction rule that is being sent to the container-app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#description ContainerApp#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3163d33d2e2dc053402b46f8acf2e702ffe0f5dbb7405f3b97332e09e3f783e)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument ip_address_range", value=ip_address_range, expected_type=type_hints["ip_address_range"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "ip_address_range": ip_address_range,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def action(self) -> builtins.str:
        '''The action. Allow or Deny.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#action ContainerApp#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_address_range(self) -> builtins.str:
        '''The incoming IP address or range of IP addresses (in CIDR notation).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#ip_address_range ContainerApp#ip_address_range}
        '''
        result = self._values.get("ip_address_range")
        assert result is not None, "Required property 'ip_address_range' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name for the IP restriction rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Describe the IP restriction rule that is being sent to the container-app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#description ContainerApp#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppIngressIpSecurityRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppIngressIpSecurityRestrictionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppIngressIpSecurityRestrictionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a8d5f6de8e13dbc87e26de408d0b9019ff793fe52c650583679318f2724a404)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppIngressIpSecurityRestrictionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd7e91d5ac8655cde214120bd056a233443ab8352a8f19cb3c1f7c050898c6b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppIngressIpSecurityRestrictionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9088681254dece9ea8632550c0dea7add0e2e5e0670e69a31e94f3e587ab775c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce5ab8dc3b0c48c554708a8ea724071f19981f2588a7397c420322b5bbae0f8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7be71861b6be9c7e7189a6369862a0f3036b09c671765ccbe1d911631eb1222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppIngressIpSecurityRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppIngressIpSecurityRestriction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppIngressIpSecurityRestriction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f56d15d3ae8c55fc467c71712c2fb703a73dffe6a2a04bda61e87c81ba01ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppIngressIpSecurityRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppIngressIpSecurityRestrictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__278048a27d27875e5f1b6dc5fda075772029dfe56465a74702683410d55681c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressRangeInput")
    def ip_address_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f55fced17f04b113e01f76ed2b05cc92a62e4d482b4ae205cdfc90ab2edd31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caace6b8dddd7940d85944fe0aec1dae7b4cbc2d8334584f501095b89d5a36bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddressRange")
    def ip_address_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressRange"))

    @ip_address_range.setter
    def ip_address_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538c38111e7230f4102134627ddfc96eae66cc7bf873fc9513d0a670506afeec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a846ef4bbf7ffe3e8cd10a253474002a38fa2c6c4b5282425d4e40e04ae35481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppIngressIpSecurityRestriction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppIngressIpSecurityRestriction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppIngressIpSecurityRestriction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c85b234b6843e2aedf72a0b76992dee33934beb5692ece977924663d6548f131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppIngressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppIngressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__940fbf626dacf3f4c987240b99d756b45cbd04a1927e34da8b7a9eba95f7279b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCors")
    def put_cors(
        self,
        *,
        allowed_origins: typing.Sequence[builtins.str],
        allow_credentials_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        exposed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_age_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allowed_origins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#allowed_origins ContainerApp#allowed_origins}.
        :param allow_credentials_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#allow_credentials_enabled ContainerApp#allow_credentials_enabled}.
        :param allowed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#allowed_headers ContainerApp#allowed_headers}.
        :param allowed_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#allowed_methods ContainerApp#allowed_methods}.
        :param exposed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#exposed_headers ContainerApp#exposed_headers}.
        :param max_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#max_age_in_seconds ContainerApp#max_age_in_seconds}.
        '''
        value = ContainerAppIngressCors(
            allowed_origins=allowed_origins,
            allow_credentials_enabled=allow_credentials_enabled,
            allowed_headers=allowed_headers,
            allowed_methods=allowed_methods,
            exposed_headers=exposed_headers,
            max_age_in_seconds=max_age_in_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putCors", [value]))

    @jsii.member(jsii_name="putIpSecurityRestriction")
    def put_ip_security_restriction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppIngressIpSecurityRestriction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2314e4576a6ba08f020a3b0a23271aae6d708ff5747a84a8bf0a81b48ee92aa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpSecurityRestriction", [value]))

    @jsii.member(jsii_name="putTrafficWeight")
    def put_traffic_weight(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppIngressTrafficWeight", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8dbb743ae35455a2e328cda126347ece09036fbb35acba9300b79aa0ad5c1c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTrafficWeight", [value]))

    @jsii.member(jsii_name="resetAllowInsecureConnections")
    def reset_allow_insecure_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowInsecureConnections", []))

    @jsii.member(jsii_name="resetClientCertificateMode")
    def reset_client_certificate_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateMode", []))

    @jsii.member(jsii_name="resetCors")
    def reset_cors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCors", []))

    @jsii.member(jsii_name="resetExposedPort")
    def reset_exposed_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExposedPort", []))

    @jsii.member(jsii_name="resetExternalEnabled")
    def reset_external_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalEnabled", []))

    @jsii.member(jsii_name="resetIpSecurityRestriction")
    def reset_ip_security_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpSecurityRestriction", []))

    @jsii.member(jsii_name="resetTransport")
    def reset_transport(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransport", []))

    @builtins.property
    @jsii.member(jsii_name="cors")
    def cors(self) -> ContainerAppIngressCorsOutputReference:
        return typing.cast(ContainerAppIngressCorsOutputReference, jsii.get(self, "cors"))

    @builtins.property
    @jsii.member(jsii_name="customDomain")
    def custom_domain(self) -> ContainerAppIngressCustomDomainList:
        return typing.cast(ContainerAppIngressCustomDomainList, jsii.get(self, "customDomain"))

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @builtins.property
    @jsii.member(jsii_name="ipSecurityRestriction")
    def ip_security_restriction(self) -> ContainerAppIngressIpSecurityRestrictionList:
        return typing.cast(ContainerAppIngressIpSecurityRestrictionList, jsii.get(self, "ipSecurityRestriction"))

    @builtins.property
    @jsii.member(jsii_name="trafficWeight")
    def traffic_weight(self) -> "ContainerAppIngressTrafficWeightList":
        return typing.cast("ContainerAppIngressTrafficWeightList", jsii.get(self, "trafficWeight"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecureConnectionsInput")
    def allow_insecure_connections_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInsecureConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateModeInput")
    def client_certificate_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateModeInput"))

    @builtins.property
    @jsii.member(jsii_name="corsInput")
    def cors_input(self) -> typing.Optional[ContainerAppIngressCors]:
        return typing.cast(typing.Optional[ContainerAppIngressCors], jsii.get(self, "corsInput"))

    @builtins.property
    @jsii.member(jsii_name="exposedPortInput")
    def exposed_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "exposedPortInput"))

    @builtins.property
    @jsii.member(jsii_name="externalEnabledInput")
    def external_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "externalEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ipSecurityRestrictionInput")
    def ip_security_restriction_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppIngressIpSecurityRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppIngressIpSecurityRestriction]]], jsii.get(self, "ipSecurityRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="targetPortInput")
    def target_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetPortInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficWeightInput")
    def traffic_weight_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppIngressTrafficWeight"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppIngressTrafficWeight"]]], jsii.get(self, "trafficWeightInput"))

    @builtins.property
    @jsii.member(jsii_name="transportInput")
    def transport_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transportInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecureConnections")
    def allow_insecure_connections(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowInsecureConnections"))

    @allow_insecure_connections.setter
    def allow_insecure_connections(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1be0ae9619277c2b120b06d05b9b32b7698e84f8bad867c4f59607f92ad91f3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecureConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificateMode")
    def client_certificate_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateMode"))

    @client_certificate_mode.setter
    def client_certificate_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa502e5181aba2fd57caa97084ffa4eb3f8216b0bdd23e06bb816faef88141a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exposedPort")
    def exposed_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "exposedPort"))

    @exposed_port.setter
    def exposed_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4c98373b1078b43fe0c757dcc50f8e6206941e5e385d46d3e52886963b61bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposedPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalEnabled")
    def external_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "externalEnabled"))

    @external_enabled.setter
    def external_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a762ab14fe1bc810bcead999b55723d4c3edc5aa92d4754e9b1feffdc1e2e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPort")
    def target_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetPort"))

    @target_port.setter
    def target_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6b0727866c78a831f7d558f3485095b96df47f2a3c90eb6ce9748fb8b7722c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transport")
    def transport(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transport"))

    @transport.setter
    def transport(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4466d3e8541fa9dfd13e1afe6c40b94c1d8abb6a1a6a40e543b97b7601386a42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAppIngress]:
        return typing.cast(typing.Optional[ContainerAppIngress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ContainerAppIngress]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e68dd8649e36a602bd5893f9665bb1a5032e01e57beb71b5b0b30d20dabfacc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppIngressTrafficWeight",
    jsii_struct_bases=[],
    name_mapping={
        "percentage": "percentage",
        "label": "label",
        "latest_revision": "latestRevision",
        "revision_suffix": "revisionSuffix",
    },
)
class ContainerAppIngressTrafficWeight:
    def __init__(
        self,
        *,
        percentage: jsii.Number,
        label: typing.Optional[builtins.str] = None,
        latest_revision: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        revision_suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param percentage: The percentage of traffic to send to this revision. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#percentage ContainerApp#percentage}
        :param label: The label to apply to the revision as a name prefix for routing traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#label ContainerApp#label}
        :param latest_revision: This traffic Weight relates to the latest stable Container Revision. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#latest_revision ContainerApp#latest_revision}
        :param revision_suffix: The suffix string to append to the revision. This must be unique for the Container App's lifetime. A default hash created by the service will be used if this value is omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#revision_suffix ContainerApp#revision_suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df343944e26e19384e8da93e6321e64f0f11e00b7882161a5e45b5f12f3d747b)
            check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument latest_revision", value=latest_revision, expected_type=type_hints["latest_revision"])
            check_type(argname="argument revision_suffix", value=revision_suffix, expected_type=type_hints["revision_suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "percentage": percentage,
        }
        if label is not None:
            self._values["label"] = label
        if latest_revision is not None:
            self._values["latest_revision"] = latest_revision
        if revision_suffix is not None:
            self._values["revision_suffix"] = revision_suffix

    @builtins.property
    def percentage(self) -> jsii.Number:
        '''The percentage of traffic to send to this revision.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#percentage ContainerApp#percentage}
        '''
        result = self._values.get("percentage")
        assert result is not None, "Required property 'percentage' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''The label to apply to the revision as a name prefix for routing traffic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#label ContainerApp#label}
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def latest_revision(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This traffic Weight relates to the latest stable Container Revision.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#latest_revision ContainerApp#latest_revision}
        '''
        result = self._values.get("latest_revision")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def revision_suffix(self) -> typing.Optional[builtins.str]:
        '''The suffix string to append to the revision.

        This must be unique for the Container App's lifetime. A default hash created by the service will be used if this value is omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#revision_suffix ContainerApp#revision_suffix}
        '''
        result = self._values.get("revision_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppIngressTrafficWeight(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppIngressTrafficWeightList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppIngressTrafficWeightList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__449cb2a85e31c4cff051ef95a2de4a08c79e4c485e8d9555a4cee382329c3f59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppIngressTrafficWeightOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e473b14a0eefc3776f742884899ee9a81f12882812c4f38681976217bf5c8005)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppIngressTrafficWeightOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f1e5c45bbe4eeb99878e8fc41ebfccf9e79a0ea4f05eb59b970c031e4febf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d98464ab18f5eea7592cadf344055018082fce26f2be4f3951f28739ec3318fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__835afeec02739445b51f85e768f3a660819e46708591059085fc0aeff26f282c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppIngressTrafficWeight]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppIngressTrafficWeight]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppIngressTrafficWeight]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d491ec74e9b6bc781783347c0cf67a13ce8750bda34c3d347f64d62b00efa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppIngressTrafficWeightOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppIngressTrafficWeightOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da55329d7ae1312f81a3b79aacdf0aec466e3c7a9a18f180b8ca8b3d73062fbb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLabel")
    def reset_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabel", []))

    @jsii.member(jsii_name="resetLatestRevision")
    def reset_latest_revision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLatestRevision", []))

    @jsii.member(jsii_name="resetRevisionSuffix")
    def reset_revision_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevisionSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="latestRevisionInput")
    def latest_revision_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "latestRevisionInput"))

    @builtins.property
    @jsii.member(jsii_name="percentageInput")
    def percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentageInput"))

    @builtins.property
    @jsii.member(jsii_name="revisionSuffixInput")
    def revision_suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "revisionSuffixInput"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675e4014aebbc2bc854fe89d3e9ff88dd0929fe59d1a66906ac379dac3452d30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="latestRevision")
    def latest_revision(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "latestRevision"))

    @latest_revision.setter
    def latest_revision(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26fb329a124117d70d174f865bb186fc73ac5c7e3253296e2d0847f23793554b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "latestRevision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79db33c638ad524841290aaec297baf034ef2eaef441f28bd0c39a0c3bf50200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revisionSuffix")
    def revision_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revisionSuffix"))

    @revision_suffix.setter
    def revision_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec5552aa96863d057088e9c93d8064355d03670d29afdb269c22fd8dc7b9904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revisionSuffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppIngressTrafficWeight]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppIngressTrafficWeight]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppIngressTrafficWeight]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9880534b4f1fdfad134b9df40ff0d0e717d151c6c7bb664060aa98b17656b721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppRegistry",
    jsii_struct_bases=[],
    name_mapping={
        "server": "server",
        "identity": "identity",
        "password_secret_name": "passwordSecretName",
        "username": "username",
    },
)
class ContainerAppRegistry:
    def __init__(
        self,
        *,
        server: builtins.str,
        identity: typing.Optional[builtins.str] = None,
        password_secret_name: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param server: The hostname for the Container Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#server ContainerApp#server}
        :param identity: ID of the System or User Managed Identity used to pull images from the Container Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#identity ContainerApp#identity}
        :param password_secret_name: The name of the Secret Reference containing the password value for this user on the Container Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#password_secret_name ContainerApp#password_secret_name}
        :param username: The username to use for this Container Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#username ContainerApp#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d4ea0344de6b1cca976766baaf1c3903c036919d800998a8927657a5e1edb7)
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument password_secret_name", value=password_secret_name, expected_type=type_hints["password_secret_name"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "server": server,
        }
        if identity is not None:
            self._values["identity"] = identity
        if password_secret_name is not None:
            self._values["password_secret_name"] = password_secret_name
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def server(self) -> builtins.str:
        '''The hostname for the Container Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#server ContainerApp#server}
        '''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity(self) -> typing.Optional[builtins.str]:
        '''ID of the System or User Managed Identity used to pull images from the Container Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#identity ContainerApp#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password_secret_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Secret Reference containing the password value for this user on the Container Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#password_secret_name ContainerApp#password_secret_name}
        '''
        result = self._values.get("password_secret_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username to use for this Container Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#username ContainerApp#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppRegistry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppRegistryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppRegistryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9488cec1c8de16982f72bf01c4704a03907d679f43727072e64a77e1606c8a8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerAppRegistryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553f12ce33a56d912808cd84c3cfa215b9f96c04795b1bd9767875adc30abbda)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppRegistryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2731671623fea1a8ecf2d650074635a7f919a32fa81a4f698c83346a7484f383)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e63873680582b3bd3fd04a69040bde3ca063ccab30ae4188ec25c81d5ef42940)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b74848dba46b539383e4d626406032f5afed4197ddf82a7f21867d83a09e069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppRegistry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppRegistry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppRegistry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a29b9c6faf02d4ab62c427b4c218833996f163b477ee764c22df80467315de15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppRegistryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppRegistryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbd5f354b7c16f0cc90cfef95e41213aa8ba9a912baecf1558c26e097180379a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetPasswordSecretName")
    def reset_password_secret_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordSecretName", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordSecretNameInput")
    def password_secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordSecretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serverInput")
    def server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identity"))

    @identity.setter
    def identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67664b3b33b5f36dabc2a28c251e4016efceab5791ad328797e8837eb528eda4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordSecretName")
    def password_secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordSecretName"))

    @password_secret_name.setter
    def password_secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc694de369b4cd372bfd53dbc08b39fd622c0407ccd6268ec0bb8712809305eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordSecretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80d782c03c58d43f2bd77ab6a09f5b89e8b860b11e04537c3c9f25c9500fbca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2542c3a050cf0233b275bd0077f0c4726bea7ffdcaa784a89a542d0cbf574760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppRegistry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppRegistry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppRegistry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8483b444c1c48d0d9f850edcdf9510b18c0ce89fafc01e91d24884e7a4792d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppSecret",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "identity": "identity",
        "key_vault_secret_id": "keyVaultSecretId",
        "value": "value",
    },
)
class ContainerAppSecret:
    def __init__(
        self,
        *,
        name: builtins.str,
        identity: typing.Optional[builtins.str] = None,
        key_vault_secret_id: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The secret name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        :param identity: The identity to use for accessing key vault reference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#identity ContainerApp#identity}
        :param key_vault_secret_id: The Key Vault Secret ID. Could be either one of ``id`` or ``versionless_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#key_vault_secret_id ContainerApp#key_vault_secret_id}
        :param value: The value for this secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#value ContainerApp#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72091c9c14a3dcbddab91d1501c0c8a23dcce091c37f04454dd65f2833303528)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument key_vault_secret_id", value=key_vault_secret_id, expected_type=type_hints["key_vault_secret_id"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if identity is not None:
            self._values["identity"] = identity
        if key_vault_secret_id is not None:
            self._values["key_vault_secret_id"] = key_vault_secret_id
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> builtins.str:
        '''The secret name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity(self) -> typing.Optional[builtins.str]:
        '''The identity to use for accessing key vault reference.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#identity ContainerApp#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_secret_id(self) -> typing.Optional[builtins.str]:
        '''The Key Vault Secret ID. Could be either one of ``id`` or ``versionless_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#key_vault_secret_id ContainerApp#key_vault_secret_id}
        '''
        result = self._values.get("key_vault_secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The value for this secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#value ContainerApp#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppSecretList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppSecretList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a1c8ac5f2b47f71efe9bca7b945eaea78b39a557d19d5e88cde0bd8bebb4c38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerAppSecretOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c3f135f60b3541b6b353620d45814b18a2d5c4365663763973e6c1b15aa205)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppSecretOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db56308f44c61d63da6b18f57867ea1ef481ea27633d4bc3bbc1e3291d51037)
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
            type_hints = typing.get_type_hints(_typecheckingstub__766c85fa3edae8f54469f8c99786c2cedcf775a7f5f908a7382d41e029e1a0da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e25a0880582f4e88c38678ebefdd02fc614939cf397ff56c16f33edb0cc58234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppSecret]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppSecret]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppSecret]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af594e669317f5ab18a4a710f84301559f54c3975b8f07bb688165053f6baaac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__302cba9f6bc935ab5aef90c1e9e8d96e589afcbc59004de0837cf72acaebd88d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetKeyVaultSecretId")
    def reset_key_vault_secret_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultSecretId", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultSecretIdInput")
    def key_vault_secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultSecretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identity"))

    @identity.setter
    def identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa4ab1eba01c5649d75f004958bebdd48d940608390c1927d5277c3b7c651c31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultSecretId")
    def key_vault_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultSecretId"))

    @key_vault_secret_id.setter
    def key_vault_secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f0adfc8244a960c795ecfd04b100d86cb634965ce3ca9578832a38e84e94f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultSecretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79fe89a0cf8921b9fd18bbc38057888fd44da9775ce3e168a2f0ed8bae86d815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__184fd7f23ef40e29461750a562411c7dec71448559c0d85e665c72225cd3cbfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppSecret]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppSecret]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppSecret]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ffd78fffbc0b018faffabaee7cd512a287538aeae33c98f3907e153b4aaaae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "container": "container",
        "azure_queue_scale_rule": "azureQueueScaleRule",
        "custom_scale_rule": "customScaleRule",
        "http_scale_rule": "httpScaleRule",
        "init_container": "initContainer",
        "max_replicas": "maxReplicas",
        "min_replicas": "minReplicas",
        "revision_suffix": "revisionSuffix",
        "tcp_scale_rule": "tcpScaleRule",
        "termination_grace_period_seconds": "terminationGracePeriodSeconds",
        "volume": "volume",
    },
)
class ContainerAppTemplate:
    def __init__(
        self,
        *,
        container: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateContainer", typing.Dict[builtins.str, typing.Any]]]],
        azure_queue_scale_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateAzureQueueScaleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_scale_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateCustomScaleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http_scale_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateHttpScaleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        init_container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateInitContainer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_replicas: typing.Optional[jsii.Number] = None,
        min_replicas: typing.Optional[jsii.Number] = None,
        revision_suffix: typing.Optional[builtins.str] = None,
        tcp_scale_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateTcpScaleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        termination_grace_period_seconds: typing.Optional[jsii.Number] = None,
        volume: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateVolume", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#container ContainerApp#container}
        :param azure_queue_scale_rule: azure_queue_scale_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#azure_queue_scale_rule ContainerApp#azure_queue_scale_rule}
        :param custom_scale_rule: custom_scale_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#custom_scale_rule ContainerApp#custom_scale_rule}
        :param http_scale_rule: http_scale_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#http_scale_rule ContainerApp#http_scale_rule}
        :param init_container: init_container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#init_container ContainerApp#init_container}
        :param max_replicas: The maximum number of replicas for this container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#max_replicas ContainerApp#max_replicas}
        :param min_replicas: The minimum number of replicas for this container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#min_replicas ContainerApp#min_replicas}
        :param revision_suffix: The suffix for the revision. This value must be unique for the lifetime of the Resource. If omitted the service will use a hash function to create one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#revision_suffix ContainerApp#revision_suffix}
        :param tcp_scale_rule: tcp_scale_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#tcp_scale_rule ContainerApp#tcp_scale_rule}
        :param termination_grace_period_seconds: The time in seconds after the container is sent the termination signal before the process if forcibly killed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#termination_grace_period_seconds ContainerApp#termination_grace_period_seconds}
        :param volume: volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#volume ContainerApp#volume}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0f38ee2050a9a72a6ba8ab8ff306a388b685952d19af92c33d27d7804eeff9c)
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument azure_queue_scale_rule", value=azure_queue_scale_rule, expected_type=type_hints["azure_queue_scale_rule"])
            check_type(argname="argument custom_scale_rule", value=custom_scale_rule, expected_type=type_hints["custom_scale_rule"])
            check_type(argname="argument http_scale_rule", value=http_scale_rule, expected_type=type_hints["http_scale_rule"])
            check_type(argname="argument init_container", value=init_container, expected_type=type_hints["init_container"])
            check_type(argname="argument max_replicas", value=max_replicas, expected_type=type_hints["max_replicas"])
            check_type(argname="argument min_replicas", value=min_replicas, expected_type=type_hints["min_replicas"])
            check_type(argname="argument revision_suffix", value=revision_suffix, expected_type=type_hints["revision_suffix"])
            check_type(argname="argument tcp_scale_rule", value=tcp_scale_rule, expected_type=type_hints["tcp_scale_rule"])
            check_type(argname="argument termination_grace_period_seconds", value=termination_grace_period_seconds, expected_type=type_hints["termination_grace_period_seconds"])
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container": container,
        }
        if azure_queue_scale_rule is not None:
            self._values["azure_queue_scale_rule"] = azure_queue_scale_rule
        if custom_scale_rule is not None:
            self._values["custom_scale_rule"] = custom_scale_rule
        if http_scale_rule is not None:
            self._values["http_scale_rule"] = http_scale_rule
        if init_container is not None:
            self._values["init_container"] = init_container
        if max_replicas is not None:
            self._values["max_replicas"] = max_replicas
        if min_replicas is not None:
            self._values["min_replicas"] = min_replicas
        if revision_suffix is not None:
            self._values["revision_suffix"] = revision_suffix
        if tcp_scale_rule is not None:
            self._values["tcp_scale_rule"] = tcp_scale_rule
        if termination_grace_period_seconds is not None:
            self._values["termination_grace_period_seconds"] = termination_grace_period_seconds
        if volume is not None:
            self._values["volume"] = volume

    @builtins.property
    def container(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainer"]]:
        '''container block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#container ContainerApp#container}
        '''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainer"]], result)

    @builtins.property
    def azure_queue_scale_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateAzureQueueScaleRule"]]]:
        '''azure_queue_scale_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#azure_queue_scale_rule ContainerApp#azure_queue_scale_rule}
        '''
        result = self._values.get("azure_queue_scale_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateAzureQueueScaleRule"]]], result)

    @builtins.property
    def custom_scale_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateCustomScaleRule"]]]:
        '''custom_scale_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#custom_scale_rule ContainerApp#custom_scale_rule}
        '''
        result = self._values.get("custom_scale_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateCustomScaleRule"]]], result)

    @builtins.property
    def http_scale_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateHttpScaleRule"]]]:
        '''http_scale_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#http_scale_rule ContainerApp#http_scale_rule}
        '''
        result = self._values.get("http_scale_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateHttpScaleRule"]]], result)

    @builtins.property
    def init_container(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateInitContainer"]]]:
        '''init_container block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#init_container ContainerApp#init_container}
        '''
        result = self._values.get("init_container")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateInitContainer"]]], result)

    @builtins.property
    def max_replicas(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of replicas for this container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#max_replicas ContainerApp#max_replicas}
        '''
        result = self._values.get("max_replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_replicas(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of replicas for this container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#min_replicas ContainerApp#min_replicas}
        '''
        result = self._values.get("min_replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def revision_suffix(self) -> typing.Optional[builtins.str]:
        '''The suffix for the revision.

        This value must be unique for the lifetime of the Resource. If omitted the service will use a hash function to create one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#revision_suffix ContainerApp#revision_suffix}
        '''
        result = self._values.get("revision_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tcp_scale_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateTcpScaleRule"]]]:
        '''tcp_scale_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#tcp_scale_rule ContainerApp#tcp_scale_rule}
        '''
        result = self._values.get("tcp_scale_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateTcpScaleRule"]]], result)

    @builtins.property
    def termination_grace_period_seconds(self) -> typing.Optional[jsii.Number]:
        '''The time in seconds after the container is sent the termination signal before the process if forcibly killed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#termination_grace_period_seconds ContainerApp#termination_grace_period_seconds}
        '''
        result = self._values.get("termination_grace_period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateVolume"]]]:
        '''volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#volume ContainerApp#volume}
        '''
        result = self._values.get("volume")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateVolume"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateAzureQueueScaleRule",
    jsii_struct_bases=[],
    name_mapping={
        "authentication": "authentication",
        "name": "name",
        "queue_length": "queueLength",
        "queue_name": "queueName",
    },
)
class ContainerAppTemplateAzureQueueScaleRule:
    def __init__(
        self,
        *,
        authentication: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateAzureQueueScaleRuleAuthentication", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        queue_length: jsii.Number,
        queue_name: builtins.str,
    ) -> None:
        '''
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#authentication ContainerApp#authentication}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}.
        :param queue_length: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#queue_length ContainerApp#queue_length}.
        :param queue_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#queue_name ContainerApp#queue_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8440591433d5661498c4973812de956f7d91981266815a948114119ee9f40aa)
            check_type(argname="argument authentication", value=authentication, expected_type=type_hints["authentication"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument queue_length", value=queue_length, expected_type=type_hints["queue_length"])
            check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authentication": authentication,
            "name": name,
            "queue_length": queue_length,
            "queue_name": queue_name,
        }

    @builtins.property
    def authentication(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateAzureQueueScaleRuleAuthentication"]]:
        '''authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#authentication ContainerApp#authentication}
        '''
        result = self._values.get("authentication")
        assert result is not None, "Required property 'authentication' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateAzureQueueScaleRuleAuthentication"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def queue_length(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#queue_length ContainerApp#queue_length}.'''
        result = self._values.get("queue_length")
        assert result is not None, "Required property 'queue_length' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def queue_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#queue_name ContainerApp#queue_name}.'''
        result = self._values.get("queue_name")
        assert result is not None, "Required property 'queue_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateAzureQueueScaleRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateAzureQueueScaleRuleAuthentication",
    jsii_struct_bases=[],
    name_mapping={
        "secret_name": "secretName",
        "trigger_parameter": "triggerParameter",
    },
)
class ContainerAppTemplateAzureQueueScaleRuleAuthentication:
    def __init__(
        self,
        *,
        secret_name: builtins.str,
        trigger_parameter: builtins.str,
    ) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#secret_name ContainerApp#secret_name}.
        :param trigger_parameter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#trigger_parameter ContainerApp#trigger_parameter}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a99e7d5c46ab30bb958c02381531b75e964238c7be5b8457199d414635134a7)
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument trigger_parameter", value=trigger_parameter, expected_type=type_hints["trigger_parameter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_name": secret_name,
            "trigger_parameter": trigger_parameter,
        }

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#secret_name ContainerApp#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_parameter(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#trigger_parameter ContainerApp#trigger_parameter}.'''
        result = self._values.get("trigger_parameter")
        assert result is not None, "Required property 'trigger_parameter' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateAzureQueueScaleRuleAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppTemplateAzureQueueScaleRuleAuthenticationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateAzureQueueScaleRuleAuthenticationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f12a5bf1ad3f4dcd9530f2d7ddb50686fcbdedb5198c5991f9eba6f36a8ba8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateAzureQueueScaleRuleAuthenticationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e1ae4cdd1abe4daccd1eb00b0a415753cf7a72c6a11e264fb923362af03a01)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateAzureQueueScaleRuleAuthenticationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea514433bb14c620d855b1ee7230fd5e73787fc16948bf44239bc7995923695)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aed1c27b21303750ac601ca8c6299fbbc7bcacaf1308115c667faa1748bbde21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c8dbce8562a3a336cb9300a7ad84cc6434a79781defb76b8213f8ccaf6af92b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateAzureQueueScaleRuleAuthentication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateAzureQueueScaleRuleAuthentication]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateAzureQueueScaleRuleAuthentication]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__900cafb9938e0ed77a1296e441e23f4a9f927a2626d9919842f88245eaa453ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateAzureQueueScaleRuleAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateAzureQueueScaleRuleAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af23c342935bd59a956c71ddf5e2b0fdae85153ed8d15be6bee7b90db49a4065)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerParameterInput")
    def trigger_parameter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9cfcfb098ab059891e0912c4275b8a07be4ae67d941794eda99933b9d7a9dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerParameter")
    def trigger_parameter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerParameter"))

    @trigger_parameter.setter
    def trigger_parameter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd7890cb7f7f1c05330168355bd280aa782d5742de775987044b1e280b45562)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerParameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateAzureQueueScaleRuleAuthentication]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateAzureQueueScaleRuleAuthentication]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateAzureQueueScaleRuleAuthentication]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1bbb9cba939470c219aeb2a865a9dab720a71d81f72a209a1bb9a8fc31e19e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateAzureQueueScaleRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateAzureQueueScaleRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8dc170c07c665b8199c4ac64c82685c887fed9cf3b2d1359107fa23897ea769)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateAzureQueueScaleRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08224cf165a51076243454c2b023c6ccb7d9755055d4d369a7e18d667f13ad88)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateAzureQueueScaleRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c2fc75fd341662246e8949407a34f1061818ad768d6210e8367c58d11da9808)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab2e02ee3a6224a10d4c05e4163a2eef5508f4d99c08bf801f250cdb9eac7549)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ce0febdb7b3c247d437e5ba88b80683b0ca8ad65788e925bff85774ef3b5408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateAzureQueueScaleRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateAzureQueueScaleRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateAzureQueueScaleRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6bc491e06341d646cdb20dc7dddf748d1293c10754b1432254fc6f618b2c832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateAzureQueueScaleRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateAzureQueueScaleRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f276d69a423e2288a2fd50553041c58624e0a06c64d44723ad02db27bc645152)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAuthentication")
    def put_authentication(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateAzureQueueScaleRuleAuthentication, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84de7eff6f98f542d2d9c8a66efcea4868f85461434269ba5ca0a16c52fd790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthentication", [value]))

    @builtins.property
    @jsii.member(jsii_name="authentication")
    def authentication(
        self,
    ) -> ContainerAppTemplateAzureQueueScaleRuleAuthenticationList:
        return typing.cast(ContainerAppTemplateAzureQueueScaleRuleAuthenticationList, jsii.get(self, "authentication"))

    @builtins.property
    @jsii.member(jsii_name="authenticationInput")
    def authentication_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateAzureQueueScaleRuleAuthentication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateAzureQueueScaleRuleAuthentication]]], jsii.get(self, "authenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="queueLengthInput")
    def queue_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queueLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="queueNameInput")
    def queue_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueNameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe568bede4f8beaf15bef8f4f203ed825b904d8927290fc63fe91043cc87fe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueLength")
    def queue_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queueLength"))

    @queue_length.setter
    def queue_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af80696ed2679b40ee579a114f53b0d636081cfc5c31da65d98eb6e3230fd7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueName"))

    @queue_name.setter
    def queue_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692f11973988b5900b840adea7fe83fb99ce4ffae26196d723d17ff161b8bb12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateAzureQueueScaleRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateAzureQueueScaleRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateAzureQueueScaleRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9905d605fca20e294fa075413360fdf6a24d15d6747ee09b41e5e03c370ab2cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainer",
    jsii_struct_bases=[],
    name_mapping={
        "cpu": "cpu",
        "image": "image",
        "memory": "memory",
        "name": "name",
        "args": "args",
        "command": "command",
        "env": "env",
        "liveness_probe": "livenessProbe",
        "readiness_probe": "readinessProbe",
        "startup_probe": "startupProbe",
        "volume_mounts": "volumeMounts",
    },
)
class ContainerAppTemplateContainer:
    def __init__(
        self,
        *,
        cpu: jsii.Number,
        image: builtins.str,
        memory: builtins.str,
        name: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateContainerEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        liveness_probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateContainerLivenessProbe", typing.Dict[builtins.str, typing.Any]]]]] = None,
        readiness_probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateContainerReadinessProbe", typing.Dict[builtins.str, typing.Any]]]]] = None,
        startup_probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateContainerStartupProbe", typing.Dict[builtins.str, typing.Any]]]]] = None,
        volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateContainerVolumeMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cpu: The amount of vCPU to allocate to the container. Possible values include ``0.25``, ``0.5``, ``0.75``, ``1.0``, ``1.25``, ``1.5``, ``1.75``, and ``2.0``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.0`` / ``2.0`` or ``0.5`` / ``1.0``. When there's a workload profile specified, there's no such constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#cpu ContainerApp#cpu}
        :param image: The image to use to create the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#image ContainerApp#image}
        :param memory: The amount of memory to allocate to the container. Possible values include ``0.5Gi``, ``1.0Gi``, ``1.5Gi``, ``2.0Gi``, ``2.5Gi``, ``3.0Gi``, ``3.5Gi``, and ``4.0Gi``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.25`` / ``2.5Gi`` or ``0.75`` / ``1.5Gi``. When there's a workload profile specified, there's no such constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#memory ContainerApp#memory}
        :param name: The name of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        :param args: A list of args to pass to the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#args ContainerApp#args}
        :param command: A command to pass to the container to override the default. This is provided as a list of command line elements without spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#command ContainerApp#command}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#env ContainerApp#env}
        :param liveness_probe: liveness_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#liveness_probe ContainerApp#liveness_probe}
        :param readiness_probe: readiness_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#readiness_probe ContainerApp#readiness_probe}
        :param startup_probe: startup_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#startup_probe ContainerApp#startup_probe}
        :param volume_mounts: volume_mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#volume_mounts ContainerApp#volume_mounts}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65787dacf2b743288fb2aa0314db8fe68135e864c6d4a60062a9d70c0bc1c5a1)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument liveness_probe", value=liveness_probe, expected_type=type_hints["liveness_probe"])
            check_type(argname="argument readiness_probe", value=readiness_probe, expected_type=type_hints["readiness_probe"])
            check_type(argname="argument startup_probe", value=startup_probe, expected_type=type_hints["startup_probe"])
            check_type(argname="argument volume_mounts", value=volume_mounts, expected_type=type_hints["volume_mounts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu": cpu,
            "image": image,
            "memory": memory,
            "name": name,
        }
        if args is not None:
            self._values["args"] = args
        if command is not None:
            self._values["command"] = command
        if env is not None:
            self._values["env"] = env
        if liveness_probe is not None:
            self._values["liveness_probe"] = liveness_probe
        if readiness_probe is not None:
            self._values["readiness_probe"] = readiness_probe
        if startup_probe is not None:
            self._values["startup_probe"] = startup_probe
        if volume_mounts is not None:
            self._values["volume_mounts"] = volume_mounts

    @builtins.property
    def cpu(self) -> jsii.Number:
        '''The amount of vCPU to allocate to the container.

        Possible values include ``0.25``, ``0.5``, ``0.75``, ``1.0``, ``1.25``, ``1.5``, ``1.75``, and ``2.0``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.0`` / ``2.0`` or ``0.5`` / ``1.0``. When there's a workload profile specified, there's no such constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#cpu ContainerApp#cpu}
        '''
        result = self._values.get("cpu")
        assert result is not None, "Required property 'cpu' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def image(self) -> builtins.str:
        '''The image to use to create the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#image ContainerApp#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def memory(self) -> builtins.str:
        '''The amount of memory to allocate to the container.

        Possible values include ``0.5Gi``, ``1.0Gi``, ``1.5Gi``, ``2.0Gi``, ``2.5Gi``, ``3.0Gi``, ``3.5Gi``, and ``4.0Gi``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.25`` / ``2.5Gi`` or ``0.75`` / ``1.5Gi``. When there's a workload profile specified, there's no such constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#memory ContainerApp#memory}
        '''
        result = self._values.get("memory")
        assert result is not None, "Required property 'memory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of args to pass to the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#args ContainerApp#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A command to pass to the container to override the default.

        This is provided as a list of command line elements without spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#command ContainerApp#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def env(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerEnv"]]]:
        '''env block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#env ContainerApp#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerEnv"]]], result)

    @builtins.property
    def liveness_probe(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerLivenessProbe"]]]:
        '''liveness_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#liveness_probe ContainerApp#liveness_probe}
        '''
        result = self._values.get("liveness_probe")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerLivenessProbe"]]], result)

    @builtins.property
    def readiness_probe(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerReadinessProbe"]]]:
        '''readiness_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#readiness_probe ContainerApp#readiness_probe}
        '''
        result = self._values.get("readiness_probe")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerReadinessProbe"]]], result)

    @builtins.property
    def startup_probe(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerStartupProbe"]]]:
        '''startup_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#startup_probe ContainerApp#startup_probe}
        '''
        result = self._values.get("startup_probe")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerStartupProbe"]]], result)

    @builtins.property
    def volume_mounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerVolumeMounts"]]]:
        '''volume_mounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#volume_mounts ContainerApp#volume_mounts}
        '''
        result = self._values.get("volume_mounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerVolumeMounts"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "secret_name": "secretName", "value": "value"},
)
class ContainerAppTemplateContainerEnv:
    def __init__(
        self,
        *,
        name: builtins.str,
        secret_name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the environment variable for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        :param secret_name: The name of the secret that contains the value for this environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#secret_name ContainerApp#secret_name}
        :param value: The value for this environment variable. **NOTE:** This value is ignored if ``secret_name`` is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#value ContainerApp#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7187d38829264f69ea66d88bbec759812baaf96178f2082a69e0522723b922d2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if secret_name is not None:
            self._values["secret_name"] = secret_name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the environment variable for the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_name(self) -> typing.Optional[builtins.str]:
        '''The name of the secret that contains the value for this environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#secret_name ContainerApp#secret_name}
        '''
        result = self._values.get("secret_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The value for this environment variable. **NOTE:** This value is ignored if ``secret_name`` is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#value ContainerApp#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateContainerEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppTemplateContainerEnvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerEnvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6be54c385d7da8b913bfb280d8a9b4b405ad9fa5f3035a58657b69e7dc61ff01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateContainerEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__563440914244e2f0c63bf7ff63fadfdab5200fb2b215f67a90a1f9e43c1e9799)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateContainerEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32162f19f61e51f5631c028e346eb42d469a55642c153dd22bc9b52f4c4fc688)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3895c70dd3417cfe87a56bc124405d058ae88100adc1c4472e03257e79d112d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fa751c8f0a82e327b272ab879288bfe556a79da9bf001cea06d3e1ae4c344e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerEnv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e67fc380d213ce594b11ffbe45903b5e2b9904d32271c59ac89a0d0f932ef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateContainerEnvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerEnvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c1fede8acff9d7511111bf16cbaea0746a70085f9acbd01abf8663a0afc7ddc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSecretName")
    def reset_secret_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__937d11c34f1c934341c6d100a37553eeeec7435eb9578678a79f9a3bd35f0f2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e047ae30d6a1aa1d2f3a8fcdb0d17c27c2652ac7219c78fe15e8ced1d9303a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265abd63082fb22d1e86871ae621cc482b7eb74d8ac3045021b408fbc824e828)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerEnv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerEnv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerEnv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a29f1167caa55280da002e2c262d3a527712aa42019bf65c9d346183d5ce198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateContainerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ead7b1381498edb89172836f92c127379704cc036b632f5b5defe8c658a25251)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerAppTemplateContainerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e49630d0aecae74b570bbaecea8969dff2885f8a87e01a192c75fb5b5c1193)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateContainerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4386aec52b3150d577553b8db29d7e11abc9a4bdca224ae839181a5c8c10b2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4633518c521a7090b98b4c2dd13e94fad11b3042032ac0927210b697abacf556)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8290538e77fb2bfecbf4218203565e5874a80cf076eae08da074f59188a23ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainer]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainer]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d96b09265c101edc95db37f208b1bc5659fba19e7c8d800eddf591de2518755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerLivenessProbe",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "transport": "transport",
        "failure_count_threshold": "failureCountThreshold",
        "header": "header",
        "host": "host",
        "initial_delay": "initialDelay",
        "interval_seconds": "intervalSeconds",
        "path": "path",
        "timeout": "timeout",
    },
)
class ContainerAppTemplateContainerLivenessProbe:
    def __init__(
        self,
        *,
        port: jsii.Number,
        transport: builtins.str,
        failure_count_threshold: typing.Optional[jsii.Number] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateContainerLivenessProbeHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        host: typing.Optional[builtins.str] = None,
        initial_delay: typing.Optional[jsii.Number] = None,
        interval_seconds: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param port: The port number on which to connect. Possible values are between ``1`` and ``65535``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#port ContainerApp#port}
        :param transport: Type of probe. Possible values are ``TCP``, ``HTTP``, and ``HTTPS``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#transport ContainerApp#transport}
        :param failure_count_threshold: The number of consecutive failures required to consider this probe as failed. Possible values are between ``1`` and ``30``. Defaults to ``3``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#failure_count_threshold ContainerApp#failure_count_threshold}
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#header ContainerApp#header}
        :param host: The probe hostname. Defaults to the pod IP address. Setting a value for ``Host`` in ``headers`` can be used to override this for ``http`` and ``https`` type probes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#host ContainerApp#host}
        :param initial_delay: The number of seconds elapsed after the container has started before the probe is initiated. Possible values are between ``0`` and ``60``. Defaults to ``1`` seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#initial_delay ContainerApp#initial_delay}
        :param interval_seconds: How often, in seconds, the probe should run. Possible values are between ``1`` and ``240``. Defaults to ``10``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#interval_seconds ContainerApp#interval_seconds}
        :param path: The URI to use with the ``host`` for http type probes. Not valid for ``TCP`` type probes. Defaults to ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#path ContainerApp#path}
        :param timeout: Time in seconds after which the probe times out. Possible values are between ``1`` an ``240``. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#timeout ContainerApp#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ecf26d64e77558622ade789eea744df6be101d85d943de1bc1a69297becbcd4)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument transport", value=transport, expected_type=type_hints["transport"])
            check_type(argname="argument failure_count_threshold", value=failure_count_threshold, expected_type=type_hints["failure_count_threshold"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument initial_delay", value=initial_delay, expected_type=type_hints["initial_delay"])
            check_type(argname="argument interval_seconds", value=interval_seconds, expected_type=type_hints["interval_seconds"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "transport": transport,
        }
        if failure_count_threshold is not None:
            self._values["failure_count_threshold"] = failure_count_threshold
        if header is not None:
            self._values["header"] = header
        if host is not None:
            self._values["host"] = host
        if initial_delay is not None:
            self._values["initial_delay"] = initial_delay
        if interval_seconds is not None:
            self._values["interval_seconds"] = interval_seconds
        if path is not None:
            self._values["path"] = path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port number on which to connect. Possible values are between ``1`` and ``65535``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#port ContainerApp#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def transport(self) -> builtins.str:
        '''Type of probe. Possible values are ``TCP``, ``HTTP``, and ``HTTPS``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#transport ContainerApp#transport}
        '''
        result = self._values.get("transport")
        assert result is not None, "Required property 'transport' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def failure_count_threshold(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive failures required to consider this probe as failed.

        Possible values are between ``1`` and ``30``. Defaults to ``3``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#failure_count_threshold ContainerApp#failure_count_threshold}
        '''
        result = self._values.get("failure_count_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerLivenessProbeHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#header ContainerApp#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerLivenessProbeHeader"]]], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The probe hostname.

        Defaults to the pod IP address. Setting a value for ``Host`` in ``headers`` can be used to override this for ``http`` and ``https`` type probes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#host ContainerApp#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_delay(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds elapsed after the container has started before the probe is initiated.

        Possible values are between ``0`` and ``60``. Defaults to ``1`` seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#initial_delay ContainerApp#initial_delay}
        '''
        result = self._values.get("initial_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often, in seconds, the probe should run. Possible values are between ``1`` and ``240``. Defaults to ``10``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#interval_seconds ContainerApp#interval_seconds}
        '''
        result = self._values.get("interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The URI to use with the ``host`` for http type probes.

        Not valid for ``TCP`` type probes. Defaults to ``/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#path ContainerApp#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Time in seconds after which the probe times out. Possible values are between ``1`` an ``240``. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#timeout ContainerApp#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateContainerLivenessProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerLivenessProbeHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ContainerAppTemplateContainerLivenessProbeHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: The HTTP Header Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        :param value: The HTTP Header value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#value ContainerApp#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aeed8afedfedbeeb04ea544d2b1cf800f3520f001104d4e3a9f65a4ca7a45ae)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The HTTP Header Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The HTTP Header value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#value ContainerApp#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateContainerLivenessProbeHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppTemplateContainerLivenessProbeHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerLivenessProbeHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dd3efbe1dc02997624ebbb3e4f4f6fbcb66f5b62904e596f18e741063e45d17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateContainerLivenessProbeHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe634386368ccaf654f659cff848c338d29d05beabba91d4d29ca1d4df7e304)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateContainerLivenessProbeHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7561bde5492ac79016e01486b993ba62f8bd4c55c8efbf7b7d6979baf735245)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7000330fcdc4beb1ad26649e342cf102a9b639220fc4a322627053b233f2fcee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4adeeeaa674d9871f6dac84f777d6660fb2aa86a7ec97998722e2d8ad6845e15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerLivenessProbeHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerLivenessProbeHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerLivenessProbeHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d97a73d2f9761bfc43375ddd2306e424137e69923b4590443b26ce7a27ecf44a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateContainerLivenessProbeHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerLivenessProbeHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfc487f3eb82e51f6a9cc30ffc6ef4819e5e51d51ef5990187f5ff1fce87319f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__3631fcb890561e1e1153a5769e42f94d17a4c3a2ff51b04201bf16726afc5967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e881be5657f1d4710cd685fa3bbd72fc20e8767270d2bb54ec8828e575b9ffd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerLivenessProbeHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerLivenessProbeHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerLivenessProbeHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a244eb009c13066f30ba48874661846b3a375e4a90b356295621fd2d3fb3d7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateContainerLivenessProbeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerLivenessProbeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a1e9b5cab3a381a01547e33005b27953863046bff6acec9dae4f4b13a7195dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateContainerLivenessProbeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcbeecc1dd57fffa635f026bb6dc3789ad5b0ce940472bdf2db9f1c68b14d43e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateContainerLivenessProbeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce11a1d541077d053820f7fe6778fe533a6bbc0d7cd6a9b27367da81fbdb955)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5996bed9bb7360e2085072156347520e5ff0c11f1eaeabeb12de7273f29b91e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b3001a41a974000368956b6839b1b60bce7c312669952b50b94d4f13935118e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerLivenessProbe]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerLivenessProbe]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerLivenessProbe]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bcc71dddea0013b9d662eabf686cbeb4ba98daa5d9a69486749fd5f9a2278b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateContainerLivenessProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerLivenessProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8d52c9c172d6e115eb504deef70de248baa8cd8f430dbb7d87fcad98a782351)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerLivenessProbeHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__385e392d301ed370fd4831ccb18f745807d8377d8d4b93fb65d34a6ef582589a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="resetFailureCountThreshold")
    def reset_failure_count_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureCountThreshold", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetInitialDelay")
    def reset_initial_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelay", []))

    @jsii.member(jsii_name="resetIntervalSeconds")
    def reset_interval_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalSeconds", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> ContainerAppTemplateContainerLivenessProbeHeaderList:
        return typing.cast(ContainerAppTemplateContainerLivenessProbeHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="terminationGracePeriodSeconds")
    def termination_grace_period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "terminationGracePeriodSeconds"))

    @builtins.property
    @jsii.member(jsii_name="failureCountThresholdInput")
    def failure_count_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureCountThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerLivenessProbeHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerLivenessProbeHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelayInput")
    def initial_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalSecondsInput")
    def interval_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="transportInput")
    def transport_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transportInput"))

    @builtins.property
    @jsii.member(jsii_name="failureCountThreshold")
    def failure_count_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureCountThreshold"))

    @failure_count_threshold.setter
    def failure_count_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc08128123cc02cb1e724f46bdf5570c7ee2f200e0ee4a527271ec2e48fd8db2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureCountThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3528c5ecfbaf3b8ad30728d4d6d1798e552bc62810c8a5fd0d08d5982f383727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelay")
    def initial_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelay"))

    @initial_delay.setter
    def initial_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a37699af179168f471f4570f95801e5bc35c86701e53ea74948360bd43f7422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSeconds")
    def interval_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSeconds"))

    @interval_seconds.setter
    def interval_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__742f73cf4105504f0227a26b6d7bd62d71e9b2a3c85c39c62dd943e5e1e41b61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56aae862f08b7517dc2aca2190b1b0ae8d48c41dd42ccc00cd70afef48fc3dab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d926d916b22c78602b5706e26d40496355e4221461ea158c81a5862765acd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5431126c6c65f4939d48650a93e62869f5d523b9cc2f5908deaf9d8f91f69295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transport")
    def transport(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transport"))

    @transport.setter
    def transport(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcbb3678d02ce272ffbf99b26a60185f25b736765bde8e132dcaed4bacedac96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerLivenessProbe]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerLivenessProbe]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerLivenessProbe]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e375ffa719e569a85ed687959e5d8950f7c376c5d9a0ee345a86dccaab5d4a08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateContainerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__919e26b1b9c4a99977fb588bc0806529162a24fe2d3e6db07da08b926b4f3c10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerEnv, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29dc2dd220062f02d136e3a9c5fa1cb8e07ffd432b48caf48a6d6af72ecba1ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnv", [value]))

    @jsii.member(jsii_name="putLivenessProbe")
    def put_liveness_probe(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerLivenessProbe, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2566db62155552b7b32870fdc6395345d8b9f4ada543df26b94642bbe5b9cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLivenessProbe", [value]))

    @jsii.member(jsii_name="putReadinessProbe")
    def put_readiness_probe(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateContainerReadinessProbe", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce302ed7dbd7e9688bf6ca5681996d6db2587acf9d629b7a2b0e7c0f6595ece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putReadinessProbe", [value]))

    @jsii.member(jsii_name="putStartupProbe")
    def put_startup_probe(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateContainerStartupProbe", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2904bf0c8f4ab8f797945c267b076a1fb9583e4609dc52460de3b8bdcbd588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStartupProbe", [value]))

    @jsii.member(jsii_name="putVolumeMounts")
    def put_volume_mounts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateContainerVolumeMounts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef3c4c2ca6a54e9176c0d0115a1ea348630b67102ecff16387320c1665a6867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumeMounts", [value]))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetLivenessProbe")
    def reset_liveness_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLivenessProbe", []))

    @jsii.member(jsii_name="resetReadinessProbe")
    def reset_readiness_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadinessProbe", []))

    @jsii.member(jsii_name="resetStartupProbe")
    def reset_startup_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartupProbe", []))

    @jsii.member(jsii_name="resetVolumeMounts")
    def reset_volume_mounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeMounts", []))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> ContainerAppTemplateContainerEnvList:
        return typing.cast(ContainerAppTemplateContainerEnvList, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorage")
    def ephemeral_storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ephemeralStorage"))

    @builtins.property
    @jsii.member(jsii_name="livenessProbe")
    def liveness_probe(self) -> ContainerAppTemplateContainerLivenessProbeList:
        return typing.cast(ContainerAppTemplateContainerLivenessProbeList, jsii.get(self, "livenessProbe"))

    @builtins.property
    @jsii.member(jsii_name="readinessProbe")
    def readiness_probe(self) -> "ContainerAppTemplateContainerReadinessProbeList":
        return typing.cast("ContainerAppTemplateContainerReadinessProbeList", jsii.get(self, "readinessProbe"))

    @builtins.property
    @jsii.member(jsii_name="startupProbe")
    def startup_probe(self) -> "ContainerAppTemplateContainerStartupProbeList":
        return typing.cast("ContainerAppTemplateContainerStartupProbeList", jsii.get(self, "startupProbe"))

    @builtins.property
    @jsii.member(jsii_name="volumeMounts")
    def volume_mounts(self) -> "ContainerAppTemplateContainerVolumeMountsList":
        return typing.cast("ContainerAppTemplateContainerVolumeMountsList", jsii.get(self, "volumeMounts"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerEnv]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="livenessProbeInput")
    def liveness_probe_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerLivenessProbe]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerLivenessProbe]]], jsii.get(self, "livenessProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="readinessProbeInput")
    def readiness_probe_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerReadinessProbe"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerReadinessProbe"]]], jsii.get(self, "readinessProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="startupProbeInput")
    def startup_probe_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerStartupProbe"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerStartupProbe"]]], jsii.get(self, "startupProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeMountsInput")
    def volume_mounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerVolumeMounts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerVolumeMounts"]]], jsii.get(self, "volumeMountsInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39873e64f7f9a9bb84bd7f360b46e0b5010d8e65b28fa8a7000ceab3d625154c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267ee49139d48400accdd2991292fadc077c0d92193bd911f01bdeb417f20864)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__209e38734d1b448ce9d6b0226b73938653d8068ec9d08a2de5a3026382d27e4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e06b5ae38e8109f28b74f275f5135b44ccfc17afdd70c35b2f64fbcf7a0f827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49a048c0c31ef147dcce1df15136378a4246634cf4e8e3e6112292c3748b82f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6252d996813a9830113cc485590661b3b8eacc0e5f5d173bfd10be06aa02a78d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainer]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainer]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f5e7d3d68d455a7d5a77244846a6fd8920776b6cf79908fea9d92dbcfe6ff68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerReadinessProbe",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "transport": "transport",
        "failure_count_threshold": "failureCountThreshold",
        "header": "header",
        "host": "host",
        "initial_delay": "initialDelay",
        "interval_seconds": "intervalSeconds",
        "path": "path",
        "success_count_threshold": "successCountThreshold",
        "timeout": "timeout",
    },
)
class ContainerAppTemplateContainerReadinessProbe:
    def __init__(
        self,
        *,
        port: jsii.Number,
        transport: builtins.str,
        failure_count_threshold: typing.Optional[jsii.Number] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateContainerReadinessProbeHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        host: typing.Optional[builtins.str] = None,
        initial_delay: typing.Optional[jsii.Number] = None,
        interval_seconds: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        success_count_threshold: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param port: The port number on which to connect. Possible values are between ``1`` and ``65535``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#port ContainerApp#port}
        :param transport: Type of probe. Possible values are ``TCP``, ``HTTP``, and ``HTTPS``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#transport ContainerApp#transport}
        :param failure_count_threshold: The number of consecutive failures required to consider this probe as failed. Possible values are between ``1`` and ``30``. Defaults to ``3``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#failure_count_threshold ContainerApp#failure_count_threshold}
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#header ContainerApp#header}
        :param host: The probe hostname. Defaults to the pod IP address. Setting a value for ``Host`` in ``headers`` can be used to override this for ``http`` and ``https`` type probes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#host ContainerApp#host}
        :param initial_delay: The number of seconds elapsed after the container has started before the probe is initiated. Possible values are between ``0`` and ``60``. Defaults to ``0`` seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#initial_delay ContainerApp#initial_delay}
        :param interval_seconds: How often, in seconds, the probe should run. Possible values are between ``1`` and ``240``. Defaults to ``10``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#interval_seconds ContainerApp#interval_seconds}
        :param path: The URI to use for http type probes. Not valid for ``TCP`` type probes. Defaults to ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#path ContainerApp#path}
        :param success_count_threshold: The number of consecutive successful responses required to consider this probe as successful. Possible values are between ``1`` and ``10``. Defaults to ``3``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#success_count_threshold ContainerApp#success_count_threshold}
        :param timeout: Time in seconds after which the probe times out. Possible values are between ``1`` an ``240``. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#timeout ContainerApp#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8c6a021b0d75bb5b03c53a25543bf613502a7f472fa4374a6237585e12bd3d4)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument transport", value=transport, expected_type=type_hints["transport"])
            check_type(argname="argument failure_count_threshold", value=failure_count_threshold, expected_type=type_hints["failure_count_threshold"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument initial_delay", value=initial_delay, expected_type=type_hints["initial_delay"])
            check_type(argname="argument interval_seconds", value=interval_seconds, expected_type=type_hints["interval_seconds"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument success_count_threshold", value=success_count_threshold, expected_type=type_hints["success_count_threshold"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "transport": transport,
        }
        if failure_count_threshold is not None:
            self._values["failure_count_threshold"] = failure_count_threshold
        if header is not None:
            self._values["header"] = header
        if host is not None:
            self._values["host"] = host
        if initial_delay is not None:
            self._values["initial_delay"] = initial_delay
        if interval_seconds is not None:
            self._values["interval_seconds"] = interval_seconds
        if path is not None:
            self._values["path"] = path
        if success_count_threshold is not None:
            self._values["success_count_threshold"] = success_count_threshold
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port number on which to connect. Possible values are between ``1`` and ``65535``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#port ContainerApp#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def transport(self) -> builtins.str:
        '''Type of probe. Possible values are ``TCP``, ``HTTP``, and ``HTTPS``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#transport ContainerApp#transport}
        '''
        result = self._values.get("transport")
        assert result is not None, "Required property 'transport' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def failure_count_threshold(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive failures required to consider this probe as failed.

        Possible values are between ``1`` and ``30``. Defaults to ``3``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#failure_count_threshold ContainerApp#failure_count_threshold}
        '''
        result = self._values.get("failure_count_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerReadinessProbeHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#header ContainerApp#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerReadinessProbeHeader"]]], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The probe hostname.

        Defaults to the pod IP address. Setting a value for ``Host`` in ``headers`` can be used to override this for ``http`` and ``https`` type probes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#host ContainerApp#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_delay(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds elapsed after the container has started before the probe is initiated.

        Possible values are between ``0`` and ``60``. Defaults to ``0`` seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#initial_delay ContainerApp#initial_delay}
        '''
        result = self._values.get("initial_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often, in seconds, the probe should run. Possible values are between ``1`` and ``240``. Defaults to ``10``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#interval_seconds ContainerApp#interval_seconds}
        '''
        result = self._values.get("interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The URI to use for http type probes. Not valid for ``TCP`` type probes. Defaults to ``/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#path ContainerApp#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success_count_threshold(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive successful responses required to consider this probe as successful.

        Possible values are between ``1`` and ``10``. Defaults to ``3``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#success_count_threshold ContainerApp#success_count_threshold}
        '''
        result = self._values.get("success_count_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Time in seconds after which the probe times out. Possible values are between ``1`` an ``240``. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#timeout ContainerApp#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateContainerReadinessProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerReadinessProbeHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ContainerAppTemplateContainerReadinessProbeHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: The HTTP Header Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        :param value: The HTTP Header value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#value ContainerApp#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eddebcb2fb7531c136273f699395161eb61acd9565b8ed05ba96b148dc2282c8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The HTTP Header Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The HTTP Header value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#value ContainerApp#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateContainerReadinessProbeHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppTemplateContainerReadinessProbeHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerReadinessProbeHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6e0c94c5fa27e85a1180a2908134fd1321f47634e0bd9e5822074372cb2afee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateContainerReadinessProbeHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ea6f9fbfa5eddf9ed30d1e44e3e599b9fe89f8c2928b64e6fa9fa902fe1358)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateContainerReadinessProbeHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edcd577c5f35444debad4e5fa316c5ef17d2888b8379af6d9e95e0830d3d07df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0678954439e9445ab209e183339dcfdbca915b3f366c40ee850ae99dfd611b9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12b0f0706e4d15c40bd625eede92f8f2045f41a631977a9b43ee37c6f94bcca7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerReadinessProbeHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerReadinessProbeHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerReadinessProbeHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb6f739562b6c9d366d6b3920949e74987dffa0ae4c66b76a6e253c2d303756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateContainerReadinessProbeHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerReadinessProbeHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f90ec9c7e8f74e0c4052d56eec19dc5a63018ff29834a7e70a4c497ab04596e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__a7112020243bc5ed55412faa4d945e733fc3aae02cbf081ddc081e3fc73e01ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5db90e65e53da36086d8c9a45882f01574c8d6cb429f0678a4dde27dee95a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerReadinessProbeHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerReadinessProbeHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerReadinessProbeHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2dbf100837e6a67070edffb188d893634efe24377a79d6928fd828446220627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateContainerReadinessProbeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerReadinessProbeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21e99a4fbbb0a4b8763edc6acaafa97be76a476a99cbac2be1d1dbfbdd8141b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateContainerReadinessProbeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa186c9bcf05ab0a8f36a14bddda2087a332d11f3d0385acb23dab47b6f3704)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateContainerReadinessProbeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e2a336972d72e1e63374b17937f3a5da714c93582b81a453efd3b7ce7a735f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f98fb05c209f090489bf9e547045ab44cb50df50bb9de2f7e101ae006b88fdc7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da29999e8eb2cbe9ecf07b837d2e99c758b10ead8eb9d180b92219b439a8434c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerReadinessProbe]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerReadinessProbe]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerReadinessProbe]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c72e8bcc8e29e101e298aa4e710c047bee9cf5e532bac1cb2aaa35a142ea04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateContainerReadinessProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerReadinessProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2fe0b25b4faea19c556d3ad8615fcc2b15829e3d5cf85bfb29b4f81920b11fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerReadinessProbeHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__022842971e3c524ce0da70f53237cab0cf4dadb390499ff768e6648ccf820730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="resetFailureCountThreshold")
    def reset_failure_count_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureCountThreshold", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetInitialDelay")
    def reset_initial_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelay", []))

    @jsii.member(jsii_name="resetIntervalSeconds")
    def reset_interval_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalSeconds", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetSuccessCountThreshold")
    def reset_success_count_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessCountThreshold", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> ContainerAppTemplateContainerReadinessProbeHeaderList:
        return typing.cast(ContainerAppTemplateContainerReadinessProbeHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="failureCountThresholdInput")
    def failure_count_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureCountThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerReadinessProbeHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerReadinessProbeHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelayInput")
    def initial_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalSecondsInput")
    def interval_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="successCountThresholdInput")
    def success_count_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "successCountThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="transportInput")
    def transport_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transportInput"))

    @builtins.property
    @jsii.member(jsii_name="failureCountThreshold")
    def failure_count_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureCountThreshold"))

    @failure_count_threshold.setter
    def failure_count_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbbb0412307dee5e3dc9c9f3b77413ac7e8d65e7469c47c1f9bee2b0586eb177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureCountThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f4098223b41505c434742c66e1841dfa062fd481b375ca67ffec834131c634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelay")
    def initial_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelay"))

    @initial_delay.setter
    def initial_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8200f9208d09e92154a6a6280b5028a6a1731464d011cd8d5c48547a201313a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSeconds")
    def interval_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSeconds"))

    @interval_seconds.setter
    def interval_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__979478bbd603a02644c83e29b5f75180224877cb81b0841aca4aeab0a589737b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e7a7a57e5bae426a46e4a84b962da2b9c082d8298dc481f1bef640dc4e6270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4540b261040198ed9fe5e9f7a4da7d739affcf6cfec91eab3d1a8599f29787a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successCountThreshold")
    def success_count_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successCountThreshold"))

    @success_count_threshold.setter
    def success_count_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__064d5a0905253dc24d2f284c2c8a0d564ae0fafa0fd8d132ee80a12561121c1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successCountThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d502bac5ad91ab1d3f9e937149260d669141dce7e9fbe392baaf66bc9e17cc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transport")
    def transport(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transport"))

    @transport.setter
    def transport(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f561b1bbd24d16c5a9a34410f380504c54457aac6bf7ff104e6b2e0cfbb51c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerReadinessProbe]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerReadinessProbe]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerReadinessProbe]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8465e6a5baaafe269e6faf6aa84eb1b73d7291935881144c7697b48dd5d7c356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerStartupProbe",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "transport": "transport",
        "failure_count_threshold": "failureCountThreshold",
        "header": "header",
        "host": "host",
        "initial_delay": "initialDelay",
        "interval_seconds": "intervalSeconds",
        "path": "path",
        "timeout": "timeout",
    },
)
class ContainerAppTemplateContainerStartupProbe:
    def __init__(
        self,
        *,
        port: jsii.Number,
        transport: builtins.str,
        failure_count_threshold: typing.Optional[jsii.Number] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateContainerStartupProbeHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        host: typing.Optional[builtins.str] = None,
        initial_delay: typing.Optional[jsii.Number] = None,
        interval_seconds: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param port: The port number on which to connect. Possible values are between ``1`` and ``65535``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#port ContainerApp#port}
        :param transport: Type of probe. Possible values are ``TCP``, ``HTTP``, and ``HTTPS``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#transport ContainerApp#transport}
        :param failure_count_threshold: The number of consecutive failures required to consider this probe as failed. Possible values are between ``1`` and ``30``. Defaults to ``3``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#failure_count_threshold ContainerApp#failure_count_threshold}
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#header ContainerApp#header}
        :param host: The probe hostname. Defaults to the pod IP address. Setting a value for ``Host`` in ``headers`` can be used to override this for ``http`` and ``https`` type probes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#host ContainerApp#host}
        :param initial_delay: The number of seconds elapsed after the container has started before the probe is initiated. Possible values are between ``0`` and ``60``. Defaults to ``0`` seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#initial_delay ContainerApp#initial_delay}
        :param interval_seconds: How often, in seconds, the probe should run. Possible values are between ``1`` and ``240``. Defaults to ``10``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#interval_seconds ContainerApp#interval_seconds}
        :param path: The URI to use with the ``host`` for http type probes. Not valid for ``TCP`` type probes. Defaults to ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#path ContainerApp#path}
        :param timeout: Time in seconds after which the probe times out. Possible values are between ``1`` an ``240``. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#timeout ContainerApp#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d32c7a2ccff436d63148d722301729a5853aa4af06266ae74564396b594dffc2)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument transport", value=transport, expected_type=type_hints["transport"])
            check_type(argname="argument failure_count_threshold", value=failure_count_threshold, expected_type=type_hints["failure_count_threshold"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument initial_delay", value=initial_delay, expected_type=type_hints["initial_delay"])
            check_type(argname="argument interval_seconds", value=interval_seconds, expected_type=type_hints["interval_seconds"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "transport": transport,
        }
        if failure_count_threshold is not None:
            self._values["failure_count_threshold"] = failure_count_threshold
        if header is not None:
            self._values["header"] = header
        if host is not None:
            self._values["host"] = host
        if initial_delay is not None:
            self._values["initial_delay"] = initial_delay
        if interval_seconds is not None:
            self._values["interval_seconds"] = interval_seconds
        if path is not None:
            self._values["path"] = path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port number on which to connect. Possible values are between ``1`` and ``65535``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#port ContainerApp#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def transport(self) -> builtins.str:
        '''Type of probe. Possible values are ``TCP``, ``HTTP``, and ``HTTPS``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#transport ContainerApp#transport}
        '''
        result = self._values.get("transport")
        assert result is not None, "Required property 'transport' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def failure_count_threshold(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive failures required to consider this probe as failed.

        Possible values are between ``1`` and ``30``. Defaults to ``3``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#failure_count_threshold ContainerApp#failure_count_threshold}
        '''
        result = self._values.get("failure_count_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerStartupProbeHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#header ContainerApp#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateContainerStartupProbeHeader"]]], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The probe hostname.

        Defaults to the pod IP address. Setting a value for ``Host`` in ``headers`` can be used to override this for ``http`` and ``https`` type probes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#host ContainerApp#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_delay(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds elapsed after the container has started before the probe is initiated.

        Possible values are between ``0`` and ``60``. Defaults to ``0`` seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#initial_delay ContainerApp#initial_delay}
        '''
        result = self._values.get("initial_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often, in seconds, the probe should run. Possible values are between ``1`` and ``240``. Defaults to ``10``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#interval_seconds ContainerApp#interval_seconds}
        '''
        result = self._values.get("interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The URI to use with the ``host`` for http type probes.

        Not valid for ``TCP`` type probes. Defaults to ``/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#path ContainerApp#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Time in seconds after which the probe times out. Possible values are between ``1`` an ``240``. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#timeout ContainerApp#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateContainerStartupProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerStartupProbeHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ContainerAppTemplateContainerStartupProbeHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: The HTTP Header Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        :param value: The HTTP Header value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#value ContainerApp#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ab8d2cedf28729787c5ea3f5aaf743fc384704f331d9d1a2d3e65bdfb57dbe)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The HTTP Header Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The HTTP Header value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#value ContainerApp#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateContainerStartupProbeHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppTemplateContainerStartupProbeHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerStartupProbeHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed88d69229ff42ba04e58c50e7e48611187ac0cabbb4139ec9b5c4e3156ee9a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateContainerStartupProbeHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db85aa9153d37a5ae472b2fc0fd6cf03baac2d292ff8dc6a19bf98aa68c14a75)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateContainerStartupProbeHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ae45f725ae748a80f21caeb1449cca3eb86ae02a38760db598e99fbd59db0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb2c7976f52885f53c0abd8f60b7ed68ecac940a73ac264cd6b960cc968c1fce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4afe7db78fea486f6b0baeec32a7d397e8c28caf6f9e39bf67599b597a83ced8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerStartupProbeHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerStartupProbeHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerStartupProbeHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aab465f2c5be3e772dffbc1277d2c195594ca80e5300f1970e169c504661dbe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateContainerStartupProbeHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerStartupProbeHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bada8072f8c6de7504d5b9fa7d6b1c7bbb496961f3afd91049d75818ff8917bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__e444a6adcd35b8b8a4084bbcb1ec95bbf8163e2caccb4d73e97dba7a5e895e32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2051b11b02ad1e64edebd765f82a48701088dce765a1bac814890010e282fda5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerStartupProbeHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerStartupProbeHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerStartupProbeHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deed81264caa288adcf77812cc389f577fa74f0aeee9aa3c0b8c6ad95b4e48c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateContainerStartupProbeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerStartupProbeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32182a807b0f0aab847c4046c138a2d3052812cbbdf46db7d78527185f19a7b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateContainerStartupProbeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81e82f1f70f60e723b4a5fab75b49aa913bc1ea96becbcba3929d0b3b87e9b4a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateContainerStartupProbeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ffe5cebb582020094ae2925a8cde8def81cee500b169384339b66232087de47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__795c00cb553bb33463c3eb24ff26d2ad1d3111a22ea14d364e7c07e111644561)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac6c20fd5edd6613651b01547778b7eb68ea97c320af5d8a1188a83ed29ab666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerStartupProbe]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerStartupProbe]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerStartupProbe]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad972887ebbe486cc550be438ab8f83c5ce2bc0d614e21add801a58af1599e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateContainerStartupProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerStartupProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da1f7337dceba703e3dd1cf3d709a60105c734484332cda3252a56c19ed8a589)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerStartupProbeHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__756e53074972bb8129f9f5e2e768c08ab12714ea46f5e8347e15ffdf75a1aa06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="resetFailureCountThreshold")
    def reset_failure_count_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureCountThreshold", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetInitialDelay")
    def reset_initial_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelay", []))

    @jsii.member(jsii_name="resetIntervalSeconds")
    def reset_interval_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalSeconds", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> ContainerAppTemplateContainerStartupProbeHeaderList:
        return typing.cast(ContainerAppTemplateContainerStartupProbeHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="terminationGracePeriodSeconds")
    def termination_grace_period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "terminationGracePeriodSeconds"))

    @builtins.property
    @jsii.member(jsii_name="failureCountThresholdInput")
    def failure_count_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureCountThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerStartupProbeHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerStartupProbeHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelayInput")
    def initial_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalSecondsInput")
    def interval_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="transportInput")
    def transport_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transportInput"))

    @builtins.property
    @jsii.member(jsii_name="failureCountThreshold")
    def failure_count_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureCountThreshold"))

    @failure_count_threshold.setter
    def failure_count_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836e804c9e396ac15df48072749a8e0371a5ce7fc53efe0c4c183be73b401536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureCountThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71ab6553be5f9f140749ef2b248065382cc6100dbe1859c0d59b4c51591fd437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelay")
    def initial_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelay"))

    @initial_delay.setter
    def initial_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc37c49d8978ee5c077f84be7a8f441eb8653194d215d8a94398491dba71549)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSeconds")
    def interval_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSeconds"))

    @interval_seconds.setter
    def interval_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7262d6c2ae34bfb11d4b6c043280cd720c0b6f68ba398ad57e7cc7d44f854fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f481edbca84c91a7b5fa3ef252a23b50a5120fc069be26c238f75928c1b74e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d26affe49fab45e170e1898cf9e781818e30fdb748020339f0f1c2d1bc7815d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9607b93c900a10c969bc0da4b9c58b1507a475653b4341062e1ee6acb32132)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transport")
    def transport(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transport"))

    @transport.setter
    def transport(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19efb1814ea617aa0990523ce75212dd94925eb93751456c40001d0ac7274eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerStartupProbe]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerStartupProbe]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerStartupProbe]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__596962882f3c0b9ed84c08344802af9e40b902d34414ad6a6febe23496e5273e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerVolumeMounts",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "sub_path": "subPath"},
)
class ContainerAppTemplateContainerVolumeMounts:
    def __init__(
        self,
        *,
        name: builtins.str,
        path: builtins.str,
        sub_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the Volume to be mounted in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        :param path: The path in the container at which to mount this volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#path ContainerApp#path}
        :param sub_path: The sub path of the volume to be mounted in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#sub_path ContainerApp#sub_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe77f75f81f6afebcd37deb5d74acffd261f1a670c8c794ad5c034023abc1b77)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument sub_path", value=sub_path, expected_type=type_hints["sub_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "path": path,
        }
        if sub_path is not None:
            self._values["sub_path"] = sub_path

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Volume to be mounted in the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The path in the container at which to mount this volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#path ContainerApp#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sub_path(self) -> typing.Optional[builtins.str]:
        '''The sub path of the volume to be mounted in the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#sub_path ContainerApp#sub_path}
        '''
        result = self._values.get("sub_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateContainerVolumeMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppTemplateContainerVolumeMountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerVolumeMountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f03dbbaa5c9d32e56a1f866779e8775a7e6c53d7437adc7bd1c11a991ea6de68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateContainerVolumeMountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eefcbb241d52038d59c4e9083cce922fdeb370085e18a8814acfbb6d0fef29a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateContainerVolumeMountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439b0d5dfdee81d99211416fd132794121003bf82d61f3bed130b85397eeb083)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e0ed8e500de5c551cc8ec7f80cd03d76dc7222ce62f01c4f8e990372cbca254)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f1138d933400cdb94ad931fc055d3a98e29c0c5e9b73389b2433c18e9d2b375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerVolumeMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerVolumeMounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerVolumeMounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300b7dfe2d33f140f955fd44562a2efaad5729e378759d8f0bb644f1e190e007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateContainerVolumeMountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateContainerVolumeMountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da9269a069381b4d107848f047cea8c66c388aedf842a15ce8d5e3ce95571587)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSubPath")
    def reset_sub_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubPath", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="subPathInput")
    def sub_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subPathInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026a82442e74c471882b4fbd65c6273532271838a587ab14a9479a8b5f851235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc5fe3076911466eb504737d165dd4e679a506adcb48758a3d39409308812429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subPath")
    def sub_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subPath"))

    @sub_path.setter
    def sub_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a273e512d88062815524a8c4f356031c5b3b767131625f4a1a3d07da88905d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerVolumeMounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerVolumeMounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerVolumeMounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a56d62b5d5c8d40beb2f70144aa1a90b671a27e958ae5e5ea902b1e4c948574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateCustomScaleRule",
    jsii_struct_bases=[],
    name_mapping={
        "custom_rule_type": "customRuleType",
        "metadata": "metadata",
        "name": "name",
        "authentication": "authentication",
    },
)
class ContainerAppTemplateCustomScaleRule:
    def __init__(
        self,
        *,
        custom_rule_type: builtins.str,
        metadata: typing.Mapping[builtins.str, builtins.str],
        name: builtins.str,
        authentication: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateCustomScaleRuleAuthentication", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param custom_rule_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#custom_rule_type ContainerApp#custom_rule_type}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#metadata ContainerApp#metadata}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}.
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#authentication ContainerApp#authentication}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f74b1bec1525f6ce64d0eaa3be619a3dc065090f22a050b99d1c4156e7684c47)
            check_type(argname="argument custom_rule_type", value=custom_rule_type, expected_type=type_hints["custom_rule_type"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument authentication", value=authentication, expected_type=type_hints["authentication"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_rule_type": custom_rule_type,
            "metadata": metadata,
            "name": name,
        }
        if authentication is not None:
            self._values["authentication"] = authentication

    @builtins.property
    def custom_rule_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#custom_rule_type ContainerApp#custom_rule_type}.'''
        result = self._values.get("custom_rule_type")
        assert result is not None, "Required property 'custom_rule_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#metadata ContainerApp#metadata}.'''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateCustomScaleRuleAuthentication"]]]:
        '''authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#authentication ContainerApp#authentication}
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateCustomScaleRuleAuthentication"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateCustomScaleRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateCustomScaleRuleAuthentication",
    jsii_struct_bases=[],
    name_mapping={
        "secret_name": "secretName",
        "trigger_parameter": "triggerParameter",
    },
)
class ContainerAppTemplateCustomScaleRuleAuthentication:
    def __init__(
        self,
        *,
        secret_name: builtins.str,
        trigger_parameter: builtins.str,
    ) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#secret_name ContainerApp#secret_name}.
        :param trigger_parameter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#trigger_parameter ContainerApp#trigger_parameter}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05271565ed6fdf3692ba53ec3018b4f2b32475085324b75122dd8bbaef4790f1)
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument trigger_parameter", value=trigger_parameter, expected_type=type_hints["trigger_parameter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_name": secret_name,
            "trigger_parameter": trigger_parameter,
        }

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#secret_name ContainerApp#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_parameter(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#trigger_parameter ContainerApp#trigger_parameter}.'''
        result = self._values.get("trigger_parameter")
        assert result is not None, "Required property 'trigger_parameter' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateCustomScaleRuleAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppTemplateCustomScaleRuleAuthenticationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateCustomScaleRuleAuthenticationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9d8409867a39e6505bc484d5b809fe32fc2efc75f01eb66c5d3296f2a978ac9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateCustomScaleRuleAuthenticationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__542d14e43c65585487847f69081303738b7a79e8e8c5cdbbf477cd1d71b56c57)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateCustomScaleRuleAuthenticationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7a6b826c6b12473b99cf98c2f209237a08db651ebe71d8eb40822ce46e4e7f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b4b3dc92ab9e7c21e26ffb05c25c5350e03cb940c433a8d0d8aa7e31bc09167)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3ce44a30ca8c831a4ef7e5820e6e458cb4ae54c0f38a15168c24bb75d9e1d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateCustomScaleRuleAuthentication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateCustomScaleRuleAuthentication]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateCustomScaleRuleAuthentication]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__942762a392cfbbb0f2433a43a8c6223f78ceb311d2a7e82146d39b54ce57e220)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateCustomScaleRuleAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateCustomScaleRuleAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b189adec3821aa0763a93ef81ff5a20e1d0a3bb87c7f17bcd49239f17091b8cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerParameterInput")
    def trigger_parameter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5110301d0d98db7f3936950dbe59ace7221edceb416aec4d6d7888b496056cb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerParameter")
    def trigger_parameter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerParameter"))

    @trigger_parameter.setter
    def trigger_parameter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50925f7ab3c4d1f0c94c5a928250afe8fdefcc6b8ad8fe3deeb1a4cab6325d71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerParameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateCustomScaleRuleAuthentication]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateCustomScaleRuleAuthentication]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateCustomScaleRuleAuthentication]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a377d6a78ff440c3b05eb5b9f6e7bfb269ef0ae8d23cac2fb4dd16a73da4691a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateCustomScaleRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateCustomScaleRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__977459b6160e9555279c4dab00c2377ccacffed7a6507cbbcff21f4cf9446330)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateCustomScaleRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7542468327e44309917ffc03156bf31d5e3f8bba7637a6e971e5f7870ad6c4e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateCustomScaleRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55a5cb98e496147f585d559e662b5b74a63b21f3c636c5ba862329ff1071469)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b1d04b1bffa239b428f890960a3c6b0ce84d768624ef0aa09964f2f19b7a20f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec993d836d140a8566ce1adcb4a28023956a11cc092633e7f5558d3e1c6d1ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateCustomScaleRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateCustomScaleRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateCustomScaleRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5127b2cdeacced004cf3f09e98528aa73f92ac259a029ce33b5e8f94e148425f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateCustomScaleRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateCustomScaleRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a437b79d0328c29f0ee30da9b9cafe2c021da7e79928f9a8af3cc059bd6b2b93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAuthentication")
    def put_authentication(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateCustomScaleRuleAuthentication, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3c23318ce7e66a08047acad170c52950ee49f0ef2568a3fe32cdfbda515a089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthentication", [value]))

    @jsii.member(jsii_name="resetAuthentication")
    def reset_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthentication", []))

    @builtins.property
    @jsii.member(jsii_name="authentication")
    def authentication(self) -> ContainerAppTemplateCustomScaleRuleAuthenticationList:
        return typing.cast(ContainerAppTemplateCustomScaleRuleAuthenticationList, jsii.get(self, "authentication"))

    @builtins.property
    @jsii.member(jsii_name="authenticationInput")
    def authentication_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateCustomScaleRuleAuthentication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateCustomScaleRuleAuthentication]]], jsii.get(self, "authenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="customRuleTypeInput")
    def custom_rule_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customRuleTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="customRuleType")
    def custom_rule_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customRuleType"))

    @custom_rule_type.setter
    def custom_rule_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c4db8de680a7e77f8bc295485b5e6c05a501d4132b7f8c869495fef6498647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customRuleType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69af2b6f9d103d2b7f4fc7d1affaf6467157537253af6756c4e2a2620efac020)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31ea8b2c1b1262bda5acc9e0aa1966d10dfdd0c64e7a60572b75e2a1907c465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateCustomScaleRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateCustomScaleRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateCustomScaleRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6784907b65cab71f5d5b6bb065c451f6721de9246be6575793df707580f393c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateHttpScaleRule",
    jsii_struct_bases=[],
    name_mapping={
        "concurrent_requests": "concurrentRequests",
        "name": "name",
        "authentication": "authentication",
    },
)
class ContainerAppTemplateHttpScaleRule:
    def __init__(
        self,
        *,
        concurrent_requests: builtins.str,
        name: builtins.str,
        authentication: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateHttpScaleRuleAuthentication", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param concurrent_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#concurrent_requests ContainerApp#concurrent_requests}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}.
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#authentication ContainerApp#authentication}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86000771b2054d5e27fa165c385830b2a979718e757d7797f6ed85dda53e729b)
            check_type(argname="argument concurrent_requests", value=concurrent_requests, expected_type=type_hints["concurrent_requests"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument authentication", value=authentication, expected_type=type_hints["authentication"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "concurrent_requests": concurrent_requests,
            "name": name,
        }
        if authentication is not None:
            self._values["authentication"] = authentication

    @builtins.property
    def concurrent_requests(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#concurrent_requests ContainerApp#concurrent_requests}.'''
        result = self._values.get("concurrent_requests")
        assert result is not None, "Required property 'concurrent_requests' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateHttpScaleRuleAuthentication"]]]:
        '''authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#authentication ContainerApp#authentication}
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateHttpScaleRuleAuthentication"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateHttpScaleRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateHttpScaleRuleAuthentication",
    jsii_struct_bases=[],
    name_mapping={
        "secret_name": "secretName",
        "trigger_parameter": "triggerParameter",
    },
)
class ContainerAppTemplateHttpScaleRuleAuthentication:
    def __init__(
        self,
        *,
        secret_name: builtins.str,
        trigger_parameter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#secret_name ContainerApp#secret_name}.
        :param trigger_parameter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#trigger_parameter ContainerApp#trigger_parameter}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb7e461e0cf31480f4141b42f931134a35fe8ca8dc9e3f15032477b90f3ee0a)
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument trigger_parameter", value=trigger_parameter, expected_type=type_hints["trigger_parameter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_name": secret_name,
        }
        if trigger_parameter is not None:
            self._values["trigger_parameter"] = trigger_parameter

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#secret_name ContainerApp#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_parameter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#trigger_parameter ContainerApp#trigger_parameter}.'''
        result = self._values.get("trigger_parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateHttpScaleRuleAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppTemplateHttpScaleRuleAuthenticationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateHttpScaleRuleAuthenticationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a5180b2efabc98fb2bbc8bb75913d658c777146114171ad2cf6168dcb500093)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateHttpScaleRuleAuthenticationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d00dce4fe1c91a19a39c537295aa652cdb95687938548b4b264b16aa0fd7c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateHttpScaleRuleAuthenticationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e3877b1bc253921b2a2d7fac607edfadc71968c8ea75e8a1485e988b3411b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0a3a287215a721e15362e3909f1703672591a520bce4f6e907c30a8d32e63c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c837e7193c97fbe44dee9c001b1032e171601a2a9b6b3caf5960537ccf4fdbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateHttpScaleRuleAuthentication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateHttpScaleRuleAuthentication]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateHttpScaleRuleAuthentication]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88da6243ec6bf8153f0ed209a6e1d7e143bf0288cf8ebf463d258db4301ebdf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateHttpScaleRuleAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateHttpScaleRuleAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a66655e9e92ffc14a72ef988ca39b347fb7cb058f8393c98b88bcd9806561b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTriggerParameter")
    def reset_trigger_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerParameter", []))

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerParameterInput")
    def trigger_parameter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35eaa1f4b4fad4b3cd2e6e85d15e1fea3a6f98a6c789d8d7643f54b07f1c323e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerParameter")
    def trigger_parameter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerParameter"))

    @trigger_parameter.setter
    def trigger_parameter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__312ff576ed99be085ce4273adc56b8a8c0225c2365f1f51326b3c07a47eec82b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerParameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateHttpScaleRuleAuthentication]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateHttpScaleRuleAuthentication]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateHttpScaleRuleAuthentication]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f25596df0f61c747902f39262a09082811d05d9c38fdb95bc72333fc5f979e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateHttpScaleRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateHttpScaleRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f408c4b38c4677d6d64ff14d44fa3bafe5687b8278257fae70039a40ea96f9bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateHttpScaleRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5682224b2db393ba92f37eeffe63c4f4b0b42caab709d4215386d7707584ee2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateHttpScaleRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__969ea6f5e405e7fafcbf50a49534565e8f600c65635eca9d295409362d154671)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6106c5419dd9b936587a974654436c71f8ab43189e6d723ec9d02e71797ea56b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c629a2807d5db5328ea1403a0f4e94e88fa2649cc073d8568202d242d748394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateHttpScaleRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateHttpScaleRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateHttpScaleRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f08cb486695803686ee63c5159fd189ee411d29b40675a1b61c0bc380843d06a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateHttpScaleRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateHttpScaleRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fa754d9bd011b472b5364d914ca8dd1ce6c1d724b893260dd79bdc00b0a6552)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAuthentication")
    def put_authentication(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateHttpScaleRuleAuthentication, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61058ae9e44b33c7933ed503ae42f6bdf019f576ca604e628feeb516a4c7bd64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthentication", [value]))

    @jsii.member(jsii_name="resetAuthentication")
    def reset_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthentication", []))

    @builtins.property
    @jsii.member(jsii_name="authentication")
    def authentication(self) -> ContainerAppTemplateHttpScaleRuleAuthenticationList:
        return typing.cast(ContainerAppTemplateHttpScaleRuleAuthenticationList, jsii.get(self, "authentication"))

    @builtins.property
    @jsii.member(jsii_name="authenticationInput")
    def authentication_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateHttpScaleRuleAuthentication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateHttpScaleRuleAuthentication]]], jsii.get(self, "authenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="concurrentRequestsInput")
    def concurrent_requests_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "concurrentRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="concurrentRequests")
    def concurrent_requests(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "concurrentRequests"))

    @concurrent_requests.setter
    def concurrent_requests(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9660eaa30c4ac3e77990726d4db1312f11e9000fff99819901fe45808156696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "concurrentRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bfb015dac959e257db9dfbab61c1ac6a89b855e26dee59b8b5de0ac8f9793ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateHttpScaleRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateHttpScaleRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateHttpScaleRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__313ba0725c8b2b6a9e6242221f773d7aeaff3c724c8de9872c9517a7d6772cdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateInitContainer",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "name": "name",
        "args": "args",
        "command": "command",
        "cpu": "cpu",
        "env": "env",
        "memory": "memory",
        "volume_mounts": "volumeMounts",
    },
)
class ContainerAppTemplateInitContainer:
    def __init__(
        self,
        *,
        image: builtins.str,
        name: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        cpu: typing.Optional[jsii.Number] = None,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateInitContainerEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        memory: typing.Optional[builtins.str] = None,
        volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateInitContainerVolumeMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param image: The image to use to create the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#image ContainerApp#image}
        :param name: The name of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        :param args: A list of args to pass to the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#args ContainerApp#args}
        :param command: A command to pass to the container to override the default. This is provided as a list of command line elements without spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#command ContainerApp#command}
        :param cpu: The amount of vCPU to allocate to the container. Possible values include ``0.25``, ``0.5``, ``0.75``, ``1.0``, ``1.25``, ``1.5``, ``1.75``, and ``2.0``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.0`` / ``2.0`` or ``0.5`` / ``1.0``. When there's a workload profile specified, there's no such constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#cpu ContainerApp#cpu}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#env ContainerApp#env}
        :param memory: The amount of memory to allocate to the container. Possible values include ``0.5Gi``, ``1.0Gi``, ``1.5Gi``, ``2.0Gi``, ``2.5Gi``, ``3.0Gi``, ``3.5Gi``, and ``4.0Gi``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.25`` / ``2.5Gi`` or ``0.75`` / ``1.5Gi``. When there's a workload profile specified, there's no such constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#memory ContainerApp#memory}
        :param volume_mounts: volume_mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#volume_mounts ContainerApp#volume_mounts}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee1d83ef264a277dfb07f3ea1126eb98b9dc770123821cca97dc2b1c63b47948)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument volume_mounts", value=volume_mounts, expected_type=type_hints["volume_mounts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
            "name": name,
        }
        if args is not None:
            self._values["args"] = args
        if command is not None:
            self._values["command"] = command
        if cpu is not None:
            self._values["cpu"] = cpu
        if env is not None:
            self._values["env"] = env
        if memory is not None:
            self._values["memory"] = memory
        if volume_mounts is not None:
            self._values["volume_mounts"] = volume_mounts

    @builtins.property
    def image(self) -> builtins.str:
        '''The image to use to create the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#image ContainerApp#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of args to pass to the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#args ContainerApp#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A command to pass to the container to override the default.

        This is provided as a list of command line elements without spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#command ContainerApp#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The amount of vCPU to allocate to the container.

        Possible values include ``0.25``, ``0.5``, ``0.75``, ``1.0``, ``1.25``, ``1.5``, ``1.75``, and ``2.0``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.0`` / ``2.0`` or ``0.5`` / ``1.0``. When there's a workload profile specified, there's no such constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#cpu ContainerApp#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def env(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateInitContainerEnv"]]]:
        '''env block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#env ContainerApp#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateInitContainerEnv"]]], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''The amount of memory to allocate to the container.

        Possible values include ``0.5Gi``, ``1.0Gi``, ``1.5Gi``, ``2.0Gi``, ``2.5Gi``, ``3.0Gi``, ``3.5Gi``, and ``4.0Gi``. **NOTE:** ``cpu`` and ``memory`` must be specified in ``0.25'/'0.5Gi`` combination increments. e.g. ``1.25`` / ``2.5Gi`` or ``0.75`` / ``1.5Gi``. When there's a workload profile specified, there's no such constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#memory ContainerApp#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_mounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateInitContainerVolumeMounts"]]]:
        '''volume_mounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#volume_mounts ContainerApp#volume_mounts}
        '''
        result = self._values.get("volume_mounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateInitContainerVolumeMounts"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateInitContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateInitContainerEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "secret_name": "secretName", "value": "value"},
)
class ContainerAppTemplateInitContainerEnv:
    def __init__(
        self,
        *,
        name: builtins.str,
        secret_name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the environment variable for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        :param secret_name: The name of the secret that contains the value for this environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#secret_name ContainerApp#secret_name}
        :param value: The value for this environment variable. **NOTE:** This value is ignored if ``secret_name`` is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#value ContainerApp#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afb1376e8c9b09ea36fc9cae618dc9915f50fead06e78604b53d80e49f1ad6d0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if secret_name is not None:
            self._values["secret_name"] = secret_name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the environment variable for the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_name(self) -> typing.Optional[builtins.str]:
        '''The name of the secret that contains the value for this environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#secret_name ContainerApp#secret_name}
        '''
        result = self._values.get("secret_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The value for this environment variable. **NOTE:** This value is ignored if ``secret_name`` is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#value ContainerApp#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateInitContainerEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppTemplateInitContainerEnvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateInitContainerEnvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__271c639a4aded83ec94c2044e191868c312b6ec7e676b6370fede6acf2ed4463)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateInitContainerEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c247b1299b361b3c37e2dc7a0d4c1ca087d3de5daebfa64028e5ce41ab6ac6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateInitContainerEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d6cb60885260c86e66ff86f0d08a42aadf234ff1dfdacfe8310b430a07c1ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3f9c372648b745c8df05f92e15f20b706c48eb8bc0d28440fd61a951a549ebb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5be941aee8d6007e1388328a11cae90d2b0286e26533406ec972b684e394fe1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainerEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainerEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainerEnv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83aea3535e1cb48e0cd62ec41c09306833d0b6919edb5a7ac854c89d990224c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateInitContainerEnvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateInitContainerEnvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38b46d9d326b38a42c64a57e99811c49cc0ca1a9da6c047c613ddd71ed33f8f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSecretName")
    def reset_secret_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c42961ad22b7e229b81e352823708fb2fa535162246dd0fd6ee53e38ed1e555c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445bcc776e889044f8e090364ced642f881acb4c4689954c28f78386f22c193c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f4f776a5ffe24f18d743471b8cf492c25c79c5217dbf49ba9dbb15943a277b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateInitContainerEnv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateInitContainerEnv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateInitContainerEnv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27064651eb29d2215ec4382d5c121556a79d91c03c8c207a9c904628bed7ed84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateInitContainerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateInitContainerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0f7c5743c5430f269127ab54d0c7e9a6d88d3b7f64a97b8a0996caecc86d647)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateInitContainerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31fbd697343a66b0d0c0780ebd334f1365b892d13e25509b0d9dcb5260c0664b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateInitContainerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467bd1746870aa323fae728b88581a392d6f141e4c7169d96dc79f98ceac694a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c56494a4f203804a0bef8c26a116323aa64f2d60d0e26f6d7bab25693552c255)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dcd4fd9b6bb388a8c8321dcc2248fde7d6ed117e022a596d786775b77320145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainer]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainer]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac37cdca648edee0a54b2e3bdd5d4e6e2844d56e5b8b001046347f089dc3d69e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateInitContainerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateInitContainerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2377c70daba9310495227b7e42dd77254791abce2963bf6432e93c6aeaa4fe83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateInitContainerEnv, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14377158555574a185f5a7f0757968d8ee5291bbe4836c7a91ca41d5ad0cd216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnv", [value]))

    @jsii.member(jsii_name="putVolumeMounts")
    def put_volume_mounts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateInitContainerVolumeMounts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825b95756cb08234adb16ce697c89ded12e473594e344370451fb45aa60d6b2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumeMounts", [value]))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @jsii.member(jsii_name="resetVolumeMounts")
    def reset_volume_mounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeMounts", []))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> ContainerAppTemplateInitContainerEnvList:
        return typing.cast(ContainerAppTemplateInitContainerEnvList, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorage")
    def ephemeral_storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ephemeralStorage"))

    @builtins.property
    @jsii.member(jsii_name="volumeMounts")
    def volume_mounts(self) -> "ContainerAppTemplateInitContainerVolumeMountsList":
        return typing.cast("ContainerAppTemplateInitContainerVolumeMountsList", jsii.get(self, "volumeMounts"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainerEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainerEnv]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeMountsInput")
    def volume_mounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateInitContainerVolumeMounts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateInitContainerVolumeMounts"]]], jsii.get(self, "volumeMountsInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0db08c0d79ef0f75d6acaf07fde1e94b517375649d4f51822034472c983808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c4157ec97a55321c4be5d598730d6c31cdee99b4c2a602be2b20c12e7f93d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06cbe08a588c2ba68f9bb94a30b6239c4f8ebd116120aaddde31dba13b7defae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffac344c3898837a104173fc278c1e6331ff322fa89594c29f27fbc1de77b301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__892374876dd403e3538c653900efb9a390af12b2ecc5504d3f1f2fbe7ad113d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__629bdac067dffc9ba20c4c1607e923d6c4069f5e0ba89126cbce71b9aa5326e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateInitContainer]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateInitContainer]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateInitContainer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a71963ca34910bb0f66fba810b3009b6ee97fb4ea50d1fde3ae62c9772233ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateInitContainerVolumeMounts",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "sub_path": "subPath"},
)
class ContainerAppTemplateInitContainerVolumeMounts:
    def __init__(
        self,
        *,
        name: builtins.str,
        path: builtins.str,
        sub_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the Volume to be mounted in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        :param path: The path in the container at which to mount this volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#path ContainerApp#path}
        :param sub_path: The sub path of the volume to be mounted in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#sub_path ContainerApp#sub_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d9168517f4a51e6dde12191c3949d0c6a2982cd2569bf652f595d36d44bb09)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument sub_path", value=sub_path, expected_type=type_hints["sub_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "path": path,
        }
        if sub_path is not None:
            self._values["sub_path"] = sub_path

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Volume to be mounted in the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The path in the container at which to mount this volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#path ContainerApp#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sub_path(self) -> typing.Optional[builtins.str]:
        '''The sub path of the volume to be mounted in the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#sub_path ContainerApp#sub_path}
        '''
        result = self._values.get("sub_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateInitContainerVolumeMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppTemplateInitContainerVolumeMountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateInitContainerVolumeMountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15c46d533f0e8dc3dd99d7bd82e51faf57d623011c16c2c92fa337b0c7628a3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateInitContainerVolumeMountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__372fedfb4684f1836b5a6d2668199196e2285a97d79869cee82677a53872f1c4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateInitContainerVolumeMountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c757c5948eb7a05d2c60a8fdb95dd378f4df7696785df9890c4a730ff98066d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c65e944264d4a7ba3e277b5543714a5cdde09fe49604939e241ca550e963e914)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dacadbdf44b20f0c6d7f8c66a65467d3ec9f86312b14e9a12be6dcb94f9d460)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainerVolumeMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainerVolumeMounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainerVolumeMounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed0efe3498c42ecbb3ed6d5ff28d50275944dc7b105d17041dc7beb3c448af0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateInitContainerVolumeMountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateInitContainerVolumeMountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca2c1d8378aaf856095684d09939890d291bbdf341472a76e273a45658cc1827)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSubPath")
    def reset_sub_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubPath", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="subPathInput")
    def sub_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subPathInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08f066458f575a0bfadb343287d3dc6b1c66c70b6f3dbaf2711e1d9da0306761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd5b99d5fb49327ab33defa6f3a6b4e4b448b1691df6b0bfaa5f3e344335ac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subPath")
    def sub_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subPath"))

    @sub_path.setter
    def sub_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16acb4baf6219945836321d908feea4612f49bfb675abc8df9c35b0f70011b57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateInitContainerVolumeMounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateInitContainerVolumeMounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateInitContainerVolumeMounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb75b1095d85dcba09d0ce256ef0b40689e13f829ce93eb66ef26a0c04a11e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6e8111bd742f323912c5a34c98abac84f027600bbada5b4d2e7ec31cdb68c81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAzureQueueScaleRule")
    def put_azure_queue_scale_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateAzureQueueScaleRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b93ad122a97a456393e757d76ef0b1dcfbaa24ac01d253c6fbaf1779250888f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAzureQueueScaleRule", [value]))

    @jsii.member(jsii_name="putContainer")
    def put_container(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainer, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ca8816dcb5c06c1c5df9976772eb737b0a5014727938e78cbfaa28fb5ee6fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainer", [value]))

    @jsii.member(jsii_name="putCustomScaleRule")
    def put_custom_scale_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateCustomScaleRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63135c6ea18bcf43aa59abe94c20aee2e969961b2ae76748edbe00e25539032e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomScaleRule", [value]))

    @jsii.member(jsii_name="putHttpScaleRule")
    def put_http_scale_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateHttpScaleRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00cddd8213cde5bc00f74c02a56e2dc589fc662116aa5b06cf045a6de2bef5e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpScaleRule", [value]))

    @jsii.member(jsii_name="putInitContainer")
    def put_init_container(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateInitContainer, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2fcde4f68aca5d520d8ca3a5ba20063015456c30ba8b560cf5acbb38ee61562)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInitContainer", [value]))

    @jsii.member(jsii_name="putTcpScaleRule")
    def put_tcp_scale_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateTcpScaleRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da7b8ac44c6c2c0527ed496865adc6a4effd718ecf387e18d261cf46aed29145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTcpScaleRule", [value]))

    @jsii.member(jsii_name="putVolume")
    def put_volume(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateVolume", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f743cf33c23ac98f3dba3e5d13051ff20a81b65658a2820bd8a30794fc007a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolume", [value]))

    @jsii.member(jsii_name="resetAzureQueueScaleRule")
    def reset_azure_queue_scale_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureQueueScaleRule", []))

    @jsii.member(jsii_name="resetCustomScaleRule")
    def reset_custom_scale_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomScaleRule", []))

    @jsii.member(jsii_name="resetHttpScaleRule")
    def reset_http_scale_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpScaleRule", []))

    @jsii.member(jsii_name="resetInitContainer")
    def reset_init_container(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitContainer", []))

    @jsii.member(jsii_name="resetMaxReplicas")
    def reset_max_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxReplicas", []))

    @jsii.member(jsii_name="resetMinReplicas")
    def reset_min_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinReplicas", []))

    @jsii.member(jsii_name="resetRevisionSuffix")
    def reset_revision_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevisionSuffix", []))

    @jsii.member(jsii_name="resetTcpScaleRule")
    def reset_tcp_scale_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpScaleRule", []))

    @jsii.member(jsii_name="resetTerminationGracePeriodSeconds")
    def reset_termination_grace_period_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminationGracePeriodSeconds", []))

    @jsii.member(jsii_name="resetVolume")
    def reset_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolume", []))

    @builtins.property
    @jsii.member(jsii_name="azureQueueScaleRule")
    def azure_queue_scale_rule(self) -> ContainerAppTemplateAzureQueueScaleRuleList:
        return typing.cast(ContainerAppTemplateAzureQueueScaleRuleList, jsii.get(self, "azureQueueScaleRule"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> ContainerAppTemplateContainerList:
        return typing.cast(ContainerAppTemplateContainerList, jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="customScaleRule")
    def custom_scale_rule(self) -> ContainerAppTemplateCustomScaleRuleList:
        return typing.cast(ContainerAppTemplateCustomScaleRuleList, jsii.get(self, "customScaleRule"))

    @builtins.property
    @jsii.member(jsii_name="httpScaleRule")
    def http_scale_rule(self) -> ContainerAppTemplateHttpScaleRuleList:
        return typing.cast(ContainerAppTemplateHttpScaleRuleList, jsii.get(self, "httpScaleRule"))

    @builtins.property
    @jsii.member(jsii_name="initContainer")
    def init_container(self) -> ContainerAppTemplateInitContainerList:
        return typing.cast(ContainerAppTemplateInitContainerList, jsii.get(self, "initContainer"))

    @builtins.property
    @jsii.member(jsii_name="tcpScaleRule")
    def tcp_scale_rule(self) -> "ContainerAppTemplateTcpScaleRuleList":
        return typing.cast("ContainerAppTemplateTcpScaleRuleList", jsii.get(self, "tcpScaleRule"))

    @builtins.property
    @jsii.member(jsii_name="volume")
    def volume(self) -> "ContainerAppTemplateVolumeList":
        return typing.cast("ContainerAppTemplateVolumeList", jsii.get(self, "volume"))

    @builtins.property
    @jsii.member(jsii_name="azureQueueScaleRuleInput")
    def azure_queue_scale_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateAzureQueueScaleRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateAzureQueueScaleRule]]], jsii.get(self, "azureQueueScaleRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainer]]], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="customScaleRuleInput")
    def custom_scale_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateCustomScaleRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateCustomScaleRule]]], jsii.get(self, "customScaleRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="httpScaleRuleInput")
    def http_scale_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateHttpScaleRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateHttpScaleRule]]], jsii.get(self, "httpScaleRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="initContainerInput")
    def init_container_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainer]]], jsii.get(self, "initContainerInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicasInput")
    def max_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="minReplicasInput")
    def min_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="revisionSuffixInput")
    def revision_suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "revisionSuffixInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpScaleRuleInput")
    def tcp_scale_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateTcpScaleRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateTcpScaleRule"]]], jsii.get(self, "tcpScaleRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="terminationGracePeriodSecondsInput")
    def termination_grace_period_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "terminationGracePeriodSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeInput")
    def volume_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateVolume"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateVolume"]]], jsii.get(self, "volumeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicas")
    def max_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxReplicas"))

    @max_replicas.setter
    def max_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__700a80a2b5c9c50239f537ed6921fb58b3b6e7280d63308e3184287d1c52d862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicas")
    def min_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicas"))

    @min_replicas.setter
    def min_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947b9a359104d9e1d5551515907b21bc86bc862357b8cca9871ffbb2954f99b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revisionSuffix")
    def revision_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revisionSuffix"))

    @revision_suffix.setter
    def revision_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f025bccf3f4749d0e5c8fcea15477b147214b259af2431a1b1f0af8f86cfed8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revisionSuffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminationGracePeriodSeconds")
    def termination_grace_period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "terminationGracePeriodSeconds"))

    @termination_grace_period_seconds.setter
    def termination_grace_period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3bf060ca01fe3746f5b5ceb972954caa5f81b6e445c857f4697d97c6b6fa248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminationGracePeriodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAppTemplate]:
        return typing.cast(typing.Optional[ContainerAppTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ContainerAppTemplate]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2537f2247b9c90d4b98787dccf2661b27bc2a80da567c7b27de938f8d24eea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateTcpScaleRule",
    jsii_struct_bases=[],
    name_mapping={
        "concurrent_requests": "concurrentRequests",
        "name": "name",
        "authentication": "authentication",
    },
)
class ContainerAppTemplateTcpScaleRule:
    def __init__(
        self,
        *,
        concurrent_requests: builtins.str,
        name: builtins.str,
        authentication: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppTemplateTcpScaleRuleAuthentication", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param concurrent_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#concurrent_requests ContainerApp#concurrent_requests}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}.
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#authentication ContainerApp#authentication}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16e40e9000698092183ac843ee28d6a80fd4e326b1ca8f1348358d4d3f6506e)
            check_type(argname="argument concurrent_requests", value=concurrent_requests, expected_type=type_hints["concurrent_requests"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument authentication", value=authentication, expected_type=type_hints["authentication"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "concurrent_requests": concurrent_requests,
            "name": name,
        }
        if authentication is not None:
            self._values["authentication"] = authentication

    @builtins.property
    def concurrent_requests(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#concurrent_requests ContainerApp#concurrent_requests}.'''
        result = self._values.get("concurrent_requests")
        assert result is not None, "Required property 'concurrent_requests' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateTcpScaleRuleAuthentication"]]]:
        '''authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#authentication ContainerApp#authentication}
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppTemplateTcpScaleRuleAuthentication"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateTcpScaleRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateTcpScaleRuleAuthentication",
    jsii_struct_bases=[],
    name_mapping={
        "secret_name": "secretName",
        "trigger_parameter": "triggerParameter",
    },
)
class ContainerAppTemplateTcpScaleRuleAuthentication:
    def __init__(
        self,
        *,
        secret_name: builtins.str,
        trigger_parameter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#secret_name ContainerApp#secret_name}.
        :param trigger_parameter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#trigger_parameter ContainerApp#trigger_parameter}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64cf0becd61cac33ebf163dae876d92b533452f6b16c416a14f0f76073c911fa)
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument trigger_parameter", value=trigger_parameter, expected_type=type_hints["trigger_parameter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_name": secret_name,
        }
        if trigger_parameter is not None:
            self._values["trigger_parameter"] = trigger_parameter

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#secret_name ContainerApp#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_parameter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#trigger_parameter ContainerApp#trigger_parameter}.'''
        result = self._values.get("trigger_parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateTcpScaleRuleAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppTemplateTcpScaleRuleAuthenticationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateTcpScaleRuleAuthenticationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e868fcc58517a39e499a01ea4422dbb1f331a978c7cf85e6d1db0a9fd4941ad4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateTcpScaleRuleAuthenticationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76db3606342b5a5613bdccef3162261acc377f8c6524c12267019ec2a14c8325)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateTcpScaleRuleAuthenticationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714f6b41e5f2548aa5faab5a4a474447dfb6fc26bb7e92c4f631a15db8ddf48e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eee50e36f9b1c1728395848042d26d651da10e79034dc40c1748adedb20914f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c7a482d7ca5a5ed169bb2fc2e64ad5b94dbd610299f934040d5adbb055a7604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateTcpScaleRuleAuthentication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateTcpScaleRuleAuthentication]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateTcpScaleRuleAuthentication]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0e7478b43502e8d9ee8e296e34944c86a08abc5ea9fb66c207279961a59965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateTcpScaleRuleAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateTcpScaleRuleAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d59c69da7185c75bb291d2c4eae3cb350e5609279fb91693cf692cb702575d94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTriggerParameter")
    def reset_trigger_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerParameter", []))

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerParameterInput")
    def trigger_parameter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4552904acb396708290ab7a97976e1cc5b756686c6c54d4a118b95c911598583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerParameter")
    def trigger_parameter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerParameter"))

    @trigger_parameter.setter
    def trigger_parameter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2c2fd205489001571d049b09a29752e8a5b0218b39d7772d61a90d4150223ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerParameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateTcpScaleRuleAuthentication]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateTcpScaleRuleAuthentication]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateTcpScaleRuleAuthentication]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__542670505bacca75a870f078e6d38e8d5cf94f937e911e10a0c6c8d6ffc356c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateTcpScaleRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateTcpScaleRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc1401859331cded83570002466910cc1d778227e6d868ea728e69ed506b815a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppTemplateTcpScaleRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48196f8354e87ac56d169276fbe33e43f5bc9d8d07e49b12df94dd1d639ca48b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateTcpScaleRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9628fdab41e2ba99a7e8bf574641470b36eff5e3d5e8076d7d7977931d40d336)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb400af4e31d0ba91e9f949dcb090079975bb3066baa563b7d01d0a85f736852)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fbe9de2d912eb36ac5d9b859e26fbff6586fa5e94bd3a5b793f3a5dc586e3c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateTcpScaleRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateTcpScaleRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateTcpScaleRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09cd2a3a735eaad1066465acff7da79df87994746c40310e31a626fd856f879e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateTcpScaleRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateTcpScaleRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3aa57c4ae72293e0651a2db3f482f74ae71c6ad458ac5c2556b567c1579c6c3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAuthentication")
    def put_authentication(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateTcpScaleRuleAuthentication, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d6209ba98f10e11364c87834f8f18b7756bff91e311b9668576743d575767f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthentication", [value]))

    @jsii.member(jsii_name="resetAuthentication")
    def reset_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthentication", []))

    @builtins.property
    @jsii.member(jsii_name="authentication")
    def authentication(self) -> ContainerAppTemplateTcpScaleRuleAuthenticationList:
        return typing.cast(ContainerAppTemplateTcpScaleRuleAuthenticationList, jsii.get(self, "authentication"))

    @builtins.property
    @jsii.member(jsii_name="authenticationInput")
    def authentication_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateTcpScaleRuleAuthentication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateTcpScaleRuleAuthentication]]], jsii.get(self, "authenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="concurrentRequestsInput")
    def concurrent_requests_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "concurrentRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="concurrentRequests")
    def concurrent_requests(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "concurrentRequests"))

    @concurrent_requests.setter
    def concurrent_requests(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be0fa9f1bda78c6147543a8696661f5c5f1f4dd03c4854741ebb07ff8a97ad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "concurrentRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab73d061712bde3096eed77802ce2f6a4b4987a4f76af9212c4b8cd755575f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateTcpScaleRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateTcpScaleRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateTcpScaleRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4777fe3e0b28fbd17a5fc50d67e27dd8e730bec746b1bb161be42ec1ea12f1cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateVolume",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "mount_options": "mountOptions",
        "storage_name": "storageName",
        "storage_type": "storageType",
    },
)
class ContainerAppTemplateVolume:
    def __init__(
        self,
        *,
        name: builtins.str,
        mount_options: typing.Optional[builtins.str] = None,
        storage_name: typing.Optional[builtins.str] = None,
        storage_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        :param mount_options: Mount options used while mounting the AzureFile. Must be a comma-separated string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#mount_options ContainerApp#mount_options}
        :param storage_name: The name of the ``AzureFile`` storage. Required when ``storage_type`` is ``AzureFile``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#storage_name ContainerApp#storage_name}
        :param storage_type: The type of storage volume. Possible values include ``AzureFile`` and ``EmptyDir``. Defaults to ``EmptyDir``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#storage_type ContainerApp#storage_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90df6a05df3d674dc9557183015fd9e5fc1600003abda3862f61f6dac97056ae)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            check_type(argname="argument storage_name", value=storage_name, expected_type=type_hints["storage_name"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if mount_options is not None:
            self._values["mount_options"] = mount_options
        if storage_name is not None:
            self._values["storage_name"] = storage_name
        if storage_type is not None:
            self._values["storage_type"] = storage_type

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#name ContainerApp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_options(self) -> typing.Optional[builtins.str]:
        '''Mount options used while mounting the AzureFile. Must be a comma-separated string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#mount_options ContainerApp#mount_options}
        '''
        result = self._values.get("mount_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_name(self) -> typing.Optional[builtins.str]:
        '''The name of the ``AzureFile`` storage. Required when ``storage_type`` is ``AzureFile``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#storage_name ContainerApp#storage_name}
        '''
        result = self._values.get("storage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_type(self) -> typing.Optional[builtins.str]:
        '''The type of storage volume. Possible values include ``AzureFile`` and ``EmptyDir``. Defaults to ``EmptyDir``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#storage_type ContainerApp#storage_type}
        '''
        result = self._values.get("storage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTemplateVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppTemplateVolumeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateVolumeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__435dd0391afa500b517daeb77e4093dfc5cd5d3c2d683fa87a4adb5e8b788181)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerAppTemplateVolumeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d1fa80c06305f749e2a2c7565c71e559f1764fcbc7e1277f77279dac9ac13d0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppTemplateVolumeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e037407205ab2542560aaf746dd4395ade5e8c63ef5a1b89b65fc0ba61ece4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c548be8e57a2fea5fe9b5147d674e0da8779c59a33b501c4b8cce9afb465019d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47dbd62fdf1500077b4f050d14897a6ce5d8592cad709ccf01746b5ec77ae5ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateVolume]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateVolume]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateVolume]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e17db35a951699b133a489d7f5c87c24d38abc597c7ccc5a3fac89cecbfd8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppTemplateVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTemplateVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef25d2067f7f865abc7e5913036cc2d04327e6ead22d2e52c61405f2c0936fdb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMountOptions")
    def reset_mount_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountOptions", []))

    @jsii.member(jsii_name="resetStorageName")
    def reset_storage_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageName", []))

    @jsii.member(jsii_name="resetStorageType")
    def reset_storage_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageType", []))

    @builtins.property
    @jsii.member(jsii_name="mountOptionsInput")
    def mount_options_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageNameInput")
    def storage_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageTypeInput")
    def storage_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="mountOptions")
    def mount_options(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountOptions"))

    @mount_options.setter
    def mount_options(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f773e6a671d5cc50fa42328d745706bc0e58ed55cda9f83806297f8a8590bd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77eed2ca9a618f7b90f05bb295d38b7dd91a9169cc38bd96f46e51c5099ca9ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageName")
    def storage_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageName"))

    @storage_name.setter
    def storage_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78cddfbfe578df70487ea7ebe7d65b753749f4a62ba36b68a54b4ecda6139f22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageType")
    def storage_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageType"))

    @storage_type.setter
    def storage_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97b4f9304b37d6717be6299ad32726c90da9a14863712bae93cba99327dba661)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateVolume]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateVolume]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateVolume]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7a7fa523df7a9d4e79799374bc459dd8e03759488067eb0ba6684a5d4d2b788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ContainerAppTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#create ContainerApp#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#delete ContainerApp#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#read ContainerApp#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#update ContainerApp#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3262741f8c45cef90d8b8b7ddcc1fad8a935d647ee43c2f88c56b9268ded30a4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#create ContainerApp#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#delete ContainerApp#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#read ContainerApp#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app#update ContainerApp#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerApp.ContainerAppTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e2641051407b279d56ef9028b80edd18a66f5607af3c9c196354dbdbdb0c07c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3a687233fad9f8eaeefa30f0156f62cdfd91f43fdc67632807571de13ac307f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abd8b1a0d0f908ebb17d2c3decebd188313a999517a46c419d005d53f536f822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec5bdfcbd8e1ea09626d75d9375b99d26dbee30758c6231f9cfeeba6a8610b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8b38a3ab6472e662ec3e02198b8c60471b7c1308b2d220e5e0b93728880a5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb6c75eea96f04b5f46570699fcd278228e5df68b30cac8db33cf95f287c1b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ContainerApp",
    "ContainerAppConfig",
    "ContainerAppDapr",
    "ContainerAppDaprOutputReference",
    "ContainerAppIdentity",
    "ContainerAppIdentityOutputReference",
    "ContainerAppIngress",
    "ContainerAppIngressCors",
    "ContainerAppIngressCorsOutputReference",
    "ContainerAppIngressCustomDomain",
    "ContainerAppIngressCustomDomainList",
    "ContainerAppIngressCustomDomainOutputReference",
    "ContainerAppIngressIpSecurityRestriction",
    "ContainerAppIngressIpSecurityRestrictionList",
    "ContainerAppIngressIpSecurityRestrictionOutputReference",
    "ContainerAppIngressOutputReference",
    "ContainerAppIngressTrafficWeight",
    "ContainerAppIngressTrafficWeightList",
    "ContainerAppIngressTrafficWeightOutputReference",
    "ContainerAppRegistry",
    "ContainerAppRegistryList",
    "ContainerAppRegistryOutputReference",
    "ContainerAppSecret",
    "ContainerAppSecretList",
    "ContainerAppSecretOutputReference",
    "ContainerAppTemplate",
    "ContainerAppTemplateAzureQueueScaleRule",
    "ContainerAppTemplateAzureQueueScaleRuleAuthentication",
    "ContainerAppTemplateAzureQueueScaleRuleAuthenticationList",
    "ContainerAppTemplateAzureQueueScaleRuleAuthenticationOutputReference",
    "ContainerAppTemplateAzureQueueScaleRuleList",
    "ContainerAppTemplateAzureQueueScaleRuleOutputReference",
    "ContainerAppTemplateContainer",
    "ContainerAppTemplateContainerEnv",
    "ContainerAppTemplateContainerEnvList",
    "ContainerAppTemplateContainerEnvOutputReference",
    "ContainerAppTemplateContainerList",
    "ContainerAppTemplateContainerLivenessProbe",
    "ContainerAppTemplateContainerLivenessProbeHeader",
    "ContainerAppTemplateContainerLivenessProbeHeaderList",
    "ContainerAppTemplateContainerLivenessProbeHeaderOutputReference",
    "ContainerAppTemplateContainerLivenessProbeList",
    "ContainerAppTemplateContainerLivenessProbeOutputReference",
    "ContainerAppTemplateContainerOutputReference",
    "ContainerAppTemplateContainerReadinessProbe",
    "ContainerAppTemplateContainerReadinessProbeHeader",
    "ContainerAppTemplateContainerReadinessProbeHeaderList",
    "ContainerAppTemplateContainerReadinessProbeHeaderOutputReference",
    "ContainerAppTemplateContainerReadinessProbeList",
    "ContainerAppTemplateContainerReadinessProbeOutputReference",
    "ContainerAppTemplateContainerStartupProbe",
    "ContainerAppTemplateContainerStartupProbeHeader",
    "ContainerAppTemplateContainerStartupProbeHeaderList",
    "ContainerAppTemplateContainerStartupProbeHeaderOutputReference",
    "ContainerAppTemplateContainerStartupProbeList",
    "ContainerAppTemplateContainerStartupProbeOutputReference",
    "ContainerAppTemplateContainerVolumeMounts",
    "ContainerAppTemplateContainerVolumeMountsList",
    "ContainerAppTemplateContainerVolumeMountsOutputReference",
    "ContainerAppTemplateCustomScaleRule",
    "ContainerAppTemplateCustomScaleRuleAuthentication",
    "ContainerAppTemplateCustomScaleRuleAuthenticationList",
    "ContainerAppTemplateCustomScaleRuleAuthenticationOutputReference",
    "ContainerAppTemplateCustomScaleRuleList",
    "ContainerAppTemplateCustomScaleRuleOutputReference",
    "ContainerAppTemplateHttpScaleRule",
    "ContainerAppTemplateHttpScaleRuleAuthentication",
    "ContainerAppTemplateHttpScaleRuleAuthenticationList",
    "ContainerAppTemplateHttpScaleRuleAuthenticationOutputReference",
    "ContainerAppTemplateHttpScaleRuleList",
    "ContainerAppTemplateHttpScaleRuleOutputReference",
    "ContainerAppTemplateInitContainer",
    "ContainerAppTemplateInitContainerEnv",
    "ContainerAppTemplateInitContainerEnvList",
    "ContainerAppTemplateInitContainerEnvOutputReference",
    "ContainerAppTemplateInitContainerList",
    "ContainerAppTemplateInitContainerOutputReference",
    "ContainerAppTemplateInitContainerVolumeMounts",
    "ContainerAppTemplateInitContainerVolumeMountsList",
    "ContainerAppTemplateInitContainerVolumeMountsOutputReference",
    "ContainerAppTemplateOutputReference",
    "ContainerAppTemplateTcpScaleRule",
    "ContainerAppTemplateTcpScaleRuleAuthentication",
    "ContainerAppTemplateTcpScaleRuleAuthenticationList",
    "ContainerAppTemplateTcpScaleRuleAuthenticationOutputReference",
    "ContainerAppTemplateTcpScaleRuleList",
    "ContainerAppTemplateTcpScaleRuleOutputReference",
    "ContainerAppTemplateVolume",
    "ContainerAppTemplateVolumeList",
    "ContainerAppTemplateVolumeOutputReference",
    "ContainerAppTimeouts",
    "ContainerAppTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__dab6e515acad25b2aee6c2cd5a6f19f3af4da1e8d8d0e1f5b7b0afd9bd733d52(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    container_app_environment_id: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    revision_mode: builtins.str,
    template: typing.Union[ContainerAppTemplate, typing.Dict[builtins.str, typing.Any]],
    dapr: typing.Optional[typing.Union[ContainerAppDapr, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ContainerAppIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    ingress: typing.Optional[typing.Union[ContainerAppIngress, typing.Dict[builtins.str, typing.Any]]] = None,
    max_inactive_revisions: typing.Optional[jsii.Number] = None,
    registry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppRegistry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppSecret, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ContainerAppTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_profile_name: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__13015e1fcd408ee164f209e0e79d89a04279d8ee058ce736d8f1828ac9d98d9c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76c868c6a43d7ef249c63c011803112d33f07c873b5ebac32de3043143547d5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppRegistry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__366314372c1d2fca5a222833acf6f59c8353fc8c66b0e01d588463ebdf75d584(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppSecret, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ecf9c4acb19649ee7830a966f9c532410c371b02e782688376a5324f76ead72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de8247276175bc52f83edd51ad3ab7db2bd115d679dafa22eeed55d63903d9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f547c012f9b9d264667faebb7804fcffa90f1681d339dfebd5010a1eb66d9a9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19705745af8b888c3d739bd9b7eeb7389b5e21c16d1f809ab2499ef58d16a7ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2adf02e4e89dfe65b73fe8e1f4715a397935a8716dd4caeaf599568d327b31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7856a6d4bc92d97d87c36fb71213c28702b60f012957d1009f599de3034ede3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25142a32a2e7f01ac4b76de05ad599d2e2ded49a998c0a9b86a0714898e98a8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006e0877e9a3afe591122cd91de4a5f9513c42b96de19c5a39321972ff27bcf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef4933c6f7b389cb1316d1608a878808a652469c82fb2ff9fc03059bb6b7639(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    container_app_environment_id: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    revision_mode: builtins.str,
    template: typing.Union[ContainerAppTemplate, typing.Dict[builtins.str, typing.Any]],
    dapr: typing.Optional[typing.Union[ContainerAppDapr, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ContainerAppIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    ingress: typing.Optional[typing.Union[ContainerAppIngress, typing.Dict[builtins.str, typing.Any]]] = None,
    max_inactive_revisions: typing.Optional[jsii.Number] = None,
    registry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppRegistry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secret: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppSecret, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ContainerAppTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_profile_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ba1fd3395176bcd35feadafa390baf247798b5b00082cde7728f8b1c017a57(
    *,
    app_id: builtins.str,
    app_port: typing.Optional[jsii.Number] = None,
    app_protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68503c60b1a85ece06eb0e212f000726c80dbb50bd098848c31325c955b30187(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f85e61f40595e3e2abbadf713d291d55fdbb82c3cedec0e295c7fc3bad8548(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf79021921548e02f28bc46ddc8af7fa682cbcaf0e81dd872661a0cd88b804f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815ddaffbfe627317ffcc1e9e507f5ad5e97a508b4000d1f7ca977bedff8b327(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1dde5021f995755fa83765b01e33ea8bfd3e5adf5441ec8ed9ac5b454627b37(
    value: typing.Optional[ContainerAppDapr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7d9b8b8f67c98f8f7fc137b1cb5d845fbfde889dcdf557745980564cee9f97(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f11a6cfdc4e7a1c4041786626cd9d7200f55540e1e53b249d893fdd8cb6c4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370a9e729757c0174b86b7a1b57bb075ea0685b78b541f7c0cf062d1da0d42ec(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bce3f953abd635b059574972b28ca915ab3af243924d6fd99be3df7554edbf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015d8afcbdc1afefa72c56098a612418a92afa16d055ceb4e2ed18866ca335d5(
    value: typing.Optional[ContainerAppIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e16fa4bf221e40e688f48b83977355c89e9b8bfaf159d1118170ee21489c209(
    *,
    target_port: jsii.Number,
    traffic_weight: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppIngressTrafficWeight, typing.Dict[builtins.str, typing.Any]]]],
    allow_insecure_connections: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_certificate_mode: typing.Optional[builtins.str] = None,
    cors: typing.Optional[typing.Union[ContainerAppIngressCors, typing.Dict[builtins.str, typing.Any]]] = None,
    exposed_port: typing.Optional[jsii.Number] = None,
    external_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_security_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppIngressIpSecurityRestriction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    transport: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__929902f62516e315f66d416f1c5eeeb6711138aca1d29b6fc4c5905bcc20c69c(
    *,
    allowed_origins: typing.Sequence[builtins.str],
    allow_credentials_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    exposed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_age_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de22ca49ca645fd1e7eff774a19b8f8128d4f73ff32dff01281728b257583a7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc993b968193f5b04f24121ded13cb3e65397110ae2df401b468b3a528acaa3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d862ea58b945b1a07bc03cfbe128b33d4275d51ce0df62f47946740bde1edb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e700ec7aa7c7e2a781ed7da85b54423cbfcaf8c41ddaf105e8a35ddc10f3cdae(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8dc761ef267116369ba39749e210ba1f510a7d8780df1ac5684a0a0559e6f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca75d93b8865d3e2409f58692a0378e38978b34faa2224801a1f56603f11dc92(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693111cb8900bab6587f6a5d1ec3d06fbb2051867df5ecdf9d5125321b5ada6c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__766269472b1d717025edd63e9c9c252529d4695b685bfa6a4ba50f34214c4a12(
    value: typing.Optional[ContainerAppIngressCors],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ae1fb6c5b09a9d0551b7eec17d739e092eb03d9e90865a5c97e4f13900c8d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6434e8b28ded9df2424d0635cb1ca8a51dd28a9da278c79e304878d1a9f2473(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7daccfd746887f648f239cd41c619d9d4f506ba71efc7c2e1e2a605230d372(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f784ff4f75bd60aaf9e857d7a680f76b88f16e8d964e562ee4de48bcab56c62e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7715c239aee3d74639db328903558946cf29d1d37aa68cb84bef6216d2d909bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24a79c79db45167303cec3cf04dfbdef12ea603bfd1fb3fd1e792eaa116967b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40fbe6d43f2f4426bb668ebb0123547e883398fc4293d8a810bc53f8f6ce7adb(
    value: typing.Optional[ContainerAppIngressCustomDomain],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3163d33d2e2dc053402b46f8acf2e702ffe0f5dbb7405f3b97332e09e3f783e(
    *,
    action: builtins.str,
    ip_address_range: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8d5f6de8e13dbc87e26de408d0b9019ff793fe52c650583679318f2724a404(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7e91d5ac8655cde214120bd056a233443ab8352a8f19cb3c1f7c050898c6b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9088681254dece9ea8632550c0dea7add0e2e5e0670e69a31e94f3e587ab775c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5ab8dc3b0c48c554708a8ea724071f19981f2588a7397c420322b5bbae0f8b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7be71861b6be9c7e7189a6369862a0f3036b09c671765ccbe1d911631eb1222(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f56d15d3ae8c55fc467c71712c2fb703a73dffe6a2a04bda61e87c81ba01ae5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppIngressIpSecurityRestriction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278048a27d27875e5f1b6dc5fda075772029dfe56465a74702683410d55681c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f55fced17f04b113e01f76ed2b05cc92a62e4d482b4ae205cdfc90ab2edd31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caace6b8dddd7940d85944fe0aec1dae7b4cbc2d8334584f501095b89d5a36bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538c38111e7230f4102134627ddfc96eae66cc7bf873fc9513d0a670506afeec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a846ef4bbf7ffe3e8cd10a253474002a38fa2c6c4b5282425d4e40e04ae35481(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85b234b6843e2aedf72a0b76992dee33934beb5692ece977924663d6548f131(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppIngressIpSecurityRestriction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940fbf626dacf3f4c987240b99d756b45cbd04a1927e34da8b7a9eba95f7279b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2314e4576a6ba08f020a3b0a23271aae6d708ff5747a84a8bf0a81b48ee92aa7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppIngressIpSecurityRestriction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8dbb743ae35455a2e328cda126347ece09036fbb35acba9300b79aa0ad5c1c6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppIngressTrafficWeight, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be0ae9619277c2b120b06d05b9b32b7698e84f8bad867c4f59607f92ad91f3d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa502e5181aba2fd57caa97084ffa4eb3f8216b0bdd23e06bb816faef88141a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4c98373b1078b43fe0c757dcc50f8e6206941e5e385d46d3e52886963b61bcd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a762ab14fe1bc810bcead999b55723d4c3edc5aa92d4754e9b1feffdc1e2e6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6b0727866c78a831f7d558f3485095b96df47f2a3c90eb6ce9748fb8b7722c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4466d3e8541fa9dfd13e1afe6c40b94c1d8abb6a1a6a40e543b97b7601386a42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e68dd8649e36a602bd5893f9665bb1a5032e01e57beb71b5b0b30d20dabfacc(
    value: typing.Optional[ContainerAppIngress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df343944e26e19384e8da93e6321e64f0f11e00b7882161a5e45b5f12f3d747b(
    *,
    percentage: jsii.Number,
    label: typing.Optional[builtins.str] = None,
    latest_revision: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    revision_suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449cb2a85e31c4cff051ef95a2de4a08c79e4c485e8d9555a4cee382329c3f59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e473b14a0eefc3776f742884899ee9a81f12882812c4f38681976217bf5c8005(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f1e5c45bbe4eeb99878e8fc41ebfccf9e79a0ea4f05eb59b970c031e4febf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98464ab18f5eea7592cadf344055018082fce26f2be4f3951f28739ec3318fa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835afeec02739445b51f85e768f3a660819e46708591059085fc0aeff26f282c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d491ec74e9b6bc781783347c0cf67a13ce8750bda34c3d347f64d62b00efa3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppIngressTrafficWeight]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da55329d7ae1312f81a3b79aacdf0aec466e3c7a9a18f180b8ca8b3d73062fbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675e4014aebbc2bc854fe89d3e9ff88dd0929fe59d1a66906ac379dac3452d30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fb329a124117d70d174f865bb186fc73ac5c7e3253296e2d0847f23793554b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79db33c638ad524841290aaec297baf034ef2eaef441f28bd0c39a0c3bf50200(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec5552aa96863d057088e9c93d8064355d03670d29afdb269c22fd8dc7b9904(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9880534b4f1fdfad134b9df40ff0d0e717d151c6c7bb664060aa98b17656b721(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppIngressTrafficWeight]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d4ea0344de6b1cca976766baaf1c3903c036919d800998a8927657a5e1edb7(
    *,
    server: builtins.str,
    identity: typing.Optional[builtins.str] = None,
    password_secret_name: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9488cec1c8de16982f72bf01c4704a03907d679f43727072e64a77e1606c8a8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553f12ce33a56d912808cd84c3cfa215b9f96c04795b1bd9767875adc30abbda(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2731671623fea1a8ecf2d650074635a7f919a32fa81a4f698c83346a7484f383(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63873680582b3bd3fd04a69040bde3ca063ccab30ae4188ec25c81d5ef42940(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b74848dba46b539383e4d626406032f5afed4197ddf82a7f21867d83a09e069(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a29b9c6faf02d4ab62c427b4c218833996f163b477ee764c22df80467315de15(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppRegistry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd5f354b7c16f0cc90cfef95e41213aa8ba9a912baecf1558c26e097180379a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67664b3b33b5f36dabc2a28c251e4016efceab5791ad328797e8837eb528eda4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc694de369b4cd372bfd53dbc08b39fd622c0407ccd6268ec0bb8712809305eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d782c03c58d43f2bd77ab6a09f5b89e8b860b11e04537c3c9f25c9500fbca4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2542c3a050cf0233b275bd0077f0c4726bea7ffdcaa784a89a542d0cbf574760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8483b444c1c48d0d9f850edcdf9510b18c0ce89fafc01e91d24884e7a4792d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppRegistry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72091c9c14a3dcbddab91d1501c0c8a23dcce091c37f04454dd65f2833303528(
    *,
    name: builtins.str,
    identity: typing.Optional[builtins.str] = None,
    key_vault_secret_id: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1c8ac5f2b47f71efe9bca7b945eaea78b39a557d19d5e88cde0bd8bebb4c38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c3f135f60b3541b6b353620d45814b18a2d5c4365663763973e6c1b15aa205(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db56308f44c61d63da6b18f57867ea1ef481ea27633d4bc3bbc1e3291d51037(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__766c85fa3edae8f54469f8c99786c2cedcf775a7f5f908a7382d41e029e1a0da(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25a0880582f4e88c38678ebefdd02fc614939cf397ff56c16f33edb0cc58234(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af594e669317f5ab18a4a710f84301559f54c3975b8f07bb688165053f6baaac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppSecret]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__302cba9f6bc935ab5aef90c1e9e8d96e589afcbc59004de0837cf72acaebd88d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4ab1eba01c5649d75f004958bebdd48d940608390c1927d5277c3b7c651c31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f0adfc8244a960c795ecfd04b100d86cb634965ce3ca9578832a38e84e94f72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79fe89a0cf8921b9fd18bbc38057888fd44da9775ce3e168a2f0ed8bae86d815(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__184fd7f23ef40e29461750a562411c7dec71448559c0d85e665c72225cd3cbfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ffd78fffbc0b018faffabaee7cd512a287538aeae33c98f3907e153b4aaaae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppSecret]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f38ee2050a9a72a6ba8ab8ff306a388b685952d19af92c33d27d7804eeff9c(
    *,
    container: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainer, typing.Dict[builtins.str, typing.Any]]]],
    azure_queue_scale_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateAzureQueueScaleRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_scale_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateCustomScaleRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http_scale_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateHttpScaleRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    init_container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateInitContainer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_replicas: typing.Optional[jsii.Number] = None,
    min_replicas: typing.Optional[jsii.Number] = None,
    revision_suffix: typing.Optional[builtins.str] = None,
    tcp_scale_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateTcpScaleRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    termination_grace_period_seconds: typing.Optional[jsii.Number] = None,
    volume: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateVolume, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8440591433d5661498c4973812de956f7d91981266815a948114119ee9f40aa(
    *,
    authentication: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateAzureQueueScaleRuleAuthentication, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    queue_length: jsii.Number,
    queue_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a99e7d5c46ab30bb958c02381531b75e964238c7be5b8457199d414635134a7(
    *,
    secret_name: builtins.str,
    trigger_parameter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f12a5bf1ad3f4dcd9530f2d7ddb50686fcbdedb5198c5991f9eba6f36a8ba8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e1ae4cdd1abe4daccd1eb00b0a415753cf7a72c6a11e264fb923362af03a01(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea514433bb14c620d855b1ee7230fd5e73787fc16948bf44239bc7995923695(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed1c27b21303750ac601ca8c6299fbbc7bcacaf1308115c667faa1748bbde21(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8dbce8562a3a336cb9300a7ad84cc6434a79781defb76b8213f8ccaf6af92b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900cafb9938e0ed77a1296e441e23f4a9f927a2626d9919842f88245eaa453ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateAzureQueueScaleRuleAuthentication]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af23c342935bd59a956c71ddf5e2b0fdae85153ed8d15be6bee7b90db49a4065(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9cfcfb098ab059891e0912c4275b8a07be4ae67d941794eda99933b9d7a9dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd7890cb7f7f1c05330168355bd280aa782d5742de775987044b1e280b45562(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bbb9cba939470c219aeb2a865a9dab720a71d81f72a209a1bb9a8fc31e19e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateAzureQueueScaleRuleAuthentication]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8dc170c07c665b8199c4ac64c82685c887fed9cf3b2d1359107fa23897ea769(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08224cf165a51076243454c2b023c6ccb7d9755055d4d369a7e18d667f13ad88(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2fc75fd341662246e8949407a34f1061818ad768d6210e8367c58d11da9808(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2e02ee3a6224a10d4c05e4163a2eef5508f4d99c08bf801f250cdb9eac7549(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce0febdb7b3c247d437e5ba88b80683b0ca8ad65788e925bff85774ef3b5408(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6bc491e06341d646cdb20dc7dddf748d1293c10754b1432254fc6f618b2c832(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateAzureQueueScaleRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f276d69a423e2288a2fd50553041c58624e0a06c64d44723ad02db27bc645152(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84de7eff6f98f542d2d9c8a66efcea4868f85461434269ba5ca0a16c52fd790(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateAzureQueueScaleRuleAuthentication, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe568bede4f8beaf15bef8f4f203ed825b904d8927290fc63fe91043cc87fe8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af80696ed2679b40ee579a114f53b0d636081cfc5c31da65d98eb6e3230fd7bf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692f11973988b5900b840adea7fe83fb99ce4ffae26196d723d17ff161b8bb12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9905d605fca20e294fa075413360fdf6a24d15d6747ee09b41e5e03c370ab2cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateAzureQueueScaleRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65787dacf2b743288fb2aa0314db8fe68135e864c6d4a60062a9d70c0bc1c5a1(
    *,
    cpu: jsii.Number,
    image: builtins.str,
    memory: builtins.str,
    name: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
    liveness_probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerLivenessProbe, typing.Dict[builtins.str, typing.Any]]]]] = None,
    readiness_probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerReadinessProbe, typing.Dict[builtins.str, typing.Any]]]]] = None,
    startup_probe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerStartupProbe, typing.Dict[builtins.str, typing.Any]]]]] = None,
    volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerVolumeMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7187d38829264f69ea66d88bbec759812baaf96178f2082a69e0522723b922d2(
    *,
    name: builtins.str,
    secret_name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be54c385d7da8b913bfb280d8a9b4b405ad9fa5f3035a58657b69e7dc61ff01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__563440914244e2f0c63bf7ff63fadfdab5200fb2b215f67a90a1f9e43c1e9799(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32162f19f61e51f5631c028e346eb42d469a55642c153dd22bc9b52f4c4fc688(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3895c70dd3417cfe87a56bc124405d058ae88100adc1c4472e03257e79d112d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa751c8f0a82e327b272ab879288bfe556a79da9bf001cea06d3e1ae4c344e3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e67fc380d213ce594b11ffbe45903b5e2b9904d32271c59ac89a0d0f932ef5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerEnv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1fede8acff9d7511111bf16cbaea0746a70085f9acbd01abf8663a0afc7ddc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937d11c34f1c934341c6d100a37553eeeec7435eb9578678a79f9a3bd35f0f2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e047ae30d6a1aa1d2f3a8fcdb0d17c27c2652ac7219c78fe15e8ced1d9303a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265abd63082fb22d1e86871ae621cc482b7eb74d8ac3045021b408fbc824e828(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a29f1167caa55280da002e2c262d3a527712aa42019bf65c9d346183d5ce198(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerEnv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead7b1381498edb89172836f92c127379704cc036b632f5b5defe8c658a25251(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e49630d0aecae74b570bbaecea8969dff2885f8a87e01a192c75fb5b5c1193(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4386aec52b3150d577553b8db29d7e11abc9a4bdca224ae839181a5c8c10b2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4633518c521a7090b98b4c2dd13e94fad11b3042032ac0927210b697abacf556(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8290538e77fb2bfecbf4218203565e5874a80cf076eae08da074f59188a23ea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d96b09265c101edc95db37f208b1bc5659fba19e7c8d800eddf591de2518755(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainer]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecf26d64e77558622ade789eea744df6be101d85d943de1bc1a69297becbcd4(
    *,
    port: jsii.Number,
    transport: builtins.str,
    failure_count_threshold: typing.Optional[jsii.Number] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerLivenessProbeHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    host: typing.Optional[builtins.str] = None,
    initial_delay: typing.Optional[jsii.Number] = None,
    interval_seconds: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aeed8afedfedbeeb04ea544d2b1cf800f3520f001104d4e3a9f65a4ca7a45ae(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd3efbe1dc02997624ebbb3e4f4f6fbcb66f5b62904e596f18e741063e45d17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe634386368ccaf654f659cff848c338d29d05beabba91d4d29ca1d4df7e304(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7561bde5492ac79016e01486b993ba62f8bd4c55c8efbf7b7d6979baf735245(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7000330fcdc4beb1ad26649e342cf102a9b639220fc4a322627053b233f2fcee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4adeeeaa674d9871f6dac84f777d6660fb2aa86a7ec97998722e2d8ad6845e15(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d97a73d2f9761bfc43375ddd2306e424137e69923b4590443b26ce7a27ecf44a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerLivenessProbeHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc487f3eb82e51f6a9cc30ffc6ef4819e5e51d51ef5990187f5ff1fce87319f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3631fcb890561e1e1153a5769e42f94d17a4c3a2ff51b04201bf16726afc5967(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e881be5657f1d4710cd685fa3bbd72fc20e8767270d2bb54ec8828e575b9ffd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a244eb009c13066f30ba48874661846b3a375e4a90b356295621fd2d3fb3d7f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerLivenessProbeHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1e9b5cab3a381a01547e33005b27953863046bff6acec9dae4f4b13a7195dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcbeecc1dd57fffa635f026bb6dc3789ad5b0ce940472bdf2db9f1c68b14d43e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce11a1d541077d053820f7fe6778fe533a6bbc0d7cd6a9b27367da81fbdb955(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5996bed9bb7360e2085072156347520e5ff0c11f1eaeabeb12de7273f29b91e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3001a41a974000368956b6839b1b60bce7c312669952b50b94d4f13935118e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bcc71dddea0013b9d662eabf686cbeb4ba98daa5d9a69486749fd5f9a2278b6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerLivenessProbe]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d52c9c172d6e115eb504deef70de248baa8cd8f430dbb7d87fcad98a782351(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385e392d301ed370fd4831ccb18f745807d8377d8d4b93fb65d34a6ef582589a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerLivenessProbeHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc08128123cc02cb1e724f46bdf5570c7ee2f200e0ee4a527271ec2e48fd8db2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3528c5ecfbaf3b8ad30728d4d6d1798e552bc62810c8a5fd0d08d5982f383727(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a37699af179168f471f4570f95801e5bc35c86701e53ea74948360bd43f7422(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742f73cf4105504f0227a26b6d7bd62d71e9b2a3c85c39c62dd943e5e1e41b61(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56aae862f08b7517dc2aca2190b1b0ae8d48c41dd42ccc00cd70afef48fc3dab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d926d916b22c78602b5706e26d40496355e4221461ea158c81a5862765acd1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5431126c6c65f4939d48650a93e62869f5d523b9cc2f5908deaf9d8f91f69295(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcbb3678d02ce272ffbf99b26a60185f25b736765bde8e132dcaed4bacedac96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e375ffa719e569a85ed687959e5d8950f7c376c5d9a0ee345a86dccaab5d4a08(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerLivenessProbe]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919e26b1b9c4a99977fb588bc0806529162a24fe2d3e6db07da08b926b4f3c10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29dc2dd220062f02d136e3a9c5fa1cb8e07ffd432b48caf48a6d6af72ecba1ef(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerEnv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2566db62155552b7b32870fdc6395345d8b9f4ada543df26b94642bbe5b9cb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerLivenessProbe, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce302ed7dbd7e9688bf6ca5681996d6db2587acf9d629b7a2b0e7c0f6595ece(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerReadinessProbe, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2904bf0c8f4ab8f797945c267b076a1fb9583e4609dc52460de3b8bdcbd588(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerStartupProbe, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef3c4c2ca6a54e9176c0d0115a1ea348630b67102ecff16387320c1665a6867(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerVolumeMounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39873e64f7f9a9bb84bd7f360b46e0b5010d8e65b28fa8a7000ceab3d625154c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267ee49139d48400accdd2991292fadc077c0d92193bd911f01bdeb417f20864(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__209e38734d1b448ce9d6b0226b73938653d8068ec9d08a2de5a3026382d27e4a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e06b5ae38e8109f28b74f275f5135b44ccfc17afdd70c35b2f64fbcf7a0f827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49a048c0c31ef147dcce1df15136378a4246634cf4e8e3e6112292c3748b82f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6252d996813a9830113cc485590661b3b8eacc0e5f5d173bfd10be06aa02a78d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5e7d3d68d455a7d5a77244846a6fd8920776b6cf79908fea9d92dbcfe6ff68(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c6a021b0d75bb5b03c53a25543bf613502a7f472fa4374a6237585e12bd3d4(
    *,
    port: jsii.Number,
    transport: builtins.str,
    failure_count_threshold: typing.Optional[jsii.Number] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerReadinessProbeHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    host: typing.Optional[builtins.str] = None,
    initial_delay: typing.Optional[jsii.Number] = None,
    interval_seconds: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    success_count_threshold: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eddebcb2fb7531c136273f699395161eb61acd9565b8ed05ba96b148dc2282c8(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e0c94c5fa27e85a1180a2908134fd1321f47634e0bd9e5822074372cb2afee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ea6f9fbfa5eddf9ed30d1e44e3e599b9fe89f8c2928b64e6fa9fa902fe1358(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edcd577c5f35444debad4e5fa316c5ef17d2888b8379af6d9e95e0830d3d07df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0678954439e9445ab209e183339dcfdbca915b3f366c40ee850ae99dfd611b9c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b0f0706e4d15c40bd625eede92f8f2045f41a631977a9b43ee37c6f94bcca7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb6f739562b6c9d366d6b3920949e74987dffa0ae4c66b76a6e253c2d303756(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerReadinessProbeHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f90ec9c7e8f74e0c4052d56eec19dc5a63018ff29834a7e70a4c497ab04596e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7112020243bc5ed55412faa4d945e733fc3aae02cbf081ddc081e3fc73e01ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5db90e65e53da36086d8c9a45882f01574c8d6cb429f0678a4dde27dee95a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2dbf100837e6a67070edffb188d893634efe24377a79d6928fd828446220627(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerReadinessProbeHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e99a4fbbb0a4b8763edc6acaafa97be76a476a99cbac2be1d1dbfbdd8141b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa186c9bcf05ab0a8f36a14bddda2087a332d11f3d0385acb23dab47b6f3704(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2a336972d72e1e63374b17937f3a5da714c93582b81a453efd3b7ce7a735f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98fb05c209f090489bf9e547045ab44cb50df50bb9de2f7e101ae006b88fdc7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da29999e8eb2cbe9ecf07b837d2e99c758b10ead8eb9d180b92219b439a8434c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c72e8bcc8e29e101e298aa4e710c047bee9cf5e532bac1cb2aaa35a142ea04(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerReadinessProbe]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2fe0b25b4faea19c556d3ad8615fcc2b15829e3d5cf85bfb29b4f81920b11fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__022842971e3c524ce0da70f53237cab0cf4dadb390499ff768e6648ccf820730(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerReadinessProbeHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbbb0412307dee5e3dc9c9f3b77413ac7e8d65e7469c47c1f9bee2b0586eb177(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f4098223b41505c434742c66e1841dfa062fd481b375ca67ffec834131c634(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8200f9208d09e92154a6a6280b5028a6a1731464d011cd8d5c48547a201313a7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979478bbd603a02644c83e29b5f75180224877cb81b0841aca4aeab0a589737b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e7a7a57e5bae426a46e4a84b962da2b9c082d8298dc481f1bef640dc4e6270(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4540b261040198ed9fe5e9f7a4da7d739affcf6cfec91eab3d1a8599f29787a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__064d5a0905253dc24d2f284c2c8a0d564ae0fafa0fd8d132ee80a12561121c1c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d502bac5ad91ab1d3f9e937149260d669141dce7e9fbe392baaf66bc9e17cc8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f561b1bbd24d16c5a9a34410f380504c54457aac6bf7ff104e6b2e0cfbb51c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8465e6a5baaafe269e6faf6aa84eb1b73d7291935881144c7697b48dd5d7c356(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerReadinessProbe]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d32c7a2ccff436d63148d722301729a5853aa4af06266ae74564396b594dffc2(
    *,
    port: jsii.Number,
    transport: builtins.str,
    failure_count_threshold: typing.Optional[jsii.Number] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerStartupProbeHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    host: typing.Optional[builtins.str] = None,
    initial_delay: typing.Optional[jsii.Number] = None,
    interval_seconds: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ab8d2cedf28729787c5ea3f5aaf743fc384704f331d9d1a2d3e65bdfb57dbe(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed88d69229ff42ba04e58c50e7e48611187ac0cabbb4139ec9b5c4e3156ee9a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db85aa9153d37a5ae472b2fc0fd6cf03baac2d292ff8dc6a19bf98aa68c14a75(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ae45f725ae748a80f21caeb1449cca3eb86ae02a38760db598e99fbd59db0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2c7976f52885f53c0abd8f60b7ed68ecac940a73ac264cd6b960cc968c1fce(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4afe7db78fea486f6b0baeec32a7d397e8c28caf6f9e39bf67599b597a83ced8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab465f2c5be3e772dffbc1277d2c195594ca80e5300f1970e169c504661dbe6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerStartupProbeHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bada8072f8c6de7504d5b9fa7d6b1c7bbb496961f3afd91049d75818ff8917bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e444a6adcd35b8b8a4084bbcb1ec95bbf8163e2caccb4d73e97dba7a5e895e32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2051b11b02ad1e64edebd765f82a48701088dce765a1bac814890010e282fda5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deed81264caa288adcf77812cc389f577fa74f0aeee9aa3c0b8c6ad95b4e48c4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerStartupProbeHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32182a807b0f0aab847c4046c138a2d3052812cbbdf46db7d78527185f19a7b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e82f1f70f60e723b4a5fab75b49aa913bc1ea96becbcba3929d0b3b87e9b4a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ffe5cebb582020094ae2925a8cde8def81cee500b169384339b66232087de47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795c00cb553bb33463c3eb24ff26d2ad1d3111a22ea14d364e7c07e111644561(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6c20fd5edd6613651b01547778b7eb68ea97c320af5d8a1188a83ed29ab666(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad972887ebbe486cc550be438ab8f83c5ce2bc0d614e21add801a58af1599e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerStartupProbe]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1f7337dceba703e3dd1cf3d709a60105c734484332cda3252a56c19ed8a589(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__756e53074972bb8129f9f5e2e768c08ab12714ea46f5e8347e15ffdf75a1aa06(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainerStartupProbeHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836e804c9e396ac15df48072749a8e0371a5ce7fc53efe0c4c183be73b401536(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ab6553be5f9f140749ef2b248065382cc6100dbe1859c0d59b4c51591fd437(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc37c49d8978ee5c077f84be7a8f441eb8653194d215d8a94398491dba71549(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7262d6c2ae34bfb11d4b6c043280cd720c0b6f68ba398ad57e7cc7d44f854fdf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f481edbca84c91a7b5fa3ef252a23b50a5120fc069be26c238f75928c1b74e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d26affe49fab45e170e1898cf9e781818e30fdb748020339f0f1c2d1bc7815d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9607b93c900a10c969bc0da4b9c58b1507a475653b4341062e1ee6acb32132(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19efb1814ea617aa0990523ce75212dd94925eb93751456c40001d0ac7274eeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__596962882f3c0b9ed84c08344802af9e40b902d34414ad6a6febe23496e5273e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerStartupProbe]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe77f75f81f6afebcd37deb5d74acffd261f1a670c8c794ad5c034023abc1b77(
    *,
    name: builtins.str,
    path: builtins.str,
    sub_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03dbbaa5c9d32e56a1f866779e8775a7e6c53d7437adc7bd1c11a991ea6de68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eefcbb241d52038d59c4e9083cce922fdeb370085e18a8814acfbb6d0fef29a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439b0d5dfdee81d99211416fd132794121003bf82d61f3bed130b85397eeb083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0ed8e500de5c551cc8ec7f80cd03d76dc7222ce62f01c4f8e990372cbca254(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1138d933400cdb94ad931fc055d3a98e29c0c5e9b73389b2433c18e9d2b375(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300b7dfe2d33f140f955fd44562a2efaad5729e378759d8f0bb644f1e190e007(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateContainerVolumeMounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9269a069381b4d107848f047cea8c66c388aedf842a15ce8d5e3ce95571587(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026a82442e74c471882b4fbd65c6273532271838a587ab14a9479a8b5f851235(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5fe3076911466eb504737d165dd4e679a506adcb48758a3d39409308812429(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a273e512d88062815524a8c4f356031c5b3b767131625f4a1a3d07da88905d23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a56d62b5d5c8d40beb2f70144aa1a90b671a27e958ae5e5ea902b1e4c948574(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateContainerVolumeMounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74b1bec1525f6ce64d0eaa3be619a3dc065090f22a050b99d1c4156e7684c47(
    *,
    custom_rule_type: builtins.str,
    metadata: typing.Mapping[builtins.str, builtins.str],
    name: builtins.str,
    authentication: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateCustomScaleRuleAuthentication, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05271565ed6fdf3692ba53ec3018b4f2b32475085324b75122dd8bbaef4790f1(
    *,
    secret_name: builtins.str,
    trigger_parameter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d8409867a39e6505bc484d5b809fe32fc2efc75f01eb66c5d3296f2a978ac9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542d14e43c65585487847f69081303738b7a79e8e8c5cdbbf477cd1d71b56c57(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a6b826c6b12473b99cf98c2f209237a08db651ebe71d8eb40822ce46e4e7f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4b3dc92ab9e7c21e26ffb05c25c5350e03cb940c433a8d0d8aa7e31bc09167(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ce44a30ca8c831a4ef7e5820e6e458cb4ae54c0f38a15168c24bb75d9e1d5e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__942762a392cfbbb0f2433a43a8c6223f78ceb311d2a7e82146d39b54ce57e220(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateCustomScaleRuleAuthentication]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b189adec3821aa0763a93ef81ff5a20e1d0a3bb87c7f17bcd49239f17091b8cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5110301d0d98db7f3936950dbe59ace7221edceb416aec4d6d7888b496056cb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50925f7ab3c4d1f0c94c5a928250afe8fdefcc6b8ad8fe3deeb1a4cab6325d71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a377d6a78ff440c3b05eb5b9f6e7bfb269ef0ae8d23cac2fb4dd16a73da4691a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateCustomScaleRuleAuthentication]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__977459b6160e9555279c4dab00c2377ccacffed7a6507cbbcff21f4cf9446330(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7542468327e44309917ffc03156bf31d5e3f8bba7637a6e971e5f7870ad6c4e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55a5cb98e496147f585d559e662b5b74a63b21f3c636c5ba862329ff1071469(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1d04b1bffa239b428f890960a3c6b0ce84d768624ef0aa09964f2f19b7a20f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec993d836d140a8566ce1adcb4a28023956a11cc092633e7f5558d3e1c6d1ac3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5127b2cdeacced004cf3f09e98528aa73f92ac259a029ce33b5e8f94e148425f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateCustomScaleRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a437b79d0328c29f0ee30da9b9cafe2c021da7e79928f9a8af3cc059bd6b2b93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c23318ce7e66a08047acad170c52950ee49f0ef2568a3fe32cdfbda515a089(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateCustomScaleRuleAuthentication, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c4db8de680a7e77f8bc295485b5e6c05a501d4132b7f8c869495fef6498647(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69af2b6f9d103d2b7f4fc7d1affaf6467157537253af6756c4e2a2620efac020(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31ea8b2c1b1262bda5acc9e0aa1966d10dfdd0c64e7a60572b75e2a1907c465(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6784907b65cab71f5d5b6bb065c451f6721de9246be6575793df707580f393c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateCustomScaleRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86000771b2054d5e27fa165c385830b2a979718e757d7797f6ed85dda53e729b(
    *,
    concurrent_requests: builtins.str,
    name: builtins.str,
    authentication: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateHttpScaleRuleAuthentication, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb7e461e0cf31480f4141b42f931134a35fe8ca8dc9e3f15032477b90f3ee0a(
    *,
    secret_name: builtins.str,
    trigger_parameter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5180b2efabc98fb2bbc8bb75913d658c777146114171ad2cf6168dcb500093(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d00dce4fe1c91a19a39c537295aa652cdb95687938548b4b264b16aa0fd7c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e3877b1bc253921b2a2d7fac607edfadc71968c8ea75e8a1485e988b3411b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a3a287215a721e15362e3909f1703672591a520bce4f6e907c30a8d32e63c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c837e7193c97fbe44dee9c001b1032e171601a2a9b6b3caf5960537ccf4fdbb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88da6243ec6bf8153f0ed209a6e1d7e143bf0288cf8ebf463d258db4301ebdf0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateHttpScaleRuleAuthentication]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a66655e9e92ffc14a72ef988ca39b347fb7cb058f8393c98b88bcd9806561b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35eaa1f4b4fad4b3cd2e6e85d15e1fea3a6f98a6c789d8d7643f54b07f1c323e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312ff576ed99be085ce4273adc56b8a8c0225c2365f1f51326b3c07a47eec82b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f25596df0f61c747902f39262a09082811d05d9c38fdb95bc72333fc5f979e2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateHttpScaleRuleAuthentication]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f408c4b38c4677d6d64ff14d44fa3bafe5687b8278257fae70039a40ea96f9bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5682224b2db393ba92f37eeffe63c4f4b0b42caab709d4215386d7707584ee2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969ea6f5e405e7fafcbf50a49534565e8f600c65635eca9d295409362d154671(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6106c5419dd9b936587a974654436c71f8ab43189e6d723ec9d02e71797ea56b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c629a2807d5db5328ea1403a0f4e94e88fa2649cc073d8568202d242d748394(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08cb486695803686ee63c5159fd189ee411d29b40675a1b61c0bc380843d06a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateHttpScaleRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa754d9bd011b472b5364d914ca8dd1ce6c1d724b893260dd79bdc00b0a6552(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61058ae9e44b33c7933ed503ae42f6bdf019f576ca604e628feeb516a4c7bd64(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateHttpScaleRuleAuthentication, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9660eaa30c4ac3e77990726d4db1312f11e9000fff99819901fe45808156696(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfb015dac959e257db9dfbab61c1ac6a89b855e26dee59b8b5de0ac8f9793ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313ba0725c8b2b6a9e6242221f773d7aeaff3c724c8de9872c9517a7d6772cdd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateHttpScaleRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee1d83ef264a277dfb07f3ea1126eb98b9dc770123821cca97dc2b1c63b47948(
    *,
    image: builtins.str,
    name: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    cpu: typing.Optional[jsii.Number] = None,
    env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateInitContainerEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
    memory: typing.Optional[builtins.str] = None,
    volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateInitContainerVolumeMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb1376e8c9b09ea36fc9cae618dc9915f50fead06e78604b53d80e49f1ad6d0(
    *,
    name: builtins.str,
    secret_name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271c639a4aded83ec94c2044e191868c312b6ec7e676b6370fede6acf2ed4463(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c247b1299b361b3c37e2dc7a0d4c1ca087d3de5daebfa64028e5ce41ab6ac6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d6cb60885260c86e66ff86f0d08a42aadf234ff1dfdacfe8310b430a07c1ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f9c372648b745c8df05f92e15f20b706c48eb8bc0d28440fd61a951a549ebb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be941aee8d6007e1388328a11cae90d2b0286e26533406ec972b684e394fe1b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83aea3535e1cb48e0cd62ec41c09306833d0b6919edb5a7ac854c89d990224c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainerEnv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b46d9d326b38a42c64a57e99811c49cc0ca1a9da6c047c613ddd71ed33f8f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42961ad22b7e229b81e352823708fb2fa535162246dd0fd6ee53e38ed1e555c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445bcc776e889044f8e090364ced642f881acb4c4689954c28f78386f22c193c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f4f776a5ffe24f18d743471b8cf492c25c79c5217dbf49ba9dbb15943a277b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27064651eb29d2215ec4382d5c121556a79d91c03c8c207a9c904628bed7ed84(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateInitContainerEnv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0f7c5743c5430f269127ab54d0c7e9a6d88d3b7f64a97b8a0996caecc86d647(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31fbd697343a66b0d0c0780ebd334f1365b892d13e25509b0d9dcb5260c0664b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467bd1746870aa323fae728b88581a392d6f141e4c7169d96dc79f98ceac694a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56494a4f203804a0bef8c26a116323aa64f2d60d0e26f6d7bab25693552c255(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dcd4fd9b6bb388a8c8321dcc2248fde7d6ed117e022a596d786775b77320145(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac37cdca648edee0a54b2e3bdd5d4e6e2844d56e5b8b001046347f089dc3d69e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainer]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2377c70daba9310495227b7e42dd77254791abce2963bf6432e93c6aeaa4fe83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14377158555574a185f5a7f0757968d8ee5291bbe4836c7a91ca41d5ad0cd216(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateInitContainerEnv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825b95756cb08234adb16ce697c89ded12e473594e344370451fb45aa60d6b2c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateInitContainerVolumeMounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0db08c0d79ef0f75d6acaf07fde1e94b517375649d4f51822034472c983808(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c4157ec97a55321c4be5d598730d6c31cdee99b4c2a602be2b20c12e7f93d4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06cbe08a588c2ba68f9bb94a30b6239c4f8ebd116120aaddde31dba13b7defae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffac344c3898837a104173fc278c1e6331ff322fa89594c29f27fbc1de77b301(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__892374876dd403e3538c653900efb9a390af12b2ecc5504d3f1f2fbe7ad113d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629bdac067dffc9ba20c4c1607e923d6c4069f5e0ba89126cbce71b9aa5326e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a71963ca34910bb0f66fba810b3009b6ee97fb4ea50d1fde3ae62c9772233ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateInitContainer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d9168517f4a51e6dde12191c3949d0c6a2982cd2569bf652f595d36d44bb09(
    *,
    name: builtins.str,
    path: builtins.str,
    sub_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c46d533f0e8dc3dd99d7bd82e51faf57d623011c16c2c92fa337b0c7628a3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__372fedfb4684f1836b5a6d2668199196e2285a97d79869cee82677a53872f1c4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c757c5948eb7a05d2c60a8fdb95dd378f4df7696785df9890c4a730ff98066d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65e944264d4a7ba3e277b5543714a5cdde09fe49604939e241ca550e963e914(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dacadbdf44b20f0c6d7f8c66a65467d3ec9f86312b14e9a12be6dcb94f9d460(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0efe3498c42ecbb3ed6d5ff28d50275944dc7b105d17041dc7beb3c448af0f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateInitContainerVolumeMounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2c1d8378aaf856095684d09939890d291bbdf341472a76e273a45658cc1827(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f066458f575a0bfadb343287d3dc6b1c66c70b6f3dbaf2711e1d9da0306761(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd5b99d5fb49327ab33defa6f3a6b4e4b448b1691df6b0bfaa5f3e344335ac4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16acb4baf6219945836321d908feea4612f49bfb675abc8df9c35b0f70011b57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb75b1095d85dcba09d0ce256ef0b40689e13f829ce93eb66ef26a0c04a11e77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateInitContainerVolumeMounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e8111bd742f323912c5a34c98abac84f027600bbada5b4d2e7ec31cdb68c81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b93ad122a97a456393e757d76ef0b1dcfbaa24ac01d253c6fbaf1779250888f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateAzureQueueScaleRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ca8816dcb5c06c1c5df9976772eb737b0a5014727938e78cbfaa28fb5ee6fe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateContainer, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63135c6ea18bcf43aa59abe94c20aee2e969961b2ae76748edbe00e25539032e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateCustomScaleRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00cddd8213cde5bc00f74c02a56e2dc589fc662116aa5b06cf045a6de2bef5e9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateHttpScaleRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2fcde4f68aca5d520d8ca3a5ba20063015456c30ba8b560cf5acbb38ee61562(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateInitContainer, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7b8ac44c6c2c0527ed496865adc6a4effd718ecf387e18d261cf46aed29145(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateTcpScaleRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f743cf33c23ac98f3dba3e5d13051ff20a81b65658a2820bd8a30794fc007a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateVolume, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__700a80a2b5c9c50239f537ed6921fb58b3b6e7280d63308e3184287d1c52d862(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947b9a359104d9e1d5551515907b21bc86bc862357b8cca9871ffbb2954f99b9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f025bccf3f4749d0e5c8fcea15477b147214b259af2431a1b1f0af8f86cfed8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3bf060ca01fe3746f5b5ceb972954caa5f81b6e445c857f4697d97c6b6fa248(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2537f2247b9c90d4b98787dccf2661b27bc2a80da567c7b27de938f8d24eea1(
    value: typing.Optional[ContainerAppTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16e40e9000698092183ac843ee28d6a80fd4e326b1ca8f1348358d4d3f6506e(
    *,
    concurrent_requests: builtins.str,
    name: builtins.str,
    authentication: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateTcpScaleRuleAuthentication, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64cf0becd61cac33ebf163dae876d92b533452f6b16c416a14f0f76073c911fa(
    *,
    secret_name: builtins.str,
    trigger_parameter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e868fcc58517a39e499a01ea4422dbb1f331a978c7cf85e6d1db0a9fd4941ad4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76db3606342b5a5613bdccef3162261acc377f8c6524c12267019ec2a14c8325(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714f6b41e5f2548aa5faab5a4a474447dfb6fc26bb7e92c4f631a15db8ddf48e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee50e36f9b1c1728395848042d26d651da10e79034dc40c1748adedb20914f8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7a482d7ca5a5ed169bb2fc2e64ad5b94dbd610299f934040d5adbb055a7604(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0e7478b43502e8d9ee8e296e34944c86a08abc5ea9fb66c207279961a59965(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateTcpScaleRuleAuthentication]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59c69da7185c75bb291d2c4eae3cb350e5609279fb91693cf692cb702575d94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4552904acb396708290ab7a97976e1cc5b756686c6c54d4a118b95c911598583(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c2fd205489001571d049b09a29752e8a5b0218b39d7772d61a90d4150223ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542670505bacca75a870f078e6d38e8d5cf94f937e911e10a0c6c8d6ffc356c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateTcpScaleRuleAuthentication]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1401859331cded83570002466910cc1d778227e6d868ea728e69ed506b815a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48196f8354e87ac56d169276fbe33e43f5bc9d8d07e49b12df94dd1d639ca48b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9628fdab41e2ba99a7e8bf574641470b36eff5e3d5e8076d7d7977931d40d336(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb400af4e31d0ba91e9f949dcb090079975bb3066baa563b7d01d0a85f736852(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbe9de2d912eb36ac5d9b859e26fbff6586fa5e94bd3a5b793f3a5dc586e3c0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09cd2a3a735eaad1066465acff7da79df87994746c40310e31a626fd856f879e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateTcpScaleRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa57c4ae72293e0651a2db3f482f74ae71c6ad458ac5c2556b567c1579c6c3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d6209ba98f10e11364c87834f8f18b7756bff91e311b9668576743d575767f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppTemplateTcpScaleRuleAuthentication, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be0fa9f1bda78c6147543a8696661f5c5f1f4dd03c4854741ebb07ff8a97ad1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab73d061712bde3096eed77802ce2f6a4b4987a4f76af9212c4b8cd755575f01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4777fe3e0b28fbd17a5fc50d67e27dd8e730bec746b1bb161be42ec1ea12f1cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateTcpScaleRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90df6a05df3d674dc9557183015fd9e5fc1600003abda3862f61f6dac97056ae(
    *,
    name: builtins.str,
    mount_options: typing.Optional[builtins.str] = None,
    storage_name: typing.Optional[builtins.str] = None,
    storage_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435dd0391afa500b517daeb77e4093dfc5cd5d3c2d683fa87a4adb5e8b788181(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1fa80c06305f749e2a2c7565c71e559f1764fcbc7e1277f77279dac9ac13d0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e037407205ab2542560aaf746dd4395ade5e8c63ef5a1b89b65fc0ba61ece4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c548be8e57a2fea5fe9b5147d674e0da8779c59a33b501c4b8cce9afb465019d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47dbd62fdf1500077b4f050d14897a6ce5d8592cad709ccf01746b5ec77ae5ba(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e17db35a951699b133a489d7f5c87c24d38abc597c7ccc5a3fac89cecbfd8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppTemplateVolume]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef25d2067f7f865abc7e5913036cc2d04327e6ead22d2e52c61405f2c0936fdb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f773e6a671d5cc50fa42328d745706bc0e58ed55cda9f83806297f8a8590bd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77eed2ca9a618f7b90f05bb295d38b7dd91a9169cc38bd96f46e51c5099ca9ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78cddfbfe578df70487ea7ebe7d65b753749f4a62ba36b68a54b4ecda6139f22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97b4f9304b37d6717be6299ad32726c90da9a14863712bae93cba99327dba661(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a7fa523df7a9d4e79799374bc459dd8e03759488067eb0ba6684a5d4d2b788(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTemplateVolume]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3262741f8c45cef90d8b8b7ddcc1fad8a935d647ee43c2f88c56b9268ded30a4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2641051407b279d56ef9028b80edd18a66f5607af3c9c196354dbdbdb0c07c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a687233fad9f8eaeefa30f0156f62cdfd91f43fdc67632807571de13ac307f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd8b1a0d0f908ebb17d2c3decebd188313a999517a46c419d005d53f536f822(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5bdfcbd8e1ea09626d75d9375b99d26dbee30758c6231f9cfeeba6a8610b7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8b38a3ab6472e662ec3e02198b8c60471b7c1308b2d220e5e0b93728880a5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6c75eea96f04b5f46570699fcd278228e5df68b30cac8db33cf95f287c1b5c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

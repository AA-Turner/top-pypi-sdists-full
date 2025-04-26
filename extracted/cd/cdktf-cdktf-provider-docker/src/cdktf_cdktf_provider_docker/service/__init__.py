r'''
# `docker_service`

Refer to the Terraform Registry for docs: [`docker_service`](https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service).
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


class Service(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.Service",
):
    '''Represents a {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service docker_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        task_spec: typing.Union["ServiceTaskSpec", typing.Dict[builtins.str, typing.Any]],
        auth: typing.Optional[typing.Union["ServiceAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        converge_config: typing.Optional[typing.Union["ServiceConvergeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_spec: typing.Optional[typing.Union["ServiceEndpointSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mode: typing.Optional[typing.Union["ServiceMode", typing.Dict[builtins.str, typing.Any]]] = None,
        rollback_config: typing.Optional[typing.Union["ServiceRollbackConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        update_config: typing.Optional[typing.Union["ServiceUpdateConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service docker_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#name Service#name}
        :param task_spec: task_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#task_spec Service#task_spec}
        :param auth: auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#auth Service#auth}
        :param converge_config: converge_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#converge_config Service#converge_config}
        :param endpoint_spec: endpoint_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#endpoint_spec Service#endpoint_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#id Service#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#labels Service#labels}
        :param mode: mode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#mode Service#mode}
        :param rollback_config: rollback_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#rollback_config Service#rollback_config}
        :param update_config: update_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#update_config Service#update_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b578b738121d0d131ca664c81d01a1c614a67dfc3771bd097f9a04c6eaa23027)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceConfig(
            name=name,
            task_spec=task_spec,
            auth=auth,
            converge_config=converge_config,
            endpoint_spec=endpoint_spec,
            id=id,
            labels=labels,
            mode=mode,
            rollback_config=rollback_config,
            update_config=update_config,
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
        '''Generates CDKTF code for importing a Service resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Service to import.
        :param import_from_id: The id of the existing Service that should be imported. Refer to the {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Service to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a1b868124027ebaea59f0924cd442c63b6e7a6a68de848b298feac5e67342db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuth")
    def put_auth(
        self,
        *,
        server_address: builtins.str,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param server_address: The address of the server for the authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#server_address Service#server_address}
        :param password: The password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#password Service#password}
        :param username: The username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#username Service#username}
        '''
        value = ServiceAuth(
            server_address=server_address, password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putAuth", [value]))

    @jsii.member(jsii_name="putConvergeConfig")
    def put_converge_config(
        self,
        *,
        delay: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delay: The interval to check if the desired state is reached ``(ms|s)``. Defaults to ``7s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#delay Service#delay}
        :param timeout: The timeout of the service to reach the desired state ``(s|m)``. Defaults to ``3m``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#timeout Service#timeout}
        '''
        value = ServiceConvergeConfig(delay=delay, timeout=timeout)

        return typing.cast(None, jsii.invoke(self, "putConvergeConfig", [value]))

    @jsii.member(jsii_name="putEndpointSpec")
    def put_endpoint_spec(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEndpointSpecPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param mode: The mode of resolution to use for internal load balancing between tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#mode Service#mode}
        :param ports: ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#ports Service#ports}
        '''
        value = ServiceEndpointSpec(mode=mode, ports=ports)

        return typing.cast(None, jsii.invoke(self, "putEndpointSpec", [value]))

    @jsii.member(jsii_name="putLabels")
    def put_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceLabels", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794a9a60cbdfb184d2f2ec181d4261d7d4ba798a60598c1ae850fe4fb92390f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLabels", [value]))

    @jsii.member(jsii_name="putMode")
    def put_mode(
        self,
        *,
        global_: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replicated: typing.Optional[typing.Union["ServiceModeReplicated", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param global_: The global service mode. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#global Service#global}
        :param replicated: replicated block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#replicated Service#replicated}
        '''
        value = ServiceMode(global_=global_, replicated=replicated)

        return typing.cast(None, jsii.invoke(self, "putMode", [value]))

    @jsii.member(jsii_name="putRollbackConfig")
    def put_rollback_config(
        self,
        *,
        delay: typing.Optional[builtins.str] = None,
        failure_action: typing.Optional[builtins.str] = None,
        max_failure_ratio: typing.Optional[builtins.str] = None,
        monitor: typing.Optional[builtins.str] = None,
        order: typing.Optional[builtins.str] = None,
        parallelism: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delay: Delay between task rollbacks (ns|us|ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#delay Service#delay}
        :param failure_action: Action on rollback failure: pause | continue. Defaults to ``pause``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#failure_action Service#failure_action}
        :param max_failure_ratio: Failure rate to tolerate during a rollback. Defaults to ``0.0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#max_failure_ratio Service#max_failure_ratio}
        :param monitor: Duration after each task rollback to monitor for failure (ns|us|ms|s|m|h). Defaults to ``5s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#monitor Service#monitor}
        :param order: Rollback order: either 'stop-first' or 'start-first'. Defaults to ``stop-first``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#order Service#order}
        :param parallelism: Maximum number of tasks to be rollbacked in one iteration. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#parallelism Service#parallelism}
        '''
        value = ServiceRollbackConfig(
            delay=delay,
            failure_action=failure_action,
            max_failure_ratio=max_failure_ratio,
            monitor=monitor,
            order=order,
            parallelism=parallelism,
        )

        return typing.cast(None, jsii.invoke(self, "putRollbackConfig", [value]))

    @jsii.member(jsii_name="putTaskSpec")
    def put_task_spec(
        self,
        *,
        container_spec: typing.Union["ServiceTaskSpecContainerSpec", typing.Dict[builtins.str, typing.Any]],
        force_update: typing.Optional[jsii.Number] = None,
        log_driver: typing.Optional[typing.Union["ServiceTaskSpecLogDriver", typing.Dict[builtins.str, typing.Any]]] = None,
        networks_advanced: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecNetworksAdvanced", typing.Dict[builtins.str, typing.Any]]]]] = None,
        placement: typing.Optional[typing.Union["ServiceTaskSpecPlacement", typing.Dict[builtins.str, typing.Any]]] = None,
        resources: typing.Optional[typing.Union["ServiceTaskSpecResources", typing.Dict[builtins.str, typing.Any]]] = None,
        restart_policy: typing.Optional[typing.Union["ServiceTaskSpecRestartPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_spec: container_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#container_spec Service#container_spec}
        :param force_update: A counter that triggers an update even if no relevant parameters have been changed. See the `spec <https://github.com/docker/swarmkit/blob/master/api/specs.proto#L126>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#force_update Service#force_update}
        :param log_driver: log_driver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#log_driver Service#log_driver}
        :param networks_advanced: networks_advanced block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#networks_advanced Service#networks_advanced}
        :param placement: placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#placement Service#placement}
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#resources Service#resources}
        :param restart_policy: restart_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#restart_policy Service#restart_policy}
        :param runtime: Runtime is the type of runtime specified for the task executor. See the `types <https://github.com/moby/moby/blob/master/api/types/swarm/runtime.go>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#runtime Service#runtime}
        '''
        value = ServiceTaskSpec(
            container_spec=container_spec,
            force_update=force_update,
            log_driver=log_driver,
            networks_advanced=networks_advanced,
            placement=placement,
            resources=resources,
            restart_policy=restart_policy,
            runtime=runtime,
        )

        return typing.cast(None, jsii.invoke(self, "putTaskSpec", [value]))

    @jsii.member(jsii_name="putUpdateConfig")
    def put_update_config(
        self,
        *,
        delay: typing.Optional[builtins.str] = None,
        failure_action: typing.Optional[builtins.str] = None,
        max_failure_ratio: typing.Optional[builtins.str] = None,
        monitor: typing.Optional[builtins.str] = None,
        order: typing.Optional[builtins.str] = None,
        parallelism: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delay: Delay between task updates ``(ns|us|ms|s|m|h)``. Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#delay Service#delay}
        :param failure_action: Action on update failure: ``pause``, ``continue`` or ``rollback``. Defaults to ``pause``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#failure_action Service#failure_action}
        :param max_failure_ratio: Failure rate to tolerate during an update. Defaults to ``0.0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#max_failure_ratio Service#max_failure_ratio}
        :param monitor: Duration after each task update to monitor for failure (ns|us|ms|s|m|h). Defaults to ``5s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#monitor Service#monitor}
        :param order: Update order: either 'stop-first' or 'start-first'. Defaults to ``stop-first``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#order Service#order}
        :param parallelism: Maximum number of tasks to be updated in one iteration. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#parallelism Service#parallelism}
        '''
        value = ServiceUpdateConfig(
            delay=delay,
            failure_action=failure_action,
            max_failure_ratio=max_failure_ratio,
            monitor=monitor,
            order=order,
            parallelism=parallelism,
        )

        return typing.cast(None, jsii.invoke(self, "putUpdateConfig", [value]))

    @jsii.member(jsii_name="resetAuth")
    def reset_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuth", []))

    @jsii.member(jsii_name="resetConvergeConfig")
    def reset_converge_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConvergeConfig", []))

    @jsii.member(jsii_name="resetEndpointSpec")
    def reset_endpoint_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointSpec", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetRollbackConfig")
    def reset_rollback_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRollbackConfig", []))

    @jsii.member(jsii_name="resetUpdateConfig")
    def reset_update_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateConfig", []))

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
    @jsii.member(jsii_name="auth")
    def auth(self) -> "ServiceAuthOutputReference":
        return typing.cast("ServiceAuthOutputReference", jsii.get(self, "auth"))

    @builtins.property
    @jsii.member(jsii_name="convergeConfig")
    def converge_config(self) -> "ServiceConvergeConfigOutputReference":
        return typing.cast("ServiceConvergeConfigOutputReference", jsii.get(self, "convergeConfig"))

    @builtins.property
    @jsii.member(jsii_name="endpointSpec")
    def endpoint_spec(self) -> "ServiceEndpointSpecOutputReference":
        return typing.cast("ServiceEndpointSpecOutputReference", jsii.get(self, "endpointSpec"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> "ServiceLabelsList":
        return typing.cast("ServiceLabelsList", jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> "ServiceModeOutputReference":
        return typing.cast("ServiceModeOutputReference", jsii.get(self, "mode"))

    @builtins.property
    @jsii.member(jsii_name="rollbackConfig")
    def rollback_config(self) -> "ServiceRollbackConfigOutputReference":
        return typing.cast("ServiceRollbackConfigOutputReference", jsii.get(self, "rollbackConfig"))

    @builtins.property
    @jsii.member(jsii_name="taskSpec")
    def task_spec(self) -> "ServiceTaskSpecOutputReference":
        return typing.cast("ServiceTaskSpecOutputReference", jsii.get(self, "taskSpec"))

    @builtins.property
    @jsii.member(jsii_name="updateConfig")
    def update_config(self) -> "ServiceUpdateConfigOutputReference":
        return typing.cast("ServiceUpdateConfigOutputReference", jsii.get(self, "updateConfig"))

    @builtins.property
    @jsii.member(jsii_name="authInput")
    def auth_input(self) -> typing.Optional["ServiceAuth"]:
        return typing.cast(typing.Optional["ServiceAuth"], jsii.get(self, "authInput"))

    @builtins.property
    @jsii.member(jsii_name="convergeConfigInput")
    def converge_config_input(self) -> typing.Optional["ServiceConvergeConfig"]:
        return typing.cast(typing.Optional["ServiceConvergeConfig"], jsii.get(self, "convergeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointSpecInput")
    def endpoint_spec_input(self) -> typing.Optional["ServiceEndpointSpec"]:
        return typing.cast(typing.Optional["ServiceEndpointSpec"], jsii.get(self, "endpointSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLabels"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLabels"]]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional["ServiceMode"]:
        return typing.cast(typing.Optional["ServiceMode"], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="rollbackConfigInput")
    def rollback_config_input(self) -> typing.Optional["ServiceRollbackConfig"]:
        return typing.cast(typing.Optional["ServiceRollbackConfig"], jsii.get(self, "rollbackConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="taskSpecInput")
    def task_spec_input(self) -> typing.Optional["ServiceTaskSpec"]:
        return typing.cast(typing.Optional["ServiceTaskSpec"], jsii.get(self, "taskSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="updateConfigInput")
    def update_config_input(self) -> typing.Optional["ServiceUpdateConfig"]:
        return typing.cast(typing.Optional["ServiceUpdateConfig"], jsii.get(self, "updateConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b17101c3f55066c22c7874cc6478b6e67b22f8a45e7a87f7cf444a57f8d261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3e6ce206a7caa168ed74d7c08af8b2f76dcb1eed7c039b85b04a0a5b31973a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceAuth",
    jsii_struct_bases=[],
    name_mapping={
        "server_address": "serverAddress",
        "password": "password",
        "username": "username",
    },
)
class ServiceAuth:
    def __init__(
        self,
        *,
        server_address: builtins.str,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param server_address: The address of the server for the authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#server_address Service#server_address}
        :param password: The password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#password Service#password}
        :param username: The username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#username Service#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__449ee43c79aec9507a4b0db7e9a54562c9d367689e82a9ef738d88114cb1a89f)
            check_type(argname="argument server_address", value=server_address, expected_type=type_hints["server_address"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "server_address": server_address,
        }
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def server_address(self) -> builtins.str:
        '''The address of the server for the authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#server_address Service#server_address}
        '''
        result = self._values.get("server_address")
        assert result is not None, "Required property 'server_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#password Service#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#username Service#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceAuthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5990411f641325b4a5eddd6194b63b4b0a36335c7abefdcfc527751d8f142973)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="serverAddressInput")
    def server_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45b05e09fc0af4c35229ba6e4e9c146bc214efacb33c58539dbe8a92fee66f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverAddress")
    def server_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverAddress"))

    @server_address.setter
    def server_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262ae1eabd20f5aed9642495042afc7e5ec8b8cf87fdbf035fa7f3383fdc3f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982938f18f80273e9d00ba765c31feb473d47a249f1f056a7728368847aceea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceAuth]:
        return typing.cast(typing.Optional[ServiceAuth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceAuth]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__284119e61dd2c7ead3992ea0d1473596af147efe258636ec5e4b98d2e2770e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceConfig",
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
        "task_spec": "taskSpec",
        "auth": "auth",
        "converge_config": "convergeConfig",
        "endpoint_spec": "endpointSpec",
        "id": "id",
        "labels": "labels",
        "mode": "mode",
        "rollback_config": "rollbackConfig",
        "update_config": "updateConfig",
    },
)
class ServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        task_spec: typing.Union["ServiceTaskSpec", typing.Dict[builtins.str, typing.Any]],
        auth: typing.Optional[typing.Union[ServiceAuth, typing.Dict[builtins.str, typing.Any]]] = None,
        converge_config: typing.Optional[typing.Union["ServiceConvergeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_spec: typing.Optional[typing.Union["ServiceEndpointSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mode: typing.Optional[typing.Union["ServiceMode", typing.Dict[builtins.str, typing.Any]]] = None,
        rollback_config: typing.Optional[typing.Union["ServiceRollbackConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        update_config: typing.Optional[typing.Union["ServiceUpdateConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#name Service#name}
        :param task_spec: task_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#task_spec Service#task_spec}
        :param auth: auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#auth Service#auth}
        :param converge_config: converge_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#converge_config Service#converge_config}
        :param endpoint_spec: endpoint_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#endpoint_spec Service#endpoint_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#id Service#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#labels Service#labels}
        :param mode: mode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#mode Service#mode}
        :param rollback_config: rollback_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#rollback_config Service#rollback_config}
        :param update_config: update_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#update_config Service#update_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(task_spec, dict):
            task_spec = ServiceTaskSpec(**task_spec)
        if isinstance(auth, dict):
            auth = ServiceAuth(**auth)
        if isinstance(converge_config, dict):
            converge_config = ServiceConvergeConfig(**converge_config)
        if isinstance(endpoint_spec, dict):
            endpoint_spec = ServiceEndpointSpec(**endpoint_spec)
        if isinstance(mode, dict):
            mode = ServiceMode(**mode)
        if isinstance(rollback_config, dict):
            rollback_config = ServiceRollbackConfig(**rollback_config)
        if isinstance(update_config, dict):
            update_config = ServiceUpdateConfig(**update_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02ac0581c52512733a058c0c43949366de729de771427abde71054d4096ba745)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument task_spec", value=task_spec, expected_type=type_hints["task_spec"])
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument converge_config", value=converge_config, expected_type=type_hints["converge_config"])
            check_type(argname="argument endpoint_spec", value=endpoint_spec, expected_type=type_hints["endpoint_spec"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument rollback_config", value=rollback_config, expected_type=type_hints["rollback_config"])
            check_type(argname="argument update_config", value=update_config, expected_type=type_hints["update_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "task_spec": task_spec,
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
        if auth is not None:
            self._values["auth"] = auth
        if converge_config is not None:
            self._values["converge_config"] = converge_config
        if endpoint_spec is not None:
            self._values["endpoint_spec"] = endpoint_spec
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if mode is not None:
            self._values["mode"] = mode
        if rollback_config is not None:
            self._values["rollback_config"] = rollback_config
        if update_config is not None:
            self._values["update_config"] = update_config

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
        '''Name of the service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#name Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def task_spec(self) -> "ServiceTaskSpec":
        '''task_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#task_spec Service#task_spec}
        '''
        result = self._values.get("task_spec")
        assert result is not None, "Required property 'task_spec' is missing"
        return typing.cast("ServiceTaskSpec", result)

    @builtins.property
    def auth(self) -> typing.Optional[ServiceAuth]:
        '''auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#auth Service#auth}
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional[ServiceAuth], result)

    @builtins.property
    def converge_config(self) -> typing.Optional["ServiceConvergeConfig"]:
        '''converge_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#converge_config Service#converge_config}
        '''
        result = self._values.get("converge_config")
        return typing.cast(typing.Optional["ServiceConvergeConfig"], result)

    @builtins.property
    def endpoint_spec(self) -> typing.Optional["ServiceEndpointSpec"]:
        '''endpoint_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#endpoint_spec Service#endpoint_spec}
        '''
        result = self._values.get("endpoint_spec")
        return typing.cast(typing.Optional["ServiceEndpointSpec"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#id Service#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLabels"]]]:
        '''labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#labels Service#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLabels"]]], result)

    @builtins.property
    def mode(self) -> typing.Optional["ServiceMode"]:
        '''mode block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#mode Service#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional["ServiceMode"], result)

    @builtins.property
    def rollback_config(self) -> typing.Optional["ServiceRollbackConfig"]:
        '''rollback_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#rollback_config Service#rollback_config}
        '''
        result = self._values.get("rollback_config")
        return typing.cast(typing.Optional["ServiceRollbackConfig"], result)

    @builtins.property
    def update_config(self) -> typing.Optional["ServiceUpdateConfig"]:
        '''update_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#update_config Service#update_config}
        '''
        result = self._values.get("update_config")
        return typing.cast(typing.Optional["ServiceUpdateConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceConvergeConfig",
    jsii_struct_bases=[],
    name_mapping={"delay": "delay", "timeout": "timeout"},
)
class ServiceConvergeConfig:
    def __init__(
        self,
        *,
        delay: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delay: The interval to check if the desired state is reached ``(ms|s)``. Defaults to ``7s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#delay Service#delay}
        :param timeout: The timeout of the service to reach the desired state ``(s|m)``. Defaults to ``3m``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#timeout Service#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e702b821534297ef5c9ae2900e2d91b52ad07bec13938fd5374ddb81be218a73)
            check_type(argname="argument delay", value=delay, expected_type=type_hints["delay"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delay is not None:
            self._values["delay"] = delay
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def delay(self) -> typing.Optional[builtins.str]:
        '''The interval to check if the desired state is reached ``(ms|s)``. Defaults to ``7s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#delay Service#delay}
        '''
        result = self._values.get("delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''The timeout of the service to reach the desired state ``(s|m)``. Defaults to ``3m``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#timeout Service#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceConvergeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceConvergeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceConvergeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fe28dd50c249e22562cbeda3830c357ca9918512920001a8d20224f091074c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDelay")
    def reset_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelay", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="delayInput")
    def delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delayInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="delay")
    def delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delay"))

    @delay.setter
    def delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a62faee6040ce3765651f8d3097d2d13d420268cb1526c3ffc3c3726ffff7a5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca838a1ab0beeb648a10f7ab1dc36ec40e1c10e5715735af2025f3df04c83622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceConvergeConfig]:
        return typing.cast(typing.Optional[ServiceConvergeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceConvergeConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1abd31438a5e50e58103e9fdcc5f0eeae14698e09bd5bc3532488ec1576bebc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceEndpointSpec",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "ports": "ports"},
)
class ServiceEndpointSpec:
    def __init__(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEndpointSpecPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param mode: The mode of resolution to use for internal load balancing between tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#mode Service#mode}
        :param ports: ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#ports Service#ports}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a535aa7cdeb3ea7073f6ceddf77fc61ab666ef066d02d9f6f9c132d1118332)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode
        if ports is not None:
            self._values["ports"] = ports

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The mode of resolution to use for internal load balancing between tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#mode Service#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEndpointSpecPorts"]]]:
        '''ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#ports Service#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEndpointSpecPorts"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEndpointSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEndpointSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceEndpointSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff883ef1e699adb53cab87b2fd20e2b8349d61bcba707fb4d3b36e92f8cc5feb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPorts")
    def put_ports(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEndpointSpecPorts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__687c21a1a6fec04388f3205ea1b655f3d7303c49b8ebe9df37da8e10a46c48aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPorts", [value]))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> "ServiceEndpointSpecPortsList":
        return typing.cast("ServiceEndpointSpecPortsList", jsii.get(self, "ports"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEndpointSpecPorts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEndpointSpecPorts"]]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bbcdce74fbaa0b99f81b1e024e42bc5fc6b6a9493a1b276321ab9492e95f567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceEndpointSpec]:
        return typing.cast(typing.Optional[ServiceEndpointSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceEndpointSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47e4a5abac15086d71c6d80c137340eefbf9beb90d17e6f2c9af15ffc3ec7f90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceEndpointSpecPorts",
    jsii_struct_bases=[],
    name_mapping={
        "target_port": "targetPort",
        "name": "name",
        "protocol": "protocol",
        "published_port": "publishedPort",
        "publish_mode": "publishMode",
    },
)
class ServiceEndpointSpecPorts:
    def __init__(
        self,
        *,
        target_port: jsii.Number,
        name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        published_port: typing.Optional[jsii.Number] = None,
        publish_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_port: The port inside the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#target_port Service#target_port}
        :param name: A random name for the port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#name Service#name}
        :param protocol: Rrepresents the protocol of a port: ``tcp``, ``udp`` or ``sctp``. Defaults to ``tcp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#protocol Service#protocol}
        :param published_port: The port on the swarm hosts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#published_port Service#published_port}
        :param publish_mode: Represents the mode in which the port is to be published: 'ingress' or 'host'. Defaults to ``ingress``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#publish_mode Service#publish_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff206b236a332926277d52336b42c140cc8d480d22e1b057924e2a3375047163)
            check_type(argname="argument target_port", value=target_port, expected_type=type_hints["target_port"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument published_port", value=published_port, expected_type=type_hints["published_port"])
            check_type(argname="argument publish_mode", value=publish_mode, expected_type=type_hints["publish_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_port": target_port,
        }
        if name is not None:
            self._values["name"] = name
        if protocol is not None:
            self._values["protocol"] = protocol
        if published_port is not None:
            self._values["published_port"] = published_port
        if publish_mode is not None:
            self._values["publish_mode"] = publish_mode

    @builtins.property
    def target_port(self) -> jsii.Number:
        '''The port inside the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#target_port Service#target_port}
        '''
        result = self._values.get("target_port")
        assert result is not None, "Required property 'target_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A random name for the port.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#name Service#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Rrepresents the protocol of a port: ``tcp``, ``udp`` or ``sctp``. Defaults to ``tcp``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#protocol Service#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def published_port(self) -> typing.Optional[jsii.Number]:
        '''The port on the swarm hosts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#published_port Service#published_port}
        '''
        result = self._values.get("published_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def publish_mode(self) -> typing.Optional[builtins.str]:
        '''Represents the mode in which the port is to be published: 'ingress' or 'host'. Defaults to ``ingress``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#publish_mode Service#publish_mode}
        '''
        result = self._values.get("publish_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEndpointSpecPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEndpointSpecPortsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceEndpointSpecPortsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1776557f8620ffa819777cfa19b96b2ad0519fa605b1366de4ed3c8dc9bf71a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceEndpointSpecPortsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300bdac5f5730d08f3888e23675c69c61380a0de7db49a27d997f98ea8119f27)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceEndpointSpecPortsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2b5b4a0ff5c2fdaff6a92ac836f458772524e677d01bdcad466edaffe415666)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c97c1befbb9f415b349a7d47ac420c0cd72696ae1669d3d8064da065097e924)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f8dc17c302396859c625f579e1e59b7ce528229da3d6b2ca61bc981d486b937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEndpointSpecPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEndpointSpecPorts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEndpointSpecPorts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8779a37aa5ffd8758167de5bdefc4701766ae8a45853528776fea49e776fd9ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEndpointSpecPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceEndpointSpecPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6554c48602194129f8b21d8bfa43db319c8740d4e46e245dda40d6d3b2f498ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetPublishedPort")
    def reset_published_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishedPort", []))

    @jsii.member(jsii_name="resetPublishMode")
    def reset_publish_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishMode", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="publishedPortInput")
    def published_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "publishedPortInput"))

    @builtins.property
    @jsii.member(jsii_name="publishModeInput")
    def publish_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publishModeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetPortInput")
    def target_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetPortInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__526ebc150c907c47bfbeaa8084fc8dd3e56f4fcb40a02e14c6479ae24a37d635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d834f0343cd96f0e48ccdb095bf708227f1a9d103bf60cf5cd3aa13abd7049e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publishedPort")
    def published_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "publishedPort"))

    @published_port.setter
    def published_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13b6a32b5d8b8140f37b4c785718d6ea7d313343a14ecc4807d8fc228052a3c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishedPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publishMode")
    def publish_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publishMode"))

    @publish_mode.setter
    def publish_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb22aa54bc954a6d565573a7dd04d2c2b7e8bdfebaea0fcdb69436ca527a57e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPort")
    def target_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetPort"))

    @target_port.setter
    def target_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c8821d86ff370669bfb936aafb76ddfda19f1dd5f5caeb36b36dcb3a9840d1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEndpointSpecPorts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEndpointSpecPorts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEndpointSpecPorts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deffba0de2a6eafd61429e22d73c096547e1f34bef9f64f96cfe8ae5b8ee8ec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class ServiceLabels:
    def __init__(self, *, label: builtins.str, value: builtins.str) -> None:
        '''
        :param label: Name of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#label Service#label}
        :param value: Value of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#value Service#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7431e3715e35d4e41c2c33fdef85584e6bd568615438cc95cc19cc27869c065b)
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> builtins.str:
        '''Name of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#label Service#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#value Service#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd6d9cd879004a8b84d3c7090bdf9ecb2b1e8acfef679fb829268de7d5f2198b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e12a8a227e7e7aeef6f92645ccc55faa14539d26248935c820202d8b7ffe2dc1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0120b53c465eb894aa4d0d745e705ccd16eb3a7986b0ddc399bd9a94c781dd6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d598ea7be3540cacd4745006311b5e8b519d62a488c6e9566453bce921be6be5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f740c3c76e936f3eb526698f1bf10aa4e63c1179659f14c10cf6beee92377d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f86bd1043a36f333bbe8d420a19ef9979be092e159eb7fd924822fe00dac66a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75740118b86f3529c78ea31f359871cabad9ff8c00b14d601abfdaae620ece3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af058d03512930b1274fd18f5c2565fab5560d47ede9a35455676f9641bc78d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf7654ede4acf02f5c0d291d41831311a6935aac8df2349ef7061bb10c3d4f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6c7fe14c15ceb38939b4b9973a46c579f5a01ee006eb08608a68d9a75f18e5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceMode",
    jsii_struct_bases=[],
    name_mapping={"global_": "global", "replicated": "replicated"},
)
class ServiceMode:
    def __init__(
        self,
        *,
        global_: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replicated: typing.Optional[typing.Union["ServiceModeReplicated", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param global_: The global service mode. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#global Service#global}
        :param replicated: replicated block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#replicated Service#replicated}
        '''
        if isinstance(replicated, dict):
            replicated = ServiceModeReplicated(**replicated)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc13d1d41ba3985ad35923f85284c699a0192a39ef17489cc6c42b10d58785d)
            check_type(argname="argument global_", value=global_, expected_type=type_hints["global_"])
            check_type(argname="argument replicated", value=replicated, expected_type=type_hints["replicated"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if global_ is not None:
            self._values["global_"] = global_
        if replicated is not None:
            self._values["replicated"] = replicated

    @builtins.property
    def global_(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The global service mode. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#global Service#global}
        '''
        result = self._values.get("global_")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def replicated(self) -> typing.Optional["ServiceModeReplicated"]:
        '''replicated block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#replicated Service#replicated}
        '''
        result = self._values.get("replicated")
        return typing.cast(typing.Optional["ServiceModeReplicated"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceMode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceModeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceModeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bbf1ef51925a579d2af227b03b37b98c95a7b1617525fda5a119b8633e75f5d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putReplicated")
    def put_replicated(self, *, replicas: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param replicas: The amount of replicas of the service. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#replicas Service#replicas}
        '''
        value = ServiceModeReplicated(replicas=replicas)

        return typing.cast(None, jsii.invoke(self, "putReplicated", [value]))

    @jsii.member(jsii_name="resetGlobal")
    def reset_global(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlobal", []))

    @jsii.member(jsii_name="resetReplicated")
    def reset_replicated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicated", []))

    @builtins.property
    @jsii.member(jsii_name="replicated")
    def replicated(self) -> "ServiceModeReplicatedOutputReference":
        return typing.cast("ServiceModeReplicatedOutputReference", jsii.get(self, "replicated"))

    @builtins.property
    @jsii.member(jsii_name="globalInput")
    def global_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "globalInput"))

    @builtins.property
    @jsii.member(jsii_name="replicatedInput")
    def replicated_input(self) -> typing.Optional["ServiceModeReplicated"]:
        return typing.cast(typing.Optional["ServiceModeReplicated"], jsii.get(self, "replicatedInput"))

    @builtins.property
    @jsii.member(jsii_name="global")
    def global_(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "global"))

    @global_.setter
    def global_(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af312b85881b08a33cd94c9843ace183c10454ff093096868fe17fbd8a4396a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "global", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceMode]:
        return typing.cast(typing.Optional[ServiceMode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceMode]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d569204fad96cad648219a43d93ce919f2759989f9023ac3626e9577664331f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceModeReplicated",
    jsii_struct_bases=[],
    name_mapping={"replicas": "replicas"},
)
class ServiceModeReplicated:
    def __init__(self, *, replicas: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param replicas: The amount of replicas of the service. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#replicas Service#replicas}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9a9bbc2b07fd7c7f5e6373ba717dedd887536dc00c3c3207499d06bf0a307d5)
            check_type(argname="argument replicas", value=replicas, expected_type=type_hints["replicas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if replicas is not None:
            self._values["replicas"] = replicas

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        '''The amount of replicas of the service. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#replicas Service#replicas}
        '''
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceModeReplicated(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceModeReplicatedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceModeReplicatedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6449048ab9a7b9790fe38436b8527cbd8dcb0b679760a9774cfe007e625a00b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetReplicas")
    def reset_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicas", []))

    @builtins.property
    @jsii.member(jsii_name="replicasInput")
    def replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicasInput"))

    @builtins.property
    @jsii.member(jsii_name="replicas")
    def replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicas"))

    @replicas.setter
    def replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91fbde77a2ed3d2b5fc333f261b266c610ae966a816b4bd9f942a4e1538b6a9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceModeReplicated]:
        return typing.cast(typing.Optional[ServiceModeReplicated], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceModeReplicated]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27a770297c94225d8c2e200343ae22e3800fd91512588c32c9fd4432c4dd231e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceRollbackConfig",
    jsii_struct_bases=[],
    name_mapping={
        "delay": "delay",
        "failure_action": "failureAction",
        "max_failure_ratio": "maxFailureRatio",
        "monitor": "monitor",
        "order": "order",
        "parallelism": "parallelism",
    },
)
class ServiceRollbackConfig:
    def __init__(
        self,
        *,
        delay: typing.Optional[builtins.str] = None,
        failure_action: typing.Optional[builtins.str] = None,
        max_failure_ratio: typing.Optional[builtins.str] = None,
        monitor: typing.Optional[builtins.str] = None,
        order: typing.Optional[builtins.str] = None,
        parallelism: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delay: Delay between task rollbacks (ns|us|ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#delay Service#delay}
        :param failure_action: Action on rollback failure: pause | continue. Defaults to ``pause``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#failure_action Service#failure_action}
        :param max_failure_ratio: Failure rate to tolerate during a rollback. Defaults to ``0.0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#max_failure_ratio Service#max_failure_ratio}
        :param monitor: Duration after each task rollback to monitor for failure (ns|us|ms|s|m|h). Defaults to ``5s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#monitor Service#monitor}
        :param order: Rollback order: either 'stop-first' or 'start-first'. Defaults to ``stop-first``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#order Service#order}
        :param parallelism: Maximum number of tasks to be rollbacked in one iteration. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#parallelism Service#parallelism}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b2842ef70e286197c22523be5070c923d8177fae135db50b5f29a06397e228)
            check_type(argname="argument delay", value=delay, expected_type=type_hints["delay"])
            check_type(argname="argument failure_action", value=failure_action, expected_type=type_hints["failure_action"])
            check_type(argname="argument max_failure_ratio", value=max_failure_ratio, expected_type=type_hints["max_failure_ratio"])
            check_type(argname="argument monitor", value=monitor, expected_type=type_hints["monitor"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument parallelism", value=parallelism, expected_type=type_hints["parallelism"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delay is not None:
            self._values["delay"] = delay
        if failure_action is not None:
            self._values["failure_action"] = failure_action
        if max_failure_ratio is not None:
            self._values["max_failure_ratio"] = max_failure_ratio
        if monitor is not None:
            self._values["monitor"] = monitor
        if order is not None:
            self._values["order"] = order
        if parallelism is not None:
            self._values["parallelism"] = parallelism

    @builtins.property
    def delay(self) -> typing.Optional[builtins.str]:
        '''Delay between task rollbacks (ns|us|ms|s|m|h). Defaults to ``0s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#delay Service#delay}
        '''
        result = self._values.get("delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_action(self) -> typing.Optional[builtins.str]:
        '''Action on rollback failure: pause | continue. Defaults to ``pause``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#failure_action Service#failure_action}
        '''
        result = self._values.get("failure_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_failure_ratio(self) -> typing.Optional[builtins.str]:
        '''Failure rate to tolerate during a rollback. Defaults to ``0.0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#max_failure_ratio Service#max_failure_ratio}
        '''
        result = self._values.get("max_failure_ratio")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor(self) -> typing.Optional[builtins.str]:
        '''Duration after each task rollback to monitor for failure (ns|us|ms|s|m|h). Defaults to ``5s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#monitor Service#monitor}
        '''
        result = self._values.get("monitor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def order(self) -> typing.Optional[builtins.str]:
        '''Rollback order: either 'stop-first' or 'start-first'. Defaults to ``stop-first``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#order Service#order}
        '''
        result = self._values.get("order")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parallelism(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of tasks to be rollbacked in one iteration. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#parallelism Service#parallelism}
        '''
        result = self._values.get("parallelism")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceRollbackConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceRollbackConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceRollbackConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d38b918a1aeaa4d6dbe7cf27d437abbc00b4f17a5b52c8aeb09a1b68fe1c4128)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDelay")
    def reset_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelay", []))

    @jsii.member(jsii_name="resetFailureAction")
    def reset_failure_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureAction", []))

    @jsii.member(jsii_name="resetMaxFailureRatio")
    def reset_max_failure_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFailureRatio", []))

    @jsii.member(jsii_name="resetMonitor")
    def reset_monitor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitor", []))

    @jsii.member(jsii_name="resetOrder")
    def reset_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrder", []))

    @jsii.member(jsii_name="resetParallelism")
    def reset_parallelism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelism", []))

    @builtins.property
    @jsii.member(jsii_name="delayInput")
    def delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delayInput"))

    @builtins.property
    @jsii.member(jsii_name="failureActionInput")
    def failure_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "failureActionInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFailureRatioInput")
    def max_failure_ratio_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxFailureRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorInput")
    def monitor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitorInput"))

    @builtins.property
    @jsii.member(jsii_name="orderInput")
    def order_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orderInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelismInput")
    def parallelism_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelismInput"))

    @builtins.property
    @jsii.member(jsii_name="delay")
    def delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delay"))

    @delay.setter
    def delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecee4d66675559b59f3a858c7aad85c380202f672c0e0199a2977b6564b6f910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failureAction")
    def failure_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failureAction"))

    @failure_action.setter
    def failure_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b3892ac7d1cbacea3c844a6ebabd977ce8b25c327917ae17ceb3f02faf3525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFailureRatio")
    def max_failure_ratio(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxFailureRatio"))

    @max_failure_ratio.setter
    def max_failure_ratio(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__952c12ff387b42be1b71c83d511a4c02c51b35894481fe06e4151a63b155ffdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFailureRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitor")
    def monitor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitor"))

    @monitor.setter
    def monitor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__150c329aed5888faaa59781f52865e6c177c3b23e5970910d509767aca98dee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "order"))

    @order.setter
    def order(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5029f76df3901d3691949e3029663be5d5866881f0918f7ceb183c3dacf27dcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelism")
    def parallelism(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelism"))

    @parallelism.setter
    def parallelism(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f4140351b9a99f41ffc6e7a8d89cd6d4bd2030b4aefe1a64daff15137d49c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelism", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceRollbackConfig]:
        return typing.cast(typing.Optional[ServiceRollbackConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceRollbackConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec7eb086999c9dfb7b9c7826e79c107ded82415feb548221b3cdcb30d72655b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpec",
    jsii_struct_bases=[],
    name_mapping={
        "container_spec": "containerSpec",
        "force_update": "forceUpdate",
        "log_driver": "logDriver",
        "networks_advanced": "networksAdvanced",
        "placement": "placement",
        "resources": "resources",
        "restart_policy": "restartPolicy",
        "runtime": "runtime",
    },
)
class ServiceTaskSpec:
    def __init__(
        self,
        *,
        container_spec: typing.Union["ServiceTaskSpecContainerSpec", typing.Dict[builtins.str, typing.Any]],
        force_update: typing.Optional[jsii.Number] = None,
        log_driver: typing.Optional[typing.Union["ServiceTaskSpecLogDriver", typing.Dict[builtins.str, typing.Any]]] = None,
        networks_advanced: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecNetworksAdvanced", typing.Dict[builtins.str, typing.Any]]]]] = None,
        placement: typing.Optional[typing.Union["ServiceTaskSpecPlacement", typing.Dict[builtins.str, typing.Any]]] = None,
        resources: typing.Optional[typing.Union["ServiceTaskSpecResources", typing.Dict[builtins.str, typing.Any]]] = None,
        restart_policy: typing.Optional[typing.Union["ServiceTaskSpecRestartPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_spec: container_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#container_spec Service#container_spec}
        :param force_update: A counter that triggers an update even if no relevant parameters have been changed. See the `spec <https://github.com/docker/swarmkit/blob/master/api/specs.proto#L126>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#force_update Service#force_update}
        :param log_driver: log_driver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#log_driver Service#log_driver}
        :param networks_advanced: networks_advanced block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#networks_advanced Service#networks_advanced}
        :param placement: placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#placement Service#placement}
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#resources Service#resources}
        :param restart_policy: restart_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#restart_policy Service#restart_policy}
        :param runtime: Runtime is the type of runtime specified for the task executor. See the `types <https://github.com/moby/moby/blob/master/api/types/swarm/runtime.go>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#runtime Service#runtime}
        '''
        if isinstance(container_spec, dict):
            container_spec = ServiceTaskSpecContainerSpec(**container_spec)
        if isinstance(log_driver, dict):
            log_driver = ServiceTaskSpecLogDriver(**log_driver)
        if isinstance(placement, dict):
            placement = ServiceTaskSpecPlacement(**placement)
        if isinstance(resources, dict):
            resources = ServiceTaskSpecResources(**resources)
        if isinstance(restart_policy, dict):
            restart_policy = ServiceTaskSpecRestartPolicy(**restart_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a557151ba96da7ec1a3904f39bdb2aa832d5f01689a1432cc8cabfd971386ae)
            check_type(argname="argument container_spec", value=container_spec, expected_type=type_hints["container_spec"])
            check_type(argname="argument force_update", value=force_update, expected_type=type_hints["force_update"])
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument networks_advanced", value=networks_advanced, expected_type=type_hints["networks_advanced"])
            check_type(argname="argument placement", value=placement, expected_type=type_hints["placement"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument restart_policy", value=restart_policy, expected_type=type_hints["restart_policy"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_spec": container_spec,
        }
        if force_update is not None:
            self._values["force_update"] = force_update
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if networks_advanced is not None:
            self._values["networks_advanced"] = networks_advanced
        if placement is not None:
            self._values["placement"] = placement
        if resources is not None:
            self._values["resources"] = resources
        if restart_policy is not None:
            self._values["restart_policy"] = restart_policy
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def container_spec(self) -> "ServiceTaskSpecContainerSpec":
        '''container_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#container_spec Service#container_spec}
        '''
        result = self._values.get("container_spec")
        assert result is not None, "Required property 'container_spec' is missing"
        return typing.cast("ServiceTaskSpecContainerSpec", result)

    @builtins.property
    def force_update(self) -> typing.Optional[jsii.Number]:
        '''A counter that triggers an update even if no relevant parameters have been changed. See the `spec <https://github.com/docker/swarmkit/blob/master/api/specs.proto#L126>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#force_update Service#force_update}
        '''
        result = self._values.get("force_update")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_driver(self) -> typing.Optional["ServiceTaskSpecLogDriver"]:
        '''log_driver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#log_driver Service#log_driver}
        '''
        result = self._values.get("log_driver")
        return typing.cast(typing.Optional["ServiceTaskSpecLogDriver"], result)

    @builtins.property
    def networks_advanced(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecNetworksAdvanced"]]]:
        '''networks_advanced block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#networks_advanced Service#networks_advanced}
        '''
        result = self._values.get("networks_advanced")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecNetworksAdvanced"]]], result)

    @builtins.property
    def placement(self) -> typing.Optional["ServiceTaskSpecPlacement"]:
        '''placement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#placement Service#placement}
        '''
        result = self._values.get("placement")
        return typing.cast(typing.Optional["ServiceTaskSpecPlacement"], result)

    @builtins.property
    def resources(self) -> typing.Optional["ServiceTaskSpecResources"]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#resources Service#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional["ServiceTaskSpecResources"], result)

    @builtins.property
    def restart_policy(self) -> typing.Optional["ServiceTaskSpecRestartPolicy"]:
        '''restart_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#restart_policy Service#restart_policy}
        '''
        result = self._values.get("restart_policy")
        return typing.cast(typing.Optional["ServiceTaskSpecRestartPolicy"], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''Runtime is the type of runtime specified for the task executor. See the `types <https://github.com/moby/moby/blob/master/api/types/swarm/runtime.go>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#runtime Service#runtime}
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpec",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "args": "args",
        "command": "command",
        "configs": "configs",
        "dir": "dir",
        "dns_config": "dnsConfig",
        "env": "env",
        "groups": "groups",
        "healthcheck": "healthcheck",
        "hostname": "hostname",
        "hosts": "hosts",
        "isolation": "isolation",
        "labels": "labels",
        "mounts": "mounts",
        "privileges": "privileges",
        "read_only": "readOnly",
        "secrets": "secrets",
        "stop_grace_period": "stopGracePeriod",
        "stop_signal": "stopSignal",
        "sysctl": "sysctl",
        "user": "user",
    },
)
class ServiceTaskSpecContainerSpec:
    def __init__(
        self,
        *,
        image: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dir: typing.Optional[builtins.str] = None,
        dns_config: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecDnsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        healthcheck: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecHealthcheck", typing.Dict[builtins.str, typing.Any]]] = None,
        hostname: typing.Optional[builtins.str] = None,
        hosts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecHosts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        isolation: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        privileges: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecPrivileges", typing.Dict[builtins.str, typing.Any]]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecSecrets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stop_grace_period: typing.Optional[builtins.str] = None,
        stop_signal: typing.Optional[builtins.str] = None,
        sysctl: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image: The image name to use for the containers of the service, like ``nginx:1.17.6``. Also use the data-source or resource of ``docker_image`` with the ``repo_digest`` or ``docker_registry_image`` with the ``name`` attribute for this, as shown in the examples. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#image Service#image}
        :param args: Arguments to the command. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#args Service#args}
        :param command: The command/entrypoint to be run in the image. According to the `docker cli <https://github.com/docker/cli/blob/v20.10.7/cli/command/service/opts.go#L705>`_ the override of the entrypoint is also passed to the ``command`` property and there is no ``entrypoint`` attribute in the ``ContainerSpec`` of the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#command Service#command}
        :param configs: configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#configs Service#configs}
        :param dir: The working directory for commands to run in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#dir Service#dir}
        :param dns_config: dns_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#dns_config Service#dns_config}
        :param env: A list of environment variables in the form VAR="value". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#env Service#env}
        :param groups: A list of additional groups that the container process will run as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#groups Service#groups}
        :param healthcheck: healthcheck block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#healthcheck Service#healthcheck}
        :param hostname: The hostname to use for the container, as a valid RFC 1123 hostname. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#hostname Service#hostname}
        :param hosts: hosts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#hosts Service#hosts}
        :param isolation: Isolation technology of the containers running the service. (Windows only). Defaults to ``default``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#isolation Service#isolation}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#labels Service#labels}
        :param mounts: mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#mounts Service#mounts}
        :param privileges: privileges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#privileges Service#privileges}
        :param read_only: Mount the container's root filesystem as read only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#read_only Service#read_only}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#secrets Service#secrets}
        :param stop_grace_period: Amount of time to wait for the container to terminate before forcefully removing it (ms|s|m|h). If not specified or '0s' the destroy will not check if all tasks/containers of the service terminate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#stop_grace_period Service#stop_grace_period}
        :param stop_signal: Signal to stop the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#stop_signal Service#stop_signal}
        :param sysctl: Sysctls config (Linux only). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#sysctl Service#sysctl}
        :param user: The user inside the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#user Service#user}
        '''
        if isinstance(dns_config, dict):
            dns_config = ServiceTaskSpecContainerSpecDnsConfig(**dns_config)
        if isinstance(healthcheck, dict):
            healthcheck = ServiceTaskSpecContainerSpecHealthcheck(**healthcheck)
        if isinstance(privileges, dict):
            privileges = ServiceTaskSpecContainerSpecPrivileges(**privileges)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12811eebe80f327add12f713dfbcfe19ddb3188056fdd789914881c60506712c)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument configs", value=configs, expected_type=type_hints["configs"])
            check_type(argname="argument dir", value=dir, expected_type=type_hints["dir"])
            check_type(argname="argument dns_config", value=dns_config, expected_type=type_hints["dns_config"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument healthcheck", value=healthcheck, expected_type=type_hints["healthcheck"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument hosts", value=hosts, expected_type=type_hints["hosts"])
            check_type(argname="argument isolation", value=isolation, expected_type=type_hints["isolation"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument mounts", value=mounts, expected_type=type_hints["mounts"])
            check_type(argname="argument privileges", value=privileges, expected_type=type_hints["privileges"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument stop_grace_period", value=stop_grace_period, expected_type=type_hints["stop_grace_period"])
            check_type(argname="argument stop_signal", value=stop_signal, expected_type=type_hints["stop_signal"])
            check_type(argname="argument sysctl", value=sysctl, expected_type=type_hints["sysctl"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if args is not None:
            self._values["args"] = args
        if command is not None:
            self._values["command"] = command
        if configs is not None:
            self._values["configs"] = configs
        if dir is not None:
            self._values["dir"] = dir
        if dns_config is not None:
            self._values["dns_config"] = dns_config
        if env is not None:
            self._values["env"] = env
        if groups is not None:
            self._values["groups"] = groups
        if healthcheck is not None:
            self._values["healthcheck"] = healthcheck
        if hostname is not None:
            self._values["hostname"] = hostname
        if hosts is not None:
            self._values["hosts"] = hosts
        if isolation is not None:
            self._values["isolation"] = isolation
        if labels is not None:
            self._values["labels"] = labels
        if mounts is not None:
            self._values["mounts"] = mounts
        if privileges is not None:
            self._values["privileges"] = privileges
        if read_only is not None:
            self._values["read_only"] = read_only
        if secrets is not None:
            self._values["secrets"] = secrets
        if stop_grace_period is not None:
            self._values["stop_grace_period"] = stop_grace_period
        if stop_signal is not None:
            self._values["stop_signal"] = stop_signal
        if sysctl is not None:
            self._values["sysctl"] = sysctl
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def image(self) -> builtins.str:
        '''The image name to use for the containers of the service, like ``nginx:1.17.6``. Also use the data-source or resource of ``docker_image`` with the ``repo_digest`` or ``docker_registry_image`` with the ``name`` attribute for this, as shown in the examples.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#image Service#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Arguments to the command.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#args Service#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The command/entrypoint to be run in the image.

        According to the `docker cli <https://github.com/docker/cli/blob/v20.10.7/cli/command/service/opts.go#L705>`_ the override of the entrypoint is also passed to the ``command`` property and there is no ``entrypoint`` attribute in the ``ContainerSpec`` of the service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#command Service#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecConfigs"]]]:
        '''configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#configs Service#configs}
        '''
        result = self._values.get("configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecConfigs"]]], result)

    @builtins.property
    def dir(self) -> typing.Optional[builtins.str]:
        '''The working directory for commands to run in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#dir Service#dir}
        '''
        result = self._values.get("dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_config(self) -> typing.Optional["ServiceTaskSpecContainerSpecDnsConfig"]:
        '''dns_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#dns_config Service#dns_config}
        '''
        result = self._values.get("dns_config")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecDnsConfig"], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A list of environment variables in the form VAR="value".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#env Service#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of additional groups that the container process will run as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#groups Service#groups}
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def healthcheck(self) -> typing.Optional["ServiceTaskSpecContainerSpecHealthcheck"]:
        '''healthcheck block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#healthcheck Service#healthcheck}
        '''
        result = self._values.get("healthcheck")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecHealthcheck"], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''The hostname to use for the container, as a valid RFC 1123 hostname.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#hostname Service#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hosts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecHosts"]]]:
        '''hosts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#hosts Service#hosts}
        '''
        result = self._values.get("hosts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecHosts"]]], result)

    @builtins.property
    def isolation(self) -> typing.Optional[builtins.str]:
        '''Isolation technology of the containers running the service. (Windows only). Defaults to ``default``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#isolation Service#isolation}
        '''
        result = self._values.get("isolation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecLabels"]]]:
        '''labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#labels Service#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecLabels"]]], result)

    @builtins.property
    def mounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecMounts"]]]:
        '''mounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#mounts Service#mounts}
        '''
        result = self._values.get("mounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecMounts"]]], result)

    @builtins.property
    def privileges(self) -> typing.Optional["ServiceTaskSpecContainerSpecPrivileges"]:
        '''privileges block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#privileges Service#privileges}
        '''
        result = self._values.get("privileges")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecPrivileges"], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Mount the container's root filesystem as read only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#read_only Service#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecSecrets"]]]:
        '''secrets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#secrets Service#secrets}
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecSecrets"]]], result)

    @builtins.property
    def stop_grace_period(self) -> typing.Optional[builtins.str]:
        '''Amount of time to wait for the container to terminate before forcefully removing it (ms|s|m|h).

        If not specified or '0s' the destroy will not check if all tasks/containers of the service terminate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#stop_grace_period Service#stop_grace_period}
        '''
        result = self._values.get("stop_grace_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stop_signal(self) -> typing.Optional[builtins.str]:
        '''Signal to stop the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#stop_signal Service#stop_signal}
        '''
        result = self._values.get("stop_signal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sysctl(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Sysctls config (Linux only).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#sysctl Service#sysctl}
        '''
        result = self._values.get("sysctl")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''The user inside the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#user Service#user}
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "config_id": "configId",
        "file_name": "fileName",
        "config_name": "configName",
        "file_gid": "fileGid",
        "file_mode": "fileMode",
        "file_uid": "fileUid",
    },
)
class ServiceTaskSpecContainerSpecConfigs:
    def __init__(
        self,
        *,
        config_id: builtins.str,
        file_name: builtins.str,
        config_name: typing.Optional[builtins.str] = None,
        file_gid: typing.Optional[builtins.str] = None,
        file_mode: typing.Optional[jsii.Number] = None,
        file_uid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config_id: ID of the specific config that we're referencing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#config_id Service#config_id}
        :param file_name: Represents the final filename in the filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_name Service#file_name}
        :param config_name: Name of the config that this references, but this is just provided for lookup/display purposes. The config in the reference will be identified by its ID Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#config_name Service#config_name}
        :param file_gid: Represents the file GID. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_gid Service#file_gid}
        :param file_mode: Represents represents the FileMode of the file. Defaults to ``0o444``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_mode Service#file_mode}
        :param file_uid: Represents the file UID. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_uid Service#file_uid}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524d2e87218a7ae3b97508f6a0d691ddedfe599300410bd56a01ab894d6495a0)
            check_type(argname="argument config_id", value=config_id, expected_type=type_hints["config_id"])
            check_type(argname="argument file_name", value=file_name, expected_type=type_hints["file_name"])
            check_type(argname="argument config_name", value=config_name, expected_type=type_hints["config_name"])
            check_type(argname="argument file_gid", value=file_gid, expected_type=type_hints["file_gid"])
            check_type(argname="argument file_mode", value=file_mode, expected_type=type_hints["file_mode"])
            check_type(argname="argument file_uid", value=file_uid, expected_type=type_hints["file_uid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_id": config_id,
            "file_name": file_name,
        }
        if config_name is not None:
            self._values["config_name"] = config_name
        if file_gid is not None:
            self._values["file_gid"] = file_gid
        if file_mode is not None:
            self._values["file_mode"] = file_mode
        if file_uid is not None:
            self._values["file_uid"] = file_uid

    @builtins.property
    def config_id(self) -> builtins.str:
        '''ID of the specific config that we're referencing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#config_id Service#config_id}
        '''
        result = self._values.get("config_id")
        assert result is not None, "Required property 'config_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file_name(self) -> builtins.str:
        '''Represents the final filename in the filesystem.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_name Service#file_name}
        '''
        result = self._values.get("file_name")
        assert result is not None, "Required property 'file_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config_name(self) -> typing.Optional[builtins.str]:
        '''Name of the config that this references, but this is just provided for lookup/display purposes.

        The config in the reference will be identified by its ID

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#config_name Service#config_name}
        '''
        result = self._values.get("config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_gid(self) -> typing.Optional[builtins.str]:
        '''Represents the file GID. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_gid Service#file_gid}
        '''
        result = self._values.get("file_gid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_mode(self) -> typing.Optional[jsii.Number]:
        '''Represents represents the FileMode of the file. Defaults to ``0o444``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_mode Service#file_mode}
        '''
        result = self._values.get("file_mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def file_uid(self) -> typing.Optional[builtins.str]:
        '''Represents the file UID. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_uid Service#file_uid}
        '''
        result = self._values.get("file_uid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71ff3283615ff64c7307894cd31fa4068ba42c6d25347a02a29bd240cba2c225)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecContainerSpecConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d356a4f8988331ea33f010c67f5b74a39981d8aea94c6a52833c4db84d14964f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecContainerSpecConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__344362c98d935b9e78bd402c157e558e1d840dd764da015f864ab5074277295a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56045433a181f6b60642dd0b38681f08775e0d41a8fb2f22c2bfb695db236cf7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__907d1fc2b52d1380b949fe3a77752cf17167458719c6b3d6d23569e244d49c9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d3c5b9a2b9413140e1c49e3021b2c67baac76ee14f2bf3d8e983b95fc6f7a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ea6162716e97a303af4559f6881044a0effd240f753688f725ab7153b096e84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConfigName")
    def reset_config_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigName", []))

    @jsii.member(jsii_name="resetFileGid")
    def reset_file_gid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileGid", []))

    @jsii.member(jsii_name="resetFileMode")
    def reset_file_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileMode", []))

    @jsii.member(jsii_name="resetFileUid")
    def reset_file_uid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUid", []))

    @builtins.property
    @jsii.member(jsii_name="configIdInput")
    def config_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configNameInput")
    def config_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fileGidInput")
    def file_gid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileGidInput"))

    @builtins.property
    @jsii.member(jsii_name="fileModeInput")
    def file_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fileModeInput"))

    @builtins.property
    @jsii.member(jsii_name="fileNameInput")
    def file_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUidInput")
    def file_uid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileUidInput"))

    @builtins.property
    @jsii.member(jsii_name="configId")
    def config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configId"))

    @config_id.setter
    def config_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__863652747b49f3b5fd3f89057dd0f2d03e6cb1eeeb3c3c6f0aef03ce539ec395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configName")
    def config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configName"))

    @config_name.setter
    def config_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae10865658b0ea5756050d94e2b8477639a7077daf79d477c7d8f4873009893c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileGid")
    def file_gid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileGid"))

    @file_gid.setter
    def file_gid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9751c5c20b651272c6e1264f602d740b1186de45c0edf0f93e029907ca5dd44c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileGid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileMode")
    def file_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fileMode"))

    @file_mode.setter
    def file_mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b6519551fed21be49348185d8b5aaed8048af81b5888abfadac7ebc7cb915d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileName")
    def file_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileName"))

    @file_name.setter
    def file_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a86c841a07e552b1ccbc672e64dd053a4aed3cce048f5df1e5802cd7118f755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUid")
    def file_uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileUid"))

    @file_uid.setter
    def file_uid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__781258c22c4a1555c21e9a6f9e27d1056b0ed70de9b8a4f21d257ab4de105d2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbd9a74237def2e3e196402a2a5ad1f55fc8026ba31c255ddcc346a6b17a2ac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecDnsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "nameservers": "nameservers",
        "options": "options",
        "search": "search",
    },
)
class ServiceTaskSpecContainerSpecDnsConfig:
    def __init__(
        self,
        *,
        nameservers: typing.Sequence[builtins.str],
        options: typing.Optional[typing.Sequence[builtins.str]] = None,
        search: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param nameservers: The IP addresses of the name servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#nameservers Service#nameservers}
        :param options: A list of internal resolver variables to be modified (e.g., ``debug``, ``ndots:3``, etc.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#options Service#options}
        :param search: A search list for host-name lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#search Service#search}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc919fa7a74ce1c894169d02e9e1739ef63f562f9f127747c15205a9830413e)
            check_type(argname="argument nameservers", value=nameservers, expected_type=type_hints["nameservers"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument search", value=search, expected_type=type_hints["search"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "nameservers": nameservers,
        }
        if options is not None:
            self._values["options"] = options
        if search is not None:
            self._values["search"] = search

    @builtins.property
    def nameservers(self) -> typing.List[builtins.str]:
        '''The IP addresses of the name servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#nameservers Service#nameservers}
        '''
        result = self._values.get("nameservers")
        assert result is not None, "Required property 'nameservers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of internal resolver variables to be modified (e.g., ``debug``, ``ndots:3``, etc.).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#options Service#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def search(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A search list for host-name lookup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#search Service#search}
        '''
        result = self._values.get("search")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecDnsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecDnsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecDnsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adeca96c9befea02284d88027188378a2a677ad00f00153bc57fa3de56f80cf2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOptions")
    def reset_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptions", []))

    @jsii.member(jsii_name="resetSearch")
    def reset_search(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearch", []))

    @builtins.property
    @jsii.member(jsii_name="nameserversInput")
    def nameservers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nameserversInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsInput")
    def options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "optionsInput"))

    @builtins.property
    @jsii.member(jsii_name="searchInput")
    def search_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "searchInput"))

    @builtins.property
    @jsii.member(jsii_name="nameservers")
    def nameservers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nameservers"))

    @nameservers.setter
    def nameservers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf5d6fcfba77ea4c0f41bb8f62d315ef3043bfc4f876e5800d2194168a3a0e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameservers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872de710ddfa248550d19810d96ac78dd5737fb3ba140a832ddb5f20574de555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="search")
    def search(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "search"))

    @search.setter
    def search(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__888240db7eb5f6aa8247994eb99fb5c5e22d6fb16ccae45670f81871cc8048af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "search", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecContainerSpecDnsConfig]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecDnsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecDnsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__febccc1933b13afb269578856684b916c108550dfe4a3cfc320f796383880cdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecHealthcheck",
    jsii_struct_bases=[],
    name_mapping={
        "test": "test",
        "interval": "interval",
        "retries": "retries",
        "start_period": "startPeriod",
        "timeout": "timeout",
    },
)
class ServiceTaskSpecContainerSpecHealthcheck:
    def __init__(
        self,
        *,
        test: typing.Sequence[builtins.str],
        interval: typing.Optional[builtins.str] = None,
        retries: typing.Optional[jsii.Number] = None,
        start_period: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param test: The test to perform as list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#test Service#test}
        :param interval: Time between running the check (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#interval Service#interval}
        :param retries: Consecutive failures needed to report unhealthy. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#retries Service#retries}
        :param start_period: Start period for the container to initialize before counting retries towards unstable (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#start_period Service#start_period}
        :param timeout: Maximum time to allow one check to run (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#timeout Service#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f45521d61f6e1a9852714161336045126afa373cb7221fd7ff9987536d5ad24f)
            check_type(argname="argument test", value=test, expected_type=type_hints["test"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument retries", value=retries, expected_type=type_hints["retries"])
            check_type(argname="argument start_period", value=start_period, expected_type=type_hints["start_period"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "test": test,
        }
        if interval is not None:
            self._values["interval"] = interval
        if retries is not None:
            self._values["retries"] = retries
        if start_period is not None:
            self._values["start_period"] = start_period
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def test(self) -> typing.List[builtins.str]:
        '''The test to perform as list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#test Service#test}
        '''
        result = self._values.get("test")
        assert result is not None, "Required property 'test' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def interval(self) -> typing.Optional[builtins.str]:
        '''Time between running the check (ms|s|m|h). Defaults to ``0s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#interval Service#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retries(self) -> typing.Optional[jsii.Number]:
        '''Consecutive failures needed to report unhealthy. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#retries Service#retries}
        '''
        result = self._values.get("retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_period(self) -> typing.Optional[builtins.str]:
        '''Start period for the container to initialize before counting retries towards unstable (ms|s|m|h). Defaults to ``0s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#start_period Service#start_period}
        '''
        result = self._values.get("start_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Maximum time to allow one check to run (ms|s|m|h). Defaults to ``0s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#timeout Service#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecHealthcheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecHealthcheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecHealthcheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24ad7d98c4fb41f8916d0e048589be2fe7fe64fe9f0d74bb666ff64f57d5127f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetRetries")
    def reset_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetries", []))

    @jsii.member(jsii_name="resetStartPeriod")
    def reset_start_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartPeriod", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="retriesInput")
    def retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retriesInput"))

    @builtins.property
    @jsii.member(jsii_name="startPeriodInput")
    def start_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="testInput")
    def test_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "testInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db936880f880ac4e1d1254933bb432ed147a397ebe964ae52b00a28cbd949538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retries")
    def retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retries"))

    @retries.setter
    def retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c287aa9c27448d4c1d6d9cc086573cb5d34d96e7a2d720a99d7fec86e3c28978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startPeriod")
    def start_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startPeriod"))

    @start_period.setter
    def start_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb7201e3806786b19cfd2029b7776173784ec9568b1d1b5c6ee32c112518d0a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="test")
    def test(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "test"))

    @test.setter
    def test(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ac18750f263ab339938439d70e27f672ffefb0c72754c9e077b491931e764f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "test", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15f5c97e0a6d52fdf8ec9d385081a418db9974e8b837c5c0b4f087f683985836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecHealthcheck]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecHealthcheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecHealthcheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d19bc8a0dca6f1f0c7d2d7f751cdbfb9e8349858ea4c5a9cc24d4ad70b9ab62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecHosts",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "ip": "ip"},
)
class ServiceTaskSpecContainerSpecHosts:
    def __init__(self, *, host: builtins.str, ip: builtins.str) -> None:
        '''
        :param host: The name of the host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#host Service#host}
        :param ip: The ip of the host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#ip Service#ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ecca4df29cdebfcd58f083ec1a56a9418ed746e5de6e5ff1c7fec67455a70e)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
            "ip": ip,
        }

    @builtins.property
    def host(self) -> builtins.str:
        '''The name of the host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#host Service#host}
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip(self) -> builtins.str:
        '''The ip of the host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#ip Service#ip}
        '''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecHosts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecHostsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecHostsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5aafca96e45acbcf08cf1b81613650c393a988ac986cc857b197d4e29f6669c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecContainerSpecHostsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__817d0e2df4139f603ed52a1f88fbee2ed2425e7834f7079085806f746dc73fb4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecContainerSpecHostsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8f1ea3eebd614a4b3370b9e5b04205f1c2ba7c007bd7e1bf793073e4f1047b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3994004ee7411dd50693adcecc03b808ca4fcca37cf2c6954576cc7f4eb3e1c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d860e7686063ab91d63b2d81379ae983ffa5d28771167499648ed9fd8b18c819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecHosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecHosts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecHosts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2befc994619217e9b862f791c3d5f7794713fc8dc25016e35746033c259e6ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecHostsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecHostsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89fc523d8f9117beac7cdcacef2e091269db6b0fb42c78ba3af22fc7fd4dbf0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c93322c57698fb9f6dc7a7f66032643344b446e8787107d83d71f6640628ec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f23ae663b165ca55124002de1fbcbedfd4dcb3d7c952236b5e0f1acd73687f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecHosts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecHosts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecHosts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43eb159a744ad5f3e7a62ae88a53ecb8b9af7bdaf77a5fde4e87b0c39c1d722c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class ServiceTaskSpecContainerSpecLabels:
    def __init__(self, *, label: builtins.str, value: builtins.str) -> None:
        '''
        :param label: Name of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#label Service#label}
        :param value: Value of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#value Service#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab178bc59eb13d2a1b4af3c98513b2c5bc6623690187241562fd6a5cc9cd0007)
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> builtins.str:
        '''Name of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#label Service#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#value Service#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0340b88a7f9b84e19d8f37660b50e3991759ddafbad5c8b73b01c95108148146)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecContainerSpecLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59b5a76dc63c9783aef6da692f65380338bb78b5557d09aa727d77e2e2382939)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecContainerSpecLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4794dbf56e00b8ceed5aa198f95a5668117265e37fbeeab37e737cd4ba5451cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dd6459f154951bcab82820a50acd86bc0c6272cd77b99a01c0e400b22d2bd9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53717a0dce739858b2a446969baaf6bf4b8c3e67d91669804676cc2a38f61e88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ef207a0c607125cc2db1f6d6de1dbdeb5ea193f99575c5e0d14efc46bde0d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bbf30cc84c985d0733bcfba913afbbebcb2570c4f586816faeb3c5b6ba0a71f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bce6b961a53fd7a934aaff4b4fc1b16c9110b1b80cdf25e393b888da5d0c51a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66946ad2a06719da0cbd956a76c273da66441b35085f951a9d1aff0224e84902)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aa0807427c680ed4b3e8d2445e67f689e77d5d0e2d1d2f727e16ec8bcf4f387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecMounts",
    jsii_struct_bases=[],
    name_mapping={
        "target": "target",
        "type": "type",
        "bind_options": "bindOptions",
        "read_only": "readOnly",
        "source": "source",
        "tmpfs_options": "tmpfsOptions",
        "volume_options": "volumeOptions",
    },
)
class ServiceTaskSpecContainerSpecMounts:
    def __init__(
        self,
        *,
        target: builtins.str,
        type: builtins.str,
        bind_options: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecMountsBindOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source: typing.Optional[builtins.str] = None,
        tmpfs_options: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecMountsTmpfsOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_options: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecMountsVolumeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param target: Container path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#target Service#target}
        :param type: The mount type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#type Service#type}
        :param bind_options: bind_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#bind_options Service#bind_options}
        :param read_only: Whether the mount should be read-only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#read_only Service#read_only}
        :param source: Mount source (e.g. a volume name, a host path). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#source Service#source}
        :param tmpfs_options: tmpfs_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#tmpfs_options Service#tmpfs_options}
        :param volume_options: volume_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#volume_options Service#volume_options}
        '''
        if isinstance(bind_options, dict):
            bind_options = ServiceTaskSpecContainerSpecMountsBindOptions(**bind_options)
        if isinstance(tmpfs_options, dict):
            tmpfs_options = ServiceTaskSpecContainerSpecMountsTmpfsOptions(**tmpfs_options)
        if isinstance(volume_options, dict):
            volume_options = ServiceTaskSpecContainerSpecMountsVolumeOptions(**volume_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c5a4cfe63778a7eea46a5665601cf87d6964416399edd27098ac1f02c50ab5)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument bind_options", value=bind_options, expected_type=type_hints["bind_options"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument tmpfs_options", value=tmpfs_options, expected_type=type_hints["tmpfs_options"])
            check_type(argname="argument volume_options", value=volume_options, expected_type=type_hints["volume_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
            "type": type,
        }
        if bind_options is not None:
            self._values["bind_options"] = bind_options
        if read_only is not None:
            self._values["read_only"] = read_only
        if source is not None:
            self._values["source"] = source
        if tmpfs_options is not None:
            self._values["tmpfs_options"] = tmpfs_options
        if volume_options is not None:
            self._values["volume_options"] = volume_options

    @builtins.property
    def target(self) -> builtins.str:
        '''Container path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#target Service#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The mount type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#type Service#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bind_options(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecMountsBindOptions"]:
        '''bind_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#bind_options Service#bind_options}
        '''
        result = self._values.get("bind_options")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecMountsBindOptions"], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the mount should be read-only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#read_only Service#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Mount source (e.g. a volume name, a host path).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#source Service#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tmpfs_options(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecMountsTmpfsOptions"]:
        '''tmpfs_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#tmpfs_options Service#tmpfs_options}
        '''
        result = self._values.get("tmpfs_options")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecMountsTmpfsOptions"], result)

    @builtins.property
    def volume_options(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecMountsVolumeOptions"]:
        '''volume_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#volume_options Service#volume_options}
        '''
        result = self._values.get("volume_options")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecMountsVolumeOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecMountsBindOptions",
    jsii_struct_bases=[],
    name_mapping={"propagation": "propagation"},
)
class ServiceTaskSpecContainerSpecMountsBindOptions:
    def __init__(self, *, propagation: typing.Optional[builtins.str] = None) -> None:
        '''
        :param propagation: Bind propagation refers to whether or not mounts created within a given bind-mount or named volume can be propagated to replicas of that mount. See the `docs <https://docs.docker.com/storage/bind-mounts/#configure-bind-propagation>`_ for details. Defaults to ``rprivate`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#propagation Service#propagation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c9a1c46ed1f95bcbed414e91df9af8035af74134edbd9ad247bf3c864d0abf)
            check_type(argname="argument propagation", value=propagation, expected_type=type_hints["propagation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if propagation is not None:
            self._values["propagation"] = propagation

    @builtins.property
    def propagation(self) -> typing.Optional[builtins.str]:
        '''Bind propagation refers to whether or not mounts created within a given bind-mount or named volume can be propagated to replicas of that mount.

        See the `docs <https://docs.docker.com/storage/bind-mounts/#configure-bind-propagation>`_ for details. Defaults to ``rprivate``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#propagation Service#propagation}
        '''
        result = self._values.get("propagation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecMountsBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecMountsBindOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecMountsBindOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c4f2918fb86790743be059ab9e74bac7937fe260c90a3dafa29cefec14fcf79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPropagation")
    def reset_propagation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPropagation", []))

    @builtins.property
    @jsii.member(jsii_name="propagationInput")
    def propagation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "propagationInput"))

    @builtins.property
    @jsii.member(jsii_name="propagation")
    def propagation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "propagation"))

    @propagation.setter
    def propagation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9346817ac45d0e3f96dbbe9140512aa290675553054bf83df92561cfea1b164)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propagation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecMountsBindOptions]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecMountsBindOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecMountsBindOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3549a3f917f825b1bbf1b5c8103ad465830cf71ce4e9a98fde9cf46ba2459dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecMountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecMountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__473b5aec5c5e85999d9e021f3ba67a830f25ae908c2ba211c711ef04af2d8ae4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecContainerSpecMountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__485349789f479470cd0ebd426497012286987263c9f135917f1c738e800723a6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecContainerSpecMountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf833195e4e97c34c51d5ad54e3972e1d29cd3120b0b815a316600b999db4582)
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
            type_hints = typing.get_type_hints(_typecheckingstub__569fc547400da5fb24b2e5efb7eac6ae0d3c6eb5a45c597f5a61fea3df66e8fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86dc8c7622ec19568ea5c31287a619876a8ed9dd6f8181eff1e71bfb36aeda99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74eab88802085219f2259bc0029c82500f68f4a8ed6e50809c8fc9e0f52ed93d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecMountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecMountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b6ee1c900e4c078bd2e13081317367d600ffc9f95bf52332ea1d691b179d936)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBindOptions")
    def put_bind_options(
        self,
        *,
        propagation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param propagation: Bind propagation refers to whether or not mounts created within a given bind-mount or named volume can be propagated to replicas of that mount. See the `docs <https://docs.docker.com/storage/bind-mounts/#configure-bind-propagation>`_ for details. Defaults to ``rprivate`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#propagation Service#propagation}
        '''
        value = ServiceTaskSpecContainerSpecMountsBindOptions(propagation=propagation)

        return typing.cast(None, jsii.invoke(self, "putBindOptions", [value]))

    @jsii.member(jsii_name="putTmpfsOptions")
    def put_tmpfs_options(
        self,
        *,
        mode: typing.Optional[jsii.Number] = None,
        size_bytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param mode: The permission mode for the tmpfs mount in an integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#mode Service#mode}
        :param size_bytes: The size for the tmpfs mount in bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#size_bytes Service#size_bytes}
        '''
        value = ServiceTaskSpecContainerSpecMountsTmpfsOptions(
            mode=mode, size_bytes=size_bytes
        )

        return typing.cast(None, jsii.invoke(self, "putTmpfsOptions", [value]))

    @jsii.member(jsii_name="putVolumeOptions")
    def put_volume_options(
        self,
        *,
        driver_name: typing.Optional[builtins.str] = None,
        driver_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        no_copy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param driver_name: Name of the driver to use to create the volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#driver_name Service#driver_name}
        :param driver_options: key/value map of driver specific options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#driver_options Service#driver_options}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#labels Service#labels}
        :param no_copy: Populate volume with data from the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#no_copy Service#no_copy}
        '''
        value = ServiceTaskSpecContainerSpecMountsVolumeOptions(
            driver_name=driver_name,
            driver_options=driver_options,
            labels=labels,
            no_copy=no_copy,
        )

        return typing.cast(None, jsii.invoke(self, "putVolumeOptions", [value]))

    @jsii.member(jsii_name="resetBindOptions")
    def reset_bind_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBindOptions", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @jsii.member(jsii_name="resetTmpfsOptions")
    def reset_tmpfs_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTmpfsOptions", []))

    @jsii.member(jsii_name="resetVolumeOptions")
    def reset_volume_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeOptions", []))

    @builtins.property
    @jsii.member(jsii_name="bindOptions")
    def bind_options(
        self,
    ) -> ServiceTaskSpecContainerSpecMountsBindOptionsOutputReference:
        return typing.cast(ServiceTaskSpecContainerSpecMountsBindOptionsOutputReference, jsii.get(self, "bindOptions"))

    @builtins.property
    @jsii.member(jsii_name="tmpfsOptions")
    def tmpfs_options(
        self,
    ) -> "ServiceTaskSpecContainerSpecMountsTmpfsOptionsOutputReference":
        return typing.cast("ServiceTaskSpecContainerSpecMountsTmpfsOptionsOutputReference", jsii.get(self, "tmpfsOptions"))

    @builtins.property
    @jsii.member(jsii_name="volumeOptions")
    def volume_options(
        self,
    ) -> "ServiceTaskSpecContainerSpecMountsVolumeOptionsOutputReference":
        return typing.cast("ServiceTaskSpecContainerSpecMountsVolumeOptionsOutputReference", jsii.get(self, "volumeOptions"))

    @builtins.property
    @jsii.member(jsii_name="bindOptionsInput")
    def bind_options_input(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecMountsBindOptions]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecMountsBindOptions], jsii.get(self, "bindOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="tmpfsOptionsInput")
    def tmpfs_options_input(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecMountsTmpfsOptions"]:
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecMountsTmpfsOptions"], jsii.get(self, "tmpfsOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeOptionsInput")
    def volume_options_input(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecMountsVolumeOptions"]:
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecMountsVolumeOptions"], jsii.get(self, "volumeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readOnly"))

    @read_only.setter
    def read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3036d810beca7c8266cd3a8fd3fe36e26d020f2982c9f583794cd149ff450251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d82ff0728723759c5a36519360f11e30c129342d25e9e6ede77f9cdbbe7261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8100bc6cb4911291f74a01bb1debb8068d7a8548f43896cb645da2314d105e9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85951caf314e8887acb6205accf11295e9fe5532e35c462c4bfb20a428ddf44f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9878115bcb2a616ff8f1223dc9352acfc48d8a4a7220a4882763ff08b5e3be8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecMountsTmpfsOptions",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "size_bytes": "sizeBytes"},
)
class ServiceTaskSpecContainerSpecMountsTmpfsOptions:
    def __init__(
        self,
        *,
        mode: typing.Optional[jsii.Number] = None,
        size_bytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param mode: The permission mode for the tmpfs mount in an integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#mode Service#mode}
        :param size_bytes: The size for the tmpfs mount in bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#size_bytes Service#size_bytes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9802d31fde4769212339a34dfb45067f5a2fb459b6969836709421f63e55c336)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument size_bytes", value=size_bytes, expected_type=type_hints["size_bytes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode
        if size_bytes is not None:
            self._values["size_bytes"] = size_bytes

    @builtins.property
    def mode(self) -> typing.Optional[jsii.Number]:
        '''The permission mode for the tmpfs mount in an integer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#mode Service#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def size_bytes(self) -> typing.Optional[jsii.Number]:
        '''The size for the tmpfs mount in bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#size_bytes Service#size_bytes}
        '''
        result = self._values.get("size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecMountsTmpfsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecMountsTmpfsOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecMountsTmpfsOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e16784edad679558e1e0db2ff00af4d1cf1dac2dad55a6e4e56c158fd52e3df0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetSizeBytes")
    def reset_size_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeBytes", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeBytesInput")
    def size_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__341797b101e6733b5baf87a44d54b5e7e585269eae3fb7b197796925dc86947a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeBytes")
    def size_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeBytes"))

    @size_bytes.setter
    def size_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9beab2c4c09307b2d7454bca4fb822a786232ba3a0ae6ae001ea268d6912ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecMountsTmpfsOptions]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecMountsTmpfsOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecMountsTmpfsOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532552dca12144e62b0cb7f30457e12cdca826b056d048f0e0a9d524a84673ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecMountsVolumeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "driver_name": "driverName",
        "driver_options": "driverOptions",
        "labels": "labels",
        "no_copy": "noCopy",
    },
)
class ServiceTaskSpecContainerSpecMountsVolumeOptions:
    def __init__(
        self,
        *,
        driver_name: typing.Optional[builtins.str] = None,
        driver_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        no_copy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param driver_name: Name of the driver to use to create the volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#driver_name Service#driver_name}
        :param driver_options: key/value map of driver specific options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#driver_options Service#driver_options}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#labels Service#labels}
        :param no_copy: Populate volume with data from the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#no_copy Service#no_copy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f07e201271d489babf0eb6a88649e8971529078c3b485fb561155fa8ef5edbf7)
            check_type(argname="argument driver_name", value=driver_name, expected_type=type_hints["driver_name"])
            check_type(argname="argument driver_options", value=driver_options, expected_type=type_hints["driver_options"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument no_copy", value=no_copy, expected_type=type_hints["no_copy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if driver_name is not None:
            self._values["driver_name"] = driver_name
        if driver_options is not None:
            self._values["driver_options"] = driver_options
        if labels is not None:
            self._values["labels"] = labels
        if no_copy is not None:
            self._values["no_copy"] = no_copy

    @builtins.property
    def driver_name(self) -> typing.Optional[builtins.str]:
        '''Name of the driver to use to create the volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#driver_name Service#driver_name}
        '''
        result = self._values.get("driver_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def driver_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''key/value map of driver specific options.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#driver_options Service#driver_options}
        '''
        result = self._values.get("driver_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels"]]]:
        '''labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#labels Service#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels"]]], result)

    @builtins.property
    def no_copy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Populate volume with data from the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#no_copy Service#no_copy}
        '''
        result = self._values.get("no_copy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecMountsVolumeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels:
    def __init__(self, *, label: builtins.str, value: builtins.str) -> None:
        '''
        :param label: Name of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#label Service#label}
        :param value: Value of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#value Service#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb001381fbb74b7dea09cf341fbc61803e166e2bbf972bbdbecf652a165bdf9)
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> builtins.str:
        '''Name of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#label Service#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#value Service#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13d398467d62d18dcae946908254c716a5b60b8da60c438133e60f0cdbe8f1f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__093530a64132701433106c01b342fc0c6400586b881bda960f33474d27fc7773)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6df1d95b023771b68ad863ca806b78ec2302dc45885e5f11bd6cbad20061707)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39fbf4f9c70e7a0145841bf9eb13503866f40f64871da2bf25f8448a4943840c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ae14ea0325b9c528af59d39b9834687bb444e1367af8b8bfdb28830ea4adf46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fd3a78d1987a27c907f653445469f8596216374a18001b657b8bd35a9f844d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2436e5dc28f38038561e50d0e38c68f3e22ffa5a23e17147097fba6f438870b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96b75425fac010d2a7237f5f54b223de94060840819cadf23166377058e9c2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99cdd3e3d3ef36b31e716d8a2b283413e717c07fec3a1237475e281225197c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e9868b3a69e56a040fe8f7c5b86c2a693267ea4a9be460a8acb639f631d78e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecMountsVolumeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecMountsVolumeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5cd9f0663f792853fd5540378db2721cb32092ebc1df95ec42f88d8da93e3e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLabels")
    def put_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__094680f784e61e08a34e825738cebeb470e1c08520ff75dbbdf40ebf376f3690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLabels", [value]))

    @jsii.member(jsii_name="resetDriverName")
    def reset_driver_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverName", []))

    @jsii.member(jsii_name="resetDriverOptions")
    def reset_driver_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverOptions", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetNoCopy")
    def reset_no_copy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoCopy", []))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsList:
        return typing.cast(ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsList, jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="driverNameInput")
    def driver_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "driverNameInput"))

    @builtins.property
    @jsii.member(jsii_name="driverOptionsInput")
    def driver_options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="noCopyInput")
    def no_copy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noCopyInput"))

    @builtins.property
    @jsii.member(jsii_name="driverName")
    def driver_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driverName"))

    @driver_name.setter
    def driver_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdca8e458654fb86552e678804ecb7fe81a6d8ac85a3ee79d5aea6277f34df9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="driverOptions")
    def driver_options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverOptions"))

    @driver_options.setter
    def driver_options(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd63967ee84b043aa2761910fd516faa1b0f6c70e222f956e6b2a71153aa49b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noCopy")
    def no_copy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noCopy"))

    @no_copy.setter
    def no_copy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3501d7bfc7ccce86a9c93cadbbc407a05253181483a2759bcea22d0a24967ca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noCopy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecMountsVolumeOptions]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecMountsVolumeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecMountsVolumeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3050853b89dc61d4632d05ca351da136bb5edeb373dad34d11bfac4ecdb75062)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e7758d64b6ea74df05d9a73c61bc575d0f659f2ed6f8905b25bd89cd322ac44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfigs")
    def put_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f771f6ea81e0e0f305737daaaae2d2be623f4b0d0dfcab70c288f0a6adf08a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConfigs", [value]))

    @jsii.member(jsii_name="putDnsConfig")
    def put_dns_config(
        self,
        *,
        nameservers: typing.Sequence[builtins.str],
        options: typing.Optional[typing.Sequence[builtins.str]] = None,
        search: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param nameservers: The IP addresses of the name servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#nameservers Service#nameservers}
        :param options: A list of internal resolver variables to be modified (e.g., ``debug``, ``ndots:3``, etc.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#options Service#options}
        :param search: A search list for host-name lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#search Service#search}
        '''
        value = ServiceTaskSpecContainerSpecDnsConfig(
            nameservers=nameservers, options=options, search=search
        )

        return typing.cast(None, jsii.invoke(self, "putDnsConfig", [value]))

    @jsii.member(jsii_name="putHealthcheck")
    def put_healthcheck(
        self,
        *,
        test: typing.Sequence[builtins.str],
        interval: typing.Optional[builtins.str] = None,
        retries: typing.Optional[jsii.Number] = None,
        start_period: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param test: The test to perform as list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#test Service#test}
        :param interval: Time between running the check (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#interval Service#interval}
        :param retries: Consecutive failures needed to report unhealthy. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#retries Service#retries}
        :param start_period: Start period for the container to initialize before counting retries towards unstable (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#start_period Service#start_period}
        :param timeout: Maximum time to allow one check to run (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#timeout Service#timeout}
        '''
        value = ServiceTaskSpecContainerSpecHealthcheck(
            test=test,
            interval=interval,
            retries=retries,
            start_period=start_period,
            timeout=timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putHealthcheck", [value]))

    @jsii.member(jsii_name="putHosts")
    def put_hosts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecHosts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6666432ee8de9d86ffc705e37a37cb2526791497ac8bd22bebc8c537ab4431e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHosts", [value]))

    @jsii.member(jsii_name="putLabels")
    def put_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd4be99a14c2b58c696e5a7dcd4620941e155ee7d038e03bec76035596b8f4b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLabels", [value]))

    @jsii.member(jsii_name="putMounts")
    def put_mounts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecMounts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66f6a6ea25ed8a3e93721752d05858e9ae0cdf25deff13e15c8e3a05a3f5869)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMounts", [value]))

    @jsii.member(jsii_name="putPrivileges")
    def put_privileges(
        self,
        *,
        credential_spec: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecPrivilegesCredentialSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        se_linux_context: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param credential_spec: credential_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#credential_spec Service#credential_spec}
        :param se_linux_context: se_linux_context block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#se_linux_context Service#se_linux_context}
        '''
        value = ServiceTaskSpecContainerSpecPrivileges(
            credential_spec=credential_spec, se_linux_context=se_linux_context
        )

        return typing.cast(None, jsii.invoke(self, "putPrivileges", [value]))

    @jsii.member(jsii_name="putSecrets")
    def put_secrets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecSecrets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__037539875ffd244f8992fd33b63e8c9969dcb4d91b672ba9cbc6da2ea2f6b08d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecrets", [value]))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetConfigs")
    def reset_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigs", []))

    @jsii.member(jsii_name="resetDir")
    def reset_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDir", []))

    @jsii.member(jsii_name="resetDnsConfig")
    def reset_dns_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsConfig", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetGroups")
    def reset_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroups", []))

    @jsii.member(jsii_name="resetHealthcheck")
    def reset_healthcheck(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthcheck", []))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetHosts")
    def reset_hosts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHosts", []))

    @jsii.member(jsii_name="resetIsolation")
    def reset_isolation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsolation", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMounts")
    def reset_mounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMounts", []))

    @jsii.member(jsii_name="resetPrivileges")
    def reset_privileges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivileges", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetSecrets")
    def reset_secrets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecrets", []))

    @jsii.member(jsii_name="resetStopGracePeriod")
    def reset_stop_grace_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStopGracePeriod", []))

    @jsii.member(jsii_name="resetStopSignal")
    def reset_stop_signal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStopSignal", []))

    @jsii.member(jsii_name="resetSysctl")
    def reset_sysctl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSysctl", []))

    @jsii.member(jsii_name="resetUser")
    def reset_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUser", []))

    @builtins.property
    @jsii.member(jsii_name="configs")
    def configs(self) -> ServiceTaskSpecContainerSpecConfigsList:
        return typing.cast(ServiceTaskSpecContainerSpecConfigsList, jsii.get(self, "configs"))

    @builtins.property
    @jsii.member(jsii_name="dnsConfig")
    def dns_config(self) -> ServiceTaskSpecContainerSpecDnsConfigOutputReference:
        return typing.cast(ServiceTaskSpecContainerSpecDnsConfigOutputReference, jsii.get(self, "dnsConfig"))

    @builtins.property
    @jsii.member(jsii_name="healthcheck")
    def healthcheck(self) -> ServiceTaskSpecContainerSpecHealthcheckOutputReference:
        return typing.cast(ServiceTaskSpecContainerSpecHealthcheckOutputReference, jsii.get(self, "healthcheck"))

    @builtins.property
    @jsii.member(jsii_name="hosts")
    def hosts(self) -> ServiceTaskSpecContainerSpecHostsList:
        return typing.cast(ServiceTaskSpecContainerSpecHostsList, jsii.get(self, "hosts"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> ServiceTaskSpecContainerSpecLabelsList:
        return typing.cast(ServiceTaskSpecContainerSpecLabelsList, jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="mounts")
    def mounts(self) -> ServiceTaskSpecContainerSpecMountsList:
        return typing.cast(ServiceTaskSpecContainerSpecMountsList, jsii.get(self, "mounts"))

    @builtins.property
    @jsii.member(jsii_name="privileges")
    def privileges(self) -> "ServiceTaskSpecContainerSpecPrivilegesOutputReference":
        return typing.cast("ServiceTaskSpecContainerSpecPrivilegesOutputReference", jsii.get(self, "privileges"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> "ServiceTaskSpecContainerSpecSecretsList":
        return typing.cast("ServiceTaskSpecContainerSpecSecretsList", jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="configsInput")
    def configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecConfigs]]], jsii.get(self, "configsInput"))

    @builtins.property
    @jsii.member(jsii_name="dirInput")
    def dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dirInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsConfigInput")
    def dns_config_input(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecDnsConfig]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecDnsConfig], jsii.get(self, "dnsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsInput")
    def groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsInput"))

    @builtins.property
    @jsii.member(jsii_name="healthcheckInput")
    def healthcheck_input(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecHealthcheck]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecHealthcheck], jsii.get(self, "healthcheckInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostsInput")
    def hosts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecHosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecHosts]]], jsii.get(self, "hostsInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="isolationInput")
    def isolation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "isolationInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecLabels]]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="mountsInput")
    def mounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMounts]]], jsii.get(self, "mountsInput"))

    @builtins.property
    @jsii.member(jsii_name="privilegesInput")
    def privileges_input(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecPrivileges"]:
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecPrivileges"], jsii.get(self, "privilegesInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretsInput")
    def secrets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecSecrets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecSecrets"]]], jsii.get(self, "secretsInput"))

    @builtins.property
    @jsii.member(jsii_name="stopGracePeriodInput")
    def stop_grace_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stopGracePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="stopSignalInput")
    def stop_signal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stopSignalInput"))

    @builtins.property
    @jsii.member(jsii_name="sysctlInput")
    def sysctl_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "sysctlInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0b06743054378c1b4d9619e3b56ab20270ff2ee507d51e6a752849eb78f1618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574fc9087a66aa7863e8a8b6871be1e6a6648df780b07302557737bbb0c9bfa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dir")
    def dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dir"))

    @dir.setter
    def dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50904468bc1178e848b01687a67a71fe147ad47ce061f89d3d4d6836ae8f40af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "env"))

    @env.setter
    def env(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__172c254ef42edd8ae749b15c228ca3be428736e73d13fa2dc4ad782eb4e4807a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "env", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1708cc2d73587c925341cbe531c0343869ecbbfa44e8a3dae2f7b3f2a7ce0b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5860437b988259018896776c8b5cc253358fd68fcc4d6e6c599d3ffeab0125f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd98bbc601d7a9f7ffda5d679a157afcc04e40d8e571c8fa604ed806a51e5dc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isolation")
    def isolation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isolation"))

    @isolation.setter
    def isolation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e771ae9675414bb7fcfb264ed7a7aa4922647457e79b8bf3dbdf32b6978a792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isolation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readOnly"))

    @read_only.setter
    def read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db205e04c7321564c2433e3db97895d0f78775a4b00449dbe88dc43dc6caa03f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stopGracePeriod")
    def stop_grace_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stopGracePeriod"))

    @stop_grace_period.setter
    def stop_grace_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288d6879163c1693d85e373c3b7ee21111e80e331e5997d9181a275dbe77a0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stopGracePeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stopSignal")
    def stop_signal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stopSignal"))

    @stop_signal.setter
    def stop_signal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdcf9dfb1a990d3e7f078d7cb05a0a33deee1c635a5f5470b99c00c2186f18c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stopSignal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sysctl")
    def sysctl(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "sysctl"))

    @sysctl.setter
    def sysctl(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6cedd300f5a80db128f75a2645d08b8426395f29ebd38f46d20c16f02fe7dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sysctl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6bc356585cdccd2f0d801ddd2fe0589f1665d28db4c57083fa8e23d2c33f8dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecContainerSpec]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23adb8156d0a7dbfc558d7d5a8e3c15a0dab3ca93cef0b5fd40223452bc97fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecPrivileges",
    jsii_struct_bases=[],
    name_mapping={
        "credential_spec": "credentialSpec",
        "se_linux_context": "seLinuxContext",
    },
)
class ServiceTaskSpecContainerSpecPrivileges:
    def __init__(
        self,
        *,
        credential_spec: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecPrivilegesCredentialSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        se_linux_context: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param credential_spec: credential_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#credential_spec Service#credential_spec}
        :param se_linux_context: se_linux_context block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#se_linux_context Service#se_linux_context}
        '''
        if isinstance(credential_spec, dict):
            credential_spec = ServiceTaskSpecContainerSpecPrivilegesCredentialSpec(**credential_spec)
        if isinstance(se_linux_context, dict):
            se_linux_context = ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext(**se_linux_context)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a8f9f2b44701d4af985becb8caa455efa459005a2be56d26f462e957e8432dd)
            check_type(argname="argument credential_spec", value=credential_spec, expected_type=type_hints["credential_spec"])
            check_type(argname="argument se_linux_context", value=se_linux_context, expected_type=type_hints["se_linux_context"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if credential_spec is not None:
            self._values["credential_spec"] = credential_spec
        if se_linux_context is not None:
            self._values["se_linux_context"] = se_linux_context

    @builtins.property
    def credential_spec(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecPrivilegesCredentialSpec"]:
        '''credential_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#credential_spec Service#credential_spec}
        '''
        result = self._values.get("credential_spec")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecPrivilegesCredentialSpec"], result)

    @builtins.property
    def se_linux_context(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext"]:
        '''se_linux_context block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#se_linux_context Service#se_linux_context}
        '''
        result = self._values.get("se_linux_context")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecPrivileges(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecPrivilegesCredentialSpec",
    jsii_struct_bases=[],
    name_mapping={"file": "file", "registry": "registry"},
)
class ServiceTaskSpecContainerSpecPrivilegesCredentialSpec:
    def __init__(
        self,
        *,
        file: typing.Optional[builtins.str] = None,
        registry: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file: Load credential spec from this file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file Service#file}
        :param registry: Load credential spec from this value in the Windows registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#registry Service#registry}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb94d118dd724f3a0c2830c93a3f9a939f458c645f6c989bd2a794acfec5dff6)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file is not None:
            self._values["file"] = file
        if registry is not None:
            self._values["registry"] = registry

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''Load credential spec from this file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file Service#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry(self) -> typing.Optional[builtins.str]:
        '''Load credential spec from this value in the Windows registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#registry Service#registry}
        '''
        result = self._values.get("registry")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecPrivilegesCredentialSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecPrivilegesCredentialSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecPrivilegesCredentialSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdf0f610c65c480942b922b4560dd71ba97c3190374220dc8665fca8336bab77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetRegistry")
    def reset_registry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistry", []))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="registryInput")
    def registry_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryInput"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "file"))

    @file.setter
    def file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1bd7bd9dac88ad2706004a212594b5f81ca22b8047f134bfb0f2d1c9e19842)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "file", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registry")
    def registry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registry"))

    @registry.setter
    def registry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d07474977275208aa5488eee0283ea55a5cb43ad3ca680feaf7ee7ae0dab389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecPrivilegesCredentialSpec]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecPrivilegesCredentialSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecPrivilegesCredentialSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d82ee3ae5b793d4b47330b03e3e9582736be5ea0e5a75ee4ad600470de43360b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecPrivilegesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecPrivilegesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e310dd103b1be8738da2ac6ed668b9d86033e57a8005d710c00a3e055a784524)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCredentialSpec")
    def put_credential_spec(
        self,
        *,
        file: typing.Optional[builtins.str] = None,
        registry: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file: Load credential spec from this file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file Service#file}
        :param registry: Load credential spec from this value in the Windows registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#registry Service#registry}
        '''
        value = ServiceTaskSpecContainerSpecPrivilegesCredentialSpec(
            file=file, registry=registry
        )

        return typing.cast(None, jsii.invoke(self, "putCredentialSpec", [value]))

    @jsii.member(jsii_name="putSeLinuxContext")
    def put_se_linux_context(
        self,
        *,
        disable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        level: typing.Optional[builtins.str] = None,
        role: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disable: Disable SELinux. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#disable Service#disable}
        :param level: SELinux level label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#level Service#level}
        :param role: SELinux role label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#role Service#role}
        :param type: SELinux type label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#type Service#type}
        :param user: SELinux user label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#user Service#user}
        '''
        value = ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext(
            disable=disable, level=level, role=role, type=type, user=user
        )

        return typing.cast(None, jsii.invoke(self, "putSeLinuxContext", [value]))

    @jsii.member(jsii_name="resetCredentialSpec")
    def reset_credential_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialSpec", []))

    @jsii.member(jsii_name="resetSeLinuxContext")
    def reset_se_linux_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeLinuxContext", []))

    @builtins.property
    @jsii.member(jsii_name="credentialSpec")
    def credential_spec(
        self,
    ) -> ServiceTaskSpecContainerSpecPrivilegesCredentialSpecOutputReference:
        return typing.cast(ServiceTaskSpecContainerSpecPrivilegesCredentialSpecOutputReference, jsii.get(self, "credentialSpec"))

    @builtins.property
    @jsii.member(jsii_name="seLinuxContext")
    def se_linux_context(
        self,
    ) -> "ServiceTaskSpecContainerSpecPrivilegesSeLinuxContextOutputReference":
        return typing.cast("ServiceTaskSpecContainerSpecPrivilegesSeLinuxContextOutputReference", jsii.get(self, "seLinuxContext"))

    @builtins.property
    @jsii.member(jsii_name="credentialSpecInput")
    def credential_spec_input(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecPrivilegesCredentialSpec]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecPrivilegesCredentialSpec], jsii.get(self, "credentialSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="seLinuxContextInput")
    def se_linux_context_input(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext"]:
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext"], jsii.get(self, "seLinuxContextInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecContainerSpecPrivileges]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecPrivileges], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecPrivileges],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a97fd985f55cc9aaa5491a3a8160b4abcc7ff24c45e43053c62315904dc0d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext",
    jsii_struct_bases=[],
    name_mapping={
        "disable": "disable",
        "level": "level",
        "role": "role",
        "type": "type",
        "user": "user",
    },
)
class ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext:
    def __init__(
        self,
        *,
        disable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        level: typing.Optional[builtins.str] = None,
        role: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disable: Disable SELinux. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#disable Service#disable}
        :param level: SELinux level label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#level Service#level}
        :param role: SELinux role label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#role Service#role}
        :param type: SELinux type label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#type Service#type}
        :param user: SELinux user label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#user Service#user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679f8fd32dc7bd2bc72abeb0b9b8dc8ce005937a605b5e515cab5522e8738788)
            check_type(argname="argument disable", value=disable, expected_type=type_hints["disable"])
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable is not None:
            self._values["disable"] = disable
        if level is not None:
            self._values["level"] = level
        if role is not None:
            self._values["role"] = role
        if type is not None:
            self._values["type"] = type
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def disable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable SELinux.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#disable Service#disable}
        '''
        result = self._values.get("disable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def level(self) -> typing.Optional[builtins.str]:
        '''SELinux level label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#level Service#level}
        '''
        result = self._values.get("level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''SELinux role label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#role Service#role}
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''SELinux type label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#type Service#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''SELinux user label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#user Service#user}
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecPrivilegesSeLinuxContextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecPrivilegesSeLinuxContextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e82cdac32e9ec4be4cc947799310729c885afd8e86548f322593c777a10174a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisable")
    def reset_disable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisable", []))

    @jsii.member(jsii_name="resetLevel")
    def reset_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevel", []))

    @jsii.member(jsii_name="resetRole")
    def reset_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRole", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUser")
    def reset_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUser", []))

    @builtins.property
    @jsii.member(jsii_name="disableInput")
    def disable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableInput"))

    @builtins.property
    @jsii.member(jsii_name="levelInput")
    def level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "levelInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="disable")
    def disable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disable"))

    @disable.setter
    def disable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02ee5e007df929b1fc696a8c29563e76379a6a03eafad19a866c42b81a3da2f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c64c3cbbe87ede4e3afb409ff41d50e48baea5a7fe1427a9741ffc3ebed575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb8192f500053bdb5d7c3fb2d7f3c6358402dc09d074e1640eceec8dbde5471)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf881990fff1b4682c548158022db7726c440d76f4bb30d3bc24db917523ac61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e37d0a233af42c4020dca4a757c32add2e8fd0c7ce16fad437f80c8ffaf353f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7463e5ebd59a4d7831995b03a9012961c0d784a91582e4213beba4ac9f826651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecSecrets",
    jsii_struct_bases=[],
    name_mapping={
        "file_name": "fileName",
        "secret_id": "secretId",
        "file_gid": "fileGid",
        "file_mode": "fileMode",
        "file_uid": "fileUid",
        "secret_name": "secretName",
    },
)
class ServiceTaskSpecContainerSpecSecrets:
    def __init__(
        self,
        *,
        file_name: builtins.str,
        secret_id: builtins.str,
        file_gid: typing.Optional[builtins.str] = None,
        file_mode: typing.Optional[jsii.Number] = None,
        file_uid: typing.Optional[builtins.str] = None,
        secret_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_name: Represents the final filename in the filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_name Service#file_name}
        :param secret_id: ID of the specific secret that we're referencing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#secret_id Service#secret_id}
        :param file_gid: Represents the file GID. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_gid Service#file_gid}
        :param file_mode: Represents represents the FileMode of the file. Defaults to ``0o444``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_mode Service#file_mode}
        :param file_uid: Represents the file UID. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_uid Service#file_uid}
        :param secret_name: Name of the secret that this references, but this is just provided for lookup/display purposes. The config in the reference will be identified by its ID Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#secret_name Service#secret_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce17d46180321a0e6cfe524aefc26eeacd56b96720ce656bd2029f40287eae85)
            check_type(argname="argument file_name", value=file_name, expected_type=type_hints["file_name"])
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            check_type(argname="argument file_gid", value=file_gid, expected_type=type_hints["file_gid"])
            check_type(argname="argument file_mode", value=file_mode, expected_type=type_hints["file_mode"])
            check_type(argname="argument file_uid", value=file_uid, expected_type=type_hints["file_uid"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_name": file_name,
            "secret_id": secret_id,
        }
        if file_gid is not None:
            self._values["file_gid"] = file_gid
        if file_mode is not None:
            self._values["file_mode"] = file_mode
        if file_uid is not None:
            self._values["file_uid"] = file_uid
        if secret_name is not None:
            self._values["secret_name"] = secret_name

    @builtins.property
    def file_name(self) -> builtins.str:
        '''Represents the final filename in the filesystem.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_name Service#file_name}
        '''
        result = self._values.get("file_name")
        assert result is not None, "Required property 'file_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_id(self) -> builtins.str:
        '''ID of the specific secret that we're referencing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#secret_id Service#secret_id}
        '''
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file_gid(self) -> typing.Optional[builtins.str]:
        '''Represents the file GID. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_gid Service#file_gid}
        '''
        result = self._values.get("file_gid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_mode(self) -> typing.Optional[jsii.Number]:
        '''Represents represents the FileMode of the file. Defaults to ``0o444``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_mode Service#file_mode}
        '''
        result = self._values.get("file_mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def file_uid(self) -> typing.Optional[builtins.str]:
        '''Represents the file UID. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#file_uid Service#file_uid}
        '''
        result = self._values.get("file_uid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_name(self) -> typing.Optional[builtins.str]:
        '''Name of the secret that this references, but this is just provided for lookup/display purposes.

        The config in the reference will be identified by its ID

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#secret_name Service#secret_name}
        '''
        result = self._values.get("secret_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecSecretsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecSecretsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4999e6634b2627a8ffca89f1642eb17abd6a29bd966207fa84bfa565eb58229)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecContainerSpecSecretsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abee2c0e76de261453b4cc5f7fe85e0d760a84f49e8d646dfd779a361b1b53b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecContainerSpecSecretsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09a212cdb74a2e03078d594e6115f2d7d3776c86ad51c351e7eab1a453572fd8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f225880e0adeb6908c9c5c54ef4cc59cc540d0de3308c59111a70d64e4fab22e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb406c510e39ffce3ac4090e89918d9e39279c5a585d7099758f284f448bc96f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecSecrets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecSecrets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecSecrets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5898b27e7eb8e08927683b976d7deeffe7c38d617e2bcb70298a79acf074644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecSecretsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecContainerSpecSecretsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a748b51ea7ed08614f6dbc29c61c9b3c23a4d3eba08f815a0d48b9df2d89199)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFileGid")
    def reset_file_gid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileGid", []))

    @jsii.member(jsii_name="resetFileMode")
    def reset_file_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileMode", []))

    @jsii.member(jsii_name="resetFileUid")
    def reset_file_uid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUid", []))

    @jsii.member(jsii_name="resetSecretName")
    def reset_secret_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretName", []))

    @builtins.property
    @jsii.member(jsii_name="fileGidInput")
    def file_gid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileGidInput"))

    @builtins.property
    @jsii.member(jsii_name="fileModeInput")
    def file_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fileModeInput"))

    @builtins.property
    @jsii.member(jsii_name="fileNameInput")
    def file_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUidInput")
    def file_uid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileUidInput"))

    @builtins.property
    @jsii.member(jsii_name="secretIdInput")
    def secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fileGid")
    def file_gid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileGid"))

    @file_gid.setter
    def file_gid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__058fdfa7dc6e69627c40057c3b5e0233f716c7b657d53743157b3067340bc122)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileGid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileMode")
    def file_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fileMode"))

    @file_mode.setter
    def file_mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa0f4025a90d0d778a7596220ada8d1c4845bb91fda0c7c0803a18206224e506)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileName")
    def file_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileName"))

    @file_name.setter
    def file_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f916e5ea85fa36682d08367e453db04869afbfa7e367ebcb8df56c1390ad132)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUid")
    def file_uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileUid"))

    @file_uid.setter
    def file_uid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c428999f18334943bf7e74072543ddbb80c363c0df0562676610113116ee66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretId"))

    @secret_id.setter
    def secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28f2bbca216e219be16b2cdc2ada00d3a3f89b6e37e35d1b180701da6a3069a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ef3b92ce40f33958a3931f218a5e199d6ab9f05e39055479c6ec73d3d2f7e2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecSecrets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecSecrets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecSecrets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3690ffb5ae16f502d3e5898dfde3909dd0dc8fe70863545012b7fee9873d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecLogDriver",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "options": "options"},
)
class ServiceTaskSpecLogDriver:
    def __init__(
        self,
        *,
        name: builtins.str,
        options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: The logging driver to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#name Service#name}
        :param options: The options for the logging driver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#options Service#options}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5899da6d207b3477d925ccfc72eaa7f8eefbdd2593b1392beca62b6e4ad1ae67)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if options is not None:
            self._values["options"] = options

    @builtins.property
    def name(self) -> builtins.str:
        '''The logging driver to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#name Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def options(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The options for the logging driver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#options Service#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecLogDriver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecLogDriverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecLogDriverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a279093dae66ed6e7180d1573fbf6b6b9c18c3886606d3708b59713e9f632fe3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOptions")
    def reset_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptions", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsInput")
    def options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "optionsInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ced269821c352ecf2e5d1457ff59dcec119bc9fd40d9423c4eac34ce036af3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87600451f88b2a006b5f16f743a212087345c97c5a9742f8f0bb54aade5c5bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecLogDriver]:
        return typing.cast(typing.Optional[ServiceTaskSpecLogDriver], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceTaskSpecLogDriver]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ded61827ecdd383520e2bd101d6c2db67758ed549f7f7dfb8fed3241c26d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecNetworksAdvanced",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "aliases": "aliases", "driver_opts": "driverOpts"},
)
class ServiceTaskSpecNetworksAdvanced:
    def __init__(
        self,
        *,
        name: builtins.str,
        aliases: typing.Optional[typing.Sequence[builtins.str]] = None,
        driver_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: The name/id of the network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#name Service#name}
        :param aliases: The network aliases of the container in the specific network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#aliases Service#aliases}
        :param driver_opts: An array of driver options for the network, e.g. ``opts1=value``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#driver_opts Service#driver_opts}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2625b926e05b0e6827673d21ecbf073b1a23b9b9fe05b42457480bd8d3dc65a8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument aliases", value=aliases, expected_type=type_hints["aliases"])
            check_type(argname="argument driver_opts", value=driver_opts, expected_type=type_hints["driver_opts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if aliases is not None:
            self._values["aliases"] = aliases
        if driver_opts is not None:
            self._values["driver_opts"] = driver_opts

    @builtins.property
    def name(self) -> builtins.str:
        '''The name/id of the network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#name Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aliases(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The network aliases of the container in the specific network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#aliases Service#aliases}
        '''
        result = self._values.get("aliases")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def driver_opts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of driver options for the network, e.g. ``opts1=value``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#driver_opts Service#driver_opts}
        '''
        result = self._values.get("driver_opts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecNetworksAdvanced(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecNetworksAdvancedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecNetworksAdvancedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d61ed422072a6020025c50e77c7d508ddb33767fa5df8679d113386b340d6a31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecNetworksAdvancedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c681d0b95837054f78f9906f133137b86bde271ea42309b5e9726ef5123141)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecNetworksAdvancedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673862ed744db08d377608e246d86e5f9208e8fdd302ddc61a1d59d6804ffe7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33cb71e2bfb77e5d405886db002e255a2c287d2be6125d0273779f47dc661d32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__639a5c4e4a50233dd1da82b88173d055e7404f5dc82b1e7cac47aff4ac99a88d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecNetworksAdvanced]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecNetworksAdvanced]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecNetworksAdvanced]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ec5de1e91a7ce8fa5f0e541afe64d134295cd99ddec7aad5827c882ac0d9b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecNetworksAdvancedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecNetworksAdvancedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39bee5076a3f58fce1d8a312f2e11f94c7376e93bebde4a40d01ad28fc26e32d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAliases")
    def reset_aliases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAliases", []))

    @jsii.member(jsii_name="resetDriverOpts")
    def reset_driver_opts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverOpts", []))

    @builtins.property
    @jsii.member(jsii_name="aliasesInput")
    def aliases_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "aliasesInput"))

    @builtins.property
    @jsii.member(jsii_name="driverOptsInput")
    def driver_opts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "driverOptsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="aliases")
    def aliases(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "aliases"))

    @aliases.setter
    def aliases(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c632f3673e49a56ba849201315b5443cf9bc8e795745e98d035098bcc1c730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aliases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="driverOpts")
    def driver_opts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "driverOpts"))

    @driver_opts.setter
    def driver_opts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c17279942a332a4bf08f68546a9aed65e4075ea6bf212792eb6a3e6120fb95eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverOpts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e36095e7afd06a05c1520cad18bd6a906974b68a5be2ab2c9e2da756aaaa681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecNetworksAdvanced]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecNetworksAdvanced]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecNetworksAdvanced]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20122dc45d9ae6e7d01f95c8c48fcb58a32f005311033ebc5351312ba52c1cd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c817671f974721048b574c51bafbaba88961c39dcb407aab20017b84f11a49e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContainerSpec")
    def put_container_spec(
        self,
        *,
        image: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        dir: typing.Optional[builtins.str] = None,
        dns_config: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecDnsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        healthcheck: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecHealthcheck, typing.Dict[builtins.str, typing.Any]]] = None,
        hostname: typing.Optional[builtins.str] = None,
        hosts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecHosts, typing.Dict[builtins.str, typing.Any]]]]] = None,
        isolation: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
        mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
        privileges: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecPrivileges, typing.Dict[builtins.str, typing.Any]]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecSecrets, typing.Dict[builtins.str, typing.Any]]]]] = None,
        stop_grace_period: typing.Optional[builtins.str] = None,
        stop_signal: typing.Optional[builtins.str] = None,
        sysctl: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image: The image name to use for the containers of the service, like ``nginx:1.17.6``. Also use the data-source or resource of ``docker_image`` with the ``repo_digest`` or ``docker_registry_image`` with the ``name`` attribute for this, as shown in the examples. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#image Service#image}
        :param args: Arguments to the command. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#args Service#args}
        :param command: The command/entrypoint to be run in the image. According to the `docker cli <https://github.com/docker/cli/blob/v20.10.7/cli/command/service/opts.go#L705>`_ the override of the entrypoint is also passed to the ``command`` property and there is no ``entrypoint`` attribute in the ``ContainerSpec`` of the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#command Service#command}
        :param configs: configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#configs Service#configs}
        :param dir: The working directory for commands to run in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#dir Service#dir}
        :param dns_config: dns_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#dns_config Service#dns_config}
        :param env: A list of environment variables in the form VAR="value". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#env Service#env}
        :param groups: A list of additional groups that the container process will run as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#groups Service#groups}
        :param healthcheck: healthcheck block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#healthcheck Service#healthcheck}
        :param hostname: The hostname to use for the container, as a valid RFC 1123 hostname. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#hostname Service#hostname}
        :param hosts: hosts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#hosts Service#hosts}
        :param isolation: Isolation technology of the containers running the service. (Windows only). Defaults to ``default``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#isolation Service#isolation}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#labels Service#labels}
        :param mounts: mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#mounts Service#mounts}
        :param privileges: privileges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#privileges Service#privileges}
        :param read_only: Mount the container's root filesystem as read only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#read_only Service#read_only}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#secrets Service#secrets}
        :param stop_grace_period: Amount of time to wait for the container to terminate before forcefully removing it (ms|s|m|h). If not specified or '0s' the destroy will not check if all tasks/containers of the service terminate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#stop_grace_period Service#stop_grace_period}
        :param stop_signal: Signal to stop the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#stop_signal Service#stop_signal}
        :param sysctl: Sysctls config (Linux only). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#sysctl Service#sysctl}
        :param user: The user inside the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#user Service#user}
        '''
        value = ServiceTaskSpecContainerSpec(
            image=image,
            args=args,
            command=command,
            configs=configs,
            dir=dir,
            dns_config=dns_config,
            env=env,
            groups=groups,
            healthcheck=healthcheck,
            hostname=hostname,
            hosts=hosts,
            isolation=isolation,
            labels=labels,
            mounts=mounts,
            privileges=privileges,
            read_only=read_only,
            secrets=secrets,
            stop_grace_period=stop_grace_period,
            stop_signal=stop_signal,
            sysctl=sysctl,
            user=user,
        )

        return typing.cast(None, jsii.invoke(self, "putContainerSpec", [value]))

    @jsii.member(jsii_name="putLogDriver")
    def put_log_driver(
        self,
        *,
        name: builtins.str,
        options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: The logging driver to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#name Service#name}
        :param options: The options for the logging driver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#options Service#options}
        '''
        value = ServiceTaskSpecLogDriver(name=name, options=options)

        return typing.cast(None, jsii.invoke(self, "putLogDriver", [value]))

    @jsii.member(jsii_name="putNetworksAdvanced")
    def put_networks_advanced(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecNetworksAdvanced, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1552f2bece01fcbaa7e940e7e33d92e76ce3a0f1fa38263023618ac85ce95a92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworksAdvanced", [value]))

    @jsii.member(jsii_name="putPlacement")
    def put_placement(
        self,
        *,
        constraints: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_replicas: typing.Optional[jsii.Number] = None,
        platforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecPlacementPlatforms", typing.Dict[builtins.str, typing.Any]]]]] = None,
        prefs: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param constraints: An array of constraints. e.g.: ``node.role==manager``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#constraints Service#constraints}
        :param max_replicas: Maximum number of replicas for per node (default value is ``0``, which is unlimited). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#max_replicas Service#max_replicas}
        :param platforms: platforms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#platforms Service#platforms}
        :param prefs: Preferences provide a way to make the scheduler aware of factors such as topology. They are provided in order from highest to lowest precedence, e.g.: ``spread=node.role.manager`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#prefs Service#prefs}
        '''
        value = ServiceTaskSpecPlacement(
            constraints=constraints,
            max_replicas=max_replicas,
            platforms=platforms,
            prefs=prefs,
        )

        return typing.cast(None, jsii.invoke(self, "putPlacement", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        *,
        limits: typing.Optional[typing.Union["ServiceTaskSpecResourcesLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        reservation: typing.Optional[typing.Union["ServiceTaskSpecResourcesReservation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#limits Service#limits}
        :param reservation: reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#reservation Service#reservation}
        '''
        value = ServiceTaskSpecResources(limits=limits, reservation=reservation)

        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="putRestartPolicy")
    def put_restart_policy(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        delay: typing.Optional[builtins.str] = None,
        max_attempts: typing.Optional[jsii.Number] = None,
        window: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param condition: Condition for restart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#condition Service#condition}
        :param delay: Delay between restart attempts (ms|s|m|h). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#delay Service#delay}
        :param max_attempts: Maximum attempts to restart a given container before giving up (default value is ``0``, which is ignored). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#max_attempts Service#max_attempts}
        :param window: The time window used to evaluate the restart policy (default value is ``0``, which is unbounded) (ms|s|m|h). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#window Service#window}
        '''
        value = ServiceTaskSpecRestartPolicy(
            condition=condition, delay=delay, max_attempts=max_attempts, window=window
        )

        return typing.cast(None, jsii.invoke(self, "putRestartPolicy", [value]))

    @jsii.member(jsii_name="resetForceUpdate")
    def reset_force_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceUpdate", []))

    @jsii.member(jsii_name="resetLogDriver")
    def reset_log_driver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogDriver", []))

    @jsii.member(jsii_name="resetNetworksAdvanced")
    def reset_networks_advanced(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworksAdvanced", []))

    @jsii.member(jsii_name="resetPlacement")
    def reset_placement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacement", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRestartPolicy")
    def reset_restart_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestartPolicy", []))

    @jsii.member(jsii_name="resetRuntime")
    def reset_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntime", []))

    @builtins.property
    @jsii.member(jsii_name="containerSpec")
    def container_spec(self) -> ServiceTaskSpecContainerSpecOutputReference:
        return typing.cast(ServiceTaskSpecContainerSpecOutputReference, jsii.get(self, "containerSpec"))

    @builtins.property
    @jsii.member(jsii_name="logDriver")
    def log_driver(self) -> ServiceTaskSpecLogDriverOutputReference:
        return typing.cast(ServiceTaskSpecLogDriverOutputReference, jsii.get(self, "logDriver"))

    @builtins.property
    @jsii.member(jsii_name="networksAdvanced")
    def networks_advanced(self) -> ServiceTaskSpecNetworksAdvancedList:
        return typing.cast(ServiceTaskSpecNetworksAdvancedList, jsii.get(self, "networksAdvanced"))

    @builtins.property
    @jsii.member(jsii_name="placement")
    def placement(self) -> "ServiceTaskSpecPlacementOutputReference":
        return typing.cast("ServiceTaskSpecPlacementOutputReference", jsii.get(self, "placement"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> "ServiceTaskSpecResourcesOutputReference":
        return typing.cast("ServiceTaskSpecResourcesOutputReference", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="restartPolicy")
    def restart_policy(self) -> "ServiceTaskSpecRestartPolicyOutputReference":
        return typing.cast("ServiceTaskSpecRestartPolicyOutputReference", jsii.get(self, "restartPolicy"))

    @builtins.property
    @jsii.member(jsii_name="containerSpecInput")
    def container_spec_input(self) -> typing.Optional[ServiceTaskSpecContainerSpec]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpec], jsii.get(self, "containerSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="forceUpdateInput")
    def force_update_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "forceUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="logDriverInput")
    def log_driver_input(self) -> typing.Optional[ServiceTaskSpecLogDriver]:
        return typing.cast(typing.Optional[ServiceTaskSpecLogDriver], jsii.get(self, "logDriverInput"))

    @builtins.property
    @jsii.member(jsii_name="networksAdvancedInput")
    def networks_advanced_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecNetworksAdvanced]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecNetworksAdvanced]]], jsii.get(self, "networksAdvancedInput"))

    @builtins.property
    @jsii.member(jsii_name="placementInput")
    def placement_input(self) -> typing.Optional["ServiceTaskSpecPlacement"]:
        return typing.cast(typing.Optional["ServiceTaskSpecPlacement"], jsii.get(self, "placementInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional["ServiceTaskSpecResources"]:
        return typing.cast(typing.Optional["ServiceTaskSpecResources"], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="restartPolicyInput")
    def restart_policy_input(self) -> typing.Optional["ServiceTaskSpecRestartPolicy"]:
        return typing.cast(typing.Optional["ServiceTaskSpecRestartPolicy"], jsii.get(self, "restartPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="forceUpdate")
    def force_update(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "forceUpdate"))

    @force_update.setter
    def force_update(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba6e8a7157eb61fcd8dd0e162ea4f16199b80e1adda0c12d2f193d0aa4b4fe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c62099b610670d1e9f647fd6adb0ff9328a25ed6e21ec3d035ddbe5a3e55d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpec]:
        return typing.cast(typing.Optional[ServiceTaskSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceTaskSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32739cd18290f7a8356191f4dabbd4a66e8c9598c072d187f9888f8f5721cfc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecPlacement",
    jsii_struct_bases=[],
    name_mapping={
        "constraints": "constraints",
        "max_replicas": "maxReplicas",
        "platforms": "platforms",
        "prefs": "prefs",
    },
)
class ServiceTaskSpecPlacement:
    def __init__(
        self,
        *,
        constraints: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_replicas: typing.Optional[jsii.Number] = None,
        platforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecPlacementPlatforms", typing.Dict[builtins.str, typing.Any]]]]] = None,
        prefs: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param constraints: An array of constraints. e.g.: ``node.role==manager``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#constraints Service#constraints}
        :param max_replicas: Maximum number of replicas for per node (default value is ``0``, which is unlimited). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#max_replicas Service#max_replicas}
        :param platforms: platforms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#platforms Service#platforms}
        :param prefs: Preferences provide a way to make the scheduler aware of factors such as topology. They are provided in order from highest to lowest precedence, e.g.: ``spread=node.role.manager`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#prefs Service#prefs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6249eec5df7bd00a40075f9ce821749520469fd8f55ae0c73e9e8e4d465960b1)
            check_type(argname="argument constraints", value=constraints, expected_type=type_hints["constraints"])
            check_type(argname="argument max_replicas", value=max_replicas, expected_type=type_hints["max_replicas"])
            check_type(argname="argument platforms", value=platforms, expected_type=type_hints["platforms"])
            check_type(argname="argument prefs", value=prefs, expected_type=type_hints["prefs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if constraints is not None:
            self._values["constraints"] = constraints
        if max_replicas is not None:
            self._values["max_replicas"] = max_replicas
        if platforms is not None:
            self._values["platforms"] = platforms
        if prefs is not None:
            self._values["prefs"] = prefs

    @builtins.property
    def constraints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of constraints. e.g.: ``node.role==manager``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#constraints Service#constraints}
        '''
        result = self._values.get("constraints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_replicas(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of replicas for per node (default value is ``0``, which is unlimited).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#max_replicas Service#max_replicas}
        '''
        result = self._values.get("max_replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def platforms(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecPlacementPlatforms"]]]:
        '''platforms block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#platforms Service#platforms}
        '''
        result = self._values.get("platforms")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecPlacementPlatforms"]]], result)

    @builtins.property
    def prefs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Preferences provide a way to make the scheduler aware of factors such as topology.

        They are provided in order from highest to lowest precedence, e.g.: ``spread=node.role.manager``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#prefs Service#prefs}
        '''
        result = self._values.get("prefs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecPlacement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecPlacementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecPlacementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b3214ef0eded0640d5da552a462fec033bf770760f724708f1e0c8eb6bea2de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPlatforms")
    def put_platforms(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecPlacementPlatforms", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433a7653119746aae1857b66af5f2e460c417ffe7456cff8852bb3d88ecd1468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPlatforms", [value]))

    @jsii.member(jsii_name="resetConstraints")
    def reset_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConstraints", []))

    @jsii.member(jsii_name="resetMaxReplicas")
    def reset_max_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxReplicas", []))

    @jsii.member(jsii_name="resetPlatforms")
    def reset_platforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatforms", []))

    @jsii.member(jsii_name="resetPrefs")
    def reset_prefs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefs", []))

    @builtins.property
    @jsii.member(jsii_name="platforms")
    def platforms(self) -> "ServiceTaskSpecPlacementPlatformsList":
        return typing.cast("ServiceTaskSpecPlacementPlatformsList", jsii.get(self, "platforms"))

    @builtins.property
    @jsii.member(jsii_name="constraintsInput")
    def constraints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "constraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicasInput")
    def max_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="platformsInput")
    def platforms_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecPlacementPlatforms"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecPlacementPlatforms"]]], jsii.get(self, "platformsInput"))

    @builtins.property
    @jsii.member(jsii_name="prefsInput")
    def prefs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "prefsInput"))

    @builtins.property
    @jsii.member(jsii_name="constraints")
    def constraints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "constraints"))

    @constraints.setter
    def constraints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506e23e90a24ec65a39c320cfbc05de6d0f8815a17d639920dd94dd83470c45d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "constraints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxReplicas")
    def max_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxReplicas"))

    @max_replicas.setter
    def max_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9360c8966ff074a7ec69576fff09b214ad8a125b74778b7e2a6c7e9791f9e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefs")
    def prefs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "prefs"))

    @prefs.setter
    def prefs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a497d30a26f8f2b933fc21248708df3fa62ca9807181b0b98da61794d356efed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecPlacement]:
        return typing.cast(typing.Optional[ServiceTaskSpecPlacement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceTaskSpecPlacement]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaffb806d3de8cb9329c81ca4799b0998b2351952a32d5e805392d492be3f89e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecPlacementPlatforms",
    jsii_struct_bases=[],
    name_mapping={"architecture": "architecture", "os": "os"},
)
class ServiceTaskSpecPlacementPlatforms:
    def __init__(self, *, architecture: builtins.str, os: builtins.str) -> None:
        '''
        :param architecture: The architecture, e.g. ``amd64``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#architecture Service#architecture}
        :param os: The operation system, e.g. ``linux``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#os Service#os}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__150cf837840d587deaf762c48e3fcefb6904be0c7d0263f19c3b7ae76effb627)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "architecture": architecture,
            "os": os,
        }

    @builtins.property
    def architecture(self) -> builtins.str:
        '''The architecture, e.g. ``amd64``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#architecture Service#architecture}
        '''
        result = self._values.get("architecture")
        assert result is not None, "Required property 'architecture' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def os(self) -> builtins.str:
        '''The operation system, e.g. ``linux``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#os Service#os}
        '''
        result = self._values.get("os")
        assert result is not None, "Required property 'os' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecPlacementPlatforms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecPlacementPlatformsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecPlacementPlatformsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bbf1e5f2bd7fc10cfd6d2d6816f3010bd4f7cfda9d3a55449d1bec0a48c9b8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecPlacementPlatformsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ab3ff96cd51fe645e679434b9dbc1bd278cbb5beaecad3b30de0c541ec911a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecPlacementPlatformsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7d56145119750ed7ed2e05a3cad88544f2804f095287f51749b5b8cdaa9e05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c29d7575fab2549213eb147ea93c8972df8137d3a1d789386c331d59b3c0a75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05dd0bc55072771513e1187eeaba9fefe5791da7f2b976297a0bbb9a186ead8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecPlacementPlatforms]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecPlacementPlatforms]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecPlacementPlatforms]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af4105f0f853a6905807ec70b56d3a3a245e3b543acdd64883a4e7f661b704d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecPlacementPlatformsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecPlacementPlatformsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a394dba2ef7b75a58837bec11cd7fdc4457d42870fa04ab7b5e5f623e5cc941)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="architectureInput")
    def architecture_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architectureInput"))

    @builtins.property
    @jsii.member(jsii_name="osInput")
    def os_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osInput"))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "architecture"))

    @architecture.setter
    def architecture(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d78c48a50a97dc5cd60b4b42b6f0cde088bf96c758ea74289f8ef8335f21bee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architecture", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="os")
    def os(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "os"))

    @os.setter
    def os(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__894e9cca692d71405d7503e1184ad3933f2a5e2c3651ad6751ee65511f10ef15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "os", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecPlacementPlatforms]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecPlacementPlatforms]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecPlacementPlatforms]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e995945efbeb39b7729a4231bf98078dc4751faf68a918886140a49a8cc24f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecResources",
    jsii_struct_bases=[],
    name_mapping={"limits": "limits", "reservation": "reservation"},
)
class ServiceTaskSpecResources:
    def __init__(
        self,
        *,
        limits: typing.Optional[typing.Union["ServiceTaskSpecResourcesLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        reservation: typing.Optional[typing.Union["ServiceTaskSpecResourcesReservation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#limits Service#limits}
        :param reservation: reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#reservation Service#reservation}
        '''
        if isinstance(limits, dict):
            limits = ServiceTaskSpecResourcesLimits(**limits)
        if isinstance(reservation, dict):
            reservation = ServiceTaskSpecResourcesReservation(**reservation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b64d49bbf6fc0561d6dbbb3d20143ce721e689fb33a025175cac6b73319e466)
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument reservation", value=reservation, expected_type=type_hints["reservation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if limits is not None:
            self._values["limits"] = limits
        if reservation is not None:
            self._values["reservation"] = reservation

    @builtins.property
    def limits(self) -> typing.Optional["ServiceTaskSpecResourcesLimits"]:
        '''limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#limits Service#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional["ServiceTaskSpecResourcesLimits"], result)

    @builtins.property
    def reservation(self) -> typing.Optional["ServiceTaskSpecResourcesReservation"]:
        '''reservation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#reservation Service#reservation}
        '''
        result = self._values.get("reservation")
        return typing.cast(typing.Optional["ServiceTaskSpecResourcesReservation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecResourcesLimits",
    jsii_struct_bases=[],
    name_mapping={"memory_bytes": "memoryBytes", "nano_cpus": "nanoCpus"},
)
class ServiceTaskSpecResourcesLimits:
    def __init__(
        self,
        *,
        memory_bytes: typing.Optional[jsii.Number] = None,
        nano_cpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param memory_bytes: The amounf of memory in bytes the container allocates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#memory_bytes Service#memory_bytes}
        :param nano_cpus: CPU shares in units of ``1/1e9`` (or ``10^-9``) of the CPU. Should be at least ``1000000``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#nano_cpus Service#nano_cpus}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a6e21fefdf36f319274e85babb21fee82d14bb06d0aa05e8d6332681ac94133)
            check_type(argname="argument memory_bytes", value=memory_bytes, expected_type=type_hints["memory_bytes"])
            check_type(argname="argument nano_cpus", value=nano_cpus, expected_type=type_hints["nano_cpus"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if memory_bytes is not None:
            self._values["memory_bytes"] = memory_bytes
        if nano_cpus is not None:
            self._values["nano_cpus"] = nano_cpus

    @builtins.property
    def memory_bytes(self) -> typing.Optional[jsii.Number]:
        '''The amounf of memory in bytes the container allocates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#memory_bytes Service#memory_bytes}
        '''
        result = self._values.get("memory_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nano_cpus(self) -> typing.Optional[jsii.Number]:
        '''CPU shares in units of ``1/1e9`` (or ``10^-9``) of the CPU. Should be at least ``1000000``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#nano_cpus Service#nano_cpus}
        '''
        result = self._values.get("nano_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecResourcesLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecResourcesLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecResourcesLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b780274e502dc6e61a5b68cdcdf18e7f172674ea9400cf5dfc29227b3698ec99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMemoryBytes")
    def reset_memory_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryBytes", []))

    @jsii.member(jsii_name="resetNanoCpus")
    def reset_nano_cpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanoCpus", []))

    @builtins.property
    @jsii.member(jsii_name="memoryBytesInput")
    def memory_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanoCpusInput")
    def nano_cpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanoCpusInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryBytes")
    def memory_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryBytes"))

    @memory_bytes.setter
    def memory_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0af6760604a1ac7af85a09b605ddc0832541996908690bc99d6fd47229fc744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanoCpus")
    def nano_cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanoCpus"))

    @nano_cpus.setter
    def nano_cpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1a7284bad138475daa7890838a633b7784fd8f2fe861ddae56c8dfa3965f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanoCpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecResourcesLimits]:
        return typing.cast(typing.Optional[ServiceTaskSpecResourcesLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecResourcesLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ac83851ccd41490ea49b8d306b3e29a4a17ef637df0cb485713e5d75d9cf55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ccc5fe521e9a78994257252276e7ebfcddd2d78465a73c54773f20e97ada1cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLimits")
    def put_limits(
        self,
        *,
        memory_bytes: typing.Optional[jsii.Number] = None,
        nano_cpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param memory_bytes: The amounf of memory in bytes the container allocates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#memory_bytes Service#memory_bytes}
        :param nano_cpus: CPU shares in units of ``1/1e9`` (or ``10^-9``) of the CPU. Should be at least ``1000000``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#nano_cpus Service#nano_cpus}
        '''
        value = ServiceTaskSpecResourcesLimits(
            memory_bytes=memory_bytes, nano_cpus=nano_cpus
        )

        return typing.cast(None, jsii.invoke(self, "putLimits", [value]))

    @jsii.member(jsii_name="putReservation")
    def put_reservation(
        self,
        *,
        generic_resources: typing.Optional[typing.Union["ServiceTaskSpecResourcesReservationGenericResources", typing.Dict[builtins.str, typing.Any]]] = None,
        memory_bytes: typing.Optional[jsii.Number] = None,
        nano_cpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param generic_resources: generic_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#generic_resources Service#generic_resources}
        :param memory_bytes: The amounf of memory in bytes the container allocates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#memory_bytes Service#memory_bytes}
        :param nano_cpus: CPU shares in units of 1/1e9 (or 10^-9) of the CPU. Should be at least ``1000000``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#nano_cpus Service#nano_cpus}
        '''
        value = ServiceTaskSpecResourcesReservation(
            generic_resources=generic_resources,
            memory_bytes=memory_bytes,
            nano_cpus=nano_cpus,
        )

        return typing.cast(None, jsii.invoke(self, "putReservation", [value]))

    @jsii.member(jsii_name="resetLimits")
    def reset_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimits", []))

    @jsii.member(jsii_name="resetReservation")
    def reset_reservation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservation", []))

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(self) -> ServiceTaskSpecResourcesLimitsOutputReference:
        return typing.cast(ServiceTaskSpecResourcesLimitsOutputReference, jsii.get(self, "limits"))

    @builtins.property
    @jsii.member(jsii_name="reservation")
    def reservation(self) -> "ServiceTaskSpecResourcesReservationOutputReference":
        return typing.cast("ServiceTaskSpecResourcesReservationOutputReference", jsii.get(self, "reservation"))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(self) -> typing.Optional[ServiceTaskSpecResourcesLimits]:
        return typing.cast(typing.Optional[ServiceTaskSpecResourcesLimits], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationInput")
    def reservation_input(
        self,
    ) -> typing.Optional["ServiceTaskSpecResourcesReservation"]:
        return typing.cast(typing.Optional["ServiceTaskSpecResourcesReservation"], jsii.get(self, "reservationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecResources]:
        return typing.cast(typing.Optional[ServiceTaskSpecResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceTaskSpecResources]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43329c45ad92fa2d0a01b1a6c467c831cdb40d254c5f2819159752571a1b1ec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecResourcesReservation",
    jsii_struct_bases=[],
    name_mapping={
        "generic_resources": "genericResources",
        "memory_bytes": "memoryBytes",
        "nano_cpus": "nanoCpus",
    },
)
class ServiceTaskSpecResourcesReservation:
    def __init__(
        self,
        *,
        generic_resources: typing.Optional[typing.Union["ServiceTaskSpecResourcesReservationGenericResources", typing.Dict[builtins.str, typing.Any]]] = None,
        memory_bytes: typing.Optional[jsii.Number] = None,
        nano_cpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param generic_resources: generic_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#generic_resources Service#generic_resources}
        :param memory_bytes: The amounf of memory in bytes the container allocates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#memory_bytes Service#memory_bytes}
        :param nano_cpus: CPU shares in units of 1/1e9 (or 10^-9) of the CPU. Should be at least ``1000000``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#nano_cpus Service#nano_cpus}
        '''
        if isinstance(generic_resources, dict):
            generic_resources = ServiceTaskSpecResourcesReservationGenericResources(**generic_resources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5487bd3c63afcbbd53d9fa8fd485eda1545d9120c640ca767a19edfd304f493)
            check_type(argname="argument generic_resources", value=generic_resources, expected_type=type_hints["generic_resources"])
            check_type(argname="argument memory_bytes", value=memory_bytes, expected_type=type_hints["memory_bytes"])
            check_type(argname="argument nano_cpus", value=nano_cpus, expected_type=type_hints["nano_cpus"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if generic_resources is not None:
            self._values["generic_resources"] = generic_resources
        if memory_bytes is not None:
            self._values["memory_bytes"] = memory_bytes
        if nano_cpus is not None:
            self._values["nano_cpus"] = nano_cpus

    @builtins.property
    def generic_resources(
        self,
    ) -> typing.Optional["ServiceTaskSpecResourcesReservationGenericResources"]:
        '''generic_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#generic_resources Service#generic_resources}
        '''
        result = self._values.get("generic_resources")
        return typing.cast(typing.Optional["ServiceTaskSpecResourcesReservationGenericResources"], result)

    @builtins.property
    def memory_bytes(self) -> typing.Optional[jsii.Number]:
        '''The amounf of memory in bytes the container allocates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#memory_bytes Service#memory_bytes}
        '''
        result = self._values.get("memory_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nano_cpus(self) -> typing.Optional[jsii.Number]:
        '''CPU shares in units of 1/1e9 (or 10^-9) of the CPU. Should be at least ``1000000``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#nano_cpus Service#nano_cpus}
        '''
        result = self._values.get("nano_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecResourcesReservation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecResourcesReservationGenericResources",
    jsii_struct_bases=[],
    name_mapping={
        "discrete_resources_spec": "discreteResourcesSpec",
        "named_resources_spec": "namedResourcesSpec",
    },
)
class ServiceTaskSpecResourcesReservationGenericResources:
    def __init__(
        self,
        *,
        discrete_resources_spec: typing.Optional[typing.Sequence[builtins.str]] = None,
        named_resources_spec: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param discrete_resources_spec: The Integer resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#discrete_resources_spec Service#discrete_resources_spec}
        :param named_resources_spec: The String resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#named_resources_spec Service#named_resources_spec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d26e9c32125eae16020fcc1ed6da646de1bd10b9a8d878c78f970811292c02b2)
            check_type(argname="argument discrete_resources_spec", value=discrete_resources_spec, expected_type=type_hints["discrete_resources_spec"])
            check_type(argname="argument named_resources_spec", value=named_resources_spec, expected_type=type_hints["named_resources_spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if discrete_resources_spec is not None:
            self._values["discrete_resources_spec"] = discrete_resources_spec
        if named_resources_spec is not None:
            self._values["named_resources_spec"] = named_resources_spec

    @builtins.property
    def discrete_resources_spec(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Integer resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#discrete_resources_spec Service#discrete_resources_spec}
        '''
        result = self._values.get("discrete_resources_spec")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def named_resources_spec(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The String resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#named_resources_spec Service#named_resources_spec}
        '''
        result = self._values.get("named_resources_spec")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecResourcesReservationGenericResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecResourcesReservationGenericResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecResourcesReservationGenericResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a839c59a1da2ca0775e2acd587d26de2e5a1d1b951be100cc3ccae050b4b9b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiscreteResourcesSpec")
    def reset_discrete_resources_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiscreteResourcesSpec", []))

    @jsii.member(jsii_name="resetNamedResourcesSpec")
    def reset_named_resources_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamedResourcesSpec", []))

    @builtins.property
    @jsii.member(jsii_name="discreteResourcesSpecInput")
    def discrete_resources_spec_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "discreteResourcesSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="namedResourcesSpecInput")
    def named_resources_spec_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "namedResourcesSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="discreteResourcesSpec")
    def discrete_resources_spec(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "discreteResourcesSpec"))

    @discrete_resources_spec.setter
    def discrete_resources_spec(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__411db19d41f9747d7a1b296b83c6d49f61aa5998af829eec2a2db273fec1a512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "discreteResourcesSpec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namedResourcesSpec")
    def named_resources_spec(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "namedResourcesSpec"))

    @named_resources_spec.setter
    def named_resources_spec(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f76f4bba92a369be497245bcd52b6b0569bcf4f47ce6264918ec4a7444cfbaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namedResourcesSpec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceTaskSpecResourcesReservationGenericResources]:
        return typing.cast(typing.Optional[ServiceTaskSpecResourcesReservationGenericResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecResourcesReservationGenericResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__219eb14dcc863b2901f8f2dbf07223495b88a24d9cf22fe8df072dc8f13f36d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecResourcesReservationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecResourcesReservationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ff64b2773d1b9b3d2bcf340f0916b0592b8c53d29d6231a5732c8ed5e91bc2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGenericResources")
    def put_generic_resources(
        self,
        *,
        discrete_resources_spec: typing.Optional[typing.Sequence[builtins.str]] = None,
        named_resources_spec: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param discrete_resources_spec: The Integer resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#discrete_resources_spec Service#discrete_resources_spec}
        :param named_resources_spec: The String resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#named_resources_spec Service#named_resources_spec}
        '''
        value = ServiceTaskSpecResourcesReservationGenericResources(
            discrete_resources_spec=discrete_resources_spec,
            named_resources_spec=named_resources_spec,
        )

        return typing.cast(None, jsii.invoke(self, "putGenericResources", [value]))

    @jsii.member(jsii_name="resetGenericResources")
    def reset_generic_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenericResources", []))

    @jsii.member(jsii_name="resetMemoryBytes")
    def reset_memory_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryBytes", []))

    @jsii.member(jsii_name="resetNanoCpus")
    def reset_nano_cpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanoCpus", []))

    @builtins.property
    @jsii.member(jsii_name="genericResources")
    def generic_resources(
        self,
    ) -> ServiceTaskSpecResourcesReservationGenericResourcesOutputReference:
        return typing.cast(ServiceTaskSpecResourcesReservationGenericResourcesOutputReference, jsii.get(self, "genericResources"))

    @builtins.property
    @jsii.member(jsii_name="genericResourcesInput")
    def generic_resources_input(
        self,
    ) -> typing.Optional[ServiceTaskSpecResourcesReservationGenericResources]:
        return typing.cast(typing.Optional[ServiceTaskSpecResourcesReservationGenericResources], jsii.get(self, "genericResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryBytesInput")
    def memory_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanoCpusInput")
    def nano_cpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanoCpusInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryBytes")
    def memory_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryBytes"))

    @memory_bytes.setter
    def memory_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__027eba975101f8ac4a83e4acb4de8deb1030d5466805dc9a3116d78a0fd2c56a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanoCpus")
    def nano_cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanoCpus"))

    @nano_cpus.setter
    def nano_cpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b9f625deea047bcf41aec0d608634148ef9c56c2bb57f839d2ae8758507c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanoCpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecResourcesReservation]:
        return typing.cast(typing.Optional[ServiceTaskSpecResourcesReservation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecResourcesReservation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc42c9aa8ea537215a5a677f38c1443f0dad16cebaf04292cc528d8312ce6a56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecRestartPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "condition": "condition",
        "delay": "delay",
        "max_attempts": "maxAttempts",
        "window": "window",
    },
)
class ServiceTaskSpecRestartPolicy:
    def __init__(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        delay: typing.Optional[builtins.str] = None,
        max_attempts: typing.Optional[jsii.Number] = None,
        window: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param condition: Condition for restart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#condition Service#condition}
        :param delay: Delay between restart attempts (ms|s|m|h). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#delay Service#delay}
        :param max_attempts: Maximum attempts to restart a given container before giving up (default value is ``0``, which is ignored). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#max_attempts Service#max_attempts}
        :param window: The time window used to evaluate the restart policy (default value is ``0``, which is unbounded) (ms|s|m|h). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#window Service#window}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80de2a4eaf36f87c243b94af4fe179b1655cf23044e8e233570954d96fab41c7)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument delay", value=delay, expected_type=type_hints["delay"])
            check_type(argname="argument max_attempts", value=max_attempts, expected_type=type_hints["max_attempts"])
            check_type(argname="argument window", value=window, expected_type=type_hints["window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if condition is not None:
            self._values["condition"] = condition
        if delay is not None:
            self._values["delay"] = delay
        if max_attempts is not None:
            self._values["max_attempts"] = max_attempts
        if window is not None:
            self._values["window"] = window

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''Condition for restart.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#condition Service#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delay(self) -> typing.Optional[builtins.str]:
        '''Delay between restart attempts (ms|s|m|h).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#delay Service#delay}
        '''
        result = self._values.get("delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_attempts(self) -> typing.Optional[jsii.Number]:
        '''Maximum attempts to restart a given container before giving up (default value is ``0``, which is ignored).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#max_attempts Service#max_attempts}
        '''
        result = self._values.get("max_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def window(self) -> typing.Optional[builtins.str]:
        '''The time window used to evaluate the restart policy (default value is ``0``, which is unbounded) (ms|s|m|h).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#window Service#window}
        '''
        result = self._values.get("window")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecRestartPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecRestartPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceTaskSpecRestartPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5707772be0bc8e5547ee67d534d09e4f53184d1ea581c9884767cc453eada657)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDelay")
    def reset_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelay", []))

    @jsii.member(jsii_name="resetMaxAttempts")
    def reset_max_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAttempts", []))

    @jsii.member(jsii_name="resetWindow")
    def reset_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindow", []))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="delayInput")
    def delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delayInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAttemptsInput")
    def max_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="windowInput")
    def window_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "windowInput"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @condition.setter
    def condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6d607f32ed9c3ecf9e8cc58da19ba2846f2c1977b5dd2e07f4ce8e42e14d472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delay")
    def delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delay"))

    @delay.setter
    def delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4179eda3e812d847f44d73050332d8260ce60227ce45a6c3cca1b690bf23a9e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAttempts")
    def max_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAttempts"))

    @max_attempts.setter
    def max_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8bd505538ad79477c7ec796c5d294f5fc63807c4ace3698cc600a5edc97eb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="window")
    def window(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "window"))

    @window.setter
    def window(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ddb66bb86d6361e47d763f0abb9a0af957311f1a4364755a65fa405e97d0bba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "window", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecRestartPolicy]:
        return typing.cast(typing.Optional[ServiceTaskSpecRestartPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecRestartPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c361892cbde24aa69ad6fca86760a5acaa21134949b0954a20c333d551d5c5ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.service.ServiceUpdateConfig",
    jsii_struct_bases=[],
    name_mapping={
        "delay": "delay",
        "failure_action": "failureAction",
        "max_failure_ratio": "maxFailureRatio",
        "monitor": "monitor",
        "order": "order",
        "parallelism": "parallelism",
    },
)
class ServiceUpdateConfig:
    def __init__(
        self,
        *,
        delay: typing.Optional[builtins.str] = None,
        failure_action: typing.Optional[builtins.str] = None,
        max_failure_ratio: typing.Optional[builtins.str] = None,
        monitor: typing.Optional[builtins.str] = None,
        order: typing.Optional[builtins.str] = None,
        parallelism: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delay: Delay between task updates ``(ns|us|ms|s|m|h)``. Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#delay Service#delay}
        :param failure_action: Action on update failure: ``pause``, ``continue`` or ``rollback``. Defaults to ``pause``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#failure_action Service#failure_action}
        :param max_failure_ratio: Failure rate to tolerate during an update. Defaults to ``0.0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#max_failure_ratio Service#max_failure_ratio}
        :param monitor: Duration after each task update to monitor for failure (ns|us|ms|s|m|h). Defaults to ``5s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#monitor Service#monitor}
        :param order: Update order: either 'stop-first' or 'start-first'. Defaults to ``stop-first``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#order Service#order}
        :param parallelism: Maximum number of tasks to be updated in one iteration. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#parallelism Service#parallelism}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3c5a1ad148d216530609661d273964493af57c026faf188eed0348f130116c)
            check_type(argname="argument delay", value=delay, expected_type=type_hints["delay"])
            check_type(argname="argument failure_action", value=failure_action, expected_type=type_hints["failure_action"])
            check_type(argname="argument max_failure_ratio", value=max_failure_ratio, expected_type=type_hints["max_failure_ratio"])
            check_type(argname="argument monitor", value=monitor, expected_type=type_hints["monitor"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument parallelism", value=parallelism, expected_type=type_hints["parallelism"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delay is not None:
            self._values["delay"] = delay
        if failure_action is not None:
            self._values["failure_action"] = failure_action
        if max_failure_ratio is not None:
            self._values["max_failure_ratio"] = max_failure_ratio
        if monitor is not None:
            self._values["monitor"] = monitor
        if order is not None:
            self._values["order"] = order
        if parallelism is not None:
            self._values["parallelism"] = parallelism

    @builtins.property
    def delay(self) -> typing.Optional[builtins.str]:
        '''Delay between task updates ``(ns|us|ms|s|m|h)``. Defaults to ``0s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#delay Service#delay}
        '''
        result = self._values.get("delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_action(self) -> typing.Optional[builtins.str]:
        '''Action on update failure: ``pause``, ``continue`` or ``rollback``. Defaults to ``pause``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#failure_action Service#failure_action}
        '''
        result = self._values.get("failure_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_failure_ratio(self) -> typing.Optional[builtins.str]:
        '''Failure rate to tolerate during an update. Defaults to ``0.0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#max_failure_ratio Service#max_failure_ratio}
        '''
        result = self._values.get("max_failure_ratio")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor(self) -> typing.Optional[builtins.str]:
        '''Duration after each task update to monitor for failure (ns|us|ms|s|m|h). Defaults to ``5s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#monitor Service#monitor}
        '''
        result = self._values.get("monitor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def order(self) -> typing.Optional[builtins.str]:
        '''Update order: either 'stop-first' or 'start-first'. Defaults to ``stop-first``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#order Service#order}
        '''
        result = self._values.get("order")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parallelism(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of tasks to be updated in one iteration. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/service#parallelism Service#parallelism}
        '''
        result = self._values.get("parallelism")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUpdateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUpdateConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.service.ServiceUpdateConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44fcebe1fd49fefdbf509b4283dcd2bfd69191a504834c9f1b70d5c8f13b9661)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDelay")
    def reset_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelay", []))

    @jsii.member(jsii_name="resetFailureAction")
    def reset_failure_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureAction", []))

    @jsii.member(jsii_name="resetMaxFailureRatio")
    def reset_max_failure_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFailureRatio", []))

    @jsii.member(jsii_name="resetMonitor")
    def reset_monitor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitor", []))

    @jsii.member(jsii_name="resetOrder")
    def reset_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrder", []))

    @jsii.member(jsii_name="resetParallelism")
    def reset_parallelism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelism", []))

    @builtins.property
    @jsii.member(jsii_name="delayInput")
    def delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delayInput"))

    @builtins.property
    @jsii.member(jsii_name="failureActionInput")
    def failure_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "failureActionInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFailureRatioInput")
    def max_failure_ratio_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxFailureRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorInput")
    def monitor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitorInput"))

    @builtins.property
    @jsii.member(jsii_name="orderInput")
    def order_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orderInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelismInput")
    def parallelism_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelismInput"))

    @builtins.property
    @jsii.member(jsii_name="delay")
    def delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delay"))

    @delay.setter
    def delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__899b5289d943895fe9cf87a3afe22fdee40b4458420f0593ebff90314b05c5f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failureAction")
    def failure_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failureAction"))

    @failure_action.setter
    def failure_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6b27c1c43cd91e66162c22ff6176fcc5ea764d01b3ad2457b2fec3fd9ebb31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFailureRatio")
    def max_failure_ratio(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxFailureRatio"))

    @max_failure_ratio.setter
    def max_failure_ratio(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__601309d0291b306d05f87433759a2731f13d80e2ee1fff31713c2b467b7a322b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFailureRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitor")
    def monitor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitor"))

    @monitor.setter
    def monitor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90695a119f47ec0498bc944581d3ca835af9aa674b56e48b69daed9479eb817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "order"))

    @order.setter
    def order(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2239f6cef97a86f4a949b9b7e7b4d854bf480cc3402f24dec2c02743375338b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelism")
    def parallelism(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelism"))

    @parallelism.setter
    def parallelism(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3e926d5b263c3672cf8a28866a9756b8f2d6bb2526c611e1fb7743ce4a63cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelism", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceUpdateConfig]:
        return typing.cast(typing.Optional[ServiceUpdateConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceUpdateConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d71879479d78bb5b59c9661b0bf539d0a8d486ddab943b3cf19520e2b2b0c23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Service",
    "ServiceAuth",
    "ServiceAuthOutputReference",
    "ServiceConfig",
    "ServiceConvergeConfig",
    "ServiceConvergeConfigOutputReference",
    "ServiceEndpointSpec",
    "ServiceEndpointSpecOutputReference",
    "ServiceEndpointSpecPorts",
    "ServiceEndpointSpecPortsList",
    "ServiceEndpointSpecPortsOutputReference",
    "ServiceLabels",
    "ServiceLabelsList",
    "ServiceLabelsOutputReference",
    "ServiceMode",
    "ServiceModeOutputReference",
    "ServiceModeReplicated",
    "ServiceModeReplicatedOutputReference",
    "ServiceRollbackConfig",
    "ServiceRollbackConfigOutputReference",
    "ServiceTaskSpec",
    "ServiceTaskSpecContainerSpec",
    "ServiceTaskSpecContainerSpecConfigs",
    "ServiceTaskSpecContainerSpecConfigsList",
    "ServiceTaskSpecContainerSpecConfigsOutputReference",
    "ServiceTaskSpecContainerSpecDnsConfig",
    "ServiceTaskSpecContainerSpecDnsConfigOutputReference",
    "ServiceTaskSpecContainerSpecHealthcheck",
    "ServiceTaskSpecContainerSpecHealthcheckOutputReference",
    "ServiceTaskSpecContainerSpecHosts",
    "ServiceTaskSpecContainerSpecHostsList",
    "ServiceTaskSpecContainerSpecHostsOutputReference",
    "ServiceTaskSpecContainerSpecLabels",
    "ServiceTaskSpecContainerSpecLabelsList",
    "ServiceTaskSpecContainerSpecLabelsOutputReference",
    "ServiceTaskSpecContainerSpecMounts",
    "ServiceTaskSpecContainerSpecMountsBindOptions",
    "ServiceTaskSpecContainerSpecMountsBindOptionsOutputReference",
    "ServiceTaskSpecContainerSpecMountsList",
    "ServiceTaskSpecContainerSpecMountsOutputReference",
    "ServiceTaskSpecContainerSpecMountsTmpfsOptions",
    "ServiceTaskSpecContainerSpecMountsTmpfsOptionsOutputReference",
    "ServiceTaskSpecContainerSpecMountsVolumeOptions",
    "ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels",
    "ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsList",
    "ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsOutputReference",
    "ServiceTaskSpecContainerSpecMountsVolumeOptionsOutputReference",
    "ServiceTaskSpecContainerSpecOutputReference",
    "ServiceTaskSpecContainerSpecPrivileges",
    "ServiceTaskSpecContainerSpecPrivilegesCredentialSpec",
    "ServiceTaskSpecContainerSpecPrivilegesCredentialSpecOutputReference",
    "ServiceTaskSpecContainerSpecPrivilegesOutputReference",
    "ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext",
    "ServiceTaskSpecContainerSpecPrivilegesSeLinuxContextOutputReference",
    "ServiceTaskSpecContainerSpecSecrets",
    "ServiceTaskSpecContainerSpecSecretsList",
    "ServiceTaskSpecContainerSpecSecretsOutputReference",
    "ServiceTaskSpecLogDriver",
    "ServiceTaskSpecLogDriverOutputReference",
    "ServiceTaskSpecNetworksAdvanced",
    "ServiceTaskSpecNetworksAdvancedList",
    "ServiceTaskSpecNetworksAdvancedOutputReference",
    "ServiceTaskSpecOutputReference",
    "ServiceTaskSpecPlacement",
    "ServiceTaskSpecPlacementOutputReference",
    "ServiceTaskSpecPlacementPlatforms",
    "ServiceTaskSpecPlacementPlatformsList",
    "ServiceTaskSpecPlacementPlatformsOutputReference",
    "ServiceTaskSpecResources",
    "ServiceTaskSpecResourcesLimits",
    "ServiceTaskSpecResourcesLimitsOutputReference",
    "ServiceTaskSpecResourcesOutputReference",
    "ServiceTaskSpecResourcesReservation",
    "ServiceTaskSpecResourcesReservationGenericResources",
    "ServiceTaskSpecResourcesReservationGenericResourcesOutputReference",
    "ServiceTaskSpecResourcesReservationOutputReference",
    "ServiceTaskSpecRestartPolicy",
    "ServiceTaskSpecRestartPolicyOutputReference",
    "ServiceUpdateConfig",
    "ServiceUpdateConfigOutputReference",
]

publication.publish()

def _typecheckingstub__b578b738121d0d131ca664c81d01a1c614a67dfc3771bd097f9a04c6eaa23027(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    task_spec: typing.Union[ServiceTaskSpec, typing.Dict[builtins.str, typing.Any]],
    auth: typing.Optional[typing.Union[ServiceAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    converge_config: typing.Optional[typing.Union[ServiceConvergeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_spec: typing.Optional[typing.Union[ServiceEndpointSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mode: typing.Optional[typing.Union[ServiceMode, typing.Dict[builtins.str, typing.Any]]] = None,
    rollback_config: typing.Optional[typing.Union[ServiceRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    update_config: typing.Optional[typing.Union[ServiceUpdateConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8a1b868124027ebaea59f0924cd442c63b6e7a6a68de848b298feac5e67342db(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794a9a60cbdfb184d2f2ec181d4261d7d4ba798a60598c1ae850fe4fb92390f9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b17101c3f55066c22c7874cc6478b6e67b22f8a45e7a87f7cf444a57f8d261(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3e6ce206a7caa168ed74d7c08af8b2f76dcb1eed7c039b85b04a0a5b31973a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449ee43c79aec9507a4b0db7e9a54562c9d367689e82a9ef738d88114cb1a89f(
    *,
    server_address: builtins.str,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5990411f641325b4a5eddd6194b63b4b0a36335c7abefdcfc527751d8f142973(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45b05e09fc0af4c35229ba6e4e9c146bc214efacb33c58539dbe8a92fee66f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262ae1eabd20f5aed9642495042afc7e5ec8b8cf87fdbf035fa7f3383fdc3f7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982938f18f80273e9d00ba765c31feb473d47a249f1f056a7728368847aceea8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__284119e61dd2c7ead3992ea0d1473596af147efe258636ec5e4b98d2e2770e8c(
    value: typing.Optional[ServiceAuth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ac0581c52512733a058c0c43949366de729de771427abde71054d4096ba745(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    task_spec: typing.Union[ServiceTaskSpec, typing.Dict[builtins.str, typing.Any]],
    auth: typing.Optional[typing.Union[ServiceAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    converge_config: typing.Optional[typing.Union[ServiceConvergeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_spec: typing.Optional[typing.Union[ServiceEndpointSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mode: typing.Optional[typing.Union[ServiceMode, typing.Dict[builtins.str, typing.Any]]] = None,
    rollback_config: typing.Optional[typing.Union[ServiceRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    update_config: typing.Optional[typing.Union[ServiceUpdateConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e702b821534297ef5c9ae2900e2d91b52ad07bec13938fd5374ddb81be218a73(
    *,
    delay: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe28dd50c249e22562cbeda3830c357ca9918512920001a8d20224f091074c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a62faee6040ce3765651f8d3097d2d13d420268cb1526c3ffc3c3726ffff7a5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca838a1ab0beeb648a10f7ab1dc36ec40e1c10e5715735af2025f3df04c83622(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1abd31438a5e50e58103e9fdcc5f0eeae14698e09bd5bc3532488ec1576bebc1(
    value: typing.Optional[ServiceConvergeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a535aa7cdeb3ea7073f6ceddf77fc61ab666ef066d02d9f6f9c132d1118332(
    *,
    mode: typing.Optional[builtins.str] = None,
    ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEndpointSpecPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff883ef1e699adb53cab87b2fd20e2b8349d61bcba707fb4d3b36e92f8cc5feb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687c21a1a6fec04388f3205ea1b655f3d7303c49b8ebe9df37da8e10a46c48aa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEndpointSpecPorts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bbcdce74fbaa0b99f81b1e024e42bc5fc6b6a9493a1b276321ab9492e95f567(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e4a5abac15086d71c6d80c137340eefbf9beb90d17e6f2c9af15ffc3ec7f90(
    value: typing.Optional[ServiceEndpointSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff206b236a332926277d52336b42c140cc8d480d22e1b057924e2a3375047163(
    *,
    target_port: jsii.Number,
    name: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    published_port: typing.Optional[jsii.Number] = None,
    publish_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1776557f8620ffa819777cfa19b96b2ad0519fa605b1366de4ed3c8dc9bf71a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300bdac5f5730d08f3888e23675c69c61380a0de7db49a27d997f98ea8119f27(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b5b4a0ff5c2fdaff6a92ac836f458772524e677d01bdcad466edaffe415666(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c97c1befbb9f415b349a7d47ac420c0cd72696ae1669d3d8064da065097e924(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f8dc17c302396859c625f579e1e59b7ce528229da3d6b2ca61bc981d486b937(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8779a37aa5ffd8758167de5bdefc4701766ae8a45853528776fea49e776fd9ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEndpointSpecPorts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6554c48602194129f8b21d8bfa43db319c8740d4e46e245dda40d6d3b2f498ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__526ebc150c907c47bfbeaa8084fc8dd3e56f4fcb40a02e14c6479ae24a37d635(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d834f0343cd96f0e48ccdb095bf708227f1a9d103bf60cf5cd3aa13abd7049e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b6a32b5d8b8140f37b4c785718d6ea7d313343a14ecc4807d8fc228052a3c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb22aa54bc954a6d565573a7dd04d2c2b7e8bdfebaea0fcdb69436ca527a57e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8821d86ff370669bfb936aafb76ddfda19f1dd5f5caeb36b36dcb3a9840d1a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deffba0de2a6eafd61429e22d73c096547e1f34bef9f64f96cfe8ae5b8ee8ec1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEndpointSpecPorts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7431e3715e35d4e41c2c33fdef85584e6bd568615438cc95cc19cc27869c065b(
    *,
    label: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd6d9cd879004a8b84d3c7090bdf9ecb2b1e8acfef679fb829268de7d5f2198b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12a8a227e7e7aeef6f92645ccc55faa14539d26248935c820202d8b7ffe2dc1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0120b53c465eb894aa4d0d745e705ccd16eb3a7986b0ddc399bd9a94c781dd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d598ea7be3540cacd4745006311b5e8b519d62a488c6e9566453bce921be6be5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f740c3c76e936f3eb526698f1bf10aa4e63c1179659f14c10cf6beee92377d75(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f86bd1043a36f333bbe8d420a19ef9979be092e159eb7fd924822fe00dac66a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75740118b86f3529c78ea31f359871cabad9ff8c00b14d601abfdaae620ece3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af058d03512930b1274fd18f5c2565fab5560d47ede9a35455676f9641bc78d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf7654ede4acf02f5c0d291d41831311a6935aac8df2349ef7061bb10c3d4f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c7fe14c15ceb38939b4b9973a46c579f5a01ee006eb08608a68d9a75f18e5c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc13d1d41ba3985ad35923f85284c699a0192a39ef17489cc6c42b10d58785d(
    *,
    global_: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replicated: typing.Optional[typing.Union[ServiceModeReplicated, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bbf1ef51925a579d2af227b03b37b98c95a7b1617525fda5a119b8633e75f5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af312b85881b08a33cd94c9843ace183c10454ff093096868fe17fbd8a4396a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d569204fad96cad648219a43d93ce919f2759989f9023ac3626e9577664331f(
    value: typing.Optional[ServiceMode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9a9bbc2b07fd7c7f5e6373ba717dedd887536dc00c3c3207499d06bf0a307d5(
    *,
    replicas: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6449048ab9a7b9790fe38436b8527cbd8dcb0b679760a9774cfe007e625a00b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91fbde77a2ed3d2b5fc333f261b266c610ae966a816b4bd9f942a4e1538b6a9c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a770297c94225d8c2e200343ae22e3800fd91512588c32c9fd4432c4dd231e(
    value: typing.Optional[ServiceModeReplicated],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b2842ef70e286197c22523be5070c923d8177fae135db50b5f29a06397e228(
    *,
    delay: typing.Optional[builtins.str] = None,
    failure_action: typing.Optional[builtins.str] = None,
    max_failure_ratio: typing.Optional[builtins.str] = None,
    monitor: typing.Optional[builtins.str] = None,
    order: typing.Optional[builtins.str] = None,
    parallelism: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d38b918a1aeaa4d6dbe7cf27d437abbc00b4f17a5b52c8aeb09a1b68fe1c4128(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecee4d66675559b59f3a858c7aad85c380202f672c0e0199a2977b6564b6f910(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b3892ac7d1cbacea3c844a6ebabd977ce8b25c327917ae17ceb3f02faf3525(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__952c12ff387b42be1b71c83d511a4c02c51b35894481fe06e4151a63b155ffdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150c329aed5888faaa59781f52865e6c177c3b23e5970910d509767aca98dee2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5029f76df3901d3691949e3029663be5d5866881f0918f7ceb183c3dacf27dcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4140351b9a99f41ffc6e7a8d89cd6d4bd2030b4aefe1a64daff15137d49c4d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec7eb086999c9dfb7b9c7826e79c107ded82415feb548221b3cdcb30d72655b(
    value: typing.Optional[ServiceRollbackConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a557151ba96da7ec1a3904f39bdb2aa832d5f01689a1432cc8cabfd971386ae(
    *,
    container_spec: typing.Union[ServiceTaskSpecContainerSpec, typing.Dict[builtins.str, typing.Any]],
    force_update: typing.Optional[jsii.Number] = None,
    log_driver: typing.Optional[typing.Union[ServiceTaskSpecLogDriver, typing.Dict[builtins.str, typing.Any]]] = None,
    networks_advanced: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecNetworksAdvanced, typing.Dict[builtins.str, typing.Any]]]]] = None,
    placement: typing.Optional[typing.Union[ServiceTaskSpecPlacement, typing.Dict[builtins.str, typing.Any]]] = None,
    resources: typing.Optional[typing.Union[ServiceTaskSpecResources, typing.Dict[builtins.str, typing.Any]]] = None,
    restart_policy: typing.Optional[typing.Union[ServiceTaskSpecRestartPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12811eebe80f327add12f713dfbcfe19ddb3188056fdd789914881c60506712c(
    *,
    image: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dir: typing.Optional[builtins.str] = None,
    dns_config: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecDnsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    healthcheck: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecHealthcheck, typing.Dict[builtins.str, typing.Any]]] = None,
    hostname: typing.Optional[builtins.str] = None,
    hosts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecHosts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    isolation: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    privileges: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecPrivileges, typing.Dict[builtins.str, typing.Any]]] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecSecrets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stop_grace_period: typing.Optional[builtins.str] = None,
    stop_signal: typing.Optional[builtins.str] = None,
    sysctl: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524d2e87218a7ae3b97508f6a0d691ddedfe599300410bd56a01ab894d6495a0(
    *,
    config_id: builtins.str,
    file_name: builtins.str,
    config_name: typing.Optional[builtins.str] = None,
    file_gid: typing.Optional[builtins.str] = None,
    file_mode: typing.Optional[jsii.Number] = None,
    file_uid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ff3283615ff64c7307894cd31fa4068ba42c6d25347a02a29bd240cba2c225(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d356a4f8988331ea33f010c67f5b74a39981d8aea94c6a52833c4db84d14964f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344362c98d935b9e78bd402c157e558e1d840dd764da015f864ab5074277295a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56045433a181f6b60642dd0b38681f08775e0d41a8fb2f22c2bfb695db236cf7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907d1fc2b52d1380b949fe3a77752cf17167458719c6b3d6d23569e244d49c9e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d3c5b9a2b9413140e1c49e3021b2c67baac76ee14f2bf3d8e983b95fc6f7a5f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea6162716e97a303af4559f6881044a0effd240f753688f725ab7153b096e84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__863652747b49f3b5fd3f89057dd0f2d03e6cb1eeeb3c3c6f0aef03ce539ec395(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae10865658b0ea5756050d94e2b8477639a7077daf79d477c7d8f4873009893c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9751c5c20b651272c6e1264f602d740b1186de45c0edf0f93e029907ca5dd44c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b6519551fed21be49348185d8b5aaed8048af81b5888abfadac7ebc7cb915d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a86c841a07e552b1ccbc672e64dd053a4aed3cce048f5df1e5802cd7118f755(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__781258c22c4a1555c21e9a6f9e27d1056b0ed70de9b8a4f21d257ab4de105d2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd9a74237def2e3e196402a2a5ad1f55fc8026ba31c255ddcc346a6b17a2ac4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc919fa7a74ce1c894169d02e9e1739ef63f562f9f127747c15205a9830413e(
    *,
    nameservers: typing.Sequence[builtins.str],
    options: typing.Optional[typing.Sequence[builtins.str]] = None,
    search: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adeca96c9befea02284d88027188378a2a677ad00f00153bc57fa3de56f80cf2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf5d6fcfba77ea4c0f41bb8f62d315ef3043bfc4f876e5800d2194168a3a0e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872de710ddfa248550d19810d96ac78dd5737fb3ba140a832ddb5f20574de555(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888240db7eb5f6aa8247994eb99fb5c5e22d6fb16ccae45670f81871cc8048af(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__febccc1933b13afb269578856684b916c108550dfe4a3cfc320f796383880cdd(
    value: typing.Optional[ServiceTaskSpecContainerSpecDnsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45521d61f6e1a9852714161336045126afa373cb7221fd7ff9987536d5ad24f(
    *,
    test: typing.Sequence[builtins.str],
    interval: typing.Optional[builtins.str] = None,
    retries: typing.Optional[jsii.Number] = None,
    start_period: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ad7d98c4fb41f8916d0e048589be2fe7fe64fe9f0d74bb666ff64f57d5127f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db936880f880ac4e1d1254933bb432ed147a397ebe964ae52b00a28cbd949538(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c287aa9c27448d4c1d6d9cc086573cb5d34d96e7a2d720a99d7fec86e3c28978(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7201e3806786b19cfd2029b7776173784ec9568b1d1b5c6ee32c112518d0a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ac18750f263ab339938439d70e27f672ffefb0c72754c9e077b491931e764f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f5c97e0a6d52fdf8ec9d385081a418db9974e8b837c5c0b4f087f683985836(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d19bc8a0dca6f1f0c7d2d7f751cdbfb9e8349858ea4c5a9cc24d4ad70b9ab62(
    value: typing.Optional[ServiceTaskSpecContainerSpecHealthcheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ecca4df29cdebfcd58f083ec1a56a9418ed746e5de6e5ff1c7fec67455a70e(
    *,
    host: builtins.str,
    ip: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5aafca96e45acbcf08cf1b81613650c393a988ac986cc857b197d4e29f6669c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__817d0e2df4139f603ed52a1f88fbee2ed2425e7834f7079085806f746dc73fb4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f1ea3eebd614a4b3370b9e5b04205f1c2ba7c007bd7e1bf793073e4f1047b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3994004ee7411dd50693adcecc03b808ca4fcca37cf2c6954576cc7f4eb3e1c4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d860e7686063ab91d63b2d81379ae983ffa5d28771167499648ed9fd8b18c819(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2befc994619217e9b862f791c3d5f7794713fc8dc25016e35746033c259e6ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecHosts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89fc523d8f9117beac7cdcacef2e091269db6b0fb42c78ba3af22fc7fd4dbf0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c93322c57698fb9f6dc7a7f66032643344b446e8787107d83d71f6640628ec0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f23ae663b165ca55124002de1fbcbedfd4dcb3d7c952236b5e0f1acd73687f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43eb159a744ad5f3e7a62ae88a53ecb8b9af7bdaf77a5fde4e87b0c39c1d722c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecHosts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab178bc59eb13d2a1b4af3c98513b2c5bc6623690187241562fd6a5cc9cd0007(
    *,
    label: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0340b88a7f9b84e19d8f37660b50e3991759ddafbad5c8b73b01c95108148146(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b5a76dc63c9783aef6da692f65380338bb78b5557d09aa727d77e2e2382939(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4794dbf56e00b8ceed5aa198f95a5668117265e37fbeeab37e737cd4ba5451cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd6459f154951bcab82820a50acd86bc0c6272cd77b99a01c0e400b22d2bd9e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53717a0dce739858b2a446969baaf6bf4b8c3e67d91669804676cc2a38f61e88(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ef207a0c607125cc2db1f6d6de1dbdeb5ea193f99575c5e0d14efc46bde0d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbf30cc84c985d0733bcfba913afbbebcb2570c4f586816faeb3c5b6ba0a71f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bce6b961a53fd7a934aaff4b4fc1b16c9110b1b80cdf25e393b888da5d0c51a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66946ad2a06719da0cbd956a76c273da66441b35085f951a9d1aff0224e84902(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aa0807427c680ed4b3e8d2445e67f689e77d5d0e2d1d2f727e16ec8bcf4f387(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c5a4cfe63778a7eea46a5665601cf87d6964416399edd27098ac1f02c50ab5(
    *,
    target: builtins.str,
    type: builtins.str,
    bind_options: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecMountsBindOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source: typing.Optional[builtins.str] = None,
    tmpfs_options: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecMountsTmpfsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_options: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecMountsVolumeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c9a1c46ed1f95bcbed414e91df9af8035af74134edbd9ad247bf3c864d0abf(
    *,
    propagation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4f2918fb86790743be059ab9e74bac7937fe260c90a3dafa29cefec14fcf79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9346817ac45d0e3f96dbbe9140512aa290675553054bf83df92561cfea1b164(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3549a3f917f825b1bbf1b5c8103ad465830cf71ce4e9a98fde9cf46ba2459dba(
    value: typing.Optional[ServiceTaskSpecContainerSpecMountsBindOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__473b5aec5c5e85999d9e021f3ba67a830f25ae908c2ba211c711ef04af2d8ae4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485349789f479470cd0ebd426497012286987263c9f135917f1c738e800723a6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf833195e4e97c34c51d5ad54e3972e1d29cd3120b0b815a316600b999db4582(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__569fc547400da5fb24b2e5efb7eac6ae0d3c6eb5a45c597f5a61fea3df66e8fa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86dc8c7622ec19568ea5c31287a619876a8ed9dd6f8181eff1e71bfb36aeda99(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74eab88802085219f2259bc0029c82500f68f4a8ed6e50809c8fc9e0f52ed93d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b6ee1c900e4c078bd2e13081317367d600ffc9f95bf52332ea1d691b179d936(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3036d810beca7c8266cd3a8fd3fe36e26d020f2982c9f583794cd149ff450251(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d82ff0728723759c5a36519360f11e30c129342d25e9e6ede77f9cdbbe7261(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8100bc6cb4911291f74a01bb1debb8068d7a8548f43896cb645da2314d105e9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85951caf314e8887acb6205accf11295e9fe5532e35c462c4bfb20a428ddf44f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9878115bcb2a616ff8f1223dc9352acfc48d8a4a7220a4882763ff08b5e3be8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9802d31fde4769212339a34dfb45067f5a2fb459b6969836709421f63e55c336(
    *,
    mode: typing.Optional[jsii.Number] = None,
    size_bytes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16784edad679558e1e0db2ff00af4d1cf1dac2dad55a6e4e56c158fd52e3df0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341797b101e6733b5baf87a44d54b5e7e585269eae3fb7b197796925dc86947a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9beab2c4c09307b2d7454bca4fb822a786232ba3a0ae6ae001ea268d6912ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532552dca12144e62b0cb7f30457e12cdca826b056d048f0e0a9d524a84673ff(
    value: typing.Optional[ServiceTaskSpecContainerSpecMountsTmpfsOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07e201271d489babf0eb6a88649e8971529078c3b485fb561155fa8ef5edbf7(
    *,
    driver_name: typing.Optional[builtins.str] = None,
    driver_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    no_copy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb001381fbb74b7dea09cf341fbc61803e166e2bbf972bbdbecf652a165bdf9(
    *,
    label: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d398467d62d18dcae946908254c716a5b60b8da60c438133e60f0cdbe8f1f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__093530a64132701433106c01b342fc0c6400586b881bda960f33474d27fc7773(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6df1d95b023771b68ad863ca806b78ec2302dc45885e5f11bd6cbad20061707(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39fbf4f9c70e7a0145841bf9eb13503866f40f64871da2bf25f8448a4943840c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae14ea0325b9c528af59d39b9834687bb444e1367af8b8bfdb28830ea4adf46(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72fd3a78d1987a27c907f653445469f8596216374a18001b657b8bd35a9f844d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2436e5dc28f38038561e50d0e38c68f3e22ffa5a23e17147097fba6f438870b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96b75425fac010d2a7237f5f54b223de94060840819cadf23166377058e9c2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99cdd3e3d3ef36b31e716d8a2b283413e717c07fec3a1237475e281225197c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e9868b3a69e56a040fe8f7c5b86c2a693267ea4a9be460a8acb639f631d78e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5cd9f0663f792853fd5540378db2721cb32092ebc1df95ec42f88d8da93e3e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094680f784e61e08a34e825738cebeb470e1c08520ff75dbbdf40ebf376f3690(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdca8e458654fb86552e678804ecb7fe81a6d8ac85a3ee79d5aea6277f34df9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd63967ee84b043aa2761910fd516faa1b0f6c70e222f956e6b2a71153aa49b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3501d7bfc7ccce86a9c93cadbbc407a05253181483a2759bcea22d0a24967ca1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3050853b89dc61d4632d05ca351da136bb5edeb373dad34d11bfac4ecdb75062(
    value: typing.Optional[ServiceTaskSpecContainerSpecMountsVolumeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7758d64b6ea74df05d9a73c61bc575d0f659f2ed6f8905b25bd89cd322ac44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f771f6ea81e0e0f305737daaaae2d2be623f4b0d0dfcab70c288f0a6adf08a5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6666432ee8de9d86ffc705e37a37cb2526791497ac8bd22bebc8c537ab4431e7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecHosts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd4be99a14c2b58c696e5a7dcd4620941e155ee7d038e03bec76035596b8f4b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66f6a6ea25ed8a3e93721752d05858e9ae0cdf25deff13e15c8e3a05a3f5869(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecMounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037539875ffd244f8992fd33b63e8c9969dcb4d91b672ba9cbc6da2ea2f6b08d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecSecrets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b06743054378c1b4d9619e3b56ab20270ff2ee507d51e6a752849eb78f1618(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574fc9087a66aa7863e8a8b6871be1e6a6648df780b07302557737bbb0c9bfa8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50904468bc1178e848b01687a67a71fe147ad47ce061f89d3d4d6836ae8f40af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172c254ef42edd8ae749b15c228ca3be428736e73d13fa2dc4ad782eb4e4807a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1708cc2d73587c925341cbe531c0343869ecbbfa44e8a3dae2f7b3f2a7ce0b0c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5860437b988259018896776c8b5cc253358fd68fcc4d6e6c599d3ffeab0125f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd98bbc601d7a9f7ffda5d679a157afcc04e40d8e571c8fa604ed806a51e5dc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e771ae9675414bb7fcfb264ed7a7aa4922647457e79b8bf3dbdf32b6978a792(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db205e04c7321564c2433e3db97895d0f78775a4b00449dbe88dc43dc6caa03f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288d6879163c1693d85e373c3b7ee21111e80e331e5997d9181a275dbe77a0d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdcf9dfb1a990d3e7f078d7cb05a0a33deee1c635a5f5470b99c00c2186f18c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6cedd300f5a80db128f75a2645d08b8426395f29ebd38f46d20c16f02fe7dd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6bc356585cdccd2f0d801ddd2fe0589f1665d28db4c57083fa8e23d2c33f8dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23adb8156d0a7dbfc558d7d5a8e3c15a0dab3ca93cef0b5fd40223452bc97fb(
    value: typing.Optional[ServiceTaskSpecContainerSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8f9f2b44701d4af985becb8caa455efa459005a2be56d26f462e957e8432dd(
    *,
    credential_spec: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecPrivilegesCredentialSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    se_linux_context: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb94d118dd724f3a0c2830c93a3f9a939f458c645f6c989bd2a794acfec5dff6(
    *,
    file: typing.Optional[builtins.str] = None,
    registry: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf0f610c65c480942b922b4560dd71ba97c3190374220dc8665fca8336bab77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1bd7bd9dac88ad2706004a212594b5f81ca22b8047f134bfb0f2d1c9e19842(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d07474977275208aa5488eee0283ea55a5cb43ad3ca680feaf7ee7ae0dab389(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82ee3ae5b793d4b47330b03e3e9582736be5ea0e5a75ee4ad600470de43360b(
    value: typing.Optional[ServiceTaskSpecContainerSpecPrivilegesCredentialSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e310dd103b1be8738da2ac6ed668b9d86033e57a8005d710c00a3e055a784524(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a97fd985f55cc9aaa5491a3a8160b4abcc7ff24c45e43053c62315904dc0d9(
    value: typing.Optional[ServiceTaskSpecContainerSpecPrivileges],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679f8fd32dc7bd2bc72abeb0b9b8dc8ce005937a605b5e515cab5522e8738788(
    *,
    disable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    level: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82cdac32e9ec4be4cc947799310729c885afd8e86548f322593c777a10174a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ee5e007df929b1fc696a8c29563e76379a6a03eafad19a866c42b81a3da2f8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c64c3cbbe87ede4e3afb409ff41d50e48baea5a7fe1427a9741ffc3ebed575(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb8192f500053bdb5d7c3fb2d7f3c6358402dc09d074e1640eceec8dbde5471(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf881990fff1b4682c548158022db7726c440d76f4bb30d3bc24db917523ac61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e37d0a233af42c4020dca4a757c32add2e8fd0c7ce16fad437f80c8ffaf353f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7463e5ebd59a4d7831995b03a9012961c0d784a91582e4213beba4ac9f826651(
    value: typing.Optional[ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce17d46180321a0e6cfe524aefc26eeacd56b96720ce656bd2029f40287eae85(
    *,
    file_name: builtins.str,
    secret_id: builtins.str,
    file_gid: typing.Optional[builtins.str] = None,
    file_mode: typing.Optional[jsii.Number] = None,
    file_uid: typing.Optional[builtins.str] = None,
    secret_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4999e6634b2627a8ffca89f1642eb17abd6a29bd966207fa84bfa565eb58229(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abee2c0e76de261453b4cc5f7fe85e0d760a84f49e8d646dfd779a361b1b53b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a212cdb74a2e03078d594e6115f2d7d3776c86ad51c351e7eab1a453572fd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f225880e0adeb6908c9c5c54ef4cc59cc540d0de3308c59111a70d64e4fab22e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb406c510e39ffce3ac4090e89918d9e39279c5a585d7099758f284f448bc96f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5898b27e7eb8e08927683b976d7deeffe7c38d617e2bcb70298a79acf074644(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecSecrets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a748b51ea7ed08614f6dbc29c61c9b3c23a4d3eba08f815a0d48b9df2d89199(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__058fdfa7dc6e69627c40057c3b5e0233f716c7b657d53743157b3067340bc122(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0f4025a90d0d778a7596220ada8d1c4845bb91fda0c7c0803a18206224e506(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f916e5ea85fa36682d08367e453db04869afbfa7e367ebcb8df56c1390ad132(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c428999f18334943bf7e74072543ddbb80c363c0df0562676610113116ee66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28f2bbca216e219be16b2cdc2ada00d3a3f89b6e37e35d1b180701da6a3069a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef3b92ce40f33958a3931f218a5e199d6ab9f05e39055479c6ec73d3d2f7e2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3690ffb5ae16f502d3e5898dfde3909dd0dc8fe70863545012b7fee9873d5e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecSecrets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5899da6d207b3477d925ccfc72eaa7f8eefbdd2593b1392beca62b6e4ad1ae67(
    *,
    name: builtins.str,
    options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a279093dae66ed6e7180d1573fbf6b6b9c18c3886606d3708b59713e9f632fe3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ced269821c352ecf2e5d1457ff59dcec119bc9fd40d9423c4eac34ce036af3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87600451f88b2a006b5f16f743a212087345c97c5a9742f8f0bb54aade5c5bf(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ded61827ecdd383520e2bd101d6c2db67758ed549f7f7dfb8fed3241c26d0d(
    value: typing.Optional[ServiceTaskSpecLogDriver],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2625b926e05b0e6827673d21ecbf073b1a23b9b9fe05b42457480bd8d3dc65a8(
    *,
    name: builtins.str,
    aliases: typing.Optional[typing.Sequence[builtins.str]] = None,
    driver_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61ed422072a6020025c50e77c7d508ddb33767fa5df8679d113386b340d6a31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c681d0b95837054f78f9906f133137b86bde271ea42309b5e9726ef5123141(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673862ed744db08d377608e246d86e5f9208e8fdd302ddc61a1d59d6804ffe7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33cb71e2bfb77e5d405886db002e255a2c287d2be6125d0273779f47dc661d32(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639a5c4e4a50233dd1da82b88173d055e7404f5dc82b1e7cac47aff4ac99a88d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec5de1e91a7ce8fa5f0e541afe64d134295cd99ddec7aad5827c882ac0d9b40(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecNetworksAdvanced]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39bee5076a3f58fce1d8a312f2e11f94c7376e93bebde4a40d01ad28fc26e32d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c632f3673e49a56ba849201315b5443cf9bc8e795745e98d035098bcc1c730(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17279942a332a4bf08f68546a9aed65e4075ea6bf212792eb6a3e6120fb95eb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e36095e7afd06a05c1520cad18bd6a906974b68a5be2ab2c9e2da756aaaa681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20122dc45d9ae6e7d01f95c8c48fcb58a32f005311033ebc5351312ba52c1cd1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecNetworksAdvanced]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c817671f974721048b574c51bafbaba88961c39dcb407aab20017b84f11a49e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1552f2bece01fcbaa7e940e7e33d92e76ce3a0f1fa38263023618ac85ce95a92(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecNetworksAdvanced, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba6e8a7157eb61fcd8dd0e162ea4f16199b80e1adda0c12d2f193d0aa4b4fe4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c62099b610670d1e9f647fd6adb0ff9328a25ed6e21ec3d035ddbe5a3e55d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32739cd18290f7a8356191f4dabbd4a66e8c9598c072d187f9888f8f5721cfc7(
    value: typing.Optional[ServiceTaskSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6249eec5df7bd00a40075f9ce821749520469fd8f55ae0c73e9e8e4d465960b1(
    *,
    constraints: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_replicas: typing.Optional[jsii.Number] = None,
    platforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecPlacementPlatforms, typing.Dict[builtins.str, typing.Any]]]]] = None,
    prefs: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3214ef0eded0640d5da552a462fec033bf770760f724708f1e0c8eb6bea2de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433a7653119746aae1857b66af5f2e460c417ffe7456cff8852bb3d88ecd1468(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecPlacementPlatforms, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506e23e90a24ec65a39c320cfbc05de6d0f8815a17d639920dd94dd83470c45d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9360c8966ff074a7ec69576fff09b214ad8a125b74778b7e2a6c7e9791f9e3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a497d30a26f8f2b933fc21248708df3fa62ca9807181b0b98da61794d356efed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaffb806d3de8cb9329c81ca4799b0998b2351952a32d5e805392d492be3f89e(
    value: typing.Optional[ServiceTaskSpecPlacement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150cf837840d587deaf762c48e3fcefb6904be0c7d0263f19c3b7ae76effb627(
    *,
    architecture: builtins.str,
    os: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbf1e5f2bd7fc10cfd6d2d6816f3010bd4f7cfda9d3a55449d1bec0a48c9b8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ab3ff96cd51fe645e679434b9dbc1bd278cbb5beaecad3b30de0c541ec911a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7d56145119750ed7ed2e05a3cad88544f2804f095287f51749b5b8cdaa9e05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c29d7575fab2549213eb147ea93c8972df8137d3a1d789386c331d59b3c0a75(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05dd0bc55072771513e1187eeaba9fefe5791da7f2b976297a0bbb9a186ead8c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af4105f0f853a6905807ec70b56d3a3a245e3b543acdd64883a4e7f661b704d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecPlacementPlatforms]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a394dba2ef7b75a58837bec11cd7fdc4457d42870fa04ab7b5e5f623e5cc941(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d78c48a50a97dc5cd60b4b42b6f0cde088bf96c758ea74289f8ef8335f21bee9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894e9cca692d71405d7503e1184ad3933f2a5e2c3651ad6751ee65511f10ef15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e995945efbeb39b7729a4231bf98078dc4751faf68a918886140a49a8cc24f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecPlacementPlatforms]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b64d49bbf6fc0561d6dbbb3d20143ce721e689fb33a025175cac6b73319e466(
    *,
    limits: typing.Optional[typing.Union[ServiceTaskSpecResourcesLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    reservation: typing.Optional[typing.Union[ServiceTaskSpecResourcesReservation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6e21fefdf36f319274e85babb21fee82d14bb06d0aa05e8d6332681ac94133(
    *,
    memory_bytes: typing.Optional[jsii.Number] = None,
    nano_cpus: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b780274e502dc6e61a5b68cdcdf18e7f172674ea9400cf5dfc29227b3698ec99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0af6760604a1ac7af85a09b605ddc0832541996908690bc99d6fd47229fc744(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1a7284bad138475daa7890838a633b7784fd8f2fe861ddae56c8dfa3965f54(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ac83851ccd41490ea49b8d306b3e29a4a17ef637df0cb485713e5d75d9cf55(
    value: typing.Optional[ServiceTaskSpecResourcesLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ccc5fe521e9a78994257252276e7ebfcddd2d78465a73c54773f20e97ada1cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43329c45ad92fa2d0a01b1a6c467c831cdb40d254c5f2819159752571a1b1ec1(
    value: typing.Optional[ServiceTaskSpecResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5487bd3c63afcbbd53d9fa8fd485eda1545d9120c640ca767a19edfd304f493(
    *,
    generic_resources: typing.Optional[typing.Union[ServiceTaskSpecResourcesReservationGenericResources, typing.Dict[builtins.str, typing.Any]]] = None,
    memory_bytes: typing.Optional[jsii.Number] = None,
    nano_cpus: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d26e9c32125eae16020fcc1ed6da646de1bd10b9a8d878c78f970811292c02b2(
    *,
    discrete_resources_spec: typing.Optional[typing.Sequence[builtins.str]] = None,
    named_resources_spec: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a839c59a1da2ca0775e2acd587d26de2e5a1d1b951be100cc3ccae050b4b9b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411db19d41f9747d7a1b296b83c6d49f61aa5998af829eec2a2db273fec1a512(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f76f4bba92a369be497245bcd52b6b0569bcf4f47ce6264918ec4a7444cfbaa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219eb14dcc863b2901f8f2dbf07223495b88a24d9cf22fe8df072dc8f13f36d7(
    value: typing.Optional[ServiceTaskSpecResourcesReservationGenericResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff64b2773d1b9b3d2bcf340f0916b0592b8c53d29d6231a5732c8ed5e91bc2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__027eba975101f8ac4a83e4acb4de8deb1030d5466805dc9a3116d78a0fd2c56a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b9f625deea047bcf41aec0d608634148ef9c56c2bb57f839d2ae8758507c79(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc42c9aa8ea537215a5a677f38c1443f0dad16cebaf04292cc528d8312ce6a56(
    value: typing.Optional[ServiceTaskSpecResourcesReservation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80de2a4eaf36f87c243b94af4fe179b1655cf23044e8e233570954d96fab41c7(
    *,
    condition: typing.Optional[builtins.str] = None,
    delay: typing.Optional[builtins.str] = None,
    max_attempts: typing.Optional[jsii.Number] = None,
    window: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5707772be0bc8e5547ee67d534d09e4f53184d1ea581c9884767cc453eada657(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d607f32ed9c3ecf9e8cc58da19ba2846f2c1977b5dd2e07f4ce8e42e14d472(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4179eda3e812d847f44d73050332d8260ce60227ce45a6c3cca1b690bf23a9e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8bd505538ad79477c7ec796c5d294f5fc63807c4ace3698cc600a5edc97eb2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ddb66bb86d6361e47d763f0abb9a0af957311f1a4364755a65fa405e97d0bba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c361892cbde24aa69ad6fca86760a5acaa21134949b0954a20c333d551d5c5ff(
    value: typing.Optional[ServiceTaskSpecRestartPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3c5a1ad148d216530609661d273964493af57c026faf188eed0348f130116c(
    *,
    delay: typing.Optional[builtins.str] = None,
    failure_action: typing.Optional[builtins.str] = None,
    max_failure_ratio: typing.Optional[builtins.str] = None,
    monitor: typing.Optional[builtins.str] = None,
    order: typing.Optional[builtins.str] = None,
    parallelism: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44fcebe1fd49fefdbf509b4283dcd2bfd69191a504834c9f1b70d5c8f13b9661(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899b5289d943895fe9cf87a3afe22fdee40b4458420f0593ebff90314b05c5f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6b27c1c43cd91e66162c22ff6176fcc5ea764d01b3ad2457b2fec3fd9ebb31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601309d0291b306d05f87433759a2731f13d80e2ee1fff31713c2b467b7a322b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90695a119f47ec0498bc944581d3ca835af9aa674b56e48b69daed9479eb817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2239f6cef97a86f4a949b9b7e7b4d854bf480cc3402f24dec2c02743375338b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3e926d5b263c3672cf8a28866a9756b8f2d6bb2526c611e1fb7743ce4a63cb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d71879479d78bb5b59c9661b0bf539d0a8d486ddab943b3cf19520e2b2b0c23(
    value: typing.Optional[ServiceUpdateConfig],
) -> None:
    """Type checking stubs"""
    pass

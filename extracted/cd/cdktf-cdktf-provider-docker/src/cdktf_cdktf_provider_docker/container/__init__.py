r'''
# `docker_container`

Refer to the Terraform Registry for docs: [`docker_container`](https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container).
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


class Container(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.Container",
):
    '''Represents a {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container docker_container}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        image: builtins.str,
        name: builtins.str,
        attach: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        capabilities: typing.Optional[typing.Union["ContainerCapabilities", typing.Dict[builtins.str, typing.Any]]] = None,
        cgroupns_mode: typing.Optional[builtins.str] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_read_refresh_timeout_milliseconds: typing.Optional[jsii.Number] = None,
        cpus: typing.Optional[builtins.str] = None,
        cpu_set: typing.Optional[builtins.str] = None,
        cpu_shares: typing.Optional[jsii.Number] = None,
        destroy_grace_seconds: typing.Optional[jsii.Number] = None,
        devices: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerDevices", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_search: typing.Optional[typing.Sequence[builtins.str]] = None,
        domainname: typing.Optional[builtins.str] = None,
        entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Sequence[builtins.str]] = None,
        gpus: typing.Optional[builtins.str] = None,
        group_add: typing.Optional[typing.Sequence[builtins.str]] = None,
        healthcheck: typing.Optional[typing.Union["ContainerHealthcheck", typing.Dict[builtins.str, typing.Any]]] = None,
        host: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerHost", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hostname: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        init: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ipc_mode: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        log_driver: typing.Optional[builtins.str] = None,
        log_opts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_retry_count: typing.Optional[jsii.Number] = None,
        memory: typing.Optional[jsii.Number] = None,
        memory_swap: typing.Optional[jsii.Number] = None,
        mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        must_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_mode: typing.Optional[builtins.str] = None,
        networks_advanced: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNetworksAdvanced", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pid_mode: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        privileged: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        publish_all_ports: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remove_volumes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restart: typing.Optional[builtins.str] = None,
        rm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        runtime: typing.Optional[builtins.str] = None,
        security_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
        shm_size: typing.Optional[jsii.Number] = None,
        start: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        stdin_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        stop_signal: typing.Optional[builtins.str] = None,
        stop_timeout: typing.Optional[jsii.Number] = None,
        storage_opts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        sysctls: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tmpfs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ulimit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerUlimit", typing.Dict[builtins.str, typing.Any]]]]] = None,
        upload: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerUpload", typing.Dict[builtins.str, typing.Any]]]]] = None,
        user: typing.Optional[builtins.str] = None,
        userns_mode: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        wait: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        wait_timeout: typing.Optional[jsii.Number] = None,
        working_dir: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container docker_container} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param image: The ID of the image to back this container. The easiest way to get this value is to use the ``image_id`` attribute of the ``docker_image`` resource as is shown in the example. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#image Container#image}
        :param name: The name of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#name Container#name}
        :param attach: If ``true`` attach to the container after its creation and waits the end of its execution. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#attach Container#attach}
        :param capabilities: capabilities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#capabilities Container#capabilities}
        :param cgroupns_mode: Cgroup namespace mode to use for the container. Possible values are: ``private``, ``host``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#cgroupns_mode Container#cgroupns_mode}
        :param command: The command to use to start the container. For example, to run ``/usr/bin/myprogram -f baz.conf`` set the command to be ``["/usr/bin/myprogram","-f","baz.conf"]``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#command Container#command}
        :param container_read_refresh_timeout_milliseconds: The total number of milliseconds to wait for the container to reach status 'running'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#container_read_refresh_timeout_milliseconds Container#container_read_refresh_timeout_milliseconds}
        :param cpus: Specify how much of the available CPU resources a container can use. e.g a value of 1.5 means the container is guaranteed at most one and a half of the CPUs Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#cpus Container#cpus}
        :param cpu_set: A comma-separated list or hyphen-separated range of CPUs a container can use, e.g. ``0-1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#cpu_set Container#cpu_set}
        :param cpu_shares: CPU shares (relative weight) for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#cpu_shares Container#cpu_shares}
        :param destroy_grace_seconds: If defined will attempt to stop the container before destroying. Container will be destroyed after ``n`` seconds or on successful stop. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#destroy_grace_seconds Container#destroy_grace_seconds}
        :param devices: devices block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#devices Container#devices}
        :param dns: DNS servers to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#dns Container#dns}
        :param dns_opts: DNS options used by the DNS provider(s), see ``resolv.conf`` documentation for valid list of options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#dns_opts Container#dns_opts}
        :param dns_search: DNS search domains that are used when bare unqualified hostnames are used inside of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#dns_search Container#dns_search}
        :param domainname: Domain name of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#domainname Container#domainname}
        :param entrypoint: The command to use as the Entrypoint for the container. The Entrypoint allows you to configure a container to run as an executable. For example, to run ``/usr/bin/myprogram`` when starting a container, set the entrypoint to be ``"/usr/bin/myprogram"]``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#entrypoint Container#entrypoint}
        :param env: Environment variables to set in the form of ``KEY=VALUE``, e.g. ``DEBUG=0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#env Container#env}
        :param gpus: GPU devices to add to the container. Currently, only the value ``all`` is supported. Passing any other value will result in unexpected behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#gpus Container#gpus}
        :param group_add: Additional groups for the container user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#group_add Container#group_add}
        :param healthcheck: healthcheck block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#healthcheck Container#healthcheck}
        :param host: host block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#host Container#host}
        :param hostname: Hostname of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#hostname Container#hostname}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#id Container#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param init: Configured whether an init process should be injected for this container. If unset this will default to the ``dockerd`` defaults. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#init Container#init}
        :param ipc_mode: IPC sharing mode for the container. Possible values are: ``none``, ``private``, ``shareable``, ``container:<name|id>`` or ``host``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ipc_mode Container#ipc_mode}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#labels Container#labels}
        :param log_driver: The logging driver to use for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#log_driver Container#log_driver}
        :param log_opts: Key/value pairs to use as options for the logging driver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#log_opts Container#log_opts}
        :param logs: Save the container logs (``attach`` must be enabled). Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#logs Container#logs}
        :param max_retry_count: The maximum amount of times to an attempt a restart when ``restart`` is set to 'on-failure'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#max_retry_count Container#max_retry_count}
        :param memory: The memory limit for the container in MBs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#memory Container#memory}
        :param memory_swap: The total memory limit (memory + swap) for the container in MBs. This setting may compute to ``-1`` after ``terraform apply`` if the target host doesn't support memory swap, when that is the case docker will use a soft limitation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#memory_swap Container#memory_swap}
        :param mounts: mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#mounts Container#mounts}
        :param must_run: If ``true``, then the Docker container will be kept running. If ``false``, then as long as the container exists, Terraform assumes it is successful. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#must_run Container#must_run}
        :param network_mode: Network mode of the container. See https://docs.docker.com/engine/network/ for more information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#network_mode Container#network_mode}
        :param networks_advanced: networks_advanced block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#networks_advanced Container#networks_advanced}
        :param pid_mode: he PID (Process) Namespace mode for the container. Either ``container:<name|id>`` or ``host``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#pid_mode Container#pid_mode}
        :param ports: ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ports Container#ports}
        :param privileged: If ``true``, the container runs in privileged mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#privileged Container#privileged}
        :param publish_all_ports: Publish all ports of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#publish_all_ports Container#publish_all_ports}
        :param read_only: If ``true``, the container will be started as readonly. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#read_only Container#read_only}
        :param remove_volumes: If ``true``, it will remove anonymous volumes associated with the container. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#remove_volumes Container#remove_volumes}
        :param restart: The restart policy for the container. Must be one of 'no', 'on-failure', 'always', 'unless-stopped'. Defaults to ``no``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#restart Container#restart}
        :param rm: If ``true``, then the container will be automatically removed when it exits. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#rm Container#rm}
        :param runtime: Runtime to use for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#runtime Container#runtime}
        :param security_opts: List of string values to customize labels for MLS systems, such as SELinux. See https://docs.docker.com/engine/reference/run/#security-configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#security_opts Container#security_opts}
        :param shm_size: Size of ``/dev/shm`` in MBs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#shm_size Container#shm_size}
        :param start: If ``true``, then the Docker container will be started after creation. If ``false``, then the container is only created. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#start Container#start}
        :param stdin_open: If ``true``, keep STDIN open even if not attached (``docker run -i``). Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#stdin_open Container#stdin_open}
        :param stop_signal: Signal to stop a container (default ``SIGTERM``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#stop_signal Container#stop_signal}
        :param stop_timeout: Timeout (in seconds) to stop a container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#stop_timeout Container#stop_timeout}
        :param storage_opts: Key/value pairs for the storage driver options, e.g. ``size``: ``120G``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#storage_opts Container#storage_opts}
        :param sysctls: A map of kernel parameters (sysctls) to set in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#sysctls Container#sysctls}
        :param tmpfs: A map of container directories which should be replaced by ``tmpfs mounts``, and their corresponding mount options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#tmpfs Container#tmpfs}
        :param tty: If ``true``, allocate a pseudo-tty (``docker run -t``). Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#tty Container#tty}
        :param ulimit: ulimit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ulimit Container#ulimit}
        :param upload: upload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#upload Container#upload}
        :param user: User used for run the first process. Format is ``user`` or ``user:group`` which user and group can be passed literraly or by name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#user Container#user}
        :param userns_mode: Sets the usernamespace mode for the container when usernamespace remapping option is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#userns_mode Container#userns_mode}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#volumes Container#volumes}
        :param wait: If ``true``, then the Docker container is waited for being healthy state after creation. This requires your container to have a healthcheck, otherwise this provider will error. If ``false``, then the container health state is not checked. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#wait Container#wait}
        :param wait_timeout: The timeout in seconds to wait the container to be healthy after creation. Defaults to ``60``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#wait_timeout Container#wait_timeout}
        :param working_dir: The working directory for commands to run in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#working_dir Container#working_dir}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48ec2bf472b6e9fe11b252b3b812812f009c78cda3f9397468250c2087edb1f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ContainerConfig(
            image=image,
            name=name,
            attach=attach,
            capabilities=capabilities,
            cgroupns_mode=cgroupns_mode,
            command=command,
            container_read_refresh_timeout_milliseconds=container_read_refresh_timeout_milliseconds,
            cpus=cpus,
            cpu_set=cpu_set,
            cpu_shares=cpu_shares,
            destroy_grace_seconds=destroy_grace_seconds,
            devices=devices,
            dns=dns,
            dns_opts=dns_opts,
            dns_search=dns_search,
            domainname=domainname,
            entrypoint=entrypoint,
            env=env,
            gpus=gpus,
            group_add=group_add,
            healthcheck=healthcheck,
            host=host,
            hostname=hostname,
            id=id,
            init=init,
            ipc_mode=ipc_mode,
            labels=labels,
            log_driver=log_driver,
            log_opts=log_opts,
            logs=logs,
            max_retry_count=max_retry_count,
            memory=memory,
            memory_swap=memory_swap,
            mounts=mounts,
            must_run=must_run,
            network_mode=network_mode,
            networks_advanced=networks_advanced,
            pid_mode=pid_mode,
            ports=ports,
            privileged=privileged,
            publish_all_ports=publish_all_ports,
            read_only=read_only,
            remove_volumes=remove_volumes,
            restart=restart,
            rm=rm,
            runtime=runtime,
            security_opts=security_opts,
            shm_size=shm_size,
            start=start,
            stdin_open=stdin_open,
            stop_signal=stop_signal,
            stop_timeout=stop_timeout,
            storage_opts=storage_opts,
            sysctls=sysctls,
            tmpfs=tmpfs,
            tty=tty,
            ulimit=ulimit,
            upload=upload,
            user=user,
            userns_mode=userns_mode,
            volumes=volumes,
            wait=wait,
            wait_timeout=wait_timeout,
            working_dir=working_dir,
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
        '''Generates CDKTF code for importing a Container resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Container to import.
        :param import_from_id: The id of the existing Container that should be imported. Refer to the {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Container to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a117cfafff6e940fed0dc84de3a8f0c0b6e1f1a431b4f26fe5952f09d700cbc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCapabilities")
    def put_capabilities(
        self,
        *,
        add: typing.Optional[typing.Sequence[builtins.str]] = None,
        drop: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param add: List of linux capabilities to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#add Container#add}
        :param drop: List of linux capabilities to drop. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#drop Container#drop}
        '''
        value = ContainerCapabilities(add=add, drop=drop)

        return typing.cast(None, jsii.invoke(self, "putCapabilities", [value]))

    @jsii.member(jsii_name="putDevices")
    def put_devices(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerDevices", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58659796eac9660e8a92a11acea15c16b61035b5b282aabe0e88d43adf5b6f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDevices", [value]))

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
        :param test: Command to run to check health. For example, to run ``curl -f localhost/health`` set the command to be ``["CMD", "curl", "-f", "localhost/health"]``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#test Container#test}
        :param interval: Time between running the check (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#interval Container#interval}
        :param retries: Consecutive failures needed to report unhealthy. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#retries Container#retries}
        :param start_period: Start period for the container to initialize before counting retries towards unstable (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#start_period Container#start_period}
        :param timeout: Maximum time to allow one check to run (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#timeout Container#timeout}
        '''
        value = ContainerHealthcheck(
            test=test,
            interval=interval,
            retries=retries,
            start_period=start_period,
            timeout=timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putHealthcheck", [value]))

    @jsii.member(jsii_name="putHost")
    def put_host(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerHost", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2aef3baddb3762dcc8ea8e52021886544d37f9574ad37325b114fa61e200054)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHost", [value]))

    @jsii.member(jsii_name="putLabels")
    def put_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerLabels", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3ba4891e1e8f667363d8f5586bff03f79911344714cd6c2a067810f31f302c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLabels", [value]))

    @jsii.member(jsii_name="putMounts")
    def put_mounts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerMounts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e66f87b3e1d235fdb0726cb6f76ca02bb6b61a9b48990255d604b382c41bfad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMounts", [value]))

    @jsii.member(jsii_name="putNetworksAdvanced")
    def put_networks_advanced(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNetworksAdvanced", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26ba0dd23b2e4382ab4e44f5b1179ecb61692da2da10a969d40a8a14e437217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworksAdvanced", [value]))

    @jsii.member(jsii_name="putPorts")
    def put_ports(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerPorts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8472b00f573fcfe342412486e287b7cb21c7ef5b0eedc352b112e640b3d3adb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPorts", [value]))

    @jsii.member(jsii_name="putUlimit")
    def put_ulimit(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerUlimit", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3561b9173ce72dcbc2c60c7ac5f12c5a625ea8dd3f7127a0b9979394325b4cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUlimit", [value]))

    @jsii.member(jsii_name="putUpload")
    def put_upload(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerUpload", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd5e853f5d69cb38f6d69d31d5b6829e3c9ac76b43fe08813a7e983117dde74c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUpload", [value]))

    @jsii.member(jsii_name="putVolumes")
    def put_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6737613f040694b10de23b51e3fc2c7e34b5fd220fd0b24f6184197113b6b20b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumes", [value]))

    @jsii.member(jsii_name="resetAttach")
    def reset_attach(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttach", []))

    @jsii.member(jsii_name="resetCapabilities")
    def reset_capabilities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapabilities", []))

    @jsii.member(jsii_name="resetCgroupnsMode")
    def reset_cgroupns_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCgroupnsMode", []))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetContainerReadRefreshTimeoutMilliseconds")
    def reset_container_read_refresh_timeout_milliseconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerReadRefreshTimeoutMilliseconds", []))

    @jsii.member(jsii_name="resetCpus")
    def reset_cpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpus", []))

    @jsii.member(jsii_name="resetCpuSet")
    def reset_cpu_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuSet", []))

    @jsii.member(jsii_name="resetCpuShares")
    def reset_cpu_shares(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuShares", []))

    @jsii.member(jsii_name="resetDestroyGraceSeconds")
    def reset_destroy_grace_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestroyGraceSeconds", []))

    @jsii.member(jsii_name="resetDevices")
    def reset_devices(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDevices", []))

    @jsii.member(jsii_name="resetDns")
    def reset_dns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDns", []))

    @jsii.member(jsii_name="resetDnsOpts")
    def reset_dns_opts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsOpts", []))

    @jsii.member(jsii_name="resetDnsSearch")
    def reset_dns_search(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsSearch", []))

    @jsii.member(jsii_name="resetDomainname")
    def reset_domainname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainname", []))

    @jsii.member(jsii_name="resetEntrypoint")
    def reset_entrypoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntrypoint", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetGpus")
    def reset_gpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpus", []))

    @jsii.member(jsii_name="resetGroupAdd")
    def reset_group_add(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupAdd", []))

    @jsii.member(jsii_name="resetHealthcheck")
    def reset_healthcheck(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthcheck", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInit")
    def reset_init(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInit", []))

    @jsii.member(jsii_name="resetIpcMode")
    def reset_ipc_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpcMode", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLogDriver")
    def reset_log_driver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogDriver", []))

    @jsii.member(jsii_name="resetLogOpts")
    def reset_log_opts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogOpts", []))

    @jsii.member(jsii_name="resetLogs")
    def reset_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogs", []))

    @jsii.member(jsii_name="resetMaxRetryCount")
    def reset_max_retry_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetryCount", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @jsii.member(jsii_name="resetMemorySwap")
    def reset_memory_swap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemorySwap", []))

    @jsii.member(jsii_name="resetMounts")
    def reset_mounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMounts", []))

    @jsii.member(jsii_name="resetMustRun")
    def reset_must_run(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMustRun", []))

    @jsii.member(jsii_name="resetNetworkMode")
    def reset_network_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkMode", []))

    @jsii.member(jsii_name="resetNetworksAdvanced")
    def reset_networks_advanced(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworksAdvanced", []))

    @jsii.member(jsii_name="resetPidMode")
    def reset_pid_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPidMode", []))

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @jsii.member(jsii_name="resetPrivileged")
    def reset_privileged(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivileged", []))

    @jsii.member(jsii_name="resetPublishAllPorts")
    def reset_publish_all_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishAllPorts", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetRemoveVolumes")
    def reset_remove_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoveVolumes", []))

    @jsii.member(jsii_name="resetRestart")
    def reset_restart(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestart", []))

    @jsii.member(jsii_name="resetRm")
    def reset_rm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRm", []))

    @jsii.member(jsii_name="resetRuntime")
    def reset_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntime", []))

    @jsii.member(jsii_name="resetSecurityOpts")
    def reset_security_opts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityOpts", []))

    @jsii.member(jsii_name="resetShmSize")
    def reset_shm_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShmSize", []))

    @jsii.member(jsii_name="resetStart")
    def reset_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStart", []))

    @jsii.member(jsii_name="resetStdinOpen")
    def reset_stdin_open(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStdinOpen", []))

    @jsii.member(jsii_name="resetStopSignal")
    def reset_stop_signal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStopSignal", []))

    @jsii.member(jsii_name="resetStopTimeout")
    def reset_stop_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStopTimeout", []))

    @jsii.member(jsii_name="resetStorageOpts")
    def reset_storage_opts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageOpts", []))

    @jsii.member(jsii_name="resetSysctls")
    def reset_sysctls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSysctls", []))

    @jsii.member(jsii_name="resetTmpfs")
    def reset_tmpfs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTmpfs", []))

    @jsii.member(jsii_name="resetTty")
    def reset_tty(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTty", []))

    @jsii.member(jsii_name="resetUlimit")
    def reset_ulimit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUlimit", []))

    @jsii.member(jsii_name="resetUpload")
    def reset_upload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpload", []))

    @jsii.member(jsii_name="resetUser")
    def reset_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUser", []))

    @jsii.member(jsii_name="resetUsernsMode")
    def reset_userns_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernsMode", []))

    @jsii.member(jsii_name="resetVolumes")
    def reset_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumes", []))

    @jsii.member(jsii_name="resetWait")
    def reset_wait(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWait", []))

    @jsii.member(jsii_name="resetWaitTimeout")
    def reset_wait_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitTimeout", []))

    @jsii.member(jsii_name="resetWorkingDir")
    def reset_working_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkingDir", []))

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
    @jsii.member(jsii_name="bridge")
    def bridge(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bridge"))

    @builtins.property
    @jsii.member(jsii_name="capabilities")
    def capabilities(self) -> "ContainerCapabilitiesOutputReference":
        return typing.cast("ContainerCapabilitiesOutputReference", jsii.get(self, "capabilities"))

    @builtins.property
    @jsii.member(jsii_name="containerLogs")
    def container_logs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerLogs"))

    @builtins.property
    @jsii.member(jsii_name="devices")
    def devices(self) -> "ContainerDevicesList":
        return typing.cast("ContainerDevicesList", jsii.get(self, "devices"))

    @builtins.property
    @jsii.member(jsii_name="exitCode")
    def exit_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "exitCode"))

    @builtins.property
    @jsii.member(jsii_name="healthcheck")
    def healthcheck(self) -> "ContainerHealthcheckOutputReference":
        return typing.cast("ContainerHealthcheckOutputReference", jsii.get(self, "healthcheck"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> "ContainerHostList":
        return typing.cast("ContainerHostList", jsii.get(self, "host"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> "ContainerLabelsList":
        return typing.cast("ContainerLabelsList", jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="mounts")
    def mounts(self) -> "ContainerMountsList":
        return typing.cast("ContainerMountsList", jsii.get(self, "mounts"))

    @builtins.property
    @jsii.member(jsii_name="networkData")
    def network_data(self) -> "ContainerNetworkDataList":
        return typing.cast("ContainerNetworkDataList", jsii.get(self, "networkData"))

    @builtins.property
    @jsii.member(jsii_name="networksAdvanced")
    def networks_advanced(self) -> "ContainerNetworksAdvancedList":
        return typing.cast("ContainerNetworksAdvancedList", jsii.get(self, "networksAdvanced"))

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> "ContainerPortsList":
        return typing.cast("ContainerPortsList", jsii.get(self, "ports"))

    @builtins.property
    @jsii.member(jsii_name="ulimit")
    def ulimit(self) -> "ContainerUlimitList":
        return typing.cast("ContainerUlimitList", jsii.get(self, "ulimit"))

    @builtins.property
    @jsii.member(jsii_name="upload")
    def upload(self) -> "ContainerUploadList":
        return typing.cast("ContainerUploadList", jsii.get(self, "upload"))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> "ContainerVolumesList":
        return typing.cast("ContainerVolumesList", jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="attachInput")
    def attach_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "attachInput"))

    @builtins.property
    @jsii.member(jsii_name="capabilitiesInput")
    def capabilities_input(self) -> typing.Optional["ContainerCapabilities"]:
        return typing.cast(typing.Optional["ContainerCapabilities"], jsii.get(self, "capabilitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="cgroupnsModeInput")
    def cgroupns_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cgroupnsModeInput"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="containerReadRefreshTimeoutMillisecondsInput")
    def container_read_refresh_timeout_milliseconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerReadRefreshTimeoutMillisecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuSetInput")
    def cpu_set_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuSetInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuSharesInput")
    def cpu_shares_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuSharesInput"))

    @builtins.property
    @jsii.member(jsii_name="cpusInput")
    def cpus_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpusInput"))

    @builtins.property
    @jsii.member(jsii_name="destroyGraceSecondsInput")
    def destroy_grace_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "destroyGraceSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="devicesInput")
    def devices_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerDevices"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerDevices"]]], jsii.get(self, "devicesInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsInput")
    def dns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsOptsInput")
    def dns_opts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsOptsInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsSearchInput")
    def dns_search_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsSearchInput"))

    @builtins.property
    @jsii.member(jsii_name="domainnameInput")
    def domainname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainnameInput"))

    @builtins.property
    @jsii.member(jsii_name="entrypointInput")
    def entrypoint_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "entrypointInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="gpusInput")
    def gpus_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gpusInput"))

    @builtins.property
    @jsii.member(jsii_name="groupAddInput")
    def group_add_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupAddInput"))

    @builtins.property
    @jsii.member(jsii_name="healthcheckInput")
    def healthcheck_input(self) -> typing.Optional["ContainerHealthcheck"]:
        return typing.cast(typing.Optional["ContainerHealthcheck"], jsii.get(self, "healthcheckInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerHost"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerHost"]]], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="initInput")
    def init_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "initInput"))

    @builtins.property
    @jsii.member(jsii_name="ipcModeInput")
    def ipc_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipcModeInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerLabels"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerLabels"]]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="logDriverInput")
    def log_driver_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logDriverInput"))

    @builtins.property
    @jsii.member(jsii_name="logOptsInput")
    def log_opts_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "logOptsInput"))

    @builtins.property
    @jsii.member(jsii_name="logsInput")
    def logs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetryCountInput")
    def max_retry_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetryCountInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySwapInput")
    def memory_swap_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySwapInput"))

    @builtins.property
    @jsii.member(jsii_name="mountsInput")
    def mounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerMounts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerMounts"]]], jsii.get(self, "mountsInput"))

    @builtins.property
    @jsii.member(jsii_name="mustRunInput")
    def must_run_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mustRunInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkModeInput")
    def network_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkModeInput"))

    @builtins.property
    @jsii.member(jsii_name="networksAdvancedInput")
    def networks_advanced_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNetworksAdvanced"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNetworksAdvanced"]]], jsii.get(self, "networksAdvancedInput"))

    @builtins.property
    @jsii.member(jsii_name="pidModeInput")
    def pid_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pidModeInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerPorts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerPorts"]]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="privilegedInput")
    def privileged_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privilegedInput"))

    @builtins.property
    @jsii.member(jsii_name="publishAllPortsInput")
    def publish_all_ports_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publishAllPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="removeVolumesInput")
    def remove_volumes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "removeVolumesInput"))

    @builtins.property
    @jsii.member(jsii_name="restartInput")
    def restart_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restartInput"))

    @builtins.property
    @jsii.member(jsii_name="rmInput")
    def rm_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rmInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="securityOptsInput")
    def security_opts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityOptsInput"))

    @builtins.property
    @jsii.member(jsii_name="shmSizeInput")
    def shm_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "shmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="stdinOpenInput")
    def stdin_open_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "stdinOpenInput"))

    @builtins.property
    @jsii.member(jsii_name="stopSignalInput")
    def stop_signal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stopSignalInput"))

    @builtins.property
    @jsii.member(jsii_name="stopTimeoutInput")
    def stop_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "stopTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="storageOptsInput")
    def storage_opts_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "storageOptsInput"))

    @builtins.property
    @jsii.member(jsii_name="sysctlsInput")
    def sysctls_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "sysctlsInput"))

    @builtins.property
    @jsii.member(jsii_name="tmpfsInput")
    def tmpfs_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tmpfsInput"))

    @builtins.property
    @jsii.member(jsii_name="ttyInput")
    def tty_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ttyInput"))

    @builtins.property
    @jsii.member(jsii_name="ulimitInput")
    def ulimit_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerUlimit"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerUlimit"]]], jsii.get(self, "ulimitInput"))

    @builtins.property
    @jsii.member(jsii_name="uploadInput")
    def upload_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerUpload"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerUpload"]]], jsii.get(self, "uploadInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="usernsModeInput")
    def userns_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernsModeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumesInput")
    def volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerVolumes"]]], jsii.get(self, "volumesInput"))

    @builtins.property
    @jsii.member(jsii_name="waitInput")
    def wait_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "waitInput"))

    @builtins.property
    @jsii.member(jsii_name="waitTimeoutInput")
    def wait_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "waitTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="workingDirInput")
    def working_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workingDirInput"))

    @builtins.property
    @jsii.member(jsii_name="attach")
    def attach(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "attach"))

    @attach.setter
    def attach(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb274bdb3538465984fdaf28708a86154690b9e80df70fdb70a637268d24fc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attach", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cgroupnsMode")
    def cgroupns_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cgroupnsMode"))

    @cgroupns_mode.setter
    def cgroupns_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98cd52ff440d1bd2151bd18349fd965fedfe4bbc4ac82aa5ced37f3e1ad34f9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cgroupnsMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f84d6538674bdd3ecb66d195c1c0d758b817795b47b1329fec7fc2003e93407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerReadRefreshTimeoutMilliseconds")
    def container_read_refresh_timeout_milliseconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerReadRefreshTimeoutMilliseconds"))

    @container_read_refresh_timeout_milliseconds.setter
    def container_read_refresh_timeout_milliseconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f4886d5ad8b53829cec57515f09c0936b1dd144c66f208d042bdb8fbcb58ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerReadRefreshTimeoutMilliseconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpus")
    def cpus(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpus"))

    @cpus.setter
    def cpus(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__329a8989a63e99758c1de586411f59ef500fab9df562d8beebf19395ab8da916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuSet")
    def cpu_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuSet"))

    @cpu_set.setter
    def cpu_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fae00253e7ecc66830e1564df1b9fdfc33092b627e7fb79ad5e4499123e44de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuShares")
    def cpu_shares(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuShares"))

    @cpu_shares.setter
    def cpu_shares(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b15256ad7563113a5d03c63de55adde700242dbcc6d952e85d00af13b5073e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuShares", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destroyGraceSeconds")
    def destroy_grace_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "destroyGraceSeconds"))

    @destroy_grace_seconds.setter
    def destroy_grace_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1306b7d55e8e6610284ae8da440519ede69026dddba4bc6be078a3e874998684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destroyGraceSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dns")
    def dns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dns"))

    @dns.setter
    def dns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dbd8e7a75b71a36a2e1ccf9b4f19b5a734c751e45b7d452b899997087e04d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsOpts")
    def dns_opts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsOpts"))

    @dns_opts.setter
    def dns_opts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5905bd813ef43e7c4b96565e74539190415a0eb4c71209c8d5d686bff8594b57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsOpts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsSearch")
    def dns_search(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsSearch"))

    @dns_search.setter
    def dns_search(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19793de8a2eb8ce1dbffcd2ae850fbc7c2e184822a67c3e2959081cfac0ff236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsSearch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainname")
    def domainname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainname"))

    @domainname.setter
    def domainname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da338db259aaa8d39495244eb4730e4efba3d5795834766991f8af31321bcffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entrypoint")
    def entrypoint(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "entrypoint"))

    @entrypoint.setter
    def entrypoint(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4fff8bd560291e23d8d75e7490bff5dfd46664fd2f452c4e31c9048b7cd86c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entrypoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "env"))

    @env.setter
    def env(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d16947c4e02f9ade0587c2c1d10fd686ea2bd8e2e65ac386d2be5025ca82e792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "env", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpus")
    def gpus(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gpus"))

    @gpus.setter
    def gpus(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__413841d98152142bdb858457f46024aee50da2d46600509aebe2a56255e2d110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupAdd")
    def group_add(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupAdd"))

    @group_add.setter
    def group_add(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ca7fd4c5f36d1c39be4f76264816708f0796ff1685fbc20777813766a2d7b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupAdd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6abcd1784a03da45e8ad5009395a02a9ea51dde31ce8edfa2ceaf58525466331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be65dd1b0b3e60f099f9a5e9d09598c7aff60b9b6c3eee2be913a67e09ef202d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19dea8604f5eca052ffd44225a4ad570116ae3c4d48da5178a503dcd8c302da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="init")
    def init(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "init"))

    @init.setter
    def init(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca02e053996d784f380588c33ebbec1e76cbbd69a0133dc821f132f38ef382e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "init", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipcMode")
    def ipc_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipcMode"))

    @ipc_mode.setter
    def ipc_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8aa8b2c665f91c9b68d083b01e56c69945a72cbd6aaf8af72d3acfb18066250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipcMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logDriver")
    def log_driver(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logDriver"))

    @log_driver.setter
    def log_driver(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016dd2faa91127b4007aa7346f65561294c9e39af3b6101b94fc33327300bd70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logDriver", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logOpts")
    def log_opts(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "logOpts"))

    @log_opts.setter
    def log_opts(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd6f35abeabd4b2ca35db5b1051271efb0202c4cb9e9c51b8f975260b7bdfd25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logOpts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logs")
    def logs(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logs"))

    @logs.setter
    def logs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4c5b2eb265acd751a55b6735f4c0870d356051cc022f8cd5c802c585e14bb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetryCount")
    def max_retry_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRetryCount"))

    @max_retry_count.setter
    def max_retry_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015625d5a5fd5d75270804974997b1897a5effe1ea03c0aa173cf83a9ce9965a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetryCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91f26871c2eafb93fdcbe28aed36e8dcbac161138d77152866d748b107725595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorySwap")
    def memory_swap(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySwap"))

    @memory_swap.setter
    def memory_swap(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0b4bb89faca6478a54c2b061ad56d5d1fa85a3463952533b44daa977799866a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySwap", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mustRun")
    def must_run(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mustRun"))

    @must_run.setter
    def must_run(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cdb3d44f5d4194bc9317f70e76e000c7a848ae5eb5dc8ba12f5f0fd6fa6be73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mustRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb026e86f4c6dfb4790113f182e90d3e0d102cd061082f11905907974acc7b63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkMode"))

    @network_mode.setter
    def network_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c005cd8aedc9aabf75b7e0ec6fea3dbfaf8cf7043516255b9b235e8d6bcdd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pidMode")
    def pid_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pidMode"))

    @pid_mode.setter
    def pid_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5804756e6d576ef609b393913fb543c3c7718bd0352f017290de6211906a9f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pidMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privileged")
    def privileged(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privileged"))

    @privileged.setter
    def privileged(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b3e460d5f9a26e4cc768ddeed2db77f3710a08feb387e293edcefcc1145d23d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privileged", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publishAllPorts")
    def publish_all_ports(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publishAllPorts"))

    @publish_all_ports.setter
    def publish_all_ports(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a95752aa9d3ef3c1e8118f3d28294b5e5c9047cb7c128a7b2251657756e6dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishAllPorts", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__0b40943302e537dd0952c761bce598cf4e76974f8588c1d3e01c474f024c0928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="removeVolumes")
    def remove_volumes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "removeVolumes"))

    @remove_volumes.setter
    def remove_volumes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb87b5fdb4e3589d4c912da1400aacd8c491ad7d4645f30922d6796e4ac0396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "removeVolumes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restart")
    def restart(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "restart"))

    @restart.setter
    def restart(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__120d1eea976e192c1fb7d238d9b0f0498600071646ffeeedfc5b586bf5509c1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rm")
    def rm(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rm"))

    @rm.setter
    def rm(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2eea7eb89d963187709ee945cb31aad732f9ba4d2f7deec020e69fa3988b87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faec2e687b6e767361362f8b8409f134cdd0c1a585b0bcdc4463879cb6ad4886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityOpts")
    def security_opts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityOpts"))

    @security_opts.setter
    def security_opts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d148c335d2eb0e59fbbe9b0b32481525ee4fef5ef09bd805f2ee4e55464b73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityOpts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shmSize")
    def shm_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "shmSize"))

    @shm_size.setter
    def shm_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f57fcc37c326b9dd6b787f1c924a6aaf4e97c24911383ca7753b634ba3dd91b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "start"))

    @start.setter
    def start(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54911310154c0da8bed033174f4b69bfbebc4f8d238a9078b1fc95234150ea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stdinOpen")
    def stdin_open(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "stdinOpen"))

    @stdin_open.setter
    def stdin_open(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51145e7afb967a391c9aa38e5046c7c5291eb51e1df5d62959a75de64fc7fafe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stdinOpen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stopSignal")
    def stop_signal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stopSignal"))

    @stop_signal.setter
    def stop_signal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28bd4ec32109be9e9bff28c7abccbcf780afba36bd4b6f04ebaa868f259f3f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stopSignal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stopTimeout")
    def stop_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "stopTimeout"))

    @stop_timeout.setter
    def stop_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e34e0815bb868d16484878af5fefdf4c7287f1dc4cbb8582dbd8a859787a83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stopTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageOpts")
    def storage_opts(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "storageOpts"))

    @storage_opts.setter
    def storage_opts(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a773e2ad26c6a5d8fac23b3c69775083fa39e713a1bd5c1250c5e0163409819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageOpts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sysctls")
    def sysctls(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "sysctls"))

    @sysctls.setter
    def sysctls(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e65c3f9cc4077d44998621654b1bc23cc5f763c23497719d8a6ca49d8473af3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sysctls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tmpfs")
    def tmpfs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tmpfs"))

    @tmpfs.setter
    def tmpfs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1240ed7aafd9cfe1e0581842678d7c11eccb62148cd0996735bc134aa33354ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tmpfs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tty")
    def tty(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tty"))

    @tty.setter
    def tty(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__184ff37f1ed05db343b6e99c042e4569e8c080b450708b48a93ae4e934648e57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tty", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f550e02ebecc9ae49ad3543e57a173a310a41019b6380a8e77e78a3e6b9aa0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usernsMode")
    def userns_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernsMode"))

    @userns_mode.setter
    def userns_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa71d928b9a2b960e62d888ec036bb2332f67310e463a1e60dbc9b3a531bb08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernsMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wait")
    def wait(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "wait"))

    @wait.setter
    def wait(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c23505cf016507da21996d07d47161d7173e88968a2b86132cf81f0d5fef6f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wait", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitTimeout")
    def wait_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "waitTimeout"))

    @wait_timeout.setter
    def wait_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b192d3669c40cfd6e3659be1c5802670a8c9fb5f88f58334a228093ced057d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workingDir")
    def working_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workingDir"))

    @working_dir.setter
    def working_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c9403f276a1f08fdf14eb85c588d45131cfef64a224234999c7427ebcd9a8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workingDir", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerCapabilities",
    jsii_struct_bases=[],
    name_mapping={"add": "add", "drop": "drop"},
)
class ContainerCapabilities:
    def __init__(
        self,
        *,
        add: typing.Optional[typing.Sequence[builtins.str]] = None,
        drop: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param add: List of linux capabilities to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#add Container#add}
        :param drop: List of linux capabilities to drop. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#drop Container#drop}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a65902a2a3f73dc940f2671ac040643fc443224764d6023c88df51634ec901)
            check_type(argname="argument add", value=add, expected_type=type_hints["add"])
            check_type(argname="argument drop", value=drop, expected_type=type_hints["drop"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add is not None:
            self._values["add"] = add
        if drop is not None:
            self._values["drop"] = drop

    @builtins.property
    def add(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of linux capabilities to add.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#add Container#add}
        '''
        result = self._values.get("add")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def drop(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of linux capabilities to drop.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#drop Container#drop}
        '''
        result = self._values.get("drop")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerCapabilities(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerCapabilitiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerCapabilitiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb36ee23d7594966c5a21813dc63114fc910ef0969a3460c977266565762155a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdd")
    def reset_add(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdd", []))

    @jsii.member(jsii_name="resetDrop")
    def reset_drop(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrop", []))

    @builtins.property
    @jsii.member(jsii_name="addInput")
    def add_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addInput"))

    @builtins.property
    @jsii.member(jsii_name="dropInput")
    def drop_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dropInput"))

    @builtins.property
    @jsii.member(jsii_name="add")
    def add(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "add"))

    @add.setter
    def add(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41d4d42adfbb7450a312dd07c9d8253159a356e7d33f9be311a9cbec93771463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "add", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="drop")
    def drop(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "drop"))

    @drop.setter
    def drop(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645640e83b459066f10b4d04e07647d59ceb816bcd48e6dc575b069903ed9a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "drop", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerCapabilities]:
        return typing.cast(typing.Optional[ContainerCapabilities], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ContainerCapabilities]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41d269daed3c0a1d6c1d0d67df7db335efd31c158460d813bdaec9a1c69a653e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "image": "image",
        "name": "name",
        "attach": "attach",
        "capabilities": "capabilities",
        "cgroupns_mode": "cgroupnsMode",
        "command": "command",
        "container_read_refresh_timeout_milliseconds": "containerReadRefreshTimeoutMilliseconds",
        "cpus": "cpus",
        "cpu_set": "cpuSet",
        "cpu_shares": "cpuShares",
        "destroy_grace_seconds": "destroyGraceSeconds",
        "devices": "devices",
        "dns": "dns",
        "dns_opts": "dnsOpts",
        "dns_search": "dnsSearch",
        "domainname": "domainname",
        "entrypoint": "entrypoint",
        "env": "env",
        "gpus": "gpus",
        "group_add": "groupAdd",
        "healthcheck": "healthcheck",
        "host": "host",
        "hostname": "hostname",
        "id": "id",
        "init": "init",
        "ipc_mode": "ipcMode",
        "labels": "labels",
        "log_driver": "logDriver",
        "log_opts": "logOpts",
        "logs": "logs",
        "max_retry_count": "maxRetryCount",
        "memory": "memory",
        "memory_swap": "memorySwap",
        "mounts": "mounts",
        "must_run": "mustRun",
        "network_mode": "networkMode",
        "networks_advanced": "networksAdvanced",
        "pid_mode": "pidMode",
        "ports": "ports",
        "privileged": "privileged",
        "publish_all_ports": "publishAllPorts",
        "read_only": "readOnly",
        "remove_volumes": "removeVolumes",
        "restart": "restart",
        "rm": "rm",
        "runtime": "runtime",
        "security_opts": "securityOpts",
        "shm_size": "shmSize",
        "start": "start",
        "stdin_open": "stdinOpen",
        "stop_signal": "stopSignal",
        "stop_timeout": "stopTimeout",
        "storage_opts": "storageOpts",
        "sysctls": "sysctls",
        "tmpfs": "tmpfs",
        "tty": "tty",
        "ulimit": "ulimit",
        "upload": "upload",
        "user": "user",
        "userns_mode": "usernsMode",
        "volumes": "volumes",
        "wait": "wait",
        "wait_timeout": "waitTimeout",
        "working_dir": "workingDir",
    },
)
class ContainerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        image: builtins.str,
        name: builtins.str,
        attach: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        capabilities: typing.Optional[typing.Union[ContainerCapabilities, typing.Dict[builtins.str, typing.Any]]] = None,
        cgroupns_mode: typing.Optional[builtins.str] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_read_refresh_timeout_milliseconds: typing.Optional[jsii.Number] = None,
        cpus: typing.Optional[builtins.str] = None,
        cpu_set: typing.Optional[builtins.str] = None,
        cpu_shares: typing.Optional[jsii.Number] = None,
        destroy_grace_seconds: typing.Optional[jsii.Number] = None,
        devices: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerDevices", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_search: typing.Optional[typing.Sequence[builtins.str]] = None,
        domainname: typing.Optional[builtins.str] = None,
        entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Sequence[builtins.str]] = None,
        gpus: typing.Optional[builtins.str] = None,
        group_add: typing.Optional[typing.Sequence[builtins.str]] = None,
        healthcheck: typing.Optional[typing.Union["ContainerHealthcheck", typing.Dict[builtins.str, typing.Any]]] = None,
        host: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerHost", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hostname: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        init: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ipc_mode: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        log_driver: typing.Optional[builtins.str] = None,
        log_opts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_retry_count: typing.Optional[jsii.Number] = None,
        memory: typing.Optional[jsii.Number] = None,
        memory_swap: typing.Optional[jsii.Number] = None,
        mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        must_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_mode: typing.Optional[builtins.str] = None,
        networks_advanced: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerNetworksAdvanced", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pid_mode: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        privileged: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        publish_all_ports: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remove_volumes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restart: typing.Optional[builtins.str] = None,
        rm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        runtime: typing.Optional[builtins.str] = None,
        security_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
        shm_size: typing.Optional[jsii.Number] = None,
        start: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        stdin_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        stop_signal: typing.Optional[builtins.str] = None,
        stop_timeout: typing.Optional[jsii.Number] = None,
        storage_opts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        sysctls: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tmpfs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ulimit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerUlimit", typing.Dict[builtins.str, typing.Any]]]]] = None,
        upload: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerUpload", typing.Dict[builtins.str, typing.Any]]]]] = None,
        user: typing.Optional[builtins.str] = None,
        userns_mode: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        wait: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        wait_timeout: typing.Optional[jsii.Number] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param image: The ID of the image to back this container. The easiest way to get this value is to use the ``image_id`` attribute of the ``docker_image`` resource as is shown in the example. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#image Container#image}
        :param name: The name of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#name Container#name}
        :param attach: If ``true`` attach to the container after its creation and waits the end of its execution. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#attach Container#attach}
        :param capabilities: capabilities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#capabilities Container#capabilities}
        :param cgroupns_mode: Cgroup namespace mode to use for the container. Possible values are: ``private``, ``host``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#cgroupns_mode Container#cgroupns_mode}
        :param command: The command to use to start the container. For example, to run ``/usr/bin/myprogram -f baz.conf`` set the command to be ``["/usr/bin/myprogram","-f","baz.conf"]``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#command Container#command}
        :param container_read_refresh_timeout_milliseconds: The total number of milliseconds to wait for the container to reach status 'running'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#container_read_refresh_timeout_milliseconds Container#container_read_refresh_timeout_milliseconds}
        :param cpus: Specify how much of the available CPU resources a container can use. e.g a value of 1.5 means the container is guaranteed at most one and a half of the CPUs Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#cpus Container#cpus}
        :param cpu_set: A comma-separated list or hyphen-separated range of CPUs a container can use, e.g. ``0-1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#cpu_set Container#cpu_set}
        :param cpu_shares: CPU shares (relative weight) for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#cpu_shares Container#cpu_shares}
        :param destroy_grace_seconds: If defined will attempt to stop the container before destroying. Container will be destroyed after ``n`` seconds or on successful stop. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#destroy_grace_seconds Container#destroy_grace_seconds}
        :param devices: devices block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#devices Container#devices}
        :param dns: DNS servers to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#dns Container#dns}
        :param dns_opts: DNS options used by the DNS provider(s), see ``resolv.conf`` documentation for valid list of options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#dns_opts Container#dns_opts}
        :param dns_search: DNS search domains that are used when bare unqualified hostnames are used inside of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#dns_search Container#dns_search}
        :param domainname: Domain name of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#domainname Container#domainname}
        :param entrypoint: The command to use as the Entrypoint for the container. The Entrypoint allows you to configure a container to run as an executable. For example, to run ``/usr/bin/myprogram`` when starting a container, set the entrypoint to be ``"/usr/bin/myprogram"]``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#entrypoint Container#entrypoint}
        :param env: Environment variables to set in the form of ``KEY=VALUE``, e.g. ``DEBUG=0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#env Container#env}
        :param gpus: GPU devices to add to the container. Currently, only the value ``all`` is supported. Passing any other value will result in unexpected behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#gpus Container#gpus}
        :param group_add: Additional groups for the container user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#group_add Container#group_add}
        :param healthcheck: healthcheck block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#healthcheck Container#healthcheck}
        :param host: host block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#host Container#host}
        :param hostname: Hostname of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#hostname Container#hostname}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#id Container#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param init: Configured whether an init process should be injected for this container. If unset this will default to the ``dockerd`` defaults. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#init Container#init}
        :param ipc_mode: IPC sharing mode for the container. Possible values are: ``none``, ``private``, ``shareable``, ``container:<name|id>`` or ``host``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ipc_mode Container#ipc_mode}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#labels Container#labels}
        :param log_driver: The logging driver to use for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#log_driver Container#log_driver}
        :param log_opts: Key/value pairs to use as options for the logging driver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#log_opts Container#log_opts}
        :param logs: Save the container logs (``attach`` must be enabled). Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#logs Container#logs}
        :param max_retry_count: The maximum amount of times to an attempt a restart when ``restart`` is set to 'on-failure'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#max_retry_count Container#max_retry_count}
        :param memory: The memory limit for the container in MBs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#memory Container#memory}
        :param memory_swap: The total memory limit (memory + swap) for the container in MBs. This setting may compute to ``-1`` after ``terraform apply`` if the target host doesn't support memory swap, when that is the case docker will use a soft limitation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#memory_swap Container#memory_swap}
        :param mounts: mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#mounts Container#mounts}
        :param must_run: If ``true``, then the Docker container will be kept running. If ``false``, then as long as the container exists, Terraform assumes it is successful. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#must_run Container#must_run}
        :param network_mode: Network mode of the container. See https://docs.docker.com/engine/network/ for more information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#network_mode Container#network_mode}
        :param networks_advanced: networks_advanced block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#networks_advanced Container#networks_advanced}
        :param pid_mode: he PID (Process) Namespace mode for the container. Either ``container:<name|id>`` or ``host``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#pid_mode Container#pid_mode}
        :param ports: ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ports Container#ports}
        :param privileged: If ``true``, the container runs in privileged mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#privileged Container#privileged}
        :param publish_all_ports: Publish all ports of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#publish_all_ports Container#publish_all_ports}
        :param read_only: If ``true``, the container will be started as readonly. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#read_only Container#read_only}
        :param remove_volumes: If ``true``, it will remove anonymous volumes associated with the container. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#remove_volumes Container#remove_volumes}
        :param restart: The restart policy for the container. Must be one of 'no', 'on-failure', 'always', 'unless-stopped'. Defaults to ``no``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#restart Container#restart}
        :param rm: If ``true``, then the container will be automatically removed when it exits. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#rm Container#rm}
        :param runtime: Runtime to use for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#runtime Container#runtime}
        :param security_opts: List of string values to customize labels for MLS systems, such as SELinux. See https://docs.docker.com/engine/reference/run/#security-configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#security_opts Container#security_opts}
        :param shm_size: Size of ``/dev/shm`` in MBs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#shm_size Container#shm_size}
        :param start: If ``true``, then the Docker container will be started after creation. If ``false``, then the container is only created. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#start Container#start}
        :param stdin_open: If ``true``, keep STDIN open even if not attached (``docker run -i``). Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#stdin_open Container#stdin_open}
        :param stop_signal: Signal to stop a container (default ``SIGTERM``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#stop_signal Container#stop_signal}
        :param stop_timeout: Timeout (in seconds) to stop a container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#stop_timeout Container#stop_timeout}
        :param storage_opts: Key/value pairs for the storage driver options, e.g. ``size``: ``120G``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#storage_opts Container#storage_opts}
        :param sysctls: A map of kernel parameters (sysctls) to set in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#sysctls Container#sysctls}
        :param tmpfs: A map of container directories which should be replaced by ``tmpfs mounts``, and their corresponding mount options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#tmpfs Container#tmpfs}
        :param tty: If ``true``, allocate a pseudo-tty (``docker run -t``). Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#tty Container#tty}
        :param ulimit: ulimit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ulimit Container#ulimit}
        :param upload: upload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#upload Container#upload}
        :param user: User used for run the first process. Format is ``user`` or ``user:group`` which user and group can be passed literraly or by name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#user Container#user}
        :param userns_mode: Sets the usernamespace mode for the container when usernamespace remapping option is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#userns_mode Container#userns_mode}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#volumes Container#volumes}
        :param wait: If ``true``, then the Docker container is waited for being healthy state after creation. This requires your container to have a healthcheck, otherwise this provider will error. If ``false``, then the container health state is not checked. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#wait Container#wait}
        :param wait_timeout: The timeout in seconds to wait the container to be healthy after creation. Defaults to ``60``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#wait_timeout Container#wait_timeout}
        :param working_dir: The working directory for commands to run in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#working_dir Container#working_dir}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(capabilities, dict):
            capabilities = ContainerCapabilities(**capabilities)
        if isinstance(healthcheck, dict):
            healthcheck = ContainerHealthcheck(**healthcheck)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1985321a167573487d759bff6561898e2f12ca869786a5ebc7b8ef498c89a9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument attach", value=attach, expected_type=type_hints["attach"])
            check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
            check_type(argname="argument cgroupns_mode", value=cgroupns_mode, expected_type=type_hints["cgroupns_mode"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument container_read_refresh_timeout_milliseconds", value=container_read_refresh_timeout_milliseconds, expected_type=type_hints["container_read_refresh_timeout_milliseconds"])
            check_type(argname="argument cpus", value=cpus, expected_type=type_hints["cpus"])
            check_type(argname="argument cpu_set", value=cpu_set, expected_type=type_hints["cpu_set"])
            check_type(argname="argument cpu_shares", value=cpu_shares, expected_type=type_hints["cpu_shares"])
            check_type(argname="argument destroy_grace_seconds", value=destroy_grace_seconds, expected_type=type_hints["destroy_grace_seconds"])
            check_type(argname="argument devices", value=devices, expected_type=type_hints["devices"])
            check_type(argname="argument dns", value=dns, expected_type=type_hints["dns"])
            check_type(argname="argument dns_opts", value=dns_opts, expected_type=type_hints["dns_opts"])
            check_type(argname="argument dns_search", value=dns_search, expected_type=type_hints["dns_search"])
            check_type(argname="argument domainname", value=domainname, expected_type=type_hints["domainname"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument gpus", value=gpus, expected_type=type_hints["gpus"])
            check_type(argname="argument group_add", value=group_add, expected_type=type_hints["group_add"])
            check_type(argname="argument healthcheck", value=healthcheck, expected_type=type_hints["healthcheck"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument init", value=init, expected_type=type_hints["init"])
            check_type(argname="argument ipc_mode", value=ipc_mode, expected_type=type_hints["ipc_mode"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument log_opts", value=log_opts, expected_type=type_hints["log_opts"])
            check_type(argname="argument logs", value=logs, expected_type=type_hints["logs"])
            check_type(argname="argument max_retry_count", value=max_retry_count, expected_type=type_hints["max_retry_count"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument memory_swap", value=memory_swap, expected_type=type_hints["memory_swap"])
            check_type(argname="argument mounts", value=mounts, expected_type=type_hints["mounts"])
            check_type(argname="argument must_run", value=must_run, expected_type=type_hints["must_run"])
            check_type(argname="argument network_mode", value=network_mode, expected_type=type_hints["network_mode"])
            check_type(argname="argument networks_advanced", value=networks_advanced, expected_type=type_hints["networks_advanced"])
            check_type(argname="argument pid_mode", value=pid_mode, expected_type=type_hints["pid_mode"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument privileged", value=privileged, expected_type=type_hints["privileged"])
            check_type(argname="argument publish_all_ports", value=publish_all_ports, expected_type=type_hints["publish_all_ports"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument remove_volumes", value=remove_volumes, expected_type=type_hints["remove_volumes"])
            check_type(argname="argument restart", value=restart, expected_type=type_hints["restart"])
            check_type(argname="argument rm", value=rm, expected_type=type_hints["rm"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument security_opts", value=security_opts, expected_type=type_hints["security_opts"])
            check_type(argname="argument shm_size", value=shm_size, expected_type=type_hints["shm_size"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            check_type(argname="argument stdin_open", value=stdin_open, expected_type=type_hints["stdin_open"])
            check_type(argname="argument stop_signal", value=stop_signal, expected_type=type_hints["stop_signal"])
            check_type(argname="argument stop_timeout", value=stop_timeout, expected_type=type_hints["stop_timeout"])
            check_type(argname="argument storage_opts", value=storage_opts, expected_type=type_hints["storage_opts"])
            check_type(argname="argument sysctls", value=sysctls, expected_type=type_hints["sysctls"])
            check_type(argname="argument tmpfs", value=tmpfs, expected_type=type_hints["tmpfs"])
            check_type(argname="argument tty", value=tty, expected_type=type_hints["tty"])
            check_type(argname="argument ulimit", value=ulimit, expected_type=type_hints["ulimit"])
            check_type(argname="argument upload", value=upload, expected_type=type_hints["upload"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument userns_mode", value=userns_mode, expected_type=type_hints["userns_mode"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            check_type(argname="argument wait", value=wait, expected_type=type_hints["wait"])
            check_type(argname="argument wait_timeout", value=wait_timeout, expected_type=type_hints["wait_timeout"])
            check_type(argname="argument working_dir", value=working_dir, expected_type=type_hints["working_dir"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
            "name": name,
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
        if attach is not None:
            self._values["attach"] = attach
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if cgroupns_mode is not None:
            self._values["cgroupns_mode"] = cgroupns_mode
        if command is not None:
            self._values["command"] = command
        if container_read_refresh_timeout_milliseconds is not None:
            self._values["container_read_refresh_timeout_milliseconds"] = container_read_refresh_timeout_milliseconds
        if cpus is not None:
            self._values["cpus"] = cpus
        if cpu_set is not None:
            self._values["cpu_set"] = cpu_set
        if cpu_shares is not None:
            self._values["cpu_shares"] = cpu_shares
        if destroy_grace_seconds is not None:
            self._values["destroy_grace_seconds"] = destroy_grace_seconds
        if devices is not None:
            self._values["devices"] = devices
        if dns is not None:
            self._values["dns"] = dns
        if dns_opts is not None:
            self._values["dns_opts"] = dns_opts
        if dns_search is not None:
            self._values["dns_search"] = dns_search
        if domainname is not None:
            self._values["domainname"] = domainname
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if env is not None:
            self._values["env"] = env
        if gpus is not None:
            self._values["gpus"] = gpus
        if group_add is not None:
            self._values["group_add"] = group_add
        if healthcheck is not None:
            self._values["healthcheck"] = healthcheck
        if host is not None:
            self._values["host"] = host
        if hostname is not None:
            self._values["hostname"] = hostname
        if id is not None:
            self._values["id"] = id
        if init is not None:
            self._values["init"] = init
        if ipc_mode is not None:
            self._values["ipc_mode"] = ipc_mode
        if labels is not None:
            self._values["labels"] = labels
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if log_opts is not None:
            self._values["log_opts"] = log_opts
        if logs is not None:
            self._values["logs"] = logs
        if max_retry_count is not None:
            self._values["max_retry_count"] = max_retry_count
        if memory is not None:
            self._values["memory"] = memory
        if memory_swap is not None:
            self._values["memory_swap"] = memory_swap
        if mounts is not None:
            self._values["mounts"] = mounts
        if must_run is not None:
            self._values["must_run"] = must_run
        if network_mode is not None:
            self._values["network_mode"] = network_mode
        if networks_advanced is not None:
            self._values["networks_advanced"] = networks_advanced
        if pid_mode is not None:
            self._values["pid_mode"] = pid_mode
        if ports is not None:
            self._values["ports"] = ports
        if privileged is not None:
            self._values["privileged"] = privileged
        if publish_all_ports is not None:
            self._values["publish_all_ports"] = publish_all_ports
        if read_only is not None:
            self._values["read_only"] = read_only
        if remove_volumes is not None:
            self._values["remove_volumes"] = remove_volumes
        if restart is not None:
            self._values["restart"] = restart
        if rm is not None:
            self._values["rm"] = rm
        if runtime is not None:
            self._values["runtime"] = runtime
        if security_opts is not None:
            self._values["security_opts"] = security_opts
        if shm_size is not None:
            self._values["shm_size"] = shm_size
        if start is not None:
            self._values["start"] = start
        if stdin_open is not None:
            self._values["stdin_open"] = stdin_open
        if stop_signal is not None:
            self._values["stop_signal"] = stop_signal
        if stop_timeout is not None:
            self._values["stop_timeout"] = stop_timeout
        if storage_opts is not None:
            self._values["storage_opts"] = storage_opts
        if sysctls is not None:
            self._values["sysctls"] = sysctls
        if tmpfs is not None:
            self._values["tmpfs"] = tmpfs
        if tty is not None:
            self._values["tty"] = tty
        if ulimit is not None:
            self._values["ulimit"] = ulimit
        if upload is not None:
            self._values["upload"] = upload
        if user is not None:
            self._values["user"] = user
        if userns_mode is not None:
            self._values["userns_mode"] = userns_mode
        if volumes is not None:
            self._values["volumes"] = volumes
        if wait is not None:
            self._values["wait"] = wait
        if wait_timeout is not None:
            self._values["wait_timeout"] = wait_timeout
        if working_dir is not None:
            self._values["working_dir"] = working_dir

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
    def image(self) -> builtins.str:
        '''The ID of the image to back this container.

        The easiest way to get this value is to use the ``image_id`` attribute of the ``docker_image`` resource as is shown in the example.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#image Container#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#name Container#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attach(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true`` attach to the container after its creation and waits the end of its execution. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#attach Container#attach}
        '''
        result = self._values.get("attach")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def capabilities(self) -> typing.Optional[ContainerCapabilities]:
        '''capabilities block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#capabilities Container#capabilities}
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[ContainerCapabilities], result)

    @builtins.property
    def cgroupns_mode(self) -> typing.Optional[builtins.str]:
        '''Cgroup namespace mode to use for the container. Possible values are: ``private``, ``host``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#cgroupns_mode Container#cgroupns_mode}
        '''
        result = self._values.get("cgroupns_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The command to use to start the container.

        For example, to run ``/usr/bin/myprogram -f baz.conf`` set the command to be ``["/usr/bin/myprogram","-f","baz.conf"]``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#command Container#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def container_read_refresh_timeout_milliseconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''The total number of milliseconds to wait for the container to reach status 'running'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#container_read_refresh_timeout_milliseconds Container#container_read_refresh_timeout_milliseconds}
        '''
        result = self._values.get("container_read_refresh_timeout_milliseconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpus(self) -> typing.Optional[builtins.str]:
        '''Specify how much of the available CPU resources a container can use.

        e.g a value of 1.5 means the container is guaranteed at most one and a half of the CPUs

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#cpus Container#cpus}
        '''
        result = self._values.get("cpus")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_set(self) -> typing.Optional[builtins.str]:
        '''A comma-separated list or hyphen-separated range of CPUs a container can use, e.g. ``0-1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#cpu_set Container#cpu_set}
        '''
        result = self._values.get("cpu_set")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_shares(self) -> typing.Optional[jsii.Number]:
        '''CPU shares (relative weight) for the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#cpu_shares Container#cpu_shares}
        '''
        result = self._values.get("cpu_shares")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def destroy_grace_seconds(self) -> typing.Optional[jsii.Number]:
        '''If defined will attempt to stop the container before destroying.

        Container will be destroyed after ``n`` seconds or on successful stop.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#destroy_grace_seconds Container#destroy_grace_seconds}
        '''
        result = self._values.get("destroy_grace_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def devices(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerDevices"]]]:
        '''devices block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#devices Container#devices}
        '''
        result = self._values.get("devices")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerDevices"]]], result)

    @builtins.property
    def dns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''DNS servers to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#dns Container#dns}
        '''
        result = self._values.get("dns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dns_opts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''DNS options used by the DNS provider(s), see ``resolv.conf`` documentation for valid list of options.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#dns_opts Container#dns_opts}
        '''
        result = self._values.get("dns_opts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dns_search(self) -> typing.Optional[typing.List[builtins.str]]:
        '''DNS search domains that are used when bare unqualified hostnames are used inside of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#dns_search Container#dns_search}
        '''
        result = self._values.get("dns_search")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def domainname(self) -> typing.Optional[builtins.str]:
        '''Domain name of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#domainname Container#domainname}
        '''
        result = self._values.get("domainname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The command to use as the Entrypoint for the container.

        The Entrypoint allows you to configure a container to run as an executable. For example, to run ``/usr/bin/myprogram`` when starting a container, set the entrypoint to be ``"/usr/bin/myprogram"]``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#entrypoint Container#entrypoint}
        '''
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Environment variables to set in the form of ``KEY=VALUE``, e.g. ``DEBUG=0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#env Container#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def gpus(self) -> typing.Optional[builtins.str]:
        '''GPU devices to add to the container.

        Currently, only the value ``all`` is supported. Passing any other value will result in unexpected behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#gpus Container#gpus}
        '''
        result = self._values.get("gpus")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_add(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional groups for the container user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#group_add Container#group_add}
        '''
        result = self._values.get("group_add")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def healthcheck(self) -> typing.Optional["ContainerHealthcheck"]:
        '''healthcheck block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#healthcheck Container#healthcheck}
        '''
        result = self._values.get("healthcheck")
        return typing.cast(typing.Optional["ContainerHealthcheck"], result)

    @builtins.property
    def host(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerHost"]]]:
        '''host block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#host Container#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerHost"]]], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''Hostname of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#hostname Container#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#id Container#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def init(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Configured whether an init process should be injected for this container.

        If unset this will default to the ``dockerd`` defaults.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#init Container#init}
        '''
        result = self._values.get("init")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ipc_mode(self) -> typing.Optional[builtins.str]:
        '''IPC sharing mode for the container. Possible values are: ``none``, ``private``, ``shareable``, ``container:<name|id>`` or ``host``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ipc_mode Container#ipc_mode}
        '''
        result = self._values.get("ipc_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerLabels"]]]:
        '''labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#labels Container#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerLabels"]]], result)

    @builtins.property
    def log_driver(self) -> typing.Optional[builtins.str]:
        '''The logging driver to use for the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#log_driver Container#log_driver}
        '''
        result = self._values.get("log_driver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_opts(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key/value pairs to use as options for the logging driver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#log_opts Container#log_opts}
        '''
        result = self._values.get("log_opts")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def logs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Save the container logs (``attach`` must be enabled). Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#logs Container#logs}
        '''
        result = self._values.get("logs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_retry_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum amount of times to an attempt a restart when ``restart`` is set to 'on-failure'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#max_retry_count Container#max_retry_count}
        '''
        result = self._values.get("max_retry_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory(self) -> typing.Optional[jsii.Number]:
        '''The memory limit for the container in MBs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#memory Container#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_swap(self) -> typing.Optional[jsii.Number]:
        '''The total memory limit (memory + swap) for the container in MBs.

        This setting may compute to ``-1`` after ``terraform apply`` if the target host doesn't support memory swap, when that is the case docker will use a soft limitation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#memory_swap Container#memory_swap}
        '''
        result = self._values.get("memory_swap")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerMounts"]]]:
        '''mounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#mounts Container#mounts}
        '''
        result = self._values.get("mounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerMounts"]]], result)

    @builtins.property
    def must_run(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true``, then the Docker container will be kept running.

        If ``false``, then as long as the container exists, Terraform assumes it is successful. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#must_run Container#must_run}
        '''
        result = self._values.get("must_run")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def network_mode(self) -> typing.Optional[builtins.str]:
        '''Network mode of the container. See https://docs.docker.com/engine/network/ for more information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#network_mode Container#network_mode}
        '''
        result = self._values.get("network_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def networks_advanced(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNetworksAdvanced"]]]:
        '''networks_advanced block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#networks_advanced Container#networks_advanced}
        '''
        result = self._values.get("networks_advanced")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerNetworksAdvanced"]]], result)

    @builtins.property
    def pid_mode(self) -> typing.Optional[builtins.str]:
        '''he PID (Process) Namespace mode for the container. Either ``container:<name|id>`` or ``host``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#pid_mode Container#pid_mode}
        '''
        result = self._values.get("pid_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerPorts"]]]:
        '''ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ports Container#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerPorts"]]], result)

    @builtins.property
    def privileged(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true``, the container runs in privileged mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#privileged Container#privileged}
        '''
        result = self._values.get("privileged")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def publish_all_ports(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Publish all ports of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#publish_all_ports Container#publish_all_ports}
        '''
        result = self._values.get("publish_all_ports")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true``, the container will be started as readonly. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#read_only Container#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def remove_volumes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true``, it will remove anonymous volumes associated with the container. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#remove_volumes Container#remove_volumes}
        '''
        result = self._values.get("remove_volumes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restart(self) -> typing.Optional[builtins.str]:
        '''The restart policy for the container. Must be one of 'no', 'on-failure', 'always', 'unless-stopped'. Defaults to ``no``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#restart Container#restart}
        '''
        result = self._values.get("restart")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true``, then the container will be automatically removed when it exits. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#rm Container#rm}
        '''
        result = self._values.get("rm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''Runtime to use for the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#runtime Container#runtime}
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_opts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of string values to customize labels for MLS systems, such as SELinux. See https://docs.docker.com/engine/reference/run/#security-configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#security_opts Container#security_opts}
        '''
        result = self._values.get("security_opts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def shm_size(self) -> typing.Optional[jsii.Number]:
        '''Size of ``/dev/shm`` in MBs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#shm_size Container#shm_size}
        '''
        result = self._values.get("shm_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true``, then the Docker container will be started after creation.

        If ``false``, then the container is only created. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#start Container#start}
        '''
        result = self._values.get("start")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def stdin_open(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true``, keep STDIN open even if not attached (``docker run -i``). Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#stdin_open Container#stdin_open}
        '''
        result = self._values.get("stdin_open")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def stop_signal(self) -> typing.Optional[builtins.str]:
        '''Signal to stop a container (default ``SIGTERM``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#stop_signal Container#stop_signal}
        '''
        result = self._values.get("stop_signal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stop_timeout(self) -> typing.Optional[jsii.Number]:
        '''Timeout (in seconds) to stop a container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#stop_timeout Container#stop_timeout}
        '''
        result = self._values.get("stop_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_opts(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key/value pairs for the storage driver options, e.g. ``size``: ``120G``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#storage_opts Container#storage_opts}
        '''
        result = self._values.get("storage_opts")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def sysctls(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of kernel parameters (sysctls) to set in the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#sysctls Container#sysctls}
        '''
        result = self._values.get("sysctls")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tmpfs(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of container directories which should be replaced by ``tmpfs mounts``, and their corresponding mount options.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#tmpfs Container#tmpfs}
        '''
        result = self._values.get("tmpfs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tty(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true``, allocate a pseudo-tty (``docker run -t``). Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#tty Container#tty}
        '''
        result = self._values.get("tty")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ulimit(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerUlimit"]]]:
        '''ulimit block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ulimit Container#ulimit}
        '''
        result = self._values.get("ulimit")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerUlimit"]]], result)

    @builtins.property
    def upload(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerUpload"]]]:
        '''upload block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#upload Container#upload}
        '''
        result = self._values.get("upload")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerUpload"]]], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''User used for run the first process.

        Format is ``user`` or ``user:group`` which user and group can be passed literraly or by name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#user Container#user}
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def userns_mode(self) -> typing.Optional[builtins.str]:
        '''Sets the usernamespace mode for the container when usernamespace remapping option is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#userns_mode Container#userns_mode}
        '''
        result = self._values.get("userns_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerVolumes"]]]:
        '''volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#volumes Container#volumes}
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerVolumes"]]], result)

    @builtins.property
    def wait(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true``, then the Docker container is waited for being healthy state after creation.

        This requires your container to have a healthcheck, otherwise this provider will error. If ``false``, then the container health state is not checked. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#wait Container#wait}
        '''
        result = self._values.get("wait")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def wait_timeout(self) -> typing.Optional[jsii.Number]:
        '''The timeout in seconds to wait the container to be healthy after creation. Defaults to ``60``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#wait_timeout Container#wait_timeout}
        '''
        result = self._values.get("wait_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def working_dir(self) -> typing.Optional[builtins.str]:
        '''The working directory for commands to run in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#working_dir Container#working_dir}
        '''
        result = self._values.get("working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerDevices",
    jsii_struct_bases=[],
    name_mapping={
        "host_path": "hostPath",
        "container_path": "containerPath",
        "permissions": "permissions",
    },
)
class ContainerDevices:
    def __init__(
        self,
        *,
        host_path: builtins.str,
        container_path: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_path: The path on the host where the device is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#host_path Container#host_path}
        :param container_path: The path in the container where the device will be bound. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#container_path Container#container_path}
        :param permissions: The cgroup permissions given to the container to access the device. Defaults to ``rwm``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#permissions Container#permissions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__146d561b3aa3ec7af00e9c695ba6e56b56c66fc65b26bbed8137cce8e221a52d)
            check_type(argname="argument host_path", value=host_path, expected_type=type_hints["host_path"])
            check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_path": host_path,
        }
        if container_path is not None:
            self._values["container_path"] = container_path
        if permissions is not None:
            self._values["permissions"] = permissions

    @builtins.property
    def host_path(self) -> builtins.str:
        '''The path on the host where the device is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#host_path Container#host_path}
        '''
        result = self._values.get("host_path")
        assert result is not None, "Required property 'host_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_path(self) -> typing.Optional[builtins.str]:
        '''The path in the container where the device will be bound.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#container_path Container#container_path}
        '''
        result = self._values.get("container_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(self) -> typing.Optional[builtins.str]:
        '''The cgroup permissions given to the container to access the device. Defaults to ``rwm``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#permissions Container#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerDevices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerDevicesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerDevicesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3286d2c6e6cdc6a601592634ea73380c740f66b0894c4b5abefd59e0a2f7d181)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerDevicesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa2fa5a8a14e30c40cf5c023aa26e6dd870c04b3357b7dd60d18d2becc89a92d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerDevicesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__307eb655a3de46ab4efe879ceaf47ebb9f6561a37ac18451ec7ff1fd2521c606)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a20ea4bf0a4e4cec9887f8cc55f0c6eaaf15eff25596bb37c7db5e582afbfda)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efc6e95e7591990389cecc8600252e3d7de050add10afcda73dea55cc233ca4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerDevices]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerDevices]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerDevices]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77e6ae236df7bdba65a64fda882d05b216a234c082df2099ffd3c22046abb9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerDevicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerDevicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45beccb66cfd6f150ee2bd24e6481212d81a29b9cbf14249b0a2e69f26658518)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContainerPath")
    def reset_container_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerPath", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @builtins.property
    @jsii.member(jsii_name="containerPathInput")
    def container_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerPathInput"))

    @builtins.property
    @jsii.member(jsii_name="hostPathInput")
    def host_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostPathInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="containerPath")
    def container_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerPath"))

    @container_path.setter
    def container_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c366a6f1590adc22fcd578c01cb08d304388c3f7416eee3c90c856290ed94e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostPath")
    def host_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostPath"))

    @host_path.setter
    def host_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e8843735de6d75bcba52e570ed5c41c6c6cfc54a08fee163519c3eb93ebfeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissions"))

    @permissions.setter
    def permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__049ad0e59afc356f5dbd4e3fd2005f6a0fb8b578c095adfa92a90898958d7f4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerDevices]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerDevices]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerDevices]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73caa9346682731462bf8759e916531ef8936189bc211b87aff3c12b70d04d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerHealthcheck",
    jsii_struct_bases=[],
    name_mapping={
        "test": "test",
        "interval": "interval",
        "retries": "retries",
        "start_period": "startPeriod",
        "timeout": "timeout",
    },
)
class ContainerHealthcheck:
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
        :param test: Command to run to check health. For example, to run ``curl -f localhost/health`` set the command to be ``["CMD", "curl", "-f", "localhost/health"]``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#test Container#test}
        :param interval: Time between running the check (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#interval Container#interval}
        :param retries: Consecutive failures needed to report unhealthy. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#retries Container#retries}
        :param start_period: Start period for the container to initialize before counting retries towards unstable (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#start_period Container#start_period}
        :param timeout: Maximum time to allow one check to run (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#timeout Container#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9432b7d78f2e610b6c54c84150a2b48d7150a28ad33e8e0e45700acaed7b02)
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
        '''Command to run to check health.

        For example, to run ``curl -f localhost/health`` set the command to be ``["CMD", "curl", "-f", "localhost/health"]``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#test Container#test}
        '''
        result = self._values.get("test")
        assert result is not None, "Required property 'test' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def interval(self) -> typing.Optional[builtins.str]:
        '''Time between running the check (ms|s|m|h). Defaults to ``0s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#interval Container#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retries(self) -> typing.Optional[jsii.Number]:
        '''Consecutive failures needed to report unhealthy. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#retries Container#retries}
        '''
        result = self._values.get("retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_period(self) -> typing.Optional[builtins.str]:
        '''Start period for the container to initialize before counting retries towards unstable (ms|s|m|h). Defaults to ``0s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#start_period Container#start_period}
        '''
        result = self._values.get("start_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Maximum time to allow one check to run (ms|s|m|h). Defaults to ``0s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#timeout Container#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerHealthcheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerHealthcheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerHealthcheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea936c2aecdf4da07fc31fbb5190662bc94dc64cffe8f8cbb1a855beea4f870e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__376955f3161270188560145a5e2c0e35a433d95f51e5eed7501c7c54c50154e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retries")
    def retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retries"))

    @retries.setter
    def retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e796cbc50c5b40b7e17091fe1f95f4c6cf40e54a74e3475d8ba0f9adfd3181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startPeriod")
    def start_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startPeriod"))

    @start_period.setter
    def start_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b646d3724103c7fb549d6e6d38cd71bc6655e93c3c58af93df8b08a61089399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="test")
    def test(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "test"))

    @test.setter
    def test(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a8bf18656a953fcdc16f9236af6dcdce4c69b9b565d41332fd03004a593e52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "test", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f34a219127c0f07ca720152e5e32c861c8b26b825d16920e66ecef66b9dd60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerHealthcheck]:
        return typing.cast(typing.Optional[ContainerHealthcheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ContainerHealthcheck]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8192d624d798540d9d1cf16b6cb1693cf445c2573730dcb547967aa8f14743e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerHost",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "ip": "ip"},
)
class ContainerHost:
    def __init__(self, *, host: builtins.str, ip: builtins.str) -> None:
        '''
        :param host: Hostname to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#host Container#host}
        :param ip: IP address this hostname should resolve to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ip Container#ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d740eb1d81cf48185aad5246c96f804525587268943cac88414eee7b50fc60)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
            "ip": ip,
        }

    @builtins.property
    def host(self) -> builtins.str:
        '''Hostname to add.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#host Container#host}
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip(self) -> builtins.str:
        '''IP address this hostname should resolve to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ip Container#ip}
        '''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerHost(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerHostList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerHostList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__886903115c2345733e1e11caf4a97ddfa9e62329bbef55ce4afe10b9a44d9fdc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerHostOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1390991ec2e39c6c12968293141e06cb02079db64fe906199836e5aa60cdec2b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerHostOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a962951bfdfe4f707ea800b8ab051156a17308a5e94745123b46632c93f7aa0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56e7943e58bfc99e64d6256218d84a75d96e4a870cb7309241981b3230b5ce97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3df94434c766f371e2eaf509048250c0d51cbd874838dfdbd80769f5aa31ace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerHost]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerHost]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerHost]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a90cdd9c92a85d25dab4bffc745868ab4a9f5639b5ec6f7e79f079d3644e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerHostOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerHostOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e53827f9982e510c6e3a1b6a19a5a4ce7f08eaae9c932a30c84976ff20778dd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f249fc27646414edbae696ad50365246fb63e0cb5d6ac5eb5b96814261e6dc2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45e8034bc9f198770280f71442e68d94337ec3cbcdf47d857bee862a16b0d964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerHost]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerHost]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerHost]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d4be6a2799602751c095c6013ddc2d12fed9b1cbc211851c0ecba8ed0c928c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class ContainerLabels:
    def __init__(self, *, label: builtins.str, value: builtins.str) -> None:
        '''
        :param label: Name of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#label Container#label}
        :param value: Value of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#value Container#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf90c1ae6f2e0b535b5e407371d3fe8e277b8f81810a33882fe4ff1490ba5695)
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> builtins.str:
        '''Name of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#label Container#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#value Container#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaa790d79e6e3408cf7f27ee2360824ea05926d3a99f80c4ec642e0e86abeef4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7d24c4c0b4a996ca91a8b543b12a0d54ade1513bf4e46810460c3488dedafd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b098d34ec778329fa4c6aa54dff62bee27144e645bed3d4c56b453a4ac3fb49b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c68fd8dff9315ff7dd21e5ce9674a59dc6d6952018680a4af7416b136c433423)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d420afeecd71116a6916b1e36c10205a547767783b76a90bb40588939d967e2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8823069a80a3a6f36ad4461cdca45457a8a23341347602c8dbc81621d83ce41a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f4ff39618ab76ec95ff48ed10cd591d77e7ebeb01bff1e8dc27a28071f5b37d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ced1ed5db218f165cfc12bed3c45b930842ab31e5bddb183b94fdf26322f9ab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49a73b0d720c46da71694e55ce4bc5fe7de50e9774f146b3b429b66698ed855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4730ed0ff620921e465be21844a9fb20912333681bc39c8c61e7237d4d1ed0e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerMounts",
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
class ContainerMounts:
    def __init__(
        self,
        *,
        target: builtins.str,
        type: builtins.str,
        bind_options: typing.Optional[typing.Union["ContainerMountsBindOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source: typing.Optional[builtins.str] = None,
        tmpfs_options: typing.Optional[typing.Union["ContainerMountsTmpfsOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_options: typing.Optional[typing.Union["ContainerMountsVolumeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param target: Container path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#target Container#target}
        :param type: The mount type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#type Container#type}
        :param bind_options: bind_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#bind_options Container#bind_options}
        :param read_only: Whether the mount should be read-only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#read_only Container#read_only}
        :param source: Mount source (e.g. a volume name, a host path). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#source Container#source}
        :param tmpfs_options: tmpfs_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#tmpfs_options Container#tmpfs_options}
        :param volume_options: volume_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#volume_options Container#volume_options}
        '''
        if isinstance(bind_options, dict):
            bind_options = ContainerMountsBindOptions(**bind_options)
        if isinstance(tmpfs_options, dict):
            tmpfs_options = ContainerMountsTmpfsOptions(**tmpfs_options)
        if isinstance(volume_options, dict):
            volume_options = ContainerMountsVolumeOptions(**volume_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a36576a29d4694529a5b5fdc7006b4db9d468b7e4c3423bb53ce20ce5887cd2a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#target Container#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The mount type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#type Container#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bind_options(self) -> typing.Optional["ContainerMountsBindOptions"]:
        '''bind_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#bind_options Container#bind_options}
        '''
        result = self._values.get("bind_options")
        return typing.cast(typing.Optional["ContainerMountsBindOptions"], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the mount should be read-only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#read_only Container#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Mount source (e.g. a volume name, a host path).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#source Container#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tmpfs_options(self) -> typing.Optional["ContainerMountsTmpfsOptions"]:
        '''tmpfs_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#tmpfs_options Container#tmpfs_options}
        '''
        result = self._values.get("tmpfs_options")
        return typing.cast(typing.Optional["ContainerMountsTmpfsOptions"], result)

    @builtins.property
    def volume_options(self) -> typing.Optional["ContainerMountsVolumeOptions"]:
        '''volume_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#volume_options Container#volume_options}
        '''
        result = self._values.get("volume_options")
        return typing.cast(typing.Optional["ContainerMountsVolumeOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerMountsBindOptions",
    jsii_struct_bases=[],
    name_mapping={"propagation": "propagation"},
)
class ContainerMountsBindOptions:
    def __init__(self, *, propagation: typing.Optional[builtins.str] = None) -> None:
        '''
        :param propagation: A propagation mode with the value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#propagation Container#propagation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05215177c99a750e909ea2dcb1e3573adc5ddcffd355f668eee0ee2c6381701b)
            check_type(argname="argument propagation", value=propagation, expected_type=type_hints["propagation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if propagation is not None:
            self._values["propagation"] = propagation

    @builtins.property
    def propagation(self) -> typing.Optional[builtins.str]:
        '''A propagation mode with the value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#propagation Container#propagation}
        '''
        result = self._values.get("propagation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerMountsBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerMountsBindOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerMountsBindOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1778ec6a97c5fccf7439e0249f19e4e3547aea0b2cc729c296d4b8d51f2b2d90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0b83c96a1a012a961fe6975dd30c7785b80597303a2ed67d50b1692290aad60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propagation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerMountsBindOptions]:
        return typing.cast(typing.Optional[ContainerMountsBindOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerMountsBindOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7923a22b8cc349b67b4bb76d42c92c1e2ba381b85c477f60de930c2c509aa1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerMountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerMountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7633d71a5f83a7aed083b94f1047b3e0b5c611dcd5b7e5825890d560f7ef047)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerMountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467008150c788c9ad2081ed809cdebb33243fa4d86dbcbb0d6e6e2bad79c1633)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerMountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fdbd933e41e5a8443ed75a80c6ac37d75efc20f06577013f1cea8b25af9304b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c63ca0aedec654b4aee7c7e47cd199297a7a311172965d3ebf972c22a0ba22f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__579062fd51a1559a8748e5ee2b277fec876ea799c2d9a7141bb34dc670da0285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerMounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerMounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff9ffe9406f71bbb0d98415e864daf2be84982a220d041f94ae19336fc5db7bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerMountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerMountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46c9c02ebfed7fff7acf39f77f043072cb7d4c1906b784af4b092bb282e0e252)
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
        :param propagation: A propagation mode with the value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#propagation Container#propagation}
        '''
        value = ContainerMountsBindOptions(propagation=propagation)

        return typing.cast(None, jsii.invoke(self, "putBindOptions", [value]))

    @jsii.member(jsii_name="putTmpfsOptions")
    def put_tmpfs_options(
        self,
        *,
        mode: typing.Optional[jsii.Number] = None,
        size_bytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param mode: The permission mode for the tmpfs mount in an integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#mode Container#mode}
        :param size_bytes: The size for the tmpfs mount in bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#size_bytes Container#size_bytes}
        '''
        value = ContainerMountsTmpfsOptions(mode=mode, size_bytes=size_bytes)

        return typing.cast(None, jsii.invoke(self, "putTmpfsOptions", [value]))

    @jsii.member(jsii_name="putVolumeOptions")
    def put_volume_options(
        self,
        *,
        driver_name: typing.Optional[builtins.str] = None,
        driver_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerMountsVolumeOptionsLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        no_copy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subpath: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param driver_name: Name of the driver to use to create the volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#driver_name Container#driver_name}
        :param driver_options: key/value map of driver specific options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#driver_options Container#driver_options}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#labels Container#labels}
        :param no_copy: Populate volume with data from the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#no_copy Container#no_copy}
        :param subpath: Path within the volume to mount. Requires docker server version 1.45 or higher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#subpath Container#subpath}
        '''
        value = ContainerMountsVolumeOptions(
            driver_name=driver_name,
            driver_options=driver_options,
            labels=labels,
            no_copy=no_copy,
            subpath=subpath,
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
    def bind_options(self) -> ContainerMountsBindOptionsOutputReference:
        return typing.cast(ContainerMountsBindOptionsOutputReference, jsii.get(self, "bindOptions"))

    @builtins.property
    @jsii.member(jsii_name="tmpfsOptions")
    def tmpfs_options(self) -> "ContainerMountsTmpfsOptionsOutputReference":
        return typing.cast("ContainerMountsTmpfsOptionsOutputReference", jsii.get(self, "tmpfsOptions"))

    @builtins.property
    @jsii.member(jsii_name="volumeOptions")
    def volume_options(self) -> "ContainerMountsVolumeOptionsOutputReference":
        return typing.cast("ContainerMountsVolumeOptionsOutputReference", jsii.get(self, "volumeOptions"))

    @builtins.property
    @jsii.member(jsii_name="bindOptionsInput")
    def bind_options_input(self) -> typing.Optional[ContainerMountsBindOptions]:
        return typing.cast(typing.Optional[ContainerMountsBindOptions], jsii.get(self, "bindOptionsInput"))

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
    def tmpfs_options_input(self) -> typing.Optional["ContainerMountsTmpfsOptions"]:
        return typing.cast(typing.Optional["ContainerMountsTmpfsOptions"], jsii.get(self, "tmpfsOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeOptionsInput")
    def volume_options_input(self) -> typing.Optional["ContainerMountsVolumeOptions"]:
        return typing.cast(typing.Optional["ContainerMountsVolumeOptions"], jsii.get(self, "volumeOptionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d5098a27e03e8f53106fa0ae3e92fe83e32bc3417735e9131b6a0fda5b3f5c48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b83bc93ef9b814021248785419984990df2a57fa8d96c9830c3ffcf6c67bdb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83a3e5a623535de6d340f53b8a66fafbdd65a67839c9befadd53c1ac489d572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c23d1d5b5fc53fadf43059c0731f836cda90b71020c7ddf4bf07a5057a089e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerMounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerMounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerMounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6fb56ecddf30b21c255d3850f535e4fe42acf38d5678efe48c8cc93948340ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerMountsTmpfsOptions",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "size_bytes": "sizeBytes"},
)
class ContainerMountsTmpfsOptions:
    def __init__(
        self,
        *,
        mode: typing.Optional[jsii.Number] = None,
        size_bytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param mode: The permission mode for the tmpfs mount in an integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#mode Container#mode}
        :param size_bytes: The size for the tmpfs mount in bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#size_bytes Container#size_bytes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a28b6ccc911896a65cecfc1c8d445ae492e4452bd806b9cb1ec28145681e8d0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#mode Container#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def size_bytes(self) -> typing.Optional[jsii.Number]:
        '''The size for the tmpfs mount in bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#size_bytes Container#size_bytes}
        '''
        result = self._values.get("size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerMountsTmpfsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerMountsTmpfsOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerMountsTmpfsOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4db6bd9d9d8cc618fcbf092533c642ff113975f753d210b224ad1a7d7049f9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b830839d135616b369ff13d17919dd711e0b7e67c8fb17f6caa64ace938b4be0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeBytes")
    def size_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeBytes"))

    @size_bytes.setter
    def size_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee6eb8103fc7346e11e4017e657e721d2a85c8d96198351d126ae222cdc2694)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerMountsTmpfsOptions]:
        return typing.cast(typing.Optional[ContainerMountsTmpfsOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerMountsTmpfsOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df0761a3af0c7821029831d2218635e4a0d5fdaff550f6a7e20e81c42192ecd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerMountsVolumeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "driver_name": "driverName",
        "driver_options": "driverOptions",
        "labels": "labels",
        "no_copy": "noCopy",
        "subpath": "subpath",
    },
)
class ContainerMountsVolumeOptions:
    def __init__(
        self,
        *,
        driver_name: typing.Optional[builtins.str] = None,
        driver_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerMountsVolumeOptionsLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        no_copy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subpath: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param driver_name: Name of the driver to use to create the volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#driver_name Container#driver_name}
        :param driver_options: key/value map of driver specific options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#driver_options Container#driver_options}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#labels Container#labels}
        :param no_copy: Populate volume with data from the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#no_copy Container#no_copy}
        :param subpath: Path within the volume to mount. Requires docker server version 1.45 or higher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#subpath Container#subpath}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e57bf5e5517ab50538e55f56afa5df117be0622e1e391a42a3dfd77a9cf34ad)
            check_type(argname="argument driver_name", value=driver_name, expected_type=type_hints["driver_name"])
            check_type(argname="argument driver_options", value=driver_options, expected_type=type_hints["driver_options"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument no_copy", value=no_copy, expected_type=type_hints["no_copy"])
            check_type(argname="argument subpath", value=subpath, expected_type=type_hints["subpath"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if driver_name is not None:
            self._values["driver_name"] = driver_name
        if driver_options is not None:
            self._values["driver_options"] = driver_options
        if labels is not None:
            self._values["labels"] = labels
        if no_copy is not None:
            self._values["no_copy"] = no_copy
        if subpath is not None:
            self._values["subpath"] = subpath

    @builtins.property
    def driver_name(self) -> typing.Optional[builtins.str]:
        '''Name of the driver to use to create the volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#driver_name Container#driver_name}
        '''
        result = self._values.get("driver_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def driver_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''key/value map of driver specific options.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#driver_options Container#driver_options}
        '''
        result = self._values.get("driver_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerMountsVolumeOptionsLabels"]]]:
        '''labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#labels Container#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerMountsVolumeOptionsLabels"]]], result)

    @builtins.property
    def no_copy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Populate volume with data from the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#no_copy Container#no_copy}
        '''
        result = self._values.get("no_copy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def subpath(self) -> typing.Optional[builtins.str]:
        '''Path within the volume to mount. Requires docker server version 1.45 or higher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#subpath Container#subpath}
        '''
        result = self._values.get("subpath")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerMountsVolumeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerMountsVolumeOptionsLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class ContainerMountsVolumeOptionsLabels:
    def __init__(self, *, label: builtins.str, value: builtins.str) -> None:
        '''
        :param label: Name of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#label Container#label}
        :param value: Value of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#value Container#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a5ee98a467321cf1b2b71a821c63bb3bfb31930b4ca02bbca4369011cc8f65)
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> builtins.str:
        '''Name of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#label Container#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#value Container#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerMountsVolumeOptionsLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerMountsVolumeOptionsLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerMountsVolumeOptionsLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd2b4eba841bf1e4b790d3e65b9a494e55693a336f8708d8a476903bbee5be96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerMountsVolumeOptionsLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d1af0b9c130580f1e81ed07a6af28e45317b7fec6afd2cbfeaeca89b5a2685)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerMountsVolumeOptionsLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cde24a06d3b59a43795aecbc5c15017237e1beb4cbe8ac98f0e2832b8958a88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afb1688a25d041d2917f89292d71fda5e8430925ebc28ff9d15923b801f30968)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f16ef99323ee9dd6f86736fa54481baf763c1c0b089b39016f0c9dcd00136d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerMountsVolumeOptionsLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerMountsVolumeOptionsLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerMountsVolumeOptionsLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421574b3a33dc8f988de69696c8b68da8a8d82676717d44c9b96721d1cf2418d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerMountsVolumeOptionsLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerMountsVolumeOptionsLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed325a4b4cf1abdbb08611d10c7be6de074bc251b6dd5b2d031642e36f6071d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef77d8e3bba6bf912d72eaf2f7dcf262a49e0c4022918476271010ddeb9d9d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4119378555a576bf899f8753ea42c1f28445b47c1533cc153d37353eca5259bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerMountsVolumeOptionsLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerMountsVolumeOptionsLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerMountsVolumeOptionsLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083e4287498a4353454618261830d129f6bcbe98e3d112f00d87eb059b02f377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerMountsVolumeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerMountsVolumeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c2895e2c0ff8541421744fec7c0a847e24bd5abfc1ed3cf3e6e77d68b5db91e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLabels")
    def put_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerMountsVolumeOptionsLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ba68b5443374733c26794053b13a19ef7add6fefebb214266e1ea47acb7ffa1)
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

    @jsii.member(jsii_name="resetSubpath")
    def reset_subpath(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubpath", []))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> ContainerMountsVolumeOptionsLabelsList:
        return typing.cast(ContainerMountsVolumeOptionsLabelsList, jsii.get(self, "labels"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerMountsVolumeOptionsLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerMountsVolumeOptionsLabels]]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="noCopyInput")
    def no_copy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noCopyInput"))

    @builtins.property
    @jsii.member(jsii_name="subpathInput")
    def subpath_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subpathInput"))

    @builtins.property
    @jsii.member(jsii_name="driverName")
    def driver_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driverName"))

    @driver_name.setter
    def driver_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f68f54633b1caf30c2339c913e9247b38235e5ea51c8b127917123b5df22fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="driverOptions")
    def driver_options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverOptions"))

    @driver_options.setter
    def driver_options(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__917daaf07aae9615041d9a6a0e178cd367b8c6bd5811a239ac687ab46242816e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__757664c850a86379ed7bfc35aef3d67d28addaa5d08ae17e4e6575e429c56583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noCopy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subpath")
    def subpath(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subpath"))

    @subpath.setter
    def subpath(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ef88951a4ac8ec39638520f2d71d006b1e68120c4ae186e014a3c41f6b3b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subpath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerMountsVolumeOptions]:
        return typing.cast(typing.Optional[ContainerMountsVolumeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerMountsVolumeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1962b88fb142d9632273ea6993424adec1bbac242bc1564443901942a67ec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerNetworkData",
    jsii_struct_bases=[],
    name_mapping={},
)
class ContainerNetworkData:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNetworkData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNetworkDataList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerNetworkDataList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e41bd5dcb688b572bb93abe888c544b8fab950a4ba8a37693ba84d68d58372a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerNetworkDataOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bab3d84e54b74a952cea70ff60115dd93ed350240ab7c4fc3bf94efa4d1d0f08)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerNetworkDataOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d177f3db5c7470bdd851e7e49fd0863e5511d419bc672feee9a8f6795cd056c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04c20f714a7eaa28182106339fa6a33b3fa25ce23a57bc3ec405efce719cbbfa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe3271f90b13c8b77aba97d92a2ee96b8ea960cd4f0452675f46495de5f13a00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ContainerNetworkDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerNetworkDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5da48205ccd111a5ab26e77984fcabc46d32f12aa08bf2402013e60e0af850b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @builtins.property
    @jsii.member(jsii_name="globalIpv6Address")
    def global_ipv6_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "globalIpv6Address"))

    @builtins.property
    @jsii.member(jsii_name="globalIpv6PrefixLength")
    def global_ipv6_prefix_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "globalIpv6PrefixLength"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="ipPrefixLength")
    def ip_prefix_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ipPrefixLength"))

    @builtins.property
    @jsii.member(jsii_name="ipv6Gateway")
    def ipv6_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6Gateway"))

    @builtins.property
    @jsii.member(jsii_name="macAddress")
    def mac_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macAddress"))

    @builtins.property
    @jsii.member(jsii_name="networkName")
    def network_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerNetworkData]:
        return typing.cast(typing.Optional[ContainerNetworkData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ContainerNetworkData]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef0c0f6f95b7bd0c2e6599de15c076cc98172184cb759d104c5565cbf1e87b4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerNetworksAdvanced",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "aliases": "aliases",
        "ipv4_address": "ipv4Address",
        "ipv6_address": "ipv6Address",
    },
)
class ContainerNetworksAdvanced:
    def __init__(
        self,
        *,
        name: builtins.str,
        aliases: typing.Optional[typing.Sequence[builtins.str]] = None,
        ipv4_address: typing.Optional[builtins.str] = None,
        ipv6_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name or id of the network to use. You can use ``name`` or ``id`` attribute from a ``docker_network`` resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#name Container#name}
        :param aliases: The network aliases of the container in the specific network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#aliases Container#aliases}
        :param ipv4_address: The IPV4 address of the container in the specific network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ipv4_address Container#ipv4_address}
        :param ipv6_address: The IPV6 address of the container in the specific network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ipv6_address Container#ipv6_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c2845b94553388f5913a8ad2d2fa15520f344967aead9e640ea4d68fa7ce50)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument aliases", value=aliases, expected_type=type_hints["aliases"])
            check_type(argname="argument ipv4_address", value=ipv4_address, expected_type=type_hints["ipv4_address"])
            check_type(argname="argument ipv6_address", value=ipv6_address, expected_type=type_hints["ipv6_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if aliases is not None:
            self._values["aliases"] = aliases
        if ipv4_address is not None:
            self._values["ipv4_address"] = ipv4_address
        if ipv6_address is not None:
            self._values["ipv6_address"] = ipv6_address

    @builtins.property
    def name(self) -> builtins.str:
        '''The name or id of the network to use.

        You can use ``name`` or ``id`` attribute from a ``docker_network`` resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#name Container#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aliases(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The network aliases of the container in the specific network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#aliases Container#aliases}
        '''
        result = self._values.get("aliases")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ipv4_address(self) -> typing.Optional[builtins.str]:
        '''The IPV4 address of the container in the specific network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ipv4_address Container#ipv4_address}
        '''
        result = self._values.get("ipv4_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6_address(self) -> typing.Optional[builtins.str]:
        '''The IPV6 address of the container in the specific network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ipv6_address Container#ipv6_address}
        '''
        result = self._values.get("ipv6_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNetworksAdvanced(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerNetworksAdvancedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerNetworksAdvancedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de7c6c7a962a4e1d646034c826928fce2f4c380501ec411c32bddd7c096ddf5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerNetworksAdvancedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff0a80b9960df680d355b544d39f21087715f6056a0072899bef23be93a40e7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerNetworksAdvancedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4571cb59e209a173e09d6621fa8d1da5ac411e11ebd77b8bf929bd396a8d6ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce455dcc6ae59036a31c5577f205327ec2e8e3d4ec81292d9cbacc79df180b20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acfa1c61314f7de335775832d82353e6ec98bf66216eb4e7f604cdf5ab9e770c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNetworksAdvanced]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNetworksAdvanced]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNetworksAdvanced]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcf558d826c7e80a61af05679fe820e510ad42e5c766f3bfabbc3dab4ebc902b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerNetworksAdvancedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerNetworksAdvancedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa09b48a03421b4f977a5692023dcf43f913ef42c3f02a9d558632d54e119833)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAliases")
    def reset_aliases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAliases", []))

    @jsii.member(jsii_name="resetIpv4Address")
    def reset_ipv4_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4Address", []))

    @jsii.member(jsii_name="resetIpv6Address")
    def reset_ipv6_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6Address", []))

    @builtins.property
    @jsii.member(jsii_name="aliasesInput")
    def aliases_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "aliasesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4AddressInput")
    def ipv4_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv4AddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AddressInput")
    def ipv6_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6AddressInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e6c5950c8e7d1706b47dcd252b08434a05ca86d144b192f17b4778632f06c96d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aliases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv4Address")
    def ipv4_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4Address"))

    @ipv4_address.setter
    def ipv4_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8874e58bd081b1ec11ca6914576b982841772cb0dce862ba802ddfe109bea58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv6Address")
    def ipv6_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6Address"))

    @ipv6_address.setter
    def ipv6_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3389a65b9f1c0ed4ec96b86b59fb82702bb299f4eab950caec34ab8205ce07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b168f9191309b0bddfce97e99839843eff4bbf0b7eaf19dffd0ca24da3adb62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNetworksAdvanced]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNetworksAdvanced]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNetworksAdvanced]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443a09a2278608dcac2dd6e3935650d7f67af04fdad4136b87b432863b382f7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerPorts",
    jsii_struct_bases=[],
    name_mapping={
        "internal": "internal",
        "external": "external",
        "ip": "ip",
        "protocol": "protocol",
    },
)
class ContainerPorts:
    def __init__(
        self,
        *,
        internal: jsii.Number,
        external: typing.Optional[jsii.Number] = None,
        ip: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param internal: Port within the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#internal Container#internal}
        :param external: Port exposed out of the container. If not given a free random port ``>= 32768`` will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#external Container#external}
        :param ip: IP address/mask that can access this port. Defaults to ``0.0.0.0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ip Container#ip}
        :param protocol: Protocol that can be used over this port. Defaults to ``tcp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#protocol Container#protocol}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb4e25a60e4a27c8dc2a520ce3fc4bdc839c3781ae729e73552b5e727e126c2)
            check_type(argname="argument internal", value=internal, expected_type=type_hints["internal"])
            check_type(argname="argument external", value=external, expected_type=type_hints["external"])
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "internal": internal,
        }
        if external is not None:
            self._values["external"] = external
        if ip is not None:
            self._values["ip"] = ip
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def internal(self) -> jsii.Number:
        '''Port within the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#internal Container#internal}
        '''
        result = self._values.get("internal")
        assert result is not None, "Required property 'internal' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def external(self) -> typing.Optional[jsii.Number]:
        '''Port exposed out of the container. If not given a free random port ``>= 32768`` will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#external Container#external}
        '''
        result = self._values.get("external")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ip(self) -> typing.Optional[builtins.str]:
        '''IP address/mask that can access this port. Defaults to ``0.0.0.0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#ip Container#ip}
        '''
        result = self._values.get("ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Protocol that can be used over this port. Defaults to ``tcp``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#protocol Container#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerPortsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerPortsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73088e92b65cce435194e5b320ee52fc8737c5cc2c7142ce2330c5406996910c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerPortsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6604b3aae38d9b3bf34bc2c3c97b102ab7b1838aa863990e9853a4dd542b429b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerPortsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0817b5bc50eb3a13a8dfed840d6c0c44e3bf72ef68462e92eae744cdd3ef214)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b0b6c7b09f47d697b7077d520bb4d1803c9ad60861f50e2bbd2578c35a42079)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c5b5469131f8688b2393227a62e2e56fac9f44d76b19622108d8e0c9559e071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerPorts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerPorts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d51c3379cc670cbddd53ca4945ea0170d6677e303a53361b9af9506c0bc821c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9a84a72ee16381a730ad0e9ea4778033122472742540222444200ca00e8c567)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExternal")
    def reset_external(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternal", []))

    @jsii.member(jsii_name="resetIp")
    def reset_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIp", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @builtins.property
    @jsii.member(jsii_name="externalInput")
    def external_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "externalInput"))

    @builtins.property
    @jsii.member(jsii_name="internalInput")
    def internal_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "internalInput"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="external")
    def external(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "external"))

    @external.setter
    def external(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6794732795eb9a7b126bc1603b789a3e39f6b2dbe6f1e124034af10eebb12703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "external", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internal")
    def internal(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "internal"))

    @internal.setter
    def internal(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2dc45a6540a613da10e62a7b88eb64c83a1dabf3c5d81910c18787dbdc1c84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2147ad66bff4a7909a4e7ee4019f09d7714528c7a99cebcbeb6eae52200da66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c3d86973df68cbf2e2c6665c239708fab3afde576deb0910b8f0158cc39adff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerPorts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerPorts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerPorts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d77cead80c21852400598ac48e64bb50887d809c3198396474edfd86d9f3d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerUlimit",
    jsii_struct_bases=[],
    name_mapping={"hard": "hard", "name": "name", "soft": "soft"},
)
class ContainerUlimit:
    def __init__(
        self,
        *,
        hard: jsii.Number,
        name: builtins.str,
        soft: jsii.Number,
    ) -> None:
        '''
        :param hard: The hard limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#hard Container#hard}
        :param name: The name of the ulimit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#name Container#name}
        :param soft: The soft limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#soft Container#soft}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc59af47d65027182e95104dcc3169f00c9a7e41f7d1a0c392efc430a55db3e2)
            check_type(argname="argument hard", value=hard, expected_type=type_hints["hard"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument soft", value=soft, expected_type=type_hints["soft"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hard": hard,
            "name": name,
            "soft": soft,
        }

    @builtins.property
    def hard(self) -> jsii.Number:
        '''The hard limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#hard Container#hard}
        '''
        result = self._values.get("hard")
        assert result is not None, "Required property 'hard' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the ulimit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#name Container#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def soft(self) -> jsii.Number:
        '''The soft limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#soft Container#soft}
        '''
        result = self._values.get("soft")
        assert result is not None, "Required property 'soft' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerUlimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerUlimitList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerUlimitList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fec1ea1b4611fb6f14f003ad87b5763f274e8304d7a02e08a0ce967efd15a07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerUlimitOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637a2783120cf384477ec2c86070856bf6cd465b6604a576a7bc890f38459f2b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerUlimitOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e96735e74fc83aa4ebbb4d05d2b215ead819df1c44e676caf15182cb6eb02533)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfbc5167f5f23835eed18481bdf4cc9dbeac1abe2ef5f557a9583dbefd12202a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c01fba7049d4282886d5335bb84abb3037b81672110db2cdae6e72f050517f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerUlimit]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerUlimit]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerUlimit]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f247000868c32008878a7acecfb72f423a8a06b640d68cb1d43abdb73ac4e366)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerUlimitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerUlimitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59dc2df3f436a9aafec4b30d9674c9ff393820ca6b53234afb7f8ea6540e91d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hardInput")
    def hard_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hardInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="softInput")
    def soft_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "softInput"))

    @builtins.property
    @jsii.member(jsii_name="hard")
    def hard(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hard"))

    @hard.setter
    def hard(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab804314a3f0e85efe764b20d18b2ffeb9aef0cbaca5bf4297cb4a69e8eb86ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hard", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d194cf920f773a70e0ca7c94f39287fd1d74170ae461087e0180ab6cc4335b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="soft")
    def soft(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "soft"))

    @soft.setter
    def soft(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c14e3666760e0459776fc8cb4911cb79e3d2d91f3cde6764f7e7b03bfafe52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "soft", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerUlimit]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerUlimit]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerUlimit]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1759f92cee8c0e88afab4feca7c84de1827137a1018dc10442411511d255d39b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerUpload",
    jsii_struct_bases=[],
    name_mapping={
        "file": "file",
        "content": "content",
        "content_base64": "contentBase64",
        "executable": "executable",
        "permissions": "permissions",
        "source": "source",
        "source_hash": "sourceHash",
    },
)
class ContainerUpload:
    def __init__(
        self,
        *,
        file: builtins.str,
        content: typing.Optional[builtins.str] = None,
        content_base64: typing.Optional[builtins.str] = None,
        executable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        permissions: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        source_hash: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file: Path to the file in the container where is upload goes to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#file Container#file}
        :param content: Literal string value to use as the object content, which will be uploaded as UTF-8-encoded text. Conflicts with ``content_base64`` & ``source`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#content Container#content}
        :param content_base64: Base64-encoded data that will be decoded and uploaded as raw bytes for the object content. This allows safely uploading non-UTF8 binary data, but is recommended only for larger binary content such as the result of the ``base64encode`` interpolation function. See `here <https://github.com/terraform-providers/terraform-provider-docker/issues/48#issuecomment-374174588>`_ for the reason. Conflicts with ``content`` & ``source`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#content_base64 Container#content_base64}
        :param executable: If ``true``, the file will be uploaded with user executable permission. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#executable Container#executable}
        :param permissions: The permission mode for the file in the container. Has precedence over ``executable``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#permissions Container#permissions}
        :param source: A filename that references a file which will be uploaded as the object content. This allows for large file uploads that do not get stored in state. Conflicts with ``content`` & ``content_base64`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#source Container#source}
        :param source_hash: If using ``source``, this will force an update if the file content has updated but the filename has not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#source_hash Container#source_hash}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a99cf8bd42d7e72b6f951996bd6f1614a91a8b8025d0a65c7f01d6d661942c5)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_base64", value=content_base64, expected_type=type_hints["content_base64"])
            check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument source_hash", value=source_hash, expected_type=type_hints["source_hash"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file": file,
        }
        if content is not None:
            self._values["content"] = content
        if content_base64 is not None:
            self._values["content_base64"] = content_base64
        if executable is not None:
            self._values["executable"] = executable
        if permissions is not None:
            self._values["permissions"] = permissions
        if source is not None:
            self._values["source"] = source
        if source_hash is not None:
            self._values["source_hash"] = source_hash

    @builtins.property
    def file(self) -> builtins.str:
        '''Path to the file in the container where is upload goes to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#file Container#file}
        '''
        result = self._values.get("file")
        assert result is not None, "Required property 'file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''Literal string value to use as the object content, which will be uploaded as UTF-8-encoded text.

        Conflicts with ``content_base64`` & ``source``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#content Container#content}
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_base64(self) -> typing.Optional[builtins.str]:
        '''Base64-encoded data that will be decoded and uploaded as raw bytes for the object content.

        This allows safely uploading non-UTF8 binary data, but is recommended only for larger binary content such as the result of the ``base64encode`` interpolation function. See `here <https://github.com/terraform-providers/terraform-provider-docker/issues/48#issuecomment-374174588>`_ for the reason. Conflicts with ``content`` & ``source``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#content_base64 Container#content_base64}
        '''
        result = self._values.get("content_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true``, the file will be uploaded with user executable permission. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#executable Container#executable}
        '''
        result = self._values.get("executable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def permissions(self) -> typing.Optional[builtins.str]:
        '''The permission mode for the file in the container. Has precedence over ``executable``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#permissions Container#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''A filename that references a file which will be uploaded as the object content.

        This allows for large file uploads that do not get stored in state. Conflicts with ``content`` & ``content_base64``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#source Container#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_hash(self) -> typing.Optional[builtins.str]:
        '''If using ``source``, this will force an update if the file content has updated but the filename has not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#source_hash Container#source_hash}
        '''
        result = self._values.get("source_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerUpload(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerUploadList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerUploadList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec37b2da549c82f1c9ba8f7d2871859ef77ee942586fbf98ef13a592e050e216)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerUploadOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4544081f4549b8eddf21f453e84d85b199b1a46ada799b2bfaf5945eb23eab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerUploadOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f1486ef1002359fe2d339eccfb9ae54cece081078ab70a887fa73c34c9c30e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b08edd13b48dc582fc5a0a503430e7b4cc162ce529dafa6534fa356b23232d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f316ad7762e425dcb9c28d6e1139ffc0791b421c3d09dad3b578396440bb9e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerUpload]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerUpload]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerUpload]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a66cdef2af9b71cf33c3d21c90957137ff9e47415985d6fbdb10d375d27aaa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerUploadOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerUploadOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff823a79183af4d59dd32a15bf89467f8363ee82fb5c15e0fd4c2fbeb5c0bbf5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @jsii.member(jsii_name="resetContentBase64")
    def reset_content_base64(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentBase64", []))

    @jsii.member(jsii_name="resetExecutable")
    def reset_executable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutable", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @jsii.member(jsii_name="resetSourceHash")
    def reset_source_hash(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceHash", []))

    @builtins.property
    @jsii.member(jsii_name="contentBase64Input")
    def content_base64_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="executableInput")
    def executable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "executableInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceHashInput")
    def source_hash_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceHashInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__addcffbb67ab77f2cc268aad9439e2f146d1836db3b64bbfb46522324eb79fa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentBase64")
    def content_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentBase64"))

    @content_base64.setter
    def content_base64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af77bef402eb392a3d9ab5524dc1ad8669f6b017cc1d581a470badcdfbcdf9a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executable")
    def executable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "executable"))

    @executable.setter
    def executable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6050de47e8bbda8265ae77fd75db2096b508eba0e0f5150d984c81cec8cd5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "file"))

    @file.setter
    def file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d62dce7c493856004dea74a7b4889d3ef6f0ba556b4a104e3327af25be7328e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "file", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissions"))

    @permissions.setter
    def permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc3953608a3c946d02e755aeffbc7c422c805ec0a4acc8f02025a6321fbb69ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69e78774c6bba64b1fb10abeddd50d8edd11f0496c42cdd7db422348afed7f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceHash"))

    @source_hash.setter
    def source_hash(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c477d58d379ab4c1104da1b918670db3200815690373b655f6c555389f7f85f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceHash", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerUpload]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerUpload]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerUpload]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9feba0e275d8b028e5324863ae06019d1cfd7716afec5b6d7ec55753a95a99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.container.ContainerVolumes",
    jsii_struct_bases=[],
    name_mapping={
        "container_path": "containerPath",
        "from_container": "fromContainer",
        "host_path": "hostPath",
        "read_only": "readOnly",
        "volume_name": "volumeName",
    },
)
class ContainerVolumes:
    def __init__(
        self,
        *,
        container_path: typing.Optional[builtins.str] = None,
        from_container: typing.Optional[builtins.str] = None,
        host_path: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        volume_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_path: The path in the container where the volume will be mounted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#container_path Container#container_path}
        :param from_container: The container where the volume is coming from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#from_container Container#from_container}
        :param host_path: The path on the host where the volume is coming from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#host_path Container#host_path}
        :param read_only: If ``true``, this volume will be readonly. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#read_only Container#read_only}
        :param volume_name: The name of the docker volume which should be mounted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#volume_name Container#volume_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6745638491d263da41079bf3c9d9a3c5c59f747c9fdaf6e29eb3201495f1b1bd)
            check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
            check_type(argname="argument from_container", value=from_container, expected_type=type_hints["from_container"])
            check_type(argname="argument host_path", value=host_path, expected_type=type_hints["host_path"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument volume_name", value=volume_name, expected_type=type_hints["volume_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_path is not None:
            self._values["container_path"] = container_path
        if from_container is not None:
            self._values["from_container"] = from_container
        if host_path is not None:
            self._values["host_path"] = host_path
        if read_only is not None:
            self._values["read_only"] = read_only
        if volume_name is not None:
            self._values["volume_name"] = volume_name

    @builtins.property
    def container_path(self) -> typing.Optional[builtins.str]:
        '''The path in the container where the volume will be mounted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#container_path Container#container_path}
        '''
        result = self._values.get("container_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def from_container(self) -> typing.Optional[builtins.str]:
        '''The container where the volume is coming from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#from_container Container#from_container}
        '''
        result = self._values.get("from_container")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_path(self) -> typing.Optional[builtins.str]:
        '''The path on the host where the volume is coming from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#host_path Container#host_path}
        '''
        result = self._values.get("host_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If ``true``, this volume will be readonly. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#read_only Container#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def volume_name(self) -> typing.Optional[builtins.str]:
        '''The name of the docker volume which should be mounted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/container#volume_name Container#volume_name}
        '''
        result = self._values.get("volume_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71b58f4f5cd341111dcb4183d38ec8ac49a6dc7c768175471d5cc47b6a740bed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ContainerVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ce82b0bb67a61e1dc158b6918ebbe993a0292aa94d7f7457aabaaf81d9fcfe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f63334c49d9f4fbc506b1983e0d418d8ba4db7a2c999ea0c359416ef0ab996)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccb21cbf944b77196c352ac6fa88cbe7cb07c5221861102c497b8717500eb104)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25d216290f7b2106b4cdfe2b53240374f5db6f97536f3daca7be9f7b70bd715e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf6efc8f660a86dd4ddc9fb610b2d6428f2ca372a12a1dc6d4ed9d6087578ba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.container.ContainerVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5c3b3f45f74efdb190fd0a78b0241801c0c3056b108d7086050e4a131c3fb00)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContainerPath")
    def reset_container_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerPath", []))

    @jsii.member(jsii_name="resetFromContainer")
    def reset_from_container(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFromContainer", []))

    @jsii.member(jsii_name="resetHostPath")
    def reset_host_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostPath", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetVolumeName")
    def reset_volume_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeName", []))

    @builtins.property
    @jsii.member(jsii_name="containerPathInput")
    def container_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerPathInput"))

    @builtins.property
    @jsii.member(jsii_name="fromContainerInput")
    def from_container_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fromContainerInput"))

    @builtins.property
    @jsii.member(jsii_name="hostPathInput")
    def host_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostPathInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeNameInput")
    def volume_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="containerPath")
    def container_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerPath"))

    @container_path.setter
    def container_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320510974ad9c2f418c15509052d651434b3bd584d1826a363c84ac6072e36f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fromContainer")
    def from_container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fromContainer"))

    @from_container.setter
    def from_container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d60bb31c8cfe0b87ac14a901e0a5a7cb01c713397b1d383342e721fb7f814d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fromContainer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostPath")
    def host_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostPath"))

    @host_path.setter
    def host_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ef31de095e7e2320d9ded21e7cf5a0bac86946f34310387198a09d581ddb76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostPath", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__06d922def479099314664cc013313962ea821d2b528aa5a07337dedfcd4a21a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeName")
    def volume_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeName"))

    @volume_name.setter
    def volume_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a7ab7d17b70d9ed337c4d7ae1004d11a00a4ab7da86a75ba65f2beebadf433c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__401dc3edc98a286426ed9f254e519f81d15faae2cdba9afa419db430c8c50a12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Container",
    "ContainerCapabilities",
    "ContainerCapabilitiesOutputReference",
    "ContainerConfig",
    "ContainerDevices",
    "ContainerDevicesList",
    "ContainerDevicesOutputReference",
    "ContainerHealthcheck",
    "ContainerHealthcheckOutputReference",
    "ContainerHost",
    "ContainerHostList",
    "ContainerHostOutputReference",
    "ContainerLabels",
    "ContainerLabelsList",
    "ContainerLabelsOutputReference",
    "ContainerMounts",
    "ContainerMountsBindOptions",
    "ContainerMountsBindOptionsOutputReference",
    "ContainerMountsList",
    "ContainerMountsOutputReference",
    "ContainerMountsTmpfsOptions",
    "ContainerMountsTmpfsOptionsOutputReference",
    "ContainerMountsVolumeOptions",
    "ContainerMountsVolumeOptionsLabels",
    "ContainerMountsVolumeOptionsLabelsList",
    "ContainerMountsVolumeOptionsLabelsOutputReference",
    "ContainerMountsVolumeOptionsOutputReference",
    "ContainerNetworkData",
    "ContainerNetworkDataList",
    "ContainerNetworkDataOutputReference",
    "ContainerNetworksAdvanced",
    "ContainerNetworksAdvancedList",
    "ContainerNetworksAdvancedOutputReference",
    "ContainerPorts",
    "ContainerPortsList",
    "ContainerPortsOutputReference",
    "ContainerUlimit",
    "ContainerUlimitList",
    "ContainerUlimitOutputReference",
    "ContainerUpload",
    "ContainerUploadList",
    "ContainerUploadOutputReference",
    "ContainerVolumes",
    "ContainerVolumesList",
    "ContainerVolumesOutputReference",
]

publication.publish()

def _typecheckingstub__a48ec2bf472b6e9fe11b252b3b812812f009c78cda3f9397468250c2087edb1f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    image: builtins.str,
    name: builtins.str,
    attach: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    capabilities: typing.Optional[typing.Union[ContainerCapabilities, typing.Dict[builtins.str, typing.Any]]] = None,
    cgroupns_mode: typing.Optional[builtins.str] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_read_refresh_timeout_milliseconds: typing.Optional[jsii.Number] = None,
    cpus: typing.Optional[builtins.str] = None,
    cpu_set: typing.Optional[builtins.str] = None,
    cpu_shares: typing.Optional[jsii.Number] = None,
    destroy_grace_seconds: typing.Optional[jsii.Number] = None,
    devices: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerDevices, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns: typing.Optional[typing.Sequence[builtins.str]] = None,
    dns_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
    dns_search: typing.Optional[typing.Sequence[builtins.str]] = None,
    domainname: typing.Optional[builtins.str] = None,
    entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
    env: typing.Optional[typing.Sequence[builtins.str]] = None,
    gpus: typing.Optional[builtins.str] = None,
    group_add: typing.Optional[typing.Sequence[builtins.str]] = None,
    healthcheck: typing.Optional[typing.Union[ContainerHealthcheck, typing.Dict[builtins.str, typing.Any]]] = None,
    host: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerHost, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hostname: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    init: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ipc_mode: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    log_driver: typing.Optional[builtins.str] = None,
    log_opts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_retry_count: typing.Optional[jsii.Number] = None,
    memory: typing.Optional[jsii.Number] = None,
    memory_swap: typing.Optional[jsii.Number] = None,
    mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    must_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_mode: typing.Optional[builtins.str] = None,
    networks_advanced: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNetworksAdvanced, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pid_mode: typing.Optional[builtins.str] = None,
    ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    privileged: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    publish_all_ports: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    remove_volumes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restart: typing.Optional[builtins.str] = None,
    rm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    runtime: typing.Optional[builtins.str] = None,
    security_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
    shm_size: typing.Optional[jsii.Number] = None,
    start: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    stdin_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    stop_signal: typing.Optional[builtins.str] = None,
    stop_timeout: typing.Optional[jsii.Number] = None,
    storage_opts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    sysctls: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tmpfs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ulimit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerUlimit, typing.Dict[builtins.str, typing.Any]]]]] = None,
    upload: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerUpload, typing.Dict[builtins.str, typing.Any]]]]] = None,
    user: typing.Optional[builtins.str] = None,
    userns_mode: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    wait: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    wait_timeout: typing.Optional[jsii.Number] = None,
    working_dir: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__7a117cfafff6e940fed0dc84de3a8f0c0b6e1f1a431b4f26fe5952f09d700cbc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58659796eac9660e8a92a11acea15c16b61035b5b282aabe0e88d43adf5b6f54(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerDevices, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2aef3baddb3762dcc8ea8e52021886544d37f9574ad37325b114fa61e200054(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerHost, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3ba4891e1e8f667363d8f5586bff03f79911344714cd6c2a067810f31f302c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e66f87b3e1d235fdb0726cb6f76ca02bb6b61a9b48990255d604b382c41bfad(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerMounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26ba0dd23b2e4382ab4e44f5b1179ecb61692da2da10a969d40a8a14e437217(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNetworksAdvanced, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8472b00f573fcfe342412486e287b7cb21c7ef5b0eedc352b112e640b3d3adb9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerPorts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3561b9173ce72dcbc2c60c7ac5f12c5a625ea8dd3f7127a0b9979394325b4cc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerUlimit, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd5e853f5d69cb38f6d69d31d5b6829e3c9ac76b43fe08813a7e983117dde74c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerUpload, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6737613f040694b10de23b51e3fc2c7e34b5fd220fd0b24f6184197113b6b20b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb274bdb3538465984fdaf28708a86154690b9e80df70fdb70a637268d24fc0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98cd52ff440d1bd2151bd18349fd965fedfe4bbc4ac82aa5ced37f3e1ad34f9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f84d6538674bdd3ecb66d195c1c0d758b817795b47b1329fec7fc2003e93407(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f4886d5ad8b53829cec57515f09c0936b1dd144c66f208d042bdb8fbcb58ef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329a8989a63e99758c1de586411f59ef500fab9df562d8beebf19395ab8da916(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fae00253e7ecc66830e1564df1b9fdfc33092b627e7fb79ad5e4499123e44de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b15256ad7563113a5d03c63de55adde700242dbcc6d952e85d00af13b5073e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1306b7d55e8e6610284ae8da440519ede69026dddba4bc6be078a3e874998684(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dbd8e7a75b71a36a2e1ccf9b4f19b5a734c751e45b7d452b899997087e04d06(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5905bd813ef43e7c4b96565e74539190415a0eb4c71209c8d5d686bff8594b57(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19793de8a2eb8ce1dbffcd2ae850fbc7c2e184822a67c3e2959081cfac0ff236(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da338db259aaa8d39495244eb4730e4efba3d5795834766991f8af31321bcffb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4fff8bd560291e23d8d75e7490bff5dfd46664fd2f452c4e31c9048b7cd86c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16947c4e02f9ade0587c2c1d10fd686ea2bd8e2e65ac386d2be5025ca82e792(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__413841d98152142bdb858457f46024aee50da2d46600509aebe2a56255e2d110(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ca7fd4c5f36d1c39be4f76264816708f0796ff1685fbc20777813766a2d7b6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abcd1784a03da45e8ad5009395a02a9ea51dde31ce8edfa2ceaf58525466331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be65dd1b0b3e60f099f9a5e9d09598c7aff60b9b6c3eee2be913a67e09ef202d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19dea8604f5eca052ffd44225a4ad570116ae3c4d48da5178a503dcd8c302da3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca02e053996d784f380588c33ebbec1e76cbbd69a0133dc821f132f38ef382e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8aa8b2c665f91c9b68d083b01e56c69945a72cbd6aaf8af72d3acfb18066250(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016dd2faa91127b4007aa7346f65561294c9e39af3b6101b94fc33327300bd70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6f35abeabd4b2ca35db5b1051271efb0202c4cb9e9c51b8f975260b7bdfd25(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4c5b2eb265acd751a55b6735f4c0870d356051cc022f8cd5c802c585e14bb8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015625d5a5fd5d75270804974997b1897a5effe1ea03c0aa173cf83a9ce9965a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f26871c2eafb93fdcbe28aed36e8dcbac161138d77152866d748b107725595(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b4bb89faca6478a54c2b061ad56d5d1fa85a3463952533b44daa977799866a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cdb3d44f5d4194bc9317f70e76e000c7a848ae5eb5dc8ba12f5f0fd6fa6be73(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb026e86f4c6dfb4790113f182e90d3e0d102cd061082f11905907974acc7b63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c005cd8aedc9aabf75b7e0ec6fea3dbfaf8cf7043516255b9b235e8d6bcdd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5804756e6d576ef609b393913fb543c3c7718bd0352f017290de6211906a9f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3e460d5f9a26e4cc768ddeed2db77f3710a08feb387e293edcefcc1145d23d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a95752aa9d3ef3c1e8118f3d28294b5e5c9047cb7c128a7b2251657756e6dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b40943302e537dd0952c761bce598cf4e76974f8588c1d3e01c474f024c0928(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb87b5fdb4e3589d4c912da1400aacd8c491ad7d4645f30922d6796e4ac0396(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120d1eea976e192c1fb7d238d9b0f0498600071646ffeeedfc5b586bf5509c1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2eea7eb89d963187709ee945cb31aad732f9ba4d2f7deec020e69fa3988b87(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faec2e687b6e767361362f8b8409f134cdd0c1a585b0bcdc4463879cb6ad4886(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d148c335d2eb0e59fbbe9b0b32481525ee4fef5ef09bd805f2ee4e55464b73(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f57fcc37c326b9dd6b787f1c924a6aaf4e97c24911383ca7753b634ba3dd91b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54911310154c0da8bed033174f4b69bfbebc4f8d238a9078b1fc95234150ea0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51145e7afb967a391c9aa38e5046c7c5291eb51e1df5d62959a75de64fc7fafe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28bd4ec32109be9e9bff28c7abccbcf780afba36bd4b6f04ebaa868f259f3f4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e34e0815bb868d16484878af5fefdf4c7287f1dc4cbb8582dbd8a859787a83(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a773e2ad26c6a5d8fac23b3c69775083fa39e713a1bd5c1250c5e0163409819(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e65c3f9cc4077d44998621654b1bc23cc5f763c23497719d8a6ca49d8473af3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1240ed7aafd9cfe1e0581842678d7c11eccb62148cd0996735bc134aa33354ab(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__184ff37f1ed05db343b6e99c042e4569e8c080b450708b48a93ae4e934648e57(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f550e02ebecc9ae49ad3543e57a173a310a41019b6380a8e77e78a3e6b9aa0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa71d928b9a2b960e62d888ec036bb2332f67310e463a1e60dbc9b3a531bb08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c23505cf016507da21996d07d47161d7173e88968a2b86132cf81f0d5fef6f0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b192d3669c40cfd6e3659be1c5802670a8c9fb5f88f58334a228093ced057d3b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c9403f276a1f08fdf14eb85c588d45131cfef64a224234999c7427ebcd9a8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a65902a2a3f73dc940f2671ac040643fc443224764d6023c88df51634ec901(
    *,
    add: typing.Optional[typing.Sequence[builtins.str]] = None,
    drop: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb36ee23d7594966c5a21813dc63114fc910ef0969a3460c977266565762155a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41d4d42adfbb7450a312dd07c9d8253159a356e7d33f9be311a9cbec93771463(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645640e83b459066f10b4d04e07647d59ceb816bcd48e6dc575b069903ed9a3f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41d269daed3c0a1d6c1d0d67df7db335efd31c158460d813bdaec9a1c69a653e(
    value: typing.Optional[ContainerCapabilities],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1985321a167573487d759bff6561898e2f12ca869786a5ebc7b8ef498c89a9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    image: builtins.str,
    name: builtins.str,
    attach: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    capabilities: typing.Optional[typing.Union[ContainerCapabilities, typing.Dict[builtins.str, typing.Any]]] = None,
    cgroupns_mode: typing.Optional[builtins.str] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_read_refresh_timeout_milliseconds: typing.Optional[jsii.Number] = None,
    cpus: typing.Optional[builtins.str] = None,
    cpu_set: typing.Optional[builtins.str] = None,
    cpu_shares: typing.Optional[jsii.Number] = None,
    destroy_grace_seconds: typing.Optional[jsii.Number] = None,
    devices: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerDevices, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns: typing.Optional[typing.Sequence[builtins.str]] = None,
    dns_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
    dns_search: typing.Optional[typing.Sequence[builtins.str]] = None,
    domainname: typing.Optional[builtins.str] = None,
    entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
    env: typing.Optional[typing.Sequence[builtins.str]] = None,
    gpus: typing.Optional[builtins.str] = None,
    group_add: typing.Optional[typing.Sequence[builtins.str]] = None,
    healthcheck: typing.Optional[typing.Union[ContainerHealthcheck, typing.Dict[builtins.str, typing.Any]]] = None,
    host: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerHost, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hostname: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    init: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ipc_mode: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    log_driver: typing.Optional[builtins.str] = None,
    log_opts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_retry_count: typing.Optional[jsii.Number] = None,
    memory: typing.Optional[jsii.Number] = None,
    memory_swap: typing.Optional[jsii.Number] = None,
    mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    must_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_mode: typing.Optional[builtins.str] = None,
    networks_advanced: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerNetworksAdvanced, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pid_mode: typing.Optional[builtins.str] = None,
    ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    privileged: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    publish_all_ports: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    remove_volumes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restart: typing.Optional[builtins.str] = None,
    rm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    runtime: typing.Optional[builtins.str] = None,
    security_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
    shm_size: typing.Optional[jsii.Number] = None,
    start: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    stdin_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    stop_signal: typing.Optional[builtins.str] = None,
    stop_timeout: typing.Optional[jsii.Number] = None,
    storage_opts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    sysctls: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tmpfs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ulimit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerUlimit, typing.Dict[builtins.str, typing.Any]]]]] = None,
    upload: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerUpload, typing.Dict[builtins.str, typing.Any]]]]] = None,
    user: typing.Optional[builtins.str] = None,
    userns_mode: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    wait: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    wait_timeout: typing.Optional[jsii.Number] = None,
    working_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146d561b3aa3ec7af00e9c695ba6e56b56c66fc65b26bbed8137cce8e221a52d(
    *,
    host_path: builtins.str,
    container_path: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3286d2c6e6cdc6a601592634ea73380c740f66b0894c4b5abefd59e0a2f7d181(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2fa5a8a14e30c40cf5c023aa26e6dd870c04b3357b7dd60d18d2becc89a92d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307eb655a3de46ab4efe879ceaf47ebb9f6561a37ac18451ec7ff1fd2521c606(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a20ea4bf0a4e4cec9887f8cc55f0c6eaaf15eff25596bb37c7db5e582afbfda(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc6e95e7591990389cecc8600252e3d7de050add10afcda73dea55cc233ca4b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77e6ae236df7bdba65a64fda882d05b216a234c082df2099ffd3c22046abb9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerDevices]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45beccb66cfd6f150ee2bd24e6481212d81a29b9cbf14249b0a2e69f26658518(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c366a6f1590adc22fcd578c01cb08d304388c3f7416eee3c90c856290ed94e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e8843735de6d75bcba52e570ed5c41c6c6cfc54a08fee163519c3eb93ebfeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049ad0e59afc356f5dbd4e3fd2005f6a0fb8b578c095adfa92a90898958d7f4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73caa9346682731462bf8759e916531ef8936189bc211b87aff3c12b70d04d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerDevices]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9432b7d78f2e610b6c54c84150a2b48d7150a28ad33e8e0e45700acaed7b02(
    *,
    test: typing.Sequence[builtins.str],
    interval: typing.Optional[builtins.str] = None,
    retries: typing.Optional[jsii.Number] = None,
    start_period: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea936c2aecdf4da07fc31fbb5190662bc94dc64cffe8f8cbb1a855beea4f870e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376955f3161270188560145a5e2c0e35a433d95f51e5eed7501c7c54c50154e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e796cbc50c5b40b7e17091fe1f95f4c6cf40e54a74e3475d8ba0f9adfd3181(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b646d3724103c7fb549d6e6d38cd71bc6655e93c3c58af93df8b08a61089399(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a8bf18656a953fcdc16f9236af6dcdce4c69b9b565d41332fd03004a593e52(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f34a219127c0f07ca720152e5e32c861c8b26b825d16920e66ecef66b9dd60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8192d624d798540d9d1cf16b6cb1693cf445c2573730dcb547967aa8f14743e8(
    value: typing.Optional[ContainerHealthcheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d740eb1d81cf48185aad5246c96f804525587268943cac88414eee7b50fc60(
    *,
    host: builtins.str,
    ip: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886903115c2345733e1e11caf4a97ddfa9e62329bbef55ce4afe10b9a44d9fdc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1390991ec2e39c6c12968293141e06cb02079db64fe906199836e5aa60cdec2b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a962951bfdfe4f707ea800b8ab051156a17308a5e94745123b46632c93f7aa0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e7943e58bfc99e64d6256218d84a75d96e4a870cb7309241981b3230b5ce97(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3df94434c766f371e2eaf509048250c0d51cbd874838dfdbd80769f5aa31ace(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a90cdd9c92a85d25dab4bffc745868ab4a9f5639b5ec6f7e79f079d3644e85(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerHost]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53827f9982e510c6e3a1b6a19a5a4ce7f08eaae9c932a30c84976ff20778dd4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f249fc27646414edbae696ad50365246fb63e0cb5d6ac5eb5b96814261e6dc2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e8034bc9f198770280f71442e68d94337ec3cbcdf47d857bee862a16b0d964(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d4be6a2799602751c095c6013ddc2d12fed9b1cbc211851c0ecba8ed0c928c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerHost]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf90c1ae6f2e0b535b5e407371d3fe8e277b8f81810a33882fe4ff1490ba5695(
    *,
    label: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa790d79e6e3408cf7f27ee2360824ea05926d3a99f80c4ec642e0e86abeef4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7d24c4c0b4a996ca91a8b543b12a0d54ade1513bf4e46810460c3488dedafd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b098d34ec778329fa4c6aa54dff62bee27144e645bed3d4c56b453a4ac3fb49b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68fd8dff9315ff7dd21e5ce9674a59dc6d6952018680a4af7416b136c433423(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d420afeecd71116a6916b1e36c10205a547767783b76a90bb40588939d967e2f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8823069a80a3a6f36ad4461cdca45457a8a23341347602c8dbc81621d83ce41a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4ff39618ab76ec95ff48ed10cd591d77e7ebeb01bff1e8dc27a28071f5b37d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced1ed5db218f165cfc12bed3c45b930842ab31e5bddb183b94fdf26322f9ab3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49a73b0d720c46da71694e55ce4bc5fe7de50e9774f146b3b429b66698ed855(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4730ed0ff620921e465be21844a9fb20912333681bc39c8c61e7237d4d1ed0e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36576a29d4694529a5b5fdc7006b4db9d468b7e4c3423bb53ce20ce5887cd2a(
    *,
    target: builtins.str,
    type: builtins.str,
    bind_options: typing.Optional[typing.Union[ContainerMountsBindOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source: typing.Optional[builtins.str] = None,
    tmpfs_options: typing.Optional[typing.Union[ContainerMountsTmpfsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_options: typing.Optional[typing.Union[ContainerMountsVolumeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05215177c99a750e909ea2dcb1e3573adc5ddcffd355f668eee0ee2c6381701b(
    *,
    propagation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1778ec6a97c5fccf7439e0249f19e4e3547aea0b2cc729c296d4b8d51f2b2d90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b83c96a1a012a961fe6975dd30c7785b80597303a2ed67d50b1692290aad60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7923a22b8cc349b67b4bb76d42c92c1e2ba381b85c477f60de930c2c509aa1c(
    value: typing.Optional[ContainerMountsBindOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7633d71a5f83a7aed083b94f1047b3e0b5c611dcd5b7e5825890d560f7ef047(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467008150c788c9ad2081ed809cdebb33243fa4d86dbcbb0d6e6e2bad79c1633(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fdbd933e41e5a8443ed75a80c6ac37d75efc20f06577013f1cea8b25af9304b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c63ca0aedec654b4aee7c7e47cd199297a7a311172965d3ebf972c22a0ba22f9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579062fd51a1559a8748e5ee2b277fec876ea799c2d9a7141bb34dc670da0285(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff9ffe9406f71bbb0d98415e864daf2be84982a220d041f94ae19336fc5db7bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerMounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c9c02ebfed7fff7acf39f77f043072cb7d4c1906b784af4b092bb282e0e252(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5098a27e03e8f53106fa0ae3e92fe83e32bc3417735e9131b6a0fda5b3f5c48(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b83bc93ef9b814021248785419984990df2a57fa8d96c9830c3ffcf6c67bdb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83a3e5a623535de6d340f53b8a66fafbdd65a67839c9befadd53c1ac489d572(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c23d1d5b5fc53fadf43059c0731f836cda90b71020c7ddf4bf07a5057a089e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6fb56ecddf30b21c255d3850f535e4fe42acf38d5678efe48c8cc93948340ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerMounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a28b6ccc911896a65cecfc1c8d445ae492e4452bd806b9cb1ec28145681e8d0(
    *,
    mode: typing.Optional[jsii.Number] = None,
    size_bytes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4db6bd9d9d8cc618fcbf092533c642ff113975f753d210b224ad1a7d7049f9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b830839d135616b369ff13d17919dd711e0b7e67c8fb17f6caa64ace938b4be0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee6eb8103fc7346e11e4017e657e721d2a85c8d96198351d126ae222cdc2694(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df0761a3af0c7821029831d2218635e4a0d5fdaff550f6a7e20e81c42192ecd(
    value: typing.Optional[ContainerMountsTmpfsOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e57bf5e5517ab50538e55f56afa5df117be0622e1e391a42a3dfd77a9cf34ad(
    *,
    driver_name: typing.Optional[builtins.str] = None,
    driver_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerMountsVolumeOptionsLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    no_copy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subpath: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a5ee98a467321cf1b2b71a821c63bb3bfb31930b4ca02bbca4369011cc8f65(
    *,
    label: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2b4eba841bf1e4b790d3e65b9a494e55693a336f8708d8a476903bbee5be96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d1af0b9c130580f1e81ed07a6af28e45317b7fec6afd2cbfeaeca89b5a2685(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cde24a06d3b59a43795aecbc5c15017237e1beb4cbe8ac98f0e2832b8958a88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb1688a25d041d2917f89292d71fda5e8430925ebc28ff9d15923b801f30968(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f16ef99323ee9dd6f86736fa54481baf763c1c0b089b39016f0c9dcd00136d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421574b3a33dc8f988de69696c8b68da8a8d82676717d44c9b96721d1cf2418d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerMountsVolumeOptionsLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed325a4b4cf1abdbb08611d10c7be6de074bc251b6dd5b2d031642e36f6071d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef77d8e3bba6bf912d72eaf2f7dcf262a49e0c4022918476271010ddeb9d9d88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4119378555a576bf899f8753ea42c1f28445b47c1533cc153d37353eca5259bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083e4287498a4353454618261830d129f6bcbe98e3d112f00d87eb059b02f377(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerMountsVolumeOptionsLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2895e2c0ff8541421744fec7c0a847e24bd5abfc1ed3cf3e6e77d68b5db91e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba68b5443374733c26794053b13a19ef7add6fefebb214266e1ea47acb7ffa1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerMountsVolumeOptionsLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f68f54633b1caf30c2339c913e9247b38235e5ea51c8b127917123b5df22fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917daaf07aae9615041d9a6a0e178cd367b8c6bd5811a239ac687ab46242816e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757664c850a86379ed7bfc35aef3d67d28addaa5d08ae17e4e6575e429c56583(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ef88951a4ac8ec39638520f2d71d006b1e68120c4ae186e014a3c41f6b3b06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1962b88fb142d9632273ea6993424adec1bbac242bc1564443901942a67ec6(
    value: typing.Optional[ContainerMountsVolumeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41bd5dcb688b572bb93abe888c544b8fab950a4ba8a37693ba84d68d58372a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab3d84e54b74a952cea70ff60115dd93ed350240ab7c4fc3bf94efa4d1d0f08(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d177f3db5c7470bdd851e7e49fd0863e5511d419bc672feee9a8f6795cd056c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c20f714a7eaa28182106339fa6a33b3fa25ce23a57bc3ec405efce719cbbfa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3271f90b13c8b77aba97d92a2ee96b8ea960cd4f0452675f46495de5f13a00(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da48205ccd111a5ab26e77984fcabc46d32f12aa08bf2402013e60e0af850b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0c0f6f95b7bd0c2e6599de15c076cc98172184cb759d104c5565cbf1e87b4f(
    value: typing.Optional[ContainerNetworkData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c2845b94553388f5913a8ad2d2fa15520f344967aead9e640ea4d68fa7ce50(
    *,
    name: builtins.str,
    aliases: typing.Optional[typing.Sequence[builtins.str]] = None,
    ipv4_address: typing.Optional[builtins.str] = None,
    ipv6_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7c6c7a962a4e1d646034c826928fce2f4c380501ec411c32bddd7c096ddf5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff0a80b9960df680d355b544d39f21087715f6056a0072899bef23be93a40e7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4571cb59e209a173e09d6621fa8d1da5ac411e11ebd77b8bf929bd396a8d6ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce455dcc6ae59036a31c5577f205327ec2e8e3d4ec81292d9cbacc79df180b20(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfa1c61314f7de335775832d82353e6ec98bf66216eb4e7f604cdf5ab9e770c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcf558d826c7e80a61af05679fe820e510ad42e5c766f3bfabbc3dab4ebc902b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerNetworksAdvanced]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa09b48a03421b4f977a5692023dcf43f913ef42c3f02a9d558632d54e119833(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c5950c8e7d1706b47dcd252b08434a05ca86d144b192f17b4778632f06c96d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8874e58bd081b1ec11ca6914576b982841772cb0dce862ba802ddfe109bea58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3389a65b9f1c0ed4ec96b86b59fb82702bb299f4eab950caec34ab8205ce07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b168f9191309b0bddfce97e99839843eff4bbf0b7eaf19dffd0ca24da3adb62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443a09a2278608dcac2dd6e3935650d7f67af04fdad4136b87b432863b382f7b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerNetworksAdvanced]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb4e25a60e4a27c8dc2a520ce3fc4bdc839c3781ae729e73552b5e727e126c2(
    *,
    internal: jsii.Number,
    external: typing.Optional[jsii.Number] = None,
    ip: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73088e92b65cce435194e5b320ee52fc8737c5cc2c7142ce2330c5406996910c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6604b3aae38d9b3bf34bc2c3c97b102ab7b1838aa863990e9853a4dd542b429b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0817b5bc50eb3a13a8dfed840d6c0c44e3bf72ef68462e92eae744cdd3ef214(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0b6c7b09f47d697b7077d520bb4d1803c9ad60861f50e2bbd2578c35a42079(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5b5469131f8688b2393227a62e2e56fac9f44d76b19622108d8e0c9559e071(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d51c3379cc670cbddd53ca4945ea0170d6677e303a53361b9af9506c0bc821c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerPorts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a84a72ee16381a730ad0e9ea4778033122472742540222444200ca00e8c567(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6794732795eb9a7b126bc1603b789a3e39f6b2dbe6f1e124034af10eebb12703(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2dc45a6540a613da10e62a7b88eb64c83a1dabf3c5d81910c18787dbdc1c84(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2147ad66bff4a7909a4e7ee4019f09d7714528c7a99cebcbeb6eae52200da66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c3d86973df68cbf2e2c6665c239708fab3afde576deb0910b8f0158cc39adff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d77cead80c21852400598ac48e64bb50887d809c3198396474edfd86d9f3d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerPorts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc59af47d65027182e95104dcc3169f00c9a7e41f7d1a0c392efc430a55db3e2(
    *,
    hard: jsii.Number,
    name: builtins.str,
    soft: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fec1ea1b4611fb6f14f003ad87b5763f274e8304d7a02e08a0ce967efd15a07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637a2783120cf384477ec2c86070856bf6cd465b6604a576a7bc890f38459f2b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96735e74fc83aa4ebbb4d05d2b215ead819df1c44e676caf15182cb6eb02533(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbc5167f5f23835eed18481bdf4cc9dbeac1abe2ef5f557a9583dbefd12202a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c01fba7049d4282886d5335bb84abb3037b81672110db2cdae6e72f050517f6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f247000868c32008878a7acecfb72f423a8a06b640d68cb1d43abdb73ac4e366(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerUlimit]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59dc2df3f436a9aafec4b30d9674c9ff393820ca6b53234afb7f8ea6540e91d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab804314a3f0e85efe764b20d18b2ffeb9aef0cbaca5bf4297cb4a69e8eb86ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d194cf920f773a70e0ca7c94f39287fd1d74170ae461087e0180ab6cc4335b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c14e3666760e0459776fc8cb4911cb79e3d2d91f3cde6764f7e7b03bfafe52(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1759f92cee8c0e88afab4feca7c84de1827137a1018dc10442411511d255d39b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerUlimit]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a99cf8bd42d7e72b6f951996bd6f1614a91a8b8025d0a65c7f01d6d661942c5(
    *,
    file: builtins.str,
    content: typing.Optional[builtins.str] = None,
    content_base64: typing.Optional[builtins.str] = None,
    executable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    permissions: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    source_hash: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec37b2da549c82f1c9ba8f7d2871859ef77ee942586fbf98ef13a592e050e216(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4544081f4549b8eddf21f453e84d85b199b1a46ada799b2bfaf5945eb23eab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f1486ef1002359fe2d339eccfb9ae54cece081078ab70a887fa73c34c9c30e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b08edd13b48dc582fc5a0a503430e7b4cc162ce529dafa6534fa356b23232d0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f316ad7762e425dcb9c28d6e1139ffc0791b421c3d09dad3b578396440bb9e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a66cdef2af9b71cf33c3d21c90957137ff9e47415985d6fbdb10d375d27aaa7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerUpload]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff823a79183af4d59dd32a15bf89467f8363ee82fb5c15e0fd4c2fbeb5c0bbf5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__addcffbb67ab77f2cc268aad9439e2f146d1836db3b64bbfb46522324eb79fa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af77bef402eb392a3d9ab5524dc1ad8669f6b017cc1d581a470badcdfbcdf9a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6050de47e8bbda8265ae77fd75db2096b508eba0e0f5150d984c81cec8cd5d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d62dce7c493856004dea74a7b4889d3ef6f0ba556b4a104e3327af25be7328e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3953608a3c946d02e755aeffbc7c422c805ec0a4acc8f02025a6321fbb69ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69e78774c6bba64b1fb10abeddd50d8edd11f0496c42cdd7db422348afed7f01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c477d58d379ab4c1104da1b918670db3200815690373b655f6c555389f7f85f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9feba0e275d8b028e5324863ae06019d1cfd7716afec5b6d7ec55753a95a99(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerUpload]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6745638491d263da41079bf3c9d9a3c5c59f747c9fdaf6e29eb3201495f1b1bd(
    *,
    container_path: typing.Optional[builtins.str] = None,
    from_container: typing.Optional[builtins.str] = None,
    host_path: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    volume_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b58f4f5cd341111dcb4183d38ec8ac49a6dc7c768175471d5cc47b6a740bed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ce82b0bb67a61e1dc158b6918ebbe993a0292aa94d7f7457aabaaf81d9fcfe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f63334c49d9f4fbc506b1983e0d418d8ba4db7a2c999ea0c359416ef0ab996(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb21cbf944b77196c352ac6fa88cbe7cb07c5221861102c497b8717500eb104(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d216290f7b2106b4cdfe2b53240374f5db6f97536f3daca7be9f7b70bd715e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6efc8f660a86dd4ddc9fb610b2d6428f2ca372a12a1dc6d4ed9d6087578ba0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c3b3f45f74efdb190fd0a78b0241801c0c3056b108d7086050e4a131c3fb00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320510974ad9c2f418c15509052d651434b3bd584d1826a363c84ac6072e36f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d60bb31c8cfe0b87ac14a901e0a5a7cb01c713397b1d383342e721fb7f814d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ef31de095e7e2320d9ded21e7cf5a0bac86946f34310387198a09d581ddb76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06d922def479099314664cc013313962ea821d2b528aa5a07337dedfcd4a21a0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7ab7d17b70d9ed337c4d7ae1004d11a00a4ab7da86a75ba65f2beebadf433c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__401dc3edc98a286426ed9f254e519f81d15faae2cdba9afa419db430c8c50a12(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerVolumes]],
) -> None:
    """Type checking stubs"""
    pass

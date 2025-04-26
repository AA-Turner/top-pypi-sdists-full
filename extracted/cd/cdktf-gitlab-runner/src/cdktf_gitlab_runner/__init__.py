r'''
[![NPM version](https://badge.fury.io/js/cdktf-gitlab-runner.svg)](https://badge.fury.io/js/cdktf-gitlab-runner)
[![PyPI version](https://badge.fury.io/py/cdktf-gitlab-runner.svg)](https://badge.fury.io/py/cdktf-gitlab-runner)
![Release](https://github.com/neilkuan/cdktf-gitlab-runner/workflows/release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdktf-gitlab-runner?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdktf-gitlab-runner?label=pypi&color=blue)

# Welcome to `cdktf-gitlab-runner`

Use CDK fo Terraform to create gitlab runner, and use [gitlab runner](https://gitlab.com/gitlab-org/gitlab-runner) to help you execute your Gitlab Pipeline Job.

> GitLab Runner is the open source project that is used to run your CI/CD jobs and send the results back to GitLab. [(source repo)](https://gitlab.com/gitlab-org/gitlab-runner)

### Feature

* Instance Manager Group
* Auto Register Gitlab Runner
* Auto Unregister Gitlab Runner ([when destroy and shutdown](https://cloud.google.com/compute/docs/shutdownscript))
* Support [preemptible](https://cloud.google.com/compute/docs/instances/preemptible)

### Init CDKTF Project

```bash
mkdir demo
cd demo
cdktf init --template typescript --local
```

### Install `cdktf-gitlab-runner`

```bash
yarn add cdktf-gitlab-runner
or
npm i cdktf-gitlab-runner
```

### Example

```python
import * as gcp from '@cdktf/provider-google';
import * as cdktf from 'cdktf';
import { Construct } from 'constructs';
import { GitlabRunnerAutoscaling } from './index';


export class IntegDefaultStack extends cdktf.TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);
    const local = 'asia-east1';
    const projectId = `${process.env.PROJECT_ID}`;
    const provider = new gcp.GoogleProvider(this, 'GoogleAuth', {
      region: local,
      zone: local+'-c',
      project: projectId,
    });
    new GitlabRunnerAutoscaling(this, 'GitlabRunnerAutoscaling', {
      gitlabToken: `${process.env.GITLAB_TOKEN}`,
      provider,
    });
  }
}


const app = new cdktf.App();
new IntegDefaultStack(app, 'gitlab-runner');
app.synth();
```
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

from ._jsii import *

import cdktf_cdktf_provider_google.compute_instance_template as _cdktf_cdktf_provider_google_compute_instance_template_6cd2ae20
import cdktf_cdktf_provider_google.data_google_compute_network as _cdktf_cdktf_provider_google_data_google_compute_network_6cd2ae20
import cdktf_cdktf_provider_google.provider as _cdktf_cdktf_provider_google_provider_6cd2ae20
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="cdktf-gitlab-runner.DockerVolumes",
    jsii_struct_bases=[],
    name_mapping={"container_path": "containerPath", "host_path": "hostPath"},
)
class DockerVolumes:
    def __init__(
        self,
        *,
        container_path: builtins.str,
        host_path: builtins.str,
    ) -> None:
        '''Docker Volumes interface.

        :param container_path: Job Runtime Container Path Host Path.
        :param host_path: EC2 Runner Host Path.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30cc7f3d151088ac92608a86463900f48e86489ed15b894a78018b8b5d8832ef)
            check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
            check_type(argname="argument host_path", value=host_path, expected_type=type_hints["host_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_path": container_path,
            "host_path": host_path,
        }

    @builtins.property
    def container_path(self) -> builtins.str:
        '''Job Runtime Container Path Host Path.

        Example::

            - /tmp/cahce
            more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section
        '''
        result = self._values.get("container_path")
        assert result is not None, "Required property 'container_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_path(self) -> builtins.str:
        '''EC2 Runner Host Path.

        Example::

            - /tmp/cahce
            more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section
        '''
        result = self._values.get("host_path")
        assert result is not None, "Required property 'host_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitlabRunnerAutoscaling(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-gitlab-runner.GitlabRunnerAutoscaling",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        gitlab_token: builtins.str,
        provider: _cdktf_cdktf_provider_google_provider_6cd2ae20.GoogleProvider,
        automatic_restart: typing.Optional[builtins.bool] = None,
        compute_network: typing.Optional[_cdktf_cdktf_provider_google_data_google_compute_network_6cd2ae20.DataGoogleComputeNetwork] = None,
        concurrent: typing.Optional[jsii.Number] = None,
        default_disk_size_gb: typing.Optional[jsii.Number] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        docker_volumes: typing.Optional[typing.Sequence[typing.Union[DockerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
        download_gitlab_runner_binary_url: typing.Optional[builtins.str] = None,
        gitlab_url: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        preemptible: typing.Optional[builtins.bool] = None,
        service_account: typing.Optional[typing.Union[_cdktf_cdktf_provider_google_compute_instance_template_6cd2ae20.ComputeInstanceTemplateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param gitlab_token: Gitlab token.
        :param provider: Google Cloud Provider.
        :param automatic_restart: If true, automatically restart instances on maintenance events. See https://cloud.google.com/compute/docs/instances/live-migration#autorestart Default: - false
        :param compute_network: VPC for the Gitlab Runner . Default: - A new VPC will be created.
        :param concurrent: gitlab runner run task concurrent at the same time. Default: - 1
        :param default_disk_size_gb: Gitlab Runner instance Disk size. Default: - 60 GB.
        :param desired_capacity: Desired capacity limit for autoscaling group. Default: - minCapacity, and leave unchanged during deployment
        :param docker_volumes: add another Gitlab Container Runner Docker Volumes Path at job runner runtime. more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section Default: - already mount "/var/run/docker.sock:/var/run/docker.sock"
        :param download_gitlab_runner_binary_url: The source URL used to install the gitlab-runner onto the VM host os. Passed to curl via cloud-config runcmd. Default: - "https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64"
        :param gitlab_url: Gitlab Runner register url . Default: - https://gitlab.com/ , The trailing slash is mandatory.
        :param machine_type: Runner default EC2 instance type. Default: -
        :param network_tags: Firewall rules for the Gitlab Runner.
        :param preemptible: If true, create preemptible VM instances intended to reduce cost. Note, the MIG will recreate pre-empted instnaces. See https://cloud.google.com/compute/docs/instances/preemptible
        :param service_account: The Service Account to be used by the Gitlab Runner.
        :param tags: tags for the runner. Default: - ['runner', 'gitlab', 'awscdk']
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__033f891cb05a9b920c1fe5001270de7f0ace57003ad62a8457ef215310793c02)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitlabRunnerAutoscalingProps(
            gitlab_token=gitlab_token,
            provider=provider,
            automatic_restart=automatic_restart,
            compute_network=compute_network,
            concurrent=concurrent,
            default_disk_size_gb=default_disk_size_gb,
            desired_capacity=desired_capacity,
            docker_volumes=docker_volumes,
            download_gitlab_runner_binary_url=download_gitlab_runner_binary_url,
            gitlab_url=gitlab_url,
            machine_type=machine_type,
            network_tags=network_tags,
            preemptible=preemptible,
            service_account=service_account,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createMetadataStartupScript")
    def create_metadata_startup_script(
        self,
        *,
        gitlab_token: builtins.str,
        provider: _cdktf_cdktf_provider_google_provider_6cd2ae20.GoogleProvider,
        automatic_restart: typing.Optional[builtins.bool] = None,
        compute_network: typing.Optional[_cdktf_cdktf_provider_google_data_google_compute_network_6cd2ae20.DataGoogleComputeNetwork] = None,
        concurrent: typing.Optional[jsii.Number] = None,
        default_disk_size_gb: typing.Optional[jsii.Number] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        docker_volumes: typing.Optional[typing.Sequence[typing.Union[DockerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
        download_gitlab_runner_binary_url: typing.Optional[builtins.str] = None,
        gitlab_url: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        preemptible: typing.Optional[builtins.bool] = None,
        service_account: typing.Optional[typing.Union[_cdktf_cdktf_provider_google_compute_instance_template_6cd2ae20.ComputeInstanceTemplateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> typing.List[builtins.str]:
        '''
        :param gitlab_token: Gitlab token.
        :param provider: Google Cloud Provider.
        :param automatic_restart: If true, automatically restart instances on maintenance events. See https://cloud.google.com/compute/docs/instances/live-migration#autorestart Default: - false
        :param compute_network: VPC for the Gitlab Runner . Default: - A new VPC will be created.
        :param concurrent: gitlab runner run task concurrent at the same time. Default: - 1
        :param default_disk_size_gb: Gitlab Runner instance Disk size. Default: - 60 GB.
        :param desired_capacity: Desired capacity limit for autoscaling group. Default: - minCapacity, and leave unchanged during deployment
        :param docker_volumes: add another Gitlab Container Runner Docker Volumes Path at job runner runtime. more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section Default: - already mount "/var/run/docker.sock:/var/run/docker.sock"
        :param download_gitlab_runner_binary_url: The source URL used to install the gitlab-runner onto the VM host os. Passed to curl via cloud-config runcmd. Default: - "https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64"
        :param gitlab_url: Gitlab Runner register url . Default: - https://gitlab.com/ , The trailing slash is mandatory.
        :param machine_type: Runner default EC2 instance type. Default: -
        :param network_tags: Firewall rules for the Gitlab Runner.
        :param preemptible: If true, create preemptible VM instances intended to reduce cost. Note, the MIG will recreate pre-empted instnaces. See https://cloud.google.com/compute/docs/instances/preemptible
        :param service_account: The Service Account to be used by the Gitlab Runner.
        :param tags: tags for the runner. Default: - ['runner', 'gitlab', 'awscdk']

        :return: Array.
        '''
        props = GitlabRunnerAutoscalingProps(
            gitlab_token=gitlab_token,
            provider=provider,
            automatic_restart=automatic_restart,
            compute_network=compute_network,
            concurrent=concurrent,
            default_disk_size_gb=default_disk_size_gb,
            desired_capacity=desired_capacity,
            docker_volumes=docker_volumes,
            download_gitlab_runner_binary_url=download_gitlab_runner_binary_url,
            gitlab_url=gitlab_url,
            machine_type=machine_type,
            network_tags=network_tags,
            preemptible=preemptible,
            service_account=service_account,
            tags=tags,
        )

        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "createMetadataStartupScript", [props]))


@jsii.data_type(
    jsii_type="cdktf-gitlab-runner.GitlabRunnerAutoscalingProps",
    jsii_struct_bases=[],
    name_mapping={
        "gitlab_token": "gitlabToken",
        "provider": "provider",
        "automatic_restart": "automaticRestart",
        "compute_network": "computeNetwork",
        "concurrent": "concurrent",
        "default_disk_size_gb": "defaultDiskSizeGb",
        "desired_capacity": "desiredCapacity",
        "docker_volumes": "dockerVolumes",
        "download_gitlab_runner_binary_url": "downloadGitlabRunnerBinaryUrl",
        "gitlab_url": "gitlabUrl",
        "machine_type": "machineType",
        "network_tags": "networkTags",
        "preemptible": "preemptible",
        "service_account": "serviceAccount",
        "tags": "tags",
    },
)
class GitlabRunnerAutoscalingProps:
    def __init__(
        self,
        *,
        gitlab_token: builtins.str,
        provider: _cdktf_cdktf_provider_google_provider_6cd2ae20.GoogleProvider,
        automatic_restart: typing.Optional[builtins.bool] = None,
        compute_network: typing.Optional[_cdktf_cdktf_provider_google_data_google_compute_network_6cd2ae20.DataGoogleComputeNetwork] = None,
        concurrent: typing.Optional[jsii.Number] = None,
        default_disk_size_gb: typing.Optional[jsii.Number] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        docker_volumes: typing.Optional[typing.Sequence[typing.Union[DockerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
        download_gitlab_runner_binary_url: typing.Optional[builtins.str] = None,
        gitlab_url: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        preemptible: typing.Optional[builtins.bool] = None,
        service_account: typing.Optional[typing.Union[_cdktf_cdktf_provider_google_compute_instance_template_6cd2ae20.ComputeInstanceTemplateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param gitlab_token: Gitlab token.
        :param provider: Google Cloud Provider.
        :param automatic_restart: If true, automatically restart instances on maintenance events. See https://cloud.google.com/compute/docs/instances/live-migration#autorestart Default: - false
        :param compute_network: VPC for the Gitlab Runner . Default: - A new VPC will be created.
        :param concurrent: gitlab runner run task concurrent at the same time. Default: - 1
        :param default_disk_size_gb: Gitlab Runner instance Disk size. Default: - 60 GB.
        :param desired_capacity: Desired capacity limit for autoscaling group. Default: - minCapacity, and leave unchanged during deployment
        :param docker_volumes: add another Gitlab Container Runner Docker Volumes Path at job runner runtime. more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section Default: - already mount "/var/run/docker.sock:/var/run/docker.sock"
        :param download_gitlab_runner_binary_url: The source URL used to install the gitlab-runner onto the VM host os. Passed to curl via cloud-config runcmd. Default: - "https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64"
        :param gitlab_url: Gitlab Runner register url . Default: - https://gitlab.com/ , The trailing slash is mandatory.
        :param machine_type: Runner default EC2 instance type. Default: -
        :param network_tags: Firewall rules for the Gitlab Runner.
        :param preemptible: If true, create preemptible VM instances intended to reduce cost. Note, the MIG will recreate pre-empted instnaces. See https://cloud.google.com/compute/docs/instances/preemptible
        :param service_account: The Service Account to be used by the Gitlab Runner.
        :param tags: tags for the runner. Default: - ['runner', 'gitlab', 'awscdk']
        '''
        if isinstance(service_account, dict):
            service_account = _cdktf_cdktf_provider_google_compute_instance_template_6cd2ae20.ComputeInstanceTemplateServiceAccount(**service_account)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88032eb7bd25ee0d2ad0139ad567354349b2287562f65346004517f962685e3)
            check_type(argname="argument gitlab_token", value=gitlab_token, expected_type=type_hints["gitlab_token"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument automatic_restart", value=automatic_restart, expected_type=type_hints["automatic_restart"])
            check_type(argname="argument compute_network", value=compute_network, expected_type=type_hints["compute_network"])
            check_type(argname="argument concurrent", value=concurrent, expected_type=type_hints["concurrent"])
            check_type(argname="argument default_disk_size_gb", value=default_disk_size_gb, expected_type=type_hints["default_disk_size_gb"])
            check_type(argname="argument desired_capacity", value=desired_capacity, expected_type=type_hints["desired_capacity"])
            check_type(argname="argument docker_volumes", value=docker_volumes, expected_type=type_hints["docker_volumes"])
            check_type(argname="argument download_gitlab_runner_binary_url", value=download_gitlab_runner_binary_url, expected_type=type_hints["download_gitlab_runner_binary_url"])
            check_type(argname="argument gitlab_url", value=gitlab_url, expected_type=type_hints["gitlab_url"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument network_tags", value=network_tags, expected_type=type_hints["network_tags"])
            check_type(argname="argument preemptible", value=preemptible, expected_type=type_hints["preemptible"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gitlab_token": gitlab_token,
            "provider": provider,
        }
        if automatic_restart is not None:
            self._values["automatic_restart"] = automatic_restart
        if compute_network is not None:
            self._values["compute_network"] = compute_network
        if concurrent is not None:
            self._values["concurrent"] = concurrent
        if default_disk_size_gb is not None:
            self._values["default_disk_size_gb"] = default_disk_size_gb
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if docker_volumes is not None:
            self._values["docker_volumes"] = docker_volumes
        if download_gitlab_runner_binary_url is not None:
            self._values["download_gitlab_runner_binary_url"] = download_gitlab_runner_binary_url
        if gitlab_url is not None:
            self._values["gitlab_url"] = gitlab_url
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if network_tags is not None:
            self._values["network_tags"] = network_tags
        if preemptible is not None:
            self._values["preemptible"] = preemptible
        if service_account is not None:
            self._values["service_account"] = service_account
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def gitlab_token(self) -> builtins.str:
        '''Gitlab token.

        Example::

            new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN' });
        '''
        result = self._values.get("gitlab_token")
        assert result is not None, "Required property 'gitlab_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider(self) -> _cdktf_cdktf_provider_google_provider_6cd2ae20.GoogleProvider:
        '''Google Cloud Provider.'''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast(_cdktf_cdktf_provider_google_provider_6cd2ae20.GoogleProvider, result)

    @builtins.property
    def automatic_restart(self) -> typing.Optional[builtins.bool]:
        '''If true, automatically restart instances on maintenance events.

        See https://cloud.google.com/compute/docs/instances/live-migration#autorestart

        :default: - false
        '''
        result = self._values.get("automatic_restart")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def compute_network(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_google_data_google_compute_network_6cd2ae20.DataGoogleComputeNetwork]:
        '''VPC for the Gitlab Runner .

        :default: - A new VPC will be created.

        Example::

            const computeNetwork = new gcp.ComputeNetwork(this, 'Network', {
              name: 'cdktf-gitlabrunner-network',
            });
            
            new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN', computeNetwork: computeNetwork });
        '''
        result = self._values.get("compute_network")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_google_data_google_compute_network_6cd2ae20.DataGoogleComputeNetwork], result)

    @builtins.property
    def concurrent(self) -> typing.Optional[jsii.Number]:
        '''gitlab runner run task concurrent at the same time.

        :default: - 1
        '''
        result = self._values.get("concurrent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Gitlab Runner instance Disk size.

        :default: - 60 GB.
        '''
        result = self._values.get("default_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        '''Desired capacity limit for autoscaling group.

        :default: - minCapacity, and leave unchanged during deployment

        Example::

            new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN', desiredCapacity: 2 });
        '''
        result = self._values.get("desired_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def docker_volumes(self) -> typing.Optional[typing.List[DockerVolumes]]:
        '''add another Gitlab Container Runner Docker Volumes Path at job runner runtime.

        more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section

        :default: - already mount "/var/run/docker.sock:/var/run/docker.sock"

        Example::

            dockerVolumes: [
              {
                hostPath: '/tmp/cache',
                containerPath: '/tmp/cache',
              },
            ],
        '''
        result = self._values.get("docker_volumes")
        return typing.cast(typing.Optional[typing.List[DockerVolumes]], result)

    @builtins.property
    def download_gitlab_runner_binary_url(self) -> typing.Optional[builtins.str]:
        '''The source URL used to install the gitlab-runner onto the VM host os.

        Passed to curl via cloud-config runcmd.

        :default: - "https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64"
        '''
        result = self._values.get("download_gitlab_runner_binary_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gitlab_url(self) -> typing.Optional[builtins.str]:
        '''Gitlab Runner register url .

        :default: - https://gitlab.com/ , The trailing slash is mandatory.

        Example::

            const runner = new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN',gitlabUrl: 'https://gitlab.com/'});
        '''
        result = self._values.get("gitlab_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Runner default EC2 instance type.

        :default: -

        Example::

            new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN', instanceType: 't3.small' });
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Firewall rules for the Gitlab Runner.'''
        result = self._values.get("network_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def preemptible(self) -> typing.Optional[builtins.bool]:
        '''If true, create preemptible VM instances intended to reduce cost.

        Note, the MIG will recreate pre-empted instnaces.
        See https://cloud.google.com/compute/docs/instances/preemptible

        :deafult: - true
        '''
        result = self._values.get("preemptible")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service_account(
        self,
    ) -> typing.Optional[_cdktf_cdktf_provider_google_compute_instance_template_6cd2ae20.ComputeInstanceTemplateServiceAccount]:
        '''The Service Account to be used by the Gitlab Runner.'''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[_cdktf_cdktf_provider_google_compute_instance_template_6cd2ae20.ComputeInstanceTemplateServiceAccount], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''tags for the runner.

        :default: - ['runner', 'gitlab', 'awscdk']
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitlabRunnerAutoscalingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DockerVolumes",
    "GitlabRunnerAutoscaling",
    "GitlabRunnerAutoscalingProps",
]

publication.publish()

def _typecheckingstub__30cc7f3d151088ac92608a86463900f48e86489ed15b894a78018b8b5d8832ef(
    *,
    container_path: builtins.str,
    host_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__033f891cb05a9b920c1fe5001270de7f0ace57003ad62a8457ef215310793c02(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    gitlab_token: builtins.str,
    provider: _cdktf_cdktf_provider_google_provider_6cd2ae20.GoogleProvider,
    automatic_restart: typing.Optional[builtins.bool] = None,
    compute_network: typing.Optional[_cdktf_cdktf_provider_google_data_google_compute_network_6cd2ae20.DataGoogleComputeNetwork] = None,
    concurrent: typing.Optional[jsii.Number] = None,
    default_disk_size_gb: typing.Optional[jsii.Number] = None,
    desired_capacity: typing.Optional[jsii.Number] = None,
    docker_volumes: typing.Optional[typing.Sequence[typing.Union[DockerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
    download_gitlab_runner_binary_url: typing.Optional[builtins.str] = None,
    gitlab_url: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    preemptible: typing.Optional[builtins.bool] = None,
    service_account: typing.Optional[typing.Union[_cdktf_cdktf_provider_google_compute_instance_template_6cd2ae20.ComputeInstanceTemplateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88032eb7bd25ee0d2ad0139ad567354349b2287562f65346004517f962685e3(
    *,
    gitlab_token: builtins.str,
    provider: _cdktf_cdktf_provider_google_provider_6cd2ae20.GoogleProvider,
    automatic_restart: typing.Optional[builtins.bool] = None,
    compute_network: typing.Optional[_cdktf_cdktf_provider_google_data_google_compute_network_6cd2ae20.DataGoogleComputeNetwork] = None,
    concurrent: typing.Optional[jsii.Number] = None,
    default_disk_size_gb: typing.Optional[jsii.Number] = None,
    desired_capacity: typing.Optional[jsii.Number] = None,
    docker_volumes: typing.Optional[typing.Sequence[typing.Union[DockerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
    download_gitlab_runner_binary_url: typing.Optional[builtins.str] = None,
    gitlab_url: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    preemptible: typing.Optional[builtins.bool] = None,
    service_account: typing.Optional[typing.Union[_cdktf_cdktf_provider_google_compute_instance_template_6cd2ae20.ComputeInstanceTemplateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

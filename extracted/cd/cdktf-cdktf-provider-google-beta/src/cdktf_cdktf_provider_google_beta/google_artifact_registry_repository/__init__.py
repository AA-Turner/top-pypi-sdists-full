r'''
# `google_artifact_registry_repository`

Refer to the Terraform Registry for docs: [`google_artifact_registry_repository`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository).
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


class GoogleArtifactRegistryRepository(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepository",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository google_artifact_registry_repository}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        format: builtins.str,
        repository_id: builtins.str,
        cleanup_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleArtifactRegistryRepositoryCleanupPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cleanup_policy_dry_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        docker_config: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryDockerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        maven_config: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryMavenConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remote_repository_config: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_repository_config: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryVirtualRepositoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vulnerability_scanning_config: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository google_artifact_registry_repository} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param format: The format of packages that are stored in the repository. Supported formats can be found `here <https://cloud.google.com/artifact-registry/docs/supported-formats>`_. You can only create alpha formats if you are a member of the `alpha user group <https://cloud.google.com/artifact-registry/docs/supported-formats#alpha-access>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#format GoogleArtifactRegistryRepository#format}
        :param repository_id: The last part of the repository name, for example: "repo1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository_id GoogleArtifactRegistryRepository#repository_id}
        :param cleanup_policies: cleanup_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#cleanup_policies GoogleArtifactRegistryRepository#cleanup_policies}
        :param cleanup_policy_dry_run: If true, the cleanup pipeline is prevented from deleting versions in this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#cleanup_policy_dry_run GoogleArtifactRegistryRepository#cleanup_policy_dry_run}
        :param description: The user-provided description of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#description GoogleArtifactRegistryRepository#description}
        :param docker_config: docker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#docker_config GoogleArtifactRegistryRepository#docker_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#id GoogleArtifactRegistryRepository#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: The Cloud KMS resource name of the customer managed encryption key that’s used to encrypt the contents of the Repository. Has the form: 'projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key'. This value may not be changed after the Repository has been created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#kms_key_name GoogleArtifactRegistryRepository#kms_key_name}
        :param labels: Labels with user-defined metadata. This field may contain up to 64 entries. Label keys and values may be no longer than 63 characters. Label keys must begin with a lowercase letter and may only contain lowercase letters, numeric characters, underscores, and dashes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#labels GoogleArtifactRegistryRepository#labels}
        :param location: The name of the repository's location. In addition to specific regions, special values for multi-region locations are 'asia', 'europe', and 'us'. See `here <https://cloud.google.com/artifact-registry/docs/repositories/repo-locations>`_, or use the `google_artifact_registry_locations <https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/artifact_registry_locations>`_ data source for possible values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#location GoogleArtifactRegistryRepository#location}
        :param maven_config: maven_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#maven_config GoogleArtifactRegistryRepository#maven_config}
        :param mode: The mode configures the repository to serve artifacts from different sources. Default value: "STANDARD_REPOSITORY" Possible values: ["STANDARD_REPOSITORY", "VIRTUAL_REPOSITORY", "REMOTE_REPOSITORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#mode GoogleArtifactRegistryRepository#mode}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#project GoogleArtifactRegistryRepository#project}.
        :param remote_repository_config: remote_repository_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#remote_repository_config GoogleArtifactRegistryRepository#remote_repository_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#timeouts GoogleArtifactRegistryRepository#timeouts}
        :param virtual_repository_config: virtual_repository_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#virtual_repository_config GoogleArtifactRegistryRepository#virtual_repository_config}
        :param vulnerability_scanning_config: vulnerability_scanning_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#vulnerability_scanning_config GoogleArtifactRegistryRepository#vulnerability_scanning_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a11e2122d6664017242aeafd4c93d9fa52129b0712698eca09688c82b13de3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleArtifactRegistryRepositoryConfig(
            format=format,
            repository_id=repository_id,
            cleanup_policies=cleanup_policies,
            cleanup_policy_dry_run=cleanup_policy_dry_run,
            description=description,
            docker_config=docker_config,
            id=id,
            kms_key_name=kms_key_name,
            labels=labels,
            location=location,
            maven_config=maven_config,
            mode=mode,
            project=project,
            remote_repository_config=remote_repository_config,
            timeouts=timeouts,
            virtual_repository_config=virtual_repository_config,
            vulnerability_scanning_config=vulnerability_scanning_config,
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
        '''Generates CDKTF code for importing a GoogleArtifactRegistryRepository resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleArtifactRegistryRepository to import.
        :param import_from_id: The id of the existing GoogleArtifactRegistryRepository that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleArtifactRegistryRepository to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a8d60b8f3b73707c536456d31fff9819f8372604d97892d8efc3b60649c84d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCleanupPolicies")
    def put_cleanup_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleArtifactRegistryRepositoryCleanupPolicies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05cfbff3cbeda33d36e9e501915cc61276b852e146b7cc1fface6d12f658a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCleanupPolicies", [value]))

    @jsii.member(jsii_name="putDockerConfig")
    def put_docker_config(
        self,
        *,
        immutable_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param immutable_tags: The repository which enabled this flag prevents all tags from being modified, moved or deleted. This does not prevent tags from being created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#immutable_tags GoogleArtifactRegistryRepository#immutable_tags}
        '''
        value = GoogleArtifactRegistryRepositoryDockerConfig(
            immutable_tags=immutable_tags
        )

        return typing.cast(None, jsii.invoke(self, "putDockerConfig", [value]))

    @jsii.member(jsii_name="putMavenConfig")
    def put_maven_config(
        self,
        *,
        allow_snapshot_overwrites: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        version_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_snapshot_overwrites: The repository with this flag will allow publishing the same snapshot versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#allow_snapshot_overwrites GoogleArtifactRegistryRepository#allow_snapshot_overwrites}
        :param version_policy: Version policy defines the versions that the registry will accept. Default value: "VERSION_POLICY_UNSPECIFIED" Possible values: ["VERSION_POLICY_UNSPECIFIED", "RELEASE", "SNAPSHOT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#version_policy GoogleArtifactRegistryRepository#version_policy}
        '''
        value = GoogleArtifactRegistryRepositoryMavenConfig(
            allow_snapshot_overwrites=allow_snapshot_overwrites,
            version_policy=version_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putMavenConfig", [value]))

    @jsii.member(jsii_name="putRemoteRepositoryConfig")
    def put_remote_repository_config(
        self,
        *,
        apt_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        common_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_upstream_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        docker_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        maven_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        npm_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        python_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        upstream_credentials: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        yum_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt_repository: apt_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#apt_repository GoogleArtifactRegistryRepository#apt_repository}
        :param common_repository: common_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#common_repository GoogleArtifactRegistryRepository#common_repository}
        :param description: The description of the remote source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#description GoogleArtifactRegistryRepository#description}
        :param disable_upstream_validation: If true, the remote repository upstream and upstream credentials will not be validated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#disable_upstream_validation GoogleArtifactRegistryRepository#disable_upstream_validation}
        :param docker_repository: docker_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#docker_repository GoogleArtifactRegistryRepository#docker_repository}
        :param maven_repository: maven_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#maven_repository GoogleArtifactRegistryRepository#maven_repository}
        :param npm_repository: npm_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#npm_repository GoogleArtifactRegistryRepository#npm_repository}
        :param python_repository: python_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#python_repository GoogleArtifactRegistryRepository#python_repository}
        :param upstream_credentials: upstream_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#upstream_credentials GoogleArtifactRegistryRepository#upstream_credentials}
        :param yum_repository: yum_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#yum_repository GoogleArtifactRegistryRepository#yum_repository}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfig(
            apt_repository=apt_repository,
            common_repository=common_repository,
            description=description,
            disable_upstream_validation=disable_upstream_validation,
            docker_repository=docker_repository,
            maven_repository=maven_repository,
            npm_repository=npm_repository,
            python_repository=python_repository,
            upstream_credentials=upstream_credentials,
            yum_repository=yum_repository,
        )

        return typing.cast(None, jsii.invoke(self, "putRemoteRepositoryConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#create GoogleArtifactRegistryRepository#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#delete GoogleArtifactRegistryRepository#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#update GoogleArtifactRegistryRepository#update}.
        '''
        value = GoogleArtifactRegistryRepositoryTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVirtualRepositoryConfig")
    def put_virtual_repository_config(
        self,
        *,
        upstream_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param upstream_policies: upstream_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#upstream_policies GoogleArtifactRegistryRepository#upstream_policies}
        '''
        value = GoogleArtifactRegistryRepositoryVirtualRepositoryConfig(
            upstream_policies=upstream_policies
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualRepositoryConfig", [value]))

    @jsii.member(jsii_name="putVulnerabilityScanningConfig")
    def put_vulnerability_scanning_config(
        self,
        *,
        enablement_config: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enablement_config: This configures whether vulnerability scanning is automatically performed for artifacts pushed to this repository. Possible values: ["INHERITED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#enablement_config GoogleArtifactRegistryRepository#enablement_config}
        '''
        value = GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig(
            enablement_config=enablement_config
        )

        return typing.cast(None, jsii.invoke(self, "putVulnerabilityScanningConfig", [value]))

    @jsii.member(jsii_name="resetCleanupPolicies")
    def reset_cleanup_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCleanupPolicies", []))

    @jsii.member(jsii_name="resetCleanupPolicyDryRun")
    def reset_cleanup_policy_dry_run(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCleanupPolicyDryRun", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDockerConfig")
    def reset_docker_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetMavenConfig")
    def reset_maven_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMavenConfig", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRemoteRepositoryConfig")
    def reset_remote_repository_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteRepositoryConfig", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVirtualRepositoryConfig")
    def reset_virtual_repository_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualRepositoryConfig", []))

    @jsii.member(jsii_name="resetVulnerabilityScanningConfig")
    def reset_vulnerability_scanning_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVulnerabilityScanningConfig", []))

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
    @jsii.member(jsii_name="cleanupPolicies")
    def cleanup_policies(self) -> "GoogleArtifactRegistryRepositoryCleanupPoliciesList":
        return typing.cast("GoogleArtifactRegistryRepositoryCleanupPoliciesList", jsii.get(self, "cleanupPolicies"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="dockerConfig")
    def docker_config(
        self,
    ) -> "GoogleArtifactRegistryRepositoryDockerConfigOutputReference":
        return typing.cast("GoogleArtifactRegistryRepositoryDockerConfigOutputReference", jsii.get(self, "dockerConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="mavenConfig")
    def maven_config(
        self,
    ) -> "GoogleArtifactRegistryRepositoryMavenConfigOutputReference":
        return typing.cast("GoogleArtifactRegistryRepositoryMavenConfigOutputReference", jsii.get(self, "mavenConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="remoteRepositoryConfig")
    def remote_repository_config(
        self,
    ) -> "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigOutputReference":
        return typing.cast("GoogleArtifactRegistryRepositoryRemoteRepositoryConfigOutputReference", jsii.get(self, "remoteRepositoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleArtifactRegistryRepositoryTimeoutsOutputReference":
        return typing.cast("GoogleArtifactRegistryRepositoryTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="virtualRepositoryConfig")
    def virtual_repository_config(
        self,
    ) -> "GoogleArtifactRegistryRepositoryVirtualRepositoryConfigOutputReference":
        return typing.cast("GoogleArtifactRegistryRepositoryVirtualRepositoryConfigOutputReference", jsii.get(self, "virtualRepositoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="vulnerabilityScanningConfig")
    def vulnerability_scanning_config(
        self,
    ) -> "GoogleArtifactRegistryRepositoryVulnerabilityScanningConfigOutputReference":
        return typing.cast("GoogleArtifactRegistryRepositoryVulnerabilityScanningConfigOutputReference", jsii.get(self, "vulnerabilityScanningConfig"))

    @builtins.property
    @jsii.member(jsii_name="cleanupPoliciesInput")
    def cleanup_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleArtifactRegistryRepositoryCleanupPolicies"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleArtifactRegistryRepositoryCleanupPolicies"]]], jsii.get(self, "cleanupPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="cleanupPolicyDryRunInput")
    def cleanup_policy_dry_run_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cleanupPolicyDryRunInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerConfigInput")
    def docker_config_input(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryDockerConfig"]:
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryDockerConfig"], jsii.get(self, "dockerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="mavenConfigInput")
    def maven_config_input(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryMavenConfig"]:
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryMavenConfig"], jsii.get(self, "mavenConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteRepositoryConfigInput")
    def remote_repository_config_input(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfig"]:
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfig"], jsii.get(self, "remoteRepositoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryIdInput")
    def repository_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleArtifactRegistryRepositoryTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleArtifactRegistryRepositoryTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualRepositoryConfigInput")
    def virtual_repository_config_input(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryVirtualRepositoryConfig"]:
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryVirtualRepositoryConfig"], jsii.get(self, "virtualRepositoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="vulnerabilityScanningConfigInput")
    def vulnerability_scanning_config_input(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig"]:
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig"], jsii.get(self, "vulnerabilityScanningConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="cleanupPolicyDryRun")
    def cleanup_policy_dry_run(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cleanupPolicyDryRun"))

    @cleanup_policy_dry_run.setter
    def cleanup_policy_dry_run(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02c6c97b7c0d307c6e3d68f07b761e6c3e505524e37996248beaf25659d6a565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cleanupPolicyDryRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a884f9ba44c40a4418e193fc168692418b837dc57d71f179490ba11b5fa40d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1acfe2b5cf2b91d73928a9e731c2cfd069bbac29dcbc52da978ca527d69737d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b587ab17be38890794c093824080b4e454003e1198e375724cdfc3178057854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec0ed70e3829cbc8930c8fbc32c7fbbafecab184eda9d737a892486619fadcad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__535062de7b2c2b2db5c98c29f5e9ac5025367fbe810e81c83ad59ef15835eaa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87602acbfc2bd41a8fb9eff6b22fb5c6b2ab9113e61fcbc5705497bd380eb496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb2ba84f604e1ab673edb088edec27614d9b6b6e5aef7daa40830753dbb93af3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a0e374397384da479f77b5ea8afb599619865d041cba21a07f3b4eec030e5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryId")
    def repository_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryId"))

    @repository_id.setter
    def repository_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755a1bd588113c26c00d7dd30beaceb0cb1af32b57a2fc7059cfce92eb73a939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryCleanupPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "action": "action",
        "condition": "condition",
        "most_recent_versions": "mostRecentVersions",
    },
)
class GoogleArtifactRegistryRepositoryCleanupPolicies:
    def __init__(
        self,
        *,
        id: builtins.str,
        action: typing.Optional[builtins.str] = None,
        condition: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryCleanupPoliciesCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        most_recent_versions: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#id GoogleArtifactRegistryRepository#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param action: Policy action. Possible values: ["DELETE", "KEEP"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#action GoogleArtifactRegistryRepository#action}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#condition GoogleArtifactRegistryRepository#condition}
        :param most_recent_versions: most_recent_versions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#most_recent_versions GoogleArtifactRegistryRepository#most_recent_versions}
        '''
        if isinstance(condition, dict):
            condition = GoogleArtifactRegistryRepositoryCleanupPoliciesCondition(**condition)
        if isinstance(most_recent_versions, dict):
            most_recent_versions = GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions(**most_recent_versions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570054b414acb7cf97eea863acdbf6ab3a59c8eafa5896fe984091478e1c7b82)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument most_recent_versions", value=most_recent_versions, expected_type=type_hints["most_recent_versions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if action is not None:
            self._values["action"] = action
        if condition is not None:
            self._values["condition"] = condition
        if most_recent_versions is not None:
            self._values["most_recent_versions"] = most_recent_versions

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#id GoogleArtifactRegistryRepository#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Policy action. Possible values: ["DELETE", "KEEP"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#action GoogleArtifactRegistryRepository#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryCleanupPoliciesCondition"]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#condition GoogleArtifactRegistryRepository#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryCleanupPoliciesCondition"], result)

    @builtins.property
    def most_recent_versions(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions"]:
        '''most_recent_versions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#most_recent_versions GoogleArtifactRegistryRepository#most_recent_versions}
        '''
        result = self._values.get("most_recent_versions")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryCleanupPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryCleanupPoliciesCondition",
    jsii_struct_bases=[],
    name_mapping={
        "newer_than": "newerThan",
        "older_than": "olderThan",
        "package_name_prefixes": "packageNamePrefixes",
        "tag_prefixes": "tagPrefixes",
        "tag_state": "tagState",
        "version_name_prefixes": "versionNamePrefixes",
    },
)
class GoogleArtifactRegistryRepositoryCleanupPoliciesCondition:
    def __init__(
        self,
        *,
        newer_than: typing.Optional[builtins.str] = None,
        older_than: typing.Optional[builtins.str] = None,
        package_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_state: typing.Optional[builtins.str] = None,
        version_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param newer_than: Match versions newer than a duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#newer_than GoogleArtifactRegistryRepository#newer_than}
        :param older_than: Match versions older than a duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#older_than GoogleArtifactRegistryRepository#older_than}
        :param package_name_prefixes: Match versions by package prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#package_name_prefixes GoogleArtifactRegistryRepository#package_name_prefixes}
        :param tag_prefixes: Match versions by tag prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#tag_prefixes GoogleArtifactRegistryRepository#tag_prefixes}
        :param tag_state: Match versions by tag status. Default value: "ANY" Possible values: ["TAGGED", "UNTAGGED", "ANY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#tag_state GoogleArtifactRegistryRepository#tag_state}
        :param version_name_prefixes: Match versions by version name prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#version_name_prefixes GoogleArtifactRegistryRepository#version_name_prefixes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2084459b9314767a18ef25c7569e01b1db52b810852e0cf8f76f555d3b84b0ea)
            check_type(argname="argument newer_than", value=newer_than, expected_type=type_hints["newer_than"])
            check_type(argname="argument older_than", value=older_than, expected_type=type_hints["older_than"])
            check_type(argname="argument package_name_prefixes", value=package_name_prefixes, expected_type=type_hints["package_name_prefixes"])
            check_type(argname="argument tag_prefixes", value=tag_prefixes, expected_type=type_hints["tag_prefixes"])
            check_type(argname="argument tag_state", value=tag_state, expected_type=type_hints["tag_state"])
            check_type(argname="argument version_name_prefixes", value=version_name_prefixes, expected_type=type_hints["version_name_prefixes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if newer_than is not None:
            self._values["newer_than"] = newer_than
        if older_than is not None:
            self._values["older_than"] = older_than
        if package_name_prefixes is not None:
            self._values["package_name_prefixes"] = package_name_prefixes
        if tag_prefixes is not None:
            self._values["tag_prefixes"] = tag_prefixes
        if tag_state is not None:
            self._values["tag_state"] = tag_state
        if version_name_prefixes is not None:
            self._values["version_name_prefixes"] = version_name_prefixes

    @builtins.property
    def newer_than(self) -> typing.Optional[builtins.str]:
        '''Match versions newer than a duration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#newer_than GoogleArtifactRegistryRepository#newer_than}
        '''
        result = self._values.get("newer_than")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def older_than(self) -> typing.Optional[builtins.str]:
        '''Match versions older than a duration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#older_than GoogleArtifactRegistryRepository#older_than}
        '''
        result = self._values.get("older_than")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package_name_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Match versions by package prefix. Applied on any prefix match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#package_name_prefixes GoogleArtifactRegistryRepository#package_name_prefixes}
        '''
        result = self._values.get("package_name_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Match versions by tag prefix. Applied on any prefix match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#tag_prefixes GoogleArtifactRegistryRepository#tag_prefixes}
        '''
        result = self._values.get("tag_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_state(self) -> typing.Optional[builtins.str]:
        '''Match versions by tag status. Default value: "ANY" Possible values: ["TAGGED", "UNTAGGED", "ANY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#tag_state GoogleArtifactRegistryRepository#tag_state}
        '''
        result = self._values.get("tag_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_name_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Match versions by version name prefix. Applied on any prefix match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#version_name_prefixes GoogleArtifactRegistryRepository#version_name_prefixes}
        '''
        result = self._values.get("version_name_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryCleanupPoliciesCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryCleanupPoliciesConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryCleanupPoliciesConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50a735369f344b6db5fcde1f4aaeb92248dc49581a24d12b63a6c31b3dce1b90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNewerThan")
    def reset_newer_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewerThan", []))

    @jsii.member(jsii_name="resetOlderThan")
    def reset_older_than(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOlderThan", []))

    @jsii.member(jsii_name="resetPackageNamePrefixes")
    def reset_package_name_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackageNamePrefixes", []))

    @jsii.member(jsii_name="resetTagPrefixes")
    def reset_tag_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagPrefixes", []))

    @jsii.member(jsii_name="resetTagState")
    def reset_tag_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagState", []))

    @jsii.member(jsii_name="resetVersionNamePrefixes")
    def reset_version_name_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionNamePrefixes", []))

    @builtins.property
    @jsii.member(jsii_name="newerThanInput")
    def newer_than_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "newerThanInput"))

    @builtins.property
    @jsii.member(jsii_name="olderThanInput")
    def older_than_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "olderThanInput"))

    @builtins.property
    @jsii.member(jsii_name="packageNamePrefixesInput")
    def package_name_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "packageNamePrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="tagPrefixesInput")
    def tag_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="tagStateInput")
    def tag_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagStateInput"))

    @builtins.property
    @jsii.member(jsii_name="versionNamePrefixesInput")
    def version_name_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "versionNamePrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="newerThan")
    def newer_than(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "newerThan"))

    @newer_than.setter
    def newer_than(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e20fee31910a72480c1a8a2efc6fe0d9d52148649332cc1fe91334323f74b6e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newerThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="olderThan")
    def older_than(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "olderThan"))

    @older_than.setter
    def older_than(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30430a1f32062224cf341daf4b13ac6b31e47f69744aaae578a58a1b42f8bdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "olderThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packageNamePrefixes")
    def package_name_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "packageNamePrefixes"))

    @package_name_prefixes.setter
    def package_name_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63bb591cca4719305e746582ef32b4353dced2dc74fe7d751f4411af2f98017c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageNamePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagPrefixes")
    def tag_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tagPrefixes"))

    @tag_prefixes.setter
    def tag_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27733cc7dab0ee759bd0d7da921b56d6302235667557e06a7636f4e461dff33a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagState")
    def tag_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagState"))

    @tag_state.setter
    def tag_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb23ccf4400f12e1f6bb4d678caed96ead574d68bb5883232d5316cf877b9037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionNamePrefixes")
    def version_name_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "versionNamePrefixes"))

    @version_name_prefixes.setter
    def version_name_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b867dde34fe1cd145509c7671e05b0944328ed62ff80edb559a10ce958e2d56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionNamePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryCleanupPoliciesCondition]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryCleanupPoliciesCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryCleanupPoliciesCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5186fc3329ef1792585a8e14b81d3363930e7c66da1e95abe7a257cbab89618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleArtifactRegistryRepositoryCleanupPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryCleanupPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eabb9538cf0e6511463748414787940e187d633e1618a3cf5ed528cde8501a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleArtifactRegistryRepositoryCleanupPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec564ec162ea3e6bfadea4eb2f6a876be56e9b0e218eb07b55b03e1973b2e811)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleArtifactRegistryRepositoryCleanupPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0fd45c62ca52a46ace6fcce6881e8508125d92117f21aaa4053119d337f1c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__740de9454f56cd0a286a6927df070053abb1556929e97b472e0910f627c7ec42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7de2f6a1663aee1f4b59d553bc58c2d2b67ac82b59ea5dbfb5135c1686c84012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleArtifactRegistryRepositoryCleanupPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleArtifactRegistryRepositoryCleanupPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleArtifactRegistryRepositoryCleanupPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a45e82609247b72d2a95db6cc9cf96cfe3a404b637fed575573be37a5152e319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions",
    jsii_struct_bases=[],
    name_mapping={
        "keep_count": "keepCount",
        "package_name_prefixes": "packageNamePrefixes",
    },
)
class GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions:
    def __init__(
        self,
        *,
        keep_count: typing.Optional[jsii.Number] = None,
        package_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param keep_count: Minimum number of versions to keep. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#keep_count GoogleArtifactRegistryRepository#keep_count}
        :param package_name_prefixes: Match versions by package prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#package_name_prefixes GoogleArtifactRegistryRepository#package_name_prefixes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b7657fe489f32895823c6607261ddf44c9fcb882d93a5bc66ad5bc4c38d11d9)
            check_type(argname="argument keep_count", value=keep_count, expected_type=type_hints["keep_count"])
            check_type(argname="argument package_name_prefixes", value=package_name_prefixes, expected_type=type_hints["package_name_prefixes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if keep_count is not None:
            self._values["keep_count"] = keep_count
        if package_name_prefixes is not None:
            self._values["package_name_prefixes"] = package_name_prefixes

    @builtins.property
    def keep_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of versions to keep.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#keep_count GoogleArtifactRegistryRepository#keep_count}
        '''
        result = self._values.get("keep_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def package_name_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Match versions by package prefix. Applied on any prefix match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#package_name_prefixes GoogleArtifactRegistryRepository#package_name_prefixes}
        '''
        result = self._values.get("package_name_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77f56a5c387d738fa5fe93825dc1d55011b06630e51c12a62e97fb1ec6e24671)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeepCount")
    def reset_keep_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepCount", []))

    @jsii.member(jsii_name="resetPackageNamePrefixes")
    def reset_package_name_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackageNamePrefixes", []))

    @builtins.property
    @jsii.member(jsii_name="keepCountInput")
    def keep_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepCountInput"))

    @builtins.property
    @jsii.member(jsii_name="packageNamePrefixesInput")
    def package_name_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "packageNamePrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="keepCount")
    def keep_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepCount"))

    @keep_count.setter
    def keep_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__979d4d92e4a9fd9a1dfaf94872de3d2c4aa17295c0f6d8dc2717f4d090413646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packageNamePrefixes")
    def package_name_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "packageNamePrefixes"))

    @package_name_prefixes.setter
    def package_name_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d4c59dcfaf56c0e6baa34acbfaddd23e5b07f3b2e5de3d99d2a9133ed46b09d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageNamePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__778729bd15de3b611803cd125db1e741ad4951393e2cd556530a80ee734593ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleArtifactRegistryRepositoryCleanupPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryCleanupPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4df0b89de0c3967d93c5381fb63cefceebe18a36fd7c2a48ac92414f512a0045)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        newer_than: typing.Optional[builtins.str] = None,
        older_than: typing.Optional[builtins.str] = None,
        package_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_state: typing.Optional[builtins.str] = None,
        version_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param newer_than: Match versions newer than a duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#newer_than GoogleArtifactRegistryRepository#newer_than}
        :param older_than: Match versions older than a duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#older_than GoogleArtifactRegistryRepository#older_than}
        :param package_name_prefixes: Match versions by package prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#package_name_prefixes GoogleArtifactRegistryRepository#package_name_prefixes}
        :param tag_prefixes: Match versions by tag prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#tag_prefixes GoogleArtifactRegistryRepository#tag_prefixes}
        :param tag_state: Match versions by tag status. Default value: "ANY" Possible values: ["TAGGED", "UNTAGGED", "ANY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#tag_state GoogleArtifactRegistryRepository#tag_state}
        :param version_name_prefixes: Match versions by version name prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#version_name_prefixes GoogleArtifactRegistryRepository#version_name_prefixes}
        '''
        value = GoogleArtifactRegistryRepositoryCleanupPoliciesCondition(
            newer_than=newer_than,
            older_than=older_than,
            package_name_prefixes=package_name_prefixes,
            tag_prefixes=tag_prefixes,
            tag_state=tag_state,
            version_name_prefixes=version_name_prefixes,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putMostRecentVersions")
    def put_most_recent_versions(
        self,
        *,
        keep_count: typing.Optional[jsii.Number] = None,
        package_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param keep_count: Minimum number of versions to keep. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#keep_count GoogleArtifactRegistryRepository#keep_count}
        :param package_name_prefixes: Match versions by package prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#package_name_prefixes GoogleArtifactRegistryRepository#package_name_prefixes}
        '''
        value = GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions(
            keep_count=keep_count, package_name_prefixes=package_name_prefixes
        )

        return typing.cast(None, jsii.invoke(self, "putMostRecentVersions", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetMostRecentVersions")
    def reset_most_recent_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMostRecentVersions", []))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(
        self,
    ) -> GoogleArtifactRegistryRepositoryCleanupPoliciesConditionOutputReference:
        return typing.cast(GoogleArtifactRegistryRepositoryCleanupPoliciesConditionOutputReference, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="mostRecentVersions")
    def most_recent_versions(
        self,
    ) -> GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersionsOutputReference:
        return typing.cast(GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersionsOutputReference, jsii.get(self, "mostRecentVersions"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryCleanupPoliciesCondition]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryCleanupPoliciesCondition], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mostRecentVersionsInput")
    def most_recent_versions_input(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions], jsii.get(self, "mostRecentVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c404ce79fe8385e853a3b14503da784bb5d10c7ac76e317e006a38b3dce4e474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2826c0147ff409b32e5cc3be251b00fdf03d065984e997ae7bd95883bfd3000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleArtifactRegistryRepositoryCleanupPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleArtifactRegistryRepositoryCleanupPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleArtifactRegistryRepositoryCleanupPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff66c7fe941a77245f624c161d105400348d42b2baa6b7d20aae314d4387a12f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "format": "format",
        "repository_id": "repositoryId",
        "cleanup_policies": "cleanupPolicies",
        "cleanup_policy_dry_run": "cleanupPolicyDryRun",
        "description": "description",
        "docker_config": "dockerConfig",
        "id": "id",
        "kms_key_name": "kmsKeyName",
        "labels": "labels",
        "location": "location",
        "maven_config": "mavenConfig",
        "mode": "mode",
        "project": "project",
        "remote_repository_config": "remoteRepositoryConfig",
        "timeouts": "timeouts",
        "virtual_repository_config": "virtualRepositoryConfig",
        "vulnerability_scanning_config": "vulnerabilityScanningConfig",
    },
)
class GoogleArtifactRegistryRepositoryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        format: builtins.str,
        repository_id: builtins.str,
        cleanup_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleArtifactRegistryRepositoryCleanupPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cleanup_policy_dry_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        docker_config: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryDockerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        maven_config: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryMavenConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remote_repository_config: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_repository_config: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryVirtualRepositoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vulnerability_scanning_config: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param format: The format of packages that are stored in the repository. Supported formats can be found `here <https://cloud.google.com/artifact-registry/docs/supported-formats>`_. You can only create alpha formats if you are a member of the `alpha user group <https://cloud.google.com/artifact-registry/docs/supported-formats#alpha-access>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#format GoogleArtifactRegistryRepository#format}
        :param repository_id: The last part of the repository name, for example: "repo1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository_id GoogleArtifactRegistryRepository#repository_id}
        :param cleanup_policies: cleanup_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#cleanup_policies GoogleArtifactRegistryRepository#cleanup_policies}
        :param cleanup_policy_dry_run: If true, the cleanup pipeline is prevented from deleting versions in this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#cleanup_policy_dry_run GoogleArtifactRegistryRepository#cleanup_policy_dry_run}
        :param description: The user-provided description of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#description GoogleArtifactRegistryRepository#description}
        :param docker_config: docker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#docker_config GoogleArtifactRegistryRepository#docker_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#id GoogleArtifactRegistryRepository#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: The Cloud KMS resource name of the customer managed encryption key that’s used to encrypt the contents of the Repository. Has the form: 'projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key'. This value may not be changed after the Repository has been created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#kms_key_name GoogleArtifactRegistryRepository#kms_key_name}
        :param labels: Labels with user-defined metadata. This field may contain up to 64 entries. Label keys and values may be no longer than 63 characters. Label keys must begin with a lowercase letter and may only contain lowercase letters, numeric characters, underscores, and dashes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#labels GoogleArtifactRegistryRepository#labels}
        :param location: The name of the repository's location. In addition to specific regions, special values for multi-region locations are 'asia', 'europe', and 'us'. See `here <https://cloud.google.com/artifact-registry/docs/repositories/repo-locations>`_, or use the `google_artifact_registry_locations <https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/artifact_registry_locations>`_ data source for possible values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#location GoogleArtifactRegistryRepository#location}
        :param maven_config: maven_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#maven_config GoogleArtifactRegistryRepository#maven_config}
        :param mode: The mode configures the repository to serve artifacts from different sources. Default value: "STANDARD_REPOSITORY" Possible values: ["STANDARD_REPOSITORY", "VIRTUAL_REPOSITORY", "REMOTE_REPOSITORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#mode GoogleArtifactRegistryRepository#mode}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#project GoogleArtifactRegistryRepository#project}.
        :param remote_repository_config: remote_repository_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#remote_repository_config GoogleArtifactRegistryRepository#remote_repository_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#timeouts GoogleArtifactRegistryRepository#timeouts}
        :param virtual_repository_config: virtual_repository_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#virtual_repository_config GoogleArtifactRegistryRepository#virtual_repository_config}
        :param vulnerability_scanning_config: vulnerability_scanning_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#vulnerability_scanning_config GoogleArtifactRegistryRepository#vulnerability_scanning_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(docker_config, dict):
            docker_config = GoogleArtifactRegistryRepositoryDockerConfig(**docker_config)
        if isinstance(maven_config, dict):
            maven_config = GoogleArtifactRegistryRepositoryMavenConfig(**maven_config)
        if isinstance(remote_repository_config, dict):
            remote_repository_config = GoogleArtifactRegistryRepositoryRemoteRepositoryConfig(**remote_repository_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleArtifactRegistryRepositoryTimeouts(**timeouts)
        if isinstance(virtual_repository_config, dict):
            virtual_repository_config = GoogleArtifactRegistryRepositoryVirtualRepositoryConfig(**virtual_repository_config)
        if isinstance(vulnerability_scanning_config, dict):
            vulnerability_scanning_config = GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig(**vulnerability_scanning_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5088d0d29bb6061ed8033079146f76ffd8db624253986f4fa50416e123b6414)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument repository_id", value=repository_id, expected_type=type_hints["repository_id"])
            check_type(argname="argument cleanup_policies", value=cleanup_policies, expected_type=type_hints["cleanup_policies"])
            check_type(argname="argument cleanup_policy_dry_run", value=cleanup_policy_dry_run, expected_type=type_hints["cleanup_policy_dry_run"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument docker_config", value=docker_config, expected_type=type_hints["docker_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument maven_config", value=maven_config, expected_type=type_hints["maven_config"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument remote_repository_config", value=remote_repository_config, expected_type=type_hints["remote_repository_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument virtual_repository_config", value=virtual_repository_config, expected_type=type_hints["virtual_repository_config"])
            check_type(argname="argument vulnerability_scanning_config", value=vulnerability_scanning_config, expected_type=type_hints["vulnerability_scanning_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "format": format,
            "repository_id": repository_id,
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
        if cleanup_policies is not None:
            self._values["cleanup_policies"] = cleanup_policies
        if cleanup_policy_dry_run is not None:
            self._values["cleanup_policy_dry_run"] = cleanup_policy_dry_run
        if description is not None:
            self._values["description"] = description
        if docker_config is not None:
            self._values["docker_config"] = docker_config
        if id is not None:
            self._values["id"] = id
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
        if maven_config is not None:
            self._values["maven_config"] = maven_config
        if mode is not None:
            self._values["mode"] = mode
        if project is not None:
            self._values["project"] = project
        if remote_repository_config is not None:
            self._values["remote_repository_config"] = remote_repository_config
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if virtual_repository_config is not None:
            self._values["virtual_repository_config"] = virtual_repository_config
        if vulnerability_scanning_config is not None:
            self._values["vulnerability_scanning_config"] = vulnerability_scanning_config

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
    def format(self) -> builtins.str:
        '''The format of packages that are stored in the repository.

        Supported formats
        can be found `here <https://cloud.google.com/artifact-registry/docs/supported-formats>`_.
        You can only create alpha formats if you are a member of the
        `alpha user group <https://cloud.google.com/artifact-registry/docs/supported-formats#alpha-access>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#format GoogleArtifactRegistryRepository#format}
        '''
        result = self._values.get("format")
        assert result is not None, "Required property 'format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_id(self) -> builtins.str:
        '''The last part of the repository name, for example: "repo1".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository_id GoogleArtifactRegistryRepository#repository_id}
        '''
        result = self._values.get("repository_id")
        assert result is not None, "Required property 'repository_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cleanup_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleArtifactRegistryRepositoryCleanupPolicies]]]:
        '''cleanup_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#cleanup_policies GoogleArtifactRegistryRepository#cleanup_policies}
        '''
        result = self._values.get("cleanup_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleArtifactRegistryRepositoryCleanupPolicies]]], result)

    @builtins.property
    def cleanup_policy_dry_run(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the cleanup pipeline is prevented from deleting versions in this repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#cleanup_policy_dry_run GoogleArtifactRegistryRepository#cleanup_policy_dry_run}
        '''
        result = self._values.get("cleanup_policy_dry_run")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The user-provided description of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#description GoogleArtifactRegistryRepository#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_config(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryDockerConfig"]:
        '''docker_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#docker_config GoogleArtifactRegistryRepository#docker_config}
        '''
        result = self._values.get("docker_config")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryDockerConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#id GoogleArtifactRegistryRepository#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The Cloud KMS resource name of the customer managed encryption key that’s used to encrypt the contents of the Repository.

        Has the form:
        'projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key'.
        This value may not be changed after the Repository has been created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#kms_key_name GoogleArtifactRegistryRepository#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels with user-defined metadata.

        This field may contain up to 64 entries. Label keys and values may be no
        longer than 63 characters. Label keys must begin with a lowercase letter
        and may only contain lowercase letters, numeric characters, underscores,
        and dashes.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#labels GoogleArtifactRegistryRepository#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The name of the repository's location.

        In addition to specific regions,
        special values for multi-region locations are 'asia', 'europe', and 'us'.
        See `here <https://cloud.google.com/artifact-registry/docs/repositories/repo-locations>`_,
        or use the
        `google_artifact_registry_locations <https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/artifact_registry_locations>`_
        data source for possible values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#location GoogleArtifactRegistryRepository#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_config(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryMavenConfig"]:
        '''maven_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#maven_config GoogleArtifactRegistryRepository#maven_config}
        '''
        result = self._values.get("maven_config")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryMavenConfig"], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The mode configures the repository to serve artifacts from different sources. Default value: "STANDARD_REPOSITORY" Possible values: ["STANDARD_REPOSITORY", "VIRTUAL_REPOSITORY", "REMOTE_REPOSITORY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#mode GoogleArtifactRegistryRepository#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#project GoogleArtifactRegistryRepository#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_repository_config(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfig"]:
        '''remote_repository_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#remote_repository_config GoogleArtifactRegistryRepository#remote_repository_config}
        '''
        result = self._values.get("remote_repository_config")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleArtifactRegistryRepositoryTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#timeouts GoogleArtifactRegistryRepository#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryTimeouts"], result)

    @builtins.property
    def virtual_repository_config(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryVirtualRepositoryConfig"]:
        '''virtual_repository_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#virtual_repository_config GoogleArtifactRegistryRepository#virtual_repository_config}
        '''
        result = self._values.get("virtual_repository_config")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryVirtualRepositoryConfig"], result)

    @builtins.property
    def vulnerability_scanning_config(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig"]:
        '''vulnerability_scanning_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#vulnerability_scanning_config GoogleArtifactRegistryRepository#vulnerability_scanning_config}
        '''
        result = self._values.get("vulnerability_scanning_config")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryDockerConfig",
    jsii_struct_bases=[],
    name_mapping={"immutable_tags": "immutableTags"},
)
class GoogleArtifactRegistryRepositoryDockerConfig:
    def __init__(
        self,
        *,
        immutable_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param immutable_tags: The repository which enabled this flag prevents all tags from being modified, moved or deleted. This does not prevent tags from being created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#immutable_tags GoogleArtifactRegistryRepository#immutable_tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f5546da03f0a36d2ba2086fd28a4f0bedd4adcb91d34687fd23ec31d9340c6)
            check_type(argname="argument immutable_tags", value=immutable_tags, expected_type=type_hints["immutable_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if immutable_tags is not None:
            self._values["immutable_tags"] = immutable_tags

    @builtins.property
    def immutable_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The repository which enabled this flag prevents all tags from being modified, moved or deleted.

        This does not prevent tags from being created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#immutable_tags GoogleArtifactRegistryRepository#immutable_tags}
        '''
        result = self._values.get("immutable_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryDockerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryDockerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryDockerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ebae7feb9192fe8276f41f9914268b82fa1ad588fb88562d165287aaa8c24fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImmutableTags")
    def reset_immutable_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImmutableTags", []))

    @builtins.property
    @jsii.member(jsii_name="immutableTagsInput")
    def immutable_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "immutableTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="immutableTags")
    def immutable_tags(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "immutableTags"))

    @immutable_tags.setter
    def immutable_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de4b4341d3cbb36cdaba4fd0cc3b01937bbe2e5f10051bdcbffbe09f4ec7b57d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "immutableTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryDockerConfig]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryDockerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryDockerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__278ef6879dfe25305d05e7f7de36e073f7669109bf4f13ece6d479c470068aa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryMavenConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allow_snapshot_overwrites": "allowSnapshotOverwrites",
        "version_policy": "versionPolicy",
    },
)
class GoogleArtifactRegistryRepositoryMavenConfig:
    def __init__(
        self,
        *,
        allow_snapshot_overwrites: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        version_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_snapshot_overwrites: The repository with this flag will allow publishing the same snapshot versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#allow_snapshot_overwrites GoogleArtifactRegistryRepository#allow_snapshot_overwrites}
        :param version_policy: Version policy defines the versions that the registry will accept. Default value: "VERSION_POLICY_UNSPECIFIED" Possible values: ["VERSION_POLICY_UNSPECIFIED", "RELEASE", "SNAPSHOT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#version_policy GoogleArtifactRegistryRepository#version_policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b86106113cd2326dfa091d75b12f264666750a8e018f6f9dd440d5671916a28f)
            check_type(argname="argument allow_snapshot_overwrites", value=allow_snapshot_overwrites, expected_type=type_hints["allow_snapshot_overwrites"])
            check_type(argname="argument version_policy", value=version_policy, expected_type=type_hints["version_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_snapshot_overwrites is not None:
            self._values["allow_snapshot_overwrites"] = allow_snapshot_overwrites
        if version_policy is not None:
            self._values["version_policy"] = version_policy

    @builtins.property
    def allow_snapshot_overwrites(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The repository with this flag will allow publishing the same snapshot versions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#allow_snapshot_overwrites GoogleArtifactRegistryRepository#allow_snapshot_overwrites}
        '''
        result = self._values.get("allow_snapshot_overwrites")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def version_policy(self) -> typing.Optional[builtins.str]:
        '''Version policy defines the versions that the registry will accept. Default value: "VERSION_POLICY_UNSPECIFIED" Possible values: ["VERSION_POLICY_UNSPECIFIED", "RELEASE", "SNAPSHOT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#version_policy GoogleArtifactRegistryRepository#version_policy}
        '''
        result = self._values.get("version_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryMavenConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryMavenConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryMavenConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbf716c7ee8f7e3708ae13c4a5ed91553e2752a5a2dc59bcabdb0955a5350231)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowSnapshotOverwrites")
    def reset_allow_snapshot_overwrites(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowSnapshotOverwrites", []))

    @jsii.member(jsii_name="resetVersionPolicy")
    def reset_version_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="allowSnapshotOverwritesInput")
    def allow_snapshot_overwrites_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowSnapshotOverwritesInput"))

    @builtins.property
    @jsii.member(jsii_name="versionPolicyInput")
    def version_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="allowSnapshotOverwrites")
    def allow_snapshot_overwrites(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowSnapshotOverwrites"))

    @allow_snapshot_overwrites.setter
    def allow_snapshot_overwrites(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b444a1b5f285427c2eab3b45eaf064e7331ea489897b86ae9d7be87d33b10a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowSnapshotOverwrites", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionPolicy")
    def version_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionPolicy"))

    @version_policy.setter
    def version_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b51472012f31563968da9a4298b224009dce64b3e481bb595e29aaed363681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryMavenConfig]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryMavenConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryMavenConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55ec6ac288c11e20f2f29ea7e5ac0c01034509432a7fd1eb1d38a1c98a11c6cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "apt_repository": "aptRepository",
        "common_repository": "commonRepository",
        "description": "description",
        "disable_upstream_validation": "disableUpstreamValidation",
        "docker_repository": "dockerRepository",
        "maven_repository": "mavenRepository",
        "npm_repository": "npmRepository",
        "python_repository": "pythonRepository",
        "upstream_credentials": "upstreamCredentials",
        "yum_repository": "yumRepository",
    },
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfig:
    def __init__(
        self,
        *,
        apt_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        common_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_upstream_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        docker_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        maven_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        npm_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        python_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        upstream_credentials: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        yum_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt_repository: apt_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#apt_repository GoogleArtifactRegistryRepository#apt_repository}
        :param common_repository: common_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#common_repository GoogleArtifactRegistryRepository#common_repository}
        :param description: The description of the remote source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#description GoogleArtifactRegistryRepository#description}
        :param disable_upstream_validation: If true, the remote repository upstream and upstream credentials will not be validated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#disable_upstream_validation GoogleArtifactRegistryRepository#disable_upstream_validation}
        :param docker_repository: docker_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#docker_repository GoogleArtifactRegistryRepository#docker_repository}
        :param maven_repository: maven_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#maven_repository GoogleArtifactRegistryRepository#maven_repository}
        :param npm_repository: npm_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#npm_repository GoogleArtifactRegistryRepository#npm_repository}
        :param python_repository: python_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#python_repository GoogleArtifactRegistryRepository#python_repository}
        :param upstream_credentials: upstream_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#upstream_credentials GoogleArtifactRegistryRepository#upstream_credentials}
        :param yum_repository: yum_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#yum_repository GoogleArtifactRegistryRepository#yum_repository}
        '''
        if isinstance(apt_repository, dict):
            apt_repository = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository(**apt_repository)
        if isinstance(common_repository, dict):
            common_repository = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository(**common_repository)
        if isinstance(docker_repository, dict):
            docker_repository = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository(**docker_repository)
        if isinstance(maven_repository, dict):
            maven_repository = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository(**maven_repository)
        if isinstance(npm_repository, dict):
            npm_repository = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository(**npm_repository)
        if isinstance(python_repository, dict):
            python_repository = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository(**python_repository)
        if isinstance(upstream_credentials, dict):
            upstream_credentials = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials(**upstream_credentials)
        if isinstance(yum_repository, dict):
            yum_repository = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository(**yum_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3124b5f04fe207fe7b9f7e70d5948dd0cc5b9ac58ea072a6c9b8ad38fa12ec7)
            check_type(argname="argument apt_repository", value=apt_repository, expected_type=type_hints["apt_repository"])
            check_type(argname="argument common_repository", value=common_repository, expected_type=type_hints["common_repository"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_upstream_validation", value=disable_upstream_validation, expected_type=type_hints["disable_upstream_validation"])
            check_type(argname="argument docker_repository", value=docker_repository, expected_type=type_hints["docker_repository"])
            check_type(argname="argument maven_repository", value=maven_repository, expected_type=type_hints["maven_repository"])
            check_type(argname="argument npm_repository", value=npm_repository, expected_type=type_hints["npm_repository"])
            check_type(argname="argument python_repository", value=python_repository, expected_type=type_hints["python_repository"])
            check_type(argname="argument upstream_credentials", value=upstream_credentials, expected_type=type_hints["upstream_credentials"])
            check_type(argname="argument yum_repository", value=yum_repository, expected_type=type_hints["yum_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apt_repository is not None:
            self._values["apt_repository"] = apt_repository
        if common_repository is not None:
            self._values["common_repository"] = common_repository
        if description is not None:
            self._values["description"] = description
        if disable_upstream_validation is not None:
            self._values["disable_upstream_validation"] = disable_upstream_validation
        if docker_repository is not None:
            self._values["docker_repository"] = docker_repository
        if maven_repository is not None:
            self._values["maven_repository"] = maven_repository
        if npm_repository is not None:
            self._values["npm_repository"] = npm_repository
        if python_repository is not None:
            self._values["python_repository"] = python_repository
        if upstream_credentials is not None:
            self._values["upstream_credentials"] = upstream_credentials
        if yum_repository is not None:
            self._values["yum_repository"] = yum_repository

    @builtins.property
    def apt_repository(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository"]:
        '''apt_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#apt_repository GoogleArtifactRegistryRepository#apt_repository}
        '''
        result = self._values.get("apt_repository")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository"], result)

    @builtins.property
    def common_repository(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository"]:
        '''common_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#common_repository GoogleArtifactRegistryRepository#common_repository}
        '''
        result = self._values.get("common_repository")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the remote source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#description GoogleArtifactRegistryRepository#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_upstream_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the remote repository upstream and upstream credentials will not be validated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#disable_upstream_validation GoogleArtifactRegistryRepository#disable_upstream_validation}
        '''
        result = self._values.get("disable_upstream_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def docker_repository(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository"]:
        '''docker_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#docker_repository GoogleArtifactRegistryRepository#docker_repository}
        '''
        result = self._values.get("docker_repository")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository"], result)

    @builtins.property
    def maven_repository(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository"]:
        '''maven_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#maven_repository GoogleArtifactRegistryRepository#maven_repository}
        '''
        result = self._values.get("maven_repository")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository"], result)

    @builtins.property
    def npm_repository(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository"]:
        '''npm_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#npm_repository GoogleArtifactRegistryRepository#npm_repository}
        '''
        result = self._values.get("npm_repository")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository"], result)

    @builtins.property
    def python_repository(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository"]:
        '''python_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#python_repository GoogleArtifactRegistryRepository#python_repository}
        '''
        result = self._values.get("python_repository")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository"], result)

    @builtins.property
    def upstream_credentials(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials"]:
        '''upstream_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#upstream_credentials GoogleArtifactRegistryRepository#upstream_credentials}
        '''
        result = self._values.get("upstream_credentials")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials"], result)

    @builtins.property
    def yum_repository(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository"]:
        '''yum_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#yum_repository GoogleArtifactRegistryRepository#yum_repository}
        '''
        result = self._values.get("yum_repository")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository",
    jsii_struct_bases=[],
    name_mapping={"public_repository": "publicRepository"},
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository:
    def __init__(
        self,
        *,
        public_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param public_repository: public_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        if isinstance(public_repository, dict):
            public_repository = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository(**public_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2c980bd897a66a6e1ba0fac71475d96f8469e5c0d76a98a194221c8052eba97)
            check_type(argname="argument public_repository", value=public_repository, expected_type=type_hints["public_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if public_repository is not None:
            self._values["public_repository"] = public_repository

    @builtins.property
    def public_repository(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository"]:
        '''public_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a70ff9c6559d97f914267bf813857c593d27eff5b4416cc9e098dc28dca3afde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPublicRepository")
    def put_public_repository(
        self,
        *,
        repository_base: builtins.str,
        repository_path: builtins.str,
    ) -> None:
        '''
        :param repository_base: A common public repository base for Apt, e.g. '"debian/dists/buster"' Possible values: ["DEBIAN", "UBUNTU", "DEBIAN_SNAPSHOT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository_base GoogleArtifactRegistryRepository#repository_base}
        :param repository_path: Specific repository from the base. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository_path GoogleArtifactRegistryRepository#repository_path}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository(
            repository_base=repository_base, repository_path=repository_path
        )

        return typing.cast(None, jsii.invoke(self, "putPublicRepository", [value]))

    @jsii.member(jsii_name="resetPublicRepository")
    def reset_public_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicRepository", []))

    @builtins.property
    @jsii.member(jsii_name="publicRepository")
    def public_repository(
        self,
    ) -> "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepositoryOutputReference":
        return typing.cast("GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepositoryOutputReference", jsii.get(self, "publicRepository"))

    @builtins.property
    @jsii.member(jsii_name="publicRepositoryInput")
    def public_repository_input(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository"]:
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository"], jsii.get(self, "publicRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0de235d7c38f16a6d8840cf942f4adb666f9bfe4bb13679d69f739308b014b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository",
    jsii_struct_bases=[],
    name_mapping={
        "repository_base": "repositoryBase",
        "repository_path": "repositoryPath",
    },
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository:
    def __init__(
        self,
        *,
        repository_base: builtins.str,
        repository_path: builtins.str,
    ) -> None:
        '''
        :param repository_base: A common public repository base for Apt, e.g. '"debian/dists/buster"' Possible values: ["DEBIAN", "UBUNTU", "DEBIAN_SNAPSHOT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository_base GoogleArtifactRegistryRepository#repository_base}
        :param repository_path: Specific repository from the base. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository_path GoogleArtifactRegistryRepository#repository_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a18b06196991ef20227e05d2ccd0d64da3ee90e55552f2bf52995cc0c0bdca10)
            check_type(argname="argument repository_base", value=repository_base, expected_type=type_hints["repository_base"])
            check_type(argname="argument repository_path", value=repository_path, expected_type=type_hints["repository_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_base": repository_base,
            "repository_path": repository_path,
        }

    @builtins.property
    def repository_base(self) -> builtins.str:
        '''A common public repository base for Apt, e.g. '"debian/dists/buster"' Possible values: ["DEBIAN", "UBUNTU", "DEBIAN_SNAPSHOT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository_base GoogleArtifactRegistryRepository#repository_base}
        '''
        result = self._values.get("repository_base")
        assert result is not None, "Required property 'repository_base' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_path(self) -> builtins.str:
        '''Specific repository from the base.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository_path GoogleArtifactRegistryRepository#repository_path}
        '''
        result = self._values.get("repository_path")
        assert result is not None, "Required property 'repository_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90028c5a9815c992b3c66f7f896bc6e1c0d7164b58efa49d58c256183b48b701)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="repositoryBaseInput")
    def repository_base_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryBaseInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryPathInput")
    def repository_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryPathInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryBase")
    def repository_base(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryBase"))

    @repository_base.setter
    def repository_base(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c95103958c34778e85f7ce67a1995e0225793ccdf16e0f29c10b18a9c70e1928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryBase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryPath")
    def repository_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryPath"))

    @repository_path.setter
    def repository_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc426db723ea553c6feb1042b1d207c8d0450467beaf88f8df43db09c5345b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e964e0fd8aa6114f86cdff78bcf797a3e49cb30dd73cce576f520eaefb899d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository:
    def __init__(self, *, uri: builtins.str) -> None:
        '''
        :param uri: One of: a. Artifact Registry Repository resource, e.g. 'projects/UPSTREAM_PROJECT_ID/locations/REGION/repositories/UPSTREAM_REPOSITORY' b. URI to the registry, e.g. '"https://registry-1.docker.io"' c. URI to Artifact Registry Repository, e.g. '"https://REGION-docker.pkg.dev/UPSTREAM_PROJECT_ID/UPSTREAM_REPOSITORY"' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#uri GoogleArtifactRegistryRepository#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5416e6d3d30e6e9d116c2e47af1ca0719c0836babd651bd3a98ae0516c3bc699)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }

    @builtins.property
    def uri(self) -> builtins.str:
        '''One of: a.

        Artifact Registry Repository resource, e.g. 'projects/UPSTREAM_PROJECT_ID/locations/REGION/repositories/UPSTREAM_REPOSITORY'
        b. URI to the registry, e.g. '"https://registry-1.docker.io"'
        c. URI to Artifact Registry Repository, e.g. '"https://REGION-docker.pkg.dev/UPSTREAM_PROJECT_ID/UPSTREAM_REPOSITORY"'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#uri GoogleArtifactRegistryRepository#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb82924f44558836601a6ac5954d978f27f002f4f86c5dc91d2bf5b92448edb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e94a3f0d497c546eecb47d8abb65bcc9b94d2a4b11601ffb58ab8e2abf2ccfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d4abe5ba28794b8828ea604b749a848b6406080339f9a8c38c7a30a84867ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository",
    jsii_struct_bases=[],
    name_mapping={
        "custom_repository": "customRepository",
        "public_repository": "publicRepository",
    },
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository:
    def __init__(
        self,
        *,
        custom_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#custom_repository GoogleArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "DOCKER_HUB" Possible values: ["DOCKER_HUB"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        if isinstance(custom_repository, dict):
            custom_repository = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository(**custom_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fe2c5a77bb1705dcdf629eeb965b6991604a2b6f152a4c0c81a4ac531d86c63)
            check_type(argname="argument custom_repository", value=custom_repository, expected_type=type_hints["custom_repository"])
            check_type(argname="argument public_repository", value=public_repository, expected_type=type_hints["public_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_repository is not None:
            self._values["custom_repository"] = custom_repository
        if public_repository is not None:
            self._values["public_repository"] = public_repository

    @builtins.property
    def custom_repository(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository"]:
        '''custom_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#custom_repository GoogleArtifactRegistryRepository#custom_repository}
        '''
        result = self._values.get("custom_repository")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository"], result)

    @builtins.property
    def public_repository(self) -> typing.Optional[builtins.str]:
        '''Address of the remote repository. Default value: "DOCKER_HUB" Possible values: ["DOCKER_HUB"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: Specific uri to the registry, e.g. '"https://registry-1.docker.io"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#uri GoogleArtifactRegistryRepository#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c654deba80c25bb018f35a53e6c1fd60e5812a729d693551393fa3c8caf083)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''Specific uri to the registry, e.g. '"https://registry-1.docker.io"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#uri GoogleArtifactRegistryRepository#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f557312eb6e63788a82c884fe33e09451a7ff3408233a3a0fcc720f1e10302a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9af5b607030e29fe521332eaa8fd1b65379275da0329c1475dc4ac8411d953e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5165ceda46a0cdd88f4049153adf4c460ab80d477dd3e876fcf1ebfca2b16f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__040cbeb20e8cafcadf2397a94e2cd6b4428dcc5af0ba3f7eb8d0c27b1078e8d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomRepository")
    def put_custom_repository(
        self,
        *,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Specific uri to the registry, e.g. '"https://registry-1.docker.io"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#uri GoogleArtifactRegistryRepository#uri}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository(
            uri=uri
        )

        return typing.cast(None, jsii.invoke(self, "putCustomRepository", [value]))

    @jsii.member(jsii_name="resetCustomRepository")
    def reset_custom_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRepository", []))

    @jsii.member(jsii_name="resetPublicRepository")
    def reset_public_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicRepository", []))

    @builtins.property
    @jsii.member(jsii_name="customRepository")
    def custom_repository(
        self,
    ) -> GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepositoryOutputReference:
        return typing.cast(GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepositoryOutputReference, jsii.get(self, "customRepository"))

    @builtins.property
    @jsii.member(jsii_name="customRepositoryInput")
    def custom_repository_input(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository], jsii.get(self, "customRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="publicRepositoryInput")
    def public_repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="publicRepository")
    def public_repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicRepository"))

    @public_repository.setter
    def public_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66d2feabb5f4c368b27b272540662a1a9503442d86b2461a00d56e4ec2c9d8a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicRepository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6583a2160ab7438cb3c884ba152391468a61b2e6724b19345ee684f8c205cea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository",
    jsii_struct_bases=[],
    name_mapping={
        "custom_repository": "customRepository",
        "public_repository": "publicRepository",
    },
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository:
    def __init__(
        self,
        *,
        custom_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#custom_repository GoogleArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "MAVEN_CENTRAL" Possible values: ["MAVEN_CENTRAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        if isinstance(custom_repository, dict):
            custom_repository = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository(**custom_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__173b40bd336c8fb892b551bfee1c08ea8e99b0d47cea7fa9c4c0f1a9ee0b07a3)
            check_type(argname="argument custom_repository", value=custom_repository, expected_type=type_hints["custom_repository"])
            check_type(argname="argument public_repository", value=public_repository, expected_type=type_hints["public_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_repository is not None:
            self._values["custom_repository"] = custom_repository
        if public_repository is not None:
            self._values["public_repository"] = public_repository

    @builtins.property
    def custom_repository(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository"]:
        '''custom_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#custom_repository GoogleArtifactRegistryRepository#custom_repository}
        '''
        result = self._values.get("custom_repository")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository"], result)

    @builtins.property
    def public_repository(self) -> typing.Optional[builtins.str]:
        '''Address of the remote repository. Default value: "MAVEN_CENTRAL" Possible values: ["MAVEN_CENTRAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: Specific uri to the registry, e.g. '"https://repo.maven.apache.org/maven2"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#uri GoogleArtifactRegistryRepository#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b6cee98bfe8df617df15db462157405f642b3d1ea77af7c70d757126db1fe0)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''Specific uri to the registry, e.g. '"https://repo.maven.apache.org/maven2"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#uri GoogleArtifactRegistryRepository#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f83aeae67e6a0f51950f674c579a08ec39a53292b0437ba983d4747d2bcd468)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd0d8a260e01be207144075e74576f22d8b02f882ec756d9032a21938baaf34e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c13d2bc7239c93d59be7447ea9ba85d6c8a2e82fce56934727901a8dbe1cfc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68d46c3562237d2564056f8672c0d6b01221c22fd9ca4cda640c2e486943f111)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomRepository")
    def put_custom_repository(
        self,
        *,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Specific uri to the registry, e.g. '"https://repo.maven.apache.org/maven2"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#uri GoogleArtifactRegistryRepository#uri}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository(
            uri=uri
        )

        return typing.cast(None, jsii.invoke(self, "putCustomRepository", [value]))

    @jsii.member(jsii_name="resetCustomRepository")
    def reset_custom_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRepository", []))

    @jsii.member(jsii_name="resetPublicRepository")
    def reset_public_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicRepository", []))

    @builtins.property
    @jsii.member(jsii_name="customRepository")
    def custom_repository(
        self,
    ) -> GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepositoryOutputReference:
        return typing.cast(GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepositoryOutputReference, jsii.get(self, "customRepository"))

    @builtins.property
    @jsii.member(jsii_name="customRepositoryInput")
    def custom_repository_input(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository], jsii.get(self, "customRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="publicRepositoryInput")
    def public_repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="publicRepository")
    def public_repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicRepository"))

    @public_repository.setter
    def public_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f760049bd8b335982e2099781703d0498c3d08e1dc5d08ac5a9415b0c72ee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicRepository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054fb94a56443fc8592c59b979b942bae9fb051f0c0bc09ce2fc26aedb68969a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository",
    jsii_struct_bases=[],
    name_mapping={
        "custom_repository": "customRepository",
        "public_repository": "publicRepository",
    },
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository:
    def __init__(
        self,
        *,
        custom_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#custom_repository GoogleArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "NPMJS" Possible values: ["NPMJS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        if isinstance(custom_repository, dict):
            custom_repository = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository(**custom_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f16c15d1e8c7e326bece8c32c34f84fadf77ae1818e4134d6e2e230f9f6f96a3)
            check_type(argname="argument custom_repository", value=custom_repository, expected_type=type_hints["custom_repository"])
            check_type(argname="argument public_repository", value=public_repository, expected_type=type_hints["public_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_repository is not None:
            self._values["custom_repository"] = custom_repository
        if public_repository is not None:
            self._values["public_repository"] = public_repository

    @builtins.property
    def custom_repository(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository"]:
        '''custom_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#custom_repository GoogleArtifactRegistryRepository#custom_repository}
        '''
        result = self._values.get("custom_repository")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository"], result)

    @builtins.property
    def public_repository(self) -> typing.Optional[builtins.str]:
        '''Address of the remote repository. Default value: "NPMJS" Possible values: ["NPMJS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: Specific uri to the registry, e.g. '"https://registry.npmjs.org"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#uri GoogleArtifactRegistryRepository#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2abae1225bf51aaf0e05bf6cdc01afa1108441e15d436f28cb6aba82f532fa)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''Specific uri to the registry, e.g. '"https://registry.npmjs.org"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#uri GoogleArtifactRegistryRepository#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94d81367179bb45d7a79e8ca227219996cdfc5b95cbf9f43e4eaaf6031fc2de5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c029cd57965ce34bc7cde06db7b856360ec3e8f4c894d9be1e596f53ea936a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b466d8bff5ca1a2bcdf767a63fd95eaf433f0a93fceb0a4d8b058edbcdd2d4ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a1f724e4e99864d72be51c8b3f7c82578696934893ddf257b6b71773d0cf95c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomRepository")
    def put_custom_repository(
        self,
        *,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Specific uri to the registry, e.g. '"https://registry.npmjs.org"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#uri GoogleArtifactRegistryRepository#uri}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository(
            uri=uri
        )

        return typing.cast(None, jsii.invoke(self, "putCustomRepository", [value]))

    @jsii.member(jsii_name="resetCustomRepository")
    def reset_custom_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRepository", []))

    @jsii.member(jsii_name="resetPublicRepository")
    def reset_public_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicRepository", []))

    @builtins.property
    @jsii.member(jsii_name="customRepository")
    def custom_repository(
        self,
    ) -> GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepositoryOutputReference:
        return typing.cast(GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepositoryOutputReference, jsii.get(self, "customRepository"))

    @builtins.property
    @jsii.member(jsii_name="customRepositoryInput")
    def custom_repository_input(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository], jsii.get(self, "customRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="publicRepositoryInput")
    def public_repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="publicRepository")
    def public_repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicRepository"))

    @public_repository.setter
    def public_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e0f119341719bd3ab10524a043e74d6e1dd5d244588b0b3436d2febc13252e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicRepository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36862856d4d641184221e86d78090b9211efb3dfa061e1469d9a97fd8fe2ca80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9316ff569fd0ec931a3c0c169b1d986bd6bca28e03205e7f1af06ab55df0002)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAptRepository")
    def put_apt_repository(
        self,
        *,
        public_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param public_repository: public_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository(
            public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putAptRepository", [value]))

    @jsii.member(jsii_name="putCommonRepository")
    def put_common_repository(self, *, uri: builtins.str) -> None:
        '''
        :param uri: One of: a. Artifact Registry Repository resource, e.g. 'projects/UPSTREAM_PROJECT_ID/locations/REGION/repositories/UPSTREAM_REPOSITORY' b. URI to the registry, e.g. '"https://registry-1.docker.io"' c. URI to Artifact Registry Repository, e.g. '"https://REGION-docker.pkg.dev/UPSTREAM_PROJECT_ID/UPSTREAM_REPOSITORY"' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#uri GoogleArtifactRegistryRepository#uri}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository(
            uri=uri
        )

        return typing.cast(None, jsii.invoke(self, "putCommonRepository", [value]))

    @jsii.member(jsii_name="putDockerRepository")
    def put_docker_repository(
        self,
        *,
        custom_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository, typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#custom_repository GoogleArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "DOCKER_HUB" Possible values: ["DOCKER_HUB"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository(
            custom_repository=custom_repository, public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putDockerRepository", [value]))

    @jsii.member(jsii_name="putMavenRepository")
    def put_maven_repository(
        self,
        *,
        custom_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository, typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#custom_repository GoogleArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "MAVEN_CENTRAL" Possible values: ["MAVEN_CENTRAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository(
            custom_repository=custom_repository, public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putMavenRepository", [value]))

    @jsii.member(jsii_name="putNpmRepository")
    def put_npm_repository(
        self,
        *,
        custom_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository, typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#custom_repository GoogleArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "NPMJS" Possible values: ["NPMJS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository(
            custom_repository=custom_repository, public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putNpmRepository", [value]))

    @jsii.member(jsii_name="putPythonRepository")
    def put_python_repository(
        self,
        *,
        custom_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#custom_repository GoogleArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "PYPI" Possible values: ["PYPI"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository(
            custom_repository=custom_repository, public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putPythonRepository", [value]))

    @jsii.member(jsii_name="putUpstreamCredentials")
    def put_upstream_credentials(
        self,
        *,
        username_password_credentials: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param username_password_credentials: username_password_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#username_password_credentials GoogleArtifactRegistryRepository#username_password_credentials}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials(
            username_password_credentials=username_password_credentials
        )

        return typing.cast(None, jsii.invoke(self, "putUpstreamCredentials", [value]))

    @jsii.member(jsii_name="putYumRepository")
    def put_yum_repository(
        self,
        *,
        public_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param public_repository: public_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository(
            public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putYumRepository", [value]))

    @jsii.member(jsii_name="resetAptRepository")
    def reset_apt_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAptRepository", []))

    @jsii.member(jsii_name="resetCommonRepository")
    def reset_common_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonRepository", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisableUpstreamValidation")
    def reset_disable_upstream_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableUpstreamValidation", []))

    @jsii.member(jsii_name="resetDockerRepository")
    def reset_docker_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerRepository", []))

    @jsii.member(jsii_name="resetMavenRepository")
    def reset_maven_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMavenRepository", []))

    @jsii.member(jsii_name="resetNpmRepository")
    def reset_npm_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNpmRepository", []))

    @jsii.member(jsii_name="resetPythonRepository")
    def reset_python_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPythonRepository", []))

    @jsii.member(jsii_name="resetUpstreamCredentials")
    def reset_upstream_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpstreamCredentials", []))

    @jsii.member(jsii_name="resetYumRepository")
    def reset_yum_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYumRepository", []))

    @builtins.property
    @jsii.member(jsii_name="aptRepository")
    def apt_repository(
        self,
    ) -> GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryOutputReference:
        return typing.cast(GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryOutputReference, jsii.get(self, "aptRepository"))

    @builtins.property
    @jsii.member(jsii_name="commonRepository")
    def common_repository(
        self,
    ) -> GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepositoryOutputReference:
        return typing.cast(GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepositoryOutputReference, jsii.get(self, "commonRepository"))

    @builtins.property
    @jsii.member(jsii_name="dockerRepository")
    def docker_repository(
        self,
    ) -> GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryOutputReference:
        return typing.cast(GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryOutputReference, jsii.get(self, "dockerRepository"))

    @builtins.property
    @jsii.member(jsii_name="mavenRepository")
    def maven_repository(
        self,
    ) -> GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryOutputReference:
        return typing.cast(GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryOutputReference, jsii.get(self, "mavenRepository"))

    @builtins.property
    @jsii.member(jsii_name="npmRepository")
    def npm_repository(
        self,
    ) -> GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryOutputReference:
        return typing.cast(GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryOutputReference, jsii.get(self, "npmRepository"))

    @builtins.property
    @jsii.member(jsii_name="pythonRepository")
    def python_repository(
        self,
    ) -> "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryOutputReference":
        return typing.cast("GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryOutputReference", jsii.get(self, "pythonRepository"))

    @builtins.property
    @jsii.member(jsii_name="upstreamCredentials")
    def upstream_credentials(
        self,
    ) -> "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsOutputReference":
        return typing.cast("GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsOutputReference", jsii.get(self, "upstreamCredentials"))

    @builtins.property
    @jsii.member(jsii_name="yumRepository")
    def yum_repository(
        self,
    ) -> "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryOutputReference":
        return typing.cast("GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryOutputReference", jsii.get(self, "yumRepository"))

    @builtins.property
    @jsii.member(jsii_name="aptRepositoryInput")
    def apt_repository_input(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository], jsii.get(self, "aptRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="commonRepositoryInput")
    def common_repository_input(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository], jsii.get(self, "commonRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disableUpstreamValidationInput")
    def disable_upstream_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableUpstreamValidationInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerRepositoryInput")
    def docker_repository_input(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository], jsii.get(self, "dockerRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="mavenRepositoryInput")
    def maven_repository_input(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository], jsii.get(self, "mavenRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="npmRepositoryInput")
    def npm_repository_input(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository], jsii.get(self, "npmRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="pythonRepositoryInput")
    def python_repository_input(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository"]:
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository"], jsii.get(self, "pythonRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="upstreamCredentialsInput")
    def upstream_credentials_input(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials"]:
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials"], jsii.get(self, "upstreamCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="yumRepositoryInput")
    def yum_repository_input(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository"]:
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository"], jsii.get(self, "yumRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb3ac6e429dd4a3f62e133f393354fd6cb3a2e16178dce77ebeeb71df894d9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableUpstreamValidation")
    def disable_upstream_validation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableUpstreamValidation"))

    @disable_upstream_validation.setter
    def disable_upstream_validation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d9145d71e5ce9f06b81f73e417c51d7d74078aa203c1de4bc34d4b54364d5bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableUpstreamValidation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfig]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a082f76f9b86582156aaf335a4794349c334590ada0f5a25d5e0148b16fed8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository",
    jsii_struct_bases=[],
    name_mapping={
        "custom_repository": "customRepository",
        "public_repository": "publicRepository",
    },
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository:
    def __init__(
        self,
        *,
        custom_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#custom_repository GoogleArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "PYPI" Possible values: ["PYPI"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        if isinstance(custom_repository, dict):
            custom_repository = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository(**custom_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcedad75dd35d3e74b7b914ae965942796cb8fa6c7deb708aa85708a47c37177)
            check_type(argname="argument custom_repository", value=custom_repository, expected_type=type_hints["custom_repository"])
            check_type(argname="argument public_repository", value=public_repository, expected_type=type_hints["public_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_repository is not None:
            self._values["custom_repository"] = custom_repository
        if public_repository is not None:
            self._values["public_repository"] = public_repository

    @builtins.property
    def custom_repository(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository"]:
        '''custom_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#custom_repository GoogleArtifactRegistryRepository#custom_repository}
        '''
        result = self._values.get("custom_repository")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository"], result)

    @builtins.property
    def public_repository(self) -> typing.Optional[builtins.str]:
        '''Address of the remote repository. Default value: "PYPI" Possible values: ["PYPI"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: Specific uri to the registry, e.g. '"https://pypi.io"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#uri GoogleArtifactRegistryRepository#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7850726c63be6fa0d56184f4fba6aee275df4ecf011fd220b43598cb7f6bf98e)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''Specific uri to the registry, e.g. '"https://pypi.io"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#uri GoogleArtifactRegistryRepository#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a51b2f6a1fad5499f1f51f647c84bb92982d3baa72df410dfc927bcc4b897d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e300d8bdaabb160ebab60148e1168582df538df8381980c260e419cc2dc02ed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f4de2b5174c2ab255b93027c4dfe3709a91ea53f5c23588e86e53a3cea9876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__679eca298cb94d2743453452bb35fea34ee385f91713f8e96c7b4c16accdd0ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomRepository")
    def put_custom_repository(
        self,
        *,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Specific uri to the registry, e.g. '"https://pypi.io"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#uri GoogleArtifactRegistryRepository#uri}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository(
            uri=uri
        )

        return typing.cast(None, jsii.invoke(self, "putCustomRepository", [value]))

    @jsii.member(jsii_name="resetCustomRepository")
    def reset_custom_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRepository", []))

    @jsii.member(jsii_name="resetPublicRepository")
    def reset_public_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicRepository", []))

    @builtins.property
    @jsii.member(jsii_name="customRepository")
    def custom_repository(
        self,
    ) -> GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepositoryOutputReference:
        return typing.cast(GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepositoryOutputReference, jsii.get(self, "customRepository"))

    @builtins.property
    @jsii.member(jsii_name="customRepositoryInput")
    def custom_repository_input(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository], jsii.get(self, "customRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="publicRepositoryInput")
    def public_repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="publicRepository")
    def public_repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicRepository"))

    @public_repository.setter
    def public_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2609820a6e299fb709facee2c41f3500c071b31e61b1839a71dda0d9dbe6092c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicRepository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa9e73c0d1d6d6979517d73c4729a948f408b4e641903d432ba88b932f1457c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials",
    jsii_struct_bases=[],
    name_mapping={"username_password_credentials": "usernamePasswordCredentials"},
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials:
    def __init__(
        self,
        *,
        username_password_credentials: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param username_password_credentials: username_password_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#username_password_credentials GoogleArtifactRegistryRepository#username_password_credentials}
        '''
        if isinstance(username_password_credentials, dict):
            username_password_credentials = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials(**username_password_credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cabdc5083d83fd88fb499ebcd11ec35778d9cb63ccf0de03515961ce47622c66)
            check_type(argname="argument username_password_credentials", value=username_password_credentials, expected_type=type_hints["username_password_credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if username_password_credentials is not None:
            self._values["username_password_credentials"] = username_password_credentials

    @builtins.property
    def username_password_credentials(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials"]:
        '''username_password_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#username_password_credentials GoogleArtifactRegistryRepository#username_password_credentials}
        '''
        result = self._values.get("username_password_credentials")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c63157429e56ebab59b4cf7e04b3d685361bb079cf9d4b2ca4118626c949166d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putUsernamePasswordCredentials")
    def put_username_password_credentials(
        self,
        *,
        password_secret_version: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password_secret_version: The Secret Manager key version that holds the password to access the remote repository. Must be in the format of 'projects/{project}/secrets/{secret}/versions/{version}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#password_secret_version GoogleArtifactRegistryRepository#password_secret_version}
        :param username: The username to access the remote repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#username GoogleArtifactRegistryRepository#username}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials(
            password_secret_version=password_secret_version, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putUsernamePasswordCredentials", [value]))

    @jsii.member(jsii_name="resetUsernamePasswordCredentials")
    def reset_username_password_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernamePasswordCredentials", []))

    @builtins.property
    @jsii.member(jsii_name="usernamePasswordCredentials")
    def username_password_credentials(
        self,
    ) -> "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentialsOutputReference":
        return typing.cast("GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentialsOutputReference", jsii.get(self, "usernamePasswordCredentials"))

    @builtins.property
    @jsii.member(jsii_name="usernamePasswordCredentialsInput")
    def username_password_credentials_input(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials"]:
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials"], jsii.get(self, "usernamePasswordCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3d0819f5d55e59b398c33fb98217cb1e227824c1f31ba5be8af0c5df2985b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "password_secret_version": "passwordSecretVersion",
        "username": "username",
    },
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials:
    def __init__(
        self,
        *,
        password_secret_version: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password_secret_version: The Secret Manager key version that holds the password to access the remote repository. Must be in the format of 'projects/{project}/secrets/{secret}/versions/{version}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#password_secret_version GoogleArtifactRegistryRepository#password_secret_version}
        :param username: The username to access the remote repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#username GoogleArtifactRegistryRepository#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1fa0b5a018a1983f06ab08990abcbc2b6c3c1030fab226bf2b4c642ab58b3db)
            check_type(argname="argument password_secret_version", value=password_secret_version, expected_type=type_hints["password_secret_version"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if password_secret_version is not None:
            self._values["password_secret_version"] = password_secret_version
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def password_secret_version(self) -> typing.Optional[builtins.str]:
        '''The Secret Manager key version that holds the password to access the remote repository. Must be in the format of 'projects/{project}/secrets/{secret}/versions/{version}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#password_secret_version GoogleArtifactRegistryRepository#password_secret_version}
        '''
        result = self._values.get("password_secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username to access the remote repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#username GoogleArtifactRegistryRepository#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0401710962be88491f3d2f7879b82183ab583895b0eb3285c2443810a6ef8618)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPasswordSecretVersion")
    def reset_password_secret_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordSecretVersion", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="passwordSecretVersionInput")
    def password_secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordSecretVersion")
    def password_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordSecretVersion"))

    @password_secret_version.setter
    def password_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3ceda79b27f40765013383a811f44634d9e8d2bfbdf77d1ab6b8ff037aa601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bec1cfe0b3729082901e30d183c7c3cadf47a351c6e990ff1eeef233fce95b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c1044c773ef97cbb9bbaa396155a05dd69f838c1963ace631a19691ebb575b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository",
    jsii_struct_bases=[],
    name_mapping={"public_repository": "publicRepository"},
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository:
    def __init__(
        self,
        *,
        public_repository: typing.Optional[typing.Union["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param public_repository: public_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        if isinstance(public_repository, dict):
            public_repository = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository(**public_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b2b37a6726a5d1055f74e3455713111055a04a21e9b83735e762a284d4b4c1f)
            check_type(argname="argument public_repository", value=public_repository, expected_type=type_hints["public_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if public_repository is not None:
            self._values["public_repository"] = public_repository

    @builtins.property
    def public_repository(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository"]:
        '''public_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#public_repository GoogleArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa7aeaa8956ba86157628c4d6db592ffcfd546d7a36bff7f63518101612268d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPublicRepository")
    def put_public_repository(
        self,
        *,
        repository_base: builtins.str,
        repository_path: builtins.str,
    ) -> None:
        '''
        :param repository_base: A common public repository base for Yum. Possible values: ["CENTOS", "CENTOS_DEBUG", "CENTOS_VAULT", "CENTOS_STREAM", "ROCKY", "EPEL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository_base GoogleArtifactRegistryRepository#repository_base}
        :param repository_path: Specific repository from the base, e.g. '"pub/rocky/9/BaseOS/x86_64/os"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository_path GoogleArtifactRegistryRepository#repository_path}
        '''
        value = GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository(
            repository_base=repository_base, repository_path=repository_path
        )

        return typing.cast(None, jsii.invoke(self, "putPublicRepository", [value]))

    @jsii.member(jsii_name="resetPublicRepository")
    def reset_public_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicRepository", []))

    @builtins.property
    @jsii.member(jsii_name="publicRepository")
    def public_repository(
        self,
    ) -> "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepositoryOutputReference":
        return typing.cast("GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepositoryOutputReference", jsii.get(self, "publicRepository"))

    @builtins.property
    @jsii.member(jsii_name="publicRepositoryInput")
    def public_repository_input(
        self,
    ) -> typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository"]:
        return typing.cast(typing.Optional["GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository"], jsii.get(self, "publicRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34080e14e9f5ac20af04fd814c0edb9f1a91cc45211d9ce39aa969973f10e68f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository",
    jsii_struct_bases=[],
    name_mapping={
        "repository_base": "repositoryBase",
        "repository_path": "repositoryPath",
    },
)
class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository:
    def __init__(
        self,
        *,
        repository_base: builtins.str,
        repository_path: builtins.str,
    ) -> None:
        '''
        :param repository_base: A common public repository base for Yum. Possible values: ["CENTOS", "CENTOS_DEBUG", "CENTOS_VAULT", "CENTOS_STREAM", "ROCKY", "EPEL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository_base GoogleArtifactRegistryRepository#repository_base}
        :param repository_path: Specific repository from the base, e.g. '"pub/rocky/9/BaseOS/x86_64/os"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository_path GoogleArtifactRegistryRepository#repository_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65757f82129cde51169f63138c4c2af18f5d99a6214dda433a6c56063083e0bb)
            check_type(argname="argument repository_base", value=repository_base, expected_type=type_hints["repository_base"])
            check_type(argname="argument repository_path", value=repository_path, expected_type=type_hints["repository_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_base": repository_base,
            "repository_path": repository_path,
        }

    @builtins.property
    def repository_base(self) -> builtins.str:
        '''A common public repository base for Yum. Possible values: ["CENTOS", "CENTOS_DEBUG", "CENTOS_VAULT", "CENTOS_STREAM", "ROCKY", "EPEL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository_base GoogleArtifactRegistryRepository#repository_base}
        '''
        result = self._values.get("repository_base")
        assert result is not None, "Required property 'repository_base' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_path(self) -> builtins.str:
        '''Specific repository from the base, e.g. '"pub/rocky/9/BaseOS/x86_64/os"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository_path GoogleArtifactRegistryRepository#repository_path}
        '''
        result = self._values.get("repository_path")
        assert result is not None, "Required property 'repository_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__769948c2865b1d000688782e3a79b1afae529fe39baabd5157a5d7337e990411)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="repositoryBaseInput")
    def repository_base_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryBaseInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryPathInput")
    def repository_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryPathInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryBase")
    def repository_base(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryBase"))

    @repository_base.setter
    def repository_base(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dbeaad2875dbf2dce00e749a33e3c61250acba759a341ad4c7b6ea0b5cdd343)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryBase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryPath")
    def repository_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryPath"))

    @repository_path.setter
    def repository_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8fad320a7bf1120357aa8154bb5390fa0de06ba42871ed182a6b1eca35daacd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa81a6cba7b7b4d74b87516f7991aebb97eb570a9e504e0d9833dc686932efea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleArtifactRegistryRepositoryTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#create GoogleArtifactRegistryRepository#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#delete GoogleArtifactRegistryRepository#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#update GoogleArtifactRegistryRepository#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a87291b666e4d5e7af926365b36a8b7d1dfc8e95b71a557f90667e16421eb3e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#create GoogleArtifactRegistryRepository#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#delete GoogleArtifactRegistryRepository#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#update GoogleArtifactRegistryRepository#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f9e60276f250dee72221e798b3a1b240878877ff9c27f907b9b597f015dada1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0aa0860854dc79f4343a966d7f5de3a49053660ceda9374eb8992aecfd3e4bf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b5ab646bffdd4ec7073552b8f5393a01749492441a3641fe7e52e15ac10132)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adece7ca2fe14e03b7b625d88e202a376ba1ae5990e2616c20fa077e8ac04b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleArtifactRegistryRepositoryTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleArtifactRegistryRepositoryTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleArtifactRegistryRepositoryTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a02c475f86c7c41e49eca96b1298ce6d21b640896b93c2aa2f8d083f4bfb52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryVirtualRepositoryConfig",
    jsii_struct_bases=[],
    name_mapping={"upstream_policies": "upstreamPolicies"},
)
class GoogleArtifactRegistryRepositoryVirtualRepositoryConfig:
    def __init__(
        self,
        *,
        upstream_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param upstream_policies: upstream_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#upstream_policies GoogleArtifactRegistryRepository#upstream_policies}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7412e9b1a0ff648494d7a4c082c89fc7466c9b14504d0e412ef8908402210284)
            check_type(argname="argument upstream_policies", value=upstream_policies, expected_type=type_hints["upstream_policies"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if upstream_policies is not None:
            self._values["upstream_policies"] = upstream_policies

    @builtins.property
    def upstream_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies"]]]:
        '''upstream_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#upstream_policies GoogleArtifactRegistryRepository#upstream_policies}
        '''
        result = self._values.get("upstream_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryVirtualRepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryVirtualRepositoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryVirtualRepositoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6839fd5d86d895f50a70cd13ee94ede11b78387e4c88b60190c892573a68625d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putUpstreamPolicies")
    def put_upstream_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c4a34f8cfba67be353027ee0ebe29b5ad1737cf0c6ea9093c96d94599a58dda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUpstreamPolicies", [value]))

    @jsii.member(jsii_name="resetUpstreamPolicies")
    def reset_upstream_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpstreamPolicies", []))

    @builtins.property
    @jsii.member(jsii_name="upstreamPolicies")
    def upstream_policies(
        self,
    ) -> "GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesList":
        return typing.cast("GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesList", jsii.get(self, "upstreamPolicies"))

    @builtins.property
    @jsii.member(jsii_name="upstreamPoliciesInput")
    def upstream_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies"]]], jsii.get(self, "upstreamPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryVirtualRepositoryConfig]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryVirtualRepositoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryVirtualRepositoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2a7fca719d728d30c290c916bbb6da0917d128ea63b4071843c9aaf76519c5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "priority": "priority", "repository": "repository"},
)
class GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The user-provided ID of the upstream policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#id GoogleArtifactRegistryRepository#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param priority: Entries with a greater priority value take precedence in the pull order. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#priority GoogleArtifactRegistryRepository#priority}
        :param repository: A reference to the repository resource, for example: "projects/p1/locations/us-central1/repository/repo1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository GoogleArtifactRegistryRepository#repository}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed8b0c183eb7336d234999f54eb5166c437a9c201e0e0acdccca0d04b09ab542)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if priority is not None:
            self._values["priority"] = priority
        if repository is not None:
            self._values["repository"] = repository

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''The user-provided ID of the upstream policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#id GoogleArtifactRegistryRepository#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Entries with a greater priority value take precedence in the pull order.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#priority GoogleArtifactRegistryRepository#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''A reference to the repository resource, for example: "projects/p1/locations/us-central1/repository/repo1".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#repository GoogleArtifactRegistryRepository#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64d9db7fad960feabf307fcff51ab73cd564ead3c1a01187f90707e1fb275493)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775e377a799fe0324be9efb13bf88edbeac0b9c5819a30b3db7aca9b41a26166)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db41e9509d65dcfa9905552fcccbd8a5e0d34b6870d59627166c1c9e1fe54c0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64b3cc3426cf2f2789fb720ade71725d470d4e99ee89a0bb259df8201cee0730)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbef3d9e60f2b124d860a8d641cacc690a5eb9056ea8262a1e2a41a3cded4400)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be00d25c3d0a71bdd3db4bc7876e4a58df4e2db640a7e6d20fdac654f816a6c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a44f8cbd508ad15d3e907ec55902d9ea95acaf1de5f5ef10a4cf0828b7aedb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetRepository")
    def reset_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepository", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07479d6c97e79c08475a12929020494b5f446814fa39ecbfb3f67f110c572b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868ca268dde619b18cc1cd5a3a4a2826dce37a05198fa3ec545aa9d86c4f7376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4375bac19d6c97b6a487a463d787012b076278c4020bb8b147c66c33975e31df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffbbe263087a0149562f8947819dd59242d3e41361bfad35f633bbdd8238eae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig",
    jsii_struct_bases=[],
    name_mapping={"enablement_config": "enablementConfig"},
)
class GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig:
    def __init__(
        self,
        *,
        enablement_config: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enablement_config: This configures whether vulnerability scanning is automatically performed for artifacts pushed to this repository. Possible values: ["INHERITED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#enablement_config GoogleArtifactRegistryRepository#enablement_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62f1e94c664fef0c336adfeb6f8eee06febc39d35977d59fe99fa11b7c4b2ef)
            check_type(argname="argument enablement_config", value=enablement_config, expected_type=type_hints["enablement_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enablement_config is not None:
            self._values["enablement_config"] = enablement_config

    @builtins.property
    def enablement_config(self) -> typing.Optional[builtins.str]:
        '''This configures whether vulnerability scanning is automatically performed for artifacts pushed to this repository. Possible values: ["INHERITED", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_artifact_registry_repository#enablement_config GoogleArtifactRegistryRepository#enablement_config}
        '''
        result = self._values.get("enablement_config")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleArtifactRegistryRepositoryVulnerabilityScanningConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleArtifactRegistryRepository.GoogleArtifactRegistryRepositoryVulnerabilityScanningConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64958e48a9ac63634228fcde49b77128fab81bd270b330c608d1d7cca861af68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnablementConfig")
    def reset_enablement_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablementConfig", []))

    @builtins.property
    @jsii.member(jsii_name="enablementState")
    def enablement_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enablementState"))

    @builtins.property
    @jsii.member(jsii_name="enablementStateReason")
    def enablement_state_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enablementStateReason"))

    @builtins.property
    @jsii.member(jsii_name="enablementConfigInput")
    def enablement_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enablementConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enablementConfig")
    def enablement_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enablementConfig"))

    @enablement_config.setter
    def enablement_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa54a6157f81a1ea6e94414d11eda0647a2009eb5f12aeff889f3a4a73826f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablementConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig]:
        return typing.cast(typing.Optional[GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6fe89614690a8185348d7aebf7a3a25a47743a658728e4882ef72abfc352c35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleArtifactRegistryRepository",
    "GoogleArtifactRegistryRepositoryCleanupPolicies",
    "GoogleArtifactRegistryRepositoryCleanupPoliciesCondition",
    "GoogleArtifactRegistryRepositoryCleanupPoliciesConditionOutputReference",
    "GoogleArtifactRegistryRepositoryCleanupPoliciesList",
    "GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions",
    "GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersionsOutputReference",
    "GoogleArtifactRegistryRepositoryCleanupPoliciesOutputReference",
    "GoogleArtifactRegistryRepositoryConfig",
    "GoogleArtifactRegistryRepositoryDockerConfig",
    "GoogleArtifactRegistryRepositoryDockerConfigOutputReference",
    "GoogleArtifactRegistryRepositoryMavenConfig",
    "GoogleArtifactRegistryRepositoryMavenConfigOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfig",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepositoryOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepositoryOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepositoryOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepositoryOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepositoryOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepositoryOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentialsOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryOutputReference",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository",
    "GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepositoryOutputReference",
    "GoogleArtifactRegistryRepositoryTimeouts",
    "GoogleArtifactRegistryRepositoryTimeoutsOutputReference",
    "GoogleArtifactRegistryRepositoryVirtualRepositoryConfig",
    "GoogleArtifactRegistryRepositoryVirtualRepositoryConfigOutputReference",
    "GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies",
    "GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesList",
    "GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesOutputReference",
    "GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig",
    "GoogleArtifactRegistryRepositoryVulnerabilityScanningConfigOutputReference",
]

publication.publish()

def _typecheckingstub__67a11e2122d6664017242aeafd4c93d9fa52129b0712698eca09688c82b13de3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    format: builtins.str,
    repository_id: builtins.str,
    cleanup_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleArtifactRegistryRepositoryCleanupPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cleanup_policy_dry_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    docker_config: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryDockerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    maven_config: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryMavenConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remote_repository_config: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_repository_config: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryVirtualRepositoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    vulnerability_scanning_config: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__64a8d60b8f3b73707c536456d31fff9819f8372604d97892d8efc3b60649c84d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05cfbff3cbeda33d36e9e501915cc61276b852e146b7cc1fface6d12f658a10(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleArtifactRegistryRepositoryCleanupPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c6c97b7c0d307c6e3d68f07b761e6c3e505524e37996248beaf25659d6a565(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a884f9ba44c40a4418e193fc168692418b837dc57d71f179490ba11b5fa40d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1acfe2b5cf2b91d73928a9e731c2cfd069bbac29dcbc52da978ca527d69737d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b587ab17be38890794c093824080b4e454003e1198e375724cdfc3178057854(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec0ed70e3829cbc8930c8fbc32c7fbbafecab184eda9d737a892486619fadcad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535062de7b2c2b2db5c98c29f5e9ac5025367fbe810e81c83ad59ef15835eaa9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87602acbfc2bd41a8fb9eff6b22fb5c6b2ab9113e61fcbc5705497bd380eb496(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2ba84f604e1ab673edb088edec27614d9b6b6e5aef7daa40830753dbb93af3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a0e374397384da479f77b5ea8afb599619865d041cba21a07f3b4eec030e5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755a1bd588113c26c00d7dd30beaceb0cb1af32b57a2fc7059cfce92eb73a939(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570054b414acb7cf97eea863acdbf6ab3a59c8eafa5896fe984091478e1c7b82(
    *,
    id: builtins.str,
    action: typing.Optional[builtins.str] = None,
    condition: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryCleanupPoliciesCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    most_recent_versions: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2084459b9314767a18ef25c7569e01b1db52b810852e0cf8f76f555d3b84b0ea(
    *,
    newer_than: typing.Optional[builtins.str] = None,
    older_than: typing.Optional[builtins.str] = None,
    package_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_state: typing.Optional[builtins.str] = None,
    version_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a735369f344b6db5fcde1f4aaeb92248dc49581a24d12b63a6c31b3dce1b90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e20fee31910a72480c1a8a2efc6fe0d9d52148649332cc1fe91334323f74b6e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30430a1f32062224cf341daf4b13ac6b31e47f69744aaae578a58a1b42f8bdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63bb591cca4719305e746582ef32b4353dced2dc74fe7d751f4411af2f98017c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27733cc7dab0ee759bd0d7da921b56d6302235667557e06a7636f4e461dff33a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb23ccf4400f12e1f6bb4d678caed96ead574d68bb5883232d5316cf877b9037(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b867dde34fe1cd145509c7671e05b0944328ed62ff80edb559a10ce958e2d56(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5186fc3329ef1792585a8e14b81d3363930e7c66da1e95abe7a257cbab89618(
    value: typing.Optional[GoogleArtifactRegistryRepositoryCleanupPoliciesCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eabb9538cf0e6511463748414787940e187d633e1618a3cf5ed528cde8501a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec564ec162ea3e6bfadea4eb2f6a876be56e9b0e218eb07b55b03e1973b2e811(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0fd45c62ca52a46ace6fcce6881e8508125d92117f21aaa4053119d337f1c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740de9454f56cd0a286a6927df070053abb1556929e97b472e0910f627c7ec42(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de2f6a1663aee1f4b59d553bc58c2d2b67ac82b59ea5dbfb5135c1686c84012(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45e82609247b72d2a95db6cc9cf96cfe3a404b637fed575573be37a5152e319(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleArtifactRegistryRepositoryCleanupPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b7657fe489f32895823c6607261ddf44c9fcb882d93a5bc66ad5bc4c38d11d9(
    *,
    keep_count: typing.Optional[jsii.Number] = None,
    package_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f56a5c387d738fa5fe93825dc1d55011b06630e51c12a62e97fb1ec6e24671(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979d4d92e4a9fd9a1dfaf94872de3d2c4aa17295c0f6d8dc2717f4d090413646(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d4c59dcfaf56c0e6baa34acbfaddd23e5b07f3b2e5de3d99d2a9133ed46b09d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__778729bd15de3b611803cd125db1e741ad4951393e2cd556530a80ee734593ca(
    value: typing.Optional[GoogleArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df0b89de0c3967d93c5381fb63cefceebe18a36fd7c2a48ac92414f512a0045(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c404ce79fe8385e853a3b14503da784bb5d10c7ac76e317e006a38b3dce4e474(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2826c0147ff409b32e5cc3be251b00fdf03d065984e997ae7bd95883bfd3000(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff66c7fe941a77245f624c161d105400348d42b2baa6b7d20aae314d4387a12f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleArtifactRegistryRepositoryCleanupPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5088d0d29bb6061ed8033079146f76ffd8db624253986f4fa50416e123b6414(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    format: builtins.str,
    repository_id: builtins.str,
    cleanup_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleArtifactRegistryRepositoryCleanupPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cleanup_policy_dry_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    docker_config: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryDockerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    maven_config: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryMavenConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remote_repository_config: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_repository_config: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryVirtualRepositoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    vulnerability_scanning_config: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f5546da03f0a36d2ba2086fd28a4f0bedd4adcb91d34687fd23ec31d9340c6(
    *,
    immutable_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebae7feb9192fe8276f41f9914268b82fa1ad588fb88562d165287aaa8c24fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4b4341d3cbb36cdaba4fd0cc3b01937bbe2e5f10051bdcbffbe09f4ec7b57d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278ef6879dfe25305d05e7f7de36e073f7669109bf4f13ece6d479c470068aa2(
    value: typing.Optional[GoogleArtifactRegistryRepositoryDockerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86106113cd2326dfa091d75b12f264666750a8e018f6f9dd440d5671916a28f(
    *,
    allow_snapshot_overwrites: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    version_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf716c7ee8f7e3708ae13c4a5ed91553e2752a5a2dc59bcabdb0955a5350231(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b444a1b5f285427c2eab3b45eaf064e7331ea489897b86ae9d7be87d33b10a5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b51472012f31563968da9a4298b224009dce64b3e481bb595e29aaed363681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ec6ac288c11e20f2f29ea7e5ac0c01034509432a7fd1eb1d38a1c98a11c6cf(
    value: typing.Optional[GoogleArtifactRegistryRepositoryMavenConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3124b5f04fe207fe7b9f7e70d5948dd0cc5b9ac58ea072a6c9b8ad38fa12ec7(
    *,
    apt_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    common_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_upstream_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    docker_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    maven_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    npm_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    python_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    upstream_credentials: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    yum_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2c980bd897a66a6e1ba0fac71475d96f8469e5c0d76a98a194221c8052eba97(
    *,
    public_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70ff9c6559d97f914267bf813857c593d27eff5b4416cc9e098dc28dca3afde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0de235d7c38f16a6d8840cf942f4adb666f9bfe4bb13679d69f739308b014b(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18b06196991ef20227e05d2ccd0d64da3ee90e55552f2bf52995cc0c0bdca10(
    *,
    repository_base: builtins.str,
    repository_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90028c5a9815c992b3c66f7f896bc6e1c0d7164b58efa49d58c256183b48b701(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c95103958c34778e85f7ce67a1995e0225793ccdf16e0f29c10b18a9c70e1928(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc426db723ea553c6feb1042b1d207c8d0450467beaf88f8df43db09c5345b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e964e0fd8aa6114f86cdff78bcf797a3e49cb30dd73cce576f520eaefb899d(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5416e6d3d30e6e9d116c2e47af1ca0719c0836babd651bd3a98ae0516c3bc699(
    *,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb82924f44558836601a6ac5954d978f27f002f4f86c5dc91d2bf5b92448edb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e94a3f0d497c546eecb47d8abb65bcc9b94d2a4b11601ffb58ab8e2abf2ccfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d4abe5ba28794b8828ea604b749a848b6406080339f9a8c38c7a30a84867ed(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe2c5a77bb1705dcdf629eeb965b6991604a2b6f152a4c0c81a4ac531d86c63(
    *,
    custom_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    public_repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c654deba80c25bb018f35a53e6c1fd60e5812a729d693551393fa3c8caf083(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f557312eb6e63788a82c884fe33e09451a7ff3408233a3a0fcc720f1e10302a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9af5b607030e29fe521332eaa8fd1b65379275da0329c1475dc4ac8411d953e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5165ceda46a0cdd88f4049153adf4c460ab80d477dd3e876fcf1ebfca2b16f24(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__040cbeb20e8cafcadf2397a94e2cd6b4428dcc5af0ba3f7eb8d0c27b1078e8d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d2feabb5f4c368b27b272540662a1a9503442d86b2461a00d56e4ec2c9d8a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6583a2160ab7438cb3c884ba152391468a61b2e6724b19345ee684f8c205cea9(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173b40bd336c8fb892b551bfee1c08ea8e99b0d47cea7fa9c4c0f1a9ee0b07a3(
    *,
    custom_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    public_repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b6cee98bfe8df617df15db462157405f642b3d1ea77af7c70d757126db1fe0(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f83aeae67e6a0f51950f674c579a08ec39a53292b0437ba983d4747d2bcd468(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0d8a260e01be207144075e74576f22d8b02f882ec756d9032a21938baaf34e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c13d2bc7239c93d59be7447ea9ba85d6c8a2e82fce56934727901a8dbe1cfc8(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d46c3562237d2564056f8672c0d6b01221c22fd9ca4cda640c2e486943f111(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f760049bd8b335982e2099781703d0498c3d08e1dc5d08ac5a9415b0c72ee3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054fb94a56443fc8592c59b979b942bae9fb051f0c0bc09ce2fc26aedb68969a(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16c15d1e8c7e326bece8c32c34f84fadf77ae1818e4134d6e2e230f9f6f96a3(
    *,
    custom_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    public_repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2abae1225bf51aaf0e05bf6cdc01afa1108441e15d436f28cb6aba82f532fa(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d81367179bb45d7a79e8ca227219996cdfc5b95cbf9f43e4eaaf6031fc2de5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c029cd57965ce34bc7cde06db7b856360ec3e8f4c894d9be1e596f53ea936a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b466d8bff5ca1a2bcdf767a63fd95eaf433f0a93fceb0a4d8b058edbcdd2d4ad(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1f724e4e99864d72be51c8b3f7c82578696934893ddf257b6b71773d0cf95c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0f119341719bd3ab10524a043e74d6e1dd5d244588b0b3436d2febc13252e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36862856d4d641184221e86d78090b9211efb3dfa061e1469d9a97fd8fe2ca80(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9316ff569fd0ec931a3c0c169b1d986bd6bca28e03205e7f1af06ab55df0002(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb3ac6e429dd4a3f62e133f393354fd6cb3a2e16178dce77ebeeb71df894d9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d9145d71e5ce9f06b81f73e417c51d7d74078aa203c1de4bc34d4b54364d5bc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a082f76f9b86582156aaf335a4794349c334590ada0f5a25d5e0148b16fed8e(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcedad75dd35d3e74b7b914ae965942796cb8fa6c7deb708aa85708a47c37177(
    *,
    custom_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    public_repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7850726c63be6fa0d56184f4fba6aee275df4ecf011fd220b43598cb7f6bf98e(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a51b2f6a1fad5499f1f51f647c84bb92982d3baa72df410dfc927bcc4b897d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e300d8bdaabb160ebab60148e1168582df538df8381980c260e419cc2dc02ed7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f4de2b5174c2ab255b93027c4dfe3709a91ea53f5c23588e86e53a3cea9876(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679eca298cb94d2743453452bb35fea34ee385f91713f8e96c7b4c16accdd0ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2609820a6e299fb709facee2c41f3500c071b31e61b1839a71dda0d9dbe6092c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa9e73c0d1d6d6979517d73c4729a948f408b4e641903d432ba88b932f1457c(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cabdc5083d83fd88fb499ebcd11ec35778d9cb63ccf0de03515961ce47622c66(
    *,
    username_password_credentials: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c63157429e56ebab59b4cf7e04b3d685361bb079cf9d4b2ca4118626c949166d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3d0819f5d55e59b398c33fb98217cb1e227824c1f31ba5be8af0c5df2985b5(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1fa0b5a018a1983f06ab08990abcbc2b6c3c1030fab226bf2b4c642ab58b3db(
    *,
    password_secret_version: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0401710962be88491f3d2f7879b82183ab583895b0eb3285c2443810a6ef8618(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3ceda79b27f40765013383a811f44634d9e8d2bfbdf77d1ab6b8ff037aa601(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bec1cfe0b3729082901e30d183c7c3cadf47a351c6e990ff1eeef233fce95b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c1044c773ef97cbb9bbaa396155a05dd69f838c1963ace631a19691ebb575b(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b2b37a6726a5d1055f74e3455713111055a04a21e9b83735e762a284d4b4c1f(
    *,
    public_repository: typing.Optional[typing.Union[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7aeaa8956ba86157628c4d6db592ffcfd546d7a36bff7f63518101612268d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34080e14e9f5ac20af04fd814c0edb9f1a91cc45211d9ce39aa969973f10e68f(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65757f82129cde51169f63138c4c2af18f5d99a6214dda433a6c56063083e0bb(
    *,
    repository_base: builtins.str,
    repository_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769948c2865b1d000688782e3a79b1afae529fe39baabd5157a5d7337e990411(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dbeaad2875dbf2dce00e749a33e3c61250acba759a341ad4c7b6ea0b5cdd343(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8fad320a7bf1120357aa8154bb5390fa0de06ba42871ed182a6b1eca35daacd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa81a6cba7b7b4d74b87516f7991aebb97eb570a9e504e0d9833dc686932efea(
    value: typing.Optional[GoogleArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a87291b666e4d5e7af926365b36a8b7d1dfc8e95b71a557f90667e16421eb3e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9e60276f250dee72221e798b3a1b240878877ff9c27f907b9b597f015dada1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa0860854dc79f4343a966d7f5de3a49053660ceda9374eb8992aecfd3e4bf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b5ab646bffdd4ec7073552b8f5393a01749492441a3641fe7e52e15ac10132(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adece7ca2fe14e03b7b625d88e202a376ba1ae5990e2616c20fa077e8ac04b33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a02c475f86c7c41e49eca96b1298ce6d21b640896b93c2aa2f8d083f4bfb52(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleArtifactRegistryRepositoryTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7412e9b1a0ff648494d7a4c082c89fc7466c9b14504d0e412ef8908402210284(
    *,
    upstream_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6839fd5d86d895f50a70cd13ee94ede11b78387e4c88b60190c892573a68625d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4a34f8cfba67be353027ee0ebe29b5ad1737cf0c6ea9093c96d94599a58dda(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a7fca719d728d30c290c916bbb6da0917d128ea63b4071843c9aaf76519c5d(
    value: typing.Optional[GoogleArtifactRegistryRepositoryVirtualRepositoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8b0c183eb7336d234999f54eb5166c437a9c201e0e0acdccca0d04b09ab542(
    *,
    id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d9db7fad960feabf307fcff51ab73cd564ead3c1a01187f90707e1fb275493(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775e377a799fe0324be9efb13bf88edbeac0b9c5819a30b3db7aca9b41a26166(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db41e9509d65dcfa9905552fcccbd8a5e0d34b6870d59627166c1c9e1fe54c0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b3cc3426cf2f2789fb720ade71725d470d4e99ee89a0bb259df8201cee0730(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbef3d9e60f2b124d860a8d641cacc690a5eb9056ea8262a1e2a41a3cded4400(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be00d25c3d0a71bdd3db4bc7876e4a58df4e2db640a7e6d20fdac654f816a6c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a44f8cbd508ad15d3e907ec55902d9ea95acaf1de5f5ef10a4cf0828b7aedb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07479d6c97e79c08475a12929020494b5f446814fa39ecbfb3f67f110c572b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868ca268dde619b18cc1cd5a3a4a2826dce37a05198fa3ec545aa9d86c4f7376(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4375bac19d6c97b6a487a463d787012b076278c4020bb8b147c66c33975e31df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffbbe263087a0149562f8947819dd59242d3e41361bfad35f633bbdd8238eae8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62f1e94c664fef0c336adfeb6f8eee06febc39d35977d59fe99fa11b7c4b2ef(
    *,
    enablement_config: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64958e48a9ac63634228fcde49b77128fab81bd270b330c608d1d7cca861af68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa54a6157f81a1ea6e94414d11eda0647a2009eb5f12aeff889f3a4a73826f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6fe89614690a8185348d7aebf7a3a25a47743a658728e4882ef72abfc352c35(
    value: typing.Optional[GoogleArtifactRegistryRepositoryVulnerabilityScanningConfig],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `google_artifact_registry_repository`

Refer to the Terraform Registry for docs: [`google_artifact_registry_repository`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository).
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


class ArtifactRegistryRepository(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepository",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository google_artifact_registry_repository}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        format: builtins.str,
        repository_id: builtins.str,
        cleanup_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ArtifactRegistryRepositoryCleanupPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cleanup_policy_dry_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        docker_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryDockerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        maven_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryMavenConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remote_repository_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ArtifactRegistryRepositoryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_repository_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryVirtualRepositoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vulnerability_scanning_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryVulnerabilityScanningConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository google_artifact_registry_repository} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param format: The format of packages that are stored in the repository. Supported formats can be found `here <https://cloud.google.com/artifact-registry/docs/supported-formats>`_. You can only create alpha formats if you are a member of the `alpha user group <https://cloud.google.com/artifact-registry/docs/supported-formats#alpha-access>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#format ArtifactRegistryRepository#format}
        :param repository_id: The last part of the repository name, for example: "repo1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository_id ArtifactRegistryRepository#repository_id}
        :param cleanup_policies: cleanup_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#cleanup_policies ArtifactRegistryRepository#cleanup_policies}
        :param cleanup_policy_dry_run: If true, the cleanup pipeline is prevented from deleting versions in this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#cleanup_policy_dry_run ArtifactRegistryRepository#cleanup_policy_dry_run}
        :param description: The user-provided description of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#description ArtifactRegistryRepository#description}
        :param docker_config: docker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#docker_config ArtifactRegistryRepository#docker_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#id ArtifactRegistryRepository#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: The Cloud KMS resource name of the customer managed encryption key that’s used to encrypt the contents of the Repository. Has the form: 'projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key'. This value may not be changed after the Repository has been created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#kms_key_name ArtifactRegistryRepository#kms_key_name}
        :param labels: Labels with user-defined metadata. This field may contain up to 64 entries. Label keys and values may be no longer than 63 characters. Label keys must begin with a lowercase letter and may only contain lowercase letters, numeric characters, underscores, and dashes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#labels ArtifactRegistryRepository#labels}
        :param location: The name of the repository's location. In addition to specific regions, special values for multi-region locations are 'asia', 'europe', and 'us'. See `here <https://cloud.google.com/artifact-registry/docs/repositories/repo-locations>`_, or use the `google_artifact_registry_locations <https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/artifact_registry_locations>`_ data source for possible values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#location ArtifactRegistryRepository#location}
        :param maven_config: maven_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#maven_config ArtifactRegistryRepository#maven_config}
        :param mode: The mode configures the repository to serve artifacts from different sources. Default value: "STANDARD_REPOSITORY" Possible values: ["STANDARD_REPOSITORY", "VIRTUAL_REPOSITORY", "REMOTE_REPOSITORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#mode ArtifactRegistryRepository#mode}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#project ArtifactRegistryRepository#project}.
        :param remote_repository_config: remote_repository_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#remote_repository_config ArtifactRegistryRepository#remote_repository_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#timeouts ArtifactRegistryRepository#timeouts}
        :param virtual_repository_config: virtual_repository_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#virtual_repository_config ArtifactRegistryRepository#virtual_repository_config}
        :param vulnerability_scanning_config: vulnerability_scanning_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#vulnerability_scanning_config ArtifactRegistryRepository#vulnerability_scanning_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bcd8979225c9247b853165d6a61a0418712e3dd7ba1d971f4a680f60b10baaf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ArtifactRegistryRepositoryConfig(
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
        '''Generates CDKTF code for importing a ArtifactRegistryRepository resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ArtifactRegistryRepository to import.
        :param import_from_id: The id of the existing ArtifactRegistryRepository that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ArtifactRegistryRepository to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33aad0a68069b65e2c34d279460b4995b6b389a08707d749699514809769f508)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCleanupPolicies")
    def put_cleanup_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ArtifactRegistryRepositoryCleanupPolicies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69ea72533f282686af801e988c50fc6c7af35bbc78fa36f7c4c4315bc6d2f735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCleanupPolicies", [value]))

    @jsii.member(jsii_name="putDockerConfig")
    def put_docker_config(
        self,
        *,
        immutable_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param immutable_tags: The repository which enabled this flag prevents all tags from being modified, moved or deleted. This does not prevent tags from being created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#immutable_tags ArtifactRegistryRepository#immutable_tags}
        '''
        value = ArtifactRegistryRepositoryDockerConfig(immutable_tags=immutable_tags)

        return typing.cast(None, jsii.invoke(self, "putDockerConfig", [value]))

    @jsii.member(jsii_name="putMavenConfig")
    def put_maven_config(
        self,
        *,
        allow_snapshot_overwrites: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        version_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_snapshot_overwrites: The repository with this flag will allow publishing the same snapshot versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#allow_snapshot_overwrites ArtifactRegistryRepository#allow_snapshot_overwrites}
        :param version_policy: Version policy defines the versions that the registry will accept. Default value: "VERSION_POLICY_UNSPECIFIED" Possible values: ["VERSION_POLICY_UNSPECIFIED", "RELEASE", "SNAPSHOT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#version_policy ArtifactRegistryRepository#version_policy}
        '''
        value = ArtifactRegistryRepositoryMavenConfig(
            allow_snapshot_overwrites=allow_snapshot_overwrites,
            version_policy=version_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putMavenConfig", [value]))

    @jsii.member(jsii_name="putRemoteRepositoryConfig")
    def put_remote_repository_config(
        self,
        *,
        apt_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        common_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_upstream_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        docker_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        maven_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        npm_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        python_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        upstream_credentials: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        yum_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt_repository: apt_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#apt_repository ArtifactRegistryRepository#apt_repository}
        :param common_repository: common_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#common_repository ArtifactRegistryRepository#common_repository}
        :param description: The description of the remote source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#description ArtifactRegistryRepository#description}
        :param disable_upstream_validation: If true, the remote repository upstream and upstream credentials will not be validated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#disable_upstream_validation ArtifactRegistryRepository#disable_upstream_validation}
        :param docker_repository: docker_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#docker_repository ArtifactRegistryRepository#docker_repository}
        :param maven_repository: maven_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#maven_repository ArtifactRegistryRepository#maven_repository}
        :param npm_repository: npm_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#npm_repository ArtifactRegistryRepository#npm_repository}
        :param python_repository: python_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#python_repository ArtifactRegistryRepository#python_repository}
        :param upstream_credentials: upstream_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#upstream_credentials ArtifactRegistryRepository#upstream_credentials}
        :param yum_repository: yum_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#yum_repository ArtifactRegistryRepository#yum_repository}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#create ArtifactRegistryRepository#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#delete ArtifactRegistryRepository#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#update ArtifactRegistryRepository#update}.
        '''
        value = ArtifactRegistryRepositoryTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVirtualRepositoryConfig")
    def put_virtual_repository_config(
        self,
        *,
        upstream_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param upstream_policies: upstream_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#upstream_policies ArtifactRegistryRepository#upstream_policies}
        '''
        value = ArtifactRegistryRepositoryVirtualRepositoryConfig(
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
        :param enablement_config: This configures whether vulnerability scanning is automatically performed for artifacts pushed to this repository. Possible values: ["INHERITED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#enablement_config ArtifactRegistryRepository#enablement_config}
        '''
        value = ArtifactRegistryRepositoryVulnerabilityScanningConfig(
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
    def cleanup_policies(self) -> "ArtifactRegistryRepositoryCleanupPoliciesList":
        return typing.cast("ArtifactRegistryRepositoryCleanupPoliciesList", jsii.get(self, "cleanupPolicies"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="dockerConfig")
    def docker_config(self) -> "ArtifactRegistryRepositoryDockerConfigOutputReference":
        return typing.cast("ArtifactRegistryRepositoryDockerConfigOutputReference", jsii.get(self, "dockerConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="mavenConfig")
    def maven_config(self) -> "ArtifactRegistryRepositoryMavenConfigOutputReference":
        return typing.cast("ArtifactRegistryRepositoryMavenConfigOutputReference", jsii.get(self, "mavenConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="remoteRepositoryConfig")
    def remote_repository_config(
        self,
    ) -> "ArtifactRegistryRepositoryRemoteRepositoryConfigOutputReference":
        return typing.cast("ArtifactRegistryRepositoryRemoteRepositoryConfigOutputReference", jsii.get(self, "remoteRepositoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ArtifactRegistryRepositoryTimeoutsOutputReference":
        return typing.cast("ArtifactRegistryRepositoryTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="virtualRepositoryConfig")
    def virtual_repository_config(
        self,
    ) -> "ArtifactRegistryRepositoryVirtualRepositoryConfigOutputReference":
        return typing.cast("ArtifactRegistryRepositoryVirtualRepositoryConfigOutputReference", jsii.get(self, "virtualRepositoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="vulnerabilityScanningConfig")
    def vulnerability_scanning_config(
        self,
    ) -> "ArtifactRegistryRepositoryVulnerabilityScanningConfigOutputReference":
        return typing.cast("ArtifactRegistryRepositoryVulnerabilityScanningConfigOutputReference", jsii.get(self, "vulnerabilityScanningConfig"))

    @builtins.property
    @jsii.member(jsii_name="cleanupPoliciesInput")
    def cleanup_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ArtifactRegistryRepositoryCleanupPolicies"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ArtifactRegistryRepositoryCleanupPolicies"]]], jsii.get(self, "cleanupPoliciesInput"))

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
    ) -> typing.Optional["ArtifactRegistryRepositoryDockerConfig"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryDockerConfig"], jsii.get(self, "dockerConfigInput"))

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
    ) -> typing.Optional["ArtifactRegistryRepositoryMavenConfig"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryMavenConfig"], jsii.get(self, "mavenConfigInput"))

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
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfig"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfig"], jsii.get(self, "remoteRepositoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryIdInput")
    def repository_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ArtifactRegistryRepositoryTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ArtifactRegistryRepositoryTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualRepositoryConfigInput")
    def virtual_repository_config_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryVirtualRepositoryConfig"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryVirtualRepositoryConfig"], jsii.get(self, "virtualRepositoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="vulnerabilityScanningConfigInput")
    def vulnerability_scanning_config_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryVulnerabilityScanningConfig"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryVulnerabilityScanningConfig"], jsii.get(self, "vulnerabilityScanningConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2ca0ab3a8fae4060ebaec2d4aa5347a729a85e2c1c9c13355d42075fd63073f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cleanupPolicyDryRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2165c18d7acb1a9627989cb5defe6b690405516e3f1d4547298a0905c9cba6ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb192c76d83ad27ed556a5fdb2c8834cef53c7d066348fc3138e98c0da765f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567479c5ca63288cb191b7917c2c8c7b1a7f65455a55aa2d836fc08bfe19347f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d27069919d7606a89c8c364f9b9c838bb781ac21dae4c0b0fff13fe3cb27a446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1efd52613e06a5587e0511c8d71a516d56312b5f65a9444853959e0e66909b1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97953148b3c876edd5e36efdcd6a37041ea048618cfa6633e207c3a2f08b5a90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e187ab5b4160e21cd06788db103967f2abe29800b19b393fa21d07c4ef5c68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5317b275f0dad4386cf514228fffbf224db11181ffc92b16a4e3fd8df2e98316)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryId")
    def repository_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryId"))

    @repository_id.setter
    def repository_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11e57d193991945e90c037b5c5b4e93d52dda2b58aa6c02b4eb1e82e6b7942b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryCleanupPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "action": "action",
        "condition": "condition",
        "most_recent_versions": "mostRecentVersions",
    },
)
class ArtifactRegistryRepositoryCleanupPolicies:
    def __init__(
        self,
        *,
        id: builtins.str,
        action: typing.Optional[builtins.str] = None,
        condition: typing.Optional[typing.Union["ArtifactRegistryRepositoryCleanupPoliciesCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        most_recent_versions: typing.Optional[typing.Union["ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#id ArtifactRegistryRepository#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param action: Policy action. Possible values: ["DELETE", "KEEP"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#action ArtifactRegistryRepository#action}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#condition ArtifactRegistryRepository#condition}
        :param most_recent_versions: most_recent_versions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#most_recent_versions ArtifactRegistryRepository#most_recent_versions}
        '''
        if isinstance(condition, dict):
            condition = ArtifactRegistryRepositoryCleanupPoliciesCondition(**condition)
        if isinstance(most_recent_versions, dict):
            most_recent_versions = ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions(**most_recent_versions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d779e108a7ad18e03bf1ed416aa69bbe1bff0562f072fd04a87d47093a2b90d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#id ArtifactRegistryRepository#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Policy action. Possible values: ["DELETE", "KEEP"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#action ArtifactRegistryRepository#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryCleanupPoliciesCondition"]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#condition ArtifactRegistryRepository#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryCleanupPoliciesCondition"], result)

    @builtins.property
    def most_recent_versions(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions"]:
        '''most_recent_versions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#most_recent_versions ArtifactRegistryRepository#most_recent_versions}
        '''
        result = self._values.get("most_recent_versions")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryCleanupPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryCleanupPoliciesCondition",
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
class ArtifactRegistryRepositoryCleanupPoliciesCondition:
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
        :param newer_than: Match versions newer than a duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#newer_than ArtifactRegistryRepository#newer_than}
        :param older_than: Match versions older than a duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#older_than ArtifactRegistryRepository#older_than}
        :param package_name_prefixes: Match versions by package prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#package_name_prefixes ArtifactRegistryRepository#package_name_prefixes}
        :param tag_prefixes: Match versions by tag prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#tag_prefixes ArtifactRegistryRepository#tag_prefixes}
        :param tag_state: Match versions by tag status. Default value: "ANY" Possible values: ["TAGGED", "UNTAGGED", "ANY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#tag_state ArtifactRegistryRepository#tag_state}
        :param version_name_prefixes: Match versions by version name prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#version_name_prefixes ArtifactRegistryRepository#version_name_prefixes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a723337ca390dc3fbca30478be0b5ee80985c4b601726f80f049f6fca0390ad)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#newer_than ArtifactRegistryRepository#newer_than}
        '''
        result = self._values.get("newer_than")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def older_than(self) -> typing.Optional[builtins.str]:
        '''Match versions older than a duration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#older_than ArtifactRegistryRepository#older_than}
        '''
        result = self._values.get("older_than")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package_name_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Match versions by package prefix. Applied on any prefix match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#package_name_prefixes ArtifactRegistryRepository#package_name_prefixes}
        '''
        result = self._values.get("package_name_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Match versions by tag prefix. Applied on any prefix match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#tag_prefixes ArtifactRegistryRepository#tag_prefixes}
        '''
        result = self._values.get("tag_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_state(self) -> typing.Optional[builtins.str]:
        '''Match versions by tag status. Default value: "ANY" Possible values: ["TAGGED", "UNTAGGED", "ANY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#tag_state ArtifactRegistryRepository#tag_state}
        '''
        result = self._values.get("tag_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_name_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Match versions by version name prefix. Applied on any prefix match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#version_name_prefixes ArtifactRegistryRepository#version_name_prefixes}
        '''
        result = self._values.get("version_name_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryCleanupPoliciesCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryCleanupPoliciesConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryCleanupPoliciesConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e481f79deaa9eb1ac26215e6049c76db5d736af99acf24272c367b24647882e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0f88fb12952d89f0567106b24f3ee6013366caa9ccd95da5841c6487ad865fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newerThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="olderThan")
    def older_than(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "olderThan"))

    @older_than.setter
    def older_than(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc77247eec1df3f287228e17f45e14857fbfcefcd0315d938bbd8274445d715e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "olderThan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packageNamePrefixes")
    def package_name_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "packageNamePrefixes"))

    @package_name_prefixes.setter
    def package_name_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4adee502c5bc851780a97491029c849836c242c6b17148f2369aac8ae389463a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageNamePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagPrefixes")
    def tag_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tagPrefixes"))

    @tag_prefixes.setter
    def tag_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a340cbb31b18924fbd48c2bc51a47de55fd845467bdaed53dfe01654dbc7c35c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagState")
    def tag_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagState"))

    @tag_state.setter
    def tag_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb6d322cdad542ea1fa341560708176d75c8957ca6db663a3776aa28b6cdcfd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionNamePrefixes")
    def version_name_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "versionNamePrefixes"))

    @version_name_prefixes.setter
    def version_name_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53562f5db986c77a266ffeb4e8b0e16e391a576d221c3947172d026db7e10ac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionNamePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryCleanupPoliciesCondition]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryCleanupPoliciesCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryCleanupPoliciesCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7cd4d2d0e42d76f3421ccb09a292f4493d77be5e5c004798b47c4e7c26e67a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ArtifactRegistryRepositoryCleanupPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryCleanupPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b1a339d85f256633fc64b8a5852ca747fe6bfc0a8e37bb9424b9441eb4f42e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ArtifactRegistryRepositoryCleanupPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f695d02e0a8ef4fbc431b72a5b5726fc293cee14601a4ad04889458441e6380)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ArtifactRegistryRepositoryCleanupPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1eff90c235fc8673674b41e8f81c44ddb83ded4cc1100676ff967078a9cb010)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd20523bf222c2a7dab7961ce681db03c0854d70ee3cdbaa023b614a2dec936b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7a3cbc280b88eeb5507a9f9770e9e9cbc77154c3341476cb8d14e329138aff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArtifactRegistryRepositoryCleanupPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArtifactRegistryRepositoryCleanupPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArtifactRegistryRepositoryCleanupPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc027772abd79f9d8904b2078a7d493fa49975f31de668e0a1249e6ecb05ce42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions",
    jsii_struct_bases=[],
    name_mapping={
        "keep_count": "keepCount",
        "package_name_prefixes": "packageNamePrefixes",
    },
)
class ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions:
    def __init__(
        self,
        *,
        keep_count: typing.Optional[jsii.Number] = None,
        package_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param keep_count: Minimum number of versions to keep. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#keep_count ArtifactRegistryRepository#keep_count}
        :param package_name_prefixes: Match versions by package prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#package_name_prefixes ArtifactRegistryRepository#package_name_prefixes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bceb6363aab0f6ce517aab071e3166026688a74a8847491729400c496d19f49)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#keep_count ArtifactRegistryRepository#keep_count}
        '''
        result = self._values.get("keep_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def package_name_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Match versions by package prefix. Applied on any prefix match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#package_name_prefixes ArtifactRegistryRepository#package_name_prefixes}
        '''
        result = self._values.get("package_name_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fa36847b57f483c582a8c59c52f140abaf03fa8de00160dd0c4f2179f1fb7f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cff47c8854efbfb84bbc752e5ca81025319518d50a2a368acba68526a1255497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packageNamePrefixes")
    def package_name_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "packageNamePrefixes"))

    @package_name_prefixes.setter
    def package_name_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3401dab278fa66741d3cd1c8b07f660d0623c1937b51f53032a56f4022a5c9cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageNamePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79034754493257cd33857698eebd1247060e5fcdd161a22fcdf78e582e1c8835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ArtifactRegistryRepositoryCleanupPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryCleanupPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c673bf2bb06a93824cd1897a666873a31dcafc12c4b2fa6c594f92690a8e1d87)
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
        :param newer_than: Match versions newer than a duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#newer_than ArtifactRegistryRepository#newer_than}
        :param older_than: Match versions older than a duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#older_than ArtifactRegistryRepository#older_than}
        :param package_name_prefixes: Match versions by package prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#package_name_prefixes ArtifactRegistryRepository#package_name_prefixes}
        :param tag_prefixes: Match versions by tag prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#tag_prefixes ArtifactRegistryRepository#tag_prefixes}
        :param tag_state: Match versions by tag status. Default value: "ANY" Possible values: ["TAGGED", "UNTAGGED", "ANY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#tag_state ArtifactRegistryRepository#tag_state}
        :param version_name_prefixes: Match versions by version name prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#version_name_prefixes ArtifactRegistryRepository#version_name_prefixes}
        '''
        value = ArtifactRegistryRepositoryCleanupPoliciesCondition(
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
        :param keep_count: Minimum number of versions to keep. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#keep_count ArtifactRegistryRepository#keep_count}
        :param package_name_prefixes: Match versions by package prefix. Applied on any prefix match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#package_name_prefixes ArtifactRegistryRepository#package_name_prefixes}
        '''
        value = ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions(
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
    ) -> ArtifactRegistryRepositoryCleanupPoliciesConditionOutputReference:
        return typing.cast(ArtifactRegistryRepositoryCleanupPoliciesConditionOutputReference, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="mostRecentVersions")
    def most_recent_versions(
        self,
    ) -> ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersionsOutputReference:
        return typing.cast(ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersionsOutputReference, jsii.get(self, "mostRecentVersions"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryCleanupPoliciesCondition]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryCleanupPoliciesCondition], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mostRecentVersionsInput")
    def most_recent_versions_input(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions], jsii.get(self, "mostRecentVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5fcb3bc7ed8295f3315f6a76f23328190aa94a4160a14ac981b548c3927c6ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b580e77ce8194044b075b430ecbef38e8999728dfe8bbdba8f81b24f5b6d48f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryCleanupPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryCleanupPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryCleanupPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d493c02781ba8d3e0ab4beb16a0a6526a13a8f73b8c5a252bfd808583749d09f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryConfig",
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
class ArtifactRegistryRepositoryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cleanup_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ArtifactRegistryRepositoryCleanupPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cleanup_policy_dry_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        docker_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryDockerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        maven_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryMavenConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remote_repository_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ArtifactRegistryRepositoryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_repository_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryVirtualRepositoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vulnerability_scanning_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryVulnerabilityScanningConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param format: The format of packages that are stored in the repository. Supported formats can be found `here <https://cloud.google.com/artifact-registry/docs/supported-formats>`_. You can only create alpha formats if you are a member of the `alpha user group <https://cloud.google.com/artifact-registry/docs/supported-formats#alpha-access>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#format ArtifactRegistryRepository#format}
        :param repository_id: The last part of the repository name, for example: "repo1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository_id ArtifactRegistryRepository#repository_id}
        :param cleanup_policies: cleanup_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#cleanup_policies ArtifactRegistryRepository#cleanup_policies}
        :param cleanup_policy_dry_run: If true, the cleanup pipeline is prevented from deleting versions in this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#cleanup_policy_dry_run ArtifactRegistryRepository#cleanup_policy_dry_run}
        :param description: The user-provided description of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#description ArtifactRegistryRepository#description}
        :param docker_config: docker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#docker_config ArtifactRegistryRepository#docker_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#id ArtifactRegistryRepository#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: The Cloud KMS resource name of the customer managed encryption key that’s used to encrypt the contents of the Repository. Has the form: 'projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key'. This value may not be changed after the Repository has been created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#kms_key_name ArtifactRegistryRepository#kms_key_name}
        :param labels: Labels with user-defined metadata. This field may contain up to 64 entries. Label keys and values may be no longer than 63 characters. Label keys must begin with a lowercase letter and may only contain lowercase letters, numeric characters, underscores, and dashes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#labels ArtifactRegistryRepository#labels}
        :param location: The name of the repository's location. In addition to specific regions, special values for multi-region locations are 'asia', 'europe', and 'us'. See `here <https://cloud.google.com/artifact-registry/docs/repositories/repo-locations>`_, or use the `google_artifact_registry_locations <https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/artifact_registry_locations>`_ data source for possible values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#location ArtifactRegistryRepository#location}
        :param maven_config: maven_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#maven_config ArtifactRegistryRepository#maven_config}
        :param mode: The mode configures the repository to serve artifacts from different sources. Default value: "STANDARD_REPOSITORY" Possible values: ["STANDARD_REPOSITORY", "VIRTUAL_REPOSITORY", "REMOTE_REPOSITORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#mode ArtifactRegistryRepository#mode}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#project ArtifactRegistryRepository#project}.
        :param remote_repository_config: remote_repository_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#remote_repository_config ArtifactRegistryRepository#remote_repository_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#timeouts ArtifactRegistryRepository#timeouts}
        :param virtual_repository_config: virtual_repository_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#virtual_repository_config ArtifactRegistryRepository#virtual_repository_config}
        :param vulnerability_scanning_config: vulnerability_scanning_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#vulnerability_scanning_config ArtifactRegistryRepository#vulnerability_scanning_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(docker_config, dict):
            docker_config = ArtifactRegistryRepositoryDockerConfig(**docker_config)
        if isinstance(maven_config, dict):
            maven_config = ArtifactRegistryRepositoryMavenConfig(**maven_config)
        if isinstance(remote_repository_config, dict):
            remote_repository_config = ArtifactRegistryRepositoryRemoteRepositoryConfig(**remote_repository_config)
        if isinstance(timeouts, dict):
            timeouts = ArtifactRegistryRepositoryTimeouts(**timeouts)
        if isinstance(virtual_repository_config, dict):
            virtual_repository_config = ArtifactRegistryRepositoryVirtualRepositoryConfig(**virtual_repository_config)
        if isinstance(vulnerability_scanning_config, dict):
            vulnerability_scanning_config = ArtifactRegistryRepositoryVulnerabilityScanningConfig(**vulnerability_scanning_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc52ffe5420733d20d2e99ce6681ef3eba8299273d736628839f8efdc4ab70f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#format ArtifactRegistryRepository#format}
        '''
        result = self._values.get("format")
        assert result is not None, "Required property 'format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_id(self) -> builtins.str:
        '''The last part of the repository name, for example: "repo1".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository_id ArtifactRegistryRepository#repository_id}
        '''
        result = self._values.get("repository_id")
        assert result is not None, "Required property 'repository_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cleanup_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArtifactRegistryRepositoryCleanupPolicies]]]:
        '''cleanup_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#cleanup_policies ArtifactRegistryRepository#cleanup_policies}
        '''
        result = self._values.get("cleanup_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArtifactRegistryRepositoryCleanupPolicies]]], result)

    @builtins.property
    def cleanup_policy_dry_run(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the cleanup pipeline is prevented from deleting versions in this repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#cleanup_policy_dry_run ArtifactRegistryRepository#cleanup_policy_dry_run}
        '''
        result = self._values.get("cleanup_policy_dry_run")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The user-provided description of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#description ArtifactRegistryRepository#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_config(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryDockerConfig"]:
        '''docker_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#docker_config ArtifactRegistryRepository#docker_config}
        '''
        result = self._values.get("docker_config")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryDockerConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#id ArtifactRegistryRepository#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#kms_key_name ArtifactRegistryRepository#kms_key_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#labels ArtifactRegistryRepository#labels}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#location ArtifactRegistryRepository#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_config(self) -> typing.Optional["ArtifactRegistryRepositoryMavenConfig"]:
        '''maven_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#maven_config ArtifactRegistryRepository#maven_config}
        '''
        result = self._values.get("maven_config")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryMavenConfig"], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The mode configures the repository to serve artifacts from different sources. Default value: "STANDARD_REPOSITORY" Possible values: ["STANDARD_REPOSITORY", "VIRTUAL_REPOSITORY", "REMOTE_REPOSITORY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#mode ArtifactRegistryRepository#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#project ArtifactRegistryRepository#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_repository_config(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfig"]:
        '''remote_repository_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#remote_repository_config ArtifactRegistryRepository#remote_repository_config}
        '''
        result = self._values.get("remote_repository_config")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ArtifactRegistryRepositoryTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#timeouts ArtifactRegistryRepository#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryTimeouts"], result)

    @builtins.property
    def virtual_repository_config(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryVirtualRepositoryConfig"]:
        '''virtual_repository_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#virtual_repository_config ArtifactRegistryRepository#virtual_repository_config}
        '''
        result = self._values.get("virtual_repository_config")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryVirtualRepositoryConfig"], result)

    @builtins.property
    def vulnerability_scanning_config(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryVulnerabilityScanningConfig"]:
        '''vulnerability_scanning_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#vulnerability_scanning_config ArtifactRegistryRepository#vulnerability_scanning_config}
        '''
        result = self._values.get("vulnerability_scanning_config")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryVulnerabilityScanningConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryDockerConfig",
    jsii_struct_bases=[],
    name_mapping={"immutable_tags": "immutableTags"},
)
class ArtifactRegistryRepositoryDockerConfig:
    def __init__(
        self,
        *,
        immutable_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param immutable_tags: The repository which enabled this flag prevents all tags from being modified, moved or deleted. This does not prevent tags from being created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#immutable_tags ArtifactRegistryRepository#immutable_tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e99d1a86a033c5197277728390e013d86ed3332415bdae6fa6c72996e795ada)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#immutable_tags ArtifactRegistryRepository#immutable_tags}
        '''
        result = self._values.get("immutable_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryDockerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryDockerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryDockerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61549e21e1cf17fd350c3e0a707660a04e2ac7d7955d5154566c8df96ae9d34d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b90f9e6c4469065dfbc2658469cd70cc9a8f3f9845ab3289682e2eb32ae21c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "immutableTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ArtifactRegistryRepositoryDockerConfig]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryDockerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryDockerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b8ac8051ca177e9ded9152217518443e9751acd881dfaad616c9466ffd1de19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryMavenConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allow_snapshot_overwrites": "allowSnapshotOverwrites",
        "version_policy": "versionPolicy",
    },
)
class ArtifactRegistryRepositoryMavenConfig:
    def __init__(
        self,
        *,
        allow_snapshot_overwrites: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        version_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_snapshot_overwrites: The repository with this flag will allow publishing the same snapshot versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#allow_snapshot_overwrites ArtifactRegistryRepository#allow_snapshot_overwrites}
        :param version_policy: Version policy defines the versions that the registry will accept. Default value: "VERSION_POLICY_UNSPECIFIED" Possible values: ["VERSION_POLICY_UNSPECIFIED", "RELEASE", "SNAPSHOT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#version_policy ArtifactRegistryRepository#version_policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab74b67816791960f5139ec576f8259b9d8cdc969e2749b89a93b9760db53f8d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#allow_snapshot_overwrites ArtifactRegistryRepository#allow_snapshot_overwrites}
        '''
        result = self._values.get("allow_snapshot_overwrites")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def version_policy(self) -> typing.Optional[builtins.str]:
        '''Version policy defines the versions that the registry will accept. Default value: "VERSION_POLICY_UNSPECIFIED" Possible values: ["VERSION_POLICY_UNSPECIFIED", "RELEASE", "SNAPSHOT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#version_policy ArtifactRegistryRepository#version_policy}
        '''
        result = self._values.get("version_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryMavenConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryMavenConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryMavenConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7de1f438e290e9ca124de6b15183000f784044a570a2cc8274dbb09ac85bd612)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59457c2988da463670a580250b3df5163145aab91c25ac2c0371ed402579b347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowSnapshotOverwrites", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionPolicy")
    def version_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionPolicy"))

    @version_policy.setter
    def version_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22571ee4ba791f992e9ab633974cdf1f60df1bf9bbe80b4988d94b0c0d23b892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ArtifactRegistryRepositoryMavenConfig]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryMavenConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryMavenConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6acea51acdad5f11b8d1e2b94559f58d2fd3610fe5ae9c52c182a472573db047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfig",
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
class ArtifactRegistryRepositoryRemoteRepositoryConfig:
    def __init__(
        self,
        *,
        apt_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        common_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_upstream_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        docker_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        maven_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        npm_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        python_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        upstream_credentials: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        yum_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt_repository: apt_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#apt_repository ArtifactRegistryRepository#apt_repository}
        :param common_repository: common_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#common_repository ArtifactRegistryRepository#common_repository}
        :param description: The description of the remote source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#description ArtifactRegistryRepository#description}
        :param disable_upstream_validation: If true, the remote repository upstream and upstream credentials will not be validated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#disable_upstream_validation ArtifactRegistryRepository#disable_upstream_validation}
        :param docker_repository: docker_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#docker_repository ArtifactRegistryRepository#docker_repository}
        :param maven_repository: maven_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#maven_repository ArtifactRegistryRepository#maven_repository}
        :param npm_repository: npm_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#npm_repository ArtifactRegistryRepository#npm_repository}
        :param python_repository: python_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#python_repository ArtifactRegistryRepository#python_repository}
        :param upstream_credentials: upstream_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#upstream_credentials ArtifactRegistryRepository#upstream_credentials}
        :param yum_repository: yum_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#yum_repository ArtifactRegistryRepository#yum_repository}
        '''
        if isinstance(apt_repository, dict):
            apt_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository(**apt_repository)
        if isinstance(common_repository, dict):
            common_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository(**common_repository)
        if isinstance(docker_repository, dict):
            docker_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository(**docker_repository)
        if isinstance(maven_repository, dict):
            maven_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository(**maven_repository)
        if isinstance(npm_repository, dict):
            npm_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository(**npm_repository)
        if isinstance(python_repository, dict):
            python_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository(**python_repository)
        if isinstance(upstream_credentials, dict):
            upstream_credentials = ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials(**upstream_credentials)
        if isinstance(yum_repository, dict):
            yum_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository(**yum_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82fae93b99966d690cce1c6ffdab21d23b5c33e8202a1d2602b9db7e859d8a22)
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
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository"]:
        '''apt_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#apt_repository ArtifactRegistryRepository#apt_repository}
        '''
        result = self._values.get("apt_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository"], result)

    @builtins.property
    def common_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository"]:
        '''common_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#common_repository ArtifactRegistryRepository#common_repository}
        '''
        result = self._values.get("common_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the remote source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#description ArtifactRegistryRepository#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_upstream_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the remote repository upstream and upstream credentials will not be validated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#disable_upstream_validation ArtifactRegistryRepository#disable_upstream_validation}
        '''
        result = self._values.get("disable_upstream_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def docker_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository"]:
        '''docker_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#docker_repository ArtifactRegistryRepository#docker_repository}
        '''
        result = self._values.get("docker_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository"], result)

    @builtins.property
    def maven_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository"]:
        '''maven_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#maven_repository ArtifactRegistryRepository#maven_repository}
        '''
        result = self._values.get("maven_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository"], result)

    @builtins.property
    def npm_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository"]:
        '''npm_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#npm_repository ArtifactRegistryRepository#npm_repository}
        '''
        result = self._values.get("npm_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository"], result)

    @builtins.property
    def python_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository"]:
        '''python_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#python_repository ArtifactRegistryRepository#python_repository}
        '''
        result = self._values.get("python_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository"], result)

    @builtins.property
    def upstream_credentials(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials"]:
        '''upstream_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#upstream_credentials ArtifactRegistryRepository#upstream_credentials}
        '''
        result = self._values.get("upstream_credentials")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials"], result)

    @builtins.property
    def yum_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository"]:
        '''yum_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#yum_repository ArtifactRegistryRepository#yum_repository}
        '''
        result = self._values.get("yum_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository",
    jsii_struct_bases=[],
    name_mapping={"public_repository": "publicRepository"},
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository:
    def __init__(
        self,
        *,
        public_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param public_repository: public_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        if isinstance(public_repository, dict):
            public_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository(**public_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300c846a2ae5a576245ccd6b3de911bd33229cf547c147df5aedbb44346ab4f9)
            check_type(argname="argument public_repository", value=public_repository, expected_type=type_hints["public_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if public_repository is not None:
            self._values["public_repository"] = public_repository

    @builtins.property
    def public_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository"]:
        '''public_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c997a4738e9b06fb888c017f90b2c96d6e06b703db6860d293315757b2ff1a24)
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
        :param repository_base: A common public repository base for Apt, e.g. '"debian/dists/stable"' Possible values: ["DEBIAN", "UBUNTU", "DEBIAN_SNAPSHOT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository_base ArtifactRegistryRepository#repository_base}
        :param repository_path: Specific repository from the base. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository_path ArtifactRegistryRepository#repository_path}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository(
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
    ) -> "ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepositoryOutputReference":
        return typing.cast("ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepositoryOutputReference", jsii.get(self, "publicRepository"))

    @builtins.property
    @jsii.member(jsii_name="publicRepositoryInput")
    def public_repository_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository"], jsii.get(self, "publicRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51161952a1b0fd8de1c6b2ed76685c9798c76167a11d2395e72f4df60f88bbe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository",
    jsii_struct_bases=[],
    name_mapping={
        "repository_base": "repositoryBase",
        "repository_path": "repositoryPath",
    },
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository:
    def __init__(
        self,
        *,
        repository_base: builtins.str,
        repository_path: builtins.str,
    ) -> None:
        '''
        :param repository_base: A common public repository base for Apt, e.g. '"debian/dists/stable"' Possible values: ["DEBIAN", "UBUNTU", "DEBIAN_SNAPSHOT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository_base ArtifactRegistryRepository#repository_base}
        :param repository_path: Specific repository from the base. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository_path ArtifactRegistryRepository#repository_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c963998b6fab43e1b3024a5bc8dd6485c1f60e3efa64427639825fa7d99e63)
            check_type(argname="argument repository_base", value=repository_base, expected_type=type_hints["repository_base"])
            check_type(argname="argument repository_path", value=repository_path, expected_type=type_hints["repository_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_base": repository_base,
            "repository_path": repository_path,
        }

    @builtins.property
    def repository_base(self) -> builtins.str:
        '''A common public repository base for Apt, e.g. '"debian/dists/stable"' Possible values: ["DEBIAN", "UBUNTU", "DEBIAN_SNAPSHOT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository_base ArtifactRegistryRepository#repository_base}
        '''
        result = self._values.get("repository_base")
        assert result is not None, "Required property 'repository_base' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_path(self) -> builtins.str:
        '''Specific repository from the base.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository_path ArtifactRegistryRepository#repository_path}
        '''
        result = self._values.get("repository_path")
        assert result is not None, "Required property 'repository_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10a07a61e91481a6b576b846227e88a00d91917819dcfd0b0d8327225ef30cd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71560d243ed7a8aed1a646a375172d987be4b26ab4d10777ff8e70e297cb153b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryBase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryPath")
    def repository_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryPath"))

    @repository_path.setter
    def repository_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92be8249b7803056c69d6384bf30dd9f6050abf802728aa51c7bb722f28f18c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df82d7514ab8a0c3f199338399c2299520bab434b2beff38020bfb410979c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository:
    def __init__(self, *, uri: builtins.str) -> None:
        '''
        :param uri: One of: a. Artifact Registry Repository resource, e.g. 'projects/UPSTREAM_PROJECT_ID/locations/REGION/repositories/UPSTREAM_REPOSITORY' b. URI to the registry, e.g. '"https://registry-1.docker.io"' c. URI to Artifact Registry Repository, e.g. '"https://REGION-docker.pkg.dev/UPSTREAM_PROJECT_ID/UPSTREAM_REPOSITORY"' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#uri ArtifactRegistryRepository#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd01b487dac2973583cf329020200c4ef67329b71a82f8ebc57b732d716f9333)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#uri ArtifactRegistryRepository#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f9281b2802fca4fd2e4e25b661370edab87a3c7da246c8527a6c92c02e0d1f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__187051c167ed5eeae51e16b685aa935d1e24b595393c8e5006f33d0be6fb591e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a1e74f0a786b2d3d7137497fe7d8a2b4e34c914a27357e9bd33e7733fab67a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository",
    jsii_struct_bases=[],
    name_mapping={
        "custom_repository": "customRepository",
        "public_repository": "publicRepository",
    },
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository:
    def __init__(
        self,
        *,
        custom_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#custom_repository ArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "DOCKER_HUB" Possible values: ["DOCKER_HUB"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        if isinstance(custom_repository, dict):
            custom_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository(**custom_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397f2d79a97ae68da0790d57673a03814fd0461db9af716c54dd50bfef356c58)
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
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository"]:
        '''custom_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#custom_repository ArtifactRegistryRepository#custom_repository}
        '''
        result = self._values.get("custom_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository"], result)

    @builtins.property
    def public_repository(self) -> typing.Optional[builtins.str]:
        '''Address of the remote repository. Default value: "DOCKER_HUB" Possible values: ["DOCKER_HUB"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: Specific uri to the registry, e.g. '"https://registry-1.docker.io"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#uri ArtifactRegistryRepository#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b16525efc386cadeefd4fd6c915f33186054d788d9ff3ec7317233513998c0)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''Specific uri to the registry, e.g. '"https://registry-1.docker.io"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#uri ArtifactRegistryRepository#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d92f6316f9657e74671f5759e3a882b6ca30ae4a518ba8cda8f6f6704a5c466)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1519864aa5fcac3629f3de8981c5f8d90b9f9203261f9c98f2fa4a8998dd2a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281b80fc471796de4e2f9f83644a82bedfcbeb5ede0d8b7143bb73a43456de03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bb18bc31ba8a67f06f888e52d0abcac0b7f2849eb3fb0820ca336eed3e5ff0f)
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
        :param uri: Specific uri to the registry, e.g. '"https://registry-1.docker.io"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#uri ArtifactRegistryRepository#uri}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository(
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
    ) -> ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepositoryOutputReference:
        return typing.cast(ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepositoryOutputReference, jsii.get(self, "customRepository"))

    @builtins.property
    @jsii.member(jsii_name="customRepositoryInput")
    def custom_repository_input(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository], jsii.get(self, "customRepositoryInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2bd180a4f130999861b9c80b55a82803cd7b6cc9c649412cf7396f3c9b296232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicRepository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c7ca8b2e52f3ee8dfe0871595bd317928ff86f260843925bc60f9706519aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository",
    jsii_struct_bases=[],
    name_mapping={
        "custom_repository": "customRepository",
        "public_repository": "publicRepository",
    },
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository:
    def __init__(
        self,
        *,
        custom_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#custom_repository ArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "MAVEN_CENTRAL" Possible values: ["MAVEN_CENTRAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        if isinstance(custom_repository, dict):
            custom_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository(**custom_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba38fdee2f2ce5531e776ee3b15dda1479027e1355ba0e50d6c99da468d0adf2)
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
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository"]:
        '''custom_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#custom_repository ArtifactRegistryRepository#custom_repository}
        '''
        result = self._values.get("custom_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository"], result)

    @builtins.property
    def public_repository(self) -> typing.Optional[builtins.str]:
        '''Address of the remote repository. Default value: "MAVEN_CENTRAL" Possible values: ["MAVEN_CENTRAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: Specific uri to the registry, e.g. '"https://repo.maven.apache.org/maven2"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#uri ArtifactRegistryRepository#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb29ac1a7c2d7fec784586db5b46afe0e7d668a19a3924c00bfae565c45526c)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''Specific uri to the registry, e.g. '"https://repo.maven.apache.org/maven2"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#uri ArtifactRegistryRepository#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__777e8f9e7c3e6a93e362a08cd4d597c63769946aa69eeeb1547367e209a1a0a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efd3998696470e26ba7e74943855059ef50b94f080f9a8b18fc592af7c21c6e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f71b79d77d41bca15fe768cc9c2c50f81127afeaa7c02d1fcb080b6db6755e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af0beed1640c17c515e7d2b326ead966ae9b114b1b5020f9ce3a1701856ca967)
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
        :param uri: Specific uri to the registry, e.g. '"https://repo.maven.apache.org/maven2"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#uri ArtifactRegistryRepository#uri}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository(
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
    ) -> ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepositoryOutputReference:
        return typing.cast(ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepositoryOutputReference, jsii.get(self, "customRepository"))

    @builtins.property
    @jsii.member(jsii_name="customRepositoryInput")
    def custom_repository_input(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository], jsii.get(self, "customRepositoryInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__15edb506c93bf8df67f6bd145fd0a3c4e8931fb25143e38292853e38cffb12d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicRepository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0967229979d8b24a2c27058db22fb49edcf98238452786dc6c4b643d6e251199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository",
    jsii_struct_bases=[],
    name_mapping={
        "custom_repository": "customRepository",
        "public_repository": "publicRepository",
    },
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository:
    def __init__(
        self,
        *,
        custom_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#custom_repository ArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "NPMJS" Possible values: ["NPMJS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        if isinstance(custom_repository, dict):
            custom_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository(**custom_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da84ff59d29f822b2ecd0f03ece2cce30e5572ee6a0e4f053a8b8fc4543eed8e)
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
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository"]:
        '''custom_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#custom_repository ArtifactRegistryRepository#custom_repository}
        '''
        result = self._values.get("custom_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository"], result)

    @builtins.property
    def public_repository(self) -> typing.Optional[builtins.str]:
        '''Address of the remote repository. Default value: "NPMJS" Possible values: ["NPMJS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: Specific uri to the registry, e.g. '"https://registry.npmjs.org"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#uri ArtifactRegistryRepository#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74fa4e0a6576d27a751c9c7231762931fbb052c51975605974b628483c35c98)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''Specific uri to the registry, e.g. '"https://registry.npmjs.org"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#uri ArtifactRegistryRepository#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cccc4b5030a0923fa86c1c3ae9699c0627b2478dc2d4ebb28036dd08d627a34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afd23bc231343654724dde51264ee81ec04e448be732e4b450c331368b8b5b3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6f0b8d3821f802437289d94d132d7b7798c0f93840615cc65743ff0277e2b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba7d1d42db8b2cbc416852b144f3b51935b5a02d2a35b43c49ba723d8449cc97)
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
        :param uri: Specific uri to the registry, e.g. '"https://registry.npmjs.org"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#uri ArtifactRegistryRepository#uri}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository(
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
    ) -> ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepositoryOutputReference:
        return typing.cast(ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepositoryOutputReference, jsii.get(self, "customRepository"))

    @builtins.property
    @jsii.member(jsii_name="customRepositoryInput")
    def custom_repository_input(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository], jsii.get(self, "customRepositoryInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__65d88a5f4effea9d3ed0c4db80cfe8cbd1db8ec5148675ceec8b9d909abcfbfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicRepository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f04d62d80a238b32126a9986d2e62e97475407018d15b73f88ddea3a313ca739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ArtifactRegistryRepositoryRemoteRepositoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b263eb93494647a7ef5a05f1542d8dc0c2ef71516a22738794e56db676bc4ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAptRepository")
    def put_apt_repository(
        self,
        *,
        public_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param public_repository: public_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository(
            public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putAptRepository", [value]))

    @jsii.member(jsii_name="putCommonRepository")
    def put_common_repository(self, *, uri: builtins.str) -> None:
        '''
        :param uri: One of: a. Artifact Registry Repository resource, e.g. 'projects/UPSTREAM_PROJECT_ID/locations/REGION/repositories/UPSTREAM_REPOSITORY' b. URI to the registry, e.g. '"https://registry-1.docker.io"' c. URI to Artifact Registry Repository, e.g. '"https://REGION-docker.pkg.dev/UPSTREAM_PROJECT_ID/UPSTREAM_REPOSITORY"' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#uri ArtifactRegistryRepository#uri}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository(
            uri=uri
        )

        return typing.cast(None, jsii.invoke(self, "putCommonRepository", [value]))

    @jsii.member(jsii_name="putDockerRepository")
    def put_docker_repository(
        self,
        *,
        custom_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository, typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#custom_repository ArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "DOCKER_HUB" Possible values: ["DOCKER_HUB"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository(
            custom_repository=custom_repository, public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putDockerRepository", [value]))

    @jsii.member(jsii_name="putMavenRepository")
    def put_maven_repository(
        self,
        *,
        custom_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository, typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#custom_repository ArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "MAVEN_CENTRAL" Possible values: ["MAVEN_CENTRAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository(
            custom_repository=custom_repository, public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putMavenRepository", [value]))

    @jsii.member(jsii_name="putNpmRepository")
    def put_npm_repository(
        self,
        *,
        custom_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository, typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#custom_repository ArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "NPMJS" Possible values: ["NPMJS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository(
            custom_repository=custom_repository, public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putNpmRepository", [value]))

    @jsii.member(jsii_name="putPythonRepository")
    def put_python_repository(
        self,
        *,
        custom_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#custom_repository ArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "PYPI" Possible values: ["PYPI"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository(
            custom_repository=custom_repository, public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putPythonRepository", [value]))

    @jsii.member(jsii_name="putUpstreamCredentials")
    def put_upstream_credentials(
        self,
        *,
        username_password_credentials: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param username_password_credentials: username_password_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#username_password_credentials ArtifactRegistryRepository#username_password_credentials}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials(
            username_password_credentials=username_password_credentials
        )

        return typing.cast(None, jsii.invoke(self, "putUpstreamCredentials", [value]))

    @jsii.member(jsii_name="putYumRepository")
    def put_yum_repository(
        self,
        *,
        public_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param public_repository: public_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository(
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
    ) -> ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryOutputReference:
        return typing.cast(ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryOutputReference, jsii.get(self, "aptRepository"))

    @builtins.property
    @jsii.member(jsii_name="commonRepository")
    def common_repository(
        self,
    ) -> ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepositoryOutputReference:
        return typing.cast(ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepositoryOutputReference, jsii.get(self, "commonRepository"))

    @builtins.property
    @jsii.member(jsii_name="dockerRepository")
    def docker_repository(
        self,
    ) -> ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryOutputReference:
        return typing.cast(ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryOutputReference, jsii.get(self, "dockerRepository"))

    @builtins.property
    @jsii.member(jsii_name="mavenRepository")
    def maven_repository(
        self,
    ) -> ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryOutputReference:
        return typing.cast(ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryOutputReference, jsii.get(self, "mavenRepository"))

    @builtins.property
    @jsii.member(jsii_name="npmRepository")
    def npm_repository(
        self,
    ) -> ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryOutputReference:
        return typing.cast(ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryOutputReference, jsii.get(self, "npmRepository"))

    @builtins.property
    @jsii.member(jsii_name="pythonRepository")
    def python_repository(
        self,
    ) -> "ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryOutputReference":
        return typing.cast("ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryOutputReference", jsii.get(self, "pythonRepository"))

    @builtins.property
    @jsii.member(jsii_name="upstreamCredentials")
    def upstream_credentials(
        self,
    ) -> "ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsOutputReference":
        return typing.cast("ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsOutputReference", jsii.get(self, "upstreamCredentials"))

    @builtins.property
    @jsii.member(jsii_name="yumRepository")
    def yum_repository(
        self,
    ) -> "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryOutputReference":
        return typing.cast("ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryOutputReference", jsii.get(self, "yumRepository"))

    @builtins.property
    @jsii.member(jsii_name="aptRepositoryInput")
    def apt_repository_input(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository], jsii.get(self, "aptRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="commonRepositoryInput")
    def common_repository_input(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository], jsii.get(self, "commonRepositoryInput"))

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
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository], jsii.get(self, "dockerRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="mavenRepositoryInput")
    def maven_repository_input(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository], jsii.get(self, "mavenRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="npmRepositoryInput")
    def npm_repository_input(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository], jsii.get(self, "npmRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="pythonRepositoryInput")
    def python_repository_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository"], jsii.get(self, "pythonRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="upstreamCredentialsInput")
    def upstream_credentials_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials"], jsii.get(self, "upstreamCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="yumRepositoryInput")
    def yum_repository_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository"], jsii.get(self, "yumRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1afb8b15d0d3fcc2add65376ff228e8a4335ba93e34ce821e01bc8255b34b217)
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
            type_hints = typing.get_type_hints(_typecheckingstub__388d7b4f6f6b4ff40a2c90e4e8106ccdc53eb5d177445f8e115f4f8a938a3868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableUpstreamValidation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfig]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__335e955d30d46bab332ba5170d3d45dacf675c50c7fb336b5003e7f48d39d827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository",
    jsii_struct_bases=[],
    name_mapping={
        "custom_repository": "customRepository",
        "public_repository": "publicRepository",
    },
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository:
    def __init__(
        self,
        *,
        custom_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_repository: custom_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#custom_repository ArtifactRegistryRepository#custom_repository}
        :param public_repository: Address of the remote repository. Default value: "PYPI" Possible values: ["PYPI"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        if isinstance(custom_repository, dict):
            custom_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository(**custom_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__def391e54a01e3f1db2cd742e8080c422019f6227a3674080966e314acde5fc2)
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
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository"]:
        '''custom_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#custom_repository ArtifactRegistryRepository#custom_repository}
        '''
        result = self._values.get("custom_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository"], result)

    @builtins.property
    def public_repository(self) -> typing.Optional[builtins.str]:
        '''Address of the remote repository. Default value: "PYPI" Possible values: ["PYPI"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: Specific uri to the registry, e.g. '"https://pypi.io"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#uri ArtifactRegistryRepository#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e3d977a5465eb2ba9661712a78ddc58e3c55562e1ca0bec537dd7e7437dafa)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''Specific uri to the registry, e.g. '"https://pypi.io"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#uri ArtifactRegistryRepository#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68d0571e8e5e91b976ac2c8fcb1b87d8e37ebd3858306db3e1a71b66e2270c6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2676708d572e81b6ed1cef789ba90142f47f234fe3f2d677321a6d76199acad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d6b08bb2e66304553a331c4ee05c58e49d70bfaa52b45d6a57c35ce5d725c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e70ac559643c59ff67274cfd635c7635237d98d75b7d6501734ea78874ed7fc8)
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
        :param uri: Specific uri to the registry, e.g. '"https://pypi.io"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#uri ArtifactRegistryRepository#uri}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository(
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
    ) -> ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepositoryOutputReference:
        return typing.cast(ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepositoryOutputReference, jsii.get(self, "customRepository"))

    @builtins.property
    @jsii.member(jsii_name="customRepositoryInput")
    def custom_repository_input(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository], jsii.get(self, "customRepositoryInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__714b00dcb034202919373219bac95b7e2c0d7bc93e65bb2f04899afa5af48512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicRepository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee424b93b167760573681b792df9ebd73f4b0f9b62314ac6aabf32f251937da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials",
    jsii_struct_bases=[],
    name_mapping={"username_password_credentials": "usernamePasswordCredentials"},
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials:
    def __init__(
        self,
        *,
        username_password_credentials: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param username_password_credentials: username_password_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#username_password_credentials ArtifactRegistryRepository#username_password_credentials}
        '''
        if isinstance(username_password_credentials, dict):
            username_password_credentials = ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials(**username_password_credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed9800845a0e580c9c5c7904c5ead630b6597168e50fb7e6ef69e15062ddd7a)
            check_type(argname="argument username_password_credentials", value=username_password_credentials, expected_type=type_hints["username_password_credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if username_password_credentials is not None:
            self._values["username_password_credentials"] = username_password_credentials

    @builtins.property
    def username_password_credentials(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials"]:
        '''username_password_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#username_password_credentials ArtifactRegistryRepository#username_password_credentials}
        '''
        result = self._values.get("username_password_credentials")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e269fe61f8e75009f7599e887af02e977bd0630f442113057cbf7889d7c5892)
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
        :param password_secret_version: The Secret Manager key version that holds the password to access the remote repository. Must be in the format of 'projects/{project}/secrets/{secret}/versions/{version}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#password_secret_version ArtifactRegistryRepository#password_secret_version}
        :param username: The username to access the remote repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#username ArtifactRegistryRepository#username}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials(
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
    ) -> "ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentialsOutputReference":
        return typing.cast("ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentialsOutputReference", jsii.get(self, "usernamePasswordCredentials"))

    @builtins.property
    @jsii.member(jsii_name="usernamePasswordCredentialsInput")
    def username_password_credentials_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials"], jsii.get(self, "usernamePasswordCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f3c2756937b6e8c73ab6c2e95de186e66a10c1ce90216a14456c1ccd8d7096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "password_secret_version": "passwordSecretVersion",
        "username": "username",
    },
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials:
    def __init__(
        self,
        *,
        password_secret_version: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password_secret_version: The Secret Manager key version that holds the password to access the remote repository. Must be in the format of 'projects/{project}/secrets/{secret}/versions/{version}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#password_secret_version ArtifactRegistryRepository#password_secret_version}
        :param username: The username to access the remote repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#username ArtifactRegistryRepository#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35ddbbca97dabcdbdf6bad4c027bc435662e6b9dfdb4e52a5fa396d2706f038)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#password_secret_version ArtifactRegistryRepository#password_secret_version}
        '''
        result = self._values.get("password_secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username to access the remote repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#username ArtifactRegistryRepository#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__626adf17d3c586e645da019a654cd00657ce54d04a299c36d0cac4cfd20515b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a42b073587a000c789091b5d3f388b93203edbbdda954cdfd00001b3fad9f463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fcd89f1f11002e0d296f740be097ba25023d46e18045e9fe3e3efa8c87c4218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4308234ff03b2fdb657f6846dfd76214c46a97b42839fd5bad8c34494f52522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository",
    jsii_struct_bases=[],
    name_mapping={"public_repository": "publicRepository"},
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository:
    def __init__(
        self,
        *,
        public_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param public_repository: public_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        if isinstance(public_repository, dict):
            public_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository(**public_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0325bb5263fbf3dd1c49906424438086b215785501498497e43318f82e268502)
            check_type(argname="argument public_repository", value=public_repository, expected_type=type_hints["public_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if public_repository is not None:
            self._values["public_repository"] = public_repository

    @builtins.property
    def public_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository"]:
        '''public_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2a679b7385c63e61781d5ba83d69f83403e966957e55e74b4b95d6f7924417e)
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
        :param repository_base: A common public repository base for Yum. Possible values: ["CENTOS", "CENTOS_DEBUG", "CENTOS_VAULT", "CENTOS_STREAM", "ROCKY", "EPEL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository_base ArtifactRegistryRepository#repository_base}
        :param repository_path: Specific repository from the base, e.g. '"pub/rocky/9/BaseOS/x86_64/os"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository_path ArtifactRegistryRepository#repository_path}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository(
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
    ) -> "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepositoryOutputReference":
        return typing.cast("ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepositoryOutputReference", jsii.get(self, "publicRepository"))

    @builtins.property
    @jsii.member(jsii_name="publicRepositoryInput")
    def public_repository_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository"], jsii.get(self, "publicRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__795c783ef1a61c13463d176923e925a389ed5535752ba0b92833d82eda9c2a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository",
    jsii_struct_bases=[],
    name_mapping={
        "repository_base": "repositoryBase",
        "repository_path": "repositoryPath",
    },
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository:
    def __init__(
        self,
        *,
        repository_base: builtins.str,
        repository_path: builtins.str,
    ) -> None:
        '''
        :param repository_base: A common public repository base for Yum. Possible values: ["CENTOS", "CENTOS_DEBUG", "CENTOS_VAULT", "CENTOS_STREAM", "ROCKY", "EPEL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository_base ArtifactRegistryRepository#repository_base}
        :param repository_path: Specific repository from the base, e.g. '"pub/rocky/9/BaseOS/x86_64/os"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository_path ArtifactRegistryRepository#repository_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6917a87e677c8afb340d0ae49a5a195f0973b54c79d23dddcd6e886b50d376c3)
            check_type(argname="argument repository_base", value=repository_base, expected_type=type_hints["repository_base"])
            check_type(argname="argument repository_path", value=repository_path, expected_type=type_hints["repository_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_base": repository_base,
            "repository_path": repository_path,
        }

    @builtins.property
    def repository_base(self) -> builtins.str:
        '''A common public repository base for Yum. Possible values: ["CENTOS", "CENTOS_DEBUG", "CENTOS_VAULT", "CENTOS_STREAM", "ROCKY", "EPEL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository_base ArtifactRegistryRepository#repository_base}
        '''
        result = self._values.get("repository_base")
        assert result is not None, "Required property 'repository_base' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_path(self) -> builtins.str:
        '''Specific repository from the base, e.g. '"pub/rocky/9/BaseOS/x86_64/os"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository_path ArtifactRegistryRepository#repository_path}
        '''
        result = self._values.get("repository_path")
        assert result is not None, "Required property 'repository_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb17542fcbef07b7b65e243e58c5a1d610542508aa99afe4e8d5d813ceae497a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30bc36ee6ab3fdbfee0513aa8c24c128a8fb26ef0024e75b9b0e08c8a9564b9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryBase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryPath")
    def repository_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryPath"))

    @repository_path.setter
    def repository_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c74e19a498de2e28d1ef89880839d03d47e506a34485b0015961b9221eddf64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca8b46f624277ac3b2ab3654bcf833d876c15ae525ba527605900e6cbcb1f16f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ArtifactRegistryRepositoryTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#create ArtifactRegistryRepository#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#delete ArtifactRegistryRepository#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#update ArtifactRegistryRepository#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1444b73787658b044250e4edc0ea20b21f736e87083196f04e2556bd8d5c677)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#create ArtifactRegistryRepository#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#delete ArtifactRegistryRepository#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#update ArtifactRegistryRepository#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26dca7d4ae65a212ede6de83a10f5b14116f2ef75ae17d92d4dc4ffcbf2041b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85d69747494000d92dc610c0eb0b57f4f3780e477255afe36ff5a0cd11cce934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12da1b37cbf109ef1a6a64d699ba5db80deefea61cce62b902f5ae18b40daff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0cc863215ef4932536d9da06d0ed0c5b214ee89661ea8cce078c9f5a2e0e4c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f058e316f09dc0fe291c88f34ed01a42fd5633e01df8fcea67d75b0dc864c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryVirtualRepositoryConfig",
    jsii_struct_bases=[],
    name_mapping={"upstream_policies": "upstreamPolicies"},
)
class ArtifactRegistryRepositoryVirtualRepositoryConfig:
    def __init__(
        self,
        *,
        upstream_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param upstream_policies: upstream_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#upstream_policies ArtifactRegistryRepository#upstream_policies}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9906605cc83e6b5985e1d336201586b3acd778608ed073fb5afa738b5022e4)
            check_type(argname="argument upstream_policies", value=upstream_policies, expected_type=type_hints["upstream_policies"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if upstream_policies is not None:
            self._values["upstream_policies"] = upstream_policies

    @builtins.property
    def upstream_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies"]]]:
        '''upstream_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#upstream_policies ArtifactRegistryRepository#upstream_policies}
        '''
        result = self._values.get("upstream_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryVirtualRepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryVirtualRepositoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryVirtualRepositoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b803975416b5f5d0bbc8f707317eb0ff6359f28a275081d3886f1f37207faf8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putUpstreamPolicies")
    def put_upstream_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7211658b6ca71f47ae5d894f55cf62b3ea4ea89908d146f41431f5704f78721c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUpstreamPolicies", [value]))

    @jsii.member(jsii_name="resetUpstreamPolicies")
    def reset_upstream_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpstreamPolicies", []))

    @builtins.property
    @jsii.member(jsii_name="upstreamPolicies")
    def upstream_policies(
        self,
    ) -> "ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesList":
        return typing.cast("ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesList", jsii.get(self, "upstreamPolicies"))

    @builtins.property
    @jsii.member(jsii_name="upstreamPoliciesInput")
    def upstream_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies"]]], jsii.get(self, "upstreamPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryVirtualRepositoryConfig]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryVirtualRepositoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryVirtualRepositoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2978abcfb56761c7ca06f7d4bb7b8a69988573a61452d5be424a6ba4c7b6dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "priority": "priority", "repository": "repository"},
)
class ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The user-provided ID of the upstream policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#id ArtifactRegistryRepository#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param priority: Entries with a greater priority value take precedence in the pull order. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#priority ArtifactRegistryRepository#priority}
        :param repository: A reference to the repository resource, for example: "projects/p1/locations/us-central1/repository/repo1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository ArtifactRegistryRepository#repository}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24574f713916965d204fbfe34b4a654ef0a2934d7c3cb3289365c70299081c42)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#id ArtifactRegistryRepository#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Entries with a greater priority value take precedence in the pull order.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#priority ArtifactRegistryRepository#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''A reference to the repository resource, for example: "projects/p1/locations/us-central1/repository/repo1".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#repository ArtifactRegistryRepository#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a874ecabc5dd02ac4c4eaaf4bce7f7e04b7ba5d0f78e84768ed764cc25f4c872)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1660bf1a29276e875a1184bd44330514a93aa5de00ea61eeee47476691977bc0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c128da1866b80bc63bc8ad24783e82f9af92fc054f65f655ef5c1cec8620e28e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f2300e1fe2ee0d0faf4882c8e5e4dfc1802b070ccfde75d4e486342d527a6ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc1aaf8cd690ebf63ed3b7f970c37841227c1a03318793e73bd3827602c1bf92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab2f3301b37bfe8f891fb8408c56769a27b373f5934dcc3f55706fe9da1eda7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d61231823d0d4f3f09e5cb548418febd034e0d518e95a60b8eeddf4c4e5fa109)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f396c652930778d5065441f65480c08523b5586baeb544a5065bcaa50714b34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d715394ad5be31535b01945855216ddeed98cc338263cfcd56fba9154146479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d0df23a58c6aa0e390bde702de297c92176603d8599f4831b0a801d73ff0ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1951af240571932f728b60aafb545caa1f7bf153c615f505418c2221cd6bc7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryVulnerabilityScanningConfig",
    jsii_struct_bases=[],
    name_mapping={"enablement_config": "enablementConfig"},
)
class ArtifactRegistryRepositoryVulnerabilityScanningConfig:
    def __init__(
        self,
        *,
        enablement_config: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enablement_config: This configures whether vulnerability scanning is automatically performed for artifacts pushed to this repository. Possible values: ["INHERITED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#enablement_config ArtifactRegistryRepository#enablement_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e919ba847c20b4a9df6715848609ca8a5284a45ab68dbcd38f15b80709c0051)
            check_type(argname="argument enablement_config", value=enablement_config, expected_type=type_hints["enablement_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enablement_config is not None:
            self._values["enablement_config"] = enablement_config

    @builtins.property
    def enablement_config(self) -> typing.Optional[builtins.str]:
        '''This configures whether vulnerability scanning is automatically performed for artifacts pushed to this repository. Possible values: ["INHERITED", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/artifact_registry_repository#enablement_config ArtifactRegistryRepository#enablement_config}
        '''
        result = self._values.get("enablement_config")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryVulnerabilityScanningConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryVulnerabilityScanningConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryVulnerabilityScanningConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0651179996c574010d059a6848493258b61dfc106f60100742ad5a30e1b54f7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a264f906bb270fe3ca5548439cfce4c17e27b98adbd7c1e95404b6cda382f5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablementConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryVulnerabilityScanningConfig]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryVulnerabilityScanningConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryVulnerabilityScanningConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47609a628ee33142d3452b7debdf2fcb68d5f82d609a0022411a96799e59bf90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ArtifactRegistryRepository",
    "ArtifactRegistryRepositoryCleanupPolicies",
    "ArtifactRegistryRepositoryCleanupPoliciesCondition",
    "ArtifactRegistryRepositoryCleanupPoliciesConditionOutputReference",
    "ArtifactRegistryRepositoryCleanupPoliciesList",
    "ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions",
    "ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersionsOutputReference",
    "ArtifactRegistryRepositoryCleanupPoliciesOutputReference",
    "ArtifactRegistryRepositoryConfig",
    "ArtifactRegistryRepositoryDockerConfig",
    "ArtifactRegistryRepositoryDockerConfigOutputReference",
    "ArtifactRegistryRepositoryMavenConfig",
    "ArtifactRegistryRepositoryMavenConfigOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfig",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentialsOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepositoryOutputReference",
    "ArtifactRegistryRepositoryTimeouts",
    "ArtifactRegistryRepositoryTimeoutsOutputReference",
    "ArtifactRegistryRepositoryVirtualRepositoryConfig",
    "ArtifactRegistryRepositoryVirtualRepositoryConfigOutputReference",
    "ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies",
    "ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesList",
    "ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesOutputReference",
    "ArtifactRegistryRepositoryVulnerabilityScanningConfig",
    "ArtifactRegistryRepositoryVulnerabilityScanningConfigOutputReference",
]

publication.publish()

def _typecheckingstub__9bcd8979225c9247b853165d6a61a0418712e3dd7ba1d971f4a680f60b10baaf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    format: builtins.str,
    repository_id: builtins.str,
    cleanup_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ArtifactRegistryRepositoryCleanupPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cleanup_policy_dry_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    docker_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryDockerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    maven_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryMavenConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remote_repository_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ArtifactRegistryRepositoryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_repository_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryVirtualRepositoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    vulnerability_scanning_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryVulnerabilityScanningConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__33aad0a68069b65e2c34d279460b4995b6b389a08707d749699514809769f508(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ea72533f282686af801e988c50fc6c7af35bbc78fa36f7c4c4315bc6d2f735(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ArtifactRegistryRepositoryCleanupPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca0ab3a8fae4060ebaec2d4aa5347a729a85e2c1c9c13355d42075fd63073f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2165c18d7acb1a9627989cb5defe6b690405516e3f1d4547298a0905c9cba6ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb192c76d83ad27ed556a5fdb2c8834cef53c7d066348fc3138e98c0da765f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567479c5ca63288cb191b7917c2c8c7b1a7f65455a55aa2d836fc08bfe19347f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27069919d7606a89c8c364f9b9c838bb781ac21dae4c0b0fff13fe3cb27a446(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1efd52613e06a5587e0511c8d71a516d56312b5f65a9444853959e0e66909b1c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97953148b3c876edd5e36efdcd6a37041ea048618cfa6633e207c3a2f08b5a90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e187ab5b4160e21cd06788db103967f2abe29800b19b393fa21d07c4ef5c68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5317b275f0dad4386cf514228fffbf224db11181ffc92b16a4e3fd8df2e98316(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11e57d193991945e90c037b5c5b4e93d52dda2b58aa6c02b4eb1e82e6b7942b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d779e108a7ad18e03bf1ed416aa69bbe1bff0562f072fd04a87d47093a2b90d(
    *,
    id: builtins.str,
    action: typing.Optional[builtins.str] = None,
    condition: typing.Optional[typing.Union[ArtifactRegistryRepositoryCleanupPoliciesCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    most_recent_versions: typing.Optional[typing.Union[ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a723337ca390dc3fbca30478be0b5ee80985c4b601726f80f049f6fca0390ad(
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

def _typecheckingstub__e481f79deaa9eb1ac26215e6049c76db5d736af99acf24272c367b24647882e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f88fb12952d89f0567106b24f3ee6013366caa9ccd95da5841c6487ad865fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc77247eec1df3f287228e17f45e14857fbfcefcd0315d938bbd8274445d715e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4adee502c5bc851780a97491029c849836c242c6b17148f2369aac8ae389463a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a340cbb31b18924fbd48c2bc51a47de55fd845467bdaed53dfe01654dbc7c35c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6d322cdad542ea1fa341560708176d75c8957ca6db663a3776aa28b6cdcfd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53562f5db986c77a266ffeb4e8b0e16e391a576d221c3947172d026db7e10ac6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7cd4d2d0e42d76f3421ccb09a292f4493d77be5e5c004798b47c4e7c26e67a(
    value: typing.Optional[ArtifactRegistryRepositoryCleanupPoliciesCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b1a339d85f256633fc64b8a5852ca747fe6bfc0a8e37bb9424b9441eb4f42e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f695d02e0a8ef4fbc431b72a5b5726fc293cee14601a4ad04889458441e6380(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1eff90c235fc8673674b41e8f81c44ddb83ded4cc1100676ff967078a9cb010(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd20523bf222c2a7dab7961ce681db03c0854d70ee3cdbaa023b614a2dec936b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a3cbc280b88eeb5507a9f9770e9e9cbc77154c3341476cb8d14e329138aff6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc027772abd79f9d8904b2078a7d493fa49975f31de668e0a1249e6ecb05ce42(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArtifactRegistryRepositoryCleanupPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bceb6363aab0f6ce517aab071e3166026688a74a8847491729400c496d19f49(
    *,
    keep_count: typing.Optional[jsii.Number] = None,
    package_name_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa36847b57f483c582a8c59c52f140abaf03fa8de00160dd0c4f2179f1fb7f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff47c8854efbfb84bbc752e5ca81025319518d50a2a368acba68526a1255497(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3401dab278fa66741d3cd1c8b07f660d0623c1937b51f53032a56f4022a5c9cd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79034754493257cd33857698eebd1247060e5fcdd161a22fcdf78e582e1c8835(
    value: typing.Optional[ArtifactRegistryRepositoryCleanupPoliciesMostRecentVersions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c673bf2bb06a93824cd1897a666873a31dcafc12c4b2fa6c594f92690a8e1d87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5fcb3bc7ed8295f3315f6a76f23328190aa94a4160a14ac981b548c3927c6ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b580e77ce8194044b075b430ecbef38e8999728dfe8bbdba8f81b24f5b6d48f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d493c02781ba8d3e0ab4beb16a0a6526a13a8f73b8c5a252bfd808583749d09f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryCleanupPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc52ffe5420733d20d2e99ce6681ef3eba8299273d736628839f8efdc4ab70f(
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
    cleanup_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ArtifactRegistryRepositoryCleanupPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cleanup_policy_dry_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    docker_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryDockerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    maven_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryMavenConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remote_repository_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ArtifactRegistryRepositoryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_repository_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryVirtualRepositoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    vulnerability_scanning_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryVulnerabilityScanningConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e99d1a86a033c5197277728390e013d86ed3332415bdae6fa6c72996e795ada(
    *,
    immutable_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61549e21e1cf17fd350c3e0a707660a04e2ac7d7955d5154566c8df96ae9d34d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b90f9e6c4469065dfbc2658469cd70cc9a8f3f9845ab3289682e2eb32ae21c9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b8ac8051ca177e9ded9152217518443e9751acd881dfaad616c9466ffd1de19(
    value: typing.Optional[ArtifactRegistryRepositoryDockerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab74b67816791960f5139ec576f8259b9d8cdc969e2749b89a93b9760db53f8d(
    *,
    allow_snapshot_overwrites: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    version_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de1f438e290e9ca124de6b15183000f784044a570a2cc8274dbb09ac85bd612(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59457c2988da463670a580250b3df5163145aab91c25ac2c0371ed402579b347(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22571ee4ba791f992e9ab633974cdf1f60df1bf9bbe80b4988d94b0c0d23b892(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acea51acdad5f11b8d1e2b94559f58d2fd3610fe5ae9c52c182a472573db047(
    value: typing.Optional[ArtifactRegistryRepositoryMavenConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fae93b99966d690cce1c6ffdab21d23b5c33e8202a1d2602b9db7e859d8a22(
    *,
    apt_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    common_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_upstream_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    docker_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    maven_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    npm_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    python_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    upstream_credentials: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    yum_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300c846a2ae5a576245ccd6b3de911bd33229cf547c147df5aedbb44346ab4f9(
    *,
    public_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c997a4738e9b06fb888c017f90b2c96d6e06b703db6860d293315757b2ff1a24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51161952a1b0fd8de1c6b2ed76685c9798c76167a11d2395e72f4df60f88bbe6(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c963998b6fab43e1b3024a5bc8dd6485c1f60e3efa64427639825fa7d99e63(
    *,
    repository_base: builtins.str,
    repository_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a07a61e91481a6b576b846227e88a00d91917819dcfd0b0d8327225ef30cd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71560d243ed7a8aed1a646a375172d987be4b26ab4d10777ff8e70e297cb153b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92be8249b7803056c69d6384bf30dd9f6050abf802728aa51c7bb722f28f18c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df82d7514ab8a0c3f199338399c2299520bab434b2beff38020bfb410979c41(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd01b487dac2973583cf329020200c4ef67329b71a82f8ebc57b732d716f9333(
    *,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9281b2802fca4fd2e4e25b661370edab87a3c7da246c8527a6c92c02e0d1f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187051c167ed5eeae51e16b685aa935d1e24b595393c8e5006f33d0be6fb591e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a1e74f0a786b2d3d7137497fe7d8a2b4e34c914a27357e9bd33e7733fab67a(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigCommonRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397f2d79a97ae68da0790d57673a03814fd0461db9af716c54dd50bfef356c58(
    *,
    custom_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    public_repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b16525efc386cadeefd4fd6c915f33186054d788d9ff3ec7317233513998c0(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d92f6316f9657e74671f5759e3a882b6ca30ae4a518ba8cda8f6f6704a5c466(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1519864aa5fcac3629f3de8981c5f8d90b9f9203261f9c98f2fa4a8998dd2a33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281b80fc471796de4e2f9f83644a82bedfcbeb5ede0d8b7143bb73a43456de03(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryCustomRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb18bc31ba8a67f06f888e52d0abcac0b7f2849eb3fb0820ca336eed3e5ff0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd180a4f130999861b9c80b55a82803cd7b6cc9c649412cf7396f3c9b296232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c7ca8b2e52f3ee8dfe0871595bd317928ff86f260843925bc60f9706519aee(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba38fdee2f2ce5531e776ee3b15dda1479027e1355ba0e50d6c99da468d0adf2(
    *,
    custom_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    public_repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb29ac1a7c2d7fec784586db5b46afe0e7d668a19a3924c00bfae565c45526c(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777e8f9e7c3e6a93e362a08cd4d597c63769946aa69eeeb1547367e209a1a0a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd3998696470e26ba7e74943855059ef50b94f080f9a8b18fc592af7c21c6e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f71b79d77d41bca15fe768cc9c2c50f81127afeaa7c02d1fcb080b6db6755e(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryCustomRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0beed1640c17c515e7d2b326ead966ae9b114b1b5020f9ce3a1701856ca967(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15edb506c93bf8df67f6bd145fd0a3c4e8931fb25143e38292853e38cffb12d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0967229979d8b24a2c27058db22fb49edcf98238452786dc6c4b643d6e251199(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da84ff59d29f822b2ecd0f03ece2cce30e5572ee6a0e4f053a8b8fc4543eed8e(
    *,
    custom_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    public_repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74fa4e0a6576d27a751c9c7231762931fbb052c51975605974b628483c35c98(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cccc4b5030a0923fa86c1c3ae9699c0627b2478dc2d4ebb28036dd08d627a34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd23bc231343654724dde51264ee81ec04e448be732e4b450c331368b8b5b3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f0b8d3821f802437289d94d132d7b7798c0f93840615cc65743ff0277e2b95(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryCustomRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7d1d42db8b2cbc416852b144f3b51935b5a02d2a35b43c49ba723d8449cc97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d88a5f4effea9d3ed0c4db80cfe8cbd1db8ec5148675ceec8b9d909abcfbfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04d62d80a238b32126a9986d2e62e97475407018d15b73f88ddea3a313ca739(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b263eb93494647a7ef5a05f1542d8dc0c2ef71516a22738794e56db676bc4ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1afb8b15d0d3fcc2add65376ff228e8a4335ba93e34ce821e01bc8255b34b217(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388d7b4f6f6b4ff40a2c90e4e8106ccdc53eb5d177445f8e115f4f8a938a3868(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__335e955d30d46bab332ba5170d3d45dacf675c50c7fb336b5003e7f48d39d827(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def391e54a01e3f1db2cd742e8080c422019f6227a3674080966e314acde5fc2(
    *,
    custom_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    public_repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e3d977a5465eb2ba9661712a78ddc58e3c55562e1ca0bec537dd7e7437dafa(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d0571e8e5e91b976ac2c8fcb1b87d8e37ebd3858306db3e1a71b66e2270c6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2676708d572e81b6ed1cef789ba90142f47f234fe3f2d677321a6d76199acad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d6b08bb2e66304553a331c4ee05c58e49d70bfaa52b45d6a57c35ce5d725c0(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryCustomRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70ac559643c59ff67274cfd635c7635237d98d75b7d6501734ea78874ed7fc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714b00dcb034202919373219bac95b7e2c0d7bc93e65bb2f04899afa5af48512(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee424b93b167760573681b792df9ebd73f4b0f9b62314ac6aabf32f251937da(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed9800845a0e580c9c5c7904c5ead630b6597168e50fb7e6ef69e15062ddd7a(
    *,
    username_password_credentials: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e269fe61f8e75009f7599e887af02e977bd0630f442113057cbf7889d7c5892(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f3c2756937b6e8c73ab6c2e95de186e66a10c1ce90216a14456c1ccd8d7096(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35ddbbca97dabcdbdf6bad4c027bc435662e6b9dfdb4e52a5fa396d2706f038(
    *,
    password_secret_version: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626adf17d3c586e645da019a654cd00657ce54d04a299c36d0cac4cfd20515b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a42b073587a000c789091b5d3f388b93203edbbdda954cdfd00001b3fad9f463(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fcd89f1f11002e0d296f740be097ba25023d46e18045e9fe3e3efa8c87c4218(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4308234ff03b2fdb657f6846dfd76214c46a97b42839fd5bad8c34494f52522(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigUpstreamCredentialsUsernamePasswordCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0325bb5263fbf3dd1c49906424438086b215785501498497e43318f82e268502(
    *,
    public_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a679b7385c63e61781d5ba83d69f83403e966957e55e74b4b95d6f7924417e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795c783ef1a61c13463d176923e925a389ed5535752ba0b92833d82eda9c2a78(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6917a87e677c8afb340d0ae49a5a195f0973b54c79d23dddcd6e886b50d376c3(
    *,
    repository_base: builtins.str,
    repository_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb17542fcbef07b7b65e243e58c5a1d610542508aa99afe4e8d5d813ceae497a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bc36ee6ab3fdbfee0513aa8c24c128a8fb26ef0024e75b9b0e08c8a9564b9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c74e19a498de2e28d1ef89880839d03d47e506a34485b0015961b9221eddf64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8b46f624277ac3b2ab3654bcf833d876c15ae525ba527605900e6cbcb1f16f(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1444b73787658b044250e4edc0ea20b21f736e87083196f04e2556bd8d5c677(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26dca7d4ae65a212ede6de83a10f5b14116f2ef75ae17d92d4dc4ffcbf2041b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d69747494000d92dc610c0eb0b57f4f3780e477255afe36ff5a0cd11cce934(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12da1b37cbf109ef1a6a64d699ba5db80deefea61cce62b902f5ae18b40daff4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0cc863215ef4932536d9da06d0ed0c5b214ee89661ea8cce078c9f5a2e0e4c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f058e316f09dc0fe291c88f34ed01a42fd5633e01df8fcea67d75b0dc864c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9906605cc83e6b5985e1d336201586b3acd778608ed073fb5afa738b5022e4(
    *,
    upstream_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b803975416b5f5d0bbc8f707317eb0ff6359f28a275081d3886f1f37207faf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7211658b6ca71f47ae5d894f55cf62b3ea4ea89908d146f41431f5704f78721c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2978abcfb56761c7ca06f7d4bb7b8a69988573a61452d5be424a6ba4c7b6dc(
    value: typing.Optional[ArtifactRegistryRepositoryVirtualRepositoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24574f713916965d204fbfe34b4a654ef0a2934d7c3cb3289365c70299081c42(
    *,
    id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a874ecabc5dd02ac4c4eaaf4bce7f7e04b7ba5d0f78e84768ed764cc25f4c872(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1660bf1a29276e875a1184bd44330514a93aa5de00ea61eeee47476691977bc0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c128da1866b80bc63bc8ad24783e82f9af92fc054f65f655ef5c1cec8620e28e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2300e1fe2ee0d0faf4882c8e5e4dfc1802b070ccfde75d4e486342d527a6ae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1aaf8cd690ebf63ed3b7f970c37841227c1a03318793e73bd3827602c1bf92(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab2f3301b37bfe8f891fb8408c56769a27b373f5934dcc3f55706fe9da1eda7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61231823d0d4f3f09e5cb548418febd034e0d518e95a60b8eeddf4c4e5fa109(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f396c652930778d5065441f65480c08523b5586baeb544a5065bcaa50714b34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d715394ad5be31535b01945855216ddeed98cc338263cfcd56fba9154146479(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d0df23a58c6aa0e390bde702de297c92176603d8599f4831b0a801d73ff0ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1951af240571932f728b60aafb545caa1f7bf153c615f505418c2221cd6bc7eb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e919ba847c20b4a9df6715848609ca8a5284a45ab68dbcd38f15b80709c0051(
    *,
    enablement_config: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0651179996c574010d059a6848493258b61dfc106f60100742ad5a30e1b54f7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a264f906bb270fe3ca5548439cfce4c17e27b98adbd7c1e95404b6cda382f5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47609a628ee33142d3452b7debdf2fcb68d5f82d609a0022411a96799e59bf90(
    value: typing.Optional[ArtifactRegistryRepositoryVulnerabilityScanningConfig],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `google_secret_manager_secret`

Refer to the Terraform Registry for docs: [`google_secret_manager_secret`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret).
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


class SecretManagerSecret(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecret",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret google_secret_manager_secret}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        replication: typing.Union["SecretManagerSecretReplication", typing.Dict[builtins.str, typing.Any]],
        secret_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expire_time: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        rotation: typing.Optional[typing.Union["SecretManagerSecretRotation", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SecretManagerSecretTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        topics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecretManagerSecretTopics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ttl: typing.Optional[builtins.str] = None,
        version_aliases: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        version_destroy_ttl: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret google_secret_manager_secret} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param replication: replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#replication SecretManagerSecret#replication}
        :param secret_id: This must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#secret_id SecretManagerSecret#secret_id}
        :param annotations: Custom metadata about the secret. Annotations are distinct from various forms of labels. Annotations exist to allow client tools to store their own state information without requiring a database. Annotation keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, begin and end with an alphanumeric character ([a-z0-9A-Z]), and may have dashes (-), underscores (_), dots (.), and alphanumerics in between these symbols. The total size of annotation keys and values must be less than 16KiB. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#annotations SecretManagerSecret#annotations}
        :param deletion_protection: Whether Terraform will be prevented from destroying the secret. Defaults to false. When the field is set to true in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the secret will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#deletion_protection SecretManagerSecret#deletion_protection}
        :param expire_time: Timestamp in UTC when the Secret is scheduled to expire. This is always provided on output, regardless of what was sent on input. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Only one of 'expire_time' or 'ttl' can be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#expire_time SecretManagerSecret#expire_time}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#id SecretManagerSecret#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels assigned to this Secret. Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}_-]{0,62} Label values must be between 0 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}_-]{0,63} No more than 64 labels can be assigned to a given resource. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#labels SecretManagerSecret#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#project SecretManagerSecret#project}.
        :param rotation: rotation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#rotation SecretManagerSecret#rotation}
        :param tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/{tag_value_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#tags SecretManagerSecret#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#timeouts SecretManagerSecret#timeouts}
        :param topics: topics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#topics SecretManagerSecret#topics}
        :param ttl: The TTL for the Secret. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Only one of 'ttl' or 'expire_time' can be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#ttl SecretManagerSecret#ttl}
        :param version_aliases: Mapping from version alias to version name. A version alias is a string with a maximum length of 63 characters and can contain uppercase and lowercase letters, numerals, and the hyphen (-) and underscore ('_') characters. An alias string must start with a letter and cannot be the string 'latest' or 'NEW'. No more than 50 aliases can be assigned to a given secret. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#version_aliases SecretManagerSecret#version_aliases}
        :param version_destroy_ttl: Secret Version TTL after destruction request. This is a part of the delayed delete feature on Secret Version. For secret with versionDestroyTtl>0, version destruction doesn't happen immediately on calling destroy instead the version goes to a disabled state and the actual destruction happens after this TTL expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#version_destroy_ttl SecretManagerSecret#version_destroy_ttl}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7375bebac0ff4e7082aec76eb7e9be7da9c8606210bdad09a93c8c5a65ec7a7f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SecretManagerSecretConfig(
            replication=replication,
            secret_id=secret_id,
            annotations=annotations,
            deletion_protection=deletion_protection,
            expire_time=expire_time,
            id=id,
            labels=labels,
            project=project,
            rotation=rotation,
            tags=tags,
            timeouts=timeouts,
            topics=topics,
            ttl=ttl,
            version_aliases=version_aliases,
            version_destroy_ttl=version_destroy_ttl,
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
        '''Generates CDKTF code for importing a SecretManagerSecret resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SecretManagerSecret to import.
        :param import_from_id: The id of the existing SecretManagerSecret that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SecretManagerSecret to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf40712bced892d6d3c293ce9d8e19b2017770392c2cf6a66819356111cd438)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putReplication")
    def put_replication(
        self,
        *,
        auto: typing.Optional[typing.Union["SecretManagerSecretReplicationAuto", typing.Dict[builtins.str, typing.Any]]] = None,
        user_managed: typing.Optional[typing.Union["SecretManagerSecretReplicationUserManaged", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto: auto block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#auto SecretManagerSecret#auto}
        :param user_managed: user_managed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#user_managed SecretManagerSecret#user_managed}
        '''
        value = SecretManagerSecretReplication(auto=auto, user_managed=user_managed)

        return typing.cast(None, jsii.invoke(self, "putReplication", [value]))

    @jsii.member(jsii_name="putRotation")
    def put_rotation(
        self,
        *,
        next_rotation_time: typing.Optional[builtins.str] = None,
        rotation_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param next_rotation_time: Timestamp in UTC at which the Secret is scheduled to rotate. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#next_rotation_time SecretManagerSecret#next_rotation_time}
        :param rotation_period: The Duration between rotation notifications. Must be in seconds and at least 3600s (1h) and at most 3153600000s (100 years). If rotationPeriod is set, 'next_rotation_time' must be set. 'next_rotation_time' will be advanced by this period when the service automatically sends rotation notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#rotation_period SecretManagerSecret#rotation_period}
        '''
        value = SecretManagerSecretRotation(
            next_rotation_time=next_rotation_time, rotation_period=rotation_period
        )

        return typing.cast(None, jsii.invoke(self, "putRotation", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#create SecretManagerSecret#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#delete SecretManagerSecret#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#update SecretManagerSecret#update}.
        '''
        value = SecretManagerSecretTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTopics")
    def put_topics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecretManagerSecretTopics", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d87c8d901c6ada177ce865658fcfd459da74a0943b72318455764f9d8e17da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTopics", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetExpireTime")
    def reset_expire_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpireTime", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRotation")
    def reset_rotation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRotation", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTopics")
    def reset_topics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopics", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

    @jsii.member(jsii_name="resetVersionAliases")
    def reset_version_aliases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionAliases", []))

    @jsii.member(jsii_name="resetVersionDestroyTtl")
    def reset_version_destroy_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionDestroyTtl", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="replication")
    def replication(self) -> "SecretManagerSecretReplicationOutputReference":
        return typing.cast("SecretManagerSecretReplicationOutputReference", jsii.get(self, "replication"))

    @builtins.property
    @jsii.member(jsii_name="rotation")
    def rotation(self) -> "SecretManagerSecretRotationOutputReference":
        return typing.cast("SecretManagerSecretRotationOutputReference", jsii.get(self, "rotation"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SecretManagerSecretTimeoutsOutputReference":
        return typing.cast("SecretManagerSecretTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(self) -> "SecretManagerSecretTopicsList":
        return typing.cast("SecretManagerSecretTopicsList", jsii.get(self, "topics"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="expireTimeInput")
    def expire_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expireTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationInput")
    def replication_input(self) -> typing.Optional["SecretManagerSecretReplication"]:
        return typing.cast(typing.Optional["SecretManagerSecretReplication"], jsii.get(self, "replicationInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationInput")
    def rotation_input(self) -> typing.Optional["SecretManagerSecretRotation"]:
        return typing.cast(typing.Optional["SecretManagerSecretRotation"], jsii.get(self, "rotationInput"))

    @builtins.property
    @jsii.member(jsii_name="secretIdInput")
    def secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SecretManagerSecretTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SecretManagerSecretTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="topicsInput")
    def topics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecretManagerSecretTopics"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecretManagerSecretTopics"]]], jsii.get(self, "topicsInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="versionAliasesInput")
    def version_aliases_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "versionAliasesInput"))

    @builtins.property
    @jsii.member(jsii_name="versionDestroyTtlInput")
    def version_destroy_ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionDestroyTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e96cf88b6a30f97b80a72b3b4469029f9fd4d16b6024b152349b07378a2c136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d274497e4763530e240b24454eae969238d52dee269bd080d76f2235860df42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expireTime")
    def expire_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireTime"))

    @expire_time.setter
    def expire_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f1a53af1f82c7d5e6f0845e9f95ebf1c803cc28f3630bed78ee6a80778395e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expireTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7cd6e8cf2153e93f020436e599266ef1667a989aa27940c38a0bf3458329b8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34df967f1497850931f5c1793d46cf7293b0a031bfdbeccb9f2dbc7d18ff72d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d9660c7c7dec736dbc62d0785748e1982cb1ea63d8df861415703e498f9d0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretId"))

    @secret_id.setter
    def secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e529b1c0b146e52023631910baed36b8e2a73132091fecc4093d43f9bec5a21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f5d8a6710fc15d9d3b48e64b86ccfeffff4e4dad6c98da6a6e50290f2cd22d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07df02dd866eb7d8542b6bc6bf1fe9c526dacb9ae818176d00b170d335377795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionAliases")
    def version_aliases(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "versionAliases"))

    @version_aliases.setter
    def version_aliases(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9fa8eb89cc0c3d71779a881d774ea4146634b7fd78b802381e1b0905a5945d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionAliases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionDestroyTtl")
    def version_destroy_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionDestroyTtl"))

    @version_destroy_ttl.setter
    def version_destroy_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9a9cf923d7ef5522ba8fd00dd9a669d6063739994ff70a4d1b2cd81c2ff29e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionDestroyTtl", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "replication": "replication",
        "secret_id": "secretId",
        "annotations": "annotations",
        "deletion_protection": "deletionProtection",
        "expire_time": "expireTime",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "rotation": "rotation",
        "tags": "tags",
        "timeouts": "timeouts",
        "topics": "topics",
        "ttl": "ttl",
        "version_aliases": "versionAliases",
        "version_destroy_ttl": "versionDestroyTtl",
    },
)
class SecretManagerSecretConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        replication: typing.Union["SecretManagerSecretReplication", typing.Dict[builtins.str, typing.Any]],
        secret_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expire_time: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        rotation: typing.Optional[typing.Union["SecretManagerSecretRotation", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SecretManagerSecretTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        topics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecretManagerSecretTopics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ttl: typing.Optional[builtins.str] = None,
        version_aliases: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        version_destroy_ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param replication: replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#replication SecretManagerSecret#replication}
        :param secret_id: This must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#secret_id SecretManagerSecret#secret_id}
        :param annotations: Custom metadata about the secret. Annotations are distinct from various forms of labels. Annotations exist to allow client tools to store their own state information without requiring a database. Annotation keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, begin and end with an alphanumeric character ([a-z0-9A-Z]), and may have dashes (-), underscores (_), dots (.), and alphanumerics in between these symbols. The total size of annotation keys and values must be less than 16KiB. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#annotations SecretManagerSecret#annotations}
        :param deletion_protection: Whether Terraform will be prevented from destroying the secret. Defaults to false. When the field is set to true in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the secret will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#deletion_protection SecretManagerSecret#deletion_protection}
        :param expire_time: Timestamp in UTC when the Secret is scheduled to expire. This is always provided on output, regardless of what was sent on input. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Only one of 'expire_time' or 'ttl' can be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#expire_time SecretManagerSecret#expire_time}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#id SecretManagerSecret#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels assigned to this Secret. Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}_-]{0,62} Label values must be between 0 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}_-]{0,63} No more than 64 labels can be assigned to a given resource. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#labels SecretManagerSecret#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#project SecretManagerSecret#project}.
        :param rotation: rotation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#rotation SecretManagerSecret#rotation}
        :param tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/{tag_value_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#tags SecretManagerSecret#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#timeouts SecretManagerSecret#timeouts}
        :param topics: topics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#topics SecretManagerSecret#topics}
        :param ttl: The TTL for the Secret. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Only one of 'ttl' or 'expire_time' can be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#ttl SecretManagerSecret#ttl}
        :param version_aliases: Mapping from version alias to version name. A version alias is a string with a maximum length of 63 characters and can contain uppercase and lowercase letters, numerals, and the hyphen (-) and underscore ('_') characters. An alias string must start with a letter and cannot be the string 'latest' or 'NEW'. No more than 50 aliases can be assigned to a given secret. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#version_aliases SecretManagerSecret#version_aliases}
        :param version_destroy_ttl: Secret Version TTL after destruction request. This is a part of the delayed delete feature on Secret Version. For secret with versionDestroyTtl>0, version destruction doesn't happen immediately on calling destroy instead the version goes to a disabled state and the actual destruction happens after this TTL expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#version_destroy_ttl SecretManagerSecret#version_destroy_ttl}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(replication, dict):
            replication = SecretManagerSecretReplication(**replication)
        if isinstance(rotation, dict):
            rotation = SecretManagerSecretRotation(**rotation)
        if isinstance(timeouts, dict):
            timeouts = SecretManagerSecretTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__349c1c7af03e290e0199f9611b9200a2c6e3cbed766ff8c2d8118e2f09204a4e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument replication", value=replication, expected_type=type_hints["replication"])
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument expire_time", value=expire_time, expected_type=type_hints["expire_time"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument rotation", value=rotation, expected_type=type_hints["rotation"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument topics", value=topics, expected_type=type_hints["topics"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            check_type(argname="argument version_aliases", value=version_aliases, expected_type=type_hints["version_aliases"])
            check_type(argname="argument version_destroy_ttl", value=version_destroy_ttl, expected_type=type_hints["version_destroy_ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "replication": replication,
            "secret_id": secret_id,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if expire_time is not None:
            self._values["expire_time"] = expire_time
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if rotation is not None:
            self._values["rotation"] = rotation
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if topics is not None:
            self._values["topics"] = topics
        if ttl is not None:
            self._values["ttl"] = ttl
        if version_aliases is not None:
            self._values["version_aliases"] = version_aliases
        if version_destroy_ttl is not None:
            self._values["version_destroy_ttl"] = version_destroy_ttl

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
    def replication(self) -> "SecretManagerSecretReplication":
        '''replication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#replication SecretManagerSecret#replication}
        '''
        result = self._values.get("replication")
        assert result is not None, "Required property 'replication' is missing"
        return typing.cast("SecretManagerSecretReplication", result)

    @builtins.property
    def secret_id(self) -> builtins.str:
        '''This must be unique within the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#secret_id SecretManagerSecret#secret_id}
        '''
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom metadata about the secret.

        Annotations are distinct from various forms of labels. Annotations exist to allow
        client tools to store their own state information without requiring a database.

        Annotation keys must be between 1 and 63 characters long, have a UTF-8 encoding of
        maximum 128 bytes, begin and end with an alphanumeric character ([a-z0-9A-Z]), and
        may have dashes (-), underscores (_), dots (.), and alphanumerics in between these
        symbols.

        The total size of annotation keys and values must be less than 16KiB.

        An object containing a list of "key": value pairs. Example:
        { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#annotations SecretManagerSecret#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Terraform will be prevented from destroying the secret.

        Defaults to false.
        When the field is set to true in Terraform state, a 'terraform apply'
        or 'terraform destroy' that would delete the secret will fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#deletion_protection SecretManagerSecret#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expire_time(self) -> typing.Optional[builtins.str]:
        '''Timestamp in UTC when the Secret is scheduled to expire.

        This is always provided on output, regardless of what was sent on input.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        Only one of 'expire_time' or 'ttl' can be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#expire_time SecretManagerSecret#expire_time}
        '''
        result = self._values.get("expire_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#id SecretManagerSecret#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels assigned to this Secret.

        Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes,
        and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}_-]{0,62}

        Label values must be between 0 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes,
        and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}_-]{0,63}

        No more than 64 labels can be assigned to a given resource.

        An object containing a list of "key": value pairs. Example:
        { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#labels SecretManagerSecret#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#project SecretManagerSecret#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotation(self) -> typing.Optional["SecretManagerSecretRotation"]:
        '''rotation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#rotation SecretManagerSecret#rotation}
        '''
        result = self._values.get("rotation")
        return typing.cast(typing.Optional["SecretManagerSecretRotation"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of resource manager tags.

        Resource manager tag keys and values have the same definition as resource manager tags.
        Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/{tag_value_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#tags SecretManagerSecret#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SecretManagerSecretTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#timeouts SecretManagerSecret#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SecretManagerSecretTimeouts"], result)

    @builtins.property
    def topics(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecretManagerSecretTopics"]]]:
        '''topics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#topics SecretManagerSecret#topics}
        '''
        result = self._values.get("topics")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecretManagerSecretTopics"]]], result)

    @builtins.property
    def ttl(self) -> typing.Optional[builtins.str]:
        '''The TTL for the Secret.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".
        Only one of 'ttl' or 'expire_time' can be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#ttl SecretManagerSecret#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_aliases(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Mapping from version alias to version name.

        A version alias is a string with a maximum length of 63 characters and can contain
        uppercase and lowercase letters, numerals, and the hyphen (-) and underscore ('_')
        characters. An alias string must start with a letter and cannot be the string
        'latest' or 'NEW'. No more than 50 aliases can be assigned to a given secret.

        An object containing a list of "key": value pairs. Example:
        { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#version_aliases SecretManagerSecret#version_aliases}
        '''
        result = self._values.get("version_aliases")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def version_destroy_ttl(self) -> typing.Optional[builtins.str]:
        '''Secret Version TTL after destruction request.

        This is a part of the delayed delete feature on Secret Version.
        For secret with versionDestroyTtl>0, version destruction doesn't happen immediately
        on calling destroy instead the version goes to a disabled state and
        the actual destruction happens after this TTL expires.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#version_destroy_ttl SecretManagerSecret#version_destroy_ttl}
        '''
        result = self._values.get("version_destroy_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretManagerSecretConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretReplication",
    jsii_struct_bases=[],
    name_mapping={"auto": "auto", "user_managed": "userManaged"},
)
class SecretManagerSecretReplication:
    def __init__(
        self,
        *,
        auto: typing.Optional[typing.Union["SecretManagerSecretReplicationAuto", typing.Dict[builtins.str, typing.Any]]] = None,
        user_managed: typing.Optional[typing.Union["SecretManagerSecretReplicationUserManaged", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto: auto block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#auto SecretManagerSecret#auto}
        :param user_managed: user_managed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#user_managed SecretManagerSecret#user_managed}
        '''
        if isinstance(auto, dict):
            auto = SecretManagerSecretReplicationAuto(**auto)
        if isinstance(user_managed, dict):
            user_managed = SecretManagerSecretReplicationUserManaged(**user_managed)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea4728d3a9c1870cd1db2de5b385f301b1697b9f4cae65f99938aae95330a68)
            check_type(argname="argument auto", value=auto, expected_type=type_hints["auto"])
            check_type(argname="argument user_managed", value=user_managed, expected_type=type_hints["user_managed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto is not None:
            self._values["auto"] = auto
        if user_managed is not None:
            self._values["user_managed"] = user_managed

    @builtins.property
    def auto(self) -> typing.Optional["SecretManagerSecretReplicationAuto"]:
        '''auto block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#auto SecretManagerSecret#auto}
        '''
        result = self._values.get("auto")
        return typing.cast(typing.Optional["SecretManagerSecretReplicationAuto"], result)

    @builtins.property
    def user_managed(
        self,
    ) -> typing.Optional["SecretManagerSecretReplicationUserManaged"]:
        '''user_managed block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#user_managed SecretManagerSecret#user_managed}
        '''
        result = self._values.get("user_managed")
        return typing.cast(typing.Optional["SecretManagerSecretReplicationUserManaged"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretManagerSecretReplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretReplicationAuto",
    jsii_struct_bases=[],
    name_mapping={"customer_managed_encryption": "customerManagedEncryption"},
)
class SecretManagerSecretReplicationAuto:
    def __init__(
        self,
        *,
        customer_managed_encryption: typing.Optional[typing.Union["SecretManagerSecretReplicationAutoCustomerManagedEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param customer_managed_encryption: customer_managed_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#customer_managed_encryption SecretManagerSecret#customer_managed_encryption}
        '''
        if isinstance(customer_managed_encryption, dict):
            customer_managed_encryption = SecretManagerSecretReplicationAutoCustomerManagedEncryption(**customer_managed_encryption)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe34db67d0755a35a2adc1d64864e2959c352d46ae3f51dd5aaae50b14a496ef)
            check_type(argname="argument customer_managed_encryption", value=customer_managed_encryption, expected_type=type_hints["customer_managed_encryption"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if customer_managed_encryption is not None:
            self._values["customer_managed_encryption"] = customer_managed_encryption

    @builtins.property
    def customer_managed_encryption(
        self,
    ) -> typing.Optional["SecretManagerSecretReplicationAutoCustomerManagedEncryption"]:
        '''customer_managed_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#customer_managed_encryption SecretManagerSecret#customer_managed_encryption}
        '''
        result = self._values.get("customer_managed_encryption")
        return typing.cast(typing.Optional["SecretManagerSecretReplicationAutoCustomerManagedEncryption"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretManagerSecretReplicationAuto(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretReplicationAutoCustomerManagedEncryption",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class SecretManagerSecretReplicationAutoCustomerManagedEncryption:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The resource name of the Cloud KMS CryptoKey used to encrypt secret payloads. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#kms_key_name SecretManagerSecret#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9c77c38667b06da814d54099bd223d8293e334b4d68cf66ddb1ae240117cb5)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''The resource name of the Cloud KMS CryptoKey used to encrypt secret payloads.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#kms_key_name SecretManagerSecret#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretManagerSecretReplicationAutoCustomerManagedEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecretManagerSecretReplicationAutoCustomerManagedEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretReplicationAutoCustomerManagedEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e595bef2797e8bd96ab39770283e6cb463b44a60c2e5ee83fece243bf28069a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880dd3f9c6cdb453d53bbd96e781bc1735b62b265cc20698d8c4c7dca1044a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecretManagerSecretReplicationAutoCustomerManagedEncryption]:
        return typing.cast(typing.Optional[SecretManagerSecretReplicationAutoCustomerManagedEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecretManagerSecretReplicationAutoCustomerManagedEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ca205ac74fc4380a9cb89fbf507ef9268674f9c083b8977e92e8a10856ce04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecretManagerSecretReplicationAutoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretReplicationAutoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73f118bc4ec42d29a1700b8556f2d10a8d2e776c8a168860b02cfe9e435f0cd6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomerManagedEncryption")
    def put_customer_managed_encryption(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The resource name of the Cloud KMS CryptoKey used to encrypt secret payloads. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#kms_key_name SecretManagerSecret#kms_key_name}
        '''
        value = SecretManagerSecretReplicationAutoCustomerManagedEncryption(
            kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putCustomerManagedEncryption", [value]))

    @jsii.member(jsii_name="resetCustomerManagedEncryption")
    def reset_customer_managed_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerManagedEncryption", []))

    @builtins.property
    @jsii.member(jsii_name="customerManagedEncryption")
    def customer_managed_encryption(
        self,
    ) -> SecretManagerSecretReplicationAutoCustomerManagedEncryptionOutputReference:
        return typing.cast(SecretManagerSecretReplicationAutoCustomerManagedEncryptionOutputReference, jsii.get(self, "customerManagedEncryption"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedEncryptionInput")
    def customer_managed_encryption_input(
        self,
    ) -> typing.Optional[SecretManagerSecretReplicationAutoCustomerManagedEncryption]:
        return typing.cast(typing.Optional[SecretManagerSecretReplicationAutoCustomerManagedEncryption], jsii.get(self, "customerManagedEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SecretManagerSecretReplicationAuto]:
        return typing.cast(typing.Optional[SecretManagerSecretReplicationAuto], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecretManagerSecretReplicationAuto],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81c379b666c82d11c72551bcde922b316c18ac4b5d800c61a173e46bc2c54ca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecretManagerSecretReplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretReplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc8ed8ff8d88a340abd25b621f5e0f938cea9b06a78686380aa9eb9ea5172ca7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuto")
    def put_auto(
        self,
        *,
        customer_managed_encryption: typing.Optional[typing.Union[SecretManagerSecretReplicationAutoCustomerManagedEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param customer_managed_encryption: customer_managed_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#customer_managed_encryption SecretManagerSecret#customer_managed_encryption}
        '''
        value = SecretManagerSecretReplicationAuto(
            customer_managed_encryption=customer_managed_encryption
        )

        return typing.cast(None, jsii.invoke(self, "putAuto", [value]))

    @jsii.member(jsii_name="putUserManaged")
    def put_user_managed(
        self,
        *,
        replicas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecretManagerSecretReplicationUserManagedReplicas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param replicas: replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#replicas SecretManagerSecret#replicas}
        '''
        value = SecretManagerSecretReplicationUserManaged(replicas=replicas)

        return typing.cast(None, jsii.invoke(self, "putUserManaged", [value]))

    @jsii.member(jsii_name="resetAuto")
    def reset_auto(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuto", []))

    @jsii.member(jsii_name="resetUserManaged")
    def reset_user_managed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserManaged", []))

    @builtins.property
    @jsii.member(jsii_name="auto")
    def auto(self) -> SecretManagerSecretReplicationAutoOutputReference:
        return typing.cast(SecretManagerSecretReplicationAutoOutputReference, jsii.get(self, "auto"))

    @builtins.property
    @jsii.member(jsii_name="userManaged")
    def user_managed(
        self,
    ) -> "SecretManagerSecretReplicationUserManagedOutputReference":
        return typing.cast("SecretManagerSecretReplicationUserManagedOutputReference", jsii.get(self, "userManaged"))

    @builtins.property
    @jsii.member(jsii_name="autoInput")
    def auto_input(self) -> typing.Optional[SecretManagerSecretReplicationAuto]:
        return typing.cast(typing.Optional[SecretManagerSecretReplicationAuto], jsii.get(self, "autoInput"))

    @builtins.property
    @jsii.member(jsii_name="userManagedInput")
    def user_managed_input(
        self,
    ) -> typing.Optional["SecretManagerSecretReplicationUserManaged"]:
        return typing.cast(typing.Optional["SecretManagerSecretReplicationUserManaged"], jsii.get(self, "userManagedInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SecretManagerSecretReplication]:
        return typing.cast(typing.Optional[SecretManagerSecretReplication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecretManagerSecretReplication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d319f5f8052b3a794e12709c14b1d9721cfa593a383fa479f34acc8eda5744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretReplicationUserManaged",
    jsii_struct_bases=[],
    name_mapping={"replicas": "replicas"},
)
class SecretManagerSecretReplicationUserManaged:
    def __init__(
        self,
        *,
        replicas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecretManagerSecretReplicationUserManagedReplicas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param replicas: replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#replicas SecretManagerSecret#replicas}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b26809d69924e0619aab37bbdd46699e98bc29d7d9ebcd7dbdc63c551a1149)
            check_type(argname="argument replicas", value=replicas, expected_type=type_hints["replicas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "replicas": replicas,
        }

    @builtins.property
    def replicas(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecretManagerSecretReplicationUserManagedReplicas"]]:
        '''replicas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#replicas SecretManagerSecret#replicas}
        '''
        result = self._values.get("replicas")
        assert result is not None, "Required property 'replicas' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecretManagerSecretReplicationUserManagedReplicas"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretManagerSecretReplicationUserManaged(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecretManagerSecretReplicationUserManagedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretReplicationUserManagedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b16dfd09ec907c4fa32f74ac4d10248ec7a076931048654bbde10e1f4612f9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putReplicas")
    def put_replicas(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecretManagerSecretReplicationUserManagedReplicas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e921d25d51ebff6811d9fcae2b535aeadf6861462f6d030405cdbc072f4f7445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putReplicas", [value]))

    @builtins.property
    @jsii.member(jsii_name="replicas")
    def replicas(self) -> "SecretManagerSecretReplicationUserManagedReplicasList":
        return typing.cast("SecretManagerSecretReplicationUserManagedReplicasList", jsii.get(self, "replicas"))

    @builtins.property
    @jsii.member(jsii_name="replicasInput")
    def replicas_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecretManagerSecretReplicationUserManagedReplicas"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecretManagerSecretReplicationUserManagedReplicas"]]], jsii.get(self, "replicasInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecretManagerSecretReplicationUserManaged]:
        return typing.cast(typing.Optional[SecretManagerSecretReplicationUserManaged], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecretManagerSecretReplicationUserManaged],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8e9325c95b9f5062bfdd59abdf18333161593fc3f853f4fe6583b666e7760b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretReplicationUserManagedReplicas",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "customer_managed_encryption": "customerManagedEncryption",
    },
)
class SecretManagerSecretReplicationUserManagedReplicas:
    def __init__(
        self,
        *,
        location: builtins.str,
        customer_managed_encryption: typing.Optional[typing.Union["SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param location: The canonical IDs of the location to replicate data. For example: "us-east1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#location SecretManagerSecret#location}
        :param customer_managed_encryption: customer_managed_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#customer_managed_encryption SecretManagerSecret#customer_managed_encryption}
        '''
        if isinstance(customer_managed_encryption, dict):
            customer_managed_encryption = SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption(**customer_managed_encryption)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf90430f1099a074d2d6ffe83f518516033c676e86c9c98f61287e808acf730)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument customer_managed_encryption", value=customer_managed_encryption, expected_type=type_hints["customer_managed_encryption"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
        }
        if customer_managed_encryption is not None:
            self._values["customer_managed_encryption"] = customer_managed_encryption

    @builtins.property
    def location(self) -> builtins.str:
        '''The canonical IDs of the location to replicate data. For example: "us-east1".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#location SecretManagerSecret#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def customer_managed_encryption(
        self,
    ) -> typing.Optional["SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption"]:
        '''customer_managed_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#customer_managed_encryption SecretManagerSecret#customer_managed_encryption}
        '''
        result = self._values.get("customer_managed_encryption")
        return typing.cast(typing.Optional["SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretManagerSecretReplicationUserManagedReplicas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: Describes the Cloud KMS encryption key that will be used to protect destination secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#kms_key_name SecretManagerSecret#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39ca7a21fdb4f5d2415ecb026dd1bdff5a80311ca9938697069934135428dca)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''Describes the Cloud KMS encryption key that will be used to protect destination secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#kms_key_name SecretManagerSecret#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69ebad0ae194a00d86e8d968fd6931562a2197c2c64cb03da5bfcac557a69ed1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14ea288972e9c9c0c8104ffb0c79fc01d909d51139e498c3ef0acb8bfe1a03c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption]:
        return typing.cast(typing.Optional[SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d81daf9b915df7e2eefed096c3fefef3a09867c6becb3ad97afe2572ff8bd68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecretManagerSecretReplicationUserManagedReplicasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretReplicationUserManagedReplicasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__415ce6447eeb1264afd875f76ee8f7be4f80b18e65de754a05931eaa82ebef3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecretManagerSecretReplicationUserManagedReplicasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d5df0f876bb243c629ff3dc3bed947ef780af90de5cb06a121b2efeed36770)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecretManagerSecretReplicationUserManagedReplicasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69ad8e5c1b1002a2c4cdfb63f559723bf02246761967b5d2735e292770730928)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c1d99ed39c2447dcc08ca8d0770812abc8ac8c086d67e7d9f9175dec8fb256e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__428842cc25ab0bbe3b3abed851a5acd29b8717642b44827daeff4eeae835c8f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecretManagerSecretReplicationUserManagedReplicas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecretManagerSecretReplicationUserManagedReplicas]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecretManagerSecretReplicationUserManagedReplicas]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55b49341b973f565880ea90c1311137bc5cf6cdd48e85908a075e066f870fb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecretManagerSecretReplicationUserManagedReplicasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretReplicationUserManagedReplicasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__832dab1249f7bc80f8f07632c59023f82a082f9cd072e76967e4be6202595913)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomerManagedEncryption")
    def put_customer_managed_encryption(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: Describes the Cloud KMS encryption key that will be used to protect destination secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#kms_key_name SecretManagerSecret#kms_key_name}
        '''
        value = SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption(
            kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putCustomerManagedEncryption", [value]))

    @jsii.member(jsii_name="resetCustomerManagedEncryption")
    def reset_customer_managed_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerManagedEncryption", []))

    @builtins.property
    @jsii.member(jsii_name="customerManagedEncryption")
    def customer_managed_encryption(
        self,
    ) -> SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryptionOutputReference:
        return typing.cast(SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryptionOutputReference, jsii.get(self, "customerManagedEncryption"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedEncryptionInput")
    def customer_managed_encryption_input(
        self,
    ) -> typing.Optional[SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption]:
        return typing.cast(typing.Optional[SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption], jsii.get(self, "customerManagedEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a72d7d18f59f08d7f65c8d4a17320dc31c53b4d71e13687d985490b182cafa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretReplicationUserManagedReplicas]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretReplicationUserManagedReplicas]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretReplicationUserManagedReplicas]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71236c2c279743f767b5e5d02765a1f7d9a27e7d3ba7f1cbf48ae211d3930a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretRotation",
    jsii_struct_bases=[],
    name_mapping={
        "next_rotation_time": "nextRotationTime",
        "rotation_period": "rotationPeriod",
    },
)
class SecretManagerSecretRotation:
    def __init__(
        self,
        *,
        next_rotation_time: typing.Optional[builtins.str] = None,
        rotation_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param next_rotation_time: Timestamp in UTC at which the Secret is scheduled to rotate. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#next_rotation_time SecretManagerSecret#next_rotation_time}
        :param rotation_period: The Duration between rotation notifications. Must be in seconds and at least 3600s (1h) and at most 3153600000s (100 years). If rotationPeriod is set, 'next_rotation_time' must be set. 'next_rotation_time' will be advanced by this period when the service automatically sends rotation notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#rotation_period SecretManagerSecret#rotation_period}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e0d39a618a8d890b47dddf51affdd0ad9e49a6bdd03ef1acba97523bb3a872)
            check_type(argname="argument next_rotation_time", value=next_rotation_time, expected_type=type_hints["next_rotation_time"])
            check_type(argname="argument rotation_period", value=rotation_period, expected_type=type_hints["rotation_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if next_rotation_time is not None:
            self._values["next_rotation_time"] = next_rotation_time
        if rotation_period is not None:
            self._values["rotation_period"] = rotation_period

    @builtins.property
    def next_rotation_time(self) -> typing.Optional[builtins.str]:
        '''Timestamp in UTC at which the Secret is scheduled to rotate.

        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#next_rotation_time SecretManagerSecret#next_rotation_time}
        '''
        result = self._values.get("next_rotation_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotation_period(self) -> typing.Optional[builtins.str]:
        '''The Duration between rotation notifications.

        Must be in seconds and at least 3600s (1h) and at most 3153600000s (100 years).
        If rotationPeriod is set, 'next_rotation_time' must be set. 'next_rotation_time' will be advanced by this period when the service automatically sends rotation notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#rotation_period SecretManagerSecret#rotation_period}
        '''
        result = self._values.get("rotation_period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretManagerSecretRotation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecretManagerSecretRotationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretRotationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed22b752a64f57264379f5bf3d7511c4e909c11cd5534e3fb0e67c0fc695f02b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNextRotationTime")
    def reset_next_rotation_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNextRotationTime", []))

    @jsii.member(jsii_name="resetRotationPeriod")
    def reset_rotation_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRotationPeriod", []))

    @builtins.property
    @jsii.member(jsii_name="nextRotationTimeInput")
    def next_rotation_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextRotationTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationPeriodInput")
    def rotation_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rotationPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="nextRotationTime")
    def next_rotation_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextRotationTime"))

    @next_rotation_time.setter
    def next_rotation_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721f52a7e1f85761398c6962da12440bd0905a3ab0711192f9b057f076cce674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextRotationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationPeriod")
    def rotation_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rotationPeriod"))

    @rotation_period.setter
    def rotation_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87327a6eac4bac4c6d02e8be96b88d285874b033a487d637f500c3cc3c231606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SecretManagerSecretRotation]:
        return typing.cast(typing.Optional[SecretManagerSecretRotation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecretManagerSecretRotation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d8c4e9faacdb113a632f5056a84a804c4dadb7482e593ad0504c6dd82b2dd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class SecretManagerSecretTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#create SecretManagerSecret#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#delete SecretManagerSecret#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#update SecretManagerSecret#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051f68fd5971a8a4f914f242270b4f0ed43104b6965780cde8de7dbf367c5220)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#create SecretManagerSecret#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#delete SecretManagerSecret#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#update SecretManagerSecret#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretManagerSecretTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecretManagerSecretTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a100a2587f640e96752d74786ee2fa1f26a67428b9f21e36ebd4b7905ecd3b02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fd0c45c782276210923dbb4047ca198a4096df1aabdd19baf265d5dae547829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4671d8fc71cdb8e4be2c6f959ee7a617fe5b8e2f4a946c88d0011f9017af7ddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d236e7051461c61763a414af7b9ff868548b7fb14ca4e8e7fe25f7187bff8bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353ec30785ac71a4f5a6a3065bcdd9573b69b318f2eb2c89482ffa1062b7a542)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretTopics",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class SecretManagerSecretTopics:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: The resource name of the Pub/Sub topic that will be published to, in the following format: projects/* /topics/*. For publication to succeed, the Secret Manager Service Agent service account must have pubsub.publisher permissions on the topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#name SecretManagerSecret#name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7436308881c7404d9ca38b164fb583b1085659a0c16c102c235404c1866b1b70)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name of the Pub/Sub topic that will be published to, in the following format: projects/* /topics/*.

        For publication to succeed, the Secret Manager Service Agent service account must have pubsub.publisher permissions on the topic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret#name SecretManagerSecret#name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretManagerSecretTopics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecretManagerSecretTopicsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretTopicsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a39a6edab10b98390b8f09e9844bf04f551a6e564cef6bdc6e1993f7e16b3467)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SecretManagerSecretTopicsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67fd56710108aac9428e3c9c23b01183bc8ed51edfecdb539b4382eec0ac236f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecretManagerSecretTopicsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5abdc63825e0e7944c9c5a3ae4371a1029d418540f431a5e32d80070145175f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3a165113c9ac428edbba077b8995d2f795029a600da573b327d5f06101039d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7028848230f5b1174e2262abebc36acbf40cab1fc88101e0139c8bfe409a1155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecretManagerSecretTopics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecretManagerSecretTopics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecretManagerSecretTopics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b4571ad10ce205c194fbe8014ffe89d6e99fe4a222ef8f853094aea22d6dcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecretManagerSecretTopicsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secretManagerSecret.SecretManagerSecretTopicsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b7c0a4a86486e8cbc23473892b1d7a8c940247fc3c7699c18fb45e4eb25cad6)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5d4cc6d838ba7c1f4ade151031abe74d28945ef5077588cc78ff6caee21875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretTopics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretTopics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretTopics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d2a279c855527e858864b4990baa95cda1678c2033a184d022f2e2e6888bd68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SecretManagerSecret",
    "SecretManagerSecretConfig",
    "SecretManagerSecretReplication",
    "SecretManagerSecretReplicationAuto",
    "SecretManagerSecretReplicationAutoCustomerManagedEncryption",
    "SecretManagerSecretReplicationAutoCustomerManagedEncryptionOutputReference",
    "SecretManagerSecretReplicationAutoOutputReference",
    "SecretManagerSecretReplicationOutputReference",
    "SecretManagerSecretReplicationUserManaged",
    "SecretManagerSecretReplicationUserManagedOutputReference",
    "SecretManagerSecretReplicationUserManagedReplicas",
    "SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption",
    "SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryptionOutputReference",
    "SecretManagerSecretReplicationUserManagedReplicasList",
    "SecretManagerSecretReplicationUserManagedReplicasOutputReference",
    "SecretManagerSecretRotation",
    "SecretManagerSecretRotationOutputReference",
    "SecretManagerSecretTimeouts",
    "SecretManagerSecretTimeoutsOutputReference",
    "SecretManagerSecretTopics",
    "SecretManagerSecretTopicsList",
    "SecretManagerSecretTopicsOutputReference",
]

publication.publish()

def _typecheckingstub__7375bebac0ff4e7082aec76eb7e9be7da9c8606210bdad09a93c8c5a65ec7a7f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    replication: typing.Union[SecretManagerSecretReplication, typing.Dict[builtins.str, typing.Any]],
    secret_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expire_time: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    rotation: typing.Optional[typing.Union[SecretManagerSecretRotation, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SecretManagerSecretTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    topics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecretManagerSecretTopics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ttl: typing.Optional[builtins.str] = None,
    version_aliases: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    version_destroy_ttl: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__fdf40712bced892d6d3c293ce9d8e19b2017770392c2cf6a66819356111cd438(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d87c8d901c6ada177ce865658fcfd459da74a0943b72318455764f9d8e17da(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecretManagerSecretTopics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e96cf88b6a30f97b80a72b3b4469029f9fd4d16b6024b152349b07378a2c136(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d274497e4763530e240b24454eae969238d52dee269bd080d76f2235860df42(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f1a53af1f82c7d5e6f0845e9f95ebf1c803cc28f3630bed78ee6a80778395e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7cd6e8cf2153e93f020436e599266ef1667a989aa27940c38a0bf3458329b8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34df967f1497850931f5c1793d46cf7293b0a031bfdbeccb9f2dbc7d18ff72d1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d9660c7c7dec736dbc62d0785748e1982cb1ea63d8df861415703e498f9d0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e529b1c0b146e52023631910baed36b8e2a73132091fecc4093d43f9bec5a21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f5d8a6710fc15d9d3b48e64b86ccfeffff4e4dad6c98da6a6e50290f2cd22d3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07df02dd866eb7d8542b6bc6bf1fe9c526dacb9ae818176d00b170d335377795(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9fa8eb89cc0c3d71779a881d774ea4146634b7fd78b802381e1b0905a5945d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9a9cf923d7ef5522ba8fd00dd9a669d6063739994ff70a4d1b2cd81c2ff29e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349c1c7af03e290e0199f9611b9200a2c6e3cbed766ff8c2d8118e2f09204a4e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    replication: typing.Union[SecretManagerSecretReplication, typing.Dict[builtins.str, typing.Any]],
    secret_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expire_time: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    rotation: typing.Optional[typing.Union[SecretManagerSecretRotation, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SecretManagerSecretTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    topics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecretManagerSecretTopics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ttl: typing.Optional[builtins.str] = None,
    version_aliases: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    version_destroy_ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea4728d3a9c1870cd1db2de5b385f301b1697b9f4cae65f99938aae95330a68(
    *,
    auto: typing.Optional[typing.Union[SecretManagerSecretReplicationAuto, typing.Dict[builtins.str, typing.Any]]] = None,
    user_managed: typing.Optional[typing.Union[SecretManagerSecretReplicationUserManaged, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe34db67d0755a35a2adc1d64864e2959c352d46ae3f51dd5aaae50b14a496ef(
    *,
    customer_managed_encryption: typing.Optional[typing.Union[SecretManagerSecretReplicationAutoCustomerManagedEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9c77c38667b06da814d54099bd223d8293e334b4d68cf66ddb1ae240117cb5(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e595bef2797e8bd96ab39770283e6cb463b44a60c2e5ee83fece243bf28069a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880dd3f9c6cdb453d53bbd96e781bc1735b62b265cc20698d8c4c7dca1044a33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ca205ac74fc4380a9cb89fbf507ef9268674f9c083b8977e92e8a10856ce04(
    value: typing.Optional[SecretManagerSecretReplicationAutoCustomerManagedEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f118bc4ec42d29a1700b8556f2d10a8d2e776c8a168860b02cfe9e435f0cd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c379b666c82d11c72551bcde922b316c18ac4b5d800c61a173e46bc2c54ca8(
    value: typing.Optional[SecretManagerSecretReplicationAuto],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8ed8ff8d88a340abd25b621f5e0f938cea9b06a78686380aa9eb9ea5172ca7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d319f5f8052b3a794e12709c14b1d9721cfa593a383fa479f34acc8eda5744(
    value: typing.Optional[SecretManagerSecretReplication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b26809d69924e0619aab37bbdd46699e98bc29d7d9ebcd7dbdc63c551a1149(
    *,
    replicas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecretManagerSecretReplicationUserManagedReplicas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b16dfd09ec907c4fa32f74ac4d10248ec7a076931048654bbde10e1f4612f9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e921d25d51ebff6811d9fcae2b535aeadf6861462f6d030405cdbc072f4f7445(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecretManagerSecretReplicationUserManagedReplicas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8e9325c95b9f5062bfdd59abdf18333161593fc3f853f4fe6583b666e7760b(
    value: typing.Optional[SecretManagerSecretReplicationUserManaged],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf90430f1099a074d2d6ffe83f518516033c676e86c9c98f61287e808acf730(
    *,
    location: builtins.str,
    customer_managed_encryption: typing.Optional[typing.Union[SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39ca7a21fdb4f5d2415ecb026dd1bdff5a80311ca9938697069934135428dca(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ebad0ae194a00d86e8d968fd6931562a2197c2c64cb03da5bfcac557a69ed1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14ea288972e9c9c0c8104ffb0c79fc01d909d51139e498c3ef0acb8bfe1a03c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d81daf9b915df7e2eefed096c3fefef3a09867c6becb3ad97afe2572ff8bd68(
    value: typing.Optional[SecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415ce6447eeb1264afd875f76ee8f7be4f80b18e65de754a05931eaa82ebef3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d5df0f876bb243c629ff3dc3bed947ef780af90de5cb06a121b2efeed36770(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ad8e5c1b1002a2c4cdfb63f559723bf02246761967b5d2735e292770730928(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1d99ed39c2447dcc08ca8d0770812abc8ac8c086d67e7d9f9175dec8fb256e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428842cc25ab0bbe3b3abed851a5acd29b8717642b44827daeff4eeae835c8f0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55b49341b973f565880ea90c1311137bc5cf6cdd48e85908a075e066f870fb4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecretManagerSecretReplicationUserManagedReplicas]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832dab1249f7bc80f8f07632c59023f82a082f9cd072e76967e4be6202595913(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a72d7d18f59f08d7f65c8d4a17320dc31c53b4d71e13687d985490b182cafa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71236c2c279743f767b5e5d02765a1f7d9a27e7d3ba7f1cbf48ae211d3930a1f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretReplicationUserManagedReplicas]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e0d39a618a8d890b47dddf51affdd0ad9e49a6bdd03ef1acba97523bb3a872(
    *,
    next_rotation_time: typing.Optional[builtins.str] = None,
    rotation_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed22b752a64f57264379f5bf3d7511c4e909c11cd5534e3fb0e67c0fc695f02b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721f52a7e1f85761398c6962da12440bd0905a3ab0711192f9b057f076cce674(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87327a6eac4bac4c6d02e8be96b88d285874b033a487d637f500c3cc3c231606(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d8c4e9faacdb113a632f5056a84a804c4dadb7482e593ad0504c6dd82b2dd2(
    value: typing.Optional[SecretManagerSecretRotation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051f68fd5971a8a4f914f242270b4f0ed43104b6965780cde8de7dbf367c5220(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a100a2587f640e96752d74786ee2fa1f26a67428b9f21e36ebd4b7905ecd3b02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd0c45c782276210923dbb4047ca198a4096df1aabdd19baf265d5dae547829(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4671d8fc71cdb8e4be2c6f959ee7a617fe5b8e2f4a946c88d0011f9017af7ddc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d236e7051461c61763a414af7b9ff868548b7fb14ca4e8e7fe25f7187bff8bcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353ec30785ac71a4f5a6a3065bcdd9573b69b318f2eb2c89482ffa1062b7a542(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7436308881c7404d9ca38b164fb583b1085659a0c16c102c235404c1866b1b70(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39a6edab10b98390b8f09e9844bf04f551a6e564cef6bdc6e1993f7e16b3467(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67fd56710108aac9428e3c9c23b01183bc8ed51edfecdb539b4382eec0ac236f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5abdc63825e0e7944c9c5a3ae4371a1029d418540f431a5e32d80070145175f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a165113c9ac428edbba077b8995d2f795029a600da573b327d5f06101039d0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7028848230f5b1174e2262abebc36acbf40cab1fc88101e0139c8bfe409a1155(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b4571ad10ce205c194fbe8014ffe89d6e99fe4a222ef8f853094aea22d6dcd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecretManagerSecretTopics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7c0a4a86486e8cbc23473892b1d7a8c940247fc3c7699c18fb45e4eb25cad6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5d4cc6d838ba7c1f4ade151031abe74d28945ef5077588cc78ff6caee21875(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2a279c855527e858864b4990baa95cda1678c2033a184d022f2e2e6888bd68(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretTopics]],
) -> None:
    """Type checking stubs"""
    pass

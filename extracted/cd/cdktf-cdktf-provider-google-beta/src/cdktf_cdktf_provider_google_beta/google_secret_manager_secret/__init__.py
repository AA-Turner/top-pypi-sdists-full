r'''
# `google_secret_manager_secret`

Refer to the Terraform Registry for docs: [`google_secret_manager_secret`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret).
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


class GoogleSecretManagerSecret(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecret",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret google_secret_manager_secret}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        replication: typing.Union["GoogleSecretManagerSecretReplication", typing.Dict[builtins.str, typing.Any]],
        secret_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        expire_time: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        rotation: typing.Optional[typing.Union["GoogleSecretManagerSecretRotation", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleSecretManagerSecretTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        topics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecretManagerSecretTopics", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret google_secret_manager_secret} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param replication: replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#replication GoogleSecretManagerSecret#replication}
        :param secret_id: This must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#secret_id GoogleSecretManagerSecret#secret_id}
        :param annotations: Custom metadata about the secret. Annotations are distinct from various forms of labels. Annotations exist to allow client tools to store their own state information without requiring a database. Annotation keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, begin and end with an alphanumeric character ([a-z0-9A-Z]), and may have dashes (-), underscores (_), dots (.), and alphanumerics in between these symbols. The total size of annotation keys and values must be less than 16KiB. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#annotations GoogleSecretManagerSecret#annotations}
        :param expire_time: Timestamp in UTC when the Secret is scheduled to expire. This is always provided on output, regardless of what was sent on input. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Only one of 'expire_time' or 'ttl' can be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#expire_time GoogleSecretManagerSecret#expire_time}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#id GoogleSecretManagerSecret#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels assigned to this Secret. Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}_-]{0,62} Label values must be between 0 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}_-]{0,63} No more than 64 labels can be assigned to a given resource. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#labels GoogleSecretManagerSecret#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#project GoogleSecretManagerSecret#project}.
        :param rotation: rotation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#rotation GoogleSecretManagerSecret#rotation}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#timeouts GoogleSecretManagerSecret#timeouts}
        :param topics: topics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#topics GoogleSecretManagerSecret#topics}
        :param ttl: The TTL for the Secret. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Only one of 'ttl' or 'expire_time' can be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#ttl GoogleSecretManagerSecret#ttl}
        :param version_aliases: Mapping from version alias to version name. A version alias is a string with a maximum length of 63 characters and can contain uppercase and lowercase letters, numerals, and the hyphen (-) and underscore ('_') characters. An alias string must start with a letter and cannot be the string 'latest' or 'NEW'. No more than 50 aliases can be assigned to a given secret. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#version_aliases GoogleSecretManagerSecret#version_aliases}
        :param version_destroy_ttl: Secret Version TTL after destruction request. This is a part of the delayed delete feature on Secret Version. For secret with versionDestroyTtl>0, version destruction doesn't happen immediately on calling destroy instead the version goes to a disabled state and the actual destruction happens after this TTL expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#version_destroy_ttl GoogleSecretManagerSecret#version_destroy_ttl}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99619e01b7779b2b6531b9ebcdbc1aec665292f089b804513dc6b46dee1c058b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleSecretManagerSecretConfig(
            replication=replication,
            secret_id=secret_id,
            annotations=annotations,
            expire_time=expire_time,
            id=id,
            labels=labels,
            project=project,
            rotation=rotation,
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
        '''Generates CDKTF code for importing a GoogleSecretManagerSecret resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleSecretManagerSecret to import.
        :param import_from_id: The id of the existing GoogleSecretManagerSecret that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleSecretManagerSecret to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__359ecfaf7e15c7dc0ef85eafb43ad2ad48a50ad22dad5c4cf34e1fd4464010d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putReplication")
    def put_replication(
        self,
        *,
        auto: typing.Optional[typing.Union["GoogleSecretManagerSecretReplicationAuto", typing.Dict[builtins.str, typing.Any]]] = None,
        user_managed: typing.Optional[typing.Union["GoogleSecretManagerSecretReplicationUserManaged", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto: auto block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#auto GoogleSecretManagerSecret#auto}
        :param user_managed: user_managed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#user_managed GoogleSecretManagerSecret#user_managed}
        '''
        value = GoogleSecretManagerSecretReplication(
            auto=auto, user_managed=user_managed
        )

        return typing.cast(None, jsii.invoke(self, "putReplication", [value]))

    @jsii.member(jsii_name="putRotation")
    def put_rotation(
        self,
        *,
        next_rotation_time: typing.Optional[builtins.str] = None,
        rotation_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param next_rotation_time: Timestamp in UTC at which the Secret is scheduled to rotate. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#next_rotation_time GoogleSecretManagerSecret#next_rotation_time}
        :param rotation_period: The Duration between rotation notifications. Must be in seconds and at least 3600s (1h) and at most 3153600000s (100 years). If rotationPeriod is set, 'next_rotation_time' must be set. 'next_rotation_time' will be advanced by this period when the service automatically sends rotation notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#rotation_period GoogleSecretManagerSecret#rotation_period}
        '''
        value = GoogleSecretManagerSecretRotation(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#create GoogleSecretManagerSecret#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#delete GoogleSecretManagerSecret#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#update GoogleSecretManagerSecret#update}.
        '''
        value = GoogleSecretManagerSecretTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTopics")
    def put_topics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecretManagerSecretTopics", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d51671337ed79998bab03ecc9c777fd8cf84b4e8efd740344027fa6199fdad04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTopics", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

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
    def replication(self) -> "GoogleSecretManagerSecretReplicationOutputReference":
        return typing.cast("GoogleSecretManagerSecretReplicationOutputReference", jsii.get(self, "replication"))

    @builtins.property
    @jsii.member(jsii_name="rotation")
    def rotation(self) -> "GoogleSecretManagerSecretRotationOutputReference":
        return typing.cast("GoogleSecretManagerSecretRotationOutputReference", jsii.get(self, "rotation"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleSecretManagerSecretTimeoutsOutputReference":
        return typing.cast("GoogleSecretManagerSecretTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(self) -> "GoogleSecretManagerSecretTopicsList":
        return typing.cast("GoogleSecretManagerSecretTopicsList", jsii.get(self, "topics"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

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
    def replication_input(
        self,
    ) -> typing.Optional["GoogleSecretManagerSecretReplication"]:
        return typing.cast(typing.Optional["GoogleSecretManagerSecretReplication"], jsii.get(self, "replicationInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationInput")
    def rotation_input(self) -> typing.Optional["GoogleSecretManagerSecretRotation"]:
        return typing.cast(typing.Optional["GoogleSecretManagerSecretRotation"], jsii.get(self, "rotationInput"))

    @builtins.property
    @jsii.member(jsii_name="secretIdInput")
    def secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleSecretManagerSecretTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleSecretManagerSecretTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="topicsInput")
    def topics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecretManagerSecretTopics"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecretManagerSecretTopics"]]], jsii.get(self, "topicsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4ad6e2066576bca96fc19ab46c09242ab28f9dcd8261c9479f7a9fc12e19c975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expireTime")
    def expire_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireTime"))

    @expire_time.setter
    def expire_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809ea3cd383a9b324a50cb82d76be784110cac73a3e80bc650d9386b4eab2704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expireTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f160b4c080a8640bb2e34ef74d78bd2ce3cb25630f151c7739ae68819a201ed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b23caf383e41c2b8a268130392291faaf937f58ca0f532783cb10503ba893c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03172ce9a097c679e7a073cb4810e563e2a9c3021edf938d1abd8df04e83621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretId"))

    @secret_id.setter
    def secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8fd5997cb897c1a0acedfa80470206b36ff76049228efc4a9aa641c3245e289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf01ab45a480cbf2d5dc9614b777c5ade7877cffda97f3de573e8af4e0c6c0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25c2d9379fd25a5f7532b8fb57a1e67a687aad484126d3b492fc8ea9f4fe46d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionAliases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionDestroyTtl")
    def version_destroy_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionDestroyTtl"))

    @version_destroy_ttl.setter
    def version_destroy_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21059d49e5a67f68b5f9a1a206ca7b6b92a424709002eed1437bf6f28c421cf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionDestroyTtl", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretConfig",
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
        "expire_time": "expireTime",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "rotation": "rotation",
        "timeouts": "timeouts",
        "topics": "topics",
        "ttl": "ttl",
        "version_aliases": "versionAliases",
        "version_destroy_ttl": "versionDestroyTtl",
    },
)
class GoogleSecretManagerSecretConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        replication: typing.Union["GoogleSecretManagerSecretReplication", typing.Dict[builtins.str, typing.Any]],
        secret_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        expire_time: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        rotation: typing.Optional[typing.Union["GoogleSecretManagerSecretRotation", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleSecretManagerSecretTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        topics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecretManagerSecretTopics", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param replication: replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#replication GoogleSecretManagerSecret#replication}
        :param secret_id: This must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#secret_id GoogleSecretManagerSecret#secret_id}
        :param annotations: Custom metadata about the secret. Annotations are distinct from various forms of labels. Annotations exist to allow client tools to store their own state information without requiring a database. Annotation keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, begin and end with an alphanumeric character ([a-z0-9A-Z]), and may have dashes (-), underscores (_), dots (.), and alphanumerics in between these symbols. The total size of annotation keys and values must be less than 16KiB. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#annotations GoogleSecretManagerSecret#annotations}
        :param expire_time: Timestamp in UTC when the Secret is scheduled to expire. This is always provided on output, regardless of what was sent on input. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Only one of 'expire_time' or 'ttl' can be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#expire_time GoogleSecretManagerSecret#expire_time}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#id GoogleSecretManagerSecret#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels assigned to this Secret. Label keys must be between 1 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}][\\p{Ll}\\p{Lo}\\p{N}_-]{0,62} Label values must be between 0 and 63 characters long, have a UTF-8 encoding of maximum 128 bytes, and must conform to the following PCRE regular expression: [\\p{Ll}\\p{Lo}\\p{N}_-]{0,63} No more than 64 labels can be assigned to a given resource. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#labels GoogleSecretManagerSecret#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#project GoogleSecretManagerSecret#project}.
        :param rotation: rotation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#rotation GoogleSecretManagerSecret#rotation}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#timeouts GoogleSecretManagerSecret#timeouts}
        :param topics: topics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#topics GoogleSecretManagerSecret#topics}
        :param ttl: The TTL for the Secret. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Only one of 'ttl' or 'expire_time' can be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#ttl GoogleSecretManagerSecret#ttl}
        :param version_aliases: Mapping from version alias to version name. A version alias is a string with a maximum length of 63 characters and can contain uppercase and lowercase letters, numerals, and the hyphen (-) and underscore ('_') characters. An alias string must start with a letter and cannot be the string 'latest' or 'NEW'. No more than 50 aliases can be assigned to a given secret. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#version_aliases GoogleSecretManagerSecret#version_aliases}
        :param version_destroy_ttl: Secret Version TTL after destruction request. This is a part of the delayed delete feature on Secret Version. For secret with versionDestroyTtl>0, version destruction doesn't happen immediately on calling destroy instead the version goes to a disabled state and the actual destruction happens after this TTL expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#version_destroy_ttl GoogleSecretManagerSecret#version_destroy_ttl}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(replication, dict):
            replication = GoogleSecretManagerSecretReplication(**replication)
        if isinstance(rotation, dict):
            rotation = GoogleSecretManagerSecretRotation(**rotation)
        if isinstance(timeouts, dict):
            timeouts = GoogleSecretManagerSecretTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d7384e95aff5e86eb11bc197acd15593522671073b405b403bc401843fb608a)
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
            check_type(argname="argument expire_time", value=expire_time, expected_type=type_hints["expire_time"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument rotation", value=rotation, expected_type=type_hints["rotation"])
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
    def replication(self) -> "GoogleSecretManagerSecretReplication":
        '''replication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#replication GoogleSecretManagerSecret#replication}
        '''
        result = self._values.get("replication")
        assert result is not None, "Required property 'replication' is missing"
        return typing.cast("GoogleSecretManagerSecretReplication", result)

    @builtins.property
    def secret_id(self) -> builtins.str:
        '''This must be unique within the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#secret_id GoogleSecretManagerSecret#secret_id}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#annotations GoogleSecretManagerSecret#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def expire_time(self) -> typing.Optional[builtins.str]:
        '''Timestamp in UTC when the Secret is scheduled to expire.

        This is always provided on output, regardless of what was sent on input.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        Only one of 'expire_time' or 'ttl' can be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#expire_time GoogleSecretManagerSecret#expire_time}
        '''
        result = self._values.get("expire_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#id GoogleSecretManagerSecret#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#labels GoogleSecretManagerSecret#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#project GoogleSecretManagerSecret#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotation(self) -> typing.Optional["GoogleSecretManagerSecretRotation"]:
        '''rotation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#rotation GoogleSecretManagerSecret#rotation}
        '''
        result = self._values.get("rotation")
        return typing.cast(typing.Optional["GoogleSecretManagerSecretRotation"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleSecretManagerSecretTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#timeouts GoogleSecretManagerSecret#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleSecretManagerSecretTimeouts"], result)

    @builtins.property
    def topics(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecretManagerSecretTopics"]]]:
        '''topics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#topics GoogleSecretManagerSecret#topics}
        '''
        result = self._values.get("topics")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecretManagerSecretTopics"]]], result)

    @builtins.property
    def ttl(self) -> typing.Optional[builtins.str]:
        '''The TTL for the Secret.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".
        Only one of 'ttl' or 'expire_time' can be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#ttl GoogleSecretManagerSecret#ttl}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#version_aliases GoogleSecretManagerSecret#version_aliases}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#version_destroy_ttl GoogleSecretManagerSecret#version_destroy_ttl}
        '''
        result = self._values.get("version_destroy_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecretManagerSecretConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretReplication",
    jsii_struct_bases=[],
    name_mapping={"auto": "auto", "user_managed": "userManaged"},
)
class GoogleSecretManagerSecretReplication:
    def __init__(
        self,
        *,
        auto: typing.Optional[typing.Union["GoogleSecretManagerSecretReplicationAuto", typing.Dict[builtins.str, typing.Any]]] = None,
        user_managed: typing.Optional[typing.Union["GoogleSecretManagerSecretReplicationUserManaged", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto: auto block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#auto GoogleSecretManagerSecret#auto}
        :param user_managed: user_managed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#user_managed GoogleSecretManagerSecret#user_managed}
        '''
        if isinstance(auto, dict):
            auto = GoogleSecretManagerSecretReplicationAuto(**auto)
        if isinstance(user_managed, dict):
            user_managed = GoogleSecretManagerSecretReplicationUserManaged(**user_managed)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7a50fc7c7248374916205a42ae8431c3a8a4abfc6989472271429ae020cdf9)
            check_type(argname="argument auto", value=auto, expected_type=type_hints["auto"])
            check_type(argname="argument user_managed", value=user_managed, expected_type=type_hints["user_managed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto is not None:
            self._values["auto"] = auto
        if user_managed is not None:
            self._values["user_managed"] = user_managed

    @builtins.property
    def auto(self) -> typing.Optional["GoogleSecretManagerSecretReplicationAuto"]:
        '''auto block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#auto GoogleSecretManagerSecret#auto}
        '''
        result = self._values.get("auto")
        return typing.cast(typing.Optional["GoogleSecretManagerSecretReplicationAuto"], result)

    @builtins.property
    def user_managed(
        self,
    ) -> typing.Optional["GoogleSecretManagerSecretReplicationUserManaged"]:
        '''user_managed block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#user_managed GoogleSecretManagerSecret#user_managed}
        '''
        result = self._values.get("user_managed")
        return typing.cast(typing.Optional["GoogleSecretManagerSecretReplicationUserManaged"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecretManagerSecretReplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretReplicationAuto",
    jsii_struct_bases=[],
    name_mapping={"customer_managed_encryption": "customerManagedEncryption"},
)
class GoogleSecretManagerSecretReplicationAuto:
    def __init__(
        self,
        *,
        customer_managed_encryption: typing.Optional[typing.Union["GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param customer_managed_encryption: customer_managed_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#customer_managed_encryption GoogleSecretManagerSecret#customer_managed_encryption}
        '''
        if isinstance(customer_managed_encryption, dict):
            customer_managed_encryption = GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption(**customer_managed_encryption)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9f61a6e2c3085c02a1288cae84a4912b51ab3267207c32b752f007fcd4f5330)
            check_type(argname="argument customer_managed_encryption", value=customer_managed_encryption, expected_type=type_hints["customer_managed_encryption"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if customer_managed_encryption is not None:
            self._values["customer_managed_encryption"] = customer_managed_encryption

    @builtins.property
    def customer_managed_encryption(
        self,
    ) -> typing.Optional["GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption"]:
        '''customer_managed_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#customer_managed_encryption GoogleSecretManagerSecret#customer_managed_encryption}
        '''
        result = self._values.get("customer_managed_encryption")
        return typing.cast(typing.Optional["GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecretManagerSecretReplicationAuto(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The resource name of the Cloud KMS CryptoKey used to encrypt secret payloads. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#kms_key_name GoogleSecretManagerSecret#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b09cd4f8ae91105f7118e46ef5dcc4be86f7e483dea436e361642d2a15d1523)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''The resource name of the Cloud KMS CryptoKey used to encrypt secret payloads.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#kms_key_name GoogleSecretManagerSecret#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57662f201ee464bb44faa4f149b2d30546eaaf3d45ea49e02e05b90e32f9b34a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bdbbd69a50d385a764bec7d54330e45745bb3333a7c34760f64ebae20efee28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption]:
        return typing.cast(typing.Optional[GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e1d82e11b1ada7859a5d55cbf118c225605f7381dfb3aa60df401952cb2e48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecretManagerSecretReplicationAutoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretReplicationAutoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae0758f14b7cfd21b15d72532141dc1da2ee997c16b32d383784e113825d58f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomerManagedEncryption")
    def put_customer_managed_encryption(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The resource name of the Cloud KMS CryptoKey used to encrypt secret payloads. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#kms_key_name GoogleSecretManagerSecret#kms_key_name}
        '''
        value = GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption(
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
    ) -> GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryptionOutputReference:
        return typing.cast(GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryptionOutputReference, jsii.get(self, "customerManagedEncryption"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedEncryptionInput")
    def customer_managed_encryption_input(
        self,
    ) -> typing.Optional[GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption]:
        return typing.cast(typing.Optional[GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption], jsii.get(self, "customerManagedEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecretManagerSecretReplicationAuto]:
        return typing.cast(typing.Optional[GoogleSecretManagerSecretReplicationAuto], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecretManagerSecretReplicationAuto],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ee3162b1763469d44bb19b324520a4911f6b68111f96b8494c94b408cdac50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecretManagerSecretReplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretReplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__761ee3a46518cb484717f49a894a43ad07a0bf7ae861444ba672ffa0eeb8f3f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuto")
    def put_auto(
        self,
        *,
        customer_managed_encryption: typing.Optional[typing.Union[GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param customer_managed_encryption: customer_managed_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#customer_managed_encryption GoogleSecretManagerSecret#customer_managed_encryption}
        '''
        value = GoogleSecretManagerSecretReplicationAuto(
            customer_managed_encryption=customer_managed_encryption
        )

        return typing.cast(None, jsii.invoke(self, "putAuto", [value]))

    @jsii.member(jsii_name="putUserManaged")
    def put_user_managed(
        self,
        *,
        replicas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecretManagerSecretReplicationUserManagedReplicas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param replicas: replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#replicas GoogleSecretManagerSecret#replicas}
        '''
        value = GoogleSecretManagerSecretReplicationUserManaged(replicas=replicas)

        return typing.cast(None, jsii.invoke(self, "putUserManaged", [value]))

    @jsii.member(jsii_name="resetAuto")
    def reset_auto(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuto", []))

    @jsii.member(jsii_name="resetUserManaged")
    def reset_user_managed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserManaged", []))

    @builtins.property
    @jsii.member(jsii_name="auto")
    def auto(self) -> GoogleSecretManagerSecretReplicationAutoOutputReference:
        return typing.cast(GoogleSecretManagerSecretReplicationAutoOutputReference, jsii.get(self, "auto"))

    @builtins.property
    @jsii.member(jsii_name="userManaged")
    def user_managed(
        self,
    ) -> "GoogleSecretManagerSecretReplicationUserManagedOutputReference":
        return typing.cast("GoogleSecretManagerSecretReplicationUserManagedOutputReference", jsii.get(self, "userManaged"))

    @builtins.property
    @jsii.member(jsii_name="autoInput")
    def auto_input(self) -> typing.Optional[GoogleSecretManagerSecretReplicationAuto]:
        return typing.cast(typing.Optional[GoogleSecretManagerSecretReplicationAuto], jsii.get(self, "autoInput"))

    @builtins.property
    @jsii.member(jsii_name="userManagedInput")
    def user_managed_input(
        self,
    ) -> typing.Optional["GoogleSecretManagerSecretReplicationUserManaged"]:
        return typing.cast(typing.Optional["GoogleSecretManagerSecretReplicationUserManaged"], jsii.get(self, "userManagedInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleSecretManagerSecretReplication]:
        return typing.cast(typing.Optional[GoogleSecretManagerSecretReplication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecretManagerSecretReplication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441589a31d2af8a44fae89f389d591898f68b57c16ca4c8fcb02d2d58d8f6050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretReplicationUserManaged",
    jsii_struct_bases=[],
    name_mapping={"replicas": "replicas"},
)
class GoogleSecretManagerSecretReplicationUserManaged:
    def __init__(
        self,
        *,
        replicas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecretManagerSecretReplicationUserManagedReplicas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param replicas: replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#replicas GoogleSecretManagerSecret#replicas}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00270bb70ebf57399ea2f6516b249e6eb5376623baf08b0557e20e8610ed403f)
            check_type(argname="argument replicas", value=replicas, expected_type=type_hints["replicas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "replicas": replicas,
        }

    @builtins.property
    def replicas(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecretManagerSecretReplicationUserManagedReplicas"]]:
        '''replicas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#replicas GoogleSecretManagerSecret#replicas}
        '''
        result = self._values.get("replicas")
        assert result is not None, "Required property 'replicas' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecretManagerSecretReplicationUserManagedReplicas"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecretManagerSecretReplicationUserManaged(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecretManagerSecretReplicationUserManagedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretReplicationUserManagedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b07d502ea20103faf41ba35349c799f5d0f08456d62f028969b77e8ee5d0d70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putReplicas")
    def put_replicas(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSecretManagerSecretReplicationUserManagedReplicas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e35e7e0fcfdcc3b088222770df1ad437e4951f15a6789270ca4bb687974e4c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putReplicas", [value]))

    @builtins.property
    @jsii.member(jsii_name="replicas")
    def replicas(self) -> "GoogleSecretManagerSecretReplicationUserManagedReplicasList":
        return typing.cast("GoogleSecretManagerSecretReplicationUserManagedReplicasList", jsii.get(self, "replicas"))

    @builtins.property
    @jsii.member(jsii_name="replicasInput")
    def replicas_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecretManagerSecretReplicationUserManagedReplicas"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSecretManagerSecretReplicationUserManagedReplicas"]]], jsii.get(self, "replicasInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecretManagerSecretReplicationUserManaged]:
        return typing.cast(typing.Optional[GoogleSecretManagerSecretReplicationUserManaged], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecretManagerSecretReplicationUserManaged],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66d804246f3dfd3e898f447d389cafc97dc2579d25d5135d49a0a65c88caf8fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretReplicationUserManagedReplicas",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "customer_managed_encryption": "customerManagedEncryption",
    },
)
class GoogleSecretManagerSecretReplicationUserManagedReplicas:
    def __init__(
        self,
        *,
        location: builtins.str,
        customer_managed_encryption: typing.Optional[typing.Union["GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param location: The canonical IDs of the location to replicate data. For example: "us-east1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#location GoogleSecretManagerSecret#location}
        :param customer_managed_encryption: customer_managed_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#customer_managed_encryption GoogleSecretManagerSecret#customer_managed_encryption}
        '''
        if isinstance(customer_managed_encryption, dict):
            customer_managed_encryption = GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption(**customer_managed_encryption)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e346c55384bf548bc89bd82aee2c9b5a5eac857095ad42f1606358799f752d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#location GoogleSecretManagerSecret#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def customer_managed_encryption(
        self,
    ) -> typing.Optional["GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption"]:
        '''customer_managed_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#customer_managed_encryption GoogleSecretManagerSecret#customer_managed_encryption}
        '''
        result = self._values.get("customer_managed_encryption")
        return typing.cast(typing.Optional["GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecretManagerSecretReplicationUserManagedReplicas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: Describes the Cloud KMS encryption key that will be used to protect destination secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#kms_key_name GoogleSecretManagerSecret#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d60db12a46511b9774863899e39df7d4a38b8afe0aef790ba0b4bd483c85bf)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''Describes the Cloud KMS encryption key that will be used to protect destination secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#kms_key_name GoogleSecretManagerSecret#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81f8ce1db860df0039ca100a9238724f508fb68cb20625c7e92181675024ecbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a78ba08a02d95aa961aff783dd6f705c245e4da7555330ec302a9207f78d715)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption]:
        return typing.cast(typing.Optional[GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221652ba62128320e47ec56f9e01c2fe9c633278e652d5209847a6eba38bbbe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecretManagerSecretReplicationUserManagedReplicasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretReplicationUserManagedReplicasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8341fa2da0bdd7f04a2ce9c9a83fe8ed022f313156aa78ea6ce5ba4e9628d903)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSecretManagerSecretReplicationUserManagedReplicasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c185addc40510593587ff56dcd39e7434fd192538fc7153770683dc067e3480f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSecretManagerSecretReplicationUserManagedReplicasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a66b0c2c100754c90deea4441517ae3fa8401d57bd2a3f138fb85e9df7019b71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__656039674c5157fda83a253568fe0bc86facaba39e6ace302f3081498bd3d121)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bbb960fb1a48764928a7b586d5d55ff89c8ff7a77a661bef6605f164d789c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecretManagerSecretReplicationUserManagedReplicas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecretManagerSecretReplicationUserManagedReplicas]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecretManagerSecretReplicationUserManagedReplicas]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9186cbc9fc394cf5446025aeeaf280f76b3876d10c6d0568377cf921bc97f604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecretManagerSecretReplicationUserManagedReplicasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretReplicationUserManagedReplicasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38c8ba606b9340c0ac91c8c22013eb8c0c7c2cae1fb04f6c4860682de48b0c93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomerManagedEncryption")
    def put_customer_managed_encryption(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: Describes the Cloud KMS encryption key that will be used to protect destination secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#kms_key_name GoogleSecretManagerSecret#kms_key_name}
        '''
        value = GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption(
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
    ) -> GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryptionOutputReference:
        return typing.cast(GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryptionOutputReference, jsii.get(self, "customerManagedEncryption"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedEncryptionInput")
    def customer_managed_encryption_input(
        self,
    ) -> typing.Optional[GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption]:
        return typing.cast(typing.Optional[GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption], jsii.get(self, "customerManagedEncryptionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__524bdac7d2e7289e2da3d9d3381622bc90140143b9c915cc022292d5035930e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecretManagerSecretReplicationUserManagedReplicas]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecretManagerSecretReplicationUserManagedReplicas]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecretManagerSecretReplicationUserManagedReplicas]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c095dbdeccaeb39572c1adfde58cc741639ab42166ba9e677c25419a4026fc17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretRotation",
    jsii_struct_bases=[],
    name_mapping={
        "next_rotation_time": "nextRotationTime",
        "rotation_period": "rotationPeriod",
    },
)
class GoogleSecretManagerSecretRotation:
    def __init__(
        self,
        *,
        next_rotation_time: typing.Optional[builtins.str] = None,
        rotation_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param next_rotation_time: Timestamp in UTC at which the Secret is scheduled to rotate. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#next_rotation_time GoogleSecretManagerSecret#next_rotation_time}
        :param rotation_period: The Duration between rotation notifications. Must be in seconds and at least 3600s (1h) and at most 3153600000s (100 years). If rotationPeriod is set, 'next_rotation_time' must be set. 'next_rotation_time' will be advanced by this period when the service automatically sends rotation notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#rotation_period GoogleSecretManagerSecret#rotation_period}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b30a0ddbe82a0197f370db8fdbbb9da6ced5f60c311d56c65d354b1215921477)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#next_rotation_time GoogleSecretManagerSecret#next_rotation_time}
        '''
        result = self._values.get("next_rotation_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotation_period(self) -> typing.Optional[builtins.str]:
        '''The Duration between rotation notifications.

        Must be in seconds and at least 3600s (1h) and at most 3153600000s (100 years).
        If rotationPeriod is set, 'next_rotation_time' must be set. 'next_rotation_time' will be advanced by this period when the service automatically sends rotation notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#rotation_period GoogleSecretManagerSecret#rotation_period}
        '''
        result = self._values.get("rotation_period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecretManagerSecretRotation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecretManagerSecretRotationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretRotationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5e28257e2db1009b31fd13fe12a535d985a975e6148505268fda10d0ad1c615)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c6bc8811fdd1580fca7140a5fe567f0f5fe903ef598013cc299939649833214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextRotationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationPeriod")
    def rotation_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rotationPeriod"))

    @rotation_period.setter
    def rotation_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01b494a3d6773b94cc9cf4efe86a6f2a4cf2921300e85b830c7e78c4e7e585e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleSecretManagerSecretRotation]:
        return typing.cast(typing.Optional[GoogleSecretManagerSecretRotation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSecretManagerSecretRotation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3136823bbde13658a38c53856e34fa341062cea0217aba2ccad697bc7fd3805b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleSecretManagerSecretTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#create GoogleSecretManagerSecret#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#delete GoogleSecretManagerSecret#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#update GoogleSecretManagerSecret#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e2ed06a6c604fef7fd4c31f25377582571abb1c04ff49b81755ffbead3c3cf5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#create GoogleSecretManagerSecret#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#delete GoogleSecretManagerSecret#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#update GoogleSecretManagerSecret#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSecretManagerSecretTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecretManagerSecretTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7544b33b6721d84a55944d69ab24c74d7cc33f84445a98a28e5397299dec4cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0916ce91ea907aa634bbf319dd72302f6715f62d560766d6d955fda95dc28521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e1bfb5460252b11032735019d23e5507556b7d44407ecf7b55b70936de89ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d36897d827bffd23e24e8812c56d9fb302e240b496a9608512301da49d63330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecretManagerSecretTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecretManagerSecretTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecretManagerSecretTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8938ece3f4b1bd4a14e5eae128680a592037da84bb4113f6e81b00be279bef20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretTopics",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleSecretManagerSecretTopics:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: The resource name of the Pub/Sub topic that will be published to, in the following format: projects/* /topics/*. For publication to succeed, the Secret Manager Service Agent service account must have pubsub.publisher permissions on the topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#name GoogleSecretManagerSecret#name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5666b0d779dbe988caf8a6b46226f11581e19378c0c69ba7bfe964d68901b68e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name of the Pub/Sub topic that will be published to, in the following format: projects/* /topics/*.

        For publication to succeed, the Secret Manager Service Agent service account must have pubsub.publisher permissions on the topic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_secret_manager_secret#name GoogleSecretManagerSecret#name}

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
        return "GoogleSecretManagerSecretTopics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSecretManagerSecretTopicsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretTopicsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe38b51bd22d4d1b231048cca0be138d63cbddbf597fbb1cdd876158928ae5aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSecretManagerSecretTopicsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66f602844d856c0902abd6682d86468c5936b57e28616b3e441b52116c49f27)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSecretManagerSecretTopicsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e089970ea7118a1c202f8cde5d7e0f8101d452f456055b1d930c2a708ac99ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e3301bccd486c98fd60b8a8b4b857338d1862860def8a87e018cff81a75d60d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eca11baaf273035179ae303b6ba5bc69dbbb1f5c4201400c17d4385a78873118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecretManagerSecretTopics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecretManagerSecretTopics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecretManagerSecretTopics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9642a23b6554861c8fe724e8dfe0ae8b4afffb40e2cde5fa88fb280d93cceea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSecretManagerSecretTopicsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSecretManagerSecret.GoogleSecretManagerSecretTopicsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aec08f9edae88ca8c3d2b00384a21c0abe3d96f5d213bb554cc1ea53ef3bf0c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__301ec26420dd01ee142d5d7550c767554fbaa43350b631d6c4e63fcfbe89240d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecretManagerSecretTopics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecretManagerSecretTopics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecretManagerSecretTopics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11fd523febcf94ce5ba0b532399dad00995abdb380c4d1fa315b37b98f5142a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleSecretManagerSecret",
    "GoogleSecretManagerSecretConfig",
    "GoogleSecretManagerSecretReplication",
    "GoogleSecretManagerSecretReplicationAuto",
    "GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption",
    "GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryptionOutputReference",
    "GoogleSecretManagerSecretReplicationAutoOutputReference",
    "GoogleSecretManagerSecretReplicationOutputReference",
    "GoogleSecretManagerSecretReplicationUserManaged",
    "GoogleSecretManagerSecretReplicationUserManagedOutputReference",
    "GoogleSecretManagerSecretReplicationUserManagedReplicas",
    "GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption",
    "GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryptionOutputReference",
    "GoogleSecretManagerSecretReplicationUserManagedReplicasList",
    "GoogleSecretManagerSecretReplicationUserManagedReplicasOutputReference",
    "GoogleSecretManagerSecretRotation",
    "GoogleSecretManagerSecretRotationOutputReference",
    "GoogleSecretManagerSecretTimeouts",
    "GoogleSecretManagerSecretTimeoutsOutputReference",
    "GoogleSecretManagerSecretTopics",
    "GoogleSecretManagerSecretTopicsList",
    "GoogleSecretManagerSecretTopicsOutputReference",
]

publication.publish()

def _typecheckingstub__99619e01b7779b2b6531b9ebcdbc1aec665292f089b804513dc6b46dee1c058b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    replication: typing.Union[GoogleSecretManagerSecretReplication, typing.Dict[builtins.str, typing.Any]],
    secret_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    expire_time: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    rotation: typing.Optional[typing.Union[GoogleSecretManagerSecretRotation, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleSecretManagerSecretTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    topics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecretManagerSecretTopics, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__359ecfaf7e15c7dc0ef85eafb43ad2ad48a50ad22dad5c4cf34e1fd4464010d9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d51671337ed79998bab03ecc9c777fd8cf84b4e8efd740344027fa6199fdad04(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecretManagerSecretTopics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad6e2066576bca96fc19ab46c09242ab28f9dcd8261c9479f7a9fc12e19c975(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809ea3cd383a9b324a50cb82d76be784110cac73a3e80bc650d9386b4eab2704(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f160b4c080a8640bb2e34ef74d78bd2ce3cb25630f151c7739ae68819a201ed5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b23caf383e41c2b8a268130392291faaf937f58ca0f532783cb10503ba893c9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03172ce9a097c679e7a073cb4810e563e2a9c3021edf938d1abd8df04e83621(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8fd5997cb897c1a0acedfa80470206b36ff76049228efc4a9aa641c3245e289(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf01ab45a480cbf2d5dc9614b777c5ade7877cffda97f3de573e8af4e0c6c0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c2d9379fd25a5f7532b8fb57a1e67a687aad484126d3b492fc8ea9f4fe46d9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21059d49e5a67f68b5f9a1a206ca7b6b92a424709002eed1437bf6f28c421cf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7384e95aff5e86eb11bc197acd15593522671073b405b403bc401843fb608a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    replication: typing.Union[GoogleSecretManagerSecretReplication, typing.Dict[builtins.str, typing.Any]],
    secret_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    expire_time: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    rotation: typing.Optional[typing.Union[GoogleSecretManagerSecretRotation, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleSecretManagerSecretTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    topics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecretManagerSecretTopics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ttl: typing.Optional[builtins.str] = None,
    version_aliases: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    version_destroy_ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7a50fc7c7248374916205a42ae8431c3a8a4abfc6989472271429ae020cdf9(
    *,
    auto: typing.Optional[typing.Union[GoogleSecretManagerSecretReplicationAuto, typing.Dict[builtins.str, typing.Any]]] = None,
    user_managed: typing.Optional[typing.Union[GoogleSecretManagerSecretReplicationUserManaged, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f61a6e2c3085c02a1288cae84a4912b51ab3267207c32b752f007fcd4f5330(
    *,
    customer_managed_encryption: typing.Optional[typing.Union[GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b09cd4f8ae91105f7118e46ef5dcc4be86f7e483dea436e361642d2a15d1523(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57662f201ee464bb44faa4f149b2d30546eaaf3d45ea49e02e05b90e32f9b34a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bdbbd69a50d385a764bec7d54330e45745bb3333a7c34760f64ebae20efee28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e1d82e11b1ada7859a5d55cbf118c225605f7381dfb3aa60df401952cb2e48(
    value: typing.Optional[GoogleSecretManagerSecretReplicationAutoCustomerManagedEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae0758f14b7cfd21b15d72532141dc1da2ee997c16b32d383784e113825d58f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ee3162b1763469d44bb19b324520a4911f6b68111f96b8494c94b408cdac50(
    value: typing.Optional[GoogleSecretManagerSecretReplicationAuto],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761ee3a46518cb484717f49a894a43ad07a0bf7ae861444ba672ffa0eeb8f3f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441589a31d2af8a44fae89f389d591898f68b57c16ca4c8fcb02d2d58d8f6050(
    value: typing.Optional[GoogleSecretManagerSecretReplication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00270bb70ebf57399ea2f6516b249e6eb5376623baf08b0557e20e8610ed403f(
    *,
    replicas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecretManagerSecretReplicationUserManagedReplicas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b07d502ea20103faf41ba35349c799f5d0f08456d62f028969b77e8ee5d0d70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35e7e0fcfdcc3b088222770df1ad437e4951f15a6789270ca4bb687974e4c5e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSecretManagerSecretReplicationUserManagedReplicas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d804246f3dfd3e898f447d389cafc97dc2579d25d5135d49a0a65c88caf8fd(
    value: typing.Optional[GoogleSecretManagerSecretReplicationUserManaged],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e346c55384bf548bc89bd82aee2c9b5a5eac857095ad42f1606358799f752d(
    *,
    location: builtins.str,
    customer_managed_encryption: typing.Optional[typing.Union[GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d60db12a46511b9774863899e39df7d4a38b8afe0aef790ba0b4bd483c85bf(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f8ce1db860df0039ca100a9238724f508fb68cb20625c7e92181675024ecbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a78ba08a02d95aa961aff783dd6f705c245e4da7555330ec302a9207f78d715(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221652ba62128320e47ec56f9e01c2fe9c633278e652d5209847a6eba38bbbe4(
    value: typing.Optional[GoogleSecretManagerSecretReplicationUserManagedReplicasCustomerManagedEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8341fa2da0bdd7f04a2ce9c9a83fe8ed022f313156aa78ea6ce5ba4e9628d903(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c185addc40510593587ff56dcd39e7434fd192538fc7153770683dc067e3480f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66b0c2c100754c90deea4441517ae3fa8401d57bd2a3f138fb85e9df7019b71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656039674c5157fda83a253568fe0bc86facaba39e6ace302f3081498bd3d121(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbb960fb1a48764928a7b586d5d55ff89c8ff7a77a661bef6605f164d789c1b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9186cbc9fc394cf5446025aeeaf280f76b3876d10c6d0568377cf921bc97f604(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecretManagerSecretReplicationUserManagedReplicas]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c8ba606b9340c0ac91c8c22013eb8c0c7c2cae1fb04f6c4860682de48b0c93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524bdac7d2e7289e2da3d9d3381622bc90140143b9c915cc022292d5035930e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c095dbdeccaeb39572c1adfde58cc741639ab42166ba9e677c25419a4026fc17(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecretManagerSecretReplicationUserManagedReplicas]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30a0ddbe82a0197f370db8fdbbb9da6ced5f60c311d56c65d354b1215921477(
    *,
    next_rotation_time: typing.Optional[builtins.str] = None,
    rotation_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e28257e2db1009b31fd13fe12a535d985a975e6148505268fda10d0ad1c615(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6bc8811fdd1580fca7140a5fe567f0f5fe903ef598013cc299939649833214(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b494a3d6773b94cc9cf4efe86a6f2a4cf2921300e85b830c7e78c4e7e585e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3136823bbde13658a38c53856e34fa341062cea0217aba2ccad697bc7fd3805b(
    value: typing.Optional[GoogleSecretManagerSecretRotation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e2ed06a6c604fef7fd4c31f25377582571abb1c04ff49b81755ffbead3c3cf5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7544b33b6721d84a55944d69ab24c74d7cc33f84445a98a28e5397299dec4cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0916ce91ea907aa634bbf319dd72302f6715f62d560766d6d955fda95dc28521(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e1bfb5460252b11032735019d23e5507556b7d44407ecf7b55b70936de89ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d36897d827bffd23e24e8812c56d9fb302e240b496a9608512301da49d63330(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8938ece3f4b1bd4a14e5eae128680a592037da84bb4113f6e81b00be279bef20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecretManagerSecretTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5666b0d779dbe988caf8a6b46226f11581e19378c0c69ba7bfe964d68901b68e(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe38b51bd22d4d1b231048cca0be138d63cbddbf597fbb1cdd876158928ae5aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66f602844d856c0902abd6682d86468c5936b57e28616b3e441b52116c49f27(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e089970ea7118a1c202f8cde5d7e0f8101d452f456055b1d930c2a708ac99ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3301bccd486c98fd60b8a8b4b857338d1862860def8a87e018cff81a75d60d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca11baaf273035179ae303b6ba5bc69dbbb1f5c4201400c17d4385a78873118(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9642a23b6554861c8fe724e8dfe0ae8b4afffb40e2cde5fa88fb280d93cceea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSecretManagerSecretTopics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec08f9edae88ca8c3d2b00384a21c0abe3d96f5d213bb554cc1ea53ef3bf0c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301ec26420dd01ee142d5d7550c767554fbaa43350b631d6c4e63fcfbe89240d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11fd523febcf94ce5ba0b532399dad00995abdb380c4d1fa315b37b98f5142a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSecretManagerSecretTopics]],
) -> None:
    """Type checking stubs"""
    pass

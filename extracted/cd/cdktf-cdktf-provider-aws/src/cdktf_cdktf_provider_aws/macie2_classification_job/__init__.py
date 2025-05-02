r'''
# `aws_macie2_classification_job`

Refer to the Terraform Registry for docs: [`aws_macie2_classification_job`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job).
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


class Macie2ClassificationJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job aws_macie2_classification_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        job_type: builtins.str,
        s3_job_definition: typing.Union["Macie2ClassificationJobS3JobDefinition", typing.Dict[builtins.str, typing.Any]],
        custom_data_identifier_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initial_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        job_status: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        sampling_percentage: typing.Optional[jsii.Number] = None,
        schedule_frequency: typing.Optional[typing.Union["Macie2ClassificationJobScheduleFrequency", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["Macie2ClassificationJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job aws_macie2_classification_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param job_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#job_type Macie2ClassificationJob#job_type}.
        :param s3_job_definition: s3_job_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#s3_job_definition Macie2ClassificationJob#s3_job_definition}
        :param custom_data_identifier_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#custom_data_identifier_ids Macie2ClassificationJob#custom_data_identifier_ids}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#description Macie2ClassificationJob#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#id Macie2ClassificationJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_run: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#initial_run Macie2ClassificationJob#initial_run}.
        :param job_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#job_status Macie2ClassificationJob#job_status}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#name Macie2ClassificationJob#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#name_prefix Macie2ClassificationJob#name_prefix}.
        :param sampling_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#sampling_percentage Macie2ClassificationJob#sampling_percentage}.
        :param schedule_frequency: schedule_frequency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#schedule_frequency Macie2ClassificationJob#schedule_frequency}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tags Macie2ClassificationJob#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tags_all Macie2ClassificationJob#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#timeouts Macie2ClassificationJob#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__074e2b3077ee774f620b6cc1f9412406c3851ecc74ebadee02a6c255e04a397c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Macie2ClassificationJobConfig(
            job_type=job_type,
            s3_job_definition=s3_job_definition,
            custom_data_identifier_ids=custom_data_identifier_ids,
            description=description,
            id=id,
            initial_run=initial_run,
            job_status=job_status,
            name=name,
            name_prefix=name_prefix,
            sampling_percentage=sampling_percentage,
            schedule_frequency=schedule_frequency,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a Macie2ClassificationJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Macie2ClassificationJob to import.
        :param import_from_id: The id of the existing Macie2ClassificationJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Macie2ClassificationJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ef5421e1a9b2a92eec77e984bc743f322ccc2fc3005761085ea842c02e874a7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putS3JobDefinition")
    def put_s3_job_definition(
        self,
        *,
        bucket_criteria: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        bucket_definitions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketDefinitions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scoping: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScoping", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_criteria: bucket_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#bucket_criteria Macie2ClassificationJob#bucket_criteria}
        :param bucket_definitions: bucket_definitions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#bucket_definitions Macie2ClassificationJob#bucket_definitions}
        :param scoping: scoping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#scoping Macie2ClassificationJob#scoping}
        '''
        value = Macie2ClassificationJobS3JobDefinition(
            bucket_criteria=bucket_criteria,
            bucket_definitions=bucket_definitions,
            scoping=scoping,
        )

        return typing.cast(None, jsii.invoke(self, "putS3JobDefinition", [value]))

    @jsii.member(jsii_name="putScheduleFrequency")
    def put_schedule_frequency(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monthly_schedule: typing.Optional[jsii.Number] = None,
        weekly_schedule: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param daily_schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#daily_schedule Macie2ClassificationJob#daily_schedule}.
        :param monthly_schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#monthly_schedule Macie2ClassificationJob#monthly_schedule}.
        :param weekly_schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#weekly_schedule Macie2ClassificationJob#weekly_schedule}.
        '''
        value = Macie2ClassificationJobScheduleFrequency(
            daily_schedule=daily_schedule,
            monthly_schedule=monthly_schedule,
            weekly_schedule=weekly_schedule,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduleFrequency", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#create Macie2ClassificationJob#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#update Macie2ClassificationJob#update}.
        '''
        value = Macie2ClassificationJobTimeouts(create=create, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCustomDataIdentifierIds")
    def reset_custom_data_identifier_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDataIdentifierIds", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitialRun")
    def reset_initial_run(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialRun", []))

    @jsii.member(jsii_name="resetJobStatus")
    def reset_job_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobStatus", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamePrefix")
    def reset_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamePrefix", []))

    @jsii.member(jsii_name="resetSamplingPercentage")
    def reset_sampling_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamplingPercentage", []))

    @jsii.member(jsii_name="resetScheduleFrequency")
    def reset_schedule_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleFrequency", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="jobArn")
    def job_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobArn"))

    @builtins.property
    @jsii.member(jsii_name="jobId")
    def job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobId"))

    @builtins.property
    @jsii.member(jsii_name="s3JobDefinition")
    def s3_job_definition(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionOutputReference", jsii.get(self, "s3JobDefinition"))

    @builtins.property
    @jsii.member(jsii_name="scheduleFrequency")
    def schedule_frequency(
        self,
    ) -> "Macie2ClassificationJobScheduleFrequencyOutputReference":
        return typing.cast("Macie2ClassificationJobScheduleFrequencyOutputReference", jsii.get(self, "scheduleFrequency"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "Macie2ClassificationJobTimeoutsOutputReference":
        return typing.cast("Macie2ClassificationJobTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="userPausedDetails")
    def user_paused_details(self) -> "Macie2ClassificationJobUserPausedDetailsList":
        return typing.cast("Macie2ClassificationJobUserPausedDetailsList", jsii.get(self, "userPausedDetails"))

    @builtins.property
    @jsii.member(jsii_name="customDataIdentifierIdsInput")
    def custom_data_identifier_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customDataIdentifierIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initialRunInput")
    def initial_run_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "initialRunInput"))

    @builtins.property
    @jsii.member(jsii_name="jobStatusInput")
    def job_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="jobTypeInput")
    def job_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="s3JobDefinitionInput")
    def s3_job_definition_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinition"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinition"], jsii.get(self, "s3JobDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="samplingPercentageInput")
    def sampling_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "samplingPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleFrequencyInput")
    def schedule_frequency_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobScheduleFrequency"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobScheduleFrequency"], jsii.get(self, "scheduleFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "Macie2ClassificationJobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "Macie2ClassificationJobTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="customDataIdentifierIds")
    def custom_data_identifier_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customDataIdentifierIds"))

    @custom_data_identifier_ids.setter
    def custom_data_identifier_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015542a72d4728e6f08abfdafd232c75134375f76ee49efc0143395ba103df85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDataIdentifierIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec48f1904c3b9c72eac0b112b6b35920c66cc07e39949f334d8082e9d7eb6418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb42990ad1dc41e598fc505fb4a6979204fe6bb164b65a877ffe0b053c5e0bf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialRun")
    def initial_run(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "initialRun"))

    @initial_run.setter
    def initial_run(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb3208183587112b033f44b2a0aa2d4a0743868c13d6331c89f732f7e665ddec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobStatus")
    def job_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobStatus"))

    @job_status.setter
    def job_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c28c4672ec91bc3209295e81df571074f2b563e732948d64886e0e3b08f8a3b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobType")
    def job_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobType"))

    @job_type.setter
    def job_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f4e12faf1e99c7429076958e043337c5f82d55fb9d131986327affa64f34d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__259373f8d71b7410008529a6f9e14b3cc7bf829d276dbf527e17b1616d9ed23b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1cb35c4eb7f08c7677dfc16a8f6edf46fa231da0085263d9e919967d24296ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samplingPercentage")
    def sampling_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "samplingPercentage"))

    @sampling_percentage.setter
    def sampling_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b3a0c97b519d850ab1bc69022ce854c480ae30abacb55682a3c1368d325d04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__369e9bb2edb070277206519175176d6a6780d18d65fe17570727236ba998dcd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361553db7331d294d672c7d77c6b7f4f20496a9a49c2de671d2d936a07ebd972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "job_type": "jobType",
        "s3_job_definition": "s3JobDefinition",
        "custom_data_identifier_ids": "customDataIdentifierIds",
        "description": "description",
        "id": "id",
        "initial_run": "initialRun",
        "job_status": "jobStatus",
        "name": "name",
        "name_prefix": "namePrefix",
        "sampling_percentage": "samplingPercentage",
        "schedule_frequency": "scheduleFrequency",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class Macie2ClassificationJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        job_type: builtins.str,
        s3_job_definition: typing.Union["Macie2ClassificationJobS3JobDefinition", typing.Dict[builtins.str, typing.Any]],
        custom_data_identifier_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initial_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        job_status: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        sampling_percentage: typing.Optional[jsii.Number] = None,
        schedule_frequency: typing.Optional[typing.Union["Macie2ClassificationJobScheduleFrequency", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["Macie2ClassificationJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param job_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#job_type Macie2ClassificationJob#job_type}.
        :param s3_job_definition: s3_job_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#s3_job_definition Macie2ClassificationJob#s3_job_definition}
        :param custom_data_identifier_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#custom_data_identifier_ids Macie2ClassificationJob#custom_data_identifier_ids}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#description Macie2ClassificationJob#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#id Macie2ClassificationJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_run: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#initial_run Macie2ClassificationJob#initial_run}.
        :param job_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#job_status Macie2ClassificationJob#job_status}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#name Macie2ClassificationJob#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#name_prefix Macie2ClassificationJob#name_prefix}.
        :param sampling_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#sampling_percentage Macie2ClassificationJob#sampling_percentage}.
        :param schedule_frequency: schedule_frequency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#schedule_frequency Macie2ClassificationJob#schedule_frequency}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tags Macie2ClassificationJob#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tags_all Macie2ClassificationJob#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#timeouts Macie2ClassificationJob#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(s3_job_definition, dict):
            s3_job_definition = Macie2ClassificationJobS3JobDefinition(**s3_job_definition)
        if isinstance(schedule_frequency, dict):
            schedule_frequency = Macie2ClassificationJobScheduleFrequency(**schedule_frequency)
        if isinstance(timeouts, dict):
            timeouts = Macie2ClassificationJobTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68bbc2ccb85df1a30f0d752ee6f96898edc52b0aa030052cd0aefb93a22a59c3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument job_type", value=job_type, expected_type=type_hints["job_type"])
            check_type(argname="argument s3_job_definition", value=s3_job_definition, expected_type=type_hints["s3_job_definition"])
            check_type(argname="argument custom_data_identifier_ids", value=custom_data_identifier_ids, expected_type=type_hints["custom_data_identifier_ids"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument initial_run", value=initial_run, expected_type=type_hints["initial_run"])
            check_type(argname="argument job_status", value=job_status, expected_type=type_hints["job_status"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument sampling_percentage", value=sampling_percentage, expected_type=type_hints["sampling_percentage"])
            check_type(argname="argument schedule_frequency", value=schedule_frequency, expected_type=type_hints["schedule_frequency"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job_type": job_type,
            "s3_job_definition": s3_job_definition,
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
        if custom_data_identifier_ids is not None:
            self._values["custom_data_identifier_ids"] = custom_data_identifier_ids
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if initial_run is not None:
            self._values["initial_run"] = initial_run
        if job_status is not None:
            self._values["job_status"] = job_status
        if name is not None:
            self._values["name"] = name
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if sampling_percentage is not None:
            self._values["sampling_percentage"] = sampling_percentage
        if schedule_frequency is not None:
            self._values["schedule_frequency"] = schedule_frequency
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
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
    def job_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#job_type Macie2ClassificationJob#job_type}.'''
        result = self._values.get("job_type")
        assert result is not None, "Required property 'job_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_job_definition(self) -> "Macie2ClassificationJobS3JobDefinition":
        '''s3_job_definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#s3_job_definition Macie2ClassificationJob#s3_job_definition}
        '''
        result = self._values.get("s3_job_definition")
        assert result is not None, "Required property 's3_job_definition' is missing"
        return typing.cast("Macie2ClassificationJobS3JobDefinition", result)

    @builtins.property
    def custom_data_identifier_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#custom_data_identifier_ids Macie2ClassificationJob#custom_data_identifier_ids}.'''
        result = self._values.get("custom_data_identifier_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#description Macie2ClassificationJob#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#id Macie2ClassificationJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_run(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#initial_run Macie2ClassificationJob#initial_run}.'''
        result = self._values.get("initial_run")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def job_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#job_status Macie2ClassificationJob#job_status}.'''
        result = self._values.get("job_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#name Macie2ClassificationJob#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#name_prefix Macie2ClassificationJob#name_prefix}.'''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sampling_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#sampling_percentage Macie2ClassificationJob#sampling_percentage}.'''
        result = self._values.get("sampling_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def schedule_frequency(
        self,
    ) -> typing.Optional["Macie2ClassificationJobScheduleFrequency"]:
        '''schedule_frequency block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#schedule_frequency Macie2ClassificationJob#schedule_frequency}
        '''
        result = self._values.get("schedule_frequency")
        return typing.cast(typing.Optional["Macie2ClassificationJobScheduleFrequency"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tags Macie2ClassificationJob#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tags_all Macie2ClassificationJob#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["Macie2ClassificationJobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#timeouts Macie2ClassificationJob#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["Macie2ClassificationJobTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_criteria": "bucketCriteria",
        "bucket_definitions": "bucketDefinitions",
        "scoping": "scoping",
    },
)
class Macie2ClassificationJobS3JobDefinition:
    def __init__(
        self,
        *,
        bucket_criteria: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        bucket_definitions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketDefinitions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scoping: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScoping", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_criteria: bucket_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#bucket_criteria Macie2ClassificationJob#bucket_criteria}
        :param bucket_definitions: bucket_definitions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#bucket_definitions Macie2ClassificationJob#bucket_definitions}
        :param scoping: scoping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#scoping Macie2ClassificationJob#scoping}
        '''
        if isinstance(bucket_criteria, dict):
            bucket_criteria = Macie2ClassificationJobS3JobDefinitionBucketCriteria(**bucket_criteria)
        if isinstance(scoping, dict):
            scoping = Macie2ClassificationJobS3JobDefinitionScoping(**scoping)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad40965da313a91c882dc3e9e9d9cb38cfdc3b196b66a9d5a17586851ea0029c)
            check_type(argname="argument bucket_criteria", value=bucket_criteria, expected_type=type_hints["bucket_criteria"])
            check_type(argname="argument bucket_definitions", value=bucket_definitions, expected_type=type_hints["bucket_definitions"])
            check_type(argname="argument scoping", value=scoping, expected_type=type_hints["scoping"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_criteria is not None:
            self._values["bucket_criteria"] = bucket_criteria
        if bucket_definitions is not None:
            self._values["bucket_definitions"] = bucket_definitions
        if scoping is not None:
            self._values["scoping"] = scoping

    @builtins.property
    def bucket_criteria(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteria"]:
        '''bucket_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#bucket_criteria Macie2ClassificationJob#bucket_criteria}
        '''
        result = self._values.get("bucket_criteria")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteria"], result)

    @builtins.property
    def bucket_definitions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketDefinitions"]]]:
        '''bucket_definitions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#bucket_definitions Macie2ClassificationJob#bucket_definitions}
        '''
        result = self._values.get("bucket_definitions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketDefinitions"]]], result)

    @builtins.property
    def scoping(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScoping"]:
        '''scoping block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#scoping Macie2ClassificationJob#scoping}
        '''
        result = self._values.get("scoping")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScoping"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteria",
    jsii_struct_bases=[],
    name_mapping={"excludes": "excludes", "includes": "includes"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteria:
    def __init__(
        self,
        *,
        excludes: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes", typing.Dict[builtins.str, typing.Any]]] = None,
        includes: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excludes: excludes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#excludes Macie2ClassificationJob#excludes}
        :param includes: includes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#includes Macie2ClassificationJob#includes}
        '''
        if isinstance(excludes, dict):
            excludes = Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes(**excludes)
        if isinstance(includes, dict):
            includes = Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes(**includes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce8fd18dd916a2ea1fd8bf2c57f29559905ba77be636eaa56d1b6f75f19d8157)
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excludes is not None:
            self._values["excludes"] = excludes
        if includes is not None:
            self._values["includes"] = includes

    @builtins.property
    def excludes(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes"]:
        '''excludes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#excludes Macie2ClassificationJob#excludes}
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes"], result)

    @builtins.property
    def includes(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes"]:
        '''includes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#includes Macie2ClassificationJob#includes}
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes",
    jsii_struct_bases=[],
    name_mapping={"and_": "and"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes:
    def __init__(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b5f05d65c2721145266103c75bc032cbd88b3ab9d1315b55fb049ce1cb80f1)
            check_type(argname="argument and_", value=and_, expected_type=type_hints["and_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if and_ is not None:
            self._values["and_"] = and_

    @builtins.property
    def and_(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd"]]]:
        '''and block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        result = self._values.get("and_")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd",
    jsii_struct_bases=[],
    name_mapping={
        "simple_criterion": "simpleCriterion",
        "tag_criterion": "tagCriterion",
    },
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd:
    def __init__(
        self,
        *,
        simple_criterion: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_criterion: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param simple_criterion: simple_criterion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#simple_criterion Macie2ClassificationJob#simple_criterion}
        :param tag_criterion: tag_criterion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_criterion Macie2ClassificationJob#tag_criterion}
        '''
        if isinstance(simple_criterion, dict):
            simple_criterion = Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion(**simple_criterion)
        if isinstance(tag_criterion, dict):
            tag_criterion = Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion(**tag_criterion)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b253dd7a5ac96ffe8f8031cb272823be37e2eb3adcbd1b6abc4a4cc51f9bc3)
            check_type(argname="argument simple_criterion", value=simple_criterion, expected_type=type_hints["simple_criterion"])
            check_type(argname="argument tag_criterion", value=tag_criterion, expected_type=type_hints["tag_criterion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if simple_criterion is not None:
            self._values["simple_criterion"] = simple_criterion
        if tag_criterion is not None:
            self._values["tag_criterion"] = tag_criterion

    @builtins.property
    def simple_criterion(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion"]:
        '''simple_criterion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#simple_criterion Macie2ClassificationJob#simple_criterion}
        '''
        result = self._values.get("simple_criterion")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion"], result)

    @builtins.property
    def tag_criterion(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion"]:
        '''tag_criterion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_criterion Macie2ClassificationJob#tag_criterion}
        '''
        result = self._values.get("tag_criterion")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b45012d6cef7d438296a14ac7bb5aeb28779ac49a8021b4f2ce6b6310638517)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd147552c3505853a73cfac69ffdabfc04fd7086d0d3c25a9a06d3c807aa2dc0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef50feebf5b834b1116d3b2dd62d790ded3fdefda702c5e52b5b63d14869ea34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af6786b2af3d2e9170e3a180e53cd1de71cdc42dc9580659e2e03236d6367f09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__817a8427b489639ce58480b8f05d4b62c38ed6a6933068bb3fe039ecb8bc1889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81eda7c267c142989f16affa584ad4d4883b8162a619eeb85bf2116377c8590f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a1b840e167eef613b67e9d71f256e770361694397ef7fb8a922ef7c2e4c072a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSimpleCriterion")
    def put_simple_criterion(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        value = Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion(
            comparator=comparator, key=key, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putSimpleCriterion", [value]))

    @jsii.member(jsii_name="putTagCriterion")
    def put_tag_criterion(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        value = Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion(
            comparator=comparator, tag_values=tag_values
        )

        return typing.cast(None, jsii.invoke(self, "putTagCriterion", [value]))

    @jsii.member(jsii_name="resetSimpleCriterion")
    def reset_simple_criterion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSimpleCriterion", []))

    @jsii.member(jsii_name="resetTagCriterion")
    def reset_tag_criterion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagCriterion", []))

    @builtins.property
    @jsii.member(jsii_name="simpleCriterion")
    def simple_criterion(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterionOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterionOutputReference", jsii.get(self, "simpleCriterion"))

    @builtins.property
    @jsii.member(jsii_name="tagCriterion")
    def tag_criterion(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionOutputReference", jsii.get(self, "tagCriterion"))

    @builtins.property
    @jsii.member(jsii_name="simpleCriterionInput")
    def simple_criterion_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion"], jsii.get(self, "simpleCriterionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagCriterionInput")
    def tag_criterion_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion"], jsii.get(self, "tagCriterionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bdef3fce821f61aec7cbebd9b2ee4734012ce65b41f68abde5ba8aa4ffc64e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion",
    jsii_struct_bases=[],
    name_mapping={"comparator": "comparator", "key": "key", "values": "values"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ea36ffa3cb30a7afd7185dd08b4ebc11781016ad4a5f51a50d9ede111b3c01d)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if key is not None:
            self._values["key"] = key
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18402509939cfb8e22271e24cff9c942895d232327303d7c391f86bfac4d6982)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474f276886672aedee3b14e58340a3a57c0ec1828c749b52501ff7a6836eb7ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e6a7dd53d66fa75761115cf2aac4369066621afd85fef0c78dbd8099057fd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354a8e0016512d85bd53a1589e25da5820f44d4e6efd52eaad1bc38dcefae157)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a50a6fa71504f5e7a62883ce2c0c56288ddd5b95fed17e0eb10593180b7d0be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion",
    jsii_struct_bases=[],
    name_mapping={"comparator": "comparator", "tag_values": "tagValues"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d11c64b77011f33ffec42761f901141728bab2c500f7fadd2f393a86a882737)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if tag_values is not None:
            self._values["tag_values"] = tag_values

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_values(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues"]]]:
        '''tag_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        result = self._values.get("tag_values")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ee61c9f762b1d02985cf351a5f3cdd98f06ed81a79b13aba96b7a0c76bc5813)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTagValues")
    def put_tag_values(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f95292532b2aff87a878a1417ecafc40dad1364625fd02757cde94fd5b0e9133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTagValues", [value]))

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetTagValues")
    def reset_tag_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValues", []))

    @builtins.property
    @jsii.member(jsii_name="tagValues")
    def tag_values(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesList":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesList", jsii.get(self, "tagValues"))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValuesInput")
    def tag_values_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues"]]], jsii.get(self, "tagValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b019d6800fde8b26526d0e0df38151f14f7da42505656b9b5842a4ba0e393c47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5904a33e24db06728a37df3aba2a601599f9935c3ff9f43dd8210d17e6a99e09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441eb7686726d117b67f558b1e9f344f2b2804210e884dbb6c287c63aeb934f6)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e317e38b8ef150c85b4a43e9a9177691f06b59e6c4e3b2fe8c7dd3cd3cde9bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98803a4ccddabd0d8b45f4015b12e086e717735236cad8759ad1d37918d024c8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d22c8877bce1a4b5f0656ba8943b78e7d9aeac1aefec331f2f291324d3c8169)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0234a77a6d74a4c4cecddb4b9c6f8448f4852f528f7936d6c1de323f50d816d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3662eba0a2c9eaf051ac4c09e25c3418a81cccbc31647750b34ab937906f1f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c92153ed27f11fcaaee63ccfb2833eee890676fe48775cb7f7a6bb5b6994d7ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2232978e7f3fc8a1273887c860ade64f74b08552b075276b0c8cf2a567bc7f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc8c4a344fa1cad8cf9202587e8350af15738ed147b40918187b092faa091f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b394ed52d3d5ee8aac19fc79d25294144b8d8419d5c072a0d5e3a840ce3c593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7bfef37608541fbfaf2d9a7d5c15d910ad12d97baa0ed5e66848ca0a1d84daa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06e9b40b1c8e6bc4f3b130a5f30dacaebdc5b20c5ed5535a4c074a3aa5dbea55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAnd")
    def put_and(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__372e59744d67b077978eedc67f6f6f2a5ac8d5ba400afa83159b156a6e22fba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnd", [value]))

    @jsii.member(jsii_name="resetAnd")
    def reset_and(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnd", []))

    @builtins.property
    @jsii.member(jsii_name="and")
    def and_(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndList:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndList, jsii.get(self, "and"))

    @builtins.property
    @jsii.member(jsii_name="andInput")
    def and_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]]], jsii.get(self, "andInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f1a8dc3c077ccf3fa76bede80de45970fd1804b37ecc2e81d925530659e623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes",
    jsii_struct_bases=[],
    name_mapping={"and_": "and"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes:
    def __init__(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a24eb836e16e152312aee8a31a78b3c847dbff772464e5d3f29c5aad4d7a602)
            check_type(argname="argument and_", value=and_, expected_type=type_hints["and_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if and_ is not None:
            self._values["and_"] = and_

    @builtins.property
    def and_(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd"]]]:
        '''and block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        result = self._values.get("and_")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd",
    jsii_struct_bases=[],
    name_mapping={
        "simple_criterion": "simpleCriterion",
        "tag_criterion": "tagCriterion",
    },
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd:
    def __init__(
        self,
        *,
        simple_criterion: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_criterion: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param simple_criterion: simple_criterion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#simple_criterion Macie2ClassificationJob#simple_criterion}
        :param tag_criterion: tag_criterion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_criterion Macie2ClassificationJob#tag_criterion}
        '''
        if isinstance(simple_criterion, dict):
            simple_criterion = Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion(**simple_criterion)
        if isinstance(tag_criterion, dict):
            tag_criterion = Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion(**tag_criterion)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f5025f719310e64962f62fe1c530956bcf900af0de7e1ccbc3ef19e9c90cf55)
            check_type(argname="argument simple_criterion", value=simple_criterion, expected_type=type_hints["simple_criterion"])
            check_type(argname="argument tag_criterion", value=tag_criterion, expected_type=type_hints["tag_criterion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if simple_criterion is not None:
            self._values["simple_criterion"] = simple_criterion
        if tag_criterion is not None:
            self._values["tag_criterion"] = tag_criterion

    @builtins.property
    def simple_criterion(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion"]:
        '''simple_criterion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#simple_criterion Macie2ClassificationJob#simple_criterion}
        '''
        result = self._values.get("simple_criterion")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion"], result)

    @builtins.property
    def tag_criterion(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion"]:
        '''tag_criterion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_criterion Macie2ClassificationJob#tag_criterion}
        '''
        result = self._values.get("tag_criterion")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ab1c85b4c905042419ee0eddb23ab0d88026b381e86eb3e480fc61b8531a65c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1386694d3502432dbc5d89966b480125822feec7fd4157456c5e32e206509cc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc82921d7b2bf9aa8aff45e3d8f1036f6321331b43e1b915c5f0514b49748e32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ad823b055fa032997456cba9ca5a327fb59f45dd57b915964fffc224f59b7c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb39ffebc2747bcbcb5df60a72ef0f06ab355e45cc8f0103e12622e13e0d47e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da41de78a5ec610a1550df266aa9d2cc601691f385088b2ec7369723d5f12f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9df38667a39a6be3cc1c13ebaed996e2871871f89e489152b3603f44825af13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSimpleCriterion")
    def put_simple_criterion(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        value = Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion(
            comparator=comparator, key=key, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putSimpleCriterion", [value]))

    @jsii.member(jsii_name="putTagCriterion")
    def put_tag_criterion(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        value = Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion(
            comparator=comparator, tag_values=tag_values
        )

        return typing.cast(None, jsii.invoke(self, "putTagCriterion", [value]))

    @jsii.member(jsii_name="resetSimpleCriterion")
    def reset_simple_criterion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSimpleCriterion", []))

    @jsii.member(jsii_name="resetTagCriterion")
    def reset_tag_criterion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagCriterion", []))

    @builtins.property
    @jsii.member(jsii_name="simpleCriterion")
    def simple_criterion(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterionOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterionOutputReference", jsii.get(self, "simpleCriterion"))

    @builtins.property
    @jsii.member(jsii_name="tagCriterion")
    def tag_criterion(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionOutputReference", jsii.get(self, "tagCriterion"))

    @builtins.property
    @jsii.member(jsii_name="simpleCriterionInput")
    def simple_criterion_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion"], jsii.get(self, "simpleCriterionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagCriterionInput")
    def tag_criterion_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion"], jsii.get(self, "tagCriterionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264e3f8098ecba16cb05ac8e26e1dab7fb12bb30cba6af1a6d1cab1010a96f67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion",
    jsii_struct_bases=[],
    name_mapping={"comparator": "comparator", "key": "key", "values": "values"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1373ed675b01025e33806777b0e2ee70184cb252d2a1cf5bbaa7285dd37ea6)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if key is not None:
            self._values["key"] = key
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb04cf23a1cfb9e03fcaa7583d779a0dc5d15d87c88e11fc854fb9ad741b6db2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cfb5a67e352e63030d764bd83e7e7c8264bf9136ea93e8a8fb8f2e048e0945b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749413920a8f7afa91a91413b53a9e207ed6c6b36a2317932bb20972f875741a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1b1b14d47c2eab97443c2f2c49b5682e938bbaae96333fb65e5b9fe3026fa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de062c01657297679dc0d125090431b77cd4ffc92f10e2718f604e2096b6be91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion",
    jsii_struct_bases=[],
    name_mapping={"comparator": "comparator", "tag_values": "tagValues"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b132989bc20c80d382925e4974a7e3083fa5c9b48721ff1cf14473542b787e9)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if tag_values is not None:
            self._values["tag_values"] = tag_values

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_values(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues"]]]:
        '''tag_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        result = self._values.get("tag_values")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3826c0416dc30cd07c8fd0930a5f935496b29fab58c10a675cf52c0f4702b897)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTagValues")
    def put_tag_values(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574eca5171683894f4b6add03c08e9ef0b20da5456b75969692682d55ac5bd3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTagValues", [value]))

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetTagValues")
    def reset_tag_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValues", []))

    @builtins.property
    @jsii.member(jsii_name="tagValues")
    def tag_values(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesList":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesList", jsii.get(self, "tagValues"))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValuesInput")
    def tag_values_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues"]]], jsii.get(self, "tagValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be590e2e1460572bdc982cb4872f777ddd1427bee739dd09f5a838ce78b81cc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df2c07ca8400f0ae399d241960968e1e876646f83a36e2fc476d1695e56e3304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caeffee2e9f83f80faaecfb0be3bce0519d4fd46619ceed2ddf253baa280b790)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91408c987cdecf8d2cea946fd27072ae628ec7d6adaa1e8865933d3b306889a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e01c2a67c4968f04d69e72f1713d94cdcad0bd001613ad588a1007f14eea008)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23916b61ffe9d4b4e6772d0554c93a4769c87bf2170baf6ea0985f937d4c8d3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31b385edb1a339fa7d41cad54dbb73b251efa1cdc250597e6a353973141b53e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc7c026e66111d7c90e59c0c16c281cfd20e81ff7b42ca827ae1b96ed6c636b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fdd9cc1c2ff009c10192bbd50ac44844141a6c433449acd17ed0cef957645ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bf9b247be3ec268e71843d928ec3c8300070e4203c7a5682ab9b5a958755e67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f71762d1173290aca3e6c250872750a743e8d856673fddb3985bef4531756b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5a3274bd7332490a2d2f0af421274c63bfde48c1323221d972b98744415fd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__365d9551842400fa2a1ae23109e42d57e4eb798fcc28a4c1bb536f25ac69948e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbe2c18784c9b211c235d5ef6dad3cbdd4eb728ecc33fc11acd12162570f0247)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAnd")
    def put_and(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2221b3c68bf15876c10043d5edb015b3236ef9e6c09509cf6553328ebe8aa1c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnd", [value]))

    @jsii.member(jsii_name="resetAnd")
    def reset_and(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnd", []))

    @builtins.property
    @jsii.member(jsii_name="and")
    def and_(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndList:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndList, jsii.get(self, "and"))

    @builtins.property
    @jsii.member(jsii_name="andInput")
    def and_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]]], jsii.get(self, "andInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2b21d96c1fb534135939d4ff7ab9ad65c889da4c732a4193cfeee30da8a6b91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__727faffbdb928857d42a28ff2aedbdf666f3818db90e30e738d3c91b8d1478fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExcludes")
    def put_excludes(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        value = Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes(and_=and_)

        return typing.cast(None, jsii.invoke(self, "putExcludes", [value]))

    @jsii.member(jsii_name="putIncludes")
    def put_includes(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        value = Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes(and_=and_)

        return typing.cast(None, jsii.invoke(self, "putIncludes", [value]))

    @jsii.member(jsii_name="resetExcludes")
    def reset_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludes", []))

    @jsii.member(jsii_name="resetIncludes")
    def reset_includes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludes", []))

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesOutputReference:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesOutputReference, jsii.get(self, "excludes"))

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesOutputReference:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesOutputReference, jsii.get(self, "includes"))

    @builtins.property
    @jsii.member(jsii_name="excludesInput")
    def excludes_input(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes], jsii.get(self, "excludesInput"))

    @builtins.property
    @jsii.member(jsii_name="includesInput")
    def includes_input(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes], jsii.get(self, "includesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteria]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb994e7b075369ed83ff3028bc789da07d96371250fd92e0d39fce7edcc69d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketDefinitions",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId", "buckets": "buckets"},
)
class Macie2ClassificationJobS3JobDefinitionBucketDefinitions:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        buckets: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#account_id Macie2ClassificationJob#account_id}.
        :param buckets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#buckets Macie2ClassificationJob#buckets}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0749a2f40360dd2866cee3123009bc78e57ea68b9080e9e9c33da749395be3d1)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument buckets", value=buckets, expected_type=type_hints["buckets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "buckets": buckets,
        }

    @builtins.property
    def account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#account_id Macie2ClassificationJob#account_id}.'''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def buckets(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#buckets Macie2ClassificationJob#buckets}.'''
        result = self._values.get("buckets")
        assert result is not None, "Required property 'buckets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketDefinitions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketDefinitionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketDefinitionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93e421defeadde00db95b630324223db07a2b45a339716edf23312df89e911d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketDefinitionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ec1a5b244e5aff866cd1b5b4734fde741a9e45029303d6527801e4ec6ab088)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketDefinitionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62087dcaa77d2f6808045b3ee0efdccb338897722c1ef0dfc4d6b828e9c529be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22648dca569b916725b80622eb01655574a0fa83b9ebaa87be393be522410c3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__875c43d00751b62281f4809889b9291252ff37fc1e7f50de674465cec57d4335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketDefinitions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketDefinitions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketDefinitions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3c9783dcbe702f2fc3c22ab002624162c0770ebc2dea72bd58c8e92812cfbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketDefinitionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketDefinitionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a27d1413237b72c4cfb32bc0fc5725e7bb9272f3d6fbbdefb6c579996773b114)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketsInput")
    def buckets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "bucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28a6f82ebb5555beda36bac8876b453be46d51710739ca8f0bee2900e51792e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buckets")
    def buckets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "buckets"))

    @buckets.setter
    def buckets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ab000b12f7d3364a09b5afe3222c912788183143d9e9a318f8af109c08825e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buckets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketDefinitions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketDefinitions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketDefinitions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bccf4379dd4728efcc2929ad8db0d7f1e49f3d82d5ebdc5b40fb7b3611d4bb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6220f8fc88e0e91e09102d6a55ba608d0a1ba9afcc7b160e1f8ea505e75883fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBucketCriteria")
    def put_bucket_criteria(
        self,
        *,
        excludes: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes, typing.Dict[builtins.str, typing.Any]]] = None,
        includes: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excludes: excludes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#excludes Macie2ClassificationJob#excludes}
        :param includes: includes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#includes Macie2ClassificationJob#includes}
        '''
        value = Macie2ClassificationJobS3JobDefinitionBucketCriteria(
            excludes=excludes, includes=includes
        )

        return typing.cast(None, jsii.invoke(self, "putBucketCriteria", [value]))

    @jsii.member(jsii_name="putBucketDefinitions")
    def put_bucket_definitions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketDefinitions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a5725ede8c5278fb290318c10bc3e0df831608df80f98addce04ed92a76aff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBucketDefinitions", [value]))

    @jsii.member(jsii_name="putScoping")
    def put_scoping(
        self,
        *,
        excludes: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludes", typing.Dict[builtins.str, typing.Any]]] = None,
        includes: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excludes: excludes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#excludes Macie2ClassificationJob#excludes}
        :param includes: includes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#includes Macie2ClassificationJob#includes}
        '''
        value = Macie2ClassificationJobS3JobDefinitionScoping(
            excludes=excludes, includes=includes
        )

        return typing.cast(None, jsii.invoke(self, "putScoping", [value]))

    @jsii.member(jsii_name="resetBucketCriteria")
    def reset_bucket_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketCriteria", []))

    @jsii.member(jsii_name="resetBucketDefinitions")
    def reset_bucket_definitions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketDefinitions", []))

    @jsii.member(jsii_name="resetScoping")
    def reset_scoping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScoping", []))

    @builtins.property
    @jsii.member(jsii_name="bucketCriteria")
    def bucket_criteria(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionBucketCriteriaOutputReference:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionBucketCriteriaOutputReference, jsii.get(self, "bucketCriteria"))

    @builtins.property
    @jsii.member(jsii_name="bucketDefinitions")
    def bucket_definitions(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionBucketDefinitionsList:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionBucketDefinitionsList, jsii.get(self, "bucketDefinitions"))

    @builtins.property
    @jsii.member(jsii_name="scoping")
    def scoping(self) -> "Macie2ClassificationJobS3JobDefinitionScopingOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingOutputReference", jsii.get(self, "scoping"))

    @builtins.property
    @jsii.member(jsii_name="bucketCriteriaInput")
    def bucket_criteria_input(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteria]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteria], jsii.get(self, "bucketCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketDefinitionsInput")
    def bucket_definitions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketDefinitions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketDefinitions]]], jsii.get(self, "bucketDefinitionsInput"))

    @builtins.property
    @jsii.member(jsii_name="scopingInput")
    def scoping_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScoping"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScoping"], jsii.get(self, "scopingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Macie2ClassificationJobS3JobDefinition]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9519678e184c9a265f9c1cdad33f61470cd8764da0abe72d77a037bf3479e71f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScoping",
    jsii_struct_bases=[],
    name_mapping={"excludes": "excludes", "includes": "includes"},
)
class Macie2ClassificationJobS3JobDefinitionScoping:
    def __init__(
        self,
        *,
        excludes: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludes", typing.Dict[builtins.str, typing.Any]]] = None,
        includes: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excludes: excludes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#excludes Macie2ClassificationJob#excludes}
        :param includes: includes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#includes Macie2ClassificationJob#includes}
        '''
        if isinstance(excludes, dict):
            excludes = Macie2ClassificationJobS3JobDefinitionScopingExcludes(**excludes)
        if isinstance(includes, dict):
            includes = Macie2ClassificationJobS3JobDefinitionScopingIncludes(**includes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d4ad3d8f0fc1a8893807a79b677383b5f63ec74e367118fb76c92981408d234)
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excludes is not None:
            self._values["excludes"] = excludes
        if includes is not None:
            self._values["includes"] = includes

    @builtins.property
    def excludes(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludes"]:
        '''excludes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#excludes Macie2ClassificationJob#excludes}
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludes"], result)

    @builtins.property
    def includes(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludes"]:
        '''includes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#includes Macie2ClassificationJob#includes}
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludes"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScoping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludes",
    jsii_struct_bases=[],
    name_mapping={"and_": "and"},
)
class Macie2ClassificationJobS3JobDefinitionScopingExcludes:
    def __init__(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dba534096041adfe43905ed364573baa4117ff5efe41d26fb6c02ae17547478)
            check_type(argname="argument and_", value=and_, expected_type=type_hints["and_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if and_ is not None:
            self._values["and_"] = and_

    @builtins.property
    def and_(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd"]]]:
        '''and block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        result = self._values.get("and_")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingExcludes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd",
    jsii_struct_bases=[],
    name_mapping={
        "simple_scope_term": "simpleScopeTerm",
        "tag_scope_term": "tagScopeTerm",
    },
)
class Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd:
    def __init__(
        self,
        *,
        simple_scope_term: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_scope_term: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param simple_scope_term: simple_scope_term block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#simple_scope_term Macie2ClassificationJob#simple_scope_term}
        :param tag_scope_term: tag_scope_term block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_scope_term Macie2ClassificationJob#tag_scope_term}
        '''
        if isinstance(simple_scope_term, dict):
            simple_scope_term = Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm(**simple_scope_term)
        if isinstance(tag_scope_term, dict):
            tag_scope_term = Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm(**tag_scope_term)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279ee517ea574ce4ca8e301f50a67b039622868d3c1cd28368b33e4b010bea35)
            check_type(argname="argument simple_scope_term", value=simple_scope_term, expected_type=type_hints["simple_scope_term"])
            check_type(argname="argument tag_scope_term", value=tag_scope_term, expected_type=type_hints["tag_scope_term"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if simple_scope_term is not None:
            self._values["simple_scope_term"] = simple_scope_term
        if tag_scope_term is not None:
            self._values["tag_scope_term"] = tag_scope_term

    @builtins.property
    def simple_scope_term(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm"]:
        '''simple_scope_term block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#simple_scope_term Macie2ClassificationJob#simple_scope_term}
        '''
        result = self._values.get("simple_scope_term")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm"], result)

    @builtins.property
    def tag_scope_term(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm"]:
        '''tag_scope_term block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_scope_term Macie2ClassificationJob#tag_scope_term}
        '''
        result = self._values.get("tag_scope_term")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ad7531638004a07c0966a1fabb94a5878b53bd42b2cc8ecddb2247dba9c13bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a5448e3aa0140d0ae044f14eee73b6504778f6cc028d931a3f118c1bfca45a2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingExcludesAndOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3bfcafbd43be9ff3b44dbabb017a57fb3a312fa4a99b222e900b210c705dfcb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a93b5dc1af91838a949528f2ad76c1f49c50eac8b78614334d29b13da452d56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__472db1921a847501c5a11294e711b3b17d06e7ba1de8fe73190f4916a7ce84dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d6769943ec9614fc96b5c1ccae5ee89b176f7734191f0778183e2d6e1e4e541)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5fd87cc259fa46424055344babdceea7d25de553e855b6e6eb1a4c828ef0136)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSimpleScopeTerm")
    def put_simple_scope_term(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        value = Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm(
            comparator=comparator, key=key, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putSimpleScopeTerm", [value]))

    @jsii.member(jsii_name="putTagScopeTerm")
    def put_tag_scope_term(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#target Macie2ClassificationJob#target}.
        '''
        value = Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm(
            comparator=comparator, key=key, tag_values=tag_values, target=target
        )

        return typing.cast(None, jsii.invoke(self, "putTagScopeTerm", [value]))

    @jsii.member(jsii_name="resetSimpleScopeTerm")
    def reset_simple_scope_term(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSimpleScopeTerm", []))

    @jsii.member(jsii_name="resetTagScopeTerm")
    def reset_tag_scope_term(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagScopeTerm", []))

    @builtins.property
    @jsii.member(jsii_name="simpleScopeTerm")
    def simple_scope_term(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTermOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTermOutputReference", jsii.get(self, "simpleScopeTerm"))

    @builtins.property
    @jsii.member(jsii_name="tagScopeTerm")
    def tag_scope_term(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermOutputReference", jsii.get(self, "tagScopeTerm"))

    @builtins.property
    @jsii.member(jsii_name="simpleScopeTermInput")
    def simple_scope_term_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm"], jsii.get(self, "simpleScopeTermInput"))

    @builtins.property
    @jsii.member(jsii_name="tagScopeTermInput")
    def tag_scope_term_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm"], jsii.get(self, "tagScopeTermInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e291fd29ba3923fb205db59cba385a15cf553c38d1adbde95e1232d45339ba21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm",
    jsii_struct_bases=[],
    name_mapping={"comparator": "comparator", "key": "key", "values": "values"},
)
class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2169c8aa72d83203d7bdbf0be49853bcb673efef6d723e93fc78f95987bba57)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if key is not None:
            self._values["key"] = key
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTermOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTermOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3ace96ab0df7fe5e7285f14a8331e2bbbdd71fdf3df57536b7cc86d7b5d8115)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21b47a96044480241d9c5fd43e446bbc9d4eabf7ba5c80bd38cbcfb224b9622f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2375fb51185915850825a73fdd35c392133dc8dd63180c16efe02c2794739dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73a8c55ea97392c9fcd5703958600cbad61b66558bb3deb83c6fed75c4e3e05d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ff693f7c6401d27c83071a2571e436046a0e29bd98b254dc0fbf58318398ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm",
    jsii_struct_bases=[],
    name_mapping={
        "comparator": "comparator",
        "key": "key",
        "tag_values": "tagValues",
        "target": "target",
    },
)
class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#target Macie2ClassificationJob#target}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf8588b063e92ba2d4311f2dc6b95a8726949ef1f175504a6c34d51deef77b9)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if key is not None:
            self._values["key"] = key
        if tag_values is not None:
            self._values["tag_values"] = tag_values
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_values(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues"]]]:
        '''tag_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        result = self._values.get("tag_values")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues"]]], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#target Macie2ClassificationJob#target}.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c7599aece3e904fd87465959aba49ab6d524a34b01708651b20e7ef28374743)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTagValues")
    def put_tag_values(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d3aa953f834f473c2c333b212237ff3978a603773b59be62ffc95ce432dc12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTagValues", [value]))

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetTagValues")
    def reset_tag_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValues", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="tagValues")
    def tag_values(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesList":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesList", jsii.get(self, "tagValues"))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValuesInput")
    def tag_values_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues"]]], jsii.get(self, "tagValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc34be28a84facd2b375c8370c2b48038e4ce8cf93e0d1312c4a9cee99f9169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e1afed1b501dfbc8b8c205c368736fadf0da8fbcc0b31ff9b49b443b0d51a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88da5204047ac2dac5ffa345ad8eaddf5364f8a6f4f85dddccb9b0bdb8e0c9bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb9f252568df9f30501e43f50138cca06d9d4360b2db84efa18ef842caf7d07c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__678de4371fda9e8a20bb062d4460b38f2e85e199a508ed0ccc788702983f5fe2)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ac9246eaeeff8267458ad6cf92788f2e62a5b3608530082a8535d282467b923)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13270778c9e7d5f86462133084868d4bfcd1cd7834310124a39e7c2849f7467e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6553c8165cc48b9c0010f798df1e4da5fad0635d8526f7d97a52952eb7940e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0509e200c78dccba47c68167bfaa3204bf5d999f676fd5dd32a67b0cc3502d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__592c2bca7654bf09a27bf3be0ce0b7dada6af755dc4b617fe15a28d2b1e18b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd8993afa11dac94ee5169eb6d7d537a613985180b056815164c4957fd48c94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bc6e399dedba8ccf136d7c0567e45490bd50b52b13a584fef09e98619b85c70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__871fa15caedb1ab25c95eafe8019efd375cc6338fdcf845c1ea1eb1fc948250a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bfcc534b90104832319d8c2860ac0b6f49c973236f419686ca7aa8729fac0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33a4b6998ef85e40ca68e5f507a9f81eddc7efcc213cb2ec92c7e5292443f22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionScopingExcludesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a4cf7ab649735b5aa1faf902779c092c85adbca1d950697c9f1f450199c2d0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAnd")
    def put_and(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4519233443e9cf0c6668704c35e5b02d5a34692c614d28e985a504b0b964814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnd", [value]))

    @jsii.member(jsii_name="resetAnd")
    def reset_and(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnd", []))

    @builtins.property
    @jsii.member(jsii_name="and")
    def and_(self) -> Macie2ClassificationJobS3JobDefinitionScopingExcludesAndList:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionScopingExcludesAndList, jsii.get(self, "and"))

    @builtins.property
    @jsii.member(jsii_name="andInput")
    def and_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]]], jsii.get(self, "andInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ef871e0d2a9acdf292c4e2b870f4b49ced8349e515a5ad545ef247d7c2c447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludes",
    jsii_struct_bases=[],
    name_mapping={"and_": "and"},
)
class Macie2ClassificationJobS3JobDefinitionScopingIncludes:
    def __init__(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64c426832dd79d07ef4054b020b4ddacf36922de943b2c1596303e73d50ea9c)
            check_type(argname="argument and_", value=and_, expected_type=type_hints["and_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if and_ is not None:
            self._values["and_"] = and_

    @builtins.property
    def and_(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd"]]]:
        '''and block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        result = self._values.get("and_")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingIncludes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd",
    jsii_struct_bases=[],
    name_mapping={
        "simple_scope_term": "simpleScopeTerm",
        "tag_scope_term": "tagScopeTerm",
    },
)
class Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd:
    def __init__(
        self,
        *,
        simple_scope_term: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_scope_term: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param simple_scope_term: simple_scope_term block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#simple_scope_term Macie2ClassificationJob#simple_scope_term}
        :param tag_scope_term: tag_scope_term block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_scope_term Macie2ClassificationJob#tag_scope_term}
        '''
        if isinstance(simple_scope_term, dict):
            simple_scope_term = Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm(**simple_scope_term)
        if isinstance(tag_scope_term, dict):
            tag_scope_term = Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm(**tag_scope_term)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ccb3f10ded281a60606caf06fe9d78d501007bb5f107f2d7799f060a538958)
            check_type(argname="argument simple_scope_term", value=simple_scope_term, expected_type=type_hints["simple_scope_term"])
            check_type(argname="argument tag_scope_term", value=tag_scope_term, expected_type=type_hints["tag_scope_term"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if simple_scope_term is not None:
            self._values["simple_scope_term"] = simple_scope_term
        if tag_scope_term is not None:
            self._values["tag_scope_term"] = tag_scope_term

    @builtins.property
    def simple_scope_term(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm"]:
        '''simple_scope_term block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#simple_scope_term Macie2ClassificationJob#simple_scope_term}
        '''
        result = self._values.get("simple_scope_term")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm"], result)

    @builtins.property
    def tag_scope_term(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm"]:
        '''tag_scope_term block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_scope_term Macie2ClassificationJob#tag_scope_term}
        '''
        result = self._values.get("tag_scope_term")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a087e15fcd01e1d8b1908a9495b35a1541c855157c2f923dfc9e0694c1e89433)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84dbc843b59b6cad9188ad89eaf43f9cb31c502007acff25fa2388a935105179)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingIncludesAndOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__559bbd040e123222f6f3d9ba44c97c0c4c730faa61bf7ccc44dabcb5daef6714)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cf9c48a2bb540519c992812a9369beca81f0fa01cab1d7b7a0d9f6f194f01f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38ff4c865a0596b22dbeb7cde74aa14f9ef2cc19633fb966970aea98b0ccb967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__784860179d3bbb24e170627323f363811efa397738073574c73e7d7648ee87c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d929105c067aa128b0942e932376e9197c1e5e7397e4b40f517103008b2bc88e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSimpleScopeTerm")
    def put_simple_scope_term(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        value = Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm(
            comparator=comparator, key=key, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putSimpleScopeTerm", [value]))

    @jsii.member(jsii_name="putTagScopeTerm")
    def put_tag_scope_term(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#target Macie2ClassificationJob#target}.
        '''
        value = Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm(
            comparator=comparator, key=key, tag_values=tag_values, target=target
        )

        return typing.cast(None, jsii.invoke(self, "putTagScopeTerm", [value]))

    @jsii.member(jsii_name="resetSimpleScopeTerm")
    def reset_simple_scope_term(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSimpleScopeTerm", []))

    @jsii.member(jsii_name="resetTagScopeTerm")
    def reset_tag_scope_term(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagScopeTerm", []))

    @builtins.property
    @jsii.member(jsii_name="simpleScopeTerm")
    def simple_scope_term(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTermOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTermOutputReference", jsii.get(self, "simpleScopeTerm"))

    @builtins.property
    @jsii.member(jsii_name="tagScopeTerm")
    def tag_scope_term(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermOutputReference", jsii.get(self, "tagScopeTerm"))

    @builtins.property
    @jsii.member(jsii_name="simpleScopeTermInput")
    def simple_scope_term_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm"], jsii.get(self, "simpleScopeTermInput"))

    @builtins.property
    @jsii.member(jsii_name="tagScopeTermInput")
    def tag_scope_term_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm"], jsii.get(self, "tagScopeTermInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f906e8022451a4a3cbd8926b460cd5651af0ae60f1b274bf2f7fe21d6587b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm",
    jsii_struct_bases=[],
    name_mapping={"comparator": "comparator", "key": "key", "values": "values"},
)
class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb33dbb3d2fe67cf29191d5e49fc801f11192de63b641f3bf90604ab8934f618)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if key is not None:
            self._values["key"] = key
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTermOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTermOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__579861fcfb3f86c6f73c944595ba90993d3a796f16f6b21caf7de8327bd820a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2440b7a5a77273a28b199dc936700f6ea59dae38e1d385a2c8d6e1813918aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7e2dfc77c452bf0f3f858ac61c80a6ce1460de0942ba4ffce803e6368de28c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b6737eec50ea9b61f350ab9d006059937743d259c65a31b11f6ccc6a186234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__344746f0cd6b1bb1b1562f91db919e198eb1b27df27fead51fe106c0e15d8a1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm",
    jsii_struct_bases=[],
    name_mapping={
        "comparator": "comparator",
        "key": "key",
        "tag_values": "tagValues",
        "target": "target",
    },
)
class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#target Macie2ClassificationJob#target}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f40f864ed9573329340db4b9bff8c5a0029406402fe9f7a389ad2cc92d9b6b3)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if key is not None:
            self._values["key"] = key
        if tag_values is not None:
            self._values["tag_values"] = tag_values
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_values(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues"]]]:
        '''tag_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        result = self._values.get("tag_values")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues"]]], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#target Macie2ClassificationJob#target}.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__163321241de83ef68adae6924120bf5aceef8e6f79db4caec9c7e20a4f09c3f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTagValues")
    def put_tag_values(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4dae68ded14c88f5e729b2b3770a838e979f45793b0470c5f879d27a9736c7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTagValues", [value]))

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetTagValues")
    def reset_tag_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValues", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="tagValues")
    def tag_values(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesList":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesList", jsii.get(self, "tagValues"))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValuesInput")
    def tag_values_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues"]]], jsii.get(self, "tagValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df41e5341fa03a612551a67f86ba8a664e65dd9867357b54d8c94cbae9a3dcd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__878b4345cb786d1636196de6a2c8b41ed6aeb7ac6bb5a23b83297f2a38d8058d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40d36a7535ac54e9d05911b8e91cd26547024a921dbe84ac1c404f5138c95619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b22c003675e2cacc6ef9c66113889315678548dd1e19c57b70aa91594c2d92c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19d9460d53d0091a58fd258435ad8db53393dbc14411b9232675d60c9f21309)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef3c997a3492a1db6cbfa70d29fd2f6ea67508fde2c57db35dd34415670978a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7afba09bb2fa430f1f32714206255a9dcc47c37188734cd186c298da4090f4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__476f246e8fe2896ac4aaa29c97c1f2b79947eb78de69d59fb8a9ceb4615061df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c0d2d02c44863081fd934c207085a4c18f8421382f8c8c722449fb8b167f4d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d54a39664ffa98b073854107e322e095c15efaf4e5a3675b3d794ab1d3f1becc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8245e5bd01196a6777a760b65a461f2a3b1c8ffacc36555e47f89c21b11daa0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__348b362427ac455ff63733677e31ecbf3ce83a07ba9107415db7f7986df41177)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66401edd2ef958bc5bb73c6443c2fa833d224be54010c29d001fe6dcce1ca909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b44fad3c2a483fc2a01021af71574947ec0efd4b13b48d6109288c873403ea69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b206bb3b857becb40cd88ef075e0ccbbe29c8e866b7d4cdac6ce2e2b2d819cef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionScopingIncludesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15c5040a0c2754f50fdd5517e73f36aab15243c7834ab38248eadcebdc522a7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAnd")
    def put_and(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c7858bc6b31d6289547cbdacf99f1fe0e1a43692e8843057665f668e9f35975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnd", [value]))

    @jsii.member(jsii_name="resetAnd")
    def reset_and(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnd", []))

    @builtins.property
    @jsii.member(jsii_name="and")
    def and_(self) -> Macie2ClassificationJobS3JobDefinitionScopingIncludesAndList:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionScopingIncludesAndList, jsii.get(self, "and"))

    @builtins.property
    @jsii.member(jsii_name="andInput")
    def and_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]]], jsii.get(self, "andInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e2bde0b190ccf8355fb4b5dd081eb7ac2f48bbb5651ce3732500e253c3d6140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionScopingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c09c3267a59310e99ac0ac9b20044098fac83897fb469f8f04b2e2db0b15a926)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExcludes")
    def put_excludes(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        value = Macie2ClassificationJobS3JobDefinitionScopingExcludes(and_=and_)

        return typing.cast(None, jsii.invoke(self, "putExcludes", [value]))

    @jsii.member(jsii_name="putIncludes")
    def put_includes(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        value = Macie2ClassificationJobS3JobDefinitionScopingIncludes(and_=and_)

        return typing.cast(None, jsii.invoke(self, "putIncludes", [value]))

    @jsii.member(jsii_name="resetExcludes")
    def reset_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludes", []))

    @jsii.member(jsii_name="resetIncludes")
    def reset_includes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludes", []))

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionScopingExcludesOutputReference:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionScopingExcludesOutputReference, jsii.get(self, "excludes"))

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionScopingIncludesOutputReference:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionScopingIncludesOutputReference, jsii.get(self, "includes"))

    @builtins.property
    @jsii.member(jsii_name="excludesInput")
    def excludes_input(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludes], jsii.get(self, "excludesInput"))

    @builtins.property
    @jsii.member(jsii_name="includesInput")
    def includes_input(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludes], jsii.get(self, "includesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScoping]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScoping], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScoping],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f1d3ef10776d79fccfdbdd489540e51062596413649640360a1d80453cf353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobScheduleFrequency",
    jsii_struct_bases=[],
    name_mapping={
        "daily_schedule": "dailySchedule",
        "monthly_schedule": "monthlySchedule",
        "weekly_schedule": "weeklySchedule",
    },
)
class Macie2ClassificationJobScheduleFrequency:
    def __init__(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monthly_schedule: typing.Optional[jsii.Number] = None,
        weekly_schedule: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param daily_schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#daily_schedule Macie2ClassificationJob#daily_schedule}.
        :param monthly_schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#monthly_schedule Macie2ClassificationJob#monthly_schedule}.
        :param weekly_schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#weekly_schedule Macie2ClassificationJob#weekly_schedule}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87fc4fdeae4515d236dbae17e7848c4c7bf0616b51ece9ad224d3892fb701b1e)
            check_type(argname="argument daily_schedule", value=daily_schedule, expected_type=type_hints["daily_schedule"])
            check_type(argname="argument monthly_schedule", value=monthly_schedule, expected_type=type_hints["monthly_schedule"])
            check_type(argname="argument weekly_schedule", value=weekly_schedule, expected_type=type_hints["weekly_schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if daily_schedule is not None:
            self._values["daily_schedule"] = daily_schedule
        if monthly_schedule is not None:
            self._values["monthly_schedule"] = monthly_schedule
        if weekly_schedule is not None:
            self._values["weekly_schedule"] = weekly_schedule

    @builtins.property
    def daily_schedule(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#daily_schedule Macie2ClassificationJob#daily_schedule}.'''
        result = self._values.get("daily_schedule")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monthly_schedule(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#monthly_schedule Macie2ClassificationJob#monthly_schedule}.'''
        result = self._values.get("monthly_schedule")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def weekly_schedule(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#weekly_schedule Macie2ClassificationJob#weekly_schedule}.'''
        result = self._values.get("weekly_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobScheduleFrequency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobScheduleFrequencyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobScheduleFrequencyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5ac6da20cf9e097456825dea676e55fd0c0452ddbb7e06c64fe942e739ce9b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDailySchedule")
    def reset_daily_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDailySchedule", []))

    @jsii.member(jsii_name="resetMonthlySchedule")
    def reset_monthly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthlySchedule", []))

    @jsii.member(jsii_name="resetWeeklySchedule")
    def reset_weekly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklySchedule", []))

    @builtins.property
    @jsii.member(jsii_name="dailyScheduleInput")
    def daily_schedule_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dailyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="monthlyScheduleInput")
    def monthly_schedule_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthlyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyScheduleInput")
    def weekly_schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "weeklyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="dailySchedule")
    def daily_schedule(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dailySchedule"))

    @daily_schedule.setter
    def daily_schedule(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee0b7bd76e2283d091731195d8b84c09b70d4f694a95adf853b01780d9d0fb59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dailySchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monthlySchedule")
    def monthly_schedule(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monthlySchedule"))

    @monthly_schedule.setter
    def monthly_schedule(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bca85be3bb7197aa8cbaf9c44bcf86446e919dba3cf8c84b3263a94fb4b4b57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthlySchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeklySchedule")
    def weekly_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "weeklySchedule"))

    @weekly_schedule.setter
    def weekly_schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2936960e057297dab53d5c667761d131af3f0999536dbf4b53dfee9bef1135)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeklySchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobScheduleFrequency]:
        return typing.cast(typing.Optional[Macie2ClassificationJobScheduleFrequency], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobScheduleFrequency],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c463ffb637e7de793820c8f325ec9e8bf566ccc6d4c65a7bf2e6a7240392674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "update": "update"},
)
class Macie2ClassificationJobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#create Macie2ClassificationJob#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#update Macie2ClassificationJob#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__656cb70c6ffe9baad8b5828a88a0eb01a69d8eaad0fd114d1a31b719097482ad)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#create Macie2ClassificationJob#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/macie2_classification_job#update Macie2ClassificationJob#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3482f8d9ffed280801be2605ac19617aaf835f0656f3e2e82d5e5d55d4005c72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cdf49a90b4f04270c076e4750655777df1f8fd3ebbc741832c0f85c0289ac500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e2f97a1837e20b91554bfca65fc2411085be8415157f3cc790b9dbafe37922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb2ca75ce5192a656fba4ac31243406500e2d4fbf8e2c87d49c9ad88562a5f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobUserPausedDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class Macie2ClassificationJobUserPausedDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobUserPausedDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobUserPausedDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobUserPausedDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d098e36796f139166cdb66f55bd6b3de19f026a289f80b5bb8ad00aa084e73f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobUserPausedDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad5482e4a3497650e7e0d3e0a0137a865a5d8426c8f17525adbd2709cacd924)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobUserPausedDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93df0e5e22f4722775d39ff8b405e6c53241cc981d7257a88885e1ccc23984a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a79139bfaea1eec79c167c19117003cb7a30d92207475f6eb8dfdca783862099)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b95e14fc8d5e1adfdcafc6422577f33e371168228919721f5687828885ed181a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobUserPausedDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macie2ClassificationJob.Macie2ClassificationJobUserPausedDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61f65e05ed9b6ea3f65df69b1dae7abbc18e77fcfbcbf9812bf4888d1c876c0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="jobExpiresAt")
    def job_expires_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobExpiresAt"))

    @builtins.property
    @jsii.member(jsii_name="jobImminentExpirationHealthEventArn")
    def job_imminent_expiration_health_event_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobImminentExpirationHealthEventArn"))

    @builtins.property
    @jsii.member(jsii_name="jobPausedAt")
    def job_paused_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobPausedAt"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobUserPausedDetails]:
        return typing.cast(typing.Optional[Macie2ClassificationJobUserPausedDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobUserPausedDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f949b2fd12a79ee6bbe966edc95297184ed6a91a6d1182f1558c98c17aeaee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Macie2ClassificationJob",
    "Macie2ClassificationJobConfig",
    "Macie2ClassificationJobS3JobDefinition",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteria",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndList",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterionOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesList",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndList",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterionOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesList",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketDefinitions",
    "Macie2ClassificationJobS3JobDefinitionBucketDefinitionsList",
    "Macie2ClassificationJobS3JobDefinitionBucketDefinitionsOutputReference",
    "Macie2ClassificationJobS3JobDefinitionOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScoping",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludes",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndList",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTermOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesList",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludes",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndList",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTermOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesList",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingOutputReference",
    "Macie2ClassificationJobScheduleFrequency",
    "Macie2ClassificationJobScheduleFrequencyOutputReference",
    "Macie2ClassificationJobTimeouts",
    "Macie2ClassificationJobTimeoutsOutputReference",
    "Macie2ClassificationJobUserPausedDetails",
    "Macie2ClassificationJobUserPausedDetailsList",
    "Macie2ClassificationJobUserPausedDetailsOutputReference",
]

publication.publish()

def _typecheckingstub__074e2b3077ee774f620b6cc1f9412406c3851ecc74ebadee02a6c255e04a397c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    job_type: builtins.str,
    s3_job_definition: typing.Union[Macie2ClassificationJobS3JobDefinition, typing.Dict[builtins.str, typing.Any]],
    custom_data_identifier_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initial_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    job_status: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    sampling_percentage: typing.Optional[jsii.Number] = None,
    schedule_frequency: typing.Optional[typing.Union[Macie2ClassificationJobScheduleFrequency, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[Macie2ClassificationJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4ef5421e1a9b2a92eec77e984bc743f322ccc2fc3005761085ea842c02e874a7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015542a72d4728e6f08abfdafd232c75134375f76ee49efc0143395ba103df85(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec48f1904c3b9c72eac0b112b6b35920c66cc07e39949f334d8082e9d7eb6418(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb42990ad1dc41e598fc505fb4a6979204fe6bb164b65a877ffe0b053c5e0bf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3208183587112b033f44b2a0aa2d4a0743868c13d6331c89f732f7e665ddec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c28c4672ec91bc3209295e81df571074f2b563e732948d64886e0e3b08f8a3b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f4e12faf1e99c7429076958e043337c5f82d55fb9d131986327affa64f34d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__259373f8d71b7410008529a6f9e14b3cc7bf829d276dbf527e17b1616d9ed23b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1cb35c4eb7f08c7677dfc16a8f6edf46fa231da0085263d9e919967d24296ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b3a0c97b519d850ab1bc69022ce854c480ae30abacb55682a3c1368d325d04(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369e9bb2edb070277206519175176d6a6780d18d65fe17570727236ba998dcd1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361553db7331d294d672c7d77c6b7f4f20496a9a49c2de671d2d936a07ebd972(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68bbc2ccb85df1a30f0d752ee6f96898edc52b0aa030052cd0aefb93a22a59c3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    job_type: builtins.str,
    s3_job_definition: typing.Union[Macie2ClassificationJobS3JobDefinition, typing.Dict[builtins.str, typing.Any]],
    custom_data_identifier_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initial_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    job_status: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    sampling_percentage: typing.Optional[jsii.Number] = None,
    schedule_frequency: typing.Optional[typing.Union[Macie2ClassificationJobScheduleFrequency, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[Macie2ClassificationJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad40965da313a91c882dc3e9e9d9cb38cfdc3b196b66a9d5a17586851ea0029c(
    *,
    bucket_criteria: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
    bucket_definitions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketDefinitions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scoping: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionScoping, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8fd18dd916a2ea1fd8bf2c57f29559905ba77be636eaa56d1b6f75f19d8157(
    *,
    excludes: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes, typing.Dict[builtins.str, typing.Any]]] = None,
    includes: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b5f05d65c2721145266103c75bc032cbd88b3ab9d1315b55fb049ce1cb80f1(
    *,
    and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b253dd7a5ac96ffe8f8031cb272823be37e2eb3adcbd1b6abc4a4cc51f9bc3(
    *,
    simple_criterion: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_criterion: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b45012d6cef7d438296a14ac7bb5aeb28779ac49a8021b4f2ce6b6310638517(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd147552c3505853a73cfac69ffdabfc04fd7086d0d3c25a9a06d3c807aa2dc0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef50feebf5b834b1116d3b2dd62d790ded3fdefda702c5e52b5b63d14869ea34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af6786b2af3d2e9170e3a180e53cd1de71cdc42dc9580659e2e03236d6367f09(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__817a8427b489639ce58480b8f05d4b62c38ed6a6933068bb3fe039ecb8bc1889(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81eda7c267c142989f16affa584ad4d4883b8162a619eeb85bf2116377c8590f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1b840e167eef613b67e9d71f256e770361694397ef7fb8a922ef7c2e4c072a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bdef3fce821f61aec7cbebd9b2ee4734012ce65b41f68abde5ba8aa4ffc64e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea36ffa3cb30a7afd7185dd08b4ebc11781016ad4a5f51a50d9ede111b3c01d(
    *,
    comparator: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18402509939cfb8e22271e24cff9c942895d232327303d7c391f86bfac4d6982(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474f276886672aedee3b14e58340a3a57c0ec1828c749b52501ff7a6836eb7ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e6a7dd53d66fa75761115cf2aac4369066621afd85fef0c78dbd8099057fd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354a8e0016512d85bd53a1589e25da5820f44d4e6efd52eaad1bc38dcefae157(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a50a6fa71504f5e7a62883ce2c0c56288ddd5b95fed17e0eb10593180b7d0be(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d11c64b77011f33ffec42761f901141728bab2c500f7fadd2f393a86a882737(
    *,
    comparator: typing.Optional[builtins.str] = None,
    tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee61c9f762b1d02985cf351a5f3cdd98f06ed81a79b13aba96b7a0c76bc5813(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f95292532b2aff87a878a1417ecafc40dad1364625fd02757cde94fd5b0e9133(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b019d6800fde8b26526d0e0df38151f14f7da42505656b9b5842a4ba0e393c47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5904a33e24db06728a37df3aba2a601599f9935c3ff9f43dd8210d17e6a99e09(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441eb7686726d117b67f558b1e9f344f2b2804210e884dbb6c287c63aeb934f6(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e317e38b8ef150c85b4a43e9a9177691f06b59e6c4e3b2fe8c7dd3cd3cde9bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98803a4ccddabd0d8b45f4015b12e086e717735236cad8759ad1d37918d024c8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d22c8877bce1a4b5f0656ba8943b78e7d9aeac1aefec331f2f291324d3c8169(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0234a77a6d74a4c4cecddb4b9c6f8448f4852f528f7936d6c1de323f50d816d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3662eba0a2c9eaf051ac4c09e25c3418a81cccbc31647750b34ab937906f1f0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92153ed27f11fcaaee63ccfb2833eee890676fe48775cb7f7a6bb5b6994d7ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2232978e7f3fc8a1273887c860ade64f74b08552b075276b0c8cf2a567bc7f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc8c4a344fa1cad8cf9202587e8350af15738ed147b40918187b092faa091f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b394ed52d3d5ee8aac19fc79d25294144b8d8419d5c072a0d5e3a840ce3c593(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7bfef37608541fbfaf2d9a7d5c15d910ad12d97baa0ed5e66848ca0a1d84daa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e9b40b1c8e6bc4f3b130a5f30dacaebdc5b20c5ed5535a4c074a3aa5dbea55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__372e59744d67b077978eedc67f6f6f2a5ac8d5ba400afa83159b156a6e22fba1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f1a8dc3c077ccf3fa76bede80de45970fd1804b37ecc2e81d925530659e623(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a24eb836e16e152312aee8a31a78b3c847dbff772464e5d3f29c5aad4d7a602(
    *,
    and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5025f719310e64962f62fe1c530956bcf900af0de7e1ccbc3ef19e9c90cf55(
    *,
    simple_criterion: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_criterion: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab1c85b4c905042419ee0eddb23ab0d88026b381e86eb3e480fc61b8531a65c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1386694d3502432dbc5d89966b480125822feec7fd4157456c5e32e206509cc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc82921d7b2bf9aa8aff45e3d8f1036f6321331b43e1b915c5f0514b49748e32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad823b055fa032997456cba9ca5a327fb59f45dd57b915964fffc224f59b7c8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb39ffebc2747bcbcb5df60a72ef0f06ab355e45cc8f0103e12622e13e0d47e0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da41de78a5ec610a1550df266aa9d2cc601691f385088b2ec7369723d5f12f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9df38667a39a6be3cc1c13ebaed996e2871871f89e489152b3603f44825af13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264e3f8098ecba16cb05ac8e26e1dab7fb12bb30cba6af1a6d1cab1010a96f67(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1373ed675b01025e33806777b0e2ee70184cb252d2a1cf5bbaa7285dd37ea6(
    *,
    comparator: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb04cf23a1cfb9e03fcaa7583d779a0dc5d15d87c88e11fc854fb9ad741b6db2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cfb5a67e352e63030d764bd83e7e7c8264bf9136ea93e8a8fb8f2e048e0945b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749413920a8f7afa91a91413b53a9e207ed6c6b36a2317932bb20972f875741a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1b1b14d47c2eab97443c2f2c49b5682e938bbaae96333fb65e5b9fe3026fa8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de062c01657297679dc0d125090431b77cd4ffc92f10e2718f604e2096b6be91(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b132989bc20c80d382925e4974a7e3083fa5c9b48721ff1cf14473542b787e9(
    *,
    comparator: typing.Optional[builtins.str] = None,
    tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3826c0416dc30cd07c8fd0930a5f935496b29fab58c10a675cf52c0f4702b897(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574eca5171683894f4b6add03c08e9ef0b20da5456b75969692682d55ac5bd3a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be590e2e1460572bdc982cb4872f777ddd1427bee739dd09f5a838ce78b81cc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2c07ca8400f0ae399d241960968e1e876646f83a36e2fc476d1695e56e3304(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caeffee2e9f83f80faaecfb0be3bce0519d4fd46619ceed2ddf253baa280b790(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91408c987cdecf8d2cea946fd27072ae628ec7d6adaa1e8865933d3b306889a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e01c2a67c4968f04d69e72f1713d94cdcad0bd001613ad588a1007f14eea008(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23916b61ffe9d4b4e6772d0554c93a4769c87bf2170baf6ea0985f937d4c8d3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b385edb1a339fa7d41cad54dbb73b251efa1cdc250597e6a353973141b53e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7c026e66111d7c90e59c0c16c281cfd20e81ff7b42ca827ae1b96ed6c636b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fdd9cc1c2ff009c10192bbd50ac44844141a6c433449acd17ed0cef957645ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf9b247be3ec268e71843d928ec3c8300070e4203c7a5682ab9b5a958755e67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f71762d1173290aca3e6c250872750a743e8d856673fddb3985bef4531756b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5a3274bd7332490a2d2f0af421274c63bfde48c1323221d972b98744415fd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__365d9551842400fa2a1ae23109e42d57e4eb798fcc28a4c1bb536f25ac69948e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe2c18784c9b211c235d5ef6dad3cbdd4eb728ecc33fc11acd12162570f0247(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2221b3c68bf15876c10043d5edb015b3236ef9e6c09509cf6553328ebe8aa1c1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b21d96c1fb534135939d4ff7ab9ad65c889da4c732a4193cfeee30da8a6b91(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727faffbdb928857d42a28ff2aedbdf666f3818db90e30e738d3c91b8d1478fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb994e7b075369ed83ff3028bc789da07d96371250fd92e0d39fce7edcc69d1(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0749a2f40360dd2866cee3123009bc78e57ea68b9080e9e9c33da749395be3d1(
    *,
    account_id: builtins.str,
    buckets: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e421defeadde00db95b630324223db07a2b45a339716edf23312df89e911d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ec1a5b244e5aff866cd1b5b4734fde741a9e45029303d6527801e4ec6ab088(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62087dcaa77d2f6808045b3ee0efdccb338897722c1ef0dfc4d6b828e9c529be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22648dca569b916725b80622eb01655574a0fa83b9ebaa87be393be522410c3c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__875c43d00751b62281f4809889b9291252ff37fc1e7f50de674465cec57d4335(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3c9783dcbe702f2fc3c22ab002624162c0770ebc2dea72bd58c8e92812cfbb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketDefinitions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27d1413237b72c4cfb32bc0fc5725e7bb9272f3d6fbbdefb6c579996773b114(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a6f82ebb5555beda36bac8876b453be46d51710739ca8f0bee2900e51792e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ab000b12f7d3364a09b5afe3222c912788183143d9e9a318f8af109c08825e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bccf4379dd4728efcc2929ad8db0d7f1e49f3d82d5ebdc5b40fb7b3611d4bb8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketDefinitions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6220f8fc88e0e91e09102d6a55ba608d0a1ba9afcc7b160e1f8ea505e75883fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a5725ede8c5278fb290318c10bc3e0df831608df80f98addce04ed92a76aff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketDefinitions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9519678e184c9a265f9c1cdad33f61470cd8764da0abe72d77a037bf3479e71f(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4ad3d8f0fc1a8893807a79b677383b5f63ec74e367118fb76c92981408d234(
    *,
    excludes: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludes, typing.Dict[builtins.str, typing.Any]]] = None,
    includes: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dba534096041adfe43905ed364573baa4117ff5efe41d26fb6c02ae17547478(
    *,
    and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279ee517ea574ce4ca8e301f50a67b039622868d3c1cd28368b33e4b010bea35(
    *,
    simple_scope_term: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_scope_term: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad7531638004a07c0966a1fabb94a5878b53bd42b2cc8ecddb2247dba9c13bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5448e3aa0140d0ae044f14eee73b6504778f6cc028d931a3f118c1bfca45a2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3bfcafbd43be9ff3b44dbabb017a57fb3a312fa4a99b222e900b210c705dfcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a93b5dc1af91838a949528f2ad76c1f49c50eac8b78614334d29b13da452d56(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472db1921a847501c5a11294e711b3b17d06e7ba1de8fe73190f4916a7ce84dd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d6769943ec9614fc96b5c1ccae5ee89b176f7734191f0778183e2d6e1e4e541(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5fd87cc259fa46424055344babdceea7d25de553e855b6e6eb1a4c828ef0136(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e291fd29ba3923fb205db59cba385a15cf553c38d1adbde95e1232d45339ba21(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2169c8aa72d83203d7bdbf0be49853bcb673efef6d723e93fc78f95987bba57(
    *,
    comparator: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ace96ab0df7fe5e7285f14a8331e2bbbdd71fdf3df57536b7cc86d7b5d8115(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b47a96044480241d9c5fd43e446bbc9d4eabf7ba5c80bd38cbcfb224b9622f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2375fb51185915850825a73fdd35c392133dc8dd63180c16efe02c2794739dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73a8c55ea97392c9fcd5703958600cbad61b66558bb3deb83c6fed75c4e3e05d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ff693f7c6401d27c83071a2571e436046a0e29bd98b254dc0fbf58318398ba(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf8588b063e92ba2d4311f2dc6b95a8726949ef1f175504a6c34d51deef77b9(
    *,
    comparator: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c7599aece3e904fd87465959aba49ab6d524a34b01708651b20e7ef28374743(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d3aa953f834f473c2c333b212237ff3978a603773b59be62ffc95ce432dc12(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc34be28a84facd2b375c8370c2b48038e4ce8cf93e0d1312c4a9cee99f9169(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e1afed1b501dfbc8b8c205c368736fadf0da8fbcc0b31ff9b49b443b0d51a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88da5204047ac2dac5ffa345ad8eaddf5364f8a6f4f85dddccb9b0bdb8e0c9bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9f252568df9f30501e43f50138cca06d9d4360b2db84efa18ef842caf7d07c(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678de4371fda9e8a20bb062d4460b38f2e85e199a508ed0ccc788702983f5fe2(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac9246eaeeff8267458ad6cf92788f2e62a5b3608530082a8535d282467b923(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13270778c9e7d5f86462133084868d4bfcd1cd7834310124a39e7c2849f7467e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6553c8165cc48b9c0010f798df1e4da5fad0635d8526f7d97a52952eb7940e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0509e200c78dccba47c68167bfaa3204bf5d999f676fd5dd32a67b0cc3502d5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592c2bca7654bf09a27bf3be0ce0b7dada6af755dc4b617fe15a28d2b1e18b7f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd8993afa11dac94ee5169eb6d7d537a613985180b056815164c4957fd48c94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc6e399dedba8ccf136d7c0567e45490bd50b52b13a584fef09e98619b85c70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871fa15caedb1ab25c95eafe8019efd375cc6338fdcf845c1ea1eb1fc948250a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bfcc534b90104832319d8c2860ac0b6f49c973236f419686ca7aa8729fac0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33a4b6998ef85e40ca68e5f507a9f81eddc7efcc213cb2ec92c7e5292443f22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4cf7ab649735b5aa1faf902779c092c85adbca1d950697c9f1f450199c2d0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4519233443e9cf0c6668704c35e5b02d5a34692c614d28e985a504b0b964814(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ef871e0d2a9acdf292c4e2b870f4b49ced8349e515a5ad545ef247d7c2c447(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64c426832dd79d07ef4054b020b4ddacf36922de943b2c1596303e73d50ea9c(
    *,
    and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ccb3f10ded281a60606caf06fe9d78d501007bb5f107f2d7799f060a538958(
    *,
    simple_scope_term: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_scope_term: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a087e15fcd01e1d8b1908a9495b35a1541c855157c2f923dfc9e0694c1e89433(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84dbc843b59b6cad9188ad89eaf43f9cb31c502007acff25fa2388a935105179(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__559bbd040e123222f6f3d9ba44c97c0c4c730faa61bf7ccc44dabcb5daef6714(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf9c48a2bb540519c992812a9369beca81f0fa01cab1d7b7a0d9f6f194f01f5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ff4c865a0596b22dbeb7cde74aa14f9ef2cc19633fb966970aea98b0ccb967(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__784860179d3bbb24e170627323f363811efa397738073574c73e7d7648ee87c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d929105c067aa128b0942e932376e9197c1e5e7397e4b40f517103008b2bc88e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f906e8022451a4a3cbd8926b460cd5651af0ae60f1b274bf2f7fe21d6587b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb33dbb3d2fe67cf29191d5e49fc801f11192de63b641f3bf90604ab8934f618(
    *,
    comparator: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579861fcfb3f86c6f73c944595ba90993d3a796f16f6b21caf7de8327bd820a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2440b7a5a77273a28b199dc936700f6ea59dae38e1d385a2c8d6e1813918aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7e2dfc77c452bf0f3f858ac61c80a6ce1460de0942ba4ffce803e6368de28c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b6737eec50ea9b61f350ab9d006059937743d259c65a31b11f6ccc6a186234(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344746f0cd6b1bb1b1562f91db919e198eb1b27df27fead51fe106c0e15d8a1b(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f40f864ed9573329340db4b9bff8c5a0029406402fe9f7a389ad2cc92d9b6b3(
    *,
    comparator: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__163321241de83ef68adae6924120bf5aceef8e6f79db4caec9c7e20a4f09c3f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4dae68ded14c88f5e729b2b3770a838e979f45793b0470c5f879d27a9736c7b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df41e5341fa03a612551a67f86ba8a664e65dd9867357b54d8c94cbae9a3dcd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__878b4345cb786d1636196de6a2c8b41ed6aeb7ac6bb5a23b83297f2a38d8058d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d36a7535ac54e9d05911b8e91cd26547024a921dbe84ac1c404f5138c95619(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22c003675e2cacc6ef9c66113889315678548dd1e19c57b70aa91594c2d92c7(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19d9460d53d0091a58fd258435ad8db53393dbc14411b9232675d60c9f21309(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef3c997a3492a1db6cbfa70d29fd2f6ea67508fde2c57db35dd34415670978a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7afba09bb2fa430f1f32714206255a9dcc47c37188734cd186c298da4090f4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__476f246e8fe2896ac4aaa29c97c1f2b79947eb78de69d59fb8a9ceb4615061df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c0d2d02c44863081fd934c207085a4c18f8421382f8c8c722449fb8b167f4d2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54a39664ffa98b073854107e322e095c15efaf4e5a3675b3d794ab1d3f1becc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8245e5bd01196a6777a760b65a461f2a3b1c8ffacc36555e47f89c21b11daa0f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348b362427ac455ff63733677e31ecbf3ce83a07ba9107415db7f7986df41177(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66401edd2ef958bc5bb73c6443c2fa833d224be54010c29d001fe6dcce1ca909(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44fad3c2a483fc2a01021af71574947ec0efd4b13b48d6109288c873403ea69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b206bb3b857becb40cd88ef075e0ccbbe29c8e866b7d4cdac6ce2e2b2d819cef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c5040a0c2754f50fdd5517e73f36aab15243c7834ab38248eadcebdc522a7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c7858bc6b31d6289547cbdacf99f1fe0e1a43692e8843057665f668e9f35975(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2bde0b190ccf8355fb4b5dd081eb7ac2f48bbb5651ce3732500e253c3d6140(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c09c3267a59310e99ac0ac9b20044098fac83897fb469f8f04b2e2db0b15a926(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f1d3ef10776d79fccfdbdd489540e51062596413649640360a1d80453cf353(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScoping],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fc4fdeae4515d236dbae17e7848c4c7bf0616b51ece9ad224d3892fb701b1e(
    *,
    daily_schedule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monthly_schedule: typing.Optional[jsii.Number] = None,
    weekly_schedule: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ac6da20cf9e097456825dea676e55fd0c0452ddbb7e06c64fe942e739ce9b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0b7bd76e2283d091731195d8b84c09b70d4f694a95adf853b01780d9d0fb59(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bca85be3bb7197aa8cbaf9c44bcf86446e919dba3cf8c84b3263a94fb4b4b57(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2936960e057297dab53d5c667761d131af3f0999536dbf4b53dfee9bef1135(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c463ffb637e7de793820c8f325ec9e8bf566ccc6d4c65a7bf2e6a7240392674(
    value: typing.Optional[Macie2ClassificationJobScheduleFrequency],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656cb70c6ffe9baad8b5828a88a0eb01a69d8eaad0fd114d1a31b719097482ad(
    *,
    create: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3482f8d9ffed280801be2605ac19617aaf835f0656f3e2e82d5e5d55d4005c72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf49a90b4f04270c076e4750655777df1f8fd3ebbc741832c0f85c0289ac500(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e2f97a1837e20b91554bfca65fc2411085be8415157f3cc790b9dbafe37922(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb2ca75ce5192a656fba4ac31243406500e2d4fbf8e2c87d49c9ad88562a5f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d098e36796f139166cdb66f55bd6b3de19f026a289f80b5bb8ad00aa084e73f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad5482e4a3497650e7e0d3e0a0137a865a5d8426c8f17525adbd2709cacd924(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93df0e5e22f4722775d39ff8b405e6c53241cc981d7257a88885e1ccc23984a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79139bfaea1eec79c167c19117003cb7a30d92207475f6eb8dfdca783862099(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95e14fc8d5e1adfdcafc6422577f33e371168228919721f5687828885ed181a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f65e05ed9b6ea3f65df69b1dae7abbc18e77fcfbcbf9812bf4888d1c876c0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f949b2fd12a79ee6bbe966edc95297184ed6a91a6d1182f1558c98c17aeaee5(
    value: typing.Optional[Macie2ClassificationJobUserPausedDetails],
) -> None:
    """Type checking stubs"""
    pass

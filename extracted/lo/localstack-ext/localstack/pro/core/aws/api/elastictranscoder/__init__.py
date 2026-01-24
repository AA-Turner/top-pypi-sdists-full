from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

AccessControl = str
Ascending = str
AspectRatio = str
AudioBitDepth = str
AudioBitOrder = str
AudioBitRate = str
AudioChannels = str
AudioCodec = str
AudioCodecProfile = str
AudioPackingMode = str
AudioSampleRate = str
AudioSigned = str
Base64EncodedString = str
BucketName = str
CaptionFormatFormat = str
CaptionFormatPattern = str
CaptionMergePolicy = str
CodecOption = str
Description = str
Digits = str
DigitsOrAuto = str
EncryptionMode = str
Filename = str
FixedGOP = str
FloatString = str
FrameRate = str
Grantee = str
GranteeType = str
HlsContentProtectionMethod = str
HorizontalAlign = str
Id = str
Interlaced = str
JobContainer = str
JobStatus = str
JpgOrPng = str
Key = str
KeyArn = str
KeyIdGuid = str
KeyStoragePolicy = str
KeyframesMaxDist = str
LongKey = str
MaxFrameRate = str
MergePolicy = str
Name = str
NonEmptyBase64EncodedString = str
NullableInteger = int
OneTo512String = str
Opacity = str
PaddingPolicy = str
PipelineStatus = str
PixelsOrPercent = str
PlayReadyDrmFormatString = str
PlaylistFormat = str
PresetContainer = str
PresetType = str
PresetWatermarkId = str
Resolution = str
Role = str
Rotate = str
SizingPolicy = str
SnsTopic = str
StorageClass = str
String = str
Success = str
Target = str
ThumbnailPattern = str
ThumbnailResolution = str
Time = str
TimeOffset = str
VerticalAlign = str
VideoBitRate = str
VideoCodec = str
WatermarkKey = str
WatermarkSizingPolicy = str
ZeroTo255String = str
ZeroTo512String = str


class AccessDeniedException(ServiceException):
    """General authentication failure. The request was not signed correctly."""

    code: str = "AccessDeniedException"
    sender_fault: bool = False
    status_code: int = 403


class IncompatibleVersionException(ServiceException):
    code: str = "IncompatibleVersionException"
    sender_fault: bool = False
    status_code: int = 400


class InternalServiceException(ServiceException):
    """Elastic Transcoder encountered an unexpected exception while trying to
    fulfill the request.
    """

    code: str = "InternalServiceException"
    sender_fault: bool = False
    status_code: int = 400


class LimitExceededException(ServiceException):
    """Too many operations for a given AWS account. For example, the number of
    pipelines exceeds the maximum allowed.
    """

    code: str = "LimitExceededException"
    sender_fault: bool = False
    status_code: int = 429


class ResourceInUseException(ServiceException):
    """The resource you are attempting to change is in use. For example, you
    are attempting to delete a pipeline that is currently in use.
    """

    code: str = "ResourceInUseException"
    sender_fault: bool = False
    status_code: int = 409


class ResourceNotFoundException(ServiceException):
    """The requested resource does not exist or is not available. For example,
    the pipeline to which you're trying to add a job doesn't exist or is
    still being created.
    """

    code: str = "ResourceNotFoundException"
    sender_fault: bool = False
    status_code: int = 404


class ValidationException(ServiceException):
    """One or more required parameter values were not provided in the request."""

    code: str = "ValidationException"
    sender_fault: bool = False
    status_code: int = 400


AccessControls = list[AccessControl]


class Encryption(TypedDict, total=False):
    """The encryption settings, if any, that are used for decrypting your input
    files or encrypting your output files. If your input file is encrypted,
    you must specify the mode that Elastic Transcoder uses to decrypt your
    file, otherwise you must specify the mode you want Elastic Transcoder to
    use to encrypt your output files.
    """

    Mode: EncryptionMode | None
    Key: Base64EncodedString | None
    KeyMd5: Base64EncodedString | None
    InitializationVector: ZeroTo255String | None


class Artwork(TypedDict, total=False):
    """The file to be used as album art. There can be multiple artworks
    associated with an audio file, to a maximum of 20.

    To remove artwork or leave the artwork empty, you can either set
    ``Artwork`` to null, or set the ``Merge Policy`` to "Replace" and use an
    empty ``Artwork`` array.

    To pass through existing artwork unchanged, set the ``Merge Policy`` to
    "Prepend", "Append", or "Fallback", and use an empty ``Artwork`` array.
    """

    InputKey: WatermarkKey | None
    MaxWidth: DigitsOrAuto | None
    MaxHeight: DigitsOrAuto | None
    SizingPolicy: SizingPolicy | None
    PaddingPolicy: PaddingPolicy | None
    AlbumArtFormat: JpgOrPng | None
    Encryption: Encryption | None


Artworks = list[Artwork]


class AudioCodecOptions(TypedDict, total=False):
    """Options associated with your audio codec."""

    Profile: AudioCodecProfile | None
    BitDepth: AudioBitDepth | None
    BitOrder: AudioBitOrder | None
    Signed: AudioSigned | None


class AudioParameters(TypedDict, total=False):
    """Parameters required for transcoding audio."""

    Codec: AudioCodec | None
    SampleRate: AudioSampleRate | None
    BitRate: AudioBitRate | None
    Channels: AudioChannels | None
    AudioPackingMode: AudioPackingMode | None
    CodecOptions: AudioCodecOptions | None


class CancelJobRequest(ServiceRequest):
    """The ``CancelJobRequest`` structure."""

    Id: Id


class CancelJobResponse(TypedDict, total=False):
    """The response body contains a JSON object. If the job is successfully
    canceled, the value of ``Success`` is ``true``.
    """

    pass


class CaptionFormat(TypedDict, total=False):
    """The file format of the output captions. If you leave this value blank,
    Elastic Transcoder returns an error.
    """

    Format: CaptionFormatFormat | None
    Pattern: CaptionFormatPattern | None
    Encryption: Encryption | None


CaptionFormats = list[CaptionFormat]


class CaptionSource(TypedDict, total=False):
    """A source file for the input sidecar captions used during the transcoding
    process.
    """

    Key: LongKey | None
    Language: Key | None
    TimeOffset: TimeOffset | None
    Label: Name | None
    Encryption: Encryption | None


CaptionSources = list[CaptionSource]


class Captions(TypedDict, total=False):
    """The captions to be created, if any."""

    MergePolicy: CaptionMergePolicy | None
    CaptionSources: CaptionSources | None
    CaptionFormats: CaptionFormats | None


class TimeSpan(TypedDict, total=False):
    """Settings that determine when a clip begins and how long it lasts."""

    StartTime: Time | None
    Duration: Time | None


class Clip(TypedDict, total=False):
    """Settings for one clip in a composition. All jobs in a playlist must have
    the same clip settings.
    """

    TimeSpan: TimeSpan | None


CodecOptions = dict[CodecOption, CodecOption]
Composition = list[Clip]


class JobAlbumArt(TypedDict, total=False):
    """The .jpg or .png file associated with an audio file."""

    MergePolicy: MergePolicy | None
    Artwork: Artworks | None


class JobWatermark(TypedDict, total=False):
    """Watermarks can be in .png or .jpg format. If you want to display a
    watermark that is not rectangular, use the .png format, which supports
    transparency.
    """

    PresetWatermarkId: PresetWatermarkId | None
    InputKey: WatermarkKey | None
    Encryption: Encryption | None


JobWatermarks = list[JobWatermark]


class CreateJobOutput(TypedDict, total=False):
    """The ``CreateJobOutput`` structure."""

    Key: Key | None
    ThumbnailPattern: ThumbnailPattern | None
    ThumbnailEncryption: Encryption | None
    Rotate: Rotate | None
    PresetId: Id | None
    SegmentDuration: FloatString | None
    Watermarks: JobWatermarks | None
    AlbumArt: JobAlbumArt | None
    Composition: Composition | None
    Captions: Captions | None
    Encryption: Encryption | None


CreateJobOutputs = list[CreateJobOutput]


class PlayReadyDrm(TypedDict, total=False):
    """The PlayReady DRM settings, if any, that you want Elastic Transcoder to
    apply to the output files associated with this playlist.

    PlayReady DRM encrypts your media files using ``aes-ctr`` encryption.

    If you use DRM for an ``HLSv3`` playlist, your outputs must have a
    master playlist.
    """

    Format: PlayReadyDrmFormatString | None
    Key: NonEmptyBase64EncodedString | None
    KeyMd5: NonEmptyBase64EncodedString | None
    KeyId: KeyIdGuid | None
    InitializationVector: ZeroTo255String | None
    LicenseAcquisitionUrl: OneTo512String | None


class HlsContentProtection(TypedDict, total=False):
    """The HLS content protection settings, if any, that you want Elastic
    Transcoder to apply to your output files.
    """

    Method: HlsContentProtectionMethod | None
    Key: Base64EncodedString | None
    KeyMd5: Base64EncodedString | None
    InitializationVector: ZeroTo255String | None
    LicenseAcquisitionUrl: ZeroTo512String | None
    KeyStoragePolicy: KeyStoragePolicy | None


OutputKeys = list[Key]


class CreateJobPlaylist(TypedDict, total=False):
    """Information about the master playlist."""

    Name: Filename | None
    Format: PlaylistFormat | None
    OutputKeys: OutputKeys | None
    HlsContentProtection: HlsContentProtection | None
    PlayReadyDrm: PlayReadyDrm | None


CreateJobPlaylists = list[CreateJobPlaylist]
UserMetadata = dict[String, String]
NullableLong = int


class DetectedProperties(TypedDict, total=False):
    """The detected properties of the input file. Elastic Transcoder identifies
    these values from the input file.
    """

    Width: NullableInteger | None
    Height: NullableInteger | None
    FrameRate: FloatString | None
    FileSize: NullableLong | None
    DurationMillis: NullableLong | None


class InputCaptions(TypedDict, total=False):
    """The captions to be created, if any."""

    MergePolicy: CaptionMergePolicy | None
    CaptionSources: CaptionSources | None


class JobInput(TypedDict, total=False):
    """Information about the file that you're transcoding."""

    Key: LongKey | None
    FrameRate: FrameRate | None
    Resolution: Resolution | None
    AspectRatio: AspectRatio | None
    Interlaced: Interlaced | None
    Container: JobContainer | None
    Encryption: Encryption | None
    TimeSpan: TimeSpan | None
    InputCaptions: InputCaptions | None
    DetectedProperties: DetectedProperties | None


JobInputs = list[JobInput]


class CreateJobRequest(ServiceRequest):
    """The ``CreateJobRequest`` structure."""

    PipelineId: Id
    Input: JobInput | None
    Inputs: JobInputs | None
    Output: CreateJobOutput | None
    Outputs: CreateJobOutputs | None
    OutputKeyPrefix: Key | None
    Playlists: CreateJobPlaylists | None
    UserMetadata: UserMetadata | None


class Timing(TypedDict, total=False):
    """Details about the timing of a job."""

    SubmitTimeMillis: NullableLong | None
    StartTimeMillis: NullableLong | None
    FinishTimeMillis: NullableLong | None


class Playlist(TypedDict, total=False):
    """Use Only for Fragmented MP4 or MPEG-TS Outputs. If you specify a preset
    for which the value of Container is ``fmp4`` (Fragmented MP4) or ``ts``
    (MPEG-TS), Playlists contains information about the master playlists
    that you want Elastic Transcoder to create. We recommend that you create
    only one master playlist per output format. The maximum number of master
    playlists in a job is 30.
    """

    Name: Filename | None
    Format: PlaylistFormat | None
    OutputKeys: OutputKeys | None
    HlsContentProtection: HlsContentProtection | None
    PlayReadyDrm: PlayReadyDrm | None
    Status: JobStatus | None
    StatusDetail: Description | None


Playlists = list[Playlist]


class JobOutput(TypedDict, total=False):
    """Outputs recommended instead.

    If you specified one output for a job, information about that output. If
    you specified multiple outputs for a job, the ``Output`` object lists
    information about the first output. This duplicates the information that
    is listed for the first output in the ``Outputs`` object.
    """

    Id: String | None
    Key: Key | None
    ThumbnailPattern: ThumbnailPattern | None
    ThumbnailEncryption: Encryption | None
    Rotate: Rotate | None
    PresetId: Id | None
    SegmentDuration: FloatString | None
    Status: JobStatus | None
    StatusDetail: Description | None
    Duration: NullableLong | None
    Width: NullableInteger | None
    Height: NullableInteger | None
    FrameRate: FloatString | None
    FileSize: NullableLong | None
    DurationMillis: NullableLong | None
    Watermarks: JobWatermarks | None
    AlbumArt: JobAlbumArt | None
    Composition: Composition | None
    Captions: Captions | None
    Encryption: Encryption | None
    AppliedColorSpaceConversion: String | None


JobOutputs = list[JobOutput]


class Job(TypedDict, total=False):
    """A section of the response body that provides information about the job
    that is created.
    """

    Id: Id | None
    Arn: String | None
    PipelineId: Id | None
    Input: JobInput | None
    Inputs: JobInputs | None
    Output: JobOutput | None
    Outputs: JobOutputs | None
    OutputKeyPrefix: Key | None
    Playlists: Playlists | None
    Status: JobStatus | None
    UserMetadata: UserMetadata | None
    Timing: Timing | None


class CreateJobResponse(TypedDict, total=False):
    """The CreateJobResponse structure."""

    Job: Job | None


class Permission(TypedDict, total=False):
    """The ``Permission`` structure."""

    GranteeType: GranteeType | None
    Grantee: Grantee | None
    Access: AccessControls | None


Permissions = list[Permission]


class PipelineOutputConfig(TypedDict, total=False):
    """The ``PipelineOutputConfig`` structure."""

    Bucket: BucketName | None
    StorageClass: StorageClass | None
    Permissions: Permissions | None


class Notifications(TypedDict, total=False):
    """The Amazon Simple Notification Service (Amazon SNS) topic or topics to
    notify in order to report job status.

    To receive notifications, you must also subscribe to the new topic in
    the Amazon SNS console.
    """

    Progressing: SnsTopic | None
    Completed: SnsTopic | None
    Warning: SnsTopic | None
    Error: SnsTopic | None


class CreatePipelineRequest(ServiceRequest):
    """The ``CreatePipelineRequest`` structure."""

    Name: Name
    InputBucket: BucketName
    OutputBucket: BucketName | None
    Role: Role
    AwsKmsKeyArn: KeyArn | None
    Notifications: Notifications | None
    ContentConfig: PipelineOutputConfig | None
    ThumbnailConfig: PipelineOutputConfig | None


class Warning(TypedDict, total=False):
    """Elastic Transcoder returns a warning if the resources used by your
    pipeline are not in the same region as the pipeline.

    Using resources in the same region, such as your Amazon S3 buckets,
    Amazon SNS notification topics, and AWS KMS key, reduces processing time
    and prevents cross-regional charges.
    """

    Code: String | None
    Message: String | None


Warnings = list[Warning]


class Pipeline(TypedDict, total=False):
    """The pipeline (queue) that is used to manage jobs."""

    Id: Id | None
    Arn: String | None
    Name: Name | None
    Status: PipelineStatus | None
    InputBucket: BucketName | None
    OutputBucket: BucketName | None
    Role: Role | None
    AwsKmsKeyArn: KeyArn | None
    Notifications: Notifications | None
    ContentConfig: PipelineOutputConfig | None
    ThumbnailConfig: PipelineOutputConfig | None


class CreatePipelineResponse(TypedDict, total=False):
    """When you create a pipeline, Elastic Transcoder returns the values that
    you specified in the request.
    """

    Pipeline: Pipeline | None
    Warnings: Warnings | None


class Thumbnails(TypedDict, total=False):
    """Thumbnails for videos."""

    Format: JpgOrPng | None
    Interval: Digits | None
    Resolution: ThumbnailResolution | None
    AspectRatio: AspectRatio | None
    MaxWidth: DigitsOrAuto | None
    MaxHeight: DigitsOrAuto | None
    SizingPolicy: SizingPolicy | None
    PaddingPolicy: PaddingPolicy | None


class PresetWatermark(TypedDict, total=False):
    """Settings for the size, location, and opacity of graphics that you want
    Elastic Transcoder to overlay over videos that are transcoded using this
    preset. You can specify settings for up to four watermarks. Watermarks
    appear in the specified size and location, and with the specified
    opacity for the duration of the transcoded video.

    Watermarks can be in .png or .jpg format. If you want to display a
    watermark that is not rectangular, use the .png format, which supports
    transparency.

    When you create a job that uses this preset, you specify the .png or
    .jpg graphics that you want Elastic Transcoder to include in the
    transcoded videos. You can specify fewer graphics in the job than you
    specify watermark settings in the preset, which allows you to use the
    same preset for up to four watermarks that have different dimensions.
    """

    Id: PresetWatermarkId | None
    MaxWidth: PixelsOrPercent | None
    MaxHeight: PixelsOrPercent | None
    SizingPolicy: WatermarkSizingPolicy | None
    HorizontalAlign: HorizontalAlign | None
    HorizontalOffset: PixelsOrPercent | None
    VerticalAlign: VerticalAlign | None
    VerticalOffset: PixelsOrPercent | None
    Opacity: Opacity | None
    Target: Target | None


PresetWatermarks = list[PresetWatermark]


class VideoParameters(TypedDict, total=False):
    """The ``VideoParameters`` structure."""

    Codec: VideoCodec | None
    CodecOptions: CodecOptions | None
    KeyframesMaxDist: KeyframesMaxDist | None
    FixedGOP: FixedGOP | None
    BitRate: VideoBitRate | None
    FrameRate: FrameRate | None
    MaxFrameRate: MaxFrameRate | None
    Resolution: Resolution | None
    AspectRatio: AspectRatio | None
    MaxWidth: DigitsOrAuto | None
    MaxHeight: DigitsOrAuto | None
    DisplayAspectRatio: AspectRatio | None
    SizingPolicy: SizingPolicy | None
    PaddingPolicy: PaddingPolicy | None
    Watermarks: PresetWatermarks | None


class CreatePresetRequest(ServiceRequest):
    """The ``CreatePresetRequest`` structure."""

    Name: Name
    Description: Description | None
    Container: PresetContainer
    Video: VideoParameters | None
    Audio: AudioParameters | None
    Thumbnails: Thumbnails | None


class Preset(TypedDict, total=False):
    """Presets are templates that contain most of the settings for transcoding
    media files from one format to another. Elastic Transcoder includes some
    default presets for common formats, for example, several iPod and iPhone
    versions. You can also create your own presets for formats that aren't
    included among the default presets. You specify which preset you want to
    use when you create a job.
    """

    Id: Id | None
    Arn: String | None
    Name: Name | None
    Description: Description | None
    Container: PresetContainer | None
    Audio: AudioParameters | None
    Video: VideoParameters | None
    Thumbnails: Thumbnails | None
    Type: PresetType | None


class CreatePresetResponse(TypedDict, total=False):
    """The ``CreatePresetResponse`` structure."""

    Preset: Preset | None
    Warning: String | None


class DeletePipelineRequest(ServiceRequest):
    """The ``DeletePipelineRequest`` structure."""

    Id: Id


class DeletePipelineResponse(TypedDict, total=False):
    """The ``DeletePipelineResponse`` structure."""

    pass


class DeletePresetRequest(ServiceRequest):
    """The ``DeletePresetRequest`` structure."""

    Id: Id


class DeletePresetResponse(TypedDict, total=False):
    """The ``DeletePresetResponse`` structure."""

    pass


ExceptionMessages = list[String]
Jobs = list[Job]


class ListJobsByPipelineRequest(ServiceRequest):
    """The ``ListJobsByPipelineRequest`` structure."""

    PipelineId: Id
    Ascending: Ascending | None
    PageToken: Id | None


class ListJobsByPipelineResponse(TypedDict, total=False):
    """The ``ListJobsByPipelineResponse`` structure."""

    Jobs: Jobs | None
    NextPageToken: Id | None


class ListJobsByStatusRequest(ServiceRequest):
    """The ``ListJobsByStatusRequest`` structure."""

    Status: JobStatus
    Ascending: Ascending | None
    PageToken: Id | None


class ListJobsByStatusResponse(TypedDict, total=False):
    """The ``ListJobsByStatusResponse`` structure."""

    Jobs: Jobs | None
    NextPageToken: Id | None


class ListPipelinesRequest(ServiceRequest):
    """The ``ListPipelineRequest`` structure."""

    Ascending: Ascending | None
    PageToken: Id | None


Pipelines = list[Pipeline]


class ListPipelinesResponse(TypedDict, total=False):
    """A list of the pipelines associated with the current AWS account."""

    Pipelines: Pipelines | None
    NextPageToken: Id | None


class ListPresetsRequest(ServiceRequest):
    """The ``ListPresetsRequest`` structure."""

    Ascending: Ascending | None
    PageToken: Id | None


Presets = list[Preset]


class ListPresetsResponse(TypedDict, total=False):
    """The ``ListPresetsResponse`` structure."""

    Presets: Presets | None
    NextPageToken: Id | None


class ReadJobRequest(ServiceRequest):
    """The ``ReadJobRequest`` structure."""

    Id: Id


class ReadJobResponse(TypedDict, total=False):
    """The ``ReadJobResponse`` structure."""

    Job: Job | None


class ReadPipelineRequest(ServiceRequest):
    """The ``ReadPipelineRequest`` structure."""

    Id: Id


class ReadPipelineResponse(TypedDict, total=False):
    """The ``ReadPipelineResponse`` structure."""

    Pipeline: Pipeline | None
    Warnings: Warnings | None


class ReadPresetRequest(ServiceRequest):
    """The ``ReadPresetRequest`` structure."""

    Id: Id


class ReadPresetResponse(TypedDict, total=False):
    """The ``ReadPresetResponse`` structure."""

    Preset: Preset | None


SnsTopics = list[SnsTopic]


class TestRoleRequest(ServiceRequest):
    """The ``TestRoleRequest`` structure."""

    Role: Role
    InputBucket: BucketName
    OutputBucket: BucketName
    Topics: SnsTopics


class TestRoleResponse(TypedDict, total=False):
    """The ``TestRoleResponse`` structure."""

    Success: Success | None
    Messages: ExceptionMessages | None


class UpdatePipelineNotificationsRequest(ServiceRequest):
    """The ``UpdatePipelineNotificationsRequest`` structure."""

    Id: Id
    Notifications: Notifications


class UpdatePipelineNotificationsResponse(TypedDict, total=False):
    """The ``UpdatePipelineNotificationsResponse`` structure."""

    Pipeline: Pipeline | None


class UpdatePipelineRequest(ServiceRequest):
    """The ``UpdatePipelineRequest`` structure."""

    Id: Id
    Name: Name | None
    InputBucket: BucketName | None
    Role: Role | None
    AwsKmsKeyArn: KeyArn | None
    Notifications: Notifications | None
    ContentConfig: PipelineOutputConfig | None
    ThumbnailConfig: PipelineOutputConfig | None


class UpdatePipelineResponse(TypedDict, total=False):
    """When you update a pipeline, Elastic Transcoder returns the values that
    you specified in the request.
    """

    Pipeline: Pipeline | None
    Warnings: Warnings | None


class UpdatePipelineStatusRequest(ServiceRequest):
    """The ``UpdatePipelineStatusRequest`` structure."""

    Id: Id
    Status: PipelineStatus


class UpdatePipelineStatusResponse(TypedDict, total=False):
    """When you update status for a pipeline, Elastic Transcoder returns the
    values that you specified in the request.
    """

    Pipeline: Pipeline | None


class ElastictranscoderApi:
    service: str = "elastictranscoder"
    version: str = "2012-09-25"

    @handler("CancelJob")
    def cancel_job(self, context: RequestContext, id: Id, **kwargs) -> CancelJobResponse:
        """The CancelJob operation cancels an unfinished job.

        You can only cancel a job that has a status of ``Submitted``. To prevent
        a pipeline from starting to process a job while you're getting the job
        identifier, use UpdatePipelineStatus to temporarily pause the pipeline.

        :param id: The identifier of the job that you want to cancel.
        :returns: CancelJobResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises ResourceNotFoundException:
        :raises ResourceInUseException:
        :raises AccessDeniedException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("CreateJob")
    def create_job(
        self,
        context: RequestContext,
        pipeline_id: Id,
        input: JobInput | None = None,
        inputs: JobInputs | None = None,
        output: CreateJobOutput | None = None,
        outputs: CreateJobOutputs | None = None,
        output_key_prefix: Key | None = None,
        playlists: CreateJobPlaylists | None = None,
        user_metadata: UserMetadata | None = None,
        **kwargs,
    ) -> CreateJobResponse:
        """When you create a job, Elastic Transcoder returns JSON data that
        includes the values that you specified plus information about the job
        that is created.

        If you have specified more than one output for your jobs (for example,
        one output for the Kindle Fire and another output for the Apple iPhone
        4s), you currently must use the Elastic Transcoder API to list the jobs
        (as opposed to the AWS Console).

        :param pipeline_id: The ``Id`` of the pipeline that you want Elastic Transcoder to use for
        transcoding.
        :param input: A section of the request body that provides information about the file
        that is being transcoded.
        :param inputs: A section of the request body that provides information about the files
        that are being transcoded.
        :param output: A section of the request body that provides information about the
        transcoded (target) file.
        :param outputs: A section of the request body that provides information about the
        transcoded (target) files.
        :param output_key_prefix: The value, if any, that you want Elastic Transcoder to prepend to the
        names of all files that this job creates, including output files,
        thumbnails, and playlists.
        :param playlists: If you specify a preset in ``PresetId`` for which the value of
        ``Container`` is fmp4 (Fragmented MP4) or ts (MPEG-TS), Playlists
        contains information about the master playlists that you want Elastic
        Transcoder to create.
        :param user_metadata: User-defined metadata that you want to associate with an Elastic
        Transcoder job.
        :returns: CreateJobResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises LimitExceededException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("CreatePipeline")
    def create_pipeline(
        self,
        context: RequestContext,
        name: Name,
        input_bucket: BucketName,
        role: Role,
        output_bucket: BucketName | None = None,
        aws_kms_key_arn: KeyArn | None = None,
        notifications: Notifications | None = None,
        content_config: PipelineOutputConfig | None = None,
        thumbnail_config: PipelineOutputConfig | None = None,
        **kwargs,
    ) -> CreatePipelineResponse:
        """The CreatePipeline operation creates a pipeline with settings that you
        specify.

        :param name: The name of the pipeline.
        :param input_bucket: The Amazon S3 bucket in which you saved the media files that you want to
        transcode.
        :param role: The IAM Amazon Resource Name (ARN) for the role that you want Elastic
        Transcoder to use to create the pipeline.
        :param output_bucket: The Amazon S3 bucket in which you want Elastic Transcoder to save the
        transcoded files.
        :param aws_kms_key_arn: The AWS Key Management Service (AWS KMS) key that you want to use with
        this pipeline.
        :param notifications: The Amazon Simple Notification Service (Amazon SNS) topic that you want
        to notify to report job status.
        :param content_config: The optional ``ContentConfig`` object specifies information about the
        Amazon S3 bucket in which you want Elastic Transcoder to save transcoded
        files and playlists: which bucket to use, which users you want to have
        access to the files, the type of access you want users to have, and the
        storage class that you want to assign to the files.
        :param thumbnail_config: The ``ThumbnailConfig`` object specifies several values, including the
        Amazon S3 bucket in which you want Elastic Transcoder to save thumbnail
        files, which users you want to have access to the files, the type of
        access you want users to have, and the storage class that you want to
        assign to the files.
        :returns: CreatePipelineResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises LimitExceededException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("CreatePreset")
    def create_preset(
        self,
        context: RequestContext,
        name: Name,
        container: PresetContainer,
        description: Description | None = None,
        video: VideoParameters | None = None,
        audio: AudioParameters | None = None,
        thumbnails: Thumbnails | None = None,
        **kwargs,
    ) -> CreatePresetResponse:
        """The CreatePreset operation creates a preset with settings that you
        specify.

        Elastic Transcoder checks the CreatePreset settings to ensure that they
        meet Elastic Transcoder requirements and to determine whether they
        comply with H.264 standards. If your settings are not valid for Elastic
        Transcoder, Elastic Transcoder returns an HTTP 400 response
        (``ValidationException``) and does not create the preset. If the
        settings are valid for Elastic Transcoder but aren't strictly compliant
        with the H.264 standard, Elastic Transcoder creates the preset and
        returns a warning message in the response. This helps you determine
        whether your settings comply with the H.264 standard while giving you
        greater flexibility with respect to the video that Elastic Transcoder
        produces.

        Elastic Transcoder uses the H.264 video-compression format. For more
        information, see the International Telecommunication Union publication
        *Recommendation ITU-T H.264: Advanced video coding for generic
        audiovisual services*.

        :param name: The name of the preset.
        :param container: The container type for the output file.
        :param description: A description of the preset.
        :param video: A section of the request body that specifies the video parameters.
        :param audio: A section of the request body that specifies the audio parameters.
        :param thumbnails: A section of the request body that specifies the thumbnail parameters,
        if any.
        :returns: CreatePresetResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises AccessDeniedException:
        :raises LimitExceededException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("DeletePipeline")
    def delete_pipeline(self, context: RequestContext, id: Id, **kwargs) -> DeletePipelineResponse:
        """The DeletePipeline operation removes a pipeline.

        You can only delete a pipeline that has never been used or that is not
        currently in use (doesn't contain any active jobs). If the pipeline is
        currently in use, ``DeletePipeline`` returns an error.

        :param id: The identifier of the pipeline that you want to delete.
        :returns: DeletePipelineResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises ResourceNotFoundException:
        :raises ResourceInUseException:
        :raises AccessDeniedException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("DeletePreset")
    def delete_preset(self, context: RequestContext, id: Id, **kwargs) -> DeletePresetResponse:
        """The DeletePreset operation removes a preset that you've added in an AWS
        region.

        You can't delete the default presets that are included with Elastic
        Transcoder.

        :param id: The identifier of the preset for which you want to get detailed
        information.
        :returns: DeletePresetResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("ListJobsByPipeline")
    def list_jobs_by_pipeline(
        self,
        context: RequestContext,
        pipeline_id: Id,
        ascending: Ascending | None = None,
        page_token: Id | None = None,
        **kwargs,
    ) -> ListJobsByPipelineResponse:
        """The ListJobsByPipeline operation gets a list of the jobs currently in a
        pipeline.

        Elastic Transcoder returns all of the jobs currently in the specified
        pipeline. The response body contains one element for each job that
        satisfies the search criteria.

        :param pipeline_id: The ID of the pipeline for which you want to get job information.
        :param ascending: To list jobs in chronological order by the date and time that they were
        submitted, enter ``true``.
        :param page_token: When Elastic Transcoder returns more than one page of results, use
        ``pageToken`` in subsequent ``GET`` requests to get each successive page
        of results.
        :returns: ListJobsByPipelineResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("ListJobsByStatus")
    def list_jobs_by_status(
        self,
        context: RequestContext,
        status: JobStatus,
        ascending: Ascending | None = None,
        page_token: Id | None = None,
        **kwargs,
    ) -> ListJobsByStatusResponse:
        """The ListJobsByStatus operation gets a list of jobs that have a specified
        status. The response body contains one element for each job that
        satisfies the search criteria.

        :param status: To get information about all of the jobs associated with the current AWS
        account that have a given status, specify the following status:
        ``Submitted``, ``Progressing``, ``Complete``, ``Canceled``, or
        ``Error``.
        :param ascending: To list jobs in chronological order by the date and time that they were
        submitted, enter ``true``.
        :param page_token: When Elastic Transcoder returns more than one page of results, use
        ``pageToken`` in subsequent ``GET`` requests to get each successive page
        of results.
        :returns: ListJobsByStatusResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("ListPipelines")
    def list_pipelines(
        self,
        context: RequestContext,
        ascending: Ascending | None = None,
        page_token: Id | None = None,
        **kwargs,
    ) -> ListPipelinesResponse:
        """The ListPipelines operation gets a list of the pipelines associated with
        the current AWS account.

        :param ascending: To list pipelines in chronological order by the date and time that they
        were created, enter ``true``.
        :param page_token: When Elastic Transcoder returns more than one page of results, use
        ``pageToken`` in subsequent ``GET`` requests to get each successive page
        of results.
        :returns: ListPipelinesResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises AccessDeniedException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("ListPresets")
    def list_presets(
        self,
        context: RequestContext,
        ascending: Ascending | None = None,
        page_token: Id | None = None,
        **kwargs,
    ) -> ListPresetsResponse:
        """The ListPresets operation gets a list of the default presets included
        with Elastic Transcoder and the presets that you've added in an AWS
        region.

        :param ascending: To list presets in chronological order by the date and time that they
        were created, enter ``true``.
        :param page_token: When Elastic Transcoder returns more than one page of results, use
        ``pageToken`` in subsequent ``GET`` requests to get each successive page
        of results.
        :returns: ListPresetsResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises AccessDeniedException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("ReadJob")
    def read_job(self, context: RequestContext, id: Id, **kwargs) -> ReadJobResponse:
        """The ReadJob operation returns detailed information about a job.

        :param id: The identifier of the job for which you want to get detailed
        information.
        :returns: ReadJobResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("ReadPipeline")
    def read_pipeline(self, context: RequestContext, id: Id, **kwargs) -> ReadPipelineResponse:
        """The ReadPipeline operation gets detailed information about a pipeline.

        :param id: The identifier of the pipeline to read.
        :returns: ReadPipelineResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("ReadPreset")
    def read_preset(self, context: RequestContext, id: Id, **kwargs) -> ReadPresetResponse:
        """The ReadPreset operation gets detailed information about a preset.

        :param id: The identifier of the preset for which you want to get detailed
        information.
        :returns: ReadPresetResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("TestRole")
    def test_role(
        self,
        context: RequestContext,
        role: Role,
        input_bucket: BucketName,
        output_bucket: BucketName,
        topics: SnsTopics,
        **kwargs,
    ) -> TestRoleResponse:
        """The TestRole operation tests the IAM role used to create the pipeline.

        The ``TestRole`` action lets you determine whether the IAM role you are
        using has sufficient permissions to let Elastic Transcoder perform tasks
        associated with the transcoding process. The action attempts to assume
        the specified IAM role, checks read access to the input and output
        buckets, and tries to send a test notification to Amazon SNS topics that
        you specify.

        :param role: The IAM Amazon Resource Name (ARN) for the role that you want Elastic
        Transcoder to test.
        :param input_bucket: The Amazon S3 bucket that contains media files to be transcoded.
        :param output_bucket: The Amazon S3 bucket that Elastic Transcoder writes transcoded media
        files to.
        :param topics: The ARNs of one or more Amazon Simple Notification Service (Amazon SNS)
        topics that you want the action to send a test notification to.
        :returns: TestRoleResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("UpdatePipeline")
    def update_pipeline(
        self,
        context: RequestContext,
        id: Id,
        name: Name | None = None,
        input_bucket: BucketName | None = None,
        role: Role | None = None,
        aws_kms_key_arn: KeyArn | None = None,
        notifications: Notifications | None = None,
        content_config: PipelineOutputConfig | None = None,
        thumbnail_config: PipelineOutputConfig | None = None,
        **kwargs,
    ) -> UpdatePipelineResponse:
        """Use the ``UpdatePipeline`` operation to update settings for a pipeline.

        When you change pipeline settings, your changes take effect immediately.
        Jobs that you have already submitted and that Elastic Transcoder has not
        started to process are affected in addition to jobs that you submit
        after you change settings.

        :param id: The ID of the pipeline that you want to update.
        :param name: The name of the pipeline.
        :param input_bucket: The Amazon S3 bucket in which you saved the media files that you want to
        transcode and the graphics that you want to use as watermarks.
        :param role: The IAM Amazon Resource Name (ARN) for the role that you want Elastic
        Transcoder to use to transcode jobs for this pipeline.
        :param aws_kms_key_arn: The AWS Key Management Service (AWS KMS) key that you want to use with
        this pipeline.
        :param notifications: The topic ARN for the Amazon Simple Notification Service (Amazon SNS)
        topic that you want to notify to report job status.
        :param content_config: The optional ``ContentConfig`` object specifies information about the
        Amazon S3 bucket in which you want Elastic Transcoder to save transcoded
        files and playlists: which bucket to use, which users you want to have
        access to the files, the type of access you want users to have, and the
        storage class that you want to assign to the files.
        :param thumbnail_config: The ``ThumbnailConfig`` object specifies several values, including the
        Amazon S3 bucket in which you want Elastic Transcoder to save thumbnail
        files, which users you want to have access to the files, the type of
        access you want users to have, and the storage class that you want to
        assign to the files.
        :returns: UpdatePipelineResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises AccessDeniedException:
        :raises ResourceInUseException:
        :raises ResourceNotFoundException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("UpdatePipelineNotifications")
    def update_pipeline_notifications(
        self, context: RequestContext, id: Id, notifications: Notifications, **kwargs
    ) -> UpdatePipelineNotificationsResponse:
        """With the UpdatePipelineNotifications operation, you can update Amazon
        Simple Notification Service (Amazon SNS) notifications for a pipeline.

        When you update notifications for a pipeline, Elastic Transcoder returns
        the values that you specified in the request.

        :param id: The identifier of the pipeline for which you want to change notification
        settings.
        :param notifications: The topic ARN for the Amazon Simple Notification Service (Amazon SNS)
        topic that you want to notify to report job status.
        :returns: UpdatePipelineNotificationsResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises ResourceNotFoundException:
        :raises ResourceInUseException:
        :raises AccessDeniedException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("UpdatePipelineStatus")
    def update_pipeline_status(
        self, context: RequestContext, id: Id, status: PipelineStatus, **kwargs
    ) -> UpdatePipelineStatusResponse:
        """The UpdatePipelineStatus operation pauses or reactivates a pipeline, so
        that the pipeline stops or restarts the processing of jobs.

        Changing the pipeline status is useful if you want to cancel one or more
        jobs. You can't cancel jobs after Elastic Transcoder has started
        processing them; if you pause the pipeline to which you submitted the
        jobs, you have more time to get the job IDs for the jobs that you want
        to cancel, and to send a CancelJob request.

        :param id: The identifier of the pipeline to update.
        :param status: The desired status of the pipeline:

        -  ``Active``: The pipeline is processing jobs.
        :returns: UpdatePipelineStatusResponse
        :raises ValidationException:
        :raises IncompatibleVersionException:
        :raises ResourceNotFoundException:
        :raises ResourceInUseException:
        :raises AccessDeniedException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

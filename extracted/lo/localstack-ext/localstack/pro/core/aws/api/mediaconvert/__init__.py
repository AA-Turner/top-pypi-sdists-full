from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

_boolean = bool
_double = float
_doubleMin0 = float
_doubleMin0Max1 = float
_doubleMin0Max2147483647 = float
_doubleMin1Max10 = float
_doubleMinNegative59Max0 = float
_doubleMinNegative60Max3 = float
_doubleMinNegative60Max6 = float
_doubleMinNegative60MaxNegative1 = float
_doubleMinNegative6Max3 = float
_doubleMinNegative8Max0 = float
_integer = int
_integerMin0Max0 = int
_integerMin0Max1 = int
_integerMin0Max10 = int
_integerMin0Max100 = int
_integerMin0Max1000 = int
_integerMin0Max10000 = int
_integerMin0Max1152000000 = int
_integerMin0Max128 = int
_integerMin0Max1466400000 = int
_integerMin0Max15 = int
_integerMin0Max16 = int
_integerMin0Max2147483647 = int
_integerMin0Max255 = int
_integerMin0Max3 = int
_integerMin0Max30 = int
_integerMin0Max30000 = int
_integerMin0Max3600 = int
_integerMin0Max4 = int
_integerMin0Max4000 = int
_integerMin0Max4194303 = int
_integerMin0Max47185920 = int
_integerMin0Max5 = int
_integerMin0Max500 = int
_integerMin0Max50000 = int
_integerMin0Max65534 = int
_integerMin0Max65535 = int
_integerMin0Max7 = int
_integerMin0Max8 = int
_integerMin0Max9 = int
_integerMin0Max96 = int
_integerMin0Max99 = int
_integerMin100000Max100000000 = int
_integerMin1000Max1152000000 = int
_integerMin1000Max1466400000 = int
_integerMin1000Max288000000 = int
_integerMin1000Max30000 = int
_integerMin1000Max300000000 = int
_integerMin1000Max480000000 = int
_integerMin100Max1000 = int
_integerMin10Max48 = int
_integerMin16000Max320000 = int
_integerMin16000Max48000 = int
_integerMin16Max24 = int
_integerMin1Max1 = int
_integerMin1Max10 = int
_integerMin1Max100 = int
_integerMin1Max10000000 = int
_integerMin1Max1001 = int
_integerMin1Max150 = int
_integerMin1Max17895697 = int
_integerMin1Max2 = int
_integerMin1Max20 = int
_integerMin1Max2048 = int
_integerMin1Max2147483640 = int
_integerMin1Max2147483647 = int
_integerMin1Max31 = int
_integerMin1Max32 = int
_integerMin1Max4 = int
_integerMin1Max4096 = int
_integerMin1Max512 = int
_integerMin1Max6 = int
_integerMin1Max60000 = int
_integerMin1Max64 = int
_integerMin1Max8 = int
_integerMin1Max86400000 = int
_integerMin2000Max30000 = int
_integerMin22050Max192000 = int
_integerMin22050Max48000 = int
_integerMin24Max60000 = int
_integerMin256Max3840 = int
_integerMin25Max10000 = int
_integerMin25Max2000 = int
_integerMin2Max2147483647 = int
_integerMin2Max4096 = int
_integerMin32000Max192000 = int
_integerMin32000Max3024000 = int
_integerMin32000Max384000 = int
_integerMin32000Max48000 = int
_integerMin32Max8182 = int
_integerMin32Max8192 = int
_integerMin384000Max1024000 = int
_integerMin3Max15 = int
_integerMin48000Max48000 = int
_integerMin4Max12 = int
_integerMin6000Max1024000 = int
_integerMin64000Max640000 = int
_integerMin64Max2160 = int
_integerMin6Max16 = int
_integerMin8000Max192000 = int
_integerMin8000Max96000 = int
_integerMin8Max12 = int
_integerMin8Max4096 = int
_integerMin90Max105 = int
_integerMin920Max1023 = int
_integerMin96Max600 = int
_integerMinNegative10000Max10000 = int
_integerMinNegative1000Max1000 = int
_integerMinNegative180Max180 = int
_integerMinNegative1Max10 = int
_integerMinNegative1Max2147483647 = int
_integerMinNegative1Max3 = int
_integerMinNegative2147483648Max2147483647 = int
_integerMinNegative2Max3 = int
_integerMinNegative50Max50 = int
_integerMinNegative5Max10 = int
_integerMinNegative60Max6 = int
_integerMinNegative70Max0 = int
_string = str
_stringMax100 = str
_stringMax1000 = str
_stringMax2048 = str
_stringMax2048PatternS3Https = str
_stringMax256 = str
_stringMin0 = str
_stringMin1 = str
_stringMin11Max11Pattern01D20305D205D = str
_stringMin14PatternS3BmpBMPPngPNGHttpsBmpBMPPngPNG = str
_stringMin14PatternS3BmpBMPPngPNGTgaTGAHttpsBmpBMPPngPNGTgaTGA = str
_stringMin14PatternS3CubeCUBEHttpsCubeCUBE = str
_stringMin14PatternS3Mov09PngHttpsMov09Png = str
_stringMin14PatternS3SccSCCTtmlTTMLDfxpDFXPStlSTLSrtSRTXmlXMLSmiSMIVttVTTWebvttWEBVTTHttpsSccSCCTtmlTTMLDfxpDFXPStlSTLSrtSRTXmlXMLSmiSMIVttVTTWebvttWEBVTT = str
_stringMin14PatternS3XmlXMLHttpsXmlXML = str
_stringMin16Max24PatternAZaZ0922AZaZ0916 = str
_stringMin1Max100000 = str
_stringMin1Max20 = str
_stringMin1Max2048PatternArnAZSecretsmanagerWD12SecretAZAZ09 = str
_stringMin1Max256 = str
_stringMin1Max50 = str
_stringMin1Max50PatternAZAZ09 = str
_stringMin1PatternArnAwsUsGovCnKmsAZ26EastWestCentralNorthSouthEastWest1912D12KeyAFAF098AFAF094AFAF094AFAF094AFAF0912MrkAFAF0932 = str
_stringMin24Max512PatternAZaZ0902 = str
_stringMin32Max32Pattern09aFAF32 = str
_stringMin36Max36Pattern09aFAF809aFAF409aFAF409aFAF409aFAF12 = str
_stringMin3Max3Pattern1809aFAF09aEAE = str
_stringMin3Max3PatternAZaZ3 = str
_stringMin6Max8Pattern09aFAF609aFAF2 = str
_stringMin9Max19PatternAZ26EastWestCentralNorthSouthEastWest1912 = str
_stringPattern = str
_stringPattern010920405090509092 = str
_stringPattern010920405090509092090909 = str
_stringPattern019090190908019090190908 = str
_stringPattern01D20305D205D = str
_stringPattern0940191020191209301 = str
_stringPattern09aFAF809aFAF409aFAF409aFAF409aFAF12 = str
_stringPattern0xAFaF0908190908 = str
_stringPatternAZaZ0902 = str
_stringPatternAZaZ0932 = str
_stringPatternAZaZ23AZaZ = str
_stringPatternAZaZ23AZaZ09 = str
_stringPatternArnAwsAZ09EventsAZ090912ConnectionAZAZ09AF0936 = str
_stringPatternArnAwsUsGovAcm = str
_stringPatternArnAwsUsGovCnKmsAZ26EastWestCentralNorthSouthEastWest1912D12KeyAFAF098AFAF094AFAF094AFAF094AFAF0912MrkAFAF0932 = str
_stringPatternDD = str
_stringPatternHttps = str
_stringPatternHttpsD = str
_stringPatternHttpsKantarmedia = str
_stringPatternIdentityAZaZ26AZaZ09163 = str
_stringPatternS3 = str
_stringPatternS3ASSETMAPXml = str
_stringPatternS3Https = str
_stringPatternS3TtfHttpsTtf = str
_stringPatternSNManifestConfirmConditionNotificationNS = str
_stringPatternSNSignalProcessingNotificationNS = str
_stringPatternW = str
_stringPatternWS = str


class AacAudioDescriptionBroadcasterMix(StrEnum):
    BROADCASTER_MIXED_AD = "BROADCASTER_MIXED_AD"
    NORMAL = "NORMAL"


class AacCodecProfile(StrEnum):
    LC = "LC"
    HEV1 = "HEV1"
    HEV2 = "HEV2"
    XHE = "XHE"


class AacCodingMode(StrEnum):
    AD_RECEIVER_MIX = "AD_RECEIVER_MIX"
    CODING_MODE_1_0 = "CODING_MODE_1_0"
    CODING_MODE_1_1 = "CODING_MODE_1_1"
    CODING_MODE_2_0 = "CODING_MODE_2_0"
    CODING_MODE_5_1 = "CODING_MODE_5_1"


class AacLoudnessMeasurementMode(StrEnum):
    PROGRAM = "PROGRAM"
    ANCHOR = "ANCHOR"


class AacRateControlMode(StrEnum):
    CBR = "CBR"
    VBR = "VBR"


class AacRawFormat(StrEnum):
    LATM_LOAS = "LATM_LOAS"
    NONE = "NONE"


class AacSpecification(StrEnum):
    MPEG2 = "MPEG2"
    MPEG4 = "MPEG4"


class AacVbrQuality(StrEnum):
    LOW = "LOW"
    MEDIUM_LOW = "MEDIUM_LOW"
    MEDIUM_HIGH = "MEDIUM_HIGH"
    HIGH = "HIGH"


class Ac3BitstreamMode(StrEnum):
    COMPLETE_MAIN = "COMPLETE_MAIN"
    COMMENTARY = "COMMENTARY"
    DIALOGUE = "DIALOGUE"
    EMERGENCY = "EMERGENCY"
    HEARING_IMPAIRED = "HEARING_IMPAIRED"
    MUSIC_AND_EFFECTS = "MUSIC_AND_EFFECTS"
    VISUALLY_IMPAIRED = "VISUALLY_IMPAIRED"
    VOICE_OVER = "VOICE_OVER"


class Ac3CodingMode(StrEnum):
    CODING_MODE_1_0 = "CODING_MODE_1_0"
    CODING_MODE_1_1 = "CODING_MODE_1_1"
    CODING_MODE_2_0 = "CODING_MODE_2_0"
    CODING_MODE_3_2_LFE = "CODING_MODE_3_2_LFE"


class Ac3DynamicRangeCompressionLine(StrEnum):
    FILM_STANDARD = "FILM_STANDARD"
    FILM_LIGHT = "FILM_LIGHT"
    MUSIC_STANDARD = "MUSIC_STANDARD"
    MUSIC_LIGHT = "MUSIC_LIGHT"
    SPEECH = "SPEECH"
    NONE = "NONE"


class Ac3DynamicRangeCompressionProfile(StrEnum):
    FILM_STANDARD = "FILM_STANDARD"
    NONE = "NONE"


class Ac3DynamicRangeCompressionRf(StrEnum):
    FILM_STANDARD = "FILM_STANDARD"
    FILM_LIGHT = "FILM_LIGHT"
    MUSIC_STANDARD = "MUSIC_STANDARD"
    MUSIC_LIGHT = "MUSIC_LIGHT"
    SPEECH = "SPEECH"
    NONE = "NONE"


class Ac3LfeFilter(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class Ac3MetadataControl(StrEnum):
    FOLLOW_INPUT = "FOLLOW_INPUT"
    USE_CONFIGURED = "USE_CONFIGURED"


class AccelerationMode(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"
    PREFERRED = "PREFERRED"


class AccelerationStatus(StrEnum):
    NOT_APPLICABLE = "NOT_APPLICABLE"
    IN_PROGRESS = "IN_PROGRESS"
    ACCELERATED = "ACCELERATED"
    NOT_ACCELERATED = "NOT_ACCELERATED"


class AdvancedInputFilter(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class AdvancedInputFilterAddTexture(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class AdvancedInputFilterSharpen(StrEnum):
    OFF = "OFF"
    LOW = "LOW"
    HIGH = "HIGH"


class AfdSignaling(StrEnum):
    NONE = "NONE"
    AUTO = "AUTO"
    FIXED = "FIXED"


class AlphaBehavior(StrEnum):
    DISCARD = "DISCARD"
    REMAP_TO_LUMA = "REMAP_TO_LUMA"


class AncillaryConvert608To708(StrEnum):
    UPCONVERT = "UPCONVERT"
    DISABLED = "DISABLED"


class AncillaryTerminateCaptions(StrEnum):
    END_OF_INPUT = "END_OF_INPUT"
    DISABLED = "DISABLED"


class AntiAlias(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class AudioChannelTag(StrEnum):
    L = "L"
    R = "R"
    C = "C"
    LFE = "LFE"
    LS = "LS"
    RS = "RS"
    LC = "LC"
    RC = "RC"
    CS = "CS"
    LSD = "LSD"
    RSD = "RSD"
    TCS = "TCS"
    VHL = "VHL"
    VHC = "VHC"
    VHR = "VHR"
    TBL = "TBL"
    TBC = "TBC"
    TBR = "TBR"
    RSL = "RSL"
    RSR = "RSR"
    LW = "LW"
    RW = "RW"
    LFE2 = "LFE2"
    LT = "LT"
    RT = "RT"
    HI = "HI"
    NAR = "NAR"
    M = "M"


class AudioCodec(StrEnum):
    AAC = "AAC"
    MP2 = "MP2"
    MP3 = "MP3"
    WAV = "WAV"
    AIFF = "AIFF"
    AC3 = "AC3"
    EAC3 = "EAC3"
    EAC3_ATMOS = "EAC3_ATMOS"
    VORBIS = "VORBIS"
    OPUS = "OPUS"
    PASSTHROUGH = "PASSTHROUGH"
    FLAC = "FLAC"


class AudioDefaultSelection(StrEnum):
    DEFAULT = "DEFAULT"
    NOT_DEFAULT = "NOT_DEFAULT"


class AudioDurationCorrection(StrEnum):
    DISABLED = "DISABLED"
    AUTO = "AUTO"
    TRACK = "TRACK"
    FRAME = "FRAME"
    FORCE = "FORCE"


class AudioLanguageCodeControl(StrEnum):
    FOLLOW_INPUT = "FOLLOW_INPUT"
    USE_CONFIGURED = "USE_CONFIGURED"


class AudioNormalizationAlgorithm(StrEnum):
    ITU_BS_1770_1 = "ITU_BS_1770_1"
    ITU_BS_1770_2 = "ITU_BS_1770_2"
    ITU_BS_1770_3 = "ITU_BS_1770_3"
    ITU_BS_1770_4 = "ITU_BS_1770_4"


class AudioNormalizationAlgorithmControl(StrEnum):
    CORRECT_AUDIO = "CORRECT_AUDIO"
    MEASURE_ONLY = "MEASURE_ONLY"


class AudioNormalizationLoudnessLogging(StrEnum):
    LOG = "LOG"
    DONT_LOG = "DONT_LOG"


class AudioNormalizationPeakCalculation(StrEnum):
    TRUE_PEAK = "TRUE_PEAK"
    NONE = "NONE"


class AudioSelectorType(StrEnum):
    PID = "PID"
    TRACK = "TRACK"
    LANGUAGE_CODE = "LANGUAGE_CODE"
    HLS_RENDITION_GROUP = "HLS_RENDITION_GROUP"
    ALL_PCM = "ALL_PCM"
    STREAM = "STREAM"


class AudioTypeControl(StrEnum):
    FOLLOW_INPUT = "FOLLOW_INPUT"
    USE_CONFIGURED = "USE_CONFIGURED"


class Av1AdaptiveQuantization(StrEnum):
    OFF = "OFF"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    HIGHER = "HIGHER"
    MAX = "MAX"


class Av1BitDepth(StrEnum):
    BIT_8 = "BIT_8"
    BIT_10 = "BIT_10"


class Av1FilmGrainSynthesis(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class Av1FramerateControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class Av1FramerateConversionAlgorithm(StrEnum):
    DUPLICATE_DROP = "DUPLICATE_DROP"
    INTERPOLATE = "INTERPOLATE"
    FRAMEFORMER = "FRAMEFORMER"
    MAINTAIN_FRAME_COUNT = "MAINTAIN_FRAME_COUNT"


class Av1RateControlMode(StrEnum):
    QVBR = "QVBR"


class Av1SpatialAdaptiveQuantization(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class AvcIntraClass(StrEnum):
    CLASS_50 = "CLASS_50"
    CLASS_100 = "CLASS_100"
    CLASS_200 = "CLASS_200"
    CLASS_4K_2K = "CLASS_4K_2K"


class AvcIntraFramerateControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class AvcIntraFramerateConversionAlgorithm(StrEnum):
    DUPLICATE_DROP = "DUPLICATE_DROP"
    INTERPOLATE = "INTERPOLATE"
    FRAMEFORMER = "FRAMEFORMER"
    MAINTAIN_FRAME_COUNT = "MAINTAIN_FRAME_COUNT"


class AvcIntraInterlaceMode(StrEnum):
    PROGRESSIVE = "PROGRESSIVE"
    TOP_FIELD = "TOP_FIELD"
    BOTTOM_FIELD = "BOTTOM_FIELD"
    FOLLOW_TOP_FIELD = "FOLLOW_TOP_FIELD"
    FOLLOW_BOTTOM_FIELD = "FOLLOW_BOTTOM_FIELD"


class AvcIntraScanTypeConversionMode(StrEnum):
    INTERLACED = "INTERLACED"
    INTERLACED_OPTIMIZE = "INTERLACED_OPTIMIZE"


class AvcIntraSlowPal(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class AvcIntraTelecine(StrEnum):
    NONE = "NONE"
    HARD = "HARD"


class AvcIntraUhdQualityTuningLevel(StrEnum):
    SINGLE_PASS = "SINGLE_PASS"
    MULTI_PASS = "MULTI_PASS"


class BandwidthReductionFilterSharpening(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    OFF = "OFF"


class BandwidthReductionFilterStrength(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    AUTO = "AUTO"
    OFF = "OFF"


class BillingTagsSource(StrEnum):
    QUEUE = "QUEUE"
    PRESET = "PRESET"
    JOB_TEMPLATE = "JOB_TEMPLATE"
    JOB = "JOB"


class BurnInSubtitleStylePassthrough(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class BurninSubtitleAlignment(StrEnum):
    CENTERED = "CENTERED"
    LEFT = "LEFT"
    AUTO = "AUTO"


class BurninSubtitleApplyFontColor(StrEnum):
    WHITE_TEXT_ONLY = "WHITE_TEXT_ONLY"
    ALL_TEXT = "ALL_TEXT"


class BurninSubtitleBackgroundColor(StrEnum):
    NONE = "NONE"
    BLACK = "BLACK"
    WHITE = "WHITE"
    AUTO = "AUTO"


class BurninSubtitleFallbackFont(StrEnum):
    BEST_MATCH = "BEST_MATCH"
    MONOSPACED_SANSSERIF = "MONOSPACED_SANSSERIF"
    MONOSPACED_SERIF = "MONOSPACED_SERIF"
    PROPORTIONAL_SANSSERIF = "PROPORTIONAL_SANSSERIF"
    PROPORTIONAL_SERIF = "PROPORTIONAL_SERIF"


class BurninSubtitleFontColor(StrEnum):
    WHITE = "WHITE"
    BLACK = "BLACK"
    YELLOW = "YELLOW"
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    HEX = "HEX"
    AUTO = "AUTO"


class BurninSubtitleOutlineColor(StrEnum):
    BLACK = "BLACK"
    WHITE = "WHITE"
    YELLOW = "YELLOW"
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    AUTO = "AUTO"


class BurninSubtitleShadowColor(StrEnum):
    NONE = "NONE"
    BLACK = "BLACK"
    WHITE = "WHITE"
    AUTO = "AUTO"


class BurninSubtitleTeletextSpacing(StrEnum):
    FIXED_GRID = "FIXED_GRID"
    PROPORTIONAL = "PROPORTIONAL"
    AUTO = "AUTO"


class CaptionDestinationType(StrEnum):
    BURN_IN = "BURN_IN"
    DVB_SUB = "DVB_SUB"
    EMBEDDED = "EMBEDDED"
    EMBEDDED_PLUS_SCTE20 = "EMBEDDED_PLUS_SCTE20"
    IMSC = "IMSC"
    SCTE20_PLUS_EMBEDDED = "SCTE20_PLUS_EMBEDDED"
    SCC = "SCC"
    SRT = "SRT"
    SMI = "SMI"
    TELETEXT = "TELETEXT"
    TTML = "TTML"
    WEBVTT = "WEBVTT"


class CaptionSourceByteRateLimit(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class CaptionSourceConvertPaintOnToPopOn(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class CaptionSourceType(StrEnum):
    ANCILLARY = "ANCILLARY"
    DVB_SUB = "DVB_SUB"
    EMBEDDED = "EMBEDDED"
    SCTE20 = "SCTE20"
    SCC = "SCC"
    TTML = "TTML"
    STL = "STL"
    SRT = "SRT"
    SMI = "SMI"
    SMPTE_TT = "SMPTE_TT"
    TELETEXT = "TELETEXT"
    NULL_SOURCE = "NULL_SOURCE"
    IMSC = "IMSC"
    WEBVTT = "WEBVTT"
    TT_3GPP = "TT_3GPP"


class CaptionSourceUpconvertSTLToTeletext(StrEnum):
    UPCONVERT = "UPCONVERT"
    DISABLED = "DISABLED"


class ChromaPositionMode(StrEnum):
    AUTO = "AUTO"
    FORCE_CENTER = "FORCE_CENTER"
    FORCE_TOP_LEFT = "FORCE_TOP_LEFT"


class CmafClientCache(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class CmafCodecSpecification(StrEnum):
    RFC_6381 = "RFC_6381"
    RFC_4281 = "RFC_4281"


class CmafEncryptionType(StrEnum):
    SAMPLE_AES = "SAMPLE_AES"
    AES_CTR = "AES_CTR"


class CmafImageBasedTrickPlay(StrEnum):
    NONE = "NONE"
    THUMBNAIL = "THUMBNAIL"
    THUMBNAIL_AND_FULLFRAME = "THUMBNAIL_AND_FULLFRAME"
    ADVANCED = "ADVANCED"


class CmafInitializationVectorInManifest(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class CmafIntervalCadence(StrEnum):
    FOLLOW_IFRAME = "FOLLOW_IFRAME"
    FOLLOW_CUSTOM = "FOLLOW_CUSTOM"


class CmafKeyProviderType(StrEnum):
    SPEKE = "SPEKE"
    STATIC_KEY = "STATIC_KEY"


class CmafManifestCompression(StrEnum):
    GZIP = "GZIP"
    NONE = "NONE"


class CmafManifestDurationFormat(StrEnum):
    FLOATING_POINT = "FLOATING_POINT"
    INTEGER = "INTEGER"


class CmafMpdManifestBandwidthType(StrEnum):
    AVERAGE = "AVERAGE"
    MAX = "MAX"


class CmafMpdProfile(StrEnum):
    MAIN_PROFILE = "MAIN_PROFILE"
    ON_DEMAND_PROFILE = "ON_DEMAND_PROFILE"


class CmafPtsOffsetHandlingForBFrames(StrEnum):
    ZERO_BASED = "ZERO_BASED"
    MATCH_INITIAL_PTS = "MATCH_INITIAL_PTS"


class CmafSegmentControl(StrEnum):
    SINGLE_FILE = "SINGLE_FILE"
    SEGMENTED_FILES = "SEGMENTED_FILES"


class CmafSegmentLengthControl(StrEnum):
    EXACT = "EXACT"
    GOP_MULTIPLE = "GOP_MULTIPLE"
    MATCH = "MATCH"


class CmafStreamInfResolution(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class CmafTargetDurationCompatibilityMode(StrEnum):
    LEGACY = "LEGACY"
    SPEC_COMPLIANT = "SPEC_COMPLIANT"


class CmafVideoCompositionOffsets(StrEnum):
    SIGNED = "SIGNED"
    UNSIGNED = "UNSIGNED"


class CmafWriteDASHManifest(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class CmafWriteHLSManifest(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class CmafWriteSegmentTimelineInRepresentation(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class CmfcAudioDuration(StrEnum):
    DEFAULT_CODEC_DURATION = "DEFAULT_CODEC_DURATION"
    MATCH_VIDEO_DURATION = "MATCH_VIDEO_DURATION"


class CmfcAudioTrackType(StrEnum):
    ALTERNATE_AUDIO_AUTO_SELECT_DEFAULT = "ALTERNATE_AUDIO_AUTO_SELECT_DEFAULT"
    ALTERNATE_AUDIO_AUTO_SELECT = "ALTERNATE_AUDIO_AUTO_SELECT"
    ALTERNATE_AUDIO_NOT_AUTO_SELECT = "ALTERNATE_AUDIO_NOT_AUTO_SELECT"
    AUDIO_ONLY_VARIANT_STREAM = "AUDIO_ONLY_VARIANT_STREAM"


class CmfcC2paManifest(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class CmfcDescriptiveVideoServiceFlag(StrEnum):
    DONT_FLAG = "DONT_FLAG"
    FLAG = "FLAG"


class CmfcIFrameOnlyManifest(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class CmfcKlvMetadata(StrEnum):
    PASSTHROUGH = "PASSTHROUGH"
    NONE = "NONE"


class CmfcManifestMetadataSignaling(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class CmfcScte35Esam(StrEnum):
    INSERT = "INSERT"
    NONE = "NONE"


class CmfcScte35Source(StrEnum):
    PASSTHROUGH = "PASSTHROUGH"
    NONE = "NONE"


class CmfcTimedMetadata(StrEnum):
    PASSTHROUGH = "PASSTHROUGH"
    NONE = "NONE"


class CmfcTimedMetadataBoxVersion(StrEnum):
    VERSION_0 = "VERSION_0"
    VERSION_1 = "VERSION_1"


class Codec(StrEnum):
    UNKNOWN = "UNKNOWN"
    AAC = "AAC"
    AC3 = "AC3"
    EAC3 = "EAC3"
    FLAC = "FLAC"
    MP3 = "MP3"
    OPUS = "OPUS"
    PCM = "PCM"
    VORBIS = "VORBIS"
    AV1 = "AV1"
    AVC = "AVC"
    HEVC = "HEVC"
    JPEG2000 = "JPEG2000"
    MJPEG = "MJPEG"
    MPEG1 = "MPEG1"
    MP4V = "MP4V"
    MPEG2 = "MPEG2"
    PRORES = "PRORES"
    THEORA = "THEORA"
    VFW = "VFW"
    VP8 = "VP8"
    VP9 = "VP9"
    QTRLE = "QTRLE"
    C608 = "C608"
    C708 = "C708"
    WEBVTT = "WEBVTT"


class ColorMetadata(StrEnum):
    IGNORE = "IGNORE"
    INSERT = "INSERT"


class ColorPrimaries(StrEnum):
    ITU_709 = "ITU_709"
    UNSPECIFIED = "UNSPECIFIED"
    RESERVED = "RESERVED"
    ITU_470M = "ITU_470M"
    ITU_470BG = "ITU_470BG"
    SMPTE_170M = "SMPTE_170M"
    SMPTE_240M = "SMPTE_240M"
    GENERIC_FILM = "GENERIC_FILM"
    ITU_2020 = "ITU_2020"
    SMPTE_428_1 = "SMPTE_428_1"
    SMPTE_431_2 = "SMPTE_431_2"
    SMPTE_EG_432_1 = "SMPTE_EG_432_1"
    IPT = "IPT"
    SMPTE_2067XYZ = "SMPTE_2067XYZ"
    EBU_3213_E = "EBU_3213_E"
    LAST = "LAST"


class ColorSpace(StrEnum):
    FOLLOW = "FOLLOW"
    REC_601 = "REC_601"
    REC_709 = "REC_709"
    HDR10 = "HDR10"
    HLG_2020 = "HLG_2020"
    P3DCI = "P3DCI"
    P3D65_SDR = "P3D65_SDR"
    P3D65_HDR = "P3D65_HDR"


class ColorSpaceConversion(StrEnum):
    NONE = "NONE"
    FORCE_601 = "FORCE_601"
    FORCE_709 = "FORCE_709"
    FORCE_HDR10 = "FORCE_HDR10"
    FORCE_HLG_2020 = "FORCE_HLG_2020"
    FORCE_P3DCI = "FORCE_P3DCI"
    FORCE_P3D65_SDR = "FORCE_P3D65_SDR"
    FORCE_P3D65_HDR = "FORCE_P3D65_HDR"


class ColorSpaceUsage(StrEnum):
    FORCE = "FORCE"
    FALLBACK = "FALLBACK"


class Commitment(StrEnum):
    ONE_YEAR = "ONE_YEAR"


class ContainerType(StrEnum):
    F4V = "F4V"
    GIF = "GIF"
    ISMV = "ISMV"
    M2TS = "M2TS"
    M3U8 = "M3U8"
    CMFC = "CMFC"
    MOV = "MOV"
    MP4 = "MP4"
    MPD = "MPD"
    MXF = "MXF"
    OGG = "OGG"
    WEBM = "WEBM"
    RAW = "RAW"
    Y4M = "Y4M"


class CopyProtectionAction(StrEnum):
    PASSTHROUGH = "PASSTHROUGH"
    STRIP = "STRIP"


class DashIsoGroupAudioChannelConfigSchemeIdUri(StrEnum):
    MPEG_CHANNEL_CONFIGURATION = "MPEG_CHANNEL_CONFIGURATION"
    DOLBY_CHANNEL_CONFIGURATION = "DOLBY_CHANNEL_CONFIGURATION"


class DashIsoHbbtvCompliance(StrEnum):
    HBBTV_1_5 = "HBBTV_1_5"
    NONE = "NONE"


class DashIsoImageBasedTrickPlay(StrEnum):
    NONE = "NONE"
    THUMBNAIL = "THUMBNAIL"
    THUMBNAIL_AND_FULLFRAME = "THUMBNAIL_AND_FULLFRAME"
    ADVANCED = "ADVANCED"


class DashIsoIntervalCadence(StrEnum):
    FOLLOW_IFRAME = "FOLLOW_IFRAME"
    FOLLOW_CUSTOM = "FOLLOW_CUSTOM"


class DashIsoMpdManifestBandwidthType(StrEnum):
    AVERAGE = "AVERAGE"
    MAX = "MAX"


class DashIsoMpdProfile(StrEnum):
    MAIN_PROFILE = "MAIN_PROFILE"
    ON_DEMAND_PROFILE = "ON_DEMAND_PROFILE"


class DashIsoPlaybackDeviceCompatibility(StrEnum):
    CENC_V1 = "CENC_V1"
    UNENCRYPTED_SEI = "UNENCRYPTED_SEI"


class DashIsoPtsOffsetHandlingForBFrames(StrEnum):
    ZERO_BASED = "ZERO_BASED"
    MATCH_INITIAL_PTS = "MATCH_INITIAL_PTS"


class DashIsoSegmentControl(StrEnum):
    SINGLE_FILE = "SINGLE_FILE"
    SEGMENTED_FILES = "SEGMENTED_FILES"


class DashIsoSegmentLengthControl(StrEnum):
    EXACT = "EXACT"
    GOP_MULTIPLE = "GOP_MULTIPLE"
    MATCH = "MATCH"


class DashIsoVideoCompositionOffsets(StrEnum):
    SIGNED = "SIGNED"
    UNSIGNED = "UNSIGNED"


class DashIsoWriteSegmentTimelineInRepresentation(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class DashManifestStyle(StrEnum):
    BASIC = "BASIC"
    COMPACT = "COMPACT"
    DISTINCT = "DISTINCT"
    FULL = "FULL"


class DecryptionMode(StrEnum):
    AES_CTR = "AES_CTR"
    AES_CBC = "AES_CBC"
    AES_GCM = "AES_GCM"


class DeinterlaceAlgorithm(StrEnum):
    INTERPOLATE = "INTERPOLATE"
    INTERPOLATE_TICKER = "INTERPOLATE_TICKER"
    BLEND = "BLEND"
    BLEND_TICKER = "BLEND_TICKER"
    LINEAR_INTERPOLATION = "LINEAR_INTERPOLATION"


class DeinterlacerControl(StrEnum):
    FORCE_ALL_FRAMES = "FORCE_ALL_FRAMES"
    NORMAL = "NORMAL"


class DeinterlacerMode(StrEnum):
    DEINTERLACE = "DEINTERLACE"
    INVERSE_TELECINE = "INVERSE_TELECINE"
    ADAPTIVE = "ADAPTIVE"


class DescribeEndpointsMode(StrEnum):
    DEFAULT = "DEFAULT"
    GET_ONLY = "GET_ONLY"


class DolbyVisionLevel6Mode(StrEnum):
    PASSTHROUGH = "PASSTHROUGH"
    RECALCULATE = "RECALCULATE"
    SPECIFY = "SPECIFY"


class DolbyVisionMapping(StrEnum):
    HDR10_NOMAP = "HDR10_NOMAP"
    HDR10_1000 = "HDR10_1000"


class DolbyVisionProfile(StrEnum):
    PROFILE_5 = "PROFILE_5"
    PROFILE_8_1 = "PROFILE_8_1"


class DropFrameTimecode(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class DvbSubSubtitleFallbackFont(StrEnum):
    BEST_MATCH = "BEST_MATCH"
    MONOSPACED_SANSSERIF = "MONOSPACED_SANSSERIF"
    MONOSPACED_SERIF = "MONOSPACED_SERIF"
    PROPORTIONAL_SANSSERIF = "PROPORTIONAL_SANSSERIF"
    PROPORTIONAL_SERIF = "PROPORTIONAL_SERIF"


class DvbSubtitleAlignment(StrEnum):
    CENTERED = "CENTERED"
    LEFT = "LEFT"
    AUTO = "AUTO"


class DvbSubtitleApplyFontColor(StrEnum):
    WHITE_TEXT_ONLY = "WHITE_TEXT_ONLY"
    ALL_TEXT = "ALL_TEXT"


class DvbSubtitleBackgroundColor(StrEnum):
    NONE = "NONE"
    BLACK = "BLACK"
    WHITE = "WHITE"
    AUTO = "AUTO"


class DvbSubtitleFontColor(StrEnum):
    WHITE = "WHITE"
    BLACK = "BLACK"
    YELLOW = "YELLOW"
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    HEX = "HEX"
    AUTO = "AUTO"


class DvbSubtitleOutlineColor(StrEnum):
    BLACK = "BLACK"
    WHITE = "WHITE"
    YELLOW = "YELLOW"
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    AUTO = "AUTO"


class DvbSubtitleShadowColor(StrEnum):
    NONE = "NONE"
    BLACK = "BLACK"
    WHITE = "WHITE"
    AUTO = "AUTO"


class DvbSubtitleStylePassthrough(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class DvbSubtitleTeletextSpacing(StrEnum):
    FIXED_GRID = "FIXED_GRID"
    PROPORTIONAL = "PROPORTIONAL"
    AUTO = "AUTO"


class DvbSubtitlingType(StrEnum):
    HEARING_IMPAIRED = "HEARING_IMPAIRED"
    STANDARD = "STANDARD"


class DvbddsHandling(StrEnum):
    NONE = "NONE"
    SPECIFIED = "SPECIFIED"
    NO_DISPLAY_WINDOW = "NO_DISPLAY_WINDOW"
    SPECIFIED_OPTIMAL = "SPECIFIED_OPTIMAL"


class DynamicAudioSelectorType(StrEnum):
    ALL_TRACKS = "ALL_TRACKS"
    LANGUAGE_CODE = "LANGUAGE_CODE"


class Eac3AtmosBitstreamMode(StrEnum):
    COMPLETE_MAIN = "COMPLETE_MAIN"


class Eac3AtmosCodingMode(StrEnum):
    CODING_MODE_AUTO = "CODING_MODE_AUTO"
    CODING_MODE_5_1_4 = "CODING_MODE_5_1_4"
    CODING_MODE_7_1_4 = "CODING_MODE_7_1_4"
    CODING_MODE_9_1_6 = "CODING_MODE_9_1_6"


class Eac3AtmosDialogueIntelligence(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class Eac3AtmosDownmixControl(StrEnum):
    SPECIFIED = "SPECIFIED"
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"


class Eac3AtmosDynamicRangeCompressionLine(StrEnum):
    NONE = "NONE"
    FILM_STANDARD = "FILM_STANDARD"
    FILM_LIGHT = "FILM_LIGHT"
    MUSIC_STANDARD = "MUSIC_STANDARD"
    MUSIC_LIGHT = "MUSIC_LIGHT"
    SPEECH = "SPEECH"


class Eac3AtmosDynamicRangeCompressionRf(StrEnum):
    NONE = "NONE"
    FILM_STANDARD = "FILM_STANDARD"
    FILM_LIGHT = "FILM_LIGHT"
    MUSIC_STANDARD = "MUSIC_STANDARD"
    MUSIC_LIGHT = "MUSIC_LIGHT"
    SPEECH = "SPEECH"


class Eac3AtmosDynamicRangeControl(StrEnum):
    SPECIFIED = "SPECIFIED"
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"


class Eac3AtmosMeteringMode(StrEnum):
    LEQ_A = "LEQ_A"
    ITU_BS_1770_1 = "ITU_BS_1770_1"
    ITU_BS_1770_2 = "ITU_BS_1770_2"
    ITU_BS_1770_3 = "ITU_BS_1770_3"
    ITU_BS_1770_4 = "ITU_BS_1770_4"


class Eac3AtmosStereoDownmix(StrEnum):
    NOT_INDICATED = "NOT_INDICATED"
    STEREO = "STEREO"
    SURROUND = "SURROUND"
    DPL2 = "DPL2"


class Eac3AtmosSurroundExMode(StrEnum):
    NOT_INDICATED = "NOT_INDICATED"
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class Eac3AttenuationControl(StrEnum):
    ATTENUATE_3_DB = "ATTENUATE_3_DB"
    NONE = "NONE"


class Eac3BitstreamMode(StrEnum):
    COMPLETE_MAIN = "COMPLETE_MAIN"
    COMMENTARY = "COMMENTARY"
    EMERGENCY = "EMERGENCY"
    HEARING_IMPAIRED = "HEARING_IMPAIRED"
    VISUALLY_IMPAIRED = "VISUALLY_IMPAIRED"


class Eac3CodingMode(StrEnum):
    CODING_MODE_1_0 = "CODING_MODE_1_0"
    CODING_MODE_2_0 = "CODING_MODE_2_0"
    CODING_MODE_3_2 = "CODING_MODE_3_2"


class Eac3DcFilter(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class Eac3DynamicRangeCompressionLine(StrEnum):
    NONE = "NONE"
    FILM_STANDARD = "FILM_STANDARD"
    FILM_LIGHT = "FILM_LIGHT"
    MUSIC_STANDARD = "MUSIC_STANDARD"
    MUSIC_LIGHT = "MUSIC_LIGHT"
    SPEECH = "SPEECH"


class Eac3DynamicRangeCompressionRf(StrEnum):
    NONE = "NONE"
    FILM_STANDARD = "FILM_STANDARD"
    FILM_LIGHT = "FILM_LIGHT"
    MUSIC_STANDARD = "MUSIC_STANDARD"
    MUSIC_LIGHT = "MUSIC_LIGHT"
    SPEECH = "SPEECH"


class Eac3LfeControl(StrEnum):
    LFE = "LFE"
    NO_LFE = "NO_LFE"


class Eac3LfeFilter(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class Eac3MetadataControl(StrEnum):
    FOLLOW_INPUT = "FOLLOW_INPUT"
    USE_CONFIGURED = "USE_CONFIGURED"


class Eac3PassthroughControl(StrEnum):
    WHEN_POSSIBLE = "WHEN_POSSIBLE"
    NO_PASSTHROUGH = "NO_PASSTHROUGH"


class Eac3PhaseControl(StrEnum):
    SHIFT_90_DEGREES = "SHIFT_90_DEGREES"
    NO_SHIFT = "NO_SHIFT"


class Eac3StereoDownmix(StrEnum):
    NOT_INDICATED = "NOT_INDICATED"
    LO_RO = "LO_RO"
    LT_RT = "LT_RT"
    DPL2 = "DPL2"


class Eac3SurroundExMode(StrEnum):
    NOT_INDICATED = "NOT_INDICATED"
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class Eac3SurroundMode(StrEnum):
    NOT_INDICATED = "NOT_INDICATED"
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class EmbeddedConvert608To708(StrEnum):
    UPCONVERT = "UPCONVERT"
    DISABLED = "DISABLED"


class EmbeddedTerminateCaptions(StrEnum):
    END_OF_INPUT = "END_OF_INPUT"
    DISABLED = "DISABLED"


class EmbeddedTimecodeOverride(StrEnum):
    NONE = "NONE"
    USE_MDPM = "USE_MDPM"


class F4vMoovPlacement(StrEnum):
    PROGRESSIVE_DOWNLOAD = "PROGRESSIVE_DOWNLOAD"
    NORMAL = "NORMAL"


class FileSourceConvert608To708(StrEnum):
    UPCONVERT = "UPCONVERT"
    DISABLED = "DISABLED"


class FileSourceTimeDeltaUnits(StrEnum):
    SECONDS = "SECONDS"
    MILLISECONDS = "MILLISECONDS"


class FontScript(StrEnum):
    AUTOMATIC = "AUTOMATIC"
    HANS = "HANS"
    HANT = "HANT"


class Format(StrEnum):
    mp4 = "mp4"
    quicktime = "quicktime"
    matroska = "matroska"
    webm = "webm"
    mxf = "mxf"


class FrameControl(StrEnum):
    NEAREST_IDRFRAME = "NEAREST_IDRFRAME"
    NEAREST_IFRAME = "NEAREST_IFRAME"


class FrameMetricType(StrEnum):
    PSNR = "PSNR"
    SSIM = "SSIM"
    MS_SSIM = "MS_SSIM"
    PSNR_HVS = "PSNR_HVS"
    VMAF = "VMAF"
    QVBR = "QVBR"
    SHOT_CHANGE = "SHOT_CHANGE"


class GifFramerateControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class GifFramerateConversionAlgorithm(StrEnum):
    DUPLICATE_DROP = "DUPLICATE_DROP"
    INTERPOLATE = "INTERPOLATE"


class H264AdaptiveQuantization(StrEnum):
    OFF = "OFF"
    AUTO = "AUTO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    HIGHER = "HIGHER"
    MAX = "MAX"


class H264CodecLevel(StrEnum):
    AUTO = "AUTO"
    LEVEL_1 = "LEVEL_1"
    LEVEL_1_1 = "LEVEL_1_1"
    LEVEL_1_2 = "LEVEL_1_2"
    LEVEL_1_3 = "LEVEL_1_3"
    LEVEL_2 = "LEVEL_2"
    LEVEL_2_1 = "LEVEL_2_1"
    LEVEL_2_2 = "LEVEL_2_2"
    LEVEL_3 = "LEVEL_3"
    LEVEL_3_1 = "LEVEL_3_1"
    LEVEL_3_2 = "LEVEL_3_2"
    LEVEL_4 = "LEVEL_4"
    LEVEL_4_1 = "LEVEL_4_1"
    LEVEL_4_2 = "LEVEL_4_2"
    LEVEL_5 = "LEVEL_5"
    LEVEL_5_1 = "LEVEL_5_1"
    LEVEL_5_2 = "LEVEL_5_2"


class H264CodecProfile(StrEnum):
    BASELINE = "BASELINE"
    HIGH = "HIGH"
    HIGH_10BIT = "HIGH_10BIT"
    HIGH_422 = "HIGH_422"
    HIGH_422_10BIT = "HIGH_422_10BIT"
    MAIN = "MAIN"


class H264DynamicSubGop(StrEnum):
    ADAPTIVE = "ADAPTIVE"
    STATIC = "STATIC"


class H264EndOfStreamMarkers(StrEnum):
    INCLUDE = "INCLUDE"
    SUPPRESS = "SUPPRESS"


class H264EntropyEncoding(StrEnum):
    CABAC = "CABAC"
    CAVLC = "CAVLC"


class H264FieldEncoding(StrEnum):
    PAFF = "PAFF"
    FORCE_FIELD = "FORCE_FIELD"
    MBAFF = "MBAFF"


class H264FlickerAdaptiveQuantization(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H264FramerateControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class H264FramerateConversionAlgorithm(StrEnum):
    DUPLICATE_DROP = "DUPLICATE_DROP"
    INTERPOLATE = "INTERPOLATE"
    FRAMEFORMER = "FRAMEFORMER"
    MAINTAIN_FRAME_COUNT = "MAINTAIN_FRAME_COUNT"


class H264GopBReference(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H264GopSizeUnits(StrEnum):
    FRAMES = "FRAMES"
    SECONDS = "SECONDS"
    AUTO = "AUTO"


class H264InterlaceMode(StrEnum):
    PROGRESSIVE = "PROGRESSIVE"
    TOP_FIELD = "TOP_FIELD"
    BOTTOM_FIELD = "BOTTOM_FIELD"
    FOLLOW_TOP_FIELD = "FOLLOW_TOP_FIELD"
    FOLLOW_BOTTOM_FIELD = "FOLLOW_BOTTOM_FIELD"


class H264ParControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class H264QualityTuningLevel(StrEnum):
    SINGLE_PASS = "SINGLE_PASS"
    SINGLE_PASS_HQ = "SINGLE_PASS_HQ"
    MULTI_PASS_HQ = "MULTI_PASS_HQ"


class H264RateControlMode(StrEnum):
    VBR = "VBR"
    CBR = "CBR"
    QVBR = "QVBR"


class H264RepeatPps(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H264SaliencyAwareEncoding(StrEnum):
    DISABLED = "DISABLED"
    PREFERRED = "PREFERRED"


class H264ScanTypeConversionMode(StrEnum):
    INTERLACED = "INTERLACED"
    INTERLACED_OPTIMIZE = "INTERLACED_OPTIMIZE"


class H264SceneChangeDetect(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"
    TRANSITION_DETECTION = "TRANSITION_DETECTION"


class H264SlowPal(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H264SpatialAdaptiveQuantization(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H264Syntax(StrEnum):
    DEFAULT = "DEFAULT"
    RP2027 = "RP2027"


class H264Telecine(StrEnum):
    NONE = "NONE"
    SOFT = "SOFT"
    HARD = "HARD"


class H264TemporalAdaptiveQuantization(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H264UnregisteredSeiTimecode(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H264WriteMp4PackagingType(StrEnum):
    AVC1 = "AVC1"
    AVC3 = "AVC3"


class H265AdaptiveQuantization(StrEnum):
    OFF = "OFF"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    HIGHER = "HIGHER"
    MAX = "MAX"
    AUTO = "AUTO"


class H265AlternateTransferFunctionSei(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H265CodecLevel(StrEnum):
    AUTO = "AUTO"
    LEVEL_1 = "LEVEL_1"
    LEVEL_2 = "LEVEL_2"
    LEVEL_2_1 = "LEVEL_2_1"
    LEVEL_3 = "LEVEL_3"
    LEVEL_3_1 = "LEVEL_3_1"
    LEVEL_4 = "LEVEL_4"
    LEVEL_4_1 = "LEVEL_4_1"
    LEVEL_5 = "LEVEL_5"
    LEVEL_5_1 = "LEVEL_5_1"
    LEVEL_5_2 = "LEVEL_5_2"
    LEVEL_6 = "LEVEL_6"
    LEVEL_6_1 = "LEVEL_6_1"
    LEVEL_6_2 = "LEVEL_6_2"


class H265CodecProfile(StrEnum):
    MAIN_MAIN = "MAIN_MAIN"
    MAIN_HIGH = "MAIN_HIGH"
    MAIN10_MAIN = "MAIN10_MAIN"
    MAIN10_HIGH = "MAIN10_HIGH"
    MAIN_422_8BIT_MAIN = "MAIN_422_8BIT_MAIN"
    MAIN_422_8BIT_HIGH = "MAIN_422_8BIT_HIGH"
    MAIN_422_10BIT_MAIN = "MAIN_422_10BIT_MAIN"
    MAIN_422_10BIT_HIGH = "MAIN_422_10BIT_HIGH"


class H265Deblocking(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class H265DynamicSubGop(StrEnum):
    ADAPTIVE = "ADAPTIVE"
    STATIC = "STATIC"


class H265EndOfStreamMarkers(StrEnum):
    INCLUDE = "INCLUDE"
    SUPPRESS = "SUPPRESS"


class H265FlickerAdaptiveQuantization(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H265FramerateControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class H265FramerateConversionAlgorithm(StrEnum):
    DUPLICATE_DROP = "DUPLICATE_DROP"
    INTERPOLATE = "INTERPOLATE"
    FRAMEFORMER = "FRAMEFORMER"
    MAINTAIN_FRAME_COUNT = "MAINTAIN_FRAME_COUNT"


class H265GopBReference(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H265GopSizeUnits(StrEnum):
    FRAMES = "FRAMES"
    SECONDS = "SECONDS"
    AUTO = "AUTO"


class H265InterlaceMode(StrEnum):
    PROGRESSIVE = "PROGRESSIVE"
    TOP_FIELD = "TOP_FIELD"
    BOTTOM_FIELD = "BOTTOM_FIELD"
    FOLLOW_TOP_FIELD = "FOLLOW_TOP_FIELD"
    FOLLOW_BOTTOM_FIELD = "FOLLOW_BOTTOM_FIELD"


class H265MvOverPictureBoundaries(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class H265MvTemporalPredictor(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class H265ParControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class H265QualityTuningLevel(StrEnum):
    SINGLE_PASS = "SINGLE_PASS"
    SINGLE_PASS_HQ = "SINGLE_PASS_HQ"
    MULTI_PASS_HQ = "MULTI_PASS_HQ"


class H265RateControlMode(StrEnum):
    VBR = "VBR"
    CBR = "CBR"
    QVBR = "QVBR"


class H265SampleAdaptiveOffsetFilterMode(StrEnum):
    DEFAULT = "DEFAULT"
    ADAPTIVE = "ADAPTIVE"
    OFF = "OFF"


class H265ScanTypeConversionMode(StrEnum):
    INTERLACED = "INTERLACED"
    INTERLACED_OPTIMIZE = "INTERLACED_OPTIMIZE"


class H265SceneChangeDetect(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"
    TRANSITION_DETECTION = "TRANSITION_DETECTION"


class H265SlowPal(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H265SpatialAdaptiveQuantization(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H265Telecine(StrEnum):
    NONE = "NONE"
    SOFT = "SOFT"
    HARD = "HARD"


class H265TemporalAdaptiveQuantization(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H265TemporalIds(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H265TilePadding(StrEnum):
    NONE = "NONE"
    PADDED = "PADDED"


class H265Tiles(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H265TreeBlockSize(StrEnum):
    AUTO = "AUTO"
    TREE_SIZE_32X32 = "TREE_SIZE_32X32"


class H265UnregisteredSeiTimecode(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class H265WriteMp4PackagingType(StrEnum):
    HVC1 = "HVC1"
    HEV1 = "HEV1"


class HDRToSDRToneMapper(StrEnum):
    PRESERVE_DETAILS = "PRESERVE_DETAILS"
    VIBRANT = "VIBRANT"


class HlsAdMarkers(StrEnum):
    ELEMENTAL = "ELEMENTAL"
    ELEMENTAL_SCTE35 = "ELEMENTAL_SCTE35"


class HlsAudioOnlyContainer(StrEnum):
    AUTOMATIC = "AUTOMATIC"
    M2TS = "M2TS"


class HlsAudioOnlyHeader(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class HlsAudioTrackType(StrEnum):
    ALTERNATE_AUDIO_AUTO_SELECT_DEFAULT = "ALTERNATE_AUDIO_AUTO_SELECT_DEFAULT"
    ALTERNATE_AUDIO_AUTO_SELECT = "ALTERNATE_AUDIO_AUTO_SELECT"
    ALTERNATE_AUDIO_NOT_AUTO_SELECT = "ALTERNATE_AUDIO_NOT_AUTO_SELECT"
    AUDIO_ONLY_VARIANT_STREAM = "AUDIO_ONLY_VARIANT_STREAM"


class HlsCaptionLanguageSetting(StrEnum):
    INSERT = "INSERT"
    OMIT = "OMIT"
    NONE = "NONE"


class HlsCaptionSegmentLengthControl(StrEnum):
    LARGE_SEGMENTS = "LARGE_SEGMENTS"
    MATCH_VIDEO = "MATCH_VIDEO"


class HlsClientCache(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class HlsCodecSpecification(StrEnum):
    RFC_6381 = "RFC_6381"
    RFC_4281 = "RFC_4281"


class HlsDescriptiveVideoServiceFlag(StrEnum):
    DONT_FLAG = "DONT_FLAG"
    FLAG = "FLAG"


class HlsDirectoryStructure(StrEnum):
    SINGLE_DIRECTORY = "SINGLE_DIRECTORY"
    SUBDIRECTORY_PER_STREAM = "SUBDIRECTORY_PER_STREAM"


class HlsEncryptionType(StrEnum):
    AES128 = "AES128"
    SAMPLE_AES = "SAMPLE_AES"


class HlsIFrameOnlyManifest(StrEnum):
    INCLUDE = "INCLUDE"
    INCLUDE_AS_TS = "INCLUDE_AS_TS"
    EXCLUDE = "EXCLUDE"


class HlsImageBasedTrickPlay(StrEnum):
    NONE = "NONE"
    THUMBNAIL = "THUMBNAIL"
    THUMBNAIL_AND_FULLFRAME = "THUMBNAIL_AND_FULLFRAME"
    ADVANCED = "ADVANCED"


class HlsInitializationVectorInManifest(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class HlsIntervalCadence(StrEnum):
    FOLLOW_IFRAME = "FOLLOW_IFRAME"
    FOLLOW_CUSTOM = "FOLLOW_CUSTOM"


class HlsKeyProviderType(StrEnum):
    SPEKE = "SPEKE"
    STATIC_KEY = "STATIC_KEY"


class HlsManifestCompression(StrEnum):
    GZIP = "GZIP"
    NONE = "NONE"


class HlsManifestDurationFormat(StrEnum):
    FLOATING_POINT = "FLOATING_POINT"
    INTEGER = "INTEGER"


class HlsOfflineEncrypted(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class HlsOutputSelection(StrEnum):
    MANIFESTS_AND_SEGMENTS = "MANIFESTS_AND_SEGMENTS"
    SEGMENTS_ONLY = "SEGMENTS_ONLY"


class HlsProgramDateTime(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class HlsProgressiveWriteHlsManifest(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class HlsSegmentControl(StrEnum):
    SINGLE_FILE = "SINGLE_FILE"
    SEGMENTED_FILES = "SEGMENTED_FILES"


class HlsSegmentLengthControl(StrEnum):
    EXACT = "EXACT"
    GOP_MULTIPLE = "GOP_MULTIPLE"
    MATCH = "MATCH"


class HlsStreamInfResolution(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class HlsTargetDurationCompatibilityMode(StrEnum):
    LEGACY = "LEGACY"
    SPEC_COMPLIANT = "SPEC_COMPLIANT"


class HlsTimedMetadataId3Frame(StrEnum):
    NONE = "NONE"
    PRIV = "PRIV"
    TDRL = "TDRL"


class ImscAccessibilitySubs(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class ImscStylePassthrough(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class InputDeblockFilter(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class InputDenoiseFilter(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class InputFilterEnable(StrEnum):
    AUTO = "AUTO"
    DISABLE = "DISABLE"
    FORCE = "FORCE"


class InputPolicy(StrEnum):
    ALLOWED = "ALLOWED"
    DISALLOWED = "DISALLOWED"


class InputPsiControl(StrEnum):
    IGNORE_PSI = "IGNORE_PSI"
    USE_PSI = "USE_PSI"


class InputRotate(StrEnum):
    DEGREE_0 = "DEGREE_0"
    DEGREES_90 = "DEGREES_90"
    DEGREES_180 = "DEGREES_180"
    DEGREES_270 = "DEGREES_270"
    AUTO = "AUTO"


class InputSampleRange(StrEnum):
    FOLLOW = "FOLLOW"
    FULL_RANGE = "FULL_RANGE"
    LIMITED_RANGE = "LIMITED_RANGE"


class InputScanType(StrEnum):
    AUTO = "AUTO"
    PSF = "PSF"


class InputTimecodeSource(StrEnum):
    EMBEDDED = "EMBEDDED"
    ZEROBASED = "ZEROBASED"
    SPECIFIEDSTART = "SPECIFIEDSTART"


class JobPhase(StrEnum):
    PROBING = "PROBING"
    TRANSCODING = "TRANSCODING"
    UPLOADING = "UPLOADING"


class JobStatus(StrEnum):
    SUBMITTED = "SUBMITTED"
    PROGRESSING = "PROGRESSING"
    COMPLETE = "COMPLETE"
    CANCELED = "CANCELED"
    ERROR = "ERROR"


class JobTemplateListBy(StrEnum):
    NAME = "NAME"
    CREATION_DATE = "CREATION_DATE"
    SYSTEM = "SYSTEM"


class JobsQueryFilterKey(StrEnum):
    queue = "queue"
    status = "status"
    fileInput = "fileInput"
    jobEngineVersionRequested = "jobEngineVersionRequested"
    jobEngineVersionUsed = "jobEngineVersionUsed"
    audioCodec = "audioCodec"
    videoCodec = "videoCodec"


class JobsQueryStatus(StrEnum):
    SUBMITTED = "SUBMITTED"
    PROGRESSING = "PROGRESSING"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"


class LanguageCode(StrEnum):
    ENG = "ENG"
    SPA = "SPA"
    FRA = "FRA"
    DEU = "DEU"
    GER = "GER"
    ZHO = "ZHO"
    ARA = "ARA"
    HIN = "HIN"
    JPN = "JPN"
    RUS = "RUS"
    POR = "POR"
    ITA = "ITA"
    URD = "URD"
    VIE = "VIE"
    KOR = "KOR"
    PAN = "PAN"
    ABK = "ABK"
    AAR = "AAR"
    AFR = "AFR"
    AKA = "AKA"
    SQI = "SQI"
    AMH = "AMH"
    ARG = "ARG"
    HYE = "HYE"
    ASM = "ASM"
    AVA = "AVA"
    AVE = "AVE"
    AYM = "AYM"
    AZE = "AZE"
    BAM = "BAM"
    BAK = "BAK"
    EUS = "EUS"
    BEL = "BEL"
    BEN = "BEN"
    BIH = "BIH"
    BIS = "BIS"
    BOS = "BOS"
    BRE = "BRE"
    BUL = "BUL"
    MYA = "MYA"
    CAT = "CAT"
    KHM = "KHM"
    CHA = "CHA"
    CHE = "CHE"
    NYA = "NYA"
    CHU = "CHU"
    CHV = "CHV"
    COR = "COR"
    COS = "COS"
    CRE = "CRE"
    HRV = "HRV"
    CES = "CES"
    DAN = "DAN"
    DIV = "DIV"
    NLD = "NLD"
    DZO = "DZO"
    ENM = "ENM"
    EPO = "EPO"
    EST = "EST"
    EWE = "EWE"
    FAO = "FAO"
    FIJ = "FIJ"
    FIN = "FIN"
    FRM = "FRM"
    FUL = "FUL"
    GLA = "GLA"
    GLG = "GLG"
    LUG = "LUG"
    KAT = "KAT"
    ELL = "ELL"
    GRN = "GRN"
    GUJ = "GUJ"
    HAT = "HAT"
    HAU = "HAU"
    HEB = "HEB"
    HER = "HER"
    HMO = "HMO"
    HUN = "HUN"
    ISL = "ISL"
    IDO = "IDO"
    IBO = "IBO"
    IND = "IND"
    INA = "INA"
    ILE = "ILE"
    IKU = "IKU"
    IPK = "IPK"
    GLE = "GLE"
    JAV = "JAV"
    KAL = "KAL"
    KAN = "KAN"
    KAU = "KAU"
    KAS = "KAS"
    KAZ = "KAZ"
    KIK = "KIK"
    KIN = "KIN"
    KIR = "KIR"
    KOM = "KOM"
    KON = "KON"
    KUA = "KUA"
    KUR = "KUR"
    LAO = "LAO"
    LAT = "LAT"
    LAV = "LAV"
    LIM = "LIM"
    LIN = "LIN"
    LIT = "LIT"
    LUB = "LUB"
    LTZ = "LTZ"
    MKD = "MKD"
    MLG = "MLG"
    MSA = "MSA"
    MAL = "MAL"
    MLT = "MLT"
    GLV = "GLV"
    MRI = "MRI"
    MAR = "MAR"
    MAH = "MAH"
    MON = "MON"
    NAU = "NAU"
    NAV = "NAV"
    NDE = "NDE"
    NBL = "NBL"
    NDO = "NDO"
    NEP = "NEP"
    SME = "SME"
    NOR = "NOR"
    NOB = "NOB"
    NNO = "NNO"
    OCI = "OCI"
    OJI = "OJI"
    ORI = "ORI"
    ORM = "ORM"
    OSS = "OSS"
    PLI = "PLI"
    FAS = "FAS"
    POL = "POL"
    PUS = "PUS"
    QUE = "QUE"
    QAA = "QAA"
    RON = "RON"
    ROH = "ROH"
    RUN = "RUN"
    SMO = "SMO"
    SAG = "SAG"
    SAN = "SAN"
    SRD = "SRD"
    SRB = "SRB"
    SNA = "SNA"
    III = "III"
    SND = "SND"
    SIN = "SIN"
    SLK = "SLK"
    SLV = "SLV"
    SOM = "SOM"
    SOT = "SOT"
    SUN = "SUN"
    SWA = "SWA"
    SSW = "SSW"
    SWE = "SWE"
    TGL = "TGL"
    TAH = "TAH"
    TGK = "TGK"
    TAM = "TAM"
    TAT = "TAT"
    TEL = "TEL"
    THA = "THA"
    BOD = "BOD"
    TIR = "TIR"
    TON = "TON"
    TSO = "TSO"
    TSN = "TSN"
    TUR = "TUR"
    TUK = "TUK"
    TWI = "TWI"
    UIG = "UIG"
    UKR = "UKR"
    UZB = "UZB"
    VEN = "VEN"
    VOL = "VOL"
    WLN = "WLN"
    CYM = "CYM"
    FRY = "FRY"
    WOL = "WOL"
    XHO = "XHO"
    YID = "YID"
    YOR = "YOR"
    ZHA = "ZHA"
    ZUL = "ZUL"
    ORJ = "ORJ"
    QPC = "QPC"
    TNG = "TNG"
    SRP = "SRP"


class M2tsAudioBufferModel(StrEnum):
    DVB = "DVB"
    ATSC = "ATSC"


class M2tsAudioDuration(StrEnum):
    DEFAULT_CODEC_DURATION = "DEFAULT_CODEC_DURATION"
    MATCH_VIDEO_DURATION = "MATCH_VIDEO_DURATION"


class M2tsBufferModel(StrEnum):
    MULTIPLEX = "MULTIPLEX"
    NONE = "NONE"


class M2tsDataPtsControl(StrEnum):
    AUTO = "AUTO"
    ALIGN_TO_VIDEO = "ALIGN_TO_VIDEO"


class M2tsEbpAudioInterval(StrEnum):
    VIDEO_AND_FIXED_INTERVALS = "VIDEO_AND_FIXED_INTERVALS"
    VIDEO_INTERVAL = "VIDEO_INTERVAL"


class M2tsEbpPlacement(StrEnum):
    VIDEO_AND_AUDIO_PIDS = "VIDEO_AND_AUDIO_PIDS"
    VIDEO_PID = "VIDEO_PID"


class M2tsEsRateInPes(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class M2tsForceTsVideoEbpOrder(StrEnum):
    FORCE = "FORCE"
    DEFAULT = "DEFAULT"


class M2tsKlvMetadata(StrEnum):
    PASSTHROUGH = "PASSTHROUGH"
    NONE = "NONE"


class M2tsNielsenId3(StrEnum):
    INSERT = "INSERT"
    NONE = "NONE"


class M2tsPcrControl(StrEnum):
    PCR_EVERY_PES_PACKET = "PCR_EVERY_PES_PACKET"
    CONFIGURED_PCR_PERIOD = "CONFIGURED_PCR_PERIOD"


class M2tsPreventBufferUnderflow(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class M2tsRateMode(StrEnum):
    VBR = "VBR"
    CBR = "CBR"


class M2tsScte35Source(StrEnum):
    PASSTHROUGH = "PASSTHROUGH"
    NONE = "NONE"


class M2tsSegmentationMarkers(StrEnum):
    NONE = "NONE"
    RAI_SEGSTART = "RAI_SEGSTART"
    RAI_ADAPT = "RAI_ADAPT"
    PSI_SEGSTART = "PSI_SEGSTART"
    EBP = "EBP"
    EBP_LEGACY = "EBP_LEGACY"


class M2tsSegmentationStyle(StrEnum):
    MAINTAIN_CADENCE = "MAINTAIN_CADENCE"
    RESET_CADENCE = "RESET_CADENCE"


class M3u8AudioDuration(StrEnum):
    DEFAULT_CODEC_DURATION = "DEFAULT_CODEC_DURATION"
    MATCH_VIDEO_DURATION = "MATCH_VIDEO_DURATION"


class M3u8DataPtsControl(StrEnum):
    AUTO = "AUTO"
    ALIGN_TO_VIDEO = "ALIGN_TO_VIDEO"


class M3u8NielsenId3(StrEnum):
    INSERT = "INSERT"
    NONE = "NONE"


class M3u8PcrControl(StrEnum):
    PCR_EVERY_PES_PACKET = "PCR_EVERY_PES_PACKET"
    CONFIGURED_PCR_PERIOD = "CONFIGURED_PCR_PERIOD"


class M3u8Scte35Source(StrEnum):
    PASSTHROUGH = "PASSTHROUGH"
    NONE = "NONE"


class MatrixCoefficients(StrEnum):
    RGB = "RGB"
    ITU_709 = "ITU_709"
    UNSPECIFIED = "UNSPECIFIED"
    RESERVED = "RESERVED"
    FCC = "FCC"
    ITU_470BG = "ITU_470BG"
    SMPTE_170M = "SMPTE_170M"
    SMPTE_240M = "SMPTE_240M"
    YCgCo = "YCgCo"
    ITU_2020_NCL = "ITU_2020_NCL"
    ITU_2020_CL = "ITU_2020_CL"
    SMPTE_2085 = "SMPTE_2085"
    CD_NCL = "CD_NCL"
    CD_CL = "CD_CL"
    ITU_2100ICtCp = "ITU_2100ICtCp"
    IPT = "IPT"
    EBU3213 = "EBU3213"
    LAST = "LAST"


class MotionImageInsertionMode(StrEnum):
    MOV = "MOV"
    PNG = "PNG"


class MotionImagePlayback(StrEnum):
    ONCE = "ONCE"
    REPEAT = "REPEAT"


class MovClapAtom(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class MovCslgAtom(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class MovMpeg2FourCCControl(StrEnum):
    XDCAM = "XDCAM"
    MPEG = "MPEG"


class MovPaddingControl(StrEnum):
    OMNEON = "OMNEON"
    NONE = "NONE"


class MovReference(StrEnum):
    SELF_CONTAINED = "SELF_CONTAINED"
    EXTERNAL = "EXTERNAL"


class Mp2AudioDescriptionMix(StrEnum):
    BROADCASTER_MIXED_AD = "BROADCASTER_MIXED_AD"
    NONE = "NONE"


class Mp3RateControlMode(StrEnum):
    CBR = "CBR"
    VBR = "VBR"


class Mp4C2paManifest(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class Mp4CslgAtom(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class Mp4FreeSpaceBox(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class Mp4MoovPlacement(StrEnum):
    PROGRESSIVE_DOWNLOAD = "PROGRESSIVE_DOWNLOAD"
    NORMAL = "NORMAL"


class MpdAccessibilityCaptionHints(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class MpdAudioDuration(StrEnum):
    DEFAULT_CODEC_DURATION = "DEFAULT_CODEC_DURATION"
    MATCH_VIDEO_DURATION = "MATCH_VIDEO_DURATION"


class MpdC2paManifest(StrEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class MpdCaptionContainerType(StrEnum):
    RAW = "RAW"
    FRAGMENTED_MP4 = "FRAGMENTED_MP4"


class MpdKlvMetadata(StrEnum):
    NONE = "NONE"
    PASSTHROUGH = "PASSTHROUGH"


class MpdManifestMetadataSignaling(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class MpdScte35Esam(StrEnum):
    INSERT = "INSERT"
    NONE = "NONE"


class MpdScte35Source(StrEnum):
    PASSTHROUGH = "PASSTHROUGH"
    NONE = "NONE"


class MpdTimedMetadata(StrEnum):
    PASSTHROUGH = "PASSTHROUGH"
    NONE = "NONE"


class MpdTimedMetadataBoxVersion(StrEnum):
    VERSION_0 = "VERSION_0"
    VERSION_1 = "VERSION_1"


class Mpeg2AdaptiveQuantization(StrEnum):
    OFF = "OFF"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Mpeg2CodecLevel(StrEnum):
    AUTO = "AUTO"
    LOW = "LOW"
    MAIN = "MAIN"
    HIGH1440 = "HIGH1440"
    HIGH = "HIGH"


class Mpeg2CodecProfile(StrEnum):
    MAIN = "MAIN"
    PROFILE_422 = "PROFILE_422"


class Mpeg2DynamicSubGop(StrEnum):
    ADAPTIVE = "ADAPTIVE"
    STATIC = "STATIC"


class Mpeg2FramerateControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class Mpeg2FramerateConversionAlgorithm(StrEnum):
    DUPLICATE_DROP = "DUPLICATE_DROP"
    INTERPOLATE = "INTERPOLATE"
    FRAMEFORMER = "FRAMEFORMER"
    MAINTAIN_FRAME_COUNT = "MAINTAIN_FRAME_COUNT"


class Mpeg2GopSizeUnits(StrEnum):
    FRAMES = "FRAMES"
    SECONDS = "SECONDS"


class Mpeg2InterlaceMode(StrEnum):
    PROGRESSIVE = "PROGRESSIVE"
    TOP_FIELD = "TOP_FIELD"
    BOTTOM_FIELD = "BOTTOM_FIELD"
    FOLLOW_TOP_FIELD = "FOLLOW_TOP_FIELD"
    FOLLOW_BOTTOM_FIELD = "FOLLOW_BOTTOM_FIELD"


class Mpeg2IntraDcPrecision(StrEnum):
    AUTO = "AUTO"
    INTRA_DC_PRECISION_8 = "INTRA_DC_PRECISION_8"
    INTRA_DC_PRECISION_9 = "INTRA_DC_PRECISION_9"
    INTRA_DC_PRECISION_10 = "INTRA_DC_PRECISION_10"
    INTRA_DC_PRECISION_11 = "INTRA_DC_PRECISION_11"


class Mpeg2ParControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class Mpeg2QualityTuningLevel(StrEnum):
    SINGLE_PASS = "SINGLE_PASS"
    MULTI_PASS = "MULTI_PASS"


class Mpeg2RateControlMode(StrEnum):
    VBR = "VBR"
    CBR = "CBR"


class Mpeg2ScanTypeConversionMode(StrEnum):
    INTERLACED = "INTERLACED"
    INTERLACED_OPTIMIZE = "INTERLACED_OPTIMIZE"


class Mpeg2SceneChangeDetect(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class Mpeg2SlowPal(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class Mpeg2SpatialAdaptiveQuantization(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class Mpeg2Syntax(StrEnum):
    DEFAULT = "DEFAULT"
    D_10 = "D_10"


class Mpeg2Telecine(StrEnum):
    NONE = "NONE"
    SOFT = "SOFT"
    HARD = "HARD"


class Mpeg2TemporalAdaptiveQuantization(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class MsSmoothAudioDeduplication(StrEnum):
    COMBINE_DUPLICATE_STREAMS = "COMBINE_DUPLICATE_STREAMS"
    NONE = "NONE"


class MsSmoothFragmentLengthControl(StrEnum):
    EXACT = "EXACT"
    GOP_MULTIPLE = "GOP_MULTIPLE"


class MsSmoothManifestEncoding(StrEnum):
    UTF8 = "UTF8"
    UTF16 = "UTF16"


class MxfAfdSignaling(StrEnum):
    NO_COPY = "NO_COPY"
    COPY_FROM_VIDEO = "COPY_FROM_VIDEO"


class MxfProfile(StrEnum):
    D_10 = "D_10"
    XDCAM = "XDCAM"
    OP1A = "OP1A"
    XAVC = "XAVC"
    XDCAM_RDD9 = "XDCAM_RDD9"


class MxfXavcDurationMode(StrEnum):
    ALLOW_ANY_DURATION = "ALLOW_ANY_DURATION"
    DROP_FRAMES_FOR_COMPLIANCE = "DROP_FRAMES_FOR_COMPLIANCE"


class NielsenActiveWatermarkProcessType(StrEnum):
    NAES2_AND_NW = "NAES2_AND_NW"
    CBET = "CBET"
    NAES2_AND_NW_AND_CBET = "NAES2_AND_NW_AND_CBET"


class NielsenSourceWatermarkStatusType(StrEnum):
    CLEAN = "CLEAN"
    WATERMARKED = "WATERMARKED"


class NielsenUniqueTicPerAudioTrackType(StrEnum):
    RESERVE_UNIQUE_TICS_PER_TRACK = "RESERVE_UNIQUE_TICS_PER_TRACK"
    SAME_TICS_PER_TRACK = "SAME_TICS_PER_TRACK"


class NoiseFilterPostTemporalSharpening(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"
    AUTO = "AUTO"


class NoiseFilterPostTemporalSharpeningStrength(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class NoiseReducerFilter(StrEnum):
    BILATERAL = "BILATERAL"
    MEAN = "MEAN"
    GAUSSIAN = "GAUSSIAN"
    LANCZOS = "LANCZOS"
    SHARPEN = "SHARPEN"
    CONSERVE = "CONSERVE"
    SPATIAL = "SPATIAL"
    TEMPORAL = "TEMPORAL"


class Order(StrEnum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class OutputGroupType(StrEnum):
    HLS_GROUP_SETTINGS = "HLS_GROUP_SETTINGS"
    DASH_ISO_GROUP_SETTINGS = "DASH_ISO_GROUP_SETTINGS"
    FILE_GROUP_SETTINGS = "FILE_GROUP_SETTINGS"
    MS_SMOOTH_GROUP_SETTINGS = "MS_SMOOTH_GROUP_SETTINGS"
    CMAF_GROUP_SETTINGS = "CMAF_GROUP_SETTINGS"


class OutputSdt(StrEnum):
    SDT_FOLLOW = "SDT_FOLLOW"
    SDT_FOLLOW_IF_PRESENT = "SDT_FOLLOW_IF_PRESENT"
    SDT_MANUAL = "SDT_MANUAL"
    SDT_NONE = "SDT_NONE"


class PadVideo(StrEnum):
    DISABLED = "DISABLED"
    BLACK = "BLACK"


class PresetListBy(StrEnum):
    NAME = "NAME"
    CREATION_DATE = "CREATION_DATE"
    SYSTEM = "SYSTEM"


class PresetSpeke20Audio(StrEnum):
    PRESET_AUDIO_1 = "PRESET_AUDIO_1"
    PRESET_AUDIO_2 = "PRESET_AUDIO_2"
    PRESET_AUDIO_3 = "PRESET_AUDIO_3"
    SHARED = "SHARED"
    UNENCRYPTED = "UNENCRYPTED"


class PresetSpeke20Video(StrEnum):
    PRESET_VIDEO_1 = "PRESET_VIDEO_1"
    PRESET_VIDEO_2 = "PRESET_VIDEO_2"
    PRESET_VIDEO_3 = "PRESET_VIDEO_3"
    PRESET_VIDEO_4 = "PRESET_VIDEO_4"
    PRESET_VIDEO_5 = "PRESET_VIDEO_5"
    PRESET_VIDEO_6 = "PRESET_VIDEO_6"
    PRESET_VIDEO_7 = "PRESET_VIDEO_7"
    PRESET_VIDEO_8 = "PRESET_VIDEO_8"
    SHARED = "SHARED"
    UNENCRYPTED = "UNENCRYPTED"


class PricingPlan(StrEnum):
    ON_DEMAND = "ON_DEMAND"
    RESERVED = "RESERVED"


class ProresChromaSampling(StrEnum):
    PRESERVE_444_SAMPLING = "PRESERVE_444_SAMPLING"
    SUBSAMPLE_TO_422 = "SUBSAMPLE_TO_422"


class ProresCodecProfile(StrEnum):
    APPLE_PRORES_422 = "APPLE_PRORES_422"
    APPLE_PRORES_422_HQ = "APPLE_PRORES_422_HQ"
    APPLE_PRORES_422_LT = "APPLE_PRORES_422_LT"
    APPLE_PRORES_422_PROXY = "APPLE_PRORES_422_PROXY"
    APPLE_PRORES_4444 = "APPLE_PRORES_4444"
    APPLE_PRORES_4444_XQ = "APPLE_PRORES_4444_XQ"


class ProresFramerateControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class ProresFramerateConversionAlgorithm(StrEnum):
    DUPLICATE_DROP = "DUPLICATE_DROP"
    INTERPOLATE = "INTERPOLATE"
    FRAMEFORMER = "FRAMEFORMER"
    MAINTAIN_FRAME_COUNT = "MAINTAIN_FRAME_COUNT"


class ProresInterlaceMode(StrEnum):
    PROGRESSIVE = "PROGRESSIVE"
    TOP_FIELD = "TOP_FIELD"
    BOTTOM_FIELD = "BOTTOM_FIELD"
    FOLLOW_TOP_FIELD = "FOLLOW_TOP_FIELD"
    FOLLOW_BOTTOM_FIELD = "FOLLOW_BOTTOM_FIELD"


class ProresParControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class ProresScanTypeConversionMode(StrEnum):
    INTERLACED = "INTERLACED"
    INTERLACED_OPTIMIZE = "INTERLACED_OPTIMIZE"


class ProresSlowPal(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class ProresTelecine(StrEnum):
    NONE = "NONE"
    HARD = "HARD"


class QueueListBy(StrEnum):
    NAME = "NAME"
    CREATION_DATE = "CREATION_DATE"


class QueueStatus(StrEnum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"


class RemoveRubyReserveAttributes(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class RenewalType(StrEnum):
    AUTO_RENEW = "AUTO_RENEW"
    EXPIRE = "EXPIRE"


class RequiredFlag(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class ReservationPlanStatus(StrEnum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"


class RespondToAfd(StrEnum):
    NONE = "NONE"
    RESPOND = "RESPOND"
    PASSTHROUGH = "PASSTHROUGH"


class RuleType(StrEnum):
    MIN_TOP_RENDITION_SIZE = "MIN_TOP_RENDITION_SIZE"
    MIN_BOTTOM_RENDITION_SIZE = "MIN_BOTTOM_RENDITION_SIZE"
    FORCE_INCLUDE_RENDITIONS = "FORCE_INCLUDE_RENDITIONS"
    ALLOWED_RENDITIONS = "ALLOWED_RENDITIONS"


class S3ObjectCannedAcl(StrEnum):
    PUBLIC_READ = "PUBLIC_READ"
    AUTHENTICATED_READ = "AUTHENTICATED_READ"
    BUCKET_OWNER_READ = "BUCKET_OWNER_READ"
    BUCKET_OWNER_FULL_CONTROL = "BUCKET_OWNER_FULL_CONTROL"


class S3ServerSideEncryptionType(StrEnum):
    SERVER_SIDE_ENCRYPTION_S3 = "SERVER_SIDE_ENCRYPTION_S3"
    SERVER_SIDE_ENCRYPTION_KMS = "SERVER_SIDE_ENCRYPTION_KMS"


class S3StorageClass(StrEnum):
    STANDARD = "STANDARD"
    REDUCED_REDUNDANCY = "REDUCED_REDUNDANCY"
    STANDARD_IA = "STANDARD_IA"
    ONEZONE_IA = "ONEZONE_IA"
    INTELLIGENT_TIERING = "INTELLIGENT_TIERING"
    GLACIER = "GLACIER"
    DEEP_ARCHIVE = "DEEP_ARCHIVE"


class SampleRangeConversion(StrEnum):
    LIMITED_RANGE_SQUEEZE = "LIMITED_RANGE_SQUEEZE"
    NONE = "NONE"
    LIMITED_RANGE_CLIP = "LIMITED_RANGE_CLIP"


class ScalingBehavior(StrEnum):
    DEFAULT = "DEFAULT"
    STRETCH_TO_OUTPUT = "STRETCH_TO_OUTPUT"
    FIT = "FIT"
    FIT_NO_UPSCALE = "FIT_NO_UPSCALE"
    FILL = "FILL"


class SccDestinationFramerate(StrEnum):
    FRAMERATE_23_97 = "FRAMERATE_23_97"
    FRAMERATE_24 = "FRAMERATE_24"
    FRAMERATE_25 = "FRAMERATE_25"
    FRAMERATE_29_97_DROPFRAME = "FRAMERATE_29_97_DROPFRAME"
    FRAMERATE_29_97_NON_DROPFRAME = "FRAMERATE_29_97_NON_DROPFRAME"


class ShareStatus(StrEnum):
    NOT_SHARED = "NOT_SHARED"
    INITIATED = "INITIATED"
    SHARED = "SHARED"


class SimulateReservedQueue(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class SlowPalPitchCorrection(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class SrtStylePassthrough(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class StatusUpdateInterval(StrEnum):
    SECONDS_10 = "SECONDS_10"
    SECONDS_12 = "SECONDS_12"
    SECONDS_15 = "SECONDS_15"
    SECONDS_20 = "SECONDS_20"
    SECONDS_30 = "SECONDS_30"
    SECONDS_60 = "SECONDS_60"
    SECONDS_120 = "SECONDS_120"
    SECONDS_180 = "SECONDS_180"
    SECONDS_240 = "SECONDS_240"
    SECONDS_300 = "SECONDS_300"
    SECONDS_360 = "SECONDS_360"
    SECONDS_420 = "SECONDS_420"
    SECONDS_480 = "SECONDS_480"
    SECONDS_540 = "SECONDS_540"
    SECONDS_600 = "SECONDS_600"


class TamsGapHandling(StrEnum):
    SKIP_GAPS = "SKIP_GAPS"
    FILL_WITH_BLACK = "FILL_WITH_BLACK"
    HOLD_LAST_FRAME = "HOLD_LAST_FRAME"


class TeletextPageType(StrEnum):
    PAGE_TYPE_INITIAL = "PAGE_TYPE_INITIAL"
    PAGE_TYPE_SUBTITLE = "PAGE_TYPE_SUBTITLE"
    PAGE_TYPE_ADDL_INFO = "PAGE_TYPE_ADDL_INFO"
    PAGE_TYPE_PROGRAM_SCHEDULE = "PAGE_TYPE_PROGRAM_SCHEDULE"
    PAGE_TYPE_HEARING_IMPAIRED_SUBTITLE = "PAGE_TYPE_HEARING_IMPAIRED_SUBTITLE"


class TimecodeBurninPosition(StrEnum):
    TOP_CENTER = "TOP_CENTER"
    TOP_LEFT = "TOP_LEFT"
    TOP_RIGHT = "TOP_RIGHT"
    MIDDLE_LEFT = "MIDDLE_LEFT"
    MIDDLE_CENTER = "MIDDLE_CENTER"
    MIDDLE_RIGHT = "MIDDLE_RIGHT"
    BOTTOM_LEFT = "BOTTOM_LEFT"
    BOTTOM_CENTER = "BOTTOM_CENTER"
    BOTTOM_RIGHT = "BOTTOM_RIGHT"


class TimecodeSource(StrEnum):
    EMBEDDED = "EMBEDDED"
    ZEROBASED = "ZEROBASED"
    SPECIFIEDSTART = "SPECIFIEDSTART"


class TimecodeTrack(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class TimedMetadata(StrEnum):
    PASSTHROUGH = "PASSTHROUGH"
    NONE = "NONE"


class TrackType(StrEnum):
    video = "video"
    audio = "audio"
    data = "data"


class TransferCharacteristics(StrEnum):
    ITU_709 = "ITU_709"
    UNSPECIFIED = "UNSPECIFIED"
    RESERVED = "RESERVED"
    ITU_470M = "ITU_470M"
    ITU_470BG = "ITU_470BG"
    SMPTE_170M = "SMPTE_170M"
    SMPTE_240M = "SMPTE_240M"
    LINEAR = "LINEAR"
    LOG10_2 = "LOG10_2"
    LOC10_2_5 = "LOC10_2_5"
    IEC_61966_2_4 = "IEC_61966_2_4"
    ITU_1361 = "ITU_1361"
    IEC_61966_2_1 = "IEC_61966_2_1"
    ITU_2020_10bit = "ITU_2020_10bit"
    ITU_2020_12bit = "ITU_2020_12bit"
    SMPTE_2084 = "SMPTE_2084"
    SMPTE_428_1 = "SMPTE_428_1"
    ARIB_B67 = "ARIB_B67"
    LAST = "LAST"


class TsPtsOffset(StrEnum):
    AUTO = "AUTO"
    SECONDS = "SECONDS"
    MILLISECONDS = "MILLISECONDS"


class TtmlStylePassthrough(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class Type(StrEnum):
    SYSTEM = "SYSTEM"
    CUSTOM = "CUSTOM"


class UncompressedFourcc(StrEnum):
    I420 = "I420"
    I422 = "I422"
    I444 = "I444"


class UncompressedFramerateControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class UncompressedFramerateConversionAlgorithm(StrEnum):
    DUPLICATE_DROP = "DUPLICATE_DROP"
    INTERPOLATE = "INTERPOLATE"
    FRAMEFORMER = "FRAMEFORMER"
    MAINTAIN_FRAME_COUNT = "MAINTAIN_FRAME_COUNT"


class UncompressedInterlaceMode(StrEnum):
    INTERLACED = "INTERLACED"
    PROGRESSIVE = "PROGRESSIVE"


class UncompressedScanTypeConversionMode(StrEnum):
    INTERLACED = "INTERLACED"
    INTERLACED_OPTIMIZE = "INTERLACED_OPTIMIZE"


class UncompressedSlowPal(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class UncompressedTelecine(StrEnum):
    NONE = "NONE"
    HARD = "HARD"


class Vc3Class(StrEnum):
    CLASS_145_8BIT = "CLASS_145_8BIT"
    CLASS_220_8BIT = "CLASS_220_8BIT"
    CLASS_220_10BIT = "CLASS_220_10BIT"


class Vc3FramerateControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class Vc3FramerateConversionAlgorithm(StrEnum):
    DUPLICATE_DROP = "DUPLICATE_DROP"
    INTERPOLATE = "INTERPOLATE"
    FRAMEFORMER = "FRAMEFORMER"
    MAINTAIN_FRAME_COUNT = "MAINTAIN_FRAME_COUNT"


class Vc3InterlaceMode(StrEnum):
    INTERLACED = "INTERLACED"
    PROGRESSIVE = "PROGRESSIVE"


class Vc3ScanTypeConversionMode(StrEnum):
    INTERLACED = "INTERLACED"
    INTERLACED_OPTIMIZE = "INTERLACED_OPTIMIZE"


class Vc3SlowPal(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class Vc3Telecine(StrEnum):
    NONE = "NONE"
    HARD = "HARD"


class VchipAction(StrEnum):
    PASSTHROUGH = "PASSTHROUGH"
    STRIP = "STRIP"


class VideoCodec(StrEnum):
    AV1 = "AV1"
    AVC_INTRA = "AVC_INTRA"
    FRAME_CAPTURE = "FRAME_CAPTURE"
    GIF = "GIF"
    H_264 = "H_264"
    H_265 = "H_265"
    MPEG2 = "MPEG2"
    PASSTHROUGH = "PASSTHROUGH"
    PRORES = "PRORES"
    UNCOMPRESSED = "UNCOMPRESSED"
    VC3 = "VC3"
    VP8 = "VP8"
    VP9 = "VP9"
    XAVC = "XAVC"


class VideoOverlayPlayBackMode(StrEnum):
    ONCE = "ONCE"
    REPEAT = "REPEAT"


class VideoOverlayUnit(StrEnum):
    PIXELS = "PIXELS"
    PERCENTAGE = "PERCENTAGE"


class VideoSelectorMode(StrEnum):
    AUTO = "AUTO"
    REMUX_ALL = "REMUX_ALL"


class VideoSelectorType(StrEnum):
    AUTO = "AUTO"
    STREAM = "STREAM"


class VideoTimecodeInsertion(StrEnum):
    DISABLED = "DISABLED"
    PIC_TIMING_SEI = "PIC_TIMING_SEI"


class Vp8FramerateControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class Vp8FramerateConversionAlgorithm(StrEnum):
    DUPLICATE_DROP = "DUPLICATE_DROP"
    INTERPOLATE = "INTERPOLATE"
    FRAMEFORMER = "FRAMEFORMER"
    MAINTAIN_FRAME_COUNT = "MAINTAIN_FRAME_COUNT"


class Vp8ParControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class Vp8QualityTuningLevel(StrEnum):
    MULTI_PASS = "MULTI_PASS"
    MULTI_PASS_HQ = "MULTI_PASS_HQ"


class Vp8RateControlMode(StrEnum):
    VBR = "VBR"


class Vp9FramerateControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class Vp9FramerateConversionAlgorithm(StrEnum):
    DUPLICATE_DROP = "DUPLICATE_DROP"
    INTERPOLATE = "INTERPOLATE"
    FRAMEFORMER = "FRAMEFORMER"
    MAINTAIN_FRAME_COUNT = "MAINTAIN_FRAME_COUNT"


class Vp9ParControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class Vp9QualityTuningLevel(StrEnum):
    MULTI_PASS = "MULTI_PASS"
    MULTI_PASS_HQ = "MULTI_PASS_HQ"


class Vp9RateControlMode(StrEnum):
    VBR = "VBR"


class WatermarkingStrength(StrEnum):
    LIGHTEST = "LIGHTEST"
    LIGHTER = "LIGHTER"
    DEFAULT = "DEFAULT"
    STRONGER = "STRONGER"
    STRONGEST = "STRONGEST"


class WavFormat(StrEnum):
    RIFF = "RIFF"
    RF64 = "RF64"
    EXTENSIBLE = "EXTENSIBLE"


class WebvttAccessibilitySubs(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class WebvttStylePassthrough(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    STRICT = "STRICT"
    MERGE = "MERGE"


class Xavc4kIntraCbgProfileClass(StrEnum):
    CLASS_100 = "CLASS_100"
    CLASS_300 = "CLASS_300"
    CLASS_480 = "CLASS_480"


class Xavc4kIntraVbrProfileClass(StrEnum):
    CLASS_100 = "CLASS_100"
    CLASS_300 = "CLASS_300"
    CLASS_480 = "CLASS_480"


class Xavc4kProfileBitrateClass(StrEnum):
    BITRATE_CLASS_100 = "BITRATE_CLASS_100"
    BITRATE_CLASS_140 = "BITRATE_CLASS_140"
    BITRATE_CLASS_200 = "BITRATE_CLASS_200"


class Xavc4kProfileCodecProfile(StrEnum):
    HIGH = "HIGH"
    HIGH_422 = "HIGH_422"


class Xavc4kProfileQualityTuningLevel(StrEnum):
    SINGLE_PASS = "SINGLE_PASS"
    SINGLE_PASS_HQ = "SINGLE_PASS_HQ"
    MULTI_PASS_HQ = "MULTI_PASS_HQ"


class XavcAdaptiveQuantization(StrEnum):
    OFF = "OFF"
    AUTO = "AUTO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    HIGHER = "HIGHER"
    MAX = "MAX"


class XavcEntropyEncoding(StrEnum):
    AUTO = "AUTO"
    CABAC = "CABAC"
    CAVLC = "CAVLC"


class XavcFlickerAdaptiveQuantization(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class XavcFramerateControl(StrEnum):
    INITIALIZE_FROM_SOURCE = "INITIALIZE_FROM_SOURCE"
    SPECIFIED = "SPECIFIED"


class XavcFramerateConversionAlgorithm(StrEnum):
    DUPLICATE_DROP = "DUPLICATE_DROP"
    INTERPOLATE = "INTERPOLATE"
    FRAMEFORMER = "FRAMEFORMER"
    MAINTAIN_FRAME_COUNT = "MAINTAIN_FRAME_COUNT"


class XavcGopBReference(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class XavcHdIntraCbgProfileClass(StrEnum):
    CLASS_50 = "CLASS_50"
    CLASS_100 = "CLASS_100"
    CLASS_200 = "CLASS_200"


class XavcHdProfileBitrateClass(StrEnum):
    BITRATE_CLASS_25 = "BITRATE_CLASS_25"
    BITRATE_CLASS_35 = "BITRATE_CLASS_35"
    BITRATE_CLASS_50 = "BITRATE_CLASS_50"


class XavcHdProfileQualityTuningLevel(StrEnum):
    SINGLE_PASS = "SINGLE_PASS"
    SINGLE_PASS_HQ = "SINGLE_PASS_HQ"
    MULTI_PASS_HQ = "MULTI_PASS_HQ"


class XavcHdProfileTelecine(StrEnum):
    NONE = "NONE"
    HARD = "HARD"


class XavcInterlaceMode(StrEnum):
    PROGRESSIVE = "PROGRESSIVE"
    TOP_FIELD = "TOP_FIELD"
    BOTTOM_FIELD = "BOTTOM_FIELD"
    FOLLOW_TOP_FIELD = "FOLLOW_TOP_FIELD"
    FOLLOW_BOTTOM_FIELD = "FOLLOW_BOTTOM_FIELD"


class XavcProfile(StrEnum):
    XAVC_HD_INTRA_CBG = "XAVC_HD_INTRA_CBG"
    XAVC_4K_INTRA_CBG = "XAVC_4K_INTRA_CBG"
    XAVC_4K_INTRA_VBR = "XAVC_4K_INTRA_VBR"
    XAVC_HD = "XAVC_HD"
    XAVC_4K = "XAVC_4K"


class XavcSlowPal(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class XavcSpatialAdaptiveQuantization(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class XavcTemporalAdaptiveQuantization(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class BadRequestException(ServiceException):
    """The service can't process your request because of a problem in the
    request. Please check your request form and syntax.
    """

    code: str = "BadRequestException"
    sender_fault: bool = False
    status_code: int = 400


class ConflictException(ServiceException):
    """The service couldn't complete your request because there is a conflict
    with the current state of the resource.
    """

    code: str = "ConflictException"
    sender_fault: bool = False
    status_code: int = 409


class ForbiddenException(ServiceException):
    """You don't have permissions for this action with the credentials you
    sent.
    """

    code: str = "ForbiddenException"
    sender_fault: bool = False
    status_code: int = 403


class InternalServerErrorException(ServiceException):
    """The service encountered an unexpected condition and can't fulfill your
    request.
    """

    code: str = "InternalServerErrorException"
    sender_fault: bool = False
    status_code: int = 500


class NotFoundException(ServiceException):
    """The resource you requested doesn't exist."""

    code: str = "NotFoundException"
    sender_fault: bool = False
    status_code: int = 404


class ServiceQuotaExceededException(ServiceException):
    """You attempted to create more resources than the service allows based on
    service quotas.
    """

    code: str = "ServiceQuotaExceededException"
    sender_fault: bool = False
    status_code: int = 402


class TooManyRequestsException(ServiceException):
    """Too many requests have been sent in too short of a time. The service
    limits the rate at which it will accept requests.
    """

    code: str = "TooManyRequestsException"
    sender_fault: bool = False
    status_code: int = 429


class AacSettings(TypedDict, total=False):
    """Required when you set Codec to the value AAC. The service accepts one of
    two mutually exclusive groups of AAC settings--VBR and CBR. To select
    one of these modes, set the value of Bitrate control mode to "VBR" or
    "CBR". In VBR mode, you control the audio quality with the setting VBR
    quality. In CBR mode, you use the setting Bitrate. Defaults and valid
    values depend on the rate control mode.
    """

    AudioDescriptionBroadcasterMix: AacAudioDescriptionBroadcasterMix | None
    Bitrate: _integerMin6000Max1024000 | None
    CodecProfile: AacCodecProfile | None
    CodingMode: AacCodingMode | None
    LoudnessMeasurementMode: AacLoudnessMeasurementMode | None
    RapInterval: _integerMin2000Max30000 | None
    RateControlMode: AacRateControlMode | None
    RawFormat: AacRawFormat | None
    SampleRate: _integerMin8000Max96000 | None
    Specification: AacSpecification | None
    TargetLoudnessRange: _integerMin6Max16 | None
    VbrQuality: AacVbrQuality | None


class Ac3Settings(TypedDict, total=False):
    """Required when you set Codec to the value AC3."""

    Bitrate: _integerMin64000Max640000 | None
    BitstreamMode: Ac3BitstreamMode | None
    CodingMode: Ac3CodingMode | None
    Dialnorm: _integerMin1Max31 | None
    DynamicRangeCompressionLine: Ac3DynamicRangeCompressionLine | None
    DynamicRangeCompressionProfile: Ac3DynamicRangeCompressionProfile | None
    DynamicRangeCompressionRf: Ac3DynamicRangeCompressionRf | None
    LfeFilter: Ac3LfeFilter | None
    MetadataControl: Ac3MetadataControl | None
    SampleRate: _integerMin48000Max48000 | None


class AccelerationSettings(TypedDict, total=False):
    """Accelerated transcoding can significantly speed up jobs with long,
    visually complex content.
    """

    Mode: AccelerationMode


class AdvancedInputFilterSettings(TypedDict, total=False):
    """Optional settings for Advanced input filter when you set Advanced input
    filter to Enabled.
    """

    AddTexture: AdvancedInputFilterAddTexture | None
    Sharpening: AdvancedInputFilterSharpen | None


class AiffSettings(TypedDict, total=False):
    """Required when you set Codec to the value AIFF."""

    BitDepth: _integerMin16Max24 | None
    Channels: _integerMin1Max64 | None
    SampleRate: _integerMin8000Max192000 | None


class AllowedRenditionSize(TypedDict, total=False):
    """Use Allowed renditions to specify a list of possible resolutions in your
    ABR stack. \\* MediaConvert will create an ABR stack exclusively from the
    list of resolutions that you specify. \\* Some resolutions in the Allowed
    renditions list may not be included, however you can force a resolution
    to be included by setting Required to ENABLED. \\* You must specify at
    least one resolution that is greater than or equal to any resolutions
    that you specify in Min top rendition size or Min bottom rendition size.
    \\* If you specify Allowed renditions, you must not specify a separate
    rule for Force include renditions.
    """

    Height: _integerMin32Max8192 | None
    Required: RequiredFlag | None
    Width: _integerMin32Max8192 | None


class AncillarySourceSettings(TypedDict, total=False):
    """Settings for ancillary captions source."""

    Convert608To708: AncillaryConvert608To708 | None
    SourceAncillaryChannelNumber: _integerMin1Max4 | None
    TerminateCaptions: AncillaryTerminateCaptions | None


class AssociateCertificateRequest(ServiceRequest):
    Arn: _string


class AssociateCertificateResponse(TypedDict, total=False):
    pass


_listOfAudioChannelTag = list[AudioChannelTag]


class AudioChannelTaggingSettings(TypedDict, total=False):
    """Specify the QuickTime audio channel layout tags for the audio channels
    in this audio track. When you don't specify a value, MediaConvert labels
    your track as Center (C) by default. To use Audio layout tagging, your
    output must be in a QuickTime (MOV) container and your audio codec must
    be AAC, WAV, or AIFF.
    """

    ChannelTag: AudioChannelTag | None
    ChannelTags: _listOfAudioChannelTag | None


class WavSettings(TypedDict, total=False):
    """Required when you set Codec to the value WAV."""

    BitDepth: _integerMin16Max24 | None
    Channels: _integerMin1Max64 | None
    Format: WavFormat | None
    SampleRate: _integerMin8000Max192000 | None


class VorbisSettings(TypedDict, total=False):
    """Required when you set Codec, under AudioDescriptions>CodecSettings, to
    the value Vorbis.
    """

    Channels: _integerMin1Max2 | None
    SampleRate: _integerMin22050Max48000 | None
    VbrQuality: _integerMinNegative1Max10 | None


class OpusSettings(TypedDict, total=False):
    """Required when you set Codec, under AudioDescriptions>CodecSettings, to
    the value OPUS.
    """

    Bitrate: _integerMin32000Max192000 | None
    Channels: _integerMin1Max2 | None
    SampleRate: _integerMin16000Max48000 | None


class Mp3Settings(TypedDict, total=False):
    """Required when you set Codec, under AudioDescriptions>CodecSettings, to
    the value MP3.
    """

    Bitrate: _integerMin16000Max320000 | None
    Channels: _integerMin1Max2 | None
    RateControlMode: Mp3RateControlMode | None
    SampleRate: _integerMin22050Max48000 | None
    VbrQuality: _integerMin0Max9 | None


class Mp2Settings(TypedDict, total=False):
    """Required when you set Codec to the value MP2."""

    AudioDescriptionMix: Mp2AudioDescriptionMix | None
    Bitrate: _integerMin32000Max384000 | None
    Channels: _integerMin1Max2 | None
    SampleRate: _integerMin32000Max48000 | None


class FlacSettings(TypedDict, total=False):
    """Required when you set Codec, under AudioDescriptions>CodecSettings, to
    the value FLAC.
    """

    BitDepth: _integerMin16Max24 | None
    Channels: _integerMin1Max8 | None
    SampleRate: _integerMin22050Max192000 | None


class Eac3Settings(TypedDict, total=False):
    """Required when you set Codec to the value EAC3."""

    AttenuationControl: Eac3AttenuationControl | None
    Bitrate: _integerMin32000Max3024000 | None
    BitstreamMode: Eac3BitstreamMode | None
    CodingMode: Eac3CodingMode | None
    DcFilter: Eac3DcFilter | None
    Dialnorm: _integerMin1Max31 | None
    DynamicRangeCompressionLine: Eac3DynamicRangeCompressionLine | None
    DynamicRangeCompressionRf: Eac3DynamicRangeCompressionRf | None
    LfeControl: Eac3LfeControl | None
    LfeFilter: Eac3LfeFilter | None
    LoRoCenterMixLevel: _doubleMinNegative60Max3 | None
    LoRoSurroundMixLevel: _doubleMinNegative60MaxNegative1 | None
    LtRtCenterMixLevel: _doubleMinNegative60Max3 | None
    LtRtSurroundMixLevel: _doubleMinNegative60MaxNegative1 | None
    MetadataControl: Eac3MetadataControl | None
    PassthroughControl: Eac3PassthroughControl | None
    PhaseControl: Eac3PhaseControl | None
    SampleRate: _integerMin48000Max48000 | None
    StereoDownmix: Eac3StereoDownmix | None
    SurroundExMode: Eac3SurroundExMode | None
    SurroundMode: Eac3SurroundMode | None


class Eac3AtmosSettings(TypedDict, total=False):
    """Required when you set Codec to the value EAC3_ATMOS."""

    Bitrate: _integerMin384000Max1024000 | None
    BitstreamMode: Eac3AtmosBitstreamMode | None
    CodingMode: Eac3AtmosCodingMode | None
    DialogueIntelligence: Eac3AtmosDialogueIntelligence | None
    DownmixControl: Eac3AtmosDownmixControl | None
    DynamicRangeCompressionLine: Eac3AtmosDynamicRangeCompressionLine | None
    DynamicRangeCompressionRf: Eac3AtmosDynamicRangeCompressionRf | None
    DynamicRangeControl: Eac3AtmosDynamicRangeControl | None
    LoRoCenterMixLevel: _doubleMinNegative6Max3 | None
    LoRoSurroundMixLevel: _doubleMinNegative60MaxNegative1 | None
    LtRtCenterMixLevel: _doubleMinNegative6Max3 | None
    LtRtSurroundMixLevel: _doubleMinNegative60MaxNegative1 | None
    MeteringMode: Eac3AtmosMeteringMode | None
    SampleRate: _integerMin48000Max48000 | None
    SpeechThreshold: _integerMin0Max100 | None
    StereoDownmix: Eac3AtmosStereoDownmix | None
    SurroundExMode: Eac3AtmosSurroundExMode | None


class AudioCodecSettings(TypedDict, total=False):
    """Settings related to audio encoding. The settings in this group vary
    depending on the value that you choose for your audio codec.
    """

    AacSettings: AacSettings | None
    Ac3Settings: Ac3Settings | None
    AiffSettings: AiffSettings | None
    Codec: AudioCodec | None
    Eac3AtmosSettings: Eac3AtmosSettings | None
    Eac3Settings: Eac3Settings | None
    FlacSettings: FlacSettings | None
    Mp2Settings: Mp2Settings | None
    Mp3Settings: Mp3Settings | None
    OpusSettings: OpusSettings | None
    VorbisSettings: VorbisSettings | None
    WavSettings: WavSettings | None


_listOf__doubleMinNegative60Max6 = list[_doubleMinNegative60Max6]
_listOf__integerMinNegative60Max6 = list[_integerMinNegative60Max6]


class OutputChannelMapping(TypedDict, total=False):
    """OutputChannel mapping settings."""

    InputChannels: _listOf__integerMinNegative60Max6 | None
    InputChannelsFineTune: _listOf__doubleMinNegative60Max6 | None


_listOfOutputChannelMapping = list[OutputChannelMapping]


class ChannelMapping(TypedDict, total=False):
    """Channel mapping contains the group of fields that hold the remixing
    value for each channel, in dB. Specify remix values to indicate how much
    of the content from your input audio channel you want in your output
    audio channels. Each instance of the InputChannels or
    InputChannelsFineTune array specifies these values for one output
    channel. Use one instance of this array for each output channel. In the
    console, each array corresponds to a column in the graphical depiction
    of the mapping matrix. The rows of the graphical matrix correspond to
    input channels. Valid values are within the range from -60 (mute)
    through 6. A setting of 0 passes the input channel unchanged to the
    output channel (no attenuation or amplification). Use InputChannels or
    InputChannelsFineTune to specify your remix values. Don't use both.
    """

    OutputChannels: _listOfOutputChannelMapping | None


class RemixSettings(TypedDict, total=False):
    """Use Manual audio remixing to adjust audio levels for each audio channel
    in each output of your job. With audio remixing, you can output more or
    fewer audio channels than your input audio source provides.
    """

    AudioDescriptionAudioChannel: _integerMin1Max64 | None
    AudioDescriptionDataChannel: _integerMin1Max64 | None
    ChannelMapping: ChannelMapping | None
    ChannelsIn: _integerMin1Max64 | None
    ChannelsOut: _integerMin1Max64 | None


class AudioPitchCorrectionSettings(TypedDict, total=False):
    """Settings for audio pitch correction during framerate conversion."""

    SlowPalPitchCorrection: SlowPalPitchCorrection | None


class AudioNormalizationSettings(TypedDict, total=False):
    """Advanced audio normalization settings. Ignore these settings unless you
    need to comply with a loudness standard.
    """

    Algorithm: AudioNormalizationAlgorithm | None
    AlgorithmControl: AudioNormalizationAlgorithmControl | None
    CorrectionGateLevel: _integerMinNegative70Max0 | None
    LoudnessLogging: AudioNormalizationLoudnessLogging | None
    PeakCalculation: AudioNormalizationPeakCalculation | None
    TargetLkfs: _doubleMinNegative59Max0 | None
    TruePeakLimiterThreshold: _doubleMinNegative8Max0 | None


class AudioDescription(TypedDict, total=False):
    """Settings related to one audio tab on the MediaConvert console. In your
    job JSON, an instance of AudioDescription is equivalent to one audio tab
    in the console. Usually, one audio tab corresponds to one output audio
    track. Depending on how you set up your input audio selectors and
    whether you use audio selector groups, one audio tab can correspond to a
    group of output audio tracks.
    """

    AudioChannelTaggingSettings: AudioChannelTaggingSettings | None
    AudioNormalizationSettings: AudioNormalizationSettings | None
    AudioPitchCorrectionSettings: AudioPitchCorrectionSettings | None
    AudioSourceName: _stringMax2048 | None
    AudioType: _integerMin0Max255 | None
    AudioTypeControl: AudioTypeControl | None
    CodecSettings: AudioCodecSettings | None
    CustomLanguageCode: _stringPatternAZaZ23AZaZ09 | None
    LanguageCode: LanguageCode | None
    LanguageCodeControl: AudioLanguageCodeControl | None
    RemixSettings: RemixSettings | None
    StreamName: _stringPatternWS | None


class FrameRate(TypedDict, total=False):
    """The frame rate of the video or audio track, expressed as a fraction with
    numerator and denominator values.
    """

    Denominator: _integer | None
    Numerator: _integer | None


_long = int


class AudioProperties(TypedDict, total=False):
    """Details about the media file's audio track."""

    BitDepth: _integer | None
    BitRate: _long | None
    Channels: _integer | None
    FrameRate: FrameRate | None
    LanguageCode: _string | None
    SampleRate: _integer | None


_listOf__integerMin1Max2147483647 = list[_integerMin1Max2147483647]


class HlsRenditionGroupSettings(TypedDict, total=False):
    """Settings specific to audio sources in an HLS alternate rendition group.
    Specify the properties (renditionGroupId, renditionName or
    renditionLanguageCode) to identify the unique audio track among the
    alternative rendition groups present in the HLS manifest. If no unique
    track is found, or multiple tracks match the properties provided, the
    job fails. If no properties in hlsRenditionGroupSettings are specified,
    the default audio track within the video segment is chosen. If there is
    no audio within video segment, the alternative audio with DEFAULT=YES is
    chosen instead.
    """

    RenditionGroupId: _string | None
    RenditionLanguageCode: LanguageCode | None
    RenditionName: _string | None


class AudioSelector(TypedDict, total=False):
    """Use Audio selectors to specify a track or set of tracks from the input
    that you will use in your outputs. You can use multiple Audio selectors
    per input.
    """

    AudioDurationCorrection: AudioDurationCorrection | None
    CustomLanguageCode: _stringMin3Max3PatternAZaZ3 | None
    DefaultSelection: AudioDefaultSelection | None
    ExternalAudioFileInput: _stringPatternS3Https | None
    HlsRenditionGroupSettings: HlsRenditionGroupSettings | None
    LanguageCode: LanguageCode | None
    Offset: _integerMinNegative2147483648Max2147483647 | None
    Pids: _listOf__integerMin1Max2147483647 | None
    ProgramSelection: _integerMin0Max8 | None
    RemixSettings: RemixSettings | None
    SelectorType: AudioSelectorType | None
    Streams: _listOf__integerMin1Max2147483647 | None
    Tracks: _listOf__integerMin1Max2147483647 | None


_listOf__stringMin1 = list[_stringMin1]


class AudioSelectorGroup(TypedDict, total=False):
    """Use audio selector groups to combine multiple sidecar audio inputs so
    that you can assign them to a single output audio tab. Note that, if
    you're working with embedded audio, it's simpler to assign multiple
    input tracks into a single audio selector rather than use an audio
    selector group.
    """

    AudioSelectorNames: _listOf__stringMin1 | None


class MinTopRenditionSize(TypedDict, total=False):
    """Use Min top rendition size to specify a minimum size for the highest
    resolution in your ABR stack. \\* The highest resolution in your ABR
    stack will be equal to or greater than the value that you enter. For
    example: If you specify 1280x720 the highest resolution in your ABR
    stack will be equal to or greater than 1280x720. \\* If you specify a
    value for Max resolution, the value that you specify for Min top
    rendition size must be less than, or equal to, Max resolution.
    """

    Height: _integerMin32Max8192 | None
    Width: _integerMin32Max8192 | None


class MinBottomRenditionSize(TypedDict, total=False):
    """Use Min bottom rendition size to specify a minimum size for the lowest
    resolution in your ABR stack. \\* The lowest resolution in your ABR stack
    will be equal to or greater than the value that you enter. For example:
    If you specify 640x360 the lowest resolution in your ABR stack will be
    equal to or greater than to 640x360. \\* If you specify a Min top
    rendition size rule, the value that you specify for Min bottom rendition
    size must be less than, or equal to, Min top rendition size.
    """

    Height: _integerMin32Max8192 | None
    Width: _integerMin32Max8192 | None


class ForceIncludeRenditionSize(TypedDict, total=False):
    """Use Force include renditions to specify one or more resolutions to
    include your ABR stack. \\* (Recommended) To optimize automated ABR,
    specify as few resolutions as possible. \\* (Required) The number of
    resolutions that you specify must be equal to, or less than, the Max
    renditions setting. \\* If you specify a Min top rendition size rule,
    specify at least one resolution that is equal to, or greater than, Min
    top rendition size. \\* If you specify a Min bottom rendition size rule,
    only specify resolutions that are equal to, or greater than, Min bottom
    rendition size. \\* If you specify a Force include renditions rule, do
    not specify a separate rule for Allowed renditions. \\* Note: The ABR
    stack may include other resolutions that you do not specify here,
    depending on the Max renditions setting.
    """

    Height: _integerMin32Max8192 | None
    Width: _integerMin32Max8192 | None


_listOfForceIncludeRenditionSize = list[ForceIncludeRenditionSize]
_listOfAllowedRenditionSize = list[AllowedRenditionSize]


class AutomatedAbrRule(TypedDict, total=False):
    """Specify one or more Automated ABR rule types. Note: Force include and
    Allowed renditions are mutually exclusive.
    """

    AllowedRenditions: _listOfAllowedRenditionSize | None
    ForceIncludeRenditions: _listOfForceIncludeRenditionSize | None
    MinBottomRenditionSize: MinBottomRenditionSize | None
    MinTopRenditionSize: MinTopRenditionSize | None
    Type: RuleType | None


_listOfAutomatedAbrRule = list[AutomatedAbrRule]


class AutomatedAbrSettings(TypedDict, total=False):
    """Use automated ABR to have MediaConvert set up the renditions in your ABR
    package for you automatically, based on characteristics of your input
    video. This feature optimizes video quality while minimizing the overall
    size of your ABR package.
    """

    MaxAbrBitrate: _integerMin100000Max100000000 | None
    MaxQualityLevel: _doubleMin1Max10 | None
    MaxRenditions: _integerMin3Max15 | None
    MinAbrBitrate: _integerMin100000Max100000000 | None
    Rules: _listOfAutomatedAbrRule | None


class AutomatedEncodingSettings(TypedDict, total=False):
    """Use automated encoding to have MediaConvert choose your encoding
    settings for you, based on characteristics of your input video.
    """

    AbrSettings: AutomatedAbrSettings | None


class Av1QvbrSettings(TypedDict, total=False):
    """Settings for quality-defined variable bitrate encoding with the AV1
    codec. Use these settings only when you set QVBR for Rate control mode.
    """

    QvbrQualityLevel: _integerMin1Max10 | None
    QvbrQualityLevelFineTune: _doubleMin0Max1 | None


_listOfFrameMetricType = list[FrameMetricType]


class Av1Settings(TypedDict, total=False):
    """Required when you set Codec, under VideoDescription>CodecSettings to the
    value AV1.
    """

    AdaptiveQuantization: Av1AdaptiveQuantization | None
    BitDepth: Av1BitDepth | None
    FilmGrainSynthesis: Av1FilmGrainSynthesis | None
    FramerateControl: Av1FramerateControl | None
    FramerateConversionAlgorithm: Av1FramerateConversionAlgorithm | None
    FramerateDenominator: _integerMin1Max2147483647 | None
    FramerateNumerator: _integerMin1Max2147483647 | None
    GopSize: _doubleMin0 | None
    MaxBitrate: _integerMin1000Max1152000000 | None
    NumberBFramesBetweenReferenceFrames: _integerMin0Max15 | None
    PerFrameMetrics: _listOfFrameMetricType | None
    QvbrSettings: Av1QvbrSettings | None
    RateControlMode: Av1RateControlMode | None
    Slices: _integerMin1Max32 | None
    SpatialAdaptiveQuantization: Av1SpatialAdaptiveQuantization | None


class AvailBlanking(TypedDict, total=False):
    """Use ad avail blanking settings to specify your output content during
    SCTE-35 triggered ad avails. You can blank your video or overlay it with
    an image. MediaConvert also removes any audio and embedded captions
    during the ad avail. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/ad-avail-blanking.html.
    """

    AvailBlankingImage: _stringMin14PatternS3BmpBMPPngPNGHttpsBmpBMPPngPNG | None


class AvcIntraUhdSettings(TypedDict, total=False):
    """Optional when you set AVC-Intra class to Class 4K/2K. When you set
    AVC-Intra class to a different value, this object isn't allowed.
    """

    QualityTuningLevel: AvcIntraUhdQualityTuningLevel | None


class AvcIntraSettings(TypedDict, total=False):
    """Required when you choose AVC-Intra for your output video codec. For more
    information about the AVC-Intra settings, see the relevant
    specification. For detailed information about SD and HD in AVC-Intra,
    see https://ieeexplore.ieee.org/document/7290936. For information about
    4K/2K in AVC-Intra, see
    https://pro-av.panasonic.net/en/avc-ultra/AVC-ULTRAoverview.pdf.
    """

    AvcIntraClass: AvcIntraClass | None
    AvcIntraUhdSettings: AvcIntraUhdSettings | None
    FramerateControl: AvcIntraFramerateControl | None
    FramerateConversionAlgorithm: AvcIntraFramerateConversionAlgorithm | None
    FramerateDenominator: _integerMin1Max1001 | None
    FramerateNumerator: _integerMin24Max60000 | None
    InterlaceMode: AvcIntraInterlaceMode | None
    PerFrameMetrics: _listOfFrameMetricType | None
    ScanTypeConversionMode: AvcIntraScanTypeConversionMode | None
    SlowPal: AvcIntraSlowPal | None
    Telecine: AvcIntraTelecine | None


class BandwidthReductionFilter(TypedDict, total=False):
    """The Bandwidth reduction filter increases the video quality of your
    output relative to its bitrate. Use to lower the bitrate of your
    constant quality QVBR output, with little or no perceptual decrease in
    quality. Or, use to increase the video quality of outputs with other
    rate control modes relative to the bitrate that you specify. Bandwidth
    reduction increases further when your input is low quality or noisy.
    Outputs that use this feature incur pro-tier pricing. When you include
    Bandwidth reduction filter, you cannot include the Noise reducer
    preprocessor.
    """

    Sharpening: BandwidthReductionFilterSharpening | None
    Strength: BandwidthReductionFilterStrength | None


class BurninDestinationSettings(TypedDict, total=False):
    """Burn-in is a captions delivery method, rather than a captions format.
    Burn-in writes the captions directly on your video frames, replacing
    pixels of video content with the captions. Set up burn-in captions in
    the same output as your video. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/burn-in-output-captions.html.
    """

    Alignment: BurninSubtitleAlignment | None
    ApplyFontColor: BurninSubtitleApplyFontColor | None
    BackgroundColor: BurninSubtitleBackgroundColor | None
    BackgroundOpacity: _integerMin0Max255 | None
    FallbackFont: BurninSubtitleFallbackFont | None
    FontColor: BurninSubtitleFontColor | None
    FontFileBold: _stringPatternS3TtfHttpsTtf | None
    FontFileBoldItalic: _string | None
    FontFileItalic: _stringPatternS3TtfHttpsTtf | None
    FontFileRegular: _stringPatternS3TtfHttpsTtf | None
    FontOpacity: _integerMin0Max255 | None
    FontResolution: _integerMin96Max600 | None
    FontScript: FontScript | None
    FontSize: _integerMin0Max96 | None
    HexFontColor: _stringMin6Max8Pattern09aFAF609aFAF2 | None
    OutlineColor: BurninSubtitleOutlineColor | None
    OutlineSize: _integerMin0Max10 | None
    RemoveRubyReserveAttributes: RemoveRubyReserveAttributes | None
    ShadowColor: BurninSubtitleShadowColor | None
    ShadowOpacity: _integerMin0Max255 | None
    ShadowXOffset: _integerMinNegative2147483648Max2147483647 | None
    ShadowYOffset: _integerMinNegative2147483648Max2147483647 | None
    StylePassthrough: BurnInSubtitleStylePassthrough | None
    TeletextSpacing: BurninSubtitleTeletextSpacing | None
    XPosition: _integerMin0Max2147483647 | None
    YPosition: _integerMin0Max2147483647 | None


class CancelJobRequest(ServiceRequest):
    Id: _string


class CancelJobResponse(TypedDict, total=False):
    pass


class WebvttDestinationSettings(TypedDict, total=False):
    """Settings related to WebVTT captions. WebVTT is a sidecar format that
    holds captions in a file that is separate from the video container. Set
    up sidecar captions in the same output group, but different output from
    your video. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/ttml-and-webvtt-output-captions.html.
    """

    Accessibility: WebvttAccessibilitySubs | None
    StylePassthrough: WebvttStylePassthrough | None


class TtmlDestinationSettings(TypedDict, total=False):
    """Settings related to TTML captions. TTML is a sidecar format that holds
    captions in a file that is separate from the video container. Set up
    sidecar captions in the same output group, but different output from
    your video. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/ttml-and-webvtt-output-captions.html.
    """

    StylePassthrough: TtmlStylePassthrough | None


_listOfTeletextPageType = list[TeletextPageType]


class TeletextDestinationSettings(TypedDict, total=False):
    """Settings related to teletext captions. Set up teletext captions in the
    same output as your video. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/teletext-output-captions.html.
    """

    PageNumber: _stringMin3Max3Pattern1809aFAF09aEAE | None
    PageTypes: _listOfTeletextPageType | None


class SrtDestinationSettings(TypedDict, total=False):
    """Settings related to SRT captions. SRT is a sidecar format that holds
    captions in a file that is separate from the video container. Set up
    sidecar captions in the same output group, but different output from
    your video.
    """

    StylePassthrough: SrtStylePassthrough | None


class SccDestinationSettings(TypedDict, total=False):
    """Settings related to SCC captions. SCC is a sidecar format that holds
    captions in a file that is separate from the video container. Set up
    sidecar captions in the same output group, but different output from
    your video. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/scc-srt-output-captions.html.
    """

    Framerate: SccDestinationFramerate | None


class ImscDestinationSettings(TypedDict, total=False):
    """Settings related to IMSC captions. IMSC is a sidecar format that holds
    captions in a file that is separate from the video container. Set up
    sidecar captions in the same output group, but different output from
    your video. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/ttml-and-webvtt-output-captions.html.
    """

    Accessibility: ImscAccessibilitySubs | None
    StylePassthrough: ImscStylePassthrough | None


class EmbeddedDestinationSettings(TypedDict, total=False):
    """Settings related to CEA/EIA-608 and CEA/EIA-708 (also called embedded or
    ancillary) captions. Set up embedded captions in the same output as your
    video. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/embedded-output-captions.html.
    """

    Destination608ChannelNumber: _integerMin1Max4 | None
    Destination708ServiceNumber: _integerMin1Max6 | None


class DvbSubDestinationSettings(TypedDict, total=False):
    """Settings related to DVB-Sub captions. Set up DVB-Sub captions in the
    same output as your video. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/dvb-sub-output-captions.html.
    """

    Alignment: DvbSubtitleAlignment | None
    ApplyFontColor: DvbSubtitleApplyFontColor | None
    BackgroundColor: DvbSubtitleBackgroundColor | None
    BackgroundOpacity: _integerMin0Max255 | None
    DdsHandling: DvbddsHandling | None
    DdsXCoordinate: _integerMin0Max2147483647 | None
    DdsYCoordinate: _integerMin0Max2147483647 | None
    FallbackFont: DvbSubSubtitleFallbackFont | None
    FontColor: DvbSubtitleFontColor | None
    FontFileBold: _stringPatternS3TtfHttpsTtf | None
    FontFileBoldItalic: _stringPatternS3TtfHttpsTtf | None
    FontFileItalic: _stringPatternS3TtfHttpsTtf | None
    FontFileRegular: _stringPatternS3TtfHttpsTtf | None
    FontOpacity: _integerMin0Max255 | None
    FontResolution: _integerMin96Max600 | None
    FontScript: FontScript | None
    FontSize: _integerMin0Max96 | None
    Height: _integerMin1Max2147483647 | None
    HexFontColor: _stringMin6Max8Pattern09aFAF609aFAF2 | None
    OutlineColor: DvbSubtitleOutlineColor | None
    OutlineSize: _integerMin0Max10 | None
    ShadowColor: DvbSubtitleShadowColor | None
    ShadowOpacity: _integerMin0Max255 | None
    ShadowXOffset: _integerMinNegative2147483648Max2147483647 | None
    ShadowYOffset: _integerMinNegative2147483648Max2147483647 | None
    StylePassthrough: DvbSubtitleStylePassthrough | None
    SubtitlingType: DvbSubtitlingType | None
    TeletextSpacing: DvbSubtitleTeletextSpacing | None
    Width: _integerMin1Max2147483647 | None
    XPosition: _integerMin0Max2147483647 | None
    YPosition: _integerMin0Max2147483647 | None


class CaptionDestinationSettings(TypedDict, total=False):
    """Settings related to one captions tab on the MediaConvert console.
    Usually, one captions tab corresponds to one output captions track.
    Depending on your output captions format, one tab might correspond to a
    set of output captions tracks. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/including-captions.html.
    """

    BurninDestinationSettings: BurninDestinationSettings | None
    DestinationType: CaptionDestinationType | None
    DvbSubDestinationSettings: DvbSubDestinationSettings | None
    EmbeddedDestinationSettings: EmbeddedDestinationSettings | None
    ImscDestinationSettings: ImscDestinationSettings | None
    SccDestinationSettings: SccDestinationSettings | None
    SrtDestinationSettings: SrtDestinationSettings | None
    TeletextDestinationSettings: TeletextDestinationSettings | None
    TtmlDestinationSettings: TtmlDestinationSettings | None
    WebvttDestinationSettings: WebvttDestinationSettings | None


class CaptionDescription(TypedDict, total=False):
    """This object holds groups of settings related to captions for one output.
    For each output that has captions, include one instance of
    CaptionDescriptions.
    """

    CaptionSelectorName: _stringMin1 | None
    CustomLanguageCode: _stringPatternAZaZ23AZaZ | None
    DestinationSettings: CaptionDestinationSettings | None
    LanguageCode: LanguageCode | None
    LanguageDescription: _string | None


class CaptionDescriptionPreset(TypedDict, total=False):
    """Caption Description for preset"""

    CustomLanguageCode: _stringPatternAZaZ23AZaZ | None
    DestinationSettings: CaptionDestinationSettings | None
    LanguageCode: LanguageCode | None
    LanguageDescription: _string | None


class WebvttHlsSourceSettings(TypedDict, total=False):
    """Settings specific to WebVTT sources in HLS alternative rendition group.
    Specify the properties (renditionGroupId, renditionName or
    renditionLanguageCode) to identify the unique subtitle track among the
    alternative rendition groups present in the HLS manifest. If no unique
    track is found, or multiple tracks match the specified properties, the
    job fails. If there is only one subtitle track in the rendition group,
    the settings can be left empty and the default subtitle track will be
    chosen. If your caption source is a sidecar file, use FileSourceSettings
    instead of WebvttHlsSourceSettings.
    """

    RenditionGroupId: _string | None
    RenditionLanguageCode: LanguageCode | None
    RenditionName: _string | None


class TrackSourceSettings(TypedDict, total=False):
    """Settings specific to caption sources that are specified by track number.
    Currently, this is only IMSC captions in an IMF package. If your caption
    source is IMSC 1.1 in a separate xml file, use FileSourceSettings
    instead of TrackSourceSettings.
    """

    StreamNumber: _integerMin1Max2147483647 | None
    TrackNumber: _integerMin1Max2147483647 | None


class TeletextSourceSettings(TypedDict, total=False):
    """Settings specific to Teletext caption sources, including Page number."""

    PageNumber: _stringMin3Max3Pattern1809aFAF09aEAE | None


class CaptionSourceFramerate(TypedDict, total=False):
    """Ignore this setting unless your input captions format is SCC. To have
    the service compensate for differing frame rates between your input
    captions and input video, specify the frame rate of the captions file.
    Specify this value as a fraction. For example, you might specify 24 / 1
    for 24 fps, 25 / 1 for 25 fps, 24000 / 1001 for 23.976 fps, or 30000 /
    1001 for 29.97 fps.
    """

    FramerateDenominator: _integerMin1Max1001 | None
    FramerateNumerator: _integerMin1Max60000 | None


class FileSourceSettings(TypedDict, total=False):
    """If your input captions are SCC, SMI, SRT, STL, TTML, WebVTT, or IMSC 1.1
    in an xml file, specify the URI of the input caption source file. If
    your caption source is IMSC in an IMF package, use TrackSourceSettings
    instead of FileSoureSettings.
    """

    ByteRateLimit: CaptionSourceByteRateLimit | None
    Convert608To708: FileSourceConvert608To708 | None
    ConvertPaintToPop: CaptionSourceConvertPaintOnToPopOn | None
    Framerate: CaptionSourceFramerate | None
    SourceFile: (
        _stringMin14PatternS3SccSCCTtmlTTMLDfxpDFXPStlSTLSrtSRTXmlXMLSmiSMIVttVTTWebvttWEBVTTHttpsSccSCCTtmlTTMLDfxpDFXPStlSTLSrtSRTXmlXMLSmiSMIVttVTTWebvttWEBVTT
        | None
    )
    TimeDelta: _integerMinNegative2147483648Max2147483647 | None
    TimeDeltaUnits: FileSourceTimeDeltaUnits | None
    UpconvertSTLToTeletext: CaptionSourceUpconvertSTLToTeletext | None


class EmbeddedSourceSettings(TypedDict, total=False):
    """Settings for embedded captions Source"""

    Convert608To708: EmbeddedConvert608To708 | None
    Source608ChannelNumber: _integerMin1Max4 | None
    Source608TrackNumber: _integerMin1Max1 | None
    TerminateCaptions: EmbeddedTerminateCaptions | None


class DvbSubSourceSettings(TypedDict, total=False):
    """DVB Sub Source Settings"""

    Pid: _integerMin1Max2147483647 | None


class CaptionSourceSettings(TypedDict, total=False):
    """If your input captions are SCC, TTML, STL, SMI, SRT, or IMSC in an xml
    file, specify the URI of the input captions source file. If your input
    captions are IMSC in an IMF package, use TrackSourceSettings instead of
    FileSoureSettings.
    """

    AncillarySourceSettings: AncillarySourceSettings | None
    DvbSubSourceSettings: DvbSubSourceSettings | None
    EmbeddedSourceSettings: EmbeddedSourceSettings | None
    FileSourceSettings: FileSourceSettings | None
    SourceType: CaptionSourceType | None
    TeletextSourceSettings: TeletextSourceSettings | None
    TrackSourceSettings: TrackSourceSettings | None
    WebvttHlsSourceSettings: WebvttHlsSourceSettings | None


class CaptionSelector(TypedDict, total=False):
    """Use captions selectors to specify the captions data from your input that
    you use in your outputs. You can use up to 100 captions selectors per
    input.
    """

    CustomLanguageCode: _stringMin3Max3PatternAZaZ3 | None
    LanguageCode: LanguageCode | None
    SourceSettings: CaptionSourceSettings | None


class ClipLimits(TypedDict, total=False):
    """Specify YUV limits and RGB tolerances when you set Sample range
    conversion to Limited range clip.
    """

    MaximumRGBTolerance: _integerMin90Max105 | None
    MaximumYUV: _integerMin920Max1023 | None
    MinimumRGBTolerance: _integerMinNegative5Max10 | None
    MinimumYUV: _integerMin0Max128 | None


class CmafAdditionalManifest(TypedDict, total=False):
    """Specify the details for each pair of HLS and DASH additional manifests
    that you want the service to generate for this CMAF output group. Each
    pair of manifests can reference a different subset of outputs in the
    group.
    """

    ManifestNameModifier: _stringMin1 | None
    SelectedOutputs: _listOf__stringMin1 | None


class StaticKeyProvider(TypedDict, total=False):
    """Use these settings to set up encryption with a static key provider."""

    KeyFormat: _stringPatternIdentityAZaZ26AZaZ09163 | None
    KeyFormatVersions: _stringPatternDD | None
    StaticKeyValue: _stringPatternAZaZ0932 | None
    Url: _string | None


_listOf__stringMin36Max36Pattern09aFAF809aFAF409aFAF409aFAF409aFAF12 = list[
    _stringMin36Max36Pattern09aFAF809aFAF409aFAF409aFAF409aFAF12
]


class EncryptionContractConfiguration(TypedDict, total=False):
    """Specify the SPEKE version, either v1.0 or v2.0, that MediaConvert uses
    when encrypting your output. For more information, see:
    https://docs.aws.amazon.com/speke/latest/documentation/speke-api-specification.html
    To use SPEKE v1.0: Leave blank. To use SPEKE v2.0: Specify a SPEKE v2.0
    video preset and a SPEKE v2.0 audio preset.
    """

    SpekeAudioPreset: PresetSpeke20Audio | None
    SpekeVideoPreset: PresetSpeke20Video | None


class SpekeKeyProviderCmaf(TypedDict, total=False):
    """If your output group type is CMAF, use these settings when doing DRM
    encryption with a SPEKE-compliant key provider. If your output group
    type is HLS, DASH, or Microsoft Smooth, use the SpekeKeyProvider
    settings instead.
    """

    CertificateArn: _stringPatternArnAwsUsGovAcm | None
    DashSignaledSystemIds: (
        _listOf__stringMin36Max36Pattern09aFAF809aFAF409aFAF409aFAF409aFAF12 | None
    )
    EncryptionContractConfiguration: EncryptionContractConfiguration | None
    HlsSignaledSystemIds: (
        _listOf__stringMin36Max36Pattern09aFAF809aFAF409aFAF409aFAF409aFAF12 | None
    )
    ResourceId: _stringPatternW | None
    Url: _stringPatternHttpsD | None


class CmafEncryptionSettings(TypedDict, total=False):
    """Settings for CMAF encryption"""

    ConstantInitializationVector: _stringMin32Max32Pattern09aFAF32 | None
    EncryptionMethod: CmafEncryptionType | None
    InitializationVectorInManifest: CmafInitializationVectorInManifest | None
    SpekeKeyProvider: SpekeKeyProviderCmaf | None
    StaticKeyProvider: StaticKeyProvider | None
    Type: CmafKeyProviderType | None


class CmafImageBasedTrickPlaySettings(TypedDict, total=False):
    """Tile and thumbnail settings applicable when imageBasedTrickPlay is
    ADVANCED
    """

    IntervalCadence: CmafIntervalCadence | None
    ThumbnailHeight: _integerMin2Max4096 | None
    ThumbnailInterval: _doubleMin0Max2147483647 | None
    ThumbnailWidth: _integerMin8Max4096 | None
    TileHeight: _integerMin1Max2048 | None
    TileWidth: _integerMin1Max512 | None


class S3EncryptionSettings(TypedDict, total=False):
    """Settings for how your job outputs are encrypted as they are uploaded to
    Amazon S3.
    """

    EncryptionType: S3ServerSideEncryptionType | None
    KmsEncryptionContext: _stringPatternAZaZ0902 | None
    KmsKeyArn: (
        _stringPatternArnAwsUsGovCnKmsAZ26EastWestCentralNorthSouthEastWest1912D12KeyAFAF098AFAF094AFAF094AFAF094AFAF0912MrkAFAF0932
        | None
    )


class S3DestinationAccessControl(TypedDict, total=False):
    """Optional. Have MediaConvert automatically apply Amazon S3 access control
    for the outputs in this output group. When you don't use this setting,
    S3 automatically applies the default access control list PRIVATE.
    """

    CannedAcl: S3ObjectCannedAcl | None


class S3DestinationSettings(TypedDict, total=False):
    """Settings associated with S3 destination"""

    AccessControl: S3DestinationAccessControl | None
    Encryption: S3EncryptionSettings | None
    StorageClass: S3StorageClass | None


class DestinationSettings(TypedDict, total=False):
    """Settings associated with the destination. Will vary based on the type of
    destination
    """

    S3Settings: S3DestinationSettings | None


_listOfCmafAdditionalManifest = list[CmafAdditionalManifest]


class CmafGroupSettings(TypedDict, total=False):
    """Settings related to your CMAF output package. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/outputs-file-ABR.html.
    """

    AdditionalManifests: _listOfCmafAdditionalManifest | None
    BaseUrl: _string | None
    ClientCache: CmafClientCache | None
    CodecSpecification: CmafCodecSpecification | None
    DashIFrameTrickPlayNameModifier: _stringMin1Max256 | None
    DashManifestStyle: DashManifestStyle | None
    Destination: _stringPatternS3 | None
    DestinationSettings: DestinationSettings | None
    Encryption: CmafEncryptionSettings | None
    FragmentLength: _integerMin1Max2147483647 | None
    ImageBasedTrickPlay: CmafImageBasedTrickPlay | None
    ImageBasedTrickPlaySettings: CmafImageBasedTrickPlaySettings | None
    ManifestCompression: CmafManifestCompression | None
    ManifestDurationFormat: CmafManifestDurationFormat | None
    MinBufferTime: _integerMin0Max2147483647 | None
    MinFinalSegmentLength: _doubleMin0Max2147483647 | None
    MpdManifestBandwidthType: CmafMpdManifestBandwidthType | None
    MpdProfile: CmafMpdProfile | None
    PtsOffsetHandlingForBFrames: CmafPtsOffsetHandlingForBFrames | None
    SegmentControl: CmafSegmentControl | None
    SegmentLength: _integerMin1Max2147483647 | None
    SegmentLengthControl: CmafSegmentLengthControl | None
    StreamInfResolution: CmafStreamInfResolution | None
    TargetDurationCompatibilityMode: CmafTargetDurationCompatibilityMode | None
    VideoCompositionOffsets: CmafVideoCompositionOffsets | None
    WriteDashManifest: CmafWriteDASHManifest | None
    WriteHlsManifest: CmafWriteHLSManifest | None
    WriteSegmentTimelineInRepresentation: CmafWriteSegmentTimelineInRepresentation | None


class CmfcSettings(TypedDict, total=False):
    """These settings relate to the fragmented MP4 container for the segments
    in your CMAF outputs.
    """

    AudioDuration: CmfcAudioDuration | None
    AudioGroupId: _string | None
    AudioRenditionSets: _string | None
    AudioTrackType: CmfcAudioTrackType | None
    C2paManifest: CmfcC2paManifest | None
    CertificateSecret: _stringMin1Max2048PatternArnAZSecretsmanagerWD12SecretAZAZ09 | None
    DescriptiveVideoServiceFlag: CmfcDescriptiveVideoServiceFlag | None
    IFrameOnlyManifest: CmfcIFrameOnlyManifest | None
    KlvMetadata: CmfcKlvMetadata | None
    ManifestMetadataSignaling: CmfcManifestMetadataSignaling | None
    Scte35Esam: CmfcScte35Esam | None
    Scte35Source: CmfcScte35Source | None
    SigningKmsKey: (
        _stringMin1PatternArnAwsUsGovCnKmsAZ26EastWestCentralNorthSouthEastWest1912D12KeyAFAF098AFAF094AFAF094AFAF094AFAF0912MrkAFAF0932
        | None
    )
    TimedMetadata: CmfcTimedMetadata | None
    TimedMetadataBoxVersion: CmfcTimedMetadataBoxVersion | None
    TimedMetadataSchemeIdUri: _stringMax1000 | None
    TimedMetadataValue: _stringMax1000 | None


class CodecMetadata(TypedDict, total=False):
    """Codec-specific parameters parsed from the video essence headers. This
    information provides detailed technical specifications about how the
    video was encoded, including profile settings, resolution details, and
    color space information that can help you understand the source video
    characteristics and make informed encoding decisions.
    """

    BitDepth: _integer | None
    ChromaSubsampling: _string | None
    CodedFrameRate: FrameRate | None
    ColorPrimaries: ColorPrimaries | None
    Height: _integer | None
    Level: _string | None
    MatrixCoefficients: MatrixCoefficients | None
    Profile: _string | None
    ScanType: _string | None
    TransferCharacteristics: TransferCharacteristics | None
    Width: _integer | None


class ColorConversion3DLUTSetting(TypedDict, total=False):
    """Custom 3D lut settings"""

    FileInput: _stringMin14PatternS3CubeCUBEHttpsCubeCUBE | None
    InputColorSpace: ColorSpace | None
    InputMasteringLuminance: _integerMin0Max2147483647 | None
    OutputColorSpace: ColorSpace | None
    OutputMasteringLuminance: _integerMin0Max2147483647 | None


class Hdr10Metadata(TypedDict, total=False):
    """Use these settings to specify static color calibration metadata, as
    defined by SMPTE ST 2086. These values don't affect the pixel values
    that are encoded in the video stream. They are intended to help the
    downstream video player display content in a way that reflects the
    intentions of the the content creator.
    """

    BluePrimaryX: _integerMin0Max50000 | None
    BluePrimaryY: _integerMin0Max50000 | None
    GreenPrimaryX: _integerMin0Max50000 | None
    GreenPrimaryY: _integerMin0Max50000 | None
    MaxContentLightLevel: _integerMin0Max65535 | None
    MaxFrameAverageLightLevel: _integerMin0Max65535 | None
    MaxLuminance: _integerMin0Max2147483647 | None
    MinLuminance: _integerMin0Max2147483647 | None
    RedPrimaryX: _integerMin0Max50000 | None
    RedPrimaryY: _integerMin0Max50000 | None
    WhitePointX: _integerMin0Max50000 | None
    WhitePointY: _integerMin0Max50000 | None


class ColorCorrector(TypedDict, total=False):
    """Settings for color correction."""

    Brightness: _integerMin1Max100 | None
    ClipLimits: ClipLimits | None
    ColorSpaceConversion: ColorSpaceConversion | None
    Contrast: _integerMin1Max100 | None
    Hdr10Metadata: Hdr10Metadata | None
    HdrToSdrToneMapper: HDRToSDRToneMapper | None
    Hue: _integerMinNegative180Max180 | None
    MaxLuminance: _integerMin0Max2147483647 | None
    SampleRangeConversion: SampleRangeConversion | None
    Saturation: _integerMin1Max100 | None
    SdrReferenceWhiteLevel: _integerMin100Max1000 | None


class VideoProperties(TypedDict, total=False):
    """Details about the media file's video track."""

    BitDepth: _integer | None
    BitRate: _long | None
    CodecMetadata: CodecMetadata | None
    ColorPrimaries: ColorPrimaries | None
    FrameRate: FrameRate | None
    Height: _integer | None
    MatrixCoefficients: MatrixCoefficients | None
    TransferCharacteristics: TransferCharacteristics | None
    Width: _integer | None


class DataProperties(TypedDict, total=False):
    """Details about the media file's data track."""

    LanguageCode: _string | None


class Track(TypedDict, total=False):
    """Details about each track (video, audio, or data) in the media file."""

    AudioProperties: AudioProperties | None
    Codec: Codec | None
    DataProperties: DataProperties | None
    Duration: _double | None
    Index: _integer | None
    TrackType: TrackType | None
    VideoProperties: VideoProperties | None


_listOfTrack = list[Track]


class Container(TypedDict, total=False):
    """The container of your media file. This information helps you understand
    the overall structure and details of your media, including format,
    duration, and track layout.
    """

    Duration: _double | None
    Format: Format | None
    Tracks: _listOfTrack | None


class MxfXavcProfileSettings(TypedDict, total=False):
    """Specify the XAVC profile settings for MXF outputs when you set your MXF
    profile to XAVC.
    """

    DurationMode: MxfXavcDurationMode | None
    MaxAncDataSize: _integerMin0Max2147483647 | None


class MxfSettings(TypedDict, total=False):
    """These settings relate to your MXF output container."""

    AfdSignaling: MxfAfdSignaling | None
    Profile: MxfProfile | None
    XavcProfileSettings: MxfXavcProfileSettings | None


class MpdSettings(TypedDict, total=False):
    """These settings relate to the fragmented MP4 container for the segments
    in your DASH outputs.
    """

    AccessibilityCaptionHints: MpdAccessibilityCaptionHints | None
    AudioDuration: MpdAudioDuration | None
    C2paManifest: MpdC2paManifest | None
    CaptionContainerType: MpdCaptionContainerType | None
    CertificateSecret: _stringMin1Max2048PatternArnAZSecretsmanagerWD12SecretAZAZ09 | None
    KlvMetadata: MpdKlvMetadata | None
    ManifestMetadataSignaling: MpdManifestMetadataSignaling | None
    Scte35Esam: MpdScte35Esam | None
    Scte35Source: MpdScte35Source | None
    SigningKmsKey: (
        _stringMin1PatternArnAwsUsGovCnKmsAZ26EastWestCentralNorthSouthEastWest1912D12KeyAFAF098AFAF094AFAF094AFAF094AFAF0912MrkAFAF0932
        | None
    )
    TimedMetadata: MpdTimedMetadata | None
    TimedMetadataBoxVersion: MpdTimedMetadataBoxVersion | None
    TimedMetadataSchemeIdUri: _stringMax1000 | None
    TimedMetadataValue: _stringMax1000 | None


class Mp4Settings(TypedDict, total=False):
    """These settings relate to your MP4 output container. You can create audio
    only outputs with this container. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/supported-codecs-containers-audio-only.html#output-codecs-and-containers-supported-for-audio-only.
    """

    AudioDuration: CmfcAudioDuration | None
    C2paManifest: Mp4C2paManifest | None
    CertificateSecret: _stringMin1Max2048PatternArnAZSecretsmanagerWD12SecretAZAZ09 | None
    CslgAtom: Mp4CslgAtom | None
    CttsVersion: _integerMin0Max1 | None
    FreeSpaceBox: Mp4FreeSpaceBox | None
    MoovPlacement: Mp4MoovPlacement | None
    Mp4MajorBrand: _string | None
    SigningKmsKey: (
        _stringMin1PatternArnAwsUsGovCnKmsAZ26EastWestCentralNorthSouthEastWest1912D12KeyAFAF098AFAF094AFAF094AFAF094AFAF0912MrkAFAF0932
        | None
    )


class MovSettings(TypedDict, total=False):
    """These settings relate to your QuickTime MOV output container."""

    ClapAtom: MovClapAtom | None
    CslgAtom: MovCslgAtom | None
    Mpeg2FourCCControl: MovMpeg2FourCCControl | None
    PaddingControl: MovPaddingControl | None
    Reference: MovReference | None


_listOf__integerMin32Max8182 = list[_integerMin32Max8182]


class M3u8Settings(TypedDict, total=False):
    """These settings relate to the MPEG-2 transport stream (MPEG2-TS)
    container for the MPEG2-TS segments in your HLS outputs.
    """

    AudioDuration: M3u8AudioDuration | None
    AudioFramesPerPes: _integerMin0Max2147483647 | None
    AudioPids: _listOf__integerMin32Max8182 | None
    AudioPtsOffsetDelta: _integerMinNegative10000Max10000 | None
    DataPTSControl: M3u8DataPtsControl | None
    MaxPcrInterval: _integerMin0Max500 | None
    NielsenId3: M3u8NielsenId3 | None
    PatInterval: _integerMin0Max1000 | None
    PcrControl: M3u8PcrControl | None
    PcrPid: _integerMin32Max8182 | None
    PmtInterval: _integerMin0Max1000 | None
    PmtPid: _integerMin32Max8182 | None
    PrivateMetadataPid: _integerMin32Max8182 | None
    ProgramNumber: _integerMin0Max65535 | None
    PtsOffset: _integerMin0Max3600 | None
    PtsOffsetMode: TsPtsOffset | None
    Scte35Pid: _integerMin32Max8182 | None
    Scte35Source: M3u8Scte35Source | None
    TimedMetadata: TimedMetadata | None
    TimedMetadataPid: _integerMin32Max8182 | None
    TransportStreamId: _integerMin0Max65535 | None
    VideoPid: _integerMin32Max8182 | None


class M2tsScte35Esam(TypedDict, total=False):
    """Settings for SCTE-35 signals from ESAM. Include this in your job
    settings to put SCTE-35 markers in your HLS and transport stream outputs
    at the insertion points that you specify in an ESAM XML document.
    Provide the document in the setting SCC XML.
    """

    Scte35EsamPid: _integerMin32Max8182 | None


class DvbTdtSettings(TypedDict, total=False):
    """Use these settings to insert a DVB Time and Date Table (TDT) in the
    transport stream of this output.
    """

    TdtInterval: _integerMin1000Max30000 | None


class DvbSdtSettings(TypedDict, total=False):
    """Use these settings to insert a DVB Service Description Table (SDT) in
    the transport stream of this output.
    """

    OutputSdt: OutputSdt | None
    SdtInterval: _integerMin25Max2000 | None
    ServiceName: _stringMin1Max256 | None
    ServiceProviderName: _stringMin1Max256 | None


class DvbNitSettings(TypedDict, total=False):
    """Use these settings to insert a DVB Network Information Table (NIT) in
    the transport stream of this output.
    """

    NetworkId: _integerMin0Max65535 | None
    NetworkName: _stringMin1Max256 | None
    NitInterval: _integerMin25Max10000 | None


class M2tsSettings(TypedDict, total=False):
    """MPEG-2 TS container settings. These apply to outputs in a File output
    group when the output's container is MPEG-2 Transport Stream (M2TS). In
    these assets, data is organized by the program map table (PMT). Each
    transport stream program contains subsets of data, including audio,
    video, and metadata. Each of these subsets of data has a numerical label
    called a packet identifier (PID). Each transport stream program
    corresponds to one MediaConvert output. The PMT lists the types of data
    in a program along with their PID. Downstream systems and players use
    the program map table to look up the PID for each type of data it
    accesses and then uses the PIDs to locate specific data within the
    asset.
    """

    AudioBufferModel: M2tsAudioBufferModel | None
    AudioDuration: M2tsAudioDuration | None
    AudioFramesPerPes: _integerMin0Max2147483647 | None
    AudioPids: _listOf__integerMin32Max8182 | None
    AudioPtsOffsetDelta: _integerMinNegative10000Max10000 | None
    Bitrate: _integerMin0Max2147483647 | None
    BufferModel: M2tsBufferModel | None
    DataPTSControl: M2tsDataPtsControl | None
    DvbNitSettings: DvbNitSettings | None
    DvbSdtSettings: DvbSdtSettings | None
    DvbSubPids: _listOf__integerMin32Max8182 | None
    DvbTdtSettings: DvbTdtSettings | None
    DvbTeletextPid: _integerMin32Max8182 | None
    EbpAudioInterval: M2tsEbpAudioInterval | None
    EbpPlacement: M2tsEbpPlacement | None
    EsRateInPes: M2tsEsRateInPes | None
    ForceTsVideoEbpOrder: M2tsForceTsVideoEbpOrder | None
    FragmentTime: _doubleMin0 | None
    KlvMetadata: M2tsKlvMetadata | None
    MaxPcrInterval: _integerMin0Max500 | None
    MinEbpInterval: _integerMin0Max10000 | None
    NielsenId3: M2tsNielsenId3 | None
    NullPacketBitrate: _doubleMin0 | None
    PatInterval: _integerMin0Max1000 | None
    PcrControl: M2tsPcrControl | None
    PcrPid: _integerMin32Max8182 | None
    PmtInterval: _integerMin0Max1000 | None
    PmtPid: _integerMin32Max8182 | None
    PreventBufferUnderflow: M2tsPreventBufferUnderflow | None
    PrivateMetadataPid: _integerMin32Max8182 | None
    ProgramNumber: _integerMin0Max65535 | None
    PtsOffset: _integerMin0Max3600 | None
    PtsOffsetMode: TsPtsOffset | None
    RateMode: M2tsRateMode | None
    Scte35Esam: M2tsScte35Esam | None
    Scte35Pid: _integerMin32Max8182 | None
    Scte35Source: M2tsScte35Source | None
    SegmentationMarkers: M2tsSegmentationMarkers | None
    SegmentationStyle: M2tsSegmentationStyle | None
    SegmentationTime: _doubleMin0 | None
    TimedMetadataPid: _integerMin32Max8182 | None
    TransportStreamId: _integerMin0Max65535 | None
    VideoPid: _integerMin32Max8182 | None


class F4vSettings(TypedDict, total=False):
    """Settings for F4v container"""

    MoovPlacement: F4vMoovPlacement | None


class ContainerSettings(TypedDict, total=False):
    """Container specific settings."""

    CmfcSettings: CmfcSettings | None
    Container: ContainerType | None
    F4vSettings: F4vSettings | None
    M2tsSettings: M2tsSettings | None
    M3u8Settings: M3u8Settings | None
    MovSettings: MovSettings | None
    Mp4Settings: Mp4Settings | None
    MpdSettings: MpdSettings | None
    MxfSettings: MxfSettings | None


_mapOf__string = dict[_string, _string]


class Id3Insertion(TypedDict, total=False):
    """To insert ID3 tags in your output, specify two values. Use ID3 tag to
    specify the base 64 encoded string and use Timecode to specify the time
    when the tag should be inserted. To insert multiple ID3 tags in your
    output, create multiple instances of ID3 insertion.
    """

    Id3: _stringPatternAZaZ0902 | None
    Timecode: _stringPattern010920405090509092 | None


_listOfId3Insertion = list[Id3Insertion]


class TimedMetadataInsertion(TypedDict, total=False):
    """Insert user-defined custom ID3 metadata at timecodes that you specify.
    In each output that you want to include this metadata, you must set ID3
    metadata to Passthrough.
    """

    Id3Insertions: _listOfId3Insertion | None


class TimecodeConfig(TypedDict, total=False):
    """These settings control how the service handles timecodes throughout the
    job. These settings don't affect input clipping.
    """

    Anchor: _stringPattern010920405090509092 | None
    Source: TimecodeSource | None
    Start: _stringPattern010920405090509092 | None
    TimestampOffset: _stringPattern0940191020191209301 | None


class TimecodeBurnin(TypedDict, total=False):
    """Settings for burning the output timecode and specified prefix into the
    output.
    """

    FontSize: _integerMin10Max48 | None
    Position: TimecodeBurninPosition | None
    Prefix: _stringPattern | None


class NexGuardFileMarkerSettings(TypedDict, total=False):
    """For forensic video watermarking, MediaConvert supports Nagra NexGuard
    File Marker watermarking. MediaConvert supports both PreRelease Content
    (NGPR/G2) and OTT Streaming workflows.
    """

    License: _stringMin1Max100000 | None
    Payload: _integerMin0Max4194303 | None
    Preset: _stringMin1Max256 | None
    Strength: WatermarkingStrength | None


class PartnerWatermarking(TypedDict, total=False):
    """If you work with a third party video watermarking partner, use the group
    of settings that correspond with your watermarking partner to include
    watermarks in your output.
    """

    NexguardFileMarkerSettings: NexGuardFileMarkerSettings | None


class NoiseReducerTemporalFilterSettings(TypedDict, total=False):
    """Noise reducer filter settings for temporal filter."""

    AggressiveMode: _integerMin0Max4 | None
    PostTemporalSharpening: NoiseFilterPostTemporalSharpening | None
    PostTemporalSharpeningStrength: NoiseFilterPostTemporalSharpeningStrength | None
    Speed: _integerMinNegative1Max3 | None
    Strength: _integerMin0Max16 | None


class NoiseReducerSpatialFilterSettings(TypedDict, total=False):
    """Noise reducer filter settings for spatial filter."""

    PostFilterSharpenStrength: _integerMin0Max3 | None
    Speed: _integerMinNegative2Max3 | None
    Strength: _integerMin0Max16 | None


class NoiseReducerFilterSettings(TypedDict, total=False):
    """Settings for a noise reducer filter"""

    Strength: _integerMin0Max3 | None


class NoiseReducer(TypedDict, total=False):
    """Enable the Noise reducer feature to remove noise from your video output
    if necessary. Enable or disable this feature for each output
    individually. This setting is disabled by default. When you enable Noise
    reducer, you must also select a value for Noise reducer filter. For AVC
    outputs, when you include Noise reducer, you cannot include the
    Bandwidth reduction filter.
    """

    Filter: NoiseReducerFilter | None
    FilterSettings: NoiseReducerFilterSettings | None
    SpatialFilterSettings: NoiseReducerSpatialFilterSettings | None
    TemporalFilterSettings: NoiseReducerTemporalFilterSettings | None


class InsertableImage(TypedDict, total=False):
    """These settings apply to a specific graphic overlay. You can include
    multiple overlays in your job.
    """

    Duration: _integerMin0Max2147483647 | None
    FadeIn: _integerMin0Max2147483647 | None
    FadeOut: _integerMin0Max2147483647 | None
    Height: _integerMin0Max2147483647 | None
    ImageInserterInput: _stringMin14PatternS3BmpBMPPngPNGTgaTGAHttpsBmpBMPPngPNGTgaTGA | None
    ImageX: _integerMin0Max2147483647 | None
    ImageY: _integerMin0Max2147483647 | None
    Layer: _integerMin0Max99 | None
    Opacity: _integerMin0Max100 | None
    StartTime: _stringPattern01D20305D205D | None
    Width: _integerMin0Max2147483647 | None


_listOfInsertableImage = list[InsertableImage]


class ImageInserter(TypedDict, total=False):
    """Use the image inserter feature to include a graphic overlay on your
    video. Enable or disable this feature for each input or output
    individually. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/graphic-overlay.html.
    This setting is disabled by default.
    """

    InsertableImages: _listOfInsertableImage | None
    SdrReferenceWhiteLevel: _integerMin100Max1000 | None


class Hdr10Plus(TypedDict, total=False):
    """Setting for HDR10+ metadata insertion"""

    MasteringMonitorNits: _integerMin0Max4000 | None
    TargetMonitorNits: _integerMin0Max4000 | None


class DolbyVisionLevel6Metadata(TypedDict, total=False):
    """Use these settings when you set DolbyVisionLevel6Mode to SPECIFY to
    override the MaxCLL and MaxFALL values in your input with new values.
    """

    MaxCll: _integerMin0Max65535 | None
    MaxFall: _integerMin0Max65535 | None


class DolbyVision(TypedDict, total=False):
    """Create Dolby Vision Profile 5 or Profile 8.1 compatible video output."""

    L6Metadata: DolbyVisionLevel6Metadata | None
    L6Mode: DolbyVisionLevel6Mode | None
    Mapping: DolbyVisionMapping | None
    Profile: DolbyVisionProfile | None


class Deinterlacer(TypedDict, total=False):
    """Settings for deinterlacer"""

    Algorithm: DeinterlaceAlgorithm | None
    Control: DeinterlacerControl | None
    Mode: DeinterlacerMode | None


class VideoPreprocessor(TypedDict, total=False):
    """Find additional transcoding features under Preprocessors. Enable the
    features at each output individually. These features are disabled by
    default.
    """

    ColorCorrector: ColorCorrector | None
    Deinterlacer: Deinterlacer | None
    DolbyVision: DolbyVision | None
    Hdr10Plus: Hdr10Plus | None
    ImageInserter: ImageInserter | None
    NoiseReducer: NoiseReducer | None
    PartnerWatermarking: PartnerWatermarking | None
    TimecodeBurnin: TimecodeBurnin | None


class Rectangle(TypedDict, total=False):
    """Use Rectangle to identify a specific area of the video frame."""

    Height: _integerMin2Max2147483647 | None
    Width: _integerMin2Max2147483647 | None
    X: _integerMin0Max2147483647 | None
    Y: _integerMin0Max2147483647 | None


class XavcHdProfileSettings(TypedDict, total=False):
    """Required when you set Profile to the value XAVC_HD."""

    BitrateClass: XavcHdProfileBitrateClass | None
    FlickerAdaptiveQuantization: XavcFlickerAdaptiveQuantization | None
    GopBReference: XavcGopBReference | None
    GopClosedCadence: _integerMin0Max2147483647 | None
    HrdBufferSize: _integerMin0Max1152000000 | None
    InterlaceMode: XavcInterlaceMode | None
    QualityTuningLevel: XavcHdProfileQualityTuningLevel | None
    Slices: _integerMin4Max12 | None
    Telecine: XavcHdProfileTelecine | None


class XavcHdIntraCbgProfileSettings(TypedDict, total=False):
    """Required when you set Profile to the value XAVC_HD_INTRA_CBG."""

    XavcClass: XavcHdIntraCbgProfileClass | None


class Xavc4kProfileSettings(TypedDict, total=False):
    """Required when you set Profile to the value XAVC_4K."""

    BitrateClass: Xavc4kProfileBitrateClass | None
    CodecProfile: Xavc4kProfileCodecProfile | None
    FlickerAdaptiveQuantization: XavcFlickerAdaptiveQuantization | None
    GopBReference: XavcGopBReference | None
    GopClosedCadence: _integerMin0Max2147483647 | None
    HrdBufferSize: _integerMin0Max1152000000 | None
    QualityTuningLevel: Xavc4kProfileQualityTuningLevel | None
    Slices: _integerMin8Max12 | None


class Xavc4kIntraVbrProfileSettings(TypedDict, total=False):
    """Required when you set Profile to the value XAVC_4K_INTRA_VBR."""

    XavcClass: Xavc4kIntraVbrProfileClass | None


class Xavc4kIntraCbgProfileSettings(TypedDict, total=False):
    """Required when you set Profile to the value XAVC_4K_INTRA_CBG."""

    XavcClass: Xavc4kIntraCbgProfileClass | None


class XavcSettings(TypedDict, total=False):
    """Required when you set Codec to the value XAVC."""

    AdaptiveQuantization: XavcAdaptiveQuantization | None
    EntropyEncoding: XavcEntropyEncoding | None
    FramerateControl: XavcFramerateControl | None
    FramerateConversionAlgorithm: XavcFramerateConversionAlgorithm | None
    FramerateDenominator: _integerMin1Max1001 | None
    FramerateNumerator: _integerMin24Max60000 | None
    PerFrameMetrics: _listOfFrameMetricType | None
    Profile: XavcProfile | None
    SlowPal: XavcSlowPal | None
    Softness: _integerMin0Max128 | None
    SpatialAdaptiveQuantization: XavcSpatialAdaptiveQuantization | None
    TemporalAdaptiveQuantization: XavcTemporalAdaptiveQuantization | None
    Xavc4kIntraCbgProfileSettings: Xavc4kIntraCbgProfileSettings | None
    Xavc4kIntraVbrProfileSettings: Xavc4kIntraVbrProfileSettings | None
    Xavc4kProfileSettings: Xavc4kProfileSettings | None
    XavcHdIntraCbgProfileSettings: XavcHdIntraCbgProfileSettings | None
    XavcHdProfileSettings: XavcHdProfileSettings | None


class Vp9Settings(TypedDict, total=False):
    """Required when you set Codec to the value VP9."""

    Bitrate: _integerMin1000Max480000000 | None
    FramerateControl: Vp9FramerateControl | None
    FramerateConversionAlgorithm: Vp9FramerateConversionAlgorithm | None
    FramerateDenominator: _integerMin1Max2147483647 | None
    FramerateNumerator: _integerMin1Max2147483647 | None
    GopSize: _doubleMin0 | None
    HrdBufferSize: _integerMin0Max47185920 | None
    MaxBitrate: _integerMin1000Max480000000 | None
    ParControl: Vp9ParControl | None
    ParDenominator: _integerMin1Max2147483647 | None
    ParNumerator: _integerMin1Max2147483647 | None
    QualityTuningLevel: Vp9QualityTuningLevel | None
    RateControlMode: Vp9RateControlMode | None


class Vp8Settings(TypedDict, total=False):
    """Required when you set Codec to the value VP8."""

    Bitrate: _integerMin1000Max1152000000 | None
    FramerateControl: Vp8FramerateControl | None
    FramerateConversionAlgorithm: Vp8FramerateConversionAlgorithm | None
    FramerateDenominator: _integerMin1Max2147483647 | None
    FramerateNumerator: _integerMin1Max2147483647 | None
    GopSize: _doubleMin0 | None
    HrdBufferSize: _integerMin0Max47185920 | None
    MaxBitrate: _integerMin1000Max1152000000 | None
    ParControl: Vp8ParControl | None
    ParDenominator: _integerMin1Max2147483647 | None
    ParNumerator: _integerMin1Max2147483647 | None
    QualityTuningLevel: Vp8QualityTuningLevel | None
    RateControlMode: Vp8RateControlMode | None


class Vc3Settings(TypedDict, total=False):
    """Required when you set Codec to the value VC3"""

    FramerateControl: Vc3FramerateControl | None
    FramerateConversionAlgorithm: Vc3FramerateConversionAlgorithm | None
    FramerateDenominator: _integerMin1Max1001 | None
    FramerateNumerator: _integerMin24Max60000 | None
    InterlaceMode: Vc3InterlaceMode | None
    ScanTypeConversionMode: Vc3ScanTypeConversionMode | None
    SlowPal: Vc3SlowPal | None
    Telecine: Vc3Telecine | None
    Vc3Class: Vc3Class | None


class UncompressedSettings(TypedDict, total=False):
    """Required when you set Codec, under VideoDescription>CodecSettings to the
    value UNCOMPRESSED.
    """

    Fourcc: UncompressedFourcc | None
    FramerateControl: UncompressedFramerateControl | None
    FramerateConversionAlgorithm: UncompressedFramerateConversionAlgorithm | None
    FramerateDenominator: _integerMin1Max2147483647 | None
    FramerateNumerator: _integerMin1Max2147483647 | None
    InterlaceMode: UncompressedInterlaceMode | None
    ScanTypeConversionMode: UncompressedScanTypeConversionMode | None
    SlowPal: UncompressedSlowPal | None
    Telecine: UncompressedTelecine | None


class ProresSettings(TypedDict, total=False):
    """Required when you set Codec to the value PRORES."""

    ChromaSampling: ProresChromaSampling | None
    CodecProfile: ProresCodecProfile | None
    FramerateControl: ProresFramerateControl | None
    FramerateConversionAlgorithm: ProresFramerateConversionAlgorithm | None
    FramerateDenominator: _integerMin1Max2147483647 | None
    FramerateNumerator: _integerMin1Max2147483647 | None
    InterlaceMode: ProresInterlaceMode | None
    ParControl: ProresParControl | None
    ParDenominator: _integerMin1Max2147483647 | None
    ParNumerator: _integerMin1Max2147483647 | None
    PerFrameMetrics: _listOfFrameMetricType | None
    ScanTypeConversionMode: ProresScanTypeConversionMode | None
    SlowPal: ProresSlowPal | None
    Telecine: ProresTelecine | None


class PassthroughSettings(TypedDict, total=False):
    """Optional settings when you set Codec to the value Passthrough."""

    FrameControl: FrameControl | None
    VideoSelectorMode: VideoSelectorMode | None


class Mpeg2Settings(TypedDict, total=False):
    """Required when you set Codec to the value MPEG2."""

    AdaptiveQuantization: Mpeg2AdaptiveQuantization | None
    Bitrate: _integerMin1000Max288000000 | None
    CodecLevel: Mpeg2CodecLevel | None
    CodecProfile: Mpeg2CodecProfile | None
    DynamicSubGop: Mpeg2DynamicSubGop | None
    FramerateControl: Mpeg2FramerateControl | None
    FramerateConversionAlgorithm: Mpeg2FramerateConversionAlgorithm | None
    FramerateDenominator: _integerMin1Max1001 | None
    FramerateNumerator: _integerMin24Max60000 | None
    GopClosedCadence: _integerMin0Max2147483647 | None
    GopSize: _doubleMin0 | None
    GopSizeUnits: Mpeg2GopSizeUnits | None
    HrdBufferFinalFillPercentage: _integerMin0Max100 | None
    HrdBufferInitialFillPercentage: _integerMin0Max100 | None
    HrdBufferSize: _integerMin0Max47185920 | None
    InterlaceMode: Mpeg2InterlaceMode | None
    IntraDcPrecision: Mpeg2IntraDcPrecision | None
    MaxBitrate: _integerMin1000Max300000000 | None
    MinIInterval: _integerMin0Max30 | None
    NumberBFramesBetweenReferenceFrames: _integerMin0Max7 | None
    ParControl: Mpeg2ParControl | None
    ParDenominator: _integerMin1Max2147483647 | None
    ParNumerator: _integerMin1Max2147483647 | None
    PerFrameMetrics: _listOfFrameMetricType | None
    QualityTuningLevel: Mpeg2QualityTuningLevel | None
    RateControlMode: Mpeg2RateControlMode | None
    ScanTypeConversionMode: Mpeg2ScanTypeConversionMode | None
    SceneChangeDetect: Mpeg2SceneChangeDetect | None
    SlowPal: Mpeg2SlowPal | None
    Softness: _integerMin0Max128 | None
    SpatialAdaptiveQuantization: Mpeg2SpatialAdaptiveQuantization | None
    Syntax: Mpeg2Syntax | None
    Telecine: Mpeg2Telecine | None
    TemporalAdaptiveQuantization: Mpeg2TemporalAdaptiveQuantization | None


class H265QvbrSettings(TypedDict, total=False):
    """Settings for quality-defined variable bitrate encoding with the H.265
    codec. Use these settings only when you set QVBR for Rate control mode.
    """

    MaxAverageBitrate: _integerMin1000Max1466400000 | None
    QvbrQualityLevel: _integerMin1Max10 | None
    QvbrQualityLevelFineTune: _doubleMin0Max1 | None


class H265Settings(TypedDict, total=False):
    """Settings for H265 codec"""

    AdaptiveQuantization: H265AdaptiveQuantization | None
    AlternateTransferFunctionSei: H265AlternateTransferFunctionSei | None
    BandwidthReductionFilter: BandwidthReductionFilter | None
    Bitrate: _integerMin1000Max1466400000 | None
    CodecLevel: H265CodecLevel | None
    CodecProfile: H265CodecProfile | None
    Deblocking: H265Deblocking | None
    DynamicSubGop: H265DynamicSubGop | None
    EndOfStreamMarkers: H265EndOfStreamMarkers | None
    FlickerAdaptiveQuantization: H265FlickerAdaptiveQuantization | None
    FramerateControl: H265FramerateControl | None
    FramerateConversionAlgorithm: H265FramerateConversionAlgorithm | None
    FramerateDenominator: _integerMin1Max2147483647 | None
    FramerateNumerator: _integerMin1Max2147483647 | None
    GopBReference: H265GopBReference | None
    GopClosedCadence: _integerMin0Max2147483647 | None
    GopSize: _doubleMin0 | None
    GopSizeUnits: H265GopSizeUnits | None
    HrdBufferFinalFillPercentage: _integerMin0Max100 | None
    HrdBufferInitialFillPercentage: _integerMin0Max100 | None
    HrdBufferSize: _integerMin0Max1466400000 | None
    InterlaceMode: H265InterlaceMode | None
    MaxBitrate: _integerMin1000Max1466400000 | None
    MinIInterval: _integerMin0Max30 | None
    MvOverPictureBoundaries: H265MvOverPictureBoundaries | None
    MvTemporalPredictor: H265MvTemporalPredictor | None
    NumberBFramesBetweenReferenceFrames: _integerMin0Max7 | None
    NumberReferenceFrames: _integerMin1Max6 | None
    ParControl: H265ParControl | None
    ParDenominator: _integerMin1Max2147483647 | None
    ParNumerator: _integerMin1Max2147483647 | None
    PerFrameMetrics: _listOfFrameMetricType | None
    QualityTuningLevel: H265QualityTuningLevel | None
    QvbrSettings: H265QvbrSettings | None
    RateControlMode: H265RateControlMode | None
    SampleAdaptiveOffsetFilterMode: H265SampleAdaptiveOffsetFilterMode | None
    ScanTypeConversionMode: H265ScanTypeConversionMode | None
    SceneChangeDetect: H265SceneChangeDetect | None
    Slices: _integerMin1Max32 | None
    SlowPal: H265SlowPal | None
    SpatialAdaptiveQuantization: H265SpatialAdaptiveQuantization | None
    Telecine: H265Telecine | None
    TemporalAdaptiveQuantization: H265TemporalAdaptiveQuantization | None
    TemporalIds: H265TemporalIds | None
    TileHeight: _integerMin64Max2160 | None
    TilePadding: H265TilePadding | None
    TileWidth: _integerMin256Max3840 | None
    Tiles: H265Tiles | None
    TreeBlockSize: H265TreeBlockSize | None
    UnregisteredSeiTimecode: H265UnregisteredSeiTimecode | None
    WriteMp4PackagingType: H265WriteMp4PackagingType | None


class H264QvbrSettings(TypedDict, total=False):
    """Settings for quality-defined variable bitrate encoding with the H.264
    codec. Use these settings only when you set QVBR for Rate control mode.
    """

    MaxAverageBitrate: _integerMin1000Max1152000000 | None
    QvbrQualityLevel: _integerMin1Max10 | None
    QvbrQualityLevelFineTune: _doubleMin0Max1 | None


class H264Settings(TypedDict, total=False):
    """Required when you set Codec to the value H_264."""

    AdaptiveQuantization: H264AdaptiveQuantization | None
    BandwidthReductionFilter: BandwidthReductionFilter | None
    Bitrate: _integerMin1000Max1152000000 | None
    CodecLevel: H264CodecLevel | None
    CodecProfile: H264CodecProfile | None
    DynamicSubGop: H264DynamicSubGop | None
    EndOfStreamMarkers: H264EndOfStreamMarkers | None
    EntropyEncoding: H264EntropyEncoding | None
    FieldEncoding: H264FieldEncoding | None
    FlickerAdaptiveQuantization: H264FlickerAdaptiveQuantization | None
    FramerateControl: H264FramerateControl | None
    FramerateConversionAlgorithm: H264FramerateConversionAlgorithm | None
    FramerateDenominator: _integerMin1Max2147483647 | None
    FramerateNumerator: _integerMin1Max2147483647 | None
    GopBReference: H264GopBReference | None
    GopClosedCadence: _integerMin0Max2147483647 | None
    GopSize: _doubleMin0 | None
    GopSizeUnits: H264GopSizeUnits | None
    HrdBufferFinalFillPercentage: _integerMin0Max100 | None
    HrdBufferInitialFillPercentage: _integerMin0Max100 | None
    HrdBufferSize: _integerMin0Max1152000000 | None
    InterlaceMode: H264InterlaceMode | None
    MaxBitrate: _integerMin1000Max1152000000 | None
    MinIInterval: _integerMin0Max30 | None
    NumberBFramesBetweenReferenceFrames: _integerMin0Max7 | None
    NumberReferenceFrames: _integerMin1Max6 | None
    ParControl: H264ParControl | None
    ParDenominator: _integerMin1Max2147483647 | None
    ParNumerator: _integerMin1Max2147483647 | None
    PerFrameMetrics: _listOfFrameMetricType | None
    QualityTuningLevel: H264QualityTuningLevel | None
    QvbrSettings: H264QvbrSettings | None
    RateControlMode: H264RateControlMode | None
    RepeatPps: H264RepeatPps | None
    SaliencyAwareEncoding: H264SaliencyAwareEncoding | None
    ScanTypeConversionMode: H264ScanTypeConversionMode | None
    SceneChangeDetect: H264SceneChangeDetect | None
    Slices: _integerMin1Max32 | None
    SlowPal: H264SlowPal | None
    Softness: _integerMin0Max128 | None
    SpatialAdaptiveQuantization: H264SpatialAdaptiveQuantization | None
    Syntax: H264Syntax | None
    Telecine: H264Telecine | None
    TemporalAdaptiveQuantization: H264TemporalAdaptiveQuantization | None
    UnregisteredSeiTimecode: H264UnregisteredSeiTimecode | None
    WriteMp4PackagingType: H264WriteMp4PackagingType | None


class GifSettings(TypedDict, total=False):
    """Required when you set (Codec) under (VideoDescription)>(CodecSettings)
    to the value GIF
    """

    FramerateControl: GifFramerateControl | None
    FramerateConversionAlgorithm: GifFramerateConversionAlgorithm | None
    FramerateDenominator: _integerMin1Max2147483647 | None
    FramerateNumerator: _integerMin1Max2147483647 | None


class FrameCaptureSettings(TypedDict, total=False):
    """Required when you set Codec to the value FRAME_CAPTURE."""

    FramerateDenominator: _integerMin1Max2147483647 | None
    FramerateNumerator: _integerMin1Max2147483647 | None
    MaxCaptures: _integerMin1Max10000000 | None
    Quality: _integerMin1Max100 | None


class VideoCodecSettings(TypedDict, total=False):
    """Video codec settings contains the group of settings related to video
    encoding. The settings in this group vary depending on the value that
    you choose for Video codec. For each codec enum that you choose, define
    the corresponding settings object. The following lists the codec enum,
    settings object pairs. \\* AV1, Av1Settings \\* AVC_INTRA,
    AvcIntraSettings \\* FRAME_CAPTURE, FrameCaptureSettings \\* GIF,
    GifSettings \\* H_264, H264Settings \\* H_265, H265Settings \\* MPEG2,
    Mpeg2Settings \\* PRORES, ProresSettings \\* UNCOMPRESSED,
    UncompressedSettings \\* VC3, Vc3Settings \\* VP8, Vp8Settings \\* VP9,
    Vp9Settings \\* XAVC, XavcSettings
    """

    Av1Settings: Av1Settings | None
    AvcIntraSettings: AvcIntraSettings | None
    Codec: VideoCodec | None
    FrameCaptureSettings: FrameCaptureSettings | None
    GifSettings: GifSettings | None
    H264Settings: H264Settings | None
    H265Settings: H265Settings | None
    Mpeg2Settings: Mpeg2Settings | None
    PassthroughSettings: PassthroughSettings | None
    ProresSettings: ProresSettings | None
    UncompressedSettings: UncompressedSettings | None
    Vc3Settings: Vc3Settings | None
    Vp8Settings: Vp8Settings | None
    Vp9Settings: Vp9Settings | None
    XavcSettings: XavcSettings | None


class VideoDescription(TypedDict, total=False):
    """Settings related to video encoding of your output. The specific video
    settings depend on the video codec that you choose.
    """

    AfdSignaling: AfdSignaling | None
    AntiAlias: AntiAlias | None
    ChromaPositionMode: ChromaPositionMode | None
    CodecSettings: VideoCodecSettings | None
    ColorMetadata: ColorMetadata | None
    Crop: Rectangle | None
    DropFrameTimecode: DropFrameTimecode | None
    FixedAfd: _integerMin0Max15 | None
    Height: _integerMin32Max8192 | None
    Position: Rectangle | None
    RespondToAfd: RespondToAfd | None
    ScalingBehavior: ScalingBehavior | None
    Sharpness: _integerMin0Max100 | None
    TimecodeInsertion: VideoTimecodeInsertion | None
    TimecodeTrack: TimecodeTrack | None
    VideoPreprocessors: VideoPreprocessor | None
    Width: _integerMin32Max8192 | None


class HlsSettings(TypedDict, total=False):
    """Settings for HLS output groups"""

    AudioGroupId: _string | None
    AudioOnlyContainer: HlsAudioOnlyContainer | None
    AudioRenditionSets: _string | None
    AudioTrackType: HlsAudioTrackType | None
    DescriptiveVideoServiceFlag: HlsDescriptiveVideoServiceFlag | None
    IFrameOnlyManifest: HlsIFrameOnlyManifest | None
    SegmentModifier: _string | None


class OutputSettings(TypedDict, total=False):
    """Specific settings for this type of output."""

    HlsSettings: HlsSettings | None


_listOfCaptionDescription = list[CaptionDescription]
_listOfAudioDescription = list[AudioDescription]


class Output(TypedDict, total=False):
    """Each output in your job is a collection of settings that describes how
    you want MediaConvert to encode a single output file or stream. For more
    information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/create-outputs.html.
    """

    AudioDescriptions: _listOfAudioDescription | None
    CaptionDescriptions: _listOfCaptionDescription | None
    ContainerSettings: ContainerSettings | None
    Extension: _stringMax256 | None
    NameModifier: _stringMin1Max256 | None
    OutputSettings: OutputSettings | None
    Preset: _stringMin0 | None
    VideoDescription: VideoDescription | None


_listOfOutput = list[Output]
_listOf__stringPattern09aFAF809aFAF409aFAF409aFAF409aFAF12 = list[
    _stringPattern09aFAF809aFAF409aFAF409aFAF409aFAF12
]


class SpekeKeyProvider(TypedDict, total=False):
    """If your output group type is HLS, DASH, or Microsoft Smooth, use these
    settings when doing DRM encryption with a SPEKE-compliant key provider.
    If your output group type is CMAF, use the SpekeKeyProviderCmaf settings
    instead.
    """

    CertificateArn: _stringPatternArnAwsUsGovAcm | None
    EncryptionContractConfiguration: EncryptionContractConfiguration | None
    ResourceId: _string | None
    SystemIds: _listOf__stringPattern09aFAF809aFAF409aFAF409aFAF409aFAF12 | None
    Url: _stringPatternHttpsD | None


class MsSmoothEncryptionSettings(TypedDict, total=False):
    """If you are using DRM, set DRM System to specify the value
    SpekeKeyProvider.
    """

    SpekeKeyProvider: SpekeKeyProvider | None


class MsSmoothAdditionalManifest(TypedDict, total=False):
    """Specify the details for each additional Microsoft Smooth Streaming
    manifest that you want the service to generate for this output group.
    Each manifest can reference a different subset of outputs in the group.
    """

    ManifestNameModifier: _stringMin1 | None
    SelectedOutputs: _listOf__stringMin1 | None


_listOfMsSmoothAdditionalManifest = list[MsSmoothAdditionalManifest]


class MsSmoothGroupSettings(TypedDict, total=False):
    """Settings related to your Microsoft Smooth Streaming output package. For
    more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/outputs-file-ABR.html.
    """

    AdditionalManifests: _listOfMsSmoothAdditionalManifest | None
    AudioDeduplication: MsSmoothAudioDeduplication | None
    Destination: _stringPatternS3 | None
    DestinationSettings: DestinationSettings | None
    Encryption: MsSmoothEncryptionSettings | None
    FragmentLength: _integerMin1Max2147483647 | None
    FragmentLengthControl: MsSmoothFragmentLengthControl | None
    ManifestEncoding: MsSmoothManifestEncoding | None


class HlsImageBasedTrickPlaySettings(TypedDict, total=False):
    """Tile and thumbnail settings applicable when imageBasedTrickPlay is
    ADVANCED
    """

    IntervalCadence: HlsIntervalCadence | None
    ThumbnailHeight: _integerMin2Max4096 | None
    ThumbnailInterval: _doubleMin0Max2147483647 | None
    ThumbnailWidth: _integerMin8Max4096 | None
    TileHeight: _integerMin1Max2048 | None
    TileWidth: _integerMin1Max512 | None


class HlsEncryptionSettings(TypedDict, total=False):
    """Settings for HLS encryption"""

    ConstantInitializationVector: _stringMin32Max32Pattern09aFAF32 | None
    EncryptionMethod: HlsEncryptionType | None
    InitializationVectorInManifest: HlsInitializationVectorInManifest | None
    OfflineEncrypted: HlsOfflineEncrypted | None
    SpekeKeyProvider: SpekeKeyProvider | None
    StaticKeyProvider: StaticKeyProvider | None
    Type: HlsKeyProviderType | None


class HlsCaptionLanguageMapping(TypedDict, total=False):
    """Caption Language Mapping"""

    CaptionChannel: _integerMinNegative2147483648Max2147483647 | None
    CustomLanguageCode: _stringMin3Max3PatternAZaZ3 | None
    LanguageCode: LanguageCode | None
    LanguageDescription: _string | None


_listOfHlsCaptionLanguageMapping = list[HlsCaptionLanguageMapping]


class HlsAdditionalManifest(TypedDict, total=False):
    """Specify the details for each additional HLS manifest that you want the
    service to generate for this output group. Each manifest can reference a
    different subset of outputs in the group.
    """

    ManifestNameModifier: _stringMin1 | None
    SelectedOutputs: _listOf__stringMin1 | None


_listOfHlsAdditionalManifest = list[HlsAdditionalManifest]
_listOfHlsAdMarkers = list[HlsAdMarkers]


class HlsGroupSettings(TypedDict, total=False):
    """Settings related to your HLS output package. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/outputs-file-ABR.html.
    """

    AdMarkers: _listOfHlsAdMarkers | None
    AdditionalManifests: _listOfHlsAdditionalManifest | None
    AudioOnlyHeader: HlsAudioOnlyHeader | None
    BaseUrl: _string | None
    CaptionLanguageMappings: _listOfHlsCaptionLanguageMapping | None
    CaptionLanguageSetting: HlsCaptionLanguageSetting | None
    CaptionSegmentLengthControl: HlsCaptionSegmentLengthControl | None
    ClientCache: HlsClientCache | None
    CodecSpecification: HlsCodecSpecification | None
    Destination: _stringPatternS3 | None
    DestinationSettings: DestinationSettings | None
    DirectoryStructure: HlsDirectoryStructure | None
    Encryption: HlsEncryptionSettings | None
    ImageBasedTrickPlay: HlsImageBasedTrickPlay | None
    ImageBasedTrickPlaySettings: HlsImageBasedTrickPlaySettings | None
    ManifestCompression: HlsManifestCompression | None
    ManifestDurationFormat: HlsManifestDurationFormat | None
    MinFinalSegmentLength: _doubleMin0Max2147483647 | None
    MinSegmentLength: _integerMin0Max2147483647 | None
    OutputSelection: HlsOutputSelection | None
    ProgramDateTime: HlsProgramDateTime | None
    ProgramDateTimePeriod: _integerMin0Max3600 | None
    ProgressiveWriteHlsManifest: HlsProgressiveWriteHlsManifest | None
    SegmentControl: HlsSegmentControl | None
    SegmentLength: _integerMin1Max2147483647 | None
    SegmentLengthControl: HlsSegmentLengthControl | None
    SegmentsPerSubdirectory: _integerMin1Max2147483647 | None
    StreamInfResolution: HlsStreamInfResolution | None
    TargetDurationCompatibilityMode: HlsTargetDurationCompatibilityMode | None
    TimedMetadataId3Frame: HlsTimedMetadataId3Frame | None
    TimedMetadataId3Period: _integerMinNegative2147483648Max2147483647 | None
    TimestampDeltaMilliseconds: _integerMinNegative2147483648Max2147483647 | None


class FileGroupSettings(TypedDict, total=False):
    """Settings related to your File output group. MediaConvert uses this group
    of settings to generate a single standalone file, rather than a
    streaming package.
    """

    Destination: _stringPatternS3 | None
    DestinationSettings: DestinationSettings | None


class DashIsoImageBasedTrickPlaySettings(TypedDict, total=False):
    """Tile and thumbnail settings applicable when imageBasedTrickPlay is
    ADVANCED
    """

    IntervalCadence: DashIsoIntervalCadence | None
    ThumbnailHeight: _integerMin1Max4096 | None
    ThumbnailInterval: _doubleMin0Max2147483647 | None
    ThumbnailWidth: _integerMin8Max4096 | None
    TileHeight: _integerMin1Max2048 | None
    TileWidth: _integerMin1Max512 | None


class DashIsoEncryptionSettings(TypedDict, total=False):
    """Specifies DRM settings for DASH outputs."""

    PlaybackDeviceCompatibility: DashIsoPlaybackDeviceCompatibility | None
    SpekeKeyProvider: SpekeKeyProvider | None


class DashAdditionalManifest(TypedDict, total=False):
    """Specify the details for each additional DASH manifest that you want the
    service to generate for this output group. Each manifest can reference a
    different subset of outputs in the group.
    """

    ManifestNameModifier: _stringMin1 | None
    SelectedOutputs: _listOf__stringMin1 | None


_listOfDashAdditionalManifest = list[DashAdditionalManifest]


class DashIsoGroupSettings(TypedDict, total=False):
    """Settings related to your DASH output package. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/outputs-file-ABR.html.
    """

    AdditionalManifests: _listOfDashAdditionalManifest | None
    AudioChannelConfigSchemeIdUri: DashIsoGroupAudioChannelConfigSchemeIdUri | None
    BaseUrl: _string | None
    DashIFrameTrickPlayNameModifier: _stringMin1Max256 | None
    DashManifestStyle: DashManifestStyle | None
    Destination: _stringPatternS3 | None
    DestinationSettings: DestinationSettings | None
    Encryption: DashIsoEncryptionSettings | None
    FragmentLength: _integerMin1Max2147483647 | None
    HbbtvCompliance: DashIsoHbbtvCompliance | None
    ImageBasedTrickPlay: DashIsoImageBasedTrickPlay | None
    ImageBasedTrickPlaySettings: DashIsoImageBasedTrickPlaySettings | None
    MinBufferTime: _integerMin0Max2147483647 | None
    MinFinalSegmentLength: _doubleMin0Max2147483647 | None
    MpdManifestBandwidthType: DashIsoMpdManifestBandwidthType | None
    MpdProfile: DashIsoMpdProfile | None
    PtsOffsetHandlingForBFrames: DashIsoPtsOffsetHandlingForBFrames | None
    SegmentControl: DashIsoSegmentControl | None
    SegmentLength: _integerMin1Max2147483647 | None
    SegmentLengthControl: DashIsoSegmentLengthControl | None
    VideoCompositionOffsets: DashIsoVideoCompositionOffsets | None
    WriteSegmentTimelineInRepresentation: DashIsoWriteSegmentTimelineInRepresentation | None


class OutputGroupSettings(TypedDict, total=False):
    """Output Group settings, including type"""

    CmafGroupSettings: CmafGroupSettings | None
    DashIsoGroupSettings: DashIsoGroupSettings | None
    FileGroupSettings: FileGroupSettings | None
    HlsGroupSettings: HlsGroupSettings | None
    MsSmoothGroupSettings: MsSmoothGroupSettings | None
    PerFrameMetrics: _listOfFrameMetricType | None
    Type: OutputGroupType | None


class OutputGroup(TypedDict, total=False):
    """Group of outputs"""

    AutomatedEncodingSettings: AutomatedEncodingSettings | None
    CustomName: _string | None
    Name: _stringMax2048 | None
    OutputGroupSettings: OutputGroupSettings | None
    Outputs: _listOfOutput | None


_listOfOutputGroup = list[OutputGroup]


class NielsenNonLinearWatermarkSettings(TypedDict, total=False):
    """Ignore these settings unless you are using Nielsen non-linear
    watermarking. Specify the values that MediaConvert uses to generate and
    place Nielsen watermarks in your output audio. In addition to specifying
    these values, you also need to set up your cloud TIC server. These
    settings apply to every output in your job. The MediaConvert
    implementation is currently with the following Nielsen versions: Nielsen
    Watermark SDK Version 6.0.13 Nielsen NLM Watermark Engine Version 1.3.3
    Nielsen Watermark Authenticator [SID_TIC] Version [7.0.0]
    """

    ActiveWatermarkProcess: NielsenActiveWatermarkProcessType | None
    AdiFilename: _stringPatternS3 | None
    AssetId: _stringMin1Max20 | None
    AssetName: _stringMin1Max50 | None
    CbetSourceId: _stringPattern0xAFaF0908190908 | None
    EpisodeId: _stringMin1Max20 | None
    MetadataDestination: _stringPatternS3 | None
    SourceId: _integerMin0Max65534 | None
    SourceWatermarkStatus: NielsenSourceWatermarkStatusType | None
    TicServerUrl: _stringPatternHttps | None
    UniqueTicPerAudioTrack: NielsenUniqueTicPerAudioTrackType | None


class NielsenConfiguration(TypedDict, total=False):
    """Settings for your Nielsen configuration. If you don't do Nielsen
    measurement and analytics, ignore these settings. When you enable
    Nielsen configuration, MediaConvert enables PCM to ID3 tagging for all
    outputs in the job.
    """

    BreakoutCode: _integerMin0Max0 | None
    DistributorId: _string | None


class MotionImageInsertionOffset(TypedDict, total=False):
    """Specify the offset between the upper-left corner of the video frame and
    the top left corner of the overlay.
    """

    ImageX: _integerMin0Max2147483647 | None
    ImageY: _integerMin0Max2147483647 | None


class MotionImageInsertionFramerate(TypedDict, total=False):
    """For motion overlays that don't have a built-in frame rate, specify the
    frame rate of the overlay in frames per second, as a fraction. For
    example, specify 24 fps as 24/1. The overlay frame rate doesn't need to
    match the frame rate of the underlying video.
    """

    FramerateDenominator: _integerMin1Max17895697 | None
    FramerateNumerator: _integerMin1Max2147483640 | None


class MotionImageInserter(TypedDict, total=False):
    """Overlay motion graphics on top of your video. The motion graphics that
    you specify here appear on all outputs in all output groups. For more
    information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/motion-graphic-overlay.html.
    """

    Framerate: MotionImageInsertionFramerate | None
    Input: _stringMin14PatternS3Mov09PngHttpsMov09Png | None
    InsertionMode: MotionImageInsertionMode | None
    Offset: MotionImageInsertionOffset | None
    Playback: MotionImagePlayback | None
    StartTime: _stringMin11Max11Pattern01D20305D205D | None


class KantarWatermarkSettings(TypedDict, total=False):
    """Use these settings only when you use Kantar watermarking. Specify the
    values that MediaConvert uses to generate and place Kantar watermarks in
    your output audio. These settings apply to every output in your job. In
    addition to specifying these values, you also need to store your Kantar
    credentials in AWS Secrets Manager. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/kantar-watermarking.html.
    """

    ChannelName: _stringMin1Max20 | None
    ContentReference: _stringMin1Max50PatternAZAZ09 | None
    CredentialsSecretName: _stringMin1Max2048PatternArnAZSecretsmanagerWD12SecretAZAZ09 | None
    FileOffset: _doubleMin0 | None
    KantarLicenseId: _integerMin0Max2147483647 | None
    KantarServerUrl: _stringPatternHttpsKantarmedia | None
    LogDestination: _stringPatternS3 | None
    Metadata3: _stringMin1Max50 | None
    Metadata4: _stringMin1Max50 | None
    Metadata5: _stringMin1Max50 | None
    Metadata6: _stringMin1Max50 | None
    Metadata7: _stringMin1Max50 | None
    Metadata8: _stringMin1Max50 | None


class VideoSelector(TypedDict, total=False):
    """Input video selectors contain the video settings for the input. Each of
    your inputs can have up to one video selector.
    """

    AlphaBehavior: AlphaBehavior | None
    ColorSpace: ColorSpace | None
    ColorSpaceUsage: ColorSpaceUsage | None
    EmbeddedTimecodeOverride: EmbeddedTimecodeOverride | None
    Hdr10Metadata: Hdr10Metadata | None
    MaxLuminance: _integerMin0Max2147483647 | None
    PadVideo: PadVideo | None
    Pid: _integerMin1Max2147483647 | None
    ProgramNumber: _integerMinNegative2147483648Max2147483647 | None
    Rotate: InputRotate | None
    SampleRange: InputSampleRange | None
    SelectorType: VideoSelectorType | None
    Streams: _listOf__integerMin1Max2147483647 | None


class VideoOverlayPosition(TypedDict, total=False):
    """position of video overlay"""

    Height: _integerMinNegative1Max2147483647 | None
    Opacity: _integerMin0Max100 | None
    Unit: VideoOverlayUnit | None
    Width: _integerMinNegative1Max2147483647 | None
    XPosition: _integerMinNegative2147483648Max2147483647 | None
    YPosition: _integerMinNegative2147483648Max2147483647 | None


class VideoOverlayTransition(TypedDict, total=False):
    """Specify one or more Transitions for your video overlay. Use Transitions
    to reposition or resize your overlay over time. To use the same position
    and size for the duration of your video overlay: Leave blank. To specify
    a Transition: Enter a value for Start timecode, End Timecode, X
    Position, Y Position, Width, Height, or Opacity
    """

    EndPosition: VideoOverlayPosition | None
    EndTimecode: _stringPattern010920405090509092 | None
    StartTimecode: _stringPattern010920405090509092 | None


_listOfVideoOverlayTransition = list[VideoOverlayTransition]


class VideoOverlayInputClipping(TypedDict, total=False):
    """To transcode only portions of your video overlay, include one input clip
    for each part of your video overlay that you want in your output.
    """

    EndTimecode: _stringPattern010920405090509092090909 | None
    StartTimecode: _stringPattern010920405090509092090909 | None


_listOfVideoOverlayInputClipping = list[VideoOverlayInputClipping]
_mapOfAudioSelector = dict[_string, AudioSelector]


class VideoOverlayInput(TypedDict, total=False):
    """Input settings for Video overlay. You can include one or more video
    overlays in sequence at different times that you specify.
    """

    AudioSelectors: _mapOfAudioSelector | None
    FileInput: _stringPatternS3Https | None
    InputClippings: _listOfVideoOverlayInputClipping | None
    TimecodeSource: InputTimecodeSource | None
    TimecodeStart: _stringMin11Max11Pattern01D20305D205D | None


class VideoOverlayCrop(TypedDict, total=False):
    """Specify a rectangle of content to crop and use from your video overlay's
    input video. When you do, MediaConvert uses the cropped dimensions that
    you specify under X offset, Y offset, Width, and Height.
    """

    Height: _integerMin0Max2147483647 | None
    Unit: VideoOverlayUnit | None
    Width: _integerMin0Max2147483647 | None
    X: _integerMin0Max2147483647 | None
    Y: _integerMin0Max2147483647 | None


class VideoOverlay(TypedDict, total=False):
    """Overlay one or more videos on top of your input video. For more
    information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/video-overlays.html
    """

    Crop: VideoOverlayCrop | None
    EndTimecode: _stringPattern010920405090509092 | None
    InitialPosition: VideoOverlayPosition | None
    Input: VideoOverlayInput | None
    Playback: VideoOverlayPlayBackMode | None
    StartTimecode: _stringPattern010920405090509092 | None
    Transitions: _listOfVideoOverlayTransition | None


_listOfVideoOverlay = list[VideoOverlay]


class InputVideoGenerator(TypedDict, total=False):
    """When you include Video generator, MediaConvert creates a video input
    with black frames. Use this setting if you do not have a video input or
    if you want to add black video frames before, or after, other inputs.
    You can specify Video generator, or you can specify an Input file, but
    you cannot specify both. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/video-generator.html
    """

    Channels: _integerMin1Max32 | None
    Duration: _integerMin1Max86400000 | None
    FramerateDenominator: _integerMin1Max1001 | None
    FramerateNumerator: _integerMin1Max60000 | None
    Height: _integerMin32Max8192 | None
    ImageInput: _stringMin14PatternS3BmpBMPPngPNGTgaTGAHttpsBmpBMPPngPNGTgaTGA | None
    SampleRate: _integerMin32000Max48000 | None
    Width: _integerMin32Max8192 | None


class InputTamsSettings(TypedDict, total=False):
    """Specify a Time Addressable Media Store (TAMS) server as an input source.
    TAMS is an open-source API specification that provides access to
    time-segmented media content. Use TAMS to retrieve specific time ranges
    from live or archived media streams. When you specify TAMS settings,
    MediaConvert connects to your TAMS server, retrieves the media segments
    for your specified time range, and processes them as a single input.
    This enables workflows like extracting clips from live streams or
    processing specific portions of archived content. To use TAMS, you must:
    1. Have access to a TAMS-compliant server 2. Specify the server URL in
    the Input file URL field 3. Provide the required SourceId and Timerange
    parameters 4. Configure authentication, if your TAMS server requires it
    """

    AuthConnectionArn: _stringPatternArnAwsAZ09EventsAZ090912ConnectionAZAZ09AF0936 | None
    GapHandling: TamsGapHandling | None
    SourceId: _string | None
    Timerange: _stringPattern019090190908019090190908 | None


_listOf__stringPatternS3ASSETMAPXml = list[_stringPatternS3ASSETMAPXml]


class InputClipping(TypedDict, total=False):
    """To transcode only portions of your input, include one input clip for
    each part of your input that you want in your output. All input clips
    that you specify will be included in every output of the job. For more
    information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/assembling-multiple-inputs-and-input-clips.html.
    """

    EndTimecode: _stringPattern010920405090509092090909 | None
    StartTimecode: _stringPattern010920405090509092090909 | None


_listOfInputClipping = list[InputClipping]


class DynamicAudioSelector(TypedDict, total=False):
    """Use Dynamic audio selectors when you do not know the track layout of
    your source when you submit your job, but want to select multiple audio
    tracks. When you include an audio track in your output and specify this
    Dynamic audio selector as the Audio source, MediaConvert creates an
    audio track within that output for each dynamically selected track. Note
    that when you include a Dynamic audio selector for two or more inputs,
    each input must have the same number of audio tracks and audio channels.
    """

    AudioDurationCorrection: AudioDurationCorrection | None
    ExternalAudioFileInput: _stringPatternS3Https | None
    LanguageCode: LanguageCode | None
    Offset: _integerMinNegative2147483648Max2147483647 | None
    SelectorType: DynamicAudioSelectorType | None


_mapOfDynamicAudioSelector = dict[_string, DynamicAudioSelector]


class InputDecryptionSettings(TypedDict, total=False):
    """Settings for decrypting any input files that you encrypt before you
    upload them to Amazon S3. MediaConvert can decrypt files only when you
    use AWS Key Management Service (KMS) to encrypt the data key that you
    use to encrypt your content.
    """

    DecryptionMode: DecryptionMode | None
    EncryptedDecryptionKey: _stringMin24Max512PatternAZaZ0902 | None
    InitializationVector: _stringMin16Max24PatternAZaZ0922AZaZ0916 | None
    KmsKeyRegion: _stringMin9Max19PatternAZ26EastWestCentralNorthSouthEastWest1912 | None


_mapOfCaptionSelector = dict[_string, CaptionSelector]
_mapOfAudioSelectorGroup = dict[_string, AudioSelectorGroup]


class Input(TypedDict, total=False):
    """Use inputs to define the source files used in your transcoding job. For
    more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/specify-input-settings.html.
    You can use multiple video inputs to do input stitching. For more
    information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/assembling-multiple-inputs-and-input-clips.html
    """

    AdvancedInputFilter: AdvancedInputFilter | None
    AdvancedInputFilterSettings: AdvancedInputFilterSettings | None
    AudioSelectorGroups: _mapOfAudioSelectorGroup | None
    AudioSelectors: _mapOfAudioSelector | None
    CaptionSelectors: _mapOfCaptionSelector | None
    Crop: Rectangle | None
    DeblockFilter: InputDeblockFilter | None
    DecryptionSettings: InputDecryptionSettings | None
    DenoiseFilter: InputDenoiseFilter | None
    DolbyVisionMetadataXml: _stringMin14PatternS3XmlXMLHttpsXmlXML | None
    DynamicAudioSelectors: _mapOfDynamicAudioSelector | None
    FileInput: _stringMax2048PatternS3Https | None
    FilterEnable: InputFilterEnable | None
    FilterStrength: _integerMin0Max5 | None
    ImageInserter: ImageInserter | None
    InputClippings: _listOfInputClipping | None
    InputScanType: InputScanType | None
    Position: Rectangle | None
    ProgramNumber: _integerMin1Max2147483647 | None
    PsiControl: InputPsiControl | None
    SupplementalImps: _listOf__stringPatternS3ASSETMAPXml | None
    TamsSettings: InputTamsSettings | None
    TimecodeSource: InputTimecodeSource | None
    TimecodeStart: _stringMin11Max11Pattern01D20305D205D | None
    VideoGenerator: InputVideoGenerator | None
    VideoOverlays: _listOfVideoOverlay | None
    VideoSelector: VideoSelector | None


_listOfInput = list[Input]


class ExtendedDataServices(TypedDict, total=False):
    """If your source content has EIA-608 Line 21 Data Services, enable this
    feature to specify what MediaConvert does with the Extended Data
    Services (XDS) packets. You can choose to pass through XDS packets, or
    remove them from the output. For more information about XDS, see EIA-608
    Line Data Services, section 9.5.1.5 05h Content Advisory.
    """

    CopyProtectionAction: CopyProtectionAction | None
    VchipAction: VchipAction | None


class EsamSignalProcessingNotification(TypedDict, total=False):
    """ESAM SignalProcessingNotification data defined by
    OC-SP-ESAM-API-I03-131025.
    """

    SccXml: _stringPatternSNSignalProcessingNotificationNS | None


class EsamManifestConfirmConditionNotification(TypedDict, total=False):
    """ESAM ManifestConfirmConditionNotification defined by
    OC-SP-ESAM-API-I03-131025.
    """

    MccXml: _stringPatternSNManifestConfirmConditionNotificationNS | None


class EsamSettings(TypedDict, total=False):
    """Settings for Event Signaling And Messaging (ESAM). If you don't do ad
    insertion, you can ignore these settings.
    """

    ManifestConfirmConditionNotification: EsamManifestConfirmConditionNotification | None
    ResponseSignalPreroll: _integerMin0Max30000 | None
    SignalProcessingNotification: EsamSignalProcessingNotification | None


_listOfColorConversion3DLUTSetting = list[ColorConversion3DLUTSetting]


class JobSettings(TypedDict, total=False):
    """JobSettings contains all the transcode settings for a job."""

    AdAvailOffset: _integerMinNegative1000Max1000 | None
    AvailBlanking: AvailBlanking | None
    ColorConversion3DLUTSettings: _listOfColorConversion3DLUTSetting | None
    Esam: EsamSettings | None
    ExtendedDataServices: ExtendedDataServices | None
    FollowSource: _integerMin1Max150 | None
    Inputs: _listOfInput | None
    KantarWatermark: KantarWatermarkSettings | None
    MotionImageInserter: MotionImageInserter | None
    NielsenConfiguration: NielsenConfiguration | None
    NielsenNonLinearWatermark: NielsenNonLinearWatermarkSettings | None
    OutputGroups: _listOfOutputGroup | None
    TimecodeConfig: TimecodeConfig | None
    TimedMetadataInsertion: TimedMetadataInsertion | None


class HopDestination(TypedDict, total=False):
    """Optional. Configuration for a destination queue to which the job can hop
    once a customer-defined minimum wait time has passed.
    """

    Priority: _integerMinNegative50Max50 | None
    Queue: _string | None
    WaitMinutes: _integer | None


_listOfHopDestination = list[HopDestination]


class CreateJobRequest(ServiceRequest):
    AccelerationSettings: AccelerationSettings | None
    BillingTagsSource: BillingTagsSource | None
    ClientRequestToken: _string | None
    HopDestinations: _listOfHopDestination | None
    JobEngineVersion: _string | None
    JobTemplate: _string | None
    Priority: _integerMinNegative50Max50 | None
    Queue: _string | None
    Role: _string
    Settings: JobSettings
    SimulateReservedQueue: SimulateReservedQueue | None
    StatusUpdateInterval: StatusUpdateInterval | None
    Tags: _mapOf__string | None
    UserMetadata: _mapOf__string | None


class WarningGroup(TypedDict, total=False):
    """Contains any warning codes and their count for the job."""

    Code: _integer
    Count: _integer


_listOfWarningGroup = list[WarningGroup]
_timestampUnix = datetime


class Timing(TypedDict, total=False):
    """Information about when jobs are submitted, started, and finished is
    specified in Unix epoch format in seconds.
    """

    FinishTime: _timestampUnix | None
    StartTime: _timestampUnix | None
    SubmitTime: _timestampUnix | None


class QueueTransition(TypedDict, total=False):
    """Description of the source and destination queues between which the job
    has moved, along with the timestamp of the move
    """

    DestinationQueue: _string | None
    SourceQueue: _string | None
    Timestamp: _timestampUnix | None


_listOfQueueTransition = list[QueueTransition]


class VideoDetail(TypedDict, total=False):
    """Contains details about the output's video stream"""

    HeightInPx: _integer | None
    WidthInPx: _integer | None


class OutputDetail(TypedDict, total=False):
    """Details regarding output"""

    DurationInMs: _integer | None
    VideoDetails: VideoDetail | None


_listOfOutputDetail = list[OutputDetail]


class OutputGroupDetail(TypedDict, total=False):
    """Contains details about the output groups specified in the job settings."""

    OutputDetails: _listOfOutputDetail | None


_listOfOutputGroupDetail = list[OutputGroupDetail]
_listOf__string = list[_string]


class JobMessages(TypedDict, total=False):
    """Provides messages from the service about jobs that you have already
    successfully submitted.
    """

    Info: _listOf__string | None
    Warning: _listOf__string | None


class Job(TypedDict, total=False):
    """Each job converts an input file into an output file or files. For more
    information, see the User Guide at
    https://docs.aws.amazon.com/mediaconvert/latest/ug/what-is.html
    """

    AccelerationSettings: AccelerationSettings | None
    AccelerationStatus: AccelerationStatus | None
    Arn: _string | None
    BillingTagsSource: BillingTagsSource | None
    ClientRequestToken: _string | None
    CreatedAt: _timestampUnix | None
    CurrentPhase: JobPhase | None
    ErrorCode: _integer | None
    ErrorMessage: _string | None
    HopDestinations: _listOfHopDestination | None
    Id: _string | None
    JobEngineVersionRequested: _string | None
    JobEngineVersionUsed: _string | None
    JobPercentComplete: _integer | None
    JobTemplate: _string | None
    LastShareDetails: _string | None
    Messages: JobMessages | None
    OutputGroupDetails: _listOfOutputGroupDetail | None
    Priority: _integerMinNegative50Max50 | None
    Queue: _string | None
    QueueTransitions: _listOfQueueTransition | None
    RetryCount: _integer | None
    Role: _string
    Settings: JobSettings
    ShareStatus: ShareStatus | None
    SimulateReservedQueue: SimulateReservedQueue | None
    Status: JobStatus | None
    StatusUpdateInterval: StatusUpdateInterval | None
    Timing: Timing | None
    UserMetadata: _mapOf__string | None
    Warnings: _listOfWarningGroup | None


class CreateJobResponse(TypedDict, total=False):
    Job: Job | None


class InputTemplate(TypedDict, total=False):
    """Specified video input in a template."""

    AdvancedInputFilter: AdvancedInputFilter | None
    AdvancedInputFilterSettings: AdvancedInputFilterSettings | None
    AudioSelectorGroups: _mapOfAudioSelectorGroup | None
    AudioSelectors: _mapOfAudioSelector | None
    CaptionSelectors: _mapOfCaptionSelector | None
    Crop: Rectangle | None
    DeblockFilter: InputDeblockFilter | None
    DenoiseFilter: InputDenoiseFilter | None
    DolbyVisionMetadataXml: _stringMin14PatternS3XmlXMLHttpsXmlXML | None
    DynamicAudioSelectors: _mapOfDynamicAudioSelector | None
    FilterEnable: InputFilterEnable | None
    FilterStrength: _integerMin0Max5 | None
    ImageInserter: ImageInserter | None
    InputClippings: _listOfInputClipping | None
    InputScanType: InputScanType | None
    Position: Rectangle | None
    ProgramNumber: _integerMin1Max2147483647 | None
    PsiControl: InputPsiControl | None
    TimecodeSource: InputTimecodeSource | None
    TimecodeStart: _stringMin11Max11Pattern01D20305D205D | None
    VideoOverlays: _listOfVideoOverlay | None
    VideoSelector: VideoSelector | None


_listOfInputTemplate = list[InputTemplate]


class JobTemplateSettings(TypedDict, total=False):
    """JobTemplateSettings contains all the transcode settings saved in the
    template that will be applied to jobs created from it.
    """

    AdAvailOffset: _integerMinNegative1000Max1000 | None
    AvailBlanking: AvailBlanking | None
    ColorConversion3DLUTSettings: _listOfColorConversion3DLUTSetting | None
    Esam: EsamSettings | None
    ExtendedDataServices: ExtendedDataServices | None
    FollowSource: _integerMin1Max150 | None
    Inputs: _listOfInputTemplate | None
    KantarWatermark: KantarWatermarkSettings | None
    MotionImageInserter: MotionImageInserter | None
    NielsenConfiguration: NielsenConfiguration | None
    NielsenNonLinearWatermark: NielsenNonLinearWatermarkSettings | None
    OutputGroups: _listOfOutputGroup | None
    TimecodeConfig: TimecodeConfig | None
    TimedMetadataInsertion: TimedMetadataInsertion | None


class CreateJobTemplateRequest(ServiceRequest):
    AccelerationSettings: AccelerationSettings | None
    Category: _string | None
    Description: _string | None
    HopDestinations: _listOfHopDestination | None
    Name: _string
    Priority: _integerMinNegative50Max50 | None
    Queue: _string | None
    Settings: JobTemplateSettings
    StatusUpdateInterval: StatusUpdateInterval | None
    Tags: _mapOf__string | None


class JobTemplate(TypedDict, total=False):
    """A job template is a pre-made set of encoding instructions that you can
    use to quickly create a job.
    """

    AccelerationSettings: AccelerationSettings | None
    Arn: _string | None
    Category: _string | None
    CreatedAt: _timestampUnix | None
    Description: _string | None
    HopDestinations: _listOfHopDestination | None
    LastUpdated: _timestampUnix | None
    Name: _string
    Priority: _integerMinNegative50Max50 | None
    Queue: _string | None
    Settings: JobTemplateSettings
    StatusUpdateInterval: StatusUpdateInterval | None
    Type: Type | None


class CreateJobTemplateResponse(TypedDict, total=False):
    JobTemplate: JobTemplate | None


_listOfCaptionDescriptionPreset = list[CaptionDescriptionPreset]


class PresetSettings(TypedDict, total=False):
    """Settings for preset"""

    AudioDescriptions: _listOfAudioDescription | None
    CaptionDescriptions: _listOfCaptionDescriptionPreset | None
    ContainerSettings: ContainerSettings | None
    VideoDescription: VideoDescription | None


class CreatePresetRequest(ServiceRequest):
    Category: _string | None
    Description: _string | None
    Name: _string
    Settings: PresetSettings
    Tags: _mapOf__string | None


class Preset(TypedDict, total=False):
    """A preset is a collection of preconfigured media conversion settings that
    you want MediaConvert to apply to the output during the conversion
    process.
    """

    Arn: _string | None
    Category: _string | None
    CreatedAt: _timestampUnix | None
    Description: _string | None
    LastUpdated: _timestampUnix | None
    Name: _string
    Settings: PresetSettings
    Type: Type | None


class CreatePresetResponse(TypedDict, total=False):
    Preset: Preset | None


class ReservationPlanSettings(TypedDict, total=False):
    """Details about the pricing plan for your reserved queue. Required for
    reserved queues and not applicable to on-demand queues.
    """

    Commitment: Commitment
    RenewalType: RenewalType
    ReservedSlots: _integer


class CreateQueueRequest(ServiceRequest):
    ConcurrentJobs: _integer | None
    Description: _string | None
    Name: _string
    PricingPlan: PricingPlan | None
    ReservationPlanSettings: ReservationPlanSettings | None
    Status: QueueStatus | None
    Tags: _mapOf__string | None


class ServiceOverride(TypedDict, total=False):
    """A service override applied by MediaConvert to the settings that you have
    configured. If you see any overrides, we recommend that you contact AWS
    Support.
    """

    Message: _string | None
    Name: _string | None
    OverrideValue: _string | None
    Value: _string | None


_listOfServiceOverride = list[ServiceOverride]


class ReservationPlan(TypedDict, total=False):
    """Details about the pricing plan for your reserved queue. Required for
    reserved queues and not applicable to on-demand queues.
    """

    Commitment: Commitment | None
    ExpiresAt: _timestampUnix | None
    PurchasedAt: _timestampUnix | None
    RenewalType: RenewalType | None
    ReservedSlots: _integer | None
    Status: ReservationPlanStatus | None


class Queue(TypedDict, total=False):
    """You can use queues to manage the resources that are available to your
    AWS account for running multiple transcoding jobs at the same time. If
    you don't specify a queue, the service sends all jobs through the
    default queue. For more information, see
    https://docs.aws.amazon.com/mediaconvert/latest/ug/working-with-queues.html.
    """

    Arn: _string | None
    ConcurrentJobs: _integer | None
    CreatedAt: _timestampUnix | None
    Description: _string | None
    LastUpdated: _timestampUnix | None
    Name: _string
    PricingPlan: PricingPlan | None
    ProgressingJobsCount: _integer | None
    ReservationPlan: ReservationPlan | None
    ServiceOverrides: _listOfServiceOverride | None
    Status: QueueStatus | None
    SubmittedJobsCount: _integer | None
    Type: Type | None


class CreateQueueResponse(TypedDict, total=False):
    Queue: Queue | None


class CreateResourceShareRequest(ServiceRequest):
    JobId: _string
    SupportCaseId: _string


class CreateResourceShareResponse(TypedDict, total=False):
    pass


class DeleteJobTemplateRequest(ServiceRequest):
    Name: _string


class DeleteJobTemplateResponse(TypedDict, total=False):
    pass


class DeletePolicyRequest(ServiceRequest):
    pass


class DeletePolicyResponse(TypedDict, total=False):
    pass


class DeletePresetRequest(ServiceRequest):
    Name: _string


class DeletePresetResponse(TypedDict, total=False):
    pass


class DeleteQueueRequest(ServiceRequest):
    Name: _string


class DeleteQueueResponse(TypedDict, total=False):
    pass


class DescribeEndpointsRequest(ServiceRequest):
    MaxResults: _integer | None
    Mode: DescribeEndpointsMode | None
    NextToken: _string | None


class Endpoint(TypedDict, total=False):
    """Describes an account-specific API endpoint."""

    Url: _string | None


_listOfEndpoint = list[Endpoint]


class DescribeEndpointsResponse(TypedDict, total=False):
    Endpoints: _listOfEndpoint | None
    NextToken: _string | None


class DisassociateCertificateRequest(ServiceRequest):
    Arn: _string


class DisassociateCertificateResponse(TypedDict, total=False):
    pass


class ExceptionBody(TypedDict, total=False):
    Message: _string | None


class GetJobRequest(ServiceRequest):
    Id: _string


class GetJobResponse(TypedDict, total=False):
    Job: Job | None


class GetJobTemplateRequest(ServiceRequest):
    Name: _string


class GetJobTemplateResponse(TypedDict, total=False):
    JobTemplate: JobTemplate | None


class GetJobsQueryResultsRequest(ServiceRequest):
    Id: _string


_listOfJob = list[Job]


class GetJobsQueryResultsResponse(TypedDict, total=False):
    Jobs: _listOfJob | None
    NextToken: _string | None
    Status: JobsQueryStatus | None


class GetPolicyRequest(ServiceRequest):
    pass


class Policy(TypedDict, total=False):
    """A policy configures behavior that you allow or disallow for your
    account. For information about MediaConvert policies, see the user guide
    at http://docs.aws.amazon.com/mediaconvert/latest/ug/what-is.html
    """

    HttpInputs: InputPolicy | None
    HttpsInputs: InputPolicy | None
    S3Inputs: InputPolicy | None


class GetPolicyResponse(TypedDict, total=False):
    Policy: Policy | None


class GetPresetRequest(ServiceRequest):
    Name: _string


class GetPresetResponse(TypedDict, total=False):
    Preset: Preset | None


class GetQueueRequest(ServiceRequest):
    Name: _string


class GetQueueResponse(TypedDict, total=False):
    Queue: Queue | None


class JobEngineVersion(TypedDict, total=False):
    """Use Job engine versions to run jobs for your production workflow on one
    version, while you test and validate the latest version. Job engine
    versions are in a YYYY-MM-DD format.
    """

    ExpirationDate: _timestampUnix | None
    Version: _string | None


_listOf__stringMax100 = list[_stringMax100]


class JobsQueryFilter(TypedDict, total=False):
    """Provide one or more JobsQueryFilter objects, each containing a Key with
    an associated Values array. Note that MediaConvert queries jobs using OR
    logic.
    """

    Key: JobsQueryFilterKey | None
    Values: _listOf__stringMax100 | None


class ListJobTemplatesRequest(ServiceRequest):
    Category: _string | None
    ListBy: JobTemplateListBy | None
    MaxResults: _integerMin1Max20 | None
    NextToken: _string | None
    Order: Order | None


_listOfJobTemplate = list[JobTemplate]


class ListJobTemplatesResponse(TypedDict, total=False):
    JobTemplates: _listOfJobTemplate | None
    NextToken: _string | None


class ListJobsRequest(ServiceRequest):
    MaxResults: _integerMin1Max20 | None
    NextToken: _string | None
    Order: Order | None
    Queue: _string | None
    Status: JobStatus | None


class ListJobsResponse(TypedDict, total=False):
    Jobs: _listOfJob | None
    NextToken: _string | None


class ListPresetsRequest(ServiceRequest):
    Category: _string | None
    ListBy: PresetListBy | None
    MaxResults: _integerMin1Max20 | None
    NextToken: _string | None
    Order: Order | None


_listOfPreset = list[Preset]


class ListPresetsResponse(TypedDict, total=False):
    NextToken: _string | None
    Presets: _listOfPreset | None


class ListQueuesRequest(ServiceRequest):
    ListBy: QueueListBy | None
    MaxResults: _integerMin1Max20 | None
    NextToken: _string | None
    Order: Order | None


_listOfQueue = list[Queue]


class ListQueuesResponse(TypedDict, total=False):
    NextToken: _string | None
    Queues: _listOfQueue | None
    TotalConcurrentJobs: _integer | None
    UnallocatedConcurrentJobs: _integer | None


class ListTagsForResourceRequest(ServiceRequest):
    Arn: _string


class ResourceTags(TypedDict, total=False):
    """The Amazon Resource Name (ARN) and tags for an AWS Elemental
    MediaConvert resource.
    """

    Arn: _string | None
    Tags: _mapOf__string | None


class ListTagsForResourceResponse(TypedDict, total=False):
    ResourceTags: ResourceTags | None


class ListVersionsRequest(ServiceRequest):
    MaxResults: _integerMin1Max20 | None
    NextToken: _string | None


_listOfJobEngineVersion = list[JobEngineVersion]


class ListVersionsResponse(TypedDict, total=False):
    NextToken: _string | None
    Versions: _listOfJobEngineVersion | None


class Metadata(TypedDict, total=False):
    """Metadata and other file information."""

    ETag: _string | None
    FileSize: _long | None
    LastModified: _timestampUnix | None
    MimeType: _string | None


class ProbeInputFile(TypedDict, total=False):
    """The input file that needs to be analyzed."""

    FileUrl: _string | None


_listOfProbeInputFile = list[ProbeInputFile]


class ProbeRequest(ServiceRequest):
    InputFiles: _listOfProbeInputFile | None


_listOf__integer = list[_integer]


class TrackMapping(TypedDict, total=False):
    """An array containing track mapping information."""

    AudioTrackIndexes: _listOf__integer | None
    DataTrackIndexes: _listOf__integer | None
    VideoTrackIndexes: _listOf__integer | None


_listOfTrackMapping = list[TrackMapping]


class ProbeResult(TypedDict, total=False):
    """Probe results for your media file."""

    Container: Container | None
    Metadata: Metadata | None
    TrackMappings: _listOfTrackMapping | None


_listOfProbeResult = list[ProbeResult]


class ProbeResponse(TypedDict, total=False):
    ProbeResults: _listOfProbeResult | None


class PutPolicyRequest(ServiceRequest):
    Policy: Policy


class PutPolicyResponse(TypedDict, total=False):
    Policy: Policy | None


class SearchJobsRequest(ServiceRequest):
    InputFile: _string | None
    MaxResults: _integerMin1Max20 | None
    NextToken: _string | None
    Order: Order | None
    Queue: _string | None
    Status: JobStatus | None


class SearchJobsResponse(TypedDict, total=False):
    Jobs: _listOfJob | None
    NextToken: _string | None


_listOfJobsQueryFilter = list[JobsQueryFilter]


class StartJobsQueryRequest(ServiceRequest):
    FilterList: _listOfJobsQueryFilter | None
    MaxResults: _integerMin1Max20 | None
    NextToken: _string | None
    Order: Order | None


class StartJobsQueryResponse(TypedDict, total=False):
    Id: _string | None


class TagResourceRequest(ServiceRequest):
    Arn: _string
    Tags: _mapOf__string


class TagResourceResponse(TypedDict, total=False):
    pass


class UntagResourceRequest(ServiceRequest):
    Arn: _string
    TagKeys: _listOf__string | None


class UntagResourceResponse(TypedDict, total=False):
    pass


class UpdateJobTemplateRequest(ServiceRequest):
    AccelerationSettings: AccelerationSettings | None
    Category: _string | None
    Description: _string | None
    HopDestinations: _listOfHopDestination | None
    Name: _string
    Priority: _integerMinNegative50Max50 | None
    Queue: _string | None
    Settings: JobTemplateSettings | None
    StatusUpdateInterval: StatusUpdateInterval | None


class UpdateJobTemplateResponse(TypedDict, total=False):
    JobTemplate: JobTemplate | None


class UpdatePresetRequest(ServiceRequest):
    Category: _string | None
    Description: _string | None
    Name: _string
    Settings: PresetSettings | None


class UpdatePresetResponse(TypedDict, total=False):
    Preset: Preset | None


class UpdateQueueRequest(ServiceRequest):
    ConcurrentJobs: _integer | None
    Description: _string | None
    Name: _string
    ReservationPlanSettings: ReservationPlanSettings | None
    Status: QueueStatus | None


class UpdateQueueResponse(TypedDict, total=False):
    Queue: Queue | None


_timestampIso8601 = datetime


class MediaconvertApi:
    service: str = "mediaconvert"
    version: str = "2017-08-29"

    @handler("AssociateCertificate")
    def associate_certificate(
        self, context: RequestContext, arn: _string, **kwargs
    ) -> AssociateCertificateResponse:
        """Associates an AWS Certificate Manager (ACM) Amazon Resource Name (ARN)
        with AWS Elemental MediaConvert.

        :param arn: The ARN of the ACM certificate that you want to associate with your
        MediaConvert resource.
        :returns: AssociateCertificateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CancelJob")
    def cancel_job(self, context: RequestContext, id: _string, **kwargs) -> CancelJobResponse:
        """Permanently cancel a job. Once you have canceled a job, you can't start
        it again.

        :param id: The Job ID of the job to be cancelled.
        :returns: CancelJobResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateJob")
    def create_job(
        self,
        context: RequestContext,
        role: _string,
        settings: JobSettings,
        acceleration_settings: AccelerationSettings | None = None,
        billing_tags_source: BillingTagsSource | None = None,
        client_request_token: _string | None = None,
        hop_destinations: _listOfHopDestination | None = None,
        job_engine_version: _string | None = None,
        job_template: _string | None = None,
        priority: _integerMinNegative50Max50 | None = None,
        queue: _string | None = None,
        simulate_reserved_queue: SimulateReservedQueue | None = None,
        status_update_interval: StatusUpdateInterval | None = None,
        tags: _mapOf__string | None = None,
        user_metadata: _mapOf__string | None = None,
        **kwargs,
    ) -> CreateJobResponse:
        """Create a new transcoding job. For information about jobs and job
        settings, see the User Guide at
        http://docs.aws.amazon.com/mediaconvert/latest/ug/what-is.html

        :param role: Required.
        :param settings: JobSettings contains all the transcode settings for a job.
        :param acceleration_settings: Optional.
        :param billing_tags_source: Optionally choose a Billing tags source that AWS Billing and Cost
        Management will use to display tags for individual output costs on any
        billing report that you set up.
        :param client_request_token: Prevent duplicate jobs from being created and ensure idempotency for
        your requests.
        :param hop_destinations: Optional.
        :param job_engine_version: Use Job engine versions to run jobs for your production workflow on one
        version, while you test and validate the latest version.
        :param job_template: Optional.
        :param priority: Optional.
        :param queue: Optional.
        :param simulate_reserved_queue: Optional.
        :param status_update_interval: Optional.
        :param tags: Optional.
        :param user_metadata: Optional.
        :returns: CreateJobResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateJobTemplate")
    def create_job_template(
        self,
        context: RequestContext,
        settings: JobTemplateSettings,
        name: _string,
        acceleration_settings: AccelerationSettings | None = None,
        category: _string | None = None,
        description: _string | None = None,
        hop_destinations: _listOfHopDestination | None = None,
        priority: _integerMinNegative50Max50 | None = None,
        queue: _string | None = None,
        status_update_interval: StatusUpdateInterval | None = None,
        tags: _mapOf__string | None = None,
        **kwargs,
    ) -> CreateJobTemplateResponse:
        """Create a new job template. For information about job templates see the
        User Guide at
        http://docs.aws.amazon.com/mediaconvert/latest/ug/what-is.html

        :param settings: JobTemplateSettings contains all the transcode settings saved in the
        template that will be applied to jobs created from it.
        :param name: The name of the job template you are creating.
        :param acceleration_settings: Accelerated transcoding can significantly speed up jobs with long,
        visually complex content.
        :param category: Optional.
        :param description: Optional.
        :param hop_destinations: Optional.
        :param priority: Specify the relative priority for this job.
        :param queue: Optional.
        :param status_update_interval: Specify how often MediaConvert sends STATUS_UPDATE events to Amazon
        CloudWatch Events.
        :param tags: The tags that you want to add to the resource.
        :returns: CreateJobTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreatePreset")
    def create_preset(
        self,
        context: RequestContext,
        settings: PresetSettings,
        name: _string,
        category: _string | None = None,
        description: _string | None = None,
        tags: _mapOf__string | None = None,
        **kwargs,
    ) -> CreatePresetResponse:
        """Create a new preset. For information about job templates see the User
        Guide at http://docs.aws.amazon.com/mediaconvert/latest/ug/what-is.html

        :param settings: Settings for preset.
        :param name: The name of the preset you are creating.
        :param category: Optional.
        :param description: Optional.
        :param tags: The tags that you want to add to the resource.
        :returns: CreatePresetResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateQueue")
    def create_queue(
        self,
        context: RequestContext,
        name: _string,
        concurrent_jobs: _integer | None = None,
        description: _string | None = None,
        pricing_plan: PricingPlan | None = None,
        reservation_plan_settings: ReservationPlanSettings | None = None,
        status: QueueStatus | None = None,
        tags: _mapOf__string | None = None,
        **kwargs,
    ) -> CreateQueueResponse:
        """Create a new transcoding queue. For information about queues, see
        Working With Queues in the User Guide at
        https://docs.aws.amazon.com/mediaconvert/latest/ug/working-with-queues.html

        :param name: The name of the queue that you are creating.
        :param concurrent_jobs: Specify the maximum number of jobs your queue can process concurrently.
        :param description: Optional.
        :param pricing_plan: Specifies whether the pricing plan for the queue is on-demand or
        reserved.
        :param reservation_plan_settings: Details about the pricing plan for your reserved queue.
        :param status: Initial state of the queue.
        :param tags: The tags that you want to add to the resource.
        :returns: CreateQueueResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateResourceShare")
    def create_resource_share(
        self, context: RequestContext, support_case_id: _string, job_id: _string, **kwargs
    ) -> CreateResourceShareResponse:
        """Create a new resource share request for MediaConvert resources with AWS
        Support.

        :param support_case_id: AWS Support case identifier.
        :param job_id: Specify MediaConvert Job ID or ARN to share.
        :returns: CreateResourceShareResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("DeleteJobTemplate")
    def delete_job_template(
        self, context: RequestContext, name: _string, **kwargs
    ) -> DeleteJobTemplateResponse:
        """Permanently delete a job template you have created.

        :param name: The name of the job template to be deleted.
        :returns: DeleteJobTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("DeletePolicy")
    def delete_policy(self, context: RequestContext, **kwargs) -> DeletePolicyResponse:
        """Permanently delete a policy that you created.

        :returns: DeletePolicyResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("DeletePreset")
    def delete_preset(
        self, context: RequestContext, name: _string, **kwargs
    ) -> DeletePresetResponse:
        """Permanently delete a preset you have created.

        :param name: The name of the preset to be deleted.
        :returns: DeletePresetResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("DeleteQueue")
    def delete_queue(self, context: RequestContext, name: _string, **kwargs) -> DeleteQueueResponse:
        """Permanently delete a queue you have created.

        :param name: The name of the queue that you want to delete.
        :returns: DeleteQueueResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("DescribeEndpoints")
    def describe_endpoints(
        self,
        context: RequestContext,
        max_results: _integer | None = None,
        mode: DescribeEndpointsMode | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> DescribeEndpointsResponse:
        """Send a request with an empty body to the regional API endpoint to get
        your account API endpoint. Note that DescribeEndpoints is no longer
        required. We recommend that you send your requests directly to the
        regional endpoint instead.

        :param max_results: Optional.
        :param mode: Optional field, defaults to DEFAULT.
        :param next_token: Use this string, provided with the response to a previous request, to
        request the next batch of endpoints.
        :returns: DescribeEndpointsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("DisassociateCertificate")
    def disassociate_certificate(
        self, context: RequestContext, arn: _string, **kwargs
    ) -> DisassociateCertificateResponse:
        """Removes an association between the Amazon Resource Name (ARN) of an AWS
        Certificate Manager (ACM) certificate and an AWS Elemental MediaConvert
        resource.

        :param arn: The ARN of the ACM certificate that you want to disassociate from your
        MediaConvert resource.
        :returns: DisassociateCertificateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("GetJob")
    def get_job(self, context: RequestContext, id: _string, **kwargs) -> GetJobResponse:
        """Retrieve the JSON for a specific transcoding job.

        :param id: the job ID of the job.
        :returns: GetJobResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("GetJobTemplate")
    def get_job_template(
        self, context: RequestContext, name: _string, **kwargs
    ) -> GetJobTemplateResponse:
        """Retrieve the JSON for a specific job template.

        :param name: The name of the job template.
        :returns: GetJobTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("GetJobsQueryResults")
    def get_jobs_query_results(
        self, context: RequestContext, id: _string, **kwargs
    ) -> GetJobsQueryResultsResponse:
        """Retrieve a JSON array of up to twenty of your most recent jobs matched
        by a jobs query.

        :param id: The ID of the jobs query.
        :returns: GetJobsQueryResultsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("GetPolicy")
    def get_policy(self, context: RequestContext, **kwargs) -> GetPolicyResponse:
        """Retrieve the JSON for your policy.

        :returns: GetPolicyResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("GetPreset")
    def get_preset(self, context: RequestContext, name: _string, **kwargs) -> GetPresetResponse:
        """Retrieve the JSON for a specific preset.

        :param name: The name of the preset.
        :returns: GetPresetResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("GetQueue")
    def get_queue(self, context: RequestContext, name: _string, **kwargs) -> GetQueueResponse:
        """Retrieve the JSON for a specific queue.

        :param name: The name of the queue that you want information about.
        :returns: GetQueueResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("ListJobTemplates")
    def list_job_templates(
        self,
        context: RequestContext,
        category: _string | None = None,
        list_by: JobTemplateListBy | None = None,
        max_results: _integerMin1Max20 | None = None,
        next_token: _string | None = None,
        order: Order | None = None,
        **kwargs,
    ) -> ListJobTemplatesResponse:
        """Retrieve a JSON array of up to twenty of your job templates. This will
        return the templates themselves, not just a list of them. To retrieve
        the next twenty templates, use the nextToken string returned with the
        array

        :param category: Optionally, specify a job template category to limit responses to only
        job templates from that category.
        :param list_by: Optional.
        :param max_results: Optional.
        :param next_token: Use this string, provided with the response to a previous request, to
        request the next batch of job templates.
        :param order: Optional.
        :returns: ListJobTemplatesResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("ListJobs")
    def list_jobs(
        self,
        context: RequestContext,
        max_results: _integerMin1Max20 | None = None,
        next_token: _string | None = None,
        order: Order | None = None,
        queue: _string | None = None,
        status: JobStatus | None = None,
        **kwargs,
    ) -> ListJobsResponse:
        """Retrieve a JSON array of up to twenty of your most recently created
        jobs. This array includes in-process, completed, and errored jobs. This
        will return the jobs themselves, not just a list of the jobs. To
        retrieve the twenty next most recent jobs, use the nextToken string
        returned with the array.

        :param max_results: Optional.
        :param next_token: Optional.
        :param order: Optional.
        :param queue: Optional.
        :param status: Optional.
        :returns: ListJobsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("ListPresets")
    def list_presets(
        self,
        context: RequestContext,
        category: _string | None = None,
        list_by: PresetListBy | None = None,
        max_results: _integerMin1Max20 | None = None,
        next_token: _string | None = None,
        order: Order | None = None,
        **kwargs,
    ) -> ListPresetsResponse:
        """Retrieve a JSON array of up to twenty of your presets. This will return
        the presets themselves, not just a list of them. To retrieve the next
        twenty presets, use the nextToken string returned with the array.

        :param category: Optionally, specify a preset category to limit responses to only presets
        from that category.
        :param list_by: Optional.
        :param max_results: Optional.
        :param next_token: Use this string, provided with the response to a previous request, to
        request the next batch of presets.
        :param order: Optional.
        :returns: ListPresetsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("ListQueues")
    def list_queues(
        self,
        context: RequestContext,
        list_by: QueueListBy | None = None,
        max_results: _integerMin1Max20 | None = None,
        next_token: _string | None = None,
        order: Order | None = None,
        **kwargs,
    ) -> ListQueuesResponse:
        """Retrieve a JSON array of up to twenty of your queues. This will return
        the queues themselves, not just a list of them. To retrieve the next
        twenty queues, use the nextToken string returned with the array.

        :param list_by: Optional.
        :param max_results: Optional.
        :param next_token: Use this string, provided with the response to a previous request, to
        request the next batch of queues.
        :param order: Optional.
        :returns: ListQueuesResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self, context: RequestContext, arn: _string, **kwargs
    ) -> ListTagsForResourceResponse:
        """Retrieve the tags for a MediaConvert resource.

        :param arn: The Amazon Resource Name (ARN) of the resource that you want to list
        tags for.
        :returns: ListTagsForResourceResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("ListVersions")
    def list_versions(
        self,
        context: RequestContext,
        max_results: _integerMin1Max20 | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListVersionsResponse:
        """Retrieve a JSON array of all available Job engine versions and the date
        they expire.

        :param max_results: Optional.
        :param next_token: Optional.
        :returns: ListVersionsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("Probe")
    def probe(
        self, context: RequestContext, input_files: _listOfProbeInputFile | None = None, **kwargs
    ) -> ProbeResponse:
        """Use Probe to obtain detailed information about your input media files.
        Probe returns a JSON that includes container, codec, frame rate,
        resolution, track count, audio layout, captions, and more. You can use
        this information to learn more about your media files, or to help make
        decisions while automating your transcoding workflow.

        :param input_files: Specify a media file to probe.
        :returns: ProbeResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("PutPolicy")
    def put_policy(self, context: RequestContext, policy: Policy, **kwargs) -> PutPolicyResponse:
        """Create or change your policy. For more information about policies, see
        the user guide at
        http://docs.aws.amazon.com/mediaconvert/latest/ug/what-is.html

        :param policy: A policy configures behavior that you allow or disallow for your
        account.
        :returns: PutPolicyResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("SearchJobs")
    def search_jobs(
        self,
        context: RequestContext,
        input_file: _string | None = None,
        max_results: _integerMin1Max20 | None = None,
        next_token: _string | None = None,
        order: Order | None = None,
        queue: _string | None = None,
        status: JobStatus | None = None,
        **kwargs,
    ) -> SearchJobsResponse:
        """Retrieve a JSON array that includes job details for up to twenty of your
        most recent jobs. Optionally filter results further according to input
        file, queue, or status. To retrieve the twenty next most recent jobs,
        use the nextToken string returned with the array.

        :param input_file: Optional.
        :param max_results: Optional.
        :param next_token: Optional.
        :param order: Optional.
        :param queue: Optional.
        :param status: Optional.
        :returns: SearchJobsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("StartJobsQuery")
    def start_jobs_query(
        self,
        context: RequestContext,
        filter_list: _listOfJobsQueryFilter | None = None,
        max_results: _integerMin1Max20 | None = None,
        next_token: _string | None = None,
        order: Order | None = None,
        **kwargs,
    ) -> StartJobsQueryResponse:
        """Start an asynchronous jobs query using the provided filters. To receive
        the list of jobs that match your query, call the GetJobsQueryResults API
        using the query ID returned by this API.

        :param filter_list: Optional.
        :param max_results: Optional.
        :param next_token: Use this string to request the next batch of jobs matched by a jobs
        query.
        :param order: Optional.
        :returns: StartJobsQueryResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, arn: _string, tags: _mapOf__string, **kwargs
    ) -> TagResourceResponse:
        """Add tags to a MediaConvert queue, preset, or job template. For
        information about tagging, see the User Guide at
        https://docs.aws.amazon.com/mediaconvert/latest/ug/tagging-resources.html

        :param arn: The Amazon Resource Name (ARN) of the resource that you want to tag.
        :param tags: The tags that you want to add to the resource.
        :returns: TagResourceResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self,
        context: RequestContext,
        arn: _string,
        tag_keys: _listOf__string | None = None,
        **kwargs,
    ) -> UntagResourceResponse:
        """Remove tags from a MediaConvert queue, preset, or job template. For
        information about tagging, see the User Guide at
        https://docs.aws.amazon.com/mediaconvert/latest/ug/tagging-resources.html

        :param arn: The Amazon Resource Name (ARN) of the resource that you want to remove
        tags from.
        :param tag_keys: The keys of the tags that you want to remove from the resource.
        :returns: UntagResourceResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdateJobTemplate")
    def update_job_template(
        self,
        context: RequestContext,
        name: _string,
        acceleration_settings: AccelerationSettings | None = None,
        category: _string | None = None,
        description: _string | None = None,
        hop_destinations: _listOfHopDestination | None = None,
        priority: _integerMinNegative50Max50 | None = None,
        queue: _string | None = None,
        settings: JobTemplateSettings | None = None,
        status_update_interval: StatusUpdateInterval | None = None,
        **kwargs,
    ) -> UpdateJobTemplateResponse:
        """Modify one of your existing job templates.

        :param name: The name of the job template you are modifying.
        :param acceleration_settings: Accelerated transcoding can significantly speed up jobs with long,
        visually complex content.
        :param category: The new category for the job template, if you are changing it.
        :param description: The new description for the job template, if you are changing it.
        :param hop_destinations: Optional list of hop destinations.
        :param priority: Specify the relative priority for this job.
        :param queue: The new queue for the job template, if you are changing it.
        :param settings: JobTemplateSettings contains all the transcode settings saved in the
        template that will be applied to jobs created from it.
        :param status_update_interval: Specify how often MediaConvert sends STATUS_UPDATE events to Amazon
        CloudWatch Events.
        :returns: UpdateJobTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdatePreset")
    def update_preset(
        self,
        context: RequestContext,
        name: _string,
        category: _string | None = None,
        description: _string | None = None,
        settings: PresetSettings | None = None,
        **kwargs,
    ) -> UpdatePresetResponse:
        """Modify one of your existing presets.

        :param name: The name of the preset you are modifying.
        :param category: The new category for the preset, if you are changing it.
        :param description: The new description for the preset, if you are changing it.
        :param settings: Settings for preset.
        :returns: UpdatePresetResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdateQueue")
    def update_queue(
        self,
        context: RequestContext,
        name: _string,
        concurrent_jobs: _integer | None = None,
        description: _string | None = None,
        reservation_plan_settings: ReservationPlanSettings | None = None,
        status: QueueStatus | None = None,
        **kwargs,
    ) -> UpdateQueueResponse:
        """Modify one of your existing queues.

        :param name: The name of the queue that you are modifying.
        :param concurrent_jobs: Specify the maximum number of jobs your queue can process concurrently.
        :param description: The new description for the queue, if you are changing it.
        :param reservation_plan_settings: The new details of your pricing plan for your reserved queue.
        :param status: Pause or activate a queue by changing its status between ACTIVE and
        PAUSED.
        :returns: UpdateQueueResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ServiceQuotaExceededException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

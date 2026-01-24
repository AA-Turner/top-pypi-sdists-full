# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from cvg_sdk.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from cvg_sdk.model.aggregated_latencies import AggregatedLatencies
from cvg_sdk.model.audio_playback_failed import AudioPlaybackFailed
from cvg_sdk.model.audio_playback_failed_all_of import AudioPlaybackFailedAllOf
from cvg_sdk.model.endpoint_call import EndpointCall
from cvg_sdk.model.endpoint_call_all_of import EndpointCallAllOf
from cvg_sdk.model.endpoint_call_failed import EndpointCallFailed
from cvg_sdk.model.endpoint_call_failed_all_of import EndpointCallFailedAllOf
from cvg_sdk.model.health_event_status import HealthEventStatus
from cvg_sdk.model.health_status import HealthStatus
from cvg_sdk.model.internal_error import InternalError
from cvg_sdk.model.internal_error_all_of import InternalErrorAllOf
from cvg_sdk.model.language import Language
from cvg_sdk.model.project_health import ProjectHealth
from cvg_sdk.model.project_health_event import ProjectHealthEvent
from cvg_sdk.model.provisioning_timed_out import ProvisioningTimedOut
from cvg_sdk.model.speech_service_configuration import SpeechServiceConfiguration
from cvg_sdk.model.speech_service_failed_properties import SpeechServiceFailedProperties
from cvg_sdk.model.synthesis import Synthesis
from cvg_sdk.model.synthesis_failed import SynthesisFailed
from cvg_sdk.model.time_range import TimeRange
from cvg_sdk.model.transcription import Transcription
from cvg_sdk.model.transcription_all_of import TranscriptionAllOf
from cvg_sdk.model.transcription_failed import TranscriptionFailed

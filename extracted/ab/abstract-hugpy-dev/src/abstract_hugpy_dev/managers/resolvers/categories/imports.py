from ..imports import *
from ...generate import DeepCoderChatRunner
from ...vision import VisionRunner
from ...vision.schemas import VisionRequest
from ...llama import LlamaCppChatRunner
from ...summarizers import SummarizeRunner
from ...whisper_model import WhisperRunner, TranscribeRequest
# TTS (chatterbox seat). ``managers.tts`` is lazy (PEP 562 __getattr__), so
# these two names cost the runner import only where the tables are built —
# never on the worker heartbeat path that reads managers.tts.seat.
from ...tts import ChatterboxTtsRunner, TtsRequest

from ...embed import FeatureExtractionRunner, EmbedRequest
# Video (studio seat). Import-light: the runner pays for the studio spine
# inside run(), so these names cost pydantic only where the tables are built.
from ...video_gen import StudioVideoRunner, VideoGenRequest
from ...imagegen import ImageGenRunner, Img2ImgRunner, ImageGenRequest
from ...comfy import ComfyRunner
from ...keywords import KeywordRunner, KeywordTaskRequest
from ...vision_analysis import (
    VisionAnalysisRequest,
    DepthEstimationRunner,
    ObjectDetectionRunner,
    ImageClassificationRunner,
    ImageSegmentationRunner,
)
logger = logging.getLogger(__name__)


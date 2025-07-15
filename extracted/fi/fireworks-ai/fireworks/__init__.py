from .llm import LLM
from .dataset import Dataset
from .evaluator import Evaluator
from .supervised_fine_tuning_job import SupervisedFineTuningJob
from .batch_inference_job import BatchInferenceJob
import importlib.metadata
from reward_kit import reward_function
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from .platform import FireworksPlatform
import fireworks.control_plane.generated.protos.gateway as fw

try:
    __version__ = importlib.metadata.version("fireworks-ai")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback for development mode

__all__ = [
    "LLM",
    "Dataset",
    "Evaluator",
    "SupervisedFineTuningJob",
    "BatchInferenceJob",
    "FireworksPlatform",
    "fw",
    "__version__",
    "reward_function",
    "ChatCompletion",
    "ChatCompletionChunk",
    "ChatCompletionMessageParam",
    "ChatCompletionToolParam",
]

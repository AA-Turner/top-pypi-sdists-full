"""Base types, utilities, and abstract Renderer class for chat template rendering."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Literal, NotRequired, TypedDict, Union, cast


# ─── Tokenizer type alias ────────────────────────────────────────────────

Tokenizer = Any  # PreTrainedTokenizer | PreTrainedTokenizerFast


# ─── Content part types ──────────────────────────────────────────────────

# Image container formats supported end-to-end. Decoding is handled by Pillow
# where dimensions are needed, and server-side processing sniffs the bytes'
# magic header. The ``format`` field is advisory.
ImageFormat = Literal["png", "jpeg", "webp", "gif", "bmp", "tiff"]


class TextPart(TypedDict):
    type: Literal["text"]
    text: str


class ThinkingPart(TypedDict):
    type: Literal["thinking"]
    thinking: str


class ImagePart(TypedDict):
    """A single image inside a multimodal message.

    The renderer needs ``height``/``width`` to compute the number of
    placeholder tokens the image expands to. When they're absent the
    renderer falls back to ``PIL.Image.open(BytesIO(image)).size`` —
    callers preferring to avoid the soft Pillow dependency should
    pass dimensions explicitly via :func:`image_part`.

    The raw image bytes ride through ``forward_backward`` /
    ``sample()`` untouched; image preprocessing happens server-side.
    """

    type: Literal["image"]
    image: bytes
    format: ImageFormat
    height: NotRequired[int]
    width: NotRequired[int]


ContentPart = Union[TextPart, ThinkingPart, ImagePart]


def image_part(
    image: bytes,
    *,
    format: ImageFormat = "png",
    height: int | None = None,
    width: int | None = None,
) -> ImagePart:
    """Build an :class:`ImagePart` from raw image bytes.

    Passing ``height``/``width`` makes the renderer Pillow-free. When
    omitted, the renderer reads them lazily via PIL the first time the
    image is rendered.
    """
    part: ImagePart = {"type": "image", "image": image, "format": format}
    if height is not None:
        part["height"] = height
    if width is not None:
        part["width"] = width
    return part


def image_part_size(part: ImagePart) -> tuple[int, int]:
    """Return ``(height, width)`` for an :class:`ImagePart`.

    Returns explicit fields when present, otherwise decodes the image
    header via Pillow. Raises ``ValueError`` if Pillow is not installed
    or if it cannot decode the bytes — callers that want to avoid the
    soft Pillow dependency should pass ``height``/``width`` explicitly.
    """
    h = part.get("height")
    w = part.get("width")
    if h is not None and w is not None:
        return h, w
    try:
        import io

        from PIL import Image
    except ImportError as exc:
        raise ValueError(
            "ImagePart without explicit height/width requires Pillow "
            "(`pip install pillow`). Alternatively, pass height=... and "
            "width=... to image_part()."
        ) from exc
    try:
        with Image.open(io.BytesIO(part["image"])) as img:
            return img.height, img.width
    except Exception as exc:  # PIL raises UnidentifiedImageError / OSError / etc.
        raise ValueError(
            "ImagePart image bytes could not be decoded by Pillow; pass "
            "height=... and width=... to image_part() to skip decoding."
        ) from exc


# ─── ModelInput chunk types (training wire format) ───────────────────────


class EncodedTextChunk(TypedDict):
    """A run of pre-tokenized text inside a chunked model input."""

    type: Literal["text"]
    tokens: list[int]


class ImageChunk(TypedDict):
    """A single image inside a chunked model input.

    ``data`` is raw image bytes (PNG/JPEG); the worker base64-decodes
    them, runs its ``AutoProcessor``, and verifies that the actual
    feature count matches ``expected_tokens`` before splicing the
    placeholder ids into the LLM stream.
    """

    type: Literal["image"]
    data: bytes
    format: ImageFormat
    expected_tokens: int


ModelInputChunk = Union[EncodedTextChunk, ImageChunk]


# ─── Tool types ──────────────────────────────────────────────────────────


class ToolCallFunction(TypedDict):
    name: str
    # Parsed model output uses a JSON string; callers may provide structured
    # OpenAI-style arguments directly when rendering training examples.
    arguments: str | dict[str, Any]


class ToolCall(TypedDict):
    """Parsed tool invocation from model output."""

    type: Literal["function"]
    id: str | None
    function: ToolCallFunction


class UnparsedToolCall(TypedDict):
    """Tool call that failed to parse."""

    raw_text: str
    error: str


class ToolSpec(TypedDict):
    """OpenAI-format function tool specification."""

    name: str
    description: str
    parameters: dict


# ─── Message type ────────────────────────────────────────────────────────


class Message(TypedDict):
    role: str  # "system", "user", "assistant", "tool"
    content: str | list[ContentPart]
    # OpenAI-compatible reasoning channel. Renderers also accept an inline
    # ``<think>...</think>`` block in ``content`` for callers that do not
    # preserve this field separately.
    reasoning_content: NotRequired[str]
    tool_calls: NotRequired[list[ToolCall]]
    unparsed_tool_calls: NotRequired[list[UnparsedToolCall]]
    tool_call_id: NotRequired[str]
    name: NotRequired[str]


# ─── Training types ─────────────────────────────────────────────────────


class TrainOnWhat(StrEnum):
    """Which assistant messages get loss weight in SFT."""

    LAST_ASSISTANT = "last_assistant"
    ALL_ASSISTANT = "all_assistant"


@dataclass(frozen=True)
class TrainingExample:
    """SFT training datum ready for River's forward_backward API.

    ``input_ids`` and ``weights`` are always aligned to the *expanded*
    sequence the model will see (i.e. for multimodal samples, image
    placeholder slots are already in ``input_ids`` and have weight 0).

    When ``model_input`` is set, the example also carries the chunked
    representation that the server worker rehydrates with its own
    image processor — :meth:`to_dict` then emits the chunked wire form
    rather than the flat ``input_ids`` form. ``input_ids`` is still
    kept for clients that want to inspect tokenization locally.
    """

    input_ids: list[int]
    weights: list[float]
    model_input: list[ModelInputChunk] | None = None

    def __post_init__(self):
        if len(self.input_ids) != len(self.weights):
            raise ValueError(
                f"input_ids length ({len(self.input_ids)}) != "
                f"weights length ({len(self.weights)})"
            )
        if self.model_input is not None:
            expanded = 0
            for chunk in self.model_input:
                if chunk["type"] == "text":
                    expanded += len(chunk["tokens"])
                elif chunk["type"] == "image":
                    expanded += chunk["expected_tokens"]
                else:  # pragma: no cover — TypedDict guards prevent this
                    raise ValueError(f"Unknown chunk type: {chunk}")
            if expanded != len(self.input_ids):
                raise ValueError(
                    f"model_input expanded length ({expanded}) does not "
                    f"match input_ids length ({len(self.input_ids)}). "
                    "weights/input_ids must align to the expanded sequence."
                )

    @property
    def num_loss_tokens(self) -> int:
        return sum(1 for w in self.weights if w > 0)

    def to_dict(
        self,
        normalize_weights: bool = True,
        shift_weights_for_pre_shift_loss: bool = True,
    ) -> dict:
        """Convert to dict for model.forward_backward(loss_fn='cross_entropy').

        Args:
            normalize_weights: If True, normalize weights to sum to 1.0
                per example (token-mean loss). Matches default behavior.
            shift_weights_for_pre_shift_loss: If True (default), shift
                the per-token ``weights`` array left by one before
                emitting. See the discussion below.

        **Why the shift.** Internally the renderer assigns
        ``weights[i] = 1.0`` to *completion-token positions* — the
        ergonomic convention where "the weight is on the
        token you care about". But River's ``cross_entropy_loss``
        follows a *pre-shift* contract: ``weights[i]`` is the weight
        for the prediction *emitted at position i*, whose target is
        ``input_ids[i+1]`` (the auto-shifted next-token derived by the
        worker's ``_finalize_loss_inputs``). To train the model to
        emit completion token C at position K (i.e. produce it from
        the hidden state at position K-1), the wire weight needs to
        sit at K-1, not K.

        Without this shift, every completion token's signal gets
        misaligned by one position. For long completions the error is
        a small relative loss (you lose the first-token signal and
        gain a phantom "predict-beyond-end" position that gets zeroed
        anyway); for one-token completions the entire training signal
        is lost (you only ever train the model to emit EOS after the
        completion, which an instruction-tuned model already does
        with P ≈ 1.0 → loss ≈ 0).

        Returns:
            Dict with ``weights`` (left-shifted) plus either
            ``model_input`` (chunked, multimodal) or
            ``input_ids``+``attention_mask`` (flat, text-only). The
            worker rehydrates chunked inputs; flat inputs go through
            the legacy text-only path.
        """
        weights = list(self.weights)
        if normalize_weights:
            total = sum(weights)
            if total > 0:
                weights = [w / total for w in weights]
        if shift_weights_for_pre_shift_loss:
            # weights[i] should weight the *prediction* at position i,
            # whose target is the original weights[i+1]. The trailing
            # position has no valid next-token target and is force-zero
            # in the worker's ``_finalize_loss_inputs`` regardless, so
            # we set it to 0 here too for clarity.
            if len(weights) > 0:
                weights = weights[1:] + [0.0]
        if self.model_input is not None:
            return {
                "model_input": [dict(chunk) for chunk in self.model_input],
                "weights": weights,
            }
        return {
            "input_ids": list(self.input_ids),
            "attention_mask": [1] * len(self.input_ids),
            "weights": weights,
        }


@dataclass(frozen=True)
class SamplePrompt:
    """Inference-ready prompt for ``model.sample(...)``.

    Vision-aware renderers emit a fully expanded prompt string with
    per-image placeholder runs already in place, alongside a parallel
    list of raw image bytes. The client base64-encodes the images and
    ships them in ``InferencePrompt.images`` for inference.
    """

    prompt: str
    images: list[bytes] = field(default_factory=list)
    image_formats: list[str] = field(default_factory=list)

    def __post_init__(self):
        if len(self.images) != len(self.image_formats):
            raise ValueError(
                f"images length ({len(self.images)}) != image_formats "
                f"length ({len(self.image_formats)})"
            )

    def to_kwargs(self) -> dict:
        """Return kwargs ready to splat into ``model.sample(...)``.

        We deliberately omit ``image_formats`` from the splat: the image format
        is inferred from the bytes' magic header, and the wire format has no
        slot for it, so passing it through the public API would be silently
        advisory. The field is still carried on the :class:`SamplePrompt`
        dataclass itself for introspection / caching keys, but doesn't traverse
        the API.
        """
        out: dict = {"prompt": self.prompt}
        if self.images:
            out["images"] = list(self.images)
        return out


@dataclass(frozen=True)
class ParsedResponse:
    """Result of parsing a raw model response string."""

    message: Message
    stop_found: bool


# ─── Chunked-training-example helpers ────────────────────────────────────


class _ChunkBuilder:
    """Stream text tokens into a single :class:`EncodedTextChunk` until
    an image arrives, then flush.

    Keeps a parallel flat ``input_ids``/``weights`` for inspection so
    callers can print decoded prompts without rehydrating chunks.
    Model-agnostic: vision renderers (Qwen, Kimi) share it.
    """

    def __init__(self) -> None:
        self.chunks: list[ModelInputChunk] = []
        self.weights: list[float] = []
        self.flat_ids: list[int] = []
        self._buf_ids: list[int] = []
        self._buf_weights: list[float] = []

    def add_text(self, tokens: list[int], weight: float) -> None:
        self._buf_ids.extend(tokens)
        self._buf_weights.extend([weight] * len(tokens))

    def _flush(self) -> None:
        if self._buf_ids:
            self.chunks.append(
                EncodedTextChunk(type="text", tokens=list(self._buf_ids))
            )
            self.weights.extend(self._buf_weights)
            self.flat_ids.extend(self._buf_ids)
            self._buf_ids = []
            self._buf_weights = []

    def add_image(
        self,
        *,
        data: bytes,
        format: str,
        expected_tokens: int,
        placeholder_id: int,
    ) -> None:
        self._flush()
        self.chunks.append(
            ImageChunk(
                type="image",
                data=data,
                format=cast("ImageFormat", format),
                expected_tokens=expected_tokens,
            )
        )
        self.weights.extend([0.0] * expected_tokens)
        self.flat_ids.extend([placeholder_id] * expected_tokens)

    def finish(self) -> None:
        self._flush()


def _truncate_chunks_to_length(
    chunks: list[ModelInputChunk], max_length: int
) -> tuple[list[ModelInputChunk], int]:
    """Trim a chunk list so its expanded length is <= ``max_length``.

    Drops trailing chunks; if truncation lands mid-text-chunk, the last
    chunk is shortened. Image chunks cannot be partially kept — the
    worker materializer needs the whole image to compute
    ``pixel_values`` rows, and partial placeholder runs would put
    ``input_ids`` out of sync with the ViT feature count. If a full
    image doesn't fit, the image (and every chunk after it) is
    dropped.

    Returns ``(truncated_chunks, expanded_length)`` — the second value
    is the actual expanded length of the returned chunks, which can be
    *less than* ``max_length`` when the cut falls on an image boundary.
    Callers should slice their flat ``input_ids`` / ``weights`` to
    ``expanded_length`` (not ``max_length``) so the chunked form and
    the flat form stay in lock-step with what
    :meth:`TrainingExample.__post_init__` validates.
    """
    out: list[ModelInputChunk] = []
    expanded = 0
    for chunk in chunks:
        remaining = max_length - expanded
        if remaining <= 0:
            break
        if chunk["type"] == "text":
            tokens = chunk["tokens"]
            if len(tokens) <= remaining:
                out.append(chunk)
                expanded += len(tokens)
            else:
                out.append(EncodedTextChunk(type="text", tokens=tokens[:remaining]))
                expanded += remaining
                break
        elif chunk["type"] == "image":
            if chunk["expected_tokens"] <= remaining:
                out.append(chunk)
                expanded += chunk["expected_tokens"]
            else:
                # Can't partially materialize an image — drop it and bail.
                break
    return out, expanded


# ─── Generic content utilities ───────────────────────────────────────────


def remove_thinking(parts: list[ContentPart]) -> list[ContentPart]:
    """Filter out ThinkingPart elements."""
    return [p for p in parts if p["type"] != "thinking"]


def get_text_content(message: Message) -> str:
    """Extract text content from a message, ignoring thinking/image parts."""
    content = message["content"]
    if isinstance(content, str):
        return content
    return "".join(p["text"] for p in content if p["type"] == "text")


# ─── Abstract base class ────────────────────────────────────────────────


class Renderer(ABC):
    """Abstract base for chat template renderers.

    Stateless: holds a tokenizer and configuration, no mutable state.
    """

    def __init__(self, tokenizer: Tokenizer) -> None:
        self.tokenizer = tokenizer

    @abstractmethod
    def build_prompt_str(
        self,
        messages: list[Message],
        *,
        tools: list[ToolSpec] | None = None,
    ) -> str:
        """Render a conversation into a prompt string for model.sample().

        Args:
            messages: Conversation history.
            tools: Optional tool specs to inject into the system message.

        Returns:
            Complete prompt string including generation prompt.
        """
        ...

    def build_text_prompt(
        self,
        messages: list[Message],
        *,
        tools: list[ToolSpec] | None = None,
    ) -> str:
        """Deprecated alias for ``build_prompt_str``."""
        return self.build_prompt_str(messages, tools=tools)

    def build_sample_prompt(
        self,
        messages: list[Message],
        *,
        tools: list[ToolSpec] | None = None,
    ) -> SamplePrompt:
        """Render a conversation for inference (``model.sample``).

        Default implementation is text-only: delegates to
        :meth:`build_prompt_str` and returns a :class:`SamplePrompt`
        with no images. Vision-aware renderers override to emit the
        per-image placeholder runs in ``prompt`` and collect the raw
        image bytes in :attr:`SamplePrompt.images`.
        """
        return SamplePrompt(
            prompt=self.build_prompt_str(messages, tools=tools),
            images=[],
            image_formats=[],
        )

    @abstractmethod
    def get_stop_strings(self) -> list[str]:
        """Return stop strings for model.sample(stop=...)."""
        ...

    @abstractmethod
    def parse_response(self, text: str) -> ParsedResponse:
        """Parse sampled text into a structured Message.

        Parses renderer-specific response syntax and strips stop strings.

        Args:
            text: Raw text from Sample.text.

        Returns:
            ParsedResponse with structured message and stop_found flag.
        """
        ...

    @abstractmethod
    def build_training_example(
        self,
        messages: list[Message],
        *,
        train_on: TrainOnWhat = TrainOnWhat.LAST_ASSISTANT,
        train_on_eos: bool = True,
        max_length: int | None = None,
        tools: list[ToolSpec] | None = None,
    ) -> TrainingExample:
        """Build tokenized input_ids and per-token weights for SFT.

        Headers get weight=0. Content of trainable messages gets weight=1.

        Args:
            messages: Full conversation including assistant response to train on.
            train_on: Which assistant messages get weight=1.
            train_on_eos: Whether to include the stop token in trainable weights.
            max_length: Optional max sequence length (truncates from end).
            tools: Optional tool definitions rendered into the training prompt.

        Returns:
            TrainingExample with input_ids and weights.
        """
        ...

    def build_system_message_with_tools(
        self, tools: list[ToolSpec], system_prompt: str = ""
    ) -> Message:
        """Create a system message with tool specifications.

        Default raises NotImplementedError. Override for tool support.
        """
        raise NotImplementedError(
            f"{type(self).__name__} does not support tool calling"
        )

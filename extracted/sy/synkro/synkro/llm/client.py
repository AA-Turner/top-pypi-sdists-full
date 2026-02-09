"""Type-safe LLM wrapper using LiteLLM."""

import asyncio
import json
import re
import warnings
from typing import TYPE_CHECKING, Optional, Type, TypeVar, overload

from pydantic import BaseModel, ValidationError

from synkro.models import LocalModel, Model, OpenAI, get_model_string

# Lazy LiteLLM import to avoid import-time side effects (important for CLIs/tests)
_LITELLM_CONFIGURED = False


def _get_litellm():
    global _LITELLM_CONFIGURED

    import litellm
    from litellm import acompletion, completion_cost, supports_response_schema

    if not _LITELLM_CONFIGURED:
        litellm.suppress_debug_info = True
        litellm.enable_json_schema_validation = True
        litellm.drop_params = True  # Drop unsupported params (e.g., temperature for gpt-5)
        _LITELLM_CONFIGURED = True

    return litellm, acompletion, completion_cost, supports_response_schema


# Retry configuration for rate limits
MAX_RETRIES = 5
INITIAL_BACKOFF = 1.0  # seconds
MAX_BACKOFF = 60.0  # seconds


async def _retry_with_backoff(coro_func, *args, **kwargs):
    """Execute async function with exponential backoff on rate limit errors."""
    backoff = INITIAL_BACKOFF
    last_exception = None

    for attempt in range(MAX_RETRIES):
        try:
            return await coro_func(*args, **kwargs)
        except Exception as e:
            error_str = str(e).lower()
            # Check for rate limit errors (429, resource exhausted, rate limit)
            is_rate_limit = (
                "429" in error_str
                or "rate" in error_str
                or "resource exhausted" in error_str
                or "ratelimit" in error_str
            )
            if not is_rate_limit:
                raise  # Not a rate limit error, don't retry

            last_exception = e
            if attempt < MAX_RETRIES - 1:
                # Exponential backoff with jitter
                import random

                jitter = random.uniform(0, backoff * 0.1)
                sleep_time = min(backoff + jitter, MAX_BACKOFF)
                await asyncio.sleep(sleep_time)
                backoff *= 2  # Exponential increase

    # All retries exhausted
    raise last_exception


if TYPE_CHECKING:
    from synkro.types.metrics import Metrics, TrackedLLM

# Suppress Pydantic serialization warnings from litellm response types
warnings.filterwarnings(
    "ignore",
    message=".*Pydantic serializer warnings.*",
    category=UserWarning,
)
warnings.filterwarnings(
    "ignore",
    message=".*Expected `Message`.*",
    category=UserWarning,
)
warnings.filterwarnings(
    "ignore",
    message=".*Expected `StreamingChoices`.*",
    category=UserWarning,
)

T = TypeVar("T", bound=BaseModel)


def _is_local_model_with_native_format(model: str) -> bool:
    """Check if model is a local provider that supports native structured output."""
    return model.startswith(("ollama/", "vllm/"))


# Repair prompt for validation retries
_REPAIR_PROMPT = """Fix this JSON to match the required schema.

Original JSON:
{raw_json}

Validation Errors:
{errors}

Required Schema:
{schema}

Return ONLY the corrected JSON, no explanation."""

_FALLBACK_PROMPT = """You must respond with valid JSON matching this schema:

{schema}

User request:
{prompt}

Return ONLY valid JSON, no explanation or markdown."""


class SchemaValidationError(Exception):
    """Raised when JSON has extra fields not in schema."""

    def __init__(self, extra_fields: list, message: str):
        self.extra_fields = extra_fields
        super().__init__(message)


def _get_expected_fields(schema: dict) -> set:
    """Extract expected field names from JSON schema."""
    fields = set()
    if "properties" in schema:
        fields.update(schema["properties"].keys())
    return fields


def _resolve_ref(ref: str, defs: dict) -> dict:
    """Resolve a $ref to its definition."""
    # ref format: "#/$defs/ClassName"
    if ref.startswith("#/$defs/"):
        def_name = ref.split("/")[-1]
        return defs.get(def_name, {})
    return {}


def _find_extra_fields(data: dict, schema: dict, path: str = "", defs: dict | None = None) -> list:
    """Recursively find fields in data that aren't in schema."""
    # Get $defs from root schema on first call
    if defs is None:
        defs = schema.get("$defs", {})

    extras = []
    expected = _get_expected_fields(schema)

    for key in data.keys():
        full_path = f"{path}.{key}" if path else key
        if key not in expected:
            extras.append(full_path)
        elif isinstance(data[key], dict):
            # Get nested schema, resolving $ref if needed
            nested_schema = schema.get("properties", {}).get(key, {})
            if "$ref" in nested_schema:
                nested_schema = _resolve_ref(nested_schema["$ref"], defs)
            if "properties" in nested_schema:
                extras.extend(_find_extra_fields(data[key], nested_schema, full_path, defs))
        elif isinstance(data[key], list):
            # Get array item schema, resolving $ref if needed
            item_schema = schema.get("properties", {}).get(key, {}).get("items", {})
            if "$ref" in item_schema:
                item_schema = _resolve_ref(item_schema["$ref"], defs)
            if "properties" in item_schema:
                for i, item in enumerate(data[key]):
                    if isinstance(item, dict):
                        extras.extend(
                            _find_extra_fields(item, item_schema, f"{full_path}[{i}]", defs)
                        )

    return extras


def _strip_extra_fields(data: dict, schema: dict, defs: dict | None = None) -> dict:
    """Recursively remove fields from data that aren't in schema.

    This is a programmatic fix for models that add extra fields - no LLM needed.
    Works with nested objects and arrays.
    """
    # Get $defs from root schema on first call
    if defs is None:
        defs = schema.get("$defs", {})

    expected = _get_expected_fields(schema)
    result = {}

    for key, value in data.items():
        if key not in expected:
            continue  # Skip extra fields

        if isinstance(value, dict):
            # Get nested schema, resolving $ref if needed
            nested_schema = schema.get("properties", {}).get(key, {})
            if "$ref" in nested_schema:
                nested_schema = _resolve_ref(nested_schema["$ref"], defs)
            if "properties" in nested_schema:
                # Recursively strip nested object
                result[key] = _strip_extra_fields(value, nested_schema, defs)
            else:
                result[key] = value
        elif isinstance(value, list):
            # Get array item schema, resolving $ref if needed
            item_schema = schema.get("properties", {}).get(key, {}).get("items", {})
            if "$ref" in item_schema:
                item_schema = _resolve_ref(item_schema["$ref"], defs)
            if "properties" in item_schema:
                # Recursively strip each array item
                result[key] = [
                    _strip_extra_fields(item, item_schema, defs) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                result[key] = value
        else:
            result[key] = value

    return result


def _sanitize_json_strings(content: str) -> str:
    """Escape unescaped control characters inside JSON string values."""
    result = []
    in_string = False
    escape_next = False

    for c in content:
        if escape_next:
            result.append(c)
            escape_next = False
            continue

        if c == "\\" and in_string:
            result.append(c)
            escape_next = True
            continue

        if c == '"':
            in_string = not in_string
            result.append(c)
        elif in_string and ord(c) < 32:
            # Escape control characters inside strings
            if c == "\n":
                result.append("\\n")
            elif c == "\r":
                result.append("\\r")
            elif c == "\t":
                result.append("\\t")
            else:
                # Other control chars - use unicode escape
                result.append(f"\\u{ord(c):04x}")
        else:
            result.append(c)

    return "".join(result)


def _clean_json_content(content: str) -> str:
    """Strip markdown fences, extract JSON, and sanitize control characters."""
    # Strip markdown code fences (```json ... ```)
    content = re.sub(r"```json\s*", "", content)
    content = re.sub(r"```\s*", "", content)
    content = content.strip()

    # Extract JSON if embedded in other text
    extracted = content
    if not (content.startswith("{") or content.startswith("[")):
        # Try to extract JSON object or array from surrounding text
        for start_char, end_char in [("{", "}"), ("[", "]")]:
            start = content.find(start_char)
            if start == -1:
                continue

            depth = 0
            in_string = False
            escape = False

            for i in range(start, len(content)):
                char = content[i]

                if escape:
                    escape = False
                    continue
                if char == "\\" and in_string:
                    escape = True
                    continue
                if char == '"':
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if char == start_char:
                    depth += 1
                if char == end_char:
                    depth -= 1
                if depth == 0:
                    extracted = content[start : i + 1]
                    break
            if extracted != content:
                break

    # Sanitize control characters inside JSON strings
    return _sanitize_json_strings(extracted)


def _validate_strict(content: str, response_model: Type[T]) -> T:
    """Validate JSON strictly - strip extra fields programmatically, then run Pydantic.

    Extra fields are removed automatically (no LLM needed). Only type errors
    will propagate for potential LLM repair.
    """
    # Clean content: strip markdown fences and extract JSON
    content = _clean_json_content(content)
    data = json.loads(content)
    schema = response_model.model_json_schema()

    # Programmatically strip extra fields - no LLM needed for this
    data = _strip_extra_fields(data, schema)

    # Now run Pydantic for type validation (may raise ValidationError)
    return response_model.model_validate(data)


def _format_validation_errors(e: Exception) -> str:
    """Convert validation errors to actionable feedback."""
    if isinstance(e, SchemaValidationError):
        lines = ["The JSON response had extra fields not in the schema:"]
        for field in e.extra_fields:
            lines.append(f"  - Remove field: '{field}'")
        return "\n".join(lines)

    # JSON syntax error
    if isinstance(e, json.JSONDecodeError):
        return (
            f"The JSON response has a syntax error: {e.msg} at line {e.lineno} column {e.colno}.\n"
            "Please fix the JSON syntax and return valid JSON."
        )

    # Pydantic ValidationError
    if isinstance(e, ValidationError):
        lines = ["The JSON response had validation errors:"]
        for err in e.errors():
            loc = " -> ".join(str(x) for x in err["loc"])
            msg = err["msg"]
            lines.append(f"  - Field '{loc}': {msg}")
        return "\n".join(lines)

    # Fallback
    return str(e)


class LLM:
    """
    Type-safe LLM wrapper using LiteLLM for universal provider support.

    Supports structured outputs via native JSON mode for reliable responses.

    Supported providers: OpenAI, Anthropic, Google (Gemini), Local (Ollama, vLLM)

    Examples:
        >>> from synkro import LLM, OpenAI, Anthropic, Google, Local

        # Use OpenAI
        >>> llm = LLM(model=OpenAI.GPT_4O_MINI)
        >>> response = await llm.generate("Hello!")

        # Use Anthropic
        >>> llm = LLM(model=Anthropic.CLAUDE_35_SONNET)

        # Use Google Gemini
        >>> llm = LLM(model=Google.GEMINI_25_FLASH)

        # Use local Ollama
        >>> llm = LLM(model=Local.OLLAMA("llama3.1"))

        # Use local vLLM
        >>> llm = LLM(model=Local.VLLM("mistral"))

        # Structured output
        >>> class Output(BaseModel):
        ...     answer: str
        ...     confidence: float
        >>> result = await llm.generate_structured("What is 2+2?", Output)
        >>> result.answer
        '4'
    """

    def __init__(
        self,
        model: Model = OpenAI.GPT_4O_MINI,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        validation_model: Optional["LLM"] = None,
        validation_retries: int = 0,
    ):
        """
        Initialize the LLM client.

        Args:
            model: Model to use (enum, LocalModel, or string)
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate (default: None = model's max)
            api_key: Optional API key override
            base_url: Optional API base URL (auto-set when using Local models)
            validation_model: Default LLM to use for repairing invalid structured outputs
            validation_retries: Default number of validation retry attempts (0 = no retries)
        """
        # Handle LocalModel - extract endpoint automatically
        if isinstance(model, LocalModel):
            self.model = f"{model.provider}/{model.model}"
            self._base_url = model.endpoint
        else:
            self.model = get_model_string(model)
            self._base_url = base_url

        self.temperature = temperature
        self.max_tokens = max_tokens
        self._api_key = api_key

        # Validation defaults for structured outputs
        self._validation_model = validation_model
        self._validation_retries = validation_retries

        # Cost and usage tracking
        self._total_cost = 0.0
        self._call_count = 0

    async def generate(self, prompt: str, system: str | None = None) -> str:
        """
        Generate a text response.

        Args:
            prompt: The user prompt
            system: Optional system prompt

        Returns:
            Generated text response
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "api_key": self._api_key,
        }
        if self.max_tokens is not None:
            kwargs["max_tokens"] = self.max_tokens
        if self._base_url:
            kwargs["api_base"] = self._base_url

        _, acompletion, _, _ = _get_litellm()
        response = await _retry_with_backoff(acompletion, **kwargs)
        self._track_cost(response)
        return response.choices[0].message.content

    async def generate_batch(self, prompts: list[str], system: str | None = None) -> list[str]:
        """
        Generate responses for multiple prompts in parallel.

        Args:
            prompts: List of user prompts
            system: Optional system prompt for all

        Returns:
            List of generated responses
        """
        import asyncio

        tasks = [self.generate(p, system) for p in prompts]
        return await asyncio.gather(*tasks)

    @overload
    async def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        system: str | None = None,
        temperature: float | None = None,
        validation_retries: int | None = None,
        validation_model: Optional["LLM"] = None,
        strict: bool = True,
    ) -> T: ...

    @overload
    async def generate_structured(
        self,
        prompt: str,
        response_model: Type[list[T]],
        system: str | None = None,
        temperature: float | None = None,
        validation_retries: int | None = None,
        validation_model: Optional["LLM"] = None,
        strict: bool = True,
    ) -> list[T]: ...

    async def generate_structured(
        self,
        prompt: str,
        response_model: Type[T] | Type[list[T]],
        system: str | None = None,
        temperature: float | None = None,
        validation_retries: int | None = None,
        validation_model: Optional["LLM"] = None,
        strict: bool = True,
    ) -> T | list[T]:
        """
        Generate a structured response matching a Pydantic model.

        Uses LiteLLM's native JSON mode with response_format for
        reliable structured outputs.

        Args:
            prompt: The user prompt
            response_model: Pydantic model class for the response
            system: Optional system prompt
            temperature: Optional temperature override
            validation_retries: Number of retry attempts on validation failure.
                If None, uses instance default (set in __init__).
            validation_model: Optional separate LLM to use for repairing invalid JSON.
                If None, uses instance default or self. Use a stronger model for better repairs.
            strict: If True (default), reject extra fields not in schema.
                If False, use Pydantic's default behavior (ignore extra fields).

        Returns:
            Parsed response matching the model

        Example:
            >>> class Analysis(BaseModel):
            ...     sentiment: str
            ...     score: float
            >>> result = await llm.generate_structured(
            ...     "Analyze: I love this product!",
            ...     Analysis
            ... )
            >>> result.sentiment
            'positive'

            # With validation retries for unreliable models:
            >>> result = await llm.generate_structured(
            ...     prompt,
            ...     Analysis,
            ...     validation_retries=3,
            ...     validation_model=stronger_llm,
            ... )
        """
        # Use instance defaults if not specified
        if validation_retries is None:
            validation_retries = self._validation_retries
        if validation_model is None:
            validation_model = self._validation_model

        # Check if model supports structured outputs
        _, _, _, supports_response_schema = _get_litellm()
        use_fallback = False

        if not supports_response_schema(model=self.model, custom_llm_provider=None):
            # Ollama/vLLM support structured output natively.
            if _is_local_model_with_native_format(self.model):
                use_fallback = False
            else:
                warnings.warn(
                    f"Model '{self.model}' may not support structured outputs. "
                    f"Falling back to prompt-based JSON generation with validation.",
                    UserWarning,
                )
                use_fallback = True
                # Auto-enable retries for fallback mode if not already set
                if validation_retries == 0:
                    validation_retries = 3

        if use_fallback:
            # Fallback: embed schema in prompt and use regular generate
            schema_text = response_model.model_json_schema()
            fallback_prompt = _FALLBACK_PROMPT.format(
                schema=json.dumps(schema_text, indent=2),
                prompt=prompt,
            )
            if system:
                fallback_prompt = f"{system}\n\n{fallback_prompt}"
            content = await self.generate(fallback_prompt)
        else:
            # Use LiteLLM's native response_format with Pydantic model
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            kwargs = {
                "model": self.model,
                "messages": messages,
                "response_format": response_model,
                "temperature": temperature if temperature is not None else self.temperature,
                "api_key": self._api_key,
            }
            if self.max_tokens is not None:
                kwargs["max_tokens"] = self.max_tokens
            if self._base_url:
                kwargs["api_base"] = self._base_url

            _, acompletion, _, _ = _get_litellm()
            response = await _retry_with_backoff(acompletion, **kwargs)
            self._track_cost(response)
            content = response.choices[0].message.content

        # Clean content once before validation loop
        content = _clean_json_content(content)

        # Validation with optional retries
        for attempt in range(validation_retries + 1):
            try:
                if strict:
                    return _validate_strict(content, response_model)
                else:
                    return response_model.model_validate_json(content)
            except (ValidationError, SchemaValidationError, json.JSONDecodeError) as e:
                if attempt >= validation_retries:
                    raise  # No more retries, propagate the error

                # Use validation_model (or self) to repair the JSON
                repair_llm = validation_model or self
                error_text = _format_validation_errors(e)
                schema_text = response_model.model_json_schema()

                repair_prompt = _REPAIR_PROMPT.format(
                    raw_json=content,
                    errors=error_text,
                    schema=json.dumps(schema_text, indent=2),
                )

                # Get repaired JSON from validation model and clean it
                content = _clean_json_content(await repair_llm.generate(repair_prompt))

        # Should never reach here, but satisfy type checker
        if strict:
            return _validate_strict(content, response_model)
        return response_model.model_validate_json(content)

    async def generate_chat(
        self,
        messages: list[dict],
        response_model: Type[T] | None = None,
        validation_retries: int = 0,
        validation_model: Optional["LLM"] = None,
        strict: bool = True,
    ) -> str | T:
        """
        Generate a response for a full conversation.

        Args:
            messages: List of message dicts with 'role' and 'content'
            response_model: Optional Pydantic model for structured output
            validation_retries: Number of retry attempts on validation failure (default: 0)
            validation_model: Optional separate LLM to use for repairing invalid JSON
            strict: If True (default), reject extra fields not in schema.

        Returns:
            Generated response (string or structured)
        """
        if response_model:
            # Check if model supports structured outputs
            _, _, _, supports_response_schema = _get_litellm()
            use_fallback = False

            if not supports_response_schema(model=self.model, custom_llm_provider=None):
                if _is_local_model_with_native_format(self.model):
                    use_fallback = False
                else:
                    warnings.warn(
                        f"Model '{self.model}' may not support structured outputs. "
                        f"Falling back to prompt-based JSON generation with validation.",
                        UserWarning,
                    )
                    use_fallback = True
                    if validation_retries == 0:
                        validation_retries = 3

            if use_fallback:
                # Fallback: append schema request to last message
                schema_text = response_model.model_json_schema()
                fallback_messages = list(messages)
                last_content = fallback_messages[-1].get("content", "")
                fallback_messages[-1] = {
                    **fallback_messages[-1],
                    "content": _FALLBACK_PROMPT.format(
                        schema=json.dumps(schema_text, indent=2),
                        prompt=last_content,
                    ),
                }
                kwargs = {
                    "model": self.model,
                    "messages": fallback_messages,
                    "temperature": self.temperature,
                    "api_key": self._api_key,
                }
                if self.max_tokens is not None:
                    kwargs["max_tokens"] = self.max_tokens
                if self._base_url:
                    kwargs["api_base"] = self._base_url
                _, acompletion, _, _ = _get_litellm()
                response = await _retry_with_backoff(acompletion, **kwargs)
                self._track_cost(response)
                content = response.choices[0].message.content
            else:
                # Use LiteLLM's native response_format with Pydantic model
                kwargs = {
                    "model": self.model,
                    "messages": messages,
                    "response_format": response_model,
                    "temperature": self.temperature,
                    "api_key": self._api_key,
                }
                if self.max_tokens is not None:
                    kwargs["max_tokens"] = self.max_tokens
                if self._base_url:
                    kwargs["api_base"] = self._base_url

                _, acompletion, _, _ = _get_litellm()
                response = await _retry_with_backoff(acompletion, **kwargs)
                self._track_cost(response)
                content = response.choices[0].message.content

            # Clean content once before validation loop
            content = _clean_json_content(content)

            # Validation with optional retries
            for attempt in range(validation_retries + 1):
                try:
                    if strict:
                        return _validate_strict(content, response_model)
                    else:
                        return response_model.model_validate_json(content)
                except (ValidationError, SchemaValidationError, json.JSONDecodeError) as e:
                    if attempt >= validation_retries:
                        raise  # No more retries, propagate the error

                    # Use validation_model (or self) to repair the JSON
                    repair_llm = validation_model or self
                    error_text = _format_validation_errors(e)
                    schema_text = response_model.model_json_schema()

                    repair_prompt = _REPAIR_PROMPT.format(
                        raw_json=content,
                        errors=error_text,
                        schema=json.dumps(schema_text, indent=2),
                    )

                    # Get repaired JSON from validation model and clean it
                    content = _clean_json_content(await repair_llm.generate(repair_prompt))

            # Should never reach here, but satisfy type checker
            if strict:
                return _validate_strict(content, response_model)
            return response_model.model_validate_json(content)

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "api_key": self._api_key,
        }
        if self.max_tokens is not None:
            kwargs["max_tokens"] = self.max_tokens
        if self._base_url:
            kwargs["api_base"] = self._base_url

        _, acompletion, _, _ = _get_litellm()
        response = await _retry_with_backoff(acompletion, **kwargs)
        self._track_cost(response)
        return response.choices[0].message.content

    def _track_cost(self, response) -> None:
        """Track cost and call count from a response."""
        self._call_count += 1
        try:
            _, _, completion_cost, _ = _get_litellm()
            cost = completion_cost(completion_response=response)
            self._total_cost += cost
        except Exception:
            # Some models may not have pricing info
            pass

    @property
    def total_cost(self) -> float:
        """Get total cost of all LLM calls made by this client."""
        return self._total_cost

    @property
    def call_count(self) -> int:
        """Get total number of LLM calls made by this client."""
        return self._call_count

    def reset_tracking(self) -> None:
        """Reset cost and call tracking."""
        self._total_cost = 0.0
        self._call_count = 0

    def reset_call_count(self) -> None:
        """Reset only the call count, preserving cost tracking."""
        self._call_count = 0

    def with_metrics(self, metrics: "Metrics", phase: str) -> "TrackedLLM":
        """Create a tracked wrapper that records to an external Metrics object.

        Use this to track costs across multiple LLM clients into a unified
        Metrics instance.

        Args:
            metrics: External Metrics object to track to
            phase: Phase name for tracking (e.g., "extraction", "scenarios")

        Returns:
            TrackedLLM wrapper that proxies calls and records metrics

        Examples:
            >>> metrics = Metrics()
            >>> tracked = llm.with_metrics(metrics, phase="extraction")
            >>> result = await tracked.generate("Hello")
            >>> print(metrics.get_phase("extraction").cost)
        """
        from synkro.types.metrics import TrackedLLM

        return TrackedLLM(self, metrics, phase)

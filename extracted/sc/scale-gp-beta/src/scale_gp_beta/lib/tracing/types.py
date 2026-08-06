from typing_extensions import Any, Dict, Literal

SpanInputParam = Dict[str, Any]
SpanOutputParam = Dict[str, Any]
SpanMetadataParam = Dict[str, Any]
ErrorCategory = Literal["application", "platform", "unknown"]

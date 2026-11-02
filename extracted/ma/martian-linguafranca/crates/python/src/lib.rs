use linguafranca::anthropic::convert::collect::collector::AnthropicCollector;
use linguafranca::anthropic::convert::stream::{
    AnthropicMessagesToOpenResponsesStream, OpenResponsesToAnthropicMessagesStream,
};
use linguafranca::anthropic::request::AnthropicRequest;
use linguafranca::anthropic::response::AnthropicResponse;
use linguafranca::chat_completions_openai::convert::collect::collector::ChatCompletionsCollector;
use linguafranca::chat_completions_openai::convert::stream::{
    ChatCompletionsToOpenResponsesStream, OpenResponsesToChatCompletionsStream,
};
use linguafranca::chat_completions_openai::request::ChatCompletionsOpenAiRequest;
use linguafranca::chat_completions_openai::response::ChatCompletionsOpenAiResponse;
use linguafranca::collect::DynResponseCollector;
use linguafranca::config::ConversionConfig;
use linguafranca::error::{ConversionError, ConversionResult, ConversionWarning, WarningAction};
use linguafranca::open_responses::convert::collect::collector::OpenResponsesCollector;
use linguafranca::open_responses::request::OpenResponsesRequest;
use linguafranca::open_responses::response::OpenResponsesResponse;
use linguafranca::stream::composed::ComposedStream;
use linguafranca::stream::dynamic::DynStreamTransform;
use linguafranca::traits::{DecomposeToStream, FromOpenResponses, IntoOpenResponses};
use pyo3::create_exception;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum FormatName {
    OpenResponses,
    OpenAiChatCompletions,
    AnthropicMessages,
}

impl TryFrom<&str> for FormatName {
    type Error = ConversionError;

    fn try_from(value: &str) -> Result<Self, Self::Error> {
        match value {
            "open_responses" => Ok(Self::OpenResponses),
            "openai_chat_completions" => Ok(Self::OpenAiChatCompletions),
            "anthropic_messages" => Ok(Self::AnthropicMessages),
            _ => Err(ConversionError::InvalidInput(format!(
                "unknown format name: {value}. Supported formats: open_responses, openai_chat_completions, anthropic_messages"
            ))),
        }
    }
}

impl FormatName {
    fn label(self) -> &'static str {
        match self {
            Self::OpenResponses => "Open Responses",
            Self::OpenAiChatCompletions => "OpenAI Chat Completions",
            Self::AnthropicMessages => "Anthropic Messages",
        }
    }
}

fn conversion_error_to_py(err: ConversionError) -> PyErr {
    match err {
        ConversionError::InvalidInput(msg) => InvalidInputError::new_err(msg),
        ConversionError::UnsupportedConversion(msg) => UnsupportedConversionError::new_err(msg),
        ConversionError::Serde(msg) => SchemaValidationError::new_err(msg.to_string()),
    }
}

fn encode_result_json<T: serde::Serialize>(result: ConversionResult<T>) -> PyResult<String> {
    let payload = serde_json::json!({
        "value": result.value,
        "warnings": result.warnings,
    });
    serde_json::to_string(&payload)
        .map_err(|e| SchemaValidationError::new_err(format!("failed to encode result: {e}")))
}

fn parse_json_with_ignored_fields<T: serde::de::DeserializeOwned>(
    payload_json: &str,
    format: FormatName,
    payload_kind: &str,
) -> Result<(T, Vec<ConversionWarning>), ConversionError> {
    let mut ignored_paths = Vec::new();
    let mut deserializer = serde_json::Deserializer::from_str(payload_json);
    let value = serde_ignored::deserialize(&mut deserializer, |path| {
        ignored_paths.push(path.to_string());
    })?;
    deserializer.end()?;

    let warnings = ignored_paths
        .into_iter()
        .map(|field| ConversionWarning {
            field,
            action: WarningAction::Dropped,
            message: format!("unknown {} {payload_kind} field dropped", format.label()),
        })
        .collect();
    Ok((value, warnings))
}

fn with_parse_warnings<T>(
    mut result: ConversionResult<T>,
    parse_warnings: Vec<ConversionWarning>,
) -> ConversionResult<T> {
    result.warnings.splice(0..0, parse_warnings);
    result
}

fn identity_conversion<T>(source: T) -> ConversionResult<T> {
    ConversionResult {
        value: source,
        warnings: Vec::new(),
    }
}

fn parse_config(config_json: Option<&str>) -> PyResult<Option<ConversionConfig>> {
    match config_json {
        None => Ok(None),
        Some(json) => {
            let config: ConversionConfig = serde_json::from_str(json)
                .map_err(|e| SchemaValidationError::new_err(format!("invalid config: {e}")))?;
            Ok(Some(config))
        }
    }
}

#[pyclass(unsendable)]
struct PyStreamConverter {
    inner: Box<dyn DynStreamTransform>,
}

#[pymethods]
impl PyStreamConverter {
    fn transform_json_str(&mut self, event_json: &str) -> PyResult<String> {
        let value: serde_json::Value = serde_json::from_str(event_json)
            .map_err(|e| SchemaValidationError::new_err(e.to_string()))?;
        let out = self
            .inner
            .transform_value(value)
            .map_err(conversion_error_to_py)?;
        serde_json::to_string(&out).map_err(|e| {
            SchemaValidationError::new_err(format!("failed to encode stream output: {e}"))
        })
    }

    fn flush_json_str(&mut self) -> PyResult<String> {
        let out = self.inner.flush_value().map_err(conversion_error_to_py)?;
        serde_json::to_string(&out).map_err(|e| {
            SchemaValidationError::new_err(format!("failed to encode stream flush output: {e}"))
        })
    }

    fn take_warnings_json_str(&mut self) -> PyResult<String> {
        let warnings = self.inner.take_warnings_value();
        serde_json::to_string(&warnings)
            .map_err(|e| SchemaValidationError::new_err(format!("failed to encode warnings: {e}")))
    }
}

#[pyfunction]
#[pyo3(signature = (payload_json, source_format, target_format, config_json=None))]
fn convert_request_json_str(
    payload_json: &str,
    source_format: &str,
    target_format: &str,
    config_json: Option<&str>,
) -> PyResult<String> {
    let source = FormatName::try_from(source_format).map_err(conversion_error_to_py)?;
    let target = FormatName::try_from(target_format).map_err(conversion_error_to_py)?;
    let config = parse_config(config_json)?;

    match (source, target) {
        (FormatName::OpenResponses, FormatName::OpenResponses) => {
            let (source, parse_warnings): (OpenResponsesRequest, _) =
                parse_json_with_ignored_fields(payload_json, source, "request")
                    .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(
                identity_conversion(source),
                parse_warnings,
            ))
        }
        (FormatName::OpenResponses, FormatName::OpenAiChatCompletions) => {
            let (source, parse_warnings): (OpenResponsesRequest, _) =
                parse_json_with_ignored_fields(payload_json, source, "request")
                    .map_err(conversion_error_to_py)?;
            let result = ChatCompletionsOpenAiRequest::from_open_responses(source, None)
                .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(result, parse_warnings))
        }
        (FormatName::OpenResponses, FormatName::AnthropicMessages) => {
            let (source, parse_warnings): (OpenResponsesRequest, _) =
                parse_json_with_ignored_fields(payload_json, source, "request")
                    .map_err(conversion_error_to_py)?;
            let result = AnthropicRequest::from_open_responses(source, config)
                .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(result, parse_warnings))
        }
        (FormatName::OpenAiChatCompletions, FormatName::OpenResponses) => {
            let (source, parse_warnings): (ChatCompletionsOpenAiRequest, _) =
                parse_json_with_ignored_fields(payload_json, source, "request")
                    .map_err(conversion_error_to_py)?;
            let result = source
                .into_open_responses(None)
                .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(result, parse_warnings))
        }
        (FormatName::OpenAiChatCompletions, FormatName::OpenAiChatCompletions) => {
            let (source, parse_warnings): (ChatCompletionsOpenAiRequest, _) =
                parse_json_with_ignored_fields(payload_json, source, "request")
                    .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(
                identity_conversion(source),
                parse_warnings,
            ))
        }
        (FormatName::OpenAiChatCompletions, FormatName::AnthropicMessages) => {
            let (source, parse_warnings): (ChatCompletionsOpenAiRequest, _) =
                parse_json_with_ignored_fields(payload_json, source, "request")
                    .map_err(conversion_error_to_py)?;
            let or = source
                .into_open_responses(None)
                .map_err(conversion_error_to_py)?;
            let mut result = AnthropicRequest::from_open_responses(or.value, config)
                .map_err(conversion_error_to_py)?;
            result.warnings.splice(0..0, or.warnings);
            encode_result_json(with_parse_warnings(result, parse_warnings))
        }
        (FormatName::AnthropicMessages, FormatName::OpenResponses) => {
            let (source, parse_warnings): (AnthropicRequest, _) =
                parse_json_with_ignored_fields(payload_json, source, "request")
                    .map_err(conversion_error_to_py)?;
            let result = source
                .into_open_responses(config)
                .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(result, parse_warnings))
        }
        (FormatName::AnthropicMessages, FormatName::OpenAiChatCompletions) => {
            let (source, parse_warnings): (AnthropicRequest, _) =
                parse_json_with_ignored_fields(payload_json, source, "request")
                    .map_err(conversion_error_to_py)?;
            let or = source
                .into_open_responses(config)
                .map_err(conversion_error_to_py)?;
            let mut result = ChatCompletionsOpenAiRequest::from_open_responses(or.value, None)
                .map_err(conversion_error_to_py)?;
            result.warnings.splice(0..0, or.warnings);
            encode_result_json(with_parse_warnings(result, parse_warnings))
        }
        (FormatName::AnthropicMessages, FormatName::AnthropicMessages) => {
            let (source, parse_warnings): (AnthropicRequest, _) =
                parse_json_with_ignored_fields(payload_json, source, "request")
                    .map_err(conversion_error_to_py)?;
            if config.as_ref().is_some_and(|c| c.strip_encrypted_reasoning) {
                let or = source
                    .into_open_responses(config.clone())
                    .map_err(conversion_error_to_py)?;
                let mut result = AnthropicRequest::from_open_responses(or.value, config)
                    .map_err(conversion_error_to_py)?;
                result.warnings.splice(0..0, or.warnings);
                encode_result_json(with_parse_warnings(result, parse_warnings))
            } else {
                encode_result_json(with_parse_warnings(
                    identity_conversion(source),
                    parse_warnings,
                ))
            }
        }
    }
}

#[pyfunction]
fn convert_response_json_str(
    payload_json: &str,
    source_format: &str,
    target_format: &str,
) -> PyResult<String> {
    let source = FormatName::try_from(source_format).map_err(conversion_error_to_py)?;
    let target = FormatName::try_from(target_format).map_err(conversion_error_to_py)?;

    match (source, target) {
        (FormatName::OpenResponses, FormatName::OpenResponses) => {
            let (source, parse_warnings): (OpenResponsesResponse, _) =
                parse_json_with_ignored_fields(payload_json, source, "response")
                    .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(
                identity_conversion(source),
                parse_warnings,
            ))
        }
        (FormatName::OpenResponses, FormatName::OpenAiChatCompletions) => {
            let (source, parse_warnings): (OpenResponsesResponse, _) =
                parse_json_with_ignored_fields(payload_json, source, "response")
                    .map_err(conversion_error_to_py)?;
            let result = ChatCompletionsOpenAiResponse::from_open_responses(source, None)
                .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(result, parse_warnings))
        }
        (FormatName::OpenResponses, FormatName::AnthropicMessages) => {
            let (source, parse_warnings): (OpenResponsesResponse, _) =
                parse_json_with_ignored_fields(payload_json, source, "response")
                    .map_err(conversion_error_to_py)?;
            let result = AnthropicResponse::from_open_responses(source, None)
                .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(result, parse_warnings))
        }
        (FormatName::OpenAiChatCompletions, FormatName::OpenResponses) => {
            let (source, parse_warnings): (ChatCompletionsOpenAiResponse, _) =
                parse_json_with_ignored_fields(payload_json, source, "response")
                    .map_err(conversion_error_to_py)?;
            let result = source
                .into_open_responses(None)
                .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(result, parse_warnings))
        }
        (FormatName::OpenAiChatCompletions, FormatName::OpenAiChatCompletions) => {
            let (source, parse_warnings): (ChatCompletionsOpenAiResponse, _) =
                parse_json_with_ignored_fields(payload_json, source, "response")
                    .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(
                identity_conversion(source),
                parse_warnings,
            ))
        }
        (FormatName::OpenAiChatCompletions, FormatName::AnthropicMessages) => {
            let (source, parse_warnings): (ChatCompletionsOpenAiResponse, _) =
                parse_json_with_ignored_fields(payload_json, source, "response")
                    .map_err(conversion_error_to_py)?;
            let or = source
                .into_open_responses(None)
                .map_err(conversion_error_to_py)?;
            let mut result = AnthropicResponse::from_open_responses(or.value, None)
                .map_err(conversion_error_to_py)?;
            result.warnings.splice(0..0, or.warnings);
            encode_result_json(with_parse_warnings(result, parse_warnings))
        }
        (FormatName::AnthropicMessages, FormatName::OpenResponses) => {
            let (source, parse_warnings): (AnthropicResponse, _) =
                parse_json_with_ignored_fields(payload_json, source, "response")
                    .map_err(conversion_error_to_py)?;
            let result = source
                .into_open_responses(None)
                .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(result, parse_warnings))
        }
        (FormatName::AnthropicMessages, FormatName::OpenAiChatCompletions) => {
            let (source, parse_warnings): (AnthropicResponse, _) =
                parse_json_with_ignored_fields(payload_json, source, "response")
                    .map_err(conversion_error_to_py)?;
            let or = source
                .into_open_responses(None)
                .map_err(conversion_error_to_py)?;
            let mut result = ChatCompletionsOpenAiResponse::from_open_responses(or.value, None)
                .map_err(conversion_error_to_py)?;
            result.warnings.splice(0..0, or.warnings);
            encode_result_json(with_parse_warnings(result, parse_warnings))
        }
        (FormatName::AnthropicMessages, FormatName::AnthropicMessages) => {
            let (source, parse_warnings): (AnthropicResponse, _) =
                parse_json_with_ignored_fields(payload_json, source, "response")
                    .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(
                identity_conversion(source),
                parse_warnings,
            ))
        }
    }
}

#[pyfunction]
fn create_response_stream_converter(
    source_format: &str,
    target_format: &str,
) -> PyResult<PyStreamConverter> {
    let source = FormatName::try_from(source_format).map_err(conversion_error_to_py)?;
    let target = FormatName::try_from(target_format).map_err(conversion_error_to_py)?;

    let inner: Box<dyn DynStreamTransform> = match (source, target) {
        (FormatName::OpenAiChatCompletions, FormatName::OpenResponses) => {
            Box::new(ChatCompletionsToOpenResponsesStream::new())
        }
        (FormatName::OpenResponses, FormatName::OpenAiChatCompletions) => {
            Box::new(OpenResponsesToChatCompletionsStream::new())
        }
        (FormatName::AnthropicMessages, FormatName::OpenResponses) => {
            Box::new(AnthropicMessagesToOpenResponsesStream::new())
        }
        (FormatName::OpenResponses, FormatName::AnthropicMessages) => {
            Box::new(OpenResponsesToAnthropicMessagesStream::new())
        }
        (FormatName::AnthropicMessages, FormatName::OpenAiChatCompletions) => {
            Box::new(ComposedStream::new(
                AnthropicMessagesToOpenResponsesStream::new(),
                OpenResponsesToChatCompletionsStream::new(),
            ))
        }
        (FormatName::OpenAiChatCompletions, FormatName::AnthropicMessages) => {
            Box::new(ComposedStream::new(
                ChatCompletionsToOpenResponsesStream::new(),
                OpenResponsesToAnthropicMessagesStream::new(),
            ))
        }
        _ => {
            return Err(UnsupportedConversionError::new_err(format!(
                "unsupported stream conversion: {source_format} -> {target_format}"
            )));
        }
    };

    Ok(PyStreamConverter { inner })
}

#[pyclass(unsendable)]
struct PyResponseCollector {
    inner: Box<dyn DynResponseCollector>,
}

#[pymethods]
impl PyResponseCollector {
    fn feed_json_str(&mut self, event_json: &str) -> PyResult<()> {
        let value: serde_json::Value = serde_json::from_str(event_json)
            .map_err(|e| SchemaValidationError::new_err(e.to_string()))?;
        self.inner.feed_value(value).map_err(conversion_error_to_py)
    }

    fn finalize_json_str(&mut self) -> PyResult<String> {
        let (response, warnings) = self
            .inner
            .finalize_value()
            .map_err(conversion_error_to_py)?;
        let payload = serde_json::json!({
            "value": response,
            "warnings": warnings,
        });
        serde_json::to_string(&payload).map_err(|e| {
            SchemaValidationError::new_err(format!("failed to encode collector result: {e}"))
        })
    }
}

#[pyfunction]
fn create_response_collector(format: &str) -> PyResult<PyResponseCollector> {
    let format = FormatName::try_from(format).map_err(conversion_error_to_py)?;

    let inner: Box<dyn DynResponseCollector> = match format {
        FormatName::OpenResponses => Box::new(OpenResponsesCollector::new()),
        FormatName::AnthropicMessages => Box::new(AnthropicCollector::new()),
        FormatName::OpenAiChatCompletions => Box::new(ChatCompletionsCollector::new()),
    };

    Ok(PyResponseCollector { inner })
}

#[pyfunction]
fn decompose_response_to_stream_json_str(response_json: &str, format: &str) -> PyResult<String> {
    let format = FormatName::try_from(format).map_err(conversion_error_to_py)?;

    match format {
        FormatName::OpenResponses => {
            let (response, parse_warnings): (OpenResponsesResponse, _) =
                parse_json_with_ignored_fields(response_json, format, "response")
                    .map_err(conversion_error_to_py)?;
            let result = response
                .decompose_to_stream()
                .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(result, parse_warnings))
        }
        FormatName::AnthropicMessages => {
            let (response, parse_warnings): (AnthropicResponse, _) =
                parse_json_with_ignored_fields(response_json, format, "response")
                    .map_err(conversion_error_to_py)?;
            let result = response
                .decompose_to_stream()
                .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(result, parse_warnings))
        }
        FormatName::OpenAiChatCompletions => {
            let (response, parse_warnings): (ChatCompletionsOpenAiResponse, _) =
                parse_json_with_ignored_fields(response_json, format, "response")
                    .map_err(conversion_error_to_py)?;
            let result = response
                .decompose_to_stream()
                .map_err(conversion_error_to_py)?;
            encode_result_json(with_parse_warnings(result, parse_warnings))
        }
    }
}

#[pymodule]
fn _linguafranca(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyStreamConverter>()?;
    m.add_class::<PyResponseCollector>()?;
    m.add_function(wrap_pyfunction!(convert_request_json_str, m)?)?;
    m.add_function(wrap_pyfunction!(convert_response_json_str, m)?)?;
    m.add_function(wrap_pyfunction!(create_response_stream_converter, m)?)?;
    m.add_function(wrap_pyfunction!(create_response_collector, m)?)?;
    m.add_function(wrap_pyfunction!(decompose_response_to_stream_json_str, m)?)?;

    let errors = PyModule::new(py, "errors")?;
    errors.add("ConversionError", py.get_type::<ConversionErrorPy>())?;
    errors.add("InvalidInputError", py.get_type::<InvalidInputError>())?;
    errors.add(
        "UnsupportedConversionError",
        py.get_type::<UnsupportedConversionError>(),
    )?;
    errors.add(
        "SchemaValidationError",
        py.get_type::<SchemaValidationError>(),
    )?;
    m.add_submodule(&errors)?;

    // Ensure exception classes are also exported on root for easier imports.
    m.add("ConversionError", py.get_type::<ConversionErrorPy>())?;
    m.add("InvalidInputError", py.get_type::<InvalidInputError>())?;
    m.add(
        "UnsupportedConversionError",
        py.get_type::<UnsupportedConversionError>(),
    )?;
    m.add(
        "SchemaValidationError",
        py.get_type::<SchemaValidationError>(),
    )?;

    Ok(())
}
create_exception!(_linguafranca, ConversionErrorPy, PyValueError);
create_exception!(_linguafranca, InvalidInputError, ConversionErrorPy);
create_exception!(_linguafranca, UnsupportedConversionError, ConversionErrorPy);
create_exception!(_linguafranca, SchemaValidationError, ConversionErrorPy);

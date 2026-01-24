mod error;
mod matching;
mod processor;
mod proto_builder;
mod types;
pub mod utils;

// Re-export types
pub use types::{CompletedSpawningToolSpan, CompletedToolSpan, NestedContext, RegistrationContext};

// Re-export processor
pub use processor::SpanProcessor;

// Re-export proto builder
pub use proto_builder::{ToolSpanData, build_tool_span_request};

pub use error::SpanError;
use serde_json::Value;

use crate::{
    anthropic::{request::PostMessagesRequest, response::MessageResponse},
    proto::{
        opentelemetry_collector_trace_v1::ExportTraceServiceRequest,
        opentelemetry_proto_common_v1::KeyValue as KeyValueInner,
        opentelemetry_proto_trace_v1::{
            ResourceSpans, ScopeSpans, Span as ProtoSpan, Status, span::SpanKind,
            status::StatusCode,
        },
    },
    spans::utils::convert_attributes_to_proto_key_value,
};

use utils::{
    bytes_to_uuid_like_string, extract_attributes, generate_span_id, is_gzip_encoded,
    parse_span_id, parse_sse_events, parse_trace_id,
};

pub fn create_span_request(
    request_body: String,
    response_body: Vec<u8>,
    trace_id: String,
    parent_span_id: String,
    span_ids_path: Vec<String>,
    start_time_unix_nano: u64,
    end_time_unix_nano: u64,
    span_path: Vec<String>,
    has_gzip_content_encoding: bool,
) -> Result<Option<ExportTraceServiceRequest>, SpanError> {
    let input: PostMessagesRequest =
        serde_json::from_str(&request_body).map_err(|e| SpanError::JsonParseError {
            context: format!("request body: {}", request_body),
            error: e.to_string(),
        })?;

    let output = if input.stream {
        // Streaming response: parse as SSE events
        let response_str = String::from_utf8_lossy(&response_body);
        let events = parse_sse_events(&response_str);
        MessageResponse::try_from_stream_events(events)?
    } else {
        if is_gzip_encoded(&response_body, has_gzip_content_encoding) {
            return Ok(None);
        }
        let string_response_body = String::from_utf8_lossy(&response_body).to_string();
        let message_response: MessageResponse = serde_json::from_str(&string_response_body)
            .map_err(|e| SpanError::JsonParseError {
                context: "response body".to_string(),
                error: e.to_string(),
            })?;
        message_response
    };

    // Parse trace_id and span_id from UUID format to bytes
    let trace_id_bytes = parse_trace_id(&trace_id)?;
    let parent_span_id_bytes = parse_span_id(&parent_span_id)?;
    let span_id_bytes = generate_span_id()?;

    // Validate lengths (trace_id: 16 bytes, span_id: 8 bytes)
    if trace_id_bytes.len() != 16 {
        return Err(SpanError::InvalidBytesLength {
            expected: 16,
            got: trace_id_bytes.len(),
        });
    }
    if parent_span_id_bytes.len() != 8 {
        return Err(SpanError::InvalidBytesLength {
            expected: 8,
            got: parent_span_id_bytes.len(),
        });
    }

    let span_id_string = bytes_to_uuid_like_string(&span_id_bytes)?;
    let ids_path = span_ids_path
        .clone()
        .into_iter()
        .chain(vec![span_id_string])
        .collect::<Vec<_>>();

    // Note: Tool spans are now created separately via SpanProcessor.complete_tool_spans()
    // which tracks tool duration properly (from tool_use in response to tool_result in next request)

    let mut attributes = extract_attributes(input, output);
    attributes.insert(
        "lmnr.span.ids_path".to_string(),
        Value::Array(ids_path.into_iter().map(|s| Value::String(s)).collect()),
    );
    attributes.insert(
        "lmnr.span.path".to_string(),
        Value::Array(span_path.into_iter().map(|s| Value::String(s)).collect()),
    );

    // Convert attributes HashMap to proto KeyValue format
    let proto_attributes: Vec<KeyValueInner> = convert_attributes_to_proto_key_value(attributes)?;

    // Create the proto Span
    let proto_span = ProtoSpan {
        trace_id: trace_id_bytes,
        span_id: span_id_bytes,
        name: "anthropic.messages".to_string(),
        attributes: proto_attributes,
        // Leave other fields as default/empty for now
        trace_state: String::new(),
        parent_span_id: parent_span_id_bytes,
        flags: 1,                      // TraceFlags::SAMPLED
        kind: SpanKind::Client as i32, // Client
        start_time_unix_nano,
        end_time_unix_nano,
        events: Vec::new(),
        dropped_attributes_count: 0,
        dropped_events_count: 0,
        links: Vec::new(),
        dropped_links_count: 0,
        status: Some(Status {
            code: StatusCode::Ok as i32,
            message: String::new(),
        }),
    };

    // Wrap in ScopeSpans
    let scope_spans = ScopeSpans {
        scope: None,
        spans: vec![proto_span],
        schema_url: String::new(),
    };

    // Wrap in ResourceSpans
    let resource_spans = ResourceSpans {
        resource: None,
        scope_spans: vec![scope_spans],
        schema_url: String::new(),
    };

    // Create the ExportTraceServiceRequest
    let export_request = ExportTraceServiceRequest {
        resource_spans: vec![resource_spans],
    };

    Ok(Some(export_request))
}

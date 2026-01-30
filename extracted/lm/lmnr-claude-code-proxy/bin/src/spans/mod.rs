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
            ResourceSpans, ScopeSpans, Span as ProtoSpan, Status,
            span::{Event, SpanKind},
            status::StatusCode,
        },
    },
    spans::utils::{convert_attributes_to_proto_key_value, json_value_to_any_value},
};

use utils::{
    bytes_to_uuid_like_string, extract_attributes, generate_span_id, parse_span_id, parse_trace_id,
};

pub struct ResponseFailure {
    pub status_code: hyper::StatusCode,
    pub body: Vec<u8>,
}

pub enum ResponseInfo {
    Success(MessageResponse),
    Failure(ResponseFailure),
}

pub fn create_span_request(
    trace_id: String,
    parent_span_id: String,
    span_ids_path: Vec<String>,
    start_time_unix_nano: u64,
    end_time_unix_nano: u64,
    span_path: Vec<String>,
    input: PostMessagesRequest,
    response_info: ResponseInfo,
) -> Result<ExportTraceServiceRequest, SpanError> {
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

    let mut events = Vec::new();
    let mut status_message = String::new();
    let status_code = match &response_info {
        ResponseInfo::Success(_) => StatusCode::Ok,
        ResponseInfo::Failure(status_and_body) => StatusCode::Error,
    };

    if let ResponseInfo::Failure(status_and_body) = &response_info {
        let body = String::from_utf8(status_and_body.body.clone()).ok();
        if let Some(body) = &body {
            status_message = body.clone();
        }
        events.push(Event {
            time_unix_nano: end_time_unix_nano,
            name: "exception".to_string(),
            attributes: vec![
                KeyValueInner {
                    key: "exception.message".to_string(),
                    value: json_value_to_any_value(body.map(Value::String).unwrap_or_default())
                        .ok(),
                },
                KeyValueInner {
                    key: "exception.status_code".to_string(),
                    value: json_value_to_any_value(Value::Number(
                        status_and_body.status_code.as_u16().into(),
                    ))
                    .ok(),
                },
                KeyValueInner {
                    key: "exception.type".to_string(),
                    value: json_value_to_any_value(Value::String(
                        status_and_body
                            .status_code
                            .canonical_reason()
                            .map(|s| s.to_string())
                            .unwrap_or(status_and_body.status_code.as_str().to_string()),
                    ))
                    .ok(),
                },
            ],
            dropped_attributes_count: 0,
        });
    }

    // Note: Tool spans are now created separately via SpanProcessor.complete_tool_spans()
    // which tracks tool duration properly (from tool_use in response to tool_result in next request)
    let mut attributes = extract_attributes(input, response_info);
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
        events,
        dropped_attributes_count: 0,
        dropped_events_count: 0,
        links: Vec::new(),
        dropped_links_count: 0,
        status: Some(Status {
            code: status_code as i32,
            message: status_message,
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

    Ok(export_request)
}

//! Helpers for building OpenTelemetry protobuf spans

use crate::proto::{
    opentelemetry_collector_trace_v1::ExportTraceServiceRequest,
    opentelemetry_proto_common_v1::KeyValue as KeyValueInner,
    opentelemetry_proto_trace_v1::{
        ResourceSpans, ScopeSpans, Span as ProtoSpan, Status, span::SpanKind, status::StatusCode,
    },
};

use serde_json::Value;
use std::collections::HashMap;

use super::types::{CompletedSpawningToolSpan, CompletedToolSpan, SpawningToolType};
use super::utils::convert_attributes_to_proto_key_value;

/// Common data needed to build a tool span
pub struct ToolSpanData {
    pub trace_id_bytes: Vec<u8>,
    pub span_id_bytes: Vec<u8>,
    pub parent_span_id_bytes: Vec<u8>,
    pub span_ids_path: Vec<String>,
    pub span_path: Vec<String>,
    pub name: String,
    pub input: String,
    pub output: Option<String>,
    pub start_time_unix_nano: u64,
    pub end_time_unix_nano: u64,
    pub is_error: bool,
}

impl From<CompletedToolSpan> for ToolSpanData {
    fn from(span: CompletedToolSpan) -> Self {
        Self {
            trace_id_bytes: span.trace_id_bytes,
            span_id_bytes: span.span_id_bytes,
            parent_span_id_bytes: span.parent_span_id_bytes,
            span_ids_path: span.span_ids_path,
            span_path: span.span_path,
            name: span.tool_name,
            input: span.tool_input.to_string(),
            output: span.tool_output,
            start_time_unix_nano: span.start_time_unix_nano,
            end_time_unix_nano: span.end_time_unix_nano,
            is_error: span.is_error,
        }
    }
}

impl From<CompletedSpawningToolSpan> for ToolSpanData {
    fn from(span: CompletedSpawningToolSpan) -> Self {
        // Format input based on tool type
        let input = match span.tool_type {
            SpawningToolType::Task => serde_json::json!({
                "description": span.description,
                "prompt": span.prompt,
            })
            .to_string(),
            SpawningToolType::WebSearch => serde_json::json!({
                "query": span.prompt,
            })
            .to_string(),
            SpawningToolType::Bash => serde_json::json!({
                "command": span.prompt,
            })
            .to_string(),
        };

        Self {
            trace_id_bytes: span.trace_id_bytes,
            span_id_bytes: span.tool_span_id_bytes,
            parent_span_id_bytes: span.parent_span_id_bytes,
            span_ids_path: span.span_ids_path,
            span_path: span.span_path,
            name: span.tool_name,
            input,
            output: span.tool_output,
            start_time_unix_nano: span.start_time_unix_nano,
            end_time_unix_nano: span.end_time_unix_nano,
            is_error: false,
        }
    }
}

/// Build attributes for a tool span
fn build_tool_attributes(data: &ToolSpanData) -> HashMap<String, Value> {
    let mut attributes: HashMap<String, Value> = HashMap::new();

    attributes.insert(
        "lmnr.span.ids_path".to_string(),
        Value::Array(
            data.span_ids_path
                .iter()
                .map(|s| Value::String(s.clone()))
                .collect(),
        ),
    );
    attributes.insert(
        "lmnr.span.path".to_string(),
        Value::Array(
            data.span_path
                .iter()
                .map(|s| Value::String(s.clone()))
                .collect(),
        ),
    );
    attributes.insert(
        "lmnr.span.type".to_string(),
        Value::String("TOOL".to_string()),
    );
    attributes.insert(
        "lmnr.span.input".to_string(),
        Value::String(data.input.clone()),
    );

    if let Some(output) = &data.output {
        attributes.insert(
            "lmnr.span.output".to_string(),
            Value::String(output.clone()),
        );
    }

    attributes
}

/// Build an ExportTraceServiceRequest from ToolSpanData
pub fn build_tool_span_request(
    data: ToolSpanData,
) -> Result<ExportTraceServiceRequest, Box<dyn std::error::Error + Send + Sync>> {
    let attributes = build_tool_attributes(&data);
    let proto_attributes: Vec<KeyValueInner> = convert_attributes_to_proto_key_value(attributes)?;

    let proto_span = ProtoSpan {
        trace_id: data.trace_id_bytes,
        span_id: data.span_id_bytes,
        name: data.name,
        attributes: proto_attributes,
        trace_state: String::new(),
        parent_span_id: data.parent_span_id_bytes,
        flags: 1,
        kind: SpanKind::Client as i32,
        start_time_unix_nano: data.start_time_unix_nano,
        end_time_unix_nano: data.end_time_unix_nano,
        events: Vec::new(),
        dropped_attributes_count: 0,
        dropped_events_count: 0,
        links: Vec::new(),
        dropped_links_count: 0,
        status: Some(Status {
            code: if data.is_error {
                StatusCode::Error as i32
            } else {
                StatusCode::Ok as i32
            },
            message: String::new(),
        }),
    };

    let scope_spans = ScopeSpans {
        scope: None,
        spans: vec![proto_span],
        schema_url: String::new(),
    };

    let resource_spans = ResourceSpans {
        resource: None,
        scope_spans: vec![scope_spans],
        schema_url: String::new(),
    };

    Ok(ExportTraceServiceRequest {
        resource_spans: vec![resource_spans],
    })
}

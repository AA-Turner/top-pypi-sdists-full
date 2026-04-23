use std::collections::HashMap;

use serde_json::Value;

use super::conversion::json_value_to_any_value;
use crate::{
    anthropic::{
        request::{MessageContent, MessageRole, PostMessagesRequest},
        response::{MessageResponse, ResponseContentBlock},
    },
    proto::opentelemetry_proto_common_v1::KeyValue as KeyValueInner,
    spans::{ResponseInfo, SpanError},
};

pub fn extract_attributes(
    input: PostMessagesRequest,
    output: ResponseInfo,
) -> HashMap<String, Value> {
    let mut attributes = HashMap::new();
    attributes.insert(
        "gen_ai.system".to_string(),
        Value::String("anthropic".to_string()),
    );
    attributes.insert(
        "lmnr.internal.claude_code_proxy".to_string(),
        Value::Bool(true),
    );
    attributes.insert(
        "lmnr.span.type".to_string(),
        Value::String("LLM".to_string()),
    );
    if let Some(req_model) = input.model {
        attributes.insert("gen_ai.request.model".to_string(), Value::String(req_model));
    }
    attributes.insert(
        "gen_ai.request.max_tokens".to_string(),
        Value::Number(input.max_tokens.into()),
    );
    if let Some(temperature) = input.temperature {
        attributes.insert(
            "gen_ai.request.temperature".to_string(),
            Value::Number(
                serde_json::Number::from_f64(temperature).unwrap_or(serde_json::Number::from(0)),
            ),
        );
    }
    if let Some(top_k) = input.top_k {
        attributes.insert(
            "gen_ai.request.top_k".to_string(),
            Value::Number(top_k.into()),
        );
    }
    if let Some(top_p) = input.top_p {
        attributes.insert(
            "gen_ai.request.top_p".to_string(),
            Value::Number(
                serde_json::Number::from_f64(top_p).unwrap_or(serde_json::Number::from(0)),
            ),
        );
    }
    if let Some(stop_sequences) = input.stop_sequences {
        attributes.insert(
            "gen_ai.request.stop_sequences".to_string(),
            Value::Array(
                stop_sequences
                    .into_iter()
                    .map(|s| Value::String(s))
                    .collect(),
            ),
        );
    }
    if let Some(tools) = input.tools {
        attributes.insert(
            "gen_ai.tool.definitions".to_string(),
            Value::Array(
                tools
                    .iter()
                    .map(|t| serde_json::to_value(t).unwrap_or(Value::Null))
                    .collect(),
            ),
        );
    }

    let mut messages = input
        .system
        .map(|s| {
            serde_json::json!({
                "role": "system",
                "content": s
            })
        })
        .map(|s| vec![s])
        .unwrap_or(vec![]);

    messages.extend(
        input
            .messages
            .iter()
            .filter_map(|m| serde_json::to_value(m).ok()),
    );

    attributes.insert("gen_ai.input.messages".to_string(), Value::Array(messages));

    add_response_attributes(&mut attributes, output);

    attributes
}

fn add_response_attributes(attributes: &mut HashMap<String, Value>, response_info: ResponseInfo) {
    match response_info {
        ResponseInfo::Success(response) => {
            add_success_attributes(attributes, response);
        }
        ResponseInfo::Failure(response_failure) => {
            attributes.insert(
                "lmnr.span.output".to_string(),
                String::from_utf8(response_failure.body.clone())
                    .ok()
                    .map(|s| Value::String(s))
                    .unwrap_or_default(),
            );
        }
    }
}

fn add_success_attributes(attributes: &mut HashMap<String, Value>, output: MessageResponse) {
    attributes.insert("gen_ai.response.id".to_string(), Value::String(output.id));
    attributes.insert(
        "gen_ai.response.model".to_string(),
        Value::String(output.model),
    );

    let total_input_tokens = output.usage.input_tokens
        + output.usage.cache_creation_input_tokens.unwrap_or(0)
        + output.usage.cache_read_input_tokens.unwrap_or(0);

    // our backend (and so does regular anthropic instrumentation) assumes
    // input tokens includes cached tokens
    // Ref: https://github.com/lmnr-ai/lmnr-python/blob/9f309522321490176ddca313bf6303d2028bf4e7/src/lmnr/opentelemetry_lib/opentelemetry/instrumentation/anthropic/__init__.py#L260
    attributes.insert(
        "gen_ai.usage.input_tokens".to_string(),
        Value::Number(total_input_tokens.into()),
    );
    attributes.insert(
        "gen_ai.usage.output_tokens".to_string(),
        Value::Number(output.usage.output_tokens.into()),
    );
    if let Some(cache_creation_input_tokens) = output.usage.cache_creation_input_tokens {
        attributes.insert(
            "gen_ai.usage.cache_creation_input_tokens".to_string(),
            Value::Number(cache_creation_input_tokens.into()),
        );
    }
    if let Some(cache_read_input_tokens) = output.usage.cache_read_input_tokens {
        attributes.insert(
            "gen_ai.usage.cache_read_input_tokens".to_string(),
            Value::Number(cache_read_input_tokens.into()),
        );
    }

    let mut result = HashMap::from([("role".to_string(), Value::String("assistant".to_string()))]);
    if let Some(stop_reason) = output.stop_reason {
        let stop_reason_val = serde_json::to_value(stop_reason);
        if let Ok(stop_reason_val) = stop_reason_val {
            attributes.insert(
                "gen_ai.response.finish_reasons".to_string(),
                Value::Array(vec![stop_reason_val.clone()]),
            );
            result.insert("stop_reason".to_string(), stop_reason_val);
        }
    }

    let output_blocks = output
        .content
        .iter()
        .filter_map(|block| serde_json::to_value(block).ok())
        .collect::<Vec<_>>();

    result.insert("content".to_string(), Value::Array(output_blocks));

    let output_messages = serde_json::to_value(result)
        .map(|v| vec![v])
        .unwrap_or_default();

    attributes.insert(
        "gen_ai.output.messages".to_string(),
        Value::Array(output_messages),
    );
}

pub fn convert_attributes_to_proto_key_value(
    attributes: HashMap<String, Value>,
) -> Result<Vec<KeyValueInner>, SpanError> {
    let proto_attributes = attributes
        .into_iter()
        .map(|(k, v)| {
            let value = json_value_to_any_value(v.clone()).map_err(|_| {
                SpanError::AttributeConversionError {
                    value: v.to_string(),
                }
            })?;
            Ok(KeyValueInner {
                key: k,
                value: Some(value),
            })
        })
        .collect::<Result<Vec<_>, SpanError>>()?;
    Ok(proto_attributes)
}

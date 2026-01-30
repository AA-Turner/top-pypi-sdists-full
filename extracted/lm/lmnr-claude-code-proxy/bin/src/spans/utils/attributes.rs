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

struct AttributeToolCall {
    id: String,
    name: String,
    input: Value,
}

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
    attributes.insert(
        "gen_ai.request.model".to_string(),
        Value::String(input.model),
    );
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
        tools.iter().enumerate().for_each(|(i, tool)| {
            attributes.insert(
                format!("llm.request.functions.{}.name", i),
                Value::String(tool.name.clone()),
            );
            if let Some(description) = &tool.description {
                attributes.insert(
                    format!("llm.request.functions.{}.description", i),
                    Value::String(description.clone()),
                );
            }
            attributes.insert(
                format!("llm.request.functions.{}.parameters", i),
                tool.input_schema.clone(),
            );
        });
    }
    let increment_message_index = if input.system.is_some() { 1 } else { 0 };
    if let Some(system) = input.system {
        attributes.insert(
            format!("gen_ai.prompt.0.role"),
            Value::String("system".to_string()),
        );
        attributes.insert(
            format!("gen_ai.prompt.0.content"),
            Value::String(system.to_string()),
        );
    }
    for (i, message) in input.messages.iter().enumerate() {
        let role = match message.role {
            MessageRole::User => "user".to_string(),
            MessageRole::Assistant => "assistant".to_string(),
        };
        let msg_idx = i + increment_message_index;
        attributes.insert(format!("gen_ai.prompt.{msg_idx}.role"), Value::String(role));
        match &message.content {
            MessageContent::String(text) => {
                attributes.insert(
                    format!("gen_ai.prompt.{msg_idx}.content"),
                    Value::String(text.clone()),
                );
            }
            MessageContent::Blocks(blocks) => match serde_json::to_string(&blocks) {
                Ok(blocks_string) => {
                    attributes.insert(
                        format!("gen_ai.prompt.{msg_idx}.content"),
                        Value::String(blocks_string),
                    );
                }
                Err(e) => {
                    eprintln!("Failed to serialize blocks: {}", e);
                }
            },
        }
    }

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

    attributes.insert(
        "gen_ai.usage.input_tokens".to_string(),
        Value::Number(output.usage.input_tokens.into()),
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

    if let Some(stop_reason) = output.stop_reason {
        attributes.insert(
            "llm.response.stop_reason".to_string(),
            serde_json::to_value(stop_reason).unwrap(),
        );
    }

    // Parsing output in legacy attributes format. Once the frontend supports
    // the Anthropic format, and the backend passes the messages through raw,
    // we can just send `gen_ai.output.messages` or `lmnr.span.output` directly.
    let mut content_string = String::new();
    let mut thinking_string = String::new();
    let mut tool_calls = Vec::new();
    output.content.iter().for_each(|block| match block {
        ResponseContentBlock::Text { text, .. } => {
            content_string.push_str(text);
        }
        ResponseContentBlock::ToolUse { id, name, input } => {
            tool_calls.push(AttributeToolCall {
                id: id.clone(),
                name: name.clone(),
                input: input.clone(),
            });
        }
        ResponseContentBlock::ServerToolUse {
            id, input, name, ..
        } => {
            tool_calls.push(AttributeToolCall {
                id: id.clone(),
                name: name.clone(),
                input: input.clone(),
            });
        }
        ResponseContentBlock::McpToolUse {
            id,
            input,
            name,
            server_name,
            ..
        } => {
            let inputs = HashMap::from([
                ("input".to_string(), input.clone()),
                (
                    "server_name".to_string(),
                    Value::String(server_name.clone()),
                ),
            ]);
            tool_calls.push(AttributeToolCall {
                id: id.clone(),
                name: name.clone(),
                input: serde_json::to_value(inputs).unwrap_or_default(),
            });
        }
        ResponseContentBlock::Thinking { thinking, .. } => {
            thinking_string.push_str(thinking);
        }
        ResponseContentBlock::RedactedThinking { data } => {
            thinking_string.push_str(data);
        }
        // Most other blocks can't be there in response, even though the
        // anthropic API docs and SDK reuse the type `ContentBlock` for both
        // request and response.
        _ => {}
    });

    let mut completion_id = 0;
    if !thinking_string.is_empty() {
        attributes.insert(
            "gen_ai.completion.0.role".to_string(),
            Value::String("thinking".to_string()),
        );
        attributes.insert(
            "gen_ai.completion.0.thinking".to_string(),
            Value::String(thinking_string),
        );
        completion_id += 1;
    }
    attributes.insert(
        format!("gen_ai.completion.{completion_id}.role"),
        Value::String("assistant".to_string()),
    );
    attributes.insert(
        format!("gen_ai.completion.{completion_id}.content"),
        Value::String(content_string),
    );
    for (i, tool_call) in tool_calls.into_iter().enumerate() {
        attributes.insert(
            format!("gen_ai.completion.{completion_id}.tool_calls.{i}.id"),
            Value::String(tool_call.id),
        );
        attributes.insert(
            format!("gen_ai.completion.{completion_id}.tool_calls.{i}.name"),
            Value::String(tool_call.name),
        );
        attributes.insert(
            format!("gen_ai.completion.{completion_id}.tool_calls.{i}.arguments"),
            tool_call.input,
        );
    }
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

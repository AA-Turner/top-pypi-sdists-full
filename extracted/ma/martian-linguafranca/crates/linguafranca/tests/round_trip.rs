use std::path::{Path, PathBuf};

use linguafranca::anthropic::convert::stream::{
    AnthropicMessagesToOpenResponsesStream, OpenResponsesToAnthropicMessagesStream,
};
use linguafranca::anthropic::request::AnthropicRequest;
use linguafranca::anthropic::response::AnthropicResponse;
use linguafranca::open_responses::request::OpenResponsesRequest;
use linguafranca::open_responses::response::OpenResponsesResponse;
use rstest::rstest;

mod common;

fn diffs_dir() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR")).join("tests/diffs")
}

fn case_name(path: &Path) -> &str {
    path.parent()
        .unwrap()
        .file_name()
        .unwrap()
        .to_str()
        .unwrap()
}

// ── Anthropic Messages round-trips ──

#[rstest]
fn am_request_round_trip(
    #[files("tests/fixtures/anthropic_messages/request/*/messages.json")]
    #[exclude("web_search_history")]
    // tool_search round-trip is lossy: tool_reference blocks inside tool_result
    // are split into separate ToolSearchOutput items, and server-side
    // tool_search_tool_result structure is not reconstructed identically.
    #[exclude("tool_search")]
    path: PathBuf,
) {
    let case = case_name(&path);
    let fwd = common::load_diffs(&diffs_dir().join("anthropic_messages/request_to_or.json"));
    let rev = common::load_diffs(&diffs_dir().join("anthropic_messages/request_from_or.json"));
    common::run_round_trip_case::<AnthropicRequest, OpenResponsesRequest>(
        case,
        &path,
        &fwd,
        &rev,
        &format!("{case} AM request round-trip"),
    );
}

#[rstest]
fn am_response_round_trip(
    #[files("tests/fixtures/anthropic_messages/response/*/messages.json")]
    // Open Responses -> Anthropic responses drop tool_search_call/tool_search_output items.
    #[exclude("tool_search")]
    path: PathBuf,
) {
    let case = case_name(&path);
    let fwd = common::load_diffs(&diffs_dir().join("anthropic_messages/response_to_or.json"));
    let rev = common::load_diffs(&diffs_dir().join("anthropic_messages/response_from_or.json"));
    common::run_round_trip_case::<AnthropicResponse, OpenResponsesResponse>(
        case,
        &path,
        &fwd,
        &rev,
        &format!("{case} AM response round-trip"),
    );
}

#[rstest]
fn am_stream_round_trip(
    #[files("tests/fixtures/anthropic_messages/stream/*/messages_events.json")]
    // tool_search round-trip is lossy: tool_search_tool_result structure is
    // not reconstructed identically from ToolSearchCall + ToolSearchOutput.
    #[exclude("tool_search")]
    path: PathBuf,
) {
    let case = case_name(&path);
    let fwd = common::load_diffs(&diffs_dir().join("anthropic_messages/stream_to_or.json"));
    let rev = common::load_diffs(&diffs_dir().join("anthropic_messages/stream_from_or.json"));
    common::run_round_trip_stream_case(
        case,
        &path,
        AnthropicMessagesToOpenResponsesStream::new(),
        OpenResponsesToAnthropicMessagesStream::new(),
        &fwd,
        &rev,
        &format!("{case} AM stream round-trip"),
    );
}

#[rstest]
#[case::summary("THINK", None)]
#[case::carrier_only("", None)]
#[case::summary_and_text("THINK", Some("Checking"))]
fn chat_response_reasoning_carrier_replays_with_tool_call(
    #[case] summary: &str,
    #[case] text: Option<&str>,
) {
    use linguafranca::chat_completions_openai::request::ChatCompletionsOpenAiRequest;
    use linguafranca::chat_completions_openai::response::ChatCompletionsOpenAiResponse;
    use linguafranca::traits::{FromOpenResponses, IntoOpenResponses};
    use serde_json::json;

    let envelope = "lf-er:v1:k1:round-trip+/=\nexact";
    let response: ChatCompletionsOpenAiResponse = serde_json::from_value(json!({
        "id": "chatcmpl_carrier", "object": "chat.completion", "created": 1,
        "model": "deepseek", "choices": [{
            "index": 0, "finish_reason": "tool_calls",
            "message": {"role": "assistant", "content": text, "reasoning_content": summary,
                "reasoning_details": [{"type": "reasoning.encrypted", "data": envelope}],
                "tool_calls": [{"type": "function", "id": "call_1",
                    "function": {"name": "lookup", "arguments": "{}"}}]}
        }]
    }))
    .unwrap();
    let converted = response.into_open_responses(None).unwrap();
    assert!(converted.warnings.is_empty());
    let output = serde_json::to_value(converted.value.output).unwrap();
    assert_eq!(output[0]["type"], "reasoning");
    let mut input = vec![json!({"type": "message", "role": "user", "content": "Solve"})];
    input.extend(output.as_array().unwrap().iter().cloned());
    input.push(json!({"type": "function_call_output", "call_id": "call_1", "output": "ok"}));
    let request: OpenResponsesRequest =
        serde_json::from_value(json!({"model": "deepseek", "input": input})).unwrap();
    let converted = ChatCompletionsOpenAiRequest::from_open_responses(request, None).unwrap();
    assert!(
        converted.warnings.iter().all(|warning| {
            warning.field.ends_with(".id") || warning.field.ends_with(".status")
        })
    );
    let messages = serde_json::to_value(converted.value.messages).unwrap();
    assert_eq!(messages.as_array().unwrap().len(), 3);
    assert_eq!(messages[0]["role"], "user");
    assert_eq!(messages[1]["role"], "assistant");
    if let Some(text) = text {
        assert_eq!(
            messages[1]["content"],
            json!([{"type": "text", "text": text}])
        );
    }
    if summary.is_empty() {
        assert!(messages[1].get("reasoning_content").is_none());
    } else {
        assert_eq!(messages[1]["reasoning_content"], summary);
    }
    assert_eq!(
        messages[1]["reasoning_details"],
        json!([{"type": "reasoning.encrypted", "data": envelope, "format": "unknown", "index": 0}])
    );
    assert_eq!(
        messages[1]["tool_calls"],
        json!([{"id": "call_1", "type": "function", "function": {"name": "lookup", "arguments": "{}"}}])
    );
    assert_eq!(messages[2]["role"], "tool");
    assert_eq!(messages[2]["tool_call_id"], "call_1");
}

#[rstest]
#[case::summary(Some("THINK"))]
#[case::carrier_only(None)]
fn chat_request_reasoning_carrier_round_trip(#[case] summary: Option<&str>) {
    use linguafranca::chat_completions_openai::request::ChatCompletionsOpenAiRequest;
    use linguafranca::traits::{FromOpenResponses, IntoOpenResponses};
    use serde_json::json;

    let details = json!([{
        "type": "reasoning.encrypted", "data": "lf-er:v1:k1:request-round-trip+/=\nexact",
        "format": "unknown", "index": 0
    }]);
    let request: ChatCompletionsOpenAiRequest = serde_json::from_value(json!({
        "model": "deepseek", "messages": [
            {"role": "user", "content": "Solve"},
            {"role": "assistant", "reasoning_content": summary, "reasoning_details": details,
                "tool_calls": [{"type": "function", "id": "call_1",
                    "function": {"name": "lookup", "arguments": "{}"}}]},
            {"role": "tool", "tool_call_id": "call_1", "content": "ok"}
        ]
    }))
    .unwrap();
    let responses = request.into_open_responses(None).unwrap();
    assert!(responses.warnings.is_empty());
    let chat = ChatCompletionsOpenAiRequest::from_open_responses(responses.value, None).unwrap();
    assert!(chat.warnings.is_empty());
    let messages = serde_json::to_value(chat.value.messages).unwrap();
    assert_eq!(messages.as_array().unwrap().len(), 3);
    assert_eq!(messages[1]["role"], "assistant");
    assert_eq!(messages[1]["reasoning_details"], details);
    assert_eq!(messages[1]["reasoning_content"], json!(summary));
    assert_eq!(messages[1]["tool_calls"][0]["id"], "call_1");
    assert_eq!(messages[2]["tool_call_id"], "call_1");
}

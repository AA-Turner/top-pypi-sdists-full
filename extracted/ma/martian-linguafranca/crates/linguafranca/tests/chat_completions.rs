use std::path::Path;

use linguafranca::chat_completions_openai::convert::stream::{
    ChatCompletionsToOpenResponsesStream, OpenResponsesToChatCompletionsStream,
};
use linguafranca::chat_completions_openai::request::ChatCompletionsOpenAiRequest;
use linguafranca::chat_completions_openai::response::ChatCompletionsOpenAiResponse;
use linguafranca::chat_completions_openai::stream::ChatCompletionsStreamChunk;
use linguafranca::open_responses::request::OpenResponsesRequest;
use linguafranca::open_responses::response::OpenResponsesResponse;
use linguafranca::open_responses::stream::OpenResponsesStreamEvent;
use linguafranca::stream::StreamTransform;
use linguafranca::traits::{CollectStream, DecomposeToStream};
use rstest::rstest;

mod common;

#[derive(Clone, Copy)]
enum Direction {
    ChatCompletionsToOpenResponses,
    OpenResponsesToChatCompletions,
}

fn run(case: &str, direction: Direction) {
    let dir = Path::new(env!("CARGO_MANIFEST_DIR")).join(format!(
        "tests/fixtures/chat_completions_openai/request/{case}"
    ));

    match direction {
        Direction::ChatCompletionsToOpenResponses => {
            let label = format!("{case} Chat Completions -> Open Responses");
            common::run_into_open_responses_case::<
                ChatCompletionsOpenAiRequest,
                OpenResponsesRequest,
            >(
                case,
                &dir,
                "chat_completions.json",
                "open_responses.json",
                "chat_completions_to_open_responses",
                label.as_str(),
            );
        }
        Direction::OpenResponsesToChatCompletions => {
            let label = format!("{case} Open Responses -> Chat Completions");
            common::run_from_open_responses_case::<
                ChatCompletionsOpenAiRequest,
                OpenResponsesRequest,
            >(
                case,
                &dir,
                "chat_completions.json",
                "open_responses.json",
                "open_responses_to_chat_completions",
                label.as_str(),
            );
        }
    }
}

#[rstest]
#[case::simple_text("simple_text")]
#[case::multi_turn("multi_turn")]
#[case::with_tools("with_tools")]
#[case::with_image("with_image")]
#[case::with_image_url("with_image_url")]
#[case::system_and_developer_roles("system_and_developer_roles")]
#[case::tool_conversation_order("tool_conversation_order")]
#[case::reasoning_and_text_config("reasoning_and_text_config")]
#[case::assistant_output_text("assistant_output_text")]
fn chat_completions_to_open_responses_bidirectional(#[case] case: &str) {
    run(case, Direction::ChatCompletionsToOpenResponses);
}

#[rstest]
#[case::simple_text("simple_text")]
#[case::multi_turn("multi_turn")]
#[case::with_tools("with_tools")]
#[case::with_image("with_image")]
#[case::with_image_url("with_image_url")]
#[case::system_and_developer_roles("system_and_developer_roles")]
#[case::tool_conversation_order("tool_conversation_order")]
#[case::reasoning_and_text_config("reasoning_and_text_config")]
#[case::assistant_output_text("assistant_output_text")]
fn open_responses_to_chat_completions_bidirectional(#[case] case: &str) {
    run(case, Direction::OpenResponsesToChatCompletions);
}

#[rstest]
#[case::dropped_fields_chat_completions("dropped_fields_chat_completions")]
#[case::lossy_parameter_normalization("lossy_parameter_normalization")]
#[case::reasoning_effort_mapping("reasoning_effort_mapping")]
#[case::max_reasoning_effort("max_reasoning_effort")]
#[case::reasoning_content_items("reasoning_content_items")]
#[case::reasoning_object_cc_to_or("reasoning_object_cc_to_or")]
#[case::top_cache_control_cc_to_or("top_cache_control_cc_to_or")]
#[case::web_search_tool_cc_to_or("web_search_tool_cc_to_or")]
#[case::web_search_exact_type_cc_to_or("web_search_exact_type_cc_to_or")]
#[case::web_search_options_cc_to_or("web_search_options_cc_to_or")]
#[case::web_search_options_and_tool_cc_to_or("web_search_options_and_tool_cc_to_or")]
#[case::web_search_tool_warnings_cc_to_or("web_search_tool_warnings_cc_to_or")]
fn chat_completions_to_open_responses_only(#[case] case: &str) {
    run(case, Direction::ChatCompletionsToOpenResponses);
}

#[rstest]
#[case::include_logprobs_clamping("include_logprobs_clamping")]
#[case::tool_choice_missing_name("tool_choice_missing_name")]
#[case::item_reference_ordering("item_reference_ordering")]
#[case::stream_usage_defaults("stream_usage_defaults")]
#[case::dropped_fields_open_responses("dropped_fields_open_responses")]
#[case::reasoning_summary_dropped("reasoning_summary_dropped")]
#[case::reasoning_effort_mapping("reasoning_effort_mapping")]
#[case::max_reasoning_effort("max_reasoning_effort")]
#[case::max_output_tokens_mapping("max_output_tokens_mapping")]
#[case::simple_text_input_string("simple_text_input_string")]
#[case::reasoning_items_input("reasoning_items_input")]
#[case::web_search_tool_dropped_or_to_cc("web_search_tool_dropped_or_to_cc")]
#[case::namespace_tools_or_to_cc("namespace_tools_or_to_cc")]
fn open_responses_to_chat_completions_only(#[case] case: &str) {
    run(case, Direction::OpenResponsesToChatCompletions);
}

fn run_response(case: &str, direction: Direction) {
    let dir = Path::new(env!("CARGO_MANIFEST_DIR")).join(format!(
        "tests/fixtures/chat_completions_openai/response/{case}"
    ));

    match direction {
        Direction::ChatCompletionsToOpenResponses => {
            let label = format!("{case} Chat Completions Response -> Open Responses");
            common::run_into_open_responses_case::<
                ChatCompletionsOpenAiResponse,
                OpenResponsesResponse,
            >(
                case,
                &dir,
                "chat_completions.json",
                "open_responses.json",
                "chat_completions_to_open_responses",
                label.as_str(),
            );
        }
        Direction::OpenResponsesToChatCompletions => {
            let label = format!("{case} Open Responses -> Chat Completions Response");
            common::run_from_open_responses_case::<
                ChatCompletionsOpenAiResponse,
                OpenResponsesResponse,
            >(
                case,
                &dir,
                "chat_completions.json",
                "open_responses.json",
                "open_responses_to_chat_completions",
                label.as_str(),
            );
        }
    }
}

#[rstest]
#[case::simple_text("simple_text")]
#[case::tool_calls_and_reasoning("tool_calls_and_reasoning")]
#[case::with_refusal("with_refusal")]
#[case::with_annotations("with_annotations")]
#[case::max_tokens("max_tokens")]
#[case::failed_status("failed_status")]
#[case::usage_with_details("usage_with_details")]
#[case::namespaced_tool_call("namespaced_tool_call")]
fn resp_chat_completions_to_open_responses_bidirectional(#[case] case: &str) {
    run_response(case, Direction::ChatCompletionsToOpenResponses);
}

#[rstest]
#[case::simple_text("simple_text")]
#[case::tool_calls_and_reasoning("tool_calls_and_reasoning")]
#[case::with_refusal("with_refusal")]
#[case::with_annotations("with_annotations")]
#[case::max_tokens("max_tokens")]
#[case::failed_status("failed_status")]
#[case::usage_with_details("usage_with_details")]
#[case::custom_tool_call("custom_tool_call")]
#[case::namespaced_tool_call("namespaced_tool_call")]
fn resp_open_responses_to_chat_completions_bidirectional(#[case] case: &str) {
    run_response(case, Direction::OpenResponsesToChatCompletions);
}

#[rstest]
#[case::multiple_choices_first_only("multiple_choices_first_only")]
#[case::choice_logprobs_dropped("choice_logprobs_dropped")]
#[case::annotations_without_content_dropped("annotations_without_content_dropped")]
#[case::audio_dropped("audio_dropped")]
#[case::custom_tool_call_downgraded("custom_tool_call_downgraded")]
#[case::service_tier_scale_mapped_to_priority("service_tier_scale_mapped_to_priority")]
#[case::unknown_service_tier_dropped("unknown_service_tier_dropped")]
#[case::non_assistant_role_warned("non_assistant_role_warned")]
fn resp_chat_completions_to_open_responses_only(#[case] case: &str) {
    run_response(case, Direction::ChatCompletionsToOpenResponses);
}

#[rstest]
#[case::dropped_fields_open_responses("dropped_fields_open_responses")]
#[case::non_terminal_status_finish_reason_omitted("non_terminal_status_finish_reason_omitted")]
#[case::function_call_output_dropped("function_call_output_dropped")]
#[case::non_assistant_output_message_dropped("non_assistant_output_message_dropped")]
#[case::output_text_logprobs_dropped("output_text_logprobs_dropped")]
#[case::input_type_content_parts_dropped("input_type_content_parts_dropped")]
#[case::reasoning_summary_and_content_joined("reasoning_summary_and_content_joined")]
#[case::content_and_refusal_joining("content_and_refusal_joining")]
fn resp_open_responses_to_chat_completions_only(#[case] case: &str) {
    run_response(case, Direction::OpenResponsesToChatCompletions);
}

fn run_stream(case: &str, direction: Direction) {
    let dir = Path::new(env!("CARGO_MANIFEST_DIR")).join(format!(
        "tests/fixtures/chat_completions_openai/stream/{case}"
    ));

    match direction {
        Direction::ChatCompletionsToOpenResponses => {
            let input: Vec<ChatCompletionsStreamChunk> =
                common::load_fixture(&dir.join("chat_completions_events.json"), case);
            let mut stream = ChatCompletionsToOpenResponsesStream::new();
            let mut actual_events = Vec::new();
            for (i, event) in input.into_iter().enumerate() {
                actual_events.extend(stream.transform(event).expect(
                    format!("{case} stream CC->OR transform failed at input event #{i}").as_str(),
                ));
            }
            actual_events.extend(
                stream
                    .flush()
                    .expect(format!("{case} stream CC->OR flush failed").as_str()),
            );
            let warnings = stream.take_warnings();

            let expected: Vec<OpenResponsesStreamEvent> =
                common::load_fixture(&dir.join("open_responses_events.json"), case);
            let label = format!("{case} stream Chat Completions -> Open Responses");
            let actual_json = serde_json::to_value(&actual_events).expect(
                format!("{case} stream CC->OR failed to serialize actual events to JSON").as_str(),
            );
            let expected_json = serde_json::to_value(&expected).expect(
                format!("{case} stream CC->OR failed to serialize expected events to JSON")
                    .as_str(),
            );
            common::assert_json_eq(&actual_json, &expected_json, label.as_str());
            common::check_warnings(&dir, "chat_completions_to_open_responses", warnings, case);
        }
        Direction::OpenResponsesToChatCompletions => {
            let input: Vec<OpenResponsesStreamEvent> =
                common::load_fixture(&dir.join("open_responses_events.json"), case);
            let mut stream = OpenResponsesToChatCompletionsStream::new();
            let mut actual_events = Vec::new();
            for (i, event) in input.into_iter().enumerate() {
                actual_events.extend(stream.transform(event).expect(
                    format!("{case} stream OR->CC transform failed at input event #{i}").as_str(),
                ));
            }
            actual_events.extend(
                stream
                    .flush()
                    .expect(format!("{case} stream OR->CC flush failed").as_str()),
            );
            let warnings = stream.take_warnings();

            let expected: Vec<ChatCompletionsStreamChunk> =
                common::load_fixture(&dir.join("chat_completions_events.json"), case);
            let label = format!("{case} stream Open Responses -> Chat Completions");
            let actual_json = serde_json::to_value(&actual_events).expect(
                format!("{case} stream OR->CC failed to serialize actual events to JSON").as_str(),
            );
            let expected_json = serde_json::to_value(&expected).expect(
                format!("{case} stream OR->CC failed to serialize expected events to JSON")
                    .as_str(),
            );
            common::assert_json_eq(&actual_json, &expected_json, label.as_str());
            common::check_warnings(&dir, "open_responses_to_chat_completions", warnings, case);
        }
    }
}

#[rstest]
#[case::max_tokens("max_tokens_from_cc")]
#[case::multi_output_or("multi_output_or_from_cc")]
#[case::multi_tool_use("multi_tool_use_from_cc")]
#[case::response_incomplete_or("response_incomplete_or_from_cc")]
#[case::simple_text("simple_text_from_cc")]
#[case::simple_text_or("simple_text_or_from_cc")]
#[case::thinking_and_tool_use("thinking_and_tool_use_from_cc")]
#[case::tool_use_only("tool_use_only_from_cc")]
#[case::custom_tool("custom_tool_from_cc")]
#[case::custom_tool_legacy_hybrid("custom_tool_legacy_hybrid_from_cc")]
#[case::with_annotations_or("with_annotations_or_from_cc")]
#[case::with_citations("with_citations_from_cc")]
#[case::with_function_call_or("with_function_call_or_from_cc")]
#[case::with_reasoning_no_summary_or("with_reasoning_no_summary_or_from_cc")]
#[case::with_reasoning_or("with_reasoning_or_from_cc")]
#[case::with_redacted_thinking("with_redacted_thinking_from_cc")]
#[case::with_thinking("with_thinking_from_cc")]
#[case::with_tool_use("with_tool_use_from_cc")]
#[case::namespaced_tool_use("namespaced_tool_use_from_cc")]
fn stream_chat_completions_to_open_responses(#[case] case: &str) {
    run_stream(case, Direction::ChatCompletionsToOpenResponses);
}

#[rstest]
#[case::max_tokens("max_tokens_from_or")]
#[case::multi_output_or("multi_output_or_from_or")]
#[case::multi_tool_use("multi_tool_use_from_or")]
#[case::response_incomplete_or("response_incomplete_or_from_or")]
#[case::simple_text("simple_text_from_or")]
#[case::simple_text_or("simple_text_or_from_or")]
#[case::thinking_and_tool_use("thinking_and_tool_use_from_or")]
#[case::tool_use_only("tool_use_only_from_or")]
#[case::custom_tool("custom_tool_from_or")]
#[case::custom_tool_delta_then_added("custom_tool_delta_then_added_from_or")]
#[case::with_function_call_or("with_function_call_or_from_or")]
#[case::with_reasoning_no_summary_or("with_reasoning_no_summary_or_from_or")]
#[case::with_reasoning_or("with_reasoning_or_from_or")]
#[case::with_redacted_thinking("with_redacted_thinking_from_or")]
#[case::with_thinking("with_thinking_from_or")]
#[case::with_tool_use("with_tool_use_from_or")]
fn stream_open_responses_to_chat_completions(#[case] case: &str) {
    run_stream(case, Direction::OpenResponsesToChatCompletions);
}

// ════════════════════════════════════════════════════════════════════
// Decompose / Collect conversion
// ════════════════════════════════════════════════════════════════════

const CC_FIXTURE_DIR: &str = "tests/fixtures/chat_completions_openai";

fn load_cc_response(path: &Path) -> ChatCompletionsOpenAiResponse {
    let json = std::fs::read_to_string(path)
        .unwrap_or_else(|e| panic!("failed to read {}: {e}", path.display()));
    serde_json::from_str(&json)
        .unwrap_or_else(|e| panic!("failed to parse {}: {e}", path.display()))
}

fn load_cc_events(path: &Path) -> Vec<ChatCompletionsStreamChunk> {
    let json = std::fs::read_to_string(path)
        .unwrap_or_else(|e| panic!("failed to read {}: {e}", path.display()));
    serde_json::from_str(&json)
        .unwrap_or_else(|e| panic!("failed to parse {}: {e}", path.display()))
}

#[rstest]
#[case::simple_text("simple_text")]
#[case::max_tokens("max_tokens")]
#[case::with_reasoning("with_reasoning")]
#[case::with_refusal("with_refusal")]
#[case::with_tool_calls("with_tool_calls")]
#[case::multi_tool_use("multi_tool_use")]
#[case::custom_tool_call("custom_tool_call")]
fn decompose_chat_completions(#[case] case: &str) {
    let dir =
        Path::new(env!("CARGO_MANIFEST_DIR")).join(format!("{CC_FIXTURE_DIR}/decompose/{case}"));
    let response = load_cc_response(&dir.join("chat_completions.json"));
    let expected_events = load_cc_events(&dir.join("chat_completions_events.json"));

    let result = response.decompose_to_stream().expect("decompose");

    let actual: serde_json::Value = serde_json::to_value(&result.value).unwrap();
    let expected: serde_json::Value = serde_json::to_value(&expected_events).unwrap();
    assert_eq!(actual, expected, "decompose mismatch for {case}");
    assert!(
        result.warnings.is_empty(),
        "unexpected decompose warnings for {case}: {:?}",
        result.warnings
    );
}

#[rstest]
#[case::simple_text("simple_text")]
#[case::max_tokens("max_tokens")]
#[case::with_reasoning("with_reasoning")]
#[case::with_refusal("with_refusal")]
#[case::with_tool_calls("with_tool_calls")]
#[case::multi_tool_use("multi_tool_use")]
#[case::custom_tool_call("custom_tool_call")]
fn collect_chat_completions(#[case] case: &str) {
    let dir =
        Path::new(env!("CARGO_MANIFEST_DIR")).join(format!("{CC_FIXTURE_DIR}/collect/{case}"));
    let events = load_cc_events(&dir.join("chat_completions_events.json"));
    let expected = load_cc_response(&dir.join("chat_completions.json"));

    let result = ChatCompletionsOpenAiResponse::collect_stream(events).expect("collect");

    let actual: serde_json::Value = serde_json::to_value(&result.value).unwrap();
    let exp: serde_json::Value = serde_json::to_value(&expected).unwrap();
    assert_eq!(actual, exp, "collect mismatch for {case}");
    assert!(
        result.warnings.is_empty(),
        "unexpected warnings: {:?}",
        result.warnings
    );
}

#[rstest]
#[case::simple_text("simple_text")]
#[case::max_tokens("max_tokens")]
#[case::with_reasoning("with_reasoning")]
#[case::with_refusal("with_refusal")]
#[case::with_tool_calls("with_tool_calls")]
#[case::multi_tool_use("multi_tool_use")]
#[case::custom_tool_call("custom_tool_call")]
fn round_trip_cc_decompose_collect(#[case] case: &str) {
    let dir =
        Path::new(env!("CARGO_MANIFEST_DIR")).join(format!("{CC_FIXTURE_DIR}/decompose/{case}"));
    let original = load_cc_response(&dir.join("chat_completions.json"));

    let events = original
        .clone()
        .decompose_to_stream()
        .expect("decompose")
        .value;
    let collected = ChatCompletionsOpenAiResponse::collect_stream(events).expect("collect");

    let orig: serde_json::Value = serde_json::to_value(&original).unwrap();
    let coll: serde_json::Value = serde_json::to_value(&collected.value).unwrap();
    assert_eq!(coll, orig, "round-trip mismatch for {case}");
    assert!(collected.warnings.is_empty());
}

#[rstest]
#[case::summary(Some("THINK"))]
#[case::carrier_only(None)]
#[case::empty_summary(Some(""))]
fn response_reasoning_details_carrier(#[case] reasoning_content: Option<&str>) {
    use linguafranca::traits::IntoOpenResponses;
    use serde_json::json;

    let envelope = "lf-er:v1:k1:opaque+/=\nexact";
    let details = json!([
        {"type": "reasoning.text", "text": "ignored"},
        {
            "type": "reasoning.encrypted", "data": envelope,
            "format": "provider-specific", "index": 0, "provider_extra": {"v": 1}
        },
        {"type": "reasoning.encrypted", "data": "not-the-first-carrier"}
    ]);
    let response: ChatCompletionsOpenAiResponse = serde_json::from_value(json!({
        "id": "chatcmpl_carrier", "object": "chat.completion", "created": 1,
        "model": "deepseek", "choices": [{
            "index": 0, "finish_reason": "stop",
            "message": {"role": "assistant", "reasoning_content": reasoning_content,
                        "reasoning_details": details}
        }]
    }))
    .unwrap();
    assert_eq!(
        serde_json::to_value(&response).unwrap()["choices"][0]["message"]["reasoning_details"],
        details
    );

    let result = response.into_open_responses(None).unwrap();
    assert!(result.warnings.is_empty());
    let output = serde_json::to_value(result.value.output).unwrap();
    assert_eq!(output.as_array().unwrap().len(), 1);
    assert_eq!(output[0]["type"], "reasoning");
    assert_eq!(output[0]["encrypted_content"], envelope);
    let summary = match reasoning_content.filter(|text| !text.is_empty()) {
        Some(text) => json!([{"type": "summary_text", "text": text}]),
        None => json!([]),
    };
    assert_eq!(output[0]["summary"], summary);
}

#[rstest]
#[case::finish(true, false, false)]
#[case::tool_calls_after_carrier(true, false, true)]
#[case::content_before_carrier(true, true, false)]
#[case::gateway_carrier_after_content_and_tools(true, true, true)]
#[case::carrier_only_after_content(false, true, false)]
#[case::carrier_only_after_content_and_tools(false, true, true)]
fn stream_reasoning_details_carrier(
    #[case] has_reasoning: bool,
    #[case] late_carrier: bool,
    #[case] with_tool_call: bool,
) {
    use serde_json::json;

    let envelope = "lf-er:v1:k1:stream-carrier+/=";
    let carrier = json!({"reasoning_details": [{
        "type": "reasoning.encrypted", "data": envelope, "format": "unknown", "index": 0
    }]});
    let mut deltas = Vec::new();
    if has_reasoning {
        deltas.push(json!({"role": "assistant", "reasoning_content": "TH"}));
        deltas.push(json!({"reasoning_content": "INK"}));
    }
    if late_carrier {
        deltas.push(json!({"content": "Checking"}));
    } else {
        deltas.push(carrier.clone());
    }
    if with_tool_call {
        deltas.push(json!({"tool_calls": [{
            "index": 0, "id": "call_1", "type": "function",
            "function": {"name": "lookup", "arguments": "{"}
        }]}));
        deltas.push(json!({"tool_calls": [{
            "index": 0, "function": {"arguments": "}"}
        }]}));
    }
    if late_carrier {
        deltas.push(carrier);
    }
    let mut stream = ChatCompletionsToOpenResponsesStream::new();
    let mut events = Vec::new();
    for delta in deltas {
        let is_carrier = delta.get("reasoning_details").is_some();
        let chunk = serde_json::from_value(json!({
            "id": "chatcmpl_carrier", "object": "chat.completion.chunk", "created": 1,
            "model": "deepseek", "choices": [{"index": 0, "delta": delta}]
        }))
        .unwrap();
        let emitted = stream.transform(chunk).unwrap();
        if is_carrier {
            assert!(emitted.is_empty(), "carrier must not open or close items");
        }
        events.extend(emitted);
    }
    assert!(!events.iter().any(|event| matches!(
        event,
        OpenResponsesStreamEvent::OutputItemDone {
            item: linguafranca::open_responses::types::OutputItem::Reasoning { .. },
            ..
        }
    )));
    events.extend(
        stream
            .transform(
                serde_json::from_value(json!({
                    "id": "chatcmpl_carrier", "object": "chat.completion.chunk", "created": 1,
                    "model": "deepseek", "choices": [{
                        "index": 0, "delta": {},
                        "finish_reason": if with_tool_call { "tool_calls" } else { "stop" }
                    }]
                }))
                .unwrap(),
            )
            .unwrap(),
    );
    events.extend(stream.flush().unwrap());
    assert!(stream.take_warnings().is_empty());

    let events = serde_json::to_value(events).unwrap();
    let events = events.as_array().unwrap();
    let reasoning_done = events
        .iter()
        .find(|event| {
            event["type"] == "response.output_item.done" && event["item"]["type"] == "reasoning"
        })
        .unwrap();
    assert_eq!(reasoning_done["item"]["encrypted_content"], envelope);
    let completed = events.last().unwrap();
    assert_eq!(completed["type"], "response.completed");
    let output = completed["response"]["output"].as_array().unwrap();
    let reasoning: Vec<_> = output
        .iter()
        .filter(|item| item["type"] == "reasoning")
        .collect();
    assert_eq!(reasoning.len(), 1);
    assert_eq!(reasoning[0]["encrypted_content"], envelope);
    assert_eq!(reasoning[0], &reasoning_done["item"]);
    assert_eq!(
        reasoning[0]["summary"],
        if has_reasoning {
            json!([{"type": "summary_text", "text": "THINK"}])
        } else {
            json!([])
        }
    );
    let mut expected_types = Vec::new();
    if has_reasoning {
        expected_types.push("reasoning");
    }
    if late_carrier {
        expected_types.push("message");
    }
    if with_tool_call {
        expected_types.push("function_call");
    }
    if !has_reasoning {
        expected_types.push("reasoning");
    }
    assert_eq!(
        output
            .iter()
            .map(|item| item["type"].as_str().unwrap())
            .collect::<Vec<_>>(),
        expected_types
    );
    for event in events.iter().filter(|event| {
        event["type"] == "response.output_item.added"
            || event["type"] == "response.output_item.done"
    }) {
        let index = event["output_index"].as_u64().unwrap() as usize;
        assert_eq!(output[index]["id"], event["item"]["id"]);
    }
    assert_eq!(
        events
            .iter()
            .filter(|event| event["type"] == "response.output_item.done")
            .count(),
        output.len()
    );
}

#[rstest]
#[case::absent(serde_json::Value::Null, false)]
#[case::empty(serde_json::json!([]), false)]
#[case::unsupported(serde_json::json!([{"type": "reasoning.text", "text": "lost"}]), true)]
#[case::invalid_carrier(serde_json::json!([{"type": "reasoning.encrypted", "data": 123}]), true)]
#[case::supported(serde_json::json!([{"type": "reasoning.encrypted", "data": "opaque"}]), false)]
fn unsupported_reasoning_details_warn_in_request_response_and_stream(
    #[case] details: serde_json::Value,
    #[case] should_warn: bool,
) {
    use linguafranca::error::WarningAction;
    use linguafranca::traits::IntoOpenResponses;
    use serde_json::json;

    let response: ChatCompletionsOpenAiResponse = serde_json::from_value(json!({
        "id": "chatcmpl_details", "object": "chat.completion", "created": 1,
        "model": "deepseek", "choices": [{"index": 0, "finish_reason": "stop",
            "message": {"role": "assistant", "reasoning_details": details}}]
    }))
    .unwrap();
    let warnings = response.into_open_responses(None).unwrap().warnings;
    assert_eq!(warnings.len(), usize::from(should_warn));
    if should_warn {
        assert_eq!(warnings[0].field, "choices[0].message.reasoning_details");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
    }

    let mut stream = ChatCompletionsToOpenResponsesStream::new();
    stream
        .transform(
            serde_json::from_value(json!({
                "id": "chatcmpl_details", "object": "chat.completion.chunk", "created": 1,
                "model": "deepseek", "choices": [{"index": 0, "finish_reason": "stop",
                    "delta": {"role": "assistant", "reasoning_details": details}}]
            }))
            .unwrap(),
        )
        .unwrap();
    stream.flush().unwrap();
    let warnings = stream.take_warnings();
    assert_eq!(warnings.len(), usize::from(should_warn));
    if should_warn {
        assert_eq!(warnings[0].field, "choices[0].delta.reasoning_details");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
    }

    let request: ChatCompletionsOpenAiRequest = serde_json::from_value(json!({
        "model": "deepseek", "messages": [{
            "role": "assistant", "reasoning_details": details
        }]
    }))
    .unwrap();
    let warnings = request.into_open_responses(None).unwrap().warnings;
    assert_eq!(warnings.len(), usize::from(should_warn));
    if should_warn {
        assert_eq!(warnings[0].field, "messages[0].reasoning_details");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
    }
}

#[rstest]
#[case::summary(Some("THINK"), "data")]
#[case::carrier_only(None, "data")]
#[case::encrypted_content_alias(Some("THINK"), "encrypted_content")]
fn request_reasoning_details_carrier(#[case] summary: Option<&str>, #[case] data_key: &str) {
    use linguafranca::traits::IntoOpenResponses;
    use serde_json::json;

    let envelope = "lf-er:v1:k1:request+/=\nexact";
    let request: ChatCompletionsOpenAiRequest = serde_json::from_value(json!({
        "model": "deepseek", "messages": [{
            "role": "assistant", "reasoning_content": summary,
            "reasoning_details": [{"type": "reasoning.encrypted", (data_key): envelope}]
        }]
    }))
    .unwrap();
    let converted = request.into_open_responses(None).unwrap();
    assert!(converted.warnings.is_empty());
    let input = serde_json::to_value(converted.value.input).unwrap();
    assert_eq!(input.as_array().unwrap().len(), 1);
    assert_eq!(input[0]["type"], "reasoning");
    assert_eq!(input[0]["encrypted_content"], envelope);
    assert_eq!(
        input[0]["summary"],
        match summary {
            Some(text) => json!([{"type": "summary_text", "text": text}]),
            None => json!([]),
        }
    );
}

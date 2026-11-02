use std::path::Path;

use linguafranca::anthropic::convert::stream::{
    AnthropicMessagesToOpenResponsesStream, OpenResponsesToAnthropicMessagesStream,
};
use linguafranca::anthropic::request::AnthropicRequest;
use linguafranca::anthropic::response::AnthropicResponse;
use linguafranca::anthropic::stream::AnthropicStreamEvent;
use linguafranca::open_responses::request::OpenResponsesRequest;
use linguafranca::open_responses::response::OpenResponsesResponse;
use linguafranca::open_responses::stream::OpenResponsesStreamEvent;
use linguafranca::stream::StreamTransform;
use linguafranca::traits::{CollectStream, DecomposeToStream};
use rstest::rstest;

mod common;

enum Direction {
    AnthropicMessagesToOpenResponses,
    OpenResponsesToAnthropicMessages,
}

fn run(case: &str, direction: Direction) {
    let dir = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join(format!("tests/fixtures/anthropic_messages/request/{case}"));

    match direction {
        Direction::AnthropicMessagesToOpenResponses => {
            let label = format!("{case} Anthropic Messages -> Open Responses");
            common::run_into_open_responses_case::<AnthropicRequest, OpenResponsesRequest>(
                case,
                &dir,
                "messages.json",
                "open_responses.json",
                "messages_to_open_responses",
                label.as_str(),
            );
        }
        Direction::OpenResponsesToAnthropicMessages => {
            let label = format!("{case} Open Responses -> Anthropic Messages");
            common::run_from_open_responses_case::<AnthropicRequest, OpenResponsesRequest>(
                case,
                &dir,
                "messages.json",
                "open_responses.json",
                "open_responses_to_messages",
                label.as_str(),
            );
        }
    }
}

// ── Bidirectional ──

#[rstest]
#[case::simple_text("simple_text")]
#[case::with_system("with_system")]
#[case::system_blocks("system_blocks")]
#[case::multi_turn("multi_turn")]
#[case::with_tools("with_tools")]
#[case::tool_use_conversation("tool_use_conversation")]
#[case::with_image("with_image")]
#[case::with_image_url("with_image_url")]
#[case::with_json_schema("with_json_schema")]
#[case::assistant_output_text("assistant_output_text")]
#[case::mid_conversation_system_opus48("mid_conversation_system_opus48")]
fn anthropic_messages_to_open_responses(#[case] case: &str) {
    run(case, Direction::AnthropicMessagesToOpenResponses);
}

#[rstest]
#[case::simple_text("simple_text")]
#[case::with_system("with_system")]
#[case::system_blocks("system_blocks")]
#[case::multi_turn("multi_turn")]
#[case::with_tools("with_tools")]
#[case::tool_use_conversation("tool_use_conversation")]
#[case::with_image("with_image")]
#[case::with_image_url("with_image_url")]
#[case::with_json_schema("with_json_schema")]
#[case::assistant_output_text("assistant_output_text")]
fn open_responses_to_anthropic_messages(#[case] case: &str) {
    run(case, Direction::OpenResponsesToAnthropicMessages);
}

// ── Anthropic Messages → Open Responses only ──

#[rstest]
#[case::dropped_fields_messages("dropped_fields_messages")]
#[case::with_reasoning_messages("with_reasoning_messages")]
#[case::reasoning_items_messages("reasoning_items_messages")]
#[case::with_output_effort_and_adaptive("with_output_effort_and_adaptive")]
#[case::with_max_output_effort("with_max_output_effort")]
#[case::web_search_history_am_to_or("web_search_history_am_to_or")]
#[case::tool_search_am_to_or("tool_search_am_to_or")]
fn anthropic_messages_to_open_responses_only(#[case] case: &str) {
    run(case, Direction::AnthropicMessagesToOpenResponses);
}

// ── Open Responses → Anthropic Messages only ──

#[rstest]
#[case::dropped_fields_open_responses("dropped_fields_open_responses")]
#[case::with_reasoning_open_responses("with_reasoning_open_responses")]
#[case::with_output_effort_and_adaptive("with_output_effort_and_adaptive")]
#[case::with_max_output_effort("with_max_output_effort")]
#[case::default_max_tokens("default_max_tokens")]
#[case::simple_text_string_open_responses("simple_text_string_open_responses")]
#[case::reasoning_items_open_responses("reasoning_items_open_responses")]
#[case::web_search_call_dropped_or_to_am("web_search_call_dropped_or_to_am")]
#[case::system_and_developer_open_responses("system_and_developer_open_responses")]
#[case::instructions_dropped_open_responses("instructions_dropped_open_responses")]
#[case::interleaved_developer_hoisted_open_responses(
    "interleaved_developer_hoisted_open_responses"
)]
#[case::interleaved_non_text_instruction_dropped_open_responses(
    "interleaved_non_text_instruction_dropped_open_responses"
)]
#[case::mid_conversation_system_opus48("mid_conversation_system_opus48")]
#[case::mid_conv_system_invalid_placement_opus48("mid_conv_system_invalid_placement_opus48")]
#[case::mid_conv_system_hoist_merges_neighbors_opus48(
    "mid_conv_system_hoist_merges_neighbors_opus48"
)]
#[case::tool_choice_missing_name_open_responses("tool_choice_missing_name_open_responses")]
#[case::allowed_tools_dropped_open_responses("allowed_tools_dropped_open_responses")]
#[case::namespace_tools_open_responses("namespace_tools_open_responses")]
fn open_responses_to_anthropic_messages_only(#[case] case: &str) {
    run(case, Direction::OpenResponsesToAnthropicMessages);
}

// ════════════════════════════════════════════════════════════════════
// Response conversion
// ════════════════════════════════════════════════════════════════════

fn run_response(case: &str, direction: Direction) {
    let dir = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join(format!("tests/fixtures/anthropic_messages/response/{case}"));

    match direction {
        Direction::AnthropicMessagesToOpenResponses => {
            let label = format!("{case} Anthropic Messages -> Open Responses");
            common::run_into_open_responses_case::<AnthropicResponse, OpenResponsesResponse>(
                case,
                &dir,
                "messages.json",
                "open_responses.json",
                "messages_to_open_responses",
                label.as_str(),
            );
        }
        Direction::OpenResponsesToAnthropicMessages => {
            let label = format!("{case} Open Responses -> Anthropic Messages");
            common::run_from_open_responses_case::<AnthropicResponse, OpenResponsesResponse>(
                case,
                &dir,
                "messages.json",
                "open_responses.json",
                "open_responses_to_messages",
                label.as_str(),
            );
        }
    }
}

// ── Bidirectional (response) ──

#[rstest]
#[case::simple_text("simple_text")]
#[case::with_tool_use("with_tool_use")]
#[case::with_thinking("with_thinking")]
#[case::max_tokens("max_tokens")]
#[case::redacted_thinking("redacted_thinking")]
#[case::multi_tool_use("multi_tool_use")]
#[case::namespaced_tool_use("namespaced_tool_use")]
fn resp_anthropic_messages_to_open_responses(#[case] case: &str) {
    run_response(case, Direction::AnthropicMessagesToOpenResponses);
}

#[rstest]
#[case::simple_text("simple_text")]
#[case::with_tool_use("with_tool_use")]
#[case::with_thinking("with_thinking")]
#[case::max_tokens("max_tokens")]
#[case::redacted_thinking("redacted_thinking")]
#[case::multi_tool_use("multi_tool_use")]
#[case::namespaced_tool_use("namespaced_tool_use")]
fn resp_open_responses_to_anthropic_messages(#[case] case: &str) {
    run_response(case, Direction::OpenResponsesToAnthropicMessages);
}

// ── Anthropic Messages → Open Responses only (response) ──

#[rstest]
#[case::with_citations("with_citations")]
#[case::dropped_fields_messages("dropped_fields_messages")]
#[case::web_search_messages("web_search_messages")]
#[case::namespaced_tool_search("namespaced_tool_search")]
fn resp_anthropic_messages_to_open_responses_only(#[case] case: &str) {
    run_response(case, Direction::AnthropicMessagesToOpenResponses);
}

// ── Open Responses → Anthropic Messages only (response) ──

#[rstest]
#[case::dropped_fields_open_responses("dropped_fields_open_responses")]
#[case::with_refusal("with_refusal")]
#[case::function_call_output_open_responses("function_call_output_open_responses")]
#[case::with_citations_open_responses("with_citations_open_responses")]
fn resp_open_responses_to_anthropic_messages_only(#[case] case: &str) {
    run_response(case, Direction::OpenResponsesToAnthropicMessages);
}

// ════════════════════════════════════════════════════════════════════
// Stream conversion
// ════════════════════════════════════════════════════════════════════

fn run_stream(case: &str, direction: Direction) {
    let dir = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join(format!("tests/fixtures/anthropic_messages/stream/{case}"));

    match direction {
        Direction::AnthropicMessagesToOpenResponses => {
            let input: Vec<AnthropicStreamEvent> =
                common::load_fixture(&dir.join("messages_events.json"), case);
            let mut stream = AnthropicMessagesToOpenResponsesStream::new();
            let mut actual_events = Vec::new();
            for event in input {
                actual_events.extend(stream.transform(event).unwrap());
            }
            actual_events.extend(stream.flush().unwrap());
            let warnings = stream.take_warnings();

            let expected: serde_json::Value =
                common::load_fixture(&dir.join("open_responses_events.json"), case);
            let label = format!("{case} stream Anthropic Messages -> Open Responses");
            common::assert_json_eq(
                &serde_json::to_value(&actual_events).unwrap(),
                &expected,
                label.as_str(),
            );
            common::check_warnings(&dir, "messages_to_open_responses", warnings, case);
        }
        Direction::OpenResponsesToAnthropicMessages => {
            let input: Vec<OpenResponsesStreamEvent> =
                common::load_fixture(&dir.join("open_responses_events.json"), case);
            let mut stream = OpenResponsesToAnthropicMessagesStream::new();
            let mut actual_events = Vec::new();
            for event in input {
                actual_events.extend(stream.transform(event).unwrap());
            }
            actual_events.extend(stream.flush().unwrap());
            let warnings = stream.take_warnings();

            let expected: serde_json::Value =
                common::load_fixture(&dir.join("messages_events.json"), case);
            let label = format!("{case} stream Open Responses -> Anthropic Messages");
            common::assert_json_eq(
                &serde_json::to_value(&actual_events).unwrap(),
                &expected,
                label.as_str(),
            );
            common::check_warnings(&dir, "open_responses_to_messages", warnings, case);
        }
    }
}

// ── Anthropic Messages → Open Responses stream ──

#[rstest]
#[case::simple_text("simple_text")]
#[case::tool_use_only("tool_use_only")]
#[case::with_thinking("with_thinking")]
#[case::max_tokens("max_tokens")]
#[case::thinking_and_tool_use("thinking_and_tool_use")]
#[case::with_tool_use("with_tool_use")]
#[case::multi_tool_use("multi_tool_use")]
#[case::stop_sequence("stop_sequence")]
#[case::web_search_messages("web_search_messages")]
#[case::tool_search_messages("tool_search_messages")]
#[case::namespaced_tool_search_messages("namespaced_tool_search_messages")]
#[case::with_citations_delta("with_citations_delta")]
#[case::with_error_messages("with_error_messages")]
#[case::with_heartbeat("with_heartbeat")]
#[case::namespaced_tool_use_only("namespaced_tool_use_only")]
fn stream_anthropic_messages_to_open_responses(#[case] case: &str) {
    run_stream(case, Direction::AnthropicMessagesToOpenResponses);
}

// ── Open Responses → Anthropic Messages stream ──

#[rstest]
#[case::simple_text_open_responses("simple_text_open_responses")]
#[case::with_function_call_open_responses("with_function_call_open_responses")]
#[case::with_reasoning_open_responses("with_reasoning_open_responses")]
#[case::response_incomplete_open_responses("response_incomplete_open_responses")]
#[case::multi_output_open_responses("multi_output_open_responses")]
#[case::with_reasoning_no_summary_open_responses("with_reasoning_no_summary_open_responses")]
#[case::with_refusal_open_responses("with_refusal_open_responses")]
#[case::with_annotations_open_responses("with_annotations_open_responses")]
#[case::with_keepalive_open_responses("with_keepalive_open_responses")]
fn stream_open_responses_to_anthropic_messages(#[case] case: &str) {
    run_stream(case, Direction::OpenResponsesToAnthropicMessages);
}

// ════════════════════════════════════════════════════════════════════
// Decompose / Collect conversion
// ════════════════════════════════════════════════════════════════════

fn run_decompose_anthropic(case: &str) {
    let dir = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("tests/fixtures/anthropic_messages/decompose")
        .join(case);

    let response: AnthropicResponse = common::load_fixture(&dir.join("messages.json"), case);
    let expected: Vec<AnthropicStreamEvent> =
        common::load_fixture(&dir.join("messages_events.json"), case);

    let result = response
        .decompose_to_stream()
        .unwrap_or_else(|e| panic!("{case} decompose failed: {e}"));

    let actual_json = serde_json::to_value(&result.value).expect("serialize actual events");
    let expected_json = serde_json::to_value(&expected).expect("serialize expected events");

    common::assert_json_eq(&actual_json, &expected_json, &format!("{case} decompose"));

    assert!(
        result.warnings.is_empty(),
        "{case} decompose produced unexpected warnings: {:?}",
        result.warnings
    );
}

fn run_collect_anthropic(case: &str) {
    let dir = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("tests/fixtures/anthropic_messages/collect")
        .join(case);

    let events: Vec<AnthropicStreamEvent> =
        common::load_fixture(&dir.join("messages_events.json"), case);
    let expected: AnthropicResponse = common::load_fixture(&dir.join("messages.json"), case);

    let result = AnthropicResponse::collect_stream(events)
        .unwrap_or_else(|e| panic!("{case} collect failed: {e}"));

    let actual_json = serde_json::to_value(&result.value).expect("serialize actual response");
    let expected_json = serde_json::to_value(&expected).expect("serialize expected response");

    common::assert_json_eq(&actual_json, &expected_json, &format!("{case} collect"));

    common::check_warnings(&dir, "collect", result.warnings, case);
}

// ── Decompose: Response → Stream events ──

#[rstest]
#[case::simple_text("simple_text")]
#[case::with_tool_use("with_tool_use")]
#[case::with_thinking("with_thinking")]
#[case::redacted_thinking("redacted_thinking")]
#[case::multi_tool_use("multi_tool_use")]
#[case::max_tokens("max_tokens")]
fn decompose_anthropic_response(#[case] case: &str) {
    run_decompose_anthropic(case);
}

// ── Collect: Stream events → Response ──

#[rstest]
#[case::simple_text("simple_text")]
#[case::with_tool_use("with_tool_use")]
#[case::with_thinking("with_thinking")]
#[case::max_tokens("max_tokens")]
#[case::multi_tool_use("multi_tool_use")]
#[case::stop_sequence("stop_sequence")]
#[case::with_citations_delta("with_citations_delta")]
fn collect_anthropic_stream(#[case] case: &str) {
    run_collect_anthropic(case);
}

// ── Round-trip: decompose then collect should recover the original ──

#[rstest]
#[case::simple_text("simple_text")]
#[case::with_tool_use("with_tool_use")]
#[case::with_thinking("with_thinking")]
#[case::redacted_thinking("redacted_thinking")]
#[case::multi_tool_use("multi_tool_use")]
#[case::max_tokens("max_tokens")]
fn round_trip_anthropic_decompose_collect(#[case] case: &str) {
    let dir = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("tests/fixtures/anthropic_messages/response")
        .join(case);

    let original: AnthropicResponse = common::load_fixture(&dir.join("messages.json"), case);

    let decompose_result = original.clone().decompose_to_stream().expect("decompose");

    assert!(
        decompose_result.warnings.is_empty(),
        "{case} decompose produced unexpected warnings: {:?}",
        decompose_result.warnings
    );

    let collected = AnthropicResponse::collect_stream(decompose_result.value).expect("collect");

    let original_json = serde_json::to_value(&original).expect("serialize original");
    let collected_json = serde_json::to_value(&collected.value).expect("serialize collected");

    common::assert_json_eq(
        &collected_json,
        &original_json,
        &format!("{case} round-trip"),
    );

    assert!(
        collected.warnings.is_empty(),
        "{case} round-trip collect produced warnings: {:?}",
        collected.warnings
    );
}

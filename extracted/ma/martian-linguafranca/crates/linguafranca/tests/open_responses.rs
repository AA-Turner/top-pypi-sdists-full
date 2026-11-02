use std::path::Path;

use linguafranca::open_responses::response::OpenResponsesResponse;
use linguafranca::open_responses::stream::OpenResponsesStreamEvent;
use linguafranca::traits::{CollectStream, DecomposeToStream};
use rstest::rstest;

mod common;

fn run_decompose(case: &str) {
    let dir = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("tests/fixtures/open_responses/decompose")
        .join(case);

    let response: OpenResponsesResponse = common::load_fixture(&dir.join("response.json"), case);
    let expected: Vec<OpenResponsesStreamEvent> =
        common::load_fixture(&dir.join("events.json"), case);

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

fn run_collect(case: &str) {
    let dir = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("tests/fixtures/open_responses/collect")
        .join(case);

    let events: Vec<OpenResponsesStreamEvent> =
        common::load_fixture(&dir.join("events.json"), case);
    let expected: OpenResponsesResponse = common::load_fixture(&dir.join("response.json"), case);

    let result = OpenResponsesResponse::collect_stream(events)
        .unwrap_or_else(|e| panic!("{case} collect failed: {e}"));

    let actual_json = serde_json::to_value(&result.value).expect("serialize actual response");
    let expected_json = serde_json::to_value(&expected).expect("serialize expected response");

    common::assert_json_eq(&actual_json, &expected_json, &format!("{case} collect"));

    common::check_warnings(&dir, "collect", result.warnings, case);
}

// ── Decompose: Response → Stream events ──

#[rstest]
#[case::simple_text("simple_text")]
#[case::with_reasoning("with_reasoning")]
#[case::with_function_call("with_function_call")]
#[case::with_custom_tool_call("with_custom_tool_call")]
#[case::with_web_search_call("with_web_search_call")]
#[case::with_function_call_output("with_function_call_output")]
#[case::with_refusal("with_refusal")]
#[case::with_annotations("with_annotations")]
#[case::reasoning_and_message("reasoning_and_message")]
#[case::mixed_output_types("mixed_output_types")]
#[case::incomplete_response("incomplete_response")]
#[case::failed_response("failed_response")]
fn decompose_to_stream(#[case] case: &str) {
    run_decompose(case);
}

// ── Collect: Stream events → Response ──

#[rstest]
#[case::simple_text("simple_text")]
#[case::no_terminal("no_terminal")]
#[case::failed("failed")]
#[case::incomplete("incomplete")]
#[case::with_custom_tool_call("with_custom_tool_call")]
#[case::with_web_search_call("with_web_search_call")]
#[case::with_function_call_output("with_function_call_output")]
#[case::mixed_output_types("mixed_output_types")]
fn collect_stream(#[case] case: &str) {
    run_collect(case);
}

// ── Round-trip: decompose then collect should recover the original ──

#[rstest]
#[case::simple_text("simple_text")]
#[case::with_reasoning("with_reasoning")]
#[case::with_function_call("with_function_call")]
#[case::with_custom_tool_call("with_custom_tool_call")]
#[case::with_web_search_call("with_web_search_call")]
#[case::with_function_call_output("with_function_call_output")]
#[case::with_refusal("with_refusal")]
#[case::with_annotations("with_annotations")]
#[case::reasoning_and_message("reasoning_and_message")]
#[case::mixed_output_types("mixed_output_types")]
#[case::incomplete_response("incomplete_response")]
#[case::failed_response("failed_response")]
fn round_trip_decompose_collect(#[case] case: &str) {
    let dir = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("tests/fixtures/open_responses/decompose")
        .join(case);

    let original: OpenResponsesResponse = common::load_fixture(&dir.join("response.json"), case);

    let decompose_result = original.clone().decompose_to_stream().expect("decompose");

    assert!(
        decompose_result.warnings.is_empty(),
        "{case} decompose produced unexpected warnings: {:?}",
        decompose_result.warnings
    );

    let collected = OpenResponsesResponse::collect_stream(decompose_result.value).expect("collect");

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

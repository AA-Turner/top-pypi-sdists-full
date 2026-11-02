use std::path::Path;

use linguafranca::anthropic::request::AnthropicRequest;
use linguafranca::config::ConversionConfig;
use linguafranca::open_responses::request::OpenResponsesRequest;
use linguafranca::traits::{FromOpenResponses, IntoOpenResponses};
use rstest::rstest;

mod common;

fn strip_config() -> Option<ConversionConfig> {
    Some(ConversionConfig {
        strip_encrypted_reasoning: true,
    })
}

fn run_am_to_or(case: &str) {
    let dir = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join(format!("tests/fixtures/anthropic_messages/request/{case}"));

    let input: AnthropicRequest = common::load_fixture(&dir.join("messages.json"), case);
    let result = input.into_open_responses(strip_config()).unwrap();
    let expected: serde_json::Value = common::load_fixture(&dir.join("open_responses.json"), case);
    common::assert_json_eq(
        &serde_json::to_value(&result.value).unwrap(),
        &expected,
        &format!("{case} AM->OR with strip_encrypted_reasoning"),
    );
}

fn run_or_to_am(case: &str) {
    let dir = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join(format!("tests/fixtures/anthropic_messages/request/{case}"));

    let input: OpenResponsesRequest = common::load_fixture(&dir.join("open_responses.json"), case);
    let result = AnthropicRequest::from_open_responses(input, strip_config()).unwrap();
    let expected: serde_json::Value = common::load_fixture(&dir.join("messages.json"), case);
    common::assert_json_eq(
        &serde_json::to_value(&result.value).unwrap(),
        &expected,
        &format!("{case} OR->AM with strip_encrypted_reasoning"),
    );
}

#[rstest]
#[case::strip_thinking_am_to_or("strip_thinking_am_to_or")]
#[case::strip_redacted_thinking_am_to_or("strip_redacted_thinking_am_to_or")]
fn strip_am_to_or(#[case] case: &str) {
    run_am_to_or(case);
}

#[rstest]
#[case::strip_reasoning_or_to_am("strip_reasoning_or_to_am")]
fn strip_or_to_am(#[case] case: &str) {
    run_or_to_am(case);
}

#![allow(dead_code)]

use std::path::Path;

use linguafranca::error::{ConversionWarning, WarningAction};
use linguafranca::stream::StreamTransform;
use linguafranca::traits::{FromOpenResponses, IntoOpenResponses};
use pretty_assertions::assert_eq;
use serde::Serialize;
use serde::de::DeserializeOwned;

pub fn load_fixture<T: DeserializeOwned>(path: &Path, case: &str) -> T {
    let json = std::fs::read_to_string(path)
        .unwrap_or_else(|e| panic!("failed to read {}: {e}", path.display()));
    serde_json::from_str(&json).unwrap_or_else(|e| {
        panic!(
            "{case}/{} parse error: {e}",
            path.file_name().unwrap().to_str().unwrap()
        )
    })
}

pub fn assert_json_eq(actual: &serde_json::Value, expected: &serde_json::Value, label: &str) {
    let actual_pretty = serde_json::to_string_pretty(actual).unwrap();
    let expected_pretty = serde_json::to_string_pretty(expected).unwrap();
    assert_eq!(actual_pretty, expected_pretty, "{label}");
}

pub fn check_warnings(dir: &Path, direction: &str, warnings: Vec<ConversionWarning>, case: &str) {
    let path = dir.join(format!("warnings.{direction}.json"));
    if path.exists() {
        let expected: Vec<WarningFixture> = load_fixture(&path, case);
        let actual: Vec<WarningFixture> = warnings
            .into_iter()
            .map(|w| WarningFixture {
                field: w.field,
                action: w.action,
                message: w.message,
            })
            .collect();
        assert_eq!(actual, expected, "{case} {direction} warnings mismatch");
    } else {
        assert!(
            warnings.is_empty(),
            "{case} {direction} produced unexpected warnings: {warnings:?}"
        );
    }
}

pub fn run_into_open_responses_case<S, O>(
    case: &str,
    dir: &Path,
    source_filename: &str,
    open_responses_filename: &str,
    warning_direction: &str,
    label: &str,
) where
    S: DeserializeOwned + IntoOpenResponses<Target = O>,
    O: Serialize,
{
    let input: S = load_fixture(&dir.join(source_filename), case);
    let result = input.into_open_responses(None).unwrap();
    let expected: serde_json::Value = load_fixture(&dir.join(open_responses_filename), case);
    assert_json_eq(
        &serde_json::to_value(&result.value).unwrap(),
        &expected,
        label,
    );
    check_warnings(dir, warning_direction, result.warnings, case);
}

pub fn run_from_open_responses_case<T, O>(
    case: &str,
    dir: &Path,
    target_filename: &str,
    open_responses_filename: &str,
    warning_direction: &str,
    label: &str,
) where
    T: FromOpenResponses<Source = O> + Serialize,
    O: DeserializeOwned,
{
    let input: O = load_fixture(&dir.join(open_responses_filename), case);
    let result = T::from_open_responses(input, None).unwrap();
    let expected: serde_json::Value = load_fixture(&dir.join(target_filename), case);
    assert_json_eq(
        &serde_json::to_value(&result.value).unwrap(),
        &expected,
        label,
    );
    check_warnings(dir, warning_direction, result.warnings, case);
}

#[derive(Debug, PartialEq, serde::Deserialize, serde::Serialize)]
struct WarningFixture {
    field: String,
    action: WarningAction,
    message: String,
}

// ── Round-trip test support ──

#[derive(Debug, serde::Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum DiffOp {
    /// Remove the value at `path`. No-op if absent.
    Remove,
    /// Replace the value at `path` with `value`. No-op if absent.
    Replace,
    /// Add `value` at `path`.
    Add,
    /// Field value changes unpredictably — strip from both sides before comparing.
    Any,
    /// Remove array elements at `path` that match all fields in `match`.
    RemoveMatching,
}

#[derive(Debug, serde::Deserialize)]
pub struct ConversionDiff {
    /// JSON Pointer (RFC 6901), e.g. "/stop_sequences" or "/content/0/cited_text".
    pub path: String,
    pub op: DiffOp,
    /// Required for `replace` and `add`.
    #[serde(default)]
    pub value: Option<serde_json::Value>,
    /// Required for `remove_matching`: fields that must all match for removal.
    #[serde(default, rename = "match")]
    pub match_criteria: Option<serde_json::Map<String, serde_json::Value>>,
    #[allow(dead_code)]
    pub reason: String,
}

pub fn load_diffs(path: &Path) -> Vec<ConversionDiff> {
    let json = std::fs::read_to_string(path)
        .unwrap_or_else(|e| panic!("failed to read diffs {}: {e}", path.display()));
    serde_json::from_str(&json)
        .unwrap_or_else(|e| panic!("failed to parse diffs {}: {e}", path.display()))
}

fn add_at(json: &mut serde_json::Value, path: &str, new_value: serde_json::Value) {
    let (parent_pointer, last_key) = match path.rfind('/') {
        Some(pos) => (&path[..pos], &path[pos + 1..]),
        None => return,
    };
    let last_key = last_key.to_string();
    let parent = if parent_pointer.is_empty() {
        json
    } else {
        match json.pointer_mut(parent_pointer) {
            Some(p) => p,
            None => return,
        }
    };
    match parent {
        serde_json::Value::Object(map) => {
            map.insert(last_key, new_value);
        }
        serde_json::Value::Array(arr) => {
            if let Ok(idx) = last_key.parse::<usize>() {
                if idx <= arr.len() {
                    arr.insert(idx, new_value);
                }
            } else if last_key == "-" {
                arr.push(new_value);
            }
        }
        _ => {}
    }
}

pub fn apply_diffs(json: &mut serde_json::Value, diffs: &[ConversionDiff]) {
    for diff in diffs {
        match diff.op {
            DiffOp::Remove => {
                remove_at(json, &diff.path);
            }
            DiffOp::Replace => {
                let new_value = diff.value.as_ref().expect("replace diff missing 'value'");
                let segments: Vec<&str> = diff
                    .path
                    .strip_prefix('/')
                    .unwrap_or(&diff.path)
                    .split('/')
                    .collect();
                replace_at_segments(json, &segments, new_value);
            }
            DiffOp::Add => {
                let new_value = diff.value.as_ref().expect("add diff missing 'value'");
                add_at(json, &diff.path, new_value.clone());
            }
            DiffOp::Any => {}
            DiffOp::RemoveMatching => {
                let criteria = diff
                    .match_criteria
                    .as_ref()
                    .expect("remove_matching diff missing 'match'");
                let arr = resolve_array_at(json, &diff.path)
                    .expect("remove_matching diff path is not an array");
                arr.retain(|elem| !matches_criteria(elem, criteria));
            }
        }
    }
}

fn remove_at(json: &mut serde_json::Value, path: &str) {
    let segments: Vec<&str> = path.strip_prefix('/').unwrap_or(path).split('/').collect();
    remove_at_segments(json, &segments);
}

fn remove_at_segments(json: &mut serde_json::Value, segments: &[&str]) {
    let (head, tail) = match segments {
        [] => return,
        [h, rest @ ..] => (*h, rest),
    };
    if tail.is_empty() {
        match json {
            serde_json::Value::Object(map) => {
                map.remove(head);
            }
            serde_json::Value::Array(arr) => {
                if let Ok(idx) = head.parse::<usize>() {
                    if idx < arr.len() {
                        arr.remove(idx);
                    }
                }
            }
            _ => {}
        }
    } else if head == "*" {
        if let serde_json::Value::Array(arr) = json {
            for elem in arr.iter_mut() {
                remove_at_segments(elem, tail);
            }
        }
    } else {
        let child = match json {
            serde_json::Value::Object(map) => map.get_mut(head),
            serde_json::Value::Array(arr) => {
                head.parse::<usize>().ok().and_then(|i| arr.get_mut(i))
            }
            _ => None,
        };
        if let Some(child) = child {
            remove_at_segments(child, tail);
        }
    }
}

fn replace_at_segments(json: &mut serde_json::Value, segments: &[&str], value: &serde_json::Value) {
    let (head, tail) = match segments {
        [] => return,
        [h, rest @ ..] => (*h, rest),
    };
    if tail.is_empty() {
        match json {
            serde_json::Value::Object(map) => {
                if map.contains_key(head) {
                    map.insert(head.to_string(), value.clone());
                }
            }
            serde_json::Value::Array(arr) => {
                if let Ok(idx) = head.parse::<usize>() {
                    if idx < arr.len() {
                        arr[idx] = value.clone();
                    }
                }
            }
            _ => {}
        }
    } else if head == "*" {
        if let serde_json::Value::Array(arr) = json {
            for elem in arr.iter_mut() {
                replace_at_segments(elem, tail, value);
            }
        }
    } else {
        let child = match json {
            serde_json::Value::Object(map) => map.get_mut(head),
            serde_json::Value::Array(arr) => {
                head.parse::<usize>().ok().and_then(|i| arr.get_mut(i))
            }
            _ => None,
        };
        if let Some(child) = child {
            replace_at_segments(child, tail, value);
        }
    }
}

fn resolve_array_at<'a>(
    json: &'a mut serde_json::Value,
    path: &str,
) -> Option<&'a mut Vec<serde_json::Value>> {
    let val = if path.is_empty() {
        json
    } else {
        json.pointer_mut(path)?
    };
    val.as_array_mut()
}

fn matches_criteria(
    elem: &serde_json::Value,
    criteria: &serde_json::Map<String, serde_json::Value>,
) -> bool {
    let obj = match elem.as_object() {
        Some(o) => o,
        None => return false,
    };
    criteria
        .iter()
        .all(|(k, v)| obj.get(k).map_or(false, |actual| actual == v))
}

/// Strip diffs that should apply symmetrically to both sides:
/// - `Any` removes a JSON Pointer path from each.
/// - `RemoveMatching` removes elements matching `match` from arrays at `path`
///   in `actual` (the parallel removal on `expected` happens in `apply_diffs`),
///   making the diff a "neither side asserts these elements" hint.
fn strip_any_paths(
    expected: &mut serde_json::Value,
    actual: &mut serde_json::Value,
    diffs: &[ConversionDiff],
) {
    for diff in diffs {
        match diff.op {
            DiffOp::Any => {
                remove_at(expected, &diff.path);
                remove_at(actual, &diff.path);
            }
            DiffOp::RemoveMatching => {
                let criteria = diff
                    .match_criteria
                    .as_ref()
                    .expect("remove_matching diff missing 'match'");
                if let Some(arr) = resolve_array_at(actual, &diff.path) {
                    arr.retain(|elem| !matches_criteria(elem, criteria));
                }
            }
            _ => {}
        }
    }
}

pub fn run_round_trip_case<S, O>(
    case: &str,
    fixture_path: &Path,
    forward_diffs: &[ConversionDiff],
    reverse_diffs: &[ConversionDiff],
    label: &str,
) where
    S: DeserializeOwned + IntoOpenResponses<Target = O> + FromOpenResponses<Source = O> + Serialize,
    O: Serialize + DeserializeOwned,
{
    let original_json: serde_json::Value = load_fixture(fixture_path, case);
    let input: S = serde_json::from_value(original_json.clone())
        .unwrap_or_else(|e| panic!("{case} failed to deserialize fixture: {e}"));

    let or_result = input
        .into_open_responses(None)
        .unwrap_or_else(|e| panic!("{case} forward conversion failed: {e}"));

    let or_json = serde_json::to_value(&or_result.value)
        .unwrap_or_else(|e| panic!("{case} failed to serialize OR value: {e}"));
    let or_value: O = serde_json::from_value(or_json)
        .unwrap_or_else(|e| panic!("{case} failed to deserialize OR value: {e}"));

    let back_result = S::from_open_responses(or_value, None)
        .unwrap_or_else(|e| panic!("{case} reverse conversion failed: {e}"));

    let actual = serde_json::to_value(&back_result.value)
        .unwrap_or_else(|e| panic!("{case} failed to serialize round-trip result: {e}"));

    let mut expected = original_json;
    apply_diffs(&mut expected, forward_diffs);
    apply_diffs(&mut expected, reverse_diffs);

    let mut actual = actual;
    strip_any_paths(&mut expected, &mut actual, forward_diffs);
    strip_any_paths(&mut expected, &mut actual, reverse_diffs);

    assert_json_eq(&actual, &expected, label);
}

fn normalize_citation_delta_order(events: &mut serde_json::Value) {
    let Some(events) = events.as_array_mut() else {
        return;
    };

    let mut normalized = Vec::with_capacity(events.len());
    let mut pending_citations: Vec<(Option<u64>, serde_json::Value)> = Vec::new();

    for event in std::mem::take(events) {
        if is_citations_delta(&event) {
            pending_citations.push((event.get("index").and_then(|v| v.as_u64()), event));
            continue;
        }

        if event.get("type").and_then(|v| v.as_str()) == Some("content_block_stop") {
            let stop_index = event.get("index").and_then(|v| v.as_u64());
            let mut i = 0;
            while i < pending_citations.len() {
                if pending_citations[i].0 == stop_index {
                    normalized.push(pending_citations.remove(i).1);
                } else {
                    i += 1;
                }
            }
        }

        normalized.push(event);
    }

    normalized.extend(pending_citations.into_iter().map(|(_, event)| event));
    *events = normalized;
}

fn is_citations_delta(event: &serde_json::Value) -> bool {
    event.get("type").and_then(|v| v.as_str()) == Some("content_block_delta")
        && event
            .get("delta")
            .and_then(|delta| delta.get("type"))
            .and_then(|v| v.as_str())
            == Some("citations_delta")
}

pub fn run_round_trip_stream_case<F, R>(
    case: &str,
    fixture_path: &Path,
    mut forward: F,
    mut reverse: R,
    forward_diffs: &[ConversionDiff],
    reverse_diffs: &[ConversionDiff],
    label: &str,
) where
    F: StreamTransform,
    R: StreamTransform<Input = F::Output>,
    F::Input: DeserializeOwned,
    R::Output: Serialize,
{
    let original_json: serde_json::Value = load_fixture(fixture_path, case);
    let events: Vec<F::Input> = serde_json::from_value(original_json.clone())
        .unwrap_or_else(|e| panic!("{case} failed to deserialize stream events: {e}"));

    let mut or_events = Vec::new();
    for (i, event) in events.into_iter().enumerate() {
        or_events.extend(forward.transform(event).unwrap_or_else(|e| {
            panic!("{case} forward stream transform failed at event #{i}: {e}")
        }));
    }
    or_events.extend(
        forward
            .flush()
            .unwrap_or_else(|e| panic!("{case} forward stream flush failed: {e}")),
    );

    let mut result_events = Vec::new();
    for (i, event) in or_events.into_iter().enumerate() {
        result_events.extend(reverse.transform(event).unwrap_or_else(|e| {
            panic!("{case} reverse stream transform failed at event #{i}: {e}")
        }));
    }
    result_events.extend(
        reverse
            .flush()
            .unwrap_or_else(|e| panic!("{case} reverse stream flush failed: {e}")),
    );

    let actual = serde_json::to_value(&result_events)
        .unwrap_or_else(|e| panic!("{case} failed to serialize round-trip stream result: {e}"));

    let mut expected = original_json;
    apply_diffs(&mut expected, forward_diffs);
    apply_diffs(&mut expected, reverse_diffs);

    let mut actual = actual;
    strip_any_paths(&mut expected, &mut actual, forward_diffs);
    strip_any_paths(&mut expected, &mut actual, reverse_diffs);
    normalize_citation_delta_order(&mut expected);
    normalize_citation_delta_order(&mut actual);

    assert_json_eq(&actual, &expected, label);
}

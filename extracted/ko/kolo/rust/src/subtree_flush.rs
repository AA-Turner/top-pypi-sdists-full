use super::super::utils;
use super::super::utils::SerializedFrame;
use hashbrown::{HashMap, HashSet};
use pyo3::prelude::*;
use pyo3::types::{PyBool, PyDict};

// NOTE: The Python (`python/src/kolo/subtree_flush.py`) and Rust
// (`python/rust/src/subtree_flush.rs`) subtree-flush trackers still implement
// the same state machine independently. Keep the shared contract in
// `python/tests/data/subtree_flush_tracker_contract.json` in sync with any
// heuristic changes so both runtimes stay aligned.

const ROOT_SUBTREE_NAME: &str = "<root>";

pub(super) const DEFAULT_FLUSH_SUBTREE_MB: usize = 500;
pub(super) const DEFAULT_FLUSH_SUBTREE_BYTES: usize = DEFAULT_FLUSH_SUBTREE_MB * 1024 * 1024;

/// Pick the flush-subtree threshold (in bytes) from the user config.
///
/// Reads `flush_subtree_mb` (integer or float megabytes, or `false` to
/// disable flushing — TOML has no null literal). Mirrors
/// `config.resolve_flush_subtree_bytes` on the Python side. Returns
/// `None` if flushing is explicitly disabled, or
/// `DEFAULT_FLUSH_SUBTREE_BYTES` if the key is unset.
pub(super) fn resolve_flush_subtree_bytes(
    config_dict: &Bound<'_, PyDict>,
) -> PyResult<Option<usize>> {
    let Some(val) = config_dict.get_item("flush_subtree_mb")? else {
        return Ok(Some(DEFAULT_FLUSH_SUBTREE_BYTES));
    };
    if val.is_none() {
        return Ok(None);
    }
    // Must check bool BEFORE extracting f64: Python bools are a subclass
    // of int, so `False.extract::<f64>()` would silently succeed as 0.0.
    if val.is_instance_of::<PyBool>() {
        let b: bool = val.extract()?;
        if b {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "flush_subtree_mb = true is not valid; use false to disable \
                 or a non-negative number to set the threshold",
            ));
        }
        return Ok(None);
    }
    let mb: f64 = val.extract().map_err(|_| {
        pyo3::exceptions::PyValueError::new_err(
            "flush_subtree_mb must be a non-negative number or false",
        )
    })?;
    if !mb.is_finite() || mb < 0.0 {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "flush_subtree_mb must be a non-negative number or false",
        ));
    }
    // Guard against overflow when casting f64 → usize. On 32-bit targets
    // (i686, win32) usize caps at 4 GB, so ~4095 MB is the upper bound.
    let bytes_f = mb * 1024.0 * 1024.0;
    if bytes_f > usize::MAX as f64 {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "flush_subtree_mb is too large for this platform",
        ));
    }
    Ok(Some(bytes_f as usize))
}

#[derive(Clone)]
pub(super) struct FlushCandidate {
    pub(super) start_index: usize,
    pub(super) end_index: usize,
    pub(super) resident_bytes: usize,
    pub(super) co_name: String,
    pub(super) segment_count: usize,
}

#[derive(Clone)]
pub(super) struct OpenSubtree {
    pub(super) start_index: usize,
    pub(super) start_bytes: usize,
    pub(super) co_name: String,
    pub(super) flush_candidate: Option<FlushCandidate>,
}

pub(super) type CandidateOwner = usize;

pub(super) fn extract_co_name(frames: &[SerializedFrame]) -> String {
    let mut fallback = None;

    for frame in frames {
        let frame_value = match rmpv::decode::read_value(&mut &frame[..]) {
            Ok(frame_value) => frame_value,
            Err(_) => continue,
        };
        let map = match frame_value {
            rmpv::Value::Map(map) => map,
            _ => continue,
        };

        let mut co_name = None;
        let mut is_frame = false;
        for (key, value) in &map {
            match (key, value) {
                (rmpv::Value::String(key), rmpv::Value::String(value))
                    if key.as_str() == Some("type") && value.as_str() == Some("frame") =>
                {
                    is_frame = true;
                }
                (rmpv::Value::String(key), rmpv::Value::String(value))
                    if key.as_str() == Some("co_name") =>
                {
                    co_name = value.as_str().map(|value| value.to_string());
                }
                _ => {}
            }
        }

        if is_frame && co_name.is_some() {
            return co_name.unwrap();
        }
        if fallback.is_none() {
            fallback = co_name;
        }
    }

    fallback.unwrap_or_else(|| "<unknown>".to_string())
}

pub(super) fn low_water_bytes(flush_subtree_bytes: Option<usize>) -> usize {
    flush_subtree_bytes.map_or(0, |bytes| bytes / 2)
}

/// Byte threshold at which subtree tracking arms. Below this, only cheap
/// byte counting runs. For the 500MB default this returns 436MB, so subtree
/// stack bookkeeping only runs for the last 64MB of data.
pub(super) fn tracking_start_bytes(flush_subtree_bytes: Option<usize>) -> usize {
    let Some(high_water_bytes) = flush_subtree_bytes else {
        return 0;
    };
    if high_water_bytes < 1024 * 1024 {
        return 0;
    }
    let window = usize::max(high_water_bytes / 8, 64 * 1024 * 1024);
    high_water_bytes.saturating_sub(window)
}

#[cfg(test)]
pub(super) fn should_track(
    flush_subtree_bytes: Option<usize>,
    current_bytes: usize,
    flush_tracking_armed: &mut HashSet<String>,
    thread_id: &str,
) -> bool {
    let Some(_) = flush_subtree_bytes else {
        return false;
    };
    if flush_tracking_armed.contains(thread_id) {
        return true;
    }
    if current_bytes < tracking_start_bytes(flush_subtree_bytes) {
        return false;
    }

    flush_tracking_armed.insert(thread_id.to_string());
    true
}

pub(super) fn record_closed_segment(
    subtree_stack: &mut HashMap<String, Vec<OpenSubtree>>,
    thread_id: &str,
    start_index: usize,
    end_index: usize,
    resident_bytes: usize,
    co_name: String,
) {
    if resident_bytes == 0 {
        return;
    }

    let parent = stack_for_thread(subtree_stack, thread_id)
        .last_mut()
        .expect("root sentinel missing");
    let candidate = extend_flush_candidate(
        parent.flush_candidate.take(),
        start_index,
        end_index,
        resident_bytes,
        co_name,
    );
    parent.flush_candidate = Some(candidate);
}

pub(super) fn push_open_subtree(
    subtree_stack: &mut HashMap<String, Vec<OpenSubtree>>,
    thread_id: &str,
    open_subtree: OpenSubtree,
) {
    stack_for_thread(subtree_stack, thread_id).push(open_subtree);
}

pub(super) fn pop_open_subtree(
    subtree_stack: &mut HashMap<String, Vec<OpenSubtree>>,
    thread_id: &str,
) -> Option<OpenSubtree> {
    let stack = subtree_stack.get_mut(thread_id)?;
    if stack.len() <= 1 {
        return None;
    }
    stack.pop()
}

pub(super) fn select_flush_candidate(
    subtree_stack: &[OpenSubtree],
) -> Option<(CandidateOwner, FlushCandidate)> {
    let mut selected: Option<(usize, FlushCandidate)> = None;
    for (depth, subtree) in subtree_stack.iter().enumerate() {
        let Some(candidate) = subtree.flush_candidate.as_ref() else {
            continue;
        };

        let should_replace = match &selected {
            None => true,
            Some((selected_depth, selected_candidate)) => {
                candidate.resident_bytes > selected_candidate.resident_bytes
                    || (candidate.resident_bytes == selected_candidate.resident_bytes
                        && depth < *selected_depth)
                    || (candidate.resident_bytes == selected_candidate.resident_bytes
                        && depth == *selected_depth
                        && candidate.start_index < selected_candidate.start_index)
            }
        };

        if should_replace {
            selected = Some((depth, candidate.clone()));
        }
    }

    selected
}

pub(super) fn clear_flush_candidate(
    owner: CandidateOwner,
    subtree_stack: &mut HashMap<String, Vec<OpenSubtree>>,
    thread_id: &str,
) {
    if let Some(stack) = subtree_stack.get_mut(thread_id) {
        if let Some(subtree) = stack.get_mut(owner) {
            subtree.flush_candidate = None;
        }
    }
}

pub(super) fn shift_flush_state_after_flush(
    subtree_stack: Option<&mut Vec<OpenSubtree>>,
    start_index: usize,
    end_index: usize,
    resident_delta: isize,
) {
    let frame_delta = 1isize - (end_index - start_index) as isize;

    let Some(subtree_stack) = subtree_stack else {
        return;
    };
    for subtree in subtree_stack.iter_mut() {
        if subtree.start_index >= end_index {
            apply_signed_delta(&mut subtree.start_index, frame_delta);
            apply_signed_delta(&mut subtree.start_bytes, resident_delta);
        }

        if let Some(candidate) = subtree.flush_candidate.as_mut() {
            if candidate.start_index >= end_index {
                apply_signed_delta(&mut candidate.start_index, frame_delta);
                apply_signed_delta(&mut candidate.end_index, frame_delta);
            }
        }
    }
}

pub(super) fn begin_flush(
    flush_subtree_bytes: Option<usize>,
    current_bytes: usize,
    flush_in_progress: &mut HashSet<String>,
    thread_id: &str,
) -> Option<usize> {
    let high_water_bytes = flush_subtree_bytes?;
    if current_bytes < high_water_bytes || flush_in_progress.contains(thread_id) {
        return None;
    }

    flush_in_progress.insert(thread_id.to_string());
    Some(low_water_bytes(flush_subtree_bytes))
}

pub(super) fn finish_flush(flush_in_progress: &mut HashSet<String>, thread_id: &str) {
    flush_in_progress.remove(thread_id);
}

pub(super) fn reset_tracking(
    subtree_stack: &mut HashMap<String, Vec<OpenSubtree>>,
    flush_in_progress: &mut HashSet<String>,
) {
    subtree_stack.clear();
    flush_in_progress.clear();
}

pub(super) fn build_subtree_flushed_placeholder(
    co_name: &str,
    subtrace_id: &str,
    flushed_bytes: usize,
    segment_count: usize,
    timestamp: f64,
) -> SerializedFrame {
    let mut placeholder_buf = Vec::new();
    let placeholder_frame_id = utils::frame_id();
    rmp::encode::write_map_len(&mut placeholder_buf, 7).expect("Writing to memory, not I/O");
    rmp::encode::write_str(&mut placeholder_buf, "type").expect("Writing to memory, not I/O");
    rmp::encode::write_str(&mut placeholder_buf, "subtree_flushed")
        .expect("Writing to memory, not I/O");
    rmp::encode::write_str(&mut placeholder_buf, "frame_id").expect("Writing to memory, not I/O");
    rmp::encode::write_str(&mut placeholder_buf, &placeholder_frame_id)
        .expect("Writing to memory, not I/O");
    rmp::encode::write_str(&mut placeholder_buf, "co_name").expect("Writing to memory, not I/O");
    rmp::encode::write_str(&mut placeholder_buf, co_name).expect("Writing to memory, not I/O");
    rmp::encode::write_str(&mut placeholder_buf, "flushed_trace_id")
        .expect("Writing to memory, not I/O");
    rmp::encode::write_str(&mut placeholder_buf, subtrace_id).expect("Writing to memory, not I/O");
    rmp::encode::write_str(&mut placeholder_buf, "flushed_bytes")
        .expect("Writing to memory, not I/O");
    rmp::encode::write_uint(&mut placeholder_buf, flushed_bytes as u64)
        .expect("Writing to memory, not I/O");
    rmp::encode::write_str(&mut placeholder_buf, "flushed_segment_count")
        .expect("Writing to memory, not I/O");
    rmp::encode::write_uint(&mut placeholder_buf, segment_count as u64)
        .expect("Writing to memory, not I/O");
    rmp::encode::write_str(&mut placeholder_buf, "timestamp").expect("Writing to memory, not I/O");
    rmp::encode::write_f64(&mut placeholder_buf, timestamp).expect("Writing to memory, not I/O");
    placeholder_buf
}

fn extend_flush_candidate(
    candidate: Option<FlushCandidate>,
    start_index: usize,
    end_index: usize,
    resident_bytes: usize,
    co_name: String,
) -> FlushCandidate {
    match candidate {
        Some(mut candidate) if candidate.end_index == start_index => {
            candidate.end_index = end_index;
            candidate.resident_bytes += resident_bytes;
            candidate.segment_count += 1;
            candidate
        }
        _ => FlushCandidate {
            start_index,
            end_index,
            resident_bytes,
            co_name,
            segment_count: 1,
        },
    }
}

fn stack_for_thread<'a>(
    subtree_stack: &'a mut HashMap<String, Vec<OpenSubtree>>,
    thread_id: &str,
) -> &'a mut Vec<OpenSubtree> {
    subtree_stack
        .entry(thread_id.to_string())
        .or_insert_with(|| vec![root_subtree()])
}

fn root_subtree() -> OpenSubtree {
    OpenSubtree {
        start_index: 0,
        start_bytes: 0,
        co_name: ROOT_SUBTREE_NAME.to_string(),
        flush_candidate: None,
    }
}

fn apply_signed_delta(value: &mut usize, delta: isize) {
    if delta >= 0 {
        *value += delta as usize;
    } else {
        *value = value.saturating_sub((-delta) as usize);
    }
}

#[cfg(test)]
mod tests {
    use super::{
        begin_flush, clear_flush_candidate, finish_flush, low_water_bytes, push_open_subtree,
        record_closed_segment, reset_tracking, select_flush_candidate,
        shift_flush_state_after_flush, should_track, tracking_start_bytes, OpenSubtree,
    };
    use hashbrown::{HashMap, HashSet};
    use serde_json::{json, Value};
    use std::collections::BTreeMap;
    use std::sync::OnceLock;

    fn contract() -> &'static Value {
        static CONTRACT: OnceLock<Value> = OnceLock::new();

        CONTRACT.get_or_init(|| {
            serde_json::from_str(include_str!(
                "../../tests/data/subtree_flush_tracker_contract.json"
            ))
            .expect("subtree flush contract should be valid JSON")
        })
    }

    fn contract_cases(section: &str) -> &'static [Value] {
        contract()
            .get(section)
            .and_then(Value::as_array)
            .map(Vec::as_slice)
            .expect("contract section should be an array")
    }

    fn case_name(case: &Value) -> &str {
        case.get("name")
            .and_then(Value::as_str)
            .expect("contract case should have a name")
    }

    fn required_field<'a>(value: &'a Value, key: &str) -> &'a Value {
        value
            .get(key)
            .unwrap_or_else(|| panic!("contract value missing `{key}`: {value:?}"))
    }

    fn optional_usize(value: &Value, key: &str) -> Option<usize> {
        match value.get(key) {
            None | Some(Value::Null) => None,
            Some(number) => Some(
                number
                    .as_u64()
                    .unwrap_or_else(|| panic!("`{key}` should be a positive integer"))
                    as usize,
            ),
        }
    }

    fn required_usize(value: &Value, key: &str) -> usize {
        optional_usize(value, key)
            .unwrap_or_else(|| panic!("`{key}` should not be null in {value:?}"))
    }

    fn required_isize(value: &Value, key: &str) -> isize {
        required_field(value, key)
            .as_i64()
            .unwrap_or_else(|| panic!("`{key}` should be an integer")) as isize
    }

    fn required_bool(value: &Value, key: &str) -> bool {
        required_field(value, key)
            .as_bool()
            .unwrap_or_else(|| panic!("`{key}` should be a bool"))
    }

    fn required_str<'a>(value: &'a Value, key: &str) -> &'a str {
        required_field(value, key)
            .as_str()
            .unwrap_or_else(|| panic!("`{key}` should be a string"))
    }

    fn flush_candidate_state(candidate: &super::FlushCandidate) -> Value {
        json!({
            "start_index": candidate.start_index,
            "end_index": candidate.end_index,
            "resident_bytes": candidate.resident_bytes,
            "co_name": candidate.co_name,
            "segment_count": candidate.segment_count,
        })
    }

    fn open_subtree_state(subtree: &OpenSubtree) -> Value {
        json!({
            "start_index": subtree.start_index,
            "start_bytes": subtree.start_bytes,
            "co_name": subtree.co_name,
            "flush_candidate": subtree
                .flush_candidate
                .as_ref()
                .map(flush_candidate_state)
                .unwrap_or(Value::Null),
        })
    }

    fn tracker_state(
        subtree_stack: &HashMap<String, Vec<OpenSubtree>>,
        flush_in_progress: &HashSet<String>,
    ) -> Value {
        let subtree_stack = subtree_stack
            .iter()
            .map(|(thread_id, stack)| {
                (
                    thread_id.clone(),
                    Value::Array(stack.iter().map(open_subtree_state).collect()),
                )
            })
            .collect::<BTreeMap<_, _>>();

        let mut flush_in_progress = flush_in_progress.iter().cloned().collect::<Vec<_>>();
        flush_in_progress.sort();

        json!({
            "subtree_stack": subtree_stack,
            "flush_in_progress": flush_in_progress,
        })
    }

    fn selected_candidate_state(
        subtree_stack: &HashMap<String, Vec<OpenSubtree>>,
        thread_id: &str,
    ) -> Value {
        let Some(stack) = subtree_stack.get(thread_id) else {
            return Value::Null;
        };
        let Some((owner_depth, candidate)) = select_flush_candidate(stack) else {
            return Value::Null;
        };

        json!({
            "owner_depth": owner_depth,
            "candidate": flush_candidate_state(&candidate),
        })
    }

    fn clear_contract_flush_candidate(
        case: &Value,
        operation: &Value,
        subtree_stack: &mut HashMap<String, Vec<OpenSubtree>>,
    ) {
        let thread_id = required_str(operation, "thread_id");
        let owner_depth = required_usize(operation, "owner_depth");
        let stack_len = subtree_stack
            .get(thread_id)
            .unwrap_or_else(|| {
                panic!(
                    "contract case `{}` clear_flush_candidate references missing thread `{}`",
                    case_name(case),
                    thread_id,
                )
            })
            .len();
        assert!(
            owner_depth < stack_len,
            "contract case `{}` clear_flush_candidate owner_depth {} out of range for thread `{}`",
            case_name(case),
            owner_depth,
            thread_id,
        );

        clear_flush_candidate(owner_depth, subtree_stack, thread_id);
    }

    fn run_tracker_case(case: &Value) {
        let flush_subtree_bytes = optional_usize(case, "flush_subtree_bytes");
        let mut subtree_stack: HashMap<String, Vec<OpenSubtree>> = HashMap::new();
        let mut current_bytes: HashMap<String, usize> = HashMap::new();
        let mut flush_in_progress = HashSet::new();

        for operation in required_field(case, "operations")
            .as_array()
            .expect("operations should be an array")
        {
            let op = required_str(operation, "op");
            match op {
                "record_closed_segment" => record_closed_segment(
                    &mut subtree_stack,
                    required_str(operation, "thread_id"),
                    required_usize(operation, "start_index"),
                    required_usize(operation, "end_index"),
                    required_usize(operation, "resident_bytes"),
                    required_str(operation, "co_name").to_string(),
                ),
                "push_open_subtree" => push_open_subtree(
                    &mut subtree_stack,
                    required_str(operation, "thread_id"),
                    OpenSubtree {
                        start_index: required_usize(operation, "start_index"),
                        start_bytes: required_usize(operation, "start_bytes"),
                        co_name: required_str(operation, "co_name").to_string(),
                        flush_candidate: None,
                    },
                ),
                "clear_flush_candidate" => {
                    clear_contract_flush_candidate(case, operation, &mut subtree_stack)
                }
                "shift_flush_state_after_flush" => shift_flush_state_after_flush(
                    subtree_stack.get_mut(required_str(operation, "thread_id")),
                    required_usize(operation, "start_index"),
                    required_usize(operation, "end_index"),
                    required_isize(operation, "resident_delta"),
                ),
                "set_current_bytes" => {
                    current_bytes.insert(
                        required_str(operation, "thread_id").to_string(),
                        required_usize(operation, "value"),
                    );
                }
                "begin_flush" => {
                    let thread_id = required_str(operation, "thread_id");
                    let actual = begin_flush(
                        flush_subtree_bytes,
                        current_bytes.get(thread_id).copied().unwrap_or(0),
                        &mut flush_in_progress,
                        thread_id,
                    )
                    .is_some();
                    assert_eq!(
                        actual,
                        required_bool(operation, "expected"),
                        "contract case `{}` begin_flush mismatch",
                        case_name(case),
                    );
                }
                "finish_flush" => {
                    finish_flush(&mut flush_in_progress, required_str(operation, "thread_id"));
                }
                "reset" => {
                    reset_tracking(&mut subtree_stack, &mut flush_in_progress);
                    current_bytes.clear();
                }
                "select_flush_candidate" => {
                    assert_eq!(
                        selected_candidate_state(
                            &subtree_stack,
                            required_str(operation, "thread_id")
                        ),
                        required_field(operation, "expected").clone(),
                        "contract case `{}` select_flush_candidate mismatch",
                        case_name(case),
                    );
                }
                _ => panic!("unknown subtree flush contract op `{op}`"),
            }
        }

        if let Some(expected_state) = case.get("expected_state") {
            assert_eq!(
                tracker_state(&subtree_stack, &flush_in_progress),
                expected_state.clone(),
                "contract case `{}` state mismatch",
                case_name(case),
            );
        }
    }

    #[test]
    fn subtree_flush_threshold_contract() {
        for case in contract_cases("threshold_cases") {
            let flush_subtree_bytes = optional_usize(case, "flush_subtree_bytes");
            let mut armed = HashSet::new();

            assert_eq!(
                low_water_bytes(flush_subtree_bytes),
                required_usize(case, "expected_low_water_bytes"),
                "contract case `{}` low_water_bytes mismatch",
                case_name(case),
            );
            assert_eq!(
                tracking_start_bytes(flush_subtree_bytes),
                required_usize(case, "expected_tracking_start_bytes"),
                "contract case `{}` tracking_start_bytes mismatch",
                case_name(case),
            );

            for step in required_field(case, "should_track_steps")
                .as_array()
                .expect("should_track_steps should be an array")
            {
                assert_eq!(
                    should_track(
                        flush_subtree_bytes,
                        required_usize(step, "current_bytes"),
                        &mut armed,
                        required_str(step, "thread_id"),
                    ),
                    required_bool(step, "expected"),
                    "contract case `{}` should_track mismatch",
                    case_name(case),
                );
            }
        }
    }

    #[test]
    fn subtree_flush_tracker_contract() {
        for case in contract_cases("tracker_cases") {
            run_tracker_case(case);
        }
    }

    #[test]
    #[should_panic(expected = "clear_flush_candidate references missing thread `thread`")]
    fn subtree_flush_tracker_contract_rejects_clear_for_missing_thread() {
        run_tracker_case(&json!({
            "name": "missing_thread",
            "flush_subtree_bytes": 1024,
            "operations": [
                {
                    "op": "clear_flush_candidate",
                    "thread_id": "thread",
                    "owner_depth": 0
                }
            ]
        }));
    }

    #[test]
    #[should_panic(
        expected = "clear_flush_candidate owner_depth 2 out of range for thread `thread`"
    )]
    fn subtree_flush_tracker_contract_rejects_clear_for_invalid_owner_depth() {
        run_tracker_case(&json!({
            "name": "invalid_owner_depth",
            "flush_subtree_bytes": 1024,
            "operations": [
                {
                    "op": "record_closed_segment",
                    "thread_id": "thread",
                    "start_index": 5,
                    "end_index": 6,
                    "resident_bytes": 100,
                    "co_name": "child"
                },
                {
                    "op": "clear_flush_candidate",
                    "thread_id": "thread",
                    "owner_depth": 2
                }
            ]
        }));
    }

    #[test]
    #[should_panic(expected = "unknown subtree flush contract op `explode`")]
    fn subtree_flush_tracker_contract_rejects_unknown_op() {
        run_tracker_case(&json!({
            "name": "unknown_op",
            "flush_subtree_bytes": 1024,
            "operations": [{"op": "explode"}]
        }));
    }

    #[test]
    fn tracking_starts_immediately_for_small_thresholds() {
        let mut armed = HashSet::new();

        assert!(should_track(Some(1024), 1, &mut armed, "thread"));
    }

    #[test]
    fn tracking_waits_until_start_threshold() {
        let mut armed = HashSet::new();
        let threshold = Some(500 * 1024 * 1024);
        let start = tracking_start_bytes(threshold);

        // 500MB - max(500MB/8, 64MB) = 500MB - 64MB = 436MB
        assert_eq!(start, 500 * 1024 * 1024 - 64 * 1024 * 1024);
        assert!(!should_track(threshold, start - 1, &mut armed, "thread"));
        assert!(should_track(threshold, start, &mut armed, "thread"));
        // Once armed, even small values return true
        assert!(should_track(threshold, 1, &mut armed, "thread"));
    }
}

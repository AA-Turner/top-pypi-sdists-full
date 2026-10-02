//! Port of `software.amazon.kinesis.metrics.OtelMetricNameTransformer`.
//!
//! Transforms KCL metric names into OTel-compliant instrument names via a
//! documented multi-step pipeline (special-case map, character substitution,
//! camelCase splitting, lowercasing, namespacing, and BNF validation).

use std::collections::HashMap;
use std::sync::OnceLock;

use aws_sdk_cloudwatch::types::StandardUnit;

/// OTel namespace prefix prepended to every transformed name.
const NAMESPACE_PREFIX: &str = "aws.kinesis.client.";

/// The special-case rename map (`SPECIAL_CASE_MAP`), copied verbatim from Java.
///
/// If a KCL name is a key here, steps 2–5 of the pipeline are skipped and the
/// mapped value goes straight to lowercase + prefix.
fn special_case_map() -> &'static HashMap<&'static str, &'static str> {
    static MAP: OnceLock<HashMap<&'static str, &'static str>> = OnceLock::new();
    MAP.get_or_init(|| {
        let mut map = HashMap::new();
        map.insert("MillisBehindLatest", "consumer.lag.duration");
        map.insert("DataBytesProcessed", "records.size");
        map.insert("ActiveStreams.Count", "streams.active");
        map.insert("StreamsPendingDeletion.Count", "streams.pending_deletion");
        map.insert(
            "NonExistingStreamDelete.Count",
            "streams.deleted_nonexistent",
        );
        map.insert("DeletedStreams.Count", "streams.deleted");
        map.insert("NumStreamsToSync", "streams.pending_sync");
        map.insert("QueueSize", "stream_id_cache.queue.size");
        map.insert("NumWorkers", "workers");
        map.insert("NumWorkersWithInvalidEntry", "workers.invalid_entry");
        map.insert(
            "NumWorkersWithFailingWorkerMetric",
            "workers.failing_worker_metric",
        );
        map
    })
}

/// A character that is legal in an OTel instrument name body: `[A-Za-z0-9_.\-/]`.
fn is_legal_char(c: char) -> bool {
    c.is_ascii_alphanumeric() || matches!(c, '_' | '.' | '-' | '/')
}

/// OTel instrument name BNF: `[A-Za-z][A-Za-z0-9_.\-/]{0,254}`.
fn is_valid_name(name: &str) -> bool {
    let mut chars = name.chars();
    match chars.next() {
        Some(first) if first.is_ascii_alphabetic() => {}
        _ => return false,
    }
    let mut rest_len = 0usize;
    for c in chars {
        if !is_legal_char(c) {
            return false;
        }
        rest_len += 1;
    }
    rest_len <= 254
}

/// Replaces every character that is illegal in an OTel instrument name
/// (`[^A-Za-z0-9_.\-/]`) with `_`.
fn sanitize_illegal_chars(name: &str) -> String {
    name.chars()
        .map(|c| if is_legal_char(c) { c } else { '_' })
        .collect()
}

/// Transforms a KCL metric name to an OTel-compliant instrument name.
///
/// Mirrors Java `OtelMetricNameTransformer.transformName(String)`.
pub fn transform_name(kcl_name: &str) -> String {
    // Step 1: Special-case rename map
    let name: String = if let Some(special_case) = special_case_map().get(kcl_name) {
        // Skip steps 2-5, go straight to step 6 (lowercase) and step 7 (prefix)
        (*special_case).to_string()
    } else {
        let mut name = kcl_name.to_string();

        // Step 2: Substitute ':' with '.'
        name = name.replace(':', ".");

        // Step 3: Replace trailing '.Time' with '.duration'
        if let Some(stripped) = name.strip_suffix(".Time") {
            name = format!("{}.duration", stripped);
        }

        // Step 4: Strip trailing '.Count'
        if let Some(stripped) = name.strip_suffix(".Count") {
            name = stripped.to_string();
        }

        // Step 5: Split PascalCase/camelCase within each dot-separated segment
        name = split_camel_case(&name);

        // Step 6: Lowercase
        name.to_lowercase()
    };

    // Step 7: Prepend namespace prefix
    let name = format!("{}{}", NAMESPACE_PREFIX, name);

    // Step 8: Validate
    validate(name)
}

/// Transforms a KCL metric name to an OTel-compliant instrument name.
///
/// Mirrors Java `transformName(String, StandardUnit)`. Currently delegates to
/// [`transform_name`]; the `unit` parameter is reserved for future use.
pub fn transform_name_with_unit(kcl_name: &str, _unit: Option<StandardUnit>) -> String {
    transform_name(kcl_name)
}

/// Splits PascalCase/camelCase within each dot-separated segment by inserting
/// underscores. Runs of consecutive uppercase letters are treated as a single
/// word (e.g. `"GSIReadyStatus"` → `"GSI_Ready_Status"`).
///
/// Mirrors Java `splitCamelCase`: `input.split("\\.", -1)` keeps trailing empty
/// segments — Rust's `str::split('.')` has the same semantics (empty leading /
/// trailing / adjacent segments are preserved).
fn split_camel_case(input: &str) -> String {
    let mut result = String::new();
    for (i, segment) in input.split('.').enumerate() {
        if i > 0 {
            result.push('.');
        }
        result.push_str(&split_segment(segment));
    }
    result
}

/// Splits a single segment (no dots) at camelCase boundaries.
///
/// Mirrors Java `splitSegment`. Operates on `char`s; KCL metric names are ASCII
/// in practice, so this matches the Java UTF-16 `char[]` iteration.
// The two `sb.push('_')` branches below are intentionally kept separate: each
// documents a distinct camelCase boundary (lowercase/digit -> uppercase vs. the
// last uppercase of a run before a lowercase), mirroring Java `splitSegment`.
// Collapsing them into one condition would lose that distinction.
#[allow(clippy::if_same_then_else)]
fn split_segment(segment: &str) -> String {
    if segment.is_empty() {
        return segment.to_string();
    }
    let chars: Vec<char> = segment.chars().collect();
    let mut sb = String::new();
    for i in 0..chars.len() {
        if i > 0 && chars[i].is_uppercase() {
            // Insert '_' at lowercase→uppercase or digit→uppercase transition
            if chars[i - 1].is_lowercase() || chars[i - 1].is_ascii_digit() {
                sb.push('_');
            }
            // Insert '_' before the last uppercase in a run followed by lowercase
            // (e.g. "GSIReady" → "GSI_Ready").
            else if chars[i - 1].is_uppercase()
                && i + 1 < chars.len()
                && chars[i + 1].is_lowercase()
            {
                sb.push('_');
            }
        }
        sb.push(chars[i]);
    }
    sb
}

/// Validates the name against OTel BNF and the 255-char limit, sanitizing
/// illegal characters if necessary.
///
/// Mirrors Java `validate`.
fn validate(mut name: String) -> String {
    if name.chars().count() > 255 {
        tracing::warn!(
            "OTel metric name exceeds 255 characters, truncating: {}",
            name
        );
        name = truncate_chars(&name, 255);
    }
    if !is_valid_name(&name) {
        let original = name.clone();
        name = sanitize_illegal_chars(&name);
        // Ensure it starts with a letter
        if name.is_empty() || !name.chars().next().unwrap().is_alphabetic() {
            name = format!("m{}", name);
        }
        if name.chars().count() > 255 {
            name = truncate_chars(&name, 255);
        }
        tracing::warn!(
            "OTel metric name contained illegal characters, sanitized '{}' to '{}'",
            original,
            name
        );
    }
    name
}

/// Truncates a string to at most `max` chars (mirrors Java `substring(0, 255)`
/// which counts UTF-16 code units — for ASCII names this is equivalent).
fn truncate_chars(s: &str, max: usize) -> String {
    s.chars().take(max).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    const PREFIX: &str = "aws.kinesis.client.";

    // -----------------------------------------------------------------------
    // Step 1: Special-case map — all 11 entries
    // -----------------------------------------------------------------------

    #[test]
    fn test_special_case_millis_behind_latest() {
        assert_eq!(
            format!("{}consumer.lag.duration", PREFIX),
            transform_name("MillisBehindLatest")
        );
    }

    #[test]
    fn test_special_case_data_bytes_processed() {
        assert_eq!(
            format!("{}records.size", PREFIX),
            transform_name("DataBytesProcessed")
        );
    }

    #[test]
    fn test_special_case_active_streams_count() {
        assert_eq!(
            format!("{}streams.active", PREFIX),
            transform_name("ActiveStreams.Count")
        );
    }

    #[test]
    fn test_special_case_streams_pending_deletion_count() {
        assert_eq!(
            format!("{}streams.pending_deletion", PREFIX),
            transform_name("StreamsPendingDeletion.Count")
        );
    }

    #[test]
    fn test_special_case_non_existing_stream_delete_count() {
        assert_eq!(
            format!("{}streams.deleted_nonexistent", PREFIX),
            transform_name("NonExistingStreamDelete.Count")
        );
    }

    #[test]
    fn test_special_case_deleted_streams_count() {
        assert_eq!(
            format!("{}streams.deleted", PREFIX),
            transform_name("DeletedStreams.Count")
        );
    }

    #[test]
    fn test_special_case_num_streams_to_sync() {
        assert_eq!(
            format!("{}streams.pending_sync", PREFIX),
            transform_name("NumStreamsToSync")
        );
    }

    #[test]
    fn test_special_case_queue_size() {
        assert_eq!(
            format!("{}stream_id_cache.queue.size", PREFIX),
            transform_name("QueueSize")
        );
    }

    #[test]
    fn test_special_case_num_workers() {
        assert_eq!(format!("{}workers", PREFIX), transform_name("NumWorkers"));
    }

    #[test]
    fn test_special_case_num_workers_with_invalid_entry() {
        assert_eq!(
            format!("{}workers.invalid_entry", PREFIX),
            transform_name("NumWorkersWithInvalidEntry")
        );
    }

    #[test]
    fn test_special_case_num_workers_with_failing_worker_metric() {
        assert_eq!(
            format!("{}workers.failing_worker_metric", PREFIX),
            transform_name("NumWorkersWithFailingWorkerMetric")
        );
    }

    // -----------------------------------------------------------------------
    // Step 2: Colon substitution — ':' replaced with '.'
    // -----------------------------------------------------------------------

    #[test]
    fn test_colon_substitution() {
        assert_eq!(
            format!("{}get_lease.error", PREFIX),
            transform_name("GetLease:Error")
        );
    }

    #[test]
    fn test_colon_substitution_multiple_colons() {
        assert_eq!(
            format!("{}foo.bar.baz", PREFIX),
            transform_name("Foo:Bar:Baz")
        );
    }

    // -----------------------------------------------------------------------
    // Step 3: Trailing .Time → .duration
    // -----------------------------------------------------------------------

    #[test]
    fn test_trailing_time_renew_lease_time() {
        assert_eq!(
            format!("{}renew_lease.duration", PREFIX),
            transform_name("RenewLease.Time")
        );
    }

    #[test]
    fn test_trailing_time_record_processor_process_records_time() {
        assert_eq!(
            format!("{}record_processor.process_records.duration", PREFIX),
            transform_name("RecordProcessor.processRecords.Time")
        );
    }

    #[test]
    fn test_trailing_time_colon_then_time() {
        // "SomeOp:Time" → colon becomes dot → "SomeOp.Time" → trailing .Time → "SomeOp.duration"
        assert_eq!(
            format!("{}some_op.duration", PREFIX),
            transform_name("SomeOp:Time")
        );
    }

    #[test]
    fn test_time_not_trailing_is_not_replaced() {
        // "TimeSpent" does not end with ".Time", so no replacement
        assert_eq!(format!("{}time_spent", PREFIX), transform_name("TimeSpent"));
    }

    // -----------------------------------------------------------------------
    // Step 4: Strip trailing .Count (non-special-case)
    // -----------------------------------------------------------------------

    #[test]
    fn test_strip_trailing_count() {
        // "SomeMetric.Count" is not in the special-case map, so .Count is stripped
        assert_eq!(
            format!("{}some_metric", PREFIX),
            transform_name("SomeMetric.Count")
        );
    }

    #[test]
    fn test_count_not_trailing_is_not_stripped() {
        // "CountOfItems" does not end with ".Count"
        assert_eq!(
            format!("{}count_of_items", PREFIX),
            transform_name("CountOfItems")
        );
    }

    // -----------------------------------------------------------------------
    // Step 5: PascalCase splitting
    // -----------------------------------------------------------------------

    #[test]
    fn test_pascal_case_splitting_records_processed() {
        assert_eq!(
            format!("{}records_processed", PREFIX),
            transform_name("RecordsProcessed")
        );
    }

    #[test]
    fn test_pascal_case_splitting_lease_spillover() {
        assert_eq!(
            format!("{}lease_spillover", PREFIX),
            transform_name("LeaseSpillover")
        );
    }

    #[test]
    fn test_pascal_case_splitting_single_word() {
        assert_eq!(format!("{}success", PREFIX), transform_name("Success"));
    }

    #[test]
    fn test_pascal_case_splitting_camel_case() {
        assert_eq!(
            format!("{}process_records", PREFIX),
            transform_name("processRecords")
        );
    }

    #[test]
    fn test_pascal_case_splitting_with_dot_separated_segments() {
        // Each segment is split independently
        assert_eq!(
            format!("{}record_processor.process_records", PREFIX),
            transform_name("RecordProcessor.processRecords")
        );
    }

    // -----------------------------------------------------------------------
    // Step 5 (continued): Uppercase runs — consecutive uppercase treated as one word
    // -----------------------------------------------------------------------

    #[test]
    fn test_uppercase_runs_gsi_ready_status() {
        // "GSIReadyStatus" → "GSI_Ready_Status" → lowercase → "gsi_ready_status"
        assert_eq!(
            format!("{}gsi_ready_status", PREFIX),
            transform_name("GSIReadyStatus")
        );
    }

    #[test]
    fn test_uppercase_runs_ddb_table_name() {
        // "DDBTableName" → "DDB_Table_Name" → lowercase → "ddb_table_name"
        assert_eq!(
            format!("{}ddb_table_name", PREFIX),
            transform_name("DDBTableName")
        );
    }

    #[test]
    fn test_uppercase_runs_all_uppercase() {
        // "ABC" → no transitions → "ABC" → lowercase → "abc"
        assert_eq!(format!("{}abc", PREFIX), transform_name("ABC"));
    }

    // -----------------------------------------------------------------------
    // Step 7: Namespace prefix — all results start with "aws.kinesis.client."
    // -----------------------------------------------------------------------

    #[test]
    fn test_namespace_prefix_always_present() {
        assert!(transform_name("AnyMetric").starts_with(PREFIX));
    }

    #[test]
    fn test_namespace_prefix_special_case_also_has_prefix() {
        assert!(transform_name("NumWorkers").starts_with(PREFIX));
    }

    // -----------------------------------------------------------------------
    // Step 8: Simple names
    // -----------------------------------------------------------------------

    #[test]
    fn test_simple_name_success() {
        assert_eq!(format!("{}success", PREFIX), transform_name("Success"));
    }

    #[test]
    fn test_simple_name_time() {
        // "Time" does not end with ".Time" (no dot), so it goes through PascalCase
        // splitting which produces "Time" → lowercase → "time"
        assert_eq!(format!("{}time", PREFIX), transform_name("Time"));
    }

    // -----------------------------------------------------------------------
    // transformName with unit overload — delegates correctly
    // -----------------------------------------------------------------------

    #[test]
    fn test_transform_name_with_unit_delegates_to_single_arg() {
        let without_unit = transform_name("RecordsProcessed");
        let with_unit = transform_name_with_unit("RecordsProcessed", Some(StandardUnit::Count));
        assert_eq!(without_unit, with_unit);
    }

    #[test]
    fn test_transform_name_with_unit_null_unit() {
        let without_unit = transform_name("LeaseSpillover");
        let with_unit = transform_name_with_unit("LeaseSpillover", None);
        assert_eq!(without_unit, with_unit);
    }

    #[test]
    fn test_transform_name_with_unit_special_case() {
        let without_unit = transform_name("MillisBehindLatest");
        let with_unit =
            transform_name_with_unit("MillisBehindLatest", Some(StandardUnit::Milliseconds));
        assert_eq!(without_unit, with_unit);
    }

    #[test]
    fn test_transform_name_with_unit_various_units() {
        let name = "DataBytesProcessed";
        let expected = transform_name(name);
        assert_eq!(
            expected,
            transform_name_with_unit(name, Some(StandardUnit::Bytes))
        );
        assert_eq!(
            expected,
            transform_name_with_unit(name, Some(StandardUnit::None))
        );
        assert_eq!(
            expected,
            transform_name_with_unit(name, Some(StandardUnit::Milliseconds))
        );
    }

    // -----------------------------------------------------------------------
    // Edge cases and validation
    // -----------------------------------------------------------------------

    #[test]
    fn test_empty_segment_preserved() {
        // "Foo..Bar" has an empty segment between dots
        assert_eq!(format!("{}foo..bar", PREFIX), transform_name("Foo..Bar"));
    }

    #[test]
    fn test_single_character_name() {
        assert_eq!(format!("{}x", PREFIX), transform_name("X"));
    }

    #[test]
    fn test_already_lowercase() {
        assert_eq!(
            format!("{}already_lower", PREFIX),
            transform_name("alreadyLower")
        );
    }

    #[test]
    fn test_numeric_in_name() {
        // "Retry3Count" — numeric characters don't trigger splits
        // "Retry3" stays together, "Count" splits → "Retry3_Count" → lowercase
        assert_eq!(
            format!("{}retry3_count", PREFIX),
            transform_name("Retry3Count")
        );
    }
}

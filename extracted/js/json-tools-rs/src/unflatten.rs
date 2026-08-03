//! JSON unflattening engine using tape-based streaming.
//!
//! Reconstructs nested JSON structures from flat key-value maps using the same
//! tape scanner as flatten. Values remain as zero-copy byte ranges into the
//! original input via `ValueRef`, avoiding `serde_json::Value` allocation.
//!
//! Pipeline: `scan_and_fixup → extract entries → build UnflatNode tree → serialize directly`

use std::borrow::Cow;

use crate::flatten::IntBuf;
use crate::fxhash::{FxHashMap, FxIndexMap};
use compact_str::CompactString;
use memchr::{memchr, memmem};
use smallvec::SmallVec;

use crate::config::{FilteringConfig, ProcessingConfig, TypeConversionMode};
use crate::convert::convert_string_for_mode;
use crate::error::JsonToolsError;
use crate::flatten::{
    escape_json_string, scan_and_fixup, skip_tape_value, tape_content_str, tape_entry,
    tape_quoted_str, tape_scalar_bytes, unescape_json_string, write_json_escaped_key, EntryKind,
    TapeEntry, ValueRef,
};
use crate::json_parser;
use crate::transform::{apply_replacement_patterns, matches_any_pattern};

// ================================================================================================
// UnflatNode — Lightweight Tree with Zero-Copy Leaves
// ================================================================================================

/// Object node's map type: O(1) average lookup (like the old `FxHashMap`) *and* insertion
/// order preserved for iteration (so serialization needs no per-node sort). A hand-rolled
/// `Vec<(String, UnflatNode)>` was tried here first but has real O(n) lookup per key --
/// fine for typical narrow objects, but a JSON object used as a keyed map (e.g. many
/// `"user_<id>.field"` entries, each a distinct top-level key) turns that into O(n^2)
/// overall (empirically: 20K such entries went from a few ms to over a second).
///
/// Keys are `CompactString`, not `String`: real-world JSON keys are short (this
/// project's own benchmark corpus averages ~8.6 chars, max 22 -- comfortably within
/// `CompactString`'s 24-byte inline capacity), so nearly every key insertion here
/// avoids a heap allocation entirely. Validated with an isolated benchmark before
/// adopting (~3.4x faster than `String` for realistic insert+lookup key-map workloads).
type ObjectMap<'a> = FxIndexMap<CompactString, UnflatNode<'a>>;

/// Lightweight tree node for unflattened JSON. Leaf values stay as zero-copy
/// byte ranges from the original input via `ValueRef`.
enum UnflatNode<'a> {
    /// Leaf value — raw bytes from input or owned transformed value
    Leaf(ValueRef<'a>),
    /// Null placeholder for array gaps
    Null,
    /// Object node — see `ObjectMap`'s doc comment.
    Object(ObjectMap<'a>),
    /// Array with indexed elements
    Array(Vec<UnflatNode<'a>>),
}

/// Initial capacity for a freshly-created nested object/array during tree-building.
/// This project's own real-world benchmark corpus (benches/realworld_benchmarks.rs:
/// AWS CloudTrail, GitHub API, Kubernetes, Elasticsearch, Stripe, Twitter) has a
/// measured nested-object fanout of median 3, mean 4.1, p75 5 -- 6 covers the p75
/// case without a reallocation, at a bounded, modest memory cost for smaller objects
/// (this is a capacity *hint*: one allocation happens either way, this only changes
/// its size). Found via `sample` profiling: the previous value of 4 caused a
/// measurable share of total runtime in `IndexMap::insert_full` -> `finish_grow` ->
/// `realloc` for any real-world object with more than 4 fields.
const NESTED_CONTAINER_CAPACITY_HINT: usize = 6;

// ================================================================================================
// Core Entry Point
// ================================================================================================

/// Core unflattening logic for a single JSON string.
/// Entry point called by `builder.rs`.
#[inline]
pub(crate) fn process_single_json_for_unflatten(
    json: &str,
    config: &ProcessingConfig,
) -> Result<String, JsonToolsError> {
    let input = json.as_bytes();

    // Reject inputs exceeding u32 addressable range (4 GiB)
    if input.len() > u32::MAX as usize {
        return Err(JsonToolsError::input_validation_error(
            "Input exceeds 4 GiB limit",
        ));
    }

    // Skip leading whitespace
    let start = skip_whitespace(input, 0);
    if start >= input.len() {
        return Ok("{}".to_string());
    }

    let first = unsafe { *input.get_unchecked(start) };

    // Handle root-level primitives (not objects or arrays)
    if first != b'{' && first != b'[' {
        let value = json_parser::parse_json(json)?;
        if let serde_json::Value::String(s) = value {
            let has_value_replacements = !config.replacements.value_replacements.is_empty();
            let type_conversion_mode = config.type_conversion_mode;
            let auto_convert = type_conversion_mode != TypeConversionMode::Disabled;

            // Value replacement
            if has_value_replacements {
                if let Some(replaced) =
                    apply_replacement_patterns(&s, &config.replacements.value_replacements)
                {
                    // Also try type-converting the replaced value, so a replacement
                    // producing a recognized token (null/number/date/etc.) is still
                    // converted -- matches extract_value's composable order.
                    // remove_nulls stays a no-op here: there's no parent key to omit
                    // a root-level value under.
                    if auto_convert {
                        if let Some(converted) = convert_string_for_mode(
                            &replaced,
                            type_conversion_mode,
                            &config.type_conversion,
                        ) {
                            return Ok(converted.into_owned());
                        }
                    }
                    return json_parser::to_string(&serde_json::Value::String(replaced))
                        .map_err(JsonToolsError::serialization_error);
                }
            }

            // Type conversion (no replacement occurred)
            if auto_convert {
                if let Some(converted) =
                    convert_string_for_mode(&s, type_conversion_mode, &config.type_conversion)
                {
                    return Ok(converted.into_owned());
                }
            }

            return json_parser::to_string(&serde_json::Value::String(s))
                .map_err(JsonToolsError::serialization_error);
        }
        return json_parser::to_string(&value).map_err(JsonToolsError::serialization_error);
    }

    // Handle root arrays — not valid flattened JSON
    if first == b'[' {
        return Ok("{}".to_string());
    }

    // Handle empty object: {}
    let after_open = skip_whitespace(input, start + 1);
    if after_open < input.len() {
        let close = unsafe { *input.get_unchecked(after_open) };
        if close == b'}' {
            return Ok("{}".to_string());
        }
    }

    // Phase 1: Single-pass tape scan
    let tape = scan_and_fixup(input)?;

    // Phase 2: Extract flat entries with inline transforms
    let mut entries = extract_flat_entries(input, &tape, config)?;

    // Phase 3: Collision handling. `has_duplicate_keys` stays as a cheap
    // pre-check gating the common case: measured directly (interleaved
    // before/after, bench_quick), unconditionally calling
    // `handle_entry_collisions` instead -- reasoning that its own
    // no-collisions fast path made a separate pre-check redundant -- was a
    // ~2-4% *regression* for the dominant real-world case (no collision
    // handling configured, no actual duplicate keys): `handle_entry_collisions`
    // always builds a `FxHashMap<&str, SmallVec<[usize; 1]>>`, per-entry
    // costlier to populate than `has_duplicate_keys`'s plain
    // `FxHashMap<&str, ()>`, so paying for it unconditionally lost more in the
    // common case than it saved in the rare "duplicates present without
    // collision handling configured" case where the old code built both maps.
    // `handle_entry_collisions` itself still got fixed (see its doc comment)
    // to remove an unrelated, unconditionally-wasteful double lookup.
    if config.collision.has_collision_handling() || has_duplicate_keys(&entries) {
        entries = handle_entry_collisions(entries, config.collision.has_collision_handling());
    }

    // Phase 4: Build UnflatNode tree
    let tree = build_unflatten_tree(entries, &config.separator, config.max_array_index)?;

    // Phase 5: Serialize with integrated filtering. `input.len()` is a cheap, already-
    // available capacity hint: unflattening restructures the same keys/values into
    // nested form rather than adding or removing much content, so output size tracks
    // input size closely -- much better than the fixed small default this replaced,
    // without needing a separate full pass over the tree just to sum exact sizes.
    Ok(serialize_unflatten_tree(
        &tree,
        &config.filtering,
        &config.replacements.value_exclusions,
        input.len(),
    ))
}

// ================================================================================================
// Entry Extraction from Tape
// ================================================================================================

/// Walk the top-level tape object and extract key-value pairs with inline transforms.
fn extract_flat_entries<'a>(
    input: &'a [u8],
    tape: &[TapeEntry],
    config: &ProcessingConfig,
) -> Result<Vec<(CompactString, ValueRef<'a>)>, JsonToolsError> {
    if tape.is_empty() {
        return Ok(Vec::new());
    }

    // Root must be ObjectStart
    if tape[0].kind() != EntryKind::ObjectStart {
        return Err(JsonToolsError::invalid_json_structure(
            "Expected object for unflattening",
        ));
    }

    let end_idx = tape[0].aux() as usize;
    let mut entries = Vec::with_capacity(end_idx / 4); // heuristic
    let mut cursor = 1; // skip root ObjectStart

    while cursor < end_idx {
        let entry = tape_entry(tape, cursor);

        if entry.kind() != EntryKind::StringStart {
            cursor += 1;
            continue;
        }

        // Extract key
        let key_str = tape_content_str(input, entry);

        let mut key: CompactString = if entry.string_has_escapes() {
            CompactString::from(unescape_json_string(key_str).as_ref())
        } else {
            CompactString::from(key_str)
        };

        // Apply lowercase
        if config.lowercase_keys {
            key.make_ascii_lowercase();
        }

        // Apply key replacements
        if config.replacements.has_key_replacements() {
            if let Some(new_key) =
                apply_replacement_patterns(&key, &config.replacements.key_replacements)
            {
                key = CompactString::from(new_key);
            }
        }

        // Skip key + colon
        cursor += 1;
        if cursor < end_idx && tape[cursor].kind() == EntryKind::Colon {
            cursor += 1;
        }

        // Extract value
        if cursor >= end_idx {
            break;
        }

        // Key exclusion: drop this entry (and its value/subtree) entirely, without
        // extracting the value at all -- advance_past_value is O(1) via the tape's
        // precomputed container end-index.
        if config.replacements.has_key_exclusions()
            && matches_any_pattern(&key, &config.replacements.key_exclusions)
        {
            cursor = advance_past_value(tape, cursor);
            continue;
        }

        let val_entry = tape_entry(tape, cursor);
        let value = extract_value(input, tape, val_entry, config);
        cursor = advance_past_value(tape, cursor);

        entries.push((key, value));
    }

    Ok(entries)
}

/// Extract a ValueRef from a tape entry, applying value transforms inline.
#[inline]
fn extract_value<'a>(
    input: &'a [u8],
    tape: &[TapeEntry],
    entry: TapeEntry,
    config: &ProcessingConfig,
) -> ValueRef<'a> {
    match entry.kind() {
        EntryKind::StringStart => {
            let content_str = tape_content_str(input, entry);
            let has_value_replacements = config.replacements.has_value_replacements();
            let type_conversion_mode = config.type_conversion_mode;
            let auto_convert = type_conversion_mode != TypeConversionMode::Disabled;

            if has_value_replacements || auto_convert {
                let unescaped = if entry.string_has_escapes() {
                    unescape_json_string(content_str)
                } else {
                    Cow::Borrowed(content_str)
                };

                // Value replacement -- tried first, matching flatten.rs's and
                // normal mode's canonical order (unflatten previously tried type
                // conversion first, which was inconsistent with the other two
                // engines and could let a replacement's output bypass conversion,
                // and therefore remove_nulls, entirely).
                if has_value_replacements {
                    if let Some(replaced) = apply_replacement_patterns(
                        unescaped.as_ref(),
                        &config.replacements.value_replacements,
                    ) {
                        // Also try type-converting the replaced value, so a
                        // replacement producing a recognized token (null/number/
                        // date/etc.) is still converted.
                        if auto_convert {
                            if let Some(converted) = convert_string_for_mode(
                                &replaced,
                                type_conversion_mode,
                                &config.type_conversion,
                            ) {
                                return ValueRef::Owned(CompactString::from(converted));
                            }
                        }
                        let escaped = escape_json_string(&replaced);
                        let mut buf = CompactString::with_capacity(escaped.len() + 2);
                        buf.push('"');
                        buf.push_str(&escaped);
                        buf.push('"');
                        return ValueRef::Owned(buf);
                    }
                }

                // Type conversion (no replacement occurred)
                if auto_convert {
                    if let Some(converted) = convert_string_for_mode(
                        unescaped.as_ref(),
                        type_conversion_mode,
                        &config.type_conversion,
                    ) {
                        return ValueRef::Owned(CompactString::from(converted));
                    }
                }
            }

            // Zero-copy: raw bytes including quotes
            ValueRef::Raw(tape_quoted_str(input, entry).as_bytes())
        }
        EntryKind::ScalarStart => {
            let raw = tape_scalar_bytes(input, entry);
            let trimmed = crate::flatten::trim_ascii(raw);
            ValueRef::Raw(trimmed)
        }
        EntryKind::ObjectStart | EntryKind::ArrayStart => {
            // Nested container value — copy full byte range from input
            let start_offset = entry.offset();
            let end_tape_idx = entry.aux() as usize;
            let end_entry = tape[end_tape_idx];
            let end_offset = end_entry.offset() + 1; // include closing bracket
            debug_assert!(end_offset <= input.len());
            let raw = unsafe { input.get_unchecked(start_offset..end_offset) };
            ValueRef::Raw(raw)
        }
        _ => ValueRef::Raw(b"null"),
    }
}

/// Advance cursor past a value in the tape.
#[inline(always)]
fn advance_past_value(tape: &[TapeEntry], idx: usize) -> usize {
    skip_tape_value(tape, idx)
}

// ================================================================================================
// Collision Handling
// ================================================================================================

/// Check if any duplicate keys exist (fast path to skip collision handling
/// entirely for the dominant real-world case: no explicit collision-handling
/// config and no actual duplicate keys). Deliberately kept as a separate,
/// cheaper pre-check rather than folded into `handle_entry_collisions` --
/// see that function's doc comment for the measured reason why.
#[inline]
fn has_duplicate_keys(entries: &[(CompactString, ValueRef<'_>)]) -> bool {
    if entries.len() <= 1 {
        return false;
    }
    let mut seen: FxHashMap<&str, ()> =
        FxHashMap::with_capacity_and_hasher(entries.len(), Default::default());
    for (key, _) in entries {
        if seen.insert(key.as_str(), ()).is_some() {
            return true;
        }
    }
    false
}

/// Handle duplicate keys: merge into arrays (if enabled) or last-wins.
fn handle_entry_collisions<'a>(
    entries: Vec<(CompactString, ValueRef<'a>)>,
    merge_collisions: bool,
) -> Vec<(CompactString, ValueRef<'a>)> {
    let n = entries.len();

    // First pass: build index map using borrowed keys (avoids cloning every key).
    // `ordered` holds each unique key's first-occurrence index plus every
    // occurrence's index, in first-seen order; `key_positions` maps a key to
    // its slot in `ordered` (not its indices directly) so the output pass
    // below can read the indices straight out of `ordered` instead of doing
    // a second hashmap lookup per unique key for something this pass already
    // computed.
    let mut key_positions: FxHashMap<&str, usize> =
        FxHashMap::with_capacity_and_hasher(n, Default::default());
    let mut ordered: Vec<(usize, SmallVec<[usize; 1]>)> = Vec::with_capacity(n);

    for (i, (key, _)) in entries.iter().enumerate() {
        match key_positions.entry(key.as_str()) {
            std::collections::hash_map::Entry::Occupied(e) => {
                ordered[*e.get()].1.push(i);
            }
            std::collections::hash_map::Entry::Vacant(e) => {
                e.insert(ordered.len());
                ordered.push((i, SmallVec::from_elem(i, 1)));
            }
        }
    }

    // Fast path: no collisions
    if ordered.len() == entries.len() {
        return entries;
    }

    // Single pass: iterate `ordered`, build result directly from the indices
    // already computed above (no re-lookup needed).
    // Uses a consumed bitset instead of Vec<Option<T>> to avoid wrapping overhead.
    let mut consumed = vec![false; n];
    let mut result = Vec::with_capacity(ordered.len());

    for (first_idx, indices) in &ordered {
        let first_idx = *first_idx;

        if indices.len() == 1 {
            consumed[first_idx] = true;
            // Deferred: entry will be moved after loop
        } else if merge_collisions {
            // Merge values into a JSON array
            let estimated_len: usize = indices
                .iter()
                .map(|&idx| {
                    let (_, ref v) = entries[idx];
                    (match v {
                        ValueRef::Raw(b) => b.len(),
                        ValueRef::Owned(s) => s.len(),
                    }) + 1 // comma
                })
                .sum::<usize>()
                + 2; // brackets
            let mut array_json = CompactString::with_capacity(estimated_len);
            array_json.push('[');
            for (j, &idx) in indices.iter().enumerate() {
                if j > 0 {
                    array_json.push(',');
                }
                let (_, ref value) = entries[idx];
                match value {
                    ValueRef::Raw(bytes) => {
                        array_json.push_str(unsafe { std::str::from_utf8_unchecked(bytes) });
                    }
                    ValueRef::Owned(s) => {
                        array_json.push_str(s);
                    }
                }
                consumed[idx] = true;
            }
            array_json.push(']');
            // Temporarily push with empty key; will fix below
            result.push((first_idx, Some(ValueRef::Owned(array_json))));
            continue;
        } else {
            // Last wins
            let last_idx = *indices
                .last()
                .expect("collision indices non-empty: at least one index per key");
            for &idx in indices {
                consumed[idx] = true;
            }
            result.push((last_idx, None)); // None means use value from entries[last_idx]
            continue;
        }
        result.push((first_idx, None));
    }

    // Now move entries out (single drain, avoids per-element Option wrapping)
    let mut entries = entries;
    result
        .into_iter()
        .map(|(idx, override_value)| {
            let (key, original_value) = std::mem::replace(
                &mut entries[idx],
                (CompactString::new(""), ValueRef::Raw(b"null")),
            );
            let value = override_value.unwrap_or(original_value);
            (key, value)
        })
        .collect()
}

// ================================================================================================
// Path Analysis
// ================================================================================================

/// Find every separator byte-offset in `key`, once. Shared by the path-type analysis
/// pass below and the tree-building pass (`set_nested_value`) so a key's separators are
/// located exactly once instead of once per pass (the analysis pass used to walk the
/// key itself via `find_separator`, then tree-building re-walked the same key via
/// `str::split`).
fn find_separator_offsets(key_bytes: &[u8], sep_bytes: &[u8]) -> SmallVec<[usize; 16]> {
    let mut offsets = SmallVec::new();
    let mut search_start = 0;
    let sep_len = sep_bytes.len();

    while search_start < key_bytes.len() {
        match find_separator(key_bytes, sep_bytes, search_start) {
            Some(pos) => {
                offsets.push(pos);
                search_start = pos + sep_len;
            }
            None => break,
        }
    }

    offsets
}

/// Pre-analyze all flattened keys to build a path-type map for array vs object disambiguation.
fn analyze_path_types(
    entries: &[(CompactString, ValueRef<'_>)],
    offsets_per_entry: &[SmallVec<[usize; 16]>],
    sep_len: usize,
) -> FxHashMap<CompactString, bool> {
    let estimated_paths = entries.len() * 2;
    let mut state: FxHashMap<CompactString, u8> =
        FxHashMap::with_capacity_and_hasher(estimated_paths, Default::default());

    for ((key, _), offsets) in entries.iter().zip(offsets_per_entry) {
        analyze_key_path(key, offsets, sep_len, &mut state);
    }

    state
        .into_iter()
        .map(|(k, mask)| {
            let is_array = (mask & 0b10 == 0) && (mask & 0b01 != 0);
            (k, is_array)
        })
        .collect()
}

/// Analyze a single key's path segments (given its pre-found separator offsets) and
/// record child-type info per parent prefix.
///
/// Bitmask per parent: bit 0 (0b01) = has numeric child, bit 1 (0b10) = has non-numeric child.
/// A parent with only numeric children (mask == 0b01) is treated as an array;
/// mixed or non-numeric only (mask & 0b10 != 0) is treated as an object.
#[inline]
fn analyze_key_path(
    key: &str,
    offsets: &[usize],
    sep_len: usize,
    state: &mut FxHashMap<CompactString, u8>,
) {
    let key_len = key.len();

    for (i, &sep_pos) in offsets.iter().enumerate() {
        let parent = &key[..sep_pos];

        let child_start = sep_pos + sep_len;
        if child_start < key_len {
            let child_end = offsets.get(i + 1).copied().unwrap_or(key_len);
            let child = &key[child_start..child_end];

            let bit: u8 = if is_valid_array_index(child) {
                0b01
            } else {
                0b10
            };
            // Avoid allocation when key already exists (common for shared parent paths)
            if let Some(existing) = state.get_mut(parent) {
                *existing |= bit;
            } else {
                state.insert(CompactString::from(parent), bit);
            }
        }
    }
}

// ================================================================================================
// SIMD-Optimized Separator Finding
// ================================================================================================

/// SIMD-optimized separator finding using memchr crate
#[inline]
pub(crate) fn find_separator(haystack: &[u8], needle: &[u8], start: usize) -> Option<usize> {
    if needle.len() == 1 {
        memchr(needle[0], &haystack[start..]).map(|pos| start + pos)
    } else {
        memmem::find(&haystack[start..], needle).map(|pos| start + pos)
    }
}

// ================================================================================================
// Array Index Validation
// ================================================================================================

/// Optimized check for valid array index
#[inline(always)]
fn is_valid_array_index(s: &str) -> bool {
    if s.is_empty() {
        return false;
    }

    if s.len() == 1 {
        return s.as_bytes()[0].is_ascii_digit();
    }

    if s.starts_with('0') {
        return s == "0";
    }

    s.bytes().all(|b| b.is_ascii_digit())
}

// ================================================================================================
// Build UnflatNode Tree
// ================================================================================================

/// Build an UnflatNode tree from extracted flat entries.
fn build_unflatten_tree<'a>(
    entries: Vec<(CompactString, ValueRef<'a>)>,
    separator: &str,
    max_array_index: usize,
) -> Result<UnflatNode<'a>, JsonToolsError> {
    if entries.is_empty() {
        return Ok(UnflatNode::Object(ObjectMap::default()));
    }

    let sep_bytes = separator.as_bytes();
    let sep_len = separator.len();

    // Each key's separators are located exactly once here, then reused by both the
    // path-type analysis pass (which needs to see every sibling before the
    // tree-building pass can know if a parent is an array or object -- those two
    // passes are load-bearing and can't be merged) and the tree-building pass itself.
    let offsets_per_entry: Vec<SmallVec<[usize; 16]>> = entries
        .iter()
        .map(|(key, _)| find_separator_offsets(key.as_bytes(), sep_bytes))
        .collect();

    let path_types = analyze_path_types(&entries, &offsets_per_entry, sep_len);
    // Upper-bound capacity hint: every entry is either a direct child of `root` or
    // nested under one, so `entries.len()` is never too small. Confirmed via sampling
    // profiler that `ObjectMap::default()`'s zero starting capacity was a real,
    // measurable source of allocator churn -- `IndexMap::insert_full` repeatedly
    // triggering `realloc` as `root` grew one key at a time showed up directly in a
    // stress-test call-stack sample (`unflatten.rs:631` -> `finish_grow` -> `realloc`).
    let mut root: ObjectMap<'a> =
        ObjectMap::with_capacity_and_hasher(entries.len(), Default::default());

    // Reused across every entry below instead of allocating fresh per call:
    // `set_nested_value_recursive` always truncates it back to length 0 on
    // unwind (both the `Ok` and `Err` paths flow through the same truncate,
    // see its own tail), so it's guaranteed empty at the start of each
    // iteration -- the same "collapse N allocations into ~O(1)" pattern this
    // file already applies to `find_separator_offsets`/`ObjectMap` sizing
    // above, just not previously extended to this buffer.
    let mut path_buffer = String::new();

    for ((key, value), offsets) in entries.into_iter().zip(offsets_per_entry.iter()) {
        set_nested_value(
            &mut root,
            &key,
            offsets,
            value,
            separator,
            &path_types,
            &mut path_buffer,
            max_array_index,
        )?;
    }

    Ok(UnflatNode::Object(root))
}

/// Entry point for recursively setting a value at a nested path. `path_buffer`
/// is caller-owned and reused across entries (see `build_unflatten_tree`) --
/// guaranteed empty on entry.
#[allow(clippy::too_many_arguments)]
fn set_nested_value<'a>(
    result: &mut ObjectMap<'a>,
    key_path: &str,
    offsets: &[usize],
    value: ValueRef<'a>,
    separator: &str,
    path_types: &FxHashMap<CompactString, bool>,
    path_buffer: &mut String,
    max_array_index: usize,
) -> Result<(), JsonToolsError> {
    if offsets.is_empty() {
        // No separator found: the whole key is a single segment (leaf directly
        // under `result`). Flat keys are already unique at this point (collision
        // handling ran in Phase 3), so no two entries ever target the same leaf
        // slot -- safe to insert.
        result.insert(CompactString::from(key_path), UnflatNode::Leaf(value));
        return Ok(());
    }

    type PathSegments<'b> = SmallVec<[&'b str; 16]>;
    let sep_len = separator.len();
    let mut parts: PathSegments = SmallVec::with_capacity(offsets.len() + 1);
    let mut start = 0;
    for &pos in offsets {
        parts.push(&key_path[start..pos]);
        start = pos + sep_len;
    }
    parts.push(&key_path[start..]);

    set_nested_value_recursive(
        result,
        &parts,
        0,
        value,
        separator,
        path_types,
        path_buffer,
        max_array_index,
    )
}

/// Recursive helper that reuses a path buffer to avoid allocations.
#[allow(clippy::too_many_arguments)]
fn set_nested_value_recursive<'a>(
    current: &mut ObjectMap<'a>,
    parts: &[&str],
    index: usize,
    value: ValueRef<'a>,
    separator: &str,
    path_types: &FxHashMap<CompactString, bool>,
    path_buffer: &mut String,
    max_array_index: usize,
) -> Result<(), JsonToolsError> {
    let part = parts[index];

    if index == parts.len() - 1 {
        // Flat keys are already unique (collision handling ran in Phase 3), so no two
        // entries ever target the same leaf slot within this object -- safe to insert.
        current.insert(CompactString::from(part), UnflatNode::Leaf(value));
        return Ok(());
    }

    let buffer_start_len = path_buffer.len();
    if buffer_start_len > 0 {
        path_buffer.push_str(separator);
    }
    path_buffer.push_str(part);

    // Single hash lookup via entry() instead of contains_key + insert + get_mut
    // (was 2-3 lookups; IndexMap's entry() API does the equivalent in one).
    //
    // `path_types` is only consulted inside `or_insert_with` -- i.e. only on a
    // node's first visit -- rather than unconditionally on every call. Once a
    // container exists its Array/Object shape is fixed; every subsequent flat
    // key that shares this prefix (the common case: siblings under the same
    // nested object) would otherwise re-look-up a classification that was
    // already decided and baked into the existing node.
    let entry = current.entry(CompactString::from(part)).or_insert_with(|| {
        let should_be_array = path_types
            .get(path_buffer.as_str())
            .copied()
            .unwrap_or(false);
        if should_be_array {
            UnflatNode::Array(Vec::with_capacity(NESTED_CONTAINER_CAPACITY_HINT))
        } else {
            UnflatNode::Object(ObjectMap::with_capacity_and_hasher(
                NESTED_CONTAINER_CAPACITY_HINT,
                Default::default(),
            ))
        }
    });

    let result = match entry {
        UnflatNode::Object(ref mut obj) => set_nested_value_recursive(
            obj,
            parts,
            index + 1,
            value,
            separator,
            path_types,
            path_buffer,
            max_array_index,
        ),
        UnflatNode::Array(ref mut arr) => {
            let next_part = parts[index + 1];
            if let Ok(array_index) = next_part.parse::<usize>() {
                if array_index > max_array_index {
                    return Err(JsonToolsError::input_validation_error(format!(
                        "Array index {} exceeds maximum allowed index ({}). \
                         Use max_array_index() to increase the limit.",
                        array_index, max_array_index
                    )));
                }

                while arr.len() <= array_index {
                    arr.push(UnflatNode::Null);
                }

                if index + 2 == parts.len() {
                    arr[array_index] = UnflatNode::Leaf(value);
                    Ok(())
                } else {
                    path_buffer.push_str(separator);
                    path_buffer.push_str(next_part);

                    // Same reasoning as the Object branch above: only consult
                    // `path_types` when actually creating the node (first visit
                    // to this array slot), not on every revisit.
                    if matches!(arr[array_index], UnflatNode::Null) {
                        let next_should_be_array = path_types
                            .get(path_buffer.as_str())
                            .copied()
                            .unwrap_or(false);
                        arr[array_index] = if next_should_be_array {
                            UnflatNode::Array(Vec::with_capacity(NESTED_CONTAINER_CAPACITY_HINT))
                        } else {
                            UnflatNode::Object(ObjectMap::with_capacity_and_hasher(
                                NESTED_CONTAINER_CAPACITY_HINT,
                                Default::default(),
                            ))
                        };
                    }

                    match &mut arr[array_index] {
                        UnflatNode::Object(ref mut obj) => set_nested_value_recursive(
                            obj,
                            parts,
                            index + 2,
                            value,
                            separator,
                            path_types,
                            path_buffer,
                            max_array_index,
                        ),
                        UnflatNode::Array(ref mut nested_arr) => set_nested_array_value(
                            nested_arr,
                            parts,
                            index + 2,
                            value,
                            separator,
                            path_types,
                            path_buffer,
                            max_array_index,
                        ),
                        _ => Err(JsonToolsError::invalid_json_structure(format!(
                            "Array element at index {} has incompatible type",
                            array_index
                        ))),
                    }
                }
            } else {
                // Non-numeric key in array context — convert array to object
                let mut obj: ObjectMap<'a> = ObjectMap::default();
                let mut itoa_buf = IntBuf::new();
                for (i, item) in arr.iter_mut().enumerate() {
                    if !matches!(item, UnflatNode::Null) {
                        let taken = std::mem::replace(item, UnflatNode::Null);
                        obj.insert(CompactString::from(itoa_buf.format(i)), taken);
                    }
                }
                obj.insert(CompactString::from(next_part), UnflatNode::Null);
                *entry = UnflatNode::Object(obj);

                if let UnflatNode::Object(ref mut obj) = entry {
                    set_nested_value_recursive(
                        obj,
                        parts,
                        index + 1,
                        value,
                        separator,
                        path_types,
                        path_buffer,
                        max_array_index,
                    )
                } else {
                    unreachable!()
                }
            }
        }
        _ => Err(JsonToolsError::invalid_json_structure(format!(
            "Cannot navigate into non-object/non-array value at key: {}",
            part
        ))),
    };

    path_buffer.truncate(buffer_start_len);
    result
}

/// Recursive helper for setting nested values in arrays.
#[allow(clippy::too_many_arguments)]
fn set_nested_array_value<'a>(
    arr: &mut Vec<UnflatNode<'a>>,
    parts: &[&str],
    index: usize,
    value: ValueRef<'a>,
    separator: &str,
    path_types: &FxHashMap<CompactString, bool>,
    path_buffer: &mut String,
    max_array_index: usize,
) -> Result<(), JsonToolsError> {
    if index >= parts.len() {
        return Err(JsonToolsError::invalid_json_structure(
            "Invalid path for array",
        ));
    }

    let part = parts[index];

    if let Ok(array_index) = part.parse::<usize>() {
        if array_index > max_array_index {
            return Err(JsonToolsError::input_validation_error(format!(
                "Array index {} exceeds maximum allowed index ({}). \
                 Use max_array_index() to increase the limit.",
                array_index, max_array_index
            )));
        }

        while arr.len() <= array_index {
            arr.push(UnflatNode::Null);
        }

        if index == parts.len() - 1 {
            arr[array_index] = UnflatNode::Leaf(value);
            Ok(())
        } else {
            let buffer_start_len = path_buffer.len();
            if buffer_start_len > 0 {
                path_buffer.push_str(separator);
            }
            path_buffer.push_str(part);

            let next_should_be_array = path_types
                .get(path_buffer.as_str())
                .copied()
                .unwrap_or(false);

            if matches!(arr[array_index], UnflatNode::Null) {
                arr[array_index] = if next_should_be_array {
                    UnflatNode::Array(Vec::with_capacity(NESTED_CONTAINER_CAPACITY_HINT))
                } else {
                    UnflatNode::Object(ObjectMap::with_capacity_and_hasher(
                        NESTED_CONTAINER_CAPACITY_HINT,
                        Default::default(),
                    ))
                };
            }

            let result = match &mut arr[array_index] {
                UnflatNode::Object(ref mut obj) => set_nested_value_recursive(
                    obj,
                    parts,
                    index + 1,
                    value,
                    separator,
                    path_types,
                    path_buffer,
                    max_array_index,
                ),
                UnflatNode::Array(ref mut nested_arr) => set_nested_array_value(
                    nested_arr,
                    parts,
                    index + 1,
                    value,
                    separator,
                    path_types,
                    path_buffer,
                    max_array_index,
                ),
                _ => Err(JsonToolsError::invalid_json_structure(format!(
                    "Array element at index {} has incompatible type",
                    array_index
                ))),
            };

            path_buffer.truncate(buffer_start_len);
            result
        }
    } else {
        Err(JsonToolsError::invalid_json_structure(format!(
            "Expected array index but got: {}",
            part
        )))
    }
}

// ================================================================================================
// Direct Serialization with Integrated Filtering
// ================================================================================================

/// Serialize an UnflatNode tree directly to a JSON string with integrated filtering.
fn serialize_unflatten_tree(
    root: &UnflatNode<'_>,
    filtering: &FilteringConfig,
    value_exclusions: &[String],
    capacity_hint: usize,
) -> String {
    let mut output = String::with_capacity(capacity_hint);
    serialize_node(root, &mut output, filtering, value_exclusions);
    output
}

/// Check if a leaf value should be filtered out based on filtering config.
///
/// `s` is the leaf's already-JSON-serialized text (quotes included for strings, e.g.
/// `"\"hello\""`, not the unescaped logical content) -- `value_exclusions` patterns are
/// matched against this same serialized form for consistency with the other checks
/// here (`remove_empty_strings` already compares against the literal 2-quote `"\"\""`).
/// A literal pattern is unaffected by this; a regex with anchors needs to account for
/// the surrounding quotes on string values (e.g. `r'^"admin"$'`, not `r'^admin$'`).
#[inline]
fn should_filter_leaf(s: &str, filtering: &FilteringConfig, value_exclusions: &[String]) -> bool {
    (filtering.remove_nulls && s == "null")
        || (filtering.remove_empty_strings && s == "\"\"")
        || (filtering.remove_empty_objects && s == "{}")
        || (filtering.remove_empty_arrays && s == "[]")
        || (!value_exclusions.is_empty() && matches_any_pattern(s, value_exclusions))
}

/// Recursive serialization. Returns true if the node produced output (not filtered).
fn serialize_node(
    node: &UnflatNode<'_>,
    output: &mut String,
    filtering: &FilteringConfig,
    value_exclusions: &[String],
) -> bool {
    match node {
        UnflatNode::Leaf(vr) => {
            let s = vr.as_str();
            if should_filter_leaf(s, filtering, value_exclusions) {
                return false;
            }
            output.push_str(s);
            true
        }
        UnflatNode::Null => {
            if filtering.remove_nulls {
                return false;
            }
            if !value_exclusions.is_empty() && matches_any_pattern("null", value_exclusions) {
                return false;
            }
            output.push_str("null");
            true
        }
        UnflatNode::Object(obj) => {
            if obj.is_empty() {
                if filtering.remove_empty_objects {
                    return false;
                }
                output.push_str("{}");
                return true;
            }

            let saved = output.len();
            output.push('{');
            let mut first = true;

            // Insertion order, not sorted -- see UnflatNode::Object's doc comment.
            for (key, child) in obj {
                let child_saved = output.len();
                if !first {
                    output.push(',');
                }
                output.push('"');
                write_json_escaped_key(output, key);
                output.push_str("\":");

                if !serialize_node(child, output, filtering, value_exclusions) {
                    output.truncate(child_saved);
                } else {
                    first = false;
                }
            }

            if first {
                // All children were filtered out
                if filtering.remove_empty_objects {
                    output.truncate(saved);
                    return false;
                }
                // Write empty object
                output.truncate(saved);
                output.push_str("{}");
                return true;
            }

            output.push('}');
            true
        }
        UnflatNode::Array(vec) => {
            if vec.is_empty() {
                if filtering.remove_empty_arrays {
                    return false;
                }
                output.push_str("[]");
                return true;
            }

            let saved = output.len();
            output.push('[');
            let mut first = true;

            for child in vec {
                let child_saved = output.len();
                if !first {
                    output.push(',');
                }

                if !serialize_node(child, output, filtering, value_exclusions) {
                    output.truncate(child_saved);
                } else {
                    first = false;
                }
            }

            if first {
                // All children were filtered out
                if filtering.remove_empty_arrays {
                    output.truncate(saved);
                    return false;
                }
                output.truncate(saved);
                output.push_str("[]");
                return true;
            }

            output.push(']');
            true
        }
    }
}

// ================================================================================================
// Utility
// ================================================================================================

/// Skip whitespace bytes starting from `pos`.
#[inline(always)]
fn skip_whitespace(input: &[u8], mut pos: usize) -> usize {
    let len = input.len();
    while pos < len {
        let b = unsafe { *input.get_unchecked(pos) };
        if b > 0x20 || (b != b' ' && b != b'\t' && b != b'\n' && b != b'\r') {
            break;
        }
        pos += 1;
    }
    pos
}

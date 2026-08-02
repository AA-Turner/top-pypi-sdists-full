//! Key and value replacement transformations.
//!
//! Applies regex-based (with literal fallback) replacements to JSON keys and
//! values. Uses cached regex compilation and SIMD-accelerated substring search.
//!
//! Normal-mode processing uses tape-based streaming: scan the input once with
//! `scan_and_fixup`, then walk the tape writing directly to output with inline
//! value transforms, key transforms, and rollback-based filtering.

use crate::cache::{get_cached_regex, parse_pattern, ParsedPattern};
use crate::config::{ProcessingConfig, TypeConversionMode};
use crate::convert::convert_string_for_mode;
use crate::error::JsonToolsError;
use crate::flatten::{
    escape_json_string, scan_and_fixup, skip_tape_value, tape_content_str, tape_is_empty_array,
    tape_is_empty_object, tape_quoted_str, tape_scalar_bytes, trim_ascii, unescape_json_string,
    write_json_escaped_key, EntryKind, TapeEntry,
};
use crate::fxhash::FxHashMap;
use memchr::memmem;
use smallvec::SmallVec;
use std::borrow::Cow;

// ================================================================================================
// Key/Value Replacement Core Logic
// ================================================================================================

/// SIMD-accelerated literal replace-all: like `str::replace`, but locates
/// matches with `memchr::memmem::find` instead of `str::replace`'s std matcher.
/// Returns `None` when `from` doesn't occur in `s` at all, so callers can skip
/// the allocation entirely (matching the `Cow`-based change-detection
/// convention used throughout this module).
///
/// Deliberately calls the free `memmem::find` function in a loop rather than
/// building a `memmem::Finder` (by hand, or via `find_iter`, which builds one
/// internally regardless of haystack size) and driving it across all matches:
/// `memmem::find`'s own source picks a lightweight Rabin-Karp search for
/// haystacks under 64 bytes and only reaches for the heavier SIMD `Finder`
/// above that. JSON keys (dotted flatten paths) are almost always under 64
/// bytes, so a `Finder` built once per call pays SIMD setup cost on every
/// single key-pattern check without ever earning it back. An earlier version
/// of this function used a hand-rolled `Finder` (and, briefly, `find_iter`,
/// which has the identical cost shape) and regressed the real `iso_04`
/// Criterion benchmark's `literal_multiple` case by ~4-5% despite winning in
/// an isolated microbenchmark that only exercised the SIMD path -- caught by
/// re-validating against the project's own benchmark suite, not just the
/// isolated one. Calling `find` per-match lets each call re-pick the cheaper
/// algorithm as the remaining haystack shrinks, matching what the crate itself
/// would choose for a one-off search at that size.
///
/// Falls back to `None` (caller uses `str::replace` instead) for an empty
/// `from`: an empty needle matches at every position with zero width, which
/// needs different loop bookkeeping entirely. Empty literal patterns are legal
/// but degenerate user input (no config-time validation rejects them) and
/// don't need the SIMD fast path anyway.
///
/// Validated with both an isolated benchmark (~1.6-2x faster than
/// `str::replace` for realistic short-to-medium strings with 0-2 matches) and
/// the real `iso_04_key_replacement_only` Criterion benchmark (no regression
/// after switching from `Finder`/`find_iter` to looped `find`).
#[inline]
fn memmem_replace_all(s: &str, from: &str, to: &str) -> Option<String> {
    if from.is_empty() {
        return None;
    }
    let from_bytes = from.as_bytes();
    let bytes = s.as_bytes();
    let mut pos = 0;
    let mut out: Option<String> = None;
    while let Some(idx) = memmem::find(&bytes[pos..], from_bytes) {
        let start = pos + idx;
        let buf = out.get_or_insert_with(|| String::with_capacity(s.len() + to.len()));
        buf.push_str(&s[pos..start]);
        buf.push_str(to);
        pos = start + from.len();
    }
    out.map(|mut buf| {
        buf.push_str(&s[pos..]);
        buf
    })
}

/// Apply replacement patterns to a string. Used for both JSON keys and values
/// -- the logic doesn't care which, it just replaces patterns in a string --
/// so flatten's key-transform path and value-transform path (previously two
/// separate, near-duplicate implementations, one of which was missing the
/// SIMD literal-replace fix the other already had) now share this one.
///
/// A pattern wrapped as `r'...'` (e.g. `r'^admin_'`) is a regex; a bare
/// pattern is matched literally. See `crate::cache::ParsedPattern`. A
/// malformed `r'...'` regex is silently skipped (treated as no match) rather
/// than propagating a compile error through this hot path -- there's no
/// config-time validation point for replacement patterns today.
///
/// Regex lookup itself is cheap even though this runs once per key/value
/// across a whole batch: see `get_cached_regex`'s doc comment for the
/// thread-local "sticky" fast path that avoids re-hashing the pattern string
/// on every call when (as is the common case) the same pattern is reused
/// across many consecutive calls.
#[inline(always)]
pub(crate) fn apply_replacement_patterns(s: &str, patterns: &[(String, String)]) -> Option<String> {
    let mut current = Cow::Borrowed(s);
    let mut changed = false;

    for (pattern, replacement) in patterns {
        match parse_pattern(pattern) {
            ParsedPattern::Regex(inner) => {
                if let Ok(regex) = get_cached_regex(inner) {
                    // Use replace_all's Cow return to detect matches without a separate
                    // is_match() scan -- Owned means replacement happened, Borrowed means not.
                    if let Cow::Owned(s) = regex.replace_all(&current, replacement.as_str()) {
                        current = Cow::Owned(s);
                        changed = true;
                    }
                }
            }
            ParsedPattern::Literal(lit) => {
                if lit.is_empty() {
                    // Empty pattern: matches at every zero-width position (std's
                    // defined, if unusual, `str::replace` behavior) -- fall back
                    // directly rather than special-casing the SIMD path for it.
                    current = Cow::Owned(current.replace(lit, replacement));
                    changed = true;
                } else if let Some(replaced) = memmem_replace_all(&current, lit, replacement) {
                    current = Cow::Owned(replaced);
                    changed = true;
                }
            }
        }
    }

    if changed {
        Some(current.into_owned())
    } else {
        None
    }
}

/// Check whether `s` matches any exclusion pattern -- literal substring by default,
/// regex via `r'...'` wrapping, same convention as `apply_replacement_patterns`. Used
/// by `exclude_key` to decide whether a key (and its entire subtree) should be
/// dropped. A regex that fails to compile is treated as non-matching, mirroring
/// `apply_replacement_patterns`'s existing silent-failure behavior for bad patterns.
#[inline]
pub(crate) fn matches_any_pattern(s: &str, patterns: &[String]) -> bool {
    patterns.iter().any(|pattern| match parse_pattern(pattern) {
        ParsedPattern::Regex(inner) => get_cached_regex(inner)
            .map(|re| re.is_match(s))
            .unwrap_or(false),
        ParsedPattern::Literal(lit) => {
            lit.is_empty() || memmem::find(s.as_bytes(), lit.as_bytes()).is_some()
        }
    })
}

// ================================================================================================
// Normal Mode Processing — Tape-Based Streaming
// ================================================================================================

/// Core normal-mode logic for a single JSON string.
/// Uses tape-based streaming: scan once, walk once, write directly to output.
/// Two paths: fast (no key transforms) and slow (with key transforms + collision handling).
#[inline]
pub(crate) fn process_single_json_normal(
    json: &str,
    config: &ProcessingConfig,
) -> Result<String, JsonToolsError> {
    let input = json.as_bytes();
    if input.len() > u32::MAX as usize {
        return Err(JsonToolsError::input_validation_error(
            "Input exceeds 4 GiB limit",
        ));
    }

    let trimmed = trim_ascii(input);
    if trimmed.is_empty() {
        return Ok(json.to_string());
    }

    // Root primitives: handle without tape
    match trimmed[0] {
        b'{' | b'[' => {}
        _ => return handle_root_primitive(trimmed, config),
    }

    let tape = scan_and_fixup(input)?;
    if tape.is_empty() {
        return Ok(json.to_string());
    }

    let needs_slow = config.lowercase_keys
        || config.replacements.has_key_replacements()
        || config.collision.has_collision_handling();

    if needs_slow {
        normal_slow_walk(input, &tape, config)
    } else {
        Ok(normal_fast_walk(input, &tape, config))
    }
}

/// Handle root-level primitives (strings, numbers, booleans, null)
fn handle_root_primitive(
    trimmed: &[u8],
    config: &ProcessingConfig,
) -> Result<String, JsonToolsError> {
    // SAFETY: input is valid UTF-8 (came from &str)
    let s = unsafe { std::str::from_utf8_unchecked(trimmed) };

    // Check if it's a quoted string
    if trimmed.len() >= 2 && trimmed[0] == b'"' && trimmed[trimmed.len() - 1] == b'"' {
        let content = &s[1..s.len() - 1];
        let has_value_replacements = config.replacements.has_value_replacements();
        let auto_convert = config.type_conversion_mode != TypeConversionMode::Disabled;

        if has_value_replacements || auto_convert {
            let unescaped = if memchr::memchr(b'\\', content.as_bytes()).is_some() {
                unescape_json_string(content)
            } else {
                Cow::Borrowed(content)
            };

            // Value replacement
            if has_value_replacements {
                if let Some(replaced) = apply_replacement_patterns(
                    unescaped.as_ref(),
                    &config.replacements.value_replacements,
                ) {
                    // Also try type-converting the replaced value, so a replacement
                    // that produces a recognized token (e.g. a null/number/date
                    // sentinel) is still converted -- matches
                    // emit_string_value_shared's composable order.
                    if auto_convert {
                        if let Some(converted) = convert_string_for_mode(
                            &replaced,
                            config.type_conversion_mode,
                            &config.type_conversion,
                        ) {
                            return Ok(converted.into_owned());
                        }
                    }
                    // Re-escape and return
                    let escaped = escape_json_string(&replaced);
                    return Ok(format!("\"{}\"", escaped));
                }
            }

            // Type conversion (no replacement occurred)
            if auto_convert {
                if let Some(converted) = convert_string_for_mode(
                    unescaped.as_ref(),
                    config.type_conversion_mode,
                    &config.type_conversion,
                ) {
                    return Ok(converted.into_owned());
                }
            }
        }
    }

    // Root-level remove_nulls can't remove the whole document (there's no parent key
    // to omit the value under), so a root `null` is always returned unchanged --
    // documented no-op, matches flatten's root-primitive handling.
    Ok(s.to_string())
}

// ================================================================================================
// Shared String Emission Logic
// ================================================================================================

/// Shared logic for emitting a string value with replacements, type conversion, and filtering.
/// Used by both NormalFastWalker (fast path) and NormalSlowWalker (key-transform path).
///
/// Returns `(was_filtered, output_was_written)`. When `output_was_written` is false, the caller
/// should fall back to zero-copy output of the raw quoted string.
#[inline(always)]
fn emit_string_value_shared(
    output: &mut String,
    input: &[u8],
    entry: TapeEntry,
    config: &ProcessingConfig,
) -> (bool, bool) {
    let content_str = tape_content_str(input, entry);
    let has_replacements = config.replacements.has_value_replacements();
    let type_conversion_mode = config.type_conversion_mode;
    let auto_convert = type_conversion_mode != TypeConversionMode::Disabled;
    let has_value_exclusions = config.replacements.has_value_exclusions();

    // Early exit: nothing to transform or check
    if !has_replacements && !auto_convert && !has_value_exclusions {
        return (false, false);
    }

    // Unescape once if needed by either replacement or conversion
    let unescaped = if entry.string_has_escapes() {
        unescape_json_string(content_str)
    } else {
        Cow::Borrowed(content_str)
    };

    // Value replacement
    if has_replacements {
        if let Some(replaced) =
            apply_replacement_patterns(unescaped.as_ref(), &config.replacements.value_replacements)
        {
            if config.filtering.remove_empty_strings && replaced.is_empty() {
                return (true, true);
            }
            // Type convert the replaced value
            if auto_convert {
                if let Some(converted) = convert_string_for_mode(
                    &replaced,
                    type_conversion_mode,
                    &config.type_conversion,
                ) {
                    if config.filtering.remove_nulls && converted == "null" {
                        return (true, true);
                    }
                    if has_value_exclusions
                        && matches_any_pattern(&converted, &config.replacements.value_exclusions)
                    {
                        return (true, true);
                    }
                    output.push_str(&converted);
                    return (false, true);
                }
            }
            if has_value_exclusions
                && matches_any_pattern(&replaced, &config.replacements.value_exclusions)
            {
                return (true, true);
            }
            let escaped = escape_json_string(&replaced);
            output.push('"');
            output.push_str(escaped.as_ref());
            output.push('"');
            return (false, true);
        }
    }

    // Type conversion (no replacement occurred)
    if auto_convert {
        if let Some(converted) = convert_string_for_mode(
            unescaped.as_ref(),
            type_conversion_mode,
            &config.type_conversion,
        ) {
            if config.filtering.remove_nulls && converted == "null" {
                return (true, true);
            }
            if has_value_exclusions
                && matches_any_pattern(&converted, &config.replacements.value_exclusions)
            {
                return (true, true);
            }
            output.push_str(&converted);
            return (false, true);
        }
    }

    // Neither replacement nor conversion applied -- check the raw (unescaped) value.
    if has_value_exclusions
        && matches_any_pattern(unescaped.as_ref(), &config.replacements.value_exclusions)
    {
        return (true, true);
    }

    (false, false)
}

// ================================================================================================
// Fast Path — NormalFastWalker (no key transforms)
// ================================================================================================

/// Tape-based streaming walker for normal mode without key transforms.
/// Single-pass: walks tape and writes directly to output with inline value transforms
/// and rollback-based filtering.
struct NormalFastWalker<'a> {
    input: &'a [u8],
    tape: &'a [TapeEntry],
    config: &'a ProcessingConfig,
    output: String,
}

/// Walk the tape in fast mode (no key transforms) and produce output directly.
fn normal_fast_walk(input: &[u8], tape: &[TapeEntry], config: &ProcessingConfig) -> String {
    let mut walker = NormalFastWalker {
        input,
        tape,
        config,
        output: String::with_capacity(input.len()),
    };
    walker.walk_value(0);
    walker.output
}

impl<'a> NormalFastWalker<'a> {
    /// Walk a single value. Returns (next_tape_idx, was_filtered).
    #[inline(always)]
    fn walk_value(&mut self, idx: usize) -> (usize, bool) {
        if idx >= self.tape.len() {
            return (idx, false);
        }
        let entry = self.tape[idx];
        match entry.kind() {
            EntryKind::ObjectStart => self.walk_object(idx),
            EntryKind::ArrayStart => self.walk_array(idx),
            EntryKind::StringStart => self.emit_string_value(idx),
            EntryKind::ScalarStart => self.emit_scalar_value(idx),
            _ => (idx + 1, false),
        }
    }

    /// Walk an object: emit {key:value,...} with filtering rollback.
    fn walk_object(&mut self, start_idx: usize) -> (usize, bool) {
        let end_idx = self.tape[start_idx].aux() as usize;

        // Empty object check
        if tape_is_empty_object(self.tape, start_idx) {
            if self.config.filtering.remove_empty_objects {
                return (end_idx + 1, true);
            }
            self.output.push_str("{}");
            return (end_idx + 1, false);
        }

        let obj_start = self.output.len();
        self.output.push('{');
        let mut first = true;
        let mut cursor = start_idx + 1;

        while cursor < end_idx {
            let entry = self.tape[cursor];
            if entry.kind() == EntryKind::StringStart {
                // This is a key
                let is_excluded = self.config.replacements.has_key_exclusions() && {
                    let key_content = tape_content_str(self.input, entry);
                    let key_for_match = if entry.string_has_escapes() {
                        unescape_json_string(key_content)
                    } else {
                        Cow::Borrowed(key_content)
                    };
                    matches_any_pattern(
                        key_for_match.as_ref(),
                        &self.config.replacements.key_exclusions,
                    )
                };

                if is_excluded {
                    // True O(1) early skip -- nothing written to output at all, so
                    // no write-then-rollback truncate needed (unlike value
                    // filtering below).
                    cursor += 1; // skip key StringStart
                    if cursor < end_idx && self.tape[cursor].kind() == EntryKind::Colon {
                        cursor += 1;
                    }
                    cursor = skip_tape_value(self.tape, cursor);
                    continue;
                }

                let checkpoint = self.output.len();

                // Emit comma separator
                if !first {
                    self.output.push(',');
                }

                // Emit key (raw copy from input including quotes)
                let key_with_quotes = tape_quoted_str(self.input, entry);
                self.output.push_str(key_with_quotes);

                // Skip key and colon
                cursor += 1;
                if cursor < end_idx && self.tape[cursor].kind() == EntryKind::Colon {
                    self.output.push(':');
                    cursor += 1;
                }

                // Walk value
                let (next, filtered) = self.walk_value(cursor);
                cursor = next;

                if filtered {
                    // Rollback: remove comma + key + colon + value
                    self.output.truncate(checkpoint);
                } else {
                    first = false;
                }
            } else if entry.kind() == EntryKind::Comma {
                // Skip comma tape entries — we manage commas ourselves
                cursor += 1;
            } else {
                cursor += 1;
            }
        }

        // Check if object became empty after filtering
        if self.output.len() == obj_start + 1 && self.config.filtering.remove_empty_objects {
            self.output.truncate(obj_start);
            return (end_idx + 1, true);
        }

        self.output.push('}');
        (end_idx + 1, false)
    }

    /// Walk an array: emit [val,...] with filtering rollback.
    fn walk_array(&mut self, start_idx: usize) -> (usize, bool) {
        let end_idx = self.tape[start_idx].aux() as usize;

        // Empty array check
        if tape_is_empty_array(self.tape, start_idx) {
            if self.config.filtering.remove_empty_arrays {
                return (end_idx + 1, true);
            }
            self.output.push_str("[]");
            return (end_idx + 1, false);
        }

        let arr_start = self.output.len();
        self.output.push('[');
        let mut first = true;
        let mut cursor = start_idx + 1;

        while cursor < end_idx {
            let entry = self.tape[cursor];
            if entry.kind() == EntryKind::Comma {
                cursor += 1;
                continue;
            }

            let checkpoint = self.output.len();
            if !first {
                self.output.push(',');
            }

            let (next, filtered) = self.walk_value(cursor);
            cursor = next;

            if filtered {
                self.output.truncate(checkpoint);
            } else {
                first = false;
            }
        }

        // Check if array became empty after filtering
        if self.output.len() == arr_start + 1 && self.config.filtering.remove_empty_arrays {
            self.output.truncate(arr_start);
            return (end_idx + 1, true);
        }

        self.output.push(']');
        (end_idx + 1, false)
    }

    /// Emit a string value with inline transforms. Returns (next_idx, was_filtered).
    #[inline(always)]
    fn emit_string_value(&mut self, idx: usize) -> (usize, bool) {
        let entry = self.tape[idx];

        // Filtering: empty string
        if self.config.filtering.remove_empty_strings && entry.string_content_len() == 0 {
            return (idx + 1, true);
        }

        let (was_filtered, was_written) =
            emit_string_value_shared(&mut self.output, self.input, entry, self.config);
        if was_written {
            return (idx + 1, was_filtered);
        }

        // Zero-copy: raw string including quotes
        self.output.push_str(tape_quoted_str(self.input, entry));
        (idx + 1, false)
    }

    /// Emit a scalar value (number, bool, null). Returns (next_idx, was_filtered).
    #[inline(always)]
    fn emit_scalar_value(&mut self, idx: usize) -> (usize, bool) {
        let entry = self.tape[idx];
        let trimmed = trim_ascii(tape_scalar_bytes(self.input, entry));

        if self.config.filtering.remove_nulls && trimmed == b"null" {
            return (idx + 1, true);
        }

        // SAFETY: JSON scalars (numbers/true/false/null) are always ASCII/UTF-8.
        let s = unsafe { std::str::from_utf8_unchecked(trimmed) };
        if self.config.replacements.has_value_exclusions()
            && matches_any_pattern(s, &self.config.replacements.value_exclusions)
        {
            return (idx + 1, true);
        }
        self.output.push_str(s);
        (idx + 1, false)
    }
}

// ================================================================================================
// Slow Path — NormalSlowWalker (key transforms + collision handling)
// ================================================================================================

/// Per-object entry with transformed key and tape index for the value.
struct SlowObjectEntry {
    key: String,
    val_start: usize,
}

/// Lowercase `s`, using full Unicode case-folding (e.g. 'Ñ' -> 'ñ') for correctness.
/// `str::to_lowercase()` always allocates a new String even when nothing changes, so this
/// first does a cheap scan for any uppercase character and returns `s` unchanged if none are
/// found -- the common case for real-world JSON keys, which are typically already lowercase.
/// Real-world keys are also typically pure ASCII, so the scan itself uses a byte-level
/// `is_ascii_uppercase` check (cheaper than decoding UTF-8 codepoints) when the whole
/// string is ASCII, falling back to the full Unicode-aware scan otherwise for correctness
/// on non-ASCII uppercase (e.g. 'Ñ').
#[inline]
fn lowercase_if_needed(s: String) -> String {
    let bytes = s.as_bytes();
    let has_uppercase = if bytes.is_ascii() {
        bytes.iter().any(u8::is_ascii_uppercase)
    } else {
        s.chars().any(char::is_uppercase)
    };
    if has_uppercase {
        s.to_lowercase()
    } else {
        s
    }
}

/// Walk the tape with key transforms and collision handling.
fn normal_slow_walk(
    input: &[u8],
    tape: &[TapeEntry],
    config: &ProcessingConfig,
) -> Result<String, JsonToolsError> {
    let mut walker = NormalSlowWalker {
        input,
        tape,
        config,
        output: String::with_capacity(input.len()),
    };
    walker.walk_value(0)?;
    Ok(walker.output)
}

struct NormalSlowWalker<'a> {
    input: &'a [u8],
    tape: &'a [TapeEntry],
    config: &'a ProcessingConfig,
    output: String,
}

impl<'a> NormalSlowWalker<'a> {
    /// Walk a single value. Returns (next_tape_idx, was_filtered).
    fn walk_value(&mut self, idx: usize) -> Result<(usize, bool), JsonToolsError> {
        if idx >= self.tape.len() {
            return Ok((idx, false));
        }
        let entry = self.tape[idx];
        match entry.kind() {
            EntryKind::ObjectStart => self.walk_object(idx),
            EntryKind::ArrayStart => self.walk_array(idx),
            EntryKind::StringStart => Ok(self.emit_string_value(idx)),
            EntryKind::ScalarStart => Ok(self.emit_scalar_value(idx)),
            _ => Ok((idx + 1, false)),
        }
    }

    /// Walk an object with key transforms and collision handling.
    fn walk_object(&mut self, start_idx: usize) -> Result<(usize, bool), JsonToolsError> {
        let end_idx = self.tape[start_idx].aux() as usize;

        // Empty object check
        if tape_is_empty_object(self.tape, start_idx) {
            if self.config.filtering.remove_empty_objects {
                return Ok((end_idx + 1, true));
            }
            self.output.push_str("{}");
            return Ok((end_idx + 1, false));
        }

        // Phase 1: Collect entries with transformed keys
        let mut entries: SmallVec<[SlowObjectEntry; 16]> = SmallVec::new();
        let mut cursor = start_idx + 1;

        while cursor < end_idx {
            let entry = self.tape[cursor];
            if entry.kind() == EntryKind::StringStart {
                // Extract and transform key
                let key_str = tape_content_str(self.input, entry);

                let key_unescaped = if entry.string_has_escapes() {
                    unescape_json_string(key_str)
                } else {
                    Cow::Borrowed(key_str)
                };

                // Apply key replacement patterns
                let mut transformed_key = if self.config.replacements.has_key_replacements() {
                    apply_replacement_patterns(
                        key_unescaped.as_ref(),
                        &self.config.replacements.key_replacements,
                    )
                    .unwrap_or_else(|| key_unescaped.into_owned())
                } else {
                    key_unescaped.into_owned()
                };

                // Apply lowercase (full Unicode case-folding, e.g. 'Ñ' -> 'ñ')
                if self.config.lowercase_keys {
                    transformed_key = lowercase_if_needed(transformed_key);
                }

                // Skip key and colon
                cursor += 1;
                if cursor < end_idx && self.tape[cursor].kind() == EntryKind::Colon {
                    cursor += 1;
                }

                // Determine value tape position and advance cursor past it
                let val_start = cursor;
                cursor = skip_tape_value(self.tape, cursor);

                // Key exclusion: cursor is already advanced past the value above
                // (skip_tape_value is O(1) via the tape's precomputed container
                // end-index), so dropping this entry is just a matter of not
                // pushing it -- no extra bookkeeping needed.
                if self.config.replacements.has_key_exclusions()
                    && matches_any_pattern(
                        &transformed_key,
                        &self.config.replacements.key_exclusions,
                    )
                {
                    continue;
                }

                entries.push(SlowObjectEntry {
                    key: transformed_key,
                    val_start,
                });
            } else {
                // Skip commas and any other structural entries
                cursor += 1;
            }
        }

        // Phase 2: Detect collisions
        let has_collisions = if self.config.collision.has_collision_handling() {
            let mut seen = FxHashMap::with_capacity_and_hasher(entries.len(), Default::default());
            entries.iter().any(|e| seen.insert(&e.key, ()).is_some())
        } else {
            false
        };

        // Phase 3: Serialize
        let obj_start = self.output.len();
        self.output.push('{');

        if has_collisions {
            self.serialize_with_collisions(&entries)?;
        } else {
            self.serialize_no_collisions(&entries)?;
        }

        // Check if object became empty after filtering
        if self.output.len() == obj_start + 1 && self.config.filtering.remove_empty_objects {
            self.output.truncate(obj_start);
            return Ok((end_idx + 1, true));
        }

        self.output.push('}');
        Ok((end_idx + 1, false))
    }

    /// Serialize object entries without collisions.
    fn serialize_no_collisions(
        &mut self,
        entries: &[SlowObjectEntry],
    ) -> Result<(), JsonToolsError> {
        let mut first = true;
        for entry in entries {
            let checkpoint = self.output.len();
            if !first {
                self.output.push(',');
            }

            // Emit escaped key
            self.output.push('"');
            write_json_escaped_key(&mut self.output, &entry.key);
            self.output.push_str("\":");

            // Recurse into value
            let (_, filtered) = self.walk_value(entry.val_start)?;

            if filtered {
                self.output.truncate(checkpoint);
            } else {
                first = false;
            }
        }
        Ok(())
    }

    /// Serialize object entries with collision merging.
    fn serialize_with_collisions(
        &mut self,
        entries: &[SlowObjectEntry],
    ) -> Result<(), JsonToolsError> {
        // Group by key, preserving order of first occurrence
        let mut key_order: Vec<&str> = Vec::new();
        let mut key_indices: FxHashMap<&str, SmallVec<[usize; 2]>> =
            FxHashMap::with_capacity_and_hasher(entries.len(), Default::default());

        for (i, entry) in entries.iter().enumerate() {
            key_indices
                .entry(entry.key.as_str())
                .and_modify(|v| v.push(i))
                .or_insert_with(|| {
                    key_order.push(entry.key.as_str());
                    SmallVec::from_elem(i, 1)
                });
        }

        let mut first = true;
        for key in &key_order {
            let indices = &key_indices[key];

            if indices.len() == 1 {
                // Single entry — no collision
                let entry = &entries[indices[0]];
                let checkpoint = self.output.len();
                if !first {
                    self.output.push(',');
                }

                self.output.push('"');
                write_json_escaped_key(&mut self.output, &entry.key);
                self.output.push_str("\":");

                let (_, filtered) = self.walk_value(entry.val_start)?;
                if filtered {
                    self.output.truncate(checkpoint);
                } else {
                    first = false;
                }
            } else {
                // Collision — merge values into array
                let checkpoint = self.output.len();
                if !first {
                    self.output.push(',');
                }

                self.output.push('"');
                write_json_escaped_key(&mut self.output, key);
                self.output.push_str("\":[");

                let arr_start = self.output.len();
                let mut arr_first = true;

                for &idx in indices {
                    let entry = &entries[idx];
                    let val_checkpoint = self.output.len();
                    if !arr_first {
                        self.output.push(',');
                    }

                    let (_, filtered) = self.walk_value(entry.val_start)?;
                    if filtered {
                        self.output.truncate(val_checkpoint);
                    } else {
                        arr_first = false;
                    }
                }

                // If all values in the collision array were filtered, remove the entire entry
                if self.output.len() == arr_start {
                    self.output.truncate(checkpoint);
                } else {
                    self.output.push(']');
                    first = false;
                }
            }
        }

        Ok(())
    }

    /// Walk an array with filtering rollback.
    fn walk_array(&mut self, start_idx: usize) -> Result<(usize, bool), JsonToolsError> {
        let end_idx = self.tape[start_idx].aux() as usize;

        // Empty array check
        if tape_is_empty_array(self.tape, start_idx) {
            if self.config.filtering.remove_empty_arrays {
                return Ok((end_idx + 1, true));
            }
            self.output.push_str("[]");
            return Ok((end_idx + 1, false));
        }

        let arr_start = self.output.len();
        self.output.push('[');
        let mut first = true;
        let mut cursor = start_idx + 1;

        while cursor < end_idx {
            let entry = self.tape[cursor];
            if entry.kind() == EntryKind::Comma {
                cursor += 1;
                continue;
            }

            let checkpoint = self.output.len();
            if !first {
                self.output.push(',');
            }

            let (next, filtered) = self.walk_value(cursor)?;
            cursor = next;

            if filtered {
                self.output.truncate(checkpoint);
            } else {
                first = false;
            }
        }

        // Check if array became empty after filtering
        if self.output.len() == arr_start + 1 && self.config.filtering.remove_empty_arrays {
            self.output.truncate(arr_start);
            return Ok((end_idx + 1, true));
        }

        self.output.push(']');
        Ok((end_idx + 1, false))
    }

    /// Emit a string value with inline transforms. Returns (next_idx, was_filtered).
    #[inline(always)]
    fn emit_string_value(&mut self, idx: usize) -> (usize, bool) {
        let entry = self.tape[idx];

        // Filtering: empty string
        if self.config.filtering.remove_empty_strings && entry.string_content_len() == 0 {
            return (idx + 1, true);
        }

        let (was_filtered, was_written) =
            emit_string_value_shared(&mut self.output, self.input, entry, self.config);
        if was_written {
            return (idx + 1, was_filtered);
        }

        // Zero-copy: raw string including quotes
        self.output.push_str(tape_quoted_str(self.input, entry));
        (idx + 1, false)
    }

    /// Emit a scalar value. Returns (next_idx, was_filtered).
    #[inline(always)]
    fn emit_scalar_value(&mut self, idx: usize) -> (usize, bool) {
        let entry = self.tape[idx];
        let trimmed = trim_ascii(tape_scalar_bytes(self.input, entry));

        if self.config.filtering.remove_nulls && trimmed == b"null" {
            return (idx + 1, true);
        }

        // SAFETY: JSON scalars (numbers/true/false/null) are always ASCII/UTF-8.
        let s = unsafe { std::str::from_utf8_unchecked(trimmed) };
        if self.config.replacements.has_value_exclusions()
            && matches_any_pattern(s, &self.config.replacements.value_exclusions)
        {
            return (idx + 1, true);
        }
        self.output.push_str(s);
        (idx + 1, false)
    }
}

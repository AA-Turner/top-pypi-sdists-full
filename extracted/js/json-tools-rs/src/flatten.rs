//! JSON flattening engine using SIMD structural indexing.
//!
//! Converts nested JSON structures into flat key-value maps using a tape-based approach:
//! `scan → walk → output`. Values remain as zero-copy byte ranges into the original input.
//!
//! Key optimizations:
//! - Single-pass scanner (merges structural scan, validation, container pairing, string lengths)
//! - Byte classification LUT instead of multiple memchr calls
//! - Escape-flag tracking in tape entries to skip unescape_json_string for clean strings
//! - Direct-to-output fast path when no key transforms/collision handling needed
//! - Zero-copy value references (ValueRef::Raw) avoiding Value tree allocation

use crate::fxhash::FxHashMap;
use bumpalo::Bump;
use compact_str::CompactString;
use memchr::memchr;
use rayon::prelude::*;
use smallvec::SmallVec;
use std::borrow::Cow;
use std::ops::Deref;

use crate::config::{ProcessingConfig, TypeConversionMode};
use crate::convert::convert_string_for_mode;
use crate::error::JsonToolsError;
use crate::json_parser;
use crate::transform::{apply_replacement_patterns, matches_any_pattern};

// ================================================================================================
// SeparatorCache - Cached separator information for operations
// ================================================================================================

/// Cached separator information for operations with Cow optimization
#[derive(Clone)]
pub(crate) struct SeparatorCache {
    pub(crate) separator: Cow<'static, str>,
    is_single_char: bool,
    single_char: Option<char>,
}

impl SeparatorCache {
    #[inline]
    pub(crate) fn new(separator: &str) -> Self {
        let separator_cow = match separator {
            "." => Cow::Borrowed("."),
            "_" => Cow::Borrowed("_"),
            "::" => Cow::Borrowed("::"),
            "/" => Cow::Borrowed("/"),
            "-" => Cow::Borrowed("-"),
            "|" => Cow::Borrowed("|"),
            "->" => Cow::Borrowed("->"),
            "__" => Cow::Borrowed("__"),
            "#" => Cow::Borrowed("#"),
            "~" => Cow::Borrowed("~"),
            "@" => Cow::Borrowed("@"),
            "%" => Cow::Borrowed("%"),
            _ => Cow::Owned(separator.to_string()),
        };

        let is_single_char = separator.len() == 1;
        let single_char = if is_single_char {
            separator.chars().next()
        } else {
            None
        };

        Self {
            separator: separator_cow,
            is_single_char,
            single_char,
        }
    }

    #[inline]
    pub(crate) fn append_to_buffer(&self, buffer: &mut String) {
        if self.is_single_char {
            buffer.push(
                self.single_char
                    .expect("SeparatorCache: single_char set for single-byte separator"),
            );
        } else {
            buffer.push_str(&self.separator);
        }
    }
}

// ================================================================================================
// Data Structures
// ================================================================================================

/// Entry kind tag for tape entries.
#[repr(u8)]
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub(crate) enum EntryKind {
    ObjectStart = 0, // aux = index of matching ObjectEnd
    ObjectEnd = 1,   // aux = index of matching ObjectStart
    ArrayStart = 2,  // aux = index of matching ArrayEnd
    ArrayEnd = 3,    // aux = index of matching ArrayStart
    StringStart = 4, // aux = bits[0..23] content length, bit 23 = has_escape flag
    Colon = 5,
    Comma = 6,
    ScalarStart = 7, // aux = length of scalar bytes (trimmed)
}

/// Bit mask for the "has escape sequences" flag in StringStart aux data.
/// When set, the string content contains backslash escapes and needs unescaping.
pub(crate) const STRING_HAS_ESCAPE_BIT: u32 = 1 << 23;
/// Mask to extract the content length from StringStart aux data (bits 0..23).
pub(crate) const STRING_LENGTH_MASK: u32 = (1 << 23) - 1;

/// 8-byte tape entry — cache-line friendly (8 entries per 64B line).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
#[repr(C)]
pub(crate) struct TapeEntry {
    /// Byte offset into the original JSON input
    pub(crate) offset: u32,
    /// Packed tag: bits [0..8] = EntryKind, bits [8..32] = aux data
    pub(crate) tag: u32,
}

impl TapeEntry {
    #[inline(always)]
    pub(crate) fn new(offset: usize, kind: EntryKind, aux: u32) -> Self {
        debug_assert!(offset <= u32::MAX as usize);
        debug_assert!(aux <= 0x00FF_FFFF);
        Self {
            offset: offset as u32,
            tag: (kind as u32) | (aux << 8),
        }
    }

    #[inline(always)]
    pub(crate) fn kind(self) -> EntryKind {
        // SAFETY: EntryKind repr(u8) covers values 0..=7, and we only construct valid tags
        unsafe { std::mem::transmute(self.tag as u8) }
    }

    #[inline(always)]
    pub(crate) fn aux(self) -> u32 {
        self.tag >> 8
    }

    #[inline(always)]
    pub(crate) fn offset(self) -> usize {
        self.offset as usize
    }

    /// Overwrite aux data preserving kind and offset.
    #[inline(always)]
    pub(crate) fn set_aux(&mut self, aux: u32) {
        debug_assert!(aux <= 0x00FF_FFFF);
        self.tag = (self.tag & 0xFF) | (aux << 8);
    }

    /// For StringStart entries: get content length (bits 0..23 of aux).
    #[inline(always)]
    pub(crate) fn string_content_len(self) -> usize {
        (self.aux() & STRING_LENGTH_MASK) as usize
    }

    /// For StringStart entries: check if string contains escape sequences.
    #[inline(always)]
    pub(crate) fn string_has_escapes(self) -> bool {
        (self.aux() & STRING_HAS_ESCAPE_BIT) != 0
    }
}

/// Check if tape position is an empty object (`{}`).
#[inline(always)]
pub(crate) fn tape_is_empty_object(tape: &[TapeEntry], idx: usize) -> bool {
    idx + 1 < tape.len() && tape[idx + 1].kind() == EntryKind::ObjectEnd
}

/// Check if tape position is an empty array (`[]`).
#[inline(always)]
pub(crate) fn tape_is_empty_array(tape: &[TapeEntry], idx: usize) -> bool {
    idx + 1 < tape.len() && tape[idx + 1].kind() == EntryKind::ArrayEnd
}

// ================================================================================================
// Safe Tape Accessor Helpers
// ================================================================================================
//
// All tape access goes through these functions. The scanner guarantees:
//   1. All tape indices are within bounds of the tape array.
//   2. All byte offsets/lengths point within the validated input buffer.
//   3. All string content is valid UTF-8.
// debug_assert! catches violations in test/debug builds at zero release cost.

/// Dereference a tape entry by index.
#[inline(always)]
pub(crate) fn tape_entry(tape: &[TapeEntry], idx: usize) -> TapeEntry {
    debug_assert!(
        idx < tape.len(),
        "tape index {idx} out of bounds (len {})",
        tape.len()
    );
    unsafe { *tape.get_unchecked(idx) }
}

/// Get the unquoted string content bytes for a StringStart tape entry.
#[inline(always)]
pub(crate) fn tape_content_bytes(input: &[u8], entry: TapeEntry) -> &[u8] {
    let start = entry.offset() + 1;
    let len = entry.string_content_len();
    debug_assert!(start + len <= input.len());
    unsafe { input.get_unchecked(start..start + len) }
}

/// Get the unquoted string content as &str for a StringStart tape entry.
#[inline(always)]
pub(crate) fn tape_content_str(input: &[u8], entry: TapeEntry) -> &str {
    unsafe { std::str::from_utf8_unchecked(tape_content_bytes(input, entry)) }
}

/// Get the full quoted string (including surrounding quotes) as &str.
#[inline(always)]
pub(crate) fn tape_quoted_str(input: &[u8], entry: TapeEntry) -> &str {
    let str_offset = entry.offset();
    let content_len = entry.string_content_len();
    let end = str_offset + 1 + content_len + 1; // opening quote + content + closing quote
    debug_assert!(end <= input.len());
    unsafe { std::str::from_utf8_unchecked(input.get_unchecked(str_offset..end)) }
}

/// Get the raw bytes for a scalar (number, true, false, null) tape entry.
#[inline(always)]
pub(crate) fn tape_scalar_bytes(input: &[u8], entry: TapeEntry) -> &[u8] {
    let start = entry.offset();
    let len = entry.aux() as usize;
    debug_assert!(start + len <= input.len());
    unsafe { input.get_unchecked(start..start + len) }
}

// ================================================================================================
// ValueRef — Zero-Copy Value Reference
// ================================================================================================

/// Zero-copy reference to a JSON value in the original input.
#[derive(Debug)]
pub(crate) enum ValueRef<'a> {
    /// Raw byte slice from original input (includes quotes for strings)
    Raw(&'a [u8]),
    /// Converted/transformed value (owns the bytes) — valid JSON fragment
    Owned(String),
}

impl<'a> ValueRef<'a> {
    /// Get the value as a &str. Raw bytes are assumed valid UTF-8 (validated by scanner).
    #[inline]
    pub(crate) fn as_str(&self) -> &str {
        match self {
            ValueRef::Raw(bytes) => unsafe { std::str::from_utf8_unchecked(bytes) },
            ValueRef::Owned(s) => s.as_str(),
        }
    }
}

/// A collected flatten entry: transformed key + zero-copy value reference.
///
/// `key` is generic (`K`, bounded by `Deref<Target = str>` at point of use) rather than
/// a single fixed type: the sequential (single-document) slow path and the
/// nested-parallel path use different key storage strategies with the same tape-walking
/// logic. See `KeyBuilder`'s doc comment for why, and `CompactKeyBuilder`/
/// `BumpKeyBuilder` for the two concrete strategies.
struct CollectedEntry<'a, K> {
    key: K,
    value: ValueRef<'a>,
}

// ================================================================================================
// Key Storage Strategies
// ================================================================================================

/// Abstracts how `CollectingWalker` materializes an owned key from the path buffer and
/// applies lowercase/key-replacement transforms. Lets the sequential (single-document)
/// and nested-parallel code paths share all the tape-walking logic (`walk_object`,
/// `walk_array`, `emit_string_value`, etc.) while using different backing storage for
/// the key itself -- see `CompactKeyBuilder` and `BumpKeyBuilder`.
trait KeyBuilder {
    type Key: Deref<Target = str>;

    fn build(&self, path: &str, config: &ProcessingConfig) -> Self::Key;
}

/// Default key storage: `CompactString` (inlines keys up to 24 bytes). Used by the
/// nested-parallel path (`flatten_collecting_parallel`), where each worker thread would
/// otherwise need its own bump arena kept alive past the parallel merge -- `bumpalo::
/// Bump` isn't `Send`/`Sync`, and safely bundling per-chunk arenas with the entries that
/// borrow from them requires either unsafe self-referential-struct code or a
/// specialized crate (e.g. `yoke`), neither of which is worth it for what's already a
/// narrower case (a document large enough to cross `nested_parallel_threshold` *and*
/// key transforms configured at once).
struct CompactKeyBuilder;

impl KeyBuilder for CompactKeyBuilder {
    type Key = CompactString;

    #[inline]
    fn build(&self, path: &str, config: &ProcessingConfig) -> CompactString {
        let mut key = CompactString::from(path);
        if config.lowercase_keys {
            key.make_ascii_lowercase();
        }
        if config.replacements.has_key_replacements() {
            if let Some(new_key) =
                apply_replacement_patterns(&key, &config.replacements.key_replacements)
            {
                key = CompactString::from(new_key);
            }
        }
        key
    }
}

/// Arena-backed key storage for the sequential (single-document) slow path. Collapses N
/// per-leaf heap allocations into ~O(1) arena chunk allocations: flatten's slow-path
/// keys are full dotted paths (e.g. `"response.data.attributes.firstName"`), which
/// commonly exceed `CompactString`'s 24-byte inline cap for 3+ level nesting and would
/// otherwise still heap-allocate one at a time. Validated with an isolated benchmark
/// before adopting: ~5.9x faster than `CompactString` for realistic deep-nested-path
/// collection.
struct BumpKeyBuilder<'bump> {
    bump: &'bump Bump,
}

impl<'bump> KeyBuilder for BumpKeyBuilder<'bump> {
    type Key = &'bump str;

    #[inline]
    fn build(&self, path: &str, config: &ProcessingConfig) -> &'bump str {
        let mut key = bumpalo::collections::String::from_str_in(path, self.bump);
        if config.lowercase_keys {
            key.make_ascii_lowercase();
        }
        if config.replacements.has_key_replacements() {
            if let Some(new_key) =
                apply_replacement_patterns(&key, &config.replacements.key_replacements)
            {
                key = bumpalo::collections::String::from_str_in(&new_key, self.bump);
            }
        }
        key.into_bump_str()
    }
}

// ================================================================================================
// Byte Classification LUT — Single-pass Scanner
// ================================================================================================

/// Byte classification for the scanner LUT.
/// 0 = not structural (skip), non-zero = structural class.
const CLASS_NONE: u8 = 0;
const CLASS_LBRACE: u8 = 1; // {
const CLASS_RBRACE: u8 = 2; // }
const CLASS_LBRACKET: u8 = 3; // [
const CLASS_RBRACKET: u8 = 4; // ]
const CLASS_QUOTE: u8 = 5; // "
const CLASS_COLON: u8 = 6; // :
const CLASS_COMMA: u8 = 7; // ,

/// Build a 256-byte classification LUT at compile time.
const fn build_byte_lut() -> [u8; 256] {
    let mut lut = [CLASS_NONE; 256];
    lut[b'{' as usize] = CLASS_LBRACE;
    lut[b'}' as usize] = CLASS_RBRACE;
    lut[b'[' as usize] = CLASS_LBRACKET;
    lut[b']' as usize] = CLASS_RBRACKET;
    lut[b'"' as usize] = CLASS_QUOTE;
    lut[b':' as usize] = CLASS_COLON;
    lut[b',' as usize] = CLASS_COMMA;
    lut
}

static BYTE_LUT: [u8; 256] = build_byte_lut();

// ================================================================================================
// Unified Single-Pass Scanner
// ================================================================================================
//
// Merges structural scan, validation, container pairing, string length
// computation, and scalar detection into a single forward pass.

/// Scan JSON input and produce a fully-fixed-up tape in a single pass.
/// Container pairs are resolved, string lengths are computed, scalars
/// after colons/commas/array-starts are detected, and depth is validated.
/// String entries include the "has_escape" flag (bit 23 of aux) for zero-cost
/// escape detection during the walk phase.
pub(crate) fn scan_and_fixup(input: &[u8]) -> Result<Vec<TapeEntry>, JsonToolsError> {
    // Heuristic: ~1 structural char per 3 bytes of JSON
    let mut tape = Vec::with_capacity(input.len() / 3);
    // Stack for container pairing (stores tape indices)
    let mut stack: SmallVec<[u32; 32]> = SmallVec::new();
    let len = input.len();
    let mut pos: usize = 0;

    while pos < len {
        // SAFETY: pos < len is checked by the while condition
        let b = unsafe { *input.get_unchecked(pos) };
        let class = unsafe { *BYTE_LUT.get_unchecked(b as usize) };

        if class == CLASS_NONE {
            pos += 1;
            continue;
        }

        match class {
            CLASS_QUOTE => {
                // String: record position, find closing quote, compute content length
                let str_start = pos;
                pos += 1; // skip opening quote
                let content_start = pos;

                // Find closing quote using memchr (SIMD-accelerated). This loop only
                // needs to distinguish a real closing quote from an escaped one (`\"`)
                // to find the correct boundary -- it does NOT determine has_escape
                // (see below for why a separate pass is needed for that).
                loop {
                    match memchr(b'"', unsafe { input.get_unchecked(pos..len) }) {
                        Some(offset) => {
                            let candidate = pos + offset;
                            // Count preceding backslashes
                            let bs = count_trailing_backslashes_fast(input, candidate);
                            if bs & 1 == 0 {
                                // Even backslashes → unescaped closing quote
                                let content_len = candidate - content_start;
                                // has_escape must cover every escape type (\n, \t, \r, \uXXXX,
                                // \/, \b, \f, \\, \"), not just escaped quotes -- a JSON string
                                // can only contain a backslash as part of a valid escape
                                // sequence, so "any backslash in the content" is exactly
                                // equivalent to "needs unescaping". Checking backslash-runs
                                // only immediately before a matched quote (the old approach)
                                // missed every escape that isn't adjacent to a quote, e.g. a
                                // plain "\n" or "\t" alone in the string.
                                let has_escape = memchr(b'\\', unsafe {
                                    input.get_unchecked(content_start..candidate)
                                })
                                .is_some();
                                let mut aux = content_len as u32;
                                if has_escape {
                                    aux |= STRING_HAS_ESCAPE_BIT;
                                }
                                tape.push(TapeEntry::new(str_start, EntryKind::StringStart, aux));
                                pos = candidate + 1; // skip closing quote
                                break;
                            }
                            // Odd backslashes → escaped quote, keep scanning
                            pos = candidate + 1;
                        }
                        None => {
                            return Err(JsonToolsError::invalid_json_structure(
                                "Unterminated string in JSON input",
                            ));
                        }
                    }
                }
            }
            CLASS_LBRACE => {
                let idx = tape.len() as u32;
                tape.push(TapeEntry::new(pos, EntryKind::ObjectStart, 0));
                stack.push(idx);
                pos += 1;
            }
            CLASS_RBRACE => {
                let close_idx = tape.len();
                tape.push(TapeEntry::new(pos, EntryKind::ObjectEnd, 0));
                match stack.pop() {
                    Some(open_idx) => {
                        let open = open_idx as usize;
                        tape[open].set_aux(close_idx as u32);
                        tape[close_idx].set_aux(open_idx);
                    }
                    None => {
                        return Err(JsonToolsError::invalid_json_structure(
                            "Unexpected closing brace in JSON input",
                        ));
                    }
                }
                pos += 1;
            }
            CLASS_LBRACKET => {
                let idx = tape.len() as u32;
                tape.push(TapeEntry::new(pos, EntryKind::ArrayStart, 0));
                stack.push(idx);
                pos += 1;
                // Check for scalar as first array element
                maybe_emit_scalar(input, len, &mut tape, &mut pos)?;
            }
            CLASS_RBRACKET => {
                let close_idx = tape.len();
                tape.push(TapeEntry::new(pos, EntryKind::ArrayEnd, 0));
                match stack.pop() {
                    Some(open_idx) => {
                        let open = open_idx as usize;
                        tape[open].set_aux(close_idx as u32);
                        tape[close_idx].set_aux(open_idx);
                    }
                    None => {
                        return Err(JsonToolsError::invalid_json_structure(
                            "Unexpected closing bracket in JSON input",
                        ));
                    }
                }
                pos += 1;
            }
            CLASS_COLON => {
                tape.push(TapeEntry::new(pos, EntryKind::Colon, 0));
                pos += 1;
                // Check for scalar value after colon
                maybe_emit_scalar(input, len, &mut tape, &mut pos)?;
            }
            CLASS_COMMA => {
                tape.push(TapeEntry::new(pos, EntryKind::Comma, 0));
                pos += 1;
                // Check for scalar value after comma
                maybe_emit_scalar(input, len, &mut tape, &mut pos)?;
            }
            _ => {
                pos += 1;
            }
        }
    }

    // Validate: all containers must be closed
    if !stack.is_empty() {
        return Err(JsonToolsError::invalid_json_structure(
            "Unclosed object or array in JSON input",
        ));
    }

    Ok(tape)
}

/// Check if the next non-whitespace byte is a scalar and emit a ScalarStart entry.
/// Advances `pos` past the skipped whitespace AND the consumed scalar bytes, so the
/// main loop resumes directly at the next structural byte instead of re-classifying
/// every scalar/whitespace byte a second time through the LUT.
/// Returns Err for invalid scalars (anything other than true/false/null/numbers).
#[inline(always)]
fn maybe_emit_scalar(
    input: &[u8],
    len: usize,
    tape: &mut Vec<TapeEntry>,
    pos: &mut usize,
) -> Result<(), JsonToolsError> {
    let mut p = *pos;
    // Inline whitespace skip — avoid function call overhead
    while p < len {
        let b = unsafe { *input.get_unchecked(p) };
        if b > 0x20 || (b != b' ' && b != b'\t' && b != b'\n' && b != b'\r') {
            break;
        }
        p += 1;
    }
    if p < len {
        let next = unsafe { *input.get_unchecked(p) };
        // Not a string, object, array, or closing bracket → must be a scalar
        if next != b'"' && next != b'{' && next != b'[' && next != b']' && next != b'}' {
            let scalar_start = p;
            // Inline scalar end detection. The break set includes every
            // structural byte — a valid JSON scalar (number/true/false/null,
            // incl. exponent forms) can never contain any of them, and for
            // *invalid* input this leaves `p` on the offending structural byte
            // for the main loop to process, exactly as the pre-consuming
            // version of this scanner did.
            p += 1;
            while p < len {
                match unsafe { *input.get_unchecked(p) } {
                    b',' | b'}' | b']' | b'{' | b'[' | b'"' | b':' | b' ' | b'\t' | b'\n'
                    | b'\r' => break,
                    _ => p += 1,
                }
            }
            let scalar_len = p - scalar_start;
            // Validate: JSON scalars must be true, false, null, or a number
            let scalar_bytes = &input[scalar_start..scalar_start + scalar_len];
            validate_json_scalar(scalar_bytes)?;
            tape.push(TapeEntry::new(
                scalar_start,
                EntryKind::ScalarStart,
                scalar_len as u32,
            ));
        }
    }
    // Resume the main loop at the first unconsumed byte: whitespace and scalar
    // bytes were fully handled here, so re-scanning them through the LUT one
    // byte at a time (the previous behavior) is pure duplicated work.
    *pos = p;
    Ok(())
}

/// Validate that a byte slice is a valid JSON scalar (true, false, null, or number).
#[inline(always)]
fn validate_json_scalar(bytes: &[u8]) -> Result<(), JsonToolsError> {
    if bytes.is_empty() {
        return Err(JsonToolsError::invalid_json_structure("Empty scalar value"));
    }
    match bytes[0] {
        // Numbers: starts with digit or minus
        b'0'..=b'9' | b'-' => Ok(()),
        // true
        b't' if bytes == b"true" => Ok(()),
        // false
        b'f' if bytes == b"false" => Ok(()),
        // null
        b'n' if bytes == b"null" => Ok(()),
        _ => {
            let value = String::from_utf8_lossy(bytes);
            Err(JsonToolsError::invalid_json_structure(format!(
                "Invalid JSON value: `{value}`"
            )))
        }
    }
}

/// Count trailing backslashes before `pos`. Uses a tight loop (typically 0-1 iterations).
#[inline(always)]
fn count_trailing_backslashes_fast(input: &[u8], pos: usize) -> usize {
    let mut count = 0;
    let mut p = pos;
    while p > 0 {
        p -= 1;
        if unsafe { *input.get_unchecked(p) } != b'\\' {
            break;
        }
        count += 1;
    }
    count
}

// ================================================================================================
// IntBuf — stack-allocated integer formatter (replaces itoa crate)
// ================================================================================================

pub(crate) struct IntBuf {
    bytes: [u8; 20], // enough for usize::MAX on 64-bit (20 digits)
}

impl IntBuf {
    #[inline]
    pub(crate) fn new() -> Self {
        Self { bytes: [0u8; 20] }
    }

    #[inline]
    pub(crate) fn format(&mut self, mut n: usize) -> &str {
        if n == 0 {
            return "0";
        }
        let mut pos = 20usize;
        while n > 0 {
            pos -= 1;
            self.bytes[pos] = b'0' + (n % 10) as u8;
            n /= 10;
        }
        // SAFETY: bytes[pos..] contains only ASCII digit bytes
        unsafe { std::str::from_utf8_unchecked(&self.bytes[pos..]) }
    }
}

// ================================================================================================
// FastStreamingPathBuilder
// ================================================================================================

/// Incremental key path builder for flattening.
/// Maintains a string buffer and a stack of byte positions for O(1) push/pop.
struct FastStreamingPathBuilder {
    buffer: String,
    stack: SmallVec<[usize; 16]>,
    itoa_buf: IntBuf,
}

impl FastStreamingPathBuilder {
    #[inline]
    fn new() -> Self {
        Self {
            buffer: String::with_capacity(256),
            stack: SmallVec::new(),
            itoa_buf: IntBuf::new(),
        }
    }

    #[inline(always)]
    fn push_level(&mut self) {
        self.stack.push(self.buffer.len());
    }

    #[inline(always)]
    fn pop_level(&mut self) {
        if let Some(len) = self.stack.pop() {
            self.buffer.truncate(len);
        }
    }

    #[inline(always)]
    fn append_key_raw(&mut self, key: &str, separator: &SeparatorCache) {
        if !self.buffer.is_empty() {
            separator.append_to_buffer(&mut self.buffer);
        }
        self.buffer.push_str(key);
    }

    #[inline(always)]
    fn append_index(&mut self, index: usize, separator: &SeparatorCache) {
        if !self.buffer.is_empty() {
            separator.append_to_buffer(&mut self.buffer);
        }
        self.buffer.push_str(self.itoa_buf.format(index));
    }

    #[inline(always)]
    fn as_str(&self) -> &str {
        &self.buffer
    }
}

// ================================================================================================
// Direct-to-Output Walker (Fast Path)
// ================================================================================================
//
// When no key transforms (lowercase, key_replacements) and no collision handling
// are needed, we can write JSON output directly during the walk — skipping the
// intermediate Vec<CollectedEntry> and HashMap entirely.

/// Direct-output walker — writes flattened JSON directly to a String buffer.
struct DirectWalker<'a> {
    input: &'a [u8],
    tape: &'a [TapeEntry],
    path: FastStreamingPathBuilder,
    separator: SeparatorCache,
    config: &'a ProcessingConfig,
    output: String,
    first: bool, // true if no entry written yet
}

impl<'a> DirectWalker<'a> {
    fn new(
        input: &'a [u8],
        tape: &'a [TapeEntry],
        config: &'a ProcessingConfig,
        separator: SeparatorCache,
        output_capacity: usize,
    ) -> Self {
        let mut output = String::with_capacity(output_capacity);
        output.push('{');
        Self {
            input,
            tape,
            path: FastStreamingPathBuilder::new(),
            separator,
            config,
            output,
            first: true,
        }
    }

    #[inline(always)]
    fn finish(mut self) -> String {
        self.output.push('}');
        self.output
    }

    #[inline(always)]
    fn walk_value(&mut self, idx: usize) -> usize {
        if idx >= self.tape.len() {
            return idx;
        }
        let entry = tape_entry(self.tape, idx);
        match entry.kind() {
            EntryKind::ObjectStart => self.walk_object(idx),
            EntryKind::ArrayStart => self.walk_array(idx),
            EntryKind::StringStart => {
                self.emit_string_value(idx);
                idx + 1
            }
            EntryKind::ScalarStart => {
                self.emit_scalar_value(idx);
                idx + 1
            }
            _ => idx + 1,
        }
    }

    fn walk_object(&mut self, start_idx: usize) -> usize {
        let end_idx = self.tape[start_idx].aux() as usize;

        // Empty object check
        if tape_is_empty_object(self.tape, start_idx) {
            if !self.config.filtering.remove_empty_objects {
                self.write_value_raw(b"{}");
            }
            return end_idx + 1;
        }

        let mut cursor = start_idx + 1;
        while cursor < end_idx {
            let entry = tape_entry(self.tape, cursor);
            if entry.kind() == EntryKind::StringStart {
                let key_str = tape_content_str(self.input, entry);

                self.path.push_level();
                // `key_str` is the raw source slice, already valid JSON-escaped content --
                // DirectWalker never applies key transforms (that's CollectingWalker's job),
                // so the logical (unescaped) value is never needed here. Previously this
                // unescaped the key when it had escapes but never re-escaped it before
                // writing to output (append_key_raw's buffer becomes the output key
                // directly, unescaped), producing invalid JSON for any key containing an
                // escaped quote/backslash/control char. Using the raw slice unconditionally
                // fixes that and skips an unnecessary allocation.
                self.path.append_key_raw(key_str, &self.separator);

                cursor += 1; // skip key StringStart
                if cursor < end_idx {
                    let next = tape_entry(self.tape, cursor);
                    if next.kind() == EntryKind::Colon {
                        cursor += 1;
                    }
                }
                if self.config.replacements.has_key_exclusions()
                    && matches_any_pattern(
                        self.path.as_str(),
                        &self.config.replacements.key_exclusions,
                    )
                {
                    cursor = skip_tape_value(self.tape, cursor);
                } else {
                    cursor = self.walk_value(cursor);
                }
                self.path.pop_level();
            } else {
                cursor += 1;
            }
        }
        end_idx + 1
    }

    fn walk_array(&mut self, start_idx: usize) -> usize {
        let end_idx = self.tape[start_idx].aux() as usize;

        if tape_is_empty_array(self.tape, start_idx) {
            if !self.config.filtering.remove_empty_arrays {
                self.write_value_raw(b"[]");
            }
            return end_idx + 1;
        }

        let mut cursor = start_idx + 1;
        let mut index: usize = 0;

        while cursor < end_idx {
            let entry = tape_entry(self.tape, cursor);
            if entry.kind() == EntryKind::Comma {
                cursor += 1;
                continue;
            }
            self.path.push_level();
            self.path.append_index(index, &self.separator);
            cursor = self.walk_value(cursor);
            self.path.pop_level();
            index += 1;
        }
        end_idx + 1
    }

    #[inline(always)]
    fn emit_string_value(&mut self, idx: usize) {
        let entry = tape_entry(self.tape, idx);
        let content_len = entry.string_content_len();

        // Filtering: empty string
        if self.config.filtering.remove_empty_strings && content_len == 0 {
            return;
        }

        let content_str = tape_content_str(self.input, entry);

        let has_value_replacements = self.config.replacements.has_value_replacements();
        let type_conversion_mode = self.config.type_conversion_mode;
        let auto_convert_types = type_conversion_mode != TypeConversionMode::Disabled;
        let has_value_exclusions = self.config.replacements.has_value_exclusions();

        if has_value_replacements || auto_convert_types || has_value_exclusions {
            // Unescape once — reused below by both replacement and conversion checks
            // (previously each ran its own unescape, doubling the cost whenever both
            // features were enabled and the replacement didn't match).
            let unescaped = if entry.string_has_escapes() {
                unescape_json_string(content_str)
            } else {
                Cow::Borrowed(content_str)
            };

            // Value replacement
            if has_value_replacements {
                if let Some(replaced) = apply_replacement_patterns(
                    unescaped.as_ref(),
                    &self.config.replacements.value_replacements,
                ) {
                    if self.config.filtering.remove_empty_strings && replaced.is_empty() {
                        return;
                    }
                    // Also try type-converting the replaced value, so a replacement
                    // that produces e.g. a recognized null/number/date token is still
                    // converted and subject to remove_nulls -- matches
                    // transform.rs::emit_string_value_shared's composable order.
                    if auto_convert_types {
                        if let Some(converted) = convert_string_for_mode(
                            &replaced,
                            type_conversion_mode,
                            &self.config.type_conversion,
                        ) {
                            if self.config.filtering.remove_nulls && converted == "null" {
                                return;
                            }
                            if has_value_exclusions
                                && matches_any_pattern(
                                    &converted,
                                    &self.config.replacements.value_exclusions,
                                )
                            {
                                return;
                            }
                            self.write_leaf_json_fragment(&converted);
                            return;
                        }
                    }
                    if has_value_exclusions
                        && matches_any_pattern(
                            &replaced,
                            &self.config.replacements.value_exclusions,
                        )
                    {
                        return;
                    }
                    // Write as owned string value
                    let escaped = escape_json_string(&replaced);
                    self.write_leaf_owned_string(escaped.as_ref());
                    return;
                }
            }

            // Type conversion (no replacement occurred)
            if auto_convert_types {
                if let Some(converted) = convert_string_for_mode(
                    unescaped.as_ref(),
                    type_conversion_mode,
                    &self.config.type_conversion,
                ) {
                    if self.config.filtering.remove_nulls && converted == "null" {
                        return;
                    }
                    if has_value_exclusions
                        && matches_any_pattern(
                            &converted,
                            &self.config.replacements.value_exclusions,
                        )
                    {
                        return;
                    }
                    self.write_leaf_json_fragment(&converted);
                    return;
                }
            }

            // Neither replacement nor conversion applied -- check the raw (unescaped)
            // value before falling through to zero-copy.
            if has_value_exclusions
                && matches_any_pattern(
                    unescaped.as_ref(),
                    &self.config.replacements.value_exclusions,
                )
            {
                return;
            }
        }

        // Zero-copy: write raw bytes including quotes
        self.write_value_raw(tape_quoted_str(self.input, entry).as_bytes());
    }

    #[inline(always)]
    fn emit_scalar_value(&mut self, idx: usize) {
        let entry = tape_entry(self.tape, idx);

        // Scalars from the scanner are already trimmed by find_scalar_end,
        // but may have trailing whitespace — trim in-place
        let trimmed = trim_ascii(tape_scalar_bytes(self.input, entry));

        if self.config.filtering.remove_nulls && trimmed == b"null" {
            return;
        }
        if self.config.replacements.has_value_exclusions() {
            // SAFETY: JSON scalars (numbers/true/false/null) are always ASCII/UTF-8.
            let s = unsafe { std::str::from_utf8_unchecked(trimmed) };
            if matches_any_pattern(s, &self.config.replacements.value_exclusions) {
                return;
            }
        }
        self.write_value_raw(trimmed);
    }

    /// Write a value directly to output — key from path buffer, value from raw bytes.
    /// Batches the writes with a single reserve call.
    #[inline(always)]
    fn write_value_raw(&mut self, value_bytes: &[u8]) {
        let key = self.path.as_str();
        // Pre-reserve: comma(1) + quote(1) + key + "\":" (2) + value
        let needed = 1 + 1 + key.len() + 2 + value_bytes.len();
        self.output.reserve(needed);

        if !self.first {
            self.output.push(',');
        }
        self.first = false;
        self.output.push('"');
        self.output.push_str(key);
        self.output.push_str("\":");
        // SAFETY: JSON input is valid UTF-8
        self.output
            .push_str(unsafe { std::str::from_utf8_unchecked(value_bytes) });
    }

    /// Write a value with an owned string (quoted).
    #[inline(always)]
    fn write_leaf_owned_string(&mut self, escaped_content: &str) {
        let key = self.path.as_str();
        let needed = 1 + 1 + key.len() + 3 + escaped_content.len() + 1;
        self.output.reserve(needed);

        if !self.first {
            self.output.push(',');
        }
        self.first = false;
        self.output.push('"');
        self.output.push_str(key);
        self.output.push_str("\":\"");
        self.output.push_str(escaped_content);
        self.output.push('"');
    }

    /// Write a value with a JSON fragment (number, bool, null).
    #[inline(always)]
    fn write_leaf_json_fragment(&mut self, fragment: &str) {
        let key = self.path.as_str();
        let needed = 1 + 1 + key.len() + 2 + fragment.len();
        self.output.reserve(needed);

        if !self.first {
            self.output.push(',');
        }
        self.first = false;
        self.output.push('"');
        self.output.push_str(key);
        self.output.push_str("\":");
        self.output.push_str(fragment);
    }
}

// ================================================================================================
// Collecting Walker (Slow Path — for key transforms / collision handling)
// ================================================================================================

/// Walks the structural tape and collects flattened key-value entries.
/// Used when key transforms or collision handling require seeing all keys before output.
/// Generic over `KB: KeyBuilder` -- see its doc comment for why.
struct CollectingWalker<'a, KB: KeyBuilder> {
    input: &'a [u8],
    tape: &'a [TapeEntry],
    path: FastStreamingPathBuilder,
    separator: SeparatorCache,
    config: &'a ProcessingConfig,
    key_builder: KB,
    entries: Vec<CollectedEntry<'a, KB::Key>>,
}

impl<'a, KB: KeyBuilder> CollectingWalker<'a, KB> {
    #[allow(clippy::too_many_arguments)]
    fn new(
        input: &'a [u8],
        tape: &'a [TapeEntry],
        config: &'a ProcessingConfig,
        separator: SeparatorCache,
        capacity: usize,
        key_builder: KB,
    ) -> Self {
        Self {
            input,
            tape,
            path: FastStreamingPathBuilder::new(),
            separator,
            config,
            key_builder,
            entries: Vec::with_capacity(capacity),
        }
    }

    #[inline(always)]
    fn walk_value(&mut self, idx: usize) -> usize {
        if idx >= self.tape.len() {
            return idx;
        }
        let entry = tape_entry(self.tape, idx);
        match entry.kind() {
            EntryKind::ObjectStart => self.walk_object(idx),
            EntryKind::ArrayStart => self.walk_array(idx),
            EntryKind::StringStart => {
                self.emit_string_value(idx);
                idx + 1
            }
            EntryKind::ScalarStart => {
                self.emit_scalar_value(idx);
                idx + 1
            }
            _ => idx + 1,
        }
    }

    fn walk_object(&mut self, start_idx: usize) -> usize {
        let end_idx = self.tape[start_idx].aux() as usize;

        if tape_is_empty_object(self.tape, start_idx) {
            if !self.config.filtering.remove_empty_objects {
                self.collect_value(ValueRef::Raw(b"{}"));
            }
            return end_idx + 1;
        }

        let mut cursor = start_idx + 1;
        while cursor < end_idx {
            let entry = tape_entry(self.tape, cursor);
            if entry.kind() == EntryKind::StringStart {
                let key_str = tape_content_str(self.input, entry);

                self.path.push_level();
                if entry.string_has_escapes() {
                    let unescaped = unescape_json_string(key_str);
                    self.path
                        .append_key_raw(unescaped.as_ref(), &self.separator);
                } else {
                    self.path.append_key_raw(key_str, &self.separator);
                }

                cursor += 1;
                if cursor < end_idx {
                    let next = tape_entry(self.tape, cursor);
                    if next.kind() == EntryKind::Colon {
                        cursor += 1;
                    }
                }
                if self.config.replacements.has_key_exclusions()
                    && matches_any_pattern(
                        self.path.as_str(),
                        &self.config.replacements.key_exclusions,
                    )
                {
                    cursor = skip_tape_value(self.tape, cursor);
                } else {
                    cursor = self.walk_value(cursor);
                }
                self.path.pop_level();
            } else {
                cursor += 1;
            }
        }
        end_idx + 1
    }

    fn walk_array(&mut self, start_idx: usize) -> usize {
        let end_idx = self.tape[start_idx].aux() as usize;

        if tape_is_empty_array(self.tape, start_idx) {
            if !self.config.filtering.remove_empty_arrays {
                self.collect_value(ValueRef::Raw(b"[]"));
            }
            return end_idx + 1;
        }

        let mut cursor = start_idx + 1;
        let mut index: usize = 0;

        while cursor < end_idx {
            let entry = tape_entry(self.tape, cursor);
            if entry.kind() == EntryKind::Comma {
                cursor += 1;
                continue;
            }
            self.path.push_level();
            self.path.append_index(index, &self.separator);
            cursor = self.walk_value(cursor);
            self.path.pop_level();
            index += 1;
        }
        end_idx + 1
    }

    #[inline(always)]
    fn emit_string_value(&mut self, idx: usize) {
        let entry = tape_entry(self.tape, idx);
        let content_len = entry.string_content_len();

        if self.config.filtering.remove_empty_strings && content_len == 0 {
            return;
        }

        let content_str = tape_content_str(self.input, entry);

        let has_value_replacements = self.config.replacements.has_value_replacements();
        let type_conversion_mode = self.config.type_conversion_mode;
        let auto_convert_types = type_conversion_mode != TypeConversionMode::Disabled;
        let has_value_exclusions = self.config.replacements.has_value_exclusions();

        if has_value_replacements || auto_convert_types || has_value_exclusions {
            // Unescape once — reused below by both replacement and conversion checks
            // (previously each ran its own unescape, doubling the cost whenever both
            // features were enabled and the replacement didn't match).
            let unescaped = if entry.string_has_escapes() {
                unescape_json_string(content_str)
            } else {
                Cow::Borrowed(content_str)
            };

            if has_value_replacements {
                if let Some(replaced) = apply_replacement_patterns(
                    unescaped.as_ref(),
                    &self.config.replacements.value_replacements,
                ) {
                    if self.config.filtering.remove_empty_strings && replaced.is_empty() {
                        return;
                    }
                    // Also try type-converting the replaced value -- see
                    // DirectWalker::emit_string_value for the rationale.
                    if auto_convert_types {
                        if let Some(converted) = convert_string_for_mode(
                            &replaced,
                            type_conversion_mode,
                            &self.config.type_conversion,
                        ) {
                            if self.config.filtering.remove_nulls && *converted == *"null" {
                                return;
                            }
                            if has_value_exclusions
                                && matches_any_pattern(
                                    &converted,
                                    &self.config.replacements.value_exclusions,
                                )
                            {
                                return;
                            }
                            self.collect_value(ValueRef::Owned(converted.into_owned()));
                            return;
                        }
                    }
                    if has_value_exclusions
                        && matches_any_pattern(
                            &replaced,
                            &self.config.replacements.value_exclusions,
                        )
                    {
                        return;
                    }
                    let escaped = escape_json_string(&replaced);
                    let mut buf = String::with_capacity(escaped.len() + 2);
                    buf.push('"');
                    buf.push_str(&escaped);
                    buf.push('"');
                    self.collect_value(ValueRef::Owned(buf));
                    return;
                }
            }

            if auto_convert_types {
                if let Some(converted) = convert_string_for_mode(
                    unescaped.as_ref(),
                    type_conversion_mode,
                    &self.config.type_conversion,
                ) {
                    if self.config.filtering.remove_nulls && *converted == *"null" {
                        return;
                    }
                    if has_value_exclusions
                        && matches_any_pattern(
                            &converted,
                            &self.config.replacements.value_exclusions,
                        )
                    {
                        return;
                    }
                    self.collect_value(ValueRef::Owned(converted.into_owned()));
                    return;
                }
            }

            // Neither replacement nor conversion applied -- check the raw (unescaped)
            // value before falling through to zero-copy.
            if has_value_exclusions
                && matches_any_pattern(
                    unescaped.as_ref(),
                    &self.config.replacements.value_exclusions,
                )
            {
                return;
            }
        }

        self.collect_value(ValueRef::Raw(tape_quoted_str(self.input, entry).as_bytes()));
    }

    #[inline(always)]
    fn emit_scalar_value(&mut self, idx: usize) {
        let entry = tape_entry(self.tape, idx);
        let trimmed = trim_ascii(tape_scalar_bytes(self.input, entry));

        if self.config.filtering.remove_nulls && trimmed == b"null" {
            return;
        }
        if self.config.replacements.has_value_exclusions() {
            // SAFETY: JSON scalars (numbers/true/false/null) are always ASCII/UTF-8.
            let s = unsafe { std::str::from_utf8_unchecked(trimmed) };
            if matches_any_pattern(s, &self.config.replacements.value_exclusions) {
                return;
            }
        }
        self.collect_value(ValueRef::Raw(trimmed));
    }

    /// Apply key transforms and collect a value entry.
    #[inline]
    fn collect_value(&mut self, value: ValueRef<'a>) {
        let key = self.key_builder.build(self.path.as_str(), self.config);
        self.entries.push(CollectedEntry { key, value });
    }
}

// ================================================================================================
// Collision Resolution + Output Writing
// ================================================================================================

/// Resolve collisions and write the final JSON output.
/// Takes ownership of entries to avoid cloning keys. Generic over the key storage type
/// (`CompactString` or `&'bump str`, see `KeyBuilder`); every key access here only
/// needs `str`'s own methods, reachable via the `Deref` bound.
fn resolve_and_write<K: Deref<Target = str>>(
    entries: Vec<CollectedEntry<'_, K>>,
    config: &ProcessingConfig,
) -> String {
    if entries.is_empty() {
        return "{}".to_string();
    }

    let has_collision_handling = config.collision.has_collision_handling();
    let has_always_array_keys = config.collision.has_always_array_keys();

    // Check if we even need collision detection
    // If no collision handling, no always-array keys, and no key transforms
    // that could create collisions, we can use a simpler (faster) output path
    if !has_collision_handling
        && !has_always_array_keys
        && !config.lowercase_keys
        && !config.replacements.has_key_replacements()
    {
        return write_entries_simple(&entries);
    }

    // Build collision map. `ordered` holds each unique key's first-occurrence
    // index plus every occurrence's index, in first-seen order; `key_positions`
    // maps a key to its slot in `ordered` (not its indices directly), so the
    // output loop below can read a key's indices straight out of `ordered`
    // instead of doing a second hashmap lookup per unique key for something
    // this loop already computed (previously `&key_indices[key]`, a second
    // lookup right after this same loop just inserted that exact entry).
    let n = entries.len();
    let mut key_positions: FxHashMap<&str, usize> =
        FxHashMap::with_capacity_and_hasher(n, Default::default());
    let mut ordered: Vec<(usize, SmallVec<[usize; 1]>)> = Vec::with_capacity(n);

    for (i, entry) in entries.iter().enumerate() {
        let key: &str = &entry.key;
        match key_positions.entry(key) {
            std::collections::hash_map::Entry::Occupied(e) => {
                ordered[*e.get()].1.push(i);
            }
            std::collections::hash_map::Entry::Vacant(e) => {
                e.insert(ordered.len());
                ordered.push((i, SmallVec::from_elem(i, 1)));
            }
        }
    }

    // Estimate output size
    let output_cap = entries
        .iter()
        .map(|e| {
            e.key.len()
                + 4
                + match &e.value {
                    ValueRef::Raw(b) => b.len(),
                    ValueRef::Owned(s) => s.len(),
                }
        })
        .sum::<usize>()
        + ordered.len().saturating_sub(1) // commas between entries
        + 2; // {}

    let mut output = String::with_capacity(output_cap);
    output.push('{');
    let mut first = true;

    for (first_idx, indices) in &ordered {
        let first_idx = *first_idx;
        let key: &str = &entries[first_idx].key;

        if !first {
            output.push(',');
        }
        first = false;

        output.push('"');
        write_json_escaped_key(&mut output, key);
        output.push_str("\":");

        // A key named in `always_array_keys` always gets array treatment --
        // collecting every colliding value (not just last-wins) and wrapping
        // even a single value into a one-element array -- regardless of
        // `has_collision_handling`, so its shape is consistent across every
        // document, not just documents where a collision actually occurred.
        // Linear scan, not a hash set: `always_array_keys` is a small,
        // developer-configured list (SmallVec, stack-allocated up to 4) --
        // measured faster than a `HashSet` lookup for that realistic size
        // (~5.7% faster end-to-end via the real call path, 6/6 interleaved
        // rounds), the same "small N: scan beats hash" tradeoff already
        // applied to this crate's other small config lists.
        let force_array = has_always_array_keys
            && config
                .collision
                .always_array_keys
                .iter()
                .any(|k| k.as_str() == key);

        if force_array || (indices.len() > 1 && has_collision_handling) {
            output.push('[');
            for (j, &idx) in indices.iter().enumerate() {
                if j > 0 {
                    output.push(',');
                }
                write_value_ref(&mut output, &entries[idx].value);
            }
            output.push(']');
        } else if indices.len() == 1 {
            write_value_ref(&mut output, &entries[indices[0]].value);
        } else {
            // No collision handling, not an always-array key: last wins
            write_value_ref(
                &mut output,
                &entries[*indices
                    .last()
                    .expect("collision indices non-empty: at least one index per key")]
                .value,
            );
        }
    }

    output.push('}');
    output
}

/// Simple output path — no collision detection needed, just write entries in order.
#[inline]
fn write_entries_simple<K: Deref<Target = str>>(entries: &[CollectedEntry<'_, K>]) -> String {
    let output_cap = entries
        .iter()
        .map(|e| {
            e.key.len()
                + 4
                + match &e.value {
                    ValueRef::Raw(b) => b.len(),
                    ValueRef::Owned(s) => s.len(),
                }
        })
        .sum::<usize>()
        + entries.len().saturating_sub(1) // commas between entries
        + 2; // {}

    let mut output = String::with_capacity(output_cap);
    output.push('{');

    for (i, entry) in entries.iter().enumerate() {
        if i > 0 {
            output.push(',');
        }
        output.push('"');
        write_json_escaped_key(&mut output, &entry.key);
        output.push_str("\":");
        write_value_ref(&mut output, &entry.value);
    }

    output.push('}');
    output
}

/// Write a ValueRef to the output string.
#[inline(always)]
fn write_value_ref(output: &mut String, value: &ValueRef<'_>) {
    match value {
        ValueRef::Raw(bytes) => {
            // SAFETY: JSON input is valid UTF-8
            output.push_str(unsafe { std::str::from_utf8_unchecked(bytes) });
        }
        ValueRef::Owned(s) => {
            output.push_str(s);
        }
    }
}

/// Lookup table: `true` for bytes that need JSON escaping (0x00-0x1F, `"`, `\`).
/// Fits in 4 cache lines (256 bytes). Used by `write_json_escaped_key` and `escape_json_string`.
static NEEDS_JSON_ESCAPE: [bool; 256] = {
    let mut table = [false; 256];
    // Control characters 0x00-0x1F
    let mut i = 0u16;
    while i < 0x20 {
        table[i as usize] = true;
        i += 1;
    }
    table[b'"' as usize] = true;
    table[b'\\' as usize] = true;
    table
};

/// Check if a byte slice contains any characters that need JSON escaping.
#[inline(always)]
fn needs_json_escape(bytes: &[u8]) -> bool {
    bytes.iter().any(|&b| NEEDS_JSON_ESCAPE[b as usize])
}

/// Write a JSON-escaped key to the output.
/// Fast path: if key needs no escaping, write directly.
#[inline(always)]
pub(crate) fn write_json_escaped_key(output: &mut String, key: &str) {
    let bytes = key.as_bytes();
    // Fast path: single-pass LUT check (replaces memchr2 + sequential control-char scan)
    if !needs_json_escape(bytes) {
        output.push_str(key);
        return;
    }

    // Slow path: bulk-copy each run of plain (non-escape) bytes between special bytes,
    // instead of pushing every byte individually. `_ => output.push(b as char)` on a
    // per-byte basis is wrong for non-ASCII input: a multi-byte UTF-8 continuation/lead
    // byte re-encoded alone as its own `char` corrupts the character (e.g. "café" with
    // an embedded quote elsewhere would mangle to "cafÃ©"). All bytes the LUT marks as
    // needing escaping are ASCII (control chars, `"`, `\`), so `i` only ever stops at
    // UTF-8 character boundaries -- safe to slice at.
    let mut run_start = 0;
    let mut i = 0;
    while i < bytes.len() {
        let b = bytes[i];
        if NEEDS_JSON_ESCAPE[b as usize] {
            if run_start < i {
                output.push_str(&key[run_start..i]);
            }
            match b {
                b'"' => output.push_str("\\\""),
                b'\\' => output.push_str("\\\\"),
                b'\n' => output.push_str("\\n"),
                b'\r' => output.push_str("\\r"),
                b'\t' => output.push_str("\\t"),
                _ => {
                    let hex = b"0123456789abcdef";
                    output.push_str("\\u00");
                    output.push(hex[(b >> 4) as usize] as char);
                    output.push(hex[(b & 0x0F) as usize] as char);
                }
            }
            i += 1;
            run_start = i;
        } else {
            i += 1;
        }
    }
    if run_start < bytes.len() {
        output.push_str(&key[run_start..]);
    }
}

// ================================================================================================
// JSON String Escaping/Unescaping Utilities
// ================================================================================================

/// Unescape a JSON string's escape sequences for key/value processing.
/// Returns a Cow — borrowed if no escapes found, owned if unescaping was needed.
/// NOTE: Callers should check `TapeEntry::string_has_escapes()` first to avoid
/// calling this function when no escapes are present.
#[inline]
pub(crate) fn unescape_json_string(s: &str) -> Cow<'_, str> {
    // The caller should have checked string_has_escapes() already, but
    // as a safety net, do a fast memchr check
    if memchr(b'\\', s.as_bytes()).is_none() {
        return Cow::Borrowed(s);
    }

    let mut result = String::with_capacity(s.len());
    let bytes = s.as_bytes();
    let mut i = 0;
    // Tracks the start of the current run of plain (non-escape) bytes not yet flushed to `result`.
    let mut run_start = 0;

    while i < bytes.len() {
        if bytes[i] == b'\\' && i + 1 < bytes.len() {
            // Flush the plain-byte run preceding this escape in one UTF-8-safe bulk copy,
            // instead of re-encoding each byte individually (which corrupts multi-byte UTF-8).
            if run_start < i {
                result.push_str(&s[run_start..i]);
            }

            match bytes[i + 1] {
                b'"' => {
                    result.push('"');
                    i += 2;
                }
                b'\\' => {
                    result.push('\\');
                    i += 2;
                }
                b'/' => {
                    result.push('/');
                    i += 2;
                }
                b'n' => {
                    result.push('\n');
                    i += 2;
                }
                b'r' => {
                    result.push('\r');
                    i += 2;
                }
                b't' => {
                    result.push('\t');
                    i += 2;
                }
                b'b' => {
                    result.push('\u{0008}');
                    i += 2;
                }
                b'f' => {
                    result.push('\u{000C}');
                    i += 2;
                }
                b'u' if i + 5 < bytes.len() => {
                    let hex = &s[i + 2..i + 6];
                    if let Ok(code) = u16::from_str_radix(hex, 16) {
                        if let Some(ch) = char::from_u32(code as u32) {
                            result.push(ch);
                        } else {
                            result.push_str(&s[i..i + 6]);
                        }
                    } else {
                        result.push_str(&s[i..i + 6]);
                    }
                    i += 6;
                }
                _ => {
                    // Unknown escape: keep the backslash literally; the byte after it
                    // is left for the next run so multi-byte UTF-8 sequences stay intact.
                    result.push('\\');
                    i += 1;
                }
            }
            run_start = i;
        } else if bytes[i] == b'\\' {
            // Trailing lone backslash at end of string (no bytes[i+1]).
            i += 1;
        } else {
            i += 1;
        }
    }

    // Flush any trailing plain-byte run.
    if run_start < bytes.len() {
        result.push_str(&s[run_start..]);
    }

    Cow::Owned(result)
}

/// Escape a string for JSON output.
#[inline]
pub(crate) fn escape_json_string(s: &str) -> Cow<'_, str> {
    let bytes = s.as_bytes();
    if !needs_json_escape(bytes) {
        return Cow::Borrowed(s);
    }

    // Bulk-copy each run of plain (non-escape) bytes between special bytes -- see
    // `write_json_escaped_key`'s doc comment for why per-byte `push(b as char)` is
    // wrong for non-ASCII input (corrupts multi-byte UTF-8 sequences).
    let mut result = String::with_capacity(s.len() + 8);
    let mut run_start = 0;
    let mut i = 0;
    while i < bytes.len() {
        let b = bytes[i];
        if NEEDS_JSON_ESCAPE[b as usize] {
            if run_start < i {
                result.push_str(&s[run_start..i]);
            }
            match b {
                b'"' => result.push_str("\\\""),
                b'\\' => result.push_str("\\\\"),
                b'\n' => result.push_str("\\n"),
                b'\r' => result.push_str("\\r"),
                b'\t' => result.push_str("\\t"),
                _ => {
                    let hex = b"0123456789abcdef";
                    result.push_str("\\u00");
                    result.push(hex[(b >> 4) as usize] as char);
                    result.push(hex[(b & 0x0F) as usize] as char);
                }
            }
            i += 1;
            run_start = i;
        } else {
            i += 1;
        }
    }
    if run_start < bytes.len() {
        result.push_str(&s[run_start..]);
    }
    Cow::Owned(result)
}

/// Trim ASCII whitespace from both ends of a byte slice.
#[inline(always)]
pub(crate) fn trim_ascii(bytes: &[u8]) -> &[u8] {
    let mut start = 0;
    while start < bytes.len()
        && matches!(
            unsafe { *bytes.get_unchecked(start) },
            b' ' | b'\t' | b'\n' | b'\r'
        )
    {
        start += 1;
    }
    let mut end = bytes.len();
    while end > start
        && matches!(
            unsafe { *bytes.get_unchecked(end - 1) },
            b' ' | b'\t' | b'\n' | b'\r'
        )
    {
        end -= 1;
    }
    unsafe { bytes.get_unchecked(start..end) }
}

// ================================================================================================
// Parallelism Support
// ================================================================================================

/// Count top-level children in the tape without allocating.
/// Returns the count and whether the root is an object (vs array).
#[inline]
fn count_top_level_children(tape: &[TapeEntry]) -> usize {
    if tape.is_empty() {
        return 0;
    }
    let root = tape[0];
    let end_idx = root.aux() as usize;
    let mut count = 0usize;
    let mut cursor = 1; // skip root open

    match root.kind() {
        EntryKind::ObjectStart => {
            while cursor < end_idx && cursor < tape.len() {
                if tape[cursor].kind() == EntryKind::StringStart {
                    count += 1;
                    cursor += 1; // skip key StringStart
                    if cursor < tape.len() && tape[cursor].kind() == EntryKind::Colon {
                        cursor += 1;
                    }
                    cursor = skip_tape_value(tape, cursor);
                } else {
                    cursor += 1;
                }
            }
        }
        EntryKind::ArrayStart => {
            while cursor < end_idx && cursor < tape.len() {
                if tape[cursor].kind() == EntryKind::Comma {
                    cursor += 1;
                    continue;
                }
                count += 1;
                cursor = skip_tape_value(tape, cursor);
            }
        }
        _ => {}
    }

    count
}

/// Skip over a value in the tape, returning the index after the value.
#[inline(always)]
pub(crate) fn skip_tape_value(tape: &[TapeEntry], idx: usize) -> usize {
    if idx >= tape.len() {
        return idx;
    }
    match tape[idx].kind() {
        EntryKind::ObjectStart | EntryKind::ArrayStart => {
            let end = tape[idx].aux() as usize;
            end + 1
        }
        _ => idx + 1,
    }
}

/// Collect tape-index ranges for top-level children.
/// Each range is (key_tape_idx_or_none, value_tape_idx, array_index).
/// For objects: key_tape_idx is the StringStart of the key.
/// For arrays: key_tape_idx is usize::MAX (sentinel), array_index is the element index.
/// This avoids String allocation — keys are read from tape during the walk.
fn collect_child_ranges(tape: &[TapeEntry]) -> Vec<(usize, usize, usize)> {
    if tape.is_empty() {
        return Vec::new();
    }
    let root = tape[0];
    let end_idx = root.aux() as usize;
    // Heuristic capacity: each child consumes at least 2 tape entries (a
    // value, plus a comma/colon separator) -- avoids the doubling-growth
    // reallocations `scan_and_fixup`'s own capacity hint above already
    // avoids for the tape itself, same reasoning applied one level up.
    let mut ranges = Vec::with_capacity(end_idx.saturating_sub(1) / 2);
    let mut cursor = 1;

    match root.kind() {
        EntryKind::ObjectStart => {
            while cursor < end_idx && cursor < tape.len() {
                if tape[cursor].kind() == EntryKind::StringStart {
                    let key_idx = cursor;
                    cursor += 1;
                    if cursor < tape.len() && tape[cursor].kind() == EntryKind::Colon {
                        cursor += 1;
                    }
                    let val_idx = cursor;
                    ranges.push((key_idx, val_idx, 0));
                    cursor = skip_tape_value(tape, cursor);
                } else {
                    cursor += 1;
                }
            }
        }
        EntryKind::ArrayStart => {
            let mut index = 0usize;
            while cursor < end_idx && cursor < tape.len() {
                if tape[cursor].kind() == EntryKind::Comma {
                    cursor += 1;
                    continue;
                }
                ranges.push((usize::MAX, cursor, index));
                cursor = skip_tape_value(tape, cursor);
                index += 1;
            }
        }
        _ => {}
    }
    ranges
}

// ================================================================================================
// Parallel Flatten (Collecting Path)
// ================================================================================================

/// Parallel collecting flatten using tape-range chunks.
/// Each thread gets a slice of (key_tape_idx, value_tape_idx, array_index) ranges.
///
/// Uses `CompactKeyBuilder`, not the bump-arena `BumpKeyBuilder` the sequential
/// collecting path uses -- see `CompactKeyBuilder`'s doc comment for why (bumpalo's
/// `Bump` isn't `Send`/`Sync`, and safely bundling per-chunk arenas with the entries
/// that borrow from them across this rayon merge isn't worth the unsafe code it'd take).
fn flatten_collecting_parallel<'a>(
    input: &'a [u8],
    tape: &'a [TapeEntry],
    config: &'a ProcessingConfig,
    separator: &SeparatorCache,
    ranges: &[(usize, usize, usize)],
    is_root_object: bool,
) -> Result<Vec<CollectedEntry<'a, CompactString>>, JsonToolsError> {
    let n_threads = config.effective_thread_count(ranges.len());
    let chunk_size = ranges.len().div_ceil(n_threads);

    let process_chunks = || -> Vec<CollectedEntry<'a, CompactString>> {
        ranges
            .par_chunks(chunk_size)
            .flat_map(|range_chunk| {
                let sep = SeparatorCache::new(&separator.separator);
                let mut walker = CollectingWalker::new(
                    input,
                    tape,
                    config,
                    sep,
                    range_chunk.len() * 4,
                    CompactKeyBuilder,
                );

                for &(key_idx, val_idx, arr_idx) in range_chunk {
                    // Reset path (reuse buffer allocation)
                    walker.path.buffer.clear();
                    walker.path.stack.clear();

                    if is_root_object {
                        // Extract key from tape
                        let key_entry = tape[key_idx];
                        let key_offset = key_entry.offset() + 1;
                        let key_len = key_entry.string_content_len();
                        let key_bytes = &input[key_offset..key_offset + key_len];
                        let key_str = unsafe { std::str::from_utf8_unchecked(key_bytes) };

                        walker.path.push_level();
                        if key_entry.string_has_escapes() {
                            let key = unescape_json_string(key_str);
                            walker.path.append_key_raw(key.as_ref(), &walker.separator);
                        } else {
                            walker.path.append_key_raw(key_str, &walker.separator);
                        }
                    } else {
                        walker.path.push_level();
                        walker.path.append_index(arr_idx, &walker.separator);
                    }

                    walker.walk_value(val_idx);
                    walker.path.pop_level();
                }

                walker.entries
            })
            .collect()
    };

    // rayon's global pool is already sized to available_parallelism() and persists across
    // calls -- reuse it directly unless the caller explicitly overrode the thread count.
    let merged = match config.num_threads {
        None => process_chunks(),
        Some(n) => {
            let pool = rayon::ThreadPoolBuilder::new()
                .num_threads(n)
                .build()
                .map_err(|e| {
                    JsonToolsError::configuration_error(format!(
                        "failed to build thread pool with {n} threads: {e}"
                    ))
                })?;
            pool.install(process_chunks)
        }
    };

    Ok(merged)
}

// ================================================================================================
// Public Entry Point
// ================================================================================================

/// Returns true if the config requires collecting entries (key transforms or collision handling).
#[inline]
fn needs_collecting_path(config: &ProcessingConfig) -> bool {
    config.lowercase_keys
        || config.replacements.has_key_replacements()
        || config.collision.has_collision_handling()
        || config.collision.has_always_array_keys()
}

/// Core flattening logic for a single JSON string.
/// Entry point called by `builder.rs`.
#[inline]
pub(crate) fn process_single_json(
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
    let start = {
        let mut p = 0;
        let len = input.len();
        while p < len {
            let b = unsafe { *input.get_unchecked(p) };
            if b > 0x20 || (b != b' ' && b != b'\t' && b != b'\n' && b != b'\r') {
                break;
            }
            p += 1;
        }
        p
    };
    if start >= input.len() {
        return Err(JsonToolsError::input_validation_error("Empty JSON input"));
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
                    // converted -- matches emit_string_value's composable order.
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

    // Handle empty containers: {} → "{}", [] → "{}"
    let after_open = {
        let mut p = start + 1;
        let len = input.len();
        while p < len {
            let b = unsafe { *input.get_unchecked(p) };
            if b > 0x20 || (b != b' ' && b != b'\t' && b != b'\n' && b != b'\r') {
                break;
            }
            p += 1;
        }
        p
    };
    if after_open < input.len() {
        let close = unsafe { *input.get_unchecked(after_open) };
        if (first == b'{' && close == b'}') || (first == b'[' && close == b']') {
            return Ok("{}".to_string());
        }
    }

    // Phase 1: Single-pass scan + fixup + validation
    let tape = scan_and_fixup(input)?;

    // Phase 2: Walk — choose path based on config needs
    let separator = SeparatorCache::new(&config.separator);

    if needs_collecting_path(config) {
        // Slow path: collect entries, then resolve collisions
        let leaf_estimate = tape.len() / 4;
        let child_count = count_top_level_children(&tape);

        if child_count > config.nested_parallel_threshold {
            let ranges = collect_child_ranges(&tape);
            let is_root_object = tape[0].kind() == EntryKind::ObjectStart;
            let entries = flatten_collecting_parallel(
                input,
                &tape,
                config,
                &separator,
                &ranges,
                is_root_object,
            )?;
            Ok(resolve_and_write(entries, config))
        } else {
            // Bump arena for key storage -- see BumpKeyBuilder's doc comment. Scoped to
            // this call: dropped once `resolve_and_write` has produced the final owned
            // output String, which is the only thing that needs to outlive it.
            let bump = Bump::new();
            let mut walker = CollectingWalker::new(
                input,
                &tape,
                config,
                separator,
                leaf_estimate,
                BumpKeyBuilder { bump: &bump },
            );
            if !tape.is_empty() {
                walker.walk_value(0);
            }
            Ok(resolve_and_write(walker.entries, config))
        }
    } else {
        // Fast path: direct-to-output, always sequential
        let mut walker = DirectWalker::new(input, &tape, config, separator, input.len() * 3 / 2);
        if !tape.is_empty() {
            walker.walk_value(0);
        }
        Ok(walker.finish())
    }
}

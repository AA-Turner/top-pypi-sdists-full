//! String built-ins (incl. regex-using ones). Ported from
//! `com.dashjoin.jsonata.Functions` (task #7).
//!
//! IMPORTANT: all length / index / substring / pad operations work on Unicode
//! CODE POINTS (`char`s), not bytes, to match jsonata-js (e.g. `$length("😀")`
//! == 1). Java achieves this with surrogate-aware `codePointCount` /
//! `offsetByCodePoints`; in Rust `.chars()` already yields code points.

use crate::error::{JError, JResult};
use crate::evaluator::Evaluator;
use crate::value::{ArrayFlags, JRegex, JValue, NativeFn, NativeImpl, Object};
use std::rc::Rc;

// ---------------------------------------------------------------------------
// helpers
// ---------------------------------------------------------------------------

/// Number of Unicode code points in `s`.
fn cp_len(s: &str) -> usize {
    s.chars().count()
}

/// `Functions.substr` (source: Jsonata4Java JSONataUtils.substr) — Java's
/// hybrid code-point / UTF-16 semantics, replicated exactly (see COMPAT.md):
///
/// * `start` is resolved in CODE POINTS (negative counts from the end), then
///   converted to a UTF-16 offset via `offsetByCodePoints`.
/// * `length` is interpreted as a code-point count measured from the START of
///   the string and converted to a UTF-16 length the same way — so with astral
///   characters before `start`, the extracted window is longer than `length`
///   code points: `$substring('😀abc', 1, 2)` → "abc".
/// * jsonata-js indexes purely by code points ("ab" for the example above).
///
/// One deliberate deviation: when `length` (defaulted by the caller to the
/// UTF-16 unit length) exceeds the string's code-point count, Java's
/// `offsetByCodePoints(0, length)` throws StringIndexOutOfBoundsException —
/// i.e. `$substring(s, start)` with NO length crashes on ANY astral-bearing
/// string. That raw-crash class is not replicated: the count is capped at the
/// code-point length, yielding "rest of the string" (what jsonata-js returns).
fn substr(str: &str, start: i64, length: Option<i64>) -> String {
    let units: Vec<u16> = str.encode_utf16().collect();
    let orig_len = units.len() as i64; // Java str.length() — UTF-16 units
    let str_len = str.chars().count() as i64; // codePointCount

    if start >= str_len {
        return String::new();
    }

    // Resolve negative start in code points; clamp to 0.
    let resolved = if start >= 0 {
        start
    } else if str_len + start < 0 {
        0
    } else {
        str_len + start
    };
    // offsetByCodePoints(0, resolved) — UTF-16 offset of that code point.
    let start_units = utf16_offset_of_cp(str, resolved as usize) as i64;

    // Resolve length: None -> origLen (units!), negative -> "" (caller already
    // rejects <= 0 for the 3-arg form; None reaches here for the 2-arg form).
    let mut length = match length {
        None => orig_len,
        Some(l) if l < 0 => return String::new(),
        Some(l) => l.min(orig_len),
    };
    // Java: offsetByCodePoints(0, length) — interpret as code points from the
    // string start; cap at the code-point count instead of throwing.
    length = length.min(str_len);
    let length_units = utf16_offset_of_cp(str, length as usize) as i64;

    if start_units >= orig_len {
        return String::new();
    }
    let end = (start_units + length_units).min(orig_len) as usize;
    // Slicing UTF-16 units can split a surrogate pair; a Rust String cannot
    // hold the lone surrogate Java would produce -> U+FFFD (representability
    // limit, same class as test-overrides-local.json).
    String::from_utf16_lossy(&units[start_units as usize..end])
}

/// `String.offsetByCodePoints(0, cp)` — the UTF-16 unit offset of code point
/// index `cp` (clamped to the end of the string).
fn utf16_offset_of_cp(s: &str, cp: usize) -> usize {
    s.chars().take(cp).map(|c| c.len_utf16()).sum()
}

/// `Functions.leftPad` (Jsonata4Java PadFunction), code-point based.
fn left_pad(str: &str, size: i64, pad_str: &str) -> String {
    let pad_str = if cp_len(pad_str) == 0 { " " } else { pad_str };
    let str_len = cp_len(str) as i64;
    let pads = size - str_len;
    if pads <= 0 {
        return str.to_string();
    }
    // Build padding by repeating pad_str (pads+1) times then take `pads` cps.
    let mut padding = String::new();
    for _ in 0..(pads + 1) {
        padding.push_str(pad_str);
    }
    let prefix = substr(&padding, 0, Some(pads));
    format!("{}{}", prefix, str)
}

/// `Functions.rightPad` (Jsonata4Java PadFunction), code-point based.
fn right_pad(str: &str, size: i64, pad_str: &str) -> String {
    let pad_str = if cp_len(pad_str) == 0 { " " } else { pad_str };
    let str_len = cp_len(str) as i64;
    let pads = size - str_len;
    if pads <= 0 {
        return str.to_string();
    }
    let mut padding = String::new();
    for _ in 0..(pads + 1) {
        padding.push_str(pad_str);
    }
    let suffix = substr(&padding, 0, Some(pads));
    format!("{}{}", str, suffix)
}

/// Byte offset of the start of code-point index `cp` in `s`. If `cp` is past
/// the end, returns `s.len()`.
fn cp_index_to_byte(s: &str, cp: usize) -> usize {
    s.char_indices().nth(cp).map(|(b, _)| b).unwrap_or(s.len())
}

// ---------------------------------------------------------------------------
// regex building (fancy-regex)
// ---------------------------------------------------------------------------

/// Build a `fancy_regex::Regex` from a JSONata regex literal. JSONata regexes
/// always behave as global; the `g` flag is applied by the iteration logic, so
/// here we only fold in `(?i)` / `(?m)` inline flags.
///
/// PORT-NOTE: jsonata-java uses `java.util.regex`; we use `fancy-regex` (a
/// backtracking engine over the `regex` crate) to support backreferences and
/// lookaround like Java. Pattern *syntax* differs in edge cases (named groups,
/// POSIX classes, some escapes) — see PORT-NOTE at the bottom of this file.
fn build_regex(re: &JRegex) -> JResult<fancy_regex::Regex> {
    let mut src = String::new();
    if re.case_insensitive {
        src.push_str("(?i)");
    }
    if re.multiline {
        src.push_str("(?m)");
    }
    src.push_str(&asciify_perl_classes(&re.pattern));
    fancy_regex::Regex::new(&src)
        // Java would throw PatternSyntaxException at compile time; surface a
        // generic error here. (No specific JSONata code maps cleanly.)
        .map_err(|e| JError::at(&format!("Invalid regex: {}", e), -1))
}

/// Rewrite `\w`/`\W`/`\d`/`\D` to their ASCII definitions. Both
/// java.util.regex (without UNICODE_CHARACTER_CLASS) and JavaScript RegExp
/// define these classes over ASCII, while the `regex`/`fancy-regex` crates
/// default to Unicode-aware classes — `$replace('šžç', /\w/, 'X')` must leave
/// the string unchanged. (`\s` is left alone: it is Unicode in JavaScript,
/// which is the semantic reference; `\D`/`\W` inside character classes are
/// also left alone — rare, and not expressible by simple substitution.)
fn asciify_perl_classes(pattern: &str) -> String {
    let chars: Vec<char> = pattern.chars().collect();
    let mut out = String::with_capacity(pattern.len() + 8);
    let mut in_class = false;
    let mut i = 0;
    while i < chars.len() {
        let c = chars[i];
        if c == '\\' && i + 1 < chars.len() {
            let d = chars[i + 1];
            let rewritten = match (d, in_class) {
                ('w', false) => Some("[0-9A-Za-z_]"),
                ('w', true) => Some("0-9A-Za-z_"),
                ('W', false) => Some("[^0-9A-Za-z_]"),
                ('d', false) => Some("[0-9]"),
                ('d', true) => Some("0-9"),
                ('D', false) => Some("[^0-9]"),
                _ => None,
            };
            match rewritten {
                Some(r) => out.push_str(r),
                None => {
                    out.push(c);
                    out.push(d);
                }
            }
            i += 2;
            continue;
        }
        if c == '[' && !in_class {
            in_class = true;
        } else if c == ']' && in_class {
            in_class = false;
        }
        out.push(c);
        i += 1;
    }
    out
}

/// One match produced by iterating a regex globally over `str`.
struct RegexpMatch {
    /// code-point index of match start
    index: usize,
    /// the full match text (group 0)
    text: String,
    /// capturing groups 1..=n (None -> empty string, matching Java which adds
    /// `m.group(g)` that may be null but is stored as a String entry)
    groups: Vec<JValue>,
}

/// `Functions.evaluateMatcher` — iterate the pattern globally over `str`,
/// collecting each match with its (code-point) start index and capture groups.
///
/// PORT-NOTE: Java's `Matcher.find()` advances past the previous match end and,
/// for a zero-width match, the engine bumps the search position by one. We
/// replicate that bump so e.g. an empty-match pattern terminates.
fn evaluate_matcher(re: &fancy_regex::Regex, str: &str) -> JResult<Vec<RegexpMatch>> {
    let mut res = Vec::new();
    let mut search_byte = 0usize;
    loop {
        if search_byte > str.len() {
            break;
        }
        let caps = match re.captures_from_pos(str, search_byte) {
            Ok(Some(c)) => c,
            Ok(None) => break,
            Err(e) => return Err(JError::at(&format!("Regex error: {}", e), -1)),
        };
        let m0 = caps.get(0).unwrap();
        let start_byte = m0.start();
        let end_byte = m0.end();
        let index = cp_len(&str[..start_byte]);

        let mut groups: Vec<JValue> = Vec::new();
        for g in 1..caps.len() {
            match caps.get(g) {
                Some(gm) => groups.push(JValue::string(gm.as_str())),
                // Java collects m.group(g) which may be null; jsonata-js stores
                // undefined. We push Undefined for an unmatched optional group.
                None => groups.push(JValue::Undefined),
            }
        }

        res.push(RegexpMatch {
            index,
            text: m0.as_str().to_string(),
            groups,
        });

        // advance: past the end of this match; bump by one cp on zero-width.
        // The zero-width test must be match-relative (end == start), not
        // position-relative (end > search pos) — otherwise an empty match found
        // *ahead* of the search position is re-found and recorded twice.
        if end_byte > start_byte {
            search_byte = end_byte;
        } else {
            // zero-width match: advance one code point past start
            let next = str[start_byte..].chars().next().map(|c| c.len_utf8());
            match next {
                Some(n) => search_byte = start_byte + n,
                None => break,
            }
        }
    }
    Ok(res)
}

// ---------------------------------------------------------------------------
// $string
// ---------------------------------------------------------------------------

/// `$string(arg, prettify)` — the `<x-b?:s>` builtin.
pub fn string_fn(args: &[JValue]) -> JResult<JValue> {
    let raw = crate::functions::arg(args, 0);
    // Java unwraps an outer-wrapper JList to its [0] element FIRST, then checks
    // for null. Mirror that ordering so an outer-wrapped undefined -> undefined.
    let arg = match &raw {
        JValue::Array(a, f) if f.outer_wrapper && !a.is_empty() => a[0].clone(),
        _ => raw.clone(),
    };
    // Java: if (arg == null) return null;  (undefined input -> undefined)
    if arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let prettify = crate::functions::arg(args, 1);
    let prettify_bool = matches!(prettify, JValue::Bool(true));
    // crate::functions::string applies the same outer-wrapper unwrap again
    // (idempotent) and returns strings unchanged.
    let s = crate::functions::string(&arg, prettify_bool)?;
    Ok(JValue::string(s))
}

// ---------------------------------------------------------------------------
// $substring / $substringBefore / $substringAfter
// ---------------------------------------------------------------------------

/// `$substring(str, start, length?)`.
pub fn substring(args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    // undefined input -> undefined
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let str = str_arg.as_str().unwrap_or("");

    let start_v = crate::functions::arg(args, 1);
    let length_v = crate::functions::arg(args, 2);

    // Java: _start.intValue() — truncates toward zero
    let start = start_v.as_f64().map(|d| d.trunc() as i64);
    let length = if length_v.is_undefined() {
        None
    } else {
        length_v.as_f64().map(|d| d.trunc() as i64)
    };

    // Java: Integer start = _start!=null ? _start.intValue() : null; then uses
    // start unconditionally. The $substring signature makes start required.
    let start = start.unwrap_or(0);
    let str_length = cp_len(str) as i64;

    // if (strLength + start < 0) start = 0;
    let mut start = start;
    if str_length + start < 0 {
        start = 0;
    }

    match length {
        Some(l) => {
            if l <= 0 {
                Ok(JValue::string(""))
            } else {
                Ok(JValue::string(substr(str, start, Some(l))))
            }
        }
        None => Ok(JValue::string(substr(str, start, Some(str_length)))),
    }
}

/// `$substringBefore(str, chars)`.
pub fn substring_before(args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let str = str_arg.as_str().unwrap_or("");
    let chars_v = crate::functions::arg(args, 1);
    if chars_v.is_undefined() {
        return Ok(JValue::string(str));
    }
    let chars = chars_v.as_str().unwrap_or("");
    match str.find(chars) {
        Some(byte_pos) => Ok(JValue::string(&str[..byte_pos])),
        None => Ok(JValue::string(str)),
    }
}

/// `$substringAfter(str, chars)`.
pub fn substring_after(args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let str = str_arg.as_str().unwrap_or("");
    let chars_v = crate::functions::arg(args, 1);
    let chars = chars_v.as_str().unwrap_or("");
    match str.find(chars) {
        Some(byte_pos) => Ok(JValue::string(&str[byte_pos + chars.len()..])),
        None => Ok(JValue::string(str)),
    }
}

// ---------------------------------------------------------------------------
// $lowercase / $uppercase / $length / $trim / $pad
// ---------------------------------------------------------------------------

pub fn lowercase(args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let str = str_arg.as_str().unwrap_or("");
    Ok(JValue::string(str.to_lowercase()))
}

pub fn uppercase(args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let str = str_arg.as_str().unwrap_or("");
    Ok(JValue::string(str.to_uppercase()))
}

/// `$length(str)` — number of code points.
pub fn length(args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let str = str_arg.as_str().unwrap_or("");
    Ok(JValue::number(cp_len(str) as f64))
}

/// `$trim(str)` — collapse runs of `[ \t\n\r]` to a single space, then strip a
/// single leading / trailing space.
pub fn trim(args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let str = str_arg.as_str().unwrap_or("");
    if str.is_empty() {
        return Ok(JValue::string(""));
    }

    // normalize whitespace: replaceAll("[ \t\n\r]+", " ")
    let mut result = String::with_capacity(str.len());
    let mut in_ws = false;
    for c in str.chars() {
        if c == ' ' || c == '\t' || c == '\n' || c == '\r' {
            if !in_ws {
                result.push(' ');
                in_ws = true;
            }
        } else {
            result.push(c);
            in_ws = false;
        }
    }

    // strip single leading space
    if result.starts_with(' ') {
        result.remove(0);
    }
    if result.is_empty() {
        return Ok(JValue::string(""));
    }
    // strip single trailing space
    if result.ends_with(' ') {
        result.pop();
    }
    Ok(JValue::string(result))
}

/// `$pad(str, width, char?)` — negative width left-pads, positive right-pads.
pub fn pad(args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let str = str_arg.as_str().unwrap_or("");

    let char_v = crate::functions::arg(args, 2);
    let pad_char = match char_v.as_str() {
        Some(c) if !c.is_empty() => c.to_string(),
        _ => " ".to_string(),
    };

    let width_v = crate::functions::arg(args, 1);
    // Java: _width.intValue() (truncate toward zero)
    let width = width_v.as_f64().map(|d| d.trunc() as i64).unwrap_or(0);

    let result = if width < 0 {
        left_pad(str, -width, &pad_char)
    } else {
        right_pad(str, width, &pad_char)
    };
    Ok(JValue::string(result))
}

// ---------------------------------------------------------------------------
// $contains / $match / $split / $replace (regex-using)
// ---------------------------------------------------------------------------

/// `$contains(str, token)` — token is a string (substring test) or a regex.
///
/// PORT-NOTE: the `<s-(sf):b>` signature means `token` is "string or function".
/// A `/regex/` literal is a function value (`JValue::Regex`); a plain string is
/// a substring test. (jsonata-java's `contains` matches on `String` vs
/// `Pattern`; here a string-typed token is a literal substring.)
pub fn contains(ev: &mut Evaluator, args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let str = str_arg.as_str().unwrap_or("");

    let token = crate::functions::arg(args, 1);
    match &token {
        JValue::String(t) => Ok(JValue::Bool(str.contains(t.as_ref()))),
        JValue::Regex(re) => {
            let compiled = build_regex(re)?;
            let matches = evaluate_matcher(&compiled, str)?;
            Ok(JValue::Bool(!matches.is_empty()))
        }
        // A function token: apply it; treat a non-undefined / truthy match
        // result analogously to the regex path. (Java only handles String /
        // Pattern, but the signature permits a function.)
        f if f.is_function() => {
            let res = ev.func_apply(f, vec![str_arg.clone()])?;
            Ok(JValue::Bool(!res.is_undefined()))
        }
        _ => Err(JError::at("T0410", -1)),
    }
}

/// `$match(str, pattern, limit?)` — array of `{match, index, groups}`.
pub fn match_fn(ev: &mut Evaluator, args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let str = str_arg.as_str().unwrap_or("");

    let limit_v = crate::functions::arg(args, 2);
    // Java: if (limit!=null && limit < 0) throw D3040
    let limit: Option<i64> = if limit_v.is_undefined() {
        None
    } else {
        let l = limit_v.as_f64().map(|d| d.trunc() as i64).unwrap_or(0);
        if l < 0 {
            // Java: throw new JException("D3040", -1, limit)
            return Err(JError::with_current("D3040", -1, JValue::number(l as f64)));
        }
        Some(l)
    };

    let pattern = crate::functions::arg(args, 1);

    // collect matches as RegexpMatch-equivalents
    let matches: Vec<RegexpMatch> = match &pattern {
        JValue::Regex(re) => {
            let compiled = build_regex(re)?;
            evaluate_matcher(&compiled, str)?
        }
        f if f.is_function() => {
            // Applying a function pattern yields the regexClosure chain. Walk
            // the linked list of {match,index,groups,next}.
            return match_via_function(ev, f, &str_arg, limit);
        }
        _ => return Err(JError::at("T0410", -1)),
    };

    let mut result: Vec<JValue> = Vec::new();
    // Java loop: for i in 0..size { add; if i>=max break; } — note the check is
    // AFTER adding, so it actually allows (max+1) matches. We replicate exactly.
    let max = limit.unwrap_or(i64::MAX);
    for (i, rm) in matches.iter().enumerate() {
        let mut m = Object::new();
        m.insert("match".to_string(), JValue::string(rm.text.clone()));
        m.insert("index".to_string(), JValue::number(rm.index as f64));
        m.insert(
            "groups".to_string(),
            JValue::array(rm.groups.clone(), ArrayFlags::default()),
        );
        result.push(JValue::object(m));
        if (i as i64) >= max {
            break;
        }
    }
    Ok(JValue::array(result, ArrayFlags::sequence()))
}

/// Walk the regexClosure linked list produced by applying a function pattern.
fn match_via_function(
    ev: &mut Evaluator,
    func: &JValue,
    str_arg: &JValue,
    limit: Option<i64>,
) -> JResult<JValue> {
    let mut result: Vec<JValue> = Vec::new();
    let max = limit.unwrap_or(i64::MAX);
    let mut closure = ev.func_apply(func, vec![str_arg.clone()])?;
    let mut count: i64 = 0;
    loop {
        if closure.is_undefined() {
            break;
        }
        let obj = match closure.as_object() {
            Some(o) => o.clone(),
            None => break,
        };
        let m_match = obj.get("match").cloned().unwrap_or(JValue::Undefined);
        let m_index = obj.get("index").cloned().unwrap_or(JValue::Undefined);
        let m_groups = obj.get("groups").cloned().unwrap_or(JValue::Undefined);

        let mut m = Object::new();
        m.insert("match".to_string(), m_match);
        m.insert("index".to_string(), m_index);
        m.insert("groups".to_string(), m_groups);
        result.push(JValue::object(m));

        if count >= max {
            break;
        }
        count += 1;

        // call next
        let next = match obj.get("next").cloned() {
            Some(n) if n.is_function() => n,
            _ => break,
        };
        closure = ev.func_apply(&next, vec![])?;
    }
    Ok(JValue::array(result, ArrayFlags::sequence()))
}

/// `$split(str, separator, limit?)`.
pub fn split(_ev: &mut Evaluator, args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let str = str_arg.as_str().unwrap_or("");

    let limit_v = crate::functions::arg(args, 2);
    let limit: Option<i64> = if limit_v.is_undefined() {
        None
    } else {
        let l = limit_v.as_f64().map(|d| d.trunc() as i64).unwrap_or(0);
        // Java: if (limit!=null && limit.intValue()<0) throw D3020 with str
        if l < 0 {
            return Err(JError::with_current("D3020", -1, str_arg.clone()));
        }
        Some(l)
    };

    // Java: if (limit==0) return empty list. Java returns a plain List (not a
    // sequence) from split (Arrays.asList), unlike match which uses createSequence.
    if let Some(0) = limit {
        return Ok(JValue::array(Vec::new(), ArrayFlags::default()));
    }

    let pattern = crate::functions::arg(args, 1);

    let mut pieces: Vec<String> = match &pattern {
        JValue::String(sep) => {
            if sep.is_empty() {
                // $split("str","") — split into characters (code points), up to limit
                let l = limit.unwrap_or(i64::MAX);
                let mut out = Vec::new();
                for (i, c) in str.chars().enumerate() {
                    if (i as i64) >= l {
                        break;
                    }
                    out.push(c.to_string());
                }
                out
            } else {
                split_literal(str, sep)
            }
        }
        JValue::Regex(re) => {
            let compiled = build_regex(re)?;
            split_regex(&compiled, str)?
        }
        f if f.is_function() => {
            // Apply function as a separator predicate? Java only supports
            // String/Pattern for split. A function pattern is not exercised by
            // the test suite; fall back to applying it and treating result as
            // a regexClosure walk is not meaningful for split, so error.
            let _ = f;
            return Err(JError::at("T0410", -1));
        }
        _ => return Err(JError::at("T0410", -1)),
    };

    // Java: if (limit!=null && limit<result.size()) result = result.subList(0, limit)
    if let Some(l) = limit {
        let l = l as usize;
        if l < pieces.len() {
            pieces.truncate(l);
        }
    }

    let arr: Vec<JValue> = pieces.into_iter().map(JValue::string).collect();
    Ok(JValue::array(arr, ArrayFlags::default()))
}

/// Split on a literal separator, preserving trailing empty strings (Java uses
/// `str.split(Pattern.quote(sep), -1)`).
fn split_literal(str: &str, sep: &str) -> Vec<String> {
    // split_inclusive-style with trailing-empty preservation:
    // Rust's str::split already keeps trailing empties for a non-empty sep.
    str.split(sep).map(|s| s.to_string()).collect()
}

/// Split on a regex, preserving trailing empty strings (Java
/// `Pattern.split(str, -1)`).
///
/// PORT-NOTE: Java `Pattern.split(input, -1)` removes a single leading empty
/// match only in the no-trailing-removal sense; the `-1` keeps trailing empty
/// strings. We replicate by iterating matches and slicing between them.
fn split_regex(re: &fancy_regex::Regex, str: &str) -> JResult<Vec<String>> {
    let mut out: Vec<String> = Vec::new();
    let mut last_end_byte = 0usize;
    let mut search_byte = 0usize;
    loop {
        if search_byte > str.len() {
            break;
        }
        let caps = match re.captures_from_pos(str, search_byte) {
            Ok(Some(c)) => c,
            Ok(None) => break,
            Err(e) => return Err(JError::at(&format!("Regex error: {}", e), -1)),
        };
        let m0 = caps.get(0).unwrap();
        let start_byte = m0.start();
        let end_byte = m0.end();

        // Java's split does not produce a leading empty piece from a zero-width
        // match at position 0; mirror Java semantics by skipping zero-width
        // matches at the very start. (Matches Java Pattern.split behaviour.)
        if start_byte == end_byte && start_byte == last_end_byte && start_byte == 0 {
            // advance one code point and continue without emitting
            let n = str[start_byte..].chars().next().map(|c| c.len_utf8());
            match n {
                Some(n) => {
                    search_byte = start_byte + n;
                    continue;
                }
                None => break,
            }
        }

        out.push(str[last_end_byte..start_byte].to_string());
        last_end_byte = end_byte;

        if end_byte > search_byte {
            search_byte = end_byte;
        } else {
            let n = str[start_byte..].chars().next().map(|c| c.len_utf8());
            match n {
                Some(n) => search_byte = start_byte + n,
                None => break,
            }
        }
    }
    // trailing remainder (preserve trailing empties => -1 behaviour)
    out.push(str[last_end_byte..].to_string());
    Ok(out)
}

/// `$replace(str, pattern, replacement, limit?)`.
///
/// PORT-NOTE: Java `replace` distinguishes string vs Pattern pattern and string
/// vs function replacement. For Pattern + String replacement it routes through
/// `safeReplaceAll`/`safeReplaceFirst` which (a) translate JSONata `$$`/`$N`
/// replacement syntax and (b) drop references to non-existent groups. For
/// Pattern + function replacement it calls the function with a
/// `{match, groups}` object per match.
pub fn replace(ev: &mut Evaluator, args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let str = str_arg.as_str().unwrap_or("").to_string();

    let pattern = crate::functions::arg(args, 1);
    let replacement = crate::functions::arg(args, 2);
    let limit_v = crate::functions::arg(args, 3);

    // Java: empty string pattern -> error (only checked for String patterns)
    if let JValue::String(p) = &pattern {
        if p.is_empty() {
            // Java: throw new JException("Second argument of replace function
            // cannot be an empty string", 0)
            return Err(JError::at(
                "Second argument of replace function cannot be an empty string",
                0,
            ));
        }
    }

    let limit: Option<i64> = if limit_v.is_undefined() {
        None
    } else {
        let l = limit_v.as_f64().map(|d| d.trunc() as i64).unwrap_or(0);
        if l < 0 {
            // Java: throw new JException("Fourth argument of replace function
            // must evaluate to a positive number", 0)
            return Err(JError::at(
                "Fourth argument of replace function must evaluate to a positive number",
                0,
            ));
        }
        Some(l)
    };

    match limit {
        None => {
            // replace all
            match &pattern {
                JValue::String(p) => {
                    // Java: str.replace(pattern, replacement) — literal, all occurrences
                    let rep = replacement.as_str().unwrap_or("");
                    Ok(JValue::string(str.replace(p.as_ref(), rep)))
                }
                JValue::Regex(re) => {
                    let compiled = build_regex(re)?;
                    let out = regex_replace_all(ev, &compiled, &str, &replacement, None)?;
                    Ok(JValue::string(out))
                }
                f if f.is_function() => {
                    // Function pattern: not a Java code path (pattern is Pattern
                    // or String). Treat as error.
                    let _ = f;
                    Err(JError::at("T0410", -1))
                }
                _ => Err(JError::at("T0410", -1)),
            }
        }
        Some(lim) => {
            // replace first `limit` occurrences
            match &pattern {
                JValue::String(p) => {
                    let rep = replacement.as_str().unwrap_or("");
                    let mut s = str;
                    for _ in 0..lim {
                        // Java uses str.replaceFirst(pattern, replacement) where
                        // pattern is a REGEX (String) — replaceFirst treats the
                        // first arg as a regex. Replicate literal-first replace?
                        // jsonata-java passes the raw String to replaceFirst, so
                        // it IS regex-interpreted. We mirror that.
                        match replace_first_literalish(&s, p, rep) {
                            Some(ns) => s = ns,
                            None => break,
                        }
                    }
                    Ok(JValue::string(s))
                }
                JValue::Regex(re) => {
                    let compiled = build_regex(re)?;
                    if replacement.is_function() {
                        // Java's limit loop casts the replacement to String and
                        // throws ClassCastException for functions (raw-crash
                        // class, not replicated) — keep the single-pass
                        // function-replacement behavior here.
                        let out = regex_replace_all(
                            ev,
                            &compiled,
                            &str,
                            &replacement,
                            Some(lim as usize),
                        )?;
                        return Ok(JValue::string(out));
                    }
                    // Java: `for (i < limit) str = safeReplaceFirst(str, ...)`
                    // — each iteration rescans the MODIFIED string from
                    // position 0, so replacement text can itself be re-matched
                    // ($replace('ab', /a/, 'aa', 2) -> 'aaab'). jsonata-js does
                    // a single left-to-right pass; see COMPAT.md.
                    let rep = replacement.as_str().unwrap_or("");
                    let mut s = str;
                    for _ in 0..lim {
                        match regex_replace_first(&compiled, &s, rep) {
                            Some(ns) => s = ns,
                            None => break,
                        }
                    }
                    Ok(JValue::string(s))
                }
                f if f.is_function() => {
                    let _ = f;
                    Err(JError::at("T0410", -1))
                }
                _ => Err(JError::at("T0410", -1)),
            }
        }
    }
}

/// Mirror of Java `str.replaceFirst(patternStr, replacement)` where the pattern
/// string is REGEX-interpreted (java.util.regex). Returns None if no match (so
/// the limit loop can stop early — Java would just leave the string unchanged,
/// which is equivalent).
///
/// PORT-NOTE: in the Java port, the string-pattern + limit path calls
/// `String.replaceFirst`, which compiles the pattern arg AS A REGEX and expands
/// `$N` group refs in the replacement. (This differs from the no-limit string
/// path, which uses literal `String.replace`.) We replicate that asymmetry.
fn replace_first_literalish(s: &str, pattern: &str, replacement: &str) -> Option<String> {
    let re = match fancy_regex::Regex::new(pattern) {
        Ok(r) => r,
        Err(_) => return None,
    };
    regex_replace_first(&re, s, replacement)
}

/// Replace the first match of `re` in `s`, expanding the replacement with
/// JSONata `$`-semantics (Java `safeReplaceFirst`). Returns None if no match.
fn regex_replace_first(re: &fancy_regex::Regex, s: &str, replacement: &str) -> Option<String> {
    match re.captures(s) {
        Ok(Some(caps)) => {
            let m = caps.get(0).unwrap();
            let mut out = String::new();
            out.push_str(&s[..m.start()]);
            // java.util.regex replaceFirst expands $0/$N in the replacement.
            expand_jsonata_replacement(&mut out, replacement, &caps);
            out.push_str(&s[m.end()..]);
            Some(out)
        }
        _ => None,
    }
}

/// Translate a JSONata replacement string into one expanded per-match.
///
/// JSONata replacement semantics (per Java `safeReplacement`): `$$` is a
/// literal `$`; `$N` (digit) is capture group N; `$<name>` would be a named
/// group; a lone `$` not followed by a digit/`<` is literal. We expand directly
/// against the captures here (rather than translating to java.util.regex
/// backslash syntax) so the engine is irrelevant.
fn expand_jsonata_replacement(out: &mut String, template: &str, caps: &fancy_regex::Captures) {
    let chars: Vec<char> = template.chars().collect();
    let n = chars.len();
    let mut i = 0;
    while i < n {
        let c = chars[i];
        if c == '\\' {
            // java.util.regex replacement semantics: backslash escapes the
            // next character, so "\\q" emits a literal 'q'. jsonata-js keeps
            // the backslash; see COMPAT.md. (A trailing lone backslash is an
            // IllegalArgumentException in Java — raw-crash class, kept literal.)
            if i + 1 < n {
                out.push(chars[i + 1]);
                i += 2;
            } else {
                out.push('\\');
                i += 1;
            }
            continue;
        }
        if c == '$' {
            // $$ -> literal $
            if i + 1 < n && chars[i + 1] == '$' {
                out.push('$');
                i += 2;
                continue;
            }
            // $<digit...> -> group N (multi-digit, greedy like java which uses
            // as many digits as form a valid group; java.util.regex consumes
            // digits while the resulting group index is valid). We consume one
            // or two digits, preferring the largest valid group.
            if i + 1 < n && chars[i + 1].is_ascii_digit() {
                // greedily read up to 2 digits
                let d1 = chars[i + 1].to_digit(10).unwrap() as usize;
                let mut consumed = 1;
                let mut group = d1;
                if i + 2 < n && chars[i + 2].is_ascii_digit() {
                    let two = d1 * 10 + chars[i + 2].to_digit(10).unwrap() as usize;
                    if two < caps.len() {
                        group = two;
                        consumed = 2;
                    }
                }
                if group < caps.len() {
                    if let Some(m) = caps.get(group) {
                        out.push_str(m.as_str());
                    }
                }
                // group out of range -> dropped (safeReplaceAll drops unknown groups)
                i += 1 + consumed;
                continue;
            }
            // lone $ (not $$ / $digit) -> literal $
            out.push('$');
            i += 1;
            continue;
        }
        out.push(c);
        i += 1;
    }
}

/// Regex replace (all, or first `limit`) with a string or function replacement.
fn regex_replace_all(
    ev: &mut Evaluator,
    re: &fancy_regex::Regex,
    str: &str,
    replacement: &JValue,
    limit: Option<usize>,
) -> JResult<String> {
    let is_fn = replacement.is_function();
    let rep_str = if is_fn {
        None
    } else {
        Some(replacement.as_str().unwrap_or("").to_string())
    };

    let mut out = String::new();
    let mut last_end = 0usize;
    let mut search_byte = 0usize;
    let mut replaced = 0usize;

    loop {
        if let Some(lim) = limit {
            if replaced >= lim {
                break;
            }
        }
        if search_byte > str.len() {
            break;
        }
        let caps = match re.captures_from_pos(str, search_byte) {
            Ok(Some(c)) => c,
            Ok(None) => break,
            Err(e) => return Err(JError::at(&format!("Regex error: {}", e), -1)),
        };
        let m0 = caps.get(0).unwrap();
        let start_byte = m0.start();
        let end_byte = m0.end();

        // copy text before the match
        out.push_str(&str[last_end..start_byte]);

        match &rep_str {
            Some(template) => {
                expand_jsonata_replacement(&mut out, template, &caps);
            }
            None => {
                // function replacement: build {match, groups} and apply
                let func = replacement;
                let mut obj = Object::new();
                obj.insert("match".to_string(), JValue::string(m0.as_str()));
                // Java toJsonataMatch: groups include group 0..groupCount
                let mut groups: Vec<JValue> = Vec::new();
                for g in 0..caps.len() {
                    match caps.get(g) {
                        Some(gm) => groups.push(JValue::string(gm.as_str())),
                        None => groups.push(JValue::Undefined),
                    }
                }
                obj.insert(
                    "groups".to_string(),
                    JValue::array(groups, ArrayFlags::default()),
                );
                let res = ev.func_apply(func, vec![JValue::object(obj)])?;
                // Java safeReplaceAllFn returns null for a non-String result,
                // and Matcher.replaceAll then throws (NPE) -> error. JSONata
                // surfaces this as D3012 "non-string replacement value".
                if let JValue::String(s) = res {
                    out.push_str(&s);
                } else {
                    return Err(JError::with_current("D3012", -1, res));
                }
            }
        }

        last_end = end_byte;
        replaced += 1;

        if end_byte > search_byte {
            search_byte = end_byte;
        } else {
            // zero-width: emit one cp and advance
            let nc = str[start_byte..].chars().next();
            match nc {
                Some(c) => {
                    let cl = c.len_utf8();
                    // copy the skipped char so we don't drop it
                    // (it lies between last_end and next search position)
                    // Actually last_end == end_byte == start_byte here.
                    out.push(c);
                    last_end = start_byte + cl;
                    search_byte = start_byte + cl;
                }
                None => break,
            }
        }
    }
    out.push_str(&str[last_end..]);
    Ok(out)
}

// ---------------------------------------------------------------------------
// $join
// ---------------------------------------------------------------------------

/// `$join(strs, separator?)`.
pub fn join(args: &[JValue]) -> JResult<JValue> {
    let strs_arg = crate::functions::arg(args, 0);
    if strs_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }

    let sep_v = crate::functions::arg(args, 1);
    let sep = sep_v.as_str().unwrap_or("");

    // The signature coerces a singleton string to an array; handle both.
    let parts: Vec<String> = match &strs_arg {
        JValue::Array(a, _) => a
            .iter()
            .map(|v| v.as_str().unwrap_or("").to_string())
            .collect(),
        JValue::String(s) => vec![s.to_string()],
        _ => vec![],
    };
    Ok(JValue::string(parts.join(sep)))
}

// ---------------------------------------------------------------------------
// base64
// ---------------------------------------------------------------------------

const B64_ALPHABET: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

/// `$base64encode(str)` — UTF-8 bytes, standard Base64 with padding (matches
/// `java.util.Base64.getEncoder()`).
pub fn base64encode(args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let bytes = str_arg.as_str().unwrap_or("").as_bytes();
    let mut out = String::with_capacity((bytes.len() + 2) / 3 * 4);
    for chunk in bytes.chunks(3) {
        let b0 = chunk[0] as u32;
        let b1 = if chunk.len() > 1 { chunk[1] as u32 } else { 0 };
        let b2 = if chunk.len() > 2 { chunk[2] as u32 } else { 0 };
        let n = (b0 << 16) | (b1 << 8) | b2;
        out.push(B64_ALPHABET[((n >> 18) & 0x3F) as usize] as char);
        out.push(B64_ALPHABET[((n >> 12) & 0x3F) as usize] as char);
        if chunk.len() > 1 {
            out.push(B64_ALPHABET[((n >> 6) & 0x3F) as usize] as char);
        } else {
            out.push('=');
        }
        if chunk.len() > 2 {
            out.push(B64_ALPHABET[(n & 0x3F) as usize] as char);
        } else {
            out.push('=');
        }
    }
    Ok(JValue::string(out))
}

/// `$base64decode(str)` — standard Base64 -> UTF-8 string (matches
/// `java.util.Base64.getDecoder()`).
///
/// PORT-NOTE: Java's decoder is lenient about a missing final pad but strict
/// about illegal chars (throws). We skip ASCII whitespace and stop cleanly,
/// mirroring observable behaviour for the test inputs.
pub fn base64decode(args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let input = str_arg.as_str().unwrap_or("");

    fn dec(c: u8) -> Option<u32> {
        match c {
            b'A'..=b'Z' => Some((c - b'A') as u32),
            b'a'..=b'z' => Some((c - b'a' + 26) as u32),
            b'0'..=b'9' => Some((c - b'0' + 52) as u32),
            b'+' => Some(62),
            b'/' => Some(63),
            _ => None,
        }
    }

    let mut bytes = Vec::new();
    let mut buf = 0u32;
    let mut bits = 0u32;
    for &c in input.as_bytes() {
        if c == b'=' {
            break;
        }
        let v = match dec(c) {
            Some(v) => v,
            None => continue, // skip whitespace / non-alphabet
        };
        buf = (buf << 6) | v;
        bits += 6;
        if bits >= 8 {
            bits -= 8;
            bytes.push(((buf >> bits) & 0xFF) as u8);
        }
    }
    // Java decodes as UTF-8; lossily convert (Java would throw on invalid UTF-8
    // only at String construction — but jsonata test inputs are valid UTF-8).
    Ok(JValue::string(String::from_utf8_lossy(&bytes).into_owned()))
}

// ---------------------------------------------------------------------------
// URL encode / decode
// ---------------------------------------------------------------------------

/// `Utils.checkUrl` — throws on consecutive high surrogates or a trailing high
/// surrogate (malformed UTF-16). In Rust strings are valid UTF-8 (no lone
/// surrogates can exist), so this can never trigger for a `JValue::String`.
/// Retained as a no-op for fidelity.
///
/// PORT-NOTE: Java's check guards against malformed UTF-16 in the input string.
/// Rust `&str` cannot contain unpaired surrogates, so the D-error path is
/// unreachable here. (jsonata-js raises an error for malformed URI surrogates;
/// not reproducible with valid UTF-8 input.)
fn check_url(_str: &str) -> JResult<()> {
    Ok(())
}

/// Percent-encode the UTF-8 bytes of `s`, leaving `unreserved` ASCII bytes
/// untouched. Predicate receives the byte and returns true if it should be
/// emitted verbatim.
fn percent_encode(s: &str, keep: impl Fn(u8) -> bool) -> String {
    let mut out = String::new();
    for &b in s.as_bytes() {
        if keep(b) {
            out.push(b as char);
        } else {
            out.push('%');
            out.push_str(&format!("{:02X}", b));
        }
    }
    out
}

/// `$encodeUrlComponent(str)` — mirrors JS `encodeURIComponent`.
///
/// Unreserved per MDN: A-Z a-z 0-9 - _ . ! ~ * ' ( )
pub fn encode_url_component(args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let s = str_arg.as_str().unwrap_or("");
    check_url(s)?;
    let out = percent_encode(s, |b| {
        b.is_ascii_alphanumeric()
            || matches!(
                b,
                b'-' | b'_' | b'.' | b'!' | b'~' | b'*' | b'\'' | b'(' | b')'
            )
    });
    Ok(JValue::string(out))
}

/// `$encodeUrl(str)` — mirrors JS `encodeURI`.
///
/// Unreserved per MDN: A-Z a-z 0-9 ; , / ? : @ & = + $ - _ . ! ~ * ' ( ) #
///
/// PORT-NOTE: jsonata-java's `encodeUrl` does extra URL-parsing (only encodes
/// the query part if the input parses as a `java.net.URL`), but for non-URL
/// inputs falls back to `URLEncoder.encode` which over-escapes (e.g. turns `/`
/// into `%2F`). The JS `encodeURI` semantics are what the JSONata spec wants
/// and what the test suite checks, so we implement `encodeURI` directly.
pub fn encode_url(args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let s = str_arg.as_str().unwrap_or("");
    check_url(s)?;
    let out = percent_encode(s, |b| {
        b.is_ascii_alphanumeric()
            || matches!(
                b,
                b';' | b','
                    | b'/'
                    | b'?'
                    | b':'
                    | b'@'
                    | b'&'
                    | b'='
                    | b'+'
                    | b'$'
                    | b'-'
                    | b'_'
                    | b'.'
                    | b'!'
                    | b'~'
                    | b'*'
                    | b'\''
                    | b'('
                    | b')'
                    | b'#'
            )
    });
    Ok(JValue::string(out))
}

/// Percent-decode `s` (UTF-8). `plus_as_space` controls whether `+` decodes to
/// a space (Java `URLDecoder` does this; JS `decodeURIComponent` does NOT).
///
/// PORT-NOTE: jsonata-java uses `java.net.URLDecoder.decode(str, UTF_8)`, which
/// treats `+` as a space and is otherwise standard percent-decoding. We match
/// that (`plus_as_space = true`).
/// Returns `None` on a malformed escape or invalid UTF-8 result (Java
/// URLDecoder / JS decodeURIComponent throw -> JSONata D3140).
fn percent_decode(s: &str, plus_as_space: bool) -> Option<String> {
    let bytes = s.as_bytes();
    let mut out: Vec<u8> = Vec::with_capacity(bytes.len());
    let mut i = 0;
    while i < bytes.len() {
        let b = bytes[i];
        if b == b'%' {
            // need two following hex digits
            let h1 = bytes.get(i + 1).and_then(|c| (*c as char).to_digit(16));
            let h2 = bytes.get(i + 2).and_then(|c| (*c as char).to_digit(16));
            if let (Some(h1), Some(h2)) = (h1, h2) {
                out.push(((h1 << 4) | h2) as u8);
                i += 3;
                continue;
            }
            // malformed escape sequence -> error
            return None;
        } else if b == b'+' && plus_as_space {
            out.push(b' ');
            i += 1;
        } else {
            out.push(b);
            i += 1;
        }
    }
    // invalid UTF-8 in the decoded bytes -> error (JS decodeURIComponent throws)
    String::from_utf8(out).ok()
}

/// `$decodeUrlComponent(str)`.
pub fn decode_url_component(args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let s = str_arg.as_str().unwrap_or("");
    // Java uses URLDecoder which decodes '+' as space.
    match percent_decode(s, true) {
        Some(d) => Ok(JValue::string(d)),
        None => Err(JError::with_current("D3140", -1, JValue::string(s))),
    }
}

/// `$decodeUrl(str)`.
pub fn decode_url(args: &[JValue]) -> JResult<JValue> {
    let str_arg = crate::functions::arg(args, 0);
    if str_arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let s = str_arg.as_str().unwrap_or("");
    match percent_decode(s, true) {
        Some(d) => Ok(JValue::string(d)),
        None => Err(JError::with_current("D3140", -1, JValue::string(s))),
    }
}

// ---------------------------------------------------------------------------
// regex_closure — used when a /regex/ literal is invoked as a function
// ---------------------------------------------------------------------------

/// Port of `Jsonata.regexClosure(Matcher)`. Matches `re` against `s` starting
/// at code-point offset `from`; returns a `{match, index, groups, next}`
/// object, or `Undefined` if there is no further match.
///
/// `index` is the CODE-POINT offset of the match start. `next` is a native
/// closure that, when applied, re-matches from just past this match.
pub fn regex_closure(re: &Rc<JRegex>, s: &str, from: usize) -> JValue {
    let compiled = match build_regex(re) {
        Ok(c) => c,
        Err(_) => return JValue::Undefined,
    };

    let from_byte = cp_index_to_byte(s, from);
    if from_byte > s.len() {
        return JValue::Undefined;
    }

    let caps = match compiled.captures_from_pos(s, from_byte) {
        Ok(Some(c)) => c,
        _ => return JValue::Undefined,
    };
    let m0 = caps.get(0).unwrap();
    let start_byte = m0.start();
    let end_byte = m0.end();

    let match_text = m0.as_str().to_string();
    let start_cp = cp_len(&s[..start_byte]);
    let end_cp = cp_len(&s[..end_byte]);

    // jsonata-java `Jsonata.regexClosure` stores `List.of(group)` (just the
    // full match) under "groups", and uses keys match/start/end/groups/next.
    let groups: Vec<JValue> = vec![JValue::string(match_text.clone())];

    // next: re-match from just past this match (code-point index). Mirror the
    // zero-width bump so iteration terminates.
    let next_byte = if end_byte > start_byte {
        end_byte
    } else {
        end_byte
            + s[end_byte..]
                .chars()
                .next()
                .map(|c| c.len_utf8())
                .unwrap_or(0)
    };
    let next_from = cp_len(&s[..next_byte.min(s.len())]);

    let re_for_next = re.clone();
    let s_for_next = s.to_string();
    let next_fn = JValue::Native(Rc::new(NativeFn {
        name: String::new(),
        signature: None,
        implementation: NativeImpl::Closure(Rc::new(move |_args: &[JValue]| {
            Ok(regex_closure(&re_for_next, &s_for_next, next_from))
        })),
    }));

    let mut obj = Object::new();
    obj.insert("match".to_string(), JValue::string(match_text));
    obj.insert("start".to_string(), JValue::number(start_cp as f64));
    obj.insert("end".to_string(), JValue::number(end_cp as f64));
    obj.insert(
        "groups".to_string(),
        JValue::array(groups, ArrayFlags::default()),
    );
    obj.insert("next".to_string(), next_fn);
    JValue::object(obj)
}

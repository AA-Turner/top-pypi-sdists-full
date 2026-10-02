//! Array / object built-ins (task #7).

use crate::error::JResult;
use crate::functions::{append, lookup};
use crate::value::{ArrayFlags, JValue, Object};

// ---------------------------------------------------------------------------
// reverse
// ---------------------------------------------------------------------------

/// `Functions.reverse(arr)`.
pub fn reverse(args: &[JValue]) -> JResult<JValue> {
    let arr = crate::functions::arg(args, 0);
    // undefined inputs always return undefined
    if arr.is_undefined() {
        return Ok(JValue::Undefined);
    }
    match &arr {
        JValue::Array(a, _) => {
            // arr.size() <= 1 -> return arr (preserve original, incl. flags)
            if a.len() <= 1 {
                return Ok(arr.clone());
            }
            let mut result = (**a).clone();
            result.reverse();
            // Java: new ArrayList<>(arr) — a plain list; JList-ness and all
            // sequence flags are dropped (observable via $distinct($reverse(..))).
            Ok(JValue::array(result, ArrayFlags::default()))
        }
        // Non-array (signature `a` coerces singletons to arrays, but guard anyway):
        // Java would ClassCastException; we never reach here for valid input.
        other => Ok(other.clone()),
    }
}

// ---------------------------------------------------------------------------
// shuffle
// ---------------------------------------------------------------------------

/// `Functions.shuffle(arr)`.
pub fn shuffle(args: &[JValue]) -> JResult<JValue> {
    let arr = crate::functions::arg(args, 0);
    // undefined inputs always return undefined
    if arr.is_undefined() {
        return Ok(JValue::Undefined);
    }
    match &arr {
        JValue::Array(a, _flags) => {
            // arr.size() <= 1 -> return arr
            if a.len() <= 1 {
                return Ok(arr.clone());
            }
            let mut result = (**a).clone();
            // Fisher-Yates with a simple xorshift PRNG seeded from the clock.
            // Determinism is not tested; we only need a valid permutation.
            let mut state: u64 = {
                use std::time::{SystemTime, UNIX_EPOCH};
                let nanos = SystemTime::now()
                    .duration_since(UNIX_EPOCH)
                    .map(|d| d.as_nanos() as u64)
                    .unwrap_or(0x9E3779B97F4A7C15);
                // ensure non-zero seed (xorshift requires non-zero state)
                nanos ^ 0x9E3779B97F4A7C15
            };
            let mut next = || {
                // xorshift64
                state ^= state << 13;
                state ^= state >> 7;
                state ^= state << 17;
                state
            };
            let len = result.len();
            for i in (1..len).rev() {
                let j = (next() % ((i as u64) + 1)) as usize;
                result.swap(i, j);
            }
            Ok(JValue::array(result, ArrayFlags::default()))
        }
        other => Ok(other.clone()),
    }
}

// ---------------------------------------------------------------------------
// distinct
// ---------------------------------------------------------------------------

/// `Functions.distinct(_arr)`.
pub fn distinct(args: &[JValue]) -> JResult<JValue> {
    let arr = crate::functions::arg(args, 0);
    // undefined inputs always return undefined
    if arr.is_undefined() {
        return Ok(JValue::Undefined);
    }
    // Non-array, or array of size <= 1: return as-is.
    match &arr {
        JValue::Array(a, flags) => {
            if a.len() <= 1 {
                return Ok(arr.clone());
            }
            // Java: `(arr instanceof JList) ? Utils.createSequence() : new
            // ArrayList<>()` — a sequence iff the input is a JList (any kind),
            // which makes a singleton result unwrap: $distinct([1,1]) -> 1.
            // jsonata-js returns [1] here; see COMPAT.md.
            let result_flags = if flags.is_jlist() {
                ArrayFlags::sequence()
            } else {
                ArrayFlags::default()
            };
            // LinkedHashSet semantics: dedup preserving first-occurrence order,
            // using value equality (JValue: PartialEq).
            let mut result: Vec<JValue> = Vec::with_capacity(a.len());
            for el in a.iter() {
                if !result.iter().any(|existing| existing == el) {
                    result.push(el.clone());
                }
            }
            Ok(JValue::array(result, result_flags))
        }
        _ => Ok(arr.clone()),
    }
}

// ---------------------------------------------------------------------------
// zip
// ---------------------------------------------------------------------------

/// `Functions.zip(args)` — `<a+>` variadic.
///
/// Each positional arg is an array (the `a` signature coerces singletons to
/// 1-element arrays). A `null`/undefined arg forces length 0 (Java sets
/// `length = 0` and stops counting at the first null).
pub fn zip(args: &[JValue]) -> JResult<JValue> {
    // length of the shortest array; nargs = number of leading non-null args.
    let mut length = usize::MAX;
    let mut nargs = 0usize;
    while nargs < args.len() {
        match &args[nargs] {
            JValue::Array(a, _) => {
                length = length.min(a.len());
                nargs += 1;
            }
            // Java: args.get(nargs)==null -> length = 0; break;
            // undefined arg breaks the loop with length 0.
            v if v.is_undefined() => {
                length = 0;
                break;
            }
            // A non-array, non-undefined arg: under the `a` signature this
            // cannot occur (singletons are wrapped). Treat as length-1 array
            // to stay defensive without diverging from observable behavior.
            _ => {
                length = length.min(1);
                nargs += 1;
            }
        }
    }
    if length == usize::MAX {
        // no args at all -> Java's loop body never ran; length stays MAX, but
        // the for-loop `i < length` would iterate forever. In practice zip is
        // always called with >=1 arg; with zero args produce an empty array.
        length = 0;
    }

    let mut result: Vec<JValue> = Vec::with_capacity(length);
    for i in 0..length {
        let mut tuple: Vec<JValue> = Vec::with_capacity(nargs);
        for k in 0..nargs {
            // args[k] is guaranteed to be an array here.
            if let JValue::Array(a, _) = &args[k] {
                tuple.push(a[i].clone());
            } else {
                tuple.push(args[k].clone());
            }
        }
        result.push(JValue::array(tuple, ArrayFlags::default()));
    }
    Ok(JValue::array(result, ArrayFlags::default()))
}

// ---------------------------------------------------------------------------
// keys
// ---------------------------------------------------------------------------

/// `Functions.keys(arg)` — `$keys`.
pub fn keys(args: &[JValue]) -> JResult<JValue> {
    let arg = crate::functions::arg(args, 0);
    // Java builds a sequence; for undefined input the dispatch still produces
    // an empty sequence (Java does not early-return on null here), but JSONata
    // treats an empty sequence as undefined. Match Java: no null guard.
    let mut result: Vec<JValue> = Vec::new();
    collect_keys(&arg, &mut result);
    Ok(JValue::array(result, ArrayFlags::sequence()))
}

/// Recursively collect keys, deduping by string value and preserving the order
/// of first occurrence (mirrors Java's LinkedHashSet union over array items).
fn collect_keys(arg: &JValue, out: &mut Vec<JValue>) {
    match arg {
        JValue::Array(a, _) => {
            for el in a.iter() {
                collect_keys_dedup(el, out);
            }
        }
        JValue::Object(o) => {
            for k in o.keys() {
                push_key_dedup(out, k);
            }
        }
        _ => {}
    }
}

/// For array elements, Java merges each element's keys into a LinkedHashSet.
/// `keys(el)` itself returns a sequence; addAll preserves order and dedups.
fn collect_keys_dedup(el: &JValue, out: &mut Vec<JValue>) {
    match el {
        JValue::Object(o) => {
            for k in o.keys() {
                push_key_dedup(out, k);
            }
        }
        JValue::Array(a, _) => {
            for inner in a.iter() {
                collect_keys_dedup(inner, out);
            }
        }
        _ => {}
    }
}

fn push_key_dedup(out: &mut Vec<JValue>, key: &str) {
    let already = out.iter().any(|v| v.as_str() == Some(key));
    if !already {
        out.push(JValue::string(key));
    }
}

// ---------------------------------------------------------------------------
// lookup
// ---------------------------------------------------------------------------

/// `Functions.lookup(input, key)` — `$lookup(obj, key)`.
pub fn lookup_fn(args: &[JValue]) -> JResult<JValue> {
    let input = crate::functions::arg(args, 0);
    let key = crate::functions::arg(args, 1);
    // Java signature is `lookup(Object input, String key)`. The key arg is a
    // string; convert via as_str (undefined key -> empty match -> undefined).
    let key_str = match key.as_str() {
        Some(s) => s.to_string(),
        None => return Ok(JValue::Undefined),
    };
    Ok(lookup(&input, &key_str))
}

// ---------------------------------------------------------------------------
// spread
// ---------------------------------------------------------------------------

/// `Functions.spread(arg)` — `$spread`.
pub fn spread(args: &[JValue]) -> JResult<JValue> {
    let arg = crate::functions::arg(args, 0);
    Ok(spread_value(&arg))
}

fn spread_value(arg: &JValue) -> JValue {
    match arg {
        JValue::Array(a, _) => {
            // spread all of the items in the array, appending results
            let mut result = JValue::empty_sequence();
            for item in a.iter() {
                result = append(result, spread_value(item));
            }
            result
        }
        JValue::Object(o) => {
            // one single-key object per entry, preserving insertion order
            let mut result: Vec<JValue> = Vec::with_capacity(o.len());
            for (k, v) in o.iter() {
                let mut obj = Object::new();
                obj.insert(k.clone(), v.clone());
                result.push(JValue::object(obj));
            }
            JValue::array(result, ArrayFlags::sequence())
        }
        // not a list or map (incl. undefined): return arg as-is
        other => other.clone(),
    }
}

// ---------------------------------------------------------------------------
// merge
// ---------------------------------------------------------------------------

/// `Functions.merge(arg)` — `$merge`.
pub fn merge(args: &[JValue]) -> JResult<JValue> {
    let arg = crate::functions::arg(args, 0);
    // undefined inputs always return undefined
    if arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let mut result = Object::new();
    // Java iterates `List arg`; the `a` signature coerces a single object to a
    // 1-element array, so arg is an array of objects here.
    match &arg {
        JValue::Array(a, _) => {
            for obj in a.iter() {
                if let JValue::Object(o) = obj {
                    for (k, v) in o.iter() {
                        // later keys win; IndexMap.insert keeps the position of
                        // an existing key but updates its value — matching Java
                        // LinkedHashMap.put semantics.
                        result.insert(k.clone(), v.clone());
                    }
                }
            }
        }
        // Defensive: a lone object (should have been wrapped by signature).
        JValue::Object(o) => {
            for (k, v) in o.iter() {
                result.insert(k.clone(), v.clone());
            }
        }
        _ => {}
    }
    Ok(JValue::object(result))
}

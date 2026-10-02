//! Built-in functions (`com.dashjoin.jsonata.Functions`).
//!
//! `mod.rs` holds the helpers the evaluator depends on directly (string
//! serialization / number formatting, `toBoolean`, `append`, `lookup`,
//! `validateInput`, `functionClone`, null conversion) plus the `call_builtin`
//! dispatch table. The individual built-ins live in the submodules.

pub mod collections;
pub mod hof;
pub mod misc;
pub mod numeric;
pub mod strings;

use crate::error::{JError, JResult};
use crate::evaluator::Evaluator;
use crate::value::{ArrayFlags, JRegex, JValue, Object};
use std::rc::Rc;

// ---------------------------------------------------------------------------
// Number formatting
// ---------------------------------------------------------------------------

/// Java `String.valueOf(double)` style used in error-message inserts and
/// `"" + number`. Mirrors the integral / `BigDecimal(15)` split.
pub fn number_to_java_string(n: f64) -> String {
    // Java Double.toString for non-finite values (used in error inserts).
    if n.is_nan() {
        return "NaN".to_string();
    }
    if n.is_infinite() {
        return if n > 0.0 { "Infinity" } else { "-Infinity" }.to_string();
    }
    number_to_string(n)
}

/// Port of the number branch of `Functions.string`:
/// integral doubles in long range render without a decimal point; otherwise
/// `new BigDecimal(d, MathContext(15)).stripTrailingZeros().toString()` with
/// `E+`/`E-` lowercased.
pub fn number_to_string(d: f64) -> String {
    if !d.is_finite() {
        // Should not occur (guarded earlier), but be safe.
        return format!("{}", d);
    }
    // integral and within long range -> Math.round(d)
    if d % 1.0 == 0.0 && (i64::MIN as f64) < d && d <= (i64::MAX as f64) {
        return format!("{}", d as i64);
    }
    big_decimal_15(d)
}

/// Replicates `new BigDecimal(d, new MathContext(15)).stripTrailingZeros().toString()`
/// then `E+`->`e+`, `E-`->`e-`.
fn big_decimal_15(d: f64) -> String {
    let negative = d < 0.0;
    let abs = d.abs();
    // 15 significant digits in scientific form: "x.xxxxxxxxxxxxxxe±YY"
    let sci = format!("{:.*e}", 14, abs);
    // parse mantissa and exponent
    let (mantissa, exp_str) = sci.split_once('e').unwrap();
    let exp: i32 = exp_str.parse().unwrap();
    // mantissa like "3.33333333333333" (one digit, '.', 14 digits)
    let digits: String = mantissa.chars().filter(|c| *c != '.').collect();
    // value = digits * 10^(exp - 14)   (digits has 15 chars)
    // BigDecimal coeff = digits, scale = 14 - exp
    let mut coeff: Vec<u8> = digits.into_bytes();
    let mut scale: i32 = 14 - exp;

    // stripTrailingZeros
    while coeff.len() > 1 && *coeff.last().unwrap() == b'0' {
        coeff.pop();
        scale -= 1;
    }
    // if it stripped down to "0"
    if coeff == b"0" {
        return "0".to_string();
    }

    let coeff_str = String::from_utf8(coeff).unwrap();
    let len = coeff_str.len() as i32;
    let adjusted_exp = (len - 1) - scale;

    let body = if scale >= 0 && adjusted_exp >= -6 {
        // plain notation
        if scale == 0 {
            coeff_str
        } else if (len - scale) > 0 {
            // decimal point inside
            let point = (len - scale) as usize;
            format!("{}.{}", &coeff_str[..point], &coeff_str[point..])
        } else {
            // 0.00...digits
            let zeros = "0".repeat((scale - len) as usize);
            format!("0.{}{}", zeros, coeff_str)
        }
    } else {
        // scientific notation: d.ddddE±exp
        let mantissa = if len > 1 {
            format!("{}.{}", &coeff_str[..1], &coeff_str[1..])
        } else {
            coeff_str
        };
        let sign = if adjusted_exp >= 0 { "+" } else { "-" };
        format!("{}e{}{}", mantissa, sign, adjusted_exp.abs())
    };
    if negative {
        format!("-{}", body)
    } else {
        body
    }
}

// ---------------------------------------------------------------------------
// string (serializer) — Functions.string
// ---------------------------------------------------------------------------

/// `Functions.string(arg, prettify)`. Returns the rendered string; the
/// `$string` builtin wraps undefined handling differently.
pub fn string(arg: &JValue, prettify: bool) -> JResult<String> {
    // unwrap outer wrapper
    let arg = match arg {
        JValue::Array(a, f) if f.outer_wrapper && !a.is_empty() => a[0].clone(),
        other => other.clone(),
    };
    if arg.is_string() {
        return Ok(arg.as_str().unwrap().to_string());
    }
    let mut sb = String::new();
    string_into(&mut sb, &arg, prettify, "")?;
    Ok(sb)
}

fn string_into(b: &mut String, arg: &JValue, prettify: bool, indent: &str) -> JResult<()> {
    match arg {
        JValue::Undefined | JValue::Null => {
            b.push_str("null");
        }
        JValue::Lambda(_) | JValue::Native(_) | JValue::Partial(_) | JValue::Regex(_) => {
            // functions render to nothing
        }
        JValue::Number(n) => {
            // Java would hit an unchecked NumberFormatException in BigDecimal;
            // raise the catalog error for stringifying a non-finite number.
            if !n.is_finite() {
                return Err(JError::with_current("D3001", -1, JValue::Number(*n)));
            }
            b.push_str(&number_to_string(*n));
        }
        JValue::Bool(bool_) => {
            b.push_str(if *bool_ { "true" } else { "false" });
        }
        JValue::String(s) => {
            crate::json::quote(s, b);
        }
        JValue::Object(o) => {
            b.push('{');
            if prettify {
                b.push('\n');
            }
            let inner_indent = format!("{}  ", indent);
            let mut first = true;
            for (k, v) in o.iter() {
                if !first {
                    b.push(',');
                    if prettify {
                        b.push('\n');
                    }
                }
                first = false;
                if prettify {
                    b.push_str(indent);
                    b.push_str("  ");
                }
                b.push('"');
                crate::json::quote(k, b);
                b.push('"');
                b.push(':');
                if prettify {
                    b.push(' ');
                }
                let is_quoted = matches!(
                    v,
                    JValue::String(_)
                        | JValue::Lambda(_)
                        | JValue::Native(_)
                        | JValue::Partial(_)
                        | JValue::Regex(_)
                );
                if is_quoted {
                    b.push('"');
                    string_into(b, v, prettify, &inner_indent)?;
                    b.push('"');
                } else {
                    string_into(b, v, prettify, &inner_indent)?;
                }
            }
            if prettify && !o.is_empty() {
                b.push('\n');
                b.push_str(indent);
            }
            b.push('}');
        }
        JValue::Array(a, _) => {
            if a.is_empty() {
                b.push_str("[]");
                return Ok(());
            }
            b.push('[');
            if prettify {
                b.push('\n');
            }
            let inner_indent = format!("{}  ", indent);
            let mut first = true;
            for v in a.iter() {
                if !first {
                    b.push(',');
                    if prettify {
                        b.push('\n');
                    }
                }
                first = false;
                if prettify {
                    b.push_str(indent);
                    b.push_str("  ");
                }
                let is_quoted = matches!(
                    v,
                    JValue::String(_)
                        | JValue::Lambda(_)
                        | JValue::Native(_)
                        | JValue::Partial(_)
                        | JValue::Regex(_)
                );
                if is_quoted {
                    b.push('"');
                    string_into(b, v, prettify, &inner_indent)?;
                    b.push('"');
                } else {
                    string_into(b, v, prettify, &inner_indent)?;
                }
            }
            if prettify {
                b.push('\n');
                b.push_str(indent);
            }
            b.push(']');
        }
    }
    Ok(())
}

// ---------------------------------------------------------------------------
// toBoolean / boolize
// ---------------------------------------------------------------------------

/// `Functions.toBoolean` — returns None for undefined input.
pub fn to_boolean(arg: &JValue) -> Option<bool> {
    match arg {
        JValue::Undefined => None,
        JValue::Array(a, _) => {
            if a.len() == 1 {
                Some(to_boolean(&a[0]) == Some(true))
            } else if a.len() > 1 {
                Some(a.iter().any(boolize))
            } else {
                Some(false)
            }
        }
        JValue::String(s) => Some(!s.is_empty()),
        JValue::Number(n) => Some(*n != 0.0),
        JValue::Object(o) => Some(!o.is_empty()),
        JValue::Bool(b) => Some(*b),
        _ => Some(false),
    }
}

/// `Jsonata.boolize` — toBoolean with null coerced to false.
pub fn boolize(value: &JValue) -> bool {
    to_boolean(value).unwrap_or(false)
}

// ---------------------------------------------------------------------------
// append / lookup
// ---------------------------------------------------------------------------

/// `Functions.append(arg1, arg2)`.
pub fn append(arg1: JValue, arg2: JValue) -> JValue {
    if arg1.is_undefined() {
        return arg2;
    }
    if arg2.is_undefined() {
        return arg1;
    }
    let a1: Vec<JValue> = match &arg1 {
        JValue::Array(a, _) => (**a).clone(),
        other => vec![other.clone()],
    };
    let a2: Vec<JValue> = match &arg2 {
        JValue::Array(a, _) => (**a).clone(),
        other => vec![other.clone()],
    };
    let mut result = a1;
    result.extend(a2);
    // Java: arg1 = new JList<>((List)arg1) — the result is always a JList
    // (class identity matters to e.g. $distinct), with no semantic flags.
    JValue::array(result, ArrayFlags::jlist())
}

/// `Functions.lookup(input, key)`.
pub fn lookup(input: &JValue, key: &str) -> JValue {
    match input {
        JValue::Array(a, _) => {
            let mut result: Vec<JValue> = Vec::new();
            for item in a.iter() {
                let res = lookup(item, key);
                if !res.is_undefined() {
                    if let JValue::Array(ra, _) = &res {
                        result.extend(ra.iter().cloned());
                    } else {
                        result.push(res);
                    }
                }
            }
            JValue::array(result, ArrayFlags::sequence())
        }
        JValue::Object(o) => o.get(key).cloned().unwrap_or(JValue::Undefined),
        _ => JValue::Undefined,
    }
}

// ---------------------------------------------------------------------------
// validateInput / convertNulls / functionClone
// ---------------------------------------------------------------------------

/// `Functions.validateInput`.
pub fn validate_input(arg: &JValue) -> JResult<()> {
    match arg {
        JValue::Undefined
        | JValue::Null
        | JValue::Number(_)
        | JValue::Bool(_)
        | JValue::String(_)
        | JValue::Lambda(_)
        | JValue::Native(_)
        | JValue::Partial(_)
        | JValue::Regex(_) => Ok(()),
        JValue::Object(o) => {
            for (_k, v) in o.iter() {
                validate_input(v)?;
            }
            Ok(())
        }
        JValue::Array(a, _) => {
            for v in a.iter() {
                validate_input(v)?;
            }
            Ok(())
        }
    }
}

/// `Utils.convertNulls` — convert `Null` (NULL_VALUE) to `Undefined` for the
/// output of `evaluate` when `outputConvertNulls` is on. We recurse into
/// arrays/objects in place.
pub fn convert_nulls(v: JValue) -> JValue {
    match v {
        JValue::Null => JValue::Undefined,
        JValue::Array(a, f) => {
            let new: Vec<JValue> = a.iter().cloned().map(convert_nulls).collect();
            JValue::Array(Rc::new(new), f)
        }
        JValue::Object(o) => {
            let mut new = Object::new();
            for (k, val) in o.iter() {
                new.insert(k.clone(), convert_nulls(val.clone()));
            }
            JValue::object(new)
        }
        other => other,
    }
}

/// `Functions.functionClone` — deep copy via JSON round-trip.
pub fn function_clone(arg: &JValue) -> JValue {
    if arg.is_undefined() {
        return JValue::Undefined;
    }
    match string(arg, false) {
        Ok(s) => crate::json::parse_json(&s).unwrap_or(JValue::Undefined),
        Err(_) => JValue::Undefined,
    }
}

// ---------------------------------------------------------------------------
// regex closure (used by apply when a Regex is invoked as a function)
// ---------------------------------------------------------------------------

/// Build the `{match, index, groups}` closure object for a regex match against
/// `s` starting at `from` (char index). Returns Undefined when no match.
pub fn regex_match_closure(_re: &Rc<JRegex>, _s: &str, _from: usize) -> JValue {
    // Implemented in strings.rs regex support; placeholder until ported.
    crate::functions::strings::regex_closure(_re, _s, _from)
}

// ---------------------------------------------------------------------------
// type helper (shared)
// ---------------------------------------------------------------------------

/// `Functions.type` value — JSONata type name.
pub fn type_of(v: &JValue) -> Option<&'static str> {
    match v {
        JValue::Undefined => None,
        JValue::Null => Some("null"),
        JValue::Number(_) => Some("number"),
        JValue::String(_) => Some("string"),
        JValue::Bool(_) => Some("boolean"),
        JValue::Array(_, _) => Some("array"),
        JValue::Object(_) => Some("object"),
        JValue::Lambda(_) | JValue::Native(_) | JValue::Partial(_) | JValue::Regex(_) => {
            Some("function")
        }
    }
}

// ---------------------------------------------------------------------------
// Dispatch
// ---------------------------------------------------------------------------

/// Get argument `i` or Undefined.
pub fn arg(args: &[JValue], i: usize) -> JValue {
    args.get(i).cloned().unwrap_or(JValue::Undefined)
}

/// `Functions.getFunctionArity` — min args for natives, param count for lambdas.
pub fn function_arity(func: &JValue) -> usize {
    match func {
        JValue::Native(n) => n
            .signature
            .as_ref()
            .map(|s| s.get_min_number_of_args())
            .unwrap_or(0),
        JValue::Lambda(l) => l.arguments.len(),
        JValue::Partial(p) => p.args.iter().filter(|a| a.is_none()).count(),
        _ => 0,
    }
}

/// `Functions.hofFuncArgs` — build the arg list for a HOF callback based on the
/// callback's arity: always `[value]`, plus `index` if arity>=2, plus `whole`
/// if arity>=3.
pub fn hof_func_args(func: &JValue, value: JValue, index: JValue, whole: JValue) -> Vec<JValue> {
    let arity = function_arity(func);
    let mut out = vec![value];
    if arity >= 2 {
        out.push(index);
    }
    if arity >= 3 {
        out.push(whole);
    }
    out
}

/// Java `Functions.call` wraps every `Number` result through
/// `Utils.convertNumber`: a NaN becomes `null` (undefined) and an infinite
/// value throws D1001. Apply that to built-in results.
fn finalize_number_result(v: JValue) -> JResult<JValue> {
    if let JValue::Number(n) = &v {
        if n.is_nan() {
            return Ok(JValue::Undefined);
        }
        if !n.is_finite() {
            return Err(JError::with_current("D1001", 0, v));
        }
    }
    Ok(v)
}

/// Dispatch a built-in by jsonata name.
pub fn call_builtin(ev: &mut Evaluator, name: &str, args: Vec<JValue>) -> JResult<JValue> {
    finalize_number_result(call_builtin_inner(ev, name, args)?)
}

fn call_builtin_inner(ev: &mut Evaluator, name: &str, args: Vec<JValue>) -> JResult<JValue> {
    match name {
        // numeric / aggregate
        "sum" => numeric::sum(&args),
        "count" => numeric::count(&args),
        "max" => numeric::max(&args),
        "min" => numeric::min(&args),
        "average" => numeric::average(&args),
        "number" => numeric::number(&args),
        "floor" => numeric::floor(&args),
        "ceil" => numeric::ceil(&args),
        "round" => numeric::round(&args),
        "abs" => numeric::abs(&args),
        "sqrt" => numeric::sqrt(&args),
        "power" => numeric::power(&args),
        "random" => numeric::random(&args),
        "formatNumber" => numeric::format_number(&args),
        "formatBase" => numeric::format_base(&args),
        "formatInteger" => numeric::format_integer(&args),
        "parseInteger" => numeric::parse_integer(&args),

        // boolean
        "boolean" => Ok(match to_boolean(&arg(&args, 0)) {
            Some(b) => JValue::Bool(b),
            None => JValue::Undefined,
        }),
        "not" => Ok(match &arg(&args, 0) {
            JValue::Undefined => JValue::Undefined,
            v => JValue::Bool(!boolize(v)),
        }),
        "exists" => Ok(JValue::Bool(!arg(&args, 0).is_undefined())),

        // strings
        "string" => strings::string_fn(&args),
        "substring" => strings::substring(&args),
        "substringBefore" => strings::substring_before(&args),
        "substringAfter" => strings::substring_after(&args),
        "lowercase" => strings::lowercase(&args),
        "uppercase" => strings::uppercase(&args),
        "length" => strings::length(&args),
        "trim" => strings::trim(&args),
        "pad" => strings::pad(&args),
        "contains" => strings::contains(ev, &args),
        "replace" => strings::replace(ev, &args),
        "split" => strings::split(ev, &args),
        "join" => strings::join(&args),
        "match" => strings::match_fn(ev, &args),
        "base64encode" => strings::base64encode(&args),
        "base64decode" => strings::base64decode(&args),
        "encodeUrlComponent" => strings::encode_url_component(&args),
        "encodeUrl" => strings::encode_url(&args),
        "decodeUrlComponent" => strings::decode_url_component(&args),
        "decodeUrl" => strings::decode_url(&args),

        // collections / object
        "append" => Ok(append(arg(&args, 0), arg(&args, 1))),
        "reverse" => collections::reverse(&args),
        "shuffle" => collections::shuffle(&args),
        "distinct" => collections::distinct(&args),
        "zip" => collections::zip(&args),
        "keys" => collections::keys(&args),
        "lookup" => collections::lookup_fn(&args),
        "spread" => collections::spread(&args),
        "merge" => collections::merge(&args),
        "type" => Ok(match type_of(&arg(&args, 0)) {
            Some(t) => JValue::string(t),
            None => JValue::Undefined,
        }),

        // higher-order
        "map" => hof::map(ev, &args),
        "filter" => hof::filter(ev, &args),
        "single" => hof::single(ev, &args),
        "reduce" => hof::reduce(ev, &args),
        "sift" => hof::sift(ev, &args),
        "each" => hof::each(ev, &args),
        "sort" => hof::sort(ev, &args),

        // misc
        "error" => misc::error(&args),
        "assert" => misc::assert_fn(&args),
        "eval" => misc::eval(ev, &args),
        "clone" => Ok(function_clone(&arg(&args, 0))),

        // datetime
        "now" => misc::now(ev, &args),
        "millis" => Ok(JValue::Number(ev.timestamp as f64)),
        "fromMillis" => misc::from_millis(&args),
        "toMillis" => misc::to_millis(&args),

        _ => Err(JError::at(
            &format!("Function not implemented: {}", name),
            -1,
        )),
    }
}

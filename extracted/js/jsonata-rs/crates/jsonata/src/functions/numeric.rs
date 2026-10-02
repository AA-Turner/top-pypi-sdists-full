//! Numeric / aggregate built-ins. Port of `com.dashjoin.jsonata.Functions`.

use crate::error::{JError, JResult};
use crate::value::{JValue, Object};

// ---------------------------------------------------------------------------
// Aggregates: sum / count / max / min / average
//
// The signature validator turns the `a<n>` / `a` parameter into an array (a
// lone number is wrapped into a 1-element array). So `args[0]` is either an
// Array or Undefined (undefined input).
// ---------------------------------------------------------------------------

/// Java: `public static Number sum(List<Number> args)`
pub fn sum(args: &[JValue]) -> JResult<JValue> {
    let a = crate::functions::arg(args, 0);
    // undefined inputs always return undefined
    if a.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let arr = match a.as_array() {
        Some(arr) => arr,
        None => return Ok(JValue::Undefined),
    };
    let total: f64 = arr.iter().filter_map(|v| v.as_f64()).sum();
    Ok(JValue::Number(total))
}

/// Java: `public static Number count(List<Object> args)`
pub fn count(args: &[JValue]) -> JResult<JValue> {
    let a = crate::functions::arg(args, 0);
    // undefined inputs always return 0
    if a.is_undefined() {
        return Ok(JValue::Number(0.0));
    }
    let len = match a.as_array() {
        Some(arr) => arr.len(),
        None => return Ok(JValue::Number(0.0)),
    };
    Ok(JValue::Number(len as f64))
}

/// Java: `public static Number max(List<Number> args)`
pub fn max(args: &[JValue]) -> JResult<JValue> {
    let a = crate::functions::arg(args, 0);
    // undefined inputs always return undefined
    if a.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let arr = match a.as_array() {
        Some(arr) => arr,
        None => return Ok(JValue::Undefined),
    };
    if arr.is_empty() {
        return Ok(JValue::Undefined);
    }
    // OptionalDouble.max over the doubleValues
    let mut res = f64::NEG_INFINITY;
    for v in arr.iter() {
        if let Some(d) = v.as_f64() {
            if d > res {
                res = d;
            }
        }
    }
    Ok(JValue::Number(res))
}

/// Java: `public static Number min(List<Number> args)`
pub fn min(args: &[JValue]) -> JResult<JValue> {
    let a = crate::functions::arg(args, 0);
    // undefined inputs always return undefined
    if a.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let arr = match a.as_array() {
        Some(arr) => arr,
        None => return Ok(JValue::Undefined),
    };
    if arr.is_empty() {
        return Ok(JValue::Undefined);
    }
    let mut res = f64::INFINITY;
    for v in arr.iter() {
        if let Some(d) = v.as_f64() {
            if d < res {
                res = d;
            }
        }
    }
    Ok(JValue::Number(res))
}

/// Java: `public static Number average(List<Number> args)`
pub fn average(args: &[JValue]) -> JResult<JValue> {
    let a = crate::functions::arg(args, 0);
    // undefined inputs always return undefined
    if a.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let arr = match a.as_array() {
        Some(arr) => arr,
        None => return Ok(JValue::Undefined),
    };
    if arr.is_empty() {
        return Ok(JValue::Undefined);
    }
    let mut total = 0.0f64;
    let mut n = 0usize;
    for v in arr.iter() {
        if let Some(d) = v.as_f64() {
            total += d;
            n += 1;
        }
    }
    if n == 0 {
        return Ok(JValue::Undefined);
    }
    Ok(JValue::Number(total / n as f64))
}

// ---------------------------------------------------------------------------
// $number cast
// ---------------------------------------------------------------------------

/// Java: `public static Number number(Object arg)`
pub fn number(args: &[JValue]) -> JResult<JValue> {
    let arg = crate::functions::arg(args, 0);

    // undefined inputs always return undefined
    if arg.is_undefined() {
        return Ok(JValue::Undefined);
    }

    // Java: if (arg==Jsonata.NULL_VALUE) throw new JException("T0410", -1);
    if arg.is_null() {
        // Java: throw new JException("T0410", -1)
        return Err(JError::at("T0410", -1));
    }

    match &arg {
        JValue::Number(n) => Ok(JValue::Number(*n)),
        JValue::String(s) => {
            let s: &str = s;
            // Java prefixes: "0x" (hex, lowercase only), "0B" (binary,
            // uppercase only), "0O" (octal, uppercase only). Note the exact
            // casing the Java code checks for.
            let result: f64 = if let Some(rest) = s.strip_prefix("0x") {
                // Long.parseLong(rest, 16)
                match parse_radix(rest, 16) {
                    Some(v) => v as f64,
                    // Java: NumberFormatException -> surfaces as failure
                    None => return Err(number_cast_error(&arg)),
                }
            } else if let Some(rest) = s.strip_prefix("0B") {
                match parse_radix(rest, 2) {
                    Some(v) => v as f64,
                    None => return Err(number_cast_error(&arg)),
                }
            } else if let Some(rest) = s.strip_prefix("0O") {
                match parse_radix(rest, 8) {
                    Some(v) => v as f64,
                    None => return Err(number_cast_error(&arg)),
                }
            } else {
                // Double.valueOf(s). Java's Double.valueOf trims leading and
                // trailing whitespace, accepts an optional trailing 'f'/'d'
                // type suffix, and parses "Infinity"/"NaN". JSONata test
                // expectations (D3030 on bad input) mean: anything Double
                // cannot parse -> error.
                match parse_java_double(s) {
                    Some(v) => v,
                    // Java: NumberFormatException -> D3030 at call site
                    None => return Err(number_cast_error(&arg)),
                }
            };
            // Java: the raw Double flows out of Functions.number and is then
            // passed through Utils.convertNumber at the function-call return
            // path: NaN -> null (undefined result), +/-Infinity -> D1001.
            // jsonata-js raises D3030 for all of these; see COMPAT.md.
            if result.is_nan() {
                return Ok(JValue::Undefined);
            }
            if !result.is_finite() {
                return Err(JError::with_current("D1001", 0, JValue::Number(result)));
            }
            Ok(JValue::Number(result))
        }
        JValue::Bool(b) => Ok(JValue::Number(if *b { 1.0 } else { 0.0 })),
        // Java returns null (result stays null) for other types; but the
        // `<(nsb)-:n>` signature only admits number/string/bool, so this is
        // unreachable in practice.
        _ => Ok(JValue::Undefined),
    }
}

/// D3030 error carrying the offending value (matches the JSONata test suite's
/// `code: D3030`; Java surfaces the underlying NumberFormatException as a
/// RuntimeException which the harness accepts when a code is expected).
fn number_cast_error(arg: &JValue) -> JError {
    // Java: NumberFormatException; mapped to D3030 "Unable to cast value to a number"
    JError::with_current("D3030", -1, arg.clone())
}

/// Java `Long.parseLong(s, radix)` for a non-negative magnitude string.
/// Returns None on any invalid digit / overflow (NumberFormatException).
fn parse_radix(s: &str, radix: u32) -> Option<i64> {
    // Java Long.parseLong supports a leading sign; the substrings here come
    // after a "0x"/"0B"/"0O" prefix so a sign would be unusual, but emulate
    // the permissive behavior.
    if s.is_empty() {
        return None;
    }
    i64::from_str_radix(s, radix).ok()
}

/// Emulate `Double.valueOf(String)`:
/// - trims leading/trailing whitespace (Java trims chars <= ' ')
/// - accepts an optional trailing 'f','F','d','D' type suffix
/// - accepts "Infinity", "-Infinity", "+Infinity", "NaN" (with optional sign)
/// - accepts hex floating point (`0x1p1`, `0X.8p2`, ...)
/// - rejects Rust-isms Java does not know ("inf", "nan", "infinity")
/// Returns None when Java's Double.valueOf would throw NumberFormatException.
fn parse_java_double(s: &str) -> Option<f64> {
    // Java's trim() removes characters with code <= 0x20.
    let t = s.trim_matches(|c: char| (c as u32) <= 0x20);
    if t.is_empty() {
        return None;
    }

    // Strip an optional single trailing type suffix (f/F/d/D). Java's grammar
    // allows it after any of the alternatives (including NaN/Infinity).
    let core = match t.chars().last() {
        Some('f' | 'F' | 'D') => &t[..t.len() - 1],
        // 'd' also terminates a hex-float mantissa-less form? No: 'd' is a hex
        // digit, but a hex literal requires a 'p' exponent after the digits, so
        // a trailing 'd' there would be invalid anyway; treat it as the suffix.
        Some('d') => &t[..t.len() - 1],
        _ => t,
    };
    if core.is_empty() {
        return None;
    }

    let (sign, body) = match core.strip_prefix('+') {
        Some(rest) => (1.0f64, rest),
        None => match core.strip_prefix('-') {
            Some(rest) => (-1.0f64, rest),
            None => (1.0f64, core),
        },
    };
    if body == "Infinity" {
        return Some(sign * f64::INFINITY);
    }
    if body == "NaN" {
        return Some(f64::NAN);
    }

    // Hex floating point: 0[xX] HexDigits[.HexDigits] [pP] SignedInteger
    if let Some(hex) = body.strip_prefix("0x").or_else(|| body.strip_prefix("0X")) {
        return parse_hex_float(hex).map(|v| sign * v);
    }

    // Decimal: digits with at most one '.', optional [eE][+-]digits. Reject any
    // other alphabetic content ("inf", "nan", ... are accepted by Rust's f64
    // FromStr but are NumberFormatExceptions in Java).
    if body
        .chars()
        .any(|c| !(c.is_ascii_digit() || matches!(c, '.' | 'e' | 'E' | '+' | '-')))
    {
        return None;
    }
    match body.parse::<f64>() {
        Ok(v) => Some(sign * v),
        Err(_) => None,
    }
}

/// The part after `0x`/`0X` of a Java hex floating-point literal:
/// `HexDigits[.HexDigits]? [pP] SignedInteger` (the binary exponent is
/// mandatory; at least one hex digit must be present).
fn parse_hex_float(s: &str) -> Option<f64> {
    let (mantissa_str, exp_str) = s.split_once(['p', 'P'])?;
    let exp: i32 = exp_str.parse().ok()?;
    let (int_part, frac_part) = match mantissa_str.split_once('.') {
        Some((i, f)) => (i, f),
        None => (mantissa_str, ""),
    };
    if int_part.is_empty() && frac_part.is_empty() {
        return None;
    }
    let mut value = 0.0f64;
    for c in int_part.chars() {
        value = value * 16.0 + (c.to_digit(16)? as f64);
    }
    let mut scale = 1.0 / 16.0;
    for c in frac_part.chars() {
        value += (c.to_digit(16)? as f64) * scale;
        scale /= 16.0;
    }
    Some(value * 2f64.powi(exp))
}

// ---------------------------------------------------------------------------
// floor / ceil / round / abs / sqrt / power
// ---------------------------------------------------------------------------

/// Java: `public static Number abs(Number arg)`
pub fn abs(args: &[JValue]) -> JResult<JValue> {
    let arg = crate::functions::arg(args, 0);
    if arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let d = arg.as_f64().unwrap_or(f64::NAN);
    Ok(JValue::Number(d.abs()))
}

/// Java: `public static Number floor(Number arg)`
pub fn floor(args: &[JValue]) -> JResult<JValue> {
    let arg = crate::functions::arg(args, 0);
    if arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let d = arg.as_f64().unwrap_or(f64::NAN);
    Ok(JValue::Number(d.floor()))
}

/// Java: `public static Number ceil(Number arg)`
pub fn ceil(args: &[JValue]) -> JResult<JValue> {
    let arg = crate::functions::arg(args, 0);
    if arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let d = arg.as_f64().unwrap_or(f64::NAN);
    Ok(JValue::Number(d.ceil()))
}

/// Java: `public static Number round(Number arg, Number precision)`
/// ```java
/// BigDecimal b = new BigDecimal(arg+"");
/// if (precision==null) precision = 0;
/// b = b.setScale(precision.intValue(), RoundingMode.HALF_EVEN);
/// return b.doubleValue();
/// ```
pub fn round(args: &[JValue]) -> JResult<JValue> {
    let arg = crate::functions::arg(args, 0);
    if arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let d = arg.as_f64().unwrap_or(f64::NAN);

    let precision = match crate::functions::arg(args, 1) {
        JValue::Undefined => 0i32,
        p => p.as_f64().map(|x| x as i32).unwrap_or(0),
    };

    // Java builds the BigDecimal from `arg + ""` i.e. the canonical string
    // form of the double, then setScale(HALF_EVEN). Replicate by operating on
    // the decimal string (number_to_string mirrors Java's "" + double).
    let s = crate::functions::number_to_string(d);
    let result = big_decimal_set_scale_half_even(&s, precision);
    Ok(JValue::Number(result))
}

/// Java: `public static Number sqrt(Number arg)`
pub fn sqrt(args: &[JValue]) -> JResult<JValue> {
    let arg = crate::functions::arg(args, 0);
    if arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let d = arg.as_f64().unwrap_or(f64::NAN);
    if d < 0.0 {
        // Java: throw new JException("D3060", 1, arg);
        return Err(JError::with_current("D3060", 1, arg.clone()));
    }
    Ok(JValue::Number(d.sqrt()))
}

/// Java: `public static Number power(Number arg, Number exp)`
pub fn power(args: &[JValue]) -> JResult<JValue> {
    let arg = crate::functions::arg(args, 0);
    if arg.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let base = arg.as_f64().unwrap_or(f64::NAN);
    let exp = crate::functions::arg(args, 1).as_f64().unwrap_or(f64::NAN);

    let result = base.powf(exp);

    if !result.is_finite() {
        // Java: throw new JException("D3061", 1, arg, exp);
        let exp_val = crate::functions::arg(args, 1);
        return Err(JError::with_current_expected(
            "D3061",
            1,
            arg.clone(),
            exp_val,
        ));
    }
    Ok(JValue::Number(result))
}

/// Java: `public static Number random() { return Math.random(); }`
/// Returns a fresh pseudo-random double in [0,1) on each call. Determinism is
/// not testable, so a simple SystemTime-seeded xorshift suffices.
pub fn random(_args: &[JValue]) -> JResult<JValue> {
    use std::cell::Cell;
    use std::time::{SystemTime, UNIX_EPOCH};

    thread_local! {
        static STATE: Cell<u64> = const { Cell::new(0) };
    }

    let r = STATE.with(|st| {
        let mut x = st.get();
        if x == 0 {
            // Seed from the clock the first time.
            let nanos = SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .map(|d| d.as_nanos() as u64)
                .unwrap_or(0x9E3779B97F4A7C15);
            x = nanos ^ 0x9E3779B97F4A7C15;
            if x == 0 {
                x = 0x9E3779B97F4A7C15;
            }
        }
        // xorshift64*
        x ^= x >> 12;
        x ^= x << 25;
        x ^= x >> 27;
        st.set(x);
        x.wrapping_mul(0x2545F4914F6CDD1D)
    });

    // Top 53 bits -> [0,1)
    let mantissa = r >> 11;
    let val = (mantissa as f64) / ((1u64 << 53) as f64);
    Ok(JValue::Number(val))
}

// ---------------------------------------------------------------------------
// formatBase
// ---------------------------------------------------------------------------

/// Java: `public static String formatBase(Number value, Number _radix)`
pub fn format_base(args: &[JValue]) -> JResult<JValue> {
    let value = crate::functions::arg(args, 0);
    // undefined inputs always return undefined
    if value.is_undefined() {
        return Ok(JValue::Undefined);
    }

    // value = round(value, 0);
    let d = value.as_f64().unwrap_or(f64::NAN);
    let s = crate::functions::number_to_string(d);
    let rounded = big_decimal_set_scale_half_even(&s, 0);

    let radix = match crate::functions::arg(args, 1) {
        JValue::Undefined => 10i64,
        r => r.as_f64().map(|x| x as i64).unwrap_or(10),
    };

    if !(2..=36).contains(&radix) {
        // Java: throw new JException("D3100", radix);
        return Err(JError::with_current(
            "D3100",
            -1,
            JValue::Number(radix as f64),
        ));
    }

    // Long.toString(value.longValue(), radix)
    let as_long = double_to_long(rounded);
    let result = long_to_string_radix(as_long, radix as u32);
    Ok(JValue::string(result))
}

// ---------------------------------------------------------------------------
// formatNumber
//
// Faithful port of jsonata-java `formatNumber` (Functions.java), which is a
// thin wrapper over `java.text.DecimalFormat`: it builds
// `DecimalFormatSymbols(Locale.US)` (optionally overridden from the options
// map, see Java `processOptionsArg`), replaces the digits 1-9 in the picture
// with 0, folds a lowercase exponent 'e' to 'E' (restoring it in the result),
// and calls `applyLocalizedPattern` + `format`. The code below reproduces the
// OpenJDK `DecimalFormat` / `DigitList` pipeline exactly, including HALF_EVEN
// rounding with FloatingDecimal shortest-representation tie semantics.
// Where Java throws a raw RuntimeException / IllegalArgumentException, we
// raise typed D308x errors with the same accept/reject behaviour.
// ---------------------------------------------------------------------------

const DF_QUOTE: char = '\'';
const DF_CURRENCY_SIGN: char = '\u{00a4}';
/// DecimalFormat.DOUBLE_INTEGER_DIGITS
const DF_DOUBLE_INTEGER_DIGITS: i32 = 309;
/// DecimalFormat.DOUBLE_FRACTION_DIGITS
const DF_DOUBLE_FRACTION_DIGITS: i32 = 340;

/// `java.text.DecimalFormatSymbols(Locale.US)`, overridable via the options
/// object (Java `processOptionsArg`).
struct DfSymbols {
    decimal_separator: char,
    grouping_separator: char,
    infinity: String,
    minus_sign: char,
    nan: String,
    percent: char,
    per_mille: char,
    zero_digit: char,
    digit: char,
    pattern_separator: char,
    /// Not overridable: Java's options switch has no exponent key.
    exponent_separator: char,
    currency_symbol: &'static str,
    intl_currency_symbol: &'static str,
    /// Monetary separators are locale-initialized copies that the option
    /// setters never touch (Java `setDecimalSeparator` does not update them).
    monetary_decimal_separator: char,
    monetary_grouping_separator: char,
}

impl DfSymbols {
    fn locale_us() -> Self {
        DfSymbols {
            decimal_separator: '.',
            grouping_separator: ',',
            infinity: "\u{221e}".to_string(),
            minus_sign: '-',
            nan: "NaN".to_string(),
            percent: '%',
            per_mille: '\u{2030}',
            zero_digit: '0',
            digit: '#',
            pattern_separator: ';',
            exponent_separator: 'E',
            currency_symbol: "$",
            intl_currency_symbol: "USD",
            monetary_decimal_separator: '.',
            monetary_grouping_separator: ',',
        }
    }
}

/// Java `getFormattingCharacter(value, prop, isChar=true)`: exactly one char
/// (one UTF-16 unit), anything else throws.
fn df_formatting_char(value: &str) -> JResult<char> {
    if value.encode_utf16().count() == 1 {
        Ok(value.chars().next().unwrap())
    } else {
        Err(JError::at("D3080", -1))
    }
}

/// Java `getFormattingCharacter(value, prop, isChar=false)`: any non-empty
/// string.
fn df_formatting_string(value: &str) -> JResult<String> {
    if value.is_empty() {
        Err(JError::at("D3080", -1))
    } else {
        Ok(value.to_string())
    }
}

/// Java `processOptionsArg`: build DecimalFormatSymbols from the options map.
/// Unknown keys and non-string values throw (raw RuntimeException /
/// ClassCastException in Java).
fn process_options_arg(obj: &Object, sym: &mut DfSymbols) -> JResult<()> {
    for (key, val) in obj.iter() {
        let value = match val.as_str() {
            Some(s) => s,
            None => return Err(JError::at("D3080", -1)),
        };
        match key.as_str() {
            "decimal-separator" => sym.decimal_separator = df_formatting_char(value)?,
            "grouping-separator" => sym.grouping_separator = df_formatting_char(value)?,
            "infinity" => sym.infinity = df_formatting_string(value)?,
            "minus-sign" => sym.minus_sign = df_formatting_char(value)?,
            "NaN" => sym.nan = df_formatting_string(value)?,
            "percent" => sym.percent = df_formatting_char(value)?,
            // isChar=false, then Java takes charAt(0) for setPerMill.
            "per-mille" => sym.per_mille = df_formatting_string(value)?.chars().next().unwrap(),
            "zero-digit" => sym.zero_digit = df_formatting_char(value)?,
            "digit" => sym.digit = df_formatting_char(value)?,
            "pattern-separator" => sym.pattern_separator = df_formatting_char(value)?,
            _ => return Err(JError::at("D3080", -1)),
        }
    }
    Ok(())
}

/// The observable state of a `DecimalFormat` after `applyLocalizedPattern`.
#[derive(Default)]
struct DfPattern {
    positive_prefix: String,
    positive_suffix: String,
    negative_prefix: String,
    negative_suffix: String,
    multiplier: i32,
    grouping_used: bool,
    grouping_size: i32,
    use_exponential: bool,
    min_exponent_digits: i32,
    decimal_separator_always_shown: bool,
    is_currency_format: bool,
    /// Effective digit limits as seen by `format(double)` — i.e. the
    /// NumberFormat "super" fields, capped at 309 integer / 340 fraction
    /// digits by the DecimalFormat setters.
    max_int: i32,
    min_int: i32,
    max_frac: i32,
    min_frac: i32,
}

/// Port of `DecimalFormat.applyPattern(pattern, localized=true)`.
fn apply_localized_pattern(pattern_str: &str, sym: &DfSymbols) -> JResult<DfPattern> {
    let pattern: Vec<char> = pattern_str.chars().collect();
    let zero_digit = sym.zero_digit;
    let grouping_separator = sym.grouping_separator;
    let decimal_separator = sym.decimal_separator;
    let percent = sym.percent;
    let per_mill = sym.per_mille;
    let digit = sym.digit;
    let separator = sym.pattern_separator;
    let exponent = sym.exponent_separator;
    let minus = sym.minus_sign;

    let mut st = DfPattern {
        multiplier: 1,
        // State left over from the constructor's default pattern
        // ("#,##0.###"); only observable for an empty picture.
        grouping_used: true,
        grouping_size: 3,
        ..Default::default()
    };
    let mut got_negative = false;
    // Affix *patterns* (with quote-escaped specials), expanded at the end.
    let mut pos_prefix_pat = String::new();
    let mut pos_suffix_pat = String::new();
    let mut neg_prefix_pat = String::new();
    let mut neg_suffix_pat = String::new();
    // Raw (uncapped) digit-limit fields, as held by NumberFormat. Initial
    // values are the constructor defaults from "#,##0.###".
    let mut min_int_field = 1i32;
    let mut max_int_field = i32::MAX;
    let mut min_frac_field = 0i32;
    let mut max_frac_field = 3i32;

    let mut start = 0usize;
    let mut j = 1i32;
    while j >= 0 && start < pattern.len() {
        let mut in_quote = false;
        let mut prefix = String::new();
        let mut suffix = String::new();
        let mut decimal_pos = -1i32;
        let mut multiplier = 1i32;
        let mut digit_left_count = 0i32;
        let mut zero_digit_count = 0i32;
        let mut digit_right_count = 0i32;
        let mut grouping_count = -1i32;
        // Phase 0 is the prefix, phase 1 the digits/decimal/grouping section,
        // phase 2 the suffix.
        let mut phase = 0;
        let mut in_prefix = true; // Java: `affix = prefix`

        macro_rules! affix {
            () => {
                if in_prefix {
                    &mut prefix
                } else {
                    &mut suffix
                }
            };
        }

        let mut pos = start;
        'chars: while pos < pattern.len() {
            let ch = pattern[pos];
            if phase == 0 || phase == 2 {
                // Process the prefix / suffix characters.
                if in_quote {
                    if ch == DF_QUOTE {
                        if pos + 1 < pattern.len() && pattern[pos + 1] == DF_QUOTE {
                            pos += 1;
                            affix!().push_str("''"); // 'don''t'
                        } else {
                            in_quote = false; // 'do'
                        }
                        pos += 1;
                        continue 'chars;
                    }
                } else {
                    if ch == digit
                        || ch == zero_digit
                        || ch == grouping_separator
                        || ch == decimal_separator
                    {
                        phase = 1;
                        continue 'chars; // reprocess this character
                    } else if ch == DF_CURRENCY_SIGN {
                        let doubled =
                            pos + 1 < pattern.len() && pattern[pos + 1] == DF_CURRENCY_SIGN;
                        if doubled {
                            pos += 1;
                        }
                        st.is_currency_format = true;
                        affix!().push_str(if doubled { "'\u{a4}\u{a4}" } else { "'\u{a4}" });
                        pos += 1;
                        continue 'chars;
                    } else if ch == DF_QUOTE {
                        if pos + 1 < pattern.len() && pattern[pos + 1] == DF_QUOTE {
                            pos += 1;
                            affix!().push_str("''"); // o''clock
                        } else {
                            in_quote = true;
                        }
                        pos += 1;
                        continue 'chars;
                    } else if ch == separator {
                        // No separators before phase 1, none in the second
                        // pattern (Java: IllegalArgumentException).
                        if phase == 0 || j == 0 {
                            return Err(JError::at("D3080", -1));
                        }
                        start = pos + 1;
                        break 'chars; // Java: pos = pattern.length()
                    } else if ch == percent {
                        if multiplier != 1 {
                            // Java: "Too many percent/per mille characters"
                            return Err(JError::at(
                                if multiplier == 100 { "D3082" } else { "D3084" },
                                -1,
                            ));
                        }
                        multiplier = 100;
                        affix!().push_str("'%");
                        pos += 1;
                        continue 'chars;
                    } else if ch == per_mill {
                        if multiplier != 1 {
                            return Err(JError::at(
                                if multiplier == 1000 { "D3083" } else { "D3084" },
                                -1,
                            ));
                        }
                        multiplier = 1000;
                        affix!().push_str("'\u{2030}");
                        pos += 1;
                        continue 'chars;
                    } else if ch == minus {
                        affix!().push_str("'-");
                        pos += 1;
                        continue 'chars;
                    }
                }
                // Within quotes, or an unquoted non-special character.
                affix!().push(ch);
                pos += 1;
            } else {
                // Phase 1. In the negative subpattern (j == 0) the phase 1
                // characters serve no purpose and are simply skipped.
                if j == 0 {
                    while pos < pattern.len() {
                        let c = pattern[pos];
                        if c == digit
                            || c == zero_digit
                            || c == grouping_separator
                            || c == decimal_separator
                            || c == exponent
                        {
                            pos += 1;
                        } else {
                            // Not a phase 1 character: parse it in phase 2.
                            phase = 2;
                            in_prefix = false;
                            break;
                        }
                    }
                    continue 'chars;
                }
                if ch == digit {
                    if zero_digit_count > 0 {
                        digit_right_count += 1;
                    } else {
                        digit_left_count += 1;
                    }
                    if grouping_count >= 0 && decimal_pos < 0 {
                        grouping_count += 1;
                    }
                    pos += 1;
                } else if ch == zero_digit {
                    if digit_right_count > 0 {
                        // Java: "Unexpected '0' in pattern"
                        return Err(JError::at("D3091", -1));
                    }
                    zero_digit_count += 1;
                    if grouping_count >= 0 && decimal_pos < 0 {
                        grouping_count += 1;
                    }
                    pos += 1;
                } else if ch == grouping_separator {
                    grouping_count = 0;
                    pos += 1;
                } else if ch == decimal_separator {
                    if decimal_pos >= 0 {
                        // Java: "Multiple decimal separators in pattern"
                        return Err(JError::at("D3081", -1));
                    }
                    decimal_pos = digit_left_count + zero_digit_count + digit_right_count;
                    pos += 1;
                } else if ch == exponent {
                    if st.use_exponential {
                        // Java: "Multiple exponential symbols in pattern"
                        return Err(JError::at("D3090", -1));
                    }
                    st.use_exponential = true;
                    st.min_exponent_digits = 0;
                    pos += 1;
                    while pos < pattern.len() && pattern[pos] == zero_digit {
                        st.min_exponent_digits += 1;
                        pos += 1;
                    }
                    if digit_left_count + zero_digit_count < 1 || st.min_exponent_digits < 1 {
                        // Java: "Malformed exponential pattern"
                        return Err(JError::at("D3085", -1));
                    }
                    // Transition to phase 2.
                    phase = 2;
                    in_prefix = false;
                } else {
                    phase = 2;
                    in_prefix = false;
                    // Reprocess this character in phase 2 (no pos advance).
                }
            }
        }

        // Handle patterns with no '0' pattern character ("##.###" -> "#0.###",
        // ".###" -> ".0##").
        if zero_digit_count == 0 && digit_left_count > 0 && decimal_pos >= 0 {
            let mut n = decimal_pos;
            if n == 0 {
                n += 1; // Handle ".###"
            }
            digit_right_count = digit_left_count - n;
            digit_left_count = n - 1;
            zero_digit_count = 1;
        }

        // Do syntax checking on the digits (Java: "Malformed pattern").
        if (decimal_pos < 0 && digit_right_count > 0)
            || (decimal_pos >= 0
                && (decimal_pos < digit_left_count
                    || decimal_pos > digit_left_count + zero_digit_count))
            || grouping_count == 0
            || in_quote
        {
            let code = if grouping_count == 0 {
                "D3088"
            } else if in_quote {
                "D3085"
            } else {
                "D3090"
            };
            return Err(JError::at(code, -1));
        }

        if j == 1 {
            pos_prefix_pat = prefix;
            pos_suffix_pat = suffix;
            neg_prefix_pat = pos_prefix_pat.clone(); // assume these for now
            neg_suffix_pat = pos_suffix_pat.clone();

            let digit_total_count = digit_left_count + zero_digit_count + digit_right_count;
            let effective_decimal_pos = if decimal_pos >= 0 {
                decimal_pos
            } else {
                digit_total_count
            };
            // setMinimumIntegerDigits (its max-adjustment is dead: the
            // setMaximumIntegerDigits below overwrites unconditionally)
            min_int_field = (effective_decimal_pos - digit_left_count).max(0);
            // setMaximumIntegerDigits
            max_int_field = if st.use_exponential {
                digit_left_count + min_int_field
            } else {
                i32::MAX
            };
            if min_int_field > max_int_field {
                min_int_field = max_int_field;
            }
            // setMaximumFractionDigits
            max_frac_field = if decimal_pos >= 0 {
                digit_total_count - decimal_pos
            } else {
                0
            };
            // setMinimumFractionDigits (setMaximumFractionDigits' min-
            // adjustment is dead: the assignment below overwrites it)
            min_frac_field = if decimal_pos >= 0 {
                digit_left_count + zero_digit_count - decimal_pos
            } else {
                0
            };
            if min_frac_field > max_frac_field {
                max_frac_field = min_frac_field;
            }
            st.grouping_used = grouping_count > 0;
            st.grouping_size = if grouping_count > 0 {
                grouping_count
            } else {
                0
            };
            st.multiplier = multiplier;
            st.decimal_separator_always_shown =
                decimal_pos == 0 || decimal_pos == digit_total_count;
        } else {
            neg_prefix_pat = prefix;
            neg_suffix_pat = suffix;
            got_negative = true;
        }
        j -= 1;
    }

    if pattern.is_empty() {
        pos_prefix_pat.clear();
        pos_suffix_pat.clear();
        min_int_field = 0;
        max_int_field = i32::MAX;
        min_frac_field = 0;
        max_frac_field = i32::MAX;
    }

    // If there was no negative pattern, or if the negative pattern is
    // identical to the positive pattern, prepend the minus sign to the
    // positive pattern to form the negative pattern.
    if !got_negative || (neg_prefix_pat == pos_prefix_pat && neg_suffix_pat == pos_suffix_pat) {
        neg_suffix_pat = pos_suffix_pat.clone();
        neg_prefix_pat = format!("'-{}", pos_prefix_pat);
    }

    st.positive_prefix = expand_affix(&pos_prefix_pat, sym);
    st.positive_suffix = expand_affix(&pos_suffix_pat, sym);
    st.negative_prefix = expand_affix(&neg_prefix_pat, sym);
    st.negative_suffix = expand_affix(&neg_suffix_pat, sym);
    st.min_int = min_int_field.min(DF_DOUBLE_INTEGER_DIGITS);
    st.max_int = max_int_field.min(DF_DOUBLE_INTEGER_DIGITS);
    st.min_frac = min_frac_field.min(DF_DOUBLE_FRACTION_DIGITS);
    st.max_frac = max_frac_field.min(DF_DOUBLE_FRACTION_DIGITS);
    Ok(st)
}

/// Port of `DecimalFormat.expandAffix`: all characters are literal unless
/// prefixed by a quote; quoted `¤`/`¤¤`/`%`/`‰`/`-` expand to symbols.
fn expand_affix(pattern: &str, sym: &DfSymbols) -> String {
    let chars: Vec<char> = pattern.chars().collect();
    let mut out = String::new();
    let mut i = 0;
    while i < chars.len() {
        let c = chars[i];
        i += 1;
        if c == DF_QUOTE && i < chars.len() {
            let c2 = chars[i];
            i += 1;
            match c2 {
                DF_CURRENCY_SIGN => {
                    if i < chars.len() && chars[i] == DF_CURRENCY_SIGN {
                        i += 1;
                        out.push_str(sym.intl_currency_symbol);
                    } else {
                        out.push_str(sym.currency_symbol);
                    }
                }
                '%' => out.push(sym.percent),
                '\u{2030}' => out.push(sym.per_mille),
                '-' => out.push(sym.minus_sign),
                other => out.push(other),
            }
        } else {
            out.push(c);
        }
    }
    out
}

/// Port of `java.text.DigitList`: significant digits plus a decimal position,
/// with HALF_EVEN rounding that honours what the binary-to-decimal shortest
/// conversion did in tie cases (FloatingDecimal semantics).
struct DigitList {
    digits: Vec<u8>, // ASCII '0'..'9'
    decimal_at: i32,
    count: usize,
    /// How the shortest decimal representation relates to the exact binary
    /// value: Greater = FloatingDecimal rounded up, Less = it truncated,
    /// Equal = the digits are exact. Only consulted in '5'-tie cases.
    repr_vs_exact: std::cmp::Ordering,
}

impl DigitList {
    fn new() -> Self {
        DigitList {
            digits: Vec::new(),
            decimal_at: 0,
            count: 0,
            repr_vs_exact: std::cmp::Ordering::Equal,
        }
    }

    fn is_zero(&self) -> bool {
        self.digits[..self.count].iter().all(|d| *d == b'0')
    }

    /// `DigitList.set(isNegative, double, maximumDigits, fixedPoint)`.
    fn set_double(&mut self, x: f64, maximum_digits: i32, fixed_point: bool) {
        use std::cmp::Ordering;
        if x == 0.0 {
            self.digits.clear();
            self.count = 0;
            self.decimal_at = 0;
            self.repr_vs_exact = Ordering::Equal;
            return;
        }
        // Digits exactly as Java's legacy FloatingDecimal produces them
        // (DigitList parses fdConverter.toJavaFormatString()).
        let (mut digits, dec_exp, rounded_up, exact) = java_dtoa(x);
        // toJavaFormatString shape, as seen by DigitList's string parser:
        // - "plain" integers pad with zeros up to the decimal point plus the
        //   mandatory ".0" fraction digit;
        // - E-form pads a single-digit mantissa to two ("5.0E-4");
        // - plain fractions ("0.005") add nothing.
        if dec_exp > 0 && dec_exp < 8 {
            let de = dec_exp as usize;
            if digits.len() <= de {
                while digits.len() < de {
                    digits.push(b'0');
                }
                digits.push(b'0'); // the ".0"
            }
        } else if !(-2..=0).contains(&dec_exp) && digits.len() == 1 {
            digits.push(b'0');
        }
        self.decimal_at = dec_exp;
        self.count = digits.len();
        self.digits = digits;
        self.repr_vs_exact = if rounded_up {
            Ordering::Greater
        } else if exact {
            Ordering::Equal
        } else {
            Ordering::Less
        };

        if fixed_point {
            if -self.decimal_at > maximum_digits {
                // Underflow to zero (e.g. 0.0009 to 2 fraction digits).
                self.count = 0;
                return;
            } else if -self.decimal_at == maximum_digits {
                // E.g. 0.0009 to 3 fraction digits: round into a new digit.
                if self.should_round_up(0) {
                    self.count = 1;
                    self.decimal_at += 1;
                    self.digits[0] = b'1';
                } else {
                    self.count = 0;
                }
                return;
            }
        }

        // Eliminate trailing zeros.
        while self.count > 1 && self.digits[self.count - 1] == b'0' {
            self.count -= 1;
        }

        self.round(if fixed_point {
            maximum_digits.saturating_add(self.decimal_at)
        } else {
            maximum_digits
        });
    }

    /// `DigitList.set(isNegative, long)` (used for the exponent).
    fn set_long(&mut self, source: i64) {
        self.set_long_i128(source as i128, 0);
    }

    /// `DigitList.set(isNegative, long, maximumDigits)`, widened to i128 to
    /// also cover Java's BigInteger fallback for multiplier overflow.
    fn set_long_i128(&mut self, source: i128, maximum_digits: i32) {
        self.repr_vs_exact = std::cmp::Ordering::Equal;
        if source <= 0 {
            self.digits.clear();
            self.decimal_at = 0;
            self.count = 0;
        } else {
            self.digits = source.to_string().into_bytes();
            self.decimal_at = self.digits.len() as i32;
            let mut count = self.digits.len();
            while count > 1 && self.digits[count - 1] == b'0' {
                count -= 1;
            }
            self.count = count;
        }
        if maximum_digits > 0 {
            self.round(maximum_digits);
        }
    }

    /// `DigitList.round(maximumDigits, ...)`.
    fn round(&mut self, maximum_digits: i32) {
        if maximum_digits >= 0 && (maximum_digits as usize) < self.count {
            let mut m = maximum_digits;
            if self.should_round_up(maximum_digits as usize) {
                loop {
                    m -= 1;
                    if m < 0 {
                        // All 9s: increment to a single 1, adjust exponent.
                        self.digits[0] = b'1';
                        self.decimal_at += 1;
                        m = 0;
                        break;
                    }
                    self.digits[m as usize] += 1;
                    if self.digits[m as usize] <= b'9' {
                        break;
                    }
                }
                m += 1;
            }
            self.count = m as usize;
            // Eliminate trailing zeros.
            while self.count > 1 && self.digits[self.count - 1] == b'0' {
                self.count -= 1;
            }
        }
    }

    /// `DigitList.shouldRoundUp` for RoundingMode.HALF_EVEN (the only mode
    /// reachable through jsonata-java's formatNumber).
    fn should_round_up(&self, maximum_digits: usize) -> bool {
        use std::cmp::Ordering;
        let d = self.digits[maximum_digits];
        if d > b'5' {
            return true;
        }
        if d == b'5' {
            if maximum_digits == self.count - 1 {
                // The rounding position is exactly the last digit.
                return match self.repr_vs_exact {
                    // FloatingDecimal rounded up (value below tie): don't
                    // round up again.
                    Ordering::Greater => false,
                    // Digits were truncated to the tie (value above): round up.
                    Ordering::Less => true,
                    // Exact tie: IEEE half-even.
                    Ordering::Equal => {
                        maximum_digits > 0 && (self.digits[maximum_digits - 1] - b'0') % 2 != 0
                    }
                };
            } else {
                for i in maximum_digits + 1..self.count {
                    if self.digits[i] != b'0' {
                        return true;
                    }
                }
            }
        }
        false
    }
}

// ---------------------------------------------------------------------------
// Port of the legacy `jdk.internal.math.FloatingDecimal` binary-to-decimal
// conversion (`dtoa`), which JDK's DigitList still uses (it is NOT the
// shortest-representation Ryu converter that Double.toString switched to in
// JDK 19). Faithful down to the int/long/FDBigInteger path selection and
// their wrapping-arithmetic quirks, because those are observable.
// ---------------------------------------------------------------------------

/// `FloatingDecimal.insignificantDigitsForPow2` (only indices <= 8 are
/// reachable: the fast path requires binExp <= 62 with 53 significant bits).
const FD_INSIGNIFICANT_DIGITS: [i32; 9] = [0, 0, 0, 0, 1, 1, 1, 2, 2];

/// `FloatingDecimal.N_5_BITS[i]`: bit length of 5^i for i < 27, else `3*i`.
fn fd_n5_bits(i: i32) -> i32 {
    if i < 27 {
        if i == 0 {
            0
        } else {
            64 - (5u64.pow(i as u32)).leading_zeros() as i32
        }
    } else {
        i * 3
    }
}

/// `FloatingDecimal.estimateDecExp`.
fn fd_estimate_dec_exp(fract_bits: u64, bin_exp: i32) -> i32 {
    let signif_mask: u64 = 0x000f_ffff_ffff_ffff;
    let exp_one: u64 = 0x3ff0_0000_0000_0000; // exponent of 1.0
    let d2 = f64::from_bits(exp_one | (fract_bits & signif_mask));
    let d = (d2 - 1.5) * 0.289529654 + 0.176091259 + (bin_exp as f64) * 0.301029995663981;
    // The Java bit-twiddling is floor(d) ((int) truncation is only taken for
    // |d| >= 2^52, which cannot happen here).
    d.floor() as i32
}

/// `FloatingDecimal.BinaryToASCIIBuffer.roundup`. Note the all-nines carry
/// path deliberately does NOT set `decimalDigitsRoundedUp` (Java quirk).
fn fd_roundup(digits: &mut [u8], dec_exponent: &mut i32, rounded_up: &mut bool) {
    let mut i = digits.len() - 1;
    if digits[i] == b'9' {
        while digits[i] == b'9' && i > 0 {
            digits[i] = b'0';
            i -= 1;
        }
        if digits[i] == b'9' {
            // carryout! High-order 1, rest 0s, larger exp.
            *dec_exponent += 1;
            digits[0] = b'1';
            return;
        }
    }
    digits[i] += 1;
    *rounded_up = true;
}

/// `BinaryToASCIIBuffer.developLongDigits` (the fast path for integral
/// values below 2^63 — reachable here only via the percent/per-mille
/// multiplier, since integral inputs are dispatched to the long formatter).
/// NB: it leaves both conversion flags false (Java quirk).
fn fd_develop_long_digits(
    mut dec_exponent: i32,
    mut lvalue: i64,
    insignificant_digits: i32,
) -> (Vec<u8>, i32, bool, bool) {
    if insignificant_digits != 0 {
        // Discard non-significant low-order digits, while rounding.
        let pow10 = 5i64.pow(insignificant_digits as u32) << insignificant_digits;
        let residue = lvalue % pow10;
        lvalue /= pow10;
        dec_exponent += insignificant_digits;
        if residue >= (pow10 >> 1) {
            lvalue += 1;
        }
    }
    // Decimal digits of lvalue with trailing zeros folded into the exponent.
    let mut digits: Vec<u8> = Vec::new();
    let mut c = (lvalue % 10) as u8;
    lvalue /= 10;
    while c == 0 {
        dec_exponent += 1;
        c = (lvalue % 10) as u8;
        lvalue /= 10;
    }
    while lvalue != 0 {
        digits.push(b'0' + c);
        dec_exponent += 1;
        c = (lvalue % 10) as u8;
        lvalue /= 10;
    }
    digits.push(b'0' + c);
    digits.reverse();
    (digits, dec_exponent + 1, false, false)
}

/// The int/long native paths of `dtoa`, with Java's wrapping arithmetic
/// (the `m > 0` overflow hack differs between the 32- and 64-bit variants,
/// so the path split is observable).
macro_rules! fd_dtoa_native {
    ($ty:ty, $fract:expr, $b5:expr, $b2:expr, $s5:expr, $s2:expr, $m5:expr, $m2:expr, $dec_exp:expr) => {{
        let mut dec_exp: i32 = $dec_exp;
        let mut b: $ty = (($fract as $ty).wrapping_mul((5 as $ty).pow($b5 as u32))) << $b2;
        let s: $ty = ((5 as $ty).pow($s5 as u32)) << $s2;
        let mut m: $ty = ((5 as $ty).pow($m5 as u32)) << $m2;
        let tens: $ty = s.wrapping_mul(10);
        let mut digits: Vec<u8> = Vec::with_capacity(20);
        // Unroll the first iteration; a too-high decExp estimate gives a
        // leading zero, which is discarded.
        let mut q = (b / s) as u8;
        b = (b % s).wrapping_mul(10);
        m = m.wrapping_mul(10);
        let mut low = b < m;
        let mut high = b.wrapping_add(m) > tens;
        if q == 0 && !high {
            dec_exp -= 1;
        } else {
            digits.push(b'0' + q);
        }
        // Java spec sez we always have at least one digit after the '.' in
        // either F- or E-form output, so E-form needs more than one digit.
        if dec_exp < -3 || dec_exp >= 8 {
            low = false;
            high = false;
        }
        while !low && !high {
            q = (b / s) as u8;
            b = (b % s).wrapping_mul(10);
            m = m.wrapping_mul(10);
            if m > 0 {
                low = b < m;
                high = b.wrapping_add(m) > tens;
            } else {
                // m overflowed: it is certainly > b, and b+m > tens too.
                low = true;
                high = true;
            }
            digits.push(b'0' + q);
        }
        let low_digit_difference = (b << 1).wrapping_sub(tens);
        let exact = b == 0;
        let mut dec_exponent = dec_exp + 1;
        let mut rounded_up = false;
        if high {
            if low {
                if low_digit_difference == 0 {
                    // it's a tie! choose based on which digit we like.
                    if digits.last().map_or(false, |d| (d - b'0') % 2 != 0) {
                        fd_roundup(&mut digits, &mut dec_exponent, &mut rounded_up);
                    }
                } else if low_digit_difference > 0 {
                    fd_roundup(&mut digits, &mut dec_exponent, &mut rounded_up);
                }
            } else {
                fd_roundup(&mut digits, &mut dec_exponent, &mut rounded_up);
            }
        }
        (digits, dec_exponent, rounded_up, exact)
    }};
}

/// `BinaryToASCIIBuffer.dtoa(binExp, fractBits, nSignificantBits, true)` for
/// a positive finite double. Returns (digits, decExponent, digitsRoundedUp,
/// decimalDigitsExact) with value = 0.d1d2...  x 10^decExponent.
fn java_dtoa(x: f64) -> (Vec<u8>, i32, bool, bool) {
    let bits = x.to_bits();
    let raw_frac = bits & 0x000f_ffff_ffff_ffff;
    let exp_bits = ((bits >> 52) & 0x7ff) as i32;
    let (fract_bits, bin_exp, n_significant_bits) = if exp_bits == 0 {
        // Normalize denormalized numbers.
        let leading = raw_frac.leading_zeros() as i32;
        let shift = leading - 11;
        ((raw_frac << shift), (1 - shift) - 1023, 64 - leading)
    } else {
        (raw_frac | (1u64 << 52), exp_bits - 1023, 53)
    };
    let tail_zeros = fract_bits.trailing_zeros() as i32;
    let n_fract_bits = 53 - tail_zeros;
    let n_tiny_bits = (n_fract_bits - bin_exp - 1).max(0);

    // Easy case: an integer below 2^63 (MIN_SMALL_BIN_EXP..=MAX_SMALL_BIN_EXP
    // with nTinyBits == 0; the 5-power overflow check is trivially true).
    if (-21..=62).contains(&bin_exp) && n_tiny_bits == 0 {
        let insignificant = if bin_exp > n_significant_bits {
            FD_INSIGNIFICANT_DIGITS[(bin_exp - n_significant_bits - 1) as usize]
        } else {
            0
        };
        let lvalue = if bin_exp >= 52 {
            fract_bits << (bin_exp - 52)
        } else {
            fract_bits >> (52 - bin_exp)
        };
        return fd_develop_long_digits(0, lvalue as i64, insignificant);
    }

    // The hard case: d = (B / S) * 10^decExp with 1 <= B/S < 10, and
    // M = scaled (1/2) ULP of d.
    let mut dec_exp = fd_estimate_dec_exp(fract_bits, bin_exp);
    let b5 = (-dec_exp).max(0);
    let mut b2 = b5 + n_tiny_bits + bin_exp;
    let s5 = dec_exp.max(0);
    let mut s2 = s5 + n_tiny_bits;
    let m5 = b5;
    let mut m2 = b2 - n_significant_bits;
    let fract_reduced = fract_bits >> tail_zeros;
    b2 -= n_fract_bits - 1;
    let common2 = b2.min(s2);
    b2 -= common2;
    s2 -= common2;
    m2 -= common2;
    // For exact powers of two, the next smallest number is only half as far
    // away, so halve M.
    if n_fract_bits == 1 {
        m2 -= 1;
    }
    if m2 < 0 {
        // Cannot scale M down far enough: scale the other values up instead.
        b2 -= m2;
        s2 -= m2;
        m2 = 0;
    }

    let b_bits = n_fract_bits + b2 + fd_n5_bits(b5);
    let ten_s_bits = s2 + 1 + fd_n5_bits(s5 + 1);
    if b_bits < 64 && ten_s_bits < 64 {
        if b_bits < 32 && ten_s_bits < 32 {
            fd_dtoa_native!(i32, fract_reduced, b5, b2, s5, s2, m5, m2, dec_exp)
        } else {
            fd_dtoa_native!(i64, fract_reduced, b5, b2, s5, s2, m5, m2, dec_exp)
        }
    } else {
        // FDBigInteger path, with exact arithmetic. NB: unlike the native
        // paths, `high` here is a NON-strict comparison (addAndCmp <= 0).
        let mut b = big_from_u64(fract_reduced);
        big_mul_pow(&mut b, 5, b5 as u32);
        big_mul_pow(&mut b, 2, b2 as u32);
        let mut s = big_from_u64(1);
        big_mul_pow(&mut s, 5, s5 as u32);
        big_mul_pow(&mut s, 2, s2 as u32);
        let mut m = big_from_u64(1);
        big_mul_pow(&mut m, 5, m5 as u32);
        big_mul_pow(&mut m, 2, m2 as u32);
        let mut tens = s.clone();
        df_mul_small(&mut tens, 10);

        let mut digits: Vec<u8> = Vec::with_capacity(20);
        let mut q = big_quo_rem10(&mut b, &s);
        df_mul_small(&mut m, 10);
        let mut low = big_cmp(&b, &m) == std::cmp::Ordering::Less;
        let mut high = big_add_cmp(&b, &m, &tens) != std::cmp::Ordering::Less;
        if q == 0 && !high {
            dec_exp -= 1;
        } else {
            digits.push(b'0' + q);
        }
        if dec_exp < -3 || dec_exp >= 8 {
            low = false;
            high = false;
        }
        while !low && !high {
            q = big_quo_rem10(&mut b, &s);
            df_mul_small(&mut m, 10);
            low = big_cmp(&b, &m) == std::cmp::Ordering::Less;
            high = big_add_cmp(&b, &m, &tens) != std::cmp::Ordering::Less;
            digits.push(b'0' + q);
        }
        let exact = b.is_empty();
        let mut dec_exponent = dec_exp + 1;
        let mut rounded_up = false;
        if high {
            if low {
                df_mul_small(&mut b, 2);
                match big_cmp(&b, &tens) {
                    std::cmp::Ordering::Equal => {
                        if digits.last().map_or(false, |d| (d - b'0') % 2 != 0) {
                            fd_roundup(&mut digits, &mut dec_exponent, &mut rounded_up);
                        }
                    }
                    std::cmp::Ordering::Greater => {
                        fd_roundup(&mut digits, &mut dec_exponent, &mut rounded_up);
                    }
                    std::cmp::Ordering::Less => {}
                }
            } else {
                fd_roundup(&mut digits, &mut dec_exponent, &mut rounded_up);
            }
        }
        (digits, dec_exponent, rounded_up, exact)
    }
}

// Little-endian decimal-digit big integers (empty vector = zero), used only
// by the FDBigInteger path above. Sizes stay below ~800 digits.

fn big_from_u64(mut v: u64) -> Vec<u8> {
    let mut d = Vec::new();
    while v > 0 {
        d.push((v % 10) as u8);
        v /= 10;
    }
    d
}

fn big_mul_pow(v: &mut Vec<u8>, factor: u32, times: u32) {
    for _ in 0..times {
        df_mul_small(v, factor);
    }
}

fn big_cmp(a: &[u8], b: &[u8]) -> std::cmp::Ordering {
    if a.len() != b.len() {
        return a.len().cmp(&b.len());
    }
    for i in (0..a.len()).rev() {
        if a[i] != b[i] {
            return a[i].cmp(&b[i]);
        }
    }
    std::cmp::Ordering::Equal
}

/// Ordering of (a + m) versus tens.
fn big_add_cmp(a: &[u8], m: &[u8], tens: &[u8]) -> std::cmp::Ordering {
    let mut sum = Vec::with_capacity(a.len().max(m.len()) + 1);
    let mut carry = 0u8;
    for i in 0..a.len().max(m.len()) {
        let t = a.get(i).copied().unwrap_or(0) + m.get(i).copied().unwrap_or(0) + carry;
        sum.push(t % 10);
        carry = t / 10;
    }
    if carry > 0 {
        sum.push(carry);
    }
    while sum.last() == Some(&0) {
        sum.pop();
    }
    big_cmp(&sum, tens)
}

/// `FDBigInteger.quoRemIteration`: returns floor(b / s) (a single decimal
/// digit) and replaces b with (b % s) * 10.
fn big_quo_rem10(b: &mut Vec<u8>, s: &[u8]) -> u8 {
    let mut q = 0u8;
    while big_cmp(b, s) != std::cmp::Ordering::Less {
        // b -= s
        let mut borrow = 0i8;
        for i in 0..b.len() {
            let mut t = b[i] as i8 - s.get(i).copied().unwrap_or(0) as i8 - borrow;
            if t < 0 {
                t += 10;
                borrow = 1;
            } else {
                borrow = 0;
            }
            b[i] = t as u8;
        }
        while b.last() == Some(&0) {
            b.pop();
        }
        q += 1;
    }
    df_mul_small(b, 10);
    q
}

/// Multiply a little-endian decimal digit vector by a small factor.
fn df_mul_small(v: &mut Vec<u8>, factor: u32) {
    let mut carry = 0u32;
    for d in v.iter_mut() {
        let t = (*d as u32) * factor + carry;
        *d = (t % 10) as u8;
        carry = t / 10;
    }
    while carry > 0 {
        v.push((carry % 10) as u8);
        carry /= 10;
    }
}

/// Port of `DecimalFormat.format(long)`. jsonata-java stores integral
/// numbers as Integer/Long (`Utils.convertNumber`), so they reach
/// DecimalFormat through the exact-digits long path (`isInteger = true`).
fn decimal_format_long(number: i64, st: &DfPattern, sym: &DfSymbols) -> String {
    let is_negative = number < 0;
    // The multiplier (100/1000) can overflow a long; Java falls back to
    // BigInteger there. i128 covers both paths with identical digits.
    let v = (number as i128).abs() * st.multiplier as i128;

    let mut dl = DigitList::new();
    dl.set_long_i128(
        v,
        if st.use_exponential {
            st.max_int.saturating_add(st.max_frac)
        } else {
            0
        },
    );

    let mut result = String::new();
    result.push_str(if is_negative {
        &st.negative_prefix
    } else {
        &st.positive_prefix
    });
    subformat_number(&mut result, &mut dl, st, sym, true);
    result.push_str(if is_negative {
        &st.negative_suffix
    } else {
        &st.positive_suffix
    });
    result
}

/// Port of `DecimalFormat.format(double)` (+ `subformat`).
fn decimal_format_double(x: f64, st: &DfPattern, sym: &DfSymbols) -> String {
    // handleNaN
    if x.is_nan() || (x.is_infinite() && st.multiplier == 0) {
        return sym.nan.clone();
    }
    let is_negative = ((x < 0.0) || (x == 0.0 && x.is_sign_negative())) ^ (st.multiplier < 0);
    let mut number = x;
    if st.multiplier != 1 {
        number *= st.multiplier as f64;
    }

    let mut result = String::new();
    // handleInfinity
    if number.is_infinite() {
        result.push_str(if is_negative {
            &st.negative_prefix
        } else {
            &st.positive_prefix
        });
        result.push_str(&sym.infinity);
        result.push_str(if is_negative {
            &st.negative_suffix
        } else {
            &st.positive_suffix
        });
        return result;
    }
    if is_negative {
        number = -number;
    }

    let mut dl = DigitList::new();
    dl.set_double(
        number,
        if st.use_exponential {
            st.max_int.saturating_add(st.max_frac)
        } else {
            st.max_frac
        },
        !st.use_exponential,
    );

    result.push_str(if is_negative {
        &st.negative_prefix
    } else {
        &st.positive_prefix
    });
    subformat_number(&mut result, &mut dl, st, sym, false);
    result.push_str(if is_negative {
        &st.negative_suffix
    } else {
        &st.positive_suffix
    });
    result
}

/// Port of `DecimalFormat.subformatNumber` (isInteger = false).
fn subformat_number(
    result: &mut String,
    dl: &mut DigitList,
    st: &DfPattern,
    sym: &DfSymbols,
    is_integer: bool,
) {
    let grouping = if st.is_currency_format {
        sym.monetary_grouping_separator
    } else {
        sym.grouping_separator
    };
    let zero = sym.zero_digit;
    let dchar = |d: u8| char::from_u32(zero as u32 + (d - b'0') as u32).unwrap_or(zero);
    let decimal = if st.is_currency_format {
        sym.monetary_decimal_separator
    } else {
        sym.decimal_separator
    };

    if dl.is_zero() {
        dl.decimal_at = 0; // Normalize
    }

    if st.use_exponential {
        // Minimum integer digits are handled by adjusting the exponent;
        // maximum integer digits > minimum define a repeating range
        // (engineering notation).
        let mut exponent = dl.decimal_at;
        let repeat = st.max_int;
        let mut minimum_integer_digits = st.min_int;
        if repeat > 1 && repeat > st.min_int {
            if exponent >= 1 {
                exponent = ((exponent - 1) / repeat) * repeat;
            } else {
                // integer division rounds towards 0
                exponent = ((exponent - repeat) / repeat) * repeat;
            }
            minimum_integer_digits = 1;
        } else {
            exponent -= minimum_integer_digits;
        }

        let mut minimum_digits = st.min_int + st.min_frac;
        let integer_digits = if dl.is_zero() {
            minimum_integer_digits
        } else {
            dl.decimal_at - exponent
        };
        if minimum_digits < integer_digits {
            minimum_digits = integer_digits;
        }
        let mut total_digits = dl.count as i32;
        if minimum_digits > total_digits {
            total_digits = minimum_digits;
        }

        for i in 0..total_digits {
            if i == integer_digits {
                result.push(decimal);
            }
            result.push(if (i as usize) < dl.count {
                dchar(dl.digits[i as usize])
            } else {
                zero
            });
        }
        if st.decimal_separator_always_shown && total_digits == integer_digits {
            result.push(decimal);
        }

        result.push(sym.exponent_separator);

        // For zero values the exponent is forced to zero.
        if dl.is_zero() {
            exponent = 0;
        }
        let negative_exponent = exponent < 0;
        if negative_exponent {
            exponent = -exponent;
            result.push(sym.minus_sign);
        }
        dl.set_long(exponent as i64);
        for _ in dl.decimal_at..st.min_exponent_digits {
            result.push(zero);
        }
        for i in 0..dl.decimal_at {
            result.push(if (i as usize) < dl.count {
                dchar(dl.digits[i as usize])
            } else {
                zero
            });
        }
    } else {
        // Output the integer portion.
        let mut count = st.min_int;
        let mut digit_index = 0i32;
        if dl.decimal_at > 0 && count < dl.decimal_at {
            count = dl.decimal_at;
        }
        // If max integer digits is smaller than the real number of integer
        // digits, output the least significant ones.
        if count > st.max_int {
            count = st.max_int;
            digit_index = dl.decimal_at - count;
        }
        let size_before_integer_part = result.len();
        let mut i = count - 1;
        while i >= 0 {
            if i < dl.decimal_at && digit_index < dl.count as i32 {
                result.push(dchar(dl.digits[digit_index as usize]));
                digit_index += 1;
            } else {
                result.push(zero);
            }
            if st.grouping_used && i > 0 && st.grouping_size != 0 && i % st.grouping_size == 0 {
                result.push(grouping);
            }
            i -= 1;
        }

        let fraction_present = st.min_frac > 0 || (!is_integer && digit_index < dl.count as i32);
        if !fraction_present && result.len() == size_before_integer_part {
            result.push(zero);
        }
        if st.decimal_separator_always_shown || fraction_present {
            result.push(decimal);
        }

        for i in 0..st.max_frac {
            if i >= st.min_frac && (is_integer || digit_index >= dl.count as i32) {
                break;
            }
            // Leading fractional zeros (|number| < 1.0).
            if -1 - i > dl.decimal_at - 1 {
                result.push(zero);
                continue;
            }
            if !is_integer && digit_index < dl.count as i32 {
                result.push(dchar(dl.digits[digit_index as usize]));
                digit_index += 1;
            } else {
                result.push(zero);
            }
        }
    }
}

/// Java: `public static String formatNumber(Number value, String picture, Map options)`
pub fn format_number(args: &[JValue]) -> JResult<JValue> {
    let value = crate::functions::arg(args, 0);
    // undefined inputs always return undefined
    if value.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let num = value.as_f64().unwrap_or(f64::NAN);

    let picture = match crate::functions::arg(args, 1) {
        JValue::String(s) => s.to_string(),
        other => other.as_str().map(|s| s.to_string()).unwrap_or_default(),
    };

    // Java pre-checks (on the raw picture, before any rewriting).
    if picture.contains(",,") {
        // "The sub-picture must not contain two adjacent instances of the
        // 'grouping-separator' character"
        return Err(JError::at("D3089", -1));
    }
    if picture.contains('%') && picture.contains('e') {
        // "A sub-picture that contains a 'percent' or 'per-mille' character
        // must not contain a character treated as an 'exponent-separator'"
        return Err(JError::at("D3092", -1));
    }

    let mut sym = DfSymbols::locale_us();
    let options = crate::functions::arg(args, 2);
    if let Some(obj) = options.as_object() {
        process_options_arg(obj, &mut sym)?;
    }

    // fixedPicture: digits 1-9 become 0; a lowercase exponent is folded to
    // 'E' for DecimalFormat and restored in the result.
    let mut fixed: String = picture
        .chars()
        .map(|c| if matches!(c, '1'..='9') { '0' } else { c })
        .collect();
    let little_e = fixed.contains('e');
    if little_e {
        fixed = fixed.replace('e', "E");
    }

    let st = apply_localized_pattern(&fixed, &sym)?;
    // jsonata-java's Utils.convertNumber turns any number with
    // `longValue() == doubleValue()` into an Integer/Long, which DecimalFormat
    // formats through the exact long path (note: `num as i64` saturates like
    // Java's `Number.longValue()`).
    let as_long = num as i64;
    let mut result = if (as_long as f64) == num {
        decimal_format_long(as_long, &st, &sym)
    } else {
        decimal_format_double(num, &st, &sym)
    };
    if little_e {
        result = result.replace('E', "e");
    }
    Ok(JValue::string(result))
}

// ---------------------------------------------------------------------------
// formatInteger / parseInteger
// ---------------------------------------------------------------------------

/// Java: `public static String formatInteger(Number value, String picture)`
pub fn format_integer(args: &[JValue]) -> JResult<JValue> {
    let value = crate::functions::arg(args, 0);
    if value.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let picture = crate::functions::arg(args, 1);
    let pic = picture.as_str().unwrap_or("");
    // DateTimeUtils.formatInteger(value.longValue(), picture)
    let v = double_to_long(value.as_f64().unwrap_or(f64::NAN));
    let s = crate::datetime::format_integer(v, pic)?;
    Ok(JValue::string(s))
}

/// Java: `public static Number parseInteger(String value, String picture)`
pub fn parse_integer(args: &[JValue]) -> JResult<JValue> {
    let value = crate::functions::arg(args, 0);
    if value.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let mut value: String = match value.as_str() {
        Some(s) => s.to_string(),
        None => return Ok(JValue::Undefined),
    };

    let picture_arg = crate::functions::arg(args, 1);
    let mut picture: Option<String> = picture_arg.as_str().map(|s| s.to_string());

    if let Some(p) = picture.clone() {
        let mut p = p;
        // Java: if (picture.equals("#")) throw ParseException(... "#" ...)
        if p == "#" {
            // Java surfaces ParseException; the test suite expects D3130.
            return Err(JError::with_current("D3130", -1, JValue::string("#")));
        }
        // if (picture.endsWith(";o")) picture = picture.substring(0, len-2);
        if p.ends_with(";o") {
            p.truncate(p.len() - 2);
        }
        if p == "a" {
            return Ok(JValue::Number(
                crate::datetime::letters_to_decimal(&value, 'a') as f64,
            ));
        }
        if p == "A" {
            return Ok(JValue::Number(
                crate::datetime::letters_to_decimal(&value, 'A') as f64,
            ));
        }
        if p == "i" {
            return Ok(JValue::Number(
                crate::datetime::roman_to_decimal(&value.to_uppercase()) as f64,
            ));
        }
        if p == "I" {
            return Ok(JValue::Number(
                crate::datetime::roman_to_decimal(&value) as f64
            ));
        }
        if p == "w" {
            return Ok(JValue::Number(crate::datetime::words_to_long(&value) as f64));
        }
        if p == "W" || p == "wW" || p == "Ww" {
            return Ok(JValue::Number(
                crate::datetime::words_to_long(&value.to_lowercase()) as f64,
            ));
        }
        if p.contains(':') {
            value = value.replace(':', ",");
            p = p.replace(':', ",");
        }
        picture = Some(p);
    }

    // DecimalFormat(picture).parse(value) — for numeric pictures.
    match decimal_format_parse(picture.as_deref(), &value) {
        Ok(Some(n)) => Ok(JValue::Number(n)),
        // Java: parse failure (ParseException) -> return null (Undefined).
        Ok(None) => Ok(JValue::Undefined),
        // Java: IllegalArgumentException on a malformed picture -> ParseException
        // "...is not supported by this implementation" (test suite: D3130).
        Err(picture_str) => Err(JError::with_current(
            "D3130",
            -1,
            JValue::string(picture_str),
        )),
    }
}

// ===========================================================================
// Helpers: BigDecimal-style HALF_EVEN rounding on the decimal string
// ===========================================================================

/// Parse a numeric string (possibly in `dddd`, `d.ddd`, or `d.ddde±NN`
/// scientific form produced by `number_to_string`) into (negative, digits,
/// scale) where value = (-1)^neg * digits * 10^(-scale). `digits` has no
/// leading-zero significance constraints; it is the full digit run.
fn parse_decimal(s: &str) -> (bool, Vec<u8>, i32) {
    let mut chars = s.chars().peekable();
    let mut negative = false;
    if let Some(&c) = chars.peek() {
        if c == '-' {
            negative = true;
            chars.next();
        } else if c == '+' {
            chars.next();
        }
    }

    let mut int_part = String::new();
    let mut frac_part = String::new();
    let mut exp_part = String::new();
    let mut in_frac = false;
    let mut in_exp = false;
    for c in chars {
        match c {
            '.' if !in_exp => in_frac = true,
            'e' | 'E' => in_exp = true,
            _ if in_exp => exp_part.push(c),
            _ if in_frac => frac_part.push(c),
            _ => int_part.push(c),
        }
    }

    let exp: i32 = exp_part.parse().unwrap_or(0);

    // unscaled digit run = int_part + frac_part, scale = frac_part.len() - exp
    let mut digits: Vec<u8> = Vec::new();
    for c in int_part.bytes() {
        digits.push(c - b'0');
    }
    for c in frac_part.bytes() {
        digits.push(c - b'0');
    }
    let scale = frac_part.len() as i32 - exp;
    (negative, digits, scale)
}

/// Replicate `new BigDecimal(s).setScale(new_scale, HALF_EVEN).doubleValue()`.
fn big_decimal_set_scale_half_even(s: &str, new_scale: i32) -> f64 {
    let (negative, mut digits, scale) = parse_decimal(s);

    if digits.is_empty() {
        digits.push(0);
    }

    // We have value = digits * 10^(-scale). We want to round so the resulting
    // scale is new_scale (i.e. round at 10^(-new_scale)). Number of fractional
    // digits to drop = scale - new_scale.
    let drop = scale - new_scale;

    if drop <= 0 {
        // No rounding needed (we'd be adding zeros). Just reconstruct.
        return reconstruct_double(negative, &digits, scale);
    }

    let drop = drop as usize;
    if drop >= digits.len() {
        // All significant digits are dropped; need to consider the leading
        // dropped digit for rounding into a possible carry.
        // Pad with leading zeros so we can inspect.
        let pad = drop - digits.len() + 1;
        let mut padded = vec![0u8; pad];
        padded.extend_from_slice(&digits);
        digits = padded;
    }

    let keep_len = digits.len() - drop;
    let round_digit = digits[keep_len];
    let mut kept: Vec<u8> = digits[..keep_len].to_vec();

    // Determine round-half-even.
    let mut round_up = false;
    if round_digit > 5 {
        round_up = true;
    } else if round_digit == 5 {
        // any nonzero digit after the round digit -> round up
        let rest_nonzero = digits[keep_len + 1..].iter().any(|&d| d != 0);
        if rest_nonzero {
            round_up = true;
        } else {
            // half: round to even
            let last_kept = *kept.last().unwrap_or(&0);
            if last_kept % 2 == 1 {
                round_up = true;
            }
        }
    }

    if round_up {
        // increment kept by 1
        let mut i = kept.len();
        loop {
            if i == 0 {
                kept.insert(0, 1);
                break;
            }
            i -= 1;
            if kept[i] == 9 {
                kept[i] = 0;
            } else {
                kept[i] += 1;
                break;
            }
        }
    }

    if kept.is_empty() {
        kept.push(0);
    }

    // Resulting value = kept * 10^(-new_scale)
    reconstruct_double(negative, &kept, new_scale)
}

/// value = (-1)^neg * digits * 10^(-scale) as an f64, via string round-trip so
/// the decimal value parses to the nearest double (mirrors BigDecimal.doubleValue).
fn reconstruct_double(negative: bool, digits: &[u8], scale: i32) -> f64 {
    let digit_str: String = digits.iter().map(|d| (d + b'0') as char).collect();
    let digit_str = if digit_str.is_empty() {
        "0".to_string()
    } else {
        digit_str
    };
    // Build a plain decimal string with the given scale.
    let s = if scale <= 0 {
        // append (-scale) zeros
        let zeros = "0".repeat((-scale) as usize);
        format!("{}{}", digit_str, zeros)
    } else {
        let scale_u = scale as usize;
        if digit_str.len() > scale_u {
            let point = digit_str.len() - scale_u;
            format!("{}.{}", &digit_str[..point], &digit_str[point..])
        } else {
            let lead = "0".repeat(scale_u - digit_str.len());
            format!("0.{}{}", lead, digit_str)
        }
    };
    let mut v: f64 = s.parse().unwrap_or(0.0);
    if negative && v != 0.0 {
        v = -v;
    } else if negative && v == 0.0 {
        // Java BigDecimal.doubleValue() of a negative zero magnitude yields
        // 0.0 (no negative zero from BigDecimal); JSONata expects 0 for
        // $round(-0.5) etc.
        v = 0.0;
    }
    v
}

/// Java `Number.longValue()` — truncate toward zero, saturating cast.
fn double_to_long(d: f64) -> i64 {
    if d.is_nan() {
        return 0;
    }
    if d >= 9_223_372_036_854_775_807.0 {
        i64::MAX
    } else if d <= -9_223_372_036_854_775_808.0 {
        i64::MIN
    } else {
        d as i64
    }
}

/// Java `Long.toString(value, radix)` for radix 2..36 (lowercase digits, leading
/// '-' for negatives).
fn long_to_string_radix(value: i64, radix: u32) -> String {
    if value == 0 {
        return "0".to_string();
    }
    const DIGITS: &[u8] = b"0123456789abcdefghijklmnopqrstuvwxyz";
    let negative = value < 0;
    // Work with i128 to handle i64::MIN magnitude.
    let mut n = (value as i128).unsigned_abs();
    let mut buf = Vec::new();
    while n > 0 {
        let d = (n % radix as u128) as usize;
        buf.push(DIGITS[d]);
        n /= radix as u128;
    }
    if negative {
        buf.push(b'-');
    }
    buf.reverse();
    String::from_utf8(buf).unwrap()
}

// ---------------------------------------------------------------------------
// DecimalFormat.parse — numeric pictures for $parseInteger
// ---------------------------------------------------------------------------

/// Parse `value` per a numeric DecimalFormat `picture`. Returns:
/// - Ok(Some(n)) on a successful parse
/// - Ok(None) when DecimalFormat.parse would fail (ParseException)
/// - Err(picture) when the picture is an illegal pattern (IllegalArgumentException)
fn decimal_format_parse(picture: Option<&str>, value: &str) -> Result<Option<f64>, String> {
    // Validate the picture as a DecimalFormat pattern (only the limited grammar
    // used by parseInteger). A picture like "#" alone or "xyz" — Java's
    // DecimalFormat would *accept* many of these (only some throw). We follow
    // the test expectations: numeric pictures with 0/#/,/. parse; otherwise we
    // attempt a best-effort numeric extraction.
    if let Some(p) = picture {
        // A picture without any digit symbol (e.g. "abc", or "999" left over
        // from "999;o") makes DecimalFormat treat the whole picture as a
        // literal prefix, which the value then fails to match — parse() throws
        // and Java's catch-all returns null (undefined). jsonata-js raises
        // D3130 for digitless pictures; see COMPAT.md.
        if !p.chars().any(|c| c == '0' || c == '#') {
            return Ok(None);
        }
    }

    // Java DecimalFormat.parse scans from the start, accepting an optional '-'
    // (the negative prefix — a leading '+' is NOT part of the default grammar
    // and fails the parse; jsonata-js accepts it, see COMPAT.md), digits, an
    // optional decimal part, stopping at the first unparseable char. Grouping
    // separators are consumed only when the picture enables grouping (contains
    // ','), or when there is no picture (the default DecimalFormat groups);
    // otherwise ',' terminates the scan: DecimalFormat("0").parse("1,234") -> 1.
    let grouping = match picture {
        None => true,
        Some(p) => p.contains(','),
    };
    let chars: Vec<char> = value.chars().collect();
    let mut i = 0usize;
    let n = chars.len();
    let mut out = String::new();
    let mut negative = false;

    if i < n && chars[i] == '-' {
        negative = true;
        i += 1;
    }

    let mut saw_digit = false;
    let mut saw_dot = false;
    while i < n {
        let c = chars[i];
        if c.is_ascii_digit() {
            out.push(c);
            saw_digit = true;
            i += 1;
        } else if c == ',' && grouping {
            i += 1;
        } else if c == '.' && !saw_dot {
            out.push('.');
            saw_dot = true;
            i += 1;
        } else {
            break;
        }
    }

    if !saw_digit {
        return Ok(None);
    }

    match out.parse::<f64>() {
        Ok(mut v) => {
            if negative {
                v = -v;
            }
            Ok(Some(v))
        }
        Err(_) => Ok(None),
    }
}

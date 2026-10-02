//! Port of `com.dashjoin.jsonata.utils.DateTimeUtils`.
//!
//! Faithful 1:1 port of the JSONata date/time, integer-formatting and
//! integer-parsing helpers. The Java source uses `java.time`; here we use
//! `chrono` for the calendar arithmetic but re-implement the picture-string
//! parsing / formatting exactly as Java does.
//!
//! Error handling: Java throws `RuntimeException` for the picture-string error
//! conditions (these map to JSONata error codes D3133-D3148 in the engine).
//! Since the original uses bare `RuntimeException(message)` with a dynamic
//! message string (the JSONata error codes D3137/D3141 use the `{{{message}}}`
//! template, meaning the message text *is* the argument), we represent every
//! such throw as a [`JError`] whose `.error` is the JSONata code and whose
//! `.current` carries the dynamic message string. See [`runtime_err`].
//!
//! PORT-NOTE: The Java `Constants.ERR_MSG_*` strings are formatted with
//! `String.format(...)` to produce the human-readable message. We reproduce
//! those exact strings here and stash them as the dynamic message.

use crate::error::{JError, JResult};
use crate::value::JValue;

use chrono::{DateTime, Datelike, Duration, TimeZone, Timelike, Utc};

// ---------------------------------------------------------------------------
// Error-message constants (Constants.java) and error construction
// ---------------------------------------------------------------------------

// Java: Constants.ERR_MSG_SEQUENCE_UNSUPPORTED
const ERR_MSG_SEQUENCE_UNSUPPORTED: &str =
    "Formatting or parsing an integer as a sequence starting with %s is not supported by this implementation";
// Java: Constants.ERR_MSG_DIFF_DECIMAL_GROUP
const ERR_MSG_DIFF_DECIMAL_GROUP: &str =
    "In a decimal digit pattern, all digits must be from the same decimal group";
// Java: Constants.ERR_MSG_NO_CLOSING_BRACKET
const ERR_MSG_NO_CLOSING_BRACKET: &str =
    "No matching closing bracket ']' in date/time picture string";
// Java: Constants.ERR_MSG_UNKNOWN_COMPONENT_SPECIFIER
const ERR_MSG_UNKNOWN_COMPONENT_SPECIFIER: &str =
    "Unknown component specifier %s in date/time picture string";
// Java: Constants.ERR_MSG_INVALID_NAME_MODIFIER
const ERR_MSG_INVALID_NAME_MODIFIER: &str =
    "The 'name' modifier can only be applied to months and days in the date/time picture string, not %s";
// Java: Constants.ERR_MSG_TIMEZONE_FORMAT
const ERR_MSG_TIMEZONE_FORMAT: &str =
    "The timezone integer format specifier cannot have more than four digits";
// Java: Constants.ERR_MSG_MISSING_FORMAT
const ERR_MSG_MISSING_FORMAT: &str =
    "The date/time picture string is missing specifiers required to parse the timestamp";

/// Build a [`JError`] mirroring Java `throw new RuntimeException(message)` from
/// `DateTimeUtils`. The JSONata engine wraps these as D-codes whose template is
/// `{{{message}}}` (the message text is the substituted argument), notably
/// D3137 (generic format error) and D3141 (generic parse error). We attach the
/// JSONata code as `.error` and stash the dynamic human-readable message in
/// `.current`.
///
/// PORT-NOTE: `DateTimeUtils` itself only ever throws `RuntimeException` with a
/// message; the mapping to a specific D-code happens in the calling Functions
/// layer (`$fromMillis`/`$toMillis` use D3137, `$toMillis` parse uses D3141).
/// To keep this module self-contained and faithful to the *observable* message,
/// we default the formatting-side throws to "D3137" and the parsing-side throws
/// to "D3141"; the dynamic message is the load-bearing, test-validated part.
fn runtime_err(code: &str, message: String) -> JError {
    JError {
        error: code.to_string(),
        location: 0,
        current: Some(JValue::string(message)),
        expected: None,
        error_type: None,
    }
}

fn format_err(message: String) -> JError {
    runtime_err("D3137", message)
}

/// A marker whose presentation has no numeric format (e.g. `[fn]`) reaching a
/// numeric formatting path — Java hits a NullPointerException here.
fn require_int_fmt(f: &Option<Format>) -> JResult<&Format> {
    f.as_ref().ok_or_else(|| {
        format_err("Unsupported presentation modifier in date/time picture string".to_string())
    })
}

fn parse_err(message: String) -> JError {
    runtime_err("D3141", message)
}

// ---------------------------------------------------------------------------
// Word / number tables
// ---------------------------------------------------------------------------

const FEW: [&str; 20] = [
    "Zero",
    "One",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Eleven",
    "Twelve",
    "Thirteen",
    "Fourteen",
    "Fifteen",
    "Sixteen",
    "Seventeen",
    "Eighteen",
    "Nineteen",
];
const ORDINALS: [&str; 20] = [
    "Zeroth",
    "First",
    "Second",
    "Third",
    "Fourth",
    "Fifth",
    "Sixth",
    "Seventh",
    "Eighth",
    "Ninth",
    "Tenth",
    "Eleventh",
    "Twelfth",
    "Thirteenth",
    "Fourteenth",
    "Fifteenth",
    "Sixteenth",
    "Seventeenth",
    "Eighteenth",
    "Nineteenth",
];
const DECADES: [&str; 9] = [
    "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety", "Hundred",
];
const MAGNITUDES: [&str; 4] = ["Thousand", "Million", "Billion", "Trillion"];

// ---------------------------------------------------------------------------
// numberToWords / lookup
// ---------------------------------------------------------------------------

/// Java: `public static String numberToWords(long value, boolean ordinal)`
pub fn number_to_words(value: i64, ordinal: bool) -> String {
    lookup(value, false, ordinal)
}

/// Java: `private static String lookup(long num, boolean prev, boolean ord)`
fn lookup(num: i64, prev: bool, ord: bool) -> String {
    let mut words: String;
    if num <= 19 {
        words = format!(
            "{}{}",
            if prev { " and " } else { "" },
            if ord {
                ORDINALS[num as usize]
            } else {
                FEW[num as usize]
            }
        );
    } else if num < 100 {
        let tens = (num / 10) as usize;
        let remainder = num % 10;
        words = format!("{}{}", if prev { " and " } else { "" }, DECADES[tens - 2]);
        if remainder > 0 {
            words += &format!("-{}", lookup(remainder, false, ord));
        } else if ord {
            // words = words.substring(0, words.length()-1) + "ieth"
            let trimmed = &words[..words.len() - 1];
            words = format!("{}ieth", trimmed);
        }
    } else if num < 1000 {
        let hundreds = (num / 100) as usize;
        let remainder = num % 100;
        words = format!("{}{} Hundred", if prev { ", " } else { "" }, FEW[hundreds]);
        if remainder > 0 {
            words += &lookup(remainder, true, ord);
        } else if ord {
            words += "th";
        }
    } else {
        // int mag = (int) Math.floor(Math.log10(num) / 3);
        let mut mag = ((num as f64).log10() / 3.0).floor() as i64;
        if mag > MAGNITUDES.len() as i64 {
            mag = MAGNITUDES.len() as i64; // the largest word
        }
        // long factor = (long)Math.pow(10, mag * 3);
        let factor = 10f64.powi((mag * 3) as i32) as i64;
        // int mant = (int) Math.floor(num / factor);
        // PORT-NOTE: Java `num / factor` is integer division (both long), then
        // floored (no-op for non-negative). num is non-negative here.
        let mant = num / factor;
        let remainder = num - mant * factor;
        words = format!(
            "{}{} {}",
            if prev { ", " } else { "" },
            lookup(mant, false, false),
            MAGNITUDES[(mag - 1) as usize]
        );
        if remainder > 0 {
            words += &lookup(remainder, true, ord);
        } else if ord {
            words += "th";
        }
    }
    words
}

// ---------------------------------------------------------------------------
// wordValues / wordValuesLong tables (built lazily, deterministic)
// ---------------------------------------------------------------------------

use std::collections::HashMap;
use std::sync::OnceLock;

fn word_values() -> &'static HashMap<String, i64> {
    static MAP: OnceLock<HashMap<String, i64>> = OnceLock::new();
    MAP.get_or_init(|| {
        // Java builds `wordValues` (Integer) — we only ever read it as i64; the
        // values fit in i32 anyway. This corresponds to the `wordValues` static
        // initializer block.
        let mut m: HashMap<String, i64> = HashMap::new();
        for (i, w) in FEW.iter().enumerate() {
            m.insert(w.to_lowercase(), i as i64);
        }
        for (i, w) in ORDINALS.iter().enumerate() {
            m.insert(w.to_lowercase(), i as i64);
        }
        for (i, w) in DECADES.iter().enumerate() {
            let lword = w.to_lowercase();
            let val = ((i as i64) + 2) * 10;
            m.insert(lword.clone(), val);
            // lword.substring(0, lword.length()-1) + "ieth"
            let key = format!("{}ieth", &lword[..lword.len() - 1]);
            m.insert(key, val);
        }
        m.insert("hundreth".to_string(), 100);
        for (i, w) in MAGNITUDES.iter().enumerate() {
            let lword = w.to_lowercase();
            let val = 10f64.powi(((i as i32) + 1) * 3) as i64;
            m.insert(lword.clone(), val);
            m.insert(format!("{}th", lword), val);
        }
        m
    })
}

fn word_values_long() -> &'static HashMap<String, i64> {
    static MAP: OnceLock<HashMap<String, i64>> = OnceLock::new();
    MAP.get_or_init(|| {
        // Corresponds to the `wordValuesLong` static initializer block. It is
        // identical to wordValues except it adds "hundredth" -> 100.
        let mut m: HashMap<String, i64> = HashMap::new();
        for (i, w) in FEW.iter().enumerate() {
            m.insert(w.to_lowercase(), i as i64);
        }
        for (i, w) in ORDINALS.iter().enumerate() {
            m.insert(w.to_lowercase(), i as i64);
        }
        for (i, w) in DECADES.iter().enumerate() {
            let lword = w.to_lowercase();
            let val = ((i as i64) + 2) * 10;
            m.insert(lword.clone(), val);
            let key = format!("{}ieth", &lword[..lword.len() - 1]);
            m.insert(key, val);
        }
        m.insert("hundredth".to_string(), 100);
        m.insert("hundreth".to_string(), 100);
        for (i, w) in MAGNITUDES.iter().enumerate() {
            let lword = w.to_lowercase();
            let val = 10f64.powi(((i as i32) + 1) * 3) as i64;
            m.insert(lword.clone(), val);
            m.insert(format!("{}th", lword), val);
        }
        m
    })
}

/// Split text on the Java regex `,\s|\sand\s|[\s\-]` (comma+space, " and ",
/// or any single whitespace/hyphen). Java `String.split` with this pattern.
///
/// PORT-NOTE: Java `String.split(regex)` with default limit drops *trailing*
/// empty strings but keeps leading/intermediate empties. We replicate that
/// (`split` semantics with trailing-empty removal).
fn split_words(text: &str) -> Vec<String> {
    // Build the alternation manually: ", " | " and " | single [ \t\n...|-]
    // We scan and split. Because the alternatives can overlap, mimic Java's
    // leftmost-longest-by-alternation-order matching: Java's regex engine is
    // leftmost match, and among alternatives at a position it tries them in
    // order (NFA), so ",\s" before "\sand\s" before "[\s\-]".
    let chars: Vec<char> = text.chars().collect();
    let mut result: Vec<String> = Vec::new();
    let mut cur = String::new();
    let mut i = 0;
    let n = chars.len();
    while i < n {
        // Try ",\s"
        if chars[i] == ',' && i + 1 < n && chars[i + 1].is_whitespace() {
            result.push(std::mem::take(&mut cur));
            i += 2;
            continue;
        }
        // Try "\sand\s"
        if chars[i].is_whitespace()
            && i + 4 < n
            && chars[i + 1] == 'a'
            && chars[i + 2] == 'n'
            && chars[i + 3] == 'd'
            && chars[i + 4].is_whitespace()
        {
            result.push(std::mem::take(&mut cur));
            i += 5;
            continue;
        }
        // Try "[\s\-]" (single whitespace or hyphen)
        if chars[i].is_whitespace() || chars[i] == '-' {
            result.push(std::mem::take(&mut cur));
            i += 1;
            continue;
        }
        cur.push(chars[i]);
        i += 1;
    }
    result.push(cur);
    // Java split drops trailing empty strings.
    while matches!(result.last(), Some(s) if s.is_empty()) {
        result.pop();
    }
    result
}

/// Java: `public static int wordsToNumber(String text)`
pub fn words_to_number(text: &str) -> i32 {
    let parts = split_words(text);
    let wv = word_values();
    // values[i] = wordValues.get(parts[i]); — may be null in Java; a null
    // would NPE on `value < 100`. We replicate by treating a missing key as a
    // panic-equivalent; but to stay total we use 0 only if absent is impossible
    // in valid inputs. PORT-NOTE: invalid words would NPE in Java.
    let mut segs: Vec<i32> = Vec::new();
    segs.push(0);
    for part in &parts {
        let value = *wv.get(part).unwrap_or(&0) as i32;
        if value < 100 {
            let mut top = segs.pop().unwrap();
            if top >= 1000 {
                segs.push(top);
                top = 0;
            }
            segs.push(top + value);
        } else {
            let t = segs.pop().unwrap();
            segs.push(t * value);
        }
    }
    segs.iter().sum()
}

/// Java: `public static long wordsToLong(String text)`
pub fn words_to_long(text: &str) -> i64 {
    let parts = split_words(text);
    let wv = word_values_long();
    let mut segs: Vec<i64> = Vec::new();
    segs.push(0);
    for part in &parts {
        let value = *wv.get(part).unwrap_or(&0);
        if value < 100 {
            let mut top = segs.pop().unwrap();
            if top >= 1000 {
                segs.push(top);
                top = 0;
            }
            segs.push(top + value);
        } else {
            let t = segs.pop().unwrap();
            segs.push(t * value);
        }
    }
    segs.iter().sum()
}

// ---------------------------------------------------------------------------
// Roman numerals
// ---------------------------------------------------------------------------

struct RomanNumeral {
    value: i32,
    letters: &'static str,
}

const ROMAN_NUMERALS: [RomanNumeral; 13] = [
    RomanNumeral {
        value: 1000,
        letters: "m",
    },
    RomanNumeral {
        value: 900,
        letters: "cm",
    },
    RomanNumeral {
        value: 500,
        letters: "d",
    },
    RomanNumeral {
        value: 400,
        letters: "cd",
    },
    RomanNumeral {
        value: 100,
        letters: "c",
    },
    RomanNumeral {
        value: 90,
        letters: "xc",
    },
    RomanNumeral {
        value: 50,
        letters: "l",
    },
    RomanNumeral {
        value: 40,
        letters: "xl",
    },
    RomanNumeral {
        value: 10,
        letters: "x",
    },
    RomanNumeral {
        value: 9,
        letters: "ix",
    },
    RomanNumeral {
        value: 5,
        letters: "v",
    },
    RomanNumeral {
        value: 4,
        letters: "iv",
    },
    RomanNumeral {
        value: 1,
        letters: "i",
    },
];

fn roman_value(digit: char) -> Option<i32> {
    // Java: createRomanValues() map M/D/C/L/X/V/I
    match digit {
        'M' => Some(1000),
        'D' => Some(500),
        'C' => Some(100),
        'L' => Some(50),
        'X' => Some(10),
        'V' => Some(5),
        'I' => Some(1),
        _ => None,
    }
}

/// Java: `private static String decimalToRoman(int value)`
fn decimal_to_roman(value: i32) -> String {
    for numeral in ROMAN_NUMERALS.iter() {
        if value >= numeral.value {
            return format!(
                "{}{}",
                numeral.letters,
                decimal_to_roman(value - numeral.value)
            );
        }
    }
    String::new()
}

/// Java: `public static int romanToDecimal(String roman)`
pub fn roman_to_decimal(roman: &str) -> i32 {
    let mut decimal = 0;
    let mut max = 1;
    let chars: Vec<char> = roman.chars().collect();
    for i in (0..chars.len()).rev() {
        let value = roman_value(chars[i]).unwrap_or(0);
        if value < max {
            decimal -= value;
        } else {
            max = value;
            decimal += value;
        }
    }
    decimal
}

/// Java: `private static String decimalToLetters(int value, String aChar)`
fn decimal_to_letters(mut value: i32, a_char: char) -> String {
    let mut letters: Vec<char> = Vec::new();
    let a_code = a_char as u32;
    while value > 0 {
        // letters.insertElementAt(char((value-1)%26 + aCode), 0)
        let c = char::from_u32(((value - 1) % 26) as u32 + a_code).unwrap();
        letters.insert(0, c);
        value = (value - 1) / 26;
    }
    letters.into_iter().collect()
}

/// Java: `public static int lettersToDecimal(String letters, char aChar)`
pub fn letters_to_decimal(letters: &str, a_char: char) -> i32 {
    let mut decimal = 0i32;
    let chars: Vec<char> = letters.chars().collect();
    let len = chars.len();
    for i in 0..len {
        // Java: `decimal += (chars[len-i-1] - aChar + 1) * Math.pow(26, i)` —
        // the sum is computed in double and the compound assignment casts it
        // back to int, which SATURATES at +/-2^31 (jsonata-js keeps an
        // unclamped double; see COMPAT.md).
        let v = (chars[len - i - 1] as i32) - (a_char as i32) + 1;
        decimal = ((decimal as f64) + v as f64 * 26f64.powi(i as i32)) as i32;
    }
    decimal
}

// ---------------------------------------------------------------------------
// Format enums and structs
// ---------------------------------------------------------------------------

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
enum Formats {
    Decimal,
    Letters,
    Roman,
    Words,
    Sequence,
}

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
enum Tcase {
    Upper,
    Lower,
    Title,
}

#[derive(Clone)]
struct GroupingSeparator {
    position: i32,
    character: String,
}

/// Java: `private static class Format`
#[derive(Clone)]
struct Format {
    // `type` is always "integer", unused.
    primary: Formats,
    case_type: Tcase,
    ordinal: bool,
    zero_code: i32,
    mandatory_digits: i32,
    optional_digits: i32,
    regular: bool,
    grouping_separators: Vec<GroupingSeparator>,
    token: Option<String>,
}

impl Default for Format {
    fn default() -> Self {
        Format {
            primary: Formats::Decimal,
            case_type: Tcase::Lower,
            ordinal: false,
            zero_code: 0,
            mandatory_digits: 0,
            optional_digits: 0,
            regular: false,
            grouping_separators: Vec::new(),
            token: None,
        }
    }
}

fn suffix_123(last_digit: &str) -> Option<&'static str> {
    // Java: createSuffixMap() — "1"->"st", "2"->"nd", "3"->"rd"
    match last_digit {
        "1" => Some("st"),
        "2" => Some("nd"),
        "3" => Some("rd"),
        _ => None,
    }
}

// ---------------------------------------------------------------------------
// formatInteger
// ---------------------------------------------------------------------------

/// Java: `public static String formatInteger(long value, String picture)`
pub fn format_integer(value: i64, picture: &str) -> JResult<String> {
    let format = analyse_integer_picture(picture)?;
    format_integer_with(value, &format)
}

/// Left-pad `s` with `pad_char` to at least `size` chars (mirrors the use of
/// `Functions.leftPad(formattedInteger, mandatoryDigits, "0")`, which only ever
/// pads with a single "0" character here).
fn left_pad_zero(s: &str, size: i32) -> String {
    let len = s.chars().count() as i32;
    if size <= len {
        return s.to_string();
    }
    let pads = (size - len) as usize;
    let mut out = String::with_capacity(pads + s.len());
    for _ in 0..pads {
        out.push('0');
    }
    out.push_str(s);
    out
}

/// Java: `private static String formatInteger(long value, Format format)`
fn format_integer_with(value: i64, format: &Format) -> JResult<String> {
    let mut formatted_integer: String;
    let negative = value < 0;
    // Math.abs(value) — PORT-NOTE: i64::MIN.abs() overflows in Java too
    // (returns MIN); we use wrapping_abs to match.
    let value = value.wrapping_abs();
    match format.primary {
        Formats::Letters => {
            formatted_integer = decimal_to_letters(
                value as i32,
                if format.case_type == Tcase::Upper {
                    'A'
                } else {
                    'a'
                },
            );
        }
        Formats::Roman => {
            formatted_integer = decimal_to_roman(value as i32);
            if format.case_type == Tcase::Upper {
                formatted_integer = formatted_integer.to_uppercase();
            }
        }
        Formats::Words => {
            formatted_integer = number_to_words(value, format.ordinal);
            if format.case_type == Tcase::Upper {
                formatted_integer = formatted_integer.to_uppercase();
            } else if format.case_type == Tcase::Lower {
                formatted_integer = formatted_integer.to_lowercase();
            }
        }
        Formats::Decimal => {
            formatted_integer = format!("{}", value);
            let pad_length = format.mandatory_digits - formatted_integer.chars().count() as i32;
            if pad_length > 0 {
                formatted_integer = left_pad_zero(&formatted_integer, format.mandatory_digits);
            }
            if format.zero_code != 0x30 {
                // shift each char by (zeroCode - 0x30)
                let shifted: String = formatted_integer
                    .chars()
                    .map(|c| {
                        let nc = (c as i32) + format.zero_code - 0x30;
                        char::from_u32(nc as u32).unwrap_or(c)
                    })
                    .collect();
                formatted_integer = shifted;
            }
            if format.regular {
                let sep0 = &format.grouping_separators[0];
                let flen = formatted_integer.chars().count() as i32;
                let n = (flen - 1) / sep0.position;
                let mut i = n;
                while i > 0 {
                    let pos = formatted_integer.chars().count() as i32 - i * sep0.position;
                    formatted_integer =
                        insert_str_at_char(&formatted_integer, pos as usize, &sep0.character);
                    i -= 1;
                }
            } else {
                // Collections.reverse(format.groupingSeparators) — Java mutates
                // the format's list, then iterates. Since we own a clone, do the
                // same on a local reversed copy.
                let mut seps = format.grouping_separators.clone();
                seps.reverse();
                for separator in &seps {
                    let pos = formatted_integer.chars().count() as i32 - separator.position;
                    formatted_integer =
                        insert_str_at_char(&formatted_integer, pos as usize, &separator.character);
                }
            }

            if format.ordinal {
                let chars: Vec<char> = formatted_integer.chars().collect();
                let last_digit = chars[chars.len() - 1].to_string();
                let mut suffix = suffix_123(&last_digit);
                let len = chars.len();
                if suffix.is_none() || (len > 1 && chars[len - 2] == '1') {
                    suffix = Some("th");
                }
                formatted_integer += suffix.unwrap();
            }
        }
        Formats::Sequence => {
            // throw new RuntimeException(String.format(ERR_MSG_SEQUENCE_UNSUPPORTED, format.token));
            let token = format.token.clone().unwrap_or_default();
            return Err(format_err(
                ERR_MSG_SEQUENCE_UNSUPPORTED.replacen("%s", &token, 1),
            ));
        }
    }
    if negative {
        formatted_integer = format!("-{}", formatted_integer);
    }
    Ok(formatted_integer)
}

/// Insert `ins` into `s` at character index `char_pos` (0-based).
fn insert_str_at_char(s: &str, char_pos: usize, ins: &str) -> String {
    let mut byte_idx = s.len();
    for (count, (bi, _)) in s.char_indices().enumerate() {
        if count == char_pos {
            byte_idx = bi;
            break;
        }
    }
    let mut out = String::with_capacity(s.len() + ins.len());
    out.push_str(&s[..byte_idx]);
    out.push_str(ins);
    out.push_str(&s[byte_idx..]);
    out
}

// Java: decimalGroups
const DECIMAL_GROUPS: [i32; 37] = [
    0x30, 0x0660, 0x06F0, 0x07C0, 0x0966, 0x09E6, 0x0A66, 0x0AE6, 0x0B66, 0x0BE6, 0x0C66, 0x0CE6,
    0x0D66, 0x0DE6, 0x0E50, 0x0ED0, 0x0F20, 0x1040, 0x1090, 0x17E0, 0x1810, 0x1946, 0x19D0, 0x1A80,
    0x1A90, 0x1B50, 0x1BB0, 0x1C40, 0x1C50, 0xA620, 0xA8D0, 0xA900, 0xA9D0, 0xA9F0, 0xAA50, 0xABF0,
    0xFF10,
];

/// Java: `private static Format analyseIntegerPicture(String picture)`
fn analyse_integer_picture(picture: &str) -> JResult<Format> {
    let mut format = Format::default();
    let primary_format: String;
    // int semicolon = picture.lastIndexOf(";");
    let semicolon = picture.rfind(';');
    match semicolon {
        None => {
            primary_format = picture.to_string();
        }
        Some(semi) => {
            primary_format = picture[..semi].to_string();
            let format_modifier = &picture[semi + 1..];
            if format_modifier.chars().next() == Some('o') {
                format.ordinal = true;
            }
        }
    }

    match primary_format.as_str() {
        "A" => {
            format.case_type = Tcase::Upper;
            // fallthrough to 'a'
            format.primary = Formats::Letters;
        }
        "a" => {
            format.primary = Formats::Letters;
        }
        "I" => {
            format.case_type = Tcase::Upper;
            format.primary = Formats::Roman;
        }
        "i" => {
            format.primary = Formats::Roman;
        }
        "W" => {
            format.case_type = Tcase::Upper;
            format.primary = Formats::Words;
        }
        "Ww" => {
            format.case_type = Tcase::Title;
            format.primary = Formats::Words;
        }
        "w" => {
            format.primary = Formats::Words;
        }
        _ => {
            let mut zero_code: Option<i32> = None;
            let mut mandatory_digits = 0;
            let mut optional_digits = 0;
            let mut grouping_separators: Vec<GroupingSeparator> = Vec::new();
            let mut separator_position = 0;
            let format_codepoints: Vec<char> = primary_format.chars().collect();
            // for (int ix = len-1; ix >= 0; ix--)
            for ix in (0..format_codepoints.len()).rev() {
                let code_point = format_codepoints[ix] as i32;
                let mut digit = false;
                for &group in DECIMAL_GROUPS.iter() {
                    if code_point >= group && code_point <= group + 9 {
                        digit = true;
                        mandatory_digits += 1;
                        separator_position += 1;
                        if zero_code.is_none() {
                            zero_code = Some(group);
                        } else if Some(group) != zero_code {
                            // throw new RuntimeException(ERR_MSG_DIFF_DECIMAL_GROUP)
                            return Err(format_err(ERR_MSG_DIFF_DECIMAL_GROUP.to_string()));
                        }
                        break;
                    }
                }
                if !digit {
                    if code_point == 0x23 {
                        // '#'
                        separator_position += 1;
                        optional_digits += 1;
                    } else {
                        grouping_separators.push(GroupingSeparator {
                            position: separator_position,
                            character: format_codepoints[ix].to_string(),
                        });
                    }
                }
            }
            if mandatory_digits > 0 {
                format.primary = Formats::Decimal;
                format.zero_code = zero_code.unwrap();
                format.mandatory_digits = mandatory_digits;
                format.optional_digits = optional_digits;

                let regular = get_regular_repeat(&grouping_separators);
                if regular > 0 {
                    format.regular = true;
                    format.grouping_separators.push(GroupingSeparator {
                        position: regular,
                        character: grouping_separators[0].character.clone(),
                    });
                } else {
                    format.regular = false;
                    format.grouping_separators = grouping_separators;
                }
            } else {
                format.primary = Formats::Sequence;
                format.token = Some(primary_format.clone());
            }
        }
    }
    Ok(format)
}

fn gcd(a: i32, b: i32) -> i32 {
    // BigInteger.gcd semantics: non-negative result. Inputs here are positions
    // (positive). Use absolute values to be safe.
    let mut a = a.abs();
    let mut b = b.abs();
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    a
}

/// Java: `private static int getRegularRepeat(Vector<GroupingSeparator> separators)`
fn get_regular_repeat(separators: &[GroupingSeparator]) -> i32 {
    if separators.is_empty() {
        return 0;
    }
    let sep_char = &separators[0].character;
    for sep in &separators[1..] {
        if &sep.character != sep_char {
            return 0;
        }
    }
    let indexes: Vec<i32> = separators.iter().map(|s| s.position).collect();
    // factor = reduce(gcd)
    let factor = indexes.iter().copied().reduce(gcd).expect("non-empty");
    // for index in 1..=indexes.size(): if indexes.indexOf(index*factor) == -1 return 0
    for index in 1..=(indexes.len() as i32) {
        if !indexes.contains(&(index * factor)) {
            return 0;
        }
    }
    factor
}

// ---------------------------------------------------------------------------
// Date/time picture parsing
// ---------------------------------------------------------------------------

fn default_presentation_modifier(c: char) -> Option<&'static str> {
    // Java: createDefaultPresentationModifiers()
    match c {
        'Y' => Some("1"),
        'M' => Some("1"),
        'D' => Some("1"),
        'd' => Some("1"),
        'F' => Some("n"),
        'W' => Some("1"),
        'w' => Some("1"),
        'X' => Some("1"),
        'x' => Some("1"),
        'H' => Some("1"),
        'h' => Some("1"),
        'P' => Some("n"),
        'm' => Some("01"),
        's' => Some("01"),
        'f' => Some("1"),
        'Z' => Some("01:01"),
        'z' => Some("01:01"),
        'C' => Some("n"),
        'E' => Some("n"),
        _ => None,
    }
}

#[derive(Clone)]
// `presentation1` and `ordinal` mirror the Java `SpecPart` fields for
// structural fidelity; they are consumed during analysis and not re-read.
#[allow(dead_code)]
enum SpecPart {
    Literal {
        value: String,
    },
    Marker {
        component: char,
        // width pair (min, max)
        width: Option<(Option<i32>, Option<i32>)>,
        presentation1: Option<String>,
        presentation2: Option<char>,
        ordinal: bool,
        names: Option<Tcase>,
        integer_format: Option<Format>,
        n: i32,
    },
}

struct PictureFormat {
    parts: Vec<SpecPart>,
}

impl PictureFormat {
    fn new() -> Self {
        PictureFormat { parts: Vec::new() }
    }

    /// Java: `public void addLiteral(String picture, int start, int end)`
    /// Operates on char indices (Java substring is on UTF-16, but pictures are
    /// ASCII in practice; we use char indices for fidelity).
    fn add_literal(&mut self, picture_chars: &[char], start: usize, end: usize) {
        if end > start {
            let literal_str: String = picture_chars[start..end].iter().collect();
            let literal = if literal_str == "]]" {
                // special case where picture ends with ]]
                "]".to_string()
            } else {
                // String.join("]", literal.split("]]"))
                java_split_join(&literal_str, "]]", "]")
            };
            self.parts.push(SpecPart::Literal { value: literal });
        }
    }
}

/// Replicate Java `String.join(joiner, str.split(Pattern.quote-less regex))`
/// where the regex is a *literal* string `sep`. Java `split` here treats `sep`
/// as a regex but the seps used ("]]", grouping chars) are regex-literal-safe
/// in practice for this code path; we treat as literal and drop trailing empties.
fn java_split_join(s: &str, sep: &str, joiner: &str) -> String {
    let parts = java_split_literal(s, sep);
    parts.join(joiner)
}

/// Java `String.split` with a *literal* separator and default limit (trailing
/// empties removed). Splitting on an empty separator is not used here.
fn java_split_literal(s: &str, sep: &str) -> Vec<String> {
    if sep.is_empty() {
        return vec![s.to_string()];
    }
    let mut parts: Vec<String> = Vec::new();
    let mut rest = s;
    loop {
        match rest.find(sep) {
            Some(idx) => {
                parts.push(rest[..idx].to_string());
                rest = &rest[idx + sep.len()..];
            }
            None => {
                parts.push(rest.to_string());
                break;
            }
        }
    }
    // Drop trailing empty strings (Java default-limit behavior).
    while matches!(parts.last(), Some(p) if p.is_empty()) {
        parts.pop();
    }
    parts
}

/// Java: `private static Integer parseWidth(String wm)`
fn parse_width(wm: Option<&str>) -> JResult<Option<i32>> {
    match wm {
        None => Ok(None),
        Some(s) if s == "*" => Ok(None),
        Some(s) => match s.parse::<i32>() {
            Ok(v) => Ok(Some(v)),
            // Integer.parseInt would throw NumberFormatException; the engine
            // surfaces this. PORT-NOTE: malformed width -> format error.
            Err(_) => Err(format_err(format!("For input string: \"{}\"", s))),
        },
    }
}

const DAYS: [&str; 8] = [
    "",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
];
const MONTHS: [&str; 12] = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
];

/// Java: `private static PictureFormat analyseDateTimePicture(String picture)`
fn analyse_date_time_picture(picture: &str) -> JResult<PictureFormat> {
    let mut format = PictureFormat::new();
    let picture_chars: Vec<char> = picture.chars().collect();
    let len = picture_chars.len();
    let mut start = 0usize;
    let mut pos = 0usize;
    while pos < len {
        if picture_chars[pos] == '[' {
            // check it's not a doubled [[
            // PORT-NOTE: Java does picture.charAt(pos+1) which would throw
            // StringIndexOutOfBounds if '[' is the last char. We guard, matching
            // that an out-of-range access is an error path; but to be faithful
            // to observable behavior we treat a trailing '[' the same as Java's
            // exception is unlikely in tests. We index-guard to avoid panic.
            if pos + 1 < len && picture_chars[pos + 1] == '[' {
                // literal [
                format.add_literal(&picture_chars, start, pos);
                format.parts.push(SpecPart::Literal {
                    value: "[".to_string(),
                });
                pos += 2;
                start = pos;
                continue;
            }
            format.add_literal(&picture_chars, start, pos);
            start = pos;
            // pos = picture.indexOf("]", start)
            let found = (start..len).find(|&i| picture_chars[i] == ']');
            match found {
                None => {
                    return Err(format_err(ERR_MSG_NO_CLOSING_BRACKET.to_string()));
                }
                Some(p) => pos = p,
            }
            // marker = picture.substring(start+1, pos)
            let marker_raw: String = picture_chars[start + 1..pos].iter().collect();
            // marker = String.join("", marker.split("\\s+"))  -> remove all whitespace
            let marker: String = marker_raw.chars().filter(|c| !c.is_whitespace()).collect();
            let marker_chars: Vec<char> = marker.chars().collect();
            if marker_chars.is_empty() {
                // Java: marker.charAt(0) -> StringIndexOutOfBoundsException.
                return Err(format_err(
                    "Empty component marker [] in date/time picture string".to_string(),
                ));
            }
            let component = marker_chars[0];

            let mut width: Option<(Option<i32>, Option<i32>)> = None;
            let presentation1: Option<String>;
            let mut presentation2: Option<char> = None;
            let mut ordinal = false;

            // int comma = marker.lastIndexOf(",")
            let comma = marker.rfind(',');
            let pres_mod: String;
            if let Some(comma_idx) = comma {
                // widthMod = marker.substring(comma+1)
                let width_mod = &marker[comma_idx + 1..];
                let dash = width_mod.find('-');
                let (min_s, max_s): (String, Option<String>) = match dash {
                    None => (width_mod.to_string(), None),
                    Some(d) => (
                        width_mod[..d].to_string(),
                        Some(width_mod[d + 1..].to_string()),
                    ),
                };
                width = Some((
                    parse_width(Some(min_s.as_str()))?,
                    parse_width(max_s.as_deref())?,
                ));
                // presMod = marker.substring(1, comma) — skip the first
                // *character* (may be multi-byte; Java indexes UTF-16 units,
                // where any component letter is one unit).
                let first_len = marker_chars[0].len_utf8();
                pres_mod = marker[first_len..comma_idx].to_string();
            } else {
                // presMod = marker.substring(1)
                let first_len = marker_chars[0].len_utf8();
                pres_mod = marker[first_len..].to_string();
            }

            if pres_mod.chars().count() == 1 {
                presentation1 = Some(pres_mod.clone());
            } else if pres_mod.chars().count() > 1 {
                let last_char = pres_mod.chars().last().unwrap();
                if "atco".contains(last_char) {
                    presentation2 = Some(last_char);
                    if last_char == 'o' {
                        ordinal = true;
                    }
                    // presentation1 = presMod.substring(0, len-1)
                    let pm_chars: Vec<char> = pres_mod.chars().collect();
                    presentation1 = Some(pm_chars[..pm_chars.len() - 1].iter().collect());
                } else {
                    presentation1 = Some(pres_mod.clone());
                }
            } else {
                presentation1 = default_presentation_modifier(component).map(|s| s.to_string());
            }
            if presentation1.is_none() {
                // throw new RuntimeException(format(ERR_MSG_UNKNOWN_COMPONENT_SPECIFIER, component))
                return Err(format_err(ERR_MSG_UNKNOWN_COMPONENT_SPECIFIER.replacen(
                    "%s",
                    &component.to_string(),
                    1,
                )));
            }

            let mut names: Option<Tcase> = None;
            let mut integer_format: Option<Format> = None;
            let mut n: i32 = 0;

            let p1 = presentation1.clone().unwrap();
            let p1_first = p1.chars().next().unwrap();
            if p1_first == 'n' {
                names = Some(Tcase::Lower);
            } else if p1_first == 'N' {
                if p1.chars().count() > 1 && p1.chars().nth(1) == Some('n') {
                    names = Some(Tcase::Title);
                } else {
                    names = Some(Tcase::Upper);
                }
            } else if "YMDdFWwXxHhmsf".contains(component) {
                let mut integer_pattern = p1.clone();
                if let Some(p2) = presentation2 {
                    integer_pattern += &format!(";{}", p2);
                }
                let mut int_fmt = analyse_integer_picture(&integer_pattern)?;
                int_fmt.ordinal = ordinal;
                if let Some((Some(min), _)) = width {
                    if int_fmt.mandatory_digits < min {
                        int_fmt.mandatory_digits = min;
                    }
                }
                if component == 'Y' {
                    n = -1;
                    if let Some((_, Some(max))) = width {
                        n = max;
                        int_fmt.mandatory_digits = n;
                    } else {
                        let w = int_fmt.mandatory_digits + int_fmt.optional_digits;
                        if w >= 2 {
                            n = w;
                        }
                    }
                }
                integer_format = Some(int_fmt);
            }
            if component == 'Z' || component == 'z' {
                let mut int_fmt = analyse_integer_picture(&p1)?;
                int_fmt.ordinal = ordinal;
                integer_format = Some(int_fmt);
            }

            format.parts.push(SpecPart::Marker {
                component,
                width,
                presentation1,
                presentation2,
                ordinal,
                names,
                integer_format,
                n,
            });
            start = pos + 1;
        }
        pos += 1;
    }
    format.add_literal(&picture_chars, start, pos);
    Ok(format)
}

// ---------------------------------------------------------------------------
// formatDateTime / formatComponent / getDateTimeFragment
// ---------------------------------------------------------------------------

/// Java: `public static String formatDateTime(long millis, String picture, String timezone)`
pub fn format_date_time(
    millis: i64,
    picture: Option<&str>,
    timezone: Option<&str>,
) -> JResult<String> {
    let mut offset_hours: i32 = 0;
    let mut offset_minutes: i32 = 0;

    if let Some(tz) = timezone {
        // int offset = Integer.parseInt(timezone)
        let offset: i32 = tz
            .parse::<i32>()
            .map_err(|_| format_err(format!("For input string: \"{}\"", tz)))?;
        offset_hours = offset / 100;
        offset_minutes = offset % 100;
    }

    let format_spec = match picture {
        None => {
            // iso8601Spec
            analyse_date_time_picture("[Y0001]-[M01]-[D01]T[H01]:[m01]:[s01].[f001][Z01:01t]")?
        }
        Some(p) => analyse_date_time_picture(p)?,
    };

    let offset_millis = ((60 * offset_hours + offset_minutes) as i64) * 60 * 1000;
    // LocalDateTime.ofInstant(Instant.ofEpochMilli(millis + offsetMillis), UTC)
    let date_time = utc_from_millis(millis + offset_millis)?;

    let mut result = String::new();
    for part in &format_spec.parts {
        match part {
            SpecPart::Literal { value } => result.push_str(value),
            marker => {
                result.push_str(&format_component(
                    &date_time,
                    marker,
                    offset_hours,
                    offset_minutes,
                )?);
            }
        }
    }
    Ok(result)
}

/// Build a UTC DateTime from epoch-millis the way Java's
/// `LocalDateTime.ofInstant(Instant.ofEpochMilli(m), UTC)` does (handles
/// negative millis correctly via floor division for the sub-second part).
fn utc_from_millis(millis: i64) -> JResult<DateTime<Utc>> {
    let secs = millis.div_euclid(1000);
    let ms = millis.rem_euclid(1000);
    // chrono caps the calendar at about year +/-262,143 (~8.2e15 ms); Java's
    // java.time goes further. Error instead of panicking outside the range.
    Utc.timestamp_opt(secs, (ms as u32) * 1_000_000)
        .single()
        .ok_or_else(|| format_err(format!("Timestamp out of representable range: {}", millis)))
}

/// Java: `private static String formatComponent(LocalDateTime date, SpecPart markerSpec, int offsetHours, int offsetMinutes)`
fn format_component(
    date: &DateTime<Utc>,
    marker: &SpecPart,
    offset_hours: i32,
    offset_minutes: i32,
) -> JResult<String> {
    let (component, width, presentation2, names, integer_format, n) = match marker {
        SpecPart::Marker {
            component,
            width,
            presentation2,
            names,
            integer_format,
            n,
            ..
        } => (
            *component,
            width,
            *presentation2,
            *names,
            integer_format,
            *n,
        ),
        SpecPart::Literal { .. } => unreachable!(),
    };

    let mut component_value = get_date_time_fragment(date, component);

    if "YMDdFWwXxHhms".contains(component) {
        if component == 'Y' {
            if n != -1 {
                // componentValue = "" + (int)(parseInt(componentValue) % pow(10, n))
                let parsed: i64 = component_value.parse().unwrap_or(0);
                let modulus = 10f64.powi(n) as i64;
                component_value = format!("{}", (parsed % modulus) as i32);
            }
        }
        if let Some(name_case) = names {
            if component == 'M' || component == 'x' {
                let idx: usize = component_value.parse::<usize>().unwrap_or(0);
                component_value = MONTHS[idx - 1].to_string();
            } else if component == 'F' {
                let idx: usize = component_value.parse::<usize>().unwrap_or(0);
                component_value = DAYS[idx].to_string();
            } else {
                // throw new RuntimeException(format(ERR_MSG_INVALID_NAME_MODIFIER, component))
                return Err(format_err(ERR_MSG_INVALID_NAME_MODIFIER.replacen(
                    "%s",
                    &component.to_string(),
                    1,
                )));
            }
            if name_case == Tcase::Upper {
                component_value = component_value.to_uppercase();
            } else if name_case == Tcase::Lower {
                component_value = component_value.to_lowercase();
            }
            if let Some((_, Some(max))) = width {
                if component_value.chars().count() as i32 > *max {
                    // substring(0, max)
                    component_value = substring_chars(&component_value, 0, *max as usize);
                }
            }
        } else {
            let parsed: i64 = component_value.parse().unwrap_or(0);
            component_value = format_integer_with(parsed, require_int_fmt(integer_format)?)?;
        }
    } else if component == 'f' {
        let parsed: i64 = component_value.parse().unwrap_or(0);
        component_value = format_integer_with(parsed, require_int_fmt(integer_format)?)?;
    } else if component == 'Z' || component == 'z' {
        let offset = offset_hours * 100 + offset_minutes;
        let int_fmt = require_int_fmt(integer_format)?;
        if int_fmt.regular {
            component_value = format_integer_with(offset as i64, int_fmt)?;
        } else {
            let num_digits = int_fmt.mandatory_digits;
            if num_digits == 1 || num_digits == 2 {
                component_value = format_integer_with(offset_hours as i64, int_fmt)?;
                if offset_minutes != 0 {
                    component_value +=
                        &format!(":{}", format_integer(offset_minutes as i64, "00")?);
                }
            } else if num_digits == 3 || num_digits == 4 {
                component_value = format_integer_with(offset as i64, int_fmt)?;
            } else {
                // throw new RuntimeException(ERR_MSG_TIMEZONE_FORMAT)
                return Err(format_err(ERR_MSG_TIMEZONE_FORMAT.to_string()));
            }
        }
        if offset >= 0 {
            component_value = format!("+{}", component_value);
        }
        if component == 'z' {
            component_value = format!("GMT{}", component_value);
        }
        if offset == 0 && presentation2 == Some('t') {
            component_value = "Z".to_string();
        }
    } else if component == 'P' {
        // Formatting P for am/pm; getDateTimeFragment returns lower case.
        if names == Some(Tcase::Upper) {
            component_value = component_value.to_uppercase();
        }
    }
    Ok(component_value)
}

fn substring_chars(s: &str, start: usize, end: usize) -> String {
    s.chars().skip(start).take(end - start).collect()
}

/// Java: `private static String getDateTimeFragment(LocalDateTime date, Character component)`
fn get_date_time_fragment(date: &DateTime<Utc>, component: char) -> String {
    match component {
        'Y' => format!("{}", date.year()),
        'M' => format!("{}", date.month()),
        'D' => format!("{}", date.day()),
        'd' => format!("{}", date.ordinal()), // day of year
        'F' => format!("{}", iso_day_of_week(date)), // 1=Mon..7=Sun
        'W' => format!("{}", iso_week_of_year(date)), // IsoFields.WEEK_OF_WEEK_BASED_YEAR
        'w' => format!("{}", iso_week_of_month(date)), // WeekFields.ISO.weekOfMonth()
        'X' => format!("{}", date.year()),    // TODO in Java; returns year
        'x' => format!("{}", date.month()),   // TODO in Java; returns month
        'H' => format!("{}", date.hour()),
        'h' => {
            let mut hour = date.hour() as i32;
            if hour > 12 {
                hour -= 12;
            } else if hour == 0 {
                hour = 12;
            }
            format!("{}", hour)
        }
        'P' => {
            if date.hour() < 12 {
                "am".to_string()
            } else {
                "pm".to_string()
            }
        }
        'm' => format!("{}", date.minute()),
        's' => format!("{}", date.second()),
        'f' => format!("{}", date.nanosecond() / 1_000_000),
        'Z' | 'z' => String::new(),
        'C' => "ISO".to_string(),
        'E' => "ISO".to_string(),
        _ => String::new(),
    }
}

/// ISO day-of-week 1=Monday..7=Sunday, matching java.time `getDayOfWeek().getValue()`.
fn iso_day_of_week(date: &DateTime<Utc>) -> u32 {
    date.weekday().number_from_monday()
}

/// ISO 8601 week-of-week-based-year, matching `IsoFields.WEEK_OF_WEEK_BASED_YEAR`.
fn iso_week_of_year(date: &DateTime<Utc>) -> u32 {
    date.iso_week().week()
}

/// `WeekFields.ISO.weekOfMonth()`.
///
/// PORT-NOTE: java.time `WeekFields.ISO` uses firstDayOfWeek=MONDAY and
/// minimalDaysInFirstWeek=4. This is a faithful port of
/// `WeekFields.ComputedDayOfField.getWeekOfMonth` /
/// `startOfWeekOffset` / `computeWeek` for the WEEK_OF_MONTH field. Days that
/// fall in the leading partial week (when that partial week has fewer than 4
/// days) are reported as week 0 by java.time — JSONata then formats that 0.
fn iso_week_of_month(date: &DateTime<Utc>) -> i32 {
    // localizedDayOfWeek for ISO (firstDayOfWeek = MONDAY): 1=Mon..7=Sun.
    let dow = date.weekday().number_from_monday() as i32;
    let dom = date.day() as i32;
    let offset = start_of_week_offset(dom, dow);
    compute_week(offset, dom)
}

/// java.time `WeekFields.startOfWeekOffset(int value, int dow)` with
/// minimalDays = 4 (ISO).
fn start_of_week_offset(value: i32, dow: i32) -> i32 {
    // int weekStart = Math.floorMod(value - dow, 7);
    let week_start = (value - dow).rem_euclid(7);
    let mut offset = -week_start;
    if week_start + 1 > 4 {
        offset += 7;
    }
    offset
}

/// java.time `WeekFields.computeWeek(int offset, int day)`.
fn compute_week(offset: i32, day: i32) -> i32 {
    (7 + offset + (day - 1)) / 7
}

fn utc_ymd(year: i32, month: u32, day: u32) -> JResult<DateTime<Utc>> {
    Utc.with_ymd_and_hms(year, month, day, 0, 0, 0)
        .single()
        .ok_or_else(|| {
            parse_err(format!(
                "Date out of representable range: {year}-{month}-{day}"
            ))
        })
}

// ---------------------------------------------------------------------------
// parseDateTime
// ---------------------------------------------------------------------------

/// A matcher part: a regex plus a parse closure (modelled via an enum tag so we
/// can avoid trait objects).
struct MatcherPart {
    regex: String,
    component: char,
    kind: MatcherKind,
}

#[derive(Clone)]
enum MatcherKind {
    /// Literal — parse always throws UnsupportedOperationException (ignored).
    Literal,
    /// Timezone Z/z.
    Timezone {
        is_z: bool, // 'z' has GMT prefix
        separator: bool,
        sep_char: String,
    },
    /// Milliseconds 'f'.
    Fraction,
    /// Integer with a Format (letters/roman/words/decimal).
    Integer(Format),
    /// Name lookup (months/days/ampm).
    NameLookup(HashMap<String, i32>),
}

/// Java: `public static Long parseDateTime(String timestamp, String picture)`
pub fn parse_date_time(timestamp: &str, picture: &str) -> JResult<Option<i64>> {
    let format_spec = analyse_date_time_picture(picture)?;
    let match_spec = generate_regex(&format_spec)?;
    let mut full_regex = String::from("^");
    for part in &match_spec {
        full_regex += &format!("({})", part.regex);
    }
    full_regex += "$";

    // Pattern.CASE_INSENSITIVE
    let re = build_case_insensitive_regex(&full_regex)?;

    let caps = match re.captures(timestamp) {
        Some(c) => c,
        None => return Ok(None),
    };

    let mut components: HashMap<char, i64> = HashMap::new();
    // groups 1..=groupCount
    for i in 1..=match_spec.len() {
        let mpart = &match_spec[i - 1];
        if let Some(g) = caps.get(i) {
            match parse_matcher_part(mpart, g.as_str()) {
                Ok(Some(v)) => {
                    components.insert(mpart.component, v as i64);
                }
                Ok(None) => { /* UnsupportedOperationException -> do nothing */ }
                Err(e) => return Err(e),
            }
        }
    }

    if components.is_empty() {
        return Ok(None);
    }

    let mut mask: i32 = 0;
    for part in "YXMxWwdD".chars() {
        mask <<= 1;
        if components.get(&part).is_some() {
            mask += 1;
        }
    }
    let dm_a = 161;
    let dm_b = 130;
    let dm_c = 84;
    let dm_d = 72;
    let date_a = is_type(dm_a, mask);
    let date_b = !date_a && is_type(dm_b, mask);
    let date_c = is_type(dm_c, mask);
    let date_d = !date_c && is_type(dm_d, mask);

    let mut mask2: i32 = 0;
    for part in "PHhmsf".chars() {
        mask2 <<= 1;
        if components.get(&part).is_some() {
            mask2 += 1;
        }
    }
    let tm_a = 23;
    let tm_b = 47;
    let time_a = is_type(tm_a, mask2);
    let time_b = !time_a && is_type(tm_b, mask2);

    let date_comps = if date_b {
        "YB"
    } else if date_c {
        "XxwF"
    } else if date_d {
        "XWF"
    } else {
        "YMD"
    };
    let time_comps = if time_b { "Phmsf" } else { "Hmsf" };
    let comps = format!("{}{}", date_comps, time_comps);

    let now = Utc::now();

    let mut start_specified = false;
    let mut end_specified = false;
    for part in comps.chars() {
        if components.get(&part).is_none() {
            if start_specified {
                let v = if "MDd".contains(part) { 1 } else { 0 };
                components.insert(part, v);
                end_specified = true;
            } else {
                let frag = get_date_time_fragment(&now, part);
                let v: i64 = frag.parse().unwrap_or(0);
                components.insert(part, v);
            }
        } else {
            start_specified = true;
            if end_specified {
                return Err(parse_err(ERR_MSG_MISSING_FORMAT.to_string()));
            }
        }
    }

    // M handling
    if let Some(&m) = components.get(&'M') {
        if m > 0 {
            components.insert('M', m - 1);
        } else {
            components.insert('M', 0);
        }
    } else {
        components.insert('M', 0);
    }

    if date_b {
        // firstJan = LocalDateTime.of(Y, JANUARY, 1, 0, 0).withDayOfYear(d)
        let y = *components.get(&'Y').unwrap() as i32;
        let doy = *components.get(&'d').unwrap() as i64;
        let first_jan = utc_ymd(y, 1, 1)? + Duration::days(doy - 1);
        components.insert('M', (first_jan.month() as i64) - 1);
        components.insert('D', first_jan.day() as i64);
    }
    if date_c {
        // parsing this format not currently supported
        return Err(parse_err(ERR_MSG_MISSING_FORMAT.to_string()));
    }
    if date_d {
        // parsing this format (ISO week date) not currently supported
        return Err(parse_err(ERR_MSG_MISSING_FORMAT.to_string()));
    }
    if time_b {
        let h = *components.get(&'h').unwrap();
        components.insert('H', if h == 12 { 0 } else { h });
        if components.get(&'P') == Some(&1) {
            let hh = *components.get(&'H').unwrap();
            components.insert('H', hh + 12);
        }
    }

    let y = *components.get(&'Y').unwrap() as i32;
    let mo = (*components.get(&'M').unwrap() + 1) as u32;
    let d = *components.get(&'D').unwrap() as u32;
    let hh = *components.get(&'H').unwrap() as u32;
    let mi = *components.get(&'m').unwrap() as u32;
    let ss = *components.get(&'s').unwrap() as u32;
    let f = *components.get(&'f').unwrap();
    let nanos = (f * 1_000_000) as u32;

    // LocalDateTime.of(...).toInstant(UTC).toEpochMilli()
    let cal = Utc
        .with_ymd_and_hms(y, mo, d, hh, mi, ss)
        .single()
        .ok_or_else(|| parse_err(ERR_MSG_MISSING_FORMAT.to_string()))?;
    let cal = cal + Duration::nanoseconds(nanos as i64);
    let mut millis = cal.timestamp_millis();

    if let Some(&z) = components.get(&'Z') {
        millis -= z * 60 * 1000;
    } else if let Some(&z) = components.get(&'z') {
        millis -= z * 60 * 1000;
    }
    Ok(Some(millis))
}

/// Java: `private static boolean isType(int type, int mask)`
fn is_type(ty: i32, mask: i32) -> bool {
    ((!ty & mask) == 0) && (ty & mask) != 0
}

/// Build a case-insensitive regex. The `fullRegex` is built from JSONata
/// picture parts; it uses standard regex features. We use the `regex` crate
/// with the `(?i)` flag.
fn build_case_insensitive_regex(full_regex: &str) -> JResult<regex::Regex> {
    regex::RegexBuilder::new(full_regex)
        .case_insensitive(true)
        .build()
        // A malformed regex from a pathological picture: surface as parse error.
        .map_err(|e| parse_err(format!("{}", e)))
}

/// Java: `private static PictureMatcher generateRegex(PictureFormat formatSpec)`
fn generate_regex(format_spec: &PictureFormat) -> JResult<Vec<MatcherPart>> {
    let mut parts: Vec<MatcherPart> = Vec::new();
    for part in &format_spec.parts {
        match part {
            SpecPart::Literal { value } => {
                // Pattern "[.*+?^${}()|\[\]\\]" replaced with "\\$0"
                let regex = escape_literal(value);
                parts.push(MatcherPart {
                    regex,
                    component: '\0',
                    kind: MatcherKind::Literal,
                });
            }
            SpecPart::Marker {
                component,
                width,
                integer_format,
                ..
            } => {
                let comp = *component;
                let res = if comp == 'Z' || comp == 'z' {
                    let int_fmt = require_int_fmt(integer_format)?;
                    let separator = int_fmt.grouping_separators.len() == 1 && int_fmt.regular;
                    let mut regex = String::new();
                    if comp == 'z' {
                        regex = "GMT".to_string();
                    }
                    regex += "[-+][0-9]+";
                    let sep_char = if separator {
                        let c = int_fmt.grouping_separators[0].character.clone();
                        regex += &format!("{}[0-9]+", regex_escape_char(&c));
                        c
                    } else {
                        String::new()
                    };
                    MatcherPart {
                        regex,
                        component: comp,
                        kind: MatcherKind::Timezone {
                            is_z: comp == 'z',
                            separator,
                            sep_char,
                        },
                    }
                } else if comp == 'f' {
                    MatcherPart {
                        regex: "[0-9]+".to_string(),
                        component: comp,
                        kind: MatcherKind::Fraction,
                    }
                } else if let Some(int_fmt) = integer_format {
                    generate_regex_integer(comp, int_fmt)?
                } else {
                    // name lookup
                    let regex = "[a-zA-Z]+".to_string();
                    let mut lookup: HashMap<String, i32> = HashMap::new();
                    if comp == 'M' || comp == 'x' {
                        for (i, m) in MONTHS.iter().enumerate() {
                            let key = if let Some((_, Some(max))) = width {
                                substring_chars(m, 0, *max as usize)
                            } else {
                                m.to_string()
                            };
                            lookup.insert(key, (i as i32) + 1);
                        }
                    } else if comp == 'F' {
                        for i in 1..DAYS.len() {
                            let day = DAYS[i];
                            let key = if let Some((_, Some(max))) = width {
                                substring_chars(day, 0, *max as usize)
                            } else {
                                day.to_string()
                            };
                            lookup.insert(key, i as i32);
                        }
                    } else if comp == 'P' {
                        lookup.insert("am".to_string(), 0);
                        lookup.insert("AM".to_string(), 0);
                        lookup.insert("pm".to_string(), 1);
                        lookup.insert("PM".to_string(), 1);
                    } else {
                        return Err(parse_err(ERR_MSG_INVALID_NAME_MODIFIER.replacen(
                            "%s",
                            &comp.to_string(),
                            1,
                        )));
                    }
                    MatcherPart {
                        regex,
                        component: comp,
                        kind: MatcherKind::NameLookup(lookup),
                    }
                };
                parts.push(res);
            }
        }
    }
    Ok(parts)
}

/// Java: `private static MatcherPart generateRegex(char component, Format formatSpec)`
fn generate_regex_integer(component: char, format_spec: &Format) -> JResult<MatcherPart> {
    let is_upper = format_spec.case_type == Tcase::Upper;
    let regex = match format_spec.primary {
        Formats::Letters => {
            if is_upper {
                "[A-Z]+".to_string()
            } else {
                "[a-z]+".to_string()
            }
        }
        Formats::Roman => {
            if is_upper {
                "[MDCLXVI]+".to_string()
            } else {
                "[mdclxvi]+".to_string()
            }
        }
        Formats::Words => {
            // Set of wordValues keys + "and" + "[\-, ]"
            let mut words: Vec<String> = word_values().keys().cloned().collect();
            words.push("and".to_string());
            words.push("[\\-, ]".to_string());
            // PORT-NOTE: Java iterates a HashSet (unordered) when joining; order
            // does not affect alternation semantics for these literal words.
            format!("(?:{})+", words.join("|"))
        }
        Formats::Decimal => {
            let mut r = "[0-9]+".to_string();
            match component {
                'Y' => r = "[0-9]{2,4}".to_string(),
                'M' | 'D' | 'H' | 'h' | 'm' | 's' => r = "[0-9]{1,2}".to_string(),
                _ => {}
            }
            if format_spec.ordinal {
                r += "(?:th|st|nd|rd)";
            }
            r
        }
        Formats::Sequence => {
            return Err(parse_err(
                ERR_MSG_SEQUENCE_UNSUPPORTED.replacen("%s", "", 1),
            ));
        }
    };
    Ok(MatcherPart {
        regex,
        component,
        kind: MatcherKind::Integer(format_spec.clone()),
    })
}

/// Run the parse closure for a MatcherPart. Returns Ok(None) when Java would
/// throw `UnsupportedOperationException` (the literal case).
fn parse_matcher_part(part: &MatcherPart, value: &str) -> JResult<Option<i32>> {
    match &part.kind {
        MatcherKind::Literal => Ok(None), // UnsupportedOperationException
        MatcherKind::Timezone {
            is_z,
            separator,
            sep_char,
        } => {
            let mut v = value;
            if *is_z {
                // value.substring(3)
                v = &v[3..];
            }
            let (offset_hours, offset_minutes);
            if *separator {
                let idx = v.find(sep_char.as_str()).unwrap();
                offset_hours = v[..idx].parse::<i32>().unwrap_or(0);
                offset_minutes = v[idx + sep_char.len()..].parse::<i32>().unwrap_or(0);
            } else {
                let numdigits = v.chars().count() as i32 - 1;
                if numdigits <= 2 {
                    offset_hours = v.parse::<i32>().unwrap_or(0);
                    offset_minutes = 0;
                } else {
                    // value.substring(0,3), value.substring(3)
                    let vchars: Vec<char> = v.chars().collect();
                    let first3: String = vchars[..3].iter().collect();
                    let rest: String = vchars[3..].iter().collect();
                    offset_hours = first3.parse::<i32>().unwrap_or(0);
                    offset_minutes = rest.parse::<i32>().unwrap_or(0);
                }
            }
            Ok(Some(offset_hours * 60 + offset_minutes))
        }
        MatcherKind::Fraction => {
            // Integer.parseInt(value.substring(0,3))
            let vchars: Vec<char> = value.chars().collect();
            let end = vchars.len().min(3);
            let sub: String = vchars[..end].iter().collect();
            Ok(Some(sub.parse::<i32>().unwrap_or(0)))
        }
        MatcherKind::Integer(format_spec) => {
            let v = parse_integer_value(value, format_spec, part.component)?;
            Ok(Some(v))
        }
        MatcherKind::NameLookup(lookup) => {
            // Java: `lookup.get(value)` — an exact-case lookup. The overall
            // match regex is case-insensitive, but the tables only hold the
            // TitleCase month/day names ("January", "Wednesday", incl. their
            // width-truncated prefixes) and the am/AM/pm/PM meridian forms, so
            // any other casing ("january", "JANUARY", "Pm") NPEs in Java.
            // PORT-NOTE: we replicate the accept/reject split but reject with
            // a clean D3141 parse error instead of a panic.
            match lookup.get(value) {
                Some(v) => Ok(Some(*v)),
                None => Err(parse_err(ERR_MSG_MISSING_FORMAT.to_string())),
            }
        }
    }
}

/// The DECIMAL/LETTERS/ROMAN/WORDS parse closures from `generateRegex(char, Format)`.
fn parse_integer_value(value: &str, format_spec: &Format, _component: char) -> JResult<i32> {
    let is_upper = format_spec.case_type == Tcase::Upper;
    match format_spec.primary {
        Formats::Letters => Ok(letters_to_decimal(value, if is_upper { 'A' } else { 'a' })),
        Formats::Roman => {
            let v = if is_upper {
                value.to_string()
            } else {
                value.to_uppercase()
            };
            Ok(roman_to_decimal(&v))
        }
        Formats::Words => Ok(words_to_number(&value.to_lowercase())),
        Formats::Decimal => {
            let mut digits = value.to_string();
            if format_spec.ordinal {
                // value.substring(0, len-2)
                let vchars: Vec<char> = digits.chars().collect();
                digits = vchars[..vchars.len() - 2].iter().collect();
            }
            if format_spec.regular {
                // digits = join("", digits.split(","))
                digits = java_split_literal(&digits, ",").join("");
            } else {
                for sep in &format_spec.grouping_separators {
                    digits = java_split_literal(&digits, &sep.character).join("");
                }
            }
            if format_spec.zero_code != 0x30 {
                let shifted: String = digits
                    .chars()
                    .map(|c| {
                        let nc = (c as i32) - format_spec.zero_code + 0x30;
                        char::from_u32(nc as u32).unwrap_or(c)
                    })
                    .collect();
                digits = shifted;
            }
            digits
                .parse::<i32>()
                .map_err(|_| parse_err(format!("For input string: \"{}\"", digits)))
        }
        Formats::Sequence => Err(parse_err(
            ERR_MSG_SEQUENCE_UNSUPPORTED.replacen("%s", "", 1),
        )),
    }
}

/// Java literal escaping: `Pattern.compile("[.*+?^${}()|\[\]\\]").matcher(v).replaceAll("\\$0")`
fn escape_literal(value: &str) -> String {
    let mut out = String::new();
    for c in value.chars() {
        if ".*+?^${}()|[]\\".contains(c) {
            out.push('\\');
        }
        out.push(c);
    }
    out
}

/// Escape a single separator character for inclusion in a regex character
/// sequence (used for the timezone separator in `generateRegex`). Java inserts
/// the raw character; we escape regex-special chars to be safe in the Rust
/// regex engine while preserving the matched content.
fn regex_escape_char(c: &str) -> String {
    let mut out = String::new();
    for ch in c.chars() {
        if ".*+?^${}()|[]\\".contains(ch) {
            out.push('\\');
        }
        out.push(ch);
    }
    out
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_number_to_words_basic() {
        assert_eq!(number_to_words(0, false), "Zero");
        assert_eq!(number_to_words(1, false), "One");
        assert_eq!(number_to_words(19, false), "Nineteen");
        assert_eq!(number_to_words(20, false), "Twenty");
        assert_eq!(number_to_words(21, false), "Twenty-One");
        assert_eq!(number_to_words(100, false), "One Hundred");
        assert_eq!(number_to_words(123, false), "One Hundred and Twenty-Three");
        assert_eq!(number_to_words(1000, false), "One Thousand");
        assert_eq!(
            number_to_words(1234, false),
            "One Thousand, Two Hundred and Thirty-Four"
        );
        assert_eq!(number_to_words(1000000, false), "One Million");
    }

    #[test]
    fn test_number_to_words_ordinal() {
        assert_eq!(number_to_words(1, true), "First");
        assert_eq!(number_to_words(2, true), "Second");
        assert_eq!(number_to_words(20, true), "Twentieth");
        assert_eq!(number_to_words(21, true), "Twenty-First");
        assert_eq!(number_to_words(100, true), "One Hundredth");
    }

    #[test]
    fn test_words_to_number() {
        assert_eq!(words_to_number("one"), 1);
        assert_eq!(words_to_number("twenty-one"), 21);
        assert_eq!(words_to_number("one hundred and twenty-three"), 123);
        assert_eq!(
            words_to_number("one thousand, two hundred and thirty-four"),
            1234
        );
    }

    #[test]
    fn test_roman() {
        assert_eq!(decimal_to_roman(1), "i");
        assert_eq!(decimal_to_roman(4), "iv");
        assert_eq!(decimal_to_roman(9), "ix");
        assert_eq!(decimal_to_roman(1984), "mcmlxxxiv");
        assert_eq!(roman_to_decimal("MCMLXXXIV"), 1984);
        assert_eq!(roman_to_decimal("IV"), 4);
        assert_eq!(roman_to_decimal("XII"), 12);
    }

    #[test]
    fn test_letters() {
        assert_eq!(decimal_to_letters(1, 'a'), "a");
        assert_eq!(decimal_to_letters(26, 'a'), "z");
        assert_eq!(decimal_to_letters(27, 'a'), "aa");
        assert_eq!(decimal_to_letters(28, 'a'), "ab");
        assert_eq!(letters_to_decimal("a", 'a'), 1);
        assert_eq!(letters_to_decimal("z", 'a'), 26);
        assert_eq!(letters_to_decimal("aa", 'a'), 27);
        assert_eq!(letters_to_decimal("ab", 'a'), 28);
    }

    #[test]
    fn test_format_integer_decimal() {
        assert_eq!(format_integer(123, "0").unwrap(), "123");
        assert_eq!(format_integer(123, "000").unwrap(), "123");
        assert_eq!(format_integer(1, "000").unwrap(), "001");
        assert_eq!(format_integer(1234, "#,##0").unwrap(), "1,234");
        assert_eq!(format_integer(1234567, "#,##0").unwrap(), "1,234,567");
        assert_eq!(format_integer(28, "0;o").unwrap(), "28th");
        assert_eq!(format_integer(21, "0;o").unwrap(), "21st");
        assert_eq!(format_integer(22, "0;o").unwrap(), "22nd");
        assert_eq!(format_integer(23, "0;o").unwrap(), "23rd");
        assert_eq!(format_integer(11, "0;o").unwrap(), "11th");
        assert_eq!(format_integer(-5, "0").unwrap(), "-5");
    }

    #[test]
    fn test_format_integer_other() {
        assert_eq!(format_integer(1, "a").unwrap(), "a");
        assert_eq!(format_integer(1, "A").unwrap(), "A");
        assert_eq!(format_integer(1, "i").unwrap(), "i");
        assert_eq!(format_integer(1, "I").unwrap(), "I");
        assert_eq!(format_integer(12, "w").unwrap(), "twelve");
        assert_eq!(format_integer(12, "W").unwrap(), "TWELVE");
        assert_eq!(format_integer(12, "Ww").unwrap(), "Twelve");
    }

    #[test]
    fn test_format_date_time_iso() {
        // 2018-01-01T00:00:00.000Z = 1514764800000
        let s = format_date_time(1514764800000, None, None).unwrap();
        assert_eq!(s, "2018-01-01T00:00:00.000Z");
    }

    #[test]
    fn test_format_date_time_picture() {
        // 1514808000000 = 2018-01-01T12:00:00Z
        let s = format_date_time(1514808000000, Some("[Y]-[M01]-[D01]"), None).unwrap();
        assert_eq!(s, "2018-01-01");
        let s2 = format_date_time(1514808000000, Some("[H01]:[m01]:[s01]"), None).unwrap();
        assert_eq!(s2, "12:00:00");
    }

    #[test]
    fn test_format_date_time_month_name() {
        let s = format_date_time(1514808000000, Some("[MNn] [D], [Y]"), None).unwrap();
        assert_eq!(s, "January 1, 2018");
    }

    #[test]
    fn test_parse_date_time_roundtrip() {
        let millis = parse_date_time("2018-01-01", "[Y0001]-[M01]-[D01]")
            .unwrap()
            .unwrap();
        // 2018-01-01T00:00:00Z
        assert_eq!(millis, 1514764800000);
    }
}

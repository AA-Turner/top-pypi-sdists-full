//! Port of `software.amazon.kinesis.leases.DynamoUtils`.
//!
//! Static helper functions for constructing and safely extracting AWS SDK
//! DynamoDB `AttributeValue`s (strings, longs, doubles, byte arrays,
//! string-sets), used throughout the `LeaseSerializer` implementations.
//!
//! # Behavior preserved from Java
//!
//! - `create_attribute_value_*` constructors **panic** (Java
//!   `IllegalArgumentException`) on null/empty inputs — matching the strict
//!   validation. `create_attribute_value_string` rejects the **empty string**,
//!   not just null (DynamoDB historically disallowed empty `S` attributes).
//! - The `safe_get_*` accessors return `None` (Java `null`) when the attribute
//!   is absent — **except** `safe_get_string_set`, which returns an **empty
//!   `Vec`** (Java `safeGetSS` returns `new ArrayList<>()`, never null). This
//!   per-type default asymmetry is preserved exactly.

use std::collections::HashMap;

use aws_sdk_dynamodb::primitives::Blob;
use aws_sdk_dynamodb::types::AttributeValue;

/// Build a string-set (`SS`) attribute value from a collection of strings.
///
/// # Panics
/// Panics (Java `IllegalArgumentException`) if the collection is empty.
pub fn create_attribute_value_string_set<I, S>(collection_value: I) -> AttributeValue
where
    I: IntoIterator<Item = S>,
    S: Into<String>,
{
    let values: Vec<String> = collection_value.into_iter().map(Into::into).collect();
    if values.is_empty() {
        panic!("Collection attributeValues cannot be null or empty.");
    }
    AttributeValue::Ss(values)
}

/// Build a binary (`B`) attribute value from raw bytes.
///
/// (Java rejects `null`; a `&[u8]` is never null in Rust, so no runtime check
/// is needed here — the invariant is enforced by the type system.)
pub fn create_attribute_value_bytes(byte_buffer_value: &[u8]) -> AttributeValue {
    AttributeValue::B(Blob::new(byte_buffer_value))
}

/// Build a string (`S`) attribute value.
///
/// # Panics
/// Panics (Java `IllegalArgumentException`) if the string is empty.
pub fn create_attribute_value_string(string_value: impl Into<String>) -> AttributeValue {
    let s = string_value.into();
    if s.is_empty() {
        panic!("String attributeValues cannot be null or empty.");
    }
    AttributeValue::S(s)
}

/// Build a number (`N`) attribute value from a `long`.
pub fn create_attribute_value_long(long_value: i64) -> AttributeValue {
    AttributeValue::N(long_value.to_string())
}

/// Build a number (`N`) attribute value from a `double`.
pub fn create_attribute_value_double(double_value: f64) -> AttributeValue {
    AttributeValue::N(double_value.to_string())
}

/// Extract a byte array from `key`, or `None` if absent (Java `safeGetByteArray`).
pub fn safe_get_byte_array(
    dynamo_record: &HashMap<String, AttributeValue>,
    key: &str,
) -> Option<Vec<u8>> {
    dynamo_record
        .get(key)
        .and_then(|av| av.as_b().ok())
        .map(|b| b.as_ref().to_vec())
}

/// Extract a `long` from `key`, or `None` if absent (Java `safeGetLong`).
///
/// # Panics
/// Panics (Java `new Long(av.n())` throws `NumberFormatException`) if the value
/// is present but not a valid integer.
pub fn safe_get_long(dynamo_record: &HashMap<String, AttributeValue>, key: &str) -> Option<i64> {
    dynamo_record.get(key).map(|av| {
        av.as_n()
            .expect("attribute is a number")
            .parse::<i64>()
            .expect("attribute is a valid long")
    })
}

/// Extract a `double` from `key`, or `None` if absent (Java `safeGetDouble`).
///
/// # Panics
/// Panics if the value is present but not a valid double.
pub fn safe_get_double(dynamo_record: &HashMap<String, AttributeValue>, key: &str) -> Option<f64> {
    dynamo_record.get(key).map(|av| {
        av.as_n()
            .expect("attribute is a number")
            .parse::<f64>()
            .expect("attribute is a valid double")
    })
}

/// Extract a string from `key`, or `None` if absent (Java `safeGetString`).
pub fn safe_get_string(
    dynamo_record: &HashMap<String, AttributeValue>,
    key: &str,
) -> Option<String> {
    dynamo_record.get(key).and_then(safe_get_string_from_av)
}

/// Extract a string from an `AttributeValue`, or `None` if the attribute is not
/// a string (Java `safeGetString(AttributeValue)`; Java returns `av.s()` which
/// is `null` for non-string attributes).
pub fn safe_get_string_from_av(av: &AttributeValue) -> Option<String> {
    av.as_s().ok().cloned()
}

/// Extract a string-set from `key`, returning an **empty `Vec`** if absent (Java
/// `safeGetSS` returns `new ArrayList<>()`, never null).
pub fn safe_get_string_set(
    dynamo_record: &HashMap<String, AttributeValue>,
    key: &str,
) -> Vec<String> {
    match dynamo_record.get(key) {
        None => Vec::new(),
        Some(av) => av.as_ss().cloned().unwrap_or_default(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn create_string_and_number_values() {
        assert_eq!(create_attribute_value_string("hi").as_s().unwrap(), "hi");
        assert_eq!(create_attribute_value_long(42).as_n().unwrap(), "42");
        assert_eq!(create_attribute_value_double(1.5).as_n().unwrap(), "1.5");
        let ss = create_attribute_value_string_set(vec!["a".to_string(), "b".to_string()]);
        assert_eq!(ss.as_ss().unwrap(), &vec!["a".to_string(), "b".to_string()]);
        let b = create_attribute_value_bytes(&[1, 2, 3]);
        assert_eq!(b.as_b().unwrap().as_ref(), &[1, 2, 3]);
    }

    #[test]
    #[should_panic(expected = "String attributeValues cannot be null or empty.")]
    fn create_string_rejects_empty() {
        create_attribute_value_string("");
    }

    #[test]
    #[should_panic(expected = "Collection attributeValues cannot be null or empty.")]
    fn create_string_set_rejects_empty() {
        create_attribute_value_string_set(Vec::<String>::new());
    }

    #[test]
    fn safe_getters_return_none_when_absent_but_ss_returns_empty() {
        let mut record: HashMap<String, AttributeValue> = HashMap::new();
        record.insert("num".to_string(), AttributeValue::N("7".to_string()));
        record.insert("str".to_string(), AttributeValue::S("v".to_string()));
        record.insert("dbl".to_string(), AttributeValue::N("2.5".to_string()));
        record.insert(
            "set".to_string(),
            AttributeValue::Ss(vec!["x".to_string(), "y".to_string()]),
        );

        assert_eq!(safe_get_long(&record, "num"), Some(7));
        assert_eq!(safe_get_double(&record, "dbl"), Some(2.5));
        assert_eq!(safe_get_string(&record, "str"), Some("v".to_string()));
        assert_eq!(
            safe_get_string_set(&record, "set"),
            vec!["x".to_string(), "y".to_string()]
        );

        // Absent keys:
        assert_eq!(safe_get_long(&record, "missing"), None);
        assert_eq!(safe_get_double(&record, "missing"), None);
        assert_eq!(safe_get_string(&record, "missing"), None);
        assert_eq!(safe_get_byte_array(&record, "missing"), None);
        // safe_get_string_set returns an EMPTY VEC (never None) when absent.
        assert!(safe_get_string_set(&record, "missing").is_empty());
    }
}

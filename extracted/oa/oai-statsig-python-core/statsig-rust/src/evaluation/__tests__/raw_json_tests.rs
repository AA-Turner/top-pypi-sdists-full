use std::borrow::Cow;

use serde::Deserialize;

use crate::{
    evaluation::{dynamic_returnable::DynamicReturnable, raw_json::RawJson},
    hashing,
    specs_response::spec_types::SpecsResponseFull,
};

const RAW: &str = r#"{"number":1.00e+2, "escaped":"old", "escaped":"\u0061"}"#;

#[test]
fn raw_json_borrows_slice_and_string_without_changing_lexemes() {
    let input = format!(" \n{RAW} \t");
    for decoded in [
        serde_json::from_str::<RawJson<'_>>(&input).unwrap(),
        serde_json::from_slice::<RawJson<'_>>(input.as_bytes()).unwrap(),
    ] {
        assert_eq!(decoded.0, RAW);
        assert_eq!(decoded.0.as_ptr(), input[2..].as_ptr());
    }
}

#[test]
fn raw_json_owns_reader_capture_without_changing_lexemes() {
    let mut deserializer = serde_json::Deserializer::from_reader(RAW.as_bytes());
    let decoded = RawJson::deserialize(&mut deserializer).unwrap();
    assert!(matches!(decoded.0, Cow::Owned(_)));
    assert_eq!(decoded.0, RAW);
}

#[test]
#[serial_test::serial]
fn raw_json_preserves_dynamic_returnable_cache_key_and_cache_hit() {
    let first: DynamicReturnable = serde_json::from_slice(RAW.as_bytes()).unwrap();
    let second: DynamicReturnable = serde_json::from_reader(RAW.as_bytes()).unwrap();
    assert_eq!(first.get_hash(), hashing::hash_one(RAW.as_bytes()));
    assert!(std::ptr::eq(
        first.get_json_pointer_ref().unwrap(),
        second.get_json_pointer_ref().unwrap(),
    ));
}

#[test]
#[serial_test::serial]
fn dynamic_returnable_accepts_a_json_value() {
    let input = serde_json::json!({"key": [true, null]});
    let actual: DynamicReturnable = serde_json::from_value(input.clone()).unwrap();
    assert_eq!(
        actual.get_hash(),
        hashing::hash_one(input.to_string().as_bytes())
    );
    assert_eq!(serde_json::to_value(actual).unwrap(), input);
}

#[test]
fn dynamic_returnable_rejects_malformed_input() {
    for input in [br#"{"number":1"#.as_slice(), b"\"\xff\""] {
        assert!(serde_json::from_slice::<DynamicReturnable>(input).is_err());
        assert!(serde_json::from_reader::<_, DynamicReturnable>(input).is_err());
    }
}

#[test]
#[serial_test::serial]
fn deeply_nested_returnable_preserves_the_empty_object_fallback() {
    let raw = format!(r#"{{"nested":{}0{}}}"#, "[".repeat(256), "]".repeat(256));
    let value: DynamicReturnable = serde_json::from_str(&raw).unwrap();
    assert_eq!(value.get_hash(), hashing::hash_one(raw.as_bytes()));
    assert!(value.get_json().unwrap().is_empty());
}

#[test]
#[serial_test::serial]
fn raw_json_preserves_typed_specs_reader_reload() {
    let data = include_bytes!("../../../tests/data/eval_proj_dcs.json");
    let specs: SpecsResponseFull = serde_json::from_slice(data).unwrap();
    let persisted = serde_json::to_vec(&specs).unwrap();
    let reloaded: SpecsResponseFull = serde_json::from_reader(persisted.as_slice()).unwrap();
    assert_eq!(
        serde_json::to_value(reloaded).unwrap(),
        serde_json::to_value(specs).unwrap()
    );
}

#[test]
fn raw_json_requires_its_string_marker() {
    use serde::de::value::{BorrowedBytesDeserializer, MapDeserializer};

    let wrong_key = MapDeserializer::<_, serde_json::Error>::new([("wrong", "{}")].into_iter());
    assert!(RawJson::deserialize(wrong_key).is_err());

    let numeric_key = MapDeserializer::<_, serde_json::Error>::new([(0u64, "{}")].into_iter());
    assert!(RawJson::deserialize(numeric_key).is_err());

    let bytes =
        BorrowedBytesDeserializer::<serde_json::Error>::new(b"$serde_json::private::RawValue");
    let bytes_key = MapDeserializer::<_, serde_json::Error>::new([(bytes, "{}")].into_iter());
    assert!(RawJson::deserialize(bytes_key).is_err());
}

use std::collections::HashMap;

use serde::{
    Deserialize,
    de::{
        IntoDeserializer,
        value::{BorrowedBytesDeserializer, MapDeserializer},
    },
};
use serde_json::{Value, error::Category};

use crate::evaluation::rkyv_value::{
    RkyvNumber::{Float, NegInt, PosInt},
    RkyvValue::{self, Null, Number},
};

// These fixtures either fail during JSON parsing or leave values that round-trip exactly.
fn assert_matches_json(raw: &str) {
    let expected = serde_json::from_str::<Value>(raw);
    let actual =
        serde_json::from_str::<RkyvValue>(raw).map(|value| serde_json::to_value(value).unwrap());
    assert_eq!(
        actual.map_err(|e| e.classify()),
        expected.map_err(|e| e.classify()),
        "{raw}"
    );
}

#[test]
fn direct_rkyv_preserves_duplicates_and_error_precedence() {
    for raw in [
        r#"{"x":1,"x":2}"#,
        r#"{"x":1e400,"x":2}"#,
        r#"{"x":[{"bad":1e400}],"x":2}"#,
        "[1e400,",
        r#"{"x":1e400,"x":}"#,
    ] {
        assert_matches_json(raw);
    }

    // Without arbitrary_precision the JSON parser rejects overflow immediately.
    // With it the SDK rejects numbers that survive duplicate-key replacement.
    for raw in ["[1e400,2]", r#"{"x":2,"x":1e400}"#] {
        let expected = serde_json::from_str::<Value>(raw)
            .err()
            .map_or(Category::Data, |e| e.classify());
        assert_eq!(
            serde_json::from_str::<RkyvValue>(raw)
                .unwrap_err()
                .classify(),
            expected,
            "{raw}"
        );
    }

    // In the outer returnable map each value is decoded separately.
    assert!(serde_json::from_str::<HashMap<String, RkyvValue>>(r#"{"x":1e400,"x":2}"#).is_err());
}

#[test]
fn direct_rkyv_preserves_serde_json_private_marker_handling() {
    for raw in [
        r#"{"$serde_json::private::Number":"1.0"}"#,
        r#"{"$serde_json::private::Number":"wat"}"#,
        r#"{"$serde_json::private::Number":null}"#,
        r#"{"$serde_json::private::Number":"1","x":2}"#,
        r#"{"before":1,"$serde_json::private::Number":"1.0"}"#,
        r#"{"$serde_json::private::RawValue":"[1,true]"}"#,
        r#"{"$serde_json::private::RawValue":"{\"x\":1e400,\"x\":1}"}"#,
        r#"{"$serde_json::private::RawValue":"{"}"#,
        r#"{"$serde_json::private::RawValue":12}"#,
    ] {
        assert_matches_json(raw);
    }
}

#[test]
fn direct_rkyv_preserves_recursion_limit() {
    for depth in [127, 128] {
        assert_matches_json(&format!("{}0{}", "[".repeat(depth), "]".repeat(depth)));
    }
}

#[test]
fn direct_rkyv_preserves_numeric_boundaries() {
    for (raw, expected) in [
        ("18446744073709551615", PosInt(u64::MAX)),
        ("18446744073709551616", Float(2.0f64.powi(64))),
        ("-9223372036854775808", NegInt(i64::MIN)),
        ("-9223372036854775809", Float(-2.0f64.powi(63))),
        ("1e-400", Float(0.0)),
    ] {
        assert_eq!(
            serde_json::from_str::<RkyvValue>(raw).unwrap(),
            Number(expected),
            "{raw}"
        );
    }
    for decoded in [serde_json::from_str("-0.0"), decode(-0.0f64)] {
        let Number(Float(value)) = decoded.unwrap() else {
            panic!("expected a float")
        };
        assert_eq!(value.to_bits(), (-0.0f64).to_bits());
    }
}

fn decode<'de>(
    input: impl IntoDeserializer<'de, serde_json::Error>,
) -> serde_json::Result<RkyvValue> {
    RkyvValue::deserialize(input.into_deserializer())
}

#[test]
fn direct_rkyv_preserves_generic_serde_numbers() {
    assert_eq!(decode(0i64).unwrap(), Number(PosInt(0)));
    assert_eq!(decode(i64::MAX).unwrap(), Number(PosInt(i64::MAX as u64)));
    assert_eq!(decode(-1i128).unwrap(), Number(NegInt(-1)));
    assert_eq!(decode(1u128).unwrap(), Number(PosInt(1)));
    for value in [f64::NAN, f64::INFINITY, f64::NEG_INFINITY] {
        assert_eq!(decode(value).unwrap(), Null);
    }

    // Serde only accepts integers this wide with arbitrary_precision.
    assert_eq!(
        decode(i128::MIN).ok(),
        serde_json::Number::from_i128(i128::MIN).map(|_| Number(Float(i128::MIN as f64)))
    );
    assert_eq!(
        decode(u128::MAX).ok(),
        serde_json::Number::from_u128(u128::MAX).map(|_| Number(Float(u128::MAX as f64)))
    );
}

#[test]
fn direct_rkyv_rejects_generic_bytes() {
    let bytes = || BorrowedBytesDeserializer::<serde_json::Error>::new(b"x");
    let map = MapDeserializer::<_, serde_json::Error>::new(std::iter::once((bytes(), 1u64)));
    assert!(RkyvValue::deserialize(map).is_err());
    assert_eq!(
        RkyvValue::deserialize(bytes()).unwrap_err().to_string(),
        Value::deserialize(bytes()).unwrap_err().to_string()
    );
}

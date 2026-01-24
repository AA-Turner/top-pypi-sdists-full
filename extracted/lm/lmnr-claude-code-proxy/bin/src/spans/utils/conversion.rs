use serde_json::Value;

use crate::proto::opentelemetry_proto_common_v1::{
    AnyValue, ArrayValue as ArrayValueInner, KeyValue as KeyValueInner,
    KeyValueList as KeyValueListInner, any_value::Value as AnyValueInner,
};

pub fn json_value_to_any_value(value: Value) -> Result<AnyValue, String> {
    let inner_value = match value {
        Value::String(s) => Some(AnyValueInner::StringValue(s)),
        Value::Number(n) => {
            if n.is_i64() {
                Some(AnyValueInner::IntValue(n.as_i64().unwrap_or_default()))
            } else if n.is_u64() {
                Some(AnyValueInner::IntValue(
                    n.as_u64().unwrap_or_default() as i64
                ))
            } else if n.is_f64() {
                Some(AnyValueInner::DoubleValue(n.as_f64().unwrap_or_default()))
            } else {
                return Err(format!("Invalid number: {}", n));
            }
        }
        Value::Bool(b) => Some(AnyValueInner::BoolValue(b)),
        Value::Array(a) => Some(AnyValueInner::ArrayValue(ArrayValueInner {
            values: a
                .into_iter()
                .map(json_value_to_any_value)
                .collect::<Result<Vec<AnyValue>, String>>()?,
        })),
        Value::Object(o) => Some(AnyValueInner::KvlistValue(KeyValueListInner {
            values: o
                .into_iter()
                .map(|(k, v)| {
                    json_value_to_any_value(v).map(|v| KeyValueInner {
                        key: k,
                        value: Some(v),
                    })
                })
                .collect::<Result<Vec<KeyValueInner>, String>>()?,
        })),
        Value::Null => None,
    };
    Ok(AnyValue { value: inner_value })
}

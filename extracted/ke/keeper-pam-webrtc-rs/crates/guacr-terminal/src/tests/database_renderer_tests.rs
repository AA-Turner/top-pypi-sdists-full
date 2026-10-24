#[cfg(test)]
mod query_value_tests {
    use crate::database_renderer::{QueryCell, QueryResult};
    use std::{borrow::Cow, cmp::Ordering};

    #[test]
    fn native_values_preserve_payload_and_text_is_not_inferred() {
        let result = QueryResult::text(
            vec!["value".into()],
            vec![vec!["NULL".into(), "true".into(), "2".into()]],
        );
        assert_eq!(
            result.rows[0],
            vec![
                QueryCell::Text("NULL".into()),
                QueryCell::Text("true".into()),
                QueryCell::Text("2".into())
            ]
        );
        assert_ne!(QueryCell::Null, QueryCell::from("NULL"));
        let text = "界e\u{301}".repeat(200);
        assert!(matches!(
            QueryCell::Text(text.clone()).display_text(),
            Cow::Borrowed(_)
        ));
        assert_eq!(QueryCell::Text(text.clone()).to_string(), text);
        let json = serde_json::json!({"a": [null, true, "NULL", 2]});
        assert_eq!(
            serde_json::from_str::<serde_json::Value>(&QueryCell::Json(json.clone()).to_string())
                .unwrap(),
            json
        );
        assert_eq!(
            QueryCell::Blob(vec![0, 1, 128, 255]).to_string(),
            "0x000180ff"
        );
    }

    #[test]
    fn numeric_order_is_mathematical_at_boundaries() {
        let ordered = vec![
            QueryCell::Float(-f64::NAN),
            QueryCell::Float(f64::NEG_INFINITY),
            QueryCell::Int(i64::MIN),
            QueryCell::Float(-1.5),
            QueryCell::Int(-1),
            QueryCell::Int(0),
            QueryCell::Float(1.5),
            QueryCell::Int(2),
            QueryCell::Int(10),
            QueryCell::Float(9_007_199_254_740_992.0),
            QueryCell::Int(9_007_199_254_740_993),
            QueryCell::Int(i64::MAX),
            QueryCell::Float(9_223_372_036_854_775_808.0),
            QueryCell::Float(f64::INFINITY),
            QueryCell::Float(f64::NAN),
        ];
        for (i, a) in ordered.iter().enumerate() {
            for b in &ordered[i + 1..] {
                assert_eq!(a.compare(b), Ordering::Less, "{a:?} < {b:?}");
                assert_eq!(b.compare(a), Ordering::Greater);
            }
        }
        assert_eq!(
            QueryCell::Int(i64::MIN).compare(&QueryCell::Float(i64::MIN as f64)),
            Ordering::Equal
        );
        assert_eq!(
            QueryCell::Float(-0.0).compare(&QueryCell::Int(0)),
            Ordering::Equal
        );
        assert_eq!(QueryCell::Null.compare(&QueryCell::Int(0)), Ordering::Less);
    }
}

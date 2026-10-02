use jsonata::json::parse_json;
use jsonata::value::JValue;

#[test]
fn parse_nested_object() {
    // Self-contained (shape mirrors the official `dataset0`).
    let s = r#"{"foo": {"bar": 42, "blah": [{"baz": {"fud": "hello"}}]}}"#;
    let v = parse_json(s).unwrap();
    assert!(v.is_object());
    let foo = v.as_object().unwrap().get("foo").unwrap();
    assert_eq!(
        foo.as_object().unwrap().get("bar"),
        Some(&JValue::Number(42.0))
    );
}

#[test]
fn parse_primitives() {
    assert!(matches!(parse_json("null").unwrap(), JValue::Null));
    assert!(matches!(parse_json("true").unwrap(), JValue::Bool(true)));
    assert_eq!(parse_json("42").unwrap(), JValue::Number(42.0));
    assert_eq!(parse_json("-1.5e2").unwrap(), JValue::Number(-150.0));
    assert_eq!(parse_json("\"a\\nb\"").unwrap(), JValue::string("a\nb"));
    let arr = parse_json("[1,null,3]").unwrap();
    if let JValue::Array(a, _) = arr {
        assert_eq!(a.len(), 3);
        assert!(matches!(a[1], JValue::Null));
    } else {
        panic!()
    }
}

#[test]
fn parse_surrogate() {
    // emoji via surrogate pair
    let v = parse_json("\"\\uD83D\\uDE00\"").unwrap();
    assert_eq!(v.as_str().unwrap(), "😀");
}

use jsonata::json::parse_json;
use jsonata::{JValue, Jsonata};

fn eval(expr: &str, data: &str) -> JValue {
    let j = Jsonata::new(expr).expect("parse");
    let input = parse_json(data).expect("data");
    j.evaluate(input, None).expect("eval")
}

fn evals(expr: &str, data: &str) -> JValue {
    let mut j = Jsonata::new(expr).expect("parse");
    j.set_output_convert_nulls(false);
    let input = parse_json(data).expect("data");
    j.evaluate(input, None).expect("eval")
}

#[test]
fn literals_and_arith() {
    assert_eq!(eval("42", "null"), JValue::Number(42.0));
    assert_eq!(eval("(3*(4-2)+1.01e2)/-2", "null"), JValue::Number(-53.5));
    assert_eq!(eval("1+2*3", "null"), JValue::Number(7.0));
    assert_eq!(eval("\"hello\"", "null"), JValue::string("hello"));
    assert_eq!(eval("true and false", "null"), JValue::Bool(false));
    assert_eq!(eval("5 > 3", "null"), JValue::Bool(true));
    assert_eq!(eval("\"a\" & \"b\"", "null"), JValue::string("ab"));
}

#[test]
fn paths() {
    assert_eq!(
        eval("foo.bar", r#"{"foo":{"bar":42}}"#),
        JValue::Number(42.0)
    );
    assert_eq!(
        eval("a.b.c", r#"{"a":{"b":{"c":"deep"}}}"#),
        JValue::string("deep")
    );
    // array navigation
    assert_eq!(
        eval("foo[1]", r#"{"foo":[10,20,30]}"#),
        JValue::Number(20.0)
    );
    assert_eq!(
        eval("foo[-1]", r#"{"foo":[10,20,30]}"#),
        JValue::Number(30.0)
    );
}

#[test]
fn variables_and_blocks() {
    assert_eq!(eval("($x := 5; $x + 1)", "null"), JValue::Number(6.0));
    assert_eq!(
        eval("($a := 2; $b := 3; $a * $b)", "null"),
        JValue::Number(6.0)
    );
}

#[test]
fn conditionals() {
    assert_eq!(
        eval("true ? \"yes\" : \"no\"", "null"),
        JValue::string("yes")
    );
    assert_eq!(eval("5 > 10 ? \"a\" : \"b\"", "null"), JValue::string("b"));
}

#[test]
fn lambda_application() {
    assert_eq!(
        eval("($f := function($x){$x*2}; $f(21))", "null"),
        JValue::Number(42.0)
    );
}

#[test]
fn null_vs_undefined() {
    // JSON null preserved
    assert_eq!(evals("a", r#"{"a":null}"#), JValue::Null);
    // missing -> undefined
    assert_eq!(evals("b", r#"{"a":null}"#), JValue::Undefined);
    assert_eq!(evals("null", "null"), JValue::Null);
}

#[test]
fn object_constructor() {
    let r = eval(r#"{"x": 1+1}"#, "null");
    let expected = parse_json(r#"{"x":2}"#).unwrap();
    assert_eq!(r, expected);
}

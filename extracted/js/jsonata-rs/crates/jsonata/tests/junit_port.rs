//! Ports of the JUnit unit tests from jsonata-java
//! (ArrayTest, StringTest, NumberTest, VariableTest, NullSafetyTest, TypesTest,
//! ExceptionTest, RuntimeTest, CustomFunctionTest, SignatureTest, RegexTest,
//! ParseIntegerTest, DateTimeTest, SerializationTest), adapted to the Rust API.
//!
//! Java-threading tests (ThreadTest/ThreadSafetyTest) and Java object
//! serialization are not applicable to the Rust port and are covered only for
//! their observable evaluation behaviour.

use jsonata::json::parse_json;
use jsonata::value::JValue;
use jsonata::Jsonata;
use std::rc::Rc;

/// `jsonata(expr).evaluate(data)` — Java semantics (output null conversion on).
fn eval(expr: &str, input: JValue) -> JValue {
    let j = Jsonata::new(expr).unwrap_or_else(|e| panic!("parse {}: {}", expr, e.error));
    j.evaluate(input, None)
        .unwrap_or_else(|e| panic!("eval {}: {}", expr, e.error))
}

/// Like `eval` but keeps Null distinct from Undefined.
fn eval_u(expr: &str, input: JValue) -> JValue {
    let mut j = Jsonata::new(expr).unwrap();
    j.set_output_convert_nulls(false);
    j.evaluate(input, None).unwrap()
}

fn eval_err(expr: &str, input: JValue) -> jsonata::JError {
    let j = Jsonata::new(expr).unwrap();
    j.evaluate(input, None).expect_err("expected error")
}

fn json(s: &str) -> JValue {
    parse_json(s).unwrap()
}
/// Java `null` input == undefined.
fn jnull() -> JValue {
    JValue::Undefined
}

// ---------------------------------------------------------------------------
// ArrayTest
// ---------------------------------------------------------------------------

#[test]
fn array_negative_index() {
    assert_eq!(eval("item[-1]", json(r#"{"item":[]}"#)), JValue::Undefined);
    assert_eq!(eval("$[-1]", json("[]")), JValue::Undefined);
}

#[test]
fn array_append_equivalence() {
    let data = json(r#"{"key":[{"x":"y"},{"a":"b"}]}"#);
    let r1 = eval(
        "{'key': $append($.[{'x': 'y'}],$.[{'a': 'b'}])}",
        data.clone(),
    );
    let r2 = eval("{'key': $append($.[{'x': 'y'}],[{'a': 'b'}])}", data);
    assert_eq!(r1, r2);
}

#[test]
fn array_filter_frame() {
    let r = eval(
        "($arr := [{'x':1}, {'x':2}];$arr[x=$number($$.variable.field)])",
        json(r#"{"variable":{"field":"1"}}"#),
    );
    assert!(!r.is_undefined());
}

#[test]
fn array_index() {
    assert_eq!(eval("($x:=['a','b']; $x#$i.$i)", json("1")), json("[0,1]"));
    assert_eq!(eval("($x:=['a','b']; $x#$i.$i)", jnull()), json("[0,1]"));
}

#[test]
fn array_sort() {
    assert_eq!(
        eval(
            "$sort([{'x': 2}, {'x': 1}], function($l, $r){$l.x > $r.x})",
            jnull()
        ),
        json(r#"[{"x":1},{"x":2}]"#)
    );
}

#[test]
fn array_sort_null() {
    assert_eq!(
        eval(
            "$sort([{'x': 2}, {'x': 1}], function($l, $r){$l.y > $r.y})",
            jnull()
        ),
        json(r#"[{"x":2},{"x":1}]"#)
    );
}

#[test]
fn array_wildcard() {
    assert_eq!(eval("*", json(r#"[{"x":1}]"#)), json(r#"{"x":1}"#));
}

#[test]
fn array_wildcard_filter() {
    let data = json(
        r#"[{"value":{"Name":"Cell1","Product":"Product1"}},{"value":{"Name":"Cell2","Product":"Product2"}}]"#,
    );
    let v1 = json(r#"{"value":{"Name":"Cell1","Product":"Product1"}}"#);
    assert_eq!(
        eval("*[value.Product = 'Product1']", data.clone()),
        v1.clone()
    );
    assert_eq!(eval("**[value.Product = 'Product1']", data), v1);
}

#[test]
fn array_sort_types() {
    assert_eq!(
        eval("[{'value': 5.9}, {'value': 8}] ^(<value).value", jnull()),
        json("[5.9,8]")
    );
    assert_eq!(
        eval("[{'value': 'b'}, {'value': 'a'}] ^(<value).value", jnull()),
        json(r#"["a","b"]"#)
    );
}

// ---------------------------------------------------------------------------
// StringTest
// ---------------------------------------------------------------------------

#[test]
fn string_basic() {
    assert_eq!(eval("$string($)", json(r#""abc""#)), JValue::string("abc"));
    assert_eq!(eval("$string(100.0)", jnull()), JValue::string("100"));
    assert_eq!(eval("$string($)", json("true")), JValue::string("true"));
    assert_eq!(eval("$string(5)", jnull()), JValue::string("5"));
}

#[test]
fn string_exponent() {
    assert_eq!(
        eval("$string(x)", json(r#"{"x":100.0}"#)),
        JValue::string("100")
    );
    assert_eq!(
        eval("$string(x)", json(r#"{"x":1000000000000000000.0}"#)),
        JValue::string("1000000000000000000")
    );
    assert_eq!(
        eval("$string(x)", json(r#"{"x":1000000000000000000000.0}"#)),
        JValue::string("1e+21")
    );
}

#[test]
fn string_array() {
    assert_eq!(
        eval("[1..5].$string()", jnull()),
        json(r#"["1","2","3","4","5"]"#)
    );
}

#[test]
fn string_map_serialization() {
    assert_eq!(eval("$string($)", json("{}")), JValue::string("{}"));
    assert_eq!(
        eval("$string($)", json(r#"{"x":1}"#)),
        JValue::string(r#"{"x":1}"#)
    );
}

#[test]
fn string_escape() {
    assert_eq!(
        eval("$string($)", json(r#"{"a":"\""}"#)),
        JValue::string(r#"{"a":"\""}"#)
    );
    assert_eq!(
        eval("$string($)", json(r#"{"a":"\\"}"#)),
        JValue::string(r#"{"a":"\\"}"#)
    );
    assert_eq!(
        eval("$string($)", json(r#"{"a":"\t"}"#)),
        JValue::string(r#"{"a":"\t"}"#)
    );
    assert_eq!(
        eval("$string($)", json(r#"{"a":"\n"}"#)),
        JValue::string(r#"{"a":"\n"}"#)
    );
    assert_eq!(
        eval("$string($)", json(r#"{"a":"</"}"#)),
        JValue::string(r#"{"a":"</"}"#)
    );
}

#[test]
fn string_split() {
    assert_eq!(eval_u("$split(a, '-')", json("{}")), JValue::Undefined);
    assert_eq!(eval_u("a ~> $split('-')", json("{}")), JValue::Undefined);
    assert_eq!(eval("$split('', '')", jnull()), json("[]"));
    assert_eq!(
        eval("$split('a1b2c3d4', '', 4)", jnull()),
        json(r#"["a","1","b","2"]"#)
    );
    assert_eq!(
        eval("$split('this..is.a.test', '.')", jnull()),
        json(r#"["this","","is","a","test"]"#)
    );
    assert_eq!(
        eval("$split('this..is.a.test...', '.')", jnull()),
        json(r#"["this","","is","a","test","","",""]"#)
    );
    assert_eq!(
        eval("$split('this..is.a.test...', /\\./)", jnull()),
        json(r#"["this","","is","a","test","","",""]"#)
    );
    assert_eq!(
        eval(
            "$split('this.*.*is.*a.*test.*.*.*.*.*.*', '.*', 8)",
            jnull()
        ),
        json(r#"["this","","is","a","test","","",""]"#)
    );
    assert_eq!(
        eval(
            "$split('this.*.*is.*a.*test.*.*.*.*.*.*', /\\.\\*/, 8)",
            jnull()
        ),
        json(r#"["this","","is","a","test","","",""]"#)
    );
}

#[test]
fn string_trim() {
    assert_eq!(eval("$trim(\"\n\")", jnull()), JValue::string(""));
    assert_eq!(eval("$trim(\" \")", jnull()), JValue::string(""));
    assert_eq!(eval("$trim(\"\")", jnull()), JValue::string(""));
    assert_eq!(eval_u("$trim(notthere)", jnull()), JValue::Undefined);
}

#[test]
fn string_eval() {
    assert_eq!(
        eval(
            "(  $data := {'Wert1': 'AAA', 'Wert2': 'BBB'};  $eval('$data.Wert1') )",
            jnull()
        ),
        JValue::string("AAA")
    );
}

#[test]
fn string_regex_no_panic() {
    // check for IndexOutOfBoundsException-equivalent
    assert!(Jsonata::new("/endsWithSlash-i/i").is_ok());
}

#[test]
fn string_fieldname_special_char() {
    let o = json("{\"a\\nb\":\"c\\nd\"}");
    assert_eq!(eval("$ ~> |$|{}|", o.clone()), o);
}

// ---------------------------------------------------------------------------
// NumberTest
// ---------------------------------------------------------------------------

#[test]
fn number_compute() {
    assert_eq!(eval("x+0", json(r#"{"x":1.0}"#)), JValue::Number(1.0));
    assert_eq!(eval("x", json(r#"{"x":1.0}"#)), JValue::Number(1.0));
    assert_eq!(eval("$ / 2", json("1")), JValue::Number(0.5));
    assert_eq!(eval("1.0", jnull()), JValue::Number(1.0));
}

// ---------------------------------------------------------------------------
// VariableTest
// ---------------------------------------------------------------------------

#[test]
fn variable_context() {
    let input = json(
        r#"{"model":{"customer":{"identityDocumentNumber":"ABC123456","identityDocumentType":"ID_CARD"}}}"#,
    );
    let e = "($~>|$|$.model|)@$.\n({\n\"documentIdentityNumber\": customer.identityDocumentNumber,\n\"documentIdentityType\": customer.identityDocumentType\n})";
    assert_eq!(
        eval(e, input),
        json(r#"{"documentIdentityNumber":"ABC123456","documentIdentityType":"ID_CARD"}"#)
    );
}

#[test]
fn variable_context_simple() {
    assert_eq!(
        eval("model@$", json(r#"{"model":123}"#)),
        JValue::Number(123.0)
    );
}

// ---------------------------------------------------------------------------
// NullSafetyTest
// ---------------------------------------------------------------------------

#[test]
fn null_safety() {
    for expr in [
        "$sift(undefined, $uppercase)",
        "$each(undefined, $uppercase)",
        "$keys(null)",
        "$map(null, $uppercase)",
        "$filter(null, $uppercase)",
        "$single(null, $uppercase)",
        "$reduce(null, $uppercase)",
        "$lookup(null, 'anykey')",
        "$spread(null)",
    ] {
        // Java NullSafetyTest uses evaluate(null) (output null conversion on),
        // so a NULL_VALUE result (e.g. $spread(null)) becomes null/undefined.
        assert_eq!(eval(expr, jnull()), JValue::Undefined, "expr={}", expr);
    }
}

#[test]
fn null_safety_array_index_preserves_null() {
    // jsonata-java NullSafetyTest.testArrayIndexPreservesNull (fix #111/#112):
    // indexing into an array element that is JSON null must yield null, not
    // silently drop it.
    let data = json("[[1,null,3],[2,null,4],[3,null,5]]");
    let expr = "$map($, function($v) { $v[1] })";

    // With null-conversion off, the port keeps the JSON nulls as distinct
    // NULL_VALUEs — the faithful representation of Java's preserved nulls.
    assert_eq!(eval_u(expr, data.clone()), json("[null,null,null]"));

    // The nulls are not dropped from the mapped sequence...
    assert_eq!(
        eval("$count($map($, function($v){$v[1]}))", data.clone()),
        JValue::Number(3.0)
    );

    // ...and Java's default (convert-on) evaluate serializes to [null,null,null].
    assert_eq!(
        eval("$string($map($, function($v){$v[1]}))", data),
        JValue::string("[null,null,null]")
    );

    // Direct index into a null element.
    assert_eq!(eval_u("$[1]", json("[1,null,3]")), JValue::Null);
}

// ---------------------------------------------------------------------------
// TypesTest (universal subset)
// ---------------------------------------------------------------------------

#[test]
fn types_cast_in() {
    assert_eq!(eval("3 in $", json("[1.0,2.0]")), JValue::Bool(false));
    assert_eq!(eval("1 in $", json("[1.0,2.0]")), JValue::Bool(true));
}

#[test]
fn types_cast_equals() {
    assert_eq!(eval("1 = $", json("1.0")), JValue::Bool(true));
    assert_eq!(eval("1 = $", json("2.0")), JValue::Bool(false));
    assert_eq!(eval("{'x':1 } = {'x':1 }", jnull()), JValue::Bool(true));
    assert_eq!(eval("{'x':1 } = {'x':2 }", jnull()), JValue::Bool(false));
    assert_eq!(eval("[1,null] = [1,null]", jnull()), JValue::Bool(true));
    assert_eq!(eval("[1,null] = [2,null]", jnull()), JValue::Bool(false));
}

// ---------------------------------------------------------------------------
// ExceptionTest
// ---------------------------------------------------------------------------

#[test]
fn exception_error() {
    assert_eq!(eval_err("$error('message')", jnull()).message(), "message");
}

#[test]
fn exception_div_zero() {
    assert_eq!(
        eval_err("1 / 0", jnull()).message(),
        "Number out of range: \"Infinity\""
    );
}

#[test]
fn exception_assert_custom_message() {
    assert_eq!(
        eval_err("$assert(false, 'message')", jnull()).message(),
        "message"
    );
}

// ---------------------------------------------------------------------------
// RuntimeTest
// ---------------------------------------------------------------------------

#[test]
fn runtime_bounds() {
    let expr = "($a := function(){42};$b := function(){$a()};$c := function(){$b()};)";
    let j = Jsonata::new(expr).unwrap();

    let frame = j.create_frame();
    frame.borrow_mut().set_runtime_bounds(1000, 2);
    assert!(j.evaluate(jnull(), Some(frame)).is_err());

    let frame = j.create_frame();
    frame.borrow_mut().set_runtime_bounds(1000, 3);
    assert!(j.evaluate(jnull(), Some(frame)).is_ok());
}

// ---------------------------------------------------------------------------
// CustomFunctionTest
// ---------------------------------------------------------------------------

#[test]
fn custom_supplier() {
    let mut j = Jsonata::new("$greet()").unwrap();
    j.register_function(
        "greet",
        None,
        Rc::new(|_args| Ok(JValue::string("Hello world"))),
    );
    assert_eq!(
        j.evaluate(jnull(), None).unwrap(),
        JValue::string("Hello world")
    );
}

#[test]
fn custom_eval() {
    let mut j = Jsonata::new("$eval('$greet()')").unwrap();
    j.register_function(
        "greet",
        None,
        Rc::new(|_args| Ok(JValue::string("Hello world"))),
    );
    assert_eq!(
        j.evaluate(jnull(), None).unwrap(),
        JValue::string("Hello world")
    );
}

#[test]
fn custom_unary() {
    let mut j = Jsonata::new("$echo(123)").unwrap();
    j.register_function("echo", None, Rc::new(|args| Ok(args[0].clone())));
    assert_eq!(j.evaluate(jnull(), None).unwrap(), JValue::Number(123.0));
}

#[test]
fn custom_binary() {
    let mut j = Jsonata::new("$add(21, 21)").unwrap();
    j.register_function(
        "add",
        None,
        Rc::new(|args| {
            Ok(JValue::Number(
                args[0].as_f64().unwrap() + args[1].as_f64().unwrap(),
            ))
        }),
    );
    assert_eq!(j.evaluate(jnull(), None).unwrap(), JValue::Number(42.0));
}

#[test]
fn custom_ternary() {
    let mut j = Jsonata::new("$abc(a,b,c)").unwrap();
    j.register_function(
        "abc",
        Some("<sss:s>"),
        Rc::new(|args| {
            Ok(JValue::string(format!(
                "{}{}{}",
                args[0].as_str().unwrap(),
                args[1].as_str().unwrap(),
                args[2].as_str().unwrap()
            )))
        }),
    );
    assert_eq!(
        j.evaluate(json(r#"{"a":"a","b":"b","c":"c"}"#), None)
            .unwrap(),
        JValue::string("abc")
    );
}

#[test]
fn custom_signature_error() {
    let mut j = Jsonata::new("$append(1, 2)").unwrap();
    j.register_function(
        "append",
        Some("<nb:s>"),
        Rc::new(|args| Ok(JValue::string(format!("{:?}{:?}", args[0], args[1])))),
    );
    let err = j.evaluate(jnull(), None).expect_err("T0410");
    assert_eq!(err.error, "T0410");
    assert_eq!(
        err.expected.as_ref().and_then(|v| v.as_str()),
        Some("append")
    );
}

// ---------------------------------------------------------------------------
// SignatureTest
// ---------------------------------------------------------------------------

#[test]
fn signature_params_to_arrays() {
    let mut j = Jsonata::new("$greet(1,null,3)").unwrap();
    j.set_output_convert_nulls(false);
    j.register_function(
        "greet",
        Some("<a?a?a?a?:s>"),
        Rc::new(|args| {
            // return the (coerced) args as an array to inspect the coercion
            Ok(JValue::array(args.to_vec(), Default::default()))
        }),
    );
    let res = j.evaluate(jnull(), None).unwrap();
    // Java result: "[[1], null, [3], null]" — 1 wrapped to [1]; the explicit
    // null and the missing 4th arg both become Java null (undefined here).
    if let JValue::Array(a, _) = &res {
        assert_eq!(a[0], json("[1]"));
        assert!(matches!(a[1], JValue::Undefined));
        assert_eq!(a[2], json("[3]"));
        assert!(matches!(a[3], JValue::Undefined));
    } else {
        panic!("expected array, got {:?}", res);
    }
}

#[test]
fn signature_error_choice() {
    let mut j = Jsonata::new("$foo()").unwrap();
    j.register_function("foo", Some("(sao)"), Rc::new(|_args| Ok(JValue::Undefined)));
    // null not allowed (undefined input -> context is undefined)
    assert!(j.evaluate(jnull(), None).is_err());
    assert!(j.evaluate(JValue::Bool(true), None).is_err());
}

#[test]
fn signature_var_arg() {
    let mut j = Jsonata::new("$sumvar(1,2,3)").unwrap();
    j.register_function(
        "sumvar",
        Some("<n+:n>"),
        Rc::new(|args| Ok(JValue::Number(args.iter().filter_map(|v| v.as_f64()).sum()))),
    );
    assert_eq!(j.evaluate(jnull(), None).unwrap(), JValue::Number(6.0));
}

// ---------------------------------------------------------------------------
// RegexTest
// ---------------------------------------------------------------------------

#[test]
fn regex_literal() {
    // a /regex/ literal evaluates to a regex value rendered as its pattern
    let r = eval("/^test.*$/", jnull());
    assert!(matches!(r, JValue::Regex(_)));
}

#[test]
fn regex_closure_answer() {
    let r = eval(
        "( $matcher := $eval('/l/'); ('Hello World' ~> $matcher); )",
        jnull(),
    );
    let o = r.as_object().expect("object");
    assert_eq!(o.get("match").and_then(|v| v.as_str()), Some("l"));
    assert_eq!(o.get("start").and_then(|v| v.as_f64()), Some(2.0));
    assert_eq!(o.get("end").and_then(|v| v.as_f64()), Some(3.0));
    assert_eq!(o.get("groups").cloned().unwrap(), json(r#"["l"]"#));
    assert!(o.get("next").map(|v| v.is_function()).unwrap_or(false));
}

#[test]
fn regex_closure_next() {
    let r = eval(
        "( $matcher := $eval('/l/'); ('Hello World' ~> $matcher).next(); )",
        jnull(),
    );
    let o = r.as_object().expect("object");
    assert_eq!(o.get("match").and_then(|v| v.as_str()), Some("l"));
    assert_eq!(o.get("start").and_then(|v| v.as_f64()), Some(3.0));
    assert_eq!(o.get("end").and_then(|v| v.as_f64()), Some(4.0));
}

// ---------------------------------------------------------------------------
// ParseIntegerTest / DateTimeTest
// ---------------------------------------------------------------------------

#[test]
fn parse_integer_no_error() {
    assert_eq!(
        eval_u("$parseInteger('xyz','000')", jnull()),
        JValue::Undefined
    );
}

#[test]
fn datetime_format_integer() {
    assert_eq!(
        eval("$toMillis('2018th', '[Y0001;o]')", jnull()),
        JValue::Number(1514764800000.0)
    );
}

#[test]
fn datetime_to_millis_roundtrip() {
    let r = eval(
        "$fromMillis($toMillis($))",
        JValue::string("2024-08-27T22:43:15.78133"),
    );
    let s = r.as_str().unwrap();
    assert!(s.starts_with("2024-08-2"), "got {}", s);
    assert!(s.ends_with(":43:15.781Z"), "got {}", s);
}

// ---------------------------------------------------------------------------
// SerializationTest (behaviour only)
// ---------------------------------------------------------------------------

#[test]
fn serialization_custom_function_value() {
    let mut j = Jsonata::new("$hi() & '!'").unwrap();
    j.register_function("hi", None, Rc::new(|_a| Ok(JValue::string("hello world"))));
    assert_eq!(
        j.evaluate(jnull(), None).unwrap(),
        JValue::string("hello world!")
    );
}

// ---------------------------------------------------------------------------
// Thread safety: a compiled Jsonata can be evaluated repeatedly.
// ---------------------------------------------------------------------------

#[test]
fn reuse_compiled_expression() {
    let j = Jsonata::new("a + b").unwrap();
    assert_eq!(
        j.evaluate(json(r#"{"a":1,"b":2}"#), None).unwrap(),
        JValue::Number(3.0)
    );
    assert_eq!(
        j.evaluate(json(r#"{"a":10,"b":20}"#), None).unwrap(),
        JValue::Number(30.0)
    );
}

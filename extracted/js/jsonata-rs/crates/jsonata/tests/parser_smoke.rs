use jsonata::parser::Parser;

fn ptype(expr: &str) -> String {
    let mut p = Parser::new();
    match p.parse(expr) {
        Ok(n) => n.borrow().node_type.clone().unwrap_or_default(),
        Err(e) => format!("ERR:{}", e.error),
    }
}

#[test]
fn basic_parses() {
    assert_eq!(ptype("42"), "number");
    assert_eq!(ptype("(3*(4-2)+1.01e2)/-2"), "binary");
    assert_eq!(ptype("foo.bar"), "path");
    assert_eq!(ptype("foo.bar[0]"), "path");
    assert_eq!(ptype("a.b.c"), "path");
    assert_eq!(ptype("$x := 5"), "bind");
    assert_eq!(ptype("[1,2,3]"), "unary");
    assert_eq!(ptype("{\"a\": 1}"), "unary");
    assert_eq!(ptype("function($x){$x+1}"), "lambda");
    assert_eq!(ptype("$map([1,2], function($v){$v})"), "function");
    assert_eq!(ptype("a ? b : c"), "condition");
    assert_eq!(ptype("a and b or c"), "binary");
    assert_eq!(ptype("$sum([1..5])"), "function");
    assert_eq!(ptype("payload ~> $foo"), "apply");
    assert_eq!(ptype("Account.Order.Product^(Price)"), "path");
    assert_eq!(ptype("Account{`type`: value}"), "path");
    assert_eq!(ptype("$ ~> |x|{}, ['a']|"), "apply");
    // errors
    assert_eq!(ptype("1 + "), "ERR:S0207");
    assert_eq!(ptype(")"), "ERR:S0211");
}

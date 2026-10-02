//! Port of `com.dashjoin.jsonata.Parser` — a Pratt (top-down operator
//! precedence) parser plus the `processAST` post-parse stage.
//!
//! Java uses a class hierarchy of `Symbol` with polymorphic `nud`/`led`. We
//! dispatch on the symbol `id` inside [`Parser::nud`]/[`Parser::led`] instead,
//! and keep a binding-power table derived from the Java `register(...)` calls.

use std::collections::HashMap;
use std::rc::Rc;
use std::sync::Arc;

use crate::ast::{Node, NodeRef, NodeValue, Slot, SlotRef};
use crate::error::{JError, JResult};
use crate::signature::Signature;
use crate::tokenizer::{TokenValue, Tokenizer};
use crate::value::JValue;

fn nodevalue_to_jvalue(v: &NodeValue) -> JValue {
    match v {
        NodeValue::Str(s) => JValue::string(s.as_str()),
        NodeValue::Number(n) => JValue::Number(*n),
        NodeValue::Bool(b) => JValue::Bool(*b),
        NodeValue::Null => JValue::Null,
        NodeValue::None => JValue::Undefined,
        NodeValue::Regex(p, _, _) => JValue::string(p.as_str()),
    }
}

pub struct Parser {
    source_len: usize,
    pub recover: bool,
    lexer: Tokenizer,
    node: NodeRef,
    bp: HashMap<&'static str, i32>,
    pub errors: Vec<JError>,
    ancestor_label: i32,
    ancestor_index: i32,
    ancestry: Vec<NodeRef>,
    /// Current `expression()` nesting depth (see [`MAX_PARSE_DEPTH`]).
    depth: i32,
}

/// Hard cap on `expression()` recursion so pathologically nested input yields a
/// `JError` instead of overflowing the stack — in Rust an uncatchable process
/// abort, fatal for embedders such as the Python bindings. Java has no
/// equivalent guard (it throws a catchable `StackOverflowError` around ~5k
/// nested parens on a default JVM stack). 1000 is far beyond any real
/// expression and parses comfortably within a 2 MB stack.
const MAX_PARSE_DEPTH: i32 = 1000;

/// Binding powers derived from the `register(...)` calls in the Java `Parser`
/// constructor (NOT the `Tokenizer.operators` table — e.g. `|` and `**` are
/// registered as `Prefix` with bp 0).
fn binding_powers() -> HashMap<&'static str, i32> {
    let mut m = HashMap::new();
    for id in [
        "(end)",
        "(name)",
        "(literal)",
        "(regex)",
        ":",
        ";",
        ",",
        ")",
        "]",
        "}",
        "..",
        "**",
        "|",
    ] {
        m.insert(id, 0);
    }
    m.insert(".", 75);
    m.insert("+", 50);
    m.insert("-", 50);
    m.insert("*", 60);
    m.insert("/", 60);
    m.insert("%", 60);
    m.insert("=", 40);
    m.insert("<", 40);
    m.insert(">", 40);
    m.insert("!=", 40);
    m.insert("<=", 40);
    m.insert(">=", 40);
    m.insert("&", 50);
    m.insert("and", 30);
    m.insert("or", 25);
    m.insert("in", 40);
    m.insert("~>", 40);
    m.insert("??", 40);
    m.insert("(error)", 10);
    m.insert("(", 80);
    m.insert("[", 80);
    m.insert("^", 40);
    m.insert("{", 70);
    m.insert(":=", 10);
    m.insert("@", 80);
    m.insert("#", 80);
    m.insert("?", 20);
    m.insert("?:", 40);
    m
}

impl Parser {
    pub fn new() -> Parser {
        Parser {
            source_len: 0,
            recover: false,
            lexer: Tokenizer::new(""),
            node: Node::new_ref(),
            bp: binding_powers(),
            errors: Vec::new(),
            ancestor_label: 0,
            ancestor_index: 0,
            ancestry: Vec::new(),
            depth: 0,
        }
    }

    fn bp_of(&self, id: &str) -> i32 {
        *self.bp.get(id).unwrap_or(&0)
    }

    fn is_known_operator(&self, id: &str) -> bool {
        self.bp.contains_key(id)
    }

    // ---- error handling --------------------------------------------------

    fn handle_error(&mut self, err: JError) -> JResult<NodeRef> {
        if self.recover {
            // record the error and return an (error) sentinel node
            let mut e = err.clone();
            // remaining tokens are not tracked here
            e.error_type = Some("error".to_string());
            self.errors.push(e.clone());
            let mut n = Node::new();
            n.is_error = true;
            n.error = Some(e);
            Ok(n.into_ref())
        } else {
            Err(err)
        }
    }

    // ---- token stream ----------------------------------------------------

    fn advance(&mut self, id: Option<&str>, infix: bool) -> JResult<NodeRef> {
        if let Some(id) = id {
            let cur_id = self.node.borrow().id.clone();
            if cur_id != id {
                let code = if cur_id == "(end)" { "S0203" } else { "S0202" };
                let pos = self.node.borrow().position as i32;
                let val = self.node.borrow().value.clone();
                let err = JError::with_current_expected(
                    code,
                    pos,
                    JValue::string(id),
                    nodevalue_to_jvalue(&val),
                );
                return self.handle_error(err);
            }
        }
        let next_token = self.lexer.next(infix)?;
        let next_token = match next_token {
            None => {
                let mut n = Node::new();
                n.id = "(end)".to_string();
                n.lbp = 0;
                n.position = self.source_len;
                self.node = n.into_ref();
                return Ok(self.node.clone());
            }
            Some(t) => t,
        };

        let ttype = next_token.token_type.clone();
        let (id, node_type, value): (String, String, NodeValue) = match ttype.as_str() {
            "name" | "variable" => {
                let v = match next_token.value {
                    TokenValue::Str(s) => NodeValue::Str(s),
                    _ => NodeValue::None,
                };
                ("(name)".to_string(), ttype, v)
            }
            "operator" => {
                let op = match &next_token.value {
                    TokenValue::Str(s) => s.clone(),
                    _ => String::new(),
                };
                if !self.is_known_operator(&op) {
                    let err = JError::with_current(
                        "S0204",
                        next_token.position as i32,
                        JValue::string(op.as_str()),
                    );
                    return self.handle_error(err);
                }
                (op.clone(), "operator".to_string(), NodeValue::Str(op))
            }
            "string" | "number" | "value" => {
                let v = match next_token.value {
                    TokenValue::Str(s) => NodeValue::Str(s),
                    TokenValue::Number(n) => NodeValue::Number(n),
                    TokenValue::Bool(b) => NodeValue::Bool(b),
                    TokenValue::Null => NodeValue::Null,
                    TokenValue::Regex(..) => NodeValue::None,
                };
                ("(literal)".to_string(), ttype, v)
            }
            "regex" => {
                let v = match next_token.value {
                    TokenValue::Regex(p, ci, ml) => NodeValue::Regex(p, ci, ml),
                    _ => NodeValue::None,
                };
                ("(regex)".to_string(), "regex".to_string(), v)
            }
            _ => {
                let err = JError::with_current(
                    "S0205",
                    next_token.position as i32,
                    nodevalue_to_jvalue(&NodeValue::None),
                );
                return self.handle_error(err);
            }
        };

        let lbp = self.bp_of(&id);
        let mut n = Node::new();
        n.id = id;
        n.value = value;
        n.node_type = Some(node_type);
        n.position = next_token.position;
        n.lbp = lbp;
        n.bp = lbp;
        self.node = n.into_ref();
        Ok(self.node.clone())
    }

    // ---- Pratt core ------------------------------------------------------

    fn expression(&mut self, rbp: i32) -> JResult<NodeRef> {
        self.depth += 1;
        if self.depth > MAX_PARSE_DEPTH {
            self.depth -= 1;
            // Stable code for telemetry; the limit detail goes in the message.
            return Err(JError::with_current(
                "PARSE_DEPTH",
                -1,
                JValue::string(format!("max={MAX_PARSE_DEPTH}")),
            ));
        }
        let result = self.expression_inner(rbp);
        self.depth -= 1;
        result
    }

    fn expression_inner(&mut self, rbp: i32) -> JResult<NodeRef> {
        let t = self.node.clone();
        self.advance(None, true)?;
        let mut left = self.nud(t)?;
        while rbp < self.node.borrow().lbp {
            let t = self.node.clone();
            self.advance(None, false)?;
            left = self.led(t, left)?;
        }
        Ok(left)
    }

    // ---- nud (prefix / terminal) ----------------------------------------

    fn nud(&mut self, node: NodeRef) -> JResult<NodeRef> {
        let id = node.borrow().id.clone();
        match id.as_str() {
            // Terminals (return self).
            "(name)" | "(literal)" | "(regex)" | "(end)" => Ok(node),
            // keyword operators usable as terminal/name.
            "and" | "or" | "in" => Ok(node),
            "*" => {
                node.borrow_mut().node_type = Some("wildcard".to_string());
                Ok(node)
            }
            "%" => {
                node.borrow_mut().node_type = Some("parent".to_string());
                Ok(node)
            }
            "**" => {
                node.borrow_mut().node_type = Some("descendant".to_string());
                Ok(node)
            }
            "-" => {
                // Prefix unary minus.
                let expr = self.expression(70)?;
                {
                    let mut n = node.borrow_mut();
                    n.expression = Some(expr);
                    n.node_type = Some("unary".to_string());
                }
                Ok(node)
            }
            "(" => self.nud_block(node),
            "[" => self.nud_array(node),
            "{" => self.object_parser(None),
            "|" => self.nud_transform(node),
            _ => {
                // base Symbol.nud — S0211
                let (pos, val) = {
                    let n = node.borrow();
                    (n.position as i32, n.value.clone())
                };
                let err = JError::with_current("S0211", pos, nodevalue_to_jvalue(&val));
                self.handle_error(err)
            }
        }
    }

    fn nud_block(&mut self, node: NodeRef) -> JResult<NodeRef> {
        let mut expressions = Vec::new();
        while self.node.borrow().id != ")" {
            expressions.push(self.expression(0)?);
            if self.node.borrow().id != ";" {
                break;
            }
            self.advance(Some(";"), false)?;
        }
        self.advance(Some(")"), true)?;
        {
            let mut n = node.borrow_mut();
            n.node_type = Some("block".to_string());
            n.expressions = Some(expressions);
        }
        Ok(node)
    }

    fn nud_array(&mut self, node: NodeRef) -> JResult<NodeRef> {
        let mut a = Vec::new();
        if self.node.borrow().id != "]" {
            loop {
                let mut item = self.expression(0)?;
                if self.node.borrow().id == ".." {
                    // range operator
                    let range = Node::new_ref();
                    {
                        let mut r = range.borrow_mut();
                        r.node_type = Some("binary".to_string());
                        r.value = NodeValue::Str("..".to_string());
                        r.position = self.node.borrow().position;
                        r.lhs = Some(item.clone());
                    }
                    self.advance(Some(".."), false)?;
                    let rhs = self.expression(0)?;
                    range.borrow_mut().rhs = Some(rhs);
                    item = range;
                }
                a.push(item);
                if self.node.borrow().id != "," {
                    break;
                }
                self.advance(Some(","), false)?;
            }
        }
        self.advance(Some("]"), true)?;
        {
            let mut n = node.borrow_mut();
            n.expressions = Some(a);
            n.node_type = Some("unary".to_string());
        }
        Ok(node)
    }

    fn nud_transform(&mut self, node: NodeRef) -> JResult<NodeRef> {
        let pattern = self.expression(0)?;
        self.advance(Some("|"), false)?;
        let update = self.expression(0)?;
        let mut delete = None;
        if self.node.borrow().id == "," {
            self.advance(Some(","), false)?;
            delete = Some(self.expression(0)?);
        }
        self.advance(Some("|"), false)?;
        {
            let mut n = node.borrow_mut();
            n.node_type = Some("transform".to_string());
            n.pattern = Some(pattern);
            n.update = Some(update);
            n.delete = delete;
        }
        Ok(node)
    }

    // ---- led (infix) -----------------------------------------------------

    fn led(&mut self, node: NodeRef, left: NodeRef) -> JResult<NodeRef> {
        let id = node.borrow().id.clone();
        match id.as_str() {
            // generic left-associative infix operators
            "." | "+" | "-" | "*" | "/" | "%" | "=" | "<" | ">" | "!=" | "<=" | ">=" | "&"
            | "and" | "or" | "in" | "~>" => {
                let bp = self.bp_of(&id);
                let rhs = self.expression(bp)?;
                let mut n = node.borrow_mut();
                n.lhs = Some(left);
                n.rhs = Some(rhs);
                n.node_type = Some("binary".to_string());
                drop(n);
                Ok(node)
            }
            "??" => self.led_coalesce(node, left),
            "(" => self.led_function(node, left),
            "[" => self.led_filter(node, left),
            "^" => self.led_orderby(node, left),
            "{" => self.object_parser(Some(left)),
            ":=" => self.led_bind(node, left),
            "@" => self.led_focus(node, left),
            "#" => self.led_index(node, left),
            "?" => self.led_ternary(node, left),
            "?:" => self.led_elvis(node, left),
            "(error)" => Err(JError::new("S0201")),
            _ => Err(JError::new("S0204")),
        }
    }

    fn led_coalesce(&mut self, node: NodeRef, left: NodeRef) -> JResult<NodeRef> {
        // ?? : condition = exists(left) ; then = left ; else = expression(0)
        let cond = Node::new_ref();
        {
            let c = cond.borrow_mut();
            drop(c);
        }
        {
            let mut c = cond.borrow_mut();
            c.node_type = Some("function".to_string());
            c.value = NodeValue::Str("(".to_string());
            let p = Node::new_ref();
            {
                let mut pp = p.borrow_mut();
                pp.node_type = Some("variable".to_string());
                pp.value = NodeValue::Str("exists".to_string());
            }
            c.procedure = Some(p);
            c.arguments = Some(vec![deep_clone(&left)]);
        }
        let els = self.expression(0)?;
        {
            let mut n = node.borrow_mut();
            n.node_type = Some("condition".to_string());
            n.condition = Some(cond);
            n.then = Some(left);
            n.els = Some(els);
        }
        Ok(node)
    }

    fn led_function(&mut self, node: NodeRef, left: NodeRef) -> JResult<NodeRef> {
        {
            let mut n = node.borrow_mut();
            n.procedure = Some(left.clone());
            n.node_type = Some("function".to_string());
            n.arguments = Some(Vec::new());
        }
        if self.node.borrow().id != ")" {
            loop {
                let is_q = {
                    let cur = self.node.borrow();
                    cur.node_type.as_deref() == Some("operator") && cur.id == "?"
                };
                if is_q {
                    node.borrow_mut().node_type = Some("partial".to_string());
                    let q = self.node.clone();
                    node.borrow_mut().arguments.as_mut().unwrap().push(q);
                    self.advance(Some("?"), false)?;
                } else {
                    let arg = self.expression(0)?;
                    node.borrow_mut().arguments.as_mut().unwrap().push(arg);
                }
                if self.node.borrow().id != "," {
                    break;
                }
                self.advance(Some(","), false)?;
            }
        }
        self.advance(Some(")"), true)?;

        // lambda function definition?
        let (is_lambda, _) = {
            let l = left.borrow();
            let is_name = l.type_is("name");
            let is_fn = l.value.eq_str("function") || l.value.eq_str("\u{03BB}");
            (is_name && is_fn, ())
        };
        if is_lambda {
            // all arguments must be variables
            let args = node.borrow().arguments.clone().unwrap_or_default();
            for arg in &args {
                if !arg.borrow().type_is("variable") {
                    let (pos, val) = {
                        let a = arg.borrow();
                        (a.position as i32, a.value.clone())
                    };
                    let err = JError::with_current("S0208", pos, nodevalue_to_jvalue(&val));
                    return self.handle_error(err);
                }
            }
            node.borrow_mut().node_type = Some("lambda".to_string());
            // optional signature
            if self.node.borrow().id == "<" {
                let mut depth = 1;
                let mut sig = String::from("<");
                while depth > 0 && self.node.borrow().id != "{" && self.node.borrow().id != "(end)"
                {
                    let tok = self.advance(None, false)?;
                    let tid = tok.borrow().id.clone();
                    if tid == ">" {
                        depth -= 1;
                    } else if tid == "<" {
                        depth += 1;
                    }
                    sig.push_str(&tok.borrow().value.to_string_val());
                }
                self.advance(Some(">"), false)?;
                let signature = Signature::new(&sig, "lambda");
                if let Some(err) = &signature.parse_error {
                    return Err(JError::at(&err.code, err.location));
                }
                node.borrow_mut().signature = Some(Arc::new(signature));
            }
            self.advance(Some("{"), false)?;
            let body = self.expression(0)?;
            node.borrow_mut().body = Some(body);
            self.advance(Some("}"), false)?;
        }
        Ok(node)
    }

    fn led_filter(&mut self, node: NodeRef, left: NodeRef) -> JResult<NodeRef> {
        if self.node.borrow().id == "]" {
            // empty predicate => keepArray on the underlying step
            let mut step = left.clone();
            loop {
                let is_bracket = {
                    let s = step.borrow();
                    s.type_is("binary") && s.value.eq_str("[")
                };
                if !is_bracket {
                    break;
                }
                let lhs = step.borrow().lhs.clone();
                match lhs {
                    Some(l) => step = l,
                    None => break,
                }
            }
            step.borrow_mut().keep_array = true;
            self.advance(Some("]"), false)?;
            Ok(left)
        } else {
            let rhs = self.expression(self.bp_of("]"))?;
            {
                let mut n = node.borrow_mut();
                n.lhs = Some(left);
                n.rhs = Some(rhs);
                n.node_type = Some("binary".to_string());
            }
            self.advance(Some("]"), true)?;
            Ok(node)
        }
    }

    fn led_orderby(&mut self, node: NodeRef, left: NodeRef) -> JResult<NodeRef> {
        self.advance(Some("("), false)?;
        let mut terms = Vec::new();
        loop {
            let term = Node::new_ref();
            term.borrow_mut().descending = false;
            if self.node.borrow().id == "<" {
                self.advance(Some("<"), false)?;
            } else if self.node.borrow().id == ">" {
                term.borrow_mut().descending = true;
                self.advance(Some(">"), false)?;
            }
            let expr = self.expression(0)?;
            term.borrow_mut().expression = Some(expr);
            terms.push(term);
            if self.node.borrow().id != "," {
                break;
            }
            self.advance(Some(","), false)?;
        }
        self.advance(Some(")"), false)?;
        {
            let mut n = node.borrow_mut();
            n.lhs = Some(left);
            n.rhs_terms = Some(terms);
            n.node_type = Some("binary".to_string());
        }
        Ok(node)
    }

    fn led_bind(&mut self, node: NodeRef, left: NodeRef) -> JResult<NodeRef> {
        if !left.borrow().type_is("variable") {
            let (pos, val) = {
                let l = left.borrow();
                (l.position as i32, l.value.clone())
            };
            let err = JError::with_current("S0212", pos, nodevalue_to_jvalue(&val));
            return self.handle_error(err);
        }
        let rhs = self.expression(self.bp_of(":=") - 1)?;
        {
            let mut n = node.borrow_mut();
            n.lhs = Some(left);
            n.rhs = Some(rhs);
            n.node_type = Some("binary".to_string());
        }
        Ok(node)
    }

    fn led_focus(&mut self, node: NodeRef, left: NodeRef) -> JResult<NodeRef> {
        let rhs = self.expression(self.bp_of("@"))?;
        if !rhs.borrow().type_is("variable") {
            let pos = rhs.borrow().position as i32;
            let err = JError::with_current("S0214", pos, JValue::string("@"));
            return self.handle_error(err);
        }
        {
            let mut n = node.borrow_mut();
            n.lhs = Some(left);
            n.rhs = Some(rhs);
            n.node_type = Some("binary".to_string());
        }
        Ok(node)
    }

    fn led_index(&mut self, node: NodeRef, left: NodeRef) -> JResult<NodeRef> {
        let rhs = self.expression(self.bp_of("#"))?;
        if !rhs.borrow().type_is("variable") {
            let pos = rhs.borrow().position as i32;
            let err = JError::with_current("S0214", pos, JValue::string("#"));
            return self.handle_error(err);
        }
        {
            let mut n = node.borrow_mut();
            n.lhs = Some(left);
            n.rhs = Some(rhs);
            n.node_type = Some("binary".to_string());
        }
        Ok(node)
    }

    fn led_ternary(&mut self, node: NodeRef, left: NodeRef) -> JResult<NodeRef> {
        {
            let mut n = node.borrow_mut();
            n.node_type = Some("condition".to_string());
            n.condition = Some(left);
        }
        let then = self.expression(0)?;
        node.borrow_mut().then = Some(then);
        if self.node.borrow().id == ":" {
            self.advance(Some(":"), false)?;
            let els = self.expression(0)?;
            node.borrow_mut().els = Some(els);
        }
        Ok(node)
    }

    fn led_elvis(&mut self, node: NodeRef, left: NodeRef) -> JResult<NodeRef> {
        let cond = deep_clone(&left);
        let els = self.expression(0)?;
        {
            let mut n = node.borrow_mut();
            n.node_type = Some("condition".to_string());
            n.condition = Some(cond);
            n.then = Some(left);
            n.els = Some(els);
        }
        Ok(node)
    }

    fn object_parser(&mut self, left: Option<NodeRef>) -> JResult<NodeRef> {
        let res = Node::new_ref();
        let mut a: Vec<(NodeRef, NodeRef)> = Vec::new();
        if self.node.borrow().id != "}" {
            loop {
                let n = self.expression(0)?;
                self.advance(Some(":"), false)?;
                let v = self.expression(0)?;
                a.push((n, v));
                if self.node.borrow().id != "," {
                    break;
                }
                self.advance(Some(","), false)?;
            }
        }
        self.advance(Some("}"), true)?;
        {
            let mut r = res.borrow_mut();
            match left {
                None => {
                    r.lhs_object = Some(a);
                    r.node_type = Some("unary".to_string());
                    r.value = NodeValue::Str("{".to_string());
                }
                Some(l) => {
                    r.lhs = Some(l);
                    r.rhs_object = Some(a);
                    r.node_type = Some("binary".to_string());
                    r.value = NodeValue::Str("{".to_string());
                }
            }
        }
        Ok(res)
    }

    // ---- tail-call optimization -----------------------------------------

    fn tail_call_optimize(&self, expr: NodeRef) -> NodeRef {
        let (is_fn_no_pred, is_cond, is_block) = {
            let e = expr.borrow();
            (
                e.type_is("function") && e.predicate.is_none(),
                e.type_is("condition"),
                e.type_is("block"),
            )
        };
        if is_fn_no_pred {
            let thunk = Node::new_ref();
            {
                let mut t = thunk.borrow_mut();
                t.node_type = Some("lambda".to_string());
                t.thunk = true;
                t.arguments = Some(Vec::new());
                t.position = expr.borrow().position;
                t.body = Some(expr.clone());
            }
            thunk
        } else if is_cond {
            let then = expr.borrow().then.clone();
            if let Some(then) = then {
                let opt = self.tail_call_optimize(then);
                expr.borrow_mut().then = Some(opt);
            }
            let els = expr.borrow().els.clone();
            if let Some(els) = els {
                let opt = self.tail_call_optimize(els);
                expr.borrow_mut().els = Some(opt);
            }
            expr
        } else if is_block {
            let len = expr
                .borrow()
                .expressions
                .as_ref()
                .map(|e| e.len())
                .unwrap_or(0);
            if len > 0 {
                let last = expr.borrow().expressions.as_ref().unwrap()[len - 1].clone();
                let opt = self.tail_call_optimize(last);
                expr.borrow_mut().expressions.as_mut().unwrap()[len - 1] = opt;
            }
            expr
        } else {
            expr
        }
    }

    // ---- ancestor / parent resolution -----------------------------------

    fn seek_parent(&mut self, node: NodeRef, slot: SlotRef) -> JResult<SlotRef> {
        let ntype = node.borrow().node_type.clone().unwrap_or_default();
        let mut slot = slot;
        match ntype.as_str() {
            "name" | "wildcard" => {
                slot.borrow_mut().level -= 1;
                if slot.borrow().level == 0 {
                    let has_ancestor = node.borrow().ancestor.is_some();
                    if !has_ancestor {
                        node.borrow_mut().ancestor = Some(slot.clone());
                    } else {
                        let idx = slot.borrow().index;
                        let ancestor_label = node
                            .borrow()
                            .ancestor
                            .as_ref()
                            .unwrap()
                            .borrow()
                            .label
                            .clone();
                        // ancestry.get(index).slot.label = node.ancestor.label
                        if let Some(anc) = self.ancestry.get(idx as usize) {
                            if let Some(s) = anc.borrow().slot.clone() {
                                s.borrow_mut().label = ancestor_label;
                            }
                        }
                        node.borrow_mut().ancestor = Some(slot.clone());
                    }
                    node.borrow_mut().tuple = true;
                }
            }
            "parent" => {
                slot.borrow_mut().level += 1;
            }
            "block" => {
                let last = {
                    let n = node.borrow();
                    n.expressions.as_ref().and_then(|e| e.last().cloned())
                };
                if let Some(last) = last {
                    node.borrow_mut().tuple = true;
                    slot = self.seek_parent(last, slot)?;
                }
            }
            "path" => {
                node.borrow_mut().tuple = true;
                let steps = node.borrow().steps.clone().unwrap_or_default();
                let mut index = steps.len() as i32 - 1;
                slot = self.seek_parent(steps[index as usize].clone(), slot)?;
                index -= 1;
                while slot.borrow().level > 0 && index >= 0 {
                    slot = self.seek_parent(steps[index as usize].clone(), slot)?;
                    index -= 1;
                }
            }
            _ => {
                let (pos, t) = {
                    let n = node.borrow();
                    (n.position as i32, n.node_type.clone().unwrap_or_default())
                };
                return Err(JError::with_current(
                    "S0217",
                    pos,
                    JValue::string(t.as_str()),
                ));
            }
        }
        Ok(slot)
    }

    fn push_ancestry(&self, result: &NodeRef, value: &NodeRef) {
        let (has_seeking, is_parent, seeking, vslot) = {
            let v = value.borrow();
            (
                v.seeking_parent.is_some(),
                v.type_is("parent"),
                v.seeking_parent.clone(),
                v.slot.clone(),
            )
        };
        if has_seeking || is_parent {
            let mut slots = seeking.unwrap_or_default();
            if is_parent {
                if let Some(s) = vslot {
                    slots.push(s);
                }
            }
            let mut r = result.borrow_mut();
            match r.seeking_parent {
                None => r.seeking_parent = Some(slots),
                Some(ref mut sp) => sp.extend(slots),
            }
        }
    }

    fn resolve_ancestry(&mut self, path: &NodeRef) -> JResult<()> {
        let steps = path.borrow().steps.clone().unwrap_or_default();
        let laststep = steps[steps.len() - 1].clone();
        let mut slots = laststep.borrow().seeking_parent.clone().unwrap_or_default();
        if laststep.borrow().type_is("parent") {
            if let Some(s) = laststep.borrow().slot.clone() {
                slots.push(s);
            }
        }
        for slot in slots {
            let mut index = steps.len() as i32 - 2;
            let mut slot = slot;
            while slot.borrow().level > 0 {
                if index < 0 {
                    let mut p = path.borrow_mut();
                    match p.seeking_parent {
                        None => p.seeking_parent = Some(vec![slot.clone()]),
                        Some(ref mut sp) => sp.push(slot.clone()),
                    }
                    break;
                }
                let mut step = steps[index as usize].clone();
                index -= 1;
                // skip contiguous focus-binding steps
                while index >= 0
                    && step.borrow().focus.is_some()
                    && steps[index as usize].borrow().focus.is_some()
                {
                    step = steps[index as usize].clone();
                    index -= 1;
                }
                slot = self.seek_parent(step, slot)?;
            }
        }
        Ok(())
    }

    // ---- processAST ------------------------------------------------------

    fn process_ast(&mut self, expr: Option<NodeRef>) -> JResult<Option<NodeRef>> {
        let expr = match expr {
            None => return Ok(None),
            Some(e) => e,
        };
        let etype = expr.borrow().node_type.clone();
        let result: NodeRef = match etype.as_deref() {
            Some("binary") => self.process_binary(&expr)?,
            Some("unary") => self.process_unary(&expr)?,
            Some("function") | Some("partial") => {
                let result = Node::new_ref();
                {
                    let mut r = result.borrow_mut();
                    let e = expr.borrow();
                    r.node_type = e.node_type.clone();
                    r.name = e.name.clone();
                    r.value = e.value.clone();
                    r.position = e.position;
                }
                let args = expr.borrow().arguments.clone().unwrap_or_default();
                let mut new_args = Vec::new();
                for arg in args {
                    let arg_ast = self.process_ast(Some(arg))?.unwrap();
                    self.push_ancestry(&result, &arg_ast);
                    new_args.push(arg_ast);
                }
                result.borrow_mut().arguments = Some(new_args);
                let proc = expr.borrow().procedure.clone();
                let proc = self.process_ast(proc)?;
                result.borrow_mut().procedure = proc;
                result
            }
            Some("lambda") => {
                let result = Node::new_ref();
                {
                    let mut r = result.borrow_mut();
                    let e = expr.borrow();
                    r.node_type = Some("lambda".to_string());
                    r.arguments = e.arguments.clone();
                    r.signature = e.signature.clone();
                    r.position = e.position;
                }
                let body = expr.borrow().body.clone();
                let body = self.process_ast(body)?.unwrap();
                let body = self.tail_call_optimize(body);
                result.borrow_mut().body = Some(body);
                result
            }
            Some("condition") => {
                let result = Node::new_ref();
                result.borrow_mut().node_type = Some("condition".to_string());
                result.borrow_mut().position = expr.borrow().position;
                let cond = expr.borrow().condition.clone();
                let cond = self.process_ast(cond)?;
                if let Some(ref c) = cond {
                    self.push_ancestry(&result, c);
                }
                result.borrow_mut().condition = cond;
                let then = expr.borrow().then.clone();
                let then = self.process_ast(then)?;
                if let Some(ref t) = then {
                    self.push_ancestry(&result, t);
                }
                result.borrow_mut().then = then;
                let els = expr.borrow().els.clone();
                if els.is_some() {
                    let els = self.process_ast(els)?;
                    if let Some(ref e) = els {
                        self.push_ancestry(&result, e);
                    }
                    result.borrow_mut().els = els;
                }
                result
            }
            Some("transform") => {
                let result = Node::new_ref();
                result.borrow_mut().node_type = Some("transform".to_string());
                result.borrow_mut().position = expr.borrow().position;
                let pattern = expr.borrow().pattern.clone();
                result.borrow_mut().pattern = self.process_ast(pattern)?;
                let update = expr.borrow().update.clone();
                result.borrow_mut().update = self.process_ast(update)?;
                let delete = expr.borrow().delete.clone();
                if delete.is_some() {
                    result.borrow_mut().delete = self.process_ast(delete)?;
                }
                result
            }
            Some("block") => {
                let result = Node::new_ref();
                result.borrow_mut().node_type = Some("block".to_string());
                result.borrow_mut().position = expr.borrow().position;
                let exprs = expr.borrow().expressions.clone().unwrap_or_default();
                let mut new_exprs = Vec::new();
                for item in exprs {
                    let part = self.process_ast(Some(item))?.unwrap();
                    self.push_ancestry(&result, &part);
                    let consarray = {
                        let p = part.borrow();
                        p.consarray
                            || (p.type_is("path")
                                && p.steps
                                    .as_ref()
                                    .and_then(|s| s.first())
                                    .map(|s| s.borrow().consarray)
                                    .unwrap_or(false))
                    };
                    if consarray {
                        result.borrow_mut().consarray = true;
                    }
                    new_exprs.push(part);
                }
                result.borrow_mut().expressions = Some(new_exprs);
                result
            }
            Some("name") => {
                let result = Node::new_ref();
                {
                    let mut r = result.borrow_mut();
                    r.node_type = Some("path".to_string());
                    r.steps = Some(vec![expr.clone()]);
                    if expr.borrow().keep_array {
                        r.keep_singleton_array = true;
                    }
                }
                result
            }
            Some("parent") => {
                let result = Node::new_ref();
                let slot = Rc::new(std::cell::RefCell::new(Slot {
                    label: format!("!{}", self.ancestor_label),
                    level: 1,
                    index: self.ancestor_index,
                }));
                self.ancestor_label += 1;
                self.ancestor_index += 1;
                {
                    let mut r = result.borrow_mut();
                    r.node_type = Some("parent".to_string());
                    r.slot = Some(slot);
                }
                self.ancestry.push(result.clone());
                result
            }
            Some("string") | Some("number") | Some("value") | Some("wildcard")
            | Some("descendant") | Some("variable") | Some("regex") => expr.clone(),
            Some("operator") => {
                let val = expr.borrow().value.clone();
                if val.eq_str("and") || val.eq_str("or") || val.eq_str("in") {
                    expr.borrow_mut().node_type = Some("name".to_string());
                    self.process_ast(Some(expr.clone()))?.unwrap()
                } else if val.eq_str("?") {
                    expr.clone()
                } else {
                    let (pos, v) = {
                        let e = expr.borrow();
                        (e.position as i32, e.value.clone())
                    };
                    return Err(JError::with_current("S0201", pos, nodevalue_to_jvalue(&v)));
                }
            }
            Some("error") => {
                if expr.borrow().lhs.is_some() {
                    let lhs = expr.borrow().lhs.clone();
                    self.process_ast(lhs)?.unwrap()
                } else {
                    expr.clone()
                }
            }
            _ => {
                // default — unknown / (end)
                let is_end = expr.borrow().id == "(end)";
                let code = if is_end { "S0207" } else { "S0206" };
                let (pos, v) = {
                    let e = expr.borrow();
                    (e.position as i32, e.value.clone())
                };
                let err = JError::with_current(code, pos, nodevalue_to_jvalue(&v));
                if self.recover {
                    self.errors.push(err.clone());
                    let ret = Node::new_ref();
                    ret.borrow_mut().node_type = Some("error".to_string());
                    ret.borrow_mut().error = Some(err);
                    return Ok(Some(ret));
                } else {
                    return Err(err);
                }
            }
        };
        if expr.borrow().keep_array {
            result.borrow_mut().keep_array = true;
        }
        Ok(Some(result))
    }

    fn process_binary(&mut self, expr: &NodeRef) -> JResult<NodeRef> {
        let value = expr.borrow().value.clone();
        let op = value.to_string_val();
        match op.as_str() {
            "." => self.process_dot(expr),
            "[" => self.process_predicate(expr),
            "{" => self.process_group(expr),
            "^" => self.process_orderby(expr),
            ":=" => {
                let result = Node::new_ref();
                {
                    let mut r = result.borrow_mut();
                    r.node_type = Some("bind".to_string());
                    r.value = expr.borrow().value.clone();
                    r.position = expr.borrow().position;
                }
                let lhs = expr.borrow().lhs.clone();
                result.borrow_mut().lhs = self.process_ast(lhs)?;
                let rhs = expr.borrow().rhs.clone();
                result.borrow_mut().rhs = self.process_ast(rhs)?;
                let rhs2 = result.borrow().rhs.clone();
                if let Some(ref rhs) = rhs2 {
                    self.push_ancestry(&result, rhs);
                }
                Ok(result)
            }
            "@" => self.process_focus(expr),
            "#" => self.process_index(expr),
            "~>" => {
                let result = Node::new_ref();
                {
                    let mut r = result.borrow_mut();
                    r.node_type = Some("apply".to_string());
                    r.value = expr.borrow().value.clone();
                    r.position = expr.borrow().position;
                }
                let lhs = expr.borrow().lhs.clone();
                result.borrow_mut().lhs = self.process_ast(lhs)?;
                let rhs = expr.borrow().rhs.clone();
                result.borrow_mut().rhs = self.process_ast(rhs)?;
                let ka = {
                    let r = result.borrow();
                    r.lhs
                        .as_ref()
                        .map(|l| l.borrow().keep_array)
                        .unwrap_or(false)
                        || r.rhs
                            .as_ref()
                            .map(|l| l.borrow().keep_array)
                            .unwrap_or(false)
                };
                result.borrow_mut().keep_array = ka;
                Ok(result)
            }
            _ => {
                let result = Node::new_ref();
                {
                    let mut r = result.borrow_mut();
                    r.node_type = expr.borrow().node_type.clone();
                    r.value = expr.borrow().value.clone();
                    r.position = expr.borrow().position;
                }
                let lhs = expr.borrow().lhs.clone();
                result.borrow_mut().lhs = self.process_ast(lhs)?;
                let rhs = expr.borrow().rhs.clone();
                result.borrow_mut().rhs = self.process_ast(rhs)?;
                let lhs2 = result.borrow().lhs.clone();
                if let Some(ref l) = lhs2 {
                    self.push_ancestry(&result, l);
                }
                let rhs2 = result.borrow().rhs.clone();
                if let Some(ref r) = rhs2 {
                    self.push_ancestry(&result, r);
                }
                Ok(result)
            }
        }
    }

    fn process_dot(&mut self, expr: &NodeRef) -> JResult<NodeRef> {
        let lhs = expr.borrow().lhs.clone();
        let lstep = self.process_ast(lhs)?.unwrap();

        let result: NodeRef;
        if lstep.borrow().type_is("path") {
            result = lstep.clone();
        } else {
            result = Node::new_ref();
            let mut r = result.borrow_mut();
            r.node_type = Some("path".to_string());
            r.steps = Some(vec![lstep.clone()]);
        }
        if lstep.borrow().type_is("parent") {
            let slot = lstep.borrow().slot.clone();
            result.borrow_mut().seeking_parent = Some(vec![slot.unwrap()]);
        }
        let rhs = expr.borrow().rhs.clone();
        let rest = self.process_ast(rhs)?.unwrap();

        // next function in chain
        let chain = {
            let rest_b = rest.borrow();
            if rest_b.type_is("function") {
                if let Some(ref proc) = rest_b.procedure {
                    let proc_b = proc.borrow();
                    if proc_b.type_is("path")
                        && proc_b.steps.as_ref().map(|s| s.len()).unwrap_or(0) == 1
                        && proc_b.steps.as_ref().unwrap()[0].borrow().type_is("name")
                    {
                        // result last step is function && proc.steps[0].value instanceof Symbol
                        // We don't model "value instanceof Symbol", so skip nextFunction wiring.
                        // (Java condition also requires steps[0].value to be a Symbol, which our
                        //  representation never produces — name values are strings.)
                        false
                    } else {
                        false
                    }
                } else {
                    false
                }
            } else {
                false
            }
        };
        let _ = chain;

        if rest.borrow().type_is("path") {
            let rest_steps = rest.borrow().steps.clone().unwrap_or_default();
            result
                .borrow_mut()
                .steps
                .as_mut()
                .unwrap()
                .extend(rest_steps);
        } else {
            let has_pred = rest.borrow().predicate.is_some();
            if has_pred {
                let pred = rest.borrow().predicate.clone();
                rest.borrow_mut().stages = pred;
                rest.borrow_mut().predicate = None;
            }
            result
                .borrow_mut()
                .steps
                .as_mut()
                .unwrap()
                .push(rest.clone());
        }

        // string literal steps -> name; numbers/values are errors
        let steps = result.borrow().steps.clone().unwrap_or_default();
        for step in &steps {
            let stype = step.borrow().node_type.clone().unwrap_or_default();
            if stype == "number" || stype == "value" {
                let (pos, v) = {
                    let s = step.borrow();
                    (s.position as i32, s.value.clone())
                };
                return Err(JError::with_current("S0213", pos, nodevalue_to_jvalue(&v)));
            }
            if stype == "string" {
                step.borrow_mut().node_type = Some("name".to_string());
            }
        }
        // keepSingletonArray if any step keepArray
        if steps.iter().any(|s| s.borrow().keep_array) {
            result.borrow_mut().keep_singleton_array = true;
        }
        // first/last step consarray
        if let Some(first) = steps.first() {
            let is_arr = {
                let f = first.borrow();
                f.type_is("unary") && f.value.eq_str("[")
            };
            if is_arr {
                first.borrow_mut().consarray = true;
            }
        }
        if let Some(last) = steps.last() {
            let is_arr = {
                let l = last.borrow();
                l.type_is("unary") && l.value.eq_str("[")
            };
            if is_arr {
                last.borrow_mut().consarray = true;
            }
        }
        self.resolve_ancestry(&result)?;
        Ok(result)
    }

    fn process_predicate(&mut self, expr: &NodeRef) -> JResult<NodeRef> {
        let lhs = expr.borrow().lhs.clone();
        let result = self.process_ast(lhs)?.unwrap();
        let mut step = result.clone();
        let mut is_stages = false;
        if result.borrow().type_is("path") {
            let steps = result.borrow().steps.clone().unwrap();
            step = steps[steps.len() - 1].clone();
            is_stages = true;
        }
        if step.borrow().group.is_some() {
            return Err(JError::at("S0209", expr.borrow().position as i32));
        }
        if is_stages {
            if step.borrow().stages.is_none() {
                step.borrow_mut().stages = Some(Vec::new());
            }
        } else if step.borrow().predicate.is_none() {
            step.borrow_mut().predicate = Some(Vec::new());
        }
        let rhs = expr.borrow().rhs.clone();
        let predicate = self.process_ast(rhs)?.unwrap();
        if predicate.borrow().seeking_parent.is_some() {
            let sp = predicate.borrow().seeking_parent.clone().unwrap();
            for slot in sp {
                if slot.borrow().level == 1 {
                    self.seek_parent(step.clone(), slot)?;
                } else {
                    slot.borrow_mut().level -= 1;
                }
            }
            self.push_ancestry(&step, &predicate);
        }
        let s = Node::new_ref();
        {
            let mut sb = s.borrow_mut();
            sb.node_type = Some("filter".to_string());
            sb.expr = Some(predicate);
            sb.position = expr.borrow().position;
        }
        if expr.borrow().keep_array {
            step.borrow_mut().keep_array = true;
        }
        if is_stages {
            step.borrow_mut().stages.as_mut().unwrap().push(s);
        } else {
            step.borrow_mut().predicate.as_mut().unwrap().push(s);
        }
        Ok(result)
    }

    fn process_group(&mut self, expr: &NodeRef) -> JResult<NodeRef> {
        let lhs = expr.borrow().lhs.clone();
        let result = self.process_ast(lhs)?.unwrap();
        if result.borrow().group.is_some() {
            return Err(JError::at("S0210", expr.borrow().position as i32));
        }
        let group = Node::new_ref();
        let pairs = expr.borrow().rhs_object.clone().unwrap_or_default();
        let mut new_pairs = Vec::new();
        for (k, v) in pairs {
            let k2 = self.process_ast(Some(k))?.unwrap();
            let v2 = self.process_ast(Some(v))?.unwrap();
            new_pairs.push((k2, v2));
        }
        {
            let mut g = group.borrow_mut();
            g.lhs_object = Some(new_pairs);
            g.position = expr.borrow().position;
        }
        result.borrow_mut().group = Some(group);
        Ok(result)
    }

    fn process_orderby(&mut self, expr: &NodeRef) -> JResult<NodeRef> {
        let lhs = expr.borrow().lhs.clone();
        let mut result = self.process_ast(lhs)?.unwrap();
        if !result.borrow().type_is("path") {
            let res = Node::new_ref();
            {
                let mut r = res.borrow_mut();
                r.node_type = Some("path".to_string());
                r.steps = Some(vec![result.clone()]);
            }
            result = res;
        }
        let sort_step = Node::new_ref();
        {
            let mut s = sort_step.borrow_mut();
            s.node_type = Some("sort".to_string());
            s.position = expr.borrow().position;
        }
        let terms = expr.borrow().rhs_terms.clone().unwrap_or_default();
        let mut new_terms = Vec::new();
        for term in terms {
            let term_expr = term.borrow().expression.clone();
            let expression = self.process_ast(term_expr)?.unwrap();
            self.push_ancestry(&sort_step, &expression);
            let res = Node::new_ref();
            {
                let mut r = res.borrow_mut();
                r.descending = term.borrow().descending;
                r.expression = Some(expression);
            }
            new_terms.push(res);
        }
        sort_step.borrow_mut().terms = Some(new_terms);
        result.borrow_mut().steps.as_mut().unwrap().push(sort_step);
        self.resolve_ancestry(&result)?;
        Ok(result)
    }

    fn process_focus(&mut self, expr: &NodeRef) -> JResult<NodeRef> {
        let lhs = expr.borrow().lhs.clone();
        let result = self.process_ast(lhs)?.unwrap();
        let mut step = result.clone();
        if result.borrow().type_is("path") {
            let steps = result.borrow().steps.clone().unwrap();
            step = steps[steps.len() - 1].clone();
        }
        if step.borrow().stages.is_some() || step.borrow().predicate.is_some() {
            return Err(JError::at("S0215", expr.borrow().position as i32));
        }
        if step.borrow().type_is("sort") {
            return Err(JError::at("S0216", expr.borrow().position as i32));
        }
        if expr.borrow().keep_array {
            step.borrow_mut().keep_array = true;
        }
        let focus = expr
            .borrow()
            .rhs
            .as_ref()
            .and_then(|r| r.borrow().value.as_str().map(|s| s.to_string()));
        step.borrow_mut().focus = focus;
        step.borrow_mut().tuple = true;
        Ok(result)
    }

    fn process_index(&mut self, expr: &NodeRef) -> JResult<NodeRef> {
        let lhs = expr.borrow().lhs.clone();
        let mut result = self.process_ast(lhs)?.unwrap();
        let mut step = result.clone();
        if result.borrow().type_is("path") {
            let steps = result.borrow().steps.clone().unwrap();
            step = steps[steps.len() - 1].clone();
        } else {
            let res = Node::new_ref();
            {
                let mut r = res.borrow_mut();
                r.node_type = Some("path".to_string());
                r.steps = Some(vec![result.clone()]);
            }
            result = res;
            if step.borrow().predicate.is_some() {
                let pred = step.borrow().predicate.clone();
                step.borrow_mut().stages = pred;
                step.borrow_mut().predicate = None;
            }
        }
        let idx_name = expr
            .borrow()
            .rhs
            .as_ref()
            .and_then(|r| r.borrow().value.as_str().map(|s| s.to_string()));
        if step.borrow().stages.is_none() {
            step.borrow_mut().index = idx_name;
        } else {
            let res = Node::new_ref();
            {
                let mut r = res.borrow_mut();
                r.node_type = Some("index".to_string());
                r.value = expr
                    .borrow()
                    .rhs
                    .as_ref()
                    .map(|x| x.borrow().value.clone())
                    .unwrap_or(NodeValue::None);
                r.position = expr.borrow().position;
            }
            step.borrow_mut().stages.as_mut().unwrap().push(res);
        }
        step.borrow_mut().tuple = true;
        Ok(result)
    }

    fn process_unary(&mut self, expr: &NodeRef) -> JResult<NodeRef> {
        let result = Node::new_ref();
        {
            let mut r = result.borrow_mut();
            r.node_type = expr.borrow().node_type.clone();
            r.value = expr.borrow().value.clone();
            r.position = expr.borrow().position;
        }
        let expr_value = expr.borrow().value.to_string_val();
        if expr_value == "[" {
            let items = expr.borrow().expressions.clone().unwrap_or_default();
            let mut new_items = Vec::new();
            for item in items {
                let value = self.process_ast(Some(item))?.unwrap();
                self.push_ancestry(&result, &value);
                new_items.push(value);
            }
            result.borrow_mut().expressions = Some(new_items);
            Ok(result)
        } else if expr_value == "{" {
            let pairs = expr.borrow().lhs_object.clone().unwrap_or_default();
            let mut new_pairs = Vec::new();
            for (k, v) in pairs {
                let key = self.process_ast(Some(k))?.unwrap();
                self.push_ancestry(&result, &key);
                let value = self.process_ast(Some(v))?.unwrap();
                self.push_ancestry(&result, &value);
                new_pairs.push((key, value));
            }
            result.borrow_mut().lhs_object = Some(new_pairs);
            Ok(result)
        } else {
            let inner = expr.borrow().expression.clone();
            let inner = self.process_ast(inner)?.unwrap();
            result.borrow_mut().expression = Some(inner.clone());
            // unary minus on a number literal -> fold
            let is_minus_number = expr_value == "-" && inner.borrow().type_is("number");
            if is_minus_number {
                // result = result.expression (the number), negate its value
                let folded = inner;
                let fval = folded.borrow().value.clone();
                if let NodeValue::Number(n) = fval {
                    folded.borrow_mut().value = NodeValue::Number(-n);
                }
                Ok(folded)
            } else {
                self.push_ancestry(&result, &inner);
                Ok(result)
            }
        }
    }

    // ---- entry point -----------------------------------------------------

    pub fn parse(&mut self, jsonata: &str) -> JResult<NodeRef> {
        // Java `source.length()` — UTF-16 units (matches the tokenizer's
        // externally visible positions).
        self.source_len = jsonata.encode_utf16().count();
        self.lexer = Tokenizer::new(jsonata);
        self.advance(None, false)?;
        let expr = self.expression(0)?;
        if self.node.borrow().id != "(end)" {
            let (pos, v) = {
                let n = self.node.borrow();
                (n.position as i32, n.value.clone())
            };
            let err = JError::with_current("S0201", pos, nodevalue_to_jvalue(&v));
            self.handle_error(err)?;
        }
        let expr = self.process_ast(Some(expr))?.unwrap();
        let bad = {
            let e = expr.borrow();
            e.type_is("parent") || e.seeking_parent.is_some()
        };
        if bad {
            let (pos, t) = {
                let e = expr.borrow();
                (e.position as i32, e.node_type.clone().unwrap_or_default())
            };
            return Err(JError::with_current(
                "S0217",
                pos,
                JValue::string(t.as_str()),
            ));
        }
        Ok(expr)
    }
}

impl Default for Parser {
    fn default() -> Self {
        Parser::new()
    }
}

// ---------------------------------------------------------------------------
// Deep clone of a parse subtree (Java `Parser.clone` via serialization).
// Used by `??` and `?:` to make the condition/then branches independent.
// ---------------------------------------------------------------------------

pub fn deep_clone(node: &NodeRef) -> NodeRef {
    fn clone_opt(n: &Option<NodeRef>) -> Option<NodeRef> {
        n.as_ref().map(deep_clone)
    }
    fn clone_vec(v: &Option<Vec<NodeRef>>) -> Option<Vec<NodeRef>> {
        v.as_ref().map(|vec| vec.iter().map(deep_clone).collect())
    }
    fn clone_pairs(v: &Option<Vec<(NodeRef, NodeRef)>>) -> Option<Vec<(NodeRef, NodeRef)>> {
        v.as_ref().map(|vec| {
            vec.iter()
                .map(|(a, b)| (deep_clone(a), deep_clone(b)))
                .collect()
        })
    }
    fn clone_slot(s: &Option<SlotRef>) -> Option<SlotRef> {
        s.as_ref()
            .map(|slot| Rc::new(std::cell::RefCell::new(slot.borrow().clone())))
    }

    let src = node.borrow();
    let n = Node {
        id: src.id.clone(),
        node_type: src.node_type.clone(),
        value: src.value.clone(),
        bp: src.bp,
        lbp: src.lbp,
        position: src.position,
        keep_array: src.keep_array,
        descending: src.descending,
        keep_singleton_array: src.keep_singleton_array,
        consarray: src.consarray,
        level: src.level,
        thunk: src.thunk,
        tuple: src.tuple,
        is_error: src.is_error,
        expression: clone_opt(&src.expression),
        lhs: clone_opt(&src.lhs),
        rhs: clone_opt(&src.rhs),
        procedure: clone_opt(&src.procedure),
        body: clone_opt(&src.body),
        condition: clone_opt(&src.condition),
        then: clone_opt(&src.then),
        els: clone_opt(&src.els),
        pattern: clone_opt(&src.pattern),
        update: clone_opt(&src.update),
        delete: clone_opt(&src.delete),
        group: clone_opt(&src.group),
        expr: clone_opt(&src.expr),
        next_function: clone_opt(&src.next_function),
        steps: clone_vec(&src.steps),
        stages: clone_vec(&src.stages),
        predicate: clone_vec(&src.predicate),
        arguments: clone_vec(&src.arguments),
        expressions: clone_vec(&src.expressions),
        terms: clone_vec(&src.terms),
        rhs_terms: clone_vec(&src.rhs_terms),
        lhs_object: clone_pairs(&src.lhs_object),
        rhs_object: clone_pairs(&src.rhs_object),
        focus: src.focus.clone(),
        index: src.index.clone(),
        name: src.name.clone(),
        slot: clone_slot(&src.slot),
        ancestor: clone_slot(&src.ancestor),
        seeking_parent: src.seeking_parent.as_ref().map(|v| {
            v.iter()
                .map(|s| Rc::new(std::cell::RefCell::new(s.borrow().clone())))
                .collect()
        }),
        label: src.label.clone(),
        signature: src.signature.clone(),
        error: src.error.clone(),
    };
    n.into_ref()
}

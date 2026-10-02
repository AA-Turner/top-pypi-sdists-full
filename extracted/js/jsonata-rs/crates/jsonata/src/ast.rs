//! Abstract syntax tree node, mirroring the Java `Parser.Symbol` class.
//!
//! Java uses a single mutable `Symbol` class with many optional fields and a
//! `type`/`id` string discriminator. The parser and `processAST` mutate nodes
//! in place and share mutable "slot" objects between nodes (parent-operator
//! resolution). We mirror that with `Rc<RefCell<Node>>` and `Rc<RefCell<Slot>>`.
//! The tree is mutated during parsing/processing and read-only during eval.

use std::cell::RefCell;
use std::rc::Rc;

use crate::error::JError;

pub type NodeRef = Rc<RefCell<Node>>;
pub type SlotRef = Rc<RefCell<Slot>>;

/// The dynamic `value` field of a node / token.
#[derive(Debug, Clone, Default, PartialEq)]
pub enum NodeValue {
    #[default]
    None,
    Bool(bool),
    Number(f64),
    Str(String),
    /// JSON `null` literal token value (Java null).
    Null,
    /// A `/regex/` literal: (pattern, case_insensitive, multiline).
    Regex(String, bool, bool),
}

impl NodeValue {
    pub fn as_str(&self) -> Option<&str> {
        match self {
            NodeValue::Str(s) => Some(s),
            _ => None,
        }
    }
    /// Java `(""+value).equals(s)` / `value.equals(s)` for string-ish values.
    pub fn eq_str(&self, s: &str) -> bool {
        match self {
            NodeValue::Str(v) => v == s,
            _ => false,
        }
    }
    /// Java `"" + value` rendering.
    pub fn to_string_val(&self) -> String {
        match self {
            NodeValue::Str(v) => v.clone(),
            NodeValue::Bool(b) => b.to_string(),
            NodeValue::Number(n) => crate::functions::number_to_java_string(*n),
            NodeValue::Null => "null".to_string(),
            NodeValue::None => "null".to_string(),
            NodeValue::Regex(p, _, _) => p.clone(),
        }
    }
}

/// A shared mutable "slot" used by parent-operator (ancestor) resolution.
#[derive(Debug, Clone, Default)]
pub struct Slot {
    pub label: String,
    pub level: i32,
    pub index: i32,
}

#[derive(Default)]
pub struct Node {
    pub id: String,
    /// Node type ("name", "path", "binary", "unary", "function", "lambda", ...).
    pub node_type: Option<String>,
    pub value: NodeValue,
    pub bp: i32,
    pub lbp: i32,
    pub position: usize,

    pub keep_array: bool,
    pub descending: bool,
    pub keep_singleton_array: bool,
    pub consarray: bool,
    pub level: i32,
    pub thunk: bool,
    pub tuple: bool,
    /// True if this node carried a parse error sentinel.
    pub is_error: bool,

    // Single-child / operand links.
    pub expression: Option<NodeRef>,
    pub lhs: Option<NodeRef>,
    pub rhs: Option<NodeRef>,
    pub procedure: Option<NodeRef>,
    pub body: Option<NodeRef>,
    pub condition: Option<NodeRef>,
    pub then: Option<NodeRef>,
    pub els: Option<NodeRef>,
    pub pattern: Option<NodeRef>,
    pub update: Option<NodeRef>,
    pub delete: Option<NodeRef>,
    pub group: Option<NodeRef>,
    pub expr: Option<NodeRef>,
    pub next_function: Option<NodeRef>,

    // List children.
    pub steps: Option<Vec<NodeRef>>,
    pub stages: Option<Vec<NodeRef>>,
    pub predicate: Option<Vec<NodeRef>>,
    pub arguments: Option<Vec<NodeRef>>,
    pub expressions: Option<Vec<NodeRef>>,
    pub terms: Option<Vec<NodeRef>>,
    pub rhs_terms: Option<Vec<NodeRef>>,
    pub lhs_object: Option<Vec<(NodeRef, NodeRef)>>,
    pub rhs_object: Option<Vec<(NodeRef, NodeRef)>>,

    // Path / focus / index bookkeeping.
    pub focus: Option<String>,
    pub index: Option<String>,
    pub name: Option<NodeValue>,

    // Ancestor / parent operator bookkeeping.
    pub slot: Option<SlotRef>,
    pub ancestor: Option<SlotRef>,
    pub seeking_parent: Option<Vec<SlotRef>>,
    pub label: Option<String>,

    // Function / lambda signature. `Arc` (not `Rc`) so the same parsed
    // signature can be shared with the process-global builtin table; see
    // `evaluator::builtin_signatures`.
    pub signature: Option<std::sync::Arc<crate::signature::Signature>>,

    pub error: Option<JError>,
}

impl Node {
    pub fn new() -> Node {
        Node::default()
    }

    pub fn new_ref() -> NodeRef {
        Rc::new(RefCell::new(Node::default()))
    }

    pub fn into_ref(self) -> NodeRef {
        Rc::new(RefCell::new(self))
    }

    pub fn type_is(&self, t: &str) -> bool {
        self.node_type.as_deref() == Some(t)
    }

    /// Convert a literal node's value into a runtime JValue.
    pub fn literal_value(&self) -> crate::value::JValue {
        use crate::value::JValue;
        match &self.value {
            NodeValue::Bool(b) => JValue::Bool(*b),
            NodeValue::Number(n) => JValue::Number(*n),
            NodeValue::Str(s) => JValue::string(s.as_str()),
            NodeValue::Null => JValue::Null,
            NodeValue::None => JValue::Undefined,
            NodeValue::Regex(p, ci, ml) => JValue::Regex(std::rc::Rc::new(crate::value::JRegex {
                pattern: p.clone(),
                case_insensitive: *ci,
                multiline: *ml,
            })),
        }
    }
}

impl std::fmt::Debug for Node {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Node")
            .field("id", &self.id)
            .field("type", &self.node_type)
            .field("value", &self.value)
            .finish()
    }
}

/// Convenience: clone a `NodeRef` handle.
pub fn rc(node: Node) -> NodeRef {
    node.into_ref()
}

//! The JSONata runtime value model.
//!
//! Mirrors the Java port's object model where:
//!   * Java `null`  == "undefined" (absence of a value)  -> [`JValue::Undefined`]
//!   * `Jsonata.NULL_VALUE` == a JSON `null`              -> [`JValue::Null`]
//!   * numbers are stored as `f64` (Java parses every numeric literal through
//!     `Double.parseDouble` first, so this is faithful)
//!   * arrays carry the `JList` flags (sequence/keepSingleton/cons/...)
//!   * objects preserve insertion order (Java `LinkedHashMap`).

use indexmap::IndexMap;
use std::cell::RefCell;
use std::rc::Rc;
use std::sync::Arc;

use crate::ast::NodeRef;
use crate::error::{JError, JResult};
use crate::frame::Frame;
use crate::signature::Signature;

pub type Object = IndexMap<String, JValue>;

/// Flags attached to arrays, mirroring `Utils.JList`.
#[derive(Clone, Copy, Default, Debug, PartialEq, Eq)]
pub struct ArrayFlags {
    pub sequence: bool,
    pub outer_wrapper: bool,
    pub tuple_stream: bool,
    pub keep_singleton: bool,
    pub cons: bool,
    /// Marks a Java `JList` that carries no other flag (e.g. `$append` output,
    /// array-constructor/range results). Java code sometimes branches on
    /// `instanceof JList` — class identity, independent of the flags — e.g.
    /// `$distinct` returns a sequence (singleton-unwrapping) only for JList
    /// inputs. Inert everywhere else.
    pub jlist: bool,
}

impl ArrayFlags {
    pub fn sequence() -> ArrayFlags {
        ArrayFlags {
            sequence: true,
            ..Default::default()
        }
    }

    /// A plain `new JList<>()` — no semantic flags, but `instanceof JList`.
    pub fn jlist() -> ArrayFlags {
        ArrayFlags {
            jlist: true,
            ..Default::default()
        }
    }

    /// Java `arr instanceof JList` — true for any JList-derived list.
    pub fn is_jlist(&self) -> bool {
        self.jlist
            || self.sequence
            || self.outer_wrapper
            || self.tuple_stream
            || self.keep_singleton
            || self.cons
    }
}

/// A user-defined function (lambda / closure), mirroring the Java
/// `_jsonata_lambda` procedure Symbol created by `evaluateLambda`.
#[derive(Clone)]
pub struct Lambda {
    /// Captured input value at closure-creation time (`procedure.input`).
    pub input: JValue,
    /// Closure environment (`procedure.environment`).
    pub environment: Rc<RefCell<Frame>>,
    /// Parameter nodes (`procedure.arguments`); each `.value` is the param name.
    pub arguments: Vec<NodeRef>,
    pub signature: Option<Arc<Signature>>,
    /// Body AST (`procedure.body`). For a tail-call thunk this is the
    /// function-call node to evaluate on the trampoline.
    pub body: NodeRef,
    /// True if this is a tail-call thunk (deferred evaluation).
    pub thunk: bool,
}

/// The implementation of a native function value.
#[derive(Clone)]
pub enum NativeImpl {
    /// A built-in dispatched by name in the evaluator.
    Builtin,
    /// A user-supplied closure (custom function / PyO3 binding).
    Closure(Rc<dyn Fn(&[JValue]) -> JResult<JValue>>),
    /// A transformer produced by the `|...|` operator.
    Transform(Rc<crate::evaluator::TransformDef>),
}

/// A native (built-in or user) function value (`Jsonata.JFunction`).
#[derive(Clone)]
pub struct NativeFn {
    /// The JSONata function name, e.g. "sort", "number".
    pub name: String,
    pub signature: Option<Arc<Signature>>,
    pub implementation: NativeImpl,
}

/// A partially-applied function (`partialApplyProcedure` result).
#[derive(Clone)]
pub struct Partial {
    /// The function being partially applied.
    pub func: Box<JValue>,
    /// Supplied arguments, with `None` placeholders for the `?` holes.
    pub args: Vec<Option<JValue>>,
}

/// A compiled regular expression value produced by a `/regex/` literal.
/// Stored as the original pattern + flags so we can rebuild matchers; the
/// actual matching engine is selected in `functions::regex`.
#[derive(Clone)]
pub struct JRegex {
    pub pattern: String,
    pub case_insensitive: bool,
    pub multiline: bool,
}

#[derive(Clone)]
pub enum JValue {
    /// Java `null` == undefined / no value.
    Undefined,
    /// JSON `null` == `Jsonata.NULL_VALUE`.
    Null,
    Bool(bool),
    Number(f64),
    String(Rc<str>),
    Array(Rc<Vec<JValue>>, ArrayFlags),
    Object(Rc<Object>),
    Lambda(Rc<Lambda>),
    Native(Rc<NativeFn>),
    Partial(Rc<Partial>),
    Regex(Rc<JRegex>),
}

impl JValue {
    // ---- constructors ----------------------------------------------------

    pub fn string(s: impl Into<Rc<str>>) -> JValue {
        JValue::String(s.into())
    }

    pub fn from_str_value(s: &str) -> JValue {
        JValue::String(Rc::from(s))
    }

    pub fn number(n: f64) -> JValue {
        JValue::Number(n)
    }

    pub fn array(items: Vec<JValue>, flags: ArrayFlags) -> JValue {
        JValue::Array(Rc::new(items), flags)
    }

    pub fn object(o: Object) -> JValue {
        JValue::Object(Rc::new(o))
    }

    /// `Utils.createSequence()` — empty sequence.
    pub fn empty_sequence() -> JValue {
        JValue::Array(Rc::new(Vec::new()), ArrayFlags::sequence())
    }

    pub fn singleton_sequence(el: JValue) -> JValue {
        JValue::Array(Rc::new(vec![el]), ArrayFlags::sequence())
    }

    // ---- type predicates -------------------------------------------------

    pub fn is_undefined(&self) -> bool {
        matches!(self, JValue::Undefined)
    }

    pub fn is_null(&self) -> bool {
        matches!(self, JValue::Null)
    }

    pub fn is_array(&self) -> bool {
        matches!(self, JValue::Array(..))
    }

    pub fn is_object(&self) -> bool {
        matches!(self, JValue::Object(_))
    }

    pub fn is_function(&self) -> bool {
        matches!(
            self,
            JValue::Lambda(_) | JValue::Native(_) | JValue::Partial(_)
        )
    }

    pub fn is_string(&self) -> bool {
        matches!(self, JValue::String(_))
    }

    pub fn is_bool(&self) -> bool {
        matches!(self, JValue::Bool(_))
    }

    pub fn is_number(&self) -> bool {
        matches!(self, JValue::Number(_))
    }

    /// `Utils.isNumeric` — true for a finite number; throws D1001 on infinity.
    pub fn is_numeric(&self) -> JResult<bool> {
        match self {
            JValue::Number(n) => {
                if n.is_nan() {
                    return Ok(false);
                }
                if !n.is_finite() {
                    return Err(JError::with_current("D1001", 0, self.clone()));
                }
                Ok(true)
            }
            _ => Ok(false),
        }
    }

    pub fn is_sequence(&self) -> bool {
        matches!(self, JValue::Array(_, f) if f.sequence)
    }

    // ---- accessors -------------------------------------------------------

    pub fn as_bool(&self) -> Option<bool> {
        match self {
            JValue::Bool(b) => Some(*b),
            _ => None,
        }
    }

    pub fn as_f64(&self) -> Option<f64> {
        match self {
            JValue::Number(n) => Some(*n),
            _ => None,
        }
    }

    pub fn as_str(&self) -> Option<&str> {
        match self {
            JValue::String(s) => Some(s),
            _ => None,
        }
    }

    pub fn as_array(&self) -> Option<&Rc<Vec<JValue>>> {
        match self {
            JValue::Array(a, _) => Some(a),
            _ => None,
        }
    }

    pub fn as_object(&self) -> Option<&Rc<Object>> {
        match self {
            JValue::Object(o) => Some(o),
            _ => None,
        }
    }

    /// Clone the inner object map (owned `Object`), if this is an object.
    pub fn object_clone(&self) -> Option<Object> {
        match self {
            JValue::Object(o) => Some((**o).clone()),
            _ => None,
        }
    }

    /// Clone the inner Vec (owned), if this is an array.
    pub fn array_clone(&self) -> Option<Vec<JValue>> {
        match self {
            JValue::Array(a, _) => Some((**a).clone()),
            _ => None,
        }
    }

    pub fn flags(&self) -> ArrayFlags {
        match self {
            JValue::Array(_, f) => *f,
            _ => ArrayFlags::default(),
        }
    }

    /// Return a copy of this array value with the given flags.
    pub fn with_flags(&self, flags: ArrayFlags) -> JValue {
        match self {
            JValue::Array(a, _) => JValue::Array(a.clone(), flags),
            other => other.clone(),
        }
    }

    /// Mutable access to the inner Vec of an array, cloning if shared.
    pub fn array_make_mut(&mut self) -> Option<&mut Vec<JValue>> {
        match self {
            JValue::Array(a, _) => Some(Rc::make_mut(a)),
            _ => None,
        }
    }

    /// Mutable access to the inner object, cloning if shared.
    pub fn object_make_mut(&mut self) -> Option<&mut Object> {
        match self {
            JValue::Object(o) => Some(Rc::make_mut(o)),
            _ => None,
        }
    }

    // ---- number conversion ----------------------------------------------

    /// `Utils.convertNumber` — collapse whole numbers to integers for
    /// serialization purposes. Since we store `f64`, this returns the value
    /// unchanged but is kept for API symmetry where the Java code calls it.
    pub fn convert_number(n: f64) -> Option<JValue> {
        if n.is_nan() || !n.is_finite() {
            return None;
        }
        Some(JValue::Number(n))
    }

    /// Whether this number serializes as an integer, replicating Java's
    /// `n.longValue() == n.doubleValue()` test.
    pub fn number_is_integral(n: f64) -> bool {
        if !n.is_finite() {
            return false;
        }
        // Java (long) cast saturates; emulate by clamping.
        let l = if n >= 9_223_372_036_854_775_807.0 {
            i64::MAX
        } else if n <= -9_223_372_036_854_775_808.0 {
            i64::MIN
        } else {
            n as i64
        };
        (l as f64) == n
    }

    // ---- string rendering for error messages ----------------------------

    /// Approximates Java `String.valueOf(obj)` used in error message inserts.
    pub fn error_arg_string(&self) -> String {
        match self {
            JValue::Undefined => "null".to_string(),
            JValue::Null => "null".to_string(),
            JValue::Bool(b) => b.to_string(),
            JValue::Number(n) => crate::functions::number_to_java_string(*n),
            JValue::String(s) => s.to_string(),
            JValue::Array(a, _) => {
                let parts: Vec<String> = a.iter().map(|v| v.error_arg_string()).collect();
                format!("[{}]", parts.join(", "))
            }
            JValue::Object(o) => {
                let parts: Vec<String> = o
                    .iter()
                    .map(|(k, v)| format!("{}={}", k, v.error_arg_string()))
                    .collect();
                format!("{{{}}}", parts.join(", "))
            }
            JValue::Lambda(_) | JValue::Native(_) | JValue::Partial(_) => "".to_string(),
            JValue::Regex(r) => r.pattern.clone(),
        }
    }
}

impl std::fmt::Debug for JValue {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            JValue::Undefined => write!(f, "Undefined"),
            JValue::Null => write!(f, "Null"),
            JValue::Bool(b) => write!(f, "Bool({})", b),
            JValue::Number(n) => write!(f, "Number({})", n),
            JValue::String(s) => write!(f, "String({:?})", s),
            JValue::Array(a, fl) => write!(f, "Array({:?}, {:?})", a, fl),
            JValue::Object(o) => write!(f, "Object({:?})", o),
            JValue::Lambda(_) => write!(f, "Lambda"),
            JValue::Native(n) => write!(f, "Native({})", n.name),
            JValue::Partial(_) => write!(f, "Partial"),
            JValue::Regex(r) => write!(f, "Regex(/{}/)", r.pattern),
        }
    }
}

/// Compare two strings by UTF-16 code units, matching Java `String.compareTo`
/// (and JavaScript's `<`/`>` operators). Differs from Rust's `&str` ordering
/// (Unicode scalar values) only when astral-plane characters meet BMP
/// characters above U+D800: `'\u{ffff}' < '😀'` is false in Java/JS.
pub fn java_string_cmp(a: &str, b: &str) -> std::cmp::Ordering {
    a.encode_utf16().cmp(b.encode_utf16())
}

/// Equality matching Java `Object.equals` for the JSON value subset:
///   * numbers compared as `f64`
///   * arrays compared element-wise, ignoring [`ArrayFlags`]
///   * objects compared order-independently (IndexMap PartialEq)
///   * functions compare by reference identity (Java falls back to
///     `Object.equals` on the same `JFunction`/lambda instance, so
///     `$string = $string` is true); see COMPAT.md — jsonata-js agrees.
impl PartialEq for JValue {
    fn eq(&self, other: &JValue) -> bool {
        use JValue::*;
        match (self, other) {
            (Undefined, Undefined) => true,
            (Null, Null) => true,
            (Bool(a), Bool(b)) => a == b,
            (Number(a), Number(b)) => a == b,
            (String(a), String(b)) => a == b,
            (Array(a, _), Array(b, _)) => a == b,
            (Object(a), Object(b)) => a == b,
            (Lambda(a), Lambda(b)) => Rc::ptr_eq(a, b),
            (Native(a), Native(b)) => Rc::ptr_eq(a, b),
            (Partial(a), Partial(b)) => Rc::ptr_eq(a, b),
            (Regex(a), Regex(b)) => Rc::ptr_eq(a, b),
            _ => false,
        }
    }
}

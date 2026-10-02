//! Port of `Jsonata.Frame` — a lexical environment with a parent chain.

use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;

use crate::value::JValue;

pub type FrameRef = Rc<RefCell<Frame>>;

/// Runtime bounds set by `Frame.setRuntimeBounds` (drives `Timebox`).
#[derive(Clone, Copy, Debug)]
pub struct RuntimeBounds {
    pub timeout_ms: i64,
    pub max_depth: i32,
}

#[derive(Default)]
pub struct Frame {
    pub bindings: HashMap<String, JValue>,
    pub parent: Option<FrameRef>,
    pub is_parallel_call: bool,
    /// Runtime bounds, propagated to the evaluator (Timebox).
    pub bounds: Option<RuntimeBounds>,
}

impl Frame {
    pub fn new(parent: Option<FrameRef>) -> FrameRef {
        Rc::new(RefCell::new(Frame {
            bindings: HashMap::new(),
            parent,
            is_parallel_call: false,
            bounds: None,
        }))
    }

    pub fn bind(&mut self, name: &str, val: JValue) {
        self.bindings.insert(name.to_string(), val);
    }

    /// Lookup a name through the parent chain. Returns `Undefined` if absent.
    pub fn lookup(frame: &FrameRef, name: &str) -> JValue {
        let f = frame.borrow();
        if let Some(v) = f.bindings.get(name) {
            return v.clone();
        }
        match &f.parent {
            Some(p) => Frame::lookup(p, name),
            None => JValue::Undefined,
        }
    }

    pub fn set_runtime_bounds(&mut self, timeout_ms: i64, max_depth: i32) {
        self.bounds = Some(RuntimeBounds {
            timeout_ms,
            max_depth,
        });
    }
}

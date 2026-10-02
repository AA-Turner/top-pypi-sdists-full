//! Port of `com.dashjoin.jsonata.Jsonata` — the tree-walking evaluator.

use std::rc::Rc;
use std::sync::{Arc, OnceLock};

use crate::ast::{NodeRef, NodeValue};
use crate::error::{JError, JResult};
use crate::frame::{Frame, FrameRef, RuntimeBounds};
use crate::functions;
use crate::parser::Parser;
use crate::signature::Signature;
use crate::value::{ArrayFlags, JValue, Lambda, NativeFn, NativeImpl, Object, Partial};

/// Sentinel "no value supplied" for `evaluateFunction(applytoContext)`.
/// We represent `Utils.NONE` as a distinct enum.
#[derive(Clone)]
enum ApplyContext {
    None,
    Value(JValue),
}

/// A compiled JSONata expression.
pub struct Jsonata {
    pub ast: NodeRef,
    pub environment: FrameRef,
    pub validate_input: bool,
    pub output_convert_nulls: bool,
    pub parse_errors: Vec<JError>,
}

/// Per-evaluation mutable state + all evaluation methods. Public so the
/// built-in functions (HOFs) can call back via [`Evaluator::apply`].
pub struct Evaluator {
    pub input: JValue,
    pub environment: FrameRef,
    pub timestamp: i64,
    pub depth: i32,
    pub bounds: Option<RuntimeBounds>,
    pub start_ms: i64,
    /// Entry counter; the wall-clock timeout is only sampled periodically to
    /// avoid a syscall on every node.
    pub ticks: u64,
}

/// Registry of built-in functions: (jsonata name, signature string).
pub const BUILTINS: &[(&str, &str)] = &[
    ("sum", "<a<n>:n>"),
    ("count", "<a:n>"),
    ("max", "<a<n>:n>"),
    ("min", "<a<n>:n>"),
    ("average", "<a<n>:n>"),
    ("string", "<x-b?:s>"),
    ("substring", "<s-nn?:s>"),
    ("substringBefore", "<s-s:s>"),
    ("substringAfter", "<s-s:s>"),
    ("lowercase", "<s-:s>"),
    ("uppercase", "<s-:s>"),
    ("length", "<s-:n>"),
    ("trim", "<s-:s>"),
    ("pad", "<s-ns?:s>"),
    ("match", "<s-f<s:o>n?:a<o>>"),
    ("contains", "<s-(sf):b>"),
    ("replace", "<s-(sf)(sf)n?:s>"),
    ("split", "<s-(sf)n?:a<s>>"),
    ("join", "<a<s>s?:s>"),
    ("formatNumber", "<n-so?:s>"),
    ("formatBase", "<n-n?:s>"),
    ("formatInteger", "<n-s:s>"),
    ("parseInteger", "<s-s:n>"),
    ("number", "<(nsb)-:n>"),
    ("floor", "<n-:n>"),
    ("ceil", "<n-:n>"),
    ("round", "<n-n?:n>"),
    ("abs", "<n-:n>"),
    ("sqrt", "<n-:n>"),
    ("power", "<n-n:n>"),
    ("random", "<:n>"),
    ("boolean", "<x-:b>"),
    ("not", "<x-:b>"),
    ("map", "<af>"),
    ("zip", "<a+>"),
    ("filter", "<af>"),
    ("single", "<af?>"),
    ("reduce", "<afj?:j>"),
    ("sift", "<o-f?:o>"),
    ("keys", "<x-:a<s>>"),
    ("lookup", "<x-s:x>"),
    ("append", "<xx:a>"),
    ("exists", "<x:b>"),
    ("spread", "<x-:a<o>>"),
    ("merge", "<a<o>:o>"),
    ("reverse", "<a:a>"),
    ("each", "<o-f:a>"),
    ("error", "<s?:x>"),
    ("assert", "<bs?:x>"),
    ("type", "<x:s>"),
    ("sort", "<af?:a>"),
    ("shuffle", "<a:a>"),
    ("distinct", "<x:x>"),
    ("base64encode", "<s-:s>"),
    ("base64decode", "<s-:s>"),
    ("encodeUrlComponent", "<s-:s>"),
    ("encodeUrl", "<s-:s>"),
    ("decodeUrlComponent", "<s-:s>"),
    ("decodeUrl", "<s-:s>"),
    ("eval", "<sx?:x>"),
    ("toMillis", "<s-s?:n>"),
    ("fromMillis", "<n-s?s?:s>"),
    ("clone", "<(oa)-:o>"),
    ("now", "<s?s?:s>"),
    ("millis", "<:n>"),
];

/// The parsed builtin signatures, compiled **once per process** and shared
/// across every thread via `Arc`.
///
/// Parsing a signature compiles a `regex::Regex`, and that is by far the most
/// expensive part of standing up the builtin environment (see the perf notes in
/// `CLAUDE.md`). `Signature` carries no `JValue`, so it is `Send + Sync` and can
/// live in this global — unlike the frame that wraps these signatures, which is
/// `Rc`-based (`!Send`) and must stay thread-local. A freshly-spawned thread
/// therefore never re-compiles these regexes; it only clones the `Arc` handles.
fn builtin_signatures() -> &'static [(&'static str, Arc<Signature>)] {
    static SIGS: OnceLock<Vec<(&'static str, Arc<Signature>)>> = OnceLock::new();
    SIGS.get_or_init(|| {
        BUILTINS
            .iter()
            .map(|(name, sig)| (*name, Arc::new(Signature::new(sig, name))))
            .collect()
    })
}

// Build the static frame holding all built-in functions.
thread_local! {
    /// The builtin environment is identical for every expression and immutable
    /// after construction (it is only ever a read-only *parent* of a fresh
    /// per-`Jsonata` child frame — see [`Jsonata::new`] / [`Jsonata::evaluate`]).
    ///
    /// The heavy work — parsing the signature DSL for all ~60 builtins — is
    /// hoisted to the process-global [`builtin_signatures`]. This per-thread
    /// copy only assembles the cheap `Rc`-based `NativeFn` wrappers + frame,
    /// which are `!Send`/`!Sync` and so cannot be global. A thread that reuses
    /// itself amortizes even this assembly; a freshly-spawned thread pays only
    /// ~60 `Arc` bumps + map inserts, never regex compilation.
    static STATIC_FRAME: FrameRef = make_static_frame();
}

/// Returns the shared, build-once builtin frame for the current thread.
pub fn build_static_frame() -> FrameRef {
    STATIC_FRAME.with(|f| f.clone())
}

fn make_static_frame() -> FrameRef {
    let frame = Frame::new(None);
    {
        let mut f = frame.borrow_mut();
        for (name, signature) in builtin_signatures() {
            let native = NativeFn {
                name: name.to_string(),
                signature: Some(signature.clone()),
                implementation: NativeImpl::Builtin,
            };
            f.bind(name, JValue::Native(Rc::new(native)));
        }
    }
    frame
}

fn now_ms() -> i64 {
    use std::time::{SystemTime, UNIX_EPOCH};
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_millis() as i64)
        .unwrap_or(0)
}

impl Jsonata {
    pub fn new(expr: &str) -> JResult<Jsonata> {
        let mut parser = Parser::new();
        let ast = parser.parse(expr)?;
        let static_frame = build_static_frame();
        let environment = Frame::new(Some(static_frame));
        Ok(Jsonata {
            ast,
            environment,
            validate_input: true,
            output_convert_nulls: true,
            parse_errors: parser.errors,
        })
    }

    pub fn set_output_convert_nulls(&mut self, v: bool) {
        self.output_convert_nulls = v;
    }
    pub fn set_validate_input(&mut self, v: bool) {
        self.validate_input = v;
    }

    /// Bind a value into the root environment (`assign`).
    pub fn assign(&mut self, name: &str, value: JValue) {
        self.environment.borrow_mut().bind(name, value);
    }

    /// Create a frame whose parent is this expression's environment
    /// (`Jsonata.createFrame`). Used to pass bindings / runtime bounds.
    pub fn create_frame(&self) -> FrameRef {
        Frame::new(Some(self.environment.clone()))
    }

    /// Register a custom native function.
    pub fn register_function(
        &mut self,
        name: &str,
        signature: Option<&str>,
        f: Rc<dyn Fn(&[JValue]) -> JResult<JValue>>,
    ) {
        let native = NativeFn {
            name: name.to_string(),
            signature: signature.map(|s| Arc::new(Signature::new(s, name))),
            implementation: NativeImpl::Closure(f),
        };
        self.environment
            .borrow_mut()
            .bind(name, JValue::Native(Rc::new(native)));
    }

    /// Evaluate against input data with optional extra bindings frame.
    pub fn evaluate(&self, input: JValue, bindings: Option<FrameRef>) -> JResult<JValue> {
        // Build the execution environment.
        let exec_env = if let Some(b) = &bindings {
            let env = Frame::new(Some(self.environment.clone()));
            {
                let bsrc = b.borrow();
                let mut e = env.borrow_mut();
                for (k, v) in &bsrc.bindings {
                    e.bind(k, v.clone());
                }
            }
            env
        } else {
            self.environment.clone()
        };

        // Bind the input as the root object.
        exec_env.borrow_mut().bind("$", input.clone());

        // pick up runtime bounds from the bindings frame (Timebox)
        let bounds = bindings.as_ref().and_then(|b| b.borrow().bounds);

        // If the input is a JSON array, wrap it in a singleton sequence.
        let input = if input.is_array() && !input.is_sequence() {
            let mut flags = ArrayFlags::sequence();
            flags.outer_wrapper = true;
            JValue::array(vec![input], flags)
        } else {
            input
        };

        if self.validate_input {
            functions::validate_input(&input)?;
        }

        let mut ev = Evaluator {
            input: input.clone(),
            environment: exec_env.clone(),
            timestamp: now_ms(),
            depth: 0,
            bounds,
            start_ms: now_ms(),
            ticks: 0,
        };

        let mut it = ev.evaluate(&self.ast, input, &exec_env)?;
        if self.output_convert_nulls {
            it = functions::convert_nulls(it);
        }
        Ok(it)
    }
}

/// Runtime-guard error with a stable code for telemetry bucketing; the varying
/// depth numbers go into the message detail, not the code (Java's Timebox puts
/// the whole message, numbers included, into the code slot).
fn stack_overflow_error(depth: i32, max: i32) -> JError {
    JError::with_current(
        "STACK_OVERFLOW",
        -1,
        JValue::string(format!("depth={depth}, max={max}")),
    )
}

/// Hard, always-on cap on nested `evaluate()` calls, applied even when no
/// runtime bounds are configured. Deep non-tail recursion would otherwise
/// overflow the Rust stack — an uncatchable process abort, fatal for embedders
/// such as the Python bindings (Java instead throws a catchable
/// `StackOverflowError`). 3500 nested evaluations (~600 levels of JSONata
/// function recursion) fits comfortably in a default 8 MB main-thread stack —
/// the cap does NOT protect small worker-thread stacks (e.g. musl's default);
/// embedders running on such threads should set a tighter limit via
/// `Frame::set_runtime_bounds`. Tail calls are trampolined and unaffected.
/// Debug builds use a much lower cap: their unoptimized frames cost ~10 KB of
/// stack per depth unit (measured), so an 8 MB stack overflows near depth 800.
#[cfg(not(debug_assertions))]
const MAX_EVAL_DEPTH: i32 = 3500;
#[cfg(debug_assertions)]
const MAX_EVAL_DEPTH: i32 = 400;

impl Evaluator {
    // ---- Timebox ---------------------------------------------------------

    fn timebox_entry(&mut self, env: &FrameRef) -> JResult<()> {
        if let Some(b) = self.bounds {
            if env.borrow().is_parallel_call {
                return Ok(());
            }
            self.depth += 1;
            self.check_runaway(b)?;
        } else {
            self.depth += 1;
            if self.depth > MAX_EVAL_DEPTH {
                return Err(stack_overflow_error(self.depth, MAX_EVAL_DEPTH));
            }
        }
        Ok(())
    }
    fn timebox_exit(&mut self, env: &FrameRef) {
        if self.bounds.is_some() {
            if !env.borrow().is_parallel_call {
                self.depth -= 1;
            }
        } else {
            self.depth -= 1;
        }
    }
    fn check_runaway(&mut self, b: RuntimeBounds) -> JResult<()> {
        if self.depth > b.max_depth {
            return Err(stack_overflow_error(self.depth, b.max_depth));
        }
        // Sample the wall clock only every 4096 entries to avoid a syscall per
        // node (the depth check above is what catches deep recursion).
        self.ticks = self.ticks.wrapping_add(1);
        if self.ticks % 4096 == 0 && now_ms() - self.start_ms > b.timeout_ms {
            return Err(JError::new("TIMEOUT"));
        }
        Ok(())
    }

    // ---- dispatch --------------------------------------------------------

    pub fn evaluate(&mut self, expr: &NodeRef, input: JValue, env: &FrameRef) -> JResult<JValue> {
        let _input = self.input.clone();
        let _env = self.environment.clone();
        let r = self.evaluate_inner(expr, input, env);
        self.input = _input;
        self.environment = _env;
        r
    }

    fn evaluate_inner(&mut self, expr: &NodeRef, input: JValue, env: &FrameRef) -> JResult<JValue> {
        self.input = input.clone();
        self.environment = env.clone();

        self.timebox_entry(env)?;

        let ntype = expr.borrow().node_type.clone().unwrap_or_default();
        let mut result = match ntype.as_str() {
            "path" => self.evaluate_path(expr, input.clone(), env)?,
            "binary" => self.evaluate_binary(expr, input.clone(), env)?,
            "unary" => self.evaluate_unary(expr, input.clone(), env)?,
            "name" => {
                let key = expr.borrow().value.to_string_val();
                functions::lookup(&input, &key)
            }
            "string" | "number" | "value" => self.evaluate_literal(expr),
            "wildcard" => self.evaluate_wildcard(expr, input.clone()),
            "descendant" => self.evaluate_descendants(expr, input.clone()),
            "parent" => {
                let label = expr
                    .borrow()
                    .slot
                    .as_ref()
                    .map(|s| s.borrow().label.clone())
                    .unwrap_or_default();
                Frame::lookup(env, &label)
            }
            "condition" => self.evaluate_condition(expr, input.clone(), env)?,
            "block" => self.evaluate_block(expr, input.clone(), env)?,
            "bind" => self.evaluate_bind(expr, input.clone(), env)?,
            "regex" => self.evaluate_literal(expr),
            "function" => self.evaluate_function(expr, input.clone(), env, ApplyContext::None)?,
            "variable" => self.evaluate_variable(expr, input.clone(), env),
            "lambda" => self.evaluate_lambda(expr, input.clone(), env),
            "partial" => self.evaluate_partial_application(expr, input.clone(), env)?,
            "apply" => self.evaluate_apply(expr, input.clone(), env)?,
            "transform" => self.evaluate_transform(expr, env),
            _ => JValue::Undefined,
        };

        // predicates
        let predicates = expr.borrow().predicate.clone();
        if let Some(preds) = predicates {
            for p in preds {
                let pexpr = p.borrow().expr.clone().unwrap();
                result = self.evaluate_filter(&pexpr, result, env)?;
            }
        }

        // group (when not a path)
        let group = expr.borrow().group.clone();
        if !expr.borrow().type_is("path") {
            if let Some(g) = group {
                result = self.evaluate_group(&g, result, env)?;
            }
        }

        // mangle: sequence of 1 -> element, empty -> undefined
        if result.is_sequence() {
            let is_tuple = matches!(&result, JValue::Array(_, f) if f.tuple_stream);
            if !is_tuple {
                let keep_array = expr.borrow().keep_array;
                let mut flags = result.flags();
                if keep_array {
                    flags.keep_singleton = true;
                }
                let arr = result.as_array().unwrap().clone();
                if arr.is_empty() {
                    result = JValue::Undefined;
                } else if arr.len() == 1 {
                    result = if flags.keep_singleton {
                        JValue::Array(arr, flags)
                    } else {
                        arr[0].clone()
                    };
                } else {
                    result = JValue::Array(arr, flags);
                }
            }
        }

        self.timebox_exit(env);
        Ok(result)
    }

    fn evaluate_literal(&self, expr: &NodeRef) -> JValue {
        let e = expr.borrow();
        match &e.value {
            NodeValue::None => JValue::Null, // expr.value==null -> NULL_VALUE
            _ => e.literal_value(),
        }
    }

    // ---- path ------------------------------------------------------------

    fn evaluate_path(&mut self, expr: &NodeRef, input: JValue, env: &FrameRef) -> JResult<JValue> {
        let steps = expr.borrow().steps.clone().unwrap_or_default();
        // absolute path if first step is a variable
        let first_is_var = steps
            .first()
            .map(|s| s.borrow().type_is("variable"))
            .unwrap_or(false);
        let mut input_sequence: JValue = if input.is_array() && !first_is_var {
            input.clone()
        } else {
            JValue::singleton_sequence(input.clone())
        };

        let mut result_sequence = JValue::Undefined;
        let mut is_tuple_stream = false;
        // None = not yet initialized (Java `null`); Some(empty) = filtered to
        // nothing. The distinction matters: an empty tuple stream must stay
        // empty, whereas the first tuple step seeds bindings from the input.
        let mut tuple_bindings: Option<Vec<JValue>> = None;

        for (ii, step) in steps.iter().enumerate() {
            let step_tuple = step.borrow().tuple;
            if step_tuple {
                is_tuple_stream = true;
            }

            let consarray = step.borrow().consarray;
            if ii == 0 && consarray {
                result_sequence = self.evaluate(step, input_sequence.clone(), env)?;
            } else if is_tuple_stream {
                tuple_bindings = Some(self.evaluate_tuple_step(
                    step,
                    &input_sequence,
                    tuple_bindings.as_deref(),
                    env,
                )?);
            } else {
                result_sequence =
                    self.evaluate_step(step, &input_sequence, env, ii == steps.len() - 1)?;
            }

            if !is_tuple_stream {
                let empty = match &result_sequence {
                    JValue::Undefined => true,
                    JValue::Array(a, _) => a.is_empty(),
                    _ => false,
                };
                if empty {
                    break;
                }
            }

            if step.borrow().focus.is_none() {
                input_sequence = result_sequence.clone();
            }
        }

        let tuple_bindings_vec = tuple_bindings.unwrap_or_default();
        if is_tuple_stream {
            if expr.borrow().tuple {
                result_sequence = JValue::array(tuple_bindings_vec.clone(), {
                    let mut f = ArrayFlags::sequence();
                    f.tuple_stream = true;
                    f
                });
            } else {
                let mut seq = Vec::new();
                for t in &tuple_bindings_vec {
                    if let Some(o) = t.as_object() {
                        seq.push(o.get("@").cloned().unwrap_or(JValue::Undefined));
                    }
                }
                result_sequence = JValue::array(seq, ArrayFlags::sequence());
            }
        }

        if expr.borrow().keep_singleton_array {
            let mut flags = result_sequence.flags();
            // if explicitly constructed array (cons) and not yet a sequence, wrap
            if flags.cons && !flags.sequence {
                result_sequence = JValue::singleton_sequence(result_sequence);
                flags = result_sequence.flags();
            }
            flags.sequence = true;
            flags.keep_singleton = true;
            result_sequence = match result_sequence {
                JValue::Array(a, _) => JValue::Array(a, flags),
                other => {
                    // ensure it's a JList
                    JValue::Array(Rc::new(vec![other]), flags)
                }
            };
        }

        let group = expr.borrow().group.clone();
        if let Some(g) = group {
            let to_group = if is_tuple_stream {
                JValue::array(tuple_bindings_vec, {
                    let mut f = ArrayFlags::sequence();
                    f.tuple_stream = true;
                    f
                })
            } else {
                result_sequence.clone()
            };
            result_sequence = self.evaluate_group(&g, to_group, env)?;
        }

        Ok(result_sequence)
    }

    fn create_frame_from_tuple(&self, env: &FrameRef, tuple: &Object) -> FrameRef {
        let frame = Frame::new(Some(env.clone()));
        {
            let mut f = frame.borrow_mut();
            for (k, v) in tuple {
                f.bind(k, v.clone());
            }
        }
        frame
    }

    fn evaluate_step(
        &mut self,
        expr: &NodeRef,
        input: &JValue,
        env: &FrameRef,
        last_step: bool,
    ) -> JResult<JValue> {
        if expr.borrow().type_is("sort") {
            let mut result = self.evaluate_sort_expression(expr, input, env)?;
            let stages = expr.borrow().stages.clone();
            if let Some(stages) = stages {
                result = self.evaluate_stages(&stages, result, env)?;
            }
            return Ok(result);
        }

        let input_arr = input.as_array().cloned().unwrap_or_else(|| Rc::new(vec![]));
        let mut result: Vec<JValue> = Vec::new();
        let stages = expr.borrow().stages.clone();
        for item in input_arr.iter() {
            let mut res = self.evaluate(expr, item.clone(), env)?;
            if let Some(ref stages) = stages {
                for st in stages {
                    let sexpr = st.borrow().expr.clone().unwrap();
                    res = self.evaluate_filter(&sexpr, res, env)?;
                }
            }
            if !res.is_undefined() {
                result.push(res);
            }
        }

        let mut result_sequence = Vec::new();
        if last_step && result.len() == 1 && result[0].is_array() && !result[0].is_sequence() {
            return Ok(result.into_iter().next().unwrap());
        } else {
            for res in result {
                let is_cons = matches!(&res, JValue::Array(_, f) if f.cons);
                if !res.is_array() || is_cons {
                    result_sequence.push(res);
                } else {
                    let arr = res.as_array().unwrap().clone();
                    result_sequence.extend(arr.iter().cloned());
                }
            }
        }
        Ok(JValue::array(result_sequence, ArrayFlags::sequence()))
    }

    fn evaluate_stages(
        &mut self,
        stages: &[NodeRef],
        input: JValue,
        env: &FrameRef,
    ) -> JResult<JValue> {
        let mut result = input;
        for stage in stages {
            let stype = stage.borrow().node_type.clone().unwrap_or_default();
            match stype.as_str() {
                "filter" => {
                    let sexpr = stage.borrow().expr.clone().unwrap();
                    result = self.evaluate_filter(&sexpr, result, env)?;
                }
                "index" => {
                    let var = stage.borrow().value.to_string_val();
                    if let JValue::Array(arr, flags) = &result {
                        let mut new = (**arr).clone();
                        for (ee, tuple) in new.iter_mut().enumerate() {
                            if let Some(o) = tuple.object_make_mut() {
                                o.insert(var.clone(), JValue::Number(ee as f64));
                            }
                        }
                        result = JValue::Array(Rc::new(new), *flags);
                    }
                }
                _ => {}
            }
        }
        Ok(result)
    }

    fn evaluate_tuple_step(
        &mut self,
        expr: &NodeRef,
        input: &JValue,
        tuple_bindings: Option<&[JValue]>,
        env: &FrameRef,
    ) -> JResult<Vec<JValue>> {
        if expr.borrow().type_is("sort") {
            let mut result: Vec<JValue>;
            if let Some(tb) = tuple_bindings {
                let sorted = self.evaluate_sort_expression(
                    expr,
                    &JValue::array(tb.to_vec(), {
                        let mut f = ArrayFlags::sequence();
                        f.tuple_stream = true;
                        f
                    }),
                    env,
                )?;
                result = sorted.as_array().map(|a| (**a).clone()).unwrap_or_default();
            } else {
                let sorted = self.evaluate_sort_expression(expr, input, env)?;
                let sorted_arr = sorted.as_array().map(|a| (**a).clone()).unwrap_or_default();
                result = Vec::new();
                let idx_name = expr.borrow().index.clone();
                for (ss, item) in sorted_arr.into_iter().enumerate() {
                    let mut o = Object::new();
                    o.insert("@".to_string(), item);
                    if let Some(ref idx) = idx_name {
                        o.insert(idx.clone(), JValue::Number(ss as f64));
                    }
                    result.push(JValue::object(o));
                }
            }
            let stages = expr.borrow().stages.clone();
            if let Some(stages) = stages {
                let r = self.evaluate_stages(
                    &stages,
                    JValue::array(result, {
                        let mut f = ArrayFlags::sequence();
                        f.tuple_stream = true;
                        f
                    }),
                    env,
                )?;
                return Ok(r.as_array().map(|a| (**a).clone()).unwrap_or_default());
            }
            return Ok(result);
        }

        let mut result: Vec<JValue> = Vec::new();
        // Java: `if (tupleBindings == null) tupleBindings = input.map(@)`.
        // Only seed from the input when uninitialized (None) — an empty stream
        // (Some([])) must stay empty.
        let local_bindings: Vec<JValue> = match tuple_bindings {
            Some(tb) => tb.to_vec(),
            None => {
                let input_arr = input.as_array().cloned().unwrap_or_else(|| Rc::new(vec![]));
                input_arr
                    .iter()
                    .map(|item| {
                        let mut o = Object::new();
                        o.insert("@".to_string(), item.clone());
                        JValue::object(o)
                    })
                    .collect()
            }
        };

        let focus = expr.borrow().focus.clone();
        let idx_name = expr.borrow().index.clone();
        let ancestor_label = expr
            .borrow()
            .ancestor
            .as_ref()
            .map(|s| s.borrow().label.clone());

        for binding in &local_bindings {
            let binding_obj = binding.object_clone().unwrap_or_default();
            let step_env = self.create_frame_from_tuple(env, &binding_obj);
            let at = binding_obj.get("@").cloned().unwrap_or(JValue::Undefined);
            let res = self.evaluate(expr, at.clone(), &step_env)?;
            if !res.is_undefined() {
                let res_vec: Vec<JValue> = if res.is_array() {
                    res.as_array().unwrap().iter().cloned().collect()
                } else {
                    vec![res.clone()]
                };
                let res_is_tuple = matches!(&res, JValue::Array(_, f) if f.tuple_stream);
                for (bb, item) in res_vec.iter().enumerate() {
                    let mut tuple = binding_obj.clone();
                    if res_is_tuple {
                        if let Some(o) = item.as_object() {
                            for (k, v) in o.iter() {
                                tuple.insert(k.clone(), v.clone());
                            }
                        }
                    } else {
                        if let Some(ref focus) = focus {
                            if !focus.is_empty() {
                                tuple.insert(focus.clone(), item.clone());
                                tuple.insert("@".to_string(), at.clone());
                            } else {
                                tuple.insert("@".to_string(), item.clone());
                            }
                        } else {
                            tuple.insert("@".to_string(), item.clone());
                        }
                        if let Some(ref idx) = idx_name {
                            tuple.insert(idx.clone(), JValue::Number(bb as f64));
                        }
                        if let Some(ref anc) = ancestor_label {
                            tuple.insert(anc.clone(), at.clone());
                        }
                    }
                    result.push(JValue::object(tuple));
                }
            }
        }

        let stages = expr.borrow().stages.clone();
        if let Some(stages) = stages {
            let r = self.evaluate_stages(
                &stages,
                JValue::array(result, {
                    let mut f = ArrayFlags::sequence();
                    f.tuple_stream = true;
                    f
                }),
                env,
            )?;
            return Ok(r.as_array().map(|a| (**a).clone()).unwrap_or_default());
        }
        Ok(result)
    }

    fn evaluate_filter(
        &mut self,
        predicate: &NodeRef,
        input: JValue,
        env: &FrameRef,
    ) -> JResult<JValue> {
        let mut results = JValue::empty_sequence();
        let input_is_tuple = matches!(&input, JValue::Array(_, f) if f.tuple_stream);
        if input_is_tuple {
            results = results.with_flags({
                let mut f = ArrayFlags::sequence();
                f.tuple_stream = true;
                f
            });
        }
        let input = if !input.is_array() {
            if input.is_undefined() {
                JValue::empty_sequence()
            } else {
                JValue::singleton_sequence(input)
            }
        } else {
            input
        };
        let input_arr = input.as_array().unwrap().clone();

        let ptype = predicate.borrow().node_type.clone().unwrap_or_default();
        if ptype == "number" {
            let mut index = predicate.borrow().value.clone();
            let idx = match index {
                NodeValue::Number(n) => n as i64,
                _ => 0,
            };
            let _ = &mut index;
            let mut idx = idx;
            if idx < 0 {
                idx += input_arr.len() as i64;
            }
            if idx >= 0 && (idx as usize) < input_arr.len() {
                let item = input_arr[idx as usize].clone();
                if item.is_array() {
                    results = item;
                } else {
                    results.array_make_mut().unwrap().push(item);
                }
            }
        } else {
            let res_flags = results.flags();
            let mut out = match results {
                JValue::Array(a, _) => (*a).clone(),
                _ => vec![],
            };
            for (index, item) in input_arr.iter().enumerate() {
                let mut context = item.clone();
                let mut fenv = env.clone();
                if input_is_tuple {
                    if let Some(o) = item.as_object() {
                        context = o.get("@").cloned().unwrap_or(JValue::Undefined);
                        fenv = self.create_frame_from_tuple(env, o);
                    }
                }
                let mut res = self.evaluate(predicate, context, &fenv)?;
                if res.is_numeric()? {
                    res = JValue::singleton_sequence(res);
                }
                if is_array_of_numbers(&res) {
                    for ires in res.as_array().unwrap().iter() {
                        let mut ii = ires.as_f64().unwrap() as i64;
                        if ii < 0 {
                            ii += input_arr.len() as i64;
                        }
                        if ii == index as i64 {
                            out.push(item.clone());
                        }
                    }
                } else if functions::boolize(&res) {
                    out.push(item.clone());
                }
            }
            results = JValue::Array(Rc::new(out), res_flags);
        }
        Ok(results)
    }

    // ---- binary ----------------------------------------------------------

    fn evaluate_binary(
        &mut self,
        expr: &NodeRef,
        input: JValue,
        env: &FrameRef,
    ) -> JResult<JValue> {
        let op = expr.borrow().value.to_string_val();
        let lhs_node = expr.borrow().lhs.clone().unwrap();

        if op == "and" || op == "or" {
            let lhs = self.evaluate(&lhs_node, input.clone(), env)?;
            let rhs_node = expr.borrow().rhs.clone().unwrap();
            return self.evaluate_boolean(lhs, &rhs_node, input, env, &op);
        }

        let lhs = self.evaluate(&lhs_node, input.clone(), env)?;
        let rhs_node = expr.borrow().rhs.clone().unwrap();
        let rhs = self.evaluate(&rhs_node, input.clone(), env)?;
        let pos = expr.borrow().position as i32;
        match op.as_str() {
            "+" | "-" | "*" | "/" | "%" => self.evaluate_numeric(lhs, rhs, &op),
            "=" | "!=" => Ok(self.evaluate_equality(lhs, rhs, &op)),
            "<" | "<=" | ">" | ">=" => self.evaluate_comparison(lhs, rhs, &op),
            "&" => self.evaluate_string_concat(lhs, rhs),
            ".." => self.evaluate_range(lhs, rhs),
            "in" => Ok(self.evaluate_includes(lhs, rhs)),
            _ => Err(JError::at("S0201", pos)),
        }
    }

    fn evaluate_numeric(&self, lhs: JValue, rhs: JValue, op: &str) -> JResult<JValue> {
        if !lhs.is_undefined() && !lhs.is_numeric()? {
            return Err(JError::with_current_expected(
                "T2001",
                -1,
                JValue::string(op),
                lhs,
            ));
        }
        if !rhs.is_undefined() && !rhs.is_numeric()? {
            return Err(JError::with_current_expected(
                "T2002",
                -1,
                JValue::string(op),
                rhs,
            ));
        }
        if lhs.is_undefined() || rhs.is_undefined() {
            return Ok(JValue::Undefined);
        }
        let l = lhs.as_f64().unwrap();
        let r = rhs.as_f64().unwrap();
        let result = match op {
            "+" => l + r,
            "-" => l - r,
            "*" => l * r,
            "/" => l / r,
            "%" => l % r,
            _ => 0.0,
        };
        // Java Utils.convertNumber: NaN -> null (undefined result, no error);
        // +/-Infinity -> D1001. jsonata-js instead lets NaN/Infinity flow as
        // values; see COMPAT.md.
        if result.is_nan() {
            return Ok(JValue::Undefined);
        }
        match JValue::convert_number(result) {
            Some(v) => Ok(v),
            None => Err(JError::with_current("D1001", 0, JValue::Number(result))),
        }
    }

    fn evaluate_equality(&self, lhs: JValue, rhs: JValue, op: &str) -> JValue {
        if lhs.is_undefined() || rhs.is_undefined() {
            return JValue::Bool(false);
        }
        let eq = lhs == rhs;
        JValue::Bool(if op == "=" { eq } else { !eq })
    }

    fn evaluate_comparison(&self, lhs: JValue, rhs: JValue, op: &str) -> JResult<JValue> {
        let lcomp = lhs.is_undefined() || lhs.is_string() || lhs.is_number();
        let rcomp = rhs.is_undefined() || rhs.is_string() || rhs.is_number();
        if !lcomp || !rcomp {
            let arg = if !lhs.is_undefined() { lhs } else { rhs };
            return Err(JError::with_current_expected(
                "T2010",
                0,
                JValue::string(op),
                arg,
            ));
        }
        if lhs.is_undefined() || rhs.is_undefined() {
            return Ok(JValue::Undefined);
        }
        // mixed types?
        let same_type =
            (lhs.is_number() && rhs.is_number()) || (lhs.is_string() && rhs.is_string());
        if !same_type {
            return Err(JError::with_current_expected("T2009", 0, lhs, rhs));
        }
        let result = match (&lhs, &rhs) {
            (JValue::Number(a), JValue::Number(b)) => match op {
                "<" => a < b,
                "<=" => a <= b,
                ">" => a > b,
                _ => a >= b,
            },
            (JValue::String(a), JValue::String(b)) => {
                // Java String.compareTo — UTF-16 code-unit order.
                let ord = crate::value::java_string_cmp(a, b);
                match op {
                    "<" => ord.is_lt(),
                    "<=" => ord.is_le(),
                    ">" => ord.is_gt(),
                    _ => ord.is_ge(),
                }
            }
            _ => false,
        };
        Ok(JValue::Bool(result))
    }

    fn evaluate_includes(&self, lhs: JValue, rhs: JValue) -> JValue {
        if lhs.is_undefined() || rhs.is_undefined() {
            return JValue::Bool(false);
        }
        let rhs_arr = if rhs.is_array() {
            rhs.as_array().unwrap().clone()
        } else {
            Rc::new(vec![rhs])
        };
        for item in rhs_arr.iter() {
            if lhs == *item {
                return JValue::Bool(true);
            }
        }
        JValue::Bool(false)
    }

    fn evaluate_boolean(
        &mut self,
        lhs: JValue,
        rhs_node: &NodeRef,
        input: JValue,
        env: &FrameRef,
        op: &str,
    ) -> JResult<JValue> {
        let l_bool = functions::boolize(&lhs);
        let result = match op {
            "and" => l_bool && functions::boolize(&self.evaluate(rhs_node, input, env)?),
            "or" => l_bool || functions::boolize(&self.evaluate(rhs_node, input, env)?),
            _ => false,
        };
        Ok(JValue::Bool(result))
    }

    fn evaluate_string_concat(&self, lhs: JValue, rhs: JValue) -> JResult<JValue> {
        let mut lstr = String::new();
        let mut rstr = String::new();
        if !lhs.is_undefined() {
            lstr = functions::string(&lhs, false)?;
        }
        if !rhs.is_undefined() {
            rstr = functions::string(&rhs, false)?;
        }
        Ok(JValue::string(format!("{}{}", lstr, rstr)))
    }

    fn evaluate_range(&self, lhs: JValue, rhs: JValue) -> JResult<JValue> {
        let l_is_int = matches!(&lhs, JValue::Number(n) if JValue::number_is_integral(*n));
        let r_is_int = matches!(&rhs, JValue::Number(n) if JValue::number_is_integral(*n));
        if !lhs.is_undefined() && !l_is_int {
            return Err(JError::with_current("T2003", -1, lhs));
        }
        if !rhs.is_undefined() && !r_is_int {
            return Err(JError::with_current("T2004", -1, rhs));
        }
        if lhs.is_undefined() || rhs.is_undefined() {
            return Ok(JValue::Undefined);
        }
        let l = lhs.as_f64().unwrap() as i64;
        let r = rhs.as_f64().unwrap() as i64;
        if l > r {
            return Ok(JValue::Undefined);
        }
        let size = r - l + 1;
        if size as f64 > 1e7 {
            return Err(JError::with_current(
                "D2014",
                -1,
                JValue::Number(size as f64),
            ));
        }
        let mut v = Vec::with_capacity(size as usize);
        for i in l..=r {
            v.push(JValue::Number(i as f64));
        }
        Ok(JValue::array(v, ArrayFlags::default()))
    }

    // ---- unary -----------------------------------------------------------

    fn evaluate_unary(&mut self, expr: &NodeRef, input: JValue, env: &FrameRef) -> JResult<JValue> {
        let value = expr.borrow().value.to_string_val();
        match value.as_str() {
            "-" => {
                let inner = expr.borrow().expression.clone().unwrap();
                let result = self.evaluate(&inner, input, env)?;
                if result.is_undefined() {
                    Ok(JValue::Undefined)
                } else if result.is_numeric()? {
                    Ok(JValue::Number(-result.as_f64().unwrap()))
                } else {
                    let pos = expr.borrow().position as i32;
                    Err(JError::with_current_expected(
                        "D1002",
                        pos,
                        JValue::string("-"),
                        result,
                    ))
                }
            }
            "[" => {
                let exprs = expr.borrow().expressions.clone().unwrap_or_default();
                let mut result: Vec<JValue> = Vec::new();
                for (idx, item) in exprs.iter().enumerate() {
                    env.borrow_mut().is_parallel_call = idx > 0;
                    let value = self.evaluate(item, input.clone(), env)?;
                    if !value.is_undefined() {
                        let item_is_array_cons = item.borrow().value.eq_str("[");
                        if item_is_array_cons {
                            result.push(value);
                        } else {
                            let appended = functions::append(
                                JValue::array(result, ArrayFlags::default()),
                                value,
                            );
                            result = appended
                                .as_array()
                                .map(|a| (**a).clone())
                                .unwrap_or_default();
                        }
                    }
                }
                // Java: `var result = new JList<>()` — always a JList.
                let mut flags = ArrayFlags::jlist();
                if expr.borrow().consarray {
                    flags.cons = true;
                }
                Ok(JValue::array(result, flags))
            }
            "{" => self.evaluate_group(expr, input, env),
            _ => Ok(JValue::Undefined),
        }
    }

    // ---- wildcard / descendant ------------------------------------------

    fn evaluate_wildcard(&self, _expr: &NodeRef, input: JValue) -> JValue {
        let mut results: Vec<JValue> = Vec::new();
        let input = match &input {
            JValue::Array(a, f) if f.outer_wrapper && !a.is_empty() => a[0].clone(),
            _ => input,
        };
        if let Some(o) = input.as_object() {
            for (_k, value) in o.iter() {
                if value.is_array() {
                    let flat = flatten(value.clone(), None);
                    let appended =
                        functions::append(JValue::array(results, ArrayFlags::sequence()), flat);
                    results = appended
                        .as_array()
                        .map(|a| (**a).clone())
                        .unwrap_or_default();
                } else {
                    results.push(value.clone());
                }
            }
        } else if let Some(a) = input.as_array() {
            for value in a.iter() {
                if value.is_array() {
                    let flat = flatten(value.clone(), None);
                    let appended =
                        functions::append(JValue::array(results, ArrayFlags::sequence()), flat);
                    results = appended
                        .as_array()
                        .map(|a| (**a).clone())
                        .unwrap_or_default();
                } else {
                    results.push(value.clone());
                }
            }
        }
        JValue::array(results, ArrayFlags::sequence())
    }

    fn evaluate_descendants(&self, _expr: &NodeRef, input: JValue) -> JValue {
        if input.is_undefined() {
            return JValue::Undefined;
        }
        let mut result_sequence: Vec<JValue> = Vec::new();
        recurse_descendants(&input, &mut result_sequence);
        if result_sequence.len() == 1 {
            result_sequence.into_iter().next().unwrap()
        } else {
            JValue::array(result_sequence, ArrayFlags::sequence())
        }
    }

    // ---- group -----------------------------------------------------------

    fn evaluate_group(&mut self, expr: &NodeRef, input: JValue, env: &FrameRef) -> JResult<JValue> {
        let reduce = matches!(&input, JValue::Array(_, f) if f.tuple_stream);
        let input = if !input.is_array() {
            JValue::singleton_sequence(input)
        } else {
            input
        };
        let mut input_vec: Vec<JValue> = input.as_array().unwrap().iter().cloned().collect();
        if input_vec.is_empty() {
            input_vec.push(JValue::Undefined);
        }

        // group spec: for unary "{", the pairs are in lhs_object; for path group, also lhs_object.
        let pairs = expr.borrow().lhs_object.clone().unwrap_or_default();

        // groups: key -> (data, exprIndex)
        let mut groups: indexmap::IndexMap<String, (JValue, usize)> = indexmap::IndexMap::new();
        let pos = expr.borrow().position as i32;

        for item in &input_vec {
            let env_for = if reduce {
                self.create_frame_from_tuple(env, &item.object_clone().unwrap_or_default())
            } else {
                env.clone()
            };
            for (pair_index, (key_node, _val)) in pairs.iter().enumerate() {
                let key_ctx = if reduce {
                    item.as_object()
                        .and_then(|o| o.get("@").cloned())
                        .unwrap_or(JValue::Undefined)
                } else {
                    item.clone()
                };
                let key = self.evaluate(key_node, key_ctx, &env_for)?;
                if !key.is_undefined() && !key.is_string() {
                    return Err(JError::with_current("T1003", pos, key));
                }
                if let JValue::String(ks) = &key {
                    let kstr = ks.to_string();
                    if let Some((data, ei)) = groups.get(&kstr).cloned() {
                        if ei != pair_index {
                            return Err(JError::with_current("D1009", pos, key.clone()));
                        }
                        let appended = functions::append(data, item.clone());
                        groups.insert(kstr, (appended, ei));
                    } else {
                        groups.insert(kstr, (item.clone(), pair_index));
                    }
                }
            }
        }

        let mut result = Object::new();
        let mut idx = 0;
        let keys: Vec<String> = groups.keys().cloned().collect();
        for key in keys {
            let (data, expr_index) = groups.get(&key).cloned().unwrap();
            let (context, env_for) = if reduce {
                let tuple = self.reduce_tuple_stream(&data);
                let mut tobj = tuple.object_clone().unwrap_or_default();
                let ctx = tobj.shift_remove("@").unwrap_or(JValue::Undefined);
                let fr = self.create_frame_from_tuple(env, &tobj);
                (ctx, fr)
            } else {
                (data, env.clone())
            };
            env_for.borrow_mut().is_parallel_call = idx > 0;
            let val_node = pairs[expr_index].1.clone();
            let res = self.evaluate(&val_node, context, &env_for)?;
            if !res.is_undefined() {
                result.insert(key, res);
            }
            idx += 1;
        }
        Ok(JValue::object(result))
    }

    fn reduce_tuple_stream(&self, tuple_stream: &JValue) -> JValue {
        if !tuple_stream.is_array() {
            return tuple_stream.clone();
        }
        let arr = tuple_stream.as_array().unwrap();
        if arr.is_empty() {
            return JValue::object(Object::new());
        }
        let mut result = arr[0].object_clone().unwrap_or_default();
        for el in arr.iter().skip(1) {
            if let Some(o) = el.as_object() {
                for (prop, v) in o.iter() {
                    let existing = result.get(prop).cloned().unwrap_or(JValue::Undefined);
                    result.insert(prop.clone(), functions::append(existing, v.clone()));
                }
            }
        }
        JValue::object(result)
    }

    // ---- condition / block / bind / variable ----------------------------

    fn evaluate_condition(
        &mut self,
        expr: &NodeRef,
        input: JValue,
        env: &FrameRef,
    ) -> JResult<JValue> {
        let cond_node = expr.borrow().condition.clone().unwrap();
        let condition = self.evaluate(&cond_node, input.clone(), env)?;
        if functions::boolize(&condition) {
            let then = expr.borrow().then.clone().unwrap();
            self.evaluate(&then, input, env)
        } else {
            let els = expr.borrow().els.clone();
            match els {
                Some(e) => self.evaluate(&e, input, env),
                None => Ok(JValue::Undefined),
            }
        }
    }

    fn evaluate_block(&mut self, expr: &NodeRef, input: JValue, env: &FrameRef) -> JResult<JValue> {
        let frame = Frame::new(Some(env.clone()));
        let mut result = JValue::Undefined;
        let exprs = expr.borrow().expressions.clone().unwrap_or_default();
        for ex in exprs {
            result = self.evaluate(&ex, input.clone(), &frame)?;
        }
        Ok(result)
    }

    fn evaluate_bind(&mut self, expr: &NodeRef, input: JValue, env: &FrameRef) -> JResult<JValue> {
        let rhs = expr.borrow().rhs.clone().unwrap();
        let value = self.evaluate(&rhs, input, env)?;
        let name = expr
            .borrow()
            .lhs
            .as_ref()
            .map(|l| l.borrow().value.to_string_val())
            .unwrap_or_default();
        env.borrow_mut().bind(&name, value.clone());
        Ok(value)
    }

    fn evaluate_variable(&self, expr: &NodeRef, input: JValue, env: &FrameRef) -> JValue {
        let name = expr.borrow().value.to_string_val();
        if name.is_empty() {
            match &input {
                JValue::Array(a, f) if f.outer_wrapper => a[0].clone(),
                _ => input,
            }
        } else {
            Frame::lookup(env, &name)
        }
    }

    // ---- sort ------------------------------------------------------------

    fn evaluate_sort_expression(
        &mut self,
        expr: &NodeRef,
        input: &JValue,
        env: &FrameRef,
    ) -> JResult<JValue> {
        let lhs: Vec<JValue> = input.as_array().map(|a| (**a).clone()).unwrap_or_default();
        let is_tuple_sort = matches!(input, JValue::Array(_, f) if f.tuple_stream);
        let terms = expr.borrow().terms.clone().unwrap_or_default();
        let pos = expr.borrow().position as i32;

        // stable merge sort, matching Functions.sort behavior (swap when comp>0)
        let sorted = self.merge_sort_terms(lhs, &terms, is_tuple_sort, env, pos)?;
        let mut flags = ArrayFlags::sequence();
        if is_tuple_sort {
            flags.tuple_stream = true;
        }
        Ok(JValue::array(sorted, flags))
    }

    fn merge_sort_terms(
        &mut self,
        arr: Vec<JValue>,
        terms: &[NodeRef],
        is_tuple_sort: bool,
        env: &FrameRef,
        pos: i32,
    ) -> JResult<Vec<JValue>> {
        if arr.len() <= 1 {
            return Ok(arr);
        }
        let mid = arr.len() / 2;
        let right_part = arr[mid..].to_vec();
        let left_part = arr[..mid].to_vec();
        let left = self.merge_sort_terms(left_part, terms, is_tuple_sort, env, pos)?;
        let right = self.merge_sort_terms(right_part, terms, is_tuple_sort, env, pos)?;
        let mut result = Vec::with_capacity(left.len() + right.len());
        let (mut i, mut j) = (0, 0);
        while i < left.len() && j < right.len() {
            let comp = self.sort_compare(&left[i], &right[j], terms, is_tuple_sort, env, pos)?;
            if comp <= 0 {
                result.push(left[i].clone());
                i += 1;
            } else {
                result.push(right[j].clone());
                j += 1;
            }
        }
        result.extend_from_slice(&left[i..]);
        result.extend_from_slice(&right[j..]);
        Ok(result)
    }

    fn sort_compare(
        &mut self,
        a: &JValue,
        b: &JValue,
        terms: &[NodeRef],
        is_tuple_sort: bool,
        env: &FrameRef,
        pos: i32,
    ) -> JResult<i32> {
        let mut comp = 0;
        for term in terms {
            let term_expr = term.borrow().expression.clone().unwrap();
            let (ctx_a, env_a) = if is_tuple_sort {
                let o = a.object_clone().unwrap_or_default();
                (
                    o.get("@").cloned().unwrap_or(JValue::Undefined),
                    self.create_frame_from_tuple(env, &o),
                )
            } else {
                (a.clone(), env.clone())
            };
            let aa = self.evaluate(&term_expr, ctx_a, &env_a)?;
            let (ctx_b, env_b) = if is_tuple_sort {
                let o = b.object_clone().unwrap_or_default();
                (
                    o.get("@").cloned().unwrap_or(JValue::Undefined),
                    self.create_frame_from_tuple(env, &o),
                )
            } else {
                (b.clone(), env.clone())
            };
            let bb = self.evaluate(&term_expr, ctx_b, &env_b)?;

            if aa.is_undefined() {
                comp = if bb.is_undefined() { 0 } else { 1 };
                continue;
            }
            if bb.is_undefined() {
                comp = -1;
                continue;
            }
            let a_ok = aa.is_number() || aa.is_string();
            let b_ok = bb.is_number() || bb.is_string();
            if !a_ok || !b_ok {
                return Err(JError::with_current_expected("T2008", pos, aa, bb));
            }
            let same = (aa.is_number() && bb.is_number()) || (aa.is_string() && bb.is_string());
            if !same {
                return Err(JError::with_current_expected("T2007", pos, aa, bb));
            }
            if aa == bb {
                continue;
            }
            comp = match (&aa, &bb) {
                (JValue::Number(x), JValue::Number(y)) => {
                    if x < y {
                        -1
                    } else {
                        1
                    }
                }
                (JValue::String(x), JValue::String(y)) => {
                    // Java String.compareTo — UTF-16 code-unit order.
                    if crate::value::java_string_cmp(x, y).is_lt() {
                        -1
                    } else {
                        1
                    }
                }
                _ => 0,
            };
            if term.borrow().descending {
                comp = -comp;
            }
            if comp != 0 {
                break;
            }
        }
        Ok(comp)
    }

    // ---- transform -------------------------------------------------------

    fn evaluate_transform(&self, expr: &NodeRef, env: &FrameRef) -> JValue {
        // Build a native transformer function capturing the pattern/update/delete.
        let pattern = expr.borrow().pattern.clone().unwrap();
        let update = expr.borrow().update.clone().unwrap();
        let delete = expr.borrow().delete.clone();
        let captured_env = env.clone();
        let ast = expr.clone();
        let _ = (&pattern, &update, &delete, &captured_env, &ast);
        // The transformer needs the evaluator at call time; we route it through a
        // special Native marker handled in `apply`.
        let native = NativeFn {
            name: "__transform__".to_string(),
            signature: Some(Arc::new(Signature::new("<(oa):o>", "transform"))),
            implementation: NativeImpl::Transform(Rc::new(TransformDef {
                pattern,
                update,
                delete,
                environment: captured_env,
            })),
        };
        JValue::Native(Rc::new(native))
    }

    // ---- apply (~>) ------------------------------------------------------

    fn evaluate_apply(&mut self, expr: &NodeRef, input: JValue, env: &FrameRef) -> JResult<JValue> {
        let lhs_node = expr.borrow().lhs.clone().unwrap();
        let lhs = self.evaluate(&lhs_node, input.clone(), env)?;
        let rhs_node = expr.borrow().rhs.clone().unwrap();
        let pos = expr.borrow().position as i32;

        if rhs_node.borrow().type_is("function") {
            self.evaluate_function(&rhs_node, input, env, ApplyContext::Value(lhs))
        } else {
            let func = self.evaluate(&rhs_node, input.clone(), env)?;
            if !is_function_like(&func) && !is_function_like(&lhs) {
                return Err(JError::with_current("T2006", pos, func));
            }
            if is_function_like(&lhs) {
                let chain = chain_ast();
                let chain_val = self.evaluate(&chain, JValue::Undefined, env)?;
                self.apply(&chain_val, vec![lhs, func], JValue::Undefined, env)
            } else {
                self.apply(&func, vec![lhs], JValue::Undefined, env)
            }
        }
    }

    // ---- function invocation ---------------------------------------------

    fn evaluate_function(
        &mut self,
        expr: &NodeRef,
        input: JValue,
        env: &FrameRef,
        apply_context: ApplyContext,
    ) -> JResult<JValue> {
        let proc_node = expr.borrow().procedure.clone().unwrap();
        let proc = self.evaluate(&proc_node, input.clone(), env)?;
        let pos = expr.borrow().position as i32;

        // helpful "did you forget $" error
        if proc.is_undefined() && proc_node.borrow().type_is("path") {
            let first = proc_node
                .borrow()
                .steps
                .as_ref()
                .and_then(|s| s.first().cloned());
            if let Some(first) = first {
                let name = first.borrow().value.to_string_val();
                if !Frame::lookup(env, &name).is_undefined() {
                    return Err(JError::with_current("T1005", pos, JValue::string(name)));
                }
            }
        }

        let mut evaluated_args: Vec<JValue> = Vec::new();
        if let ApplyContext::Value(v) = apply_context {
            evaluated_args.push(v);
        }
        let args = expr.borrow().arguments.clone().unwrap_or_default();
        for arg in args {
            let a = self.evaluate(&arg, input.clone(), env)?;
            evaluated_args.push(a);
        }

        let proc_name = if proc_node.borrow().type_is("path") {
            proc_node
                .borrow()
                .steps
                .as_ref()
                .and_then(|s| s.first().map(|f| f.borrow().value.to_string_val()))
                .unwrap_or_default()
        } else {
            proc_node.borrow().value.to_string_val()
        };

        if proc.is_undefined() {
            return Err(JError::with_current(
                "T1006",
                pos,
                JValue::string(proc_name),
            ));
        }

        match self.apply(&proc, evaluated_args, input, env) {
            Ok(r) => Ok(r),
            Err(mut e) => {
                if e.location < 0 {
                    e.location = pos;
                }
                Err(e)
            }
        }
    }

    /// `apply` with the tail-call trampoline.
    pub fn apply(
        &mut self,
        proc: &JValue,
        args: Vec<JValue>,
        input: JValue,
        env: &FrameRef,
    ) -> JResult<JValue> {
        let mut result = self.apply_inner(proc, args, input.clone(), env)?;
        loop {
            let thunk = match &result {
                JValue::Lambda(l) if l.thunk => l.clone(),
                _ => break,
            };
            // body is the function-call node
            let body = thunk.body.clone();
            let body_proc = body.borrow().procedure.clone().unwrap();
            let next = self.evaluate(&body_proc, thunk.input.clone(), &thunk.environment)?;
            let mut evaluated_args = Vec::new();
            let body_args = body.borrow().arguments.clone().unwrap_or_default();
            for a in body_args {
                evaluated_args.push(self.evaluate(&a, thunk.input.clone(), &thunk.environment)?);
            }
            result = self.apply_inner(&next, evaluated_args, input.clone(), env)?;
        }
        Ok(result)
    }

    fn apply_inner(
        &mut self,
        proc: &JValue,
        args: Vec<JValue>,
        input: JValue,
        env: &FrameRef,
    ) -> JResult<JValue> {
        // validate arguments against signature
        let validated = self.validate_arguments(proc, args, &input)?;

        match proc {
            JValue::Lambda(l) => self.apply_procedure(l, validated),
            JValue::Native(n) => self.call_native(n, validated, input),
            JValue::Partial(p) => self.apply_partial(p, validated, input, env),
            JValue::Regex(r) => {
                let mut res = Vec::new();
                for s in &validated {
                    if let JValue::String(st) = s {
                        res.push(functions::regex_match_closure(r, st, 0));
                    }
                }
                if res.len() == 1 {
                    Ok(res.into_iter().next().unwrap())
                } else {
                    Ok(JValue::array(res, ArrayFlags::default()))
                }
            }
            _ => Err(JError::at("T1006", 0)),
        }
    }

    fn validate_arguments(
        &self,
        proc: &JValue,
        args: Vec<JValue>,
        context: &JValue,
    ) -> JResult<Vec<JValue>> {
        match proc {
            JValue::Native(n) => {
                if let Some(sig) = &n.signature {
                    sig.validate(args, context)
                } else {
                    Ok(args)
                }
            }
            JValue::Lambda(l) => {
                if let Some(sig) = &l.signature {
                    sig.validate(args, context)
                } else {
                    Ok(args)
                }
            }
            _ => Ok(args),
        }
    }

    fn apply_procedure(&mut self, proc: &Rc<Lambda>, args: Vec<JValue>) -> JResult<JValue> {
        let env = Frame::new(Some(proc.environment.clone()));
        {
            let mut e = env.borrow_mut();
            for (i, param) in proc.arguments.iter().enumerate() {
                if i >= args.len() {
                    break;
                }
                let name = param.borrow().value.to_string_val();
                e.bind(&name, args[i].clone());
            }
        }
        self.evaluate(&proc.body, proc.input.clone(), &env)
    }

    fn apply_partial(
        &mut self,
        partial: &Rc<Partial>,
        args: Vec<JValue>,
        input: JValue,
        env: &FrameRef,
    ) -> JResult<JValue> {
        // fill in the holes with the supplied args, then apply
        let mut full = Vec::new();
        let mut ai = 0;
        for slot in &partial.args {
            match slot {
                Some(v) => full.push(v.clone()),
                None => {
                    if ai < args.len() {
                        full.push(args[ai].clone());
                        ai += 1;
                    } else {
                        full.push(JValue::Undefined);
                    }
                }
            }
        }
        self.apply(&partial.func, full, input, env)
    }

    /// Apply a function for HOFs (`Functions.funcApply`): lambdas go through the
    /// trampoline; natives are called directly (no signature validation).
    pub fn func_apply(&mut self, func: &JValue, args: Vec<JValue>) -> JResult<JValue> {
        match func {
            JValue::Lambda(_) => {
                let env = self.environment.clone();
                self.apply(func, args, JValue::Undefined, &env)
            }
            JValue::Native(n) => self.call_native(n, args, JValue::Undefined),
            JValue::Partial(_) | JValue::Regex(_) => {
                let env = self.environment.clone();
                self.apply(func, args, JValue::Undefined, &env)
            }
            _ => Err(JError::at("T1006", 0)),
        }
    }

    fn call_native(
        &mut self,
        native: &Rc<NativeFn>,
        args: Vec<JValue>,
        _input: JValue,
    ) -> JResult<JValue> {
        // Java Functions.call: when the method's first parameter is a List and
        // the first argument is a defined scalar, wrap it in a singleton list.
        // On the validated call path the signature has already array-coerced
        // the argument (no-op here); on the unvalidated funcApply path (HOF
        // callbacks) this is observable: `$map([1,2,3], $count)` -> [1,1,1].
        let mut args = args;
        if native
            .signature
            .as_ref()
            .is_some_and(|s| s.first_param_is_array())
        {
            if let Some(first) = args.first() {
                if !first.is_array() && !first.is_undefined() {
                    args[0] = JValue::array(vec![args[0].clone()], ArrayFlags::default());
                }
            }
        }
        match &native.implementation {
            NativeImpl::Builtin => functions::call_builtin(self, &native.name, args),
            NativeImpl::Closure(f) => f(&args),
            NativeImpl::Transform(t) => self.apply_transform(t, args),
        }
    }

    fn apply_transform(&mut self, t: &Rc<TransformDef>, args: Vec<JValue>) -> JResult<JValue> {
        use std::collections::HashMap;
        let obj = args.into_iter().next().unwrap_or(JValue::Undefined);
        if obj.is_undefined() {
            return Ok(JValue::Undefined);
        }
        // Fresh deep copy; matched sub-objects share the same Rc allocations,
        // which we use as identity keys to apply updates/deletes during rebuild.
        let result = functions::function_clone(&obj);
        // ptr -> (update keys to merge, in order; deletions)
        let mut changes: HashMap<usize, (Vec<(String, JValue)>, Vec<String>)> = HashMap::new();
        let mut order: Vec<usize> = Vec::new();

        let matches = self.evaluate(&t.pattern, result.clone(), &t.environment)?;
        if !matches.is_undefined() {
            let matches_vec: Vec<JValue> = if matches.is_array() {
                matches.as_array().unwrap().iter().cloned().collect()
            } else {
                vec![matches]
            };
            for m in matches_vec {
                let ptr = match &m {
                    JValue::Object(rc) => Rc::as_ptr(rc) as usize,
                    _ => continue, // updates/deletes only apply to objects
                };
                if !changes.contains_key(&ptr) {
                    order.push(ptr);
                    changes.insert(ptr, (Vec::new(), Vec::new()));
                }
                // Java merges each update into the match object immediately
                // (`((Map)match).put(...)`, Jsonata.java:1469-1471), so a later
                // match over the same object sees earlier updates (e.g.
                // `$ ~> |[$,$]|{"c": c+1}|` on {"c":1} -> {"c":3}; jsonata-js
                // agrees). Rc sharing makes in-place mutation impossible here,
                // so hand the update/delete expressions a view of the match
                // with all changes accumulated so far applied.
                let current = rebuild_with_changes(&m, &changes);
                let update = self.evaluate(&t.update, current, &t.environment)?;
                if !update.is_undefined() {
                    if !update.is_object() {
                        let pos = t.update.borrow().position as i32;
                        return Err(JError::with_current("T2011", pos, update));
                    }
                    if let Some(uo) = update.as_object() {
                        let entry = changes.get_mut(&ptr).unwrap();
                        for (k, v) in uo.iter() {
                            entry.0.push((k.clone(), v.clone()));
                        }
                    }
                }
                if let Some(del_node) = &t.delete {
                    // Java evaluates the delete expression against the
                    // already-updated match — include this match's own update.
                    let current = rebuild_with_changes(&m, &changes);
                    let deletions = self.evaluate(del_node, current, &t.environment)?;
                    if !deletions.is_undefined() {
                        let val = deletions.clone();
                        let del_vec: Vec<JValue> = if deletions.is_array() {
                            deletions.as_array().unwrap().iter().cloned().collect()
                        } else {
                            vec![deletions]
                        };
                        if !del_vec.iter().all(|d| d.is_string()) {
                            let pos = del_node.borrow().position as i32;
                            return Err(JError::with_current("T2012", pos, val));
                        }
                        let entry = changes.get_mut(&ptr).unwrap();
                        for d in del_vec {
                            if let JValue::String(s) = d {
                                entry.1.push(s.to_string());
                            }
                        }
                    }
                }
            }
        }
        Ok(rebuild_with_changes(&result, &changes))
    }

    // ---- lambda / partial application -----------------------------------

    fn evaluate_lambda(&self, expr: &NodeRef, input: JValue, env: &FrameRef) -> JValue {
        let lambda = Lambda {
            input,
            environment: env.clone(),
            arguments: expr.borrow().arguments.clone().unwrap_or_default(),
            signature: expr.borrow().signature.clone(),
            body: expr.borrow().body.clone().unwrap(),
            thunk: expr.borrow().thunk,
        };
        JValue::Lambda(Rc::new(lambda))
    }

    fn evaluate_partial_application(
        &mut self,
        expr: &NodeRef,
        input: JValue,
        env: &FrameRef,
    ) -> JResult<JValue> {
        let mut evaluated_args: Vec<Option<JValue>> = Vec::new();
        let args = expr.borrow().arguments.clone().unwrap_or_default();
        for arg in &args {
            let is_q = {
                let a = arg.borrow();
                a.type_is("operator") && a.value.eq_str("?")
            };
            if is_q {
                evaluated_args.push(None);
            } else {
                evaluated_args.push(Some(self.evaluate(arg, input.clone(), env)?));
            }
        }
        let proc_node = expr.borrow().procedure.clone().unwrap();
        let proc = self.evaluate(&proc_node, input.clone(), env)?;
        let pos = expr.borrow().position as i32;

        if !proc.is_undefined() && proc_node.borrow().type_is("path") {
            let name = proc_node
                .borrow()
                .steps
                .as_ref()
                .and_then(|s| s.first().map(|f| f.borrow().value.to_string_val()))
                .unwrap_or_default();
            if !Frame::lookup(env, &name).is_undefined() {
                return Err(JError::with_current("T1007", pos, JValue::string(name)));
            }
        }

        match &proc {
            JValue::Lambda(_) | JValue::Native(_) | JValue::Partial(_) => {
                // Java's partialApplyProcedure / partialApplyNativeFunction
                // unbind ALL remaining declared parameters, not just the `?`
                // holes — `($g := $add(?); $g(1,2))` is 3, and
                // `$substring(?, 1)` has arity 2 (string + length), so a HOF
                // feeds the element index into the length slot. jsonata-js
                // binds only the supplied slots; see COMPAT.md. Pad the slot
                // list with unbound holes up to the declared parameter count.
                let declared = match &proc {
                    JValue::Lambda(l) => Some(l.arguments.len()),
                    JValue::Native(n) => n.signature.as_ref().map(|s| s.get_number_of_args()),
                    JValue::Partial(p) => Some(p.args.iter().filter(|a| a.is_none()).count()),
                    _ => None,
                };
                if let Some(d) = declared {
                    while evaluated_args.len() < d {
                        evaluated_args.push(None);
                    }
                }
                Ok(JValue::Partial(Rc::new(Partial {
                    func: Box::new(proc),
                    args: evaluated_args,
                })))
            }
            _ => {
                let name = if proc_node.borrow().type_is("path") {
                    proc_node
                        .borrow()
                        .steps
                        .as_ref()
                        .and_then(|s| s.first().map(|f| f.borrow().value.to_string_val()))
                        .unwrap_or_default()
                } else {
                    proc_node.borrow().value.to_string_val()
                };
                Err(JError::with_current("T1008", pos, JValue::string(name)))
            }
        }
    }

    /// Parse + evaluate (`$eval`). Uses the current input/environment.
    pub fn eval_str(&mut self, expr: &str, input: JValue) -> JResult<JValue> {
        let mut parser = Parser::new();
        let ast = parser
            .parse(expr)
            .map_err(|_e| JError::with_current("D3120", -1, JValue::string(expr)))?;
        let env = self.environment.clone();
        let real_input = if input.is_undefined() {
            self.input.clone()
        } else {
            input
        };
        self.evaluate(&ast, real_input, &env).map_err(|e| {
            if e.error.starts_with('D') || e.error.starts_with('T') || e.error.starts_with('S') {
                JError::with_current("D3121", -1, JValue::string(expr))
            } else {
                e
            }
        })
    }
}

/// Definition captured by a transform (`|...|`) expression.
pub struct TransformDef {
    pub pattern: NodeRef,
    pub update: NodeRef,
    pub delete: Option<NodeRef>,
    pub environment: FrameRef,
}

// ---- free helpers --------------------------------------------------------

fn is_function_like(v: &JValue) -> bool {
    v.is_function() || matches!(v, JValue::Regex(_))
}

fn is_array_of_numbers(v: &JValue) -> bool {
    match v {
        JValue::Array(a, _) => a.iter().all(|x| matches!(x, JValue::Number(_))),
        _ => false,
    }
}

fn flatten(arg: JValue, flattened: Option<Vec<JValue>>) -> JValue {
    let mut out = flattened.unwrap_or_default();
    flatten_into(&arg, &mut out);
    JValue::array(out, ArrayFlags::default())
}

fn flatten_into(arg: &JValue, out: &mut Vec<JValue>) {
    if let Some(a) = arg.as_array() {
        for item in a.iter() {
            flatten_into(item, out);
        }
    } else {
        out.push(arg.clone());
    }
}

fn recurse_descendants(input: &JValue, results: &mut Vec<JValue>) {
    if !input.is_array() {
        results.push(input.clone());
    }
    if let Some(a) = input.as_array() {
        for member in a.iter() {
            recurse_descendants(member, results);
        }
    } else if let Some(o) = input.as_object() {
        for (_k, v) in o.iter() {
            recurse_descendants(v, results);
        }
    }
}

/// Rebuild `node`, applying transform changes to any object whose `Rc` pointer
/// is a key in `changes`. Recurses into children so nested matches are reached.
fn rebuild_with_changes(
    node: &JValue,
    changes: &std::collections::HashMap<usize, (Vec<(String, JValue)>, Vec<String>)>,
) -> JValue {
    match node {
        JValue::Object(rc) => {
            let ptr = Rc::as_ptr(rc) as usize;
            let mut new = Object::new();
            for (k, v) in rc.iter() {
                new.insert(k.clone(), rebuild_with_changes(v, changes));
            }
            if let Some((updates, deletions)) = changes.get(&ptr) {
                for (k, v) in updates {
                    new.insert(k.clone(), v.clone());
                }
                for d in deletions {
                    new.shift_remove(d.as_str());
                }
            }
            JValue::object(new)
        }
        JValue::Array(rc, flags) => {
            let new: Vec<JValue> = rc
                .iter()
                .map(|v| rebuild_with_changes(v, changes))
                .collect();
            JValue::Array(Rc::new(new), *flags)
        }
        other => other.clone(),
    }
}

thread_local! {
    static CHAIN_AST: std::cell::RefCell<Option<NodeRef>> = const { std::cell::RefCell::new(None) };
}

fn chain_ast() -> NodeRef {
    CHAIN_AST.with(|c| {
        if c.borrow().is_none() {
            let mut p = Parser::new();
            let ast = p
                .parse("function($f, $g) { function($x){ $g($f($x)) } }")
                .expect("chain ast parse");
            *c.borrow_mut() = Some(ast);
        }
        c.borrow().as_ref().unwrap().clone()
    })
}

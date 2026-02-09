#![allow(clippy::wrong_self_convention)]
#![allow(clippy::too_many_arguments)]

use std::{
    fmt::Display,
    fs::{OpenOptions, create_dir_all},
    io::Write,
    path::Path,
    str::FromStr,
    sync::LazyLock,
};

use hashlink::LinkedHashMap;
use jsonschema::Validator;
use pyo3::{
    exceptions::{PyRuntimeError, PyValueError},
    prelude::*,
    types::{PyDict, PyDictMethods},
};
use serde_json::{Map, Number, Value};
use yaml_rust2::{
    Yaml, YamlEmitter,
    yaml::{Array, Hash},
};

pub trait Yamlable {
    fn as_yaml(&self) -> Yaml;
    fn as_yaml_string(&self) -> PyResult<String> {
        let yaml = self.as_yaml();
        let mut out_str = String::new();
        let mut emitter = YamlEmitter::new(&mut out_str);
        emitter.multiline_strings(true);
        emitter
            .dump(&yaml)
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
        Ok(out_str)
    }
    fn write_to_file(&self, path: impl AsRef<Path>, overwrite: bool) -> PyResult<()> {
        let path = path.as_ref();
        if let Some(parent) = path.parent()
            && !parent.as_os_str().is_empty()
        {
            create_dir_all(parent)?;
        }
        let mut opts = OpenOptions::new();
        opts.write(true).create(true);
        if overwrite {
            opts.truncate(true);
        } else {
            opts.create_new(true);
        }
        let mut file = match opts.open(path) {
            Ok(f) => f,
            Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => return Ok(()),
            Err(e) => return Err(PyErr::from(e)),
        };

        file.write_all(self.as_yaml_string()?.as_bytes())?;
        file.flush()?;
        Ok(())
    }
}
impl Yamlable for Yaml {
    fn as_yaml(&self) -> Yaml {
        self.clone()
    }
}
impl Yamlable for &Yaml {
    fn as_yaml(&self) -> Yaml {
        self.to_owned().clone()
    }
}

fn push_escaped_control(out: &mut String, ch: char) -> bool {
    match ch {
        '\n' => out.push_str("\\n"),
        '\r' => out.push_str("\\r"),
        '\t' => out.push_str("\\t"),
        c if c.is_control() => {
            use std::fmt::Write as _;
            let _ = write!(out, "\\u{:04X}", c as u32);
        }
        _ => return false,
    }
    true
}

fn escape_control_chars(s: &str) -> String {
    let mut out = String::with_capacity(s.len());
    for ch in s.chars() {
        if !push_escaped_control(&mut out, ch) {
            out.push(ch);
        }
    }
    out
}

fn contains_github_expression(s: &str) -> bool {
    s.contains("${{") && s.contains("}}")
}

fn normalize_expression_aware_string(s: &str) -> String {
    if contains_github_expression(s) {
        escape_control_chars(s)
    } else {
        s.to_string()
    }
}

fn yaml_string_or_expression_scalar(s: &str) -> Yaml {
    if contains_github_expression(s) {
        // Keep expression strings unquoted where possible while preserving escaped control chars.
        Yaml::Real(normalize_expression_aware_string(s))
    } else {
        Yaml::String(s.to_string())
    }
}
impl Yamlable for f64 {
    fn as_yaml(&self) -> Yaml {
        Yaml::Real(self.to_string())
    }
}
impl Yamlable for &f64 {
    fn as_yaml(&self) -> Yaml {
        Yaml::Real(self.to_string())
    }
}
impl Yamlable for String {
    fn as_yaml(&self) -> Yaml {
        yaml_string_or_expression_scalar(self)
    }
}
impl Yamlable for &str {
    fn as_yaml(&self) -> Yaml {
        self.to_string().as_yaml()
    }
}
impl Yamlable for &String {
    fn as_yaml(&self) -> Yaml {
        (*self).clone().as_yaml()
    }
}
impl Yamlable for i64 {
    fn as_yaml(&self) -> Yaml {
        Yaml::Integer(*self)
    }
}
impl Yamlable for &i64 {
    fn as_yaml(&self) -> Yaml {
        Yaml::Integer(**self)
    }
}
impl Yamlable for bool {
    fn as_yaml(&self) -> Yaml {
        Yaml::Boolean(*self)
    }
}
impl Yamlable for &bool {
    fn as_yaml(&self) -> Yaml {
        Yaml::Boolean(**self)
    }
}
impl<T> Yamlable for Vec<T>
where
    T: Yamlable,
{
    fn as_yaml(&self) -> Yaml {
        Yaml::Array(self.iter().map(Yamlable::as_yaml).collect())
    }
}
impl<T> Yamlable for &Vec<T>
where
    T: Yamlable,
{
    fn as_yaml(&self) -> Yaml {
        Yaml::Array(self.iter().map(Yamlable::as_yaml).collect())
    }
}
impl<T> Yamlable for &[T]
where
    T: Yamlable,
{
    fn as_yaml(&self) -> Yaml {
        Yaml::Array(self.iter().map(Yamlable::as_yaml).collect())
    }
}

#[derive(Clone)]
pub struct PyMap<K, V>(LinkedHashMap<K, V>)
where
    K: std::cmp::Eq + std::hash::Hash;
impl<K, V> PyMap<K, V>
where
    K: std::cmp::Eq + std::hash::Hash,
{
    fn iter(&self) -> hashlink::linked_hash_map::Iter<'_, K, V> {
        self.0.iter()
    }
    fn is_empty(&self) -> bool {
        self.0.is_empty()
    }
}
impl<K, V> IntoIterator for PyMap<K, V>
where
    K: std::cmp::Eq + std::hash::Hash,
{
    type Item = <LinkedHashMap<K, V> as IntoIterator>::Item;

    type IntoIter = <LinkedHashMap<K, V> as IntoIterator>::IntoIter;

    fn into_iter(self) -> Self::IntoIter {
        self.0.into_iter()
    }
}
impl<K, V> Default for PyMap<K, V>
where
    K: std::cmp::Eq + std::hash::Hash,
{
    fn default() -> Self {
        Self(LinkedHashMap::default())
    }
}
impl<'a, 'py, K, V> FromPyObject<'a, 'py> for PyMap<K, V>
where
    K: FromPyObjectOwned<'py> + std::cmp::Eq + std::hash::Hash,
    V: FromPyObjectOwned<'py>,
{
    type Error = PyErr;

    fn extract(obj: Borrowed<'a, 'py, PyAny>) -> Result<Self, Self::Error> {
        let dict = obj.cast::<PyDict>()?;
        let mut ret = LinkedHashMap::with_capacity(dict.len());
        for (k, v) in dict.iter() {
            ret.insert(
                k.extract().map_err(Into::into)?,
                v.extract().map_err(Into::into)?,
            );
        }
        Ok(PyMap(ret))
    }
}
impl<K, V> Yamlable for &PyMap<K, V>
where
    K: std::cmp::Eq + std::hash::Hash,
    for<'a> &'a K: Yamlable,
    for<'b> &'b V: Yamlable,
{
    fn as_yaml(&self) -> Yaml {
        let mut hash = Hash::new();
        for (k, v) in &self.0 {
            hash.insert_yaml(k, v);
        }
        Yaml::Hash(hash)
    }
}
#[derive(Clone)]
pub enum BoolOrString {
    Bool(bool),
    String(String),
}
impl Yamlable for &BoolOrString {
    fn as_yaml(&self) -> Yaml {
        match self {
            BoolOrString::Bool(b) => Yaml::Boolean(*b),
            BoolOrString::String(s) => Yaml::String(s.clone()),
        }
    }
}
impl<'a, 'py> FromPyObject<'a, 'py> for BoolOrString {
    type Error = PyErr;

    fn extract(obj: Borrowed<'a, 'py, PyAny>) -> Result<Self, Self::Error> {
        if let Ok(b) = obj.extract::<bool>() {
            Ok(Self::Bool(b))
        } else if let Ok(s) = obj.extract::<String>() {
            Ok(Self::String(s))
        } else {
            Err(PyValueError::new_err(
                "Expected bool or string which evaluates to bool",
            ))
        }
    }
}

pub trait MaybeYamlable {
    fn maybe_as_yaml(&self) -> Option<Yaml>;
    fn maybe_as_yaml_string(&self) -> PyResult<String> {
        self.maybe_as_yaml()
            .map_or(Ok(String::new()), |y| y.as_yaml_string())
    }
}

pub trait TryYamlable {
    fn try_as_yaml(&self) -> PyResult<Yaml>;
}

pub trait TryHash {
    fn try_as_hash(&self) -> PyResult<Hash>;
}
pub trait TryArray {
    fn try_as_array(&self) -> PyResult<Vec<Yaml>>;
}
impl<T> TryYamlable for T
where
    T: Yamlable,
{
    fn try_as_yaml(&self) -> PyResult<Yaml> {
        Ok(self.as_yaml())
    }
}
pub trait InsertYaml {
    fn insert_yaml(&mut self, key: impl Yamlable, value: impl Yamlable);
    fn insert_yaml_opt(&mut self, key: impl Yamlable, value: impl IntoYamlOption);
}

pub trait IntoYamlOption {
    fn into_yaml_option(self) -> Option<Yaml>;
}

impl<T> IntoYamlOption for Option<T>
where
    T: Yamlable,
{
    fn into_yaml_option(self) -> Option<Yaml> {
        self.map(|value| value.as_yaml())
    }
}

impl<'a, T> IntoYamlOption for &'a Option<T>
where
    &'a T: Yamlable,
{
    fn into_yaml_option(self) -> Option<Yaml> {
        self.as_ref().map(|value| value.as_yaml())
    }
}

impl InsertYaml for Hash {
    fn insert_yaml(&mut self, key: impl Yamlable, value: impl Yamlable) {
        self.insert(key.as_yaml(), value.as_yaml());
    }
    fn insert_yaml_opt(&mut self, key: impl Yamlable, value: impl IntoYamlOption) {
        if let Some(value) = value.into_yaml_option() {
            self.insert(key.as_yaml(), value);
        }
    }
}

pub trait PushYaml {
    fn push_yaml(&mut self, value: impl Yamlable);
    fn push_yaml_opt(&mut self, value: impl IntoYamlOption);
    fn push_yaml_cond(&mut self, value: impl Yamlable, cond: bool);
}

impl PushYaml for Array {
    fn push_yaml(&mut self, value: impl Yamlable) {
        self.push(value.as_yaml());
    }

    fn push_yaml_opt(&mut self, value: impl IntoYamlOption) {
        if let Some(value) = value.into_yaml_option() {
            self.push(value.as_yaml());
        }
    }
    fn push_yaml_cond(&mut self, value: impl Yamlable, cond: bool) {
        if cond {
            self.push_yaml(value);
        }
    }
}

pub enum Either<A, B> {
    A(A),
    B(B),
}
impl<A, B> Clone for Either<A, B>
where
    A: Clone,
    B: Clone,
{
    fn clone(&self) -> Self {
        match self {
            Self::A(a) => Self::A(a.clone()),
            Self::B(b) => Self::B(b.clone()),
        }
    }
}
impl<A, B> Display for Either<A, B>
where
    A: Display,
    B: Display,
{
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Either::A(a) => write!(f, "{a}"),
            Either::B(b) => write!(f, "{b}"),
        }
    }
}
impl<'a, 'py, A, B> FromPyObject<'a, 'py> for Either<A, B>
where
    A: FromPyObject<'a, 'py>,
    B: FromPyObject<'a, 'py>,
{
    type Error = PyErr;

    fn extract(obj: Borrowed<'a, 'py, PyAny>) -> Result<Self, Self::Error> {
        if let Ok(a) = obj.extract::<A>() {
            Ok(Self::A(a))
        } else if let Ok(b) = obj.extract::<B>() {
            Ok(Self::B(b))
        } else {
            Err(PyValueError::new_err("Invalid value"))
        }
    }
}
impl<A, B> Yamlable for Either<A, B>
where
    for<'a> &'a A: Yamlable,
    for<'b> &'b B: Yamlable,
{
    fn as_yaml(&self) -> Yaml {
        match self {
            Either::A(a) => a.as_yaml(),
            Either::B(b) => b.as_yaml(),
        }
    }
}
impl<A, B> Yamlable for &Either<A, B>
where
    for<'a> &'a A: Yamlable,
    for<'b> &'b B: Yamlable,
{
    fn as_yaml(&self) -> Yaml {
        match self {
            Either::A(a) => a.as_yaml(),
            Either::B(b) => b.as_yaml(),
        }
    }
}

/// A Pythonic implementation of GitHub Actions syntax
#[pymodule]
#[pyo3(name = "_yamloom")]
mod yamloom {
    use std::{collections::HashMap, fmt::Display, path::PathBuf, str::FromStr};

    use pyo3::{
        exceptions::{PyRuntimeError, PyValueError},
        prelude::*,
        types::{PyBool, PyDict, PyFloat, PyInt, PyList, PyString, PyTuple},
    };
    use yaml_rust2::{
        Yaml,
        yaml::{Array, Hash},
    };

    use crate::{
        Either, InsertYaml, MaybeYamlable, PushYaml, PyMap, TryArray, TryHash, TryYamlable,
        WORKFLOW_SCHEMA, Yamlable, contains_github_expression, normalize_expression_aware_string,
        yaml_to_json,
        yamloom::expressions::{
            Allowed, ArrayExpression, BooleanExpression, Contexts, Funcs, NumberExpression,
            ObjectExpression, StringExpression, YamlExpression,
        },
    };

    #[pymodule]
    mod expressions {
        use std::marker::PhantomData;

        use bitflags::bitflags;
        use pyo3::{
            exceptions::PyRuntimeError,
            types::{PyFloat, PyInt},
        };

        use crate::push_escaped_control;

        use super::{
            Bound, Display, Either, Py, PyAny, PyAnyMethods, PyResult, PyValueError, Yaml,
            Yamlable, pyclass, pyfunction, pymethods,
        };

        type StringLike = Either<StringExpression, String>;
        type BoolLike = Either<BooleanExpression, bool>;
        type NumberLike = Either<NumberExpression, f64>;

        bitflags! {
            #[derive(Clone, Copy, Debug, PartialEq, Eq)]
        pub(super) struct Contexts: u32 {
                const NONE = 0;
                const GITHUB = 1 << 0;
                const SECRETS = 1 << 1;
                const ENV = 1 << 2;
                const VARS = 1 << 3;
                const INPUTS = 1 << 4;
                const NEEDS = 1 << 5;
                const STRATEGY = 1 << 6;
                const MATRIX = 1 << 7;
                const JOB = 1 << 8;
                const RUNNER = 1 << 9;
                const STEPS = 1 << 10;
                const JOBS = 1 << 11;
            }
        }

        bitflags! {
            #[derive(Clone, Copy, Debug, PartialEq, Eq)]
        pub(super) struct Funcs: u32 {
                const NONE = 0;
                const HASH_FILES = 1 << 0;
                const ALWAYS = 1 << 1;
                const CANCELLED = 1 << 2;
                const SUCCESS = 1 << 3;
                const FAILURE = 1 << 4;
            }
        }

        #[derive(Clone, Copy, Debug, PartialEq, Eq)]
        struct ExprMeta {
            contexts: Contexts,
            funcs: Funcs,
        }

        impl ExprMeta {
            const fn empty() -> Self {
                Self {
                    contexts: Contexts::NONE,
                    funcs: Funcs::NONE,
                }
            }

            const fn with_contexts(contexts: Contexts) -> Self {
                Self {
                    contexts,
                    funcs: Funcs::NONE,
                }
            }

            const fn with_funcs(funcs: Funcs) -> Self {
                Self {
                    contexts: Contexts::NONE,
                    funcs,
                }
            }

            fn union(self, other: Self) -> Self {
                Self {
                    contexts: self.contexts | other.contexts,
                    funcs: self.funcs | other.funcs,
                }
            }
        }

        #[derive(Clone)]
        struct ExprBase {
            text: String,
            meta: ExprMeta,
        }

        impl ExprBase {
            fn new(text: String, meta: ExprMeta) -> Self {
                Self { text, meta }
            }

            fn with_contexts(text: impl Into<String>, contexts: Contexts) -> Self {
                Self::new(text.into(), ExprMeta::with_contexts(contexts))
            }
        }

        struct Expression<K> {
            base: ExprBase,
            _kind: PhantomData<K>,
        }

        impl<K> Clone for Expression<K> {
            fn clone(&self) -> Self {
                Self {
                    base: self.base.clone(),
                    _kind: PhantomData,
                }
            }
        }

        impl<K> Expression<K> {
            fn new(text: String, meta: ExprMeta) -> Self {
                Self {
                    base: ExprBase::new(text, meta),
                    _kind: PhantomData,
                }
            }

            fn from_base(base: ExprBase) -> Self {
                Self {
                    base,
                    _kind: PhantomData,
                }
            }

            fn text(&self) -> &str {
                &self.base.text
            }

            fn meta(&self) -> ExprMeta {
                self.base.meta
            }
        }

        struct BoolKind;
        struct NumberKind;
        struct StringKind;
        struct ArrayKind;
        struct ObjectKind;

        #[derive(Clone, Copy, Debug)]
        pub(super) struct Allowed {
            contexts: Contexts,
            funcs: Funcs,
            label: &'static str,
        }

        impl Allowed {
            pub(super) const fn new(contexts: Contexts, funcs: Funcs, label: &'static str) -> Self {
                Self {
                    contexts,
                    funcs,
                    label,
                }
            }

            fn validate(self, meta: ExprMeta, expr: &str) -> PyResult<()> {
                let disallowed_contexts = meta.contexts & !self.contexts;
                let disallowed_funcs = meta.funcs & !self.funcs;
                if disallowed_contexts.is_empty() && disallowed_funcs.is_empty() {
                    return Ok(());
                }

                let allowed_contexts = contexts_to_names(self.contexts);
                let allowed_funcs = funcs_to_names(self.funcs);
                let used_contexts = contexts_to_names(disallowed_contexts);
                let used_funcs = funcs_to_names(disallowed_funcs);

                let mut message = format!(
                    "Key '{}' does not allow the context(s) {{{}}}",
                    self.label,
                    used_contexts.join(", ")
                );
                if !used_funcs.is_empty() {
                    message.push_str(&format!(" or function(s) {{{}}}", used_funcs.join(", ")));
                }
                message.push_str(&format!(
                    " used in this expression:\n{}\n\nAllowed contexts: {{{}}}",
                    expr,
                    allowed_contexts.join(", ")
                ));
                if !self.funcs.is_empty() {
                    message.push_str(&format!(
                        "\nAllowed functions: {{{}}}",
                        allowed_funcs.join(", ")
                    ));
                }
                Err(PyRuntimeError::new_err(message))
            }
        }

        fn contexts_to_names(contexts: Contexts) -> Vec<&'static str> {
            let mut out = Vec::new();
            if contexts.contains(Contexts::GITHUB) {
                out.push("github");
            }
            if contexts.contains(Contexts::NEEDS) {
                out.push("needs");
            }
            if contexts.contains(Contexts::STRATEGY) {
                out.push("strategy");
            }
            if contexts.contains(Contexts::MATRIX) {
                out.push("matrix");
            }
            if contexts.contains(Contexts::JOB) {
                out.push("job");
            }
            if contexts.contains(Contexts::JOBS) {
                out.push("jobs");
            }
            if contexts.contains(Contexts::RUNNER) {
                out.push("runner");
            }
            if contexts.contains(Contexts::STEPS) {
                out.push("steps");
            }
            if contexts.contains(Contexts::ENV) {
                out.push("env");
            }
            if contexts.contains(Contexts::VARS) {
                out.push("vars");
            }
            if contexts.contains(Contexts::SECRETS) {
                out.push("secrets");
            }
            if contexts.contains(Contexts::INPUTS) {
                out.push("inputs");
            }
            out
        }

        fn funcs_to_names(funcs: Funcs) -> Vec<&'static str> {
            let mut out = Vec::new();
            if funcs.contains(Funcs::HASH_FILES) {
                out.push("hashFiles");
            }
            if funcs.contains(Funcs::ALWAYS) {
                out.push("always");
            }
            if funcs.contains(Funcs::CANCELLED) {
                out.push("cancelled");
            }
            if funcs.contains(Funcs::SUCCESS) {
                out.push("success");
            }
            if funcs.contains(Funcs::FAILURE) {
                out.push("failure");
            }
            out
        }

        fn render_string_like(value: StringLike) -> (String, ExprMeta) {
            match value {
                Either::A(expr) => (expr.to_string(), expr.meta()),
                Either::B(raw) => (escape_string(&raw), ExprMeta::empty()),
            }
        }

        fn render_bool_like(value: BoolLike) -> (String, ExprMeta) {
            match value {
                Either::A(expr) => (expr.to_string(), expr.meta()),
                Either::B(raw) => (
                    if raw {
                        "true".to_string()
                    } else {
                        "false".to_string()
                    },
                    ExprMeta::empty(),
                ),
            }
        }

        fn render_number_like(value: NumberLike) -> (String, ExprMeta) {
            match value {
                Either::A(expr) => (expr.to_string(), expr.meta()),
                Either::B(raw) => (raw.to_string(), ExprMeta::empty()),
            }
        }

        pub trait YamlExpression {
            fn stringify(&self) -> &str;
            fn as_expression_string(&self) -> String {
                format!("${{{{ {} }}}}", self.stringify())
            }
        }
        impl<T> Yamlable for &T
        where
            T: YamlExpression,
        {
            fn as_yaml(&self) -> Yaml {
                Yaml::Real(self.as_expression_string())
            }
        }

        #[pyclass]
        #[derive(Clone)]
        pub struct BooleanExpression(Expression<BoolKind>);
        impl YamlExpression for BooleanExpression {
            fn stringify(&self) -> &str {
                self.0.text()
            }
        }
        impl Display for BooleanExpression {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                write!(f, "{}", self.stringify())
            }
        }
        impl BooleanExpression {
            fn new_expr(text: String, meta: ExprMeta) -> Self {
                Self(Expression::new(text, meta))
            }

            fn from_base(base: ExprBase) -> Self {
                Self(Expression::from_base(base))
            }

            fn meta(&self) -> ExprMeta {
                self.0.meta()
            }

            pub(super) fn validate_allowed(&self, allowed: Allowed) -> PyResult<()> {
                allowed.validate(self.meta(), &self.as_expression_string())
            }
        }
        #[pymethods]
        impl BooleanExpression {
            fn as_num(&self) -> NumberExpression {
                NumberExpression::new_expr(self.to_string(), self.meta())
            }
            fn as_str(&self) -> StringExpression {
                StringExpression::new_expr(self.to_string(), self.meta())
            }
            fn as_obj(&self) -> ObjectExpression {
                ObjectExpression::new_expr(self.to_string(), self.meta())
            }
            fn __invert__(&self) -> Self {
                Self::new_expr(format!("!({self})"), self.meta())
            }
            fn __and__(&self, other: BoolLike) -> Self {
                let (other, other_meta) = render_bool_like(other);
                Self::new_expr(
                    format!("({self} && {other})"),
                    self.meta().union(other_meta),
                )
            }
            fn __or__(&self, other: BoolLike) -> Self {
                let (other, other_meta) = render_bool_like(other);
                Self::new_expr(
                    format!("({self} || {other})"),
                    self.meta().union(other_meta),
                )
            }
            fn __eq__(&self, other: BoolLike) -> Self {
                let (other, other_meta) = render_bool_like(other);
                Self::new_expr(
                    format!("({self} == {other})"),
                    self.meta().union(other_meta),
                )
            }
            fn __ne__(&self, other: BoolLike) -> Self {
                let (other, other_meta) = render_bool_like(other);
                Self::new_expr(
                    format!("({self} != {other})"),
                    self.meta().union(other_meta),
                )
            }
            fn if_else(&self, condition: BoolLike, else_expr: BoolLike) -> BooleanExpression {
                let (condition, condition_meta) = render_bool_like(condition);
                let (else_expr, else_meta) = render_bool_like(else_expr);
                let meta = self.meta().union(condition_meta).union(else_meta);
                BooleanExpression::new_expr(format!("({condition} && {self} || {else_expr})"), meta)
            }
            fn to_json(&self) -> ObjectExpression {
                ObjectExpression::new_expr(format!("toJSON({self})"), self.meta())
            }
            fn __str__(&self) -> String {
                self.as_expression_string()
            }
        }
        #[pyfunction]
        fn success() -> BooleanExpression {
            BooleanExpression::new_expr(
                "success()".to_string(),
                ExprMeta::with_funcs(Funcs::SUCCESS),
            )
        }
        #[pyfunction]
        fn always() -> BooleanExpression {
            BooleanExpression::new_expr("always()".to_string(), ExprMeta::with_funcs(Funcs::ALWAYS))
        }
        #[pyfunction]
        fn cancelled() -> BooleanExpression {
            BooleanExpression::new_expr(
                "cancelled()".to_string(),
                ExprMeta::with_funcs(Funcs::CANCELLED),
            )
        }
        #[pyfunction]
        fn failure() -> BooleanExpression {
            BooleanExpression::new_expr(
                "failure()".to_string(),
                ExprMeta::with_funcs(Funcs::FAILURE),
            )
        }
        #[pyclass]
        #[derive(Clone)]
        pub struct NumberExpression(Expression<NumberKind>);
        impl YamlExpression for NumberExpression {
            fn stringify(&self) -> &str {
                self.0.text()
            }
        }
        impl Display for NumberExpression {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                write!(f, "{}", self.stringify())
            }
        }
        impl NumberExpression {
            fn new_expr(text: String, meta: ExprMeta) -> Self {
                Self(Expression::new(text, meta))
            }

            fn from_base(base: ExprBase) -> Self {
                Self(Expression::from_base(base))
            }

            fn meta(&self) -> ExprMeta {
                self.0.meta()
            }

            pub(super) fn validate_allowed(&self, allowed: Allowed) -> PyResult<()> {
                allowed.validate(self.meta(), &self.as_expression_string())
            }
        }
        #[pymethods]
        impl NumberExpression {
            fn as_bool(&self) -> BooleanExpression {
                BooleanExpression::new_expr(self.to_string(), self.meta())
            }
            fn as_str(&self) -> StringExpression {
                StringExpression::new_expr(self.to_string(), self.meta())
            }
            fn as_obj(&self) -> ObjectExpression {
                ObjectExpression::new_expr(self.to_string(), self.meta())
            }
            fn __lt__(&self, other: NumberLike) -> BooleanExpression {
                let (other, other_meta) = render_number_like(other);
                BooleanExpression::new_expr(
                    format!("({self} < {other})"),
                    self.meta().union(other_meta),
                )
            }
            fn __le__(&self, other: NumberLike) -> BooleanExpression {
                let (other, other_meta) = render_number_like(other);
                BooleanExpression::new_expr(
                    format!("({self} <= {other})"),
                    self.meta().union(other_meta),
                )
            }
            fn __gt__(&self, other: NumberLike) -> BooleanExpression {
                let (other, other_meta) = render_number_like(other);
                BooleanExpression::new_expr(
                    format!("({self} > {other})"),
                    self.meta().union(other_meta),
                )
            }
            fn __ge__(&self, other: NumberLike) -> BooleanExpression {
                let (other, other_meta) = render_number_like(other);
                BooleanExpression::new_expr(
                    format!("({self} >= {other})"),
                    self.meta().union(other_meta),
                )
            }
            fn __eq__(&self, other: NumberLike) -> BooleanExpression {
                let (other, other_meta) = render_number_like(other);
                BooleanExpression::new_expr(
                    format!("({self} == {other})"),
                    self.meta().union(other_meta),
                )
            }
            fn __ne__(&self, other: NumberLike) -> BooleanExpression {
                let (other, other_meta) = render_number_like(other);
                BooleanExpression::new_expr(
                    format!("({self} != {other})"),
                    self.meta().union(other_meta),
                )
            }
            fn if_else(&self, condition: BoolLike, else_expr: NumberLike) -> NumberExpression {
                let (condition, condition_meta) = render_bool_like(condition);
                let (else_expr, else_meta) = render_number_like(else_expr);
                let meta = self.meta().union(condition_meta).union(else_meta);
                NumberExpression::new_expr(format!("({condition} && {self} || {else_expr})"), meta)
            }
            fn to_json(&self) -> ObjectExpression {
                ObjectExpression::new_expr(format!("toJSON({self})"), self.meta())
            }
            fn __str__(&self) -> String {
                self.as_expression_string()
            }
        }
        #[pyclass]
        #[derive(Clone)]
        pub struct StringExpression(Expression<StringKind>);
        impl YamlExpression for StringExpression {
            fn stringify(&self) -> &str {
                self.0.text()
            }
        }
        impl Display for StringExpression {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                write!(f, "{}", self.stringify())
            }
        }
        impl StringExpression {
            fn new_expr(text: String, meta: ExprMeta) -> Self {
                Self(Expression::new(text, meta))
            }

            fn from_base(base: ExprBase) -> Self {
                Self(Expression::from_base(base))
            }

            fn meta(&self) -> ExprMeta {
                self.0.meta()
            }

            pub(super) fn validate_allowed(&self, allowed: Allowed) -> PyResult<()> {
                allowed.validate(self.meta(), &self.as_expression_string())
            }
        }
        #[pymethods]
        impl StringExpression {
            fn as_bool(&self) -> BooleanExpression {
                BooleanExpression::new_expr(self.to_string(), self.meta())
            }
            fn as_num(&self) -> NumberExpression {
                NumberExpression::new_expr(self.to_string(), self.meta())
            }
            fn as_obj(&self) -> ObjectExpression {
                ObjectExpression::new_expr(self.to_string(), self.meta())
            }
            fn __eq__(&self, other: StringLike) -> BooleanExpression {
                let (other, other_meta) = render_string_like(other);
                BooleanExpression::new_expr(
                    format!("({self} == {other})"),
                    self.meta().union(other_meta),
                )
            }
            fn __ne__(&self, other: StringLike) -> BooleanExpression {
                let (other, other_meta) = render_string_like(other);
                BooleanExpression::new_expr(
                    format!("({self} != {other})"),
                    self.meta().union(other_meta),
                )
            }
            fn contains(&self, other: StringLike) -> BooleanExpression {
                let (other, other_meta) = render_string_like(other);
                BooleanExpression::new_expr(
                    format!("contains({self}, {other})"),
                    self.meta().union(other_meta),
                )
            }
            fn startswith(&self, other: StringLike) -> BooleanExpression {
                let (other, other_meta) = render_string_like(other);
                BooleanExpression::new_expr(
                    format!("startsWith({self}, {other})"),
                    self.meta().union(other_meta),
                )
            }
            fn endswith(&self, other: StringLike) -> BooleanExpression {
                let (other, other_meta) = render_string_like(other);
                BooleanExpression::new_expr(
                    format!("endsWith({self}, {other})"),
                    self.meta().union(other_meta),
                )
            }
            fn format(&self, args: Vec<StringLike>) -> StringExpression {
                let mut meta = self.meta();
                let args = args
                    .into_iter()
                    .map(|arg| {
                        let (text, arg_meta) = render_string_like(arg);
                        meta = meta.union(arg_meta);
                        text
                    })
                    .collect::<Vec<String>>()
                    .join(", ");
                StringExpression::new_expr(format!("format({self}, {args})"), meta)
            }
            // I don't think we need join for single strings despite the docs
            fn to_json(&self) -> ObjectExpression {
                ObjectExpression::new_expr(format!("toJSON({self})"), self.meta())
            }
            fn from_json_to_bool(&self) -> BooleanExpression {
                BooleanExpression::new_expr(format!("fromJSON({self})"), self.meta())
            }
            fn from_json_to_num(&self) -> NumberExpression {
                NumberExpression::new_expr(format!("fromJSON({self})"), self.meta())
            }
            fn from_json_to_str(&self) -> Self {
                Self::new_expr(format!("fromJSON({self})"), self.meta())
            }
            fn from_json_to_array(&self) -> ArrayExpression {
                ArrayExpression::new_expr(format!("fromJSON({self})"), self.meta())
            }
            fn from_json_to_obj(&self) -> ObjectExpression {
                ObjectExpression::new_expr(format!("fromJSON({self})"), self.meta())
            }
            fn hash_files(&self, others: Option<Vec<StringLike>>) -> StringExpression {
                if let Some(others) = others {
                    let mut meta = self.meta().union(ExprMeta::with_funcs(Funcs::HASH_FILES));
                    let args = others
                        .into_iter()
                        .map(|other| {
                            let (text, other_meta) = render_string_like(other);
                            meta = meta.union(other_meta);
                            text
                        })
                        .collect::<Vec<String>>()
                        .join(", ");
                    StringExpression::new_expr(format!("hashFiles({self}, {args})"), meta)
                } else {
                    StringExpression::new_expr(
                        format!("hashFiles({self})"),
                        self.meta().union(ExprMeta::with_funcs(Funcs::HASH_FILES)),
                    )
                }
            }
            fn if_else(&self, condition: BoolLike, else_expr: StringLike) -> StringExpression {
                let (condition, condition_meta) = render_bool_like(condition);
                let (else_expr, else_meta) = render_string_like(else_expr);
                let meta = self.meta().union(condition_meta).union(else_meta);
                StringExpression::new_expr(format!("({condition} && {self} || {else_expr})"), meta)
            }
            fn __str__(&self) -> String {
                self.as_expression_string()
            }
        }

        impl Display for ArrayExpression {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                write!(f, "{}", self.stringify())
            }
        }

        #[pyclass]
        #[derive(Clone)]
        pub struct ArrayExpression(Expression<ArrayKind>);
        impl YamlExpression for ArrayExpression {
            fn stringify(&self) -> &str {
                self.0.text()
            }
        }
        impl ArrayExpression {
            fn new_expr(text: String, meta: ExprMeta) -> Self {
                Self(Expression::new(text, meta))
            }

            fn meta(&self) -> ExprMeta {
                self.0.meta()
            }

            pub(super) fn validate_allowed(&self, allowed: Allowed) -> PyResult<()> {
                allowed.validate(self.meta(), &self.as_expression_string())
            }
        }
        #[pymethods]
        impl ArrayExpression {
            fn as_num(&self) -> NumberExpression {
                NumberExpression::new_expr(self.to_string(), self.meta())
            }
            fn as_obj(&self) -> ObjectExpression {
                ObjectExpression::new_expr(self.to_string(), self.meta())
            }
            fn contains(&self, other: &ObjectExpression) -> BooleanExpression {
                BooleanExpression::new_expr(
                    format!("contains({}, {})", self, other.stringify()),
                    self.meta().union(other.meta()),
                )
            }
            fn join(&self, separator: Option<StringLike>) -> StringExpression {
                if let Some(sep) = separator {
                    let (sep, sep_meta) = render_string_like(sep);
                    StringExpression::new_expr(
                        format!("join({self}, {sep})"),
                        self.meta().union(sep_meta),
                    )
                } else {
                    StringExpression::new_expr(format!("join({self})"), self.meta())
                }
            }
            fn to_json(&self) -> ObjectExpression {
                ObjectExpression::new_expr(format!("toJSON({self})"), self.meta())
            }
            fn __str__(&self) -> String {
                self.as_expression_string()
            }
        }
        #[pyclass]
        #[derive(Clone)]
        pub struct ObjectExpression(Expression<ObjectKind>);
        impl YamlExpression for ObjectExpression {
            fn stringify(&self) -> &str {
                self.0.text()
            }
        }
        impl Display for ObjectExpression {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                write!(f, "{}", self.stringify())
            }
        }
        impl ObjectExpression {
            fn format_access(base: &str, key: &str) -> String {
                if validate_string(key) {
                    format!("{base}.{key}")
                } else {
                    format!("{base}[{}]", escape_string(key))
                }
            }
        }
        impl ObjectExpression {
            fn new_expr(text: String, meta: ExprMeta) -> Self {
                Self(Expression::new(text, meta))
            }

            fn from_base(base: ExprBase) -> Self {
                Self(Expression::from_base(base))
            }

            fn meta(&self) -> ExprMeta {
                self.0.meta()
            }

            pub(super) fn validate_allowed(&self, allowed: Allowed) -> PyResult<()> {
                allowed.validate(self.meta(), &self.as_expression_string())
            }
        }
        #[pymethods]
        impl ObjectExpression {
            fn as_num(&self) -> NumberExpression {
                NumberExpression::new_expr(self.stringify().to_string(), self.meta())
            }
            fn as_str(&self) -> StringExpression {
                StringExpression::new_expr(self.stringify().to_string(), self.meta())
            }
            fn as_bool(&self) -> BooleanExpression {
                BooleanExpression::new_expr(self.stringify().to_string(), self.meta())
            }
            fn as_array(&self) -> ArrayExpression {
                ArrayExpression::new_expr(self.stringify().to_string(), self.meta())
            }
            fn to_json(&self) -> ObjectExpression {
                ObjectExpression::new_expr(format!("toJSON({})", self.stringify()), self.meta())
            }
            fn from_json_to_bool(&self) -> BooleanExpression {
                BooleanExpression::new_expr(format!("fromJSON({})", self.stringify()), self.meta())
            }
            fn from_json_to_num(&self) -> NumberExpression {
                NumberExpression::new_expr(format!("fromJSON({})", self.stringify()), self.meta())
            }
            fn from_json_to_str(&self) -> Self {
                Self::new_expr(format!("fromJSON({})", self.stringify()), self.meta())
            }
            fn from_json_to_array(&self) -> ArrayExpression {
                ArrayExpression::new_expr(format!("fromJSON({})", self.stringify()), self.meta())
            }
            fn from_json_to_obj(&self) -> ObjectExpression {
                ObjectExpression::new_expr(format!("fromJSON({})", self.stringify()), self.meta())
            }
            #[classattr]
            const __contains__: Option<Py<PyAny>> = None;
            fn __getitem__(&self, key: &str) -> ObjectExpression {
                ObjectExpression::new_expr(Self::format_access(self.stringify(), key), self.meta())
            }
            fn __getattr__(&self, key: &str) -> ObjectExpression {
                self.__getitem__(key)
            }
            fn __str__(&self) -> String {
                self.as_expression_string()
            }
        }

        #[pyclass]
        pub struct GithubContext;
        #[pymethods]
        impl GithubContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts("github", Contexts::GITHUB))
            }
            #[getter]
            fn action(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.action",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn action_path(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.action_path",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn action_ref(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.action_ref",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn action_repository(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.action_repository",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn action_status(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.action_status",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn actor(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.actor",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn actor_id(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.actor_id",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn api_url(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.api_url",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn base_ref(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.base_ref",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn env(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts("github.env", Contexts::GITHUB))
            }
            #[getter]
            fn event(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts(
                    "github.event",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn event_name(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.event_name",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn event_path(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.event_path",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn graphql_url(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.graphql_url",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn head_ref(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.head_ref",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn job(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts("github.job", Contexts::GITHUB))
            }
            #[getter]
            fn path(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.path",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn r#ref(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts("github.ref", Contexts::GITHUB))
            }
            #[getter]
            fn ref_name(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.ref_name",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn ref_protected(&self) -> BooleanExpression {
                BooleanExpression::from_base(ExprBase::with_contexts(
                    "github.ref_protected",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn ref_type(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.ref_type",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn repository(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.repository",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn reporitory_id(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.reporitory_id",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn repositor_owner(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.repositor_owner",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn repository_owner_id(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.repository_owner_id",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn repository_url(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.repositoryUrl",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn retention_days(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.retention_days",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn run_id(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.run_id",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn run_number(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.run_number",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn run_attempt(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.run_attempt",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn secret_source(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.secret_source",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn server_url(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.server_url",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn sha(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts("github.sha", Contexts::GITHUB))
            }
            #[getter]
            fn token(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.token",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn triggering_actor(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.triggering_actor",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn workflow(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.workflow",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn workflow_ref(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.workflow_ref",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn workflow_sha(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.workflow_sha",
                    Contexts::GITHUB,
                ))
            }
            #[getter]
            fn workspace(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "github.workspace",
                    Contexts::GITHUB,
                ))
            }
        }

        #[pyclass]
        pub struct EnvContext;
        #[pymethods]
        impl EnvContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts("env", Contexts::ENV))
            }
            #[classattr]
            const __contains__: Option<Py<PyAny>> = None;
            fn __getitem__(&self, key: &str) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    ObjectExpression::format_access("env", key),
                    Contexts::ENV,
                ))
            }
            fn __getattr__(&self, key: &str) -> StringExpression {
                self.__getitem__(key)
            }
        }

        #[pyclass]
        pub struct VarsContext;
        #[pymethods]
        impl VarsContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts("vars", Contexts::VARS))
            }
            #[classattr]
            const __contains__: Option<Py<PyAny>> = None;
            fn __getitem__(&self, key: &str) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    ObjectExpression::format_access("vars", key),
                    Contexts::VARS,
                ))
            }
            fn __getattr__(&self, key: &str) -> StringExpression {
                self.__getitem__(key)
            }
        }

        #[pyclass]
        pub struct JobContainerContext;
        #[pymethods]
        impl JobContainerContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts("job.container", Contexts::JOB))
            }
            #[getter]
            fn id(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "job.container.id",
                    Contexts::JOB,
                ))
            }
            #[getter]
            fn network(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "job.container.network",
                    Contexts::JOB,
                ))
            }
        }

        #[pyclass]
        pub struct JobServicesIdContext(String);
        #[pymethods]
        impl JobServicesIdContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts(self.0.clone(), Contexts::JOB))
            }
            #[getter]
            fn id(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    format!("{}.id", self.0),
                    Contexts::JOB,
                ))
            }
            #[getter]
            fn network(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    format!("{}.network", self.0),
                    Contexts::JOB,
                ))
            }
            #[getter]
            fn ports(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts(
                    format!("{}.ports", self.0),
                    Contexts::JOB,
                ))
            }
        }

        #[pyclass]
        pub struct JobServicesContext;
        #[pymethods]
        impl JobServicesContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts("job.services", Contexts::JOB))
            }
            #[classattr]
            const __contains__: Option<Py<PyAny>> = None;
            fn __getitem__(&self, key: &str) -> JobServicesIdContext {
                JobServicesIdContext(ObjectExpression::format_access("job.services", key))
            }
            fn __getattr__(&self, key: &str) -> JobServicesIdContext {
                self.__getitem__(key)
            }
        }

        #[pyclass]
        pub struct JobContext;
        #[pymethods]
        impl JobContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts("job", Contexts::JOB))
            }
            #[getter]
            fn check_run_id(&self) -> NumberExpression {
                NumberExpression::from_base(ExprBase::with_contexts(
                    "job.check_run_id",
                    Contexts::JOB,
                ))
            }
            #[getter]
            fn container(&self) -> JobContainerContext {
                JobContainerContext
            }
            #[getter]
            fn services(&self) -> JobServicesContext {
                JobServicesContext
            }
            #[getter]
            fn status(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts("job.status", Contexts::JOB))
            }
        }

        #[pyclass]
        pub struct JobsJobIdOutputsContext(String);
        #[pymethods]
        impl JobsJobIdOutputsContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts(self.0.clone(), Contexts::JOBS))
            }
            #[classattr]
            const __contains__: Option<Py<PyAny>> = None;
            fn __getitem__(&self, key: &str) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    ObjectExpression::format_access(&self.0, key),
                    Contexts::JOBS,
                ))
            }
            fn __getattr__(&self, key: &str) -> StringExpression {
                self.__getitem__(key)
            }
        }

        #[pyclass]
        pub struct JobsJobIdContext(String);
        #[pymethods]
        impl JobsJobIdContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts(self.0.clone(), Contexts::JOBS))
            }
            #[getter]
            fn result(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    format!("{}.result", self.0),
                    Contexts::JOBS,
                ))
            }
            #[getter]
            fn outputs(&self) -> JobsJobIdOutputsContext {
                JobsJobIdOutputsContext(format!("{}.outputs", self.0))
            }
        }

        #[pyclass]
        pub struct JobsContext;
        #[pymethods]
        impl JobsContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts("jobs", Contexts::JOBS))
            }
            #[classattr]
            const __contains__: Option<Py<PyAny>> = None;
            fn __getitem__(&self, key: &str) -> JobsJobIdContext {
                JobsJobIdContext(ObjectExpression::format_access("jobs", key))
            }
            fn __getattr__(&self, key: &str) -> JobsJobIdContext {
                self.__getitem__(key)
            }
        }

        #[pyclass]
        pub struct StepsStepIdOutputsContext(String);
        #[pymethods]
        impl StepsStepIdOutputsContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts(
                    self.0.clone(),
                    Contexts::STEPS,
                ))
            }
            #[classattr]
            const __contains__: Option<Py<PyAny>> = None;
            fn __getitem__(&self, key: &str) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    ObjectExpression::format_access(&self.0, key),
                    Contexts::STEPS,
                ))
            }
            fn __getattr__(&self, key: &str) -> StringExpression {
                self.__getitem__(key)
            }
        }

        #[pyclass]
        pub struct StepsStepIdContext(String);
        #[pymethods]
        impl StepsStepIdContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts(
                    self.0.clone(),
                    Contexts::STEPS,
                ))
            }
            #[getter]
            fn outputs(&self) -> StepsStepIdOutputsContext {
                StepsStepIdOutputsContext(format!("{}.outputs", self.0))
            }
            #[getter]
            fn conclusion(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    format!("{}.conclusion", self.0),
                    Contexts::STEPS,
                ))
            }
            #[getter]
            fn outcome(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    format!("{}.outcome", self.0),
                    Contexts::STEPS,
                ))
            }
        }

        #[pyclass]
        pub struct StepsContext;
        #[pymethods]
        impl StepsContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts("steps", Contexts::STEPS))
            }
            #[classattr]
            const __contains__: Option<Py<PyAny>> = None;
            fn __getitem__(&self, key: &str) -> StepsStepIdContext {
                StepsStepIdContext(ObjectExpression::format_access("steps", key))
            }
            fn __getattr__(&self, key: &str) -> StepsStepIdContext {
                self.__getitem__(key)
            }
        }

        #[pyclass]
        pub struct RunnerContext;
        #[pymethods]
        impl RunnerContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts("runner", Contexts::RUNNER))
            }
            #[getter]
            fn name(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "runner.name",
                    Contexts::RUNNER,
                ))
            }
            #[getter]
            fn os(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts("runner.os", Contexts::RUNNER))
            }
            #[getter]
            fn arch(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "runner.arch",
                    Contexts::RUNNER,
                ))
            }
            #[getter]
            fn temp(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "runner.temp",
                    Contexts::RUNNER,
                ))
            }
            #[getter]
            fn tool_cache(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "runner.tool_cache",
                    Contexts::RUNNER,
                ))
            }
            #[getter]
            fn debug(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "runner.debug",
                    Contexts::RUNNER,
                ))
            }
            #[getter]
            fn environment(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "runner.environment",
                    Contexts::RUNNER,
                ))
            }
        }

        #[pyclass]
        pub struct SecretsContext;
        #[pymethods]
        impl SecretsContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts("secrets", Contexts::SECRETS))
            }
            #[getter]
            fn github_token(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    "secrets.GITHUB_TOKEN",
                    Contexts::SECRETS,
                ))
            }
            #[classattr]
            const __contains__: Option<Py<PyAny>> = None;
            fn __getitem__(&self, key: &str) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    ObjectExpression::format_access("secrets", key),
                    Contexts::SECRETS,
                ))
            }
            fn __getattr__(&self, key: &str) -> StringExpression {
                self.__getitem__(key)
            }
        }

        #[pyclass]
        pub struct StrategyContext;
        #[pymethods]
        impl StrategyContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts("strategy", Contexts::STRATEGY))
            }
            #[getter]
            fn fail_fast(&self) -> BooleanExpression {
                BooleanExpression::from_base(ExprBase::with_contexts(
                    "strategy.fail-fast",
                    Contexts::STRATEGY,
                ))
            }
            #[getter]
            fn job_index(&self) -> NumberExpression {
                NumberExpression::from_base(ExprBase::with_contexts(
                    "strategy.job-index",
                    Contexts::STRATEGY,
                ))
            }
            #[getter]
            fn job_total(&self) -> NumberExpression {
                NumberExpression::from_base(ExprBase::with_contexts(
                    "strategy.job-total",
                    Contexts::STRATEGY,
                ))
            }
            #[getter]
            fn max_parallel(&self) -> NumberExpression {
                NumberExpression::from_base(ExprBase::with_contexts(
                    "strategy.max-parallel",
                    Contexts::STRATEGY,
                ))
            }
        }

        #[pyclass]
        pub struct MatrixContext;
        #[pymethods]
        impl MatrixContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts("matrix", Contexts::MATRIX))
            }
            #[classattr]
            const __contains__: Option<Py<PyAny>> = None;
            fn __getitem__(&self, key: &str) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts(
                    ObjectExpression::format_access("matrix", key),
                    Contexts::MATRIX,
                ))
            }
            fn __getattr__(&self, key: &str) -> ObjectExpression {
                self.__getitem__(key)
            }
        }

        #[pyclass]
        pub struct NeedsJobIdOutputsContext(String);
        #[pymethods]
        impl NeedsJobIdOutputsContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts(
                    self.0.clone(),
                    Contexts::NEEDS,
                ))
            }
            #[classattr]
            const __contains__: Option<Py<PyAny>> = None;
            fn __getitem__(&self, key: &str) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    ObjectExpression::format_access(&self.0, key),
                    Contexts::NEEDS,
                ))
            }
            fn __getattr__(&self, key: &str) -> StringExpression {
                self.__getitem__(key)
            }
        }

        #[pyclass]
        pub struct NeedsJobIdContext(String);
        #[pymethods]
        impl NeedsJobIdContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts(
                    self.0.clone(),
                    Contexts::NEEDS,
                ))
            }
            #[getter]
            fn outputs(&self) -> NeedsJobIdOutputsContext {
                NeedsJobIdOutputsContext(format!("{}.outputs", self.0))
            }
            #[getter]
            fn result(&self) -> StringExpression {
                StringExpression::from_base(ExprBase::with_contexts(
                    format!("{}.result", self.0),
                    Contexts::NEEDS,
                ))
            }
        }

        #[pyclass]
        pub struct NeedsContext;
        #[pymethods]
        impl NeedsContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts("needs", Contexts::NEEDS))
            }
            #[classattr]
            const __contains__: Option<Py<PyAny>> = None;
            fn __getitem__(&self, key: &str) -> NeedsJobIdContext {
                NeedsJobIdContext(ObjectExpression::format_access("needs", key))
            }
            fn __getattr__(&self, key: &str) -> NeedsJobIdContext {
                self.__getitem__(key)
            }
        }

        #[pyclass]
        pub struct InputsContext;
        #[pymethods]
        impl InputsContext {
            #[getter]
            fn expr(&self) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts("inputs", Contexts::INPUTS))
            }
            #[classattr]
            const __contains__: Option<Py<PyAny>> = None;
            fn __getitem__(&self, key: &str) -> ObjectExpression {
                ObjectExpression::from_base(ExprBase::with_contexts(
                    ObjectExpression::format_access("inputs", key),
                    Contexts::INPUTS,
                ))
            }
            fn __getattr__(&self, key: &str) -> ObjectExpression {
                self.__getitem__(key)
            }
        }

        #[pyclass(name = "context")]
        pub struct Context;
        #[allow(non_upper_case_globals)]
        #[pymethods]
        impl Context {
            #[classattr]
            const github: GithubContext = GithubContext;
            #[classattr]
            const env: EnvContext = EnvContext;
            #[classattr]
            const vars: VarsContext = VarsContext;
            #[classattr]
            const job: JobContext = JobContext;
            #[classattr]
            const jobs: JobsContext = JobsContext;
            #[classattr]
            const steps: StepsContext = StepsContext;
            #[classattr]
            const runner: RunnerContext = RunnerContext;
            #[classattr]
            const secrets: SecretsContext = SecretsContext;
            #[classattr]
            const strategy: StrategyContext = StrategyContext;
            #[classattr]
            const matrix: MatrixContext = MatrixContext;
            #[classattr]
            const needs: NeedsContext = NeedsContext;
            #[classattr]
            const inputs: InputsContext = InputsContext;
        }

        // TODO: Does toJSON return a string?

        fn escape_string(s: &str) -> String {
            let mut out = String::with_capacity(s.len() + 2);
            out.push('\'');
            for ch in s.chars() {
                if ch == '\'' {
                    out.push_str("''");
                } else if !push_escaped_control(&mut out, ch) {
                    out.push(ch);
                }
            }
            out.push('\'');
            out
        }

        fn validate_string(s: &str) -> bool {
            let mut chars = s.chars();
            match chars.next() {
                Some(c) if c.is_ascii_alphabetic() || c == '_' => {}
                _ => return false,
            }
            chars.all(|c| c.is_ascii_alphanumeric() || c == '_' || c == '-')
        }

        #[pyfunction]
        fn lit_str(s: &str) -> StringExpression {
            StringExpression::new_expr(escape_string(s), ExprMeta::empty())
        }

        #[pyfunction]
        fn lit_bool(b: bool) -> BooleanExpression {
            BooleanExpression::new_expr(
                if b {
                    "true".to_string()
                } else {
                    "false".to_string()
                },
                ExprMeta::empty(),
            )
        }

        #[pyfunction]
        fn lit_num(n: &Bound<PyAny>) -> PyResult<NumberExpression> {
            if n.is_instance_of::<PyFloat>() {
                Ok(NumberExpression::new_expr(
                    n.extract::<f64>()?.to_string(),
                    ExprMeta::empty(),
                ))
            } else if n.is_instance_of::<PyInt>() {
                Ok(NumberExpression::new_expr(
                    n.extract::<i64>()?.to_string(),
                    ExprMeta::empty(),
                ))
            } else {
                Err(PyValueError::new_err("Expected a number"))
            }
        }
    }

    type StringLike = Either<StringExpression, String>;
    type BoolLike = Either<BooleanExpression, bool>;
    type IntLike = Either<NumberExpression, i64>;

    macro_rules! ctx {
        ($first:ident) => {
            Contexts::$first
        };
        ($first:ident, $($rest:ident),+ $(,)?) => {
            Contexts::$first$(.union(Contexts::$rest))+
        };
    }

    macro_rules! funcs {
        ($first:ident) => {
            Funcs::$first
        };
        ($first:ident, $($rest:ident),+ $(,)?) => {
            Funcs::$first$(.union(Funcs::$rest))+
        };
    }

    const ALLOWED_WORKFLOW_RUN_NAME: Allowed =
        Allowed::new(ctx!(GITHUB, INPUTS, VARS), Funcs::NONE, "run-name");
    const ALLOWED_WORKFLOW_CONCURRENCY: Allowed =
        Allowed::new(ctx!(GITHUB, INPUTS, VARS), Funcs::NONE, "concurrency");
    const ALLOWED_WORKFLOW_ENV: Allowed =
        Allowed::new(ctx!(GITHUB, SECRETS, INPUTS, VARS), Funcs::NONE, "env");
    const ALLOWED_WORKFLOW_CALL_INPUT_DEFAULT: Allowed = Allowed::new(
        ctx!(GITHUB, INPUTS, VARS),
        Funcs::NONE,
        "on.workflow_call.inputs.<inputs_id>.default",
    );
    const ALLOWED_WORKFLOW_CALL_OUTPUT_VALUE: Allowed = Allowed::new(
        ctx!(GITHUB, JOBS, VARS, INPUTS),
        Funcs::NONE,
        "on.workflow_call.outputs.<output_id>.value",
    );

    const ALLOWED_JOB_NAME: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, STRATEGY, MATRIX, VARS, INPUTS),
        Funcs::NONE,
        "jobs.<job_id>.name",
    );
    const ALLOWED_JOB_IF: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, VARS, INPUTS),
        funcs!(ALWAYS, CANCELLED, SUCCESS, FAILURE),
        "jobs.<job_id>.if",
    );
    const ALLOWED_JOB_RUNS_ON: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, STRATEGY, MATRIX, VARS, INPUTS),
        Funcs::NONE,
        "jobs.<job_id>.runs-on",
    );
    const ALLOWED_JOB_ENV: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, STRATEGY, MATRIX, VARS, SECRETS, INPUTS),
        Funcs::NONE,
        "jobs.<job_id>.env",
    );
    const ALLOWED_JOB_ENVIRONMENT: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, STRATEGY, MATRIX, VARS, INPUTS),
        Funcs::NONE,
        "jobs.<job_id>.environment",
    );
    const ALLOWED_JOB_ENVIRONMENT_URL: Allowed = Allowed::new(
        ctx!(
            GITHUB, NEEDS, STRATEGY, MATRIX, JOB, RUNNER, ENV, VARS, STEPS, INPUTS
        ),
        Funcs::NONE,
        "jobs.<job_id>.environment.url",
    );
    const ALLOWED_JOB_CONCURRENCY: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, STRATEGY, MATRIX, INPUTS, VARS),
        Funcs::NONE,
        "jobs.<job_id>.concurrency",
    );
    const ALLOWED_JOB_OUTPUTS: Allowed = Allowed::new(
        ctx!(
            GITHUB, NEEDS, STRATEGY, MATRIX, JOB, RUNNER, ENV, VARS, SECRETS, STEPS, INPUTS
        ),
        Funcs::NONE,
        "jobs.<job_id>.outputs.<output_id>",
    );
    const ALLOWED_JOB_CONTINUE_ON_ERROR: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, STRATEGY, VARS, MATRIX, INPUTS),
        Funcs::NONE,
        "jobs.<job_id>.continue-on-error",
    );
    const ALLOWED_JOB_DEFAULTS_RUN: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, STRATEGY, MATRIX, ENV, VARS, INPUTS),
        Funcs::NONE,
        "jobs.<job_id>.defaults.run",
    );
    const ALLOWED_JOB_STRATEGY: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, VARS, INPUTS),
        Funcs::NONE,
        "jobs.<job_id>.strategy",
    );
    const ALLOWED_JOB_TIMEOUT_MINUTES: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, STRATEGY, MATRIX, VARS, INPUTS),
        Funcs::NONE,
        "jobs.<job_id>.timeout-minutes",
    );
    const ALLOWED_JOB_WITH: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, STRATEGY, MATRIX, INPUTS, VARS),
        Funcs::NONE,
        "jobs.<job_id>.with.<with_id>",
    );
    const ALLOWED_JOB_SECRETS: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, STRATEGY, MATRIX, SECRETS, INPUTS, VARS),
        Funcs::NONE,
        "jobs.<job_id>.secrets.<secrets_id>",
    );

    const ALLOWED_JOB_CONTAINER: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, STRATEGY, MATRIX, VARS, INPUTS),
        Funcs::NONE,
        "jobs.<job_id>.container",
    );
    const ALLOWED_JOB_CONTAINER_CREDENTIALS: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, STRATEGY, MATRIX, ENV, VARS, SECRETS, INPUTS),
        Funcs::NONE,
        "jobs.<job_id>.container.credentials",
    );
    const ALLOWED_JOB_CONTAINER_ENV: Allowed = Allowed::new(
        ctx!(
            GITHUB, NEEDS, STRATEGY, MATRIX, JOB, RUNNER, ENV, VARS, SECRETS, INPUTS
        ),
        Funcs::NONE,
        "jobs.<job_id>.container.env.<env_id>",
    );
    const ALLOWED_JOB_CONTAINER_IMAGE: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, STRATEGY, MATRIX, VARS, INPUTS),
        Funcs::NONE,
        "jobs.<job_id>.container.image",
    );

    const ALLOWED_JOB_SERVICES: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, STRATEGY, MATRIX, VARS, INPUTS),
        Funcs::NONE,
        "jobs.<job_id>.services",
    );
    const ALLOWED_JOB_SERVICES_CREDENTIALS: Allowed = Allowed::new(
        ctx!(GITHUB, NEEDS, STRATEGY, MATRIX, ENV, VARS, SECRETS, INPUTS),
        Funcs::NONE,
        "jobs.<job_id>.services.<service_id>.credentials",
    );
    const ALLOWED_JOB_SERVICES_ENV: Allowed = Allowed::new(
        ctx!(
            GITHUB, NEEDS, STRATEGY, MATRIX, JOB, RUNNER, ENV, VARS, SECRETS, INPUTS
        ),
        Funcs::NONE,
        "jobs.<job_id>.services.<service_id>.env.<env_id>",
    );

    const ALLOWED_STEP_IF: Allowed = Allowed::new(
        ctx!(
            GITHUB, NEEDS, STRATEGY, MATRIX, JOB, RUNNER, ENV, VARS, STEPS, INPUTS
        ),
        funcs!(ALWAYS, CANCELLED, SUCCESS, FAILURE, HASH_FILES),
        "jobs.<job_id>.steps.if",
    );
    const ALLOWED_STEP_NAME: Allowed = Allowed::new(
        ctx!(
            GITHUB, NEEDS, STRATEGY, MATRIX, JOB, RUNNER, ENV, VARS, SECRETS, STEPS, INPUTS
        ),
        Funcs::HASH_FILES,
        "jobs.<job_id>.steps.name",
    );
    const ALLOWED_STEP_RUN: Allowed = Allowed::new(
        ctx!(
            GITHUB, NEEDS, STRATEGY, MATRIX, JOB, RUNNER, ENV, VARS, SECRETS, STEPS, INPUTS
        ),
        Funcs::HASH_FILES,
        "jobs.<job_id>.steps.run",
    );
    const ALLOWED_STEP_ENV: Allowed = Allowed::new(
        ctx!(
            GITHUB, NEEDS, STRATEGY, MATRIX, JOB, RUNNER, ENV, VARS, SECRETS, STEPS, INPUTS
        ),
        Funcs::HASH_FILES,
        "jobs.<job_id>.steps.env",
    );
    const ALLOWED_STEP_WITH: Allowed = Allowed::new(
        ctx!(
            GITHUB, NEEDS, STRATEGY, MATRIX, JOB, RUNNER, ENV, VARS, SECRETS, STEPS, INPUTS
        ),
        Funcs::HASH_FILES,
        "jobs.<job_id>.steps.with",
    );
    const ALLOWED_STEP_WORKING_DIRECTORY: Allowed = Allowed::new(
        ctx!(
            GITHUB, NEEDS, STRATEGY, MATRIX, JOB, RUNNER, ENV, VARS, SECRETS, STEPS, INPUTS
        ),
        Funcs::HASH_FILES,
        "jobs.<job_id>.steps.working-directory",
    );
    const ALLOWED_STEP_CONTINUE_ON_ERROR: Allowed = Allowed::new(
        ctx!(
            GITHUB, NEEDS, STRATEGY, MATRIX, JOB, RUNNER, ENV, VARS, SECRETS, STEPS, INPUTS
        ),
        Funcs::HASH_FILES,
        "jobs.<job_id>.steps.continue-on-error",
    );
    const ALLOWED_STEP_TIMEOUT_MINUTES: Allowed = Allowed::new(
        ctx!(
            GITHUB, NEEDS, STRATEGY, MATRIX, JOB, RUNNER, ENV, VARS, SECRETS, STEPS, INPUTS
        ),
        Funcs::HASH_FILES,
        "jobs.<job_id>.steps.timeout-minutes",
    );

    fn validate_string_like(value: &StringLike, allowed: Allowed) -> PyResult<()> {
        if let Either::A(expr) = value {
            expr.validate_allowed(allowed)?;
        }
        Ok(())
    }

    fn validate_bool_like(value: &BoolLike, allowed: Allowed) -> PyResult<()> {
        if let Either::A(expr) = value {
            expr.validate_allowed(allowed)?;
        }
        Ok(())
    }

    fn validate_int_like(value: &IntLike, allowed: Allowed) -> PyResult<()> {
        if let Either::A(expr) = value {
            expr.validate_allowed(allowed)?;
        }
        Ok(())
    }

    fn validate_condition(
        value: &Either<BooleanExpression, String>,
        allowed: Allowed,
    ) -> PyResult<()> {
        if let Either::A(expr) = value {
            expr.validate_allowed(allowed)?;
        }
        Ok(())
    }

    fn validate_string_map(values: &PyMap<String, StringLike>, allowed: Allowed) -> PyResult<()> {
        for (_, value) in values.iter() {
            validate_string_like(value, allowed)?;
        }
        Ok(())
    }

    fn validate_string_vec(values: &[StringLike], allowed: Allowed) -> PyResult<()> {
        for value in values {
            validate_string_like(value, allowed)?;
        }
        Ok(())
    }

    fn validate_runs_on(runs_on: &RunsOn) -> PyResult<()> {
        match runs_on {
            RunsOn::String(value) => validate_string_like(value, ALLOWED_JOB_RUNS_ON),
            RunsOn::Array(values) => validate_string_vec(values, ALLOWED_JOB_RUNS_ON),
            RunsOn::Spec(spec) => match &spec.options {
                RunsOnSpecOptions::Group(group) => validate_string_like(group, ALLOWED_JOB_RUNS_ON),
                RunsOnSpecOptions::Labels(labels) => {
                    validate_string_like(labels, ALLOWED_JOB_RUNS_ON)
                }
                RunsOnSpecOptions::GroupAndLabels(group, labels) => {
                    validate_string_like(group, ALLOWED_JOB_RUNS_ON)?;
                    validate_string_like(labels, ALLOWED_JOB_RUNS_ON)
                }
            },
        }
    }

    fn validate_with_opts(opts: &Bound<'_, PyDict>, allowed: Allowed) -> PyResult<()> {
        for (_, value) in opts.iter() {
            if let Ok(expr) = value.extract::<BooleanExpression>() {
                expr.validate_allowed(allowed)?;
            } else if let Ok(expr) = value.extract::<StringExpression>() {
                expr.validate_allowed(allowed)?;
            } else if let Ok(expr) = value.extract::<NumberExpression>() {
                expr.validate_allowed(allowed)?;
            } else if let Ok(expr) = value.extract::<ArrayExpression>() {
                expr.validate_allowed(allowed)?;
            } else if let Ok(expr) = value.extract::<ObjectExpression>() {
                expr.validate_allowed(allowed)?;
            }
        }
        Ok(())
    }

    fn validate_step_options(
        name: Option<&StringLike>,
        condition: Option<&Either<BooleanExpression, String>>,
        working_directory: Option<&StringLike>,
        env: Option<&PyMap<String, StringLike>>,
        continue_on_error: Option<&BoolLike>,
        timeout_minutes: Option<&IntLike>,
    ) -> PyResult<()> {
        if let Some(name) = name {
            validate_string_like(name, ALLOWED_STEP_NAME)?;
        }
        if let Some(condition) = condition {
            validate_condition(condition, ALLOWED_STEP_IF)?;
        }
        if let Some(working_directory) = working_directory {
            validate_string_like(working_directory, ALLOWED_STEP_WORKING_DIRECTORY)?;
        }
        if let Some(env) = env {
            validate_string_map(env, ALLOWED_STEP_ENV)?;
        }
        if let Some(continue_on_error) = continue_on_error {
            validate_bool_like(continue_on_error, ALLOWED_STEP_CONTINUE_ON_ERROR)?;
        }
        if let Some(timeout_minutes) = timeout_minutes {
            validate_int_like(timeout_minutes, ALLOWED_STEP_TIMEOUT_MINUTES)?;
        }
        Ok(())
    }

    fn validate_container_for_job(container: &Container) -> PyResult<()> {
        validate_string_like(&container.image, ALLOWED_JOB_CONTAINER_IMAGE)?;
        if let Some(options) = &container.options {
            validate_string_like(options, ALLOWED_JOB_CONTAINER)?;
        }
        if let Some(volumes) = &container.volumes {
            validate_string_vec(volumes, ALLOWED_JOB_CONTAINER)?;
        }
        if let Some(ports) = &container.ports {
            for port in ports {
                validate_int_like(port, ALLOWED_JOB_CONTAINER)?;
            }
        }
        if let Some(credentials) = &container.credentials {
            validate_string_like(&credentials.username, ALLOWED_JOB_CONTAINER_CREDENTIALS)?;
            validate_string_like(&credentials.password, ALLOWED_JOB_CONTAINER_CREDENTIALS)?;
        }
        if let Some(env) = &container.env {
            validate_string_map(env, ALLOWED_JOB_CONTAINER_ENV)?;
        }
        Ok(())
    }

    fn validate_container_for_service(container: &Container) -> PyResult<()> {
        validate_string_like(&container.image, ALLOWED_JOB_SERVICES)?;
        if let Some(options) = &container.options {
            validate_string_like(options, ALLOWED_JOB_SERVICES)?;
        }
        if let Some(volumes) = &container.volumes {
            validate_string_vec(volumes, ALLOWED_JOB_SERVICES)?;
        }
        if let Some(ports) = &container.ports {
            for port in ports {
                validate_int_like(port, ALLOWED_JOB_SERVICES)?;
            }
        }
        if let Some(credentials) = &container.credentials {
            validate_string_like(&credentials.username, ALLOWED_JOB_SERVICES_CREDENTIALS)?;
            validate_string_like(&credentials.password, ALLOWED_JOB_SERVICES_CREDENTIALS)?;
        }
        if let Some(env) = &container.env {
            validate_string_map(env, ALLOWED_JOB_SERVICES_ENV)?;
        }
        Ok(())
    }

    fn validate_concurrency(concurrency: &Concurrency, allowed: Allowed) -> PyResult<()> {
        validate_string_like(&concurrency.group, allowed)?;
        if let Some(cancel_in_progress) = &concurrency.cancel_in_progress {
            validate_bool_like(cancel_in_progress, allowed)?;
        }
        Ok(())
    }

    fn validate_environment(environment: &Environment) -> PyResult<()> {
        validate_string_like(&environment.name, ALLOWED_JOB_ENVIRONMENT)?;
        if let Some(url) = &environment.url {
            validate_string_like(url, ALLOWED_JOB_ENVIRONMENT_URL)?;
        }
        Ok(())
    }
    impl TryYamlable for Bound<'_, PyAny> {
        fn try_as_yaml(&self) -> PyResult<Yaml> {
            if self.is_none() {
                Ok(Yaml::Null)
            } else if let Ok(e) = self.extract::<StringExpression>() {
                Ok((&e).as_yaml())
            } else if let Ok(e) = self.extract::<BooleanExpression>() {
                Ok((&e).as_yaml())
            } else if let Ok(e) = self.extract::<NumberExpression>() {
                Ok((&e).as_yaml())
            } else if self.is_instance_of::<PyBool>() {
                Ok(self.extract::<bool>()?.as_yaml())
            } else if self.is_instance_of::<PyInt>() {
                Ok(self.extract::<i64>()?.as_yaml())
            } else if self.is_instance_of::<PyFloat>() {
                Ok(self.extract::<f64>()?.as_yaml())
            } else if self.is_instance_of::<PyString>() {
                Ok(self.extract::<String>()?.as_yaml())
            } else if let Ok(list) = self.cast::<PyList>() {
                Ok(Yaml::Array(list.try_as_array()?))
            } else if let Ok(dict) = self.cast::<PyDict>() {
                Ok(Yaml::Hash(dict.try_as_hash()?))
            } else {
                Err(PyValueError::new_err("Invalid value"))
            }
        }
    }

    impl TryHash for Bound<'_, PyDict> {
        fn try_as_hash(&self) -> PyResult<Hash> {
            let mut dict_internals = Hash::new();
            for (key, entry) in self.iter() {
                if let Ok(key) = key.extract::<String>() {
                    dict_internals.insert_yaml(key, entry.try_as_yaml()?);
                } else {
                    return Err(PyValueError::new_err("Invalid key"));
                }
            }
            Ok(dict_internals)
        }
    }

    impl TryArray for Bound<'_, PyList> {
        fn try_as_array(&self) -> PyResult<Vec<Yaml>> {
            let mut list_internals = Vec::new();
            for entry in self.iter() {
                list_internals.push(entry.try_as_yaml()?);
            }
            Ok(list_internals)
        }
    }

    #[derive(Clone)]
    struct WithArgs {
        options: Option<Hash>,
        args: Option<StringLike>,
        entrypoint: Option<StringLike>,
    }

    impl Yamlable for WithArgs {
        fn as_yaml(&self) -> Yaml {
            let mut entries = self.options.clone().unwrap_or_default();
            entries.insert_yaml_opt("args", &self.args);
            entries.insert_yaml_opt("entrypoint", &self.entrypoint);
            Yaml::Hash(entries)
        }
    }

    #[derive(Clone)]
    enum StepAction {
        Run(Vec<StringLike>),
        Action {
            uses: String,
            with: Option<WithArgs>,
        },
    }
    impl StepAction {
        fn render_run_line(line: &StringLike) -> String {
            let rendered = match line {
                Either::A(expr) => expr.as_expression_string(),
                Either::B(raw) => raw.clone(),
            };
            normalize_expression_aware_string(&rendered)
        }

        fn uses(&self) -> Option<String> {
            match self {
                StepAction::Run(_) => None,
                StepAction::Action { uses, .. } => Some(uses.clone()),
            }
        }
        fn with(&self) -> Option<WithArgs> {
            match self {
                StepAction::Run(_) => None,
                StepAction::Action { with, .. } => with.clone(),
            }
        }
        fn run(&self) -> Option<Yaml> {
            match self {
                StepAction::Run(script) => {
                    let lines = script.iter().map(Self::render_run_line).collect::<Vec<_>>();
                    if lines.len() == 1 && contains_github_expression(&lines[0]) {
                        Some(Yaml::Real(lines[0].clone()))
                    } else {
                        Some(Yaml::String(lines.join("\n")))
                    }
                }
                StepAction::Action { .. } => None,
            }
        }
    }

    #[pyclass(subclass)]
    #[derive(Clone)]
    struct Step {
        name: Option<StringLike>,
        step_action: StepAction,
        options: StepOptions,
        recommended_permissions: Option<Permissions>,
        skip_recommended_permissions: bool,
    }

    #[derive(Clone)]
    struct StepOptions {
        condition: Option<Either<BooleanExpression, String>>,
        working_directory: Option<StringLike>,
        shell: Option<String>,
        id: Option<String>,
        env: Option<PyMap<String, StringLike>>,
        continue_on_error: Option<BoolLike>,
        timeout_minutes: Option<IntLike>,
    }

    #[pymethods]
    impl Step {
        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for Step {
        fn as_yaml(&self) -> Yaml {
            let mut entries = Hash::new();
            entries.insert_yaml_opt("name", &self.name);
            entries.insert_yaml_opt("if", &self.options.condition);
            entries.insert_yaml_opt("uses", self.step_action.uses());
            entries.insert_yaml_opt("with", self.step_action.with());
            entries.insert_yaml_opt("run", self.step_action.run());
            entries.insert_yaml_opt("working-directory", &self.options.working_directory);
            entries.insert_yaml_opt("shell", &self.options.shell);
            entries.insert_yaml_opt("id", &self.options.id);
            entries.insert_yaml_opt("env", &self.options.env);
            entries.insert_yaml_opt("continue-on-error", &self.options.continue_on_error);
            entries.insert_yaml_opt("timeout-minutes", &self.options.timeout_minutes);
            Yaml::Hash(entries)
        }
    }
    /// Generate a `Step` from a list of shell commands.
    ///
    /// Parameters
    /// ----------
    /// *script
    ///     A list of shell commands to run in sequence. These will be concatenated with newlines
    ///     and passed as the ``run`` key of the generated step. Note that this must not exceed
    ///     21,000 characters in total.
    /// name
    ///     The name of the step to display on GitHub.
    /// condition
    ///     A boolean expression which must be met for the step to run. Note that this represents the ``if`` key in the actual YAML file.
    /// working_directory
    ///     Specifies the directory in which the script is run.
    /// shell
    ///     Used to override the default shell settings of the runner's OS (or `Job`/`Workflow` defaults).
    /// id
    ///     A unique identifier for the step which can be referenced in expressions.
    /// env
    ///     Used to specify environment variables for the step.
    /// permissions
    ///     Recommended permissions required to run this script. These are merged into the
    ///     job permissions when ``use_recommended_permissions`` is True.
    /// continue_on_error
    ///     Prevents the job from failing if this step fails.
    /// timeout_minutes
    ///     The maximum number of minutes to let the step run before GitHub automatically cancels it (defaults to 360 if not specified).
    ///
    #[pyfunction]
    #[pyo3(signature = (*script, name = None, condition = None, working_directory = None, shell = None, id = None, env = None, permissions = None, continue_on_error = None, timeout_minutes= None))]
    fn script(
        script: &Bound<'_, PyTuple>,
        name: Option<StringLike>,
        condition: Option<Either<BooleanExpression, String>>,
        working_directory: Option<StringLike>,
        shell: Option<String>,
        id: Option<String>,
        env: Option<PyMap<String, StringLike>>,
        permissions: Option<Permissions>,
        continue_on_error: Option<BoolLike>,
        timeout_minutes: Option<IntLike>,
    ) -> PyResult<Step> {
        let script = script
            .iter()
            .map(|item| item.extract::<StringLike>())
            .collect::<PyResult<Vec<StringLike>>>()?;
        for line in &script {
            validate_string_like(line, ALLOWED_STEP_RUN)?;
        }
        validate_step_options(
            name.as_ref(),
            condition.as_ref(),
            working_directory.as_ref(),
            env.as_ref(),
            continue_on_error.as_ref(),
            timeout_minutes.as_ref(),
        )?;
        Ok(Step {
            name,
            step_action: StepAction::Run(script),
            options: StepOptions {
                condition,
                working_directory,
                shell,
                id,
                env,
                continue_on_error,
                timeout_minutes,
            },
            recommended_permissions: permissions,
            skip_recommended_permissions: false,
        })
    }
    fn make_action(
        name: Option<StringLike>,
        action: &str,
        r#ref: Option<String>,
        with_opts: Option<Hash>,
        args: Option<StringLike>,
        entrypoint: Option<StringLike>,
        condition: Option<Either<BooleanExpression, String>>,
        id: Option<String>,
        env: Option<PyMap<String, StringLike>>,
        continue_on_error: Option<BoolLike>,
        timeout_minutes: Option<IntLike>,
        skip_recommended_permissions: bool,
        recommended_permissions: Option<Permissions>,
    ) -> PyResult<Step> {
        validate_step_options(
            name.as_ref(),
            condition.as_ref(),
            None,
            env.as_ref(),
            continue_on_error.as_ref(),
            timeout_minutes.as_ref(),
        )?;
        if let Some(args) = &args {
            validate_string_like(args, ALLOWED_STEP_WITH)?;
        }
        if let Some(entrypoint) = &entrypoint {
            validate_string_like(entrypoint, ALLOWED_STEP_WITH)?;
        }
        let with_args = if with_opts.is_some() || args.is_some() || entrypoint.is_some() {
            Some(WithArgs {
                options: with_opts,
                args,
                entrypoint,
            })
        } else {
            None
        };
        Ok(Step {
            name,
            step_action: StepAction::Action {
                uses: format!(
                    "{}{}",
                    action,
                    r#ref.map(|s| format!("@{s}")).unwrap_or_default()
                ),
                with: with_args,
            },
            options: StepOptions {
                condition,
                working_directory: None,
                shell: None,
                id,
                env,
                continue_on_error,
                timeout_minutes,
            },
            recommended_permissions,
            skip_recommended_permissions,
        })
    }

    /// Generate a `Step` from a reusable unit of code called an action.
    ///
    /// Parameters
    /// ----------
    /// name
    ///     The name of the step to display on GitHub.
    /// action
    ///     The location of the action's public GitHub repository (a string of the form {owner}/{repo}).
    /// ref
    ///     The branch, ref, or SHA of the action's repository to use. This is used to specify a specific version of an action.
    /// with_opts
    ///     A map of input parameters for the action. These are passed as the ``with`` key of the generated step.
    /// args
    ///     The inputs for a Docker container which are passed to the container's entrypoint. This
    ///     is a subkey of the ``with`` key of the generated step.
    /// entrypoint
    ///     Overrides the Docker ENTRYPOINT in the action's Dockerfile or sets one if it was not
    ///     specified. Accepts a single string defining the executable to run (note that this is
    ///     different from Docker's ENTRYPOINT instruction which has both a shell and exec form).
    ///     This is a subkey of the ``with`` key of the generated step.
    /// condition
    ///     A boolean expression which must be met for the step to run. Note that this represents the ``if`` key in the actual YAML file.
    /// id
    ///     A unique identifier for the step which can be referenced in expressions.
    /// env
    ///     Used to specify environment variables for the step.
    /// continue_on_error
    ///     Prevents the job from failing if this step fails.
    /// timeout_minutes
    ///     The maximum number of minutes to let the step run before GitHub automatically cancels it (defaults to 360 if not specified).
    /// skip_recommended_permissions
    ///     If True, ignore this step's recommended permissions when merging job permissions.
    /// recommended_permissions
    ///     Recommended permissions required to run this action.
    ///
    #[pyfunction]
    #[pyo3(signature = (name, action, *, r#ref = None, with_opts = None, args = None, entrypoint = None, condition = None, id = None, env = None, continue_on_error = None, timeout_minutes = None, skip_recommended_permissions = false, recommended_permissions = None))]
    fn action(
        name: Option<StringLike>,
        action: &str,
        r#ref: Option<String>,
        with_opts: Option<Bound<PyDict>>,
        args: Option<StringLike>,
        entrypoint: Option<StringLike>,
        condition: Option<Either<BooleanExpression, String>>,
        id: Option<String>,
        env: Option<PyMap<String, StringLike>>,
        continue_on_error: Option<BoolLike>,
        timeout_minutes: Option<IntLike>,
        skip_recommended_permissions: bool,
        recommended_permissions: Option<Permissions>,
    ) -> PyResult<Step> {
        if let Some(with_opts) = &with_opts {
            validate_with_opts(with_opts, ALLOWED_STEP_WITH)?;
        }
        make_action(
            name,
            action,
            r#ref,
            with_opts.map(|d| d.try_as_hash()).transpose()?,
            args,
            entrypoint,
            condition,
            id,
            env,
            continue_on_error,
            timeout_minutes,
            skip_recommended_permissions,
            recommended_permissions,
        )
    }

    #[pyclass(extends=Step, subclass)]
    struct ActionStep;
    #[pymethods]
    impl ActionStep {
        #[new]
        #[pyo3(signature = (name, action, *, r#ref = None, with_opts = None, args = None, entrypoint = None, condition = None, id = None, env = None, continue_on_error = None, timeout_minutes = None, skip_recommended_permissions = false, recommended_permissions = None))]
        fn new(
            name: Option<StringLike>,
            action: &str,
            r#ref: Option<String>,
            with_opts: Option<Bound<PyDict>>,
            args: Option<StringLike>,
            entrypoint: Option<StringLike>,
            condition: Option<Either<BooleanExpression, String>>,
            id: Option<String>,
            env: Option<PyMap<String, StringLike>>,
            continue_on_error: Option<BoolLike>,
            timeout_minutes: Option<IntLike>,
            skip_recommended_permissions: bool,
            recommended_permissions: Option<Permissions>,
        ) -> PyResult<(Self, Step)> {
            if let Some(with_opts) = &with_opts {
                validate_with_opts(with_opts, ALLOWED_STEP_WITH)?;
            }
            let step = make_action(
                name,
                action,
                r#ref,
                with_opts.map(|d| d.try_as_hash()).transpose()?,
                args,
                entrypoint,
                condition,
                id,
                env,
                continue_on_error,
                timeout_minutes,
                skip_recommended_permissions,
                recommended_permissions,
            )?;
            Ok((ActionStep, step))
        }
    }

    #[derive(Clone, Copy)]
    enum ReadWriteNonePermission {
        Read,
        Write,
        None,
    }
    impl FromStr for ReadWriteNonePermission {
        type Err = PyErr;
        fn from_str(s: &str) -> Result<Self, Self::Err> {
            match s.to_lowercase().as_str() {
                "read" => Ok(Self::Read),
                "write" => Ok(Self::Write),
                "none" => Ok(Self::None),
                _ => Err(PyValueError::new_err("Invalid permission")),
            }
        }
    }
    impl Yamlable for &ReadWriteNonePermission {
        fn as_yaml(&self) -> Yaml {
            match self {
                ReadWriteNonePermission::Read => "read",
                ReadWriteNonePermission::Write => "write",
                ReadWriteNonePermission::None => "none",
            }
            .as_yaml()
        }
    }
    #[derive(Clone, Copy)]
    enum WriteNonePermission {
        Write,
        None,
    }
    impl FromStr for WriteNonePermission {
        type Err = PyErr;
        fn from_str(s: &str) -> Result<Self, Self::Err> {
            match s.to_lowercase().as_str() {
                "write" => Ok(Self::Write),
                "none" => Ok(Self::None),
                _ => Err(PyValueError::new_err("Invalid permission")),
            }
        }
    }
    impl Yamlable for &WriteNonePermission {
        fn as_yaml(&self) -> Yaml {
            match self {
                WriteNonePermission::Write => "write",
                WriteNonePermission::None => "none",
            }
            .as_yaml()
        }
    }
    #[derive(Clone, Copy)]
    enum ReadNonePermission {
        Read,
        None,
    }
    impl FromStr for ReadNonePermission {
        type Err = PyErr;
        fn from_str(s: &str) -> Result<Self, Self::Err> {
            match s.to_lowercase().as_str() {
                "read" => Ok(Self::Read),
                "none" => Ok(Self::None),
                _ => Err(PyValueError::new_err("Invalid permission")),
            }
        }
    }
    impl Yamlable for &ReadNonePermission {
        fn as_yaml(&self) -> Yaml {
            match self {
                ReadNonePermission::Read => "read",
                ReadNonePermission::None => "none",
            }
            .as_yaml()
        }
    }

    #[derive(Clone)]
    struct IndividualPermissions {
        actions: Option<ReadWriteNonePermission>,
        artifact_metadata: Option<ReadWriteNonePermission>,
        attestations: Option<ReadWriteNonePermission>,
        checks: Option<ReadWriteNonePermission>,
        contents: Option<ReadWriteNonePermission>,
        deployments: Option<ReadWriteNonePermission>,
        id_token: Option<WriteNonePermission>,
        issues: Option<ReadWriteNonePermission>,
        models: Option<ReadNonePermission>,
        discussions: Option<ReadWriteNonePermission>,
        packages: Option<ReadWriteNonePermission>,
        pages: Option<ReadWriteNonePermission>,
        pull_requests: Option<ReadWriteNonePermission>,
        security_events: Option<ReadWriteNonePermission>,
        statuses: Option<ReadWriteNonePermission>,
    }
    impl IndividualPermissions {
        fn is_empty(&self) -> bool {
            self.actions.is_none()
                && self.artifact_metadata.is_none()
                && self.attestations.is_none()
                && self.checks.is_none()
                && self.contents.is_none()
                && self.deployments.is_none()
                && self.id_token.is_none()
                && self.issues.is_none()
                && self.models.is_none()
                && self.discussions.is_none()
                && self.packages.is_none()
                && self.pages.is_none()
                && self.pull_requests.is_none()
                && self.security_events.is_none()
                && self.statuses.is_none()
        }
    }
    #[derive(Clone)]
    enum PermissionsOptions {
        Individual(IndividualPermissions),
        ReadAll,
        WriteAll,
        None,
    }
    #[pyclass]
    #[derive(Clone)]
    struct Permissions {
        options: PermissionsOptions,
    }
    #[pymethods]
    impl Permissions {
        #[new]
        #[pyo3(signature= (actions=None, artifact_metadata=None, attestations=None, checks=None, contents=None, deployments=None, id_token=None, issues=None, models=None, discussions=None, packages=None, pages=None, pull_requests=None, security_events=None, statuses=None))]
        fn new(
            actions: Option<String>,
            artifact_metadata: Option<String>,
            attestations: Option<String>,
            checks: Option<String>,
            contents: Option<String>,
            deployments: Option<String>,
            id_token: Option<String>,
            issues: Option<String>,
            models: Option<String>,
            discussions: Option<String>,
            packages: Option<String>,
            pages: Option<String>,
            pull_requests: Option<String>,
            security_events: Option<String>,
            statuses: Option<String>,
        ) -> PyResult<Self> {
            Ok(Self {
                options: PermissionsOptions::Individual(IndividualPermissions {
                    actions: actions.map(|s| s.parse()).transpose()?,
                    artifact_metadata: artifact_metadata.map(|s| s.parse()).transpose()?,
                    attestations: attestations.map(|s| s.parse()).transpose()?,
                    checks: checks.map(|s| s.parse()).transpose()?,
                    contents: contents.map(|s| s.parse()).transpose()?,
                    deployments: deployments.map(|s| s.parse()).transpose()?,
                    id_token: id_token.map(|s| s.parse()).transpose()?,
                    issues: issues.map(|s| s.parse()).transpose()?,
                    models: models.map(|s| s.parse()).transpose()?,
                    discussions: discussions.map(|s| s.parse()).transpose()?,
                    packages: packages.map(|s| s.parse()).transpose()?,
                    pages: pages.map(|s| s.parse()).transpose()?,
                    pull_requests: pull_requests.map(|s| s.parse()).transpose()?,
                    security_events: security_events.map(|s| s.parse()).transpose()?,
                    statuses: statuses.map(|s| s.parse()).transpose()?,
                }),
            })
        }
        #[staticmethod]
        fn none() -> Self {
            Self {
                options: PermissionsOptions::None,
            }
        }
        #[staticmethod]
        fn read_all() -> Self {
            Self {
                options: PermissionsOptions::ReadAll,
            }
        }
        #[staticmethod]
        fn write_all() -> Self {
            Self {
                options: PermissionsOptions::WriteAll,
            }
        }
        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for &Permissions {
        fn as_yaml(&self) -> Yaml {
            match &self.options {
                PermissionsOptions::Individual(indiv_perms) => {
                    let mut permissions = Hash::new();
                    permissions.insert_yaml_opt("actions", &indiv_perms.actions);
                    permissions
                        .insert_yaml_opt("artifact-metadata", &indiv_perms.artifact_metadata);
                    permissions.insert_yaml_opt("attestations", &indiv_perms.attestations);
                    permissions.insert_yaml_opt("checks", &indiv_perms.checks);
                    permissions.insert_yaml_opt("contents", &indiv_perms.contents);
                    permissions.insert_yaml_opt("deployments", &indiv_perms.deployments);
                    permissions.insert_yaml_opt("id-token", &indiv_perms.id_token);
                    permissions.insert_yaml_opt("issues", &indiv_perms.issues);
                    permissions.insert_yaml_opt("models", &indiv_perms.models);
                    permissions.insert_yaml_opt("discussion", &indiv_perms.discussions);
                    permissions.insert_yaml_opt("packages", &indiv_perms.packages);
                    permissions.insert_yaml_opt("pages", &indiv_perms.pages);
                    permissions.insert_yaml_opt("pull-requests", &indiv_perms.pull_requests);
                    permissions.insert_yaml_opt("security-events", &indiv_perms.security_events);
                    permissions.insert_yaml_opt("statuses", &indiv_perms.statuses);
                    Yaml::Hash(permissions)
                }
                PermissionsOptions::ReadAll => "read-all".as_yaml(),
                PermissionsOptions::WriteAll => "write-all".as_yaml(),
                PermissionsOptions::None => Yaml::Hash(Hash::new()), // TODO: test
            }
        }
    }

    fn max_read_write_none(
        left: ReadWriteNonePermission,
        right: ReadWriteNonePermission,
    ) -> ReadWriteNonePermission {
        match (left, right) {
            (ReadWriteNonePermission::Write, _) | (_, ReadWriteNonePermission::Write) => {
                ReadWriteNonePermission::Write
            }
            (ReadWriteNonePermission::Read, _) | (_, ReadWriteNonePermission::Read) => {
                ReadWriteNonePermission::Read
            }
            _ => ReadWriteNonePermission::None,
        }
    }
    fn max_write_none(
        left: WriteNonePermission,
        right: WriteNonePermission,
    ) -> WriteNonePermission {
        match (left, right) {
            (WriteNonePermission::Write, _) | (_, WriteNonePermission::Write) => {
                WriteNonePermission::Write
            }
            _ => WriteNonePermission::None,
        }
    }
    fn max_read_none(left: ReadNonePermission, right: ReadNonePermission) -> ReadNonePermission {
        match (left, right) {
            (ReadNonePermission::Read, _) | (_, ReadNonePermission::Read) => {
                ReadNonePermission::Read
            }
            _ => ReadNonePermission::None,
        }
    }
    fn merge_rw_opt(
        left: Option<ReadWriteNonePermission>,
        right: Option<ReadWriteNonePermission>,
    ) -> Option<ReadWriteNonePermission> {
        match (left, right) {
            (None, None) => None,
            (Some(value), None) | (None, Some(value)) => Some(value),
            (Some(left), Some(right)) => Some(max_read_write_none(left, right)),
        }
    }
    fn merge_write_opt(
        left: Option<WriteNonePermission>,
        right: Option<WriteNonePermission>,
    ) -> Option<WriteNonePermission> {
        match (left, right) {
            (None, None) => None,
            (Some(value), None) | (None, Some(value)) => Some(value),
            (Some(left), Some(right)) => Some(max_write_none(left, right)),
        }
    }
    fn merge_read_opt(
        left: Option<ReadNonePermission>,
        right: Option<ReadNonePermission>,
    ) -> Option<ReadNonePermission> {
        match (left, right) {
            (None, None) => None,
            (Some(value), None) | (None, Some(value)) => Some(value),
            (Some(left), Some(right)) => Some(max_read_none(left, right)),
        }
    }
    fn merge_individual(
        left: &IndividualPermissions,
        right: &IndividualPermissions,
    ) -> IndividualPermissions {
        IndividualPermissions {
            actions: merge_rw_opt(left.actions, right.actions),
            artifact_metadata: merge_rw_opt(left.artifact_metadata, right.artifact_metadata),
            attestations: merge_rw_opt(left.attestations, right.attestations),
            checks: merge_rw_opt(left.checks, right.checks),
            contents: merge_rw_opt(left.contents, right.contents),
            deployments: merge_rw_opt(left.deployments, right.deployments),
            id_token: merge_write_opt(left.id_token, right.id_token),
            issues: merge_rw_opt(left.issues, right.issues),
            models: merge_read_opt(left.models, right.models),
            discussions: merge_rw_opt(left.discussions, right.discussions),
            packages: merge_rw_opt(left.packages, right.packages),
            pages: merge_rw_opt(left.pages, right.pages),
            pull_requests: merge_rw_opt(left.pull_requests, right.pull_requests),
            security_events: merge_rw_opt(left.security_events, right.security_events),
            statuses: merge_rw_opt(left.statuses, right.statuses),
        }
    }
    fn individual_from_permissions(permissions: &Permissions) -> IndividualPermissions {
        match &permissions.options {
            PermissionsOptions::Individual(indiv) => indiv.clone(),
            PermissionsOptions::None => IndividualPermissions {
                actions: None,
                artifact_metadata: None,
                attestations: None,
                checks: None,
                contents: None,
                deployments: None,
                id_token: None,
                issues: None,
                models: None,
                discussions: None,
                packages: None,
                pages: None,
                pull_requests: None,
                security_events: None,
                statuses: None,
            },
            PermissionsOptions::ReadAll => IndividualPermissions {
                actions: Some(ReadWriteNonePermission::Read),
                artifact_metadata: Some(ReadWriteNonePermission::Read),
                attestations: Some(ReadWriteNonePermission::Read),
                checks: Some(ReadWriteNonePermission::Read),
                contents: Some(ReadWriteNonePermission::Read),
                deployments: Some(ReadWriteNonePermission::Read),
                id_token: Some(WriteNonePermission::None),
                issues: Some(ReadWriteNonePermission::Read),
                models: Some(ReadNonePermission::Read),
                discussions: Some(ReadWriteNonePermission::Read),
                packages: Some(ReadWriteNonePermission::Read),
                pages: Some(ReadWriteNonePermission::Read),
                pull_requests: Some(ReadWriteNonePermission::Read),
                security_events: Some(ReadWriteNonePermission::Read),
                statuses: Some(ReadWriteNonePermission::Read),
            },
            PermissionsOptions::WriteAll => IndividualPermissions {
                actions: Some(ReadWriteNonePermission::Write),
                artifact_metadata: Some(ReadWriteNonePermission::Write),
                attestations: Some(ReadWriteNonePermission::Write),
                checks: Some(ReadWriteNonePermission::Write),
                contents: Some(ReadWriteNonePermission::Write),
                deployments: Some(ReadWriteNonePermission::Write),
                id_token: Some(WriteNonePermission::Write),
                issues: Some(ReadWriteNonePermission::Write),
                models: Some(ReadNonePermission::Read),
                discussions: Some(ReadWriteNonePermission::Write),
                packages: Some(ReadWriteNonePermission::Write),
                pages: Some(ReadWriteNonePermission::Write),
                pull_requests: Some(ReadWriteNonePermission::Write),
                security_events: Some(ReadWriteNonePermission::Write),
                statuses: Some(ReadWriteNonePermission::Write),
            },
        }
    }
    fn merge_permissions(left: &Permissions, right: &Permissions) -> Permissions {
        match (&left.options, &right.options) {
            (PermissionsOptions::WriteAll, _) | (_, PermissionsOptions::WriteAll) => Permissions {
                options: PermissionsOptions::WriteAll,
            },
            (PermissionsOptions::None, PermissionsOptions::None) => Permissions {
                options: PermissionsOptions::None,
            },
            (
                PermissionsOptions::ReadAll,
                PermissionsOptions::None | PermissionsOptions::ReadAll,
            )
            | (PermissionsOptions::None, PermissionsOptions::ReadAll) => Permissions {
                options: PermissionsOptions::ReadAll,
            },
            _ => Permissions {
                options: PermissionsOptions::Individual(merge_individual(
                    &individual_from_permissions(left),
                    &individual_from_permissions(right),
                )),
            },
        }
    }
    fn is_empty_individual_permissions(permissions: &Permissions) -> bool {
        match &permissions.options {
            PermissionsOptions::Individual(indiv) => indiv.is_empty(),
            _ => false,
        }
    }

    #[derive(Clone)]
    enum RunsOnSpecOptions {
        Group(StringLike),
        Labels(StringLike),
        GroupAndLabels(StringLike, StringLike),
    }
    #[pyclass]
    #[derive(Clone)]
    struct RunsOnSpec {
        options: RunsOnSpecOptions,
    }
    #[pymethods]
    impl RunsOnSpec {
        #[new]
        fn new(group: StringLike, labels: StringLike) -> Self {
            Self {
                options: RunsOnSpecOptions::GroupAndLabels(group, labels),
            }
        }
        #[staticmethod]
        fn group(group: StringLike) -> Self {
            Self {
                options: RunsOnSpecOptions::Group(group),
            }
        }
        #[staticmethod]
        fn labels(labels: StringLike) -> Self {
            Self {
                options: RunsOnSpecOptions::Labels(labels),
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for &RunsOnSpec {
        fn as_yaml(&self) -> Yaml {
            let mut out = Hash::new();
            match &self.options {
                RunsOnSpecOptions::Group(group) => out.insert_yaml("group", group),
                RunsOnSpecOptions::Labels(labels) => out.insert_yaml("labels", labels),
                RunsOnSpecOptions::GroupAndLabels(group, labels) => {
                    out.insert_yaml("group", group);
                    out.insert_yaml("labels", labels);
                }
            }
            Yaml::Hash(out)
        }
    }

    #[derive(Clone)]
    enum RunsOn {
        String(StringLike),
        Array(Vec<StringLike>),
        Spec(RunsOnSpec),
    }
    impl<'a, 'py> FromPyObject<'a, 'py> for RunsOn {
        type Error = PyErr;

        fn extract(obj: Borrowed<'a, 'py, PyAny>) -> Result<Self, Self::Error> {
            if let Ok(spec) = obj.extract::<RunsOnSpec>() {
                Ok(Self::Spec(spec))
            } else if let Ok(list) = obj.extract::<Vec<StringLike>>() {
                Ok(Self::Array(list))
            } else if let Ok(single) = obj.extract::<StringLike>() {
                Ok(Self::String(single))
            } else {
                Err(PyValueError::new_err(
                    "Expected a 'RunsOnSpec', list of strings, or a single string",
                ))
            }
        }
    }
    impl Yamlable for &RunsOn {
        fn as_yaml(&self) -> Yaml {
            match self {
                RunsOn::String(s) => s.as_yaml(),
                RunsOn::Array(l) => l.as_yaml(),
                RunsOn::Spec(spec) => spec.as_yaml(),
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct Environment {
        name: StringLike,
        url: Option<StringLike>,
    }
    #[pymethods]
    impl Environment {
        #[new]
        #[pyo3(signature = (name, url = None))]
        fn new(name: StringLike, url: Option<StringLike>) -> Self {
            Self { name, url }
        }

        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for &Environment {
        fn as_yaml(&self) -> Yaml {
            if let Some(url) = &self.url {
                let mut sub = Hash::new();
                sub.insert_yaml("name", &self.name);
                sub.insert_yaml("url", url);
                Yaml::Hash(sub)
            } else {
                self.name.as_yaml()
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct Concurrency {
        group: StringLike,
        cancel_in_progress: Option<BoolLike>,
    }
    #[pymethods]
    impl Concurrency {
        #[new]
        #[pyo3(signature = (group, *, cancel_in_progress=None))]
        fn new(group: StringLike, cancel_in_progress: Option<BoolLike>) -> Self {
            Self {
                group,
                cancel_in_progress,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for &Concurrency {
        fn as_yaml(&self) -> Yaml {
            let mut out = Hash::new();
            out.insert_yaml("group", &self.group);
            out.insert_yaml_opt("cancel-in-progress", &self.cancel_in_progress);
            Yaml::Hash(out)
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct RunDefaults {
        shell: Option<StringLike>,
        working_directory: Option<StringLike>,
    }
    #[pymethods]
    impl RunDefaults {
        #[new]
        #[pyo3(signature = (*, shell=None, working_directory=None))]
        fn new(shell: Option<StringLike>, working_directory: Option<StringLike>) -> Self {
            Self {
                shell,
                working_directory,
            }
        }
    }
    impl MaybeYamlable for &RunDefaults {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            let mut out = Hash::new();
            out.insert_yaml_opt("shell", &self.shell);
            out.insert_yaml_opt("working-directory", &self.working_directory);
            if out.is_empty() {
                None
            } else {
                Some(Yaml::Hash(out))
            }
        }
    }
    #[pyclass]
    #[derive(Clone)]
    struct Defaults {
        defaults: Option<PyMap<String, String>>,
        run_defaults: Option<RunDefaults>,
    }
    #[pymethods]
    impl Defaults {
        #[new]
        #[pyo3(signature = (*, defaults=None, run_defaults=None))]
        fn new(defaults: Option<PyMap<String, String>>, run_defaults: Option<RunDefaults>) -> Self {
            Self {
                defaults,
                run_defaults,
            }
        }
    }
    impl MaybeYamlable for &Defaults {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            let mut out = Hash::new();
            if let Some(run_defaults) = &self.run_defaults {
                out.insert_yaml_opt("run", run_defaults.maybe_as_yaml());
            }
            out.insert_yaml_opt("defaults", &self.defaults);
            if out.is_empty() {
                None
            } else {
                Some(Yaml::Hash(out))
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct Matrix {
        matrix: Option<Hash>,
        include: Option<Array>,
        exclude: Option<Array>,
    }
    #[pymethods]
    impl Matrix {
        #[new]
        #[pyo3(signature = (*, include = None, exclude = None, **matrix))]
        fn new(
            include: Option<&Bound<'_, PyList>>,
            exclude: Option<&Bound<'_, PyList>>,
            matrix: Option<&Bound<'_, PyDict>>,
        ) -> PyResult<Self> {
            Ok(Self {
                matrix: matrix
                    .map(|m| {
                        let mut hash = Hash::new();
                        for (k, v) in m.iter() {
                            hash.insert_yaml(k.try_as_yaml()?, v.try_as_yaml()?);
                        }
                        Ok::<Hash, PyErr>(hash)
                    })
                    .transpose()?,
                include: include
                    .map(|i| {
                        let mut arr = Array::new();
                        for v in i.iter() {
                            arr.push_yaml(v.try_as_yaml()?);
                        }
                        Ok::<Array, PyErr>(arr)
                    })
                    .transpose()?,
                exclude: exclude
                    .map(|e| {
                        let mut arr = Array::new();
                        for v in e.iter() {
                            arr.push_yaml(v.try_as_yaml()?);
                        }
                        Ok::<Array, PyErr>(arr)
                    })
                    .transpose()?,
            })
        }

        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for &Matrix {
        fn as_yaml(&self) -> Yaml {
            let mut matrix = self.matrix.clone().unwrap_or_default();
            matrix.insert_yaml_opt("include", &self.include);
            matrix.insert_yaml_opt("exclude", &self.exclude);
            Yaml::Hash(matrix)
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct Strategy {
        matrix: Option<Matrix>,
        fast_fail: Option<BoolLike>,
        max_parallel: Option<IntLike>,
    }
    #[pymethods]
    impl Strategy {
        #[new]
        #[pyo3(signature = (*, matrix = None, fast_fail = None, max_parallel = None))]
        fn new(
            // TODO: prevent invalid state where all are None
            matrix: Option<Matrix>,
            fast_fail: Option<BoolLike>,
            max_parallel: Option<IntLike>,
        ) -> Self {
            Self {
                matrix,
                fast_fail,
                max_parallel,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for &Strategy {
        fn as_yaml(&self) -> Yaml {
            let mut strategy = Hash::new();
            strategy.insert_yaml_opt("matrix", &self.matrix);
            strategy.insert_yaml_opt("fail-fast", &self.fast_fail);
            strategy.insert_yaml_opt("max-parallel", &self.max_parallel);
            Yaml::Hash(strategy)
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct Credentials {
        username: StringLike,
        password: StringLike,
    }
    #[pymethods]
    impl Credentials {
        #[new]
        fn new(username: StringLike, password: StringLike) -> Self {
            Self { username, password }
        }

        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for &Credentials {
        fn as_yaml(&self) -> Yaml {
            let mut out = Hash::new();
            out.insert_yaml("username", &self.username);
            out.insert_yaml("password", &self.password);
            Yaml::Hash(out)
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct Container {
        image: StringLike,
        credentials: Option<Credentials>,
        env: Option<PyMap<String, StringLike>>,
        ports: Option<Vec<IntLike>>,
        volumes: Option<Vec<StringLike>>,
        options: Option<StringLike>,
    }
    #[pymethods]
    impl Container {
        #[new]
        #[pyo3(signature = (image, *, credentials = None, env = None, ports = None, volumes = None, options = None))]
        fn new(
            image: StringLike,
            credentials: Option<Credentials>,
            env: Option<PyMap<String, StringLike>>,
            ports: Option<Vec<IntLike>>,
            volumes: Option<Vec<StringLike>>,
            options: Option<StringLike>,
        ) -> Self {
            Self {
                image,
                credentials,
                env,
                ports,
                volumes,
                options,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for &Container {
        fn as_yaml(&self) -> Yaml {
            let mut out = Hash::new();
            out.insert_yaml("image", &self.image);
            out.insert_yaml_opt("credentials", &self.credentials);
            out.insert_yaml_opt("env", &self.env);
            out.insert_yaml_opt("ports", &self.ports);
            out.insert_yaml_opt("volumes", &self.volumes);
            out.insert_yaml_opt("options", &self.options);
            Yaml::Hash(out)
        }
    }

    #[derive(Clone)]
    enum JobSecretsOptions {
        Secrets(HashMap<String, StringLike>),
        Inherit,
    }
    #[pyclass]
    #[derive(Clone)]
    struct JobSecrets {
        options: JobSecretsOptions,
    }
    #[pymethods]
    impl JobSecrets {
        #[new]
        fn new(secrets: HashMap<String, StringLike>) -> Self {
            Self {
                options: JobSecretsOptions::Secrets(secrets),
            }
        }
        #[staticmethod]
        fn inherit() -> Self {
            Self {
                options: JobSecretsOptions::Inherit,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for &JobSecrets {
        fn as_yaml(&self) -> Yaml {
            match &self.options {
                JobSecretsOptions::Secrets(s) => {
                    let mut hash = Hash::new();
                    for (k, v) in s {
                        hash.insert_yaml(k, v);
                    }
                    Yaml::Hash(hash)
                }
                JobSecretsOptions::Inherit => Yaml::String("inherit".to_string()),
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct Job {
        name: Option<StringLike>,
        permissions: Option<Permissions>,
        needs: Option<Vec<String>>,
        condition: Option<Either<BooleanExpression, String>>,
        runs_on: Option<RunsOn>,
        snapshot: Option<String>,
        environment: Option<Environment>,
        concurrency: Option<Concurrency>,
        outputs: Option<PyMap<String, StringLike>>,
        env: Option<PyMap<String, StringLike>>,
        defaults: Option<Defaults>,
        steps: Option<Vec<Step>>,
        timeout_minutes: Option<IntLike>,
        strategy: Option<Strategy>,
        continue_on_error: Option<Either<StringLike, BoolLike>>,
        container: Option<Container>,
        services: Option<PyMap<String, Container>>,
        uses: Option<String>,
        with: Option<Hash>,
        secrets: Option<JobSecrets>,
    }
    // TODO: support mapping syntax for snapshot argument
    #[pymethods]
    impl Job {
        /// A set of `Step`s which runs in an isolated environemnt.
        ///
        /// All `Job`s in a `Workflow` run in parallel by default, but dependencies can be created
        /// with the ``needs`` argument. `Job`s may also specify the ``uses`` argument to call
        /// another reusable workflow rather than a set of `Step`s. Note that exactly one of ``runs_on`` or ``uses`` must be specified, and a `Job` which specifies ``uses`` may not have any ``steps``.
        ///
        /// Parameters
        /// ----------
        /// steps
        ///     The set of `Step`s to run sequentially.
        /// name
        ///     The name of the job displayed in the GitHub UI.
        /// permissions
        ///     The permissions granted to the ``GITHUB_TOKEN`` for this job.
        /// use_recommended_permissions
        ///     Merge recommended permissions from steps into this job's permissions.
        /// needs
        ///     A list of `Job`s which must complete successfully before this job will run.
        /// condition
        ///     A condition which must be met for this job to run. Note that this represents the ``if`` key in the actual YAML file.
        /// runs_on
        ///     The type of machine on which the job will run (e.g. ``'ubuntu-latest'``)
        /// snapshot
        ///     Used to generate a custom image.
        /// environment
        ///     Used to define the environment which the job references. This is often used for trusted publishing.
        /// concurrency
        ///     The concurrency group for this job. Only a single `Job` or `Workflow` using the
        ///     same concurrency group will run at a time.
        /// outputs
        ///     Used to create a set of outputs available to all downstream jobs which depend on this job.
        /// env
        ///     A map of environment variables available to all steps in the job.
        /// defaults
        ///     A map of default settings which apply to all steps in the job.
        /// timeout_minutes
        ///     The maximum number of minutes to let a job run before GitHub automatically cancels it (defaults to 360 if not specified).
        /// strategy
        ///     Used to create a matrix strategy for a job, generating multiple jobs from a single one based on combinations of matrix variables.
        /// continue_on_error
        ///     If True, this job's failure will not trigger workflow failure (or cause other matrix strategy jobs to fail if ``fail-fast`` is enabled).
        /// container
        ///     Used to create a container to run any steps of a job which do not already specify one.
        /// services
        ///     Used to host service containers for a job.
        /// uses
        ///     Used to specify the location and version of a reusable workflow file to run as a
        ///     job. Such a job will not specify ``runs_on`` or ``steps``.
        /// with_opts
        ///     A map of inputs which are passed to a reusable workflow job specified by ``uses``. Note that this represents the ``with`` key in the actual YAML file.
        /// secrets
        ///     A map of secrets passed to a resulable workflow job specified by ``uses``.
        #[new]
        #[pyo3(signature = (*, steps=None, name=None, permissions=None, use_recommended_permissions=true, needs=None, condition=None, runs_on=None, snapshot=None, environment=None, concurrency=None, outputs=None, env=None, defaults=None, timeout_minutes=None, strategy=None, continue_on_error=None, container=None, services=None, uses=None, with_opts=None, secrets=None))]
        fn new(
            steps: Option<Vec<Step>>,
            name: Option<StringLike>,
            permissions: Option<Permissions>,
            use_recommended_permissions: bool,
            needs: Option<Vec<String>>,
            condition: Option<Either<BooleanExpression, String>>,
            runs_on: Option<RunsOn>,
            snapshot: Option<String>,
            environment: Option<Environment>,
            concurrency: Option<Concurrency>,
            outputs: Option<PyMap<String, StringLike>>,
            env: Option<PyMap<String, StringLike>>,
            defaults: Option<Defaults>,
            timeout_minutes: Option<IntLike>,
            strategy: Option<Strategy>,
            continue_on_error: Option<Either<StringLike, BoolLike>>,
            container: Option<Container>,
            services: Option<PyMap<String, Container>>,
            uses: Option<String>,
            with_opts: Option<Bound<PyDict>>,
            secrets: Option<JobSecrets>,
        ) -> PyResult<Self> {
            match (&uses, &runs_on) {
                (Some(_), Some(_)) => {
                    return Err(PyValueError::new_err(
                        "Job cannot set both 'uses' and 'runs_on'",
                    ));
                }
                (None, None) => {
                    return Err(PyValueError::new_err(
                        "Job must set either 'uses' or 'runs_on'",
                    ));
                }
                _ => {}
            }
            if uses.is_some() {
                if let Some(steps) = &steps
                    && !steps.is_empty()
                {
                    return Err(PyValueError::new_err(
                        "Job using 'uses' cannot define 'steps'",
                    ));
                }
            } else {
                match &steps {
                    Some(steps) if !steps.is_empty() => {}
                    _ => {
                        return Err(PyValueError::new_err(
                            "Job with 'runs_on' must define at least one step",
                        ));
                    }
                }
            }
            if let Some(name) = &name {
                validate_string_like(name, ALLOWED_JOB_NAME)?;
            }
            if let Some(condition) = &condition {
                validate_condition(condition, ALLOWED_JOB_IF)?;
            }
            if let Some(runs_on) = &runs_on {
                validate_runs_on(runs_on)?;
            }
            if let Some(environment) = &environment {
                validate_environment(environment)?;
            }
            if let Some(concurrency) = &concurrency {
                validate_concurrency(concurrency, ALLOWED_JOB_CONCURRENCY)?;
            }
            if let Some(outputs) = &outputs {
                validate_string_map(outputs, ALLOWED_JOB_OUTPUTS)?;
            }
            if let Some(env) = &env {
                validate_string_map(env, ALLOWED_JOB_ENV)?;
            }
            if let Some(defaults) = &defaults
                && let Some(run_defaults) = &defaults.run_defaults
            {
                if let Some(shell) = &run_defaults.shell {
                    validate_string_like(shell, ALLOWED_JOB_DEFAULTS_RUN)?;
                }
                if let Some(working_directory) = &run_defaults.working_directory {
                    validate_string_like(working_directory, ALLOWED_JOB_DEFAULTS_RUN)?;
                }
            }
            if let Some(strategy) = &strategy {
                if let Some(fast_fail) = &strategy.fast_fail {
                    validate_bool_like(fast_fail, ALLOWED_JOB_STRATEGY)?;
                }
                if let Some(max_parallel) = &strategy.max_parallel {
                    validate_int_like(max_parallel, ALLOWED_JOB_STRATEGY)?;
                }
            }
            if let Some(timeout_minutes) = &timeout_minutes {
                validate_int_like(timeout_minutes, ALLOWED_JOB_TIMEOUT_MINUTES)?;
            }
            if let Some(continue_on_error) = &continue_on_error {
                match continue_on_error {
                    Either::A(string_like) => {
                        validate_string_like(string_like, ALLOWED_JOB_CONTINUE_ON_ERROR)?;
                    }
                    Either::B(bool_like) => {
                        validate_bool_like(bool_like, ALLOWED_JOB_CONTINUE_ON_ERROR)?;
                    }
                }
            }
            if let Some(container) = &container {
                validate_container_for_job(container)?;
            }
            if let Some(services) = &services {
                for (_, container) in services.iter() {
                    validate_container_for_service(container)?;
                }
            }
            if let Some(with_opts) = &with_opts {
                validate_with_opts(with_opts, ALLOWED_JOB_WITH)?;
            }
            if let Some(secrets) = &secrets
                && let JobSecretsOptions::Secrets(values) = &secrets.options
            {
                for value in values.values() {
                    validate_string_like(value, ALLOWED_JOB_SECRETS)?;
                }
            }
            let mut permissions = permissions;
            if use_recommended_permissions && let Some(steps) = &steps {
                let mut saw_recommendation = false;
                let mut merged: Option<Permissions> = None;
                for step in steps {
                    if step.skip_recommended_permissions {
                        continue;
                    }
                    if let Some(step_permissions) = &step.recommended_permissions {
                        saw_recommendation = true;
                        merged = Some(match &merged {
                            Some(current) => merge_permissions(current, step_permissions),
                            None => step_permissions.clone(),
                        });
                    }
                }
                if saw_recommendation {
                    let mut merged = merged.unwrap_or_else(Permissions::none);
                    if is_empty_individual_permissions(&merged) {
                        merged = Permissions::none();
                    }
                    permissions = Some(match permissions {
                        Some(current) => merge_permissions(&current, &merged),
                        None => merged,
                    });
                }
            }
            Ok(Self {
                name,
                permissions,
                needs,
                condition,
                runs_on,
                snapshot,
                environment,
                concurrency,
                outputs,
                env,
                defaults,
                steps,
                timeout_minutes,
                strategy,
                continue_on_error,
                container,
                services,
                uses,
                with: with_opts.map(|w| w.try_as_hash()).transpose()?,
                secrets,
            })
        }
        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for &Job {
        fn as_yaml(&self) -> Yaml {
            let mut out = Hash::new();
            out.insert_yaml_opt("name", &self.name);
            out.insert_yaml_opt("permissions", self.permissions.as_ref());
            out.insert_yaml_opt("needs", &self.needs);
            out.insert_yaml_opt("if", &self.condition);
            out.insert_yaml_opt("runs-on", &self.runs_on);
            out.insert_yaml_opt("snapshot", &self.snapshot);
            out.insert_yaml_opt("environment", &self.environment);
            out.insert_yaml_opt("concurrency", &self.concurrency);
            out.insert_yaml_opt("outputs", &self.outputs);
            out.insert_yaml_opt("env", &self.env);
            if let Some(defaults) = &self.defaults {
                out.insert_yaml_opt("defaults", defaults.maybe_as_yaml());
            }
            out.insert_yaml_opt("strategy", &self.strategy);
            out.insert_yaml_opt("steps", &self.steps);
            out.insert_yaml_opt("timeout-minutes", &self.timeout_minutes);
            out.insert_yaml_opt("continue-on-error", &self.continue_on_error);
            out.insert_yaml_opt("container", &self.container);
            out.insert_yaml_opt("services", &self.services);
            out.insert_yaml_opt("uses", &self.uses);
            out.insert_yaml_opt("with", self.with.clone().map(Yaml::Hash));
            out.insert_yaml_opt("secrets", &self.secrets);
            Yaml::Hash(out)
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct BranchProtectionRuleEvent {
        created: bool,
        edited: bool,
        deleted: bool,
    }
    #[pymethods]
    impl BranchProtectionRuleEvent {
        #[new]
        #[pyo3(signature = (*, created=false, edited=false, deleted=false))]
        fn new(created: bool, edited: bool, deleted: bool) -> Self {
            Self {
                created,
                edited,
                deleted,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &BranchProtectionRuleEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.created || self.edited || self.deleted {
                let mut out = Hash::new();
                let mut arr = Array::new();
                arr.push_yaml_cond("created", self.created);
                arr.push_yaml_cond("edited", self.edited);
                arr.push_yaml_cond("deleted", self.deleted);
                out.insert_yaml("types", Yaml::Array(arr));
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct CheckRunEvent {
        created: bool,
        rerequested: bool,
        completed: bool,
        requested_action: bool,
    }
    #[pymethods]
    impl CheckRunEvent {
        #[new]
        #[pyo3(signature = (*, created=false, rerequested=false, completed=false, requested_action=false))]
        fn new(created: bool, rerequested: bool, completed: bool, requested_action: bool) -> Self {
            Self {
                created,
                rerequested,
                completed,
                requested_action,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &CheckRunEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.created || self.rerequested || self.completed || self.requested_action {
                let mut out = Hash::new();
                let mut arr = Array::new();
                arr.push_yaml_cond("created", self.created);
                arr.push_yaml_cond("rerequested", self.rerequested);
                arr.push_yaml_cond("completed", self.completed);
                arr.push_yaml_cond("requested_action", self.requested_action);
                out.insert_yaml("types", Yaml::Array(arr));
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct CheckSuiteEvent {
        created: bool,
    }
    #[pymethods]
    impl CheckSuiteEvent {
        #[new]
        #[pyo3(signature = (*, created=false))]
        fn new(created: bool) -> Self {
            Self { created }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &CheckSuiteEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.created {
                let mut out = Hash::new();
                let mut arr = Array::new();
                arr.push_yaml_cond("created", self.created);
                out.insert_yaml("types", Yaml::Array(arr));
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct DiscussionEvent {
        created: bool,
        edited: bool,
        deleted: bool,
        transferred: bool,
        pinned: bool,
        unpinned: bool,
        labeled: bool,
        unlabeled: bool,
        locked: bool,
        unlocked: bool,
        category_changed: bool,
        answered: bool,
        unanswered: bool,
    }
    #[pymethods]
    impl DiscussionEvent {
        #[new]
        #[pyo3(signature = (*, created=false, edited=false, deleted=false, transferred=false, pinned=false, unpinned=false, labeled=false, unlabeled=false, locked=false, unlocked=false, category_changed=false, answered=false, unanswered=false))]
        fn new(
            created: bool,
            edited: bool,
            deleted: bool,
            transferred: bool,
            pinned: bool,
            unpinned: bool,
            labeled: bool,
            unlabeled: bool,
            locked: bool,
            unlocked: bool,
            category_changed: bool,
            answered: bool,
            unanswered: bool,
        ) -> Self {
            Self {
                created,
                edited,
                deleted,
                transferred,
                pinned,
                unpinned,
                labeled,
                unlabeled,
                locked,
                unlocked,
                category_changed,
                answered,
                unanswered,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &DiscussionEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.created
                || self.edited
                || self.deleted
                || self.transferred
                || self.pinned
                || self.unpinned
                || self.labeled
                || self.unlabeled
                || self.locked
                || self.unlocked
                || self.category_changed
                || self.answered
                || self.unanswered
            {
                let mut out = Hash::new();
                let mut arr = Array::new();
                arr.push_yaml_cond("created", self.created);
                arr.push_yaml_cond("edited", self.edited);
                arr.push_yaml_cond("deleted", self.deleted);
                arr.push_yaml_cond("transferred", self.transferred);
                arr.push_yaml_cond("pinned", self.pinned);
                arr.push_yaml_cond("unpinned", self.unpinned);
                arr.push_yaml_cond("labeled", self.labeled);
                arr.push_yaml_cond("unlabeled", self.unlabeled);
                arr.push_yaml_cond("locked", self.locked);
                arr.push_yaml_cond("unlocked", self.unlocked);
                arr.push_yaml_cond("category_changed", self.category_changed);
                arr.push_yaml_cond("answered", self.answered);
                arr.push_yaml_cond("unanswered", self.unanswered);
                out.insert_yaml("types", Yaml::Array(arr));
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct DiscussionCommentEvent {
        created: bool,
        edited: bool,
        deleted: bool,
    }
    #[pymethods]
    impl DiscussionCommentEvent {
        #[new]
        #[pyo3(signature = (*, created=false, edited=false, deleted=false))]
        fn new(created: bool, edited: bool, deleted: bool) -> Self {
            Self {
                created,
                edited,
                deleted,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &DiscussionCommentEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.created || self.edited || self.deleted {
                let mut out = Hash::new();
                let mut arr = Array::new();
                arr.push_yaml_cond("created", self.created);
                arr.push_yaml_cond("edited", self.edited);
                arr.push_yaml_cond("deleted", self.deleted);
                out.insert_yaml("types", Yaml::Array(arr));
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct ImageVersionEvent {
        names: Option<Vec<String>>,
        versions: Option<Vec<String>>,
    }
    #[pymethods]
    impl ImageVersionEvent {
        #[new]
        #[pyo3(signature = (*, names=None, versions=None))]
        fn new(names: Option<Vec<String>>, versions: Option<Vec<String>>) -> Self {
            let names = names.filter(|v| !v.is_empty());
            let versions = versions.filter(|v| !v.is_empty());
            Self { names, versions }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &ImageVersionEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.names.is_some() || self.versions.is_some() {
                let mut out = Hash::new();
                out.insert_yaml_opt("names", self.names.as_ref());
                out.insert_yaml_opt("versions", self.versions.as_ref());
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct IssueCommentEvent {
        created: bool,
        edited: bool,
        deleted: bool,
    }
    #[pymethods]
    impl IssueCommentEvent {
        #[new]
        #[pyo3(signature = (*, created=false, edited=false, deleted=false))]
        fn new(created: bool, edited: bool, deleted: bool) -> Self {
            Self {
                created,
                edited,
                deleted,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &IssueCommentEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.created || self.edited || self.deleted {
                let mut out = Hash::new();
                let mut arr = Array::new();
                arr.push_yaml_cond("created", self.created);
                arr.push_yaml_cond("edited", self.edited);
                arr.push_yaml_cond("deleted", self.deleted);
                out.insert_yaml("types", Yaml::Array(arr));
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct IssuesEvent {
        created: bool,
        edited: bool,
        deleted: bool,
        transferred: bool,
        pinned: bool,
        unpinned: bool,
        closed: bool,
        reopened: bool,
        assigned: bool,
        unassigned: bool,
        labeled: bool,
        unlabeled: bool,
        locked: bool,
        unlocked: bool,
        milestoned: bool,
        demilestoned: bool,
        typed: bool,
        untyped: bool,
    }
    #[pymethods]
    impl IssuesEvent {
        #[new]
        #[pyo3(signature = (*, created=false, edited=false, deleted=false,  transferred=false, pinned=false, unpinned=false, closed=false, reopened=false, assigned=false, unassigned=false, labeled=false, unlabeled=false, locked=false, unlocked=false, milestoned=false, demilestoned=false, typed=false, untyped=false))]
        fn new(
            created: bool,
            edited: bool,
            deleted: bool,
            transferred: bool,
            pinned: bool,
            unpinned: bool,
            closed: bool,
            reopened: bool,
            assigned: bool,
            unassigned: bool,
            labeled: bool,
            unlabeled: bool,
            locked: bool,
            unlocked: bool,
            milestoned: bool,
            demilestoned: bool,
            typed: bool,
            untyped: bool,
        ) -> Self {
            Self {
                created,
                edited,
                deleted,
                transferred,
                pinned,
                unpinned,
                closed,
                reopened,
                assigned,
                unassigned,
                labeled,
                unlabeled,
                locked,
                unlocked,
                milestoned,
                demilestoned,
                typed,
                untyped,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &IssuesEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.created
                || self.edited
                || self.deleted
                || self.transferred
                || self.pinned
                || self.unpinned
                || self.closed
                || self.reopened
                || self.assigned
                || self.unassigned
                || self.labeled
                || self.unlabeled
                || self.locked
                || self.unlocked
                || self.milestoned
                || self.demilestoned
                || self.typed
                || self.untyped
            {
                let mut out = Hash::new();
                let mut arr = Array::new();
                arr.push_yaml_cond("created", self.created);
                arr.push_yaml_cond("edited", self.edited);
                arr.push_yaml_cond("deleted", self.deleted);
                arr.push_yaml_cond("transferred", self.transferred);
                arr.push_yaml_cond("pinned", self.pinned);
                arr.push_yaml_cond("unpinned", self.unpinned);
                arr.push_yaml_cond("closed", self.closed);
                arr.push_yaml_cond("reopened", self.reopened);
                arr.push_yaml_cond("assigned", self.assigned);
                arr.push_yaml_cond("unassigned", self.unassigned);
                arr.push_yaml_cond("labeled", self.labeled);
                arr.push_yaml_cond("unlabeled", self.unlabeled);
                arr.push_yaml_cond("locked", self.locked);
                arr.push_yaml_cond("unlocked", self.unlocked);
                arr.push_yaml_cond("milestoned", self.milestoned);
                arr.push_yaml_cond("demilestoned", self.demilestoned);
                arr.push_yaml_cond("typed", self.typed);
                arr.push_yaml_cond("untyped", self.untyped);
                out.insert_yaml("types", Yaml::Array(arr));
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct LabelEvent {
        created: bool,
        edited: bool,
        deleted: bool,
    }
    #[pymethods]
    impl LabelEvent {
        #[new]
        #[pyo3(signature = (*, created=false, edited=false, deleted=false))]
        fn new(created: bool, edited: bool, deleted: bool) -> Self {
            Self {
                created,
                edited,
                deleted,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &LabelEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.created || self.edited || self.deleted {
                let mut out = Hash::new();
                let mut arr = Array::new();
                arr.push_yaml_cond("created", self.created);
                arr.push_yaml_cond("edited", self.edited);
                arr.push_yaml_cond("deleted", self.deleted);
                out.insert_yaml("types", Yaml::Array(arr));
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct MergeGroupEvent {
        checks_requested: bool,
    }
    #[pymethods]
    impl MergeGroupEvent {
        #[new]
        #[pyo3(signature = (*, checks_requested=false))]
        fn new(checks_requested: bool) -> Self {
            Self { checks_requested }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &MergeGroupEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.checks_requested {
                let mut out = Hash::new();
                let mut arr = Array::new();
                arr.push_yaml_cond("checks_requested", self.checks_requested);
                out.insert_yaml("types", Yaml::Array(arr));
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct MilestoneEvent {
        created: bool,
        closed: bool,
        opened: bool,
        edited: bool,
        deleted: bool,
    }
    #[pymethods]
    impl MilestoneEvent {
        #[new]
        #[pyo3(signature = (*, created=false, closed=false, opened=false, edited=false, deleted=false))]
        fn new(created: bool, closed: bool, opened: bool, edited: bool, deleted: bool) -> Self {
            Self {
                created,
                closed,
                opened,
                edited,
                deleted,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &MilestoneEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.created || self.closed || self.opened || self.edited || self.deleted {
                let mut out = Hash::new();
                let mut arr = Array::new();
                arr.push_yaml_cond("created", self.created);
                arr.push_yaml_cond("closed", self.closed);
                arr.push_yaml_cond("opened", self.opened);
                arr.push_yaml_cond("edited", self.edited);
                arr.push_yaml_cond("deleted", self.deleted);
                out.insert_yaml("types", Yaml::Array(arr));
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct PullRequestEvent {
        assigned: bool,
        unassigned: bool,
        labeled: bool,
        unlabeled: bool,
        opened: bool,
        edited: bool,
        closed: bool,
        reopened: bool,
        synchronize: bool,
        converted_to_draft: bool,
        locked: bool,
        unlocked: bool,
        enqueued: bool,
        dequeued: bool,
        milestoned: bool,
        demilestoned: bool,
        ready_for_review: bool,
        review_requested: bool,
        review_request_removed: bool,
        auto_merge_enabled: bool,
        auto_merge_disabled: bool,
        branches: Option<Vec<String>>,
        branches_ignore: Option<Vec<String>>,
        paths: Option<Vec<String>>,
        paths_ignore: Option<Vec<String>>,
    }
    #[pymethods]
    impl PullRequestEvent {
        #[new]
        #[pyo3(signature = (*, branches=None, branches_ignore=None, paths=None, paths_ignore=None, assigned=false, unassigned=false, labeled=false, unlabeled=false, opened=false, edited=false, closed=false, reopened=false, synchronize=false, converted_to_draft=false, locked=false, unlocked=false, enqueued=false, dequeued=false, milestoned=false, demilestoned=false, ready_for_review=false, review_requested=false, review_request_removed=false, auto_merge_enabled=false, auto_merge_disabled=false))]
        fn new(
            branches: Option<Vec<String>>,
            branches_ignore: Option<Vec<String>>,
            paths: Option<Vec<String>>,
            paths_ignore: Option<Vec<String>>,
            assigned: bool,
            unassigned: bool,
            labeled: bool,
            unlabeled: bool,
            opened: bool,
            edited: bool,
            closed: bool,
            reopened: bool,
            synchronize: bool,
            converted_to_draft: bool,
            locked: bool,
            unlocked: bool,
            enqueued: bool,
            dequeued: bool,
            milestoned: bool,
            demilestoned: bool,
            ready_for_review: bool,
            review_requested: bool,
            review_request_removed: bool,
            auto_merge_enabled: bool,
            auto_merge_disabled: bool,
        ) -> Self {
            let branches = branches.filter(|v| !v.is_empty());
            let branches_ignore = branches_ignore.filter(|v| !v.is_empty());
            let paths = paths.filter(|v| !v.is_empty());
            let paths_ignore = paths_ignore.filter(|v| !v.is_empty());
            Self {
                assigned,
                unassigned,
                labeled,
                unlabeled,
                opened,
                edited,
                closed,
                reopened,
                synchronize,
                converted_to_draft,
                locked,
                unlocked,
                enqueued,
                dequeued,
                milestoned,
                demilestoned,
                ready_for_review,
                review_requested,
                review_request_removed,
                auto_merge_enabled,
                auto_merge_disabled,
                branches,
                branches_ignore,
                paths,
                paths_ignore,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &PullRequestEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            let mut out = Hash::new();
            out.insert_yaml_opt("branches", self.branches.as_ref());
            out.insert_yaml_opt("branches-ignore", self.branches_ignore.as_ref());
            out.insert_yaml_opt("paths", self.paths.as_ref());
            out.insert_yaml_opt("paths-ignore", self.paths_ignore.as_ref());
            if self.assigned
                || self.unassigned
                || self.labeled
                || self.unlabeled
                || self.opened
                || self.edited
                || self.closed
                || self.reopened
                || self.synchronize
                || self.converted_to_draft
                || self.locked
                || self.unlocked
                || self.enqueued
                || self.dequeued
                || self.milestoned
                || self.demilestoned
                || self.ready_for_review
                || self.review_requested
                || self.review_request_removed
                || self.auto_merge_enabled
                || self.auto_merge_disabled
            {
                let mut arr = Array::new();
                arr.push_yaml_cond("assigned", self.assigned);
                arr.push_yaml_cond("unassigned", self.unassigned);
                arr.push_yaml_cond("labeled", self.labeled);
                arr.push_yaml_cond("unlabeled", self.unlabeled);
                arr.push_yaml_cond("opened", self.opened);
                arr.push_yaml_cond("edited", self.edited);
                arr.push_yaml_cond("closed", self.closed);
                arr.push_yaml_cond("reopened", self.reopened);
                arr.push_yaml_cond("synchronize", self.synchronize);
                arr.push_yaml_cond("converted_to_draft", self.converted_to_draft);
                arr.push_yaml_cond("locked", self.locked);
                arr.push_yaml_cond("unlocked", self.unlocked);
                arr.push_yaml_cond("enqueued", self.enqueued);
                arr.push_yaml_cond("dequeued", self.dequeued);
                arr.push_yaml_cond("milestoned", self.milestoned);
                arr.push_yaml_cond("demilestoned", self.demilestoned);
                arr.push_yaml_cond("ready_for_review", self.ready_for_review);
                arr.push_yaml_cond("review_requested", self.review_requested);
                arr.push_yaml_cond("review_request_removed", self.review_request_removed);
                arr.push_yaml_cond("auto_merge_enabled", self.auto_merge_enabled);
                arr.push_yaml_cond("auto_merge_disabled", self.auto_merge_disabled);
                out.insert_yaml("types", Yaml::Array(arr));
            }
            if out.is_empty() {
                None
            } else {
                Some(Yaml::Hash(out))
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct PullRequestReviewEvent {
        submitted: bool,
        edited: bool,
        dismissed: bool,
    }
    #[pymethods]
    impl PullRequestReviewEvent {
        #[new]
        #[pyo3(signature = (*, submitted=false, edited=false, dismissed=false))]
        fn new(submitted: bool, edited: bool, dismissed: bool) -> Self {
            Self {
                submitted,
                edited,
                dismissed,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &PullRequestReviewEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.submitted || self.edited || self.dismissed {
                let mut out = Hash::new();
                let mut arr = Array::new();
                arr.push_yaml_cond("submitted", self.submitted);
                arr.push_yaml_cond("edited", self.edited);
                arr.push_yaml_cond("dismissed", self.dismissed);
                out.insert_yaml("types", Yaml::Array(arr));
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct PullRequestReviewCommentEvent {
        created: bool,
        edited: bool,
        deleted: bool,
    }
    #[pymethods]
    impl PullRequestReviewCommentEvent {
        #[new]
        #[pyo3(signature = (*, created=false,edited=false, deleted=false))]
        fn new(created: bool, edited: bool, deleted: bool) -> Self {
            Self {
                created,
                edited,
                deleted,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &PullRequestReviewCommentEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.created || self.edited || self.deleted {
                let mut out = Hash::new();
                let mut arr = Array::new();
                arr.push_yaml_cond("created", self.created);
                arr.push_yaml_cond("edited", self.edited);
                arr.push_yaml_cond("deleted", self.deleted);
                out.insert_yaml("types", Yaml::Array(arr));
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct PushEvent {
        branches: Option<Vec<String>>,
        branches_ignore: Option<Vec<String>>,
        tags: Option<Vec<String>>,
        tags_ignore: Option<Vec<String>>,
        paths: Option<Vec<String>>,
        paths_ignore: Option<Vec<String>>,
    }
    #[pymethods]
    impl PushEvent {
        #[new]
        #[pyo3(signature = (*, branches=None, branches_ignore=None, tags=None, tags_ignore=None, paths=None, paths_ignore=None))]
        fn new(
            branches: Option<Vec<String>>,
            branches_ignore: Option<Vec<String>>,
            tags: Option<Vec<String>>,
            tags_ignore: Option<Vec<String>>,
            paths: Option<Vec<String>>,
            paths_ignore: Option<Vec<String>>,
        ) -> Self {
            Self {
                branches,
                branches_ignore,
                tags,
                tags_ignore,
                paths,
                paths_ignore,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &PushEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            let mut out = Hash::new();
            out.insert_yaml_opt("branches", self.branches.as_ref());
            out.insert_yaml_opt("branches-ignore", self.branches_ignore.as_ref());
            out.insert_yaml_opt("tags", self.tags.as_ref());
            out.insert_yaml_opt("tags-ignore", self.tags_ignore.as_ref());
            out.insert_yaml_opt("paths", self.paths.as_ref());
            out.insert_yaml_opt("paths-ignore", self.paths_ignore.as_ref());
            if out.is_empty() {
                None
            } else {
                Some(Yaml::Hash(out))
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct RegistryPackageEvent {
        published: bool,
        updated: bool,
    }
    #[pymethods]
    impl RegistryPackageEvent {
        #[new]
        #[pyo3(signature = (*, published=false, updated=false))]
        fn new(published: bool, updated: bool) -> Self {
            Self { published, updated }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &RegistryPackageEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.published || self.updated {
                let mut out = Hash::new();
                let mut arr = Array::new();
                arr.push_yaml_cond("published", self.published);
                arr.push_yaml_cond("updated", self.updated);
                out.insert_yaml("types", Yaml::Array(arr));
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct ReleaseEvent {
        published: bool,
        unpublished: bool,
        created: bool,
        edited: bool,
        deleted: bool,
        prereleased: bool,
        released: bool,
    }
    #[pymethods]
    impl ReleaseEvent {
        #[new]
        #[pyo3(signature = (*, published=false, unpublished=false, created=false, edited=false, deleted=false, prereleased=false, released=false))]
        fn new(
            published: bool,
            unpublished: bool,
            created: bool,
            edited: bool,
            deleted: bool,
            prereleased: bool,
            released: bool,
        ) -> Self {
            Self {
                published,
                unpublished,
                created,
                edited,
                deleted,
                prereleased,
                released,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &ReleaseEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.published
                || self.unpublished
                || self.created
                || self.edited
                || self.deleted
                || self.prereleased
                || self.released
            {
                let mut out = Hash::new();
                let mut arr = Array::new();
                arr.push_yaml_cond("published", self.published);
                arr.push_yaml_cond("unpublished", self.unpublished);
                arr.push_yaml_cond("created", self.created);
                arr.push_yaml_cond("edited", self.edited);
                arr.push_yaml_cond("deleted", self.deleted);
                arr.push_yaml_cond("prereleased", self.prereleased);
                arr.push_yaml_cond("released", self.released);
                out.insert_yaml("types", Yaml::Array(arr));
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct RepositoryDispatchEvent {
        types: Option<Vec<String>>,
    }
    #[pymethods]
    impl RepositoryDispatchEvent {
        #[new]
        #[pyo3(signature = (*, types=None))]
        fn new(types: Option<Vec<String>>) -> Self {
            let types = types.filter(|v| !v.is_empty());
            Self { types }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &RepositoryDispatchEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            let mut out = Hash::new();
            out.insert_yaml_opt("types", self.types.as_ref());
            if out.is_empty() {
                None
            } else {
                Some(Yaml::Hash(out))
            }
        }
    }

    #[derive(Clone)]
    enum CronStepType {
        Value(u8),
        List(Vec<u8>),
        Range(u8, u8),
        Step { start: Option<u8>, step: u8 },
    }
    impl Display for CronStepType {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(
                f,
                "{}",
                match self {
                    Self::Value(v) => v.to_string(),
                    Self::List(items) => items
                        .iter()
                        .map(std::string::ToString::to_string)
                        .collect::<Vec<String>>()
                        .join(","),

                    Self::Range(min, max) => format!("{min}-{max}"),
                    Self::Step { start, step } => format!(
                        "{}/{}",
                        start.map(|s| s.to_string()).unwrap_or("*".to_string()),
                        step
                    ),
                }
            )
        }
    }

    #[derive(Debug, Copy, Clone, Eq, PartialEq)]
    struct CronMinute(u8);

    impl<'a, 'py> FromPyObject<'a, 'py> for CronMinute {
        type Error = PyErr;
        fn extract(obj: Borrowed<'a, 'py, PyAny>) -> Result<Self, Self::Error> {
            if let Ok(num) = obj.extract::<u8>()
                && num <= 59
            {
                return Ok(CronMinute(num));
            }
            Err(PyValueError::new_err(
                "Minute must be an integer in range 0..=59",
            ))
        }
    }

    #[derive(Debug, Copy, Clone, Eq, PartialEq)]
    struct CronHour(u8);

    impl<'a, 'py> FromPyObject<'a, 'py> for CronHour {
        type Error = PyErr;
        fn extract(obj: Borrowed<'a, 'py, PyAny>) -> Result<Self, Self::Error> {
            if let Ok(num) = obj.extract::<u8>()
                && num <= 23
            {
                return Ok(CronHour(num));
            }
            Err(PyValueError::new_err(
                "Hour must be an integer in range 0..=23",
            ))
        }
    }

    #[derive(Debug, Copy, Clone, Eq, PartialEq)]
    struct CronDay(u8);

    impl<'a, 'py> FromPyObject<'a, 'py> for CronDay {
        type Error = PyErr;
        fn extract(obj: Borrowed<'a, 'py, PyAny>) -> Result<Self, Self::Error> {
            if let Ok(num) = obj.extract::<u8>()
                && (1..=31).contains(&num)
            {
                return Ok(CronDay(num));
            }
            Err(PyValueError::new_err(
                "Hour must be an integer in range 1..=31",
            ))
        }
    }

    #[derive(Debug, Copy, Clone, Eq, PartialEq)]
    struct CronMonth(u8);

    impl<'a, 'py> FromPyObject<'a, 'py> for CronMonth {
        type Error = PyErr;
        fn extract(obj: Borrowed<'a, 'py, PyAny>) -> Result<Self, Self::Error> {
            let msg = "Month must be an integer in range 1..=12";
            if let Ok(num) = obj.extract::<u8>()
                && (1..=12).contains(&num)
            {
                return Ok(CronMonth(num));
            }
            Err(PyValueError::new_err(msg))
        }
    }

    #[derive(Debug, Copy, Clone, Eq, PartialEq)]
    struct CronDayOfWeek(u8);

    impl<'a, 'py> FromPyObject<'a, 'py> for CronDayOfWeek {
        type Error = PyErr;
        fn extract(obj: Borrowed<'a, 'py, PyAny>) -> Result<Self, Self::Error> {
            let msg = "Day of week must be an integer in range 0..=6 (0=Sunday)";
            if let Ok(num) = obj.extract::<u8>()
                && num <= 6
            {
                return Ok(CronDayOfWeek(num));
            }
            Err(PyValueError::new_err(msg))
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct Minute(CronStepType);
    impl Display for Minute {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "{}", self.0)
        }
    }
    #[pymethods]
    impl Minute {
        #[new]
        fn new(minute: &Bound<PyAny>) -> PyResult<Self> {
            if let Ok(l) = minute.extract::<Bound<PyList>>() {
                let mut res = Vec::new();
                for item in l.iter() {
                    let item = item.extract::<CronMinute>()?;
                    res.push(item.0);
                }
                return Ok(Self(CronStepType::List(res)));
            }
            let minute = minute.extract::<CronMinute>()?;
            Ok(Self(CronStepType::Value(minute.0)))
        }
        #[staticmethod]
        fn between(start: &Bound<PyAny>, end: &Bound<PyAny>) -> PyResult<Self> {
            let min = start.extract::<CronMinute>()?;
            let max = end.extract::<CronMinute>()?;
            Ok(Self(CronStepType::Range(min.0, max.0)))
        }
        #[staticmethod]
        #[pyo3(signature = (interval, *, start = None))]
        fn every(interval: &Bound<PyAny>, start: Option<Bound<PyAny>>) -> PyResult<Self> {
            let start = start
                .map(|a| a.extract::<CronMinute>())
                .transpose()?
                .map(|s| s.0);
            let interval = interval.extract::<CronMinute>()?;
            Ok(Self(CronStepType::Step {
                start,
                step: interval.0,
            }))
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct Hour(CronStepType);
    impl Display for Hour {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "{}", self.0)
        }
    }
    #[pymethods]
    impl Hour {
        #[new]
        fn new(hour: &Bound<PyAny>) -> PyResult<Self> {
            if let Ok(l) = hour.extract::<Bound<PyList>>() {
                let mut res = Vec::new();
                for item in l.iter() {
                    let item = item.extract::<CronHour>()?;
                    res.push(item.0);
                }
                return Ok(Self(CronStepType::List(res)));
            }
            let hour = hour.extract::<CronHour>()?;
            Ok(Self(CronStepType::Value(hour.0)))
        }
        #[staticmethod]
        fn between(start: &Bound<PyAny>, end: &Bound<PyAny>) -> PyResult<Self> {
            let min = start.extract::<CronHour>()?;
            let max = end.extract::<CronHour>()?;
            Ok(Self(CronStepType::Range(min.0, max.0)))
        }
        #[staticmethod]
        #[pyo3(signature = (interval, *, start = None))]
        fn every(interval: &Bound<PyAny>, start: Option<Bound<PyAny>>) -> PyResult<Self> {
            let start = start
                .map(|a| a.extract::<CronHour>())
                .transpose()?
                .map(|s| s.0);
            let interval = interval.extract::<CronHour>()?;
            Ok(Self(CronStepType::Step {
                start,
                step: interval.0,
            }))
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct Day(CronStepType);
    impl Display for Day {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "{}", self.0)
        }
    }
    #[pymethods]
    impl Day {
        #[new]
        fn new(day: &Bound<PyAny>) -> PyResult<Self> {
            if let Ok(l) = day.extract::<Bound<PyList>>() {
                let mut res = Vec::new();
                for item in l.iter() {
                    let item = item.extract::<CronDay>()?;
                    res.push(item.0);
                }
                return Ok(Self(CronStepType::List(res)));
            }
            let day = day.extract::<CronDay>()?;
            Ok(Self(CronStepType::Value(day.0)))
        }
        #[staticmethod]
        fn between(min: &Bound<PyAny>, max: &Bound<PyAny>) -> PyResult<Self> {
            let min = min.extract::<CronDay>()?;
            let max = max.extract::<CronDay>()?;
            Ok(Self(CronStepType::Range(min.0, max.0)))
        }
        #[staticmethod]
        #[pyo3(signature = (interval, *, start = None))]
        fn every(interval: &Bound<PyAny>, start: Option<Bound<PyAny>>) -> PyResult<Self> {
            let start = start
                .map(|a| a.extract::<CronDay>())
                .transpose()?
                .map(|s| s.0);
            let interval = interval.extract::<CronDay>()?;
            Ok(Self(CronStepType::Step {
                start,
                step: interval.0,
            }))
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct Month(CronStepType);
    impl Display for Month {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "{}", self.0)
        }
    }
    #[pymethods]
    impl Month {
        #[new]
        fn new(month: &Bound<PyAny>) -> PyResult<Self> {
            if let Ok(l) = month.extract::<Bound<PyList>>() {
                let mut res = Vec::new();
                for item in l.iter() {
                    let item = item.extract::<CronMonth>()?;
                    res.push(item.0);
                }
                return Ok(Self(CronStepType::List(res)));
            }
            let month = month.extract::<CronMonth>()?;
            Ok(Self(CronStepType::Value(month.0)))
        }
        #[staticmethod]
        fn between(min: &Bound<PyAny>, max: &Bound<PyAny>) -> PyResult<Self> {
            let min = min.extract::<CronMonth>()?;
            let max = max.extract::<CronMonth>()?;
            Ok(Self(CronStepType::Range(min.0, max.0)))
        }
        #[staticmethod]
        #[pyo3(signature = (interval, *, start = None))]
        fn every(interval: &Bound<PyAny>, start: Option<Bound<PyAny>>) -> PyResult<Self> {
            let start = start
                .map(|a| a.extract::<CronMonth>())
                .transpose()?
                .map(|s| s.0);
            let interval = interval.extract::<CronMonth>()?;
            Ok(Self(CronStepType::Step {
                start,
                step: interval.0,
            }))
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct DayOfWeek(CronStepType);
    impl Display for DayOfWeek {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "{}", self.0)
        }
    }
    #[pymethods]
    impl DayOfWeek {
        #[new]
        fn new(day_of_week: &Bound<PyAny>) -> PyResult<Self> {
            if let Ok(l) = day_of_week.extract::<Bound<PyList>>() {
                let mut res = Vec::new();
                for item in l.iter() {
                    let item = item.extract::<CronDayOfWeek>()?;
                    res.push(item.0);
                }
                return Ok(Self(CronStepType::List(res)));
            }
            let day_of_week = day_of_week.extract::<CronMonth>()?;
            Ok(Self(CronStepType::Value(day_of_week.0)))
        }
        #[staticmethod]
        fn between(min: &Bound<PyAny>, max: &Bound<PyAny>) -> PyResult<Self> {
            let min = min.extract::<CronDayOfWeek>()?;
            let max = max.extract::<CronDayOfWeek>()?;
            Ok(Self(CronStepType::Range(min.0, max.0)))
        }
        #[staticmethod]
        #[pyo3(signature = (interval, *, start = None))]
        fn every(interval: &Bound<PyAny>, start: Option<Bound<PyAny>>) -> PyResult<Self> {
            let start = start
                .map(|a| a.extract::<CronDayOfWeek>())
                .transpose()?
                .map(|s| s.0);
            let interval = interval.extract::<CronDayOfWeek>()?;
            Ok(Self(CronStepType::Step {
                start,
                step: interval.0,
            }))
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct Cron {
        minute: Option<Minute>,
        hour: Option<Hour>,
        day: Option<Day>,
        month: Option<Month>,
        day_of_week: Option<DayOfWeek>,
    }
    #[pymethods]
    impl Cron {
        #[new]
        #[pyo3(signature = (*, minute = None, hour = None, day = None, month = None, day_of_week = None))]
        fn new(
            minute: Option<Minute>,
            hour: Option<Hour>,
            day: Option<Day>,
            month: Option<Month>,
            day_of_week: Option<DayOfWeek>,
        ) -> Self {
            Self {
                minute,
                hour,
                day,
                month,
                day_of_week,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for &Cron {
        fn as_yaml(&self) -> Yaml {
            let mut out = Hash::new();
            let s = format!(
                "{} {} {} {} {}",
                self.minute
                    .clone()
                    .map_or("*".to_string(), |s| s.to_string()),
                self.hour.clone().map_or("*".to_string(), |s| s.to_string()),
                self.day.clone().map_or("*".to_string(), |s| s.to_string()),
                self.month
                    .clone()
                    .map_or("*".to_string(), |s| s.to_string()),
                self.day_of_week
                    .clone()
                    .map_or("*".to_string(), |s| s.to_string())
            );
            out.insert_yaml("cron", s);
            Yaml::Hash(out)
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct ScheduleEvent {
        crons: Option<Vec<Cron>>,
    }
    #[pymethods]
    impl ScheduleEvent {
        #[new]
        #[pyo3(signature = (*, crons=None))]
        fn new(crons: Option<Vec<Cron>>) -> Self {
            let crons = crons.filter(|v| !v.is_empty());
            Self { crons }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &ScheduleEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            let mut out = Array::new();
            if let Some(crons) = &self.crons {
                for cron in crons {
                    out.push_yaml(cron);
                }
                Some(Yaml::Array(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct WatchEvent {
        started: bool,
    }
    #[pymethods]
    impl WatchEvent {
        #[new]
        #[pyo3(signature = (*, started=false))]
        fn new(started: bool) -> Self {
            Self { started }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &WatchEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if self.started {
                let mut out = Hash::new();
                let mut arr = Array::new();
                arr.push_yaml_cond("started", self.started);
                out.insert_yaml("types", Yaml::Array(arr));
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[derive(Clone)]
    enum WorkflowInputType {
        Boolean { default: Option<BoolLike> },
        Number { default: Option<IntLike> },
        String { default: Option<StringLike> },
    }
    impl WorkflowInputType {
        fn get_type(&self) -> Yaml {
            match self {
                Self::Boolean { .. } => Yaml::from_str("boolean"),
                Self::Number { .. } => Yaml::from_str("number"),
                Self::String { .. } => Yaml::from_str("string"),
            }
        }
        fn get_default(&self) -> Option<Yaml> {
            match self {
                Self::Boolean { default } => default.clone().map(|b| b.as_yaml()),
                Self::Number { default } => default.clone().map(|n| n.as_yaml()),
                Self::String { default } => default.clone().map(|s| s.as_yaml()),
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct WorkflowInput {
        description: Option<String>,
        input_type: WorkflowInputType,
        required: Option<bool>,
    }
    #[pymethods]
    impl WorkflowInput {
        #[staticmethod]
        #[pyo3(signature = (*, description=None, default=None, required=None))]
        fn boolean(
            description: Option<String>,
            default: Option<BoolLike>,
            required: Option<bool>,
        ) -> PyResult<Self> {
            if let Some(default) = &default {
                validate_bool_like(default, ALLOWED_WORKFLOW_CALL_INPUT_DEFAULT)?;
            }
            Ok(Self {
                description,
                input_type: WorkflowInputType::Boolean { default },
                required,
            })
        }
        #[staticmethod]
        #[pyo3(signature = (*, description=None, default=None, required=None))]
        fn number(
            description: Option<String>,
            default: Option<IntLike>,
            required: Option<bool>,
        ) -> PyResult<Self> {
            if let Some(default) = &default {
                validate_int_like(default, ALLOWED_WORKFLOW_CALL_INPUT_DEFAULT)?;
            }
            Ok(Self {
                description,
                input_type: WorkflowInputType::Number { default },
                required,
            })
        }
        #[staticmethod]
        #[pyo3(signature = (*, description=None, default=None, required=None))]
        fn string(
            description: Option<String>,
            default: Option<StringLike>,
            required: Option<bool>,
        ) -> PyResult<Self> {
            if let Some(default) = &default {
                validate_string_like(default, ALLOWED_WORKFLOW_CALL_INPUT_DEFAULT)?;
            }
            Ok(Self {
                description,
                input_type: WorkflowInputType::String { default },
                required,
            })
        }

        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for &WorkflowInput {
        fn as_yaml(&self) -> Yaml {
            let mut out = Hash::new();
            out.insert_yaml_opt("description", &self.description);
            out.insert_yaml("type", self.input_type.get_type());
            out.insert_yaml_opt("required", self.required);
            out.insert_yaml_opt("default", self.input_type.get_default());
            Yaml::Hash(out)
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct WorkflowOutput {
        description: Option<String>,
        value: StringLike,
    }
    #[pymethods]
    impl WorkflowOutput {
        #[new]
        #[pyo3(signature = (value, *, description=None))]
        fn new(value: StringLike, description: Option<String>) -> PyResult<Self> {
            validate_string_like(&value, ALLOWED_WORKFLOW_CALL_OUTPUT_VALUE)?;
            Ok(Self { description, value })
        }

        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for &WorkflowOutput {
        fn as_yaml(&self) -> Yaml {
            let mut out = Hash::new();
            out.insert_yaml_opt("description", &self.description);
            out.insert_yaml("value", &self.value);
            Yaml::Hash(out)
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct WorkflowSecret {
        description: Option<String>,
        required: Option<bool>,
    }
    #[pymethods]
    impl WorkflowSecret {
        #[new]
        #[pyo3(signature = (*, description=None, required=None))]
        fn new(description: Option<String>, required: Option<bool>) -> Self {
            Self {
                description,
                required,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &WorkflowSecret {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            let mut out = Hash::new();
            out.insert_yaml_opt("description", &self.description);
            out.insert_yaml_opt("required", self.required);
            if out.is_empty() {
                None
            } else {
                Some(Yaml::Hash(out))
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct WorkflowCallEvent {
        inputs: PyMap<String, WorkflowInput>,
        outputs: PyMap<String, WorkflowOutput>,
        secrets: PyMap<String, WorkflowSecret>,
    }
    #[pymethods]
    impl WorkflowCallEvent {
        #[new]
        #[pyo3(signature = (*, inputs=None, outputs=None, secrets=None))]
        fn new(
            inputs: Option<PyMap<String, WorkflowInput>>,
            outputs: Option<PyMap<String, WorkflowOutput>>,
            secrets: Option<PyMap<String, WorkflowSecret>>,
        ) -> Self {
            Self {
                inputs: inputs.unwrap_or_default(),
                outputs: outputs.unwrap_or_default(),
                secrets: secrets.unwrap_or_default(),
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for WorkflowCallEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            let mut out = Hash::new();
            let mut inputs = Hash::new();
            for (k, v) in self.inputs.iter() {
                inputs.insert_yaml(k, v);
            }
            if !inputs.is_empty() {
                out.insert_yaml("inputs", Yaml::Hash(inputs));
            }
            let mut outputs = Hash::new();
            for (k, v) in self.outputs.iter() {
                outputs.insert_yaml(k, v);
            }
            if !outputs.is_empty() {
                out.insert_yaml("outputs", Yaml::Hash(outputs));
            }
            let mut secrets = Hash::new();
            for (k, v) in self.secrets.iter() {
                secrets.insert_yaml(k, v.maybe_as_yaml().unwrap_or(Yaml::Null));
            }
            if !secrets.is_empty() {
                out.insert_yaml("secrets", Yaml::Hash(secrets));
            }
            if out.is_empty() {
                None
            } else {
                Some(Yaml::Hash(out))
            }
        }
    }

    #[derive(Clone)]
    enum WorkflowDispatchInputType {
        Boolean {
            default: Option<bool>,
        },
        Choice {
            default: Option<String>,
            options: Vec<String>,
        },
        Number {
            default: Option<i64>,
        },
        Environment,
        String {
            default: Option<String>,
        },
    }
    impl WorkflowDispatchInputType {
        fn get_type(&self) -> Yaml {
            match self {
                Self::Boolean { .. } => Yaml::from_str("boolean"),
                Self::Choice { .. } => Yaml::from_str("choice"),
                Self::Number { .. } => Yaml::from_str("number"),
                Self::Environment => Yaml::from_str("environment"),
                Self::String { .. } => Yaml::from_str("string"),
            }
        }
        fn get_default(&self) -> Option<Yaml> {
            match self {
                Self::Boolean { default } => default.map(Yaml::Boolean),
                Self::Choice { default, .. } | Self::String { default } => {
                    default.clone().map(Yaml::String)
                }
                Self::Number { default } => default.map(Yaml::Integer),
                Self::Environment => None, // TODO: check if environment can have a default
            }
        }
        fn get_options(&self) -> Option<Yaml> {
            if let Self::Choice { options, .. } = self {
                Some(Yaml::Array(
                    options.iter().map(|s| Yaml::String(s.clone())).collect(),
                ))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct WorkflowDispatchInput {
        description: Option<String>,
        input_type: WorkflowDispatchInputType,
        required: Option<bool>,
    }
    #[pymethods]
    impl WorkflowDispatchInput {
        #[staticmethod]
        #[pyo3(signature = (*, description=None, default=None, required=None))]
        fn boolean(
            description: Option<String>,
            default: Option<bool>,
            required: Option<bool>,
        ) -> Self {
            Self {
                description,
                input_type: WorkflowDispatchInputType::Boolean { default },
                required,
            }
        }
        #[staticmethod]
        #[pyo3(signature = (options, *, description=None, default=None, required=None))]
        fn choice(
            options: Vec<String>,
            description: Option<String>,
            default: Option<String>,
            required: Option<bool>,
        ) -> Self {
            Self {
                description,
                input_type: WorkflowDispatchInputType::Choice { default, options },
                required,
            }
        }
        #[staticmethod]
        #[pyo3(signature = (*, description=None, default=None, required=None))]
        fn number(
            description: Option<String>,
            default: Option<i64>,
            required: Option<bool>,
        ) -> Self {
            Self {
                description,
                input_type: WorkflowDispatchInputType::Number { default },
                required,
            }
        }
        #[staticmethod]
        #[pyo3(signature = (*, description=None, required=None))]
        fn environment(description: Option<String>, required: Option<bool>) -> Self {
            Self {
                description,
                input_type: WorkflowDispatchInputType::Environment,
                required,
            }
        }
        #[staticmethod]
        #[pyo3(signature = (*, description=None, default=None, required=None))]
        fn string(
            description: Option<String>,
            default: Option<String>,
            required: Option<bool>,
        ) -> Self {
            Self {
                description,
                input_type: WorkflowDispatchInputType::String { default },
                required,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for &WorkflowDispatchInput {
        fn as_yaml(&self) -> Yaml {
            let mut out = Hash::new();
            out.insert_yaml_opt("description", &self.description);
            out.insert_yaml("type", self.input_type.get_type());
            out.insert_yaml_opt("required", self.required);
            out.insert_yaml_opt("default", self.input_type.get_default());
            out.insert_yaml_opt("options", self.input_type.get_options());
            Yaml::Hash(out)
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct WorkflowDispatchEvent {
        inputs: Option<PyMap<String, WorkflowDispatchInput>>,
    }
    #[pymethods]
    impl WorkflowDispatchEvent {
        #[new]
        #[pyo3(signature = (*, inputs=None))]
        fn new(inputs: Option<PyMap<String, WorkflowDispatchInput>>) -> Self {
            Self {
                inputs: inputs.filter(|i| !i.is_empty()),
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &WorkflowDispatchEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            if let Some(inputs) = &self.inputs {
                let mut out = Hash::new();
                for (k, v) in inputs.iter() {
                    out.insert_yaml(k, v);
                }
                Some(Yaml::Hash(out))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct WorkflowRunEvent {
        workflows: Option<Vec<String>>,
        completed: bool,
        requested: bool,
        in_progress: bool,
        branches: Option<Vec<String>>,
        branches_ignore: Option<Vec<String>>,
    }
    #[pymethods]
    impl WorkflowRunEvent {
        #[new]
        #[pyo3(signature = (*, workflows=None, completed=false, requested=false, in_progress=false, branches=None, branches_ignore=None))]
        fn new(
            workflows: Option<Vec<String>>,
            completed: bool,
            requested: bool,
            in_progress: bool,
            branches: Option<Vec<String>>,
            branches_ignore: Option<Vec<String>>,
        ) -> Self {
            let workflows = workflows.filter(|w| !w.is_empty());
            let branches = branches.filter(|b| !b.is_empty());
            let branches_ignore = branches_ignore.filter(|b| !b.is_empty());
            Self {
                workflows,
                completed,
                requested,
                in_progress,
                branches,
                branches_ignore,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &WorkflowRunEvent {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            let mut out = Hash::new();
            out.insert_yaml_opt("workflows", &self.workflows);
            if self.completed || self.requested || self.in_progress {
                let mut types = Array::new();
                types.push_yaml_cond("completed", self.completed);
                types.push_yaml_cond("requested", self.requested);
                types.push_yaml_cond("in_progress", self.in_progress);
                out.insert_yaml("types", Yaml::Array(types));
            }
            out.insert_yaml_opt("branches", &self.branches);
            out.insert_yaml_opt("branches-ignore", &self.branches_ignore);
            if out.is_empty() {
                None
            } else {
                Some(Yaml::Hash(out))
            }
        }
    }

    #[pyclass]
    #[derive(Clone)]
    struct Events {
        branch_protection_rule: Option<BranchProtectionRuleEvent>,
        check_run: Option<CheckRunEvent>,
        check_suite: Option<CheckSuiteEvent>,
        create: bool,
        delete: bool,
        deployment: bool,
        deployment_status: bool,
        discussion: Option<DiscussionEvent>,
        discussion_comment: Option<DiscussionCommentEvent>,
        fork: bool,
        gollum: bool,
        image_version: Option<ImageVersionEvent>,
        issue_comment: Option<IssueCommentEvent>,
        issues: Option<IssuesEvent>,
        label: Option<LabelEvent>,
        merge_group: Option<MergeGroupEvent>,
        milestone: Option<MilestoneEvent>,
        page_build: bool,
        public: bool,
        pull_request: Option<PullRequestEvent>,
        pull_request_review: Option<PullRequestReviewEvent>,
        pull_request_review_comment: Option<PullRequestReviewCommentEvent>,
        pull_request_target: Option<PullRequestEvent>,
        push: Option<PushEvent>,
        registry_package: Option<RegistryPackageEvent>,
        release: Option<ReleaseEvent>,
        schedule: Option<ScheduleEvent>,
        status: bool,
        watch: Option<WatchEvent>,
        workflow_call: Option<WorkflowCallEvent>,
        workflow_dispatch: Option<WorkflowDispatchEvent>,
        workflow_run: Option<WorkflowRunEvent>,
    }
    #[pymethods]
    impl Events {
        /// A set of events which may trigger a Workflow.
        ///
        /// Parameters
        /// ----------
        /// branch_protection_rule
        ///     Triggers when the branch protection rules for the repository are changed.
        /// check_run
        ///     Triggers when activity related to a check run occurs.
        /// check_suite
        ///     Triggers when activity related to a check suite occurs.
        /// create
        ///     Triggers when someone creates a new branch or tag (but not if more than three tags are made at once).
        /// delete
        ///     Triggers when someone deletes a new branch or tag
        /// deployment
        ///     Triggers when a deployment is created.
        /// deployment_status
        ///     Triggers when a third party service provides a deployment status (unlesss deployment status's state is set to ``inactive``).
        /// discussion
        ///     Triggers when a discussion is created or modified.
        /// discussion_comment
        ///     Triggers on a comment on a discussion.
        /// fork
        ///     Triggers when someone forks a repository.
        /// gollum
        ///     Triggers when someone creates/edits a Wiki page.
        /// image_version
        ///     Triggers when a new version of a specified image becomes available.
        /// issue_comment
        ///     Triggers when an issue or pull request comment is created, edited, or deleted.
        /// issues
        ///     Triggers when an issue is created or modified.
        /// label
        ///     Triggers when a label is created or modified.
        /// merge_group
        ///     Triggers when a pull request is added to a merge queue which adds the pull request
        ///     to a merge group.
        /// milestone
        ///     Triggers when a milestone is created or modified.
        /// page_build
        ///     Triggers on pushes to a branch which is the publishing source for GitHub Pages.
        /// public
        ///     Triggers when the repository visibility is changed from private to public.
        /// pull_request
        ///     Triggers on activity related to a pull request
        /// pull_request_review
        ///     Triggers on actions related to a pull request review.
        /// pull_request_review_comment
        ///     Triggers when a pull request review comment is modified.
        /// pull_request_target
        ///     Triggers when some activity occurs on a pull request. This runs in the context of
        ///     the default branch of the repository rather than the context of the merge commit
        ///     (use the ``pull_request`` argument for that).
        /// push
        ///     Triggers when a commit or tag is pushed (also when a repository is created from a
        ///     template).
        /// registry_package
        ///     Triggers on activity related to GitHub Packages
        /// release
        ///     Triggers on release activity.
        /// repository_dispatch
        ///     Triggers when the GitHub API is useed to trigger a webhook event called
        ///     ``repository_dispatch`` (used to trigger a workflow for activity that happens
        ///     outside of GitHub).
        /// schedule
        ///     Triggers on a fixed time schedule (cronjob).
        /// status
        ///     Triggers when the status of a commit changes.
        /// watch
        ///     Triggers when the repository is starred.
        /// workflow_call
        ///     Triggers when the workflow is called by another workflow.
        /// workflow_dispatch
        ///     Allows the workflow to be triggered manually through the GitHub API, CLI, or UI.
        /// workflow_run
        ///     Triggers when a workflow run is requested or completed.
        ///
        /// Notes
        /// -----
        /// See `the documentation on GitHub <https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#branch_protection_rule>`_ for more details.
        #[new]
        #[pyo3(signature = (*, branch_protection_rule=None, check_run=None, check_suite=None, create=false, delete=false, deployment=false, deployment_status=false, discussion=None, discussion_comment=None, fork=false, gollum=false, image_version=None, issue_comment=None, issues=None, label=None, merge_group=None, milestone=None, page_build=false, public=false, pull_request=None, pull_request_review=None, pull_request_review_comment=None, pull_request_target=None, push=None, registry_package=None, release=None, schedule=None, status=false, watch=None, workflow_call=None, workflow_dispatch=None, workflow_run=None))]
        fn new(
            branch_protection_rule: Option<BranchProtectionRuleEvent>,
            check_run: Option<CheckRunEvent>,
            check_suite: Option<CheckSuiteEvent>,
            create: bool,
            delete: bool,
            deployment: bool,
            deployment_status: bool,
            discussion: Option<DiscussionEvent>,
            discussion_comment: Option<DiscussionCommentEvent>,
            fork: bool,
            gollum: bool,
            image_version: Option<ImageVersionEvent>,
            issue_comment: Option<IssueCommentEvent>,
            issues: Option<IssuesEvent>,
            label: Option<LabelEvent>,
            merge_group: Option<MergeGroupEvent>,
            milestone: Option<MilestoneEvent>,
            page_build: bool,
            public: bool,
            pull_request: Option<PullRequestEvent>,
            pull_request_review: Option<PullRequestReviewEvent>,
            pull_request_review_comment: Option<PullRequestReviewCommentEvent>,
            pull_request_target: Option<PullRequestEvent>,
            push: Option<PushEvent>,
            registry_package: Option<RegistryPackageEvent>,
            release: Option<ReleaseEvent>,
            schedule: Option<ScheduleEvent>,
            status: bool,
            watch: Option<WatchEvent>,
            workflow_call: Option<WorkflowCallEvent>,
            workflow_dispatch: Option<WorkflowDispatchEvent>,
            workflow_run: Option<WorkflowRunEvent>,
        ) -> Self {
            Self {
                branch_protection_rule,
                check_run,
                check_suite,
                create,
                delete,
                deployment,
                deployment_status,
                discussion,
                discussion_comment,
                fork,
                gollum,
                image_version,
                issue_comment,
                issues,
                label,
                merge_group,
                milestone,
                page_build,
                public,
                pull_request,
                pull_request_review,
                pull_request_review_comment,
                pull_request_target,
                push,
                registry_package,
                release,
                schedule,
                status,
                watch,
                workflow_call,
                workflow_dispatch,
                workflow_run,
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.maybe_as_yaml_string()
        }
    }
    impl MaybeYamlable for &Events {
        fn maybe_as_yaml(&self) -> Option<Yaml> {
            let mut configured = Hash::new();
            let mut simple_names: Vec<&str> = Vec::new();

            if let Some(event) = &self.branch_protection_rule {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("branch_protection_rule", yaml);
                } else {
                    simple_names.push("branch_protection_rule");
                }
            }
            if let Some(event) = &self.check_run {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("check_run", yaml);
                } else {
                    simple_names.push("check_run");
                }
            }
            if let Some(event) = &self.check_suite {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("check_suite", yaml);
                } else {
                    simple_names.push("check_suite");
                }
            }
            if let Some(event) = &self.discussion {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("discussion", yaml);
                } else {
                    simple_names.push("discussion");
                }
            }
            if let Some(event) = &self.discussion_comment {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("discussion_comment", yaml);
                } else {
                    simple_names.push("discussion_comment");
                }
            }

            if let Some(event) = &self.image_version {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("image_version", yaml);
                } else {
                    simple_names.push("image_version");
                }
            }
            if let Some(event) = &self.issue_comment {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("issue_comment", yaml);
                } else {
                    simple_names.push("issue_comment");
                }
            }
            if let Some(event) = &self.issues {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("issues", yaml);
                } else {
                    simple_names.push("issues");
                }
            }
            if let Some(event) = &self.label {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("label", yaml);
                } else {
                    simple_names.push("label");
                }
            }
            if let Some(event) = &self.merge_group {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("merge_group", yaml);
                } else {
                    simple_names.push("merge_group");
                }
            }
            if let Some(event) = &self.milestone {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("milestone", yaml);
                } else {
                    simple_names.push("milestone");
                }
            }
            if let Some(event) = &self.pull_request {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("pull_request", yaml);
                } else {
                    simple_names.push("pull_request");
                }
            }
            if let Some(event) = &self.pull_request_review {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("pull_request_review", yaml);
                } else {
                    simple_names.push("pull_request_review");
                }
            }
            if let Some(event) = &self.pull_request_review_comment {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("pull_request_review_comment", yaml);
                } else {
                    simple_names.push("pull_request_review_comment");
                }
            }
            if let Some(event) = &self.pull_request_target {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("pull_request_target", yaml);
                } else {
                    simple_names.push("pull_request_target");
                }
            }
            if let Some(event) = &self.push {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("push", yaml);
                } else {
                    simple_names.push("push");
                }
            }
            if let Some(event) = &self.registry_package {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("registry_package", yaml);
                } else {
                    simple_names.push("registry_package");
                }
            }
            if let Some(event) = &self.release {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("release", yaml);
                } else {
                    simple_names.push("release");
                }
            }
            if let Some(event) = &self.schedule {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("schedule", yaml);
                } else {
                    simple_names.push("schedule");
                }
            }
            if let Some(event) = &self.watch {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("watch", yaml);
                } else {
                    simple_names.push("watch");
                }
            }
            if let Some(event) = &self.workflow_call {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("workflow_call", yaml);
                } else {
                    simple_names.push("workflow_call");
                }
            }
            if let Some(event) = &self.workflow_dispatch {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("workflow_dispatch", yaml);
                } else {
                    simple_names.push("workflow_dispatch");
                }
            }
            if let Some(event) = &self.workflow_run {
                if let Some(yaml) = event.maybe_as_yaml() {
                    configured.insert_yaml("workflow_run", yaml);
                } else {
                    simple_names.push("workflow_run");
                }
            }

            if self.create {
                simple_names.push("create");
            }
            if self.delete {
                simple_names.push("delete");
            }
            if self.deployment {
                simple_names.push("deployment");
            }
            if self.deployment_status {
                simple_names.push("deployment_status");
            }
            if self.fork {
                simple_names.push("fork");
            }
            if self.gollum {
                simple_names.push("gollum");
            }
            if self.page_build {
                simple_names.push("page_build");
            }
            if self.public {
                simple_names.push("public");
            }
            if self.status {
                simple_names.push("status");
            }

            if configured.is_empty() {
                match simple_names.len() {
                    0 => None,
                    1 => Some(simple_names[0].as_yaml()),
                    _ => {
                        let mut arr = Array::new();
                        for name in simple_names {
                            arr.push_yaml(name);
                        }
                        Some(Yaml::Array(arr))
                    }
                }
            } else {
                for name in simple_names {
                    configured.insert_yaml(name, Yaml::Null);
                }
                Some(Yaml::Hash(configured))
            }
        }
    }

    #[pyclass]
    struct Workflow {
        name: Option<String>,
        run_name: Option<StringLike>,
        on: Events,
        permissions: Option<Permissions>,
        env: Option<PyMap<String, StringLike>>,
        defaults: Option<Defaults>,
        concurrency: Option<Concurrency>,
        jobs: PyMap<String, Job>,
    }
    #[pymethods]
    impl Workflow {
        /// A configurable automated process made up of one or more jobs.
        ///
        /// Workflows are the primary entrypoint for ``yamloom``. Typical actions include constructing
        /// workflows and then writing them to a file with ``Workflow.dump('path/to/file.yml')``.
        ///
        /// Parameters
        /// ----------
        /// jobs
        ///     Jobs to run (in parallel by default).
        /// on
        ///     Events which may trigger the workflow.
        /// name
        ///     The name of the workflow.
        /// run_name
        ///     The name given to a particular run of the workflow.
        /// permissions
        ///     The default permissions granted to the ``GITHUB_TOKEN``.
        /// env
        ///     Global environment variables available at any step of any job in the workflow.
        /// defaults
        ///     Default settings which are applied to all jobs.
        /// concurrency
        ///     Settings to ensure only a single workflow of the given concurrency group runs at a time.
        ///
        /// Returns
        /// -------
        /// Workflow
        ///
        #[new]
        #[pyo3(signature = (*, jobs, on, name = None, run_name = None, permissions = None, env = None, defaults = None, concurrency = None))]
        fn new(
            jobs: PyMap<String, Job>,
            on: Events,
            name: Option<String>,
            run_name: Option<StringLike>,
            permissions: Option<Permissions>,
            env: Option<PyMap<String, StringLike>>,
            defaults: Option<Defaults>,
            concurrency: Option<Concurrency>,
        ) -> PyResult<Self> {
            if let Some(run_name) = &run_name {
                validate_string_like(run_name, ALLOWED_WORKFLOW_RUN_NAME)?;
            }
            if let Some(env) = &env {
                validate_string_map(env, ALLOWED_WORKFLOW_ENV)?;
            }
            if let Some(concurrency) = &concurrency {
                validate_concurrency(concurrency, ALLOWED_WORKFLOW_CONCURRENCY)?;
            }
            Ok(Self {
                name,
                run_name,
                on,
                permissions,
                env,
                defaults,
                concurrency,
                jobs,
            })
        }

        /// Run validation against the schemastore JSON schema for GitHub Workflows and raise a
        /// RuntimeError if validation fails.
        fn validate(&self) -> PyResult<()> {
            let workflow_yaml = self.as_yaml();
            let workflow_json = yaml_to_json(&workflow_yaml)?;
            WORKFLOW_SCHEMA
                .validate(&workflow_json)
                .map_err(|e| PyRuntimeError::new_err(e.to_string()))
        }

        /// Check if the workflow is valid YAML according to the schemastore JSON schema for GitHub
        /// Workflows.
        fn is_valid(&self) -> bool {
            self.validate().is_ok()
        }

        /// Write the YAML representation of the workflow to a file.
        ///
        /// Parameters
        /// ----------
        /// path
        ///     The path of the file to which the YAML is written.
        /// overwrite
        ///     If True, the file is overwritten if it already exists, otherwise nothing will happen.
        /// validate
        ///     If True, perform validation against the schemastore JSON schema for GitHub
        ///     Workflows.
        ///
        #[pyo3(signature = (path, *, overwrite = true, validate = true))]
        fn dump(&self, path: &Bound<PyAny>, overwrite: bool, validate: bool) -> PyResult<()> {
            if validate {
                self.validate()?;
            }
            if let Ok(p) = path.extract::<PathBuf>() {
                self.write_to_file(p, overwrite)
            } else if let Ok(s) = path.extract::<String>() {
                self.write_to_file(s, overwrite)
            } else {
                Err(PyValueError::new_err("Invalid path"))
            }
        }

        fn __str__(&self) -> PyResult<String> {
            self.as_yaml_string()
        }
    }
    impl Yamlable for &Workflow {
        fn as_yaml(&self) -> Yaml {
            let mut out = Hash::new();
            out.insert_yaml_opt("name", &self.name);
            out.insert_yaml_opt("run-name", &self.run_name);
            out.insert_yaml_opt("on", (&self.on).maybe_as_yaml());
            out.insert_yaml_opt("permissions", &self.permissions);
            out.insert_yaml_opt("env", &self.env);
            if let Some(defaults) = &self.defaults {
                out.insert_yaml_opt("defaults", defaults.maybe_as_yaml());
            }
            out.insert_yaml_opt("concurrency", &self.concurrency);
            out.insert_yaml("jobs", &self.jobs);
            Yaml::Hash(out)
        }
    }
}

fn yaml_to_json(yaml: &Yaml) -> PyResult<Value> {
    Ok(match yaml {
        Yaml::Real(v) => {
            if contains_github_expression(v) {
                Value::String(v.clone())
            } else {
                Value::Number(
                    Number::from_str(v).map_err(|e| PyRuntimeError::new_err(e.to_string()))?,
                )
            }
        }
        Yaml::Integer(v) => Value::Number(Number::from(*v)),
        Yaml::String(s) => Value::String(s.clone()),
        Yaml::Boolean(b) => Value::Bool(*b),
        Yaml::Array(values) => {
            Value::Array(values.iter().map(yaml_to_json).collect::<PyResult<_>>()?)
        }
        Yaml::Hash(hash) => {
            let mut obj = Map::new();
            for (k, v) in hash {
                let key = if let Yaml::String(s) = k {
                    s.clone()
                } else {
                    return Err(PyRuntimeError::new_err("Unsupported key type"))?;
                };
                obj.insert(key, yaml_to_json(v)?);
            }
            Value::Object(obj)
        }
        Yaml::Null => Value::Null,
        Yaml::Alias(_) | Yaml::BadValue => Err(PyRuntimeError::new_err("Unsupported YAML value"))?,
    })
}

static WORKFLOW_SCHEMA: LazyLock<Validator> = LazyLock::new(|| {
    let schema: Value = serde_json::from_str(include_str!("../schemas/github-workflow.json"))
        .expect("invalid JSON schema");
    jsonschema::options()
        .with_base_uri(
            schema
                .get("$id")
                .and_then(|v| v.as_str())
                .unwrap_or("urn:github-workflow-schema")
                .to_string(),
        )
        .build(&schema)
        .expect("schema compilation failed")
});

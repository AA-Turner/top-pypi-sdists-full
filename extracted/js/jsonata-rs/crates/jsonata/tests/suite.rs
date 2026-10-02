//! Port of `JsonataTest` — runs the official JSONata test suite (the
//! `jsonata-js` submodule under jsonata-java) against our implementation.
//!
//! Run all groups:           cargo test -p jsonata --test suite -- --nocapture
//! Run one group:  JSONATA_GROUP=function-sum cargo test -p jsonata --test suite -- --nocapture
//! Run one case:   JSONATA_CASE=groups/null/case001.json cargo test ...

use jsonata::json::parse_json;
use jsonata::value::JValue;
use jsonata::Jsonata;
use std::path::{Path, PathBuf};

/// Root of the official JSONata conformance test-suite — the `jsonata-js`
/// submodule at `third_party/jsonata` (pinned to the same commit the upstream
/// jsonata-java port uses), resolved relative to this crate.
fn suite_root() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../third_party/jsonata/test/test-suite")
        .canonicalize()
        .expect("jsonata test-suite not found — run `git submodule update --init`")
}

fn read_json_file(path: &Path) -> JValue {
    let s =
        std::fs::read_to_string(path).unwrap_or_else(|e| panic!("read {}: {}", path.display(), e));
    parse_json(&s).unwrap_or_else(|e| panic!("parse {}: {}", path.display(), e))
}

// ---- overrides ------------------------------------------------------------

struct Override {
    name: String,
    ignore_error: bool,
    alternate_result: Option<JValue>,
    alternate_code: bool,
}

fn load_overrides() -> Vec<Override> {
    let crate_dir = Path::new(env!("CARGO_MANIFEST_DIR"));
    let mut out = Vec::new();
    // Vendored from jsonata-java (the upstream port's accepted divergences)...
    parse_overrides_file(&crate_dir.join("test-overrides.json"), &mut out);
    // ...plus Rust-port-specific overrides (UTF-16 lone-surrogate limitations).
    let local = crate_dir.join("test-overrides-local.json");
    if local.exists() {
        parse_overrides_file(&local, &mut out);
    }
    out
}

fn parse_overrides_file(path: &Path, out: &mut Vec<Override>) {
    let v = read_json_file(path);
    if let Some(o) = v.as_object() {
        if let Some(JValue::Array(arr, _)) = o.get("override").map(|x| x.clone()).as_ref() {
            for item in arr.iter() {
                if let Some(io) = item.as_object() {
                    let name = io
                        .get("name")
                        .and_then(|x| x.as_str())
                        .unwrap_or("")
                        .to_string();
                    let ignore_error = io
                        .get("ignoreError")
                        .and_then(|x| x.as_bool())
                        .unwrap_or(false);
                    let alternate_result = io.get("alternateResult").cloned();
                    let alternate_code = io.get("alternateCode").is_some();
                    out.push(Override {
                        name,
                        ignore_error,
                        alternate_result,
                        alternate_code,
                    });
                }
            }
        }
    }
}

fn override_for<'a>(overrides: &'a [Override], name: &str) -> Option<&'a Override> {
    overrides.iter().find(|o| name.contains(&o.name))
}

// ---- running --------------------------------------------------------------

fn get<'a>(obj: &'a JValue, key: &str) -> Option<&'a JValue> {
    obj.as_object().and_then(|o| o.get(key))
}

/// Returns (passed, message_if_failed)
fn run_case(name: &str, def: &JValue, overrides: &[Override]) -> (bool, String) {
    let expr = match get(def, "expr").and_then(|v| v.as_str()) {
        Some(e) => e.to_string(),
        None => {
            // expr-file
            if let Some(ef) = get(def, "expr-file").and_then(|v| v.as_str()) {
                let dir = Path::new(name).parent().unwrap();
                let p = suite_root().join(dir).join(ef);
                std::fs::read_to_string(&p).unwrap_or_default()
            } else {
                String::new()
            }
        }
    };

    let dataset = get(def, "dataset")
        .and_then(|v| v.as_str())
        .map(|s| s.to_string());
    let bindings = get(def, "bindings").cloned();
    let undefined = matches!(get(def, "undefinedResult"), Some(JValue::Bool(true)));

    // override (loaded before computing expected so alternateResult/Code apply)
    let ovr = override_for(overrides, name);

    // expected
    let has_result = def
        .as_object()
        .map(|o| o.contains_key("result"))
        .unwrap_or(false);
    let mut expected: JValue = if undefined {
        JValue::Undefined
    } else if has_result {
        get(def, "result").cloned().unwrap_or(JValue::Null)
    } else {
        JValue::Null
    };

    // error code expected?
    let mut expect_error = get(def, "code").and_then(|v| v.as_str()).is_some();
    if let Some(err) = get(def, "error") {
        if get(err, "code").and_then(|v| v.as_str()).is_some() {
            expect_error = true;
        }
    }

    // apply override alternates (Java: result = alternateResult; code = alternateCode)
    if let Some(o) = ovr {
        if let Some(ar) = &o.alternate_result {
            expected = ar.clone();
        }
        if o.alternate_code {
            expect_error = true;
        }
    }

    // data
    let data: JValue = if def
        .as_object()
        .map(|o| o.contains_key("data"))
        .unwrap_or(false)
    {
        get(def, "data").cloned().unwrap_or(JValue::Null)
    } else if let Some(ds) = &dataset {
        let p = suite_root().join("datasets").join(format!("{}.json", ds));
        read_json_file(&p)
    } else {
        JValue::Undefined
    };

    // evaluate
    let outcome = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
        evaluate(&expr, data.clone(), bindings.clone())
    }));

    let (passed, msg) = match outcome {
        Err(_) => (false, format!("PANIC evaluating: {}", expr)),
        Ok(Err(e)) => {
            if expect_error {
                (true, String::new())
            } else {
                (false, format!("unexpected error {} for: {}", e.error, expr))
            }
        }
        Ok(Ok(actual)) => {
            if expect_error {
                (
                    false,
                    format!("expected error but got {:?} for: {}", actual, expr),
                )
            } else if actual == expected {
                (true, String::new())
            } else {
                (
                    false,
                    format!(
                        "expr={}\n   expected={:?}\n   actual  ={:?}",
                        expr, expected, actual
                    ),
                )
            }
        }
    };

    // apply override
    if !passed {
        if let Some(o) = ovr {
            if o.ignore_error {
                return (true, String::new());
            }
        }
    }
    (passed, msg)
}

fn evaluate(expr: &str, data: JValue, bindings: Option<JValue>) -> jsonata::JResult<JValue> {
    let mut j = Jsonata::new(expr)?;
    j.set_output_convert_nulls(false);

    let frame = if let Some(b) = bindings {
        let f = jsonata::frame::Frame::new(None);
        if let Some(o) = b.as_object() {
            let mut fb = f.borrow_mut();
            for (k, v) in o.iter() {
                fb.bind(k, v.clone());
            }
        }
        f.borrow_mut().set_runtime_bounds(1000, 303);
        Some(f)
    } else {
        None
    };

    j.evaluate(data, frame)
}

fn run_suite_file(rel: &str, overrides: &[Override]) -> (usize, usize, Vec<String>) {
    let path = suite_root().join(rel);
    let v = read_json_file(&path);
    let mut pass = 0;
    let mut total = 0;
    let mut failures = Vec::new();
    match &v {
        JValue::Array(arr, _) => {
            for (i, case) in arr.iter().enumerate() {
                total += 1;
                let cname = format!("{}_{}", rel, i);
                let (p, m) = run_case(&cname, case, overrides);
                if p {
                    pass += 1;
                } else {
                    failures.push(format!("[{}] {}", cname, m));
                }
            }
        }
        _ => {
            total += 1;
            let (p, m) = run_case(rel, &v, overrides);
            if p {
                pass += 1;
            } else {
                failures.push(format!("[{}] {}", rel, m));
            }
        }
    }
    (pass, total, failures)
}

#[allow(dead_code)]
fn list_groups() -> Vec<String> {
    let groups_dir = suite_root().join("groups");
    let mut groups: Vec<String> = std::fs::read_dir(&groups_dir)
        .unwrap()
        .filter_map(|e| e.ok())
        .filter(|e| e.path().is_dir())
        .map(|e| e.file_name().to_string_lossy().to_string())
        .collect();
    groups.sort();
    groups
}

fn run_group(group: &str, overrides: &[Override]) -> (usize, usize, Vec<String>) {
    let dir = suite_root().join("groups").join(group);
    let mut files: Vec<PathBuf> = std::fs::read_dir(&dir)
        .unwrap()
        .filter_map(|e| e.ok())
        .map(|e| e.path())
        .filter(|p| p.extension().map(|x| x == "json").unwrap_or(false))
        .collect();
    files.sort();
    let mut pass = 0;
    let mut total = 0;
    let mut failures = Vec::new();
    for f in files {
        let rel = format!(
            "groups/{}/{}",
            group,
            f.file_name().unwrap().to_string_lossy()
        );
        let (p, t, fl) = run_suite_file(&rel, overrides);
        pass += p;
        total += t;
        failures.extend(fl);
    }
    (pass, total, failures)
}

/// One `#[test]` per official test-suite group (mirrors jsonata-java's
/// per-group `runTestGroup_*` methods). Each asserts 100% of its group's cases.
/// Set `JSONATA_VERBOSE=1` to print every failure; `JSONATA_CASE=<rel-path>`
/// runs the `single_case` debug test on one file instead.
/// Run `f` on a thread with a large stack. libtest threads default to ~2 MiB,
/// which debug builds overflow on deep-recursion cases (the suite's runtime
/// bound of depth 303 costs ~10 KB of debug stack per depth unit) before any
/// guard can fire.
fn with_big_stack<T: Send + 'static>(f: impl FnOnce() -> T + Send + 'static) -> T {
    let handle = std::thread::Builder::new()
        .stack_size(32 * 1024 * 1024)
        .spawn(f)
        .expect("spawn test thread");
    match handle.join() {
        Ok(v) => v,
        Err(e) => std::panic::resume_unwind(e),
    }
}

macro_rules! group_test {
    ($fn:ident, $group:expr) => {
        #[test]
        #[allow(non_snake_case)]
        fn $fn() {
            // load_overrides() runs inside the thread: Override holds JValue
            // (Rc-based, not Send).
            let (pass, total, failures) = with_big_stack(move || {
                let overrides = load_overrides();
                run_group($group, &overrides)
            });
            for f in &failures {
                eprintln!("FAIL {}", f);
            }
            assert_eq!(
                pass, total,
                "group `{}`: {}/{} cases passed",
                $group, pass, total
            );
        }
    };
}

group_test!(group_array_constructor, "array-constructor");
group_test!(group_blocks, "blocks");
group_test!(group_boolean_expresssions, "boolean-expresssions");
group_test!(group_closures, "closures");
group_test!(group_coalescing_operator, "coalescing-operator");
group_test!(group_comments, "comments");
group_test!(group_comparison_operators, "comparison-operators");
group_test!(group_conditionals, "conditionals");
group_test!(group_context, "context");
group_test!(group_default_operator, "default-operator");
group_test!(group_descendent_operator, "descendent-operator");
group_test!(group_encoding, "encoding");
group_test!(group_errors, "errors");
group_test!(group_fields, "fields");
group_test!(group_flattening, "flattening");
group_test!(group_function_abs, "function-abs");
group_test!(group_function_append, "function-append");
group_test!(group_function_applications, "function-applications");
group_test!(group_function_assert, "function-assert");
group_test!(group_function_average, "function-average");
group_test!(group_function_boolean, "function-boolean");
group_test!(group_function_ceil, "function-ceil");
group_test!(group_function_contains, "function-contains");
group_test!(group_function_count, "function-count");
group_test!(group_function_decodeUrl, "function-decodeUrl");
group_test!(
    group_function_decodeUrlComponent,
    "function-decodeUrlComponent"
);
group_test!(group_function_distinct, "function-distinct");
group_test!(group_function_each, "function-each");
group_test!(group_function_encodeUrl, "function-encodeUrl");
group_test!(
    group_function_encodeUrlComponent,
    "function-encodeUrlComponent"
);
group_test!(group_function_error, "function-error");
group_test!(group_function_eval, "function-eval");
group_test!(group_function_exists, "function-exists");
group_test!(group_function_floor, "function-floor");
group_test!(group_function_formatBase, "function-formatBase");
group_test!(group_function_formatInteger, "function-formatInteger");
group_test!(group_function_formatNumber, "function-formatNumber");
group_test!(group_function_fromMillis, "function-fromMillis");
group_test!(group_function_join, "function-join");
group_test!(group_function_keys, "function-keys");
group_test!(group_function_length, "function-length");
group_test!(group_function_lookup, "function-lookup");
group_test!(group_function_lowercase, "function-lowercase");
group_test!(group_function_max, "function-max");
group_test!(group_function_merge, "function-merge");
group_test!(group_function_number, "function-number");
group_test!(group_function_pad, "function-pad");
group_test!(group_function_parseInteger, "function-parseInteger");
group_test!(group_function_power, "function-power");
group_test!(group_function_replace, "function-replace");
group_test!(group_function_reverse, "function-reverse");
group_test!(group_function_round, "function-round");
group_test!(group_function_shuffle, "function-shuffle");
group_test!(group_function_sift, "function-sift");
group_test!(group_function_signatures, "function-signatures");
group_test!(group_function_sort, "function-sort");
group_test!(group_function_split, "function-split");
group_test!(group_function_spread, "function-spread");
group_test!(group_function_sqrt, "function-sqrt");
group_test!(group_function_string, "function-string");
group_test!(group_function_substring, "function-substring");
group_test!(group_function_substringAfter, "function-substringAfter");
group_test!(group_function_substringBefore, "function-substringBefore");
group_test!(group_function_sum, "function-sum");
group_test!(group_function_tomillis, "function-tomillis");
group_test!(group_function_trim, "function-trim");
group_test!(group_function_typeOf, "function-typeOf");
group_test!(group_function_uppercase, "function-uppercase");
group_test!(group_function_zip, "function-zip");
group_test!(group_higher_order_functions, "higher-order-functions");
group_test!(group_hof_filter, "hof-filter");
group_test!(group_hof_map, "hof-map");
group_test!(group_hof_reduce, "hof-reduce");
group_test!(group_hof_single, "hof-single");
group_test!(group_hof_zip_map, "hof-zip-map");
group_test!(group_inclusion_operator, "inclusion-operator");
group_test!(group_joins, "joins");
group_test!(group_lambdas, "lambdas");
group_test!(group_literals, "literals");
group_test!(group_matchers, "matchers");
group_test!(group_missing_paths, "missing-paths");
group_test!(group_multiple_array_selectors, "multiple-array-selectors");
group_test!(group_null, "null");
group_test!(group_numeric_operators, "numeric-operators");
group_test!(group_object_constructor, "object-constructor");
group_test!(group_parentheses, "parentheses");
group_test!(group_parent_operator, "parent-operator");
group_test!(group_partial_application, "partial-application");
group_test!(group_performance, "performance");
group_test!(group_predicates, "predicates");
group_test!(group_quoted_selectors, "quoted-selectors");
group_test!(group_range_operator, "range-operator");
group_test!(group_regex, "regex");
group_test!(group_simple_array_selectors, "simple-array-selectors");
group_test!(group_sorting, "sorting");
group_test!(group_string_concat, "string-concat");
group_test!(group_tail_recursion, "tail-recursion");
group_test!(group_token_conversion, "token-conversion");
group_test!(group_transform, "transform");
group_test!(group_transforms, "transforms");
group_test!(group_variables, "variables");
group_test!(group_wildcards, "wildcards");

/// Debug helper: run a single case file given by `JSONATA_CASE` (a path
/// relative to the test-suite root, e.g. `groups/null/case001.json`).
/// A no-op when the variable is unset, so it never affects normal runs.
#[test]
fn single_case() {
    let case = match std::env::var("JSONATA_CASE") {
        Ok(c) => c,
        Err(_) => return,
    };
    let (p, t, fl) = {
        let case = case.clone();
        with_big_stack(move || {
            let overrides = load_overrides();
            run_suite_file(&case, &overrides)
        })
    };
    for f in &fl {
        eprintln!("FAIL {}", f);
    }
    assert_eq!(p, t, "{}: {}/{}", case, p, t);
}

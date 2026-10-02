//! Fidelity regression suite — fuzz-generated cases with jsonata-java as the
//! oracle (see `tests/fidelity/README.md` for provenance and regeneration).
//!
//! Same case format as the official suite (`expr` / `data` / `result` /
//! `undefinedResult` / `code`), one JSON array per group file under
//! `tests/fidelity/groups/`. Known, documented divergences from jsonata-java
//! are listed by exact case name in `tests/fidelity/skip.json`.

use jsonata::json::parse_json;
use jsonata::value::JValue;
use jsonata::Jsonata;
use std::collections::HashSet;
use std::path::{Path, PathBuf};

fn fidelity_root() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR")).join("tests/fidelity")
}

fn read_json_file(path: &Path) -> JValue {
    let s =
        std::fs::read_to_string(path).unwrap_or_else(|e| panic!("read {}: {}", path.display(), e));
    parse_json(&s).unwrap_or_else(|e| panic!("parse {}: {:?}", path.display(), e))
}

fn load_skips() -> HashSet<String> {
    let path = fidelity_root().join("skip.json");
    if !path.exists() {
        return HashSet::new();
    }
    let v = read_json_file(&path);
    let mut out = HashSet::new();
    if let Some(arr) = v.as_object().and_then(|o| o.get("skip")).cloned() {
        if let JValue::Array(items, _) = arr {
            for item in items.iter() {
                if let Some(name) = item.as_object().and_then(|o| o.get("name")) {
                    if let Some(s) = name.as_str() {
                        out.insert(s.to_string());
                    }
                }
            }
        }
    }
    out
}

fn get<'a>(obj: &'a JValue, key: &str) -> Option<&'a JValue> {
    obj.as_object().and_then(|o| o.get(key))
}

/// Returns None when the case passes, or Some(message) when it fails.
fn run_case(def: &JValue) -> Option<String> {
    let expr = get(def, "expr").and_then(|v| v.as_str()).unwrap_or("");
    let undefined = matches!(get(def, "undefinedResult"), Some(JValue::Bool(true)));
    let expect_code = get(def, "code").and_then(|v| v.as_str()).map(String::from);
    let has_result = def
        .as_object()
        .map(|o| o.contains_key("result"))
        .unwrap_or(false);
    let expected: JValue = if undefined {
        JValue::Undefined
    } else {
        get(def, "result").cloned().unwrap_or(JValue::Null)
    };
    let data: JValue = if def
        .as_object()
        .map(|o| o.contains_key("data"))
        .unwrap_or(false)
    {
        get(def, "data").cloned().unwrap_or(JValue::Null)
    } else {
        JValue::Undefined
    };

    let expr_owned = expr.to_string();
    let outcome = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
        let mut j = Jsonata::new(&expr_owned)?;
        j.set_output_convert_nulls(false);
        j.evaluate(data, None)
    }));

    match outcome {
        Err(_) => Some(format!("PANIC evaluating: {}", expr)),
        Ok(Err(e)) => match &expect_code {
            Some(code) if *code == e.error => None,
            Some(code) => Some(format!(
                "expected error {} but got {} for: {}",
                code, e.error, expr
            )),
            None => Some(format!("unexpected error {} for: {}", e.error, expr)),
        },
        Ok(Ok(actual)) => {
            if let Some(code) = &expect_code {
                Some(format!(
                    "expected error {} but got {:?} for: {}",
                    code, actual, expr
                ))
            } else if !has_result && !undefined {
                Some(format!("case has no expectation: {}", expr))
            } else if actual == expected {
                None
            } else {
                Some(format!(
                    "expr={}\n   expected={:?}\n   actual  ={:?}",
                    expr, expected, actual
                ))
            }
        }
    }
}

/// Run `f` on a thread with a large stack. libtest threads default to ~2 MiB,
/// which debug builds overflow on deep-recursion cases before the evaluator's
/// depth guard can fire (debug frames cost ~10 KB per evaluation-depth unit).
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

#[test]
fn fidelity_suite() {
    with_big_stack(fidelity_suite_impl)
}

fn fidelity_suite_impl() {
    let groups_dir = fidelity_root().join("groups");
    if !groups_dir.exists() {
        eprintln!("fidelity groups not generated; skipping");
        return;
    }
    let skips = load_skips();
    let mut files: Vec<PathBuf> = std::fs::read_dir(&groups_dir)
        .expect("read groups dir")
        .map(|e| e.expect("dir entry").path())
        .filter(|p| p.extension().is_some_and(|x| x == "json"))
        .collect();
    files.sort();

    let (mut pass, mut total, mut skipped) = (0usize, 0usize, 0usize);
    let mut failures = Vec::new();
    for file in &files {
        let group = file.file_stem().unwrap().to_string_lossy().to_string();
        let v = read_json_file(file);
        let cases = match &v {
            JValue::Array(arr, _) => arr.clone(),
            _ => panic!("{}: expected an array of cases", file.display()),
        };
        for (i, case) in cases.iter().enumerate() {
            let name = format!("{}:{}", group, i);
            total += 1;
            if skips.contains(&name) {
                skipped += 1;
                continue;
            }
            match run_case(case) {
                None => pass += 1,
                Some(msg) => failures.push(format!("[{}] {}", name, msg)),
            }
        }
    }
    for f in &failures {
        eprintln!("{}", f);
    }
    eprintln!(
        "fidelity: {} passed, {} failed, {} skipped (of {})",
        pass,
        failures.len(),
        skipped,
        total
    );
    assert!(
        failures.is_empty(),
        "{} fidelity case(s) failed",
        failures.len()
    );
}

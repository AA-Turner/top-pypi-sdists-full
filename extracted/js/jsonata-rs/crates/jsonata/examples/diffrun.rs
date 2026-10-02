//! Differential-testing runner: reads JSONL cases from stdin
//! (`{"expr": "...", "input": <any, optional>}`) and prints one line per case:
//!   OK <serialized-result>   ("undefined" when the result is absent)
//!   ERR <code> <location>
//!   FATAL <message>
//!
//! Mirrors the Java `DiffRun.java` harness (result serialized via `$string`).

use jsonata::functions::strings::string_fn;
use jsonata::json::parse_json;
use jsonata::value::JValue;
use jsonata::Jsonata;
use std::io::BufRead;

fn run_case(line: &str) -> String {
    let case = match parse_json(line) {
        Ok(v) => v,
        Err(e) => return format!("FATAL case-parse: {e:?}"),
    };
    let obj = case.as_object().expect("case must be an object").clone();
    let expr = obj
        .get("expr")
        .and_then(|v| v.as_str().map(|s| s.to_string()))
        .expect("expr required");
    let input = obj.get("input").cloned().unwrap_or(JValue::Undefined);
    let j = match Jsonata::new(&expr) {
        Ok(j) => j,
        Err(e) => return format!("ERR {} {}", e.error, e.location),
    };
    match j.evaluate(input, None) {
        Ok(result) => {
            if result.is_undefined() {
                "OK undefined".to_string()
            } else {
                match string_fn(&[result, JValue::Bool(false)]) {
                    Ok(JValue::String(s)) => format!("OK {s}"),
                    Ok(_) => "OK undefined".to_string(),
                    Err(e) => format!("ERR {} {}", e.error, e.location),
                }
            }
        }
        Err(e) => format!("ERR {} {}", e.error, e.location),
    }
}

fn main() {
    let stdin = std::io::stdin();
    for line in stdin.lock().lines() {
        let line = line.expect("read stdin");
        if line.trim().is_empty() {
            continue;
        }
        // Run each case on a big stack in a fresh thread so deep recursion
        // behaves like the JVM's generous default stack.
        let out = std::thread::Builder::new()
            .stack_size(256 * 1024 * 1024)
            .spawn(move || {
                std::panic::catch_unwind(|| run_case(&line))
                    .unwrap_or_else(|_| "FATAL panic".to_string())
            })
            .expect("spawn")
            .join()
            .unwrap_or_else(|_| "FATAL panic".to_string());
        println!("{out}");
    }
}

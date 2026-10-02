//! Performance harness for the Rust JSONata port.
//!
//! Measures, per scenario, two throughputs in kiloOps/s (thousands of
//! operations per second, higher = faster):
//!   * parse    — compiling the expression (`Jsonata::new`)
//!   * evaluate — evaluating a pre-compiled expression against its data
//!
//! Methodology mirrors `perf/Bench.java` exactly so the numbers are
//! apples-to-apples: a fixed warm-up budget, then a fixed measurement budget,
//! counting iterations. Emits one JSON object to stdout; progress goes to
//! stderr. See `perf/README.md`.
//!
//! Usage:
//!   cargo run -q --release -p jsonata --example bench -- <scenarios.json> [warmup_secs] [measure_secs]

use std::hint::black_box;
use std::time::{Duration, Instant};

use jsonata::json::parse_json;
use jsonata::value::JValue;
use jsonata::Jsonata;

/// Run `f` for `warmup`, then again for `measure`, returning kiloOps/s.
fn measure<F: FnMut()>(warmup: Duration, measure: Duration, mut f: F) -> f64 {
    let w = Instant::now();
    while w.elapsed() < warmup {
        f();
    }
    let mut iters: u64 = 0;
    let t = Instant::now();
    loop {
        f();
        iters += 1;
        if t.elapsed() >= measure {
            break;
        }
    }
    let secs = t.elapsed().as_secs_f64();
    (iters as f64) / secs / 1000.0
}

fn json_escape(s: &str, out: &mut String) {
    out.push('"');
    for c in s.chars() {
        match c {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            c if (c as u32) < 0x20 => out.push_str(&format!("\\u{:04x}", c as u32)),
            c => out.push(c),
        }
    }
    out.push('"');
}

fn main() {
    let mut args = std::env::args().skip(1);
    let path = args
        .next()
        .unwrap_or_else(|| "perf/scenarios.json".to_string());
    let warmup_secs: f64 = args.next().and_then(|s| s.parse().ok()).unwrap_or(1.0);
    let measure_secs: f64 = args.next().and_then(|s| s.parse().ok()).unwrap_or(3.0);
    let warmup = Duration::from_secs_f64(warmup_secs);
    let measure_d = Duration::from_secs_f64(measure_secs);

    let src = std::fs::read_to_string(&path).unwrap_or_else(|e| panic!("read {}: {}", path, e));
    let scenarios = parse_json(&src).unwrap_or_else(|e| panic!("parse {}: {}", path, e.message));
    let arr = scenarios
        .as_array()
        .expect("scenarios.json must be a JSON array")
        .clone();

    let mut out = String::new();
    out.push_str("{\n");
    out.push_str("  \"impl\": \"rust\",\n");
    out.push_str(&format!(
        "  \"warmup_secs\": {}, \"measure_secs\": {},\n",
        warmup_secs, measure_secs
    ));
    out.push_str("  \"results\": [\n");

    let n = arr.len();
    for (i, sc) in arr.iter().enumerate() {
        let obj = sc.as_object().expect("scenario must be an object");
        let name = obj
            .get("name")
            .and_then(|v| v.as_str())
            .expect("scenario.name");
        let expr = obj
            .get("expr")
            .and_then(|v| v.as_str())
            .expect("scenario.expr");
        let data = obj.get("data").cloned().unwrap_or(JValue::Undefined);

        eprintln!("[rust] {} ...", name);

        // parse throughput
        let parse_kops = measure(warmup, measure_d, || {
            let compiled = Jsonata::new(expr).expect("parse");
            black_box(&compiled);
        });

        // compile once, then measure evaluate throughput
        let compiled = Jsonata::new(expr).expect("parse");
        let sample = {
            let r = compiled.evaluate(data.clone(), None).expect("evaluate");
            jsonata::functions::string(&r, false).unwrap_or_else(|_| "<unserializable>".into())
        };
        let eval_kops = measure(warmup, measure_d, || {
            let r = compiled.evaluate(data.clone(), None).expect("evaluate");
            black_box(&r);
        });

        out.push_str("    {");
        out.push_str("\"name\": ");
        json_escape(name, &mut out);
        out.push_str(&format!(", \"parse_kops\": {:.3}", parse_kops));
        out.push_str(&format!(", \"eval_kops\": {:.3}", eval_kops));
        out.push_str(", \"sample\": ");
        json_escape(&sample, &mut out);
        out.push('}');
        out.push_str(if i + 1 < n { ",\n" } else { "\n" });
    }
    out.push_str("  ]\n}\n");
    print!("{}", out);
}

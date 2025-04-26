use std::{cmp::max, sync::OnceLock};

use pyo3::prelude::*;
use regex::Regex;
use rinja::Template;

#[pyfunction]
/// Escapes characters that will break Markdown Templating.
pub fn escape_message(failure_message: &str) -> String {
    let mut e = String::new();
    for c in failure_message.chars() {
        match c {
            '\r' => {}
            c => e.push(c),
        }
    }
    e
}

#[pyfunction]
pub fn shorten_file_paths(failure_message: &str) -> String {
    static SHORTEN_PATH_PATTERN: OnceLock<Regex> = OnceLock::new();
    /*
    Examples of strings that match:

    /path/to/file.txt
    /path/to/file
    /path/to
    path/to:1:2
    /path/to/file.txt:1:2

    Examples of strings that don't match:

    path
    file.txt
    */
    let re = SHORTEN_PATH_PATTERN
        .get_or_init(|| Regex::new(r"(?:\/*[\w\-]+\/)+(?:[\w\.]+)(?::\d+:\d+)*").unwrap());

    let mut new = String::with_capacity(failure_message.len());
    let mut last_match = 0;
    for caps in re.captures_iter(failure_message) {
        let m = caps.get(0).unwrap();
        let filepath = m.as_str();

        // we are looking for the 3rd slash (0-indexed) from the back
        if let Some((third_last_slash_idx, _)) = filepath.rmatch_indices('/').nth(2) {
            new.push_str(&failure_message[last_match..m.start()]);
            new.push_str("...");
            new.push_str(&filepath[third_last_slash_idx..]);
        } else {
            new.push_str(&failure_message[last_match..m.end()]);
        }
        last_match = m.end();
    }
    new.push_str(&failure_message[last_match..]);

    new
}

#[derive(FromPyObject, Debug, Clone)]
pub struct Failure {
    name: String,
    failure_message: Option<String>,
    duration: f64,
    build_url: Option<String>,
}
#[derive(FromPyObject, Debug)]
pub struct MessagePayload {
    passed: i32,
    failed: i32,
    skipped: i32,
    failures: Vec<Failure>,
}

#[derive(Template)]
#[template(path = "test_results_message.md")]
struct TemplateContext {
    num_tests: i32,
    num_failed: i32,
    num_passed: i32,
    num_skipped: i32,
    failures: Vec<TemplateFailure>,
}
struct TemplateFailure {
    test_name: String,
    duration: String,
    backticks: String,
    build_url: Option<String>,
    stack_trace: Vec<String>,
}

#[pyfunction]
pub fn build_message(mut payload: MessagePayload) -> String {
    let failed: i32 = payload.failed;
    let passed: i32 = payload.passed;
    let skipped: i32 = payload.skipped;

    let completed = failed + passed + skipped;

    payload
        .failures
        .sort_by(|a, b| a.duration.partial_cmp(&b.duration).unwrap());
    let template_failures = payload
        .failures
        .into_iter()
        .take(3)
        .map(|failure| {
            let failure_message = failure
                .failure_message
                .as_deref()
                .unwrap_or("No failure message available");
            let stack_trace: Vec<String> =
                failure_message.split('\n').map(escape_message).collect();

            let num_backticks: usize = max(longest_repeated_substring(failure_message, '`') + 1, 3);
            let backticks = "`".repeat(num_backticks);

            TemplateFailure {
                test_name: failure.name,
                duration: format!("{:.3}", failure.duration),
                backticks,
                build_url: failure.build_url,
                stack_trace,
            }
        })
        .collect();

    let template_context = TemplateContext {
        num_tests: completed,
        num_failed: failed,
        num_passed: passed,
        num_skipped: skipped,
        failures: template_failures,
    };

    template_context.render().unwrap()
}

fn longest_repeated_substring(s: &str, target: char) -> usize {
    let mut max_length = 0;
    let mut current_length = 0;

    for c in s.chars() {
        if c == target {
            current_length += 1;
            max_length = max_length.max(current_length);
        } else {
            current_length = 0; // Reset when the character doesn't match
        }
    }

    max_length
}

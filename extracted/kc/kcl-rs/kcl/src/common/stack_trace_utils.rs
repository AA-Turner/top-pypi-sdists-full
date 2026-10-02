//! Port of `software.amazon.kinesis.common.StackTraceUtils`.
//!
//! # Deviation from Java
//!
//! Java formats a `StackTraceElement[]` (from `Thread.currentThread().getStackTrace()`)
//! into a multi-line string, one `\tat <element>\n` per frame. Rust has no
//! reflective per-thread stack-trace API with the same shape; the closest is
//! `std::backtrace::Backtrace`, whose formatting differs substantially. The
//! *intent* (produce a printable trace for diagnostics — used by the coordinator
//! migration-state logging) is preserved:
//!
//! - [`get_printable_stack_trace`] accepts pre-split frame strings and reproduces
//!   Java's exact `\tat <frame>\n` format (so callers with their own frame source
//!   get byte-identical output).
//! - [`printable_backtrace`] formats a captured [`std::backtrace::Backtrace`] in
//!   the same `\tat <line>\n` shape for the common "capture the current trace"
//!   case.

use std::backtrace::Backtrace;

/// Format an array of stack-frame strings the way Java's
/// `getPrintableStackTrace(StackTraceElement[])` does: `"\tat " + frame + "\n"`
/// for each frame, concatenated.
pub fn get_printable_stack_trace<S: AsRef<str>>(stack_trace: &[S]) -> String {
    let mut out = String::new();
    for frame in stack_trace {
        out.push_str("\tat ");
        out.push_str(frame.as_ref());
        out.push('\n');
    }
    out
}

/// Format a captured [`Backtrace`] into the same `"\tat <line>\n"` shape, for the
/// common "capture the current thread's stack" diagnostic case (the Rust analog
/// of `Thread.currentThread().getStackTrace()`).
pub fn printable_backtrace(bt: &Backtrace) -> String {
    let rendered = bt.to_string();
    let mut out = String::new();
    for line in rendered.lines() {
        out.push_str("\tat ");
        out.push_str(line.trim());
        out.push('\n');
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn formats_frames_like_java() {
        let frames = [
            "com.foo.Bar.method(Bar.java:123)",
            "com.foo.Baz.other(Baz.java:45)",
        ];
        assert_eq!(
            get_printable_stack_trace(&frames),
            "\tat com.foo.Bar.method(Bar.java:123)\n\tat com.foo.Baz.other(Baz.java:45)\n"
        );
    }

    #[test]
    fn empty_frames_produce_empty_string() {
        let frames: [&str; 0] = [];
        assert_eq!(get_printable_stack_trace(&frames), "");
    }

    #[test]
    fn backtrace_rendering_does_not_panic() {
        let bt = Backtrace::force_capture();
        let _ = printable_backtrace(&bt);
    }
}

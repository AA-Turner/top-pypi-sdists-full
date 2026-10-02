//! Panic-containment helpers for background loops.
//!
//! Java KCL wraps periodic-task bodies in `catch (Throwable t)` so an
//! unchecked exception is logged and the schedule keeps running. The Rust
//! analogue is `std::panic::catch_unwind` around the loop tick; these helpers
//! keep that idiom uniform across the loops that port such a catch.

use futures::FutureExt;
use std::any::Any;
use std::future::Future;
use std::panic::AssertUnwindSafe;

/// Best-effort message from a `catch_unwind` payload (the analogue of Java
/// logging a caught `Throwable`).
pub(crate) fn panic_message(payload: &(dyn Any + Send)) -> &str {
    if let Some(s) = payload.downcast_ref::<&'static str>() {
        s
    } else if let Some(s) = payload.downcast_ref::<String>() {
        s.as_str()
    } else {
        "<non-string panic payload>"
    }
}

/// Run one loop tick with Java `catch (Throwable)` semantics: a panic is
/// returned as `Err(message)` instead of unwinding (and killing) the calling
/// task. The future's own `Output` is returned untouched on the happy path, so
/// per-tick `Result` handling stays with the caller.
pub(crate) async fn catch_tick<F: Future>(fut: F) -> Result<F::Output, String> {
    AssertUnwindSafe(fut)
        .catch_unwind()
        .await
        .map_err(|payload| panic_message(payload.as_ref()).to_owned())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn catch_tick_passes_through_output() {
        assert_eq!(catch_tick(async { 7 }).await, Ok(7));
    }

    #[tokio::test]
    async fn catch_tick_captures_panic_message() {
        let r = catch_tick(async { panic!("boom {}", 1) }).await;
        assert_eq!(r.unwrap_err(), "boom 1");
    }

    #[test]
    fn panic_message_handles_static_str_string_and_other() {
        assert_eq!(panic_message(&"s" as &(dyn Any + Send)), "s");
        assert_eq!(panic_message(&"o".to_string() as &(dyn Any + Send)), "o");
        assert_eq!(
            panic_message(&42_u8 as &(dyn Any + Send)),
            "<non-string panic payload>"
        );
    }
}

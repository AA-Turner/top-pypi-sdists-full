use std::{
    cell::Cell,
    future::Future,
    marker::PhantomData,
    pin::Pin,
    rc::Rc,
    task::{Context, Poll},
};

use crate::StatsigOptions;

const SILENT_CLIENT_FLAG: &str = "suppress_diagnostic_output";

/// Copied into each owning component; never inferred from a shared instance ID.
#[derive(Clone, Copy, Default, Debug, PartialEq, Eq)]
pub(crate) enum OutputPolicy {
    #[default]
    Legacy,
    Silent,
}

thread_local! {
    static CURRENT: Cell<OutputPolicy> = const { Cell::new(OutputPolicy::Legacy) };
}

pub(crate) struct OutputScope {
    previous: Option<OutputPolicy>,
    _not_send: PhantomData<Rc<()>>,
}

impl Drop for OutputScope {
    fn drop(&mut self) {
        if let Some(previous) = self.previous {
            CURRENT.with(|current| current.set(previous));
        }
    }
}

impl OutputPolicy {
    pub(crate) fn from_options(options: Option<&StatsigOptions>) -> Self {
        if options
            .and_then(|options| options.experimental_flags.as_ref())
            .is_some_and(|flags| flags.contains(SILENT_CLIENT_FLAG))
        {
            Self::Silent
        } else {
            Self::Legacy
        }
    }

    pub(crate) fn current() -> Self {
        CURRENT.with(Cell::get)
    }

    pub(crate) fn is_silent(self) -> bool {
        self == Self::Silent
    }

    pub(crate) fn run<T>(self, operation: impl FnOnce() -> T) -> T {
        let _restore = self.enter();
        operation()
    }

    pub(crate) fn enter(self) -> OutputScope {
        OutputScope {
            previous: CURRENT.with(|current| {
                let previous = current.get();
                if previous == self {
                    None
                } else {
                    current.set(self);
                    Some(previous)
                }
            }),
            _not_send: PhantomData,
        }
    }

    /// The synchronous decoder/provider context exists only during a poll, never across an
    /// await. The future owns its immutable policy, including when it moves between workers.
    pub(crate) fn scope<F: Future>(self, operation: F) -> impl Future<Output = F::Output> {
        ScopedOutput {
            policy: self,
            operation: Some(operation),
        }
    }

    pub(crate) fn configure(options: &mut StatsigOptions, enabled: bool) {
        if enabled {
            options
                .experimental_flags
                .get_or_insert_default()
                .insert(SILENT_CLIENT_FLAG.into());
        } else if let Some(flags) = options.experimental_flags.as_mut() {
            flags.remove(SILENT_CLIENT_FLAG);
        }
    }
}

pin_project_lite::pin_project! {
    struct ScopedOutput<F> {
        policy: OutputPolicy,
        #[pin]
        operation: Option<F>,
    }

    impl<F> PinnedDrop for ScopedOutput<F> {
        fn drop(this: Pin<&mut Self>) {
            let mut this = this.project();
            // Aborted hydration/provider work can run destructors outside its last poll.
            // Keep that cleanup under the same policy without delaying cancellation.
            this.policy.run(|| this.operation.set(None));
        }
    }
}

impl<F: Future> Future for ScopedOutput<F> {
    type Output = F::Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        let this = self.project();
        let mut operation = this.operation;
        this.policy.run(|| {
            let result = operation
                .as_mut()
                .as_pin_mut()
                .expect("polled after completion")
                .poll(cx);
            if result.is_ready() {
                operation.set(None);
            }
            result
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use futures::{FutureExt, future::pending};

    #[test]
    fn synchronous_scope_restores_on_unwind_and_reentrant_legacy_client() {
        let result = std::panic::catch_unwind(|| {
            OutputPolicy::Silent.run(|| {
                assert!(OutputPolicy::current().is_silent());
                OutputPolicy::Legacy.run(|| assert!(!OutputPolicy::current().is_silent()));
                assert!(OutputPolicy::current().is_silent());
                panic!("fake unwind");
            })
        });
        assert!(result.is_err());
        assert!(!OutputPolicy::current().is_silent());
    }

    #[tokio::test]
    async fn async_scope_does_not_leak_across_pending_polls_or_cancellation() {
        struct OnCancel(std::sync::Arc<std::sync::atomic::AtomicBool>);
        impl Drop for OnCancel {
            fn drop(&mut self) {
                self.0.store(
                    OutputPolicy::current().is_silent(),
                    std::sync::atomic::Ordering::SeqCst,
                );
            }
        }
        let cancelled_under_policy = std::sync::Arc::new(std::sync::atomic::AtomicBool::new(false));
        let marker = OnCancel(cancelled_under_policy.clone());
        let selected = OutputPolicy::Silent.scope(async move {
            let _marker = marker;
            assert!(OutputPolicy::current().is_silent());
            pending::<()>().await;
        });
        let mut selected = Box::pin(selected);
        assert!(selected.as_mut().now_or_never().is_none());
        assert!(!OutputPolicy::current().is_silent());
        drop(selected);
        assert!(cancelled_under_policy.load(std::sync::atomic::Ordering::SeqCst));
        assert!(!OutputPolicy::current().is_silent());
        assert_eq!(OutputPolicy::Legacy.scope(async { 42 }).await, 42);
    }

    #[tokio::test]
    async fn spawned_runtime_work_inherits_policy_without_muting_other_work() {
        let runtime = crate::StatsigRuntime::get_runtime();
        let (sender, receiver) = tokio::sync::oneshot::channel();
        OutputPolicy::Silent
            .run(|| {
                runtime.spawn("silent-test", move |_| async {
                    tokio::task::yield_now().await;
                    sender.send(OutputPolicy::current()).unwrap();
                })
            })
            .unwrap();
        assert_eq!(receiver.await.unwrap(), OutputPolicy::Silent);
        assert_eq!(OutputPolicy::current(), OutputPolicy::Legacy);
        runtime.await_tasks_with_tag("silent-test").await;
    }
}

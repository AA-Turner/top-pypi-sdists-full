use rand::RngExt;
use std::future::Future;
use std::sync::atomic::{AtomicBool, AtomicU32, Ordering};
use std::time::Duration;

use tokio::sync::Notify;
use tokio::time::Instant;

use super::NetworkError;
use crate::StatsigErr;

tokio::task_local! {
    pub(crate) static INITIALIZATION_DEADLINE: Instant;
}

#[derive(Clone, Copy)]
pub(crate) struct RetryPolicy {
    pub attempts: u32,
    pub jitter: bool,
}

impl RetryPolicy {
    pub fn state_read_override(attempts: Option<i64>) -> Option<Self> {
        attempts
            .and_then(|value| u32::try_from(value).ok())
            .filter(|value| *value > 0)
            .map(|attempts| Self {
                attempts,
                jitter: true,
            })
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum PrimaryOutcome {
    Success,
    Exhausted,
    Terminal,
}

#[derive(Default)]
pub(crate) struct RefreshFailureTracker(AtomicU32);

impl RefreshFailureTracker {
    // Store the cadence modulo five, so this remains bounded across long outages.
    pub fn record(&self, outcome: PrimaryOutcome, background: bool) -> bool {
        if !background {
            return outcome == PrimaryOutcome::Exhausted;
        }
        match outcome {
            PrimaryOutcome::Exhausted => {
                self.0
                    .fetch_update(Ordering::SeqCst, Ordering::SeqCst, |n| Some((n + 1) % 5))
                    .unwrap_or(0)
                    == 4
            }
            _ => {
                self.0.store(0, Ordering::SeqCst);
                false
            }
        }
    }
}

pub(crate) fn retryable_network_error(error: &NetworkError) -> bool {
    matches!(
        error,
        NetworkError::RequestFailed(..) | NetworkError::RetriesExhausted(..)
    ) && !matches!(
        error.status_code(),
        Some(400 | 401 | 403 | 405 | 413 | 429 | 501)
    )
}

pub(crate) fn retryable_state_error(error: &StatsigErr) -> bool {
    match error {
        StatsigErr::NetworkError(error) => retryable_network_error(error),
        // ResponseData uses this variant for retryable reader I/O errors.
        StatsigErr::SerializationError(_) => true,
        _ => false,
    }
}

fn jitter_ms() -> u64 {
    let sample = |rng: &mut dyn rand::Rng| rng.random_range(0..=100);
    #[cfg(test)]
    if let Ok(jitter) = tests::SEEDED_JITTER.try_with(|rng| sample(&mut *rng.borrow_mut())) {
        return jitter;
    }
    sample(&mut crate::utils::random::rng())
}

pub(crate) struct RetryExecutor<'a> {
    pub policy: RetryPolicy,
    pub deadline: Option<Instant>,
    pub shutdown: &'a AtomicBool,
    pub shutdown_notify: &'a Notify,
}

impl RetryExecutor<'_> {
    pub async fn run<T, E, F, Fut>(
        &self,
        mut attempt: F,
        // None is terminal; Some(limit) is a retryable error with a total-attempt ceiling.
        retry_limit: impl Fn(&E) -> Option<u32>,
        mut fallback: impl FnMut(PrimaryOutcome) -> bool,
        interrupted: impl Fn() -> E,
    ) -> Result<T, E>
    where
        F: FnMut(bool, u32) -> Fut,
        Fut: Future<Output = Result<T, E>>,
    {
        let run = async {
            let mut limit = self.policy.attempts.max(1);
            for index in 0..self.policy.attempts.max(1) {
                if self.shutdown.load(Ordering::SeqCst)
                    || self
                        .deadline
                        .is_some_and(|deadline| Instant::now() >= deadline)
                {
                    fallback(PrimaryOutcome::Terminal);
                    return Err(interrupted());
                }
                match attempt(false, index).await {
                    Ok(value) => {
                        fallback(PrimaryOutcome::Success);
                        return Ok(value);
                    }
                    Err(error) => {
                        let Some(error_limit) = retry_limit(&error) else {
                            fallback(PrimaryOutcome::Terminal);
                            return Err(error);
                        };
                        limit = limit.min(error_limit.max(1));
                        if index + 1 >= limit {
                            if !fallback(PrimaryOutcome::Exhausted) {
                                return Err(error);
                            }
                            if self.shutdown.load(Ordering::SeqCst)
                                || self
                                    .deadline
                                    .is_some_and(|deadline| Instant::now() >= deadline)
                            {
                                fallback(PrimaryOutcome::Terminal);
                                return Err(interrupted());
                            }
                            return attempt(true, index + 1).await;
                        }
                        tokio::time::sleep(Duration::from_millis(
                            200_u64
                                .saturating_mul(1_u64.checked_shl(index).unwrap_or(u64::MAX))
                                .saturating_add(if self.policy.jitter { jitter_ms() } else { 0 }),
                        ))
                        .await;
                    }
                }
            }
            unreachable!("at least one attempt")
        };
        let deadline = async {
            match self.deadline {
                Some(deadline) => tokio::time::sleep_until(deadline).await,
                None => std::future::pending().await,
            }
        };
        let result = tokio::select! {
            biased;
            _ = self.shutdown_notify.notified() => None,
            _ = deadline => None,
            result = run => Some(result),
        };
        match result {
            Some(result) => result,
            None => {
                fallback(PrimaryOutcome::Terminal);
                Err(interrupted())
            }
        }
    }
}

#[cfg(test)]
#[path = "__tests__/retry_tests.rs"]
mod tests;

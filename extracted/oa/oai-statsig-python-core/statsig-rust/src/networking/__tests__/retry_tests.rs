use super::*;
use rand::{SeedableRng, rngs::StdRng};
use std::cell::RefCell;
use std::collections::BTreeSet;
use std::sync::Mutex;

const FOREGROUND_POLICY: RetryPolicy = RetryPolicy {
    attempts: 2,
    jitter: true,
};
const BACKGROUND_POLICY: RetryPolicy = RetryPolicy {
    attempts: 4,
    ..FOREGROUND_POLICY
};

tokio::task_local! {
    pub(super) static SEEDED_JITTER: RefCell<StdRng>;
}

#[tokio::test(start_paused = true)]
async fn primary_budget_backoff_and_immediate_fallback() {
    let shutdown = AtomicBool::new(false);
    let notify = Notify::new();
    let executor = RetryExecutor {
        policy: BACKGROUND_POLICY,
        deadline: None,
        shutdown: &shutdown,
        shutdown_notify: &notify,
    };
    let start = Instant::now();
    let calls = Mutex::new(Vec::new());
    let result = executor
        .run(
            |fallback, index| {
                calls
                    .lock()
                    .unwrap()
                    .push((fallback, index, start.elapsed().as_millis()));
                async move { if fallback { Ok(42) } else { Err("retry") } }
            },
            |_| Some(u32::MAX),
            |outcome| outcome == PrimaryOutcome::Exhausted,
            || "cancelled",
        )
        .await;
    assert_eq!(result, Ok(42));
    let calls = calls.lock().unwrap();
    assert_eq!(
        calls
            .iter()
            .map(|&(fallback, index, _)| (fallback, index))
            .collect::<Vec<_>>(),
        vec![(false, 0), (false, 1), (false, 2), (false, 3), (true, 4)]
    );
    assert_eq!(calls[0].2, 0);
    for (pair, minimum) in calls[..4].windows(2).zip([200, 400, 800]) {
        assert!((minimum..=minimum + 100).contains(&(pair[1].2 - pair[0].2)));
    }
    assert_eq!(calls[3].2, calls[4].2);
}

#[tokio::test(start_paused = true)]
async fn success_and_terminal_errors_stop_without_fallback() {
    let shutdown = AtomicBool::new(false);
    let notify = Notify::new();
    for success in [true, false] {
        let executor = RetryExecutor {
            policy: BACKGROUND_POLICY,
            deadline: None,
            shutdown: &shutdown,
            shutdown_notify: &notify,
        };
        let calls = AtomicU32::new(0);
        let result = executor
            .run(
                |fallback, _| {
                    assert!(!fallback);
                    calls.fetch_add(1, Ordering::SeqCst);
                    async move { if success { Ok(()) } else { Err("terminal") } }
                },
                |_| None,
                |outcome| {
                    assert_ne!(outcome, PrimaryOutcome::Exhausted);
                    false
                },
                || "cancelled",
            )
            .await;
        assert_eq!(result.is_ok(), success);
        assert_eq!(calls.load(Ordering::SeqCst), 1);
    }
}

#[tokio::test(start_paused = true)]
async fn deadline_cancels_backoff_and_pending_attempts() {
    let shutdown = AtomicBool::new(false);
    let notify = Notify::new();
    for pending in [false, true] {
        let executor = RetryExecutor {
            policy: RetryPolicy::state_read_override(Some(i64::from(u32::MAX))).unwrap(),
            deadline: Some(Instant::now() + Duration::from_millis(100)),
            shutdown: &shutdown,
            shutdown_notify: &notify,
        };
        let calls = AtomicU32::new(0);
        let result: Result<(), _> = executor
            .run(
                |_, _| {
                    calls.fetch_add(1, Ordering::SeqCst);
                    async move {
                        if pending {
                            std::future::pending().await
                        } else {
                            Err("retry")
                        }
                    }
                },
                |_| Some(u32::MAX),
                |_| false,
                || "deadline",
            )
            .await;
        assert_eq!(result, Err("deadline"));
        assert_eq!(calls.load(Ordering::SeqCst), 1);
    }
}

#[tokio::test(start_paused = true)]
async fn maximum_budget_cancellation_interrupts_an_inflight_attempt() {
    let shutdown = AtomicBool::new(false);
    let notify = Notify::new();
    let executor = RetryExecutor {
        policy: RetryPolicy::state_read_override(Some(i64::from(u32::MAX))).unwrap(),
        deadline: None,
        shutdown: &shutdown,
        shutdown_notify: &notify,
    };
    let run = executor.run(
        |_, _| std::future::pending::<Result<(), &str>>(),
        |_| Some(u32::MAX),
        |_| false,
        || "cancelled",
    );
    let cancel = async {
        tokio::time::sleep(Duration::from_millis(10)).await;
        shutdown.store(true, Ordering::SeqCst);
        notify.notify_waiters();
    };
    assert_eq!(tokio::join!(run, cancel).0, Err("cancelled"));
}

#[test]
fn independent_cadence_and_foreground_operations() {
    let specs = RefreshFailureTracker::default();
    let files = RefreshFailureTracker::default();
    for n in 1..=10 {
        assert_eq!(files.record(PrimaryOutcome::Exhausted, true), n % 5 == 0);
        assert!(files.record(PrimaryOutcome::Exhausted, false));
        assert!(!files.record(PrimaryOutcome::Success, false));
        assert!(!specs.record(PrimaryOutcome::Success, true));
    }
    files.record(PrimaryOutcome::Exhausted, true);
    files.record(PrimaryOutcome::Terminal, true);
    for n in 1..=5 {
        assert_eq!(files.record(PrimaryOutcome::Exhausted, true), n == 5);
    }
    files.record(PrimaryOutcome::Success, true);
    assert!(!files.record(PrimaryOutcome::Exhausted, true));
}

#[tokio::test(start_paused = true)]
async fn error_ceiling_cannot_expand_and_non_state_backoff_is_unchanged() {
    let shutdown = AtomicBool::new(false);
    let notify = Notify::new();
    for capped in [false, true] {
        let executor = RetryExecutor {
            policy: RetryPolicy {
                attempts: 4,
                jitter: false,
            },
            deadline: None,
            shutdown: &shutdown,
            shutdown_notify: &notify,
        };
        let start = Instant::now();
        let calls = Mutex::new(Vec::new());
        let result = executor
            .run(
                |fallback, index| {
                    calls
                        .lock()
                        .unwrap()
                        .push((fallback, index, start.elapsed().as_millis()));
                    async move { if fallback { Ok(()) } else { Err(index) } }
                },
                |index| Some(if capped && *index == 0 { 2 } else { u32::MAX }),
                |outcome| outcome == PrimaryOutcome::Exhausted,
                || u32::MAX,
            )
            .await;
        assert!(result.is_ok());
        assert_eq!(
            *calls.lock().unwrap(),
            if capped {
                vec![(false, 0, 0), (false, 1, 200), (true, 2, 200)]
            } else {
                vec![
                    (false, 0, 0),
                    (false, 1, 200),
                    (false, 2, 600),
                    (false, 3, 1400),
                    (true, 4, 1400),
                ]
            }
        );
    }
}

#[test]
fn state_read_budget_normalizes_all_boundaries() {
    for (value, expected) in [
        (None, None),
        (Some(0), None),
        (Some(-1), None),
        (Some(i64::MIN), None),
        (Some(1), Some(1)),
        (Some(2), Some(2)),
        (Some(i64::from(u32::MAX)), Some(u32::MAX)),
        (Some(i64::from(u32::MAX) + 1), None),
        (Some(i64::MAX), None),
    ] {
        let policy = RetryPolicy::state_read_override(value);
        assert_eq!(policy.map(|policy| policy.attempts), expected);
        assert_eq!(
            policy.is_some_and(|policy| policy.jitter),
            expected.is_some()
        );
    }
}

#[tokio::test(start_paused = true)]
async fn seeded_cohort_spreads_retries_and_fallback() {
    async fn cohort(policy: RetryPolicy) -> Vec<Vec<(bool, u32, u128)>> {
        let start = Instant::now();
        futures::future::join_all((0..64).map(|client| async move {
            SEEDED_JITTER
                .scope(
                    RefCell::new(StdRng::seed_from_u64(0x5eed + client)),
                    async {
                        let shutdown = AtomicBool::new(false);
                        let notify = Notify::new();
                        let executor = RetryExecutor {
                            policy,
                            deadline: None,
                            shutdown: &shutdown,
                            shutdown_notify: &notify,
                        };
                        let calls = Mutex::new(Vec::new());
                        let result = executor
                            .run(
                                |fallback, index| {
                                    calls.lock().unwrap().push((
                                        fallback,
                                        index,
                                        start.elapsed().as_millis(),
                                    ));
                                    async move { if fallback { Ok(()) } else { Err("503") } }
                                },
                                |_| Some(u32::MAX),
                                |outcome| outcome == PrimaryOutcome::Exhausted,
                                || "cancelled",
                            )
                            .await;
                        assert!(result.is_ok());
                        calls.into_inner().unwrap()
                    },
                )
                .await
        }))
        .await
    }

    for policy in [
        FOREGROUND_POLICY,
        BACKGROUND_POLICY,
        RetryPolicy {
            jitter: false,
            ..BACKGROUND_POLICY
        },
    ] {
        let calls = cohort(policy).await;
        assert_eq!(
            calls,
            cohort(policy).await,
            "seeded execution must replay exactly"
        );
        for client in &calls {
            assert_eq!(client.len(), policy.attempts as usize + 1);
            assert_eq!(client[0], (false, 0, 0));
            for (index, pair) in client[..policy.attempts as usize].windows(2).enumerate() {
                let minimum = 200_u128 << index;
                let maximum = minimum + if policy.jitter { 100 } else { 0 };
                assert!((minimum..=maximum).contains(&(pair[1].2 - pair[0].2)));
                assert_eq!((pair[1].0, pair[1].1), (false, index as u32 + 1));
            }
            let fallback = client.last().unwrap();
            assert_eq!((fallback.0, fallback.1), (true, policy.attempts));
            assert_eq!(fallback.2, client[client.len() - 2].2);
        }
        for attempt in 1..=policy.attempts as usize {
            let times = calls
                .iter()
                .map(|client| client[attempt].2)
                .collect::<BTreeSet<_>>();
            if policy.jitter {
                assert!(times.len() > 1, "attempt {attempt} remained synchronized");
            } else {
                assert_eq!(times.len(), 1, "control should remain synchronized");
            }
        }
    }
}

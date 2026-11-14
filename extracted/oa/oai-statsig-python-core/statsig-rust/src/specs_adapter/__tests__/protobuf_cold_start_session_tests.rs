use super::*;
use std::time::Duration;

use super::super::metadata::DOWNLOAD_PATH_PREFIX;
use super::super::tests::{DeadlineProvider, remote_spec};
use rusty_fork::rusty_fork_test;
use std::sync::atomic::Ordering;

rusty_fork_test! {
    #[test]
    fn cold_start_protobuf_deadline_keeps_completed_values_and_settles_new_links() {
        // Isolate process-wide download permits.
        tokio::runtime::Builder::new_current_thread()
            .enable_all()
            .start_paused(true)
            .build()
            .unwrap()
            .block_on(async {
                let caller_deadline = TokioInstant::now() + Duration::from_secs(1);
                crate::networking::retry::INITIALIZATION_DEADLINE.scope(caller_deadline, async {
                    let healthy_body = br#"{"healthy":true}"#;
                    let (mut healthy, healthy_sha) = remote_spec(healthy_body);
                    let (mut failed, _) = remote_spec(br#"{"pending":true}"#);
                    let provider = DeadlineProvider::new(
                        format!("http://localhost{DOWNLOAD_PATH_PREFIX}{healthy_sha}"), healthy_body,
                    );
                    let hydrator = provider.hydrator();
                    let mut session = hydrator.begin_protobuf_hydration(
                        "http://localhost/v2/download_config_specs/key.json",
                    );
                    let strict_deadline = TokioInstant::from_std(session.started_at + HYDRATION_TIMEOUT);
                    assert_eq!(session.hydration_deadline(), strict_deadline);
                    session.enable_partial_hydration();
                    session.register_spec_references(&healthy).unwrap();
                    session.advance_download_window().await.unwrap();
                    assert!(session.in_flight_downloads.next().now_or_never().is_none());
                    assert_eq!(provider.starts.load(Ordering::Relaxed), 1);

                    session.register_spec_references(&failed).unwrap();
                    session.advance_download_window().await.unwrap();
                    assert_eq!(session.in_flight_downloads.len(), 2);
                    assert_eq!(provider.starts.load(Ordering::Relaxed), 1);
                    tokio::time::advance(session.hydration_deadline() - TokioInstant::now()).await;
                    assert!(TokioInstant::now() < caller_deadline);
                    provider.healthy_ready.notify_one();
                    session.download_registered_references().await.unwrap();

                    assert_eq!(provider.starts.load(Ordering::Relaxed), 1,
                        "cleanup must not start the expired, never-polled GET");
                    assert!(hydrator.in_flight_downloads().is_empty());
                    assert_eq!(session.failed_value_reasons(), vec![HydrationFailureReason::TotalTimeout]);
                    let healthy = session.take_resolved_spec_values(&mut healthy).unwrap();
                    assert_eq!(serde_json::to_value(healthy.default_value).unwrap(),
                        serde_json::json!({"healthy": true}));
                    assert_eq!(healthy.provenance.len(), 1);
                    let failed = session.take_resolved_spec_values(&mut failed).unwrap();
                    assert!(failed.unavailable_slots.contains(&None));
                    assert!(failed.default_value.is_none());
                    assert!(failed.provenance.is_empty());

                    // A large tail can still arrive after the deadline. Each SHA settles once
                    // without scheduling more downloads; duplicate references retain no proof.
                    for index in 0..600 {
                        let (mut later, _) = remote_spec(format!("{{\"later\":{index}}}").as_bytes());
                        session.register_spec_references(&later).unwrap();
                        session.register_spec_references(&later).unwrap();
                        timeout(
                            Duration::from_millis(100),
                            session.advance_download_window(),
                        )
                        .await
                        .unwrap()
                        .unwrap();
                        let later = session.take_resolved_spec_values(&mut later).unwrap();
                        assert!(later.unavailable_slots.contains(&None));
                    }
                    assert_eq!(session.failed_value_reasons().len(), 601);
                    assert_eq!(session.pending_values, 0);
                    assert!(session.in_flight_downloads.is_empty());
                    assert!(session.download_queue.is_empty());

                    let (mut reused, _) = remote_spec(healthy_body);
                    assert!(session.register_spec_references(&reused).unwrap());
                    let reused = session.take_resolved_spec_values(&mut reused).unwrap();
                    assert!(Arc::ptr_eq(
                        &reused.provenance[&healthy_sha],
                        &healthy.provenance[&healthy_sha],
                    ));

                    let (mut conflicting, _) = remote_spec(br#"{"later":0}"#);
                    conflicting
                        .remote_config_metadata
                        .as_mut()
                        .unwrap()
                        .byte_length += 1;
                    let error = session.register_spec_references(&conflicting).unwrap_err();
                    assert_eq!(
                        HydrationFailureReason::from_error(&error),
                        Some(HydrationFailureReason::MetadataConflict),
                    );
                }).await;
            });
    }
}

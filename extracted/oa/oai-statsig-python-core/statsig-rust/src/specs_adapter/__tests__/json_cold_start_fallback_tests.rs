use super::*;
use crate::specs_adapter::remote_config_value_hydrator::cold_start_hydration_deadline;
use crate::specs_adapter::remote_config_value_hydrator::download::ResponseHydrationBudget;
use crate::specs_adapter::remote_config_value_hydrator::tests::{DeadlineProvider, valid_metadata};
use futures::FutureExt;
use rusty_fork::rusty_fork_test;
use std::sync::atomic::Ordering;
use std::time::Duration;

rusty_fork_test! {
    #[test]
    fn cold_start_deadline_json_does_not_admit_queued_downloads() {
        // Fresh process-wide permits keep unrelated tests from consuming the
        // eight slots needed to leave a reference queued at the deadline.
        tokio::runtime::Builder::new_current_thread()
            .enable_all()
            .start_paused(true)
            .build()
            .unwrap()
            .block_on(async {
                let blobs: Vec<_> = (0..10)
                    .map(|index| Blob::new(format!("{{\"index\":{index}}}").as_bytes()))
                    .collect();
                let references: Vec<_> = blobs
                    .iter()
                    .map(|blob| RemoteValueReference {
                        download_url: url::Url::parse(&format!("http://localhost{}", blob.path())).unwrap(),
                        metadata: valid_metadata(blob.sha.clone(), blob.body.len() as u64),
                        occurrences: 1,
                    })
                    .collect();
                let provider = DeadlineProvider::new(references[0].download_url.to_string(), &blobs[0].body);
                provider.healthy_ready.notify_one();
                let hydrator = provider.hydrator();
                let start = tokio::time::Instant::now();
                let caller_deadline = start + Duration::from_millis(80);
                let deadline = crate::networking::retry::INITIALIZATION_DEADLINE.sync_scope(
                    caller_deadline, || cold_start_hydration_deadline(start.into_std()),
                );
                assert!(start < deadline && deadline < caller_deadline);
                let queued = references.last().unwrap().clone();
                let mut downloads = Box::pin(hydrator.download_all_allowing_fallback(
                    references, Some(deadline),
                ));
                assert!(downloads.as_mut().now_or_never().is_none());
                assert_eq!(provider.starts.load(Ordering::Relaxed), 9);

                // Callers share the SHA but have independent hydration and initialization budgets.
                let mut expiring = Box::pin(hydrator.download_one(&queued, Some(deadline)));
                let mut init_expiring = Box::pin(crate::networking::retry::INITIALIZATION_DEADLINE.scope(
                    deadline, hydrator.download_one(&queued, None),
                ));
                let mut live = Box::pin(hydrator.download_one(&queued, None));
                assert!(expiring.as_mut().now_or_never().is_none());
                assert!(init_expiring.as_mut().now_or_never().is_none());
                assert!(live.as_mut().now_or_never().is_none());

                tokio::time::advance(deadline - start).await;
                let (bodies, failures) = downloads.await.unwrap();
                assert_eq!(bodies.len(), 1);
                assert_eq!(bodies[&blobs[0].sha].as_ref(), &blobs[0].body);
                assert_eq!(failures.len(), 9);
                assert!(failures.values().all(|reason| *reason == HydrationFailureReason::TotalTimeout));
                assert_eq!(provider.starts.load(Ordering::Relaxed), 9, "queued GET must not start after the cutoff");
                for error in [expiring.await.unwrap_err(), init_expiring.await.unwrap_err()] {
                    assert_eq!(HydrationFailureReason::from_error(&error), Some(HydrationFailureReason::TotalTimeout));
                }
                assert_eq!(provider.starts.load(Ordering::Relaxed), 9);
                assert!(live.as_mut().now_or_never().is_none());
                assert_eq!(provider.starts.load(Ordering::Relaxed), 10, "the other caller can still fetch");
                drop(live);
                assert!(hydrator.in_flight_downloads().is_empty());
            });
    }
}

#[tokio::test(start_paused = true)]
async fn json_cold_start_fallback_settles_missing_blobs_when_response_budget_is_unavailable() {
    for (close_budget, expected_reason) in [
        (false, HydrationFailureReason::TotalTimeout),
        (true, HydrationFailureReason::DownloadFailed),
    ] {
        let server = MockServer::start().await;
        let missing = Blob::new(br#"{"missing":"remote"}"#);
        let other_missing = Blob::new(br#"{"other":"remote"}"#);
        let reused = Blob::new(br#"{"reused":"healthy"}"#);
        let mut failed_rule = rule("failed-rule", missing.placeholder());
        failed_rule["remoteConfigMetadata"] = missing.metadata();
        let mut healthy_rule = rule("healthy-rule", reused.placeholder());
        healthy_rule["remoteConfigMetadata"] = reused.metadata();
        let configs = json!({
            "missing_default": remote_config(&other_missing),
            "mixed_rules": config(json!({"inline": "default"}), vec![
                rule("inline-first", json!({"inline": "first"})), failed_rule, healthy_rule,
            ]),
        });
        let original = full_wire(&configs.to_string());
        let mut hydrator = test_hydrator("json-cold-start-fallback-budget");
        let budget = Arc::new(ResponseHydrationBudget::new(1));
        let _held_budget = budget.reserve(1).await.unwrap();
        if close_budget {
            budget.bytes.close();
        }
        hydrator.response_budget = budget;
        let metadata = valid_metadata(reused.sha.clone(), reused.body.len() as u64);
        let reused_value =
            VerifiedRemoteValue::from_verified_json_body(metadata, &reused.body).unwrap();
        let current_verified_values = VerifiedRemoteConfigValues::from([(
            InternedString::from_str_ref("reused"),
            Arc::new(VerifiedRemoteValues::from([(
                reused.sha.clone(),
                Arc::new(reused_value),
            )])),
        )]);
        for capture in [false, true] {
            let mut data = ResponseData::from_bytes(original.clone());
            let update = hydrator
                .prepare_json_store_update(
                    &mut data,
                    StoreHydrationOptions::new(
                        &format!("{}/v2/download_config_specs/key.json", server.uri()),
                        MmapProjectId::for_sdk_key("json-cold-start-fallback-budget"),
                    )
                    .with_data_store_capture(capture)
                    .with_partial_full_response(true),
                    &current_verified_values,
                    None,
                )
                .await
                .unwrap()
                .unwrap();
            let partial = update.partial_hydration.unwrap();
            assert_eq!(
                partial.failed_blobs,
                HashMap::from([
                    (missing.sha.clone(), expected_reason),
                    (other_missing.sha.clone(), expected_reason)
                ])
            );
            let snapshot = serde_json::to_value(update.values).unwrap();
            let configs = &snapshot["dynamic_configs"];
            let slots = &partial.unavailable;
            assert_eq!(slots.len(), 2);
            let default = InternedString::from_str_ref("missing_default");
            let mixed = InternedString::from_str_ref("mixed_rules");
            assert_eq!(slots[&default], std::collections::HashSet::from([None]));
            assert_eq!(slots[&mixed], std::collections::HashSet::from([Some(1)]));
            let rules = &configs["mixed_rules"]["rules"];
            assert_eq!(rules[0]["returnValue"], json!({"inline": "first"}));
            assert_eq!(rules[2]["returnValue"], json!({"reused": "healthy"}));
            assert_eq!(
                configs["mixed_rules"]["defaultValue"],
                json!({"inline": "default"})
            );
            assert!(update.verified_remote_values[&default].is_empty());
            let proofs = &update.verified_remote_values[&mixed];
            assert_eq!(proofs.len(), 1);
            assert!(proofs.contains_key(&reused.sha));
            assert_eq!(data.read_to_bytes().unwrap(), original);
        }
        assert!(server.received_requests().await.unwrap().is_empty());
    }
}

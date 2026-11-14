use super::*;

fn source_with_remote_rule(
    server: &MockServer,
    path: &str,
    sha: &str,
) -> Arc<CursorRecordingSource> {
    let mut payload: serde_json::Value =
        serde_json::from_slice(&remote_payload(path, sha, 2)).unwrap();
    let config = &mut payload["dynamic_configs"]["remote_config"];
    config["rules"] = serde_json::json!([{
        "name": "remote-rule", "id": "remote-rule", "passPercentage": 100.0,
        "conditions": [], "idType": "userID",
        "returnValue": config["defaultValue"],
        "remoteConfigMetadata": config["remoteConfigMetadata"]
    }]);
    CursorRecordingSource::new(Arc::new(RemotePayloadSource {
        payload: Arc::from(serde_json::to_vec(&payload).unwrap()),
        trusted_source_url: format!("{}/v2/download_config_specs", server.uri()),
    }))
}

async fn mount_blob(server: &MockServer, blob_path: &str, body: &str, count: u64) {
    Mock::given(method("GET"))
        .and(path(blob_path))
        .respond_with(ResponseTemplate::new(200).set_body_raw(body, "application/json"))
        .expect(count)
        .mount(server)
        .await;
}

fn increment_tags(observer: &RecordingObserver, name: &str) -> Vec<RecordedTags> {
    observer
        .increments
        .lock()
        .iter()
        .filter(|(metric, _)| metric == name)
        .map(|(_, tags)| tags.clone())
        .collect()
}

#[tokio::test]
async fn scoped_cold_start_accepts_degraded_snapshot_and_repairs_unchanged_metadata() {
    let server = MockServer::start().await;
    let sha: String = Sha256::digest(b"{}")
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect();
    let blob_path = format!("/v1/dynamic_config_value/{sha}");
    mount_blob(&server, &blob_path, "[]", 2).await;
    let remote = source_with_remote_rule(&server, &blob_path, &sha);
    let instance = "scoped-cold-repair";
    let adapter = Arc::new(ScopedSourceSpecsAdapter::new(remote.clone(), instance));
    let observer = Arc::new(RecordingObserver::default());
    adapter.bind_observability_client(observer.clone());
    let mut store = SpecStore::new(
        instance,
        instance.into(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    );
    store.enable_partial_blob_publication = true;
    let store = Arc::new(store);
    adapter.initialize(store.clone());
    adapter
        .clone()
        .start(&StatsigRuntime::get_runtime())
        .await
        .unwrap();
    assert!(store.get_current_values().is_none());
    assert!(store.needs_blob_hydration_repair());
    assert!(increment_tags(&observer, "statsig.sdk.scoped_snapshot.rejection.count").is_empty());
    let results = increment_tags(&observer, "statsig.sdk.remote_config_hydration.result");
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].as_ref().unwrap()["outcome"], "degraded");
    let refresh = increment_tags(&observer, "statsig.sdk.scoped_snapshot.refresh.count");
    let refresh = refresh[0].as_ref().unwrap();
    assert_eq!(refresh["result"], "updated");
    assert_eq!(refresh["fallback"], "false");

    let stale = CursorRecordingSource::new(source(122, "older"));
    let older_adapter = ScopedSourceSpecsAdapter::new(stale.clone(), "older");
    older_adapter.initialize(store.clone());
    assert!(!older_adapter.sync_impl(&mut None).await.unwrap());
    assert_eq!(stale.payload_fetches.load(Ordering::Relaxed), 0);
    adapter.sync_impl(&mut None).await.unwrap();
    let published = store.get_published_specs_info();
    assert_eq!(published.lcut, Some(123));
    assert_eq!(published.checksum.as_deref(), Some("hydrated-checksum"));
    let failures = increment_tags(
        &observer,
        "statsig.sdk.remote_config_hydration.unavailable_blob",
    );
    assert_eq!(
        failures.len(),
        1,
        "one SHA shared by default and rule over two failed polls"
    );
    let tags = failures[0].as_ref().unwrap();
    assert_eq!(tags["format"], "json");
    assert_eq!(tags["failure_reason"], "checksum_mismatch");
    server.verify().await;
    server.reset().await;

    mount_blob(&server, &blob_path, "{}", 1).await;
    assert!(adapter.sync_impl(&mut None).await.unwrap());
    let repaired = store.get_current_values().expect("complete offline export");
    let config = repaired
        .dynamic_configs
        .get(&InternedString::from_str_ref("remote_config"))
        .unwrap()
        .as_spec_ref();
    assert!(config.default_value.get_json().unwrap().is_empty());
    assert!(config.rules[0].return_value.get_json().unwrap().is_empty());
    assert_eq!(remote.payload_fetches.load(Ordering::Relaxed), 3);
    for (source, polls) in [(remote, 3), (stale, 1)] {
        let cursors = source.cursors.lock();
        assert_eq!(cursors.len(), polls);
        assert!(
            cursors
                .iter()
                .all(|cursor| cursor.lcut == Some(0) && cursor.checksum.is_none())
        );
    }
    let repaired = store.get_current_specs_info();
    assert_eq!(repaired.lcut, published.lcut);
    assert_eq!(repaired.checksum, published.checksum);
}

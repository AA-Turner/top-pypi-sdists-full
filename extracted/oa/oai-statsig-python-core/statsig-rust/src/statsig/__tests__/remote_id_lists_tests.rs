use super::*;
use crate::StatsigUser;

const PILOT_LISTS: &str = r#"{"qa":"userID","remote":"userID","extra":"userID"}"#;

fn rerun_with_pilot_env(name: &str) -> bool {
    rerun_with_allowlist(name, PILOT_LISTS)
}

// Re-exec this test with deployment settings in place before the SDK starts worker threads.
fn rerun_with_allowlist(name: &str, allowlist: &str) -> bool {
    if std::env::var("STATSIG_RUST_REMOTE_ID_LISTS_ENABLED").as_deref() == Ok("1")
        && std::env::var("STATSIG_RUST_REMOTE_ID_LIST_ALLOWLIST").as_deref() == Ok(allowlist)
    {
        return false;
    }
    let status = std::process::Command::new(std::env::current_exe().unwrap())
        .args(["--exact", name])
        .env("STATSIG_RUST_REMOTE_ID_LISTS_ENABLED", "1")
        .env("STATSIG_RUST_REMOTE_ID_LIST_ALLOWLIST", allowlist)
        .status()
        .unwrap();
    assert!(status.success(), "isolated pilot test failed: {status}");
    true
}

fn options_with_id_lists() -> StatsigOptions {
    StatsigOptions {
        enable_id_lists: Some(true),
        ..Default::default()
    }
}

fn test_resolver() -> Arc<RemoteIdListResolver> {
    let opts = Arc::new(StatsigOptions::default());
    let runtime = StatsigRuntime::get_runtime();
    let client = Arc::new(RemoteIdListResolver::new(
        &opts,
        &Arc::new(OpsStatsForInstance::new()),
        url::Url::parse("http://127.0.0.1/v1/id_list_membership").unwrap(),
        "secret-test",
        &runtime,
        None,
        RemoteIdListAllowlist::from_json(r#"{"qa":"userID","remote":"userID"}"#).unwrap(),
    ));
    client.observe_manifest(&test_manifest(10));
    client
}

fn test_manifest(size: u64) -> crate::id_lists_adapter::IdListManifest {
    serde_json::from_value(serde_json::json!({
        "qa": {"name":"qa", "url":"http://127.0.0.1/qa", "fileID":"qa", "creationTime":1, "size":size},
        "remote": {"name":"remote", "url":"http://127.0.0.1/remote", "fileID":"remote", "creationTime":1, "size":10}
    })).unwrap()
}

fn pending_entry(
    client: &RemoteIdListResolver,
    cache: &RemoteIdListCache,
    list: &str,
    id: &str,
) -> Arc<MembershipCacheEntry> {
    let CachedLookup::Pending { entry, start: true } = cache.entry_for(client, list, "userID", id)
    else {
        panic!("expected a new pending entry");
    };
    entry
}

fn finish_matching(entry: &MembershipCacheEntry, client: &RemoteIdListResolver, member: bool) {
    let revision = *entry.observed_revision.as_deref().unwrap();
    entry.finish(
        client,
        Some(MembershipAnswer {
            is_member: member,
            revision: Some(revision),
        }),
    );
}

#[test]
fn pilot_respects_network_and_adapter_options() {
    if rerun_with_pilot_env(rusty_fork::rusty_fork_test_name!(
        pilot_respects_network_and_adapter_options
    )) {
        return;
    }
    let lists_disabled = StatsigOptions {
        enable_id_lists: Some(false),
        ..Default::default()
    };
    let custom_lists = StatsigOptions {
        id_lists_adapter: Some(Arc::new(crate::StatsigHttpIdListsAdapter::new(
            "secret-test",
            &lists_disabled,
        ))),
        ..lists_disabled.clone()
    };
    let offline = StatsigOptions {
        disable_network: Some(true),
        ..options_with_id_lists()
    };
    for (options, has_adapter, compares) in [
        (StatsigOptions::default(), false, false),
        (lists_disabled, false, false),
        (options_with_id_lists(), true, true),
        (offline, true, false),
        (custom_lists, true, true),
    ] {
        let sdk = Statsig::new("secret-test", Some(Arc::new(options)));
        assert_eq!(sdk.id_lists_adapter.adapter().is_some(), has_adapter);
        assert_eq!(sdk.remote_id_list_resolver.is_some(), compares);
    }
}

#[cfg(feature = "ffi-support")]
#[test]
fn only_opted_in_bulk_calls_give_each_evaluation_the_same_deadline() {
    if rerun_with_pilot_env(rusty_fork::rusty_fork_test_name!(
        only_opted_in_bulk_calls_give_each_evaluation_the_same_deadline
    )) {
        return;
    }
    for (options, enabled) in [
        (StatsigOptions::default(), false),
        (options_with_id_lists(), true),
    ] {
        let sdk = Statsig::new("secret-test", Some(Arc::new(options)));
        let user = StatsigUser::with_user_id("test-id");
        let internal = StatsigUserInternal::new(&user, Some(&sdk));
        let data = sdk.spec_store.load_data();

        let session_deadline = |user: &StatsigUserInternal| {
            sdk.create_standard_eval_context(user, &data, None, None, false)
                .remote_id_lists
                .and_then(|session| session.deadline)
        };
        assert_eq!(session_deadline(&internal), None);

        let bulk = internal.with_membership_deadline(&sdk);
        let first = session_deadline(&bulk);
        assert_eq!(first.is_some(), enabled);
        assert_eq!(first, session_deadline(&bulk));
    }
}

#[cfg(all(feature = "reqwest", not(feature = "custom_network_provider")))]
async fn sdk_with_membership_specs(proxy: &wiremock::MockServer, specs: String) -> Statsig {
    use crate::{SpecsAdapter, StatsigBootstrapSpecsAdapter};

    let sdk = Statsig::new(
        "secret-test",
        Some(Arc::new(StatsigOptions {
            id_lists_url: Some(proxy.uri()),
            disable_all_logging: Some(true),
            ..options_with_id_lists()
        })),
    );
    let specs = Arc::new(StatsigBootstrapSpecsAdapter::new(specs));
    specs.initialize(sdk.spec_store.clone());
    specs.start(&sdk.statsig_runtime).await.unwrap();
    sdk
}

#[cfg(all(feature = "reqwest", not(feature = "custom_network_provider")))]
#[tokio::test]
async fn get_layer_shares_its_membership_wait_across_shared_control_experiments() {
    if rerun_with_pilot_env(rusty_fork::rusty_fork_test_name!(
        get_layer_shares_its_membership_wait_across_shared_control_experiments
    )) {
        return;
    }
    use serde_json::json;
    use wiremock::matchers::{method, path};
    use wiremock::{Mock, MockServer, ResponseTemplate};

    let proxy = MockServer::start().await;
    let calls = Mock::given(method("POST"))
        .and(path("/v1/id_list_membership"))
        .respond_with(ResponseTemplate::new(200).set_delay(Duration::from_secs(1)))
        .expect(3)
        .mount_as_scoped(&proxy)
        .await;
    let mut specs = json!({
        "time": 1, "has_updates": true, "feature_gates": {}, "experiment_to_layer": {},
        "dynamic_configs": {}, "condition_map": {},
        "layer_configs": {"shared": {
            "type": "layer", "entity": "layer", "idType": "userID", "enabled": true,
            "salt": "shared", "defaultValue": {}, "useNewLayerEval": true,
            "rules": [{"name": "shared", "id": "shared", "conditions": [], "returnValue": {},
                "passPercentage": 100, "idType": "userID", "sharedControlExperiments": []}]
        }}
    });
    for name in ["qa", "remote", "extra"] {
        specs["condition_map"][name] = json!({
            "type": "unit_id", "operator": "not_in_segment_list", "targetValue": name, "idType": "userID"
        });
        specs["dynamic_configs"][name] = json!({
            "type": "dynamic_config", "entity": "experiment", "idType": "userID",
            "enabled": true, "isActive": true, "salt": name, "defaultValue": {},
            "rules": [{"name": "control", "id": "control", "conditions": [name], "returnValue": {},
                "passPercentage": 100, "idType": "userID", "isExperimentGroup": true}]
        });
        specs["layer_configs"]["shared"]["rules"][0]["sharedControlExperiments"]
            .as_array_mut()
            .unwrap()
            .push(json!({"name": name, "controlGroupID": "control"}));
    }
    let sdk = sdk_with_membership_specs(&proxy, specs.to_string()).await;

    let user = StatsigUser::with_user_id("test-id");
    let start = Instant::now();
    let layer = sdk.get_layer(&user, "shared");
    let elapsed = start.elapsed();
    assert_eq!(layer.__shared_control_exposures.len(), 3);
    assert!(
        (SERVE_WAIT..2 * SERVE_WAIT).contains(&elapsed),
        "get_layer took {elapsed:?}"
    );
    tokio::time::timeout(Duration::from_secs(5), calls.wait_until_satisfied())
        .await
        .unwrap();
}

#[test]
fn shutdown_only_closes_the_resolvers_own_network() {
    if rerun_with_pilot_env(rusty_fork::rusty_fork_test_name!(
        shutdown_only_closes_the_resolvers_own_network
    )) {
        return;
    }
    use std::sync::atomic::Ordering;

    let sdk = Statsig::new("secret-test", Some(Arc::new(options_with_id_lists())));
    let shared = sdk.id_lists_adapter.network().unwrap();
    let resolver = sdk.remote_id_list_resolver.as_ref().unwrap();
    assert!(std::ptr::eq(
        resolver.network_for_lookup().unwrap(),
        shared.as_ref()
    ));
    resolver.shutdown();
    assert!(!shared.shutdown_flag().load(Ordering::Relaxed));
    assert!(resolver.session(None).is_none());

    let cold = test_resolver();
    cold.shutdown();
    assert!(cold.network_for_lookup().is_none());

    let resolver = test_resolver();
    let owned = resolver.network_for_lookup().unwrap();
    resolver.shutdown();
    assert!(owned.shutdown_flag().load(Ordering::Relaxed));
}

#[test]
fn shutdown_can_finish_while_the_owned_client_is_initializing() {
    use std::sync::mpsc;

    let resolver = test_resolver();
    let MembershipNetwork::Owned {
        client,
        sdk_key,
        options,
    } = &resolver.network
    else {
        panic!("expected an owned client");
    };
    std::thread::scope(|scope| {
        let resolver = &resolver;
        let network = client.get_or_init(|| {
            let (finished, shutdown) = mpsc::channel();
            scope.spawn(move || {
                resolver.shutdown();
                let _ = finished.send(());
            });
            shutdown
                .recv_timeout(Duration::from_secs(5))
                .expect("shutdown waited for client initialization");
            NetworkClient::with_sdk_headers(sdk_key, options)
        });
        assert!(network.is_none());
    });
}

#[cfg(all(feature = "reqwest", not(feature = "custom_network_provider")))]
#[tokio::test(flavor = "current_thread")]
async fn synchronous_membership_lookup_uses_the_sdk_runtime() {
    if rerun_with_pilot_env(rusty_fork::rusty_fork_test_name!(
        synchronous_membership_lookup_uses_the_sdk_runtime
    )) {
        return;
    }
    use crate::networking::{HttpMethod, RequestArgs};
    use wiremock::matchers::{method, path};
    use wiremock::{Mock, MockServer, ResponseTemplate};

    let proxy = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/list_body"))
        .respond_with(ResponseTemplate::new(200).set_body_string("list"))
        .expect(1)
        .mount(&proxy)
        .await;
    Mock::given(method("POST"))
        .and(path("/v1/id_list_membership"))
        .respond_with(ResponseTemplate::new(200).set_body_json(serde_json::json!({
            "is_member": true
        })))
        .expect(2)
        .mount(&proxy)
        .await;
    let sdk = Statsig::new(
        "secret-test",
        Some(Arc::new(StatsigOptions {
            id_lists_url: Some(proxy.uri()),
            ..options_with_id_lists()
        })),
    );
    let resolver = sdk.remote_id_list_resolver.as_ref().unwrap();
    let response = resolver
        .network_for_lookup()
        .unwrap()
        .request_once(
            HttpMethod::GET,
            RequestArgs {
                url: format!("{}/list_body", proxy.uri()),
                ..Default::default()
            },
            None,
            true,
            true,
            0,
        )
        .await
        .unwrap();
    assert_eq!(response.status_code, Some(200));
    // Let the caller's connection driver return its socket to the idle pool.
    tokio::time::sleep(Duration::from_millis(20)).await;
    let user = StatsigUser::with_user_id("id");
    let internal = crate::user::StatsigUserInternal::new(&user, Some(&sdk));

    // Give the fixture time to respond even on a busy CI runner. The production
    // wait budget is covered by the test below.
    let deadline = Some(Instant::now() + Duration::from_secs(5));
    let mut evaluation = resolver.session(deadline).unwrap();
    // A legacy SFP can answer without a revision. Share that reply within this
    // evaluation; a fresh evaluation with the same user must request it again.
    for _ in 0..2 {
        assert_eq!(
            evaluation.lookup(&internal, "qa", "userID", "id", None),
            Some(true)
        );
    }
    let mut next = resolver.session(deadline).unwrap();
    assert_eq!(
        next.lookup(&internal, "qa", "userID", "id", None),
        Some(true)
    );

    let cache = evaluation.cache_for(&internal);
    let io = sdk.statsig_runtime.try_get_owned_runtime_handle().unwrap();
    let entries = cache.lists.load();
    let entry = entries.get("qa").unwrap();
    assert_eq!(entry.runtime_id.get(), Some(&io.id()));
    let _sdk_runtime = io.enter();
    assert!(!entry.can_block_caller());
}

#[cfg(all(feature = "reqwest", not(feature = "custom_network_provider")))]
async fn mock_membership_list(proxy: &wiremock::MockServer) -> serde_json::Value {
    use wiremock::matchers::{method, path};
    use wiremock::{Mock, ResponseTemplate};

    let manifest = serde_json::json!({"qa":{
        "fileID":"qa", "name":"qa", "size":10, "creationTime":1, "url":format!("{}/qa", proxy.uri())
    }});
    Mock::given(method("POST"))
        .and(path("/v1/get_id_lists"))
        .respond_with(ResponseTemplate::new(200).set_body_json(&manifest))
        .mount(proxy)
        .await;
    Mock::given(method("GET"))
        .and(path("/qa"))
        .respond_with(
            ResponseTemplate::new(206)
                .insert_header("content-range", "bytes 0-9/10")
                .set_body_string("+aaaaaaaa\n"),
        )
        .mount(proxy)
        .await;
    manifest
}

#[cfg(all(feature = "reqwest", not(feature = "custom_network_provider")))]
async fn poll_lists(sdk: &Statsig) -> Result<(), crate::StatsigErr> {
    sdk.id_lists_adapter
        .adapter()
        .unwrap()
        .start(&sdk.statsig_runtime, sdk.spec_store.clone())
        .await
}

#[cfg(all(feature = "reqwest", not(feature = "custom_network_provider")))]
async fn fail_next_manifest(proxy: &wiremock::MockServer, status: u16) {
    use wiremock::matchers::{method, path};
    use wiremock::{Mock, ResponseTemplate};

    Mock::given(method("POST"))
        .and(path("/v1/get_id_lists"))
        .respond_with(ResponseTemplate::new(status))
        .with_priority(1)
        .up_to_n_times(1)
        .mount(proxy)
        .await;
}

#[cfg(all(feature = "reqwest", not(feature = "custom_network_provider")))]
#[tokio::test]
async fn shared_base_worker_reuses_membership_across_manifest_routes() {
    if rerun_with_pilot_env(rusty_fork::rusty_fork_test_name!(
        shared_base_worker_reuses_membership_across_manifest_routes
    )) {
        return;
    }
    use wiremock::matchers::{method, path};
    use wiremock::{Mock, MockServer, ResponseTemplate};

    let proxy = MockServer::start().await;
    let directory = tempfile::tempdir().unwrap();
    let options = StatsigOptions {
        shared_id_lists_dir: Some(directory.path().to_str().unwrap().to_owned()),
        fallback_to_statsig_api: Some(true),
        id_lists_url: Some(format!("{}/v1/get_id_lists", proxy.uri())),
        state_read_primary_attempts: Some(1),
        ..options_with_id_lists()
    };
    let sdk = crate::id_lists_adapter::TEST_CDN_MANIFEST_URL
        .sync_scope(format!("{}/cdn", proxy.uri()), || {
            Statsig::new("secret-shared", Some(Arc::new(options)))
        });
    let resolver = sdk.remote_id_list_resolver.as_ref().unwrap();
    let manifest = mock_membership_list(&proxy).await;
    poll_lists(&sdk).await.unwrap();
    let cache = RemoteIdListCache::new(resolver);
    finish_matching(&pending_entry(resolver, &cache, "qa", "id"), resolver, true);

    // The CDN first advertises the same list, then removes it. A failed poll
    // between those observations keeps the last successful revision.
    let removed = serde_json::json!({});
    for (status, cdn_manifest) in [(503, &manifest), (401, &manifest), (503, &removed)] {
        if status == 503 {
            Mock::given(method("GET"))
                .and(path("/cdn"))
                .respond_with(ResponseTemplate::new(200).set_body_json(cdn_manifest))
                .up_to_n_times(1)
                .expect(1)
                .mount(&proxy)
                .await;
        }
        fail_next_manifest(&proxy, status).await;
        assert_eq!(poll_lists(&sdk).await.is_ok(), status == 503);
        let lookup = cache.entry_for(resolver, "qa", "userID", "id");
        assert_eq!(
            matches!(lookup, CachedLookup::Ready(Some(true))),
            cdn_manifest.get("qa").is_some()
        );
    }
}

#[cfg(all(feature = "reqwest", not(feature = "custom_network_provider")))]
#[tokio::test]
async fn only_shared_eager_workers_expire_membership_after_failed_manifest_polls() {
    if rerun_with_pilot_env(rusty_fork::rusty_fork_test_name!(
        only_shared_eager_workers_expire_membership_after_failed_manifest_polls
    )) {
        return;
    }
    async fn advance(seconds: u64) {
        tokio::time::pause();
        tokio::time::advance(Duration::from_secs(seconds)).await;
        tokio::time::resume();
    }
    let directory = tempfile::tempdir().unwrap();
    let proxy = wiremock::MockServer::start().await;
    mock_membership_list(&proxy).await;
    for (shared, lazy, interval_ms, window, expires) in [
        (true, false, 1_000, 180, true),
        (true, false, 90_000, 270, true),
        (false, false, 1_000, 180, false),
        (true, true, 1_000, 180, false),
    ] {
        let options = StatsigOptions {
            shared_id_lists_dir: shared.then(|| directory.path().to_str().unwrap().to_owned()),
            lazy_load_id_lists: Some(lazy),
            id_lists_sync_interval_ms: Some(interval_ms),
            id_lists_url: Some(format!("{}/v1/get_id_lists", proxy.uri())),
            ..options_with_id_lists()
        };
        let sdk = Statsig::new("secret-test", Some(Arc::new(options)));
        let resolver = sdk.remote_id_list_resolver.as_ref().unwrap();
        let cache = RemoteIdListCache::new(resolver);
        let cached = || cache.entry_for(resolver, "qa", "userID", "id");
        let next_request = || pending_entry(resolver, &cache, "qa", "id");
        poll_lists(&sdk).await.unwrap();
        finish_matching(&next_request(), resolver, true);

        advance(window - 10).await;
        poll_lists(&sdk).await.unwrap(); // The same manifest renews the window.
        advance(window - 10).await;
        fail_next_manifest(&proxy, 401).await;
        assert!(poll_lists(&sdk).await.is_err());
        assert!(matches!(cached(), CachedLookup::Ready(Some(true))));

        advance(20).await;
        fail_next_manifest(&proxy, 401).await;
        assert!(poll_lists(&sdk).await.is_err());
        if expires {
            next_request();
            poll_lists(&sdk).await.unwrap();
            finish_matching(&next_request(), resolver, false);
            assert!(matches!(cached(), CachedLookup::Ready(Some(false))));
        } else {
            assert!(matches!(cached(), CachedLookup::Ready(Some(true))));
        }
    }
}

#[test]
fn joins_an_inflight_lookup_and_uses_one_wait_budget_for_selected_lists() {
    let client = test_resolver();
    let mut evaluation = client.session(None).unwrap();
    let user = StatsigUser::with_user_id("id");
    let internal = StatsigUserInternal::new(&user, None);
    let cache = evaluation.cache_for(&internal);
    let qa = pending_entry(&client, cache, "qa", "id");
    pending_entry(&client, cache, "remote", "id");
    assert_eq!(
        evaluation.lookup(&internal, "qa", "userID", "id", None),
        None
    );
    let first = evaluation.deadline.unwrap();
    assert_eq!(
        evaluation.lookup(&internal, "remote", "userID", "id", None),
        None
    );
    assert_eq!(evaluation.deadline, Some(first));

    qa.finish(&client, None);
    assert!(matches!(
        qa.cached_lookup(true),
        Some(CachedLookup::Ready(None))
    ));
    let next = client.session(None).unwrap();
    pending_entry(&client, next.cache_for(&internal), "qa", "id");
}

#[test]
fn user_cache_is_scoped_to_its_sdk_and_identity() {
    let cache_for = |resolver: &Arc<RemoteIdListResolver>, user: &StatsigUser| {
        let internal = StatsigUserInternal::new(user, None);
        let eval = resolver.session(None).unwrap();
        Arc::clone(eval.cache_for(&internal))
    };
    let mut user = StatsigUser::with_user_id("first");
    let first = test_resolver();
    let second = test_resolver();
    let original = cache_for(&first, &user);
    assert!(!Arc::ptr_eq(&original, &cache_for(&second, &user)));
    assert!(Arc::ptr_eq(&original, &cache_for(&first, &user.clone())));

    first.shutdown();
    let shared = cache_for(&second, &user);
    assert!(Arc::ptr_eq(&shared, &cache_for(&second, &user)));
    user.set_user_id("changed");
    assert!(!Arc::ptr_eq(&shared, &cache_for(&second, &user)));
}

#[test]
fn concurrent_misses_start_one_request() {
    let client = test_resolver();
    let cache = RemoteIdListCache::new(&client);
    let barrier = std::sync::Barrier::new(2);
    let lookup = || {
        barrier.wait();
        let CachedLookup::Pending { entry, start } = cache.entry_for(&client, "qa", "userID", "id")
        else {
            panic!("expected a pending entry");
        };
        (entry, start)
    };
    std::thread::scope(|scope| {
        let other = scope.spawn(lookup);
        let (entry, start) = lookup();
        let (other_entry, other_start) = other.join().unwrap();
        assert!(Arc::ptr_eq(&entry, &other_entry));
        assert_ne!(start, other_start);
    });
}

#[test]
fn manifest_changes_invalidate_only_the_affected_entries() {
    let client = test_resolver();
    let cache = RemoteIdListCache::new(&client);
    let old = pending_entry(&client, &cache, "qa", "id");
    let unaffected = pending_entry(&client, &cache, "remote", "id");
    finish_matching(&unaffected, &client, true);

    client.observe_manifest(&test_manifest(20));
    let current = pending_entry(&client, &cache, "qa", "id");
    finish_matching(&current, &client, false);
    finish_matching(&old, &client, true);
    assert!(matches!(
        cache.entry_for(&client, "qa", "userID", "id"),
        CachedLookup::Ready(Some(false))
    ));
    assert!(matches!(
        cache.entry_for(&client, "remote", "userID", "id"),
        CachedLookup::Ready(Some(true))
    ));

    client.observe_manifest(&Default::default());
    client.observe_manifest(&test_manifest(20));
    pending_entry(&client, &cache, "qa", "id");
}

#[test]
fn cached_answers_require_matching_revisions_and_identities() {
    let client = test_resolver();
    let cache = RemoteIdListCache::new(&client);
    for revision in [None, Some(*client.revisions.get("remote").unwrap())] {
        let entry = pending_entry(&client, &cache, "qa", "id");
        entry.finish(
            &client,
            Some(MembershipAnswer {
                is_member: true,
                revision,
            }),
        );
    }
    let matching = pending_entry(&client, &cache, "qa", "id");
    finish_matching(&matching, &client, true);
    assert!(matches!(
        cache.entry_for(&client, "qa", "userID", "id"),
        CachedLookup::Ready(Some(true))
    ));
    pending_entry(&client, &cache, "qa", "changed-id");
}

#[cfg(all(feature = "reqwest", not(feature = "custom_network_provider")))]
#[tokio::test]
async fn duplicate_allowlist_keys_keep_membership_local() {
    if rerun_with_allowlist(
        rusty_fork::rusty_fork_test_name!(duplicate_allowlist_keys_keep_membership_local),
        r#"{"company_id_list":"userID","company_id_list":"companyID"}"#,
    ) {
        return;
    }
    use crate::id_lists_adapter::{IdListMetadata, IdListUpdate, IdListsUpdateListener};

    let proxy = wiremock::MockServer::start().await;
    let sdk = sdk_with_membership_specs(
        &proxy,
        include_str!("../../../tests/data/eval_proj_dcs.json").into(),
    )
    .await;
    let mut manifest: HashMap<String, IdListMetadata> =
        serde_json::from_str(include_str!("../../../tests/data/get_id_lists.json")).unwrap();
    sdk.spec_store.did_receive_id_list_updates(HashMap::from([(
        "company_id_list".into(),
        IdListUpdate {
            raw_changeset: Some(include_str!("../../../tests/data/company_id_list").into()),
            new_metadata: manifest.remove("company_id_list").unwrap(),
        },
    )]));
    let member = StatsigUser::with_custom_ids(HashMap::from([("companyID", "marcos_1")]));
    assert!(sdk.check_gate(&member, "segment:company_id_list"));
    assert!(proxy.received_requests().await.unwrap().is_empty());
}

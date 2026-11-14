use super::*;
use wiremock::matchers::query_param;

#[derive(Clone, Copy, PartialEq, Eq)]
enum BlobDelta {
    AllConfigs,
    BadChecksum,
    CarryPending,
    LayerDelegate,
    DependentGate,
    RemovedCondition,
}

fn crc_envelope(
    kind: pb::SpecsEnvelopeKind,
    name: &str,
    message: impl Message,
) -> pb::SpecsEnvelope {
    let bytes = message.encode_to_vec();
    envelope(kind, name, &crc32(&bytes).to_string(), bytes)
}

fn targeted_rule(id: &str, value: pb::ReturnValue) -> pb::Rule {
    pb::Rule {
        name: id.into(),
        id: id.into(),
        id_type: Some(user_id_type()),
        pass_percentage: 100,
        conditions: vec!["shared-target".into()],
        return_value: Some(value),
        ..Default::default()
    }
}

fn gate(name: &str, default: bool, rules: Vec<pb::Rule>) -> pb::SpecsEnvelope {
    let spec = pb::Spec {
        enabled: true,
        entity: pb::EntityType::EntityFeatureGate as i32,
        id_type: Some(user_id_type()),
        default_value: Some(pb::ReturnValue {
            value: Some(return_value::Value::BoolValue(default)),
        }),
        rules,
        ..Default::default()
    };
    crc_envelope(pb::SpecsEnvelopeKind::FeatureGate, name, spec)
}

fn four_blob_response(
    generation: u64,
    blobs: Option<&[RemoteValue; 4]>,
    mode: BlobDelta,
) -> SpecsResponse {
    use pb::SpecsEnvelopeKind as Kind;
    let delta = blobs.is_some();
    let mut frames = Vec::new();
    if delta {
        frames.push(pb::SpecsEnvelope {
            kind: Kind::CopyPrev as i32,
            ..Default::default()
        });
    }
    let mut top = top(generation, delta);
    if mode == BlobDelta::DependentGate {
        let mut header = pb::SpecsTopLevel::decode(top.data.as_deref().unwrap()).unwrap();
        let mapping = |destination: &str| json!([{"new_config_name": destination, "rules": [{"rule_name":"public"}]}]);
        let mut mappings = json!({"healthy_alias": mapping("ordinary_config")});
        if delta {
            mappings["new_d"] = mapping("new_d::pipeline");
        }
        header.rest = serde_json::to_vec(&json!({
            "experiment_to_layer": {},
            "override_rules": {"public": {
                "name":"public", "id":"public", "passPercentage":100, "idType":"userID",
                "conditions":[], "returnValue":true
            }},
            "overrides": mappings
        }))
        .unwrap();
        top.data = Some(header.encode_to_vec());
    }
    frames.push(top);
    let mut targeting = if mode == BlobDelta::DependentGate {
        let mut gate_rules = Vec::new();
        if generation == 3 {
            let email = pb::Condition {
                condition_type: pb::ConditionType::UserField as i32,
                field: Some("email".into()),
                operator: Some(pb::Operator::Eq as i32),
                target_value: Some(pb::AnyValue {
                    value: Some(any_value::Value::StringValue("staff@example.com".into())),
                }),
                ..Default::default()
            };
            frames.push(crc_envelope(Kind::Condition, "staff-email", email));
            let mut rule = targeted_rule(
                "staff",
                pb::ReturnValue {
                    value: Some(return_value::Value::BoolValue(true)),
                },
            );
            rule.conditions = vec!["staff-email".into()];
            gate_rules.push(rule);
        }
        frames.push(gate("source_gate", generation == 2, gate_rules));
        let condition = pb::Condition {
            condition_type: pb::ConditionType::PassGate as i32,
            target_value: Some(pb::AnyValue {
                value: Some(any_value::Value::StringValue("source_gate".into())),
            }),
            id_type: Some(user_id_type()),
            ..Default::default()
        };
        crc_envelope(Kind::Condition, "shared-target", condition)
    } else if mode == BlobDelta::CarryPending {
        condition("changed-user")
    } else {
        condition("remote-user")
    };
    targeting.name = "shared-target".into();
    if mode == BlobDelta::RemovedCondition {
        let enabled = pb::ReturnValue {
            value: Some(return_value::Value::BoolValue(true)),
        };
        frames.push(gate(
            "new_gate",
            false,
            vec![targeted_rule("removed-condition", enabled)],
        ));
    } else {
        frames.push(targeting);
    }
    if mode == BlobDelta::LayerDelegate {
        let mut rule = targeted_rule("delegate", raw(json!({})));
        rule.config_delegate = Some("d".into());
        if delta {
            rule.conditions.clear(); // Everyone can reach an experiment previously routed to one user.
        }
        let layer = pb::Spec {
            enabled: true,
            entity: pb::EntityType::EntityLayer as i32,
            default_value: Some(raw(json!({}))),
            rules: vec![rule],
            ..Default::default()
        };
        frames.push(crc_envelope(Kind::LayerConfig, "layer", layer));
    }
    frames.push(ordinary(generation));
    if delta && mode == BlobDelta::DependentGate {
        let mut destination = ordinary(generation);
        destination.name = "new_d::pipeline".into();
        frames.push(destination);
    }
    if delta {
        frames.push(envelope(
            Kind::Deletions,
            "",
            "",
            pb::RulesetsResponseDeletions {
                condition_map: if mode == BlobDelta::RemovedCondition {
                    vec!["shared-target".into()]
                } else {
                    Vec::new()
                },
                dynamic_configs: if mode == BlobDelta::CarryPending {
                    vec!["new_d".into()]
                } else {
                    vec!["obsolete".into()]
                },
                ..Default::default()
            }
            .encode_to_vec(),
        ));
    } else {
        let mut obsolete = ordinary(generation);
        obsolete.name = "obsolete".into();
        frames.push(obsolete);
    }
    for (i, name) in ["a", "b", "c", "d", "new_d"].into_iter().enumerate() {
        if (!delta || mode == BlobDelta::CarryPending) && name == "new_d" {
            continue;
        }
        // CopyPrev carries A (healthy) and D (pending) from generation 2.
        let carried = mode == BlobDelta::CarryPending && matches!(name, "a" | "d");
        let version = if carried { 2 } else { generation };
        let remote = blobs.map(|blobs| &blobs[i.min(3)]);
        let mut spec = pb::Spec {
            salt: name.into(),
            enabled: true,
            entity: pb::EntityType::EntityDynamicConfig as i32,
            id_type: Some(user_id_type()),
            version: u32::try_from(version).unwrap(),
            default_value: Some(raw(remote.map_or_else(
                || json!({"generation": 1}),
                |blob| json!({"value":blob.path()}),
            ))),
            remote_config_metadata: remote.map(|blob| metadata(blob, None)),
            ..Default::default()
        };
        if name == "d" || (name == "c" && mode != BlobDelta::RemovedCondition) {
            let mut rule =
                targeted_rule("targeted", raw(json!({"matched":name, "version":version})));
            if name == "d" {
                spec.entity = pb::EntityType::EntityExperiment as i32;
                spec.fields_used = vec!["userID".into()];
                spec.is_active = Some(true);
                rule.group_name = Some(format!("group-v{version}"));
                rule.is_experiment_group = Some(true);
            }
            spec.rules.push(rule);
        }
        frames.push(envelope(
            Kind::DynamicConfig,
            name,
            &spec_checksum(&spec),
            spec.encode_to_vec(),
        ));
    }
    if delta {
        let checksum = |kind: Kind| {
            frames
                .iter()
                .filter(|frame| frame.kind == kind as i32)
                .map(|frame| frame.checksum.parse::<u64>().unwrap())
                .sum::<u64>()
        };
        let expected = checksums(
            checksum(Kind::DynamicConfig) + u64::from(mode == BlobDelta::BadChecksum),
            checksum(Kind::Condition),
            checksum(Kind::FeatureGate),
            checksum(Kind::LayerConfig),
        );
        if mode == BlobDelta::CarryPending {
            frames.retain(|frame| !matches!(frame.name.as_str(), "a" | "d"));
        }
        frames.push(expected);
    }
    encode_response(generation, delta, frames)
}

rusty_fork_test! {
    #[test]
    fn pending_blob_is_repaired_on_no_update_after_the_cursor_advances() {
        // The other integration test installs a process-wide diagnostic log provider.
        tokio::runtime::Builder::new_multi_thread().worker_threads(2).enable_all().build()
            .unwrap().block_on(run_partial_blob_delta());
    }

    #[test]
    fn widening_a_layer_cannot_expose_a_pending_experiment() {
        tokio::runtime::Builder::new_multi_thread().worker_threads(2).enable_all().build()
            .unwrap().block_on(async {
                let case = DeltaFixture::new(BlobDelta::LayerDelegate).await;
                let sdk = &case.sdk;
                let guest = StatsigUser::with_user_id("guest");
                let employee = StatsigUser::with_user_id("remote-user");
                assert_eq!(sdk.get_layer(&employee, "layer").allocated_experiment_name.as_deref(), Some("d"));
                assert_eq!(sdk.get_layer(&guest, "layer").allocated_experiment_name, None);

                let options = ClientInitResponseOptions {
                    hash_algorithm: Some(HashAlgorithm::None),
                    ..Default::default()
                };
                let bootstrap_has_layer = || sdk.get_client_init_response_with_options(&guest, &options)
                    .layer_configs.contains_key(&InternedString::from_str_ref("layer"));
                assert!(bootstrap_has_layer());

                case.publish(2, BlobDelta::LayerDelegate).await;
                assert!(sdk.get_layer(&guest, "layer").details.is_blob_unavailable());
                assert!(!bootstrap_has_layer());
                sdk.shutdown().await.unwrap();
            });
    }

    #[test]
    fn previous_config_evaluates_against_each_gate_update_while_its_blob_is_pending() {
        tokio::runtime::Builder::new_multi_thread().worker_threads(2).enable_all().build()
            .unwrap().block_on(async {
                let case = DeltaFixture::new(BlobDelta::DependentGate).await;
                let sdk = &case.sdk;
                let user = StatsigUser::with_user_id("user");
                let gate = || sdk.check_gate(&user, "source_gate");
                assert!(!gate());
                assert_eq!(evaluate(sdk, "user", "d"), json!({"generation": 1}));

                case.publish(2, BlobDelta::DependentGate).await;
                assert!(get_count(&case.server, &case.blobs[3].path()).await > 0);
                assert!(gate());
                assert_eq!(sdk.get_fields_needed_for_experiment("d"), ["userID"]);
                assert_eq!(evaluate(sdk, "user", "c"), json!({"matched": "c", "version": 2}));
                assert_eq!(evaluate(sdk, "user", "d"), json!({"matched": "d", "version": 1}));
                // A DCS mapping can resolve even without a same-name config spec.
                assert_eq!(evaluate(sdk, "user", "healthy_alias"), json!({"generation": 2}));
                assert_eq!(evaluate(sdk, "user", "new_d"), json!({}));
                assert_eq!(evaluate(sdk, "user", "new_d::pipeline"), json!({"generation": 2}));
                let options = ClientInitResponseOptions {
                    hash_algorithm: Some(HashAlgorithm::None),
                    ..Default::default()
                };
                let response = sdk.get_client_init_response_with_options(&user, &options);
                let client_has = |name| {
                    response.dynamic_configs.contains_key(&InternedString::from_str_ref(name))
                };
                assert!(client_has("c"));
                assert!(!client_has("new_d::pipeline"), "a failed root exposed its pipeline destination");
                case.publish(3, BlobDelta::DependentGate).await;
                assert!(!gate());
                let mut staff = StatsigUser::with_user_id("user");
                staff.set_email("staff@example.com");
                assert!(sdk.check_gate(&staff, "source_gate"));
                assert!(sdk.get_fields_needed_for_experiment("d").is_empty());
                for user in [&user, &staff] {
                    assert!(sdk.get_experiment(user, "d").details.is_blob_unavailable());
                }

                sdk.override_dynamic_config("new_d", [("local".into(), json!(true))].into(), None);
                assert_eq!(evaluate(sdk, "user", "new_d"), json!({"local": true}));
                sdk.shutdown().await.unwrap();
            });
    }

    #[test]
    fn a_removed_condition_is_private_to_the_config_retained_during_a_blob_outage() {
        tokio::runtime::Builder::new_multi_thread().worker_threads(2).enable_all().build()
            .unwrap().block_on(async {
                let case = DeltaFixture::new(BlobDelta::AllConfigs).await;
                let sdk = &case.sdk;
                let replay = utils::helpers::bootstrap_from_specs_updated(sdk).await;
                let user = StatsigUser::with_user_id("remote-user");
                assert_eq!(evaluate(sdk, "remote-user", "d"), json!({"matched":"d","version":1}));
                for generation in [2, 3] {
                    case.publish(generation, BlobDelta::RemovedCondition).await;
                    assert!(!sdk.specs_snapshot().condition_map.contains_key(&InternedString::from_str_ref("shared-target")));
                    assert!(!sdk.check_gate(&user, "new_gate"));
                    assert_eq!(evaluate(sdk, "remote-user", "c"), case.blobs[2].value);
                    assert_eq!(evaluate(sdk, "remote-user", "d"), json!({"matched":"d","version":1}));
                }
                assert_eq!(replay.specs_snapshot().time, 1);
                assert_eq!(evaluate(&replay, "remote-user", "d"), json!({"matched":"d","version":1}));
                replay.shutdown().await.unwrap();
                sdk.shutdown().await.unwrap();
            });
    }
}

struct DeltaFixture {
    server: MockServer,
    blobs: [RemoteValue; 4],
    dcs: CurrentResponse,
    sdk: Statsig,
    durable: Arc<MockDataStore>,
}

impl DeltaFixture {
    async fn new(mode: BlobDelta) -> Self {
        std::env::set_var("STATSIG_RUNNING_TESTS", "true");
        let server = MockServer::start().await;
        let blobs = ["A", "B", "C", "D"].map(|name| RemoteValue::new(name, WireFormat::Whitespace));
        for (index, blob) in blobs.iter().enumerate() {
            let response = if index == 3 {
                ResponseTemplate::new(503)
            } else {
                blob.response()
            };
            Mock::given(method("GET"))
                .and(path(blob.path()))
                .respond_with(response)
                .mount(&server)
                .await;
        }
        let dcs = CurrentResponse(Arc::new(Mutex::new(four_blob_response(1, None, mode))));
        Mock::given(method("GET"))
            .and(path("/v2/download_config_specs"))
            .and(header("statsig-api-key", SDK_KEY))
            .respond_with(dcs.clone())
            .mount(&server)
            .await;
        let durable = Arc::new(MockDataStore::new_with_byte_cache(false));
        let options = StatsigOptions {
            data_store: Some(durable.clone()),
            enable_dcs_deltas: Some(true),
            disable_remote_telemetry: Some(true),
            ..network_options(&server)
        };
        let sdk = Statsig::new(SDK_KEY, Some(Arc::new(options)));
        sdk.initialize().await.unwrap();
        Self {
            server,
            blobs,
            dcs,
            sdk,
            durable,
        }
    }

    async fn publish(&self, version: u64, mode: BlobDelta) {
        *self.dcs.0.lock().unwrap() = four_blob_response(version, Some(&self.blobs), mode);
        wait_generation(&self.sdk, version).await;
        let snapshot = self.sdk.specs_snapshot();
        assert_eq!(snapshot.time, 1);
        assert!(snapshot.checksum.is_none());
        let info = self.sdk.get_context().spec_store.get_current_specs_info();
        assert_eq!(info.lcut, Some(version));
        assert!(!self.sdk.is_config_spec_ready());
        assert_eq!(
            self.sdk
                .get_client_init_response(&StatsigUser::with_user_id("user"))
                .time,
            0
        );
    }
}

async fn run_partial_blob_delta() {
    let case = DeltaFixture::new(BlobDelta::AllConfigs).await;
    let DeltaFixture {
        server,
        blobs,
        sdk,
        dcs,
        durable,
    } = &case;
    let dcs_path = "/v2/download_config_specs";
    wait_snapshot(durable, 1).await;
    assert_eq!(evaluate(sdk, "user", "obsolete"), json!({"generation":1}));
    // Reject an invalid producer checksum even when a download has also failed.
    let polls = get_count(server, dcs_path).await;
    let mut invalid = four_blob_response(2, Some(blobs), BlobDelta::BadChecksum);
    invalid.after_once = Some(Box::new(four_blob_response(1, None, BlobDelta::AllConfigs)));
    *dcs.0.lock().unwrap() = invalid;
    wait_polls(server, polls + 4).await;
    assert_eq!(generation(sdk), 1);
    assert_eq!(evaluate(sdk, "user", "a"), json!({"generation":1}));

    case.publish(2, BlobDelta::AllConfigs).await;
    for (name, blob) in ["a", "b", "c"].iter().zip(blobs) {
        assert_eq!(evaluate(sdk, "user", name), blob.value);
    }
    // D's new default failed; even its healthy inline rule still uses v1.
    assert_eq!(evaluate(sdk, "user", "d"), json!({"generation":1}));
    let retained = sdk.get_experiment(&StatsigUser::with_user_id("remote-user"), "d");
    assert_eq!(retained.group_name.as_deref(), Some("group-v1"));
    assert_eq!(retained.value["version"], 1);
    let user = StatsigUser::with_user_id("user");
    let unavailable = |name| {
        sdk.get_dynamic_config(&user, name)
            .details
            .is_blob_unavailable()
    };
    assert!(unavailable("new_d"));
    assert!(!unavailable("typo"));
    let configs = sdk.get_dynamic_config_list();
    assert!(
        !configs
            .iter()
            .any(|name| name == "new_d" || name == "obsolete")
    );

    // The server supplies no more definitions once the SDK reaches cursor 3.
    let no_changes = Mock::given(method("GET"))
        .and(path(dcs_path))
        .and(query_param("sinceTime", "3"))
        .respond_with(ResponseTemplate::new(200).set_body_json(json!({"has_updates": false})))
        .with_priority(1)
        .expect(2..)
        .mount_as_scoped(server)
        .await;
    case.publish(3, BlobDelta::CarryPending).await;
    assert!(!unavailable("new_d"));
    assert_eq!(evaluate(sdk, "user", "a"), blobs[0].value);
    assert_eq!(
        evaluate(sdk, "changed-user", "c"),
        json!({"matched":"c","version":3})
    );
    // This delta reused D's old condition ID for different targeting. Do not
    // expose the previous value to the newly targeted user before D is ready.
    assert_eq!(evaluate(sdk, "changed-user", "d"), json!({}));
    // An offline restart can only read the last complete snapshot.
    let restarted = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            data_store: Some(durable.clone()),
            disable_network: Some(true),
            disable_remote_telemetry: Some(true),
            ..network_options(server)
        })),
    );
    let details = restarted.initialize_with_details().await.unwrap();
    assert_eq!(
        details.source,
        statsig_rust::SpecsSource::Adapter("DataStore".into())
    );
    assert_eq!(restarted.specs_snapshot().time, 1);
    assert_eq!(evaluate(&restarted, "user", "d"), json!({"generation": 1}));
    restarted.shutdown().await.unwrap();

    tokio::time::timeout(Duration::from_secs(5), no_changes.wait_until_satisfied())
        .await
        .expect("the producer cursor never advanced to 3");
    // Only D should be fetched during repair.
    for (index, blob) in blobs.iter().enumerate() {
        Mock::given(method("GET"))
            .and(path(blob.path()))
            .respond_with(blob.response())
            .with_priority(1)
            .expect(u64::from(index == 3))
            .mount(server)
            .await;
    }
    wait_until(|| evaluate(sdk, "user", "d")["marker"] == "D").await;

    assert!(sdk.is_config_spec_ready());
    assert_eq!(sdk.get_client_init_response(&user).time, 3);
    let repaired = sdk.get_experiment(&StatsigUser::with_user_id("changed-user"), "d");
    assert_eq!(repaired.group_name.as_deref(), Some("group-v2"));
    assert_eq!(repaired.value["version"], 2);
    let configs = sdk.get_dynamic_config_list();
    assert!(!configs.iter().any(|name| name == "new_d"));
    let polls = get_count(server, dcs_path).await;
    wait_polls(server, polls + 3).await;
    server.verify().await;
    sdk.shutdown().await.unwrap();
}

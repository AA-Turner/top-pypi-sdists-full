use super::super::metadata::{ReferenceTotals, insert_reference};
use super::*;

const SOURCE_URL: &str = "https://statsigcdn.openai.com/v2/download_config_specs/key.json";

fn remote_spec(body: &[u8]) -> (pb::Spec, String) {
    let sha = lowercase_hex(&Sha256::digest(body));
    let spec = pb::Spec {
        default_value: Some(raw_return_value(
            serde_json::to_vec(&format!("{DOWNLOAD_PATH_PREFIX}{sha}")).unwrap(),
        )),
        remote_config_metadata: Some(protobuf_metadata(sha.clone(), body.len())),
        ..Default::default()
    };
    (spec, sha)
}

fn verified_previous_values(
    hydrator: &RemoteConfigValueHydrator,
    bodies: &[&[u8]],
) -> VerifiedRemoteValues {
    let mut first = hydrator.begin_protobuf_hydration(SOURCE_URL);
    let mut previous = HashMap::new();
    for body in bodies {
        let (mut spec, sha) = remote_spec(body);
        assert!(!first.register_spec_references(&spec).unwrap());
        assert!(first.seed_verified_values(HashMap::from([(sha, Arc::new(body.to_vec()))])));
        previous.extend(
            first
                .take_verified_spec_values(&mut spec)
                .unwrap()
                .provenance,
        );
    }
    first.finish(Ok(()));
    previous
}

#[tokio::test]
async fn only_registered_reused_values_bypass_response_budget_with_duplicate_references() {
    let bodies: [&[u8]; 3] = [
        br#"{"value":"first"}"#,
        br#"{"value":"second"}"#,
        br#"{"value":"unused"}"#,
    ];
    let capacity = 256;
    let budget = Arc::new(ResponseHydrationBudget::new(capacity));
    let mut hydrator = test_hydrator("reused-budget-cardinality");
    hydrator.response_budget = Arc::clone(&budget);
    let previous = verified_previous_values(&hydrator, &bodies);
    assert_eq!(previous.len(), 3);

    let occupied = budget.reserve(capacity as u64).await.unwrap();
    let mut refresh = hydrator.begin_protobuf_hydration(SOURCE_URL);
    refresh.set_previous_values(previous);
    for body in &bodies[..2] {
        let (spec, _) = remote_spec(body);
        for _ in 0..3 {
            assert!(refresh.register_spec_references(&spec).unwrap());
            timeout(Duration::from_millis(25), async {
                refresh.advance_download_window().await?;
                refresh.download_registered_references().await
            })
            .await
            .expect("only registered reused SHAs should determine the budget bypass")
            .unwrap();
        }
    }
    assert_eq!(budget.bytes.available_permits(), 0);
    assert_eq!(budget.expansion.available_permits(), capacity);
    refresh.finish(Ok(()));
    drop(occupied);
    assert_eq!(budget.bytes.available_permits(), capacity);
}

#[tokio::test]
async fn new_reference_after_fully_reused_prefix_waits_for_response_budget() {
    let reused_body = br#"{"value":"reused"}"#;
    let new_body = br#"{"value":"downloaded"}"#;
    let server = MockServer::start().await;
    let (reused_spec, _) = remote_spec(reused_body);
    let (new_spec, new_sha) = remote_spec(new_body);
    mount_json_blob(
        &server,
        &format!("{DOWNLOAD_PATH_PREFIX}{new_sha}"),
        new_body,
        1,
    )
    .await;

    let capacity = reused_body.len() + new_body.len();
    let budget = Arc::new(ResponseHydrationBudget::new(capacity));
    let mut hydrator = test_hydrator("mixed-reused-budget-cardinality");
    hydrator.response_budget = Arc::clone(&budget);
    let previous = verified_previous_values(&hydrator, &[reused_body]);
    let occupied = budget.reserve(capacity as u64).await.unwrap();
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    let mut refresh = hydrator.begin_protobuf_hydration(&source_url);
    refresh.set_previous_values(previous);
    assert!(refresh.register_spec_references(&reused_spec).unwrap());
    refresh.advance_download_window().await.unwrap();
    assert!(!refresh.register_spec_references(&new_spec).unwrap());

    let mut hydration = Box::pin(refresh.download_registered_references());
    assert!(
        timeout(Duration::from_millis(25), hydration.as_mut())
            .await
            .is_err()
    );
    assert!(server.received_requests().await.unwrap().is_empty());
    drop(occupied);
    hydration.await.unwrap();
    assert_eq!(budget.bytes.available_permits(), 0);

    let mut hydrated_spec = new_spec.clone();
    assert!(
        refresh
            .take_verified_spec_values(&mut hydrated_spec)
            .unwrap()
            .default_value
            .is_some()
    );
    assert!(refresh.register_spec_references(&reused_spec).unwrap());
    assert!(refresh.register_spec_references(&new_spec).unwrap());
    refresh.download_registered_references().await.unwrap();
    assert_eq!(server.received_requests().await.unwrap().len(), 1);
    refresh.finish(Ok(()));
    assert_eq!(budget.bytes.available_permits(), capacity);
    server.verify().await;
}

#[tokio::test]
async fn resolved_seeded_bodies_still_require_response_budget_expansion() {
    let body = br#"{"value":"seeded"}"#;
    let (spec, sha) = remote_spec(body);
    let capacity = body.len() * 4;
    let budget = Arc::new(ResponseHydrationBudget::new(capacity));
    let mut hydrator = test_hydrator("resolved-body-budget-cardinality");
    hydrator.response_budget = Arc::clone(&budget);
    let mut session = hydrator.begin_protobuf_hydration(SOURCE_URL);
    assert!(!session.register_spec_references(&spec).unwrap());
    assert!(session.seed_verified_values(HashMap::from([(sha, Arc::new(body.to_vec()))])));
    let mut resolved_spec = spec.clone();
    session
        .take_verified_spec_values(&mut resolved_spec)
        .unwrap();

    let occupied = budget
        .reserve((capacity - body.len()) as u64)
        .await
        .unwrap();
    assert!(session.register_spec_references(&spec).unwrap());
    session.download_registered_references().await.unwrap();
    assert_eq!(budget.bytes.available_permits(), 0);
    assert_eq!(
        budget.expansion.available_permits(),
        body.len(),
        "resolved values with retained bodies must not bypass expansion admission"
    );
    session.finish(Ok(()));
    assert_eq!(budget.expansion.available_permits(), capacity);
    drop(occupied);
    assert_eq!(budget.bytes.available_permits(), capacity);
}

#[test]
fn incremental_reference_totals_match_full_validation_and_fail_atomically() {
    let make_reference = |sha: &str, origin: &str, occurrences, bytes| RemoteValueReference {
        download_url: Url::parse(&format!("{origin}{DOWNLOAD_PATH_PREFIX}{sha}")).unwrap(),
        metadata: valid_metadata(sha.to_string(), bytes),
        occurrences,
    };
    let first_sha = "a".repeat(64);
    let second_sha = "b".repeat(64);
    let first = make_reference(&first_sha, "https://statsigcdn.openai.com", 2, 17);
    let alternate = make_reference(&first_sha, "https://longer-source-origin.openai.com", 3, 17);
    let second = make_reference(&second_sha, "https://statsigcdn.openai.com", 4, 31);
    let mut references = HashMap::new();
    let mut totals = ReferenceTotals::default();
    for reference in [first.clone(), alternate, second, first.clone()] {
        let sha = reference.metadata.sha256.to_string();
        totals
            .add_occurrences(
                references.get(&sha).unwrap_or(&reference),
                reference.occurrences,
            )
            .unwrap();
        insert_reference(&mut references, sha, reference).unwrap();
        assert_eq!(
            (totals.reference_count, totals.total_bytes),
            validate_reference_limits(references.values()).unwrap()
        );
    }

    let metadata_bytes = std::mem::size_of::<RemoteValueReference>()
        + first.download_url.as_str().len()
        + first.metadata.sha256.as_str().len()
        + first.metadata.content_type.as_str().len();
    let allowed = MAX_REMOTE_VALUE_METADATA_BYTES_PER_SYNC / metadata_bytes;
    let mut capped = ReferenceTotals::default();
    capped.add_occurrences(&first, allowed).unwrap();
    assert!(capped.add_occurrences(&first, 1).is_err());
    assert_eq!(capped.reference_count, allowed);
    assert_eq!(capped.total_bytes, allowed as u64 * 17);
    assert!(capped.add_occurrences(&first, usize::MAX).is_err());
    assert_eq!(capped.reference_count, allowed);

    let mut huge = first;
    huge.metadata.byte_length = u64::MAX;
    let mut bytes = ReferenceTotals::default();
    bytes.add_occurrences(&huge, 1).unwrap();
    let previous_count = bytes.reference_count;
    let previous_bytes = bytes.total_bytes;
    assert!(matches!(
        bytes.add_occurrences(&huge, 1),
        Err(StatsigErr::CustomError(message))
            if message.starts_with("Dynamic config hydration failure: total_bytes_exceeded:")
    ));
    assert_eq!(
        (bytes.reference_count, bytes.total_bytes),
        (previous_count, previous_bytes)
    );
}

#[tokio::test]
async fn incremental_registration_retains_canonical_url_cost_and_rejects_over_limit_chunk() {
    let body = br#"{"value":"canonical"}"#;
    let other_body = br#"{"value":"unregistered"}"#;
    let (mut spec, sha) = remote_spec(body);
    let canonical_url = format!("https://statsigcdn.openai.com{DOWNLOAD_PATH_PREFIX}{sha}");
    spec.default_value = Some(raw_return_value(
        serde_json::to_vec(&canonical_url).unwrap(),
    ));
    let reference = RemoteValueReference {
        download_url: Url::parse(&canonical_url).unwrap(),
        metadata: valid_metadata(sha.clone(), body.len() as u64),
        occurrences: 1,
    };
    let metadata_bytes = std::mem::size_of::<RemoteValueReference>()
        + reference.download_url.as_str().len()
        + reference.metadata.sha256.as_str().len()
        + reference.metadata.content_type.as_str().len();
    let allowed = MAX_REMOTE_VALUE_METADATA_BYTES_PER_SYNC / metadata_bytes;
    let hydrator = test_hydrator("incremental-canonical-reference-limits");
    let source_url = format!(
        "https://{}.openai.com/v2/download_config_specs/key.json",
        "x".repeat(256)
    );
    let mut session = hydrator.begin_protobuf_hydration(&source_url);
    assert!(!session.register_spec_references(&spec).unwrap());

    // Later relative placeholders resolve to a much longer, also trusted URL.
    // Dedup retains the first URL, so its size must charge every occurrence.
    let (relative, _) = remote_spec(body);
    let mut remaining = allowed - 1;
    while remaining > 0 {
        let occurrences = remaining.min(1024);
        let mut chunk = relative.clone();
        chunk.rules = (1..occurrences)
            .map(|index| pb::Rule {
                id: index.to_string(),
                return_value: relative.default_value.clone(),
                remote_config_metadata: relative.remote_config_metadata.clone(),
                ..Default::default()
            })
            .collect();
        assert!(!session.register_spec_references(&chunk).unwrap());
        remaining -= occurrences;
    }

    let (other, other_sha) = remote_spec(other_body);
    assert!(matches!(
        session.register_spec_references(&other),
        Err(StatsigErr::CustomError(message))
            if message.starts_with("Dynamic config hydration failure: too_many_values:")
    ));
    assert!(
        !session.seed_verified_values(HashMap::from([(other_sha, Arc::new(other_body.to_vec())),])),
        "a rejected chunk must not add references or queue work"
    );
    assert!(session.seed_verified_values(HashMap::from([(sha, Arc::new(body.to_vec()))])));
    session.advance_download_window().await.unwrap();
    session.download_registered_references().await.unwrap();
    session.finish(Ok(()));
}

#[tokio::test]
async fn queued_downloads_preserve_partial_seeding_dedup_and_in_flight_readiness() {
    let server = MockServer::start().await;
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    let hydrator = test_hydrator("queued-protobuf-readiness-transitions");
    let bodies = (0..DOWNLOAD_CONCURRENCY + 4)
        .map(|index| format!(r#"{{"value":{index}}}"#).into_bytes())
        .collect::<Vec<_>>();
    let specs = bodies
        .iter()
        .map(|body| {
            let (mut spec, sha) = remote_spec(body);
            spec.rules.push(pb::Rule {
                id: "duplicate".to_string(),
                return_value: spec.default_value.clone(),
                remote_config_metadata: spec.remote_config_metadata.clone(),
                ..Default::default()
            });
            (spec, sha)
        })
        .collect::<Vec<_>>();
    for (index, (_, sha)) in specs.iter().enumerate().skip(1) {
        if index == 2 {
            continue;
        }
        Mock::given(method("GET"))
            .and(path(format!("{DOWNLOAD_PATH_PREFIX}{sha}")))
            .respond_with(
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .set_delay(Duration::from_millis(10))
                    .set_body_bytes(bodies[index].clone()),
            )
            .expect(1)
            .mount(&server)
            .await;
    }

    let mut session = hydrator.begin_protobuf_hydration(&source_url);
    session.set_previous_values(verified_previous_values(&hydrator, &[&bodies[2]]));
    for (index, (spec, _)) in specs[..specs.len() - 1].iter().enumerate() {
        assert_eq!(session.register_spec_references(spec).unwrap(), index == 2);
    }
    assert!(session.register_spec_references(&specs[2].0).unwrap());
    assert!(
        !session.seed_verified_values(HashMap::from([
            (specs[0].1.clone(), Arc::new(bodies[0].clone())),
            (specs[1].1.clone(), Arc::new(b"invalid".to_vec())),
        ])),
        "a failed seed must not partially complete queued references"
    );
    let first_seed = HashMap::from([(specs[0].1.clone(), Arc::new(bodies[0].clone()))]);
    assert!(session.seed_verified_values(first_seed.clone()));
    assert!(session.seed_verified_values(first_seed));
    session.advance_download_window().await.unwrap();
    assert!(
        !server.received_requests().await.unwrap().is_empty(),
        "window backpressure must poll a download before accepting seeds"
    );

    // Advancing more than one window leaves active downloads. Completing their
    // SHAs by seeding must not decrement again when those futures later finish.
    let seeds = specs[..specs.len() - 1]
        .iter()
        .zip(&bodies)
        .map(|((_, sha), body)| (sha.clone(), Arc::new(body.clone())))
        .collect::<HashMap<_, _>>();
    assert!(session.seed_verified_values(seeds));
    assert!(session.register_spec_references(&specs[2].0).unwrap());
    let (late_spec, _) = specs.last().unwrap();
    assert!(!session.register_spec_references(late_spec).unwrap());
    session.download_registered_references().await.unwrap();
    for (spec, _) in &specs {
        let mut resolved = spec.clone();
        let values = session.take_verified_spec_values(&mut resolved).unwrap();
        assert_eq!(values.provenance.len(), 1);
        assert!(values.default_value.is_some());
        assert!(values.rule_values[0].is_some());
    }
    assert!(session.register_spec_references(late_spec).unwrap());
    session.advance_download_window().await.unwrap();
    session.download_registered_references().await.unwrap();
    session.finish(Ok(()));
    assert_eq!(
        server.received_requests().await.unwrap().len(),
        specs.len() - 2
    );
    server.verify().await;
}

#[tokio::test]
async fn rejected_metadata_conflict_can_be_retried_without_stale_registration_state() {
    let server = MockServer::start().await;
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    let hydrator = test_hydrator("atomic-protobuf-reference-registration");
    let body = br#"{"value":"first"}"#;
    let other_body = br#"{"value":"second"}"#;
    let (spec, sha) = remote_spec(body);
    let (other, other_sha) = remote_spec(other_body);
    mount_json_blob(&server, &format!("{DOWNLOAD_PATH_PREFIX}{sha}"), body, 1).await;
    mount_json_blob(
        &server,
        &format!("{DOWNLOAD_PATH_PREFIX}{other_sha}"),
        other_body,
        1,
    )
    .await;
    let mut session = hydrator.begin_protobuf_hydration(&source_url);
    assert!(!session.register_spec_references(&spec).unwrap());
    let mut invalid = other.clone();
    let mut conflict = spec.remote_config_metadata.clone().unwrap();
    conflict.byte_length += 1;
    invalid.rules.push(pb::Rule {
        id: "conflict".to_string(),
        return_value: spec.default_value.clone(),
        remote_config_metadata: Some(conflict),
        ..Default::default()
    });
    assert!(matches!(session.register_spec_references(&invalid),
        Err(StatsigErr::CustomError(message))
            if message.starts_with("Dynamic config hydration failure: metadata_conflict:")
    ));
    assert!(!session.register_spec_references(&other).unwrap());
    session.download_registered_references().await.unwrap();
    for mut spec in [spec, other] {
        assert!(
            session
                .take_verified_spec_values(&mut spec)
                .unwrap()
                .default_value
                .is_some()
        );
    }
    session.finish(Ok(()));
    assert_eq!(server.received_requests().await.unwrap().len(), 2);
    server.verify().await;
}

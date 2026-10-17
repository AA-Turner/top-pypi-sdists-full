use super::*;

const FILE_URL: &str = "https://files.test/users?private=true";

fn update(ts: Option<u64>, size: u64, range: Option<Range<u64>>) -> IdListPropagationUpdate {
    IdListPropagationUpdate {
        file_id: Some("A".into()),
        url: file_identity_url(FILE_URL),
        ts,
        size,
        applied_range: range,
    }
}

// Model the published cursor for ordinary range/metadata observations. Tests
// for replay publication gates call state.apply with an explicit cursor below.
fn apply(
    state: &mut IdListPropagationState,
    update: IdListPropagationUpdate,
    initialized: bool,
    now: u64,
) -> Option<(u64, u64, u64)> {
    let published_size = update
        .applied_range
        .as_ref()
        .map_or(state.applied_size, |range| range.end);
    state.apply(update, published_size, initialized, now)
}

fn hydrated() -> IdListPropagationState {
    let mut state = IdListPropagationState::default();
    assert_eq!(
        apply(&mut state, update(Some(10), 10, Some(0..10)), false, 100),
        None
    );
    state
}

#[test]
fn reports_normal_append_once_without_retiming_replays() {
    let mut state = hydrated();
    assert_eq!(
        apply(&mut state, update(Some(20), 20, Some(10..20)), true, 200),
        Some((20, 10, 200))
    );
    assert_eq!(
        apply(&mut state, update(Some(20), 20, None), true, 300),
        None
    );
    assert_eq!(
        apply(&mut state, update(Some(20), 20, Some(0..20)), true, 400),
        None
    );
    assert_eq!(state.applied_intervals.len(), 1);
    assert_eq!(state.applied_intervals[0].applied_at, 200);
}

#[test]
fn late_timestamp_uses_the_original_append_publication_time() {
    let mut state = hydrated();
    assert_eq!(
        apply(&mut state, update(None, 20, Some(10..20)), true, 200),
        None
    );
    assert_eq!(
        apply(&mut state, update(Some(20), 20, None), true, 900),
        Some((20, 10, 200))
    );
    assert_eq!(
        apply(&mut state, update(Some(20), 20, None), true, 1_000),
        None
    );
}

#[test]
fn late_timestamp_on_cold_bytes_does_not_create_a_warm_sample() {
    let mut state = IdListPropagationState::default();
    assert_eq!(
        apply(&mut state, update(None, 10, Some(0..10)), false, 100),
        None
    );
    assert_eq!(
        apply(&mut state, update(Some(20), 10, None), true, 500),
        None
    );
    assert!(state.applied_intervals.is_empty());
    assert_eq!(
        apply(&mut state, update(Some(30), 20, Some(10..20)), true, 600),
        Some((30, 20, 600))
    );
}

#[test]
fn separate_frontiers_keep_their_own_first_application_times() {
    let mut state = hydrated();
    assert_eq!(
        apply(&mut state, update(None, 20, Some(10..20)), true, 200),
        None
    );
    assert_eq!(
        apply(&mut state, update(None, 30, Some(20..30)), true, 300),
        None
    );
    assert_eq!(
        apply(&mut state, update(Some(20), 20, None), true, 800),
        Some((20, 10, 200))
    );
    assert_eq!(
        apply(&mut state, update(Some(30), 30, None), true, 900),
        Some((30, 20, 300))
    );
}

#[test]
fn old_timestamps_do_not_discard_new_byte_coverage() {
    let mut state = hydrated();
    assert_eq!(
        apply(&mut state, update(Some(10), 20, Some(10..20)), true, 200),
        None
    );
    assert_eq!(
        apply(&mut state, update(Some(9), 30, Some(20..30)), true, 300),
        None
    );
    assert_eq!(
        apply(&mut state, update(Some(20), 20, None), true, 800),
        Some((20, 10, 200))
    );
    assert_eq!(
        apply(&mut state, update(Some(30), 30, None), true, 900),
        Some((30, 20, 300))
    );
}

#[test]
fn evicted_prefix_cannot_be_retimed_by_metadata_or_replay() {
    let mut state = hydrated();
    for index in 0..=MAX_APPLIED_INTERVALS {
        let start = 10 + index as u64;
        assert_eq!(
            apply(
                &mut state,
                update(None, start + 1, Some(start..start + 1)),
                true,
                1_000 + index as u64
            ),
            None
        );
    }
    assert_eq!(state.applied_intervals.len(), MAX_APPLIED_INTERVALS);
    assert_eq!(
        apply(&mut state, update(Some(20), 11, None), true, 2_000),
        None
    );
    assert_eq!(
        apply(&mut state, update(Some(30), 11, Some(0..11)), true, 3_000),
        None
    );
    assert_eq!(state.applied_intervals.len(), MAX_APPLIED_INTERVALS);
    // Finish replaying this retained frontier before reporting its original t2.
    assert_eq!(
        apply(&mut state, update(Some(40), 12, Some(11..12)), true, 4_000),
        Some((40, 30, 1_001))
    );
}

#[test]
fn holes_need_contiguous_application_before_reporting_a_frontier() {
    let mut state = hydrated();
    assert_eq!(
        apply(&mut state, update(Some(20), 30, Some(20..30)), true, 200),
        None
    );
    assert_eq!(state.applied_size, 10);
    assert!(state.applied_intervals.is_empty());
    assert_eq!(
        apply(&mut state, update(Some(20), 30, Some(10..20)), true, 300),
        None
    );
    assert_eq!(
        apply(&mut state, update(Some(20), 30, Some(20..30)), true, 400),
        Some((20, 10, 400))
    );
    assert_eq!(
        apply(&mut state, update(Some(20), 30, Some(0..30)), true, 500),
        None
    );
    assert_eq!(state.applied_intervals.len(), 2);
}

#[test]
fn file_or_routing_identity_changes_discard_old_application_history() {
    for (file_id, url) in [
        ("B", FILE_URL),
        ("A", "https://files.test/users?private=false"),
    ] {
        let mut state = hydrated();
        assert_eq!(
            apply(&mut state, update(None, 20, Some(10..20)), true, 200),
            None
        );
        let replacement = |range| IdListPropagationUpdate {
            file_id: Some(file_id.into()),
            url: file_identity_url(url),
            ..update(Some(20), 20, range)
        };
        assert_eq!(apply(&mut state, replacement(None), true, 300), None);
        assert!(state.applied_intervals.is_empty());
        assert_eq!(
            apply(&mut state, replacement(Some(0..20)), true, 400),
            Some((20, 10, 400))
        );
    }
}

#[test]
fn missing_file_identity_clears_history_until_bytes_are_proven_again() {
    for file_id in [None, Some(String::new())] {
        let mut state = hydrated();
        assert_eq!(
            apply(&mut state, update(None, 20, Some(10..20)), true, 200),
            None
        );
        let unidentified = IdListPropagationUpdate {
            file_id,
            ..update(Some(20), 20, None)
        };
        assert_eq!(apply(&mut state, unidentified, true, 300), None);
        assert_eq!(state.applied_size, 0);
        assert!(state.applied_intervals.is_empty());
        assert_eq!(
            apply(&mut state, update(Some(20), 20, None), true, 400),
            None
        );
        assert_eq!(
            apply(&mut state, update(Some(20), 20, Some(0..20)), true, 500),
            Some((20, 10, 500))
        );
    }
}

#[test]
fn sas_renewal_preserves_the_original_application_time() {
    let mut state = hydrated();
    let signed = |signature: &str, ts, range| IdListPropagationUpdate {
        url: file_identity_url(&format!("{FILE_URL}&se={signature}&sig={signature}")),
        ..update(ts, 20, range)
    };
    assert_eq!(
        apply(&mut state, signed("old", None, Some(10..20)), true, 200),
        None
    );
    assert_eq!(
        apply(&mut state, signed("new", Some(20), None), true, 900),
        Some((20, 10, 200))
    );
}

#[test]
fn late_timestamp_can_match_an_explicit_warm_empty_file_install() {
    let mut state = hydrated();
    let replacement = |ts, range| IdListPropagationUpdate {
        file_id: Some("B".into()),
        ..update(ts, 0, range)
    };
    assert_eq!(
        apply(&mut state, replacement(None, Some(0..0)), true, 200),
        None
    );
    assert_eq!(
        apply(&mut state, replacement(Some(20), None), true, 900),
        Some((20, 10, 200))
    );
    assert_eq!(
        apply(&mut state, replacement(Some(20), None), true, 1_000),
        None
    );
}

#[test]
fn timestamp_newer_than_applied_bytes_cannot_use_metadata_arrival_as_apply_time() {
    let mut state = hydrated();
    assert_eq!(
        apply(&mut state, update(Some(500), 20, Some(10..20)), true, 200),
        None
    );
    assert_eq!(
        apply(&mut state, update(Some(500), 20, None), true, 900),
        None
    );
    assert_eq!(
        apply(&mut state, update(Some(600), 30, Some(20..30)), true, 1_000),
        Some((600, 500, 1_000))
    );
}

#[test]
fn partial_cold_load_remains_cold_when_the_manifest_grows_with_its_original_timestamp() {
    let mut state = IdListPropagationState::default();
    assert_eq!(
        apply(&mut state, update(Some(20), 20, Some(0..10)), false, 100),
        None
    );
    assert_eq!(
        apply(&mut state, update(Some(20), 30, Some(10..30)), true, 200),
        None
    );
    assert_eq!(state.ts, 20);
    assert_eq!(state.applied_intervals[0].start, 20);
    assert_eq!(
        apply(&mut state, update(Some(30), 30, None), true, 900),
        Some((30, 20, 200))
    );
}

#[test]
fn incomplete_replay_keeps_new_coverage_without_consuming_the_checkpoint() {
    let mut state = hydrated();
    assert_eq!(
        state.apply(update(Some(20), 30, Some(0..20)), 20, true, 200),
        None
    );
    assert_eq!(state.ts, 10);
    assert_eq!(state.applied_size, 20);
    assert_eq!(
        state.apply(update(None, 30, Some(20..30)), 30, true, 300),
        None
    );
    assert_eq!(
        state.apply(update(Some(20), 30, None), 30, true, 900),
        Some((20, 10, 300))
    );
}

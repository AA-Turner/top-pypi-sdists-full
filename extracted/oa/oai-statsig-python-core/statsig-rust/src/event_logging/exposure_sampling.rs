use super::event_queue::queued_event::{EnqueueOperation, QueuedExposure};
use crate::{
    DynamicValue,
    evaluation::evaluation_types::{BaseEvaluation, ExtraExposureInfo},
    global_configs::{GlobalConfigs, PartialRolloutBoostConfig, PartialRolloutBoostRule},
    log_d, log_e,
    user::user_data::UserData,
    write_lock_or_noop, write_lock_or_return,
};
use ahash::{AHashMap, AHashSet};
use chrono::Utc;
use parking_lot::{Mutex, RwLock};
use std::{
    collections::hash_map::Entry,
    sync::{
        Arc,
        atomic::{AtomicU64, Ordering},
    },
    time::{Duration, Instant},
};

const TAG: &str = "ExposureSampling";
const DEFAULT_EXPOSURE_SAMPLING_TTL_MS: u64 = 60_000;
const SAMPLING_MAX_KEYS: usize = 100_000;
const DEDUPE_MIN_RETAINED_CAPACITY: usize = 1024;
const DEDUPE_MIN_SWEEP_INTERVAL_MS: u64 = 1_000;

#[derive(Debug)]
pub enum EvtSamplingMode {
    On,
    Shadow,
}

#[derive(Debug)]
pub enum EvtSamplingDecision {
    Deduped,
    NotSampled,
    ForceSampled,
    Sampled(Option<u64>, EvtSamplingMode, bool),
    BoostedPartialRollout,
}

impl EvtSamplingDecision {
    pub fn should_log(&self) -> bool {
        match self {
            EvtSamplingDecision::Deduped | EvtSamplingDecision::NotSampled => false,
            EvtSamplingDecision::ForceSampled
            | EvtSamplingDecision::Sampled(_, _, _)
            | EvtSamplingDecision::BoostedPartialRollout => true,
        }
    }
}

type SpecAndRuleHashTuple = (u64, u64);
type PartialRolloutBoostKey = (u64, u64, u64);

#[derive(Default)]
struct ExposureDedupeState {
    entries: AHashMap<ExposureSamplingKey, u64>,
    next_expiration_ms: Option<u64>,
    next_sweep_ms: u64,
}

impl ExposureDedupeState {
    fn sweep_due(&self, now_ms: u64) -> bool {
        self.next_expiration_ms
            .is_some_and(|next_expiration_ms| next_expiration_ms <= now_ms)
            && self.next_sweep_ms <= now_ms
    }

    fn remove_expired_entries(&mut self, now_ms: u64) {
        let previous_len = self.entries.len();
        let mut next_expiration_ms: Option<u64> = None;

        self.entries.retain(|_, expires_at| {
            if *expires_at <= now_ms {
                return false;
            }

            next_expiration_ms = Some(next_expiration_ms.map_or(*expires_at, |next_expiration| {
                next_expiration.min(*expires_at)
            }));
            true
        });

        self.next_expiration_ms = next_expiration_ms;
        self.next_sweep_ms = now_ms.saturating_add(DEDUPE_MIN_SWEEP_INTERVAL_MS);

        let removed = previous_len.saturating_sub(self.entries.len());
        if removed > 0 {
            log_d!(
                TAG,
                "Removed expired exposure dedupe entries. removed: {:?}, remaining: {:?}",
                removed,
                self.entries.len()
            );
        }
    }

    fn shrink_if_oversized(&mut self) {
        let retained_capacity = self.entries.capacity();
        if retained_capacity > DEDUPE_MIN_RETAINED_CAPACITY
            && self.entries.len() <= retained_capacity / 4
        {
            let target_capacity = self
                .entries
                .len()
                .saturating_mul(2)
                .max(DEDUPE_MIN_RETAINED_CAPACITY);
            self.entries.shrink_to(target_capacity);
        }
    }
}

#[derive(Debug, Default)]
struct PartialRolloutBoostLimiter {
    window: Option<(u64, u64)>,
    rollout_counts: AHashMap<PartialRolloutBoostKey, u64>,
    boosted_count: u64,
}

impl PartialRolloutBoostLimiter {
    fn try_admit(
        &mut self,
        rollout: PartialRolloutBoostKey,
        now_ms: u64,
        config: PartialRolloutBoostConfig,
    ) -> bool {
        if config.window_seconds == 0 || config.per_rollout_limit == 0 || config.global_limit == 0 {
            return false;
        }

        let Some(window_ms) = config.window_seconds.checked_mul(1_000) else {
            return false;
        };
        let window = (config.window_seconds, now_ms / window_ms);
        if self.window != Some(window) {
            self.window = Some(window);
            self.rollout_counts.clear();
            self.boosted_count = 0;
        }

        if self.boosted_count >= config.global_limit {
            return false;
        }

        let count = self.rollout_counts.entry(rollout).or_default();
        if *count >= config.per_rollout_limit {
            return false;
        }

        *count += 1;
        self.boosted_count += 1;
        true
    }
}

pub struct ExposureSampling {
    spec_sampling_set: RwLock<AHashSet<SpecAndRuleHashTuple>>,
    last_spec_sampling_reset: AtomicU64,

    exposure_dedupe: RwLock<ExposureDedupeState>,
    exposure_dedupe_started_at: Instant,

    partial_rollout_boost_limiter: Mutex<PartialRolloutBoostLimiter>,

    global_configs: Arc<GlobalConfigs>,
}

impl ExposureSampling {
    pub fn new(sdk_instance_id: &str) -> Self {
        let now = Utc::now().timestamp_millis() as u64;

        Self {
            spec_sampling_set: RwLock::from(AHashSet::default()),
            last_spec_sampling_reset: AtomicU64::from(now),

            exposure_dedupe: RwLock::from(ExposureDedupeState::default()),
            exposure_dedupe_started_at: Instant::now(),

            partial_rollout_boost_limiter: Mutex::new(PartialRolloutBoostLimiter::default()),

            global_configs: GlobalConfigs::get_instance(sdk_instance_id),
        }
    }

    pub fn get_sampling_decision(
        &self,
        payload: &impl EnqueueOperation,
        ignore_analytical_gate_force_sampling: bool,
    ) -> EvtSamplingDecision {
        let exposure = match payload.as_exposure() {
            Some(exposure) => exposure,
            None => return EvtSamplingDecision::ForceSampled,
        };

        let expo_sampling_key = exposure.create_exposure_sampling_key();
        if self.should_dedupe_exposure(&expo_sampling_key) {
            return EvtSamplingDecision::Deduped;
        }

        let sampling_mode = match self.global_configs.get_sampling_mode() {
            Some(sampling_mode) => sampling_mode,
            None => return EvtSamplingDecision::ForceSampled,
        };

        let extra_info = exposure.get_extra_exposure_info_ref();
        if self.should_sample_based_on_evaluation(extra_info, ignore_analytical_gate_force_sampling)
        {
            return EvtSamplingDecision::ForceSampled;
        }

        if self.should_sample_first_time_exposure(&expo_sampling_key) {
            return EvtSamplingDecision::ForceSampled;
        }

        let sampling_rate = self
            .get_special_case_sampling_rate(exposure)
            .or_else(|| extra_info.and_then(|info| info.sampling_rate));

        let is_sampled = expo_sampling_key.is_sampled(sampling_rate);

        match sampling_mode {
            EvtSamplingMode::On if is_sampled => {
                EvtSamplingDecision::Sampled(sampling_rate, EvtSamplingMode::On, true)
            }
            EvtSamplingMode::On
                if self.should_boost_partial_rollout(exposure, extra_info, &expo_sampling_key) =>
            {
                EvtSamplingDecision::BoostedPartialRollout
            }
            EvtSamplingMode::Shadow => {
                EvtSamplingDecision::Sampled(sampling_rate, EvtSamplingMode::Shadow, is_sampled)
            }
            _ => EvtSamplingDecision::NotSampled,
        }
    }

    pub fn try_reset_all_sampling(&self) {
        self.try_reset_exposure_dedupe_set();
        self.try_reset_spec_sampling_set();
    }

    fn should_dedupe_exposure(&self, sampling_key: &ExposureSamplingKey) -> bool {
        self.should_dedupe_exposure_at(sampling_key, self.exposure_dedupe_now_ms())
    }

    fn should_dedupe_exposure_at(&self, sampling_key: &ExposureSamplingKey, now_ms: u64) -> bool {
        let ttl_ms = self.global_configs.get_exposure_dedupe_ttl_ms();
        if ttl_ms == 0 {
            return false;
        }

        {
            let dedupe_state = match self
                .exposure_dedupe
                .try_read_for(crate::macros::LOCK_TIMEOUT)
            {
                Some(state) => state,
                None => {
                    log_e!(TAG, "Failed to acquire read lock for exposure dedupe set");
                    return false;
                }
            };

            let expires_at = dedupe_state.entries.get(sampling_key);
            if expires_at.is_some_and(|expires_at| *expires_at > now_ms) {
                return true;
            }

            if expires_at.is_none()
                && dedupe_state.entries.len() >= SAMPLING_MAX_KEYS
                && !dedupe_state.sweep_due(now_ms)
            {
                return false;
            }
        }

        let mut dedupe_state = write_lock_or_return!(TAG, self.exposure_dedupe, false);
        if dedupe_state.entries.len() >= SAMPLING_MAX_KEYS && dedupe_state.sweep_due(now_ms) {
            dedupe_state.remove_expired_entries(now_ms);
        }

        let can_admit_new_key = dedupe_state.entries.len() < SAMPLING_MAX_KEYS;
        let expires_at = now_ms.saturating_add(ttl_ms);

        match dedupe_state.entries.entry(sampling_key.clone()) {
            Entry::Occupied(mut entry) => {
                if *entry.get() > now_ms {
                    return true;
                }

                entry.insert(expires_at);
            }
            Entry::Vacant(entry) => {
                if !can_admit_new_key {
                    // Preserve existing dedupe decisions while bounding memory. A
                    // newly observed exposure is logged until an expired slot opens.
                    return false;
                }

                entry.insert(expires_at);
            }
        }

        dedupe_state.next_expiration_ms = Some(
            dedupe_state
                .next_expiration_ms
                .map_or(expires_at, |next_expiration| {
                    next_expiration.min(expires_at)
                }),
        );
        false
    }

    fn exposure_dedupe_now_ms(&self) -> u64 {
        u64::try_from(self.exposure_dedupe_started_at.elapsed().as_millis()).unwrap_or(u64::MAX)
    }

    fn should_sample_based_on_evaluation(
        &self,
        extra_info: Option<&ExtraExposureInfo>,
        ignore_analytical_gate_force_sampling: bool,
    ) -> bool {
        let exposure_info = match extra_info {
            Some(exposure_info) => exposure_info,
            None => return false,
        };

        if exposure_info.forward_all_exposures == Some(true) {
            return true;
        }

        if !ignore_analytical_gate_force_sampling
            && exposure_info.has_seen_analytical_gates == Some(true)
        {
            return true;
        }

        false
    }

    fn should_boost_partial_rollout<'a>(
        &self,
        exposure: &'a impl QueuedExposure<'a>,
        extra_info: Option<&'a ExtraExposureInfo>,
        sampling_key: &ExposureSamplingKey,
    ) -> bool {
        if !exposure.is_primary_gate_exposure() {
            return false;
        }

        let Some(rule_pass_percentage) = extra_info.and_then(|info| info.rule_pass_percentage)
        else {
            return false;
        };
        if !(0.0 < rule_pass_percentage && rule_pass_percentage < 100.0) {
            return false;
        }

        let Some((rollout, config)) = self
            .global_configs
            .get_partial_rollout_boost(sampling_key.spec_name_hash, sampling_key.rule_id_hash)
        else {
            return false;
        };

        if rule_pass_percentage != rollout.rollout_percentage {
            return false;
        }

        let Ok(now_ms) = u64::try_from(Utc::now().timestamp_millis()) else {
            return false;
        };

        self.should_boost_partial_rollout_at(sampling_key, rollout, config, now_ms)
    }

    fn should_boost_partial_rollout_at(
        &self,
        sampling_key: &ExposureSamplingKey,
        rollout: PartialRolloutBoostRule,
        config: PartialRolloutBoostConfig,
        now_ms: u64,
    ) -> bool {
        if rollout.start_time > now_ms {
            return false;
        }

        if config.duration_seconds == 0 {
            return false;
        }

        let Some(duration_ms) = config.duration_seconds.checked_mul(1_000) else {
            return false;
        };
        if now_ms - rollout.start_time >= duration_ms {
            return false;
        }

        let mut limiter = self.partial_rollout_boost_limiter.lock();

        limiter.try_admit(
            (
                sampling_key.spec_name_hash,
                sampling_key.rule_id_hash,
                rollout.start_time,
            ),
            now_ms,
            config,
        )
    }

    fn should_sample_first_time_exposure(&self, exposure: &ExposureSamplingKey) -> bool {
        let sampling_key: SpecAndRuleHashTuple = (exposure.spec_name_hash, exposure.rule_id_hash);
        if self.sample_key_exists(&sampling_key) {
            return false;
        }

        match self.spec_sampling_set.try_write_for(Duration::from_secs(5)) {
            Some(mut sampling_map) => {
                sampling_map.insert(sampling_key);
            }
            None => {
                log_e!(TAG, "Failed to acquire write lock for spec sampling set");
            }
        }

        true
    }

    fn try_reset_spec_sampling_set(&self) {
        let ttl_ms = self.global_configs.get_exposure_spec_sampling_ttl_ms();
        let now = Utc::now().timestamp_millis() as u64;
        let last_sampling_reset = self.last_spec_sampling_reset.load(Ordering::Relaxed);
        let mut sampling_map = write_lock_or_noop!(TAG, self.spec_sampling_set);

        let has_expired = now - last_sampling_reset > ttl_ms;
        let is_full = sampling_map.len() > SAMPLING_MAX_KEYS;

        if has_expired || is_full {
            log_d!(
                TAG,
                "Resetting spec sampling set. has_expired: {:?}, is_full: {:?}",
                has_expired,
                is_full
            );
            sampling_map.clear();
            self.last_spec_sampling_reset.store(now, Ordering::Relaxed);
        }
    }

    fn try_reset_exposure_dedupe_set(&self) {
        self.try_reset_exposure_dedupe_set_at(self.exposure_dedupe_now_ms());
    }

    fn try_reset_exposure_dedupe_set_at(&self, now_ms: u64) {
        {
            let dedupe_state = match self
                .exposure_dedupe
                .try_read_for(crate::macros::LOCK_TIMEOUT)
            {
                Some(state) => state,
                None => {
                    log_e!(TAG, "Failed to acquire read lock for exposure dedupe set");
                    return;
                }
            };

            if !dedupe_state.sweep_due(now_ms) {
                return;
            }
        }

        let mut dedupe_state = match self
            .exposure_dedupe
            .try_write_for(crate::macros::LOCK_TIMEOUT)
        {
            Some(state) => state,
            None => {
                log_e!(TAG, "Failed to acquire write lock for exposure dedupe set");
                return;
            }
        };

        if !dedupe_state.sweep_due(now_ms) {
            return;
        }

        dedupe_state.remove_expired_entries(now_ms);
        dedupe_state.shrink_if_oversized();
    }

    fn sample_key_exists(&self, key: &SpecAndRuleHashTuple) -> bool {
        match self.spec_sampling_set.try_read_for(Duration::from_secs(5)) {
            Some(map) => map.contains(key),
            None => false,
        }
    }

    fn get_special_case_sampling_rate<'a>(
        &self,
        exposure: &'a impl QueuedExposure<'a>,
    ) -> Option<u64> {
        let rule_id = exposure.get_rule_id_ref();
        match rule_id {
            "default" | "disabled" | "" => self.global_configs.get_special_case_sampling_rate(),
            _ => None,
        }
    }
}

impl GlobalConfigs {
    fn get_sampling_mode(&self) -> Option<EvtSamplingMode> {
        fn parse_sampling_mode(sampling_mode: Option<&DynamicValue>) -> Option<EvtSamplingMode> {
            let v = sampling_mode?.string_value.as_ref()?.value.as_str();

            match v {
                "on" => Some(EvtSamplingMode::On),
                "shadow" => Some(EvtSamplingMode::Shadow),
                _ => None,
            }
        }

        self.use_sdk_config_value("sampling_mode", parse_sampling_mode)
    }

    fn get_special_case_sampling_rate(&self) -> Option<u64> {
        fn parse_special_case_sampling_rate(value: Option<&DynamicValue>) -> Option<u64> {
            match value {
                Some(value) => value.float_value.map(|rate| rate as u64),
                None => None,
            }
        }

        self.use_sdk_config_value(
            "special_case_sampling_rate",
            parse_special_case_sampling_rate,
        )
    }

    fn get_exposure_spec_sampling_ttl_ms(&self) -> u64 {
        fn parse_exposure_spec_sampling_ttl_ms(value: Option<&DynamicValue>) -> u64 {
            match value {
                Some(value) => value
                    .float_value
                    .map(|ttl_ms| ttl_ms as u64)
                    .unwrap_or(DEFAULT_EXPOSURE_SAMPLING_TTL_MS),
                None => DEFAULT_EXPOSURE_SAMPLING_TTL_MS,
            }
        }

        self.use_sdk_config_value(
            "exposure_spec_sampling_ttl_ms",
            parse_exposure_spec_sampling_ttl_ms,
        )
    }
}

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
pub struct ExposureSamplingKey {
    pub spec_name_hash: u64,
    pub rule_id_hash: u64,
    pub user_values_hash: u64,
    pub additional_hash: u64,
}

impl ExposureSamplingKey {
    pub fn new(
        evaluation: Option<&BaseEvaluation>,
        user: &UserData,
        additional_hash: u64,
        unit_id_type: Option<&str>,
    ) -> Self {
        Self::new_from_user_values_hash(
            evaluation,
            user.create_exposure_dedupe_user_hash(unit_id_type),
            additional_hash,
        )
    }

    pub fn new_from_user_values_hash(
        evaluation: Option<&BaseEvaluation>,
        user_values_hash: u64,
        additional_hash: u64,
    ) -> Self {
        let spec_name_hash = evaluation.as_ref().map_or(0, |e| e.name.hash);
        let rule_id_hash = evaluation.as_ref().map_or(0, |e| e.rule_id.hash);

        Self {
            spec_name_hash,
            rule_id_hash,
            user_values_hash,
            additional_hash,
        }
    }

    pub fn is_sampled(&self, sampling_rate: Option<u64>) -> bool {
        let sampling_rate = match sampling_rate {
            Some(rate) => rate,
            None => return true, // without a sampling rate, we should sample
        };

        let final_hash =
            self.spec_name_hash ^ self.rule_id_hash ^ self.user_values_hash ^ self.additional_hash;

        final_hash.is_multiple_of(sampling_rate)
    }
}

#[cfg(test)]
mod partial_rollout_boost_tests {
    use super::*;
    use crate::{
        event_logging::{
            event_queue::queued_event::QueuedEvent,
            exposure_utils::get_statsig_metadata_with_sampling_decision,
        },
        hashing,
    };
    use serde_json::json;
    use std::collections::HashMap;

    struct TestExposure {
        rule_id: &'static str,
        key: ExposureSamplingKey,
        info: ExtraExposureInfo,
        primary_gate: bool,
    }

    impl EnqueueOperation for TestExposure {
        fn as_exposure(&self) -> Option<&impl QueuedExposure<'_>> {
            Some(self)
        }

        fn into_queued_event(self, _: EvtSamplingDecision) -> QueuedEvent {
            unreachable!("sampling tests never enqueue their synthetic exposures")
        }
    }

    impl<'a> QueuedExposure<'a> for TestExposure {
        fn create_exposure_sampling_key(&self) -> ExposureSamplingKey {
            self.key.clone()
        }

        fn get_rule_id_ref(&'a self) -> &'a str {
            self.rule_id
        }

        fn get_extra_exposure_info_ref(&'a self) -> Option<&'a ExtraExposureInfo> {
            Some(&self.info)
        }

        fn is_primary_gate_exposure(&self) -> bool {
            self.primary_gate
        }
    }

    fn enabled_config() -> PartialRolloutBoostConfig {
        PartialRolloutBoostConfig {
            duration_seconds: 3_600,
            window_seconds: 300,
            per_rollout_limit: 2,
            global_limit: 5,
        }
    }

    fn enabled_sampler() -> ExposureSampling {
        enabled_sampler_for_rollout("partial-rollout-gate", "partial-rollout-rule")
    }

    fn enabled_sampler_for_rollout(gate_name: &str, rule_id: &str) -> ExposureSampling {
        let sampler = ExposureSampling::new(&format!(
            "partial-rollout-boost-test-{}",
            uuid::Uuid::new_v4()
        ));
        sampler.global_configs.set_sdk_configs(rollout_sdk_configs(
            gate_name,
            rule_id,
            Utc::now().timestamp_millis() as u64,
            50.0,
        ));
        sampler
    }

    fn rollout_sdk_configs(
        gate_name: &str,
        rule_id: &str,
        start_time: u64,
        rollout_percentage: f64,
    ) -> HashMap<String, DynamicValue> {
        HashMap::from([
            ("sampling_mode".to_string(), DynamicValue::from_string("on")),
            (
                "rollout_boost_enabled".to_string(),
                DynamicValue::from_i64(1),
            ),
            (
                "rollout_boost_duration_seconds".to_string(),
                DynamicValue::from_i64(3_600),
            ),
            (
                "rollout_boost_window_seconds".to_string(),
                DynamicValue::from_i64(300),
            ),
            (
                "rollout_boost_per_rollout_limit".to_string(),
                DynamicValue::from_i64(2),
            ),
            (
                "rollout_boost_global_limit".to_string(),
                DynamicValue::from_i64(5),
            ),
            (
                "rollout_boost_max_rollouts".to_string(),
                DynamicValue::from_i64(4),
            ),
            (
                "rollout_boost_rules".to_string(),
                rollout_sidecar_for(gate_name, rule_id, start_time, rollout_percentage),
            ),
        ])
    }

    fn rollout_sidecar_for(
        gate_name: &str,
        rule_id: &str,
        start_time: u64,
        rollout_percentage: f64,
    ) -> DynamicValue {
        DynamicValue::from_string(
            json!({
                gate_name: {
                    rule_id: [start_time, rollout_percentage],
                },
            })
            .to_string(),
        )
    }

    fn rollout_hashes(gate_name: &str, rule_id: &str) -> (u64, u64) {
        (
            hashing::hash_one(gate_name.as_bytes()),
            hashing::hash_one(rule_id.as_bytes()),
        )
    }

    fn exposure(spec_name_hash: u64, rule_id_hash: u64, user_values_hash: u64) -> TestExposure {
        TestExposure {
            rule_id: "partial-rollout-rule",
            key: ExposureSamplingKey {
                spec_name_hash,
                rule_id_hash,
                user_values_hash,
                additional_hash: 0,
            },
            info: ExtraExposureInfo {
                sampling_rate: Some(201),
                rule_pass_percentage: Some(50.0),
                ..ExtraExposureInfo::default()
            },
            primary_gate: true,
        }
    }

    fn next_deterministic_miss(
        spec_name_hash: u64,
        rule_id_hash: u64,
        cursor: &mut u64,
    ) -> TestExposure {
        loop {
            *cursor += 1;
            let candidate = exposure(spec_name_hash, rule_id_hash, *cursor);
            if !candidate.key.is_sampled(candidate.info.sampling_rate) {
                return candidate;
            }
        }
    }

    #[test]
    fn partial_rollout_boost_enforces_fixed_windows() {
        let mut limiter = PartialRolloutBoostLimiter::default();
        let config = PartialRolloutBoostConfig {
            window_seconds: 1,
            per_rollout_limit: 1,
            global_limit: 1,
            ..enabled_config()
        };

        let first_rollout = (1, 11, 100);
        let second_rollout = (2, 22, 200);
        assert!(limiter.try_admit(first_rollout, 300_000, config));
        assert!(!limiter.try_admit(first_rollout, 300_000, config));
        assert!(!limiter.try_admit(second_rollout, 300_999, config));
        assert!(!limiter.rollout_counts.contains_key(&second_rollout));
        assert!(limiter.try_admit(second_rollout, 301_000, config));
        assert_eq!(limiter.boosted_count, 1);
        assert_eq!(limiter.rollout_counts.len(), 1);

        let mut generation_limiter = PartialRolloutBoostLimiter::default();
        let generation_config = PartialRolloutBoostConfig {
            global_limit: 2,
            ..config
        };
        assert!(generation_limiter.try_admit(first_rollout, 300_000, generation_config));
        assert!(!generation_limiter.try_admit(first_rollout, 300_001, generation_config));
        assert!(generation_limiter.try_admit((1, 11, 101), 300_002, generation_config));
        assert!(!generation_limiter.try_admit(second_rollout, 300_003, generation_config));
        assert_eq!(generation_limiter.boosted_count, 2);

        let mut refreshed_window_limiter = PartialRolloutBoostLimiter::default();
        assert!(refreshed_window_limiter.try_admit(first_rollout, 500, config));
        let refreshed_config = PartialRolloutBoostConfig {
            window_seconds: 2,
            ..config
        };
        assert!(refreshed_window_limiter.try_admit(second_rollout, 500, refreshed_config));
        assert!(!refreshed_window_limiter.try_admit(first_rollout, 501, refreshed_config));

        let increased_limits = PartialRolloutBoostConfig {
            per_rollout_limit: 2,
            global_limit: 2,
            ..refreshed_config
        };
        assert!(refreshed_window_limiter.try_admit(second_rollout, 502, increased_limits));
        assert!(!refreshed_window_limiter.try_admit(second_rollout, 503, increased_limits));
        assert!(!refreshed_window_limiter.try_admit(
            (3, 33, 300),
            504,
            PartialRolloutBoostConfig {
                window_seconds: u64::MAX,
                ..enabled_config()
            },
        ));
    }

    #[test]
    fn partial_rollout_boost_limits_are_owned_by_each_sdk_instance() {
        let sdk_instance_id = format!("partial-rollout-boost-test-{}", uuid::Uuid::new_v4());
        let first_sampler = ExposureSampling::new(&sdk_instance_id);
        let second_sampler = ExposureSampling::new(&sdk_instance_id);
        let start_time = Utc::now().timestamp_millis() as u64;

        let mut configs = rollout_sdk_configs("first-gate", "first-rule", start_time, 50.0);
        configs.insert(
            "rollout_boost_rules".to_string(),
            DynamicValue::from_string(
                json!({
                    "first-gate": { "first-rule": [start_time, 50.0] },
                    "second-gate": { "second-rule": [start_time, 50.0] },
                    "third-gate": { "third-rule": [start_time, 50.0] },
                })
                .to_string(),
            ),
        );
        first_sampler.global_configs.set_sdk_configs(configs);

        for sampler in [&first_sampler, &second_sampler] {
            assert_eq!(
                sampler.partial_rollout_boost_limiter.lock().boosted_count,
                0
            );

            for (gate_name, rule_id, limit) in [
                ("first-gate", "first-rule", 2),
                ("second-gate", "second-rule", 2),
                ("third-gate", "third-rule", 1),
            ] {
                let (spec_name_hash, rule_id_hash) = rollout_hashes(gate_name, rule_id);
                let mut cursor = 0;
                let budget_before = sampler.partial_rollout_boost_limiter.lock().boosted_count;
                let first = next_deterministic_miss(spec_name_hash, rule_id_hash, &mut cursor);
                assert!(matches!(
                    sampler.get_sampling_decision(&first, false),
                    EvtSamplingDecision::ForceSampled,
                ));

                let baseline =
                    exposure(spec_name_hash, rule_id_hash, spec_name_hash ^ rule_id_hash);
                assert!(matches!(
                    sampler.get_sampling_decision(&baseline, false),
                    EvtSamplingDecision::Sampled(Some(201), EvtSamplingMode::On, true),
                ));
                assert_eq!(
                    sampler.partial_rollout_boost_limiter.lock().boosted_count,
                    budget_before,
                );

                for _ in 0..limit {
                    let miss = next_deterministic_miss(spec_name_hash, rule_id_hash, &mut cursor);
                    assert!(matches!(
                        sampler.get_sampling_decision(&miss, false),
                        EvtSamplingDecision::BoostedPartialRollout,
                    ));
                }

                let exhausted = next_deterministic_miss(spec_name_hash, rule_id_hash, &mut cursor);
                assert!(matches!(
                    sampler.get_sampling_decision(&exhausted, false),
                    EvtSamplingDecision::NotSampled,
                ));
            }

            let limiter = sampler.partial_rollout_boost_limiter.lock();
            assert_eq!(limiter.boosted_count, 5);
            assert_eq!(limiter.rollout_counts.len(), 3);
        }
    }

    #[test]
    fn scheduled_partial_rollout_respects_configured_duration() {
        let sampler = enabled_sampler();
        let (spec_name_hash, rule_id_hash) =
            rollout_hashes("partial-rollout-gate", "partial-rollout-rule");
        let start_time = 4_000_000_000_000;
        let mut configs = rollout_sdk_configs(
            "partial-rollout-gate",
            "partial-rollout-rule",
            start_time,
            50.0,
        );
        configs.insert(
            "rollout_boost_duration_seconds".to_string(),
            DynamicValue::from_i64(60),
        );
        sampler.global_configs.set_sdk_configs(configs);

        let (rollout, config) = sampler
            .global_configs
            .get_partial_rollout_boost(spec_name_hash, rule_id_hash)
            .expect("a complete DCS payload must retain its scheduled rollout");
        let sample = exposure(spec_name_hash, rule_id_hash, 1);

        assert_eq!(config.duration_seconds, 60);
        assert!(!sampler.should_boost_partial_rollout_at(
            &sample.key,
            rollout,
            config,
            start_time - 1,
        ));
        assert!(sampler.should_boost_partial_rollout_at(&sample.key, rollout, config, start_time));
        assert!(!sampler.should_boost_partial_rollout_at(
            &sample.key,
            rollout,
            config,
            start_time + 60_000,
        ));
        assert!(!sampler.should_boost_partial_rollout_at(
            &sample.key,
            rollout,
            PartialRolloutBoostConfig {
                duration_seconds: u64::MAX,
                ..config
            },
            start_time,
        ));
    }

    #[test]
    fn ineligible_rollouts_preserve_normal_sampling_and_respect_live_disable() {
        let sampler = enabled_sampler();
        let now_ms = Utc::now().timestamp_millis() as u64;
        let (spec_name_hash, rule_id_hash) =
            rollout_hashes("partial-rollout-gate", "partial-rollout-rule");
        let mut cursor = 0;

        let warmup = next_deterministic_miss(spec_name_hash, rule_id_hash, &mut cursor);
        assert!(matches!(
            sampler.get_sampling_decision(&warmup, false),
            EvtSamplingDecision::ForceSampled,
        ));

        sampler.global_configs.set_sdk_configs(rollout_sdk_configs(
            "partial-rollout-gate",
            "partial-rollout-rule",
            now_ms,
            49.0,
        ));

        let missed = next_deterministic_miss(spec_name_hash, rule_id_hash, &mut cursor);
        assert!(matches!(
            sampler.get_sampling_decision(&missed, false),
            EvtSamplingDecision::NotSampled,
        ));

        let baseline = exposure(
            spec_name_hash,
            rule_id_hash,
            spec_name_hash ^ rule_id_hash ^ ((cursor + 1) * 201),
        );
        assert!(matches!(
            sampler.get_sampling_decision(&baseline, false),
            EvtSamplingDecision::Sampled(Some(201), EvtSamplingMode::On, true),
        ));

        {
            let limiter = sampler.partial_rollout_boost_limiter.lock();
            assert_eq!(limiter.boosted_count, 0);
            assert!(limiter.rollout_counts.is_empty());
        }

        sampler.global_configs.set_sdk_configs(rollout_sdk_configs(
            "partial-rollout-gate",
            "partial-rollout-rule",
            Utc::now().timestamp_millis() as u64,
            50.0,
        ));

        let mut secondary = next_deterministic_miss(spec_name_hash, rule_id_hash, &mut cursor);
        secondary.primary_gate = false;
        assert!(matches!(
            sampler.get_sampling_decision(&secondary, false),
            EvtSamplingDecision::NotSampled,
        ));

        let boosted = next_deterministic_miss(spec_name_hash, rule_id_hash, &mut cursor);
        assert!(matches!(
            sampler.get_sampling_decision(&boosted, false),
            EvtSamplingDecision::BoostedPartialRollout,
        ));

        let mut incomplete = rollout_sdk_configs(
            "partial-rollout-gate",
            "partial-rollout-rule",
            Utc::now().timestamp_millis() as u64,
            50.0,
        );
        incomplete.remove("rollout_boost_global_limit");
        sampler.global_configs.set_sdk_configs(incomplete);

        let incomplete_miss = next_deterministic_miss(spec_name_hash, rule_id_hash, &mut cursor);
        assert!(matches!(
            sampler.get_sampling_decision(&incomplete_miss, false),
            EvtSamplingDecision::NotSampled,
        ));

        sampler.global_configs.set_sdk_configs(HashMap::from([
            (
                "rollout_boost_enabled".to_string(),
                DynamicValue::from_i64(0),
            ),
            (
                "rollout_boost_rules".to_string(),
                DynamicValue::from_string("{}"),
            ),
        ]));

        let disabled = next_deterministic_miss(spec_name_hash, rule_id_hash, &mut cursor);
        assert!(matches!(
            sampler.get_sampling_decision(&disabled, false),
            EvtSamplingDecision::NotSampled,
        ));
        assert_eq!(
            sampler.partial_rollout_boost_limiter.lock().boosted_count,
            1
        );
    }

    #[test]
    fn partial_rollout_boost_marks_only_actually_boosted_primary_events() {
        let boosted =
            get_statsig_metadata_with_sampling_decision(EvtSamplingDecision::BoostedPartialRollout);
        assert_eq!(boosted.get("samplingMode"), Some(&json!("on")));
        assert_eq!(boosted.get("samplingRate"), Some(&json!(1)));
        assert_eq!(boosted.get("samplingReason"), Some(&json!("rollout_boost")));
        assert!(!boosted.contains_key("rollout_start_time"));

        let baseline = get_statsig_metadata_with_sampling_decision(EvtSamplingDecision::Sampled(
            Some(1),
            EvtSamplingMode::On,
            true,
        ));
        assert!(!baseline.contains_key("samplingReason"));
        assert!(
            get_statsig_metadata_with_sampling_decision(EvtSamplingDecision::ForceSampled)
                .is_empty()
        );
    }
}

#[cfg(test)]
mod exposure_dedupe_tests {
    use super::{
        DEDUPE_MIN_RETAINED_CAPACITY, ExposureSampling, ExposureSamplingKey, SAMPLING_MAX_KEYS,
    };
    use crate::{DynamicValue, global_configs::GlobalConfigs};
    use std::{
        collections::HashMap,
        sync::{
            Arc, Barrier,
            atomic::{AtomicU64, AtomicUsize, Ordering},
        },
        thread,
    };

    fn sampler_with_ttl(ttl_ms: u64) -> ExposureSampling {
        static NEXT_INSTANCE_ID: AtomicU64 = AtomicU64::new(0);

        let instance_id = format!(
            "exposure-dedupe-unit-test-{}",
            NEXT_INSTANCE_ID.fetch_add(1, Ordering::Relaxed)
        );
        let global_configs = GlobalConfigs::get_instance(&instance_id);
        global_configs.set_sdk_configs(HashMap::from([(
            "exposure_dedupe_ttl_ms".to_string(),
            DynamicValue::from_i64(i64::try_from(ttl_ms).expect("test TTL must fit in i64")),
        )]));

        ExposureSampling::new(&instance_id)
    }

    fn exposure_key(user_values_hash: u64) -> ExposureSamplingKey {
        ExposureSamplingKey {
            spec_name_hash: 1,
            rule_id_hash: 2,
            user_values_hash,
            additional_hash: 0,
        }
    }

    fn fill_cache(sampler: &ExposureSampling, expiration_for: impl Fn(usize) -> u64) {
        let mut state = sampler.exposure_dedupe.write();
        state.entries.reserve(SAMPLING_MAX_KEYS);
        for index in 0..SAMPLING_MAX_KEYS {
            state
                .entries
                .insert(exposure_key(index as u64), expiration_for(index));
        }
        state.next_expiration_ms = state.entries.values().copied().min();
    }

    #[test]
    fn exposure_dedupe_expires_at_exact_boundary_without_extending_duplicate_hits() {
        let sampler = sampler_with_ttl(10);
        let key = exposure_key(1);

        assert!(!sampler.should_dedupe_exposure_at(&key, 100));
        assert!(sampler.should_dedupe_exposure_at(&key, 101));
        assert!(sampler.should_dedupe_exposure_at(&key, 109));
        assert!(!sampler.should_dedupe_exposure_at(&key, 110));
        assert!(sampler.should_dedupe_exposure_at(&key, 119));
        assert!(!sampler.should_dedupe_exposure_at(&key, 120));
    }

    #[test]
    fn exposure_dedupe_cleanup_preserves_entries_with_later_expirations() {
        let sampler = sampler_with_ttl(10);
        let first_key = exposure_key(1);
        let second_key = exposure_key(2);

        assert!(!sampler.should_dedupe_exposure_at(&first_key, 100));
        assert!(!sampler.should_dedupe_exposure_at(&second_key, 105));

        {
            let state = sampler.exposure_dedupe.read();
            sampler.try_reset_exposure_dedupe_set_at(109);
            assert_eq!(state.entries.get(&first_key), Some(&110));
        }

        sampler.try_reset_exposure_dedupe_set_at(110);

        let state = sampler.exposure_dedupe.read();
        assert!(!state.entries.contains_key(&first_key));
        assert_eq!(state.entries.get(&second_key), Some(&115));
        assert_eq!(state.next_expiration_ms, Some(115));
        drop(state);

        assert!(sampler.should_dedupe_exposure_at(&second_key, 110));
        assert!(!sampler.should_dedupe_exposure_at(&first_key, 110));
    }

    #[test]
    fn exposure_dedupe_full_cache_fails_open_without_a_write_lock() {
        let sampler = sampler_with_ttl(50);
        fill_cache(&sampler, |_| 100);

        let new_key = exposure_key(SAMPLING_MAX_KEYS as u64);
        {
            let state = sampler.exposure_dedupe.read();
            assert!(!sampler.should_dedupe_exposure_at(&new_key, 50));
            assert!(!sampler.should_dedupe_exposure_at(&new_key, 51));
            assert!(sampler.should_dedupe_exposure_at(&exposure_key(0), 51));
            assert_eq!(state.entries.len(), SAMPLING_MAX_KEYS);
            assert!(!state.entries.contains_key(&new_key));
        }

        assert!(!sampler.should_dedupe_exposure_at(&new_key, 100));

        let state = sampler.exposure_dedupe.read();
        assert_eq!(state.entries.len(), 1);
        assert_eq!(state.entries.get(&new_key), Some(&150));
    }

    #[test]
    fn exposure_dedupe_full_cache_reclaims_only_expired_entries_before_admission() {
        let sampler = sampler_with_ttl(25);
        fill_cache(&sampler, |index| if index == 0 { 100 } else { 200 });

        let new_key = exposure_key(SAMPLING_MAX_KEYS as u64);
        assert!(!sampler.should_dedupe_exposure_at(&new_key, 100));

        let state = sampler.exposure_dedupe.read();
        assert_eq!(state.entries.len(), SAMPLING_MAX_KEYS);
        assert!(!state.entries.contains_key(&exposure_key(0)));
        assert_eq!(state.entries.get(&exposure_key(1)), Some(&200));
        assert_eq!(state.entries.get(&new_key), Some(&125));
    }

    #[test]
    fn request_sweep_prevents_background_sweep_until_shared_cooldown_expires() {
        let sampler = sampler_with_ttl(50);
        fill_cache(&sampler, |index| match index {
            0 => 100,
            1 => 101,
            _ => 2_000,
        });

        let admitted_key = exposure_key(SAMPLING_MAX_KEYS as u64);
        assert!(!sampler.should_dedupe_exposure_at(&admitted_key, 100));
        assert_eq!(sampler.exposure_dedupe.read().next_sweep_ms, 1_100);

        sampler.try_reset_exposure_dedupe_set_at(101);
        {
            let state = sampler.exposure_dedupe.read();
            assert!(state.entries.contains_key(&exposure_key(1)));
            assert!(
                !sampler
                    .should_dedupe_exposure_at(&exposure_key(SAMPLING_MAX_KEYS as u64 + 1), 101,)
            );
        }

        sampler.try_reset_exposure_dedupe_set_at(1_100);
        let state = sampler.exposure_dedupe.read();
        assert!(!state.entries.contains_key(&exposure_key(1)));
        assert_eq!(state.next_sweep_ms, 2_100);
    }

    #[test]
    fn background_sweep_prevents_request_sweep_until_shared_cooldown_expires() {
        let sampler = sampler_with_ttl(2_000);
        fill_cache(&sampler, |index| match index {
            0 => 100,
            1 => 101,
            _ => 3_000,
        });

        sampler.try_reset_exposure_dedupe_set_at(100);
        assert_eq!(sampler.exposure_dedupe.read().next_sweep_ms, 1_100);

        let admitted_key = exposure_key(SAMPLING_MAX_KEYS as u64);
        assert!(!sampler.should_dedupe_exposure_at(&admitted_key, 100));
        assert_eq!(
            sampler.exposure_dedupe.read().entries.len(),
            SAMPLING_MAX_KEYS,
        );

        let throttled_key = exposure_key(SAMPLING_MAX_KEYS as u64 + 1);
        {
            let state = sampler.exposure_dedupe.read();
            assert!(!sampler.should_dedupe_exposure_at(&throttled_key, 101));
            assert_eq!(state.entries.len(), SAMPLING_MAX_KEYS);
            assert!(state.entries.contains_key(&exposure_key(1)));
            assert!(!state.entries.contains_key(&throttled_key));
        }

        assert!(!sampler.should_dedupe_exposure_at(&throttled_key, 1_100));
        let state = sampler.exposure_dedupe.read();
        assert_eq!(state.entries.len(), SAMPLING_MAX_KEYS);
        assert!(!state.entries.contains_key(&exposure_key(1)));
        assert_eq!(state.entries.get(&throttled_key), Some(&3_100));
        assert_eq!(state.next_sweep_ms, 2_100);
    }

    #[test]
    fn exposure_dedupe_capacity_cleanup_does_not_shrink_on_request_path() {
        let sampler = sampler_with_ttl(50);
        fill_cache(&sampler, |_| 100);

        let new_key = exposure_key(SAMPLING_MAX_KEYS as u64);
        assert!(!sampler.should_dedupe_exposure_at(&new_key, 100));

        let request_path_capacity = {
            let state = sampler.exposure_dedupe.read();
            assert_eq!(state.entries.len(), 1);
            // Removed entries can reduce hashbrown's reported usable capacity
            // through tombstones even though the backing allocation is retained.
            assert!(state.entries.capacity() > DEDUPE_MIN_RETAINED_CAPACITY * 2);
            state.entries.capacity()
        };

        // The exposure still expires logically after 50 ms even though its
        // physical eviction waits for the shared one-second sweep cooldown.
        assert!(!sampler.should_dedupe_exposure_at(&new_key, 150));
        sampler.try_reset_exposure_dedupe_set_at(1_100);

        let state = sampler.exposure_dedupe.read();
        assert!(state.entries.is_empty());
        assert!(state.entries.capacity() < request_path_capacity);
        assert!(state.entries.capacity() <= DEDUPE_MIN_RETAINED_CAPACITY * 2);
        assert_eq!(state.next_expiration_ms, None);
    }

    #[test]
    fn exposure_dedupe_uses_updated_ttl_without_rewriting_existing_expirations() {
        let sampler = sampler_with_ttl(10);
        let original_key = exposure_key(1);
        let updated_key = exposure_key(2);

        assert!(!sampler.should_dedupe_exposure_at(&original_key, 100));
        sampler.global_configs.set_sdk_configs(HashMap::from([(
            "exposure_dedupe_ttl_ms".to_string(),
            DynamicValue::from_i64(25),
        )]));

        assert!(!sampler.should_dedupe_exposure_at(&updated_key, 101));

        let state = sampler.exposure_dedupe.read();
        assert_eq!(state.entries.get(&original_key), Some(&110));
        assert_eq!(state.entries.get(&updated_key), Some(&126));
    }

    #[test]
    fn zero_exposure_dedupe_ttl_disables_caching() {
        let sampler = sampler_with_ttl(0);
        let key = exposure_key(1);

        assert!(!sampler.should_dedupe_exposure_at(&key, 100));
        assert!(!sampler.should_dedupe_exposure_at(&key, 100));
        assert!(sampler.exposure_dedupe.read().entries.is_empty());
    }

    #[test]
    fn concurrent_duplicate_exposures_are_logged_exactly_once() {
        const THREAD_COUNT: usize = 16;
        const EXPOSURES_PER_THREAD: usize = 128;

        let sampler = Arc::new(sampler_with_ttl(10));
        let barrier = Arc::new(Barrier::new(THREAD_COUNT));
        let logged_count = Arc::new(AtomicUsize::new(0));

        thread::scope(|scope| {
            for _ in 0..THREAD_COUNT {
                let sampler = Arc::clone(&sampler);
                let barrier = Arc::clone(&barrier);
                let logged_count = Arc::clone(&logged_count);

                scope.spawn(move || {
                    let key = exposure_key(1);
                    barrier.wait();

                    for _ in 0..EXPOSURES_PER_THREAD {
                        if !sampler.should_dedupe_exposure_at(&key, 100) {
                            logged_count.fetch_add(1, Ordering::Relaxed);
                        }
                    }
                });
            }
        });

        assert_eq!(logged_count.load(Ordering::Relaxed), 1);
        assert_eq!(sampler.exposure_dedupe.read().entries.len(), 1);
    }
}

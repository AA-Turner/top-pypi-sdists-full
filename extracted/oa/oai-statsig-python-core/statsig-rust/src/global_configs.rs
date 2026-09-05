use crate::{DynamicValue, hashing, log_e};
use ahash::AHashMap;
use lazy_static::lazy_static;
use parking_lot::RwLock;
use std::{
    collections::HashMap,
    sync::{
        Arc, Weak,
        atomic::{AtomicBool, AtomicU64, Ordering},
    },
    time::Duration,
};

const TAG: &str = stringify!(GlobalConfigs);

pub const MAX_SAMPLING_RATE: f64 = 10000.0;
const DEFAULT_EXPOSURE_DEDUPE_TTL_MS: u64 = 60_000;
const ROLLOUT_BOOST_RULES_CONFIG: &str = "rollout_boost_rules";
const ROLLOUT_BOOST_MAX_ROLLOUTS_CONFIG: &str = "rollout_boost_max_rollouts";

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) struct PartialRolloutBoostConfig {
    pub(crate) duration_seconds: u64,
    pub(crate) window_seconds: u64,
    pub(crate) per_rollout_limit: u64,
    pub(crate) global_limit: u64,
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub(crate) struct PartialRolloutBoostRule {
    pub(crate) start_time: u64,
    pub(crate) rollout_percentage: f64,
}

type PartialRolloutBoostRules = AHashMap<(u64, u64), PartialRolloutBoostRule>;
type PartialRolloutBoostSidecar = HashMap<String, HashMap<String, (u64, f64)>>;

#[derive(Default)]
struct PartialRolloutBoostState {
    config: Option<PartialRolloutBoostConfig>,
    rules: PartialRolloutBoostRules,
}

lazy_static! {
    static ref GLOBAL_CONFIG_INSTANCES: RwLock<HashMap<String, Weak<GlobalConfigs>>> =
        RwLock::new(HashMap::new());
}

struct Configs {
    sdk_configs: HashMap<String, DynamicValue>,
    partial_rollout_boost: PartialRolloutBoostState,
    sdk_flags: HashMap<String, bool>,
    diagnostics_sampling_rates: HashMap<String, f64>,
}

pub struct GlobalConfigs {
    configs: RwLock<Configs>,
    exposure_dedupe_ttl_ms: AtomicU64,
    partial_rollout_boost_enabled: AtomicBool,
}

impl GlobalConfigs {
    pub fn get_instance(sdk_key: &str) -> Arc<GlobalConfigs> {
        match GLOBAL_CONFIG_INSTANCES.try_read_for(Duration::from_secs(5)) {
            Some(read_guard) => {
                if let Some(instance) = read_guard.get(sdk_key) {
                    if let Some(instance) = instance.upgrade() {
                        return instance.clone();
                    }
                }
            }
            None => {
                log_e!(
                    TAG,
                    "Failed to get read guard: Failed to lock GLOBAL_CONFIG_INSTANCES"
                );
            }
        }

        let instance = Arc::new(GlobalConfigs {
            configs: RwLock::new(Configs {
                sdk_configs: HashMap::new(),
                partial_rollout_boost: PartialRolloutBoostState::default(),
                sdk_flags: HashMap::new(),
                diagnostics_sampling_rates: HashMap::from([
                    ("initialize".to_string(), 10000.0),
                    ("config_sync".to_string(), 1000.0),
                    ("dcs".to_string(), 1000.0),
                    ("get_id_list".to_string(), 100.0), // default sampling rates
                ]),
            }),
            exposure_dedupe_ttl_ms: AtomicU64::new(DEFAULT_EXPOSURE_DEDUPE_TTL_MS),
            partial_rollout_boost_enabled: AtomicBool::new(false),
        });

        match GLOBAL_CONFIG_INSTANCES.try_write_for(Duration::from_secs(5)) {
            Some(mut write_guard) => {
                write_guard.insert(sdk_key.into(), Arc::downgrade(&instance));
            }
            None => {
                log_e!(
                    TAG,
                    "Failed to get write guard: Failed to lock GLOBAL_CONFIG_INSTANCES"
                );
            }
        }

        instance
    }

    pub fn set_sdk_configs(&self, new_configs: HashMap<String, DynamicValue>) {
        let partial_rollout_boost = Self::partial_rollout_boost_config(&new_configs)
            .map(|(config, max_rollouts)| PartialRolloutBoostState {
                config: Some(config),
                rules: Self::parse_partial_rollout_boost_rules(
                    new_configs.get(ROLLOUT_BOOST_RULES_CONFIG),
                    max_rollouts,
                ),
            })
            .unwrap_or_default();
        let partial_rollout_boost_enabled =
            partial_rollout_boost.config.is_some() && !partial_rollout_boost.rules.is_empty();
        let exposure_dedupe_ttl_ms = new_configs.get("exposure_dedupe_ttl_ms").map(|value| {
            value
                .float_value
                .map(|ttl_ms| ttl_ms as u64)
                .unwrap_or(DEFAULT_EXPOSURE_DEDUPE_TTL_MS)
        });

        match self.configs.try_write_for(Duration::from_secs(5)) {
            Some(mut configs_guard) => {
                configs_guard.partial_rollout_boost = partial_rollout_boost;
                configs_guard.sdk_configs.extend(new_configs);
                if let Some(ttl_ms) = exposure_dedupe_ttl_ms {
                    self.exposure_dedupe_ttl_ms.store(ttl_ms, Ordering::Relaxed);
                }
                self.partial_rollout_boost_enabled
                    .store(partial_rollout_boost_enabled, Ordering::Relaxed);
            }
            None => {
                log_e!(TAG, "Failed to get write guard: Failed to lock configs");
            }
        }
    }

    pub(crate) fn get_exposure_dedupe_ttl_ms(&self) -> u64 {
        self.exposure_dedupe_ttl_ms.load(Ordering::Relaxed)
    }

    fn positive_rollout_value(value: Option<&DynamicValue>) -> Option<u64> {
        value
            .and_then(|value| value.json_value.as_u64())
            .filter(|value| *value > 0)
    }

    fn partial_rollout_boost_config(
        configs: &HashMap<String, DynamicValue>,
    ) -> Option<(PartialRolloutBoostConfig, usize)> {
        let enabled = configs.get("rollout_boost_enabled").is_some_and(|value| {
            value.json_value.as_bool() == Some(true) || value.json_value.as_u64() == Some(1)
        });
        if !enabled {
            return None;
        }

        let max_rollouts =
            Self::positive_rollout_value(configs.get(ROLLOUT_BOOST_MAX_ROLLOUTS_CONFIG))
                .and_then(|value| usize::try_from(value).ok())?;

        let config = PartialRolloutBoostConfig {
            duration_seconds: Self::positive_rollout_value(
                configs.get("rollout_boost_duration_seconds"),
            )?,
            window_seconds: Self::positive_rollout_value(
                configs.get("rollout_boost_window_seconds"),
            )?,
            per_rollout_limit: Self::positive_rollout_value(
                configs.get("rollout_boost_per_rollout_limit"),
            )?,
            global_limit: Self::positive_rollout_value(configs.get("rollout_boost_global_limit"))?,
        };

        Some((config, max_rollouts))
    }

    fn parse_partial_rollout_boost_rules(
        value: Option<&DynamicValue>,
        max_rollouts: usize,
    ) -> PartialRolloutBoostRules {
        let Some(value) = value else {
            return AHashMap::new();
        };

        if !value.json_value.is_string() {
            return AHashMap::new();
        }

        let Some(serialized) = value
            .string_value
            .as_ref()
            .map(|value| value.value.as_str())
        else {
            return AHashMap::new();
        };

        let Ok(sidecar) = serde_json::from_str::<PartialRolloutBoostSidecar>(serialized) else {
            return AHashMap::new();
        };

        let mut rules = AHashMap::new();
        for (gate_name, gate_rules) in sidecar {
            if gate_name.is_empty() || gate_rules.is_empty() {
                return AHashMap::new();
            }

            if gate_rules.len() > max_rollouts.saturating_sub(rules.len()) {
                return AHashMap::new();
            }

            let gate_hash = hashing::hash_one(gate_name.as_bytes());
            for (rule_id, (start_time, rollout_percentage)) in gate_rules {
                if rule_id.is_empty()
                    || start_time == 0
                    || !rollout_percentage.is_finite()
                    || !(0.0 < rollout_percentage && rollout_percentage < 100.0)
                {
                    return AHashMap::new();
                }

                if rules
                    .insert(
                        (gate_hash, hashing::hash_one(rule_id.as_bytes())),
                        PartialRolloutBoostRule {
                            start_time,
                            rollout_percentage,
                        },
                    )
                    .is_some()
                {
                    return AHashMap::new();
                }
            }
        }

        rules
    }

    pub(crate) fn get_partial_rollout_boost(
        &self,
        gate_hash: u64,
        rule_hash: u64,
    ) -> Option<(PartialRolloutBoostRule, PartialRolloutBoostConfig)> {
        if !self.partial_rollout_boost_enabled.load(Ordering::Relaxed) {
            return None;
        }

        let configs = self.configs.read();
        let config = configs.partial_rollout_boost.config?;
        configs
            .partial_rollout_boost
            .rules
            .get(&(gate_hash, rule_hash))
            .copied()
            .map(|rule| (rule, config))
    }

    pub fn set_sdk_flags(&self, new_configs: HashMap<String, bool>) {
        match self.configs.try_write_for(Duration::from_secs(5)) {
            Some(mut configs_guard) => {
                for (key, value) in new_configs {
                    configs_guard.sdk_flags.insert(key, value);
                }
            }
            None => {
                log_e!(TAG, "Failed to get write guard: Failed to lock configs");
            }
        }
    }

    pub fn set_diagnostics_sampling_rates(&self, new_sampling_rate: HashMap<String, f64>) {
        match self.configs.try_write_for(Duration::from_secs(5)) {
            Some(mut configs_guard) => {
                for (key, rate) in new_sampling_rate {
                    let clamped_rate = rate.clamp(0.0, MAX_SAMPLING_RATE);
                    configs_guard
                        .diagnostics_sampling_rates
                        .insert(key, clamped_rate);
                }
            }
            None => {
                log_e!(TAG, "Failed to get write guard: Failed to lock configs");
            }
        }
    }

    pub fn use_sdk_config_value<T>(
        &self,
        key: &str,
        f: impl FnOnce(Option<&DynamicValue>) -> T,
    ) -> T {
        match self.configs.try_read_for(Duration::from_secs(5)) {
            Some(configs_guard) => f(configs_guard.sdk_configs.get(key)),
            None => {
                log_e!(TAG, "Failed to get read guard: Failed to lock configs");
                f(None)
            }
        }
    }

    pub fn use_diagnostics_sampling_rate<T>(
        &self,
        key: &str,
        f: impl FnOnce(Option<&f64>) -> T,
    ) -> T {
        match self.configs.try_read_for(Duration::from_secs(5)) {
            Some(configs_guard) => f(configs_guard.diagnostics_sampling_rates.get(key)),
            None => {
                log_e!(TAG, "Failed to get read guard: Failed to lock configs");
                f(None)
            }
        }
    }

    pub fn get_sdk_flag_value(&self, key: &str) -> bool {
        match self.configs.try_read_for(Duration::from_secs(5)) {
            Some(configs_guard) => *configs_guard.sdk_flags.get(key).unwrap_or(&false),
            None => {
                log_e!(TAG, "Failed to get read guard: Failed to lock configs");
                false
            }
        }
    }
}

#[cfg(test)]
mod partial_rollout_boost_sidecar_tests {
    use super::*;
    use serde_json::json;

    fn new_configs() -> Arc<GlobalConfigs> {
        GlobalConfigs::get_instance(&format!(
            "partial-rollout-sidecar-test-{}",
            uuid::Uuid::new_v4(),
        ))
    }

    fn complete_rollout_configs(sidecar: &str) -> HashMap<String, DynamicValue> {
        HashMap::from([
            (
                "rollout_boost_enabled".to_string(),
                DynamicValue::from_bool(true),
            ),
            (
                "rollout_boost_duration_seconds".to_string(),
                DynamicValue::from_i64(86_400),
            ),
            (
                "rollout_boost_window_seconds".to_string(),
                DynamicValue::from_i64(120),
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
                ROLLOUT_BOOST_MAX_ROLLOUTS_CONFIG.to_string(),
                DynamicValue::from_i64(4),
            ),
            (
                ROLLOUT_BOOST_RULES_CONFIG.to_string(),
                DynamicValue::from_string(sidecar),
            ),
        ])
    }

    fn lookup_rule(
        configs: &GlobalConfigs,
        gate_name: &str,
        rule_id: &str,
    ) -> Option<(PartialRolloutBoostRule, PartialRolloutBoostConfig)> {
        configs.get_partial_rollout_boost(
            hashing::hash_one(gate_name.as_bytes()),
            hashing::hash_one(rule_id.as_bytes()),
        )
    }

    fn valid_rule() -> serde_json::Value {
        json!([1_750_000_000_000_u64, 50.0])
    }

    fn rollout_sidecar(count: usize) -> String {
        let gates: serde_json::Map<String, serde_json::Value> = (0..count)
            .map(|index| {
                (
                    format!("gate_{index}"),
                    json!({ format!("rule_{index}"): valid_rule() }),
                )
            })
            .collect();

        serde_json::Value::Object(gates).to_string()
    }

    #[test]
    fn exposure_dedupe_ttl_updates_immediately_and_preserves_existing_config_semantics() {
        let configs = new_configs();
        assert_eq!(
            configs.get_exposure_dedupe_ttl_ms(),
            DEFAULT_EXPOSURE_DEDUPE_TTL_MS,
        );

        configs.set_sdk_configs(HashMap::from([(
            "exposure_dedupe_ttl_ms".to_string(),
            DynamicValue::from_i64(1_500),
        )]));
        assert_eq!(configs.get_exposure_dedupe_ttl_ms(), 1_500);

        configs.set_sdk_configs(HashMap::from([(
            "unrelated_setting".to_string(),
            DynamicValue::from_bool(true),
        )]));
        assert_eq!(configs.get_exposure_dedupe_ttl_ms(), 1_500);

        for (value, expected_ttl_ms) in [
            (DynamicValue::from_i64(0), 0),
            (DynamicValue::from_i64(-1), 0),
            (
                DynamicValue::from_string("invalid"),
                DEFAULT_EXPOSURE_DEDUPE_TTL_MS,
            ),
        ] {
            configs.set_sdk_configs(HashMap::from([(
                "exposure_dedupe_ttl_ms".to_string(),
                value,
            )]));
            assert_eq!(configs.get_exposure_dedupe_ttl_ms(), expected_ttl_ms);
        }
    }

    #[test]
    fn requires_complete_valid_rollout_configs_from_each_dcs_payload() {
        let configs = new_configs();
        let sidecar = rollout_sidecar(1);
        configs.set_sdk_configs(complete_rollout_configs(&sidecar));

        assert_eq!(
            lookup_rule(&configs, "gate_0", "rule_0"),
            Some((
                PartialRolloutBoostRule {
                    start_time: 1_750_000_000_000,
                    rollout_percentage: 50.0,
                },
                PartialRolloutBoostConfig {
                    duration_seconds: 86_400,
                    window_seconds: 120,
                    per_rollout_limit: 2,
                    global_limit: 5,
                },
            )),
        );

        for key in [
            "rollout_boost_enabled",
            "rollout_boost_duration_seconds",
            "rollout_boost_window_seconds",
            "rollout_boost_per_rollout_limit",
            "rollout_boost_global_limit",
            ROLLOUT_BOOST_MAX_ROLLOUTS_CONFIG,
            ROLLOUT_BOOST_RULES_CONFIG,
        ] {
            let mut incomplete = complete_rollout_configs(&sidecar);
            incomplete.remove(key);
            configs.set_sdk_configs(incomplete);
            assert!(
                lookup_rule(&configs, "gate_0", "rule_0").is_none(),
                "missing {key} must disable boosting instead of reusing stale values",
            );
            configs.set_sdk_configs(complete_rollout_configs(&sidecar));
        }

        for key in [
            "rollout_boost_duration_seconds",
            "rollout_boost_window_seconds",
            "rollout_boost_per_rollout_limit",
            "rollout_boost_global_limit",
            ROLLOUT_BOOST_MAX_ROLLOUTS_CONFIG,
        ] {
            let mut invalid = complete_rollout_configs(&sidecar);
            invalid.insert(key.to_string(), DynamicValue::from_i64(0));
            configs.set_sdk_configs(invalid);
            assert!(
                lookup_rule(&configs, "gate_0", "rule_0").is_none(),
                "invalid {key} must disable boosting",
            );
        }
    }

    #[test]
    fn rejects_malformed_and_over_budget_sidecars_without_clamping_valid_limits() {
        let configs = new_configs();
        let mut large_budget = complete_rollout_configs(&rollout_sidecar(129));
        large_budget.insert(
            ROLLOUT_BOOST_MAX_ROLLOUTS_CONFIG.to_string(),
            DynamicValue::from_i64(129),
        );
        configs.set_sdk_configs(large_budget);
        assert!(lookup_rule(&configs, "gate_128", "rule_128").is_some());

        let mut over_budget = complete_rollout_configs(&rollout_sidecar(3));
        over_budget.insert(
            ROLLOUT_BOOST_MAX_ROLLOUTS_CONFIG.to_string(),
            DynamicValue::from_i64(2),
        );
        configs.set_sdk_configs(over_budget);
        assert!(lookup_rule(&configs, "gate_0", "rule_0").is_none());

        for sidecar in [
            "{not valid json".to_string(),
            json!({"": {"rule_0": valid_rule()}}).to_string(),
            json!({"gate_0": {"": valid_rule()}}).to_string(),
        ] {
            configs.set_sdk_configs(complete_rollout_configs(&sidecar));
            assert!(lookup_rule(&configs, "gate_0", "rule_0").is_none());
        }
    }
}

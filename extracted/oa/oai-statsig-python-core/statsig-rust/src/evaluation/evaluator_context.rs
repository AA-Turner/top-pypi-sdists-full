use std::collections::HashMap;
use std::sync::Arc;

use ahash::AHashMap;

use crate::StatsigErr::StackOverflowError;
use crate::evaluation::dynamic_value::DynamicValue;
use crate::evaluation::evaluator_result::EvaluatorResult;
use crate::hashing::HashUtil;
use crate::id_lists_adapter::IdList;
use crate::interned_string::InternedString;
use crate::specs_response::spec_types::{Rule, Spec, SpecsResponseFull};
use crate::user::StatsigUserInternal;
use crate::{OverrideAdapter, SecondaryExposure, StatsigErr};

const MAX_RECURSIVE_DEPTH: u16 = 300;

// (gate_name, (bool_value, rule_id, secondary_exposures))
type NestedGateMemo =
    AHashMap<InternedString, (bool, Option<InternedString>, Vec<SecondaryExposure>)>;

pub(crate) struct NestedExperimentExposure {
    pub(crate) experiment_name: InternedString,
    pub(crate) recognized: bool,
    pub(crate) result: EvaluatorResult,
}

pub enum IdListResolution<'a> {
    MapLookup(&'a HashMap<String, IdList>),
    Callback(&'a dyn Fn(&str, &str) -> bool),
}

pub struct EvaluatorContext<'a> {
    pub user: &'a StatsigUserInternal<'a, 'a>,
    pub specs_data: &'a SpecsResponseFull,
    pub id_list_resolver: IdListResolution<'a>,
    pub hashing: &'a HashUtil,
    pub result: EvaluatorResult,
    pub nested_count: u16,
    pub app_id: Option<&'a DynamicValue>,
    pub override_adapter: Option<&'a Arc<dyn OverrideAdapter>>,
    pub nested_gate_memo: NestedGateMemo,
    pub should_user_third_party_parser: bool,
    pub(crate) capture_nested_experiment_exposures: bool,
    pub(crate) nested_experiment_exposures: Vec<NestedExperimentExposure>,
    pub gcir_hashes: Vec<u64>,
}

impl<'a> EvaluatorContext<'a> {
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        user: &'a StatsigUserInternal,
        specs_data: &'a SpecsResponseFull,
        id_list_resolver: IdListResolution<'a>,
        hashing: &'a HashUtil,
        app_id: Option<&'a DynamicValue>,
        override_adapter: Option<&'a Arc<dyn OverrideAdapter>>,
        should_user_third_party_parser: bool,
        capture_nested_experiment_exposures: bool,
    ) -> Self {
        let result = EvaluatorResult::default();

        Self {
            user,
            specs_data,
            id_list_resolver,
            hashing,
            app_id,
            result,
            override_adapter,
            nested_count: 0,
            nested_gate_memo: AHashMap::new(),
            should_user_third_party_parser,
            capture_nested_experiment_exposures,
            nested_experiment_exposures: Vec::new(),
            gcir_hashes: Vec::new(),
        }
    }

    pub fn reset_result(&mut self) {
        self.nested_count = 0;
        self.result.clear_for_reuse();
    }

    pub fn finalize_evaluation(&mut self, spec: &Spec, rule: Option<&Rule>) {
        self.finalize_evaluation_values(
            rule.and_then(|rule| rule.sampling_rate),
            spec.forward_all_exposures,
        );
    }

    pub(crate) fn finalize_evaluation_values(
        &mut self,
        sampling_rate: Option<u64>,
        forward_all_exposures: Option<bool>,
    ) {
        self.result.sampling_rate = sampling_rate;
        self.result.forward_all_exposures = forward_all_exposures;

        if self.nested_count > 0 {
            self.nested_count -= 1;
            return;
        }

        if self.result.secondary_exposures.is_empty() {
            return;
        }

        if self.result.undelegated_secondary_exposures.is_some() {
            return;
        }

        self.result.undelegated_secondary_exposures = Some(self.result.secondary_exposures.clone());
    }

    pub fn prep_for_nested_evaluation(&mut self) -> Result<(), StatsigErr> {
        self.nested_count += 1;

        self.result.bool_value = false;
        self.result.json_value = None;

        if self.nested_count > MAX_RECURSIVE_DEPTH {
            return Err(StackOverflowError);
        }

        Ok(())
    }
}

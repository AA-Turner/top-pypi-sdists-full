use std::sync::Arc;

#[cfg(any(test, feature = "testing"))]
use std::collections::{HashMap, HashSet};

use tokio::sync::OnceCell;

use crate::scoped_evaluation_request::ScopedEvaluationRequest;
use crate::scoped_snapshot_registry::EvaluationEngine;
use crate::specs_response::spec_types::SpecsResponseFull;
use crate::{EvaluationOperation, EvaluationRequest, EvaluationResult, StatsigErr, StatsigUser};

/// Fixture-backed evaluation client for local benchmarking and service contract tests.
///
/// Fixture normalization, bootstrap initialization, and SDK instance ownership remain inside the
/// SDK, so host services never need to construct or manage configuration snapshots.
pub struct EvaluationFixtureClient {
    specs_json: Option<String>,
    engine: OnceCell<Arc<EvaluationEngine>>,
    #[cfg(any(test, feature = "testing"))]
    id_list_memberships: HashMap<String, HashSet<String>>,
}

impl EvaluationFixtureClient {
    pub async fn from_file(path: &str) -> Result<Self, StatsigErr> {
        Self::from_file_with_interned_mmap_key(path, None).await
    }

    pub async fn from_file_with_interned_mmap_key(
        path: &str,
        interned_mmap_sdk_key: Option<&str>,
    ) -> Result<Self, StatsigErr> {
        let bytes = std::fs::read(path).map_err(|error| {
            StatsigErr::FileError(format!("Failed to read evaluation fixture {path}: {error}"))
        })?;
        let mut specs = serde_json::from_slice::<SpecsResponseFull>(&bytes).map_err(|error| {
            StatsigErr::JsonParseError("evaluation fixture".to_string(), error.to_string())
        })?;
        drop(bytes);
        let specs_json = serialize_specs(&mut specs)?;
        drop(specs);
        let engine = EvaluationEngine::from_fixture(specs_json, interned_mmap_sdk_key)?;

        Ok(Self {
            specs_json: None,
            engine: OnceCell::new_with(Some(engine)),
            #[cfg(any(test, feature = "testing"))]
            id_list_memberships: HashMap::new(),
        })
    }

    #[doc(hidden)]
    #[cfg(any(test, feature = "testing"))]
    pub fn from_specs_for_test(specs: SpecsResponseFull) -> Self {
        Self::from_specs_with_id_lists_for_test(specs, HashMap::new())
    }

    #[doc(hidden)]
    #[cfg(any(test, feature = "testing"))]
    pub fn from_specs_with_id_lists_for_test(
        mut specs: SpecsResponseFull,
        id_list_memberships: HashMap<String, HashSet<String>>,
    ) -> Self {
        Self {
            specs_json: Some(serialize_specs(&mut specs).expect("test specs should serialize")),
            engine: OnceCell::new(),
            id_list_memberships,
        }
    }

    #[doc(hidden)]
    #[cfg(any(test, feature = "testing"))]
    pub fn from_specs_json_for_test(specs_json: String) -> Self {
        Self {
            specs_json: Some(specs_json),
            engine: OnceCell::new(),
            id_list_memberships: HashMap::new(),
        }
    }

    pub async fn prepare_evaluation(
        &self,
        tenant_key: &str,
        user: StatsigUser,
        target_app_id: Option<String>,
    ) -> Result<EvaluationRequest, StatsigErr> {
        let engine = self
            .engine
            .get_or_try_init(|| async {
                let specs_json = self.specs_json.as_ref().ok_or_else(|| {
                    StatsigErr::InvalidOperation(
                        "Evaluation fixture was not initialized".to_string(),
                    )
                })?;
                let engine = EvaluationEngine::from_fixture(specs_json.clone(), None)?;
                #[cfg(any(test, feature = "testing"))]
                if !self.id_list_memberships.is_empty() {
                    engine.seed_id_lists_for_test(&self.id_list_memberships);
                }
                Ok::<Arc<EvaluationEngine>, StatsigErr>(engine)
            })
            .await?;

        Ok(EvaluationRequest::new(
            ScopedEvaluationRequest::from_engine(Arc::clone(engine), user, target_app_id),
            Arc::from(tenant_key),
        ))
    }

    pub async fn evaluate(
        &self,
        tenant_key: &str,
        user: StatsigUser,
        target_app_id: Option<String>,
        operation: EvaluationOperation<'_>,
    ) -> Result<EvaluationResult, StatsigErr> {
        self.prepare_evaluation(tenant_key, user, target_app_id)
            .await?
            .evaluate(operation)
            .await
    }
}

fn serialize_specs(specs: &mut SpecsResponseFull) -> Result<String, StatsigErr> {
    specs.has_updates = true;
    serde_json::to_string(specs).map_err(|error| StatsigErr::SerializationError(error.to_string()))
}

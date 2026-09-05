pub use evaluation::dynamic_returnable::DynamicReturnable;
pub use evaluation::dynamic_value::DynamicValue;
pub use evaluation::evaluation_details::EvaluationDetails;
pub use evaluation::evaluation_types::SecondaryExposure;
pub use evaluation_fixture_client::EvaluationFixtureClient;
pub use event_logging_adapter::*;
pub use gcir::gcir_formatter::GCIRResponseFormat;
pub use gcir::gcir_options::ClientInitResponseOptions;
pub use hashing::HashAlgorithm;
pub use id_lists_adapter::{IdListsAdapter, StatsigHttpIdListsAdapter};
pub use init_details::{FailureDetails, InitializeDetails};
pub use initialize_response::InitializeResponse;
pub use instance_registry::InstanceRegistry;
pub use observability::{
    observability_client_adapter::ObservabilityClient, ops_stats::OPS_STATS,
    ops_stats::OpsStatsEventObserver,
};
pub use override_adapter::{
    override_adapter_trait::OverrideAdapter,
    statsig_local_override_adapter::StatsigLocalOverrideAdapter,
};
pub use persistent_storage::persistent_storage_trait::*;
pub use scoped_evaluation_request::{
    ConfigEvaluationResult, EvaluationMetadata, EvaluationOperation, EvaluationRequest,
    EvaluationResult, GateEvaluationResult, InitializeEvaluationResult, LiveEntityNames,
};
pub use scoped_snapshot_registry::{
    EvaluationClient, EvaluationDataTransport, EvaluationDataVersion, EvaluationInstance,
    SharedIdLists,
};
pub use spec_store::SpecStore;
pub use specs_adapter::*;
pub use statsig::Statsig;
pub use statsig_core_api_options::{
    DynamicConfigEvaluationOptions, ExperimentEvaluationOptions, FeatureGateEvaluationOptions,
    LayerEvaluationOptions, ParameterStoreEvaluationOptions,
};
pub use statsig_err::StatsigErr;
pub use statsig_options::StatsigOptions;
pub use statsig_runtime::StatsigRuntime;
#[cfg(feature = "ffi-support")]
pub use statsig_types::{
    BulkEvaluationOptions, BulkEvaluationResponse, ResolvedBulkEvaluationOptions,
};
pub use user::user_data::{
    UserCustomMap as StatsigUserCustomMap, UserData as StatsigUserData,
    UserDataMap as StatsigUserDataMap, UserDataStringMap as StatsigUserDataStringMap,
    UserUnitIDMap as StatsigUserUnitIDMap,
};
pub use user::user_value::UserValue as StatsigUserValue;
pub use user::{StatsigUser, StatsigUserBuilder};

#[cfg(feature = "gcir-bench-timings")]
macro_rules! gcir_time {
    ($label:expr, $body:expr) => {
        crate::gcir::timing::time($label, || $body)
    };
}

#[cfg(not(feature = "gcir-bench-timings"))]
macro_rules! gcir_time {
    ($label:expr, $body:expr) => {
        $body
    };
}

pub mod compression;
pub mod console_capture;
pub mod data_store_interface;
pub mod evaluation;
pub mod event_logging;
pub mod gcir;
pub mod global_configs;
pub mod hashing;
pub mod init_details;
pub mod instance_registry;
pub mod interned_string;
pub mod interned_values;
pub mod logging_utils;
pub mod macros;
pub mod networking;
pub mod output_logger;
pub mod override_adapter;
pub mod sdk_diagnostics;
pub mod sdk_event_emitter;
pub mod specs_response;
pub mod statsig_core_api_options;
pub mod statsig_global;
pub mod statsig_metadata;
pub mod statsig_options;
pub mod statsig_runtime;
pub mod statsig_types;
pub mod statsig_types_raw;
pub mod user;

#[cfg(test)]
mod dcs_str;
mod evaluation_fixture_client;
mod event_logging_adapter;
mod id_lists_adapter;
mod initialize_evaluations_response;
mod initialize_response;
mod initialize_v2_response;
mod observability;
mod persistent_storage;
mod scoped_evaluation_request;
mod scoped_id_list_membership_service;
mod scoped_snapshot_registry;
mod snapshot_evaluation_session;
mod spec_store;
mod specs_adapter;
mod statsig;
mod statsig_err;
mod statsig_type_factories;
mod utils;
mod value_parsing;

#[cfg(test)]
mod __tests__;

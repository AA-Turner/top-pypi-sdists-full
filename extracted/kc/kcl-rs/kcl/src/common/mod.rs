//! Port of `software.amazon.kinesis.common`.
//!
//! Common value types and configuration shared across subsystems.

pub mod arn;
pub mod common_calculations;
pub mod configs_builder;
pub mod ddb_table_config;
pub mod deprecation_utils;
pub mod diagnostic_utils;
pub mod future_utils;
pub mod hash_key_range_for_lease;
pub mod initial_position;
pub mod kinesis_client_util;
pub mod kinesis_requests_builder;
pub mod lease_cleanup_config;
pub mod request_details;
pub mod stack_trace_utils;
pub mod stream_arn_constructor;
pub mod stream_config;
pub mod stream_identifier;
pub mod user_agent_utils;

pub use arn::{Arn, ArnResource};
pub use common_calculations::get_renewer_taker_interval_millis;
pub use configs_builder::ConfigsBuilder;
pub use ddb_table_config::DdbTableConfig;
pub use deprecation_utils::{convert, Either, StreamTrackerKind};
pub use diagnostic_utils::{
    take_delayed_delivery_action_if_required, take_delayed_delivery_action_if_required_with_now,
    MAX_TIME_BETWEEN_REQUEST_RESPONSE,
};
pub use future_utils::{resolve_or_cancel, TimedOut};
pub use hash_key_range_for_lease::HashKeyRangeForLease;
pub use initial_position::{InitialPositionInStream, InitialPositionInStreamExtended};
pub use kinesis_client_util::{
    adjust_kinesis_client_builder, HEALTH_CHECK_PING_PERIOD_MILLIS, INITIAL_WINDOW_SIZE_BYTES,
};
pub use kinesis_requests_builder::{kcl_user_agent_config, user_agent_name, user_agent_version};
pub use lease_cleanup_config::LeaseCleanupConfig;
pub use request_details::RequestDetails;
pub use stack_trace_utils::{get_printable_stack_trace, printable_backtrace};
pub use stream_arn_constructor::{
    partition_for_region, DefaultKinesisStreamArnConstructor, StreamArnConstructor,
    KINESIS_SERVICE_NAME, STREAM_RESOURCE_PREFIX,
};
pub use stream_config::StreamConfig;
pub use stream_identifier::{StreamIdentifier, STREAM_TYPE_KINESIS};
pub use user_agent_utils::{generate_consumer_id, get_consumer_id};

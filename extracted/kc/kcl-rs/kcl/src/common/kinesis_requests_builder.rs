//! Port of `software.amazon.kinesis.common.KinesisRequestsBuilder`.
//!
//! Centralizes construction of Kinesis SDK requests, uniformly tagging each with
//! a KCL user-agent so AWS can attribute traffic to the KCL library (and
//! optionally a specific consumer).
//!
//! # Deviation from Java
//!
//! The Java version returns SDK request *builders* pre-populated with an
//! `AwsRequestOverrideConfiguration` carrying an `ApiName{name, version}`. The
//! Rust AWS SDK has no `ApiName`/`addApiName` per-request hook; the equivalent
//! business-metric/user-agent attribution is applied via a per-request
//! [`config_override`](aws_sdk_kinesis::operation::list_shards::builders::ListShardsFluentBuilder::config_override)
//! carrying an [`AppName`](aws_sdk_kinesis::config::AppName).
//!
//! This module therefore ports the **load-bearing behavior** — the exact
//! user-agent *name* string (base, or `base-consumerId`) and version — and
//! provides [`kcl_user_agent_config`] which builds a Kinesis `config::Builder`
//! applying that name as the SDK `AppName`. Retrieval-wave call sites apply it
//! via each request's `.config_override(...)`. `AppName` restricts the charset
//! (alphanumerics plus a few punctuation marks including `-`), which the KCL
//! user-agent name and consumer-ids satisfy.

use aws_sdk_kinesis::config::AppName;

use crate::retrieval::{KINESIS_CLIENT_LIB_USER_AGENT, KINESIS_CLIENT_LIB_USER_AGENT_VERSION};

/// The user-agent *name* for the KCL, matching Java's `ApiName.name`.
///
/// Without a consumer id this is the bare
/// [`KINESIS_CLIENT_LIB_USER_AGENT`]; with a consumer id it is
/// `format!("{base}-{consumerId}")` (Java `String.format("%s-%s", ...)`).
pub fn user_agent_name(consumer_id: Option<&str>) -> String {
    match consumer_id {
        None => KINESIS_CLIENT_LIB_USER_AGENT.to_string(),
        Some(id) => format!("{}-{}", KINESIS_CLIENT_LIB_USER_AGENT, id),
    }
}

/// The user-agent *version* for the KCL, matching Java's `ApiName.version`.
pub fn user_agent_version() -> &'static str {
    KINESIS_CLIENT_LIB_USER_AGENT_VERSION
}

/// Build a Kinesis `config::Builder` applying the KCL user-agent as the SDK
/// `AppName` (the Rust analog of Java's per-request `ApiName` override).
///
/// Apply to a request via `request_builder.config_override(kcl_user_agent_config(consumer_id))`.
///
/// # Panics
///
/// Panics if the derived name is not a valid [`AppName`] (should not happen for
/// the KCL user-agent name / KCL consumer-ids, which use a valid charset).
pub fn kcl_user_agent_config(consumer_id: Option<&str>) -> aws_sdk_kinesis::config::Builder {
    let name = user_agent_name(consumer_id);
    let app_name = AppName::new(name).expect("KCL user-agent name is a valid AppName");
    aws_sdk_kinesis::config::Builder::default().app_name(app_name)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn base_user_agent_name() {
        assert_eq!(user_agent_name(None), "amazon-kinesis-client-library-java");
    }

    #[test]
    fn consumer_id_suffixes_name() {
        assert_eq!(
            user_agent_name(Some("KCL-ConsumerId-abc")),
            "amazon-kinesis-client-library-java-KCL-ConsumerId-abc"
        );
    }

    #[test]
    fn version_is_present() {
        assert!(!user_agent_version().is_empty());
    }

    #[test]
    fn config_builds_with_valid_app_name() {
        // Should not panic for base or consumer-id-suffixed names.
        let _base = kcl_user_agent_config(None);
        let _with_consumer = kcl_user_agent_config(Some("KCL-ConsumerId-abc"));
    }
}

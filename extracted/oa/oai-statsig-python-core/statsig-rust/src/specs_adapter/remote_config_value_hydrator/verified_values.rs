use std::collections::HashMap;
use std::sync::Arc;

use crate::{DynamicReturnable, StatsigErr};

use super::errors::{HydrationFailureReason, hydration_error};
use super::metadata::RemoteConfigValueMetadata;

/// A parsed value whose original remote body has already passed verification.
/// Keep the metadata private so callers cannot create a trusted entry from an
/// arbitrary parsed value or from a reserialized datastore sidecar.
#[derive(Debug)]
pub(crate) struct VerifiedRemoteValue {
    metadata: RemoteConfigValueMetadata,
    pub(crate) value: DynamicReturnable,
    json_sidecar_reuse_safe: bool,
}

impl VerifiedRemoteValue {
    /// Parse an original body returned by the verified download path. Never
    /// call this with reserialized snapshot or datastore values.
    pub(super) fn from_verified_body(
        metadata: RemoteConfigValueMetadata,
        body: &[u8],
    ) -> Result<Self, StatsigErr> {
        let value = serde_json::from_slice::<DynamicReturnable>(body).map_err(|error| {
            hydration_error(HydrationFailureReason::InvalidJson, &error.to_string())
        })?;
        Ok(Self {
            metadata,
            value,
            json_sidecar_reuse_safe: false,
        })
    }

    /// JSON sidecars must preserve original number lexemes, which parsing a
    /// DynamicReturnable can round. Keep only a conservative reuse bit, never
    /// the original body. Protobuf hydration does not need this extra scan.
    pub(super) fn from_verified_json_body(
        metadata: RemoteConfigValueMetadata,
        body: &[u8],
    ) -> Result<Self, StatsigErr> {
        let mut value = Self::from_verified_body(metadata, body)?;
        value.json_sidecar_reuse_safe = !json_body_has_number(body);
        Ok(value)
    }

    pub(super) fn can_reuse_json_sidecar(&self) -> bool {
        self.json_sidecar_reuse_safe
    }

    pub(super) fn matches_metadata(&self, metadata: &RemoteConfigValueMetadata) -> bool {
        self.metadata == *metadata
    }

    pub(super) fn sha256(&self) -> &str {
        self.metadata.sha256.as_str()
    }

    /// Identify the actual immutable value previously verified without
    /// serializing it or trusting a value hash alone.
    pub(super) fn matches_backing_value(&self, value: &DynamicReturnable) -> bool {
        use crate::evaluation::dynamic_returnable::DynamicReturnableValue;

        match (&self.value.value, &value.value) {
            (DynamicReturnableValue::Null, DynamicReturnableValue::Null) => true,
            (DynamicReturnableValue::Bool(left), DynamicReturnableValue::Bool(right)) => {
                left == right
            }
            (
                DynamicReturnableValue::JsonPointer(left),
                DynamicReturnableValue::JsonPointer(right),
            ) => Arc::ptr_eq(left, right),
            (
                DynamicReturnableValue::JsonStatic(left),
                DynamicReturnableValue::JsonStatic(right),
            ) => std::ptr::eq(*left, *right),
            (
                DynamicReturnableValue::JsonArchived(left),
                DynamicReturnableValue::JsonArchived(right),
            ) => std::ptr::eq(*left, *right),
            _ => false,
        }
    }
}

fn json_body_has_number(body: &[u8]) -> bool {
    let mut in_string = false;
    let mut escaped = false;
    for &byte in body {
        if in_string {
            if escaped {
                escaped = false;
            } else if byte == b'\\' {
                escaped = true;
            } else if byte == b'"' {
                in_string = false;
            }
        } else if byte == b'"' {
            in_string = true;
        } else if byte == b'-' || byte.is_ascii_digit() {
            // The original body has already passed JSON verification, so a
            // digit or minus outside a string necessarily starts a number.
            return true;
        }
    }
    false
}

pub(crate) type VerifiedRemoteValues = HashMap<String, Arc<VerifiedRemoteValue>>;

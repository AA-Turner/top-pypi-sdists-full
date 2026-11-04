use std::collections::HashMap;
use std::sync::Arc;

use crate::{DynamicReturnable, StatsigErr};

use super::errors::{HydrationFailureReason, hydration_error};
use super::metadata::{
    RemoteCompression, RemoteConfigValueMetadata, RemoteConfigValueMetadataWire,
};

/// A writer-verified remote body and its handle in the same mmap artifact.
/// Version 1 of the manifest extension supports JSON objects only.
#[derive(Clone, Debug, Eq, PartialEq, serde::Serialize, serde::Deserialize)]
pub(crate) struct MmapRemoteValueProof {
    pub(crate) sha256: String,
    pub(crate) byte_length: u64,
    pub(crate) compression: String,
    pub(crate) returnable_hash: u64,
    #[serde(default, skip_serializing_if = "std::ops::Not::not")]
    pub(crate) json_sidecar_reuse_safe: bool,
}

impl MmapRemoteValueProof {
    fn metadata(&self) -> Result<RemoteConfigValueMetadata, StatsigErr> {
        RemoteConfigValueMetadata::try_from(RemoteConfigValueMetadataWire {
            sha256: self.sha256.clone(),
            byte_length: self.byte_length,
            content_type: "application/json".to_owned(),
            compression: self.compression.clone(),
        })
    }

    pub(crate) fn is_valid(&self) -> bool {
        self.metadata().is_ok()
    }
}

/// A parsed value whose original remote body has already passed verification.
/// Keep the metadata private so callers cannot create a trusted entry from an
/// arbitrary parsed value or from a reserialized datastore sidecar.
#[derive(Debug)]
pub(crate) struct VerifiedRemoteValue {
    metadata: RemoteConfigValueMetadata,
    pub(crate) value: DynamicReturnable,
    json_sidecar_reuse_safe: bool,
}

#[derive(Eq, PartialEq, Hash)]
pub(crate) enum ReturnableBackingIdentity {
    Null,
    Bool(bool),
    JsonPointer(usize),
    JsonStatic(usize),
    JsonArchived(usize),
}

impl VerifiedRemoteValue {
    pub(crate) fn mmap_proof(&self) -> Option<MmapRemoteValueProof> {
        use crate::evaluation::dynamic_returnable::DynamicReturnableValue;

        if !matches!(
            self.value.value,
            DynamicReturnableValue::JsonPointer(_)
                | DynamicReturnableValue::JsonStatic(_)
                | DynamicReturnableValue::JsonArchived(_)
        ) {
            return None;
        }
        Some(MmapRemoteValueProof {
            sha256: self.metadata.sha256.as_str().to_owned(),
            byte_length: self.metadata.byte_length,
            compression: match self.metadata.compression {
                RemoteCompression::None => "none",
                RemoteCompression::Gzip => "gzip",
                RemoteCompression::Zstd => "zstd",
            }
            .to_owned(),
            returnable_hash: self.value.hash,
            json_sidecar_reuse_safe: self.json_sidecar_reuse_safe,
        })
    }

    /// The reader must first validate the committed artifact's digest and key,
    /// and resolve this handle in that exact mapped artifact. Parsed snapshots
    /// or caller-supplied metadata are not sufficient verification provenance.
    pub(crate) fn from_verified_mmap(
        proof: &MmapRemoteValueProof,
        value: DynamicReturnable,
    ) -> Option<Self> {
        if value.hash != proof.returnable_hash || value.get_json_archived_ref().is_none() {
            return None;
        }
        Some(Self {
            metadata: proof.metadata().ok()?,
            value,
            json_sidecar_reuse_safe: proof.json_sidecar_reuse_safe,
        })
    }

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
    pub(crate) fn matches_backing_value(&self, value: &DynamicReturnable) -> bool {
        Self::backing_identity(&self.value) == Self::backing_identity(value)
    }

    pub(crate) fn backing_identity(value: &DynamicReturnable) -> ReturnableBackingIdentity {
        use crate::evaluation::dynamic_returnable::DynamicReturnableValue;

        match &value.value {
            DynamicReturnableValue::Null => ReturnableBackingIdentity::Null,
            DynamicReturnableValue::Bool(value) => ReturnableBackingIdentity::Bool(*value),
            DynamicReturnableValue::JsonPointer(value) => {
                ReturnableBackingIdentity::JsonPointer(Arc::as_ptr(value) as usize)
            }
            DynamicReturnableValue::JsonStatic(value) => {
                ReturnableBackingIdentity::JsonStatic(std::ptr::from_ref(*value) as usize)
            }
            DynamicReturnableValue::JsonArchived(value) => {
                ReturnableBackingIdentity::JsonArchived(std::ptr::from_ref(*value) as usize)
            }
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

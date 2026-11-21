use std::collections::HashMap;

use crate::user::unit_id::{USER_ID_TYPE, is_user_id_type};

/// The primary unit has a reserved canonical key. Custom keys preserve case.
pub(super) fn canonical_id_type(id_type: &str) -> &str {
    if is_user_id_type(id_type) {
        USER_ID_TYPE
    } else {
        id_type
    }
}

#[derive(serde::Deserialize)]
#[serde(transparent)]
pub(super) struct RemoteIdListAllowlist {
    #[serde(with = "serde_with::rust::maps_duplicate_key_is_error")]
    lists: HashMap<String, String>,
}

impl RemoteIdListAllowlist {
    /// Read the process-wide pilot configuration once per SDK instance.
    pub(super) fn from_env() -> Option<Self> {
        if std::env::var("STATSIG_RUST_REMOTE_ID_LISTS_ENABLED").as_deref() != Ok("1") {
            return None;
        }
        let raw = std::env::var("STATSIG_RUST_REMOTE_ID_LIST_ALLOWLIST").ok()?;
        Self::from_json(&raw)
    }

    pub(super) fn from_json(raw: &str) -> Option<Self> {
        let mut allowlist: Self = serde_json::from_str(raw).ok()?;
        for (name, kind) in &mut allowlist.lists {
            if name.trim().is_empty() || kind.trim().is_empty() {
                return None;
            }
            let canonical = canonical_id_type(kind);
            if canonical != kind {
                *kind = canonical.to_owned();
            }
        }
        (!allowlist.lists.is_empty()).then_some(allowlist)
    }

    pub(super) fn list_names(&self) -> impl Iterator<Item = &str> {
        self.lists.keys().map(String::as_str)
    }

    pub(super) fn allows(&self, list: &str, id_type: &str) -> bool {
        self.lists
            .get(list)
            .is_some_and(|kind| kind == canonical_id_type(id_type))
    }
}

#[cfg(test)]
#[path = "__tests__/remote_id_list_allowlist_tests.rs"]
mod tests;

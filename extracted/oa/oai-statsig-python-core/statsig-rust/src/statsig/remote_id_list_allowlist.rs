use std::collections::HashMap;

/// The primary unit has a reserved canonical key. Custom keys preserve case.
pub(super) fn canonical_id_type(id_type: &str) -> &str {
    if id_type.eq_ignore_ascii_case("userID") {
        "userID"
    } else {
        id_type
    }
}

#[derive(Default)]
pub(super) struct RemoteIdListAllowlist {
    lists: HashMap<String, String>,
}

impl RemoteIdListAllowlist {
    pub(super) fn from_lists(mut lists: HashMap<String, String>) -> Self {
        for (name, kind) in &mut lists {
            if name.trim().is_empty() || kind.trim().is_empty() {
                return Self::default();
            }
            let canonical = canonical_id_type(kind);
            if canonical != kind {
                *kind = canonical.to_owned();
            }
        }
        Self { lists }
    }

    pub(super) fn is_empty(&self) -> bool {
        self.lists.is_empty()
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

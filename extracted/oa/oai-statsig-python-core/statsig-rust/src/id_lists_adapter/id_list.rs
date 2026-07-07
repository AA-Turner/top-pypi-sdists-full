use serde::Serialize;

use crate::{
    id_lists_adapter::{IdListMetadata, IdListUpdate},
    unwrap_or_noop,
};
use std::{collections::HashSet, sync::Arc};

#[derive(Clone, Serialize)]
pub struct IdList {
    pub metadata: IdListMetadata,

    #[serde(skip_serializing)]
    pub ids: Arc<HashSet<String>>,
}

impl IdList {
    pub fn new(metadata: IdListMetadata) -> Self {
        let mut local_metadata = metadata;
        local_metadata.size = 0;

        Self {
            metadata: local_metadata,
            ids: Arc::new(HashSet::new()),
        }
    }

    pub fn apply_update(&mut self, update: IdListUpdate) {
        let updated_meta = update.new_metadata;
        let current_meta = &self.metadata;

        if updated_meta.file_id != current_meta.file_id
            && updated_meta.creation_time >= current_meta.creation_time
        {
            self.update_metadata(updated_meta);
        }

        let changeset_data = unwrap_or_noop!(&update.raw_changeset);
        let ids = Arc::make_mut(&mut self.ids);

        for change in changeset_data.lines() {
            let trimmed = change.trim();
            if trimmed.len() <= 1 {
                continue;
            }

            let op = change.chars().next();
            let id = &change[1..];

            match op {
                Some('+') => {
                    ids.insert(id.to_string());
                }
                Some('-') => {
                    ids.remove(id);
                }
                _ => continue,
            }
        }

        self.metadata.size += changeset_data.len() as u64;
    }

    fn update_metadata(&mut self, metadata: IdListMetadata) {
        self.metadata = metadata;
        self.metadata.size = 0;
        self.ids = Arc::new(HashSet::new());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn metadata() -> IdListMetadata {
        IdListMetadata {
            name: "employees".to_string(),
            url: "https://example.com/employees".to_string(),
            file_id: Some("file-1".to_string()),
            size: 0,
            creation_time: 1,
        }
    }

    #[test]
    fn cloned_list_copies_ids_only_when_updated() {
        let mut original = IdList::new(metadata());
        original.apply_update(IdListUpdate {
            raw_changeset: Some("+alice".to_string()),
            new_metadata: metadata(),
        });

        let mut updated = original.clone();
        assert!(Arc::ptr_eq(&original.ids, &updated.ids));

        updated.apply_update(IdListUpdate {
            raw_changeset: Some("+bob".to_string()),
            new_metadata: metadata(),
        });

        assert!(!Arc::ptr_eq(&original.ids, &updated.ids));
        assert!(original.ids.contains("alice"));
        assert!(!original.ids.contains("bob"));
        assert!(updated.ids.contains("alice"));
        assert!(updated.ids.contains("bob"));
    }
}

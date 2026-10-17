use serde::Serialize;

use crate::{
    id_lists_adapter::{IdListIds, IdListMetadata, IdListUpdate},
    unwrap_or_noop,
};
use std::sync::Arc;

#[derive(Clone, Serialize)]
pub struct IdList {
    pub metadata: IdListMetadata,

    #[serde(skip_serializing)]
    pub ids: Arc<IdListIds>,
}

impl IdList {
    pub fn new(metadata: IdListMetadata) -> Self {
        let mut local_metadata = metadata;
        local_metadata.size = 0;

        Self {
            metadata: local_metadata,
            ids: Arc::new(IdListIds::new()),
        }
    }

    pub fn apply_update(&mut self, update: IdListUpdate) {
        let changeset_data = unwrap_or_noop!(&update.raw_changeset);
        let updated_meta = update.new_metadata;
        let current_meta = &self.metadata;

        // The HTTP adapter downloads from byte zero when creationTime advances,
        // even if the file ID is unchanged. Apply that body as a full replay so
        // the consumed cursor and timestamp match the next manifest poll.
        if updated_meta.creation_time > current_meta.creation_time
            || (updated_meta.file_id != current_meta.file_id
                && updated_meta.creation_time >= current_meta.creation_time)
        {
            self.update_metadata(updated_meta);
        }

        let ids = Arc::make_mut(&mut self.ids);

        for change in changeset_data.lines() {
            let trimmed = change.trim();
            if trimmed.len() <= 1 {
                continue;
            }

            if let Some(id) = change.strip_prefix('+') {
                ids.insert_str(id);
            } else if let Some(id) = change.strip_prefix('-') {
                ids.remove(id);
            }
        }

        self.metadata.size += changeset_data.len() as u64;
    }

    fn update_metadata(&mut self, metadata: IdListMetadata) {
        self.metadata = metadata;
        self.metadata.size = 0;
        self.ids = Arc::new(IdListIds::new());
    }
}

#[cfg(test)]
#[path = "__tests__/id_list_tests.rs"]
mod tests;

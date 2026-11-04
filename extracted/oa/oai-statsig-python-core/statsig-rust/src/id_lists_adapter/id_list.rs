use super::id_list_ids::CompactionPolicy;
use super::shared_id_list_format::IdListImage;
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

#[derive(PartialEq)]
enum UpdateMode {
    PrivateHash,
    PrivateEliasFano,
    SharedPublisher,
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
        self.apply_update_inner(update, UpdateMode::PrivateHash);
    }

    pub(super) fn apply_update_for_publish(&mut self, update: IdListUpdate) {
        self.apply_update_inner(update, UpdateMode::SharedPublisher);
    }

    pub(crate) fn apply_update_with_elias_fano(&mut self, update: IdListUpdate) {
        self.apply_update_inner(update, UpdateMode::PrivateEliasFano);
    }

    fn apply_update_inner(&mut self, update: IdListUpdate, mode: UpdateMode) {
        let mut changeset_data = unwrap_or_noop!(update.raw_changeset);
        let consumed = changeset_data.len() as u64;
        let updated_meta = update.new_metadata;
        let current_meta = &self.metadata;
        if updated_meta.creation_time < current_meta.creation_time {
            return;
        }

        // The HTTP adapter downloads from byte zero when creationTime advances,
        // even if the file ID is unchanged. Apply that body as a full replay so
        // the consumed cursor and timestamp match the next manifest poll.
        if updated_meta.creation_time > current_meta.creation_time
            || updated_meta.file_id != current_meta.file_id
        {
            self.update_metadata(updated_meta);
        }

        let private_compact = mode == UpdateMode::PrivateEliasFano;
        if private_compact && changeset_data.is_empty() {
            return;
        }

        if private_compact && self.ids.is_empty() {
            match IdListImage::try_heap_from_adds(&[0; 32], &self.metadata.name, changeset_data) {
                Ok(image) => {
                    self.ids = Arc::new(IdListIds::from_image(image));
                    self.metadata.size += consumed;
                    return;
                }
                Err(body) => changeset_data = body,
            }
        }

        let policy = match mode {
            UpdateMode::PrivateHash => CompactionPolicy::Immediate,
            UpdateMode::PrivateEliasFano | UpdateMode::SharedPublisher => CompactionPolicy::Batch,
        };
        let mut edits = changeset_data.lines().filter_map(|change| {
            let (sign, id) = change.split_at_checked(1)?;
            let present = match sign {
                "+" => true,
                "-" => false,
                _ => return None,
            };
            (!id.trim().is_empty()).then_some((id, present))
        });
        let first = if private_compact {
            edits.find(|(id, present)| self.ids.contains(id) != *present)
        } else {
            edits.next()
        };
        if first.is_some() || !private_compact {
            let ids = Arc::make_mut(&mut self.ids);
            for (id, present) in first.into_iter().chain(edits) {
                ids.set(id, present, policy);
            }
        }
        if private_compact {
            self.ids.finish_private_batch(&self.metadata.name);
        }
        self.metadata.size += consumed;
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

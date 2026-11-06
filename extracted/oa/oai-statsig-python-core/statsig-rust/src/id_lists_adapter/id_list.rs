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

#[derive(Clone, Copy, PartialEq, Eq)]
pub(crate) enum IdListEncoding {
    Hash,
    EliasFano,
}

enum UpdateMode {
    Private(IdListEncoding),
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
        self.apply_update_with_encoding(IdListEncoding::Hash, update);
    }

    pub(super) fn apply_update_for_publish(&mut self, update: IdListUpdate) {
        self.apply_update_inner(update, UpdateMode::SharedPublisher);
    }

    pub(crate) fn apply_update_with_encoding(
        &mut self,
        encoding: IdListEncoding,
        update: IdListUpdate,
    ) {
        self.apply_update_inner(update, UpdateMode::Private(encoding));
    }

    fn apply_update_inner(&mut self, update: IdListUpdate, mode: UpdateMode) {
        let changeset_data = unwrap_or_noop!(update.raw_changeset);
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

        match mode {
            UpdateMode::Private(IdListEncoding::Hash) => {
                self.apply_edits(parse_edits(&changeset_data), CompactionPolicy::Immediate);
            }
            UpdateMode::SharedPublisher => {
                self.apply_edits(parse_edits(&changeset_data), CompactionPolicy::Batch);
            }
            UpdateMode::Private(IdListEncoding::EliasFano) => {
                self.apply_private_elias_fano_changes(changeset_data);
            }
        }
        self.metadata.size += consumed;
    }

    fn apply_private_elias_fano_changes(&mut self, mut changeset_data: String) {
        if changeset_data.is_empty() {
            return;
        }
        if self.ids.is_empty() {
            match IdListImage::try_heap_from_adds(&[0; 32], &self.metadata.name, changeset_data) {
                Ok(image) => {
                    self.ids = Arc::new(IdListIds::from_image(image));
                    return;
                }
                Err(body) => changeset_data = body,
            }
        }

        // Keep the existing index shared when every edit is a no-op.
        let mut edits = parse_edits(&changeset_data);
        if let Some(first_change) = edits.find(|(id, present)| self.ids.contains(id) != *present) {
            self.apply_edits(
                std::iter::once(first_change).chain(edits),
                CompactionPolicy::Batch,
            );
        }
        self.ids.finish_private_batch(&self.metadata.name);
    }

    fn apply_edits<'a>(
        &mut self,
        edits: impl Iterator<Item = (&'a str, bool)>,
        policy: CompactionPolicy,
    ) {
        let mut edits = edits.peekable();
        if edits.peek().is_none() {
            return;
        }
        let ids = Arc::make_mut(&mut self.ids);
        for (id, present) in edits {
            ids.set(id, present, policy);
        }
    }

    fn update_metadata(&mut self, metadata: IdListMetadata) {
        self.metadata = metadata;
        self.metadata.size = 0;
        self.ids = Arc::new(IdListIds::new());
    }
}

fn parse_edits(changeset_data: &str) -> impl Iterator<Item = (&str, bool)> {
    changeset_data.lines().filter_map(|change| {
        let (sign, id) = change.split_at_checked(1)?;
        let present = match sign {
            "+" => true,
            "-" => false,
            _ => return None,
        };
        (!id.trim().is_empty()).then_some((id, present))
    })
}

#[cfg(test)]
#[path = "__tests__/id_list_tests.rs"]
mod tests;

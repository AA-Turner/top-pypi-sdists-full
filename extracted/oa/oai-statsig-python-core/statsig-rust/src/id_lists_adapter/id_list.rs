use super::id_list_ids::CompactionPolicy;
use super::shared_id_list_format::IdListImage;
use serde::Serialize;

use crate::{
    id_lists_adapter::{IdListIds, IdListMetadata, IdListUpdate},
    unwrap_or_noop,
};
use std::{borrow::Cow, io, sync::Arc};

#[derive(Clone, Serialize)]
pub struct IdList {
    pub metadata: IdListMetadata,

    #[serde(skip_serializing)]
    pub ids: Arc<IdListIds>,
}

/// The generation and byte length of an ordinary ID-list file. A signed URL may
/// change while these values and the installed membership stay the same.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct IdListFileVersion<'a> {
    pub file_id: Option<&'a str>,
    /// Compares signed SDK and unsigned proxy manifest timestamps without narrowing either.
    pub creation_time: i128,
    pub size: u64,
}

impl IdListMetadata {
    pub(super) fn file_version(&self) -> IdListFileVersion<'_> {
        IdListFileVersion {
            file_id: self.file_id.as_deref(),
            creation_time: self.creation_time.into(),
            size: self.size,
        }
    }
}

impl IdListFileVersion<'_> {
    fn is_older_than(&self, previous: IdListFileVersion<'_>) -> bool {
        self.creation_time < previous.creation_time
    }

    fn requires_full_replay(&self, previous: IdListFileVersion<'_>) -> bool {
        self.creation_time > previous.creation_time || self.file_id != previous.file_id
    }

    // The HTTP adapter selects bytes before its update listener decides whether
    // to install them. Keep that download contract for custom listeners.
    pub(super) fn download_from(
        &self,
        previous: Option<IdListFileVersion<'_>>,
    ) -> Option<IdListFileUpdate> {
        let start = match previous {
            None => 0,
            Some(old) if self.requires_full_replay(old) => 0,
            Some(old) if old.size < self.size => old.size,
            Some(_) => return None,
        };
        Some(IdListFileUpdate {
            start,
            end: self.size,
        })
    }

    /// Plan a full replay or an append from the installed cursor. An older file,
    /// an unchanged file, or a same-file shrink has no update to apply.
    pub fn update_from(&self, previous: Option<IdListFileVersion<'_>>) -> Option<IdListFileUpdate> {
        if previous.is_some_and(|old| self.is_older_than(old)) {
            return None;
        }
        self.download_from(previous)
    }
}

/// The byte range to consume from a complete ordinary ID-list file.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct IdListFileUpdate {
    pub(super) start: u64,
    end: u64,
}

impl IdListFileUpdate {
    /// Build a new membership snapshot from a body starting at byte zero. For
    /// an append, supply the membership used to plan this update. Extra bytes
    /// past the target size are left for a future update. As in the SDK refresh
    /// path, the changeset must be UTF-8 and unrecognized lines are skipped.
    pub fn apply_to_membership(
        &self,
        name: &str,
        previous: Option<&IdListMembership>,
        body: &[u8],
    ) -> io::Result<IdListMembership> {
        if (body.len() as u64) < self.end {
            return Err(io::ErrorKind::UnexpectedEof.into());
        }
        let mut members = if self.start == 0 {
            IdListMembership::default()
        } else {
            previous.cloned().ok_or_else(|| {
                io::Error::new(
                    io::ErrorKind::InvalidInput,
                    "missing membership for ID-list append",
                )
            })?
        };
        // Both offsets fit in usize because start <= end <= body.len().
        members.apply(name, &body[self.start as usize..self.end as usize])?;
        Ok(members)
    }
}

/// A resident 48-bit ordinary ID list using the SDK's private Elias–Fano update policy.
/// Clones share their current contents and can subsequently be updated independently.
#[derive(Clone, Default)]
pub struct IdListMembership {
    ids: Arc<IdListIds>,
}

impl IdListMembership {
    /// Apply a complete signed changeset for this list. Start with an empty instance
    /// for a replacement file and pass only the new records when appending.
    /// Pass a `Vec<u8>` to let the initial index build reuse its allocation.
    /// Appends can be read directly from a borrowed `&[u8]`.
    /// As in SDK refresh, apply signed, nonblank IDs and skip unrecognized lines.
    /// Invalid UTF-8 rejects the entire changeset before any edits are applied.
    pub fn apply<'a>(&mut self, name: &str, changeset: impl Into<Cow<'a, [u8]>>) -> io::Result<()> {
        let body = match changeset.into() {
            Cow::Borrowed(bytes) => {
                Cow::Borrowed(std::str::from_utf8(bytes).map_err(|_| io::ErrorKind::InvalidData)?)
            }
            Cow::Owned(bytes) => {
                Cow::Owned(String::from_utf8(bytes).map_err(|_| io::ErrorKind::InvalidData)?)
            }
        };
        self.ids
            .apply_changeset(name, body, UpdateMode::Private(IdListEncoding::EliasFano));
        Ok(())
    }

    /// Check a key encoded with `IdListFingerprintWidth::Bits48`.
    pub fn contains(&self, hashed_id: &str) -> bool {
        self.ids.contains(hashed_id)
    }
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
    pub(crate) fn from_update_base(
        previous: Option<&Self>,
        snapshot: Option<Self>,
        metadata: &IdListMetadata,
    ) -> Self {
        snapshot
            .filter(|staged| {
                previous
                    .is_none_or(|old| old.metadata.creation_time <= staged.metadata.creation_time)
            })
            .or_else(|| previous.cloned())
            .unwrap_or_else(|| Self::new(metadata.clone()))
    }

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
        // A listener may supply a partial HTTP response or a delta with no
        // advertised size. Advance by its actual bytes after checking the generation.
        let current = self.metadata.file_version();
        let target = updated_meta.file_version();
        if target.is_older_than(current) {
            return;
        }
        if target.requires_full_replay(current) {
            self.update_metadata(updated_meta);
        }

        self.ids
            .apply_changeset(&self.metadata.name, changeset_data.into(), mode);
        self.metadata.size += consumed;
    }

    fn update_metadata(&mut self, metadata: IdListMetadata) {
        self.metadata = metadata;
        self.metadata.size = 0;
        self.ids = Arc::new(IdListIds::new());
    }
}

impl IdListIds {
    fn apply_changeset(
        self: &mut Arc<Self>,
        name: &str,
        changeset: Cow<'_, str>,
        mode: UpdateMode,
    ) {
        let policy = match mode {
            UpdateMode::Private(IdListEncoding::Hash) => CompactionPolicy::Immediate,
            UpdateMode::SharedPublisher => CompactionPolicy::Batch,
            UpdateMode::Private(IdListEncoding::EliasFano) => {
                return self.apply_private_elias_fano_changes(name, changeset);
            }
        };
        self.apply_edits(parse_edits(&changeset), policy);
    }

    fn apply_private_elias_fano_changes(
        self: &mut Arc<Self>,
        name: &str,
        mut changeset_data: Cow<'_, str>,
    ) {
        if changeset_data.is_empty() {
            return;
        }
        if self.is_empty() {
            match IdListImage::try_heap_from_adds(&[0; 32], name, changeset_data) {
                Ok(image) => {
                    *self = Arc::new(IdListIds::from_image(image));
                    return;
                }
                Err(body) => changeset_data = body,
            }
        }

        // Keep the existing index shared when every edit is a no-op.
        let mut edits = parse_edits(&changeset_data);
        if let Some(first_change) = edits.find(|(id, present)| self.contains(id) != *present) {
            self.apply_edits(
                std::iter::once(first_change).chain(edits),
                CompactionPolicy::Batch,
            );
        }
        self.finish_private_batch(name);
    }

    fn apply_edits<'a>(
        self: &mut Arc<Self>,
        edits: impl Iterator<Item = (&'a str, bool)>,
        policy: CompactionPolicy,
    ) {
        let mut edits = edits.peekable();
        if edits.peek().is_none() {
            return;
        }
        let ids = Arc::make_mut(self);
        for (id, present) in edits {
            ids.set(id, present, policy);
        }
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

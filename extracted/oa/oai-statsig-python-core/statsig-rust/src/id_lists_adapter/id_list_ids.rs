use std::collections::{HashMap, HashSet};
use std::fmt;
use std::sync::Arc;

use super::shared_id_list_format::IdListImage;

/// Exact membership, with a bounded cumulative delta for immutable bases.
#[derive(Clone, Default)]
pub struct IdListIds {
    storage: Storage,
}

#[derive(Clone)]
enum Storage {
    Owned(OwnedIds),
    Image(Arc<IdListImage>),
    Pending(PendingDelta),
}
impl Default for Storage {
    fn default() -> Self {
        Self::Owned(OwnedIds::default())
    }
}

#[derive(Clone, Default)]
struct OwnedIds {
    inline: HashSet<[u8; 8], ahash::RandomState>,
    other: HashSet<String>,
}
impl OwnedIds {
    fn contains(&self, key: &str) -> bool {
        match <[u8; 8]>::try_from(key.as_bytes()) {
            Ok(k) => self.inline.contains(&k),
            Err(_) => self.other.contains(key),
        }
    }
    fn set(&mut self, key: &str, present: bool) -> bool {
        match (<[u8; 8]>::try_from(key.as_bytes()), present) {
            (Ok(k), true) => self.inline.insert(k),
            (Ok(k), false) => self.inline.remove(&k),
            (Err(_), true) => self.other.insert(key.to_owned()),
            (Err(_), false) => self.other.remove(key),
        }
    }
    fn iter(&self) -> impl Iterator<Item = &str> {
        self.inline
            .iter()
            .map(|key| std::str::from_utf8(key).expect("IDs originated as UTF-8"))
            .chain(self.other.iter().map(String::as_str))
    }
}

#[derive(Clone, Default)]
struct DeltaChanges {
    inline: HashMap<[u8; 8], bool, ahash::RandomState>,
    other: HashMap<String, bool, ahash::RandomState>,
}
impl DeltaChanges {
    fn get(&self, key: &str) -> Option<bool> {
        match <[u8; 8]>::try_from(key.as_bytes()) {
            Ok(k) => self.inline.get(&k),
            Err(_) => self.other.get(key),
        }
        .copied()
    }
    fn set(&mut self, key: &str, operation: bool) {
        match <[u8; 8]>::try_from(key.as_bytes()) {
            Ok(k) => {
                self.inline.insert(k, operation);
            }
            Err(_) => {
                self.other.insert(key.to_owned(), operation);
            }
        }
    }
    fn remove(&mut self, key: &str) -> bool {
        match <[u8; 8]>::try_from(key.as_bytes()) {
            Ok(k) => self.inline.remove(&k),
            Err(_) => self.other.remove(key),
        }
        .is_some()
    }
    fn len(&self) -> usize {
        self.inline.len() + self.other.len()
    }
    fn iter(&self) -> impl Iterator<Item = (&str, bool)> {
        self.inline
            .iter()
            .map(|(key, op)| {
                (
                    std::str::from_utf8(key).expect("IDs originated as UTF-8"),
                    *op,
                )
            })
            .chain(self.other.iter().map(|(key, op)| (key.as_str(), *op)))
    }
}

#[derive(Clone)]
pub(super) struct PendingDelta {
    base: Arc<IdListImage>,
    changes: DeltaChanges,
    counts: (usize, usize),
    // Once a batch crosses the compaction threshold, reversing an edit
    // cannot cancel the full-base rebuild.
    pub(super) requires_full_base: bool,
}

#[derive(Clone, Copy)]
pub(super) enum CompactionPolicy {
    Immediate,
    Batch,
}

const BATCH_DELTA_DIVISOR: usize = 16;
const BATCH_SCRATCH_DIVISOR: usize = 8;

fn batch_compaction_limits(base_memberships: usize) -> (usize, usize) {
    (
        (base_memberships / 8)
            .clamp(1024, 65_536)
            .max(base_memberships / BATCH_DELTA_DIVISOR),
        (base_memberships / BATCH_SCRATCH_DIVISOR).max(1024),
    )
}

impl IdListIds {
    pub fn new() -> Self {
        Self::default()
    }
    pub fn contains(&self, value: &str) -> bool {
        match &self.storage {
            Storage::Owned(ids) => ids.contains(value),
            Storage::Image(image) => image.contains(value),
            Storage::Pending(p) => p
                .changes
                .get(value)
                .unwrap_or_else(|| p.base.contains(value)),
        }
    }
    pub fn insert(&mut self, value: String) -> bool {
        if let Storage::Owned(ids) = &mut self.storage {
            return match <[u8; 8]>::try_from(value.as_bytes()) {
                Ok(key) => ids.inline.insert(key),
                Err(_) => ids.other.insert(value),
            };
        }
        self.set(&value, true, CompactionPolicy::Immediate)
    }
    pub fn insert_str(&mut self, value: &str) -> bool {
        self.set(value, true, CompactionPolicy::Immediate)
    }
    pub fn remove(&mut self, value: &str) -> bool {
        self.set(value, false, CompactionPolicy::Immediate)
    }

    pub(super) fn set(&mut self, value: &str, present: bool, policy: CompactionPolicy) -> bool {
        if let Storage::Owned(ids) = &mut self.storage {
            return ids.set(value, present);
        }
        if self.contains(value) == present {
            return false;
        }
        self.make_pending();
        let Storage::Pending(p) = &mut self.storage else {
            unreachable!()
        };
        // A normalized operation differs from its base. Flipping it restores
        // the base value without probing the immutable image again.
        if !p.changes.remove(value) {
            p.changes.set(value, present);
        }
        let count = if value.len() == 8 {
            &mut p.counts.0
        } else {
            &mut p.counts.1
        };
        if present {
            *count += 1;
        } else {
            *count -= 1;
        }
        let base_len = p.base.len();
        let edits = p.changes.len();
        let shrunk = p.counts.0 + p.counts.1 < base_len / 4;
        let materialize = match policy {
            CompactionPolicy::Immediate => shrunk || edits > (base_len / 8).clamp(1024, 65_536),
            CompactionPolicy::Batch => {
                let (batch_limit, scratch_limit) = batch_compaction_limits(base_len);
                p.requires_full_base |= shrunk || edits > batch_limit;
                edits > scratch_limit
            }
        };
        if materialize {
            self.materialize();
        }
        true
    }
    fn make_pending(&mut self) {
        if let Storage::Image(base) = &self.storage {
            self.storage = Storage::Pending(PendingDelta {
                base: Arc::clone(base),
                changes: DeltaChanges::default(),
                counts: base.partition_counts(),
                requires_full_base: false,
            });
        }
    }
    fn materialize(&mut self) {
        let (inline, other) = self.partition_counts();
        let mut ids = OwnedIds {
            inline: HashSet::with_capacity_and_hasher(inline, Default::default()),
            other: HashSet::with_capacity(other),
        };
        self.visit_image_keys(
            |key| {
                ids.inline.insert(key);
            },
            |key| {
                ids.other.insert(key.to_owned());
            },
        );
        self.storage = Storage::Owned(ids);
    }
    #[cfg(test)]
    pub(super) fn has_compact_base(&self) -> bool {
        self.base_image().is_some_and(|image| image.is_compact())
    }
    pub fn len(&self) -> usize {
        if let Storage::Image(image) = &self.storage {
            return image.len();
        }
        let (a, b) = self.partition_counts();
        a + b
    }
    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }
    pub(crate) fn partition_counts(&self) -> (usize, usize) {
        match &self.storage {
            Storage::Owned(ids) => (ids.inline.len(), ids.other.len()),
            Storage::Image(image) => image.partition_counts(),
            Storage::Pending(p) => p.counts,
        }
    }
    /// Collect canonical encoder input without converting inline bytes through str.
    /// Public iteration and membership keep their existing behavior.
    pub(super) fn collect_image_keys(&self) -> (Vec<[u8; 8]>, Vec<&str>) {
        let (inline_count, other_count) = self.partition_counts();
        let mut inline = Vec::with_capacity(inline_count);
        let mut other = Vec::with_capacity(other_count);
        self.visit_image_keys(|key| inline.push(key), |key| other.push(key));
        (inline, other)
    }

    fn visit_image_keys<'a>(
        &'a self,
        mut inline: impl FnMut([u8; 8]),
        mut other: impl FnMut(&'a str),
    ) {
        self.all_image_keys(
            |key| {
                inline(key);
                true
            },
            |key| {
                other(key);
                true
            },
        );
    }

    fn all_image_keys<'a>(
        &'a self,
        mut inline: impl FnMut([u8; 8]) -> bool,
        mut other: impl FnMut(&'a str) -> bool,
    ) -> bool {
        match &self.storage {
            Storage::Owned(ids) => {
                ids.inline.iter().copied().all(inline)
                    && ids.other.iter().map(String::as_str).all(other)
            }
            Storage::Image(image) => image.all_image_keys(inline, other),
            Storage::Pending(p) => {
                let base_matches = p.base.all_image_keys(
                    |key| p.changes.inline.get(&key) == Some(&false) || inline(key),
                    |key| p.changes.other.get(key) == Some(&false) || other(key),
                );
                base_matches
                    && p.changes
                        .inline
                        .iter()
                        .all(|(key, present)| !*present || inline(*key))
                    && p.changes
                        .other
                        .iter()
                        .all(|(key, present)| !*present || other(key))
            }
        }
    }

    fn base_image(&self) -> Option<&Arc<IdListImage>> {
        match &self.storage {
            Storage::Image(image) => Some(image),
            Storage::Pending(p) => Some(&p.base),
            Storage::Owned(_) => None,
        }
    }

    pub fn iter(&self) -> impl Iterator<Item = &str> {
        let iter: Box<dyn Iterator<Item = &str> + '_> = match &self.storage {
            Storage::Owned(ids) => Box::new(ids.iter()),
            Storage::Image(image) => Box::new(image.iter()),
            Storage::Pending(p) => Box::new(
                p.base
                    .iter()
                    .filter(move |key| p.changes.get(key) != Some(false))
                    .chain(p.changes.iter().filter_map(|(key, op)| op.then_some(key))),
            ),
        };
        iter
    }
    pub(super) fn finish_private_batch(self: &mut Arc<Self>, name: &str) {
        if self.is_empty() {
            *Arc::make_mut(self) = Self::new();
            return;
        }
        match &self.storage {
            Storage::Image(_) => return,
            Storage::Pending(p) if !p.requires_full_base => {
                if p.changes.len() == 0 {
                    let base = Arc::clone(&p.base);
                    Arc::make_mut(self).storage = Storage::Image(base);
                }
                return;
            }
            Storage::Pending(p) if p.changes.other.is_empty() => {
                if let Some(image) = p.base.try_merge_heap(
                    name,
                    p.counts.0,
                    p.changes.inline.iter().map(|(key, &op)| (key, op)),
                ) {
                    *self = Arc::new(Self::from_image(image));
                    return;
                }
            }
            _ => {}
        }
        // Keep current storage if encoding fails.
        if let Ok(image) = IdListImage::build_heap(&[0; 32], name, self) {
            *Arc::make_mut(self) = Self::from_image(image);
        }
    }
    pub(crate) fn from_image(image: IdListImage) -> Self {
        Self {
            storage: Storage::Image(Arc::new(image)),
        }
    }
    #[cfg(test)]
    pub(super) fn pending(&self) -> Option<&PendingDelta> {
        if let Storage::Pending(p) = &self.storage {
            Some(p)
        } else {
            None
        }
    }
    #[cfg(test)]
    pub(super) fn base_digest(&self) -> Option<[u8; 32]> {
        self.base_image()
            .filter(|image| image.is_mapped())
            .map(|image| image.content_digest())
    }
    pub(super) fn packed_ef_section(&self) -> Option<&[u8]> {
        match &self.storage {
            Storage::Image(image) => image.packed_ef_section(),
            _ => None,
        }
    }
    pub(crate) fn mapped_bytes(&self) -> usize {
        self.base_image().map_or(0, |image| image.mapped_bytes())
    }
    pub(crate) fn is_mapped(&self) -> bool {
        self.mapped_bytes() > 0
    }

    #[cfg(test)]
    pub(crate) fn owned_capacities_for_test(&self) -> Option<(usize, usize)> {
        if let Storage::Owned(ids) = &self.storage {
            Some((ids.inline.capacity(), ids.other.capacity()))
        } else {
            None
        }
    }
    #[cfg(test)]
    pub(super) fn delta_len_for_test(&self) -> usize {
        match &self.storage {
            Storage::Pending(p) => p.changes.len(),
            _ => 0,
        }
    }
}
impl PartialEq for IdListIds {
    fn eq(&self, other: &Self) -> bool {
        self.len() == other.len()
            && self.all_image_keys(
                |key| other.contains(std::str::from_utf8(&key).expect("valid inline key")),
                |key| other.contains(key),
            )
    }
}
impl Eq for IdListIds {}
impl fmt::Debug for IdListIds {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("IdListIds")
            .field("len", &self.len())
            .field("mapped", &self.is_mapped())
            .field("mapped_bytes", &self.mapped_bytes())
            .finish()
    }
}
impl FromIterator<String> for IdListIds {
    fn from_iter<T: IntoIterator<Item = String>>(values: T) -> Self {
        let mut ids = Self::new();
        for value in values {
            ids.insert(value);
        }
        ids
    }
}
impl<const N: usize> From<[String; N]> for IdListIds {
    fn from(values: [String; N]) -> Self {
        values.into_iter().collect()
    }
}

#[cfg(test)]
#[path = "pending_ahash_tests.rs"]
mod pending_ahash_tests;

#[cfg(test)]
#[path = "private_id_list_tests.rs"]
mod private_id_list_tests;

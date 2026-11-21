//! List updates between source selection and publication. A base carries its
//! covered prefix; raw changes advance an installed cursor by consumed bytes.
use super::{
    IdList, IdListManifest, IdListMetadata, IdListPropagationUpdate, IdListPublicationMode,
    IdListUpdate, IdListUpdateBase, IdListsUpdateListener,
};
use crate::StatsigErr;
use std::collections::HashMap;

type Cursors = HashMap<String, IdListMetadata>;

pub(crate) enum PreparedIdListUpdate {
    Raw(IdListUpdate),
    Base(IdList),
}

impl PreparedIdListUpdate {
    pub(super) fn metadata(&self) -> &IdListMetadata {
        match self {
            Self::Raw(update) => &update.new_metadata,
            Self::Base(list) => &list.metadata,
        }
    }
}

impl From<IdListUpdate> for PreparedIdListUpdate {
    fn from(update: IdListUpdate) -> Self {
        Self::Raw(update)
    }
}

pub(crate) struct IdListUpdateBatch {
    pub(crate) mode: IdListPublicationMode,
    pub(crate) expected: Option<HashMap<String, IdListUpdateBase>>,
    pub(crate) file_failure: Option<StatsigErr>,
    pub(crate) updates: HashMap<String, PreparedIdListUpdate>,
    pub(crate) propagation: HashMap<String, IdListPropagationUpdate>,
}

impl IdListUpdateBatch {
    pub(super) fn new(
        installed: &Cursors,
        targets: &IdListManifest,
        mode: IdListPublicationMode,
        check_cursors: bool,
    ) -> Self {
        // A full refresh also checks cursors for names it will remove.
        let expected = check_cursors.then(|| {
            installed
                .iter()
                .filter(|(name, _)| {
                    mode != IdListPublicationMode::Merge || targets.contains_key(*name)
                })
                .map(|(name, metadata)| {
                    (
                        name.clone(),
                        IdListUpdateBase::expected(Some(metadata.clone())),
                    )
                })
                .collect()
        });
        Self {
            mode,
            expected,
            file_failure: None,
            updates: HashMap::with_capacity(targets.len()),
            propagation: HashMap::with_capacity(targets.len()),
        }
    }

    pub(super) fn record(
        &mut self,
        name: String,
        update: PreparedIdListUpdate,
        range: std::ops::Range<u64>,
    ) {
        if let Some(expected) = &mut self.expected {
            expected
                .entry(name.clone())
                .or_insert_with(|| IdListUpdateBase::expected(None));
        }
        if let Some(observation) = self.propagation.get_mut(&name) {
            observation.applied_range = Some(range);
        }
        self.updates.insert(name, update);
    }

    pub(super) fn keep(&mut self, name: String, metadata: IdListMetadata) {
        self.updates.insert(
            name,
            PreparedIdListUpdate::Raw(IdListUpdate {
                raw_changeset: None,
                new_metadata: metadata,
            }),
        );
    }

    pub(super) fn retain_failed_list(&mut self, name: String, installed: Option<&IdListMetadata>) {
        self.propagation.remove(&name);
        if let Some(metadata) = installed {
            self.keep(name, metadata.clone());
        }
    }

    // A concurrent cold load can have installed a prefix while the poll
    // fetched other names. Retain it only if the advertised target is stable.
    pub(super) fn preserve_concurrent_loads(
        &mut self,
        installed: Cursors,
        previous: Option<&IdListManifest>,
        targets: &IdListManifest,
    ) {
        for (name, current) in installed {
            let old = previous.and_then(|manifest| manifest.get(&name));
            if !self.updates.contains_key(&name)
                && old.zip(targets.get(&name)).is_some_and(|(old, new)| {
                    old.metadata.file_version() == new.metadata.file_version()
                })
            {
                if let Some(expected) = &mut self.expected {
                    expected
                        .entry(name.clone())
                        .or_insert_with(|| IdListUpdateBase::expected(Some(current.clone())));
                }
                self.keep(name, current);
            }
        }
    }

    pub(super) fn matches_cursors(&self, planned: &Cursors, installed: &Cursors) -> bool {
        self.updates.iter().all(|(name, update)| {
            let target = update.metadata();
            id_list_range_start(planned.get(name), target)
                == id_list_range_start(installed.get(name), target)
        })
    }

    pub(super) fn publish_to_listener(
        self,
        listener: &dyn IdListsUpdateListener,
        eager_downloads: Option<u64>,
    ) -> Result<(), StatsigErr> {
        let Self {
            updates,
            expected,
            mode,
            propagation,
            ..
        } = self;
        // The public listener predates typed payloads. Convert at this boundary.
        let mut bases = expected;
        let mut raw = HashMap::with_capacity(updates.len());
        for (name, update) in updates {
            let update = match update {
                PreparedIdListUpdate::Raw(update) => update,
                PreparedIdListUpdate::Base(list) => {
                    let Some(bases) = &mut bases else {
                        return Err(StatsigErr::InvalidOperation(
                            "unexpected ID-list base".into(),
                        ));
                    };
                    let new_metadata = list.metadata.clone();
                    bases
                        .entry(name.clone())
                        .or_insert_with(|| IdListUpdateBase::expected(None))
                        .list = Some(Box::new(list));
                    IdListUpdate {
                        new_metadata,
                        raw_changeset: Some(String::new()),
                    }
                }
            };
            raw.insert(name, update);
        }
        if let Some(bases) = bases {
            return listener.try_receive_id_list_snapshot_updates(
                raw,
                bases,
                propagation,
                mode,
                eager_downloads,
            );
        }
        if let Some(downloads) = eager_downloads {
            return listener.try_receive_eager_id_list_updates(
                raw,
                propagation,
                mode == IdListPublicationMode::IncompleteRefresh,
                downloads,
            );
        }
        match mode {
            IdListPublicationMode::Replace => {
                listener.try_receive_id_list_updates_with_propagation(raw, propagation)
            }
            IdListPublicationMode::IncompleteRefresh => {
                listener.try_receive_incomplete_id_list_refresh(raw, propagation)
            }
            IdListPublicationMode::Merge => {
                listener.try_receive_partial_id_list_updates_with_propagation(raw, propagation)
            }
        }
    }
}

pub(super) fn id_list_range_start(
    current: Option<&IdListMetadata>,
    target: &IdListMetadata,
) -> Option<u64> {
    target
        .file_version()
        .download_from(current.map(IdListMetadata::file_version))
        .map(|update| update.start)
}

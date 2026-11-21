use std::collections::HashMap;
use std::sync::Arc;

use arc_swap::ArcSwap;

use crate::id_lists_adapter::membership_client::MembershipRevision;

#[derive(Default)]
pub(crate) struct RemoteIdListRevisions {
    lists: ArcSwap<HashMap<String, Arc<MembershipRevision>>>,
}

impl RemoteIdListRevisions {
    pub(crate) fn get(&self, list: &str) -> Option<Arc<MembershipRevision>> {
        self.lists.load().get(list).cloned()
    }

    /// Preserve a list's Arc while its observed revision matches, including across CDN fallback.
    /// Removing and re-adding a list gives it a new Arc.
    pub(super) fn update<'a>(
        &self,
        enrolled: impl Iterator<Item = &'a str>,
        revision_for: impl Fn(&str) -> Option<MembershipRevision>,
    ) {
        let current = self.lists.load();
        let next: HashMap<_, _> = enrolled
            .filter_map(|name| {
                let revision = revision_for(name)?;
                let observed = match current.get(name) {
                    Some(previous) if **previous == revision => Arc::clone(previous),
                    _ => Arc::new(revision),
                };
                Some((name.to_owned(), observed))
            })
            .collect();
        if **current != next {
            self.lists.store(Arc::new(next));
        }
    }
}

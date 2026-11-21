use super::evaluator_context::{EvaluatorContext, IdListResolution};
use crate::event_logging::id_list_accesses::IdListAccessRecorder;
use crate::hashing::{IdListFingerprintWidth, with_id_list_fingerprint};

impl EvaluatorContext<'_> {
    /// Returns None when the local list is unavailable.
    pub(super) fn resolve_id_list_membership(
        &mut self,
        list: &str,
        id: &str,
        unit_id_type: Option<&str>,
    ) -> Option<bool> {
        let local = self
            .id_list_resolver
            .lookup(list, id, self.id_list_access_recorder);
        if id.is_empty() {
            return local;
        }
        if let (Some(remote), Some(id_type)) = (&mut self.remote_id_lists, unit_id_type) {
            // The remote lookup records comparison metrics. Evaluation uses the local result.
            let _ = remote.lookup(self.user, list, id_type, id, local);
        }
        local
    }
}

impl IdListResolution<'_> {
    fn lookup(&self, name: &str, id: &str, recorder: &dyn IdListAccessRecorder) -> Option<bool> {
        with_id_list_fingerprint(id, IdListFingerprintWidth::Bits48, |key| match self {
            Self::MapLookup(lists) => {
                let list = lists.get(name)?;
                recorder.record(name);
                Some(list.ids.contains(key))
            }
            Self::Callback(callback) => Some(callback(name, key)),
        })
    }
}

//! Remote membership comparisons share a cache on the native user, scoped to its SDK.
use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, OnceLock, Weak};
use std::time::{Duration, Instant};

use arc_swap::{ArcSwap, ArcSwapOption, RefCnt};
use parking_lot::{Condvar, Mutex};

use crate::id_lists_adapter::membership_client::{
    MembershipAnswer, MembershipRevision, lookup_membership,
};
use crate::networking::NetworkClient;
use crate::observability::ops_stats::OpsStatsForInstance;
use crate::statsig_runtime::StatsigRuntime;
use crate::user::StatsigUserInternal;
use crate::user::fast_statsig_user::FastStatsigUser;
use crate::user::statsig_user_internal::InternalUserRef;
use crate::{Statsig, StatsigOptions};

use super::remote_id_list_allowlist::{RemoteIdListAllowlist, canonical_id_type};
use super::remote_id_list_metrics::{LocalFallbackCounts, RemoteIdListMetrics, rpc_result_label};

const SERVE_WAIT: Duration = Duration::from_millis(100);

impl StatsigUserInternal<'_, '_> {
    /// Share one membership wait budget across the evaluations in this call.
    #[doc(hidden)]
    #[must_use]
    pub fn with_membership_deadline(mut self, sdk: &Statsig) -> Self {
        if sdk.remote_id_list_resolver.is_some() {
            self.membership_deadline
                .get_or_insert_with(|| Instant::now() + SERVE_WAIT);
        }
        self
    }
}

type MembershipWait = fn(&mut (dyn FnMut() + Send));

enum MembershipNetwork {
    Shared(Arc<NetworkClient>),
    Owned {
        sdk_key: String,
        options: Arc<StatsigOptions>,
        client: OwnedMembershipClient,
    },
}

#[derive(Default)]
struct OwnedMembershipClient {
    initialization: OnceLock<()>,
    published: OnceLock<Option<Box<NetworkClient>>>,
}

impl OwnedMembershipClient {
    fn get_or_init(&self, build: impl FnOnce() -> NetworkClient) -> Option<&NetworkClient> {
        self.initialization.get_or_init(|| {
            // Build outside the publication slot so shutdown can seal it immediately.
            let network = Box::new(build());
            let _ = self.published.set(Some(network));
        });
        self.published.get()?.as_deref()
    }

    fn shutdown(&self) {
        if let Some(network) = self.published.get_or_init(|| None) {
            network.shutdown();
        }
    }
}

pub(crate) struct RemoteIdListResolver {
    endpoint: String,
    network: MembershipNetwork,
    allowlist: RemoteIdListAllowlist,
    closed: AtomicBool,
    revisions: super::remote_id_list_revisions::RemoteIdListRevisions,
    revision_deadline: Mutex<Option<tokio::time::Instant>>,
    wait_with_binding: OnceLock<MembershipWait>,
    metrics: RemoteIdListMetrics,
    runtime: Weak<StatsigRuntime>,
}

impl RemoteIdListResolver {
    pub(super) fn new(
        options: &Arc<StatsigOptions>,
        ops: &Arc<OpsStatsForInstance>,
        endpoint: url::Url,
        sdk_key: &str,
        runtime: &Arc<StatsigRuntime>,
        network: Option<Arc<NetworkClient>>,
        allowlist: RemoteIdListAllowlist,
    ) -> Self {
        runtime.prepare_owned_runtime();
        Self {
            endpoint: endpoint.into(),
            network: match network {
                Some(network) => MembershipNetwork::Shared(network),
                None => MembershipNetwork::Owned {
                    sdk_key: sdk_key.to_owned(),
                    options: Arc::clone(options),
                    client: OwnedMembershipClient::default(),
                },
            },
            allowlist,
            closed: AtomicBool::new(false),
            revisions: Default::default(),
            revision_deadline: Mutex::new(None),
            wait_with_binding: OnceLock::new(),
            metrics: RemoteIdListMetrics::new(options, ops),
            runtime: Arc::downgrade(runtime),
        }
    }

    fn is_closed(&self) -> bool {
        self.closed.load(Ordering::Acquire)
    }

    fn network_for_lookup(&self) -> Option<&NetworkClient> {
        if self.is_closed() {
            return None;
        }
        match &self.network {
            MembershipNetwork::Shared(client) => Some(client),
            MembershipNetwork::Owned {
                sdk_key,
                options,
                client,
            } => client.get_or_init(|| NetworkClient::with_sdk_headers(sdk_key, options)),
        }
    }

    pub(super) fn session(
        self: &Arc<Self>,
        deadline: Option<Instant>,
    ) -> Option<RemoteIdListSession<'_>> {
        (!self.is_closed()).then(|| RemoteIdListSession {
            client: self,
            deadline,
            cache: OnceLock::new(),
            unconfirmed: HashMap::new(),
        })
    }

    pub(crate) fn observe_manifest_poll(
        &self,
        manifest: Option<&crate::id_lists_adapter::IdListManifest>,
        max_age: Option<Duration>,
    ) {
        if let Some(max_age) = max_age {
            let now = tokio::time::Instant::now();
            let mut deadline = self.revision_deadline.lock();
            if manifest.is_some() {
                *deadline = Some(now + max_age);
            } else if deadline.take_if(|expires| now > *expires).is_some() {
                self.revisions.clear();
            }
        }
        if let Some(manifest) = manifest {
            self.observe_manifest(manifest);
        }
    }

    fn observe_manifest(&self, manifest: &crate::id_lists_adapter::IdListManifest) {
        self.revisions.update(self.allowlist.list_names(), |name| {
            manifest
                .get(name)?
                .metadata
                .file_version()
                .membership_revision()
        });
    }

    pub(super) fn shutdown(&self) {
        self.closed.store(true, Ordering::Release);
        if let MembershipNetwork::Owned { client, .. } = &self.network {
            client.shutdown();
        }
    }
}

enum CachedLookup {
    Ready(Option<bool>),
    Pending {
        entry: Arc<MembershipCacheEntry>,
        start: bool,
    },
}

#[derive(Clone, Copy)]
struct CompletedMembership {
    is_member: bool,
    reusable: bool,
}

/// Replacing the entry for a changed identity or manifest revision leaves
/// in-flight requests and their waiters attached to their original entry.
struct MembershipCacheEntry {
    list: String,
    id_type: String,
    id: String,
    observed_revision: Option<Arc<MembershipRevision>>,
    answer: OnceLock<Option<CompletedMembership>>,
    runtime_id: OnceLock<tokio::runtime::Id>,
    wait_lock: Mutex<()>,
    fallbacks: LocalFallbackCounts,
    completed: Condvar,
}

/// All conditions in one evaluation share its requests and answers.
pub(crate) struct RemoteIdListSession<'a> {
    client: &'a Arc<RemoteIdListResolver>,
    deadline: Option<Instant>,
    cache: OnceLock<Arc<RemoteIdListCache>>,
    // Only a pending or uncorroborated reply needs evaluation-local retention.
    unconfirmed: HashMap<String, Arc<MembershipCacheEntry>>,
}

impl RemoteIdListSession<'_> {
    fn cache_for(&self, user: &StatsigUserInternal<'_, '_>) -> &Arc<RemoteIdListCache> {
        self.cache
            .get_or_init(|| RemoteIdListCache::for_user(user, self.client))
    }

    pub(crate) fn lookup(
        &mut self,
        user: &StatsigUserInternal<'_, '_>,
        list: &str,
        id_type: &str,
        id: &str,
        local: Option<bool>,
    ) -> Option<bool> {
        let id_type = canonical_id_type(id_type);
        let cached = self
            .unconfirmed
            .get(list)
            .filter(|entry| entry.id_type == id_type && entry.id == id)
            .and_then(|entry| entry.cached_lookup(true));
        let lookup = match cached {
            Some(lookup) => lookup,
            None if self.client.allowlist.allows(list, id_type) => {
                self.cache_for(user)
                    .entry_for(self.client, list, id_type, id)
            }
            None => return None,
        };
        let (entry, start) = match lookup {
            CachedLookup::Ready(Some(member)) => {
                self.client.metrics.record_cache_hit(list, local, member);
                return Some(member);
            }
            CachedLookup::Ready(None) => {
                self.client
                    .metrics
                    .record_cache_miss(list, local, Some(None));
                return None;
            }
            CachedLookup::Pending { entry, start } => (entry, start),
        };
        let deadline = *self
            .deadline
            .get_or_insert_with(|| Instant::now() + SERVE_WAIT);
        if start {
            entry.start(self.client);
        }
        let mut answer = entry.answer.get().copied();
        if answer.is_none() && deadline > Instant::now() && entry.can_block_caller() {
            let mut wait = || {
                entry.wait_until(deadline);
                // Reacquiring the binding's runtime lock can take longer than the wait budget.
                answer = entry.answer.get().copied();
            };
            match self.client.wait_with_binding.get() {
                Some(wait_with_binding) => wait_with_binding(&mut wait),
                None => wait(),
            }
        }
        let comparison = answer.map(|reply| reply.map(|answer| answer.is_member));
        let metrics = &self.client.metrics;
        metrics.record_cache_miss(list, local, comparison);
        if answer.is_none() && metrics.is_enabled() {
            entry.fallbacks.add(local);
            // Completion may already have drained the counters before this increment.
            if let Some(Some(ready)) = entry.answer.get() {
                metrics.record_completed_fallbacks(list, &entry.fallbacks, ready.is_member);
            }
        }
        if !matches!(
            answer,
            Some(Some(CompletedMembership { reusable: true, .. }))
        ) {
            self.unconfirmed.insert(list.to_owned(), entry);
        }
        comparison.flatten()
    }
}

/// A user may share this slot with its clones before any SDK has claimed it.
pub(crate) type SharedMembershipCache = Arc<ArcSwapOption<RemoteIdListCache>>;

pub(crate) struct RemoteIdListCache {
    owner: Weak<RemoteIdListResolver>,
    lists: ArcSwap<HashMap<String, Arc<MembershipCacheEntry>>>,
}

impl RemoteIdListCache {
    fn for_user(
        user: &StatsigUserInternal<'_, '_>,
        client: &Arc<RemoteIdListResolver>,
    ) -> Arc<Self> {
        let memberships = match user.user_ref {
            InternalUserRef::Fast(user) => &user.memberships,
            InternalUserRef::Public(user) => &user.memberships,
            // Prepared overlays share metadata across identities.
            InternalUserRef::Prepared(_) => return Arc::new(Self::new(client)),
        };
        let slot =
            memberships.get_or_init(|| Arc::new(ArcSwapOption::from_pointee(Self::new(client))));
        loop {
            let current = slot.load();
            if let Some(cache) = current.as_ref() {
                if cache.owner.as_ptr() == Arc::as_ptr(client) {
                    return Arc::clone(cache);
                }
                // A second live SDK gets its own cache for this evaluation.
                if cache.owner.upgrade().is_some_and(|sdk| !sdk.is_closed()) {
                    return Arc::new(Self::new(client));
                }
            }
            let replacement = Arc::new(Self::new(client));
            let previous = slot.compare_and_swap(&current, Some(Arc::clone(&replacement)));
            if RefCnt::as_ptr(&*current) == RefCnt::as_ptr(&*previous) {
                return replacement;
            }
        }
    }

    fn new(client: &Arc<RemoteIdListResolver>) -> Self {
        Self {
            owner: Arc::downgrade(client),
            lists: ArcSwap::default(),
        }
    }

    fn entry_for(
        &self,
        client: &RemoteIdListResolver,
        list: &str,
        id_type: &str,
        id: &str,
    ) -> CachedLookup {
        loop {
            let lists = self.lists.load();
            let observed_revision = client.revisions.get(list);
            if let Some(lookup) = lists
                .get(list)
                .filter(|entry| {
                    entry.id_type == id_type
                        && entry.id == id
                        && entry.observed_revision.as_ref().map(Arc::as_ptr)
                            == observed_revision.as_ref().map(Arc::as_ptr)
                })
                .and_then(|entry| entry.cached_lookup(false))
            {
                return lookup;
            }
            let entry = Arc::new(MembershipCacheEntry {
                list: list.into(),
                id_type: id_type.into(),
                id: id.into(),
                observed_revision,
                answer: OnceLock::new(),
                runtime_id: OnceLock::new(),
                wait_lock: Mutex::default(),
                fallbacks: LocalFallbackCounts::default(),
                completed: Condvar::new(),
            });
            // The writer that publishes the pending entry owns starting its request.
            let mut next = (**lists).clone();
            next.insert(list.into(), entry.clone());
            if Arc::ptr_eq(&lists, &self.lists.compare_and_swap(&lists, Arc::new(next))) {
                return CachedLookup::Pending { entry, start: true };
            }
        }
    }
}

impl MembershipCacheEntry {
    fn cached_lookup(self: &Arc<Self>, same_evaluation: bool) -> Option<CachedLookup> {
        match self.answer.get() {
            Some(Some(answer)) if same_evaluation || answer.reusable => {
                Some(CachedLookup::Ready(Some(answer.is_member)))
            }
            Some(None) if same_evaluation => Some(CachedLookup::Ready(None)),
            None => Some(CachedLookup::Pending {
                entry: self.clone(),
                start: false,
            }),
            Some(_) => None,
        }
    }

    fn can_block_caller(&self) -> bool {
        // Avoid waiting on the reactor that must complete the request.
        let Ok(current) = tokio::runtime::Handle::try_current() else {
            return true;
        };
        self.runtime_id.get().is_some_and(|io| current.id() != *io)
    }

    fn wait_until(&self, deadline: Instant) {
        if let Some(mut guard) = self.wait_lock.try_lock_until(deadline) {
            self.completed
                .wait_while_until(&mut guard, |_| self.answer.get().is_none(), deadline);
        }
    }

    fn start(self: &Arc<Self>, client: &Arc<RemoteIdListResolver>) {
        // Wake waiters on cancellation or spawn failure, including SDK shutdown.
        let client = client.clone();
        let completion_client = client.clone();
        let task = scopeguard::guard(self.clone(), move |entry| {
            entry.finish(completion_client.as_ref(), None)
        });
        let Some(runtime) = client.runtime.upgrade() else {
            return;
        };
        let Some(io) = runtime.try_get_owned_runtime_handle() else {
            return;
        };
        let _ = self.runtime_id.set(io.id());
        runtime.try_spawn_on(&io, "id_list_membership_lookup", async move {
            let Some(network) = client.network_for_lookup() else {
                return;
            };
            let rpc_start = client.metrics.rpc_start();
            let result = lookup_membership(
                network,
                &client.endpoint,
                &task.list,
                &task.id_type,
                &task.id,
            )
            .await;
            let elapsed = rpc_start.map(|start| start.elapsed());
            let outcome = rpc_result_label(&result);
            let entry = scopeguard::ScopeGuard::into_inner(task);
            entry.finish(&client, result.ok().flatten());
            client
                .metrics
                .record_rpc_latency(&entry.list, elapsed, outcome);
        });
    }

    fn finish(&self, client: &RemoteIdListResolver, response: Option<MembershipAnswer>) {
        // This lookup can compare any reply. Reuse across evaluations requires a matching revision.
        let answer = response.map(|response| CompletedMembership {
            is_member: response.is_member,
            reusable: response.revision.is_some()
                && response.revision.as_ref() == self.observed_revision.as_deref(),
        });
        let guard = self.wait_lock.lock();
        if self.answer.set(answer).is_err() {
            return;
        }
        drop(guard);
        self.completed.notify_all();
        if let Some(answer) = answer {
            client.metrics.record_completed_fallbacks(
                &self.list,
                &self.fallbacks,
                answer.is_member,
            );
        }
    }
}

impl Statsig {
    /// Whether binding evaluations can encounter a remote membership wait.
    #[doc(hidden)]
    pub fn has_remote_id_list_resolver(&self) -> bool {
        self.remote_id_list_resolver.is_some()
    }

    /// Let a binding release its runtime lock while a remote answer is pending.
    /// Set at binding construction. Only an opted-in resolver uses the callback.
    #[doc(hidden)]
    pub fn set_remote_id_list_wait(&self, wait: fn(&mut (dyn FnMut() + Send))) {
        if let Some(resolver) = &self.remote_id_list_resolver {
            let _ = resolver.wait_with_binding.set(wait);
        }
    }

    /// Share membership lookups between a binding's original user and its evaluation clone.
    #[doc(hidden)]
    pub fn clone_user_for_evaluation(&self, user: &FastStatsigUser) -> FastStatsigUser {
        if self.remote_id_list_resolver.is_some() {
            user.memberships.get_or_init(Default::default);
        }
        user.clone()
    }
}

#[cfg(test)]
#[path = "__tests__/remote_id_lists_tests.rs"]
mod tests;

//! Immutable metadata with an independently owned identity for one evaluation.
//!
//! This is an input snapshot, not an evaluation or configuration cache. The
//! evaluator always reads the current Statsig instance. Cloning an exposure
//! retains the base metadata and this call's overlay without cloning its maps.
use std::{
    ops::Deref,
    sync::{Arc, OnceLock},
};

use super::{
    fast_statsig_user::{FastStatsigUser, FastUserCustomMap, FastUserData, FastUserUnitIDMap},
    user_value::UserValue,
};
use crate::hashing;

pub struct PreparedUser {
    pub(crate) base: Option<Arc<FastUserData>>,
    pub(crate) input: PreparedUserInputStorage,
}

#[derive(Clone, Default)]
pub struct PreparedUserInput {
    pub user_id: Option<UserValue>,
    pub custom: Option<FastUserCustomMap>,
    /// Only caller-supplied IDs. Context IDs remain shared in the base snapshot.
    pub custom_ids: Option<Arc<FastUserUnitIDMap>>,
    pub request: Option<Arc<PreparedRequestFields>>,
}

/// Borrowed exact-key overlay, equivalent to extending the context ID map.
/// Lookup, hashing, and logging use this same view without building a merged map.
pub(crate) struct PreparedCustomIDs<'a> {
    base: Option<&'a FastUserUnitIDMap>,
    overlay: Option<&'a FastUserUnitIDMap>,
}

impl<'a> PreparedCustomIDs<'a> {
    fn get_exact(&self, id_type: &str) -> Option<&'a UserValue> {
        self.overlay
            .and_then(|ids| ids.get(id_type))
            .or_else(|| self.base?.get(id_type))
    }

    fn get(&self, id_type: &str, lowercased_id_type: &str) -> Option<&'a UserValue> {
        // Exact context keys precede alternate-case overlay keys, just as they
        // do after an ordinary map merge.
        self.get_exact(id_type)
            .or_else(|| self.get_exact(lowercased_id_type))
    }

    pub(crate) fn iter(&self) -> impl Iterator<Item = (&'a String, &'a UserValue)> + '_ {
        self.base
            .into_iter()
            .flat_map(|ids| ids.iter())
            .filter(|(key, _)| !self.overlay.is_some_and(|ids| ids.contains_key(*key)))
            .chain(self.overlay.into_iter().flat_map(|ids| ids.iter()))
    }
}

impl serde::Serialize for PreparedCustomIDs<'_> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        if self.overlay.is_none() {
            return serde::Serialize::serialize(&self.base, serializer);
        }
        serializer.collect_map(self.iter())
    }
}

fn custom_ids<'a>(
    input: &'a PreparedUserInput,
    base: Option<&'a FastUserData>,
) -> Option<PreparedCustomIDs<'a>> {
    let base = base.and_then(|data| data.custom_ids.as_ref());
    let overlay = input.custom_ids.as_deref();
    (base.is_some() || overlay.is_some()).then_some(PreparedCustomIDs { base, overlay })
}

/// Sparse request overlay: calls without request fields allocate no storage for
/// these values. Promoted inputs share this immutable snapshot.
#[derive(Default)]
pub struct PreparedRequestFields {
    pub ip: Option<UserValue>,
    pub country: Option<UserValue>,
    pub locale: Option<UserValue>,
    pub user_agent: Option<UserValue>,
}

// Intentionally inline: boxing scalar-only input would restore the allocation
// avoided before sampling. Nonempty custom maps share ownership immediately, so promotion
// never duplicates a map. The loggable form below remains two compact Arcs.
#[allow(clippy::large_enum_variant)]
pub(crate) enum PreparedUserInputStorage {
    Inline(PreparedUserInput, OnceLock<Arc<PreparedUserInput>>),
    Shared(Arc<PreparedUserInput>),
}

impl Deref for PreparedUserInputStorage {
    type Target = PreparedUserInput;
    fn deref(&self) -> &Self::Target {
        match self {
            Self::Inline(input, _) => input,
            Self::Shared(input) => input,
        }
    }
}

impl PreparedUserInputStorage {
    fn shared(&self) -> Arc<PreparedUserInput> {
        match self {
            Self::Inline(input, shared) => shared.get_or_init(|| Arc::new(input.clone())).clone(),
            Self::Shared(input) => input.clone(),
        }
    }
}

#[derive(Clone)]
pub struct OwnedPreparedUser {
    pub(crate) base: Option<Arc<FastUserData>>,
    pub(crate) input: Arc<PreparedUserInput>,
}

impl Clone for PreparedUser {
    fn clone(&self) -> Self {
        Self {
            base: self.base.clone(),
            input: PreparedUserInputStorage::Shared(self.input.shared()),
        }
    }
}

impl PreparedUser {
    pub fn new(
        base: Option<Arc<FastUserData>>,
        user_id: Option<UserValue>,
        custom: Option<FastUserCustomMap>,
    ) -> Self {
        Self::with_input(
            base,
            PreparedUserInput {
                user_id,
                custom,
                ..Default::default()
            },
        )
    }

    pub fn with_input(base: Option<Arc<FastUserData>>, input: PreparedUserInput) -> Self {
        let input = if input
            .custom
            .as_ref()
            .is_some_and(|custom| !custom.is_empty())
        {
            PreparedUserInputStorage::Shared(Arc::new(input))
        } else {
            PreparedUserInputStorage::Inline(input, OnceLock::new())
        };
        Self { base, input }
    }

    pub(crate) fn to_owned(&self) -> OwnedPreparedUser {
        OwnedPreparedUser {
            base: self.base.clone(),
            input: self.input.shared(),
        }
    }

    pub(crate) fn get_primary_value(&self, field: &str) -> Option<&UserValue> {
        primary_value(&self.input, self.base.as_deref(), field)
    }

    pub(crate) fn get_unit_id_by_name(
        &self,
        id_type: &str,
        lowercased_id_type: &str,
    ) -> Option<&UserValue> {
        if lowercased_id_type == "userid" {
            return self.input.user_id.as_ref();
        }
        self.custom_ids()?.get(id_type, lowercased_id_type)
    }

    pub(crate) fn custom_ids(&self) -> Option<PreparedCustomIDs<'_>> {
        custom_ids(&self.input, self.base.as_deref())
    }

    pub(crate) fn get_custom_value(&self, key: &str) -> Option<&UserValue> {
        self.input
            .custom
            .as_ref()
            .and_then(|custom| custom.get(key))
            .or_else(|| self.base.as_ref()?.custom.as_ref()?.get(key))
    }

    pub(crate) fn create_exposure_dedupe_user_hash(&self, unit_id_type: Option<&str>) -> u64 {
        exposure_hash(&self.input, self.base.as_deref(), unit_id_type)
    }

    // Used only by compatibility callbacks requiring a public StatsigUser.
    pub(crate) fn to_public_user(&self) -> crate::StatsigUser {
        let mut data = self.base.as_deref().cloned().unwrap_or_default();
        data.user_id = self.input.user_id.clone();
        if let Some(request) = &self.input.request {
            for (destination, overlay) in [
                (&mut data.ip, &request.ip),
                (&mut data.country, &request.country),
                (&mut data.locale, &request.locale),
                (&mut data.user_agent, &request.user_agent),
            ] {
                if overlay.is_some() {
                    *destination = overlay.clone();
                }
            }
        }
        if let Some(custom) = &self.input.custom {
            data.custom.get_or_insert_with(Default::default).extend(
                custom
                    .iter()
                    .map(|(key, value)| (key.clone(), value.clone())),
            );
        }
        if let Some(ids) = &self.input.custom_ids {
            data.custom_ids
                .get_or_insert_with(Default::default)
                .extend(ids.iter().map(|(key, value)| (key.clone(), value.clone())));
        }
        FastStatsigUser::new(data).to_public_user()
    }
}

impl OwnedPreparedUser {
    pub(crate) fn custom_ids(&self) -> Option<PreparedCustomIDs<'_>> {
        custom_ids(&self.input, self.base.as_deref())
    }

    pub(crate) fn get_primary_value(&self, field: &str) -> Option<&UserValue> {
        primary_value(&self.input, self.base.as_deref(), field)
    }

    pub(crate) fn create_exposure_dedupe_user_hash(&self, unit_id_type: Option<&str>) -> u64 {
        exposure_hash(&self.input, self.base.as_deref(), unit_id_type)
    }
}

fn primary_value<'a>(
    input: &'a PreparedUserInput,
    base: Option<&'a FastUserData>,
    field: &str,
) -> Option<&'a UserValue> {
    let request = input.request.as_deref();
    match field {
        "userid" => input.user_id.as_ref(),
        "ip" => request
            .and_then(|request| request.ip.as_ref())
            .or_else(|| base?.ip.as_ref()),
        "country" => request
            .and_then(|request| request.country.as_ref())
            .or_else(|| base?.country.as_ref()),
        "locale" => request
            .and_then(|request| request.locale.as_ref())
            .or_else(|| base?.locale.as_ref()),
        "useragent" => request
            .and_then(|request| request.user_agent.as_ref())
            .or_else(|| base?.user_agent.as_ref()),
        "email" => base?.email.as_ref(),
        "appversion" => base?.app_version.as_ref(),
        _ => None,
    }
}

fn exposure_hash(
    input: &PreparedUserInput,
    base: Option<&FastUserData>,
    unit_id_type: Option<&str>,
) -> u64 {
    let user_id_hash = input.user_id.as_ref().map_or(0, UserValue::hash_value);
    if input.custom_ids.is_some() {
        let ids = custom_ids(input, base).expect("custom ID overlay is present");
        let unit_id_hash = |id_type: &str| {
            if id_type.eq_ignore_ascii_case("userid") {
                user_id_hash
            } else {
                ids.get_exact(id_type)
                    .or_else(|| ids.get_exact(&id_type.to_lowercase()))
                    .map_or(0, UserValue::hash_value)
            }
        };
        return hashing::hash_u64_slice(&[
            user_id_hash,
            unit_id_hash("stableID"),
            unit_id_type.map_or(0, unit_id_hash),
            ids.iter()
                .fold(0u64, |acc, (_, value)| acc.wrapping_add(value.hash_value())),
        ]);
    }
    let unit_id_hash = |id_type: &str| {
        if id_type.eq_ignore_ascii_case("userid") {
            user_id_hash
        } else {
            base.map_or(0, |base| base.get_unit_id_hash(id_type))
        }
    };
    hashing::hash_u64_slice(&[
        user_id_hash,
        unit_id_hash("stableID"),
        unit_id_type.map_or(0, unit_id_hash),
        base.map_or(0, FastUserData::sum_custom_id_hashes),
    ])
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::user::{
        statsig_user_internal::StatsigUserInternal, statsig_user_loggable::StatsigUserLoggable,
    };

    #[test]
    fn custom_ids_match_a_merged_user_for_lookup_hashing_callbacks_and_logging() {
        let base_ids: FastUserUnitIDMap = [
            ("stableID", "exact-base"),
            ("stableid", "lower-base"),
            ("companyID", "company-base"),
        ]
        .into_iter()
        .map(|(key, value)| (key.to_owned(), UserValue::from(value)))
        .collect();
        for overlay_ids in [
            FastUserUnitIDMap::default(),
            [("stableid", "lower-overlay"), ("newID", "new")]
                .into_iter()
                .map(|(key, value)| (key.to_owned(), UserValue::from(value)))
                .collect(),
            [
                ("stableID", "exact-overlay"),
                ("companyID", "company-overlay"),
                ("userID", "must-not-replace-primary"),
            ]
            .into_iter()
            .map(|(key, value)| (key.to_owned(), UserValue::from(value)))
            .collect(),
        ] {
            for context_ids in [None, Some(base_ids.clone())] {
                let base = Arc::new(FastUserData {
                    custom_ids: context_ids,
                    ..Default::default()
                });
                let mut expected = base.as_ref().clone();
                expected.user_id = Some(UserValue::from("random-primary"));
                expected
                    .custom_ids
                    .get_or_insert_with(Default::default)
                    .extend(overlay_ids.clone());
                let expected = FastStatsigUser::new(expected);
                let user = PreparedUser::with_input(
                    Some(base),
                    PreparedUserInput {
                        user_id: Some(UserValue::from("random-primary")),
                        custom_ids: Some(Arc::new(overlay_ids.clone())),
                        ..Default::default()
                    },
                );
                let owned = user.to_owned();
                for id_type in [
                    "userID",
                    "stableID",
                    "STABLEID",
                    "companyID",
                    "newID",
                    "missing",
                ] {
                    assert_eq!(
                        user.get_unit_id_by_name(id_type, &id_type.to_lowercase())
                            .and_then(UserValue::string_value),
                        expected
                            .get_unit_id_by_name(id_type, &id_type.to_lowercase())
                            .and_then(UserValue::string_value),
                    );
                    for unit in [None, Some(id_type)] {
                        let hash = expected.data.create_exposure_dedupe_user_hash(unit);
                        assert_eq!(user.create_exposure_dedupe_user_hash(unit), hash);
                        assert_eq!(owned.create_exposure_dedupe_user_hash(unit), hash);
                    }
                }
                let actual_internal = StatsigUserInternal::from_prepared_user(&user, None);
                let expected_internal = StatsigUserInternal::from_fast_user(&expected, None);
                let mut actual_pairs = actual_internal.custom_id_pairs();
                let mut expected_pairs = expected_internal.custom_id_pairs();
                actual_pairs.sort();
                expected_pairs.sort();
                assert_eq!(actual_pairs, expected_pairs);
                assert_eq!(
                    serde_json::to_value(user.to_public_user().data.as_ref()).unwrap(),
                    serde_json::to_value(expected.to_public_user().data.as_ref()).unwrap(),
                );
                let actual_log = StatsigUserLoggable::new_prepared(owned, None, None);
                let expected_log = StatsigUserLoggable::new_fast(&expected.data, None, None);
                drop(user);
                assert_eq!(
                    serde_json::to_value(actual_log).unwrap(),
                    serde_json::to_value(expected_log).unwrap()
                );
            }
        }
    }

    #[test]
    fn custom_id_snapshot_is_shared_during_promotion() {
        let ids = Arc::new(
            [("device".to_owned(), UserValue::from("one"))]
                .into_iter()
                .collect(),
        );
        let user = PreparedUser::with_input(
            None,
            PreparedUserInput {
                user_id: Some(UserValue::from("anonymous")),
                custom_ids: Some(Arc::clone(&ids)),
                ..Default::default()
            },
        );
        let owned = user.to_owned();
        let cloned = user.clone();
        assert!(Arc::ptr_eq(owned.input.custom_ids.as_ref().unwrap(), &ids));
        assert!(Arc::ptr_eq(cloned.input.custom_ids.as_ref().unwrap(), &ids));
        drop(user);
        assert_eq!(
            owned
                .custom_ids()
                .unwrap()
                .get("device", "device")
                .and_then(UserValue::string_value),
            Some("one")
        );
    }

    #[test]
    fn scalar_input_promotes_once_and_outlives_evaluation() {
        let user = PreparedUser::new(None, Some(UserValue::from("anon-one")), None);
        assert!(user.input.request.is_none());
        assert!(
            matches!(&user.input, PreparedUserInputStorage::Inline(_, shared) if shared.get().is_none())
        );
        let first = user.to_owned();
        let second = user.to_owned();
        assert!(Arc::ptr_eq(&first.input, &second.input));
        assert!(first.input.request.is_none());
        drop(user);
        assert_eq!(
            first
                .input
                .user_id
                .as_ref()
                .and_then(UserValue::string_value),
            Some("anon-one")
        );
    }

    #[test]
    fn custom_input_promotes_without_cloning_the_map() {
        let custom = [("key".to_owned(), UserValue::from("value"))]
            .into_iter()
            .collect();
        let user = PreparedUser::new(None, Some(UserValue::from("anon-two")), Some(custom));
        let PreparedUserInputStorage::Shared(input) = &user.input else {
            panic!("custom input must be shared")
        };
        let owned = user.to_owned();
        assert!(Arc::ptr_eq(input, &owned.input));
        assert!(owned.input.request.is_none());
    }

    #[test]
    fn empty_custom_remains_present_without_allocating_shared_input_before_promotion() {
        let user = PreparedUser::new(
            None,
            Some(UserValue::from("anon-empty-custom")),
            Some(FastUserCustomMap::default()),
        );
        assert!(
            matches!(&user.input, PreparedUserInputStorage::Inline(_, shared) if shared.get().is_none())
        );
        assert!(user.input.custom.as_ref().unwrap().is_empty());
        let first = user.to_owned();
        let second = user.to_owned();
        assert!(Arc::ptr_eq(&first.input, &second.input));
        drop(user);
        assert!(first.input.custom.as_ref().unwrap().is_empty());
    }

    #[test]
    fn request_snapshot_is_shared_across_promotion_and_retained_after_drop() {
        let base = Arc::new(FastUserData {
            country: Some(UserValue::from("US")),
            locale: Some(UserValue::from("en-US")),
            ..Default::default()
        });
        let request = Arc::new(PreparedRequestFields {
            country: Some(UserValue::from("")),
            ip: Some(UserValue::from("192.0.2.1")),
            ..Default::default()
        });
        let user = PreparedUser::with_input(
            Some(base),
            PreparedUserInput {
                user_id: Some(UserValue::from("anon-request")),
                request: Some(request.clone()),
                ..Default::default()
            },
        );
        let first = user.to_owned();
        let cloned = user.clone();
        let second = cloned.to_owned();
        assert!(Arc::ptr_eq(first.input.request.as_ref().unwrap(), &request));
        assert!(Arc::ptr_eq(
            first.input.request.as_ref().unwrap(),
            second.input.request.as_ref().unwrap()
        ));
        drop(user);
        drop(cloned);
        drop(request);
        assert_eq!(
            first
                .get_primary_value("country")
                .and_then(UserValue::string_value),
            Some("")
        );
        assert_eq!(
            first
                .get_primary_value("locale")
                .and_then(UserValue::string_value),
            Some("en-US")
        );
        assert_eq!(
            second
                .get_primary_value("ip")
                .and_then(UserValue::string_value),
            Some("192.0.2.1")
        );
    }
}

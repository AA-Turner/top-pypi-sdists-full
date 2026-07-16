use std::collections::HashMap;
use std::sync::atomic::{AtomicU64, Ordering};

use chrono::Utc;

use super::{
    fast_statsig_user::FastStatsigUser,
    user_data::UserDataMap,
    user_value::{UserValue, UserValueRef},
    StatsigUserLoggable,
};
use crate::evaluation::{dynamic_value::DynamicValue, evaluation_data::DynamicStringRef};
use crate::hashing::djb2_number;
use crate::{evaluation::dynamic_string::DynamicString, Statsig};
use crate::{log_w, statsig_metadata, StatsigUser};

pub type FullUserKey = (
    u64,      // app_version
    u64,      // country
    u64,      // email
    u64,      // ip
    u64,      // locale
    u64,      // user_agent
    u64,      // user_id
    Vec<u64>, // custom_ids
    Vec<u64>, // custom
    Vec<u64>, // private_attributes
    Vec<u64>, // statsig_env
);

const TAG: &str = stringify!(StatsigUserInternal);
const VERSION_CHECK_THROTTLE_MS: u64 = 60_000;

#[derive(Clone)]
pub struct StatsigUserInternal<'statsig, 'user> {
    pub(crate) user_ref: InternalUserRef<'user>,
    pub statsig_instance: Option<&'statsig Statsig>,
}

#[derive(Clone, Copy)]
pub(crate) enum InternalUserRef<'user> {
    Public(&'user StatsigUser),
    Fast(&'user FastStatsigUser),
}

static LAST_VERSION_CHECK: AtomicU64 = AtomicU64::new(0);

impl<'statsig, 'user> StatsigUserInternal<'statsig, 'user> {
    pub fn new(user: &'user StatsigUser, statsig_instance: Option<&'statsig Statsig>) -> Self {
        throttled_version_check(user.sdk_version);

        Self {
            user_ref: InternalUserRef::Public(user),
            statsig_instance,
        }
    }

    pub fn from_fast_user(
        user: &'user FastStatsigUser,
        statsig_instance: Option<&'statsig Statsig>,
    ) -> Self {
        throttled_version_check(user.sdk_version);

        Self {
            user_ref: InternalUserRef::Fast(user),
            statsig_instance,
        }
    }

    pub fn get_unit_id(&self, id_type: &DynamicString) -> Option<UserValueRef<'_>> {
        self.get_unit_id_ref(id_type.into())
    }

    pub(crate) fn get_unit_id_ref(
        &self,
        id_type: DynamicStringRef<'_>,
    ) -> Option<UserValueRef<'_>> {
        match self.user_ref {
            InternalUserRef::Public(user) => user
                .get_unit_id_by_name(id_type.value(), id_type.lowercased_value())
                .map(UserValueRef::Dynamic),
            InternalUserRef::Fast(user) => user
                .get_unit_id_by_name(id_type.value(), id_type.lowercased_value())
                .map(UserValueRef::User),
        }
    }

    pub fn get_user_value(&self, field: &Option<DynamicString>) -> Option<UserValueRef<'_>> {
        let field = field.as_ref()?;

        let lowered_field = &field.lowercased_value;

        if let Some(value) = self.get_primary_user_value(lowered_field) {
            if value.string_value().is_some_and(|value| !value.is_empty()) {
                return Some(value);
            }
        }

        if let Some(found) = self.get_custom_value(field.value.as_str()) {
            return Some(found);
        }
        if let Some(lowered_found) = self.get_custom_value(lowered_field.as_str()) {
            return Some(lowered_found);
        }

        if let Some(instance) = &self.statsig_instance {
            if let Some(val) = instance.get_value_from_global_custom_fields(&field.value) {
                return Some(UserValueRef::Dynamic(val));
            }

            if let Some(val) = instance.get_value_from_global_custom_fields(&field.lowercased_value)
            {
                return Some(UserValueRef::Dynamic(val));
            }
        }

        if let Some(found) = self.get_private_attribute_value(field.value.as_str()) {
            return Some(UserValueRef::Dynamic(found));
        }
        if let Some(lowered_found) = self.get_private_attribute_value(lowered_field.as_str()) {
            return Some(UserValueRef::Dynamic(lowered_found));
        }

        self.get_primary_user_value_alt(lowered_field)
    }

    pub fn get_value_from_environment(
        &self,
        field: &Option<DynamicString>,
    ) -> Option<DynamicValue> {
        let field = field.as_ref()?;

        if let Some(statsig_environment) = self.statsig_environment() {
            if let Some(result) = statsig_environment.get(field.value.as_str()) {
                return Some(result.clone());
            }
        }

        if let Some(result) = self.statsig_instance?.get_from_statsig_env(&field.value) {
            return Some(result);
        }

        self.statsig_instance?
            .get_from_statsig_env(&field.lowercased_value)
    }

    pub fn to_loggable(&self) -> StatsigUserLoggable {
        let mut environment = self.statsig_environment().cloned();
        let mut global_custom: Option<HashMap<String, DynamicValue>> = None;

        if let Some(statsig_instance) = &self.statsig_instance {
            if environment.is_none() {
                environment = statsig_instance.use_statsig_env(hashmap_to_user_data_map);
            }
            global_custom = statsig_instance.use_global_custom_fields(|gc| gc.cloned());
        }

        match self.user_ref {
            InternalUserRef::Public(user) => {
                StatsigUserLoggable::new(&user.data, environment, global_custom)
            }
            InternalUserRef::Fast(user) => {
                StatsigUserLoggable::new_fast(&user.data, environment, global_custom)
            }
        }
    }

    pub fn get_hashed_private_attributes(&self) -> Option<String> {
        let private_attributes = self.private_attributes()?;

        if private_attributes.is_empty() {
            return None;
        }

        let mut val: i64 = 0;
        for (key, value) in private_attributes {
            let hash_key = match value.string_value {
                Some(ref s) => key.to_owned() + ":" + &s.value,
                None => key.to_owned() + ":",
            };
            val += djb2_number(&hash_key);
            val &= 0xFFFF_FFFF;
        }
        Some(val.to_string())
    }

    pub(crate) fn create_exposure_dedupe_user_hash(&self, unit_id_type: Option<&str>) -> u64 {
        match self.user_ref {
            InternalUserRef::Public(user) => {
                user.data.create_exposure_dedupe_user_hash(unit_id_type)
            }
            InternalUserRef::Fast(user) => user.data.create_exposure_dedupe_user_hash(unit_id_type),
        }
    }

    pub(crate) fn get_persistent_storage_key(&self, id_type: &str) -> Option<String> {
        let dyn_str_id_type = DynamicString::from(id_type.to_string());
        self.get_unit_id(&dyn_str_id_type).map(|id| {
            let id_str = id.string_value().unwrap_or("");
            format!("{id_str}:{id_type}")
        })
    }

    pub(crate) fn get_user_id_str(&self) -> Option<&str> {
        match self.user_ref {
            InternalUserRef::Public(user) => user
                .data
                .user_id
                .as_ref()
                .and_then(|value| value.string_value.as_ref())
                .map(|value| value.value.as_str()),
            InternalUserRef::Fast(user) => {
                user.data.user_id.as_ref().and_then(UserValue::string_value)
            }
        }
    }

    pub(crate) fn custom_id_pairs(&self) -> Vec<(&str, &str)> {
        match self.user_ref {
            InternalUserRef::Public(user) => user
                .data
                .custom_ids
                .as_ref()
                .map(|custom_ids| {
                    custom_ids
                        .iter()
                        .map(|(key, value)| {
                            (
                                key.as_str(),
                                value
                                    .string_value
                                    .as_ref()
                                    .map(|value| value.value.as_str())
                                    .unwrap_or(""),
                            )
                        })
                        .collect()
                })
                .unwrap_or_default(),
            InternalUserRef::Fast(user) => user
                .data
                .custom_ids
                .as_ref()
                .map(|custom_ids| {
                    custom_ids
                        .iter()
                        .map(|(key, value)| (key.as_str(), value.string_value().unwrap_or("")))
                        .collect()
                })
                .unwrap_or_default(),
        }
    }

    pub(crate) fn with_public_user<R>(&self, f: impl FnOnce(&StatsigUser) -> R) -> R {
        match self.user_ref {
            InternalUserRef::Public(user) => f(user),
            InternalUserRef::Fast(user) => {
                let materialized = user.to_public_user();
                f(&materialized)
            }
        }
    }

    fn get_primary_user_value(&self, lowered_field: &str) -> Option<UserValueRef<'_>> {
        match self.user_ref {
            InternalUserRef::Public(user) => match lowered_field {
                "userid" => user.data.user_id.as_ref().map(UserValueRef::Dynamic),
                "email" => user.data.email.as_ref().map(UserValueRef::Dynamic),
                "ip" => user.data.ip.as_ref().map(UserValueRef::Dynamic),
                "country" => user.data.country.as_ref().map(UserValueRef::Dynamic),
                "locale" => user.data.locale.as_ref().map(UserValueRef::Dynamic),
                "appversion" => user.data.app_version.as_ref().map(UserValueRef::Dynamic),
                "useragent" => user.data.user_agent.as_ref().map(UserValueRef::Dynamic),
                _ => None,
            },
            InternalUserRef::Fast(user) => match lowered_field {
                "userid" => user.data.user_id.as_ref().map(UserValueRef::User),
                "email" => user.data.email.as_ref().map(UserValueRef::User),
                "ip" => user.data.ip.as_ref().map(UserValueRef::User),
                "country" => user.data.country.as_ref().map(UserValueRef::User),
                "locale" => user.data.locale.as_ref().map(UserValueRef::User),
                "appversion" => user.data.app_version.as_ref().map(UserValueRef::User),
                "useragent" => user.data.user_agent.as_ref().map(UserValueRef::User),
                _ => None,
            },
        }
    }

    fn get_primary_user_value_alt(&self, lowered_field: &str) -> Option<UserValueRef<'_>> {
        match lowered_field {
            "user_id" => self.get_primary_user_value("userid"),
            "app_version" => self.get_primary_user_value("appversion"),
            "user_agent" => self.get_primary_user_value("useragent"),
            _ => None,
        }
    }

    fn get_custom_value(&self, key: &str) -> Option<UserValueRef<'_>> {
        match self.user_ref {
            InternalUserRef::Public(user) => user
                .data
                .custom
                .as_ref()?
                .get(key)
                .map(UserValueRef::Dynamic),
            InternalUserRef::Fast(user) => {
                user.data.custom.as_ref()?.get(key).map(UserValueRef::User)
            }
        }
    }

    fn get_private_attribute_value(&self, key: &str) -> Option<&DynamicValue> {
        self.private_attributes()?.get(key)
    }

    fn private_attributes(&self) -> Option<&UserDataMap> {
        match self.user_ref {
            InternalUserRef::Public(user) => user.data.private_attributes.as_ref(),
            InternalUserRef::Fast(user) => user.data.private_attributes.as_ref(),
        }
    }

    fn statsig_environment(&self) -> Option<&UserDataMap> {
        match self.user_ref {
            InternalUserRef::Public(user) => user.data.statsig_environment.as_ref(),
            InternalUserRef::Fast(user) => user.data.statsig_environment.as_ref(),
        }
    }
}

fn hashmap_to_user_data_map(map: Option<&HashMap<String, DynamicValue>>) -> Option<UserDataMap> {
    map.map(|map| {
        map.iter()
            .map(|(key, value)| (key.clone(), value.clone()))
            .collect()
    })
}

fn throttled_version_check(user_sdk_version: &'static str) {
    let current_version = statsig_metadata::SDK_VERSION;

    // compare pointers (faster than string comparison)
    if user_sdk_version.as_ptr() == current_version.as_ptr() {
        return;
    }

    // compare the values
    if user_sdk_version == current_version {
        return;
    }

    let now = Utc::now().timestamp_millis() as u64;
    let last = LAST_VERSION_CHECK.load(Ordering::Relaxed);

    if now.saturating_sub(last) < VERSION_CHECK_THROTTLE_MS {
        return;
    }

    if LAST_VERSION_CHECK
        .compare_exchange(last, now, Ordering::Relaxed, Ordering::Relaxed)
        .is_ok()
    {
        log_w!(
            TAG,
            "Multiple SDK versions detected. This may cause unexpected behavior. Expected: {}, Got: {}",
            statsig_metadata::SDK_VERSION,
            user_sdk_version
        );
    }
}

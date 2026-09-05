use crate::statsig_metadata;
use crate::{evaluation::dynamic_value::DynamicValue, hashing};
use serde::{Deserialize, Serialize};
use serde_with::skip_serializing_none;
use std::{collections::HashMap, sync::Arc};

use super::{
    into_optional::IntoOptional,
    unit_id::UnitID,
    user_data::{UserData, UserDataMap, UserDataMapOf},
    user_value::{UserValue, UserValueMap},
};

pub type FastUserCustomMap = UserValueMap;
pub type FastUserUnitIDMap = UserDataMapOf<UserValue>;

#[skip_serializing_none]
#[derive(Clone, Deserialize, Serialize, Default)]
#[serde(rename_all = "camelCase")]
pub struct FastUserData {
    #[serde(rename = "userID")]
    pub user_id: Option<UserValue>,
    #[serde(rename = "customIDs")]
    pub custom_ids: Option<FastUserUnitIDMap>,

    pub email: Option<UserValue>,
    pub ip: Option<UserValue>,
    pub user_agent: Option<UserValue>,
    pub country: Option<UserValue>,
    pub locale: Option<UserValue>,
    pub app_version: Option<UserValue>,
    pub statsig_environment: Option<UserDataMap>,

    #[serde(skip_serializing)]
    pub private_attributes: Option<UserDataMap>,
    pub custom: Option<FastUserCustomMap>,
}

impl FastUserData {
    pub(crate) fn create_exposure_dedupe_user_hash(&self, unit_id_type: Option<&str>) -> u64 {
        let user_id_hash = self.user_id.as_ref().map_or(0, UserValue::hash_value);
        let stable_id_hash = self.get_unit_id_hash("stableID");
        let unit_type_hash = unit_id_type.map_or(0, |id_type| self.get_unit_id_hash(id_type));
        let custom_ids_hash_sum = self.sum_custom_id_hashes();

        hashing::hash_u64_slice(&[
            user_id_hash,
            stable_id_hash,
            unit_type_hash,
            custom_ids_hash_sum,
        ])
    }

    pub(crate) fn sum_custom_id_hashes(&self) -> u64 {
        self.custom_ids.as_ref().map_or(0, |custom_ids| {
            custom_ids
                .values()
                .fold(0u64, |acc, value| acc.wrapping_add(value.hash_value()))
        })
    }

    pub(crate) fn get_unit_id_hash(&self, id_type: &str) -> u64 {
        if id_type.eq_ignore_ascii_case("userid") {
            return self.user_id.as_ref().map_or(0, UserValue::hash_value);
        }

        if let Some(custom_ids) = &self.custom_ids {
            if let Some(id) = custom_ids.get(id_type) {
                return id.hash_value();
            }

            if let Some(id) = custom_ids.get(&id_type.to_lowercase()) {
                return id.hash_value();
            }
        }

        0
    }

    pub(crate) fn to_bytes(&self) -> Option<Vec<u8>> {
        serde_json::to_vec(self).ok()
    }
}

#[derive(Clone)]
pub struct FastStatsigUser {
    pub data: Arc<FastUserData>,
    pub(crate) sdk_version: &'static str,
}

impl FastStatsigUser {
    pub fn new(inner: FastUserData) -> Self {
        Self {
            data: Arc::new(inner),
            sdk_version: statsig_metadata::SDK_VERSION,
        }
    }

    pub fn get_user_id(&self) -> Option<&str> {
        self.data.user_id.as_ref().and_then(UserValue::string_value)
    }

    pub fn set_user_id(&mut self, user_id: impl Into<UnitID>) {
        let unit_id = user_id.into();
        let mut_data = Arc::make_mut(&mut self.data);
        mut_data.user_id = Some(UserValue::from(unit_id));
    }

    pub fn get_custom_ids(&self) -> Option<HashMap<&str, &str>> {
        let mapped = self
            .data
            .custom_ids
            .as_ref()?
            .iter()
            .map(|(key, value)| (key.as_str(), value.string_value().unwrap_or("")))
            .collect();

        Some(mapped)
    }

    pub fn set_custom_ids<K, U>(&mut self, custom_ids: HashMap<K, U>)
    where
        K: Into<String>,
        U: Into<UnitID>,
    {
        let custom_ids = custom_ids
            .into_iter()
            .map(|(key, value)| (key.into(), UserValue::from(value.into())))
            .collect();

        let mut_data = Arc::make_mut(&mut self.data);
        mut_data.custom_ids = Some(custom_ids);
    }

    pub(crate) fn get_unit_id_by_name(
        &self,
        id_type: &str,
        lowercased_id_type: &str,
    ) -> Option<&UserValue> {
        if lowercased_id_type == "userid" {
            return self.data.user_id.as_ref();
        }

        let custom_ids = self.data.custom_ids.as_ref()?;

        if let Some(custom_id) = custom_ids.get(id_type) {
            return Some(custom_id);
        }

        custom_ids.get(lowercased_id_type)
    }

    pub fn get_statsig_environment(&self) -> Option<HashMap<&str, &str>> {
        let mapped = self
            .data
            .statsig_environment
            .as_ref()?
            .iter()
            .map(dynamic_entry_to_key_value_refs)
            .collect();

        Some(mapped)
    }

    pub fn set_statsig_environment<K, U>(&mut self, statsig_environment: Option<HashMap<K, U>>)
    where
        K: Into<String>,
        U: Into<String>,
    {
        let mut_data = Arc::make_mut(&mut self.data);
        let statsig_environment = match statsig_environment {
            Some(value) => value,
            None => {
                mut_data.statsig_environment = None;
                return;
            }
        };

        let statsig_environment: UserDataMap = statsig_environment
            .into_iter()
            .map(|(key, value)| (key.into(), value.into().into()))
            .collect();

        mut_data.statsig_environment = Some(statsig_environment);
    }

    pub fn get_custom(&self) -> Option<&FastUserCustomMap> {
        self.data.custom.as_ref()
    }

    pub fn set_custom<K, V>(&mut self, value: impl IntoOptional<HashMap<K, V>>)
    where
        K: Into<String>,
        V: Into<UserValue>,
    {
        let mut_data = Arc::make_mut(&mut self.data);
        let value = match value.into_optional() {
            Some(value) => value,
            None => {
                mut_data.custom = None;
                return;
            }
        };

        mut_data.custom = Some(
            value
                .into_iter()
                .map(|(key, value)| (key.into(), value.into()))
                .collect(),
        );
    }

    pub fn get_private_attributes(&self) -> Option<&UserDataMap> {
        self.data.private_attributes.as_ref()
    }

    pub fn set_private_attributes<K, V>(&mut self, value: impl IntoOptional<HashMap<K, V>>)
    where
        K: Into<String>,
        V: Into<DynamicValue>,
    {
        let mut_data = Arc::make_mut(&mut self.data);
        let value = match value.into_optional() {
            Some(value) => value,
            None => {
                mut_data.private_attributes = None;
                return;
            }
        };

        mut_data.private_attributes = Some(
            value
                .into_iter()
                .map(|(key, value)| (key.into(), value.into()))
                .collect(),
        );
    }

    pub fn to_public_user(&self) -> crate::StatsigUser {
        crate::StatsigUser::new(self.to_public_user_data())
    }

    pub(crate) fn to_public_user_data(&self) -> UserData {
        UserData {
            user_id: self.data.user_id.as_ref().map(user_value_to_dynamic_value),
            custom_ids: self
                .data
                .custom_ids
                .as_ref()
                .map(user_value_map_to_dynamic_value_map),
            email: self.data.email.as_ref().map(user_value_to_dynamic_value),
            ip: self.data.ip.as_ref().map(user_value_to_dynamic_value),
            user_agent: self
                .data
                .user_agent
                .as_ref()
                .map(user_value_to_dynamic_value),
            country: self.data.country.as_ref().map(user_value_to_dynamic_value),
            locale: self.data.locale.as_ref().map(user_value_to_dynamic_value),
            app_version: self
                .data
                .app_version
                .as_ref()
                .map(user_value_to_dynamic_value),
            statsig_environment: self.data.statsig_environment.clone(),
            private_attributes: self.data.private_attributes.clone(),
            custom: self.data.custom.as_ref().map(|values| {
                values
                    .iter()
                    .map(|(key, value)| (key.clone(), user_value_to_dynamic_value(value)))
                    .collect()
            }),
        }
    }
}

macro_rules! string_field_accessor {
    ($getter_name:ident, $setter_name:ident, $field:ident) => {
        pub fn $getter_name(&self) -> Option<&str> {
            self.data.$field.as_ref().and_then(UserValue::string_value)
        }

        pub fn $setter_name(&mut self, value: impl IntoOptional<String>) {
            let value = value.into_optional();
            let mut_data = Arc::make_mut(&mut self.data);
            match value {
                Some(value) => {
                    mut_data.$field = Some(UserValue::from(value));
                }
                None => mut_data.$field = None,
            }
        }
    };
}

impl FastStatsigUser {
    string_field_accessor!(get_email, set_email, email);
    string_field_accessor!(get_ip, set_ip, ip);
    string_field_accessor!(get_user_agent, set_user_agent, user_agent);
    string_field_accessor!(get_country, set_country, country);
    string_field_accessor!(get_locale, set_locale, locale);
    string_field_accessor!(get_app_version, set_app_version, app_version);
}

impl FastStatsigUser {
    pub fn to_bytes(&self) -> Option<Vec<u8>> {
        self.data.to_bytes()
    }
}

fn dynamic_entry_to_key_value_refs<'a>(
    entry: (&'a String, &'a DynamicValue),
) -> (&'a str, &'a str) {
    let (key, value) = entry;

    (
        key.as_str(),
        value
            .string_value
            .as_ref()
            .map(|value| value.value.as_str())
            .unwrap_or(""),
    )
}

fn user_value_to_dynamic_value(value: &UserValue) -> DynamicValue {
    DynamicValue::from_json_value(value)
}

fn user_value_map_to_dynamic_value_map(values: &UserDataMapOf<UserValue>) -> UserDataMap {
    values
        .iter()
        .map(|(key, value)| (key.clone(), user_value_to_dynamic_value(value)))
        .collect()
}

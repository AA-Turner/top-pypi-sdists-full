use super::{
    fast_statsig_user::{FastUserCustomMap, FastUserData},
    user_data::{UserData, UserDataMap},
};
use crate::{DynamicValue, StatsigUser};
use serde::{
    ser::{SerializeMap, SerializeStruct},
    Deserialize, Serialize,
};
use serde_json::Value;
use std::{collections::HashMap, sync::Arc};

const TAG: &str = "StatsigUserLoggable";

#[derive(Clone)]
pub enum StatsigUserLoggableData {
    Public(Arc<UserData>),
    Fast(Arc<FastUserData>),
}

impl Default for StatsigUserLoggableData {
    fn default() -> Self {
        Self::Public(Arc::new(UserData::default()))
    }
}

#[derive(Clone, Default)]
pub struct StatsigUserLoggable {
    pub data: StatsigUserLoggableData,
    pub environment: Option<UserDataMap>,
    pub global_custom: Option<HashMap<String, DynamicValue>>,
}

impl StatsigUserLoggable {
    pub fn new(
        user_inner: &Arc<UserData>,
        environment: Option<UserDataMap>,
        global_custom: Option<HashMap<String, DynamicValue>>,
    ) -> Self {
        Self {
            data: StatsigUserLoggableData::Public(user_inner.clone()),
            environment,
            global_custom,
        }
    }

    pub fn null() -> Self {
        Self::default()
    }

    pub(crate) fn new_fast(
        user_inner: &Arc<FastUserData>,
        environment: Option<UserDataMap>,
        global_custom: Option<HashMap<String, DynamicValue>>,
    ) -> Self {
        Self {
            data: StatsigUserLoggableData::Fast(user_inner.clone()),
            environment,
            global_custom,
        }
    }

    pub(crate) fn create_exposure_dedupe_user_hash(&self, unit_id_type: Option<&str>) -> u64 {
        match &self.data {
            StatsigUserLoggableData::Public(data) => {
                data.create_exposure_dedupe_user_hash(unit_id_type)
            }
            StatsigUserLoggableData::Fast(data) => {
                data.create_exposure_dedupe_user_hash(unit_id_type)
            }
        }
    }

    pub fn default_console_capture_user(
        environment: Option<UserDataMap>,
        global_custom: Option<HashMap<String, DynamicValue>>,
    ) -> Self {
        Self::new(
            &StatsigUser::with_user_id("console-capture-user").data,
            environment,
            global_custom,
        )
    }
}

// ----------------------------------------------------- [Serialization]

impl Serialize for StatsigUserLoggable {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        let mut state = serializer.serialize_struct(TAG, 10)?;

        match &self.data {
            StatsigUserLoggableData::Public(data) => {
                serialize_public_user_data(&mut state, data, &self.global_custom)?;
            }
            StatsigUserLoggableData::Fast(data) => {
                serialize_fast_user_data(&mut state, data, &self.global_custom)?;
            }
        }

        serialize_data_field(&mut state, "statsigEnvironment", &self.environment)?;

        // DO NOT SERIALIZE "privateAttributes"

        state.end()
    }
}

impl<'de> Deserialize<'de> for StatsigUserLoggable {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: serde::Deserializer<'de>,
    {
        let mut value = Value::deserialize(deserializer)?;
        let env = value["statsigEnvironment"].take();
        let data = serde_json::from_value::<UserData>(value).map_err(|e| {
            serde::de::Error::custom(format!("Error deserializing StatsigUserInner: {e}"))
        })?;

        let environment = serde_json::from_value::<Option<UserDataMap>>(env).map_err(|e| {
            serde::de::Error::custom(format!("Error deserializing StatsigUserInner: {e}"))
        })?;

        Ok(StatsigUserLoggable {
            data: StatsigUserLoggableData::Public(Arc::new(data)),
            environment,
            global_custom: None, // there is no way to discern between user-defined and global custom fields
        })
    }
}

fn serialize_data_field<S, T>(
    state: &mut S,
    field: &'static str,
    value: &Option<T>,
) -> Result<(), S::Error>
where
    S: SerializeStruct,
    T: Serialize,
{
    if let Some(value) = value {
        state.serialize_field(field, value)?;
    }
    Ok(())
}

fn serialize_custom_field<S>(
    state: &mut S,
    custom: &Option<UserDataMap>,
    global_custom: &Option<HashMap<String, DynamicValue>>,
) -> Result<(), S::Error>
where
    S: SerializeStruct,
{
    if global_custom.is_none() && custom.is_none() {
        return Ok(());
    }

    state.serialize_field(
        "custom",
        &MergedCustomFields {
            custom: custom.as_ref(),
            global_custom: global_custom.as_ref(),
        },
    )
}

fn serialize_public_user_data<S>(
    state: &mut S,
    data: &UserData,
    global_custom: &Option<HashMap<String, DynamicValue>>,
) -> Result<(), S::Error>
where
    S: SerializeStruct,
{
    serialize_data_field(state, "userID", &data.user_id)?;
    serialize_data_field(state, "customIDs", &data.custom_ids)?;
    serialize_data_field(state, "email", &data.email)?;
    serialize_data_field(state, "ip", &data.ip)?;
    serialize_data_field(state, "userAgent", &data.user_agent)?;
    serialize_data_field(state, "country", &data.country)?;
    serialize_data_field(state, "locale", &data.locale)?;
    serialize_data_field(state, "appVersion", &data.app_version)?;
    serialize_custom_field(state, &data.custom, global_custom)
}

fn serialize_fast_user_data<S>(
    state: &mut S,
    data: &FastUserData,
    global_custom: &Option<HashMap<String, DynamicValue>>,
) -> Result<(), S::Error>
where
    S: SerializeStruct,
{
    serialize_data_field(state, "userID", &data.user_id)?;
    serialize_data_field(state, "customIDs", &data.custom_ids)?;
    serialize_data_field(state, "email", &data.email)?;
    serialize_data_field(state, "ip", &data.ip)?;
    serialize_data_field(state, "userAgent", &data.user_agent)?;
    serialize_data_field(state, "country", &data.country)?;
    serialize_data_field(state, "locale", &data.locale)?;
    serialize_data_field(state, "appVersion", &data.app_version)?;
    serialize_fast_custom_field(state, &data.custom, global_custom)
}

fn serialize_fast_custom_field<S>(
    state: &mut S,
    custom: &Option<FastUserCustomMap>,
    global_custom: &Option<HashMap<String, DynamicValue>>,
) -> Result<(), S::Error>
where
    S: SerializeStruct,
{
    if global_custom.is_none() && custom.is_none() {
        return Ok(());
    }

    state.serialize_field(
        "custom",
        &MergedFastCustomFields {
            custom: custom.as_ref(),
            global_custom: global_custom.as_ref(),
        },
    )
}

struct MergedCustomFields<'a> {
    custom: Option<&'a UserDataMap>,
    global_custom: Option<&'a HashMap<String, DynamicValue>>,
}

struct MergedFastCustomFields<'a> {
    custom: Option<&'a FastUserCustomMap>,
    global_custom: Option<&'a HashMap<String, DynamicValue>>,
}

impl MergedCustomFields<'_> {
    fn serialized_len(&self) -> usize {
        let global_len = self.global_custom.map_or(0, HashMap::len);
        let custom_only_len = self.custom.map_or(0, |custom| {
            custom
                .keys()
                .filter(|key| {
                    !self
                        .global_custom
                        .is_some_and(|global_custom| global_custom.contains_key(*key))
                })
                .count()
        });

        global_len + custom_only_len
    }
}

impl Serialize for MergedCustomFields<'_> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        let mut map = serializer.serialize_map(Some(self.serialized_len()))?;

        if let Some(global_custom) = self.global_custom {
            for (key, global_value) in global_custom {
                let value = self
                    .custom
                    .and_then(|custom| custom.get(key))
                    .unwrap_or(global_value);
                map.serialize_entry(key, value)?;
            }
        }

        if let Some(custom) = self.custom {
            for (key, value) in custom {
                if self
                    .global_custom
                    .is_some_and(|global_custom| global_custom.contains_key(key))
                {
                    continue;
                }

                map.serialize_entry(key, value)?;
            }
        }

        map.end()
    }
}

impl MergedFastCustomFields<'_> {
    fn serialized_len(&self) -> usize {
        let global_len = self.global_custom.map_or(0, HashMap::len);
        let custom_only_len = self.custom.map_or(0, |custom| {
            custom
                .keys()
                .filter(|key| {
                    !self
                        .global_custom
                        .is_some_and(|global_custom| global_custom.contains_key(*key))
                })
                .count()
        });

        global_len + custom_only_len
    }
}

impl Serialize for MergedFastCustomFields<'_> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        let mut map = serializer.serialize_map(Some(self.serialized_len()))?;

        if let Some(global_custom) = self.global_custom {
            for (key, global_value) in global_custom {
                if let Some(value) = self.custom.and_then(|custom| custom.get(key)) {
                    map.serialize_entry(key, value)?;
                } else {
                    map.serialize_entry(key, global_value)?;
                }
            }
        }

        if let Some(custom) = self.custom {
            for (key, value) in custom {
                if self
                    .global_custom
                    .is_some_and(|global_custom| global_custom.contains_key(key))
                {
                    continue;
                }

                map.serialize_entry(key, value)?;
            }
        }

        map.end()
    }
}

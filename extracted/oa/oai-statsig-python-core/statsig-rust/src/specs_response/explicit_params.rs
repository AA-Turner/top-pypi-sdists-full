use std::sync::Arc;

use serde::{Deserialize, Deserializer, Serialize, Serializer};

use crate::interned_string::InternedString;

#[derive(Clone, PartialEq, Debug, Default)]
pub struct ExplicitParameters {
    inner: Arc<Vec<InternedString>>,
}

impl ExplicitParameters {
    pub(crate) fn from_interned(parameters: Vec<InternedString>) -> Self {
        Self {
            inner: Arc::new(parameters),
        }
    }

    pub fn from_vec(parameters: Vec<String>) -> Self {
        Self::from_interned(
            parameters
                .into_iter()
                .map(InternedString::from_string)
                .collect(),
        )
    }

    pub fn contains(&self, parameter: &str) -> bool {
        self.inner.iter().any(|p| p.as_str() == parameter)
    }

    pub fn unperformant_to_vec(&self) -> Vec<String> {
        self.inner
            .iter()
            .map(|p| p.unperformant_to_string())
            .collect()
    }

    pub fn to_vec_interned(&self) -> Vec<&InternedString> {
        self.inner.as_ref().iter().collect()
    }

    pub fn as_slice(&self) -> &[InternedString] {
        self.inner.as_ref()
    }
}

impl<'de> Deserialize<'de> for ExplicitParameters {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let parameters = Vec::<InternedString>::deserialize(deserializer)?;
        Ok(ExplicitParameters {
            inner: Arc::new(parameters),
        })
    }
}

impl Serialize for ExplicitParameters {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        self.inner.serialize(serializer)
    }
}

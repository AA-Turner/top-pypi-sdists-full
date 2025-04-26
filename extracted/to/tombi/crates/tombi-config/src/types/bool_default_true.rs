#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "jsonschema", derive(schemars::JsonSchema))]
#[cfg_attr(feature = "jsonschema", schemars(extend("default" = true)))]
pub struct BoolDefaultTrue(pub bool);

impl BoolDefaultTrue {
    #[inline]
    pub fn value(&self) -> bool {
        self.0
    }
}

impl Default for BoolDefaultTrue {
    fn default() -> Self {
        Self(true)
    }
}

impl From<bool> for BoolDefaultTrue {
    fn from(value: bool) -> Self {
        Self(value)
    }
}

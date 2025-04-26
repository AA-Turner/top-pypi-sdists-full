#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "jsonschema", derive(schemars::JsonSchema))]
pub struct IndentWidth(u8);

impl IndentWidth {
    #[inline]
    pub fn value(&self) -> u8 {
        self.0
    }
}

impl Default for IndentWidth {
    fn default() -> Self {
        Self(2)
    }
}

impl From<u8> for IndentWidth {
    fn from(value: u8) -> Self {
        Self(value)
    }
}

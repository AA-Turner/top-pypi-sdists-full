use std::borrow::Cow;

use crate::error::JsonToolsError;

/// Input type for JSON flattening operations with Cow optimization
#[derive(Debug, Clone)]
#[repr(u8)] // OPTIMIZATION: Smaller discriminant for better cache locality
pub enum JsonInput<'a> {
    /// Single JSON string with Cow for efficient memory usage
    Single(Cow<'a, str>),
    /// Multiple JSON strings (borrowing)
    Multiple(&'a [&'a str]),
    /// Multiple JSON strings (owned)
    MultipleOwned(Vec<Cow<'a, str>>),
}

impl<'a> From<&'a str> for JsonInput<'a> {
    fn from(json: &'a str) -> Self {
        JsonInput::Single(Cow::Borrowed(json))
    }
}

impl<'a> From<&'a String> for JsonInput<'a> {
    fn from(json: &'a String) -> Self {
        JsonInput::Single(Cow::Borrowed(json.as_str()))
    }
}

impl<'a> From<&'a [&'a str]> for JsonInput<'a> {
    fn from(json_list: &'a [&'a str]) -> Self {
        JsonInput::Multiple(json_list)
    }
}

impl<'a> From<Vec<&'a str>> for JsonInput<'a> {
    fn from(json_list: Vec<&'a str>) -> Self {
        JsonInput::MultipleOwned(json_list.into_iter().map(Cow::Borrowed).collect())
    }
}

impl<'a> From<Vec<String>> for JsonInput<'a> {
    fn from(json_list: Vec<String>) -> Self {
        JsonInput::MultipleOwned(json_list.into_iter().map(Cow::Owned).collect())
    }
}

impl<'a> From<&'a [String]> for JsonInput<'a> {
    fn from(json_list: &'a [String]) -> Self {
        JsonInput::MultipleOwned(
            json_list
                .iter()
                .map(|s| Cow::Borrowed(s.as_str()))
                .collect(),
        )
    }
}

/// Output type for JSON flattening operations
#[derive(Debug, Clone)]
#[repr(u8)] // OPTIMIZATION: Smaller discriminant for better cache locality
pub enum JsonOutput {
    /// Single flattened JSON string
    Single(String),
    /// Multiple flattened JSON strings
    Multiple(Vec<String>),
}

impl JsonOutput {
    /// Extract single result, panicking if multiple results.
    ///
    /// # Panics
    /// Panics if this is a `Multiple` variant. Use [`try_into_single`](Self::try_into_single)
    /// for a non-panicking alternative.
    #[must_use]
    #[deprecated(
        since = "0.10.0",
        note = "Use try_into_single() instead to avoid panics"
    )]
    pub fn into_single(self) -> String {
        match self {
            JsonOutput::Single(result) => result,
            JsonOutput::Multiple(_) => panic!("Expected single result but got multiple"),
        }
    }

    /// Extract multiple results, panicking if single result.
    ///
    /// # Panics
    /// Panics if this is a `Single` variant. Use [`try_into_multiple`](Self::try_into_multiple)
    /// for a non-panicking alternative.
    #[must_use]
    #[deprecated(
        since = "0.10.0",
        note = "Use try_into_multiple() instead to avoid panics"
    )]
    pub fn into_multiple(self) -> Vec<String> {
        match self {
            JsonOutput::Single(_) => panic!("Expected multiple results but got single"),
            JsonOutput::Multiple(results) => results,
        }
    }

    /// Try to extract single result, returning an error if multiple results.
    pub fn try_into_single(self) -> Result<String, JsonToolsError> {
        match self {
            JsonOutput::Single(result) => Ok(result),
            JsonOutput::Multiple(_) => Err(JsonToolsError::input_validation_error(
                "Expected single result but got multiple",
            )),
        }
    }

    /// Try to extract multiple results, returning an error if single result.
    pub fn try_into_multiple(self) -> Result<Vec<String>, JsonToolsError> {
        match self {
            JsonOutput::Single(_) => Err(JsonToolsError::input_validation_error(
                "Expected multiple results but got single",
            )),
            JsonOutput::Multiple(results) => Ok(results),
        }
    }

    /// Get results as vector (single result becomes vec with one element)
    #[must_use]
    pub fn into_vec(self) -> Vec<String> {
        match self {
            JsonOutput::Single(result) => vec![result],
            JsonOutput::Multiple(results) => results,
        }
    }
}

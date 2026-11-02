use thiserror::Error;

#[derive(Debug, Error)]
pub enum ConversionError {
    #[error("invalid input: {0}")]
    InvalidInput(String),
    #[error("unsupported conversion: {0}")]
    UnsupportedConversion(String),
    #[error("serde error: {0}")]
    Serde(#[from] serde_json::Error),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum WarningAction {
    /// Field/value was removed entirely — information lost.
    Dropped,
    /// Field value was altered to fit the target — information preserved but approximate.
    Changed,
    /// A value was created that didn't exist in the source — information invented.
    Added,
}

#[derive(Debug, Clone, serde::Serialize)]
pub struct ConversionWarning {
    pub field: String,
    pub action: WarningAction,
    pub message: String,
}

#[derive(Debug)]
pub struct ConversionResult<T> {
    pub value: T,
    pub warnings: Vec<ConversionWarning>,
}

impl<T> ConversionResult<T> {
    pub fn new(value: T) -> Self {
        Self {
            value,
            warnings: Vec::new(),
        }
    }

    pub fn with_warnings(value: T, warnings: Vec<ConversionWarning>) -> Self {
        Self { value, warnings }
    }

    pub fn warn(
        &mut self,
        field: impl Into<String>,
        action: WarningAction,
        message: impl Into<String>,
    ) {
        self.warnings.push(ConversionWarning {
            field: field.into(),
            action,
            message: message.into(),
        });
    }

    /// Emit a "not supported in {target}" warning with action [`WarningAction::Dropped`]
    /// for each present field.
    ///
    /// ```ignore
    /// result.warn_unsupported("Anthropic", &[
    ///     ("presence_penalty", source.presence_penalty.is_some()),
    ///     ("store",            source.store.is_some()),
    /// ]);
    /// ```
    pub fn warn_unsupported(&mut self, target: &str, fields: &[(&str, bool)]) {
        for &(field, present) in fields {
            if present {
                self.warn(
                    field,
                    WarningAction::Dropped,
                    format!("not supported in {target}"),
                );
            }
        }
    }
}

use tombi_x_keyword::{ArrayValuesOrder, TableKeysOrder};

use super::default_value::DefaultValue;

#[derive(Debug, Clone, Default)]
pub struct DataConstraints {
    // Common
    pub enumerate: Option<Vec<DefaultValue>>,
    pub default: Option<DefaultValue>,

    // Integer OR Float
    pub minimum: Option<DefaultValue>,
    pub maximum: Option<DefaultValue>,
    pub exclusive_minimum: Option<DefaultValue>,
    pub exclusive_maximum: Option<DefaultValue>,
    pub multiple_of: Option<DefaultValue>,
    // String
    pub min_length: Option<usize>,
    pub max_length: Option<usize>,
    pub pattern: Option<String>,

    // Array
    pub min_items: Option<usize>,
    pub max_items: Option<usize>,
    pub unique_items: Option<bool>,
    pub values_order: Option<ArrayValuesOrder>,

    // Table
    pub required_keys: Option<Vec<String>>,
    pub min_keys: Option<usize>,
    pub max_keys: Option<usize>,
    pub key_patterns: Option<Vec<String>>,
    pub additional_keys: Option<bool>,
    pub keys_order: Option<TableKeysOrder>,
}

impl std::fmt::Display for DataConstraints {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if let Some(enumerate) = &self.enumerate {
            write!(f, "Enumerated Values:\n\n")?;
            for value in enumerate {
                write!(f, "- `{}`\n\n", value)?;
            }
            writeln!(f)?;
        }

        if let Some(default) = &self.default {
            write!(f, "Default: `{}`\n\n", default)?;
        }

        if let Some(minimum) = &self.minimum {
            write!(f, "Minimum: `{}`\n\n", minimum)?;
        }

        if let Some(exclusive_minimum) = &self.exclusive_minimum {
            write!(f, "Exclusive Minimum: `{}`\n\n", exclusive_minimum)?;
        }

        if let Some(maximum) = &self.maximum {
            write!(f, "Maximum: `{}`\n\n", maximum)?;
        }

        if let Some(exclusive_maximum) = &self.exclusive_maximum {
            write!(f, "Exclusive Maximum: `{}`\n\n", exclusive_maximum)?;
        }

        if let Some(multiple_of) = &self.multiple_of {
            write!(f, "Multiple of: `{}`\n\n", multiple_of)?;
        }

        if let Some(min_length) = self.min_length {
            write!(f, "Minimum Length: `{}`\n\n", min_length)?;
        }

        if let Some(max_length) = self.max_length {
            write!(f, "Maximum Length: `{}`\n\n", max_length)?;
        }

        if let Some(pattern) = &self.pattern {
            write!(f, "Pattern: `{}`\n\n", pattern)?;
        }

        if let Some(min_items) = self.min_items {
            write!(f, "Minimum Items: `{}`\n\n", min_items)?;
        }

        if let Some(max_items) = self.max_items {
            write!(f, "Maximum Items: `{}`\n\n", max_items)?;
        }

        if self.unique_items.unwrap_or(false) {
            write!(f, "Unique Items: `true`\n\n")?;
        }

        if let Some(values_order) = &self.values_order {
            write!(f, "Values Order: `{}`\n\n", values_order)?;
        }

        if let Some(required_keys) = &self.required_keys {
            write!(f, "Required Keys:\n\n")?;
            for key in required_keys.iter() {
                write!(f, "- `{}`\n\n", key)?;
            }
        }

        if let Some(min_keys) = self.min_keys {
            write!(f, "Minimum Keys: `{}`\n\n", min_keys)?;
        }

        if let Some(max_keys) = self.max_keys {
            write!(f, "Maximum Keys: `{}`\n\n", max_keys)?;
        }

        if let Some(key_patterns) = &self.key_patterns {
            write!(f, "Key Patterns:\n\n")?;
            for pattern_property in key_patterns.iter() {
                write!(f, "- `{}`\n\n", pattern_property)?;
            }
        }

        if self.additional_keys.unwrap_or(false) {
            write!(f, "Additional Keys: `true`\n\n")?;
        }

        if let Some(keys_order) = &self.keys_order {
            write!(f, "Keys Order: `{}`\n\n", keys_order)?;
        }

        Ok(())
    }
}

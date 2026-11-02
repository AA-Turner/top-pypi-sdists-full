use std::fmt;

use crate::error::{ConversionWarning, WarningAction};

pub(crate) struct ConversionCtx<C = ()> {
    pub config: C,
    warnings: Vec<ConversionWarning>,
    path: Vec<String>,
}

impl<C: Default> ConversionCtx<C> {
    pub fn new() -> Self {
        Self {
            config: C::default(),
            warnings: Vec::new(),
            path: Vec::new(),
        }
    }
}

impl<C> ConversionCtx<C> {
    pub fn with_config(config: C) -> Self {
        Self {
            config,
            warnings: Vec::new(),
            path: Vec::new(),
        }
    }

    pub fn push(&mut self, segment: impl fmt::Display) {
        self.path.push(segment.to_string());
    }

    pub fn pop(&mut self) {
        self.path.pop();
    }

    fn current_path(&self) -> String {
        self.path.join(".")
    }

    /// Emit a warning with `field` appended to the current path.
    /// e.g. path=["input[2]"] + field="image" -> "input[2].image"
    pub fn warn(&mut self, field: &str, action: WarningAction, message: impl Into<String>) {
        let full = if self.path.is_empty() {
            field.to_string()
        } else {
            format!("{}.{field}", self.current_path())
        };
        self.warnings.push(ConversionWarning {
            field: full,
            action,
            message: message.into(),
        });
    }

    pub fn into_warnings(self) -> Vec<ConversionWarning> {
        self.warnings
    }

    pub fn take_warnings(&mut self) -> Vec<ConversionWarning> {
        std::mem::take(&mut self.warnings)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn warn_with_empty_path() {
        let mut ctx = ConversionCtx::<()>::new();
        ctx.warn("top_level", WarningAction::Dropped, "some message");
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "top_level");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
    }

    #[test]
    fn warn_with_nested_path() {
        let mut ctx = ConversionCtx::<()>::new();
        ctx.push("input[2]");
        ctx.push("content[0]");
        ctx.warn("image", WarningAction::Dropped, "malformed");
        ctx.pop();
        ctx.pop();
        let warnings = ctx.into_warnings();
        assert_eq!(warnings[0].field, "input[2].content[0].image");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
    }

    #[test]
    fn pop_restores_path() {
        let mut ctx = ConversionCtx::<()>::new();
        ctx.push("input[0]");
        ctx.warn("a", WarningAction::Dropped, "first");
        ctx.push("content[1]");
        ctx.warn("b", WarningAction::Dropped, "second");
        ctx.pop();
        ctx.warn("c", WarningAction::Dropped, "third");
        ctx.pop();

        let warnings = ctx.into_warnings();
        assert_eq!(warnings[0].field, "input[0].a");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
        assert_eq!(warnings[1].field, "input[0].content[1].b");
        assert_eq!(warnings[1].action, WarningAction::Dropped);
        assert_eq!(warnings[2].field, "input[0].c");
        assert_eq!(warnings[2].action, WarningAction::Dropped);
    }
}

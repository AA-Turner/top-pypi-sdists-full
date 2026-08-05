use std::cell::Cell;

/// Optional behavior for parsing config-spec responses.
///
/// The default preserves the existing generic SDK parse path. SnAPI uses the
/// explicit preserving option when it needs `session_update_mode` to build a
/// live client overlay.
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub struct SpecsResponseParseOptions {
    preserve_session_update_mode: bool,
}

impl SpecsResponseParseOptions {
    pub const fn preserving_session_update_mode() -> Self {
        Self {
            preserve_session_update_mode: true,
        }
    }

    pub(crate) const fn should_preserve_session_update_mode(self) -> bool {
        self.preserve_session_update_mode
    }
}

thread_local! {
    static CURRENT_PARSE_OPTIONS: Cell<SpecsResponseParseOptions> =
        const { Cell::new(SpecsResponseParseOptions { preserve_session_update_mode: false }) };
}

struct ParseOptionsGuard {
    previous: SpecsResponseParseOptions,
}

impl Drop for ParseOptionsGuard {
    fn drop(&mut self) {
        CURRENT_PARSE_OPTIONS.with(|options| options.set(self.previous));
    }
}

pub(crate) fn with_parse_options<T>(
    options: SpecsResponseParseOptions,
    callback: impl FnOnce() -> T,
) -> T {
    let previous = CURRENT_PARSE_OPTIONS.with(|current| current.replace(options));
    let _guard = ParseOptionsGuard { previous };
    callback()
}

pub(crate) fn should_preserve_session_update_mode() -> bool {
    CURRENT_PARSE_OPTIONS
        .with(Cell::get)
        .should_preserve_session_update_mode()
}

#[cfg(test)]
mod tests {
    use super::{
        SpecsResponseParseOptions, should_preserve_session_update_mode, with_parse_options,
    };

    #[test]
    fn scoped_options_restore_after_parse() {
        assert!(!should_preserve_session_update_mode());

        with_parse_options(
            SpecsResponseParseOptions::preserving_session_update_mode(),
            || {
                assert!(should_preserve_session_update_mode());
            },
        );

        assert!(!should_preserve_session_update_mode());
    }

    #[test]
    fn nested_scoped_options_restore_previous_value() {
        with_parse_options(
            SpecsResponseParseOptions::preserving_session_update_mode(),
            || {
                assert!(should_preserve_session_update_mode());

                with_parse_options(SpecsResponseParseOptions::default(), || {
                    assert!(!should_preserve_session_update_mode());
                });

                assert!(should_preserve_session_update_mode());
            },
        );

        assert!(!should_preserve_session_update_mode());
    }
}

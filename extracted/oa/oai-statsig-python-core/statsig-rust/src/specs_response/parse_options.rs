use std::cell::Cell;

/// Optional behavior for parsing config-spec responses.
///
/// The default preserves the existing generic parse path. Callers that build
/// live client overlays can explicitly preserve `session_update_mode`.
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub struct SpecsResponseParseOptions {
    preserve_session_update_mode: bool,
    skip_unhydrated_dynamic_configs_for_preload: bool,
}

impl SpecsResponseParseOptions {
    pub const fn preserving_session_update_mode() -> Self {
        Self {
            preserve_session_update_mode: true,
            skip_unhydrated_dynamic_configs_for_preload: false,
        }
    }

    /// Only the raw-byte shared preloader may omit remote-backed dynamic
    /// configs. Live SDK decoding still requires their values to be hydrated.
    pub(crate) const fn for_shared_preload() -> Self {
        Self {
            preserve_session_update_mode: false,
            skip_unhydrated_dynamic_configs_for_preload: true,
        }
    }

    pub(crate) const fn should_preserve_session_update_mode(self) -> bool {
        self.preserve_session_update_mode
    }

    pub(crate) const fn should_skip_unhydrated_dynamic_configs_for_preload(self) -> bool {
        self.skip_unhydrated_dynamic_configs_for_preload
    }
}

thread_local! {
    static CURRENT_PARSE_OPTIONS: Cell<SpecsResponseParseOptions> =
        const { Cell::new(SpecsResponseParseOptions {
            preserve_session_update_mode: false,
            skip_unhydrated_dynamic_configs_for_preload: false,
        }) };
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

pub(crate) fn should_skip_unhydrated_dynamic_configs_for_preload() -> bool {
    CURRENT_PARSE_OPTIONS
        .with(Cell::get)
        .should_skip_unhydrated_dynamic_configs_for_preload()
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

mod document;
mod value;

pub use document::*;
pub use value::*;

fn into_directive_diagnostic(
    diagnostic: &tombi_diagnostic::Diagnostic,
    content_span: tombi_text::Span,
) -> tombi_diagnostic::Diagnostic {
    tombi_diagnostic::Diagnostic::new_warning(
        diagnostic.message(),
        diagnostic.code(),
        diagnostic.span() + content_span.start,
    )
}

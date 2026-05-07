use lsp_types::{
    Documentation, MarkupContent, MarkupKind, ParameterInformation, ParameterLabel, SignatureHelp,
    SignatureInformation,
};

use crate::analysis::{cursor_context, CursorContext};
use crate::catalog::Catalog;

/// Produce signature help for the function call at the cursor position.
pub fn signature_help(sql: &str, line: u32, col: u32) -> Option<SignatureHelp> {
    let ctx = cursor_context(sql, line, col);

    let (fn_name, arg_index) = match ctx {
        CursorContext::FunctionArg {
            function_name,
            arg_index,
        } => (function_name, arg_index),
        _ => return None,
    };

    let catalog = Catalog::get();
    let func = catalog.find_function(&fn_name)?;

    let signatures: Vec<SignatureInformation> = func
        .overloads
        .iter()
        .map(|overload| {
            let label = overload.render_signature(&func.name);
            let parameters: Vec<ParameterInformation> = overload
                .params
                .iter()
                .map(|p| ParameterInformation {
                    label: ParameterLabel::Simple(format!("{}: {}", p.name, p.typ)),
                    documentation: None,
                })
                .collect();

            let docs = func.docs.as_ref().map(|d| {
                Documentation::MarkupContent(MarkupContent {
                    kind: MarkupKind::Markdown,
                    value: d.clone(),
                })
            });

            SignatureInformation {
                label,
                documentation: docs,
                parameters: Some(parameters),
                active_parameter: Some(arg_index as u32),
            }
        })
        .collect();

    if signatures.is_empty() {
        return None;
    }

    Some(SignatureHelp {
        signatures,
        active_signature: Some(0),
        active_parameter: Some(arg_index as u32),
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_signature_help_inside_call() {
        let help = signature_help("SELECT abs(", 0, 11);
        assert!(help.is_some());
        let sh = help.unwrap();
        assert!(!sh.signatures.is_empty());
        assert_eq!(sh.active_parameter, Some(0));
    }

    #[test]
    fn test_signature_help_second_arg() {
        let help = signature_help("SELECT concat(a, ", 0, 17);
        assert!(help.is_some());
        let sh = help.unwrap();
        assert_eq!(sh.active_parameter, Some(1));
    }

    #[test]
    fn test_signature_help_outside_call() {
        let help = signature_help("SELECT abs FROM t", 0, 8);
        assert!(help.is_none());
    }
}

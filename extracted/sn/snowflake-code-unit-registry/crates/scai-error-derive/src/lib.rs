use heck::ToLowerCamelCase;
use proc_macro::TokenStream;
use proc_macro2::TokenStream as TokenStream2;
use quote::{quote, ToTokens};
use syn::{parse_macro_input, Data, DeriveInput, Fields, Lit, Meta};

/// Derive macro that generates three methods on an error enum:
///
/// - `fn error_trace(&self) -> Vec<ErrorTraceEntry>` — location + recursive source chain
/// - `fn details(&self) -> Option<serde_json::Value>` — data fields as JSON (snake_case keys)
/// - `fn all_codes() -> Vec<(&'static str, i32)>` — `(variant_name, error_code)` pairs
///
/// Requirements per variant:
/// - Must have named fields (snafu style)
/// - Must include a `location` field (compile error otherwise)
/// - `#[error_code(NNNN)]` attribute required (read from `err_code`'s attribute)
///
/// Reserved field names excluded from `details()`: `location`, `source`.
///
/// Generated code references runtime types via `crate::error_trace::*`. The
/// consuming crate must provide this module (see `scai-state-core/src/error_trace.rs`).
/// For standalone tests, define a local `mod error_trace` with the same types.
///
/// Based on Snowflake's Universal Driver Error Trace Derive
/// https://github.com/snowflakedb/universal-driver/tree/main/error_trace_derive
#[proc_macro_derive(ScaiError, attributes(error_code))]
pub fn derive_scai_error(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    match expand_scai_error(&input) {
        Ok(ts) => ts.into(),
        Err(e) => e.to_compile_error().into(),
    }
}

fn expand_scai_error(input: &DeriveInput) -> syn::Result<TokenStream2> {
    let enum_name = &input.ident;
    let data = match &input.data {
        Data::Enum(data) => data,
        _ => {
            return Err(syn::Error::new_spanned(
                input,
                "ScaiError can only be derived for enums",
            ))
        }
    };

    let mut trace_arms = Vec::new();
    let mut details_arms = Vec::new();
    let mut all_codes_entries = Vec::new();

    for variant in &data.variants {
        let vname = &variant.ident;
        let vname_str = vname.to_string();

        let named_fields = match &variant.fields {
            Fields::Named(named) => &named.named,
            _ => {
                return Err(syn::Error::new_spanned(
                    vname,
                    format!("ScaiError: variant `{vname_str}` must use named fields"),
                ))
            }
        };

        let has_location = named_fields
            .iter()
            .any(|f| f.ident.as_ref().is_some_and(|i| i == "location"));
        if !has_location {
            return Err(syn::Error::new_spanned(
                vname,
                format!(
                    "ScaiError: variant `{vname_str}` is missing a `location` field \
                     (add `#[snafu(implicit)] location: snafu::Location`)"
                ),
            ));
        }

        let has_source = named_fields
            .iter()
            .any(|f| f.ident.as_ref().is_some_and(|i| i == "source"));

        let error_code = parse_error_code_attr(&variant.attrs, vname)?;

        // --- error_trace arm ---
        let trace_arm = if has_source {
            quote! {
                #enum_name::#vname { location, source, .. } => {
                    let mut entries = vec![crate::error_trace::ErrorTraceEntry {
                        location: crate::error_trace::Location {
                            file: location.file().to_string(),
                            line: location.line(),
                            column: location.column(),
                        },
                        message: self.to_string(),
                    }];
                    {
                        use crate::error_trace::ErrorTraceFallback as _;
                        let resolver = crate::error_trace::ErrorTraceResolver(source);
                        entries.extend((&resolver).resolve());
                    }
                    entries
                }
            }
        } else {
            quote! {
                #enum_name::#vname { location, .. } => {
                    vec![crate::error_trace::ErrorTraceEntry {
                        location: crate::error_trace::Location {
                            file: location.file().to_string(),
                            line: location.line(),
                            column: location.column(),
                        },
                        message: self.to_string(),
                    }]
                }
            }
        };
        trace_arms.push(trace_arm);

        // --- details arm ---
        let data_fields: Vec<_> = named_fields
            .iter()
            .filter(|f| {
                let name = f.ident.as_ref().unwrap().to_string();
                name != "location" && name != "source"
            })
            .collect();

        let details_arm = if data_fields.is_empty() {
            quote! { #enum_name::#vname { .. } => None }
        } else {
            let field_idents: Vec<_> = data_fields
                .iter()
                .map(|f| f.ident.as_ref().unwrap())
                .collect();
            let field_name_strs: Vec<_> = data_fields
                .iter()
                .map(|f| f.ident.as_ref().unwrap().to_string().to_lower_camel_case())
                .collect();
            quote! {
                #enum_name::#vname { #(#field_idents,)* .. } => {
                    Some(serde_json::json!({
                        #(#field_name_strs: #field_idents),*
                    }))
                }
            }
        };
        details_arms.push(details_arm);

        // --- all_codes entry ---
        let code_i32 = error_code as i32;
        all_codes_entries.push(quote! { (#vname_str, #code_i32) });
    }

    Ok(quote! {
        impl #enum_name {
            pub fn error_trace(&self) -> Vec<crate::error_trace::ErrorTraceEntry> {
                match self {
                    #(#trace_arms,)*
                }
            }

            pub fn details(&self) -> Option<serde_json::Value> {
                match self {
                    #(#details_arms,)*
                }
            }

            pub fn all_codes() -> Vec<(&'static str, i32)> {
                vec![
                    #(#all_codes_entries,)*
                ]
            }
        }
    })
}

fn parse_error_code_attr(attrs: &[syn::Attribute], variant_ident: &syn::Ident) -> syn::Result<u32> {
    for attr in attrs {
        if !attr.path().is_ident("error_code") {
            continue;
        }
        let meta = &attr.meta;
        if let Meta::List(list) = meta {
            let tokens_str = list.tokens.to_token_stream().to_string();
            let trimmed = tokens_str.trim();

            // Skip the enum-level `#[error_code(type = "u32")]` form
            if trimmed.starts_with("type") {
                continue;
            }

            if let Ok(code) = trimmed.parse::<u32>() {
                return Ok(code);
            }

            // Try parsing as a syn Lit
            if let Ok(Lit::Int(lit_int)) = syn::parse2::<Lit>(list.tokens.clone()) {
                return lit_int.base10_parse::<u32>();
            }
        }
        return Err(syn::Error::new_spanned(
            attr,
            format!(
                "ScaiError: could not parse #[error_code(NNNN)] on variant `{}`",
                variant_ident
            ),
        ));
    }
    Err(syn::Error::new_spanned(
        variant_ident,
        format!(
            "ScaiError: variant `{}` is missing #[error_code(NNNN)] attribute",
            variant_ident
        ),
    ))
}

#[cfg(test)]
mod tests {
    use super::*;
    use quote::quote;

    fn parse_and_expand(tokens: proc_macro2::TokenStream) -> syn::Result<TokenStream2> {
        let input: DeriveInput = syn::parse2(tokens)?;
        expand_scai_error(&input)
    }

    #[test]
    fn rejects_variant_missing_location() {
        let input = quote! {
            enum Bad {
                #[error_code(9999)]
                NoLocation { msg: String },
            }
        };
        let err = parse_and_expand(input).unwrap_err();
        let msg = err.to_string();
        assert!(
            msg.contains("missing a `location` field"),
            "expected location error, got: {msg}"
        );
        assert!(msg.contains("NoLocation"));
    }

    #[test]
    fn rejects_variant_missing_error_code() {
        let input = quote! {
            enum Bad {
                NoCode {
                    location: (),
                },
            }
        };
        let err = parse_and_expand(input).unwrap_err();
        let msg = err.to_string();
        assert!(
            msg.contains("missing #[error_code(NNNN)]"),
            "expected error_code error, got: {msg}"
        );
        assert!(msg.contains("NoCode"));
    }

    #[test]
    fn rejects_non_enum() {
        let input = quote! {
            struct NotAnEnum {
                field: String,
            }
        };
        let err = parse_and_expand(input).unwrap_err();
        assert!(err.to_string().contains("can only be derived for enums"));
    }

    #[test]
    fn rejects_tuple_variant() {
        let input = quote! {
            enum Bad {
                #[error_code(1001)]
                TupleStyle(String),
            }
        };
        let err = parse_and_expand(input).unwrap_err();
        assert!(err.to_string().contains("must use named fields"));
    }
}

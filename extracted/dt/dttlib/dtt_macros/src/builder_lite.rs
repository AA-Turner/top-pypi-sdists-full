//! create builder functions for every field in a struct
//! except those with #[no_builder] attribute
//!
//! # Examples
//!
//! ```
//! use dtt_macros::*;
//!
//! struct NeedsCustomFunc {
//!     // this structure needs a special function
//!     // for initialization
//! }
//!
//! struct DontModify {
//!     // this structure is created internally
//!     // so should not be set during initialization
//! }
//!
//! #[builder_lite]
//! struct MyStruct {
//!     field_a: i32,
//!     field_b: String,
//!     #[no_builder]
//!     field_c: NeedsCustomFunc,
//!     #[no_builder]
//!     field_d: DontModify
//! }
//! ```
//!
//! expands to
//!
//! ```
//! use dtt_macros::*;
//!
//! struct NeedsCustomFunc {
//!     // this structure needs a special function
//!     // for initialization
//! }
//!
//! struct DontModify {
//!     // this structure is created internally
//!     // so should not be set during initialization
//! }
//!
//! struct MyStruct {
//!     field_a: i32,
//!     field_b: String,
//!     field_c: NeedsCustomFunc,
//!     field_d: DontModify
//! }
//!
//! impl MyStruct {
//!     pub fn with_field_a(mut self, field_a: i32) -> Self {
//!         self.field_a = field_a;
//!         self
//!     }
//!       
//!     pub fn with_field_b(mut self, field_b: String) -> Self {
//!         self.field_b = field_b;
//!         self
//!     }
//! }
//! ```

use proc_macro::TokenStream;
use proc_macro2::Ident;
use quote::{ToTokens, quote, quote_spanned};
use syn::spanned::Spanned;
use syn::{ItemStruct, parse_macro_input};

// return index into field attributes
fn find_attribute(attrs: &Vec<syn::Attribute>, attr_name: &str) -> Vec<usize> {
    let mut indices = Vec::new();
    for (i, attr) in attrs.iter().enumerate() {
        let segs = &attr.meta.path().segments;
        if !segs.is_empty() && segs[0].ident == attr_name {
            indices.push(i);
        }
    }
    indices
}

pub(crate) fn impl_builder_lite(item: TokenStream) -> TokenStream {
    let mut strct = parse_macro_input!(item as ItemStruct);

    let strct_name = &strct.ident.to_token_stream();

    let mut builder_funcs: proc_macro2::TokenStream = proc_macro2::TokenStream::new();

    'fields: for field in strct.fields.iter_mut() {
        let mut indices = find_attribute(&field.attrs, "no_builder");
        // go backwards so we aren't removing the wrong item
        indices.reverse();
        if !indices.is_empty() {
            for index in indices {
                field.attrs.remove(index);
            }
            continue 'fields;
        }

        let field_name = &field.ident.clone().into_token_stream();
        let field_type = &field.ty.clone().into_token_stream();
        let func_name =
            Ident::new(format!("with_{}", field_name).as_str(), field.span()).to_token_stream();

        builder_funcs.extend(quote_spanned! {
            field.ident.span()=>
            pub fn #func_name(mut self, #field_name: #field_type) -> Self {
                self.#field_name = #field_name;
                self
            }
        })
    }

    //println!("{}", builder_funcs);

    let struct_body = strct.clone().into_token_stream();

    quote! {
        #struct_body

        impl #strct_name {
                #builder_funcs
        }
    }
    .into()
}

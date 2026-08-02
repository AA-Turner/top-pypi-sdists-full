use proc_macro::TokenStream;
use proc_macro2::Span;
use quote::quote;
use syn::Ident;
use syn::punctuated::Punctuated;
use syn::token::{Comma, Gt, Lt};
use syn::{GenericParam, Generics, ItemStruct, parse_macro_input};

/// create an empty implementation for a flag or super trait
pub(crate) fn empty_derive(item: TokenStream, tr: &str) -> TokenStream {
    let st: ItemStruct = parse_macro_input!(item);

    let trait_ident = Ident::new(tr, Span::call_site());

    let st_id = st.ident.clone();
    let st_gen = st.generics.clone();

    // build generic list with names, but no qualifiers
    //let mut st_gen = TokenStream::new();

    // let mut angle_brack = AngleBracketedGenericArguments{
    //     colon2_token: None,
    //     lt_token:
    // }

    let mut angle_args = Punctuated::<GenericParam, Comma>::new();

    for generic in &st.generics.params {
        let new_gp = match generic {
            GenericParam::Type(t) => {
                let mut new_t = t.clone();
                new_t.bounds.clear();
                GenericParam::Type(new_t)
            }
            _ => generic.clone(),
        };
        angle_args.push(new_gp);
    }

    let new_gen = Generics {
        lt_token: Some(Lt::default()),
        params: angle_args,
        gt_token: Some(Gt::default()),
        where_clause: None,
    };

    quote!(
        impl #st_gen #trait_ident for #st_id #new_gen {}
    )
    .into()
}

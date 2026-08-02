use proc_macro::TokenStream;
use quote::{quote, quote_spanned};
use syn::spanned::Spanned;
use syn::{ItemFn, ReturnType, parse_macro_input, parse_quote};

//convert synchronous generators with arbitrary return values into async generators
// with the correct return value
// Function
pub(crate) fn impl_box_async(item: TokenStream) -> TokenStream {
    let fun: ItemFn = parse_macro_input!(item as ItemFn);

    // try to get the underlying PipeData type
    let ret_type = if let ReturnType::Type(_, bt) = &fun.sig.output {
        *bt.clone()
    } else {
        return quote_spanned!(
                   fun.sig.output.span() =>
                    compile_error!("A generator function must have an output that is Into<PipeResult<PipeData>>.")
            ).into();
    };

    // change signature
    let new_out: ReturnType = parse_quote!(
        -> futures::future::BoxFuture<'_, #ret_type >
    );

    let mut new_sig = fun.sig.clone();
    new_sig.output = new_out;
    let body = &fun.block;
    quote!(
        #new_sig {
            async move { #body }.boxed()
        }
    )
    .into()
}

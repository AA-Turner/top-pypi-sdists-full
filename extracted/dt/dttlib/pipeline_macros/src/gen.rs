use proc_macro::TokenStream;
use quote::{quote, quote_spanned};
use syn::{ItemFn, parse_macro_input, parse_quote, Path, ReturnType, Type, TypePath};
use syn::spanned::Spanned;

//convert synchronous generators with arbitrary return values into async generators
// with the correct return value
// Function
pub (crate) fn impl_gen(item: TokenStream, num_inputs: usize) -> TokenStream {
    let mut fun: ItemFn = parse_macro_input!(item as ItemFn);

    // try to get the underlying PipeData type
    let ret_type = if let ReturnType::Type(_, bt) = &fun.sig.output {
        *bt.clone()
    }
    else {
        return quote_spanned!(
                   fun.sig.output.span() =>
                    compile_error!("A generator function must have an output that is Into<PipeResult<PipeData>>.")
            ).into();
    };
    let pipedata_type =
        if let Ok(t) = find_base_return_type(ret_type) {
            t
        }
        else {
            return quote_spanned!(
                   fun.sig.output.span() =>
                    compile_error!("A generator function must have an output that is Into<PipeResult<PipeData>>.")
            ).into();
        };

    // change signature

    let new_out: ReturnType = parse_quote!(
      PipeResult < #pipedata_type >
    );

    let mut new_sig = fun.sig.clone();
    new_sig.output = new_out;
    let body = & fun.block;
    quote!(
        #new_sig {
            #body .into()
        }
    ).into()
}

fn find_base_return_type(ret_type: Type) -> Result<Type,()> {

    if let Type::Path(
        TypePath {
            qself: _,
            path: Path{
                leading_colon: _,
                segments: segs,
            }
        }) = &ret_type {
            
            //if segs.len() = 1 && segs[0].ident.to_string() == "Vec"
        
            Ok(ret_type)
        }
        else {
            Err(())
        }

}



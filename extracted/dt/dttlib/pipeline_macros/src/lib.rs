mod box_async;
mod derive;

extern crate proc_macro;
use crate::box_async::impl_box_async;
use crate::derive::empty_derive;
use proc_macro::TokenStream;

#[proc_macro_derive(StateData)]
pub fn state_data(input: TokenStream) -> TokenStream {
    empty_derive(input, "StateData")
}

#[proc_macro_derive(ConfigData)]
pub fn config_data(input: TokenStream) -> TokenStream {
    empty_derive(input, "ConfigData")
}

/// Turns a non-async function into an async function that returns a futures::future::BoxFuture
#[proc_macro_attribute]
pub fn box_async(_attr: TokenStream, input: TokenStream) -> TokenStream {
    impl_box_async(input)
    //input
}

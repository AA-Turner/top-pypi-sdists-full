mod builder_lite;

extern crate proc_macro;
use crate::builder_lite::impl_builder_lite;
use proc_macro::TokenStream;

/// Does nothing
/// This macro is needed so that `#[staticmethod]` method attribute used by pyo3 still builds
/// when not using pyo3
///
/// There doesn't seem to be a way to make that attribute conditional
#[proc_macro_attribute]
pub fn staticmethod(_attr: TokenStream, input: TokenStream) -> TokenStream {
    input
}

/// Does nothing
/// This macro is needed so that `#[new]` method attribute use by pyo3 still builds
/// when not using pyo3
///
/// There doesn't seem to be a way to make that attribute conditional
#[proc_macro_attribute]
pub fn new(_attr: TokenStream, input: TokenStream) -> TokenStream {
    input
}

/// Does nothing
/// This macro is needed so that `#[getter]` method attribute use by pyo3 still builds
/// when not using pyo3
///
/// There doesn't seem to be a way to make that attribute conditional
#[proc_macro_attribute]
pub fn getter(_attr: TokenStream, input: TokenStream) -> TokenStream {
    input
}

/// Does nothing
/// This macro is needed so that `#[pyo3]` method attribute use by pyo3 still builds
/// when not using pyo3
///
/// There doesn't seem to be a way to make that attribute conditional
#[proc_macro_attribute]
pub fn pyo3(_attr: TokenStream, input: TokenStream) -> TokenStream {
    input
}

/// create builder functions for every field in a struct
/// except those with #[no_builder] attribute
#[proc_macro_attribute]
pub fn builder_lite(_attr: TokenStream, input: TokenStream) -> TokenStream {
    impl_builder_lite(input)
}

/// Helper attribute for build_lite.
/// Fields marked with no_builder don't get a builder function.
///
/// Useful for private fields or fields that need a custom builder.
#[proc_macro_attribute]
pub fn no_builder(_attr: TokenStream, input: TokenStream) -> TokenStream {
    input
}

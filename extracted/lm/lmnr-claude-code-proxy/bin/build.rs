fn main() {
    // Configure for PyO3 only when python feature is enabled
    #[cfg(feature = "python")]
    {
        pyo3_build_config::add_extension_module_link_args();
    }

    // Configure for NAPI only when typescript feature is enabled
    #[cfg(feature = "typescript")]
    {
        napi_build::setup();
    }
}

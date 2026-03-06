fn main() {
    // Scope linker args to cdylib extension builds only.
    #[cfg(feature = "python-extension")]
    pyo3_build_config::add_extension_module_link_args();
}

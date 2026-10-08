use pyo3_build_config::PythonImplementation;

fn main() {
    pyo3_build_config::use_pyo3_cfgs();
    link_libpython_import_library_on_windows();
}

/// PyO3 0.28+ links Windows builds with `raw-dylib`, which only provides the
/// symbols pyo3-ffi itself declares. Kolo declares CPython functions pyo3-ffi
/// omits (e.g. `_PyType_Lookup`), so link the full import library too, as
/// PyO3 did before raw-dylib.
fn link_libpython_import_library_on_windows() {
    if std::env::var("CARGO_CFG_TARGET_OS").as_deref() != Ok("windows") {
        return;
    }
    let config = pyo3_build_config::get();
    let version = config.version();
    let lib_name = match config.implementation() {
        // PyPy's import library is named pythonXY.lib, not after its DLL.
        PythonImplementation::PyPy => format!("python{}{}", version.major, version.minor),
        _ => config
            .lib_name()
            .expect("PyO3 build config has no Python lib_name on Windows")
            .to_string(),
    };
    println!("cargo:rustc-link-lib={lib_name}");
    if let Some(lib_dir) = config.lib_dir() {
        println!("cargo:rustc-link-search=native={lib_dir}");
    }
}

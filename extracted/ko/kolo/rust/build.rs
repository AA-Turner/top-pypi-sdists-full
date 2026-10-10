use pyo3_build_config::{GilUsed, PythonAbiKind, PythonImplementation};

fn main() {
    pyo3_build_config::use_pyo3_cfgs();
    emit_line_table_cfg();
    link_libpython_import_library_on_windows();
}

/// `kolo_line_table`: the per-code line table (`utils::frame_path::CodeLines`)
/// is exact on version-specific (not abi3) GIL builds of CPython 3.12 through
/// 3.15. From 3.13 it reads private code-object layout pinned per minor
/// release (64-bit only), so a newer release stays on `PyFrame_GetLineNumber`
/// until its offsets are added.
fn emit_line_table_cfg() {
    println!("cargo:rustc-check-cfg=cfg(kolo_line_table)");
    let abi = pyo3_build_config::get().target_abi();
    let version = abi.version();
    if abi.implementation() == PythonImplementation::CPython
        && abi.kind() == PythonAbiKind::VersionSpecific(GilUsed::GilEnabled)
        && version.major == 3
        && (12..=15).contains(&version.minor)
        // The 3.13+ offsets are for 64-bit pointers.
        && (version.minor == 12
            || std::env::var("CARGO_CFG_TARGET_POINTER_WIDTH").as_deref() == Ok("64"))
    {
        println!("cargo:rustc-cfg=kolo_line_table");
    }
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

use std::env;
use std::path::PathBuf;

fn main() {
    println!("cargo:rustc-link-lib=gds-sigp");
    println!("cargo:rustc-link-lib=fftw3");
    #[cfg(feature = "nds")]
    {
        println!("cargo:rustc-link-lib=ndsclient");
        println!("cargo:rustc-link-lib=ndscxx");
    }

    let bindings = bindgen::Builder::default()
        .header("wrapper.h")
        .generate()
        .expect("Unable to generate bindings");

    let out_path =
        PathBuf::from(env::var("OUT_DIR").expect("Environment var OUT_DIR must be a path"));
    bindings
        .write_to_file(out_path.join("bindings.rs"))
        .expect("Couldn't write bindings");
}

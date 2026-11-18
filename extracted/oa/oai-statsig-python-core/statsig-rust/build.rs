use std::{env, fs, io, path::Path};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("cargo:rerun-if-changed=resources/ip_supalite.table");
    println!("cargo:rerun-if-env-changed=STATSIG_BUILD_PROTO");
    write_country_index(Path::new(&env::var_os("OUT_DIR").unwrap()))?;

    if env::var("STATSIG_BUILD_PROTO").unwrap_or_default() == "true" {
        println!("cargo:rerun-if-changed=../api-interface-definitions/protos");
        prost_build::Config::new()
            .out_dir("src/specs_response")
            .compile_protos(
                &["../api-interface-definitions/protos/config_specs.proto"],
                &["../api-interface-definitions/protos"],
            )?;
    }

    Ok(())
}

fn write_country_index(out_dir: &Path) -> io::Result<()> {
    let table = fs::read("resources/ip_supalite.table")?;
    let country_count = table
        .chunks_exact(2)
        .position(|code| code[0] == b'*')
        .expect("missing country codebook terminator");
    let (codes, mut runs) = table.split_at((country_count + 1) * 2);
    assert!(codes.is_ascii());

    let mut records = Vec::new();
    let mut end_block = 0_u32;
    while !runs.is_empty() {
        let (blocks, code, rest) = match runs {
            [n @ 0..=239, code, rest @ ..] => (u32::from(*n), *code, rest),
            [242, a, b, code, rest @ ..] => (u32::from_le_bytes([*a, *b, 0, 0]), *code, rest),
            [243, a, b, c, code, rest @ ..] => (u32::from_le_bytes([*a, *b, *c, 0]), *code, rest),
            _ => panic!("invalid country range encoding"),
        };
        assert!(blocks > 0 && usize::from(code) < country_count);
        end_block += blocks;
        assert!(end_block <= 1 << 24);
        // The high 24 bits hold the last /24 block in this range. The low byte is its country ID.
        let record = ((end_block - 1) << 8) | u32::from(code);
        records.extend_from_slice(&record.to_le_bytes());
        runs = rest;
    }
    assert_eq!(
        end_block,
        1 << 24,
        "country table must cover all IPv4 addresses"
    );
    fs::write(out_dir.join("country_codes"), &codes[..country_count * 2])?;
    fs::write(out_dir.join("country_ranges"), records)
}

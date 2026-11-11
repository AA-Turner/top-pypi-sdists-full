use std::{collections::HashMap, hint::black_box, io::Read, path::Path, time::Instant};

#[path = "utils/synthetic_specs_fixture.rs"]
mod synthetic_specs_fixture;

use bytes::Bytes;
use prost::Message;
use statsig_rust::{
    OPS_STATS,
    networking::ResponseData,
    specs_response::{
        proto_specs::deserialize_protobuf, spec_types::SpecsResponseFull,
        statsig_config_specs as pb,
    },
};

#[test]
#[ignore = "manual benchmark; run in release mode with --ignored --nocapture"]
fn benchmark_protobuf_copies() {
    let iterations = std::env::var("PROTO_COPY_BENCH_ITERATIONS")
        .ok()
        .and_then(|value| value.parse::<usize>().ok())
        .filter(|value| *value > 0)
        .unwrap_or(100);
    let ops = OPS_STATS.get_for_instance("protobuf-copy-bench");
    let current = SpecsResponseFull::default();
    let benchmark_case = |name: &str, compressed: &[u8], encoding: &str| {
        println!(
            "{name} content_encoding={encoding} bytes={}",
            compressed.len()
        );
        let headers = HashMap::from([
            ("content-type".into(), "application/octet-stream".into()),
            ("content-encoding".into(), encoding.to_owned()),
        ]);
        let decoded = match encoding {
            "statsig-zstd" => zstd::stream::decode_all(compressed).unwrap(),
            "statsig-br" => {
                let mut bytes = Vec::new();
                brotli::Decompressor::new(compressed, 4096)
                    .read_to_end(&mut bytes)
                    .unwrap();
                bytes
            }
            _ => panic!("unsupported protobuf content encoding: {encoding}"),
        };
        let mut remaining = Bytes::from(decoded);
        let mut frames = Vec::new();
        let mut dynamic_payloads = Vec::new();
        loop {
            let start = remaining.clone();
            let envelope = pb::SpecsEnvelope::decode_length_delimited(&mut remaining).unwrap();
            let frame = start.slice(..start.len() - remaining.len());
            if envelope.kind == pb::SpecsEnvelopeKind::DynamicConfig as i32 {
                dynamic_payloads.push(envelope.data.unwrap());
            }
            frames.push(frame);
            if envelope.kind == pb::SpecsEnvelopeKind::Done as i32 {
                break;
            }
        }
        for round in 0..6 {
            for use_bytes in if round % 2 == 0 {
                [false, true]
            } else {
                [true, false]
            } {
                let started = Instant::now();
                for _ in 0..iterations {
                    for frame in &frames {
                        let envelope = if use_bytes {
                            pb::SpecsEnvelope::decode_length_delimited(black_box(frame.clone()))
                        } else {
                            pb::SpecsEnvelope::decode_length_delimited(black_box(frame.as_ref()))
                        };
                        black_box(envelope.unwrap());
                    }
                }
                println!(
                    "{name} outer bytes={use_bytes} round={round} us/update={:.3}",
                    started.elapsed().as_micros() as f64 / iterations as f64
                );
            }
            for borrow in if round % 2 == 0 {
                [false, true]
            } else {
                [true, false]
            } {
                let started = Instant::now();
                for _ in 0..iterations {
                    for payload in &dynamic_payloads {
                        let spec = if borrow {
                            pb::Spec::decode(std::io::Cursor::new(black_box(payload.as_slice())))
                        } else {
                            pb::Spec::decode(std::io::Cursor::new(black_box(payload.clone())))
                        };
                        black_box(spec.unwrap());
                    }
                }
                println!(
                    "{name} dynamic borrow={borrow} round={round} us/update={:.3}",
                    started.elapsed().as_micros() as f64 / iterations as f64
                );
            }
            let started = Instant::now();
            for _ in 0..iterations {
                let mut next = SpecsResponseFull::default();
                let mut data = ResponseData::from_bytes_with_headers(
                    compressed.to_vec(),
                    Some(headers.clone()),
                );
                deserialize_protobuf(&ops, &current, &mut next, &mut data).unwrap();
                black_box(next);
            }
            println!(
                "{name} sync-full round={round} us/update={:.3}",
                started.elapsed().as_micros() as f64 / iterations as f64
            );
        }
    };

    if let Some(path) = std::env::var_os("STATSIG_BENCH_MANIFEST") {
        let fixture = synthetic_specs_fixture::load_inline_protobuf(Path::new(&path))
            .unwrap_or_else(|error| panic!("invalid STATSIG_BENCH_MANIFEST: {error}"));
        println!(
            "synthetic-inline product={} seed={} sha256={}",
            fixture.product, fixture.seed, fixture.sha256
        );
        benchmark_case(
            "synthetic-inline",
            &fixture.bytes,
            &fixture.content_encoding,
        );
    } else {
        for (name, fixture) in [
            (
                "eval",
                include_bytes!("data/eval_proj_dcs.pb.br").as_slice(),
            ),
            (
                "perf",
                include_bytes!("data/perf_proj_dcs.pb.br").as_slice(),
            ),
        ] {
            let zstd =
                zstd::stream::encode_all(brotli::Decompressor::new(fixture, 4096), 3).unwrap();
            benchmark_case(name, &zstd, "statsig-zstd");
        }
    }
}

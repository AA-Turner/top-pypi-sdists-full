use std::{hint::black_box, time::Instant};

use prost::Message;
use statsig_rust::{
    OPS_STATS,
    networking::ResponseData,
    specs_response::{
        proto_specs::deserialize_protobuf, proto_stream_reader::ProtoStreamReader,
        spec_types::SpecsResponseFull, statsig_config_specs as pb,
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
    for (name, compressed) in [
        (
            "eval",
            include_bytes!("data/eval_proj_dcs.pb.br").as_slice(),
        ),
        (
            "perf",
            include_bytes!("data/perf_proj_dcs.pb.br").as_slice(),
        ),
    ] {
        let mut data = ResponseData::from_bytes(compressed.to_vec());
        let mut reader = ProtoStreamReader::new(&mut data);
        let mut frames = Vec::new();
        let mut dynamic_payloads = Vec::new();
        loop {
            let frame = reader.read_next_delimited_proto().unwrap().freeze();
            let envelope = pb::SpecsEnvelope::decode_length_delimited(frame.clone()).unwrap();
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
                let mut data = ResponseData::from_bytes(compressed.to_vec());
                deserialize_protobuf(&ops, &current, &mut next, &mut data).unwrap();
                black_box(next);
            }
            println!(
                "{name} sync-full round={round} us/update={:.3}",
                started.elapsed().as_micros() as f64 / iterations as f64
            );
        }
    }
}

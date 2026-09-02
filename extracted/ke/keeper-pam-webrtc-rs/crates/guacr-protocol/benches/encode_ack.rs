use criterion::{black_box, criterion_group, criterion_main, BenchmarkId, Criterion};
use guacr_protocol::{GuacdInstruction, GuacdParser, StreamingParser};

fn encode_ack_new(stream_idx: u32) {
    let _ = black_box(StreamingParser::encode_ack(stream_idx));
}

fn encode_ack_old(stream_idx: u32) {
    let instr = GuacdInstruction::new(
        "ack".to_string(),
        vec![stream_idx.to_string(), "OK".to_string(), "0".to_string()],
    );
    let _ = black_box(GuacdParser::guacd_encode_instruction(&instr));
}

fn benchmark_encode_ack(c: &mut Criterion) {
    let mut group = c.benchmark_group("encode_ack");

    let stream_indices = [
        ("1-digit", 5u32),
        ("2-digit", 42u32),
        ("5-digit", 12345u32),
        ("10-digit", u32::MAX),
    ];

    for (name, idx) in stream_indices {
        group.bench_with_input(BenchmarkId::new("new_zero_alloc", name), &idx, |b, &idx| {
            b.iter(|| encode_ack_new(idx));
        });

        group.bench_with_input(
            BenchmarkId::new("old_via_instruction", name),
            &idx,
            |b, &idx| {
                b.iter(|| encode_ack_old(idx));
            },
        );
    }

    group.finish();
}

criterion_group!(benches, benchmark_encode_ack);
criterion_main!(benches);

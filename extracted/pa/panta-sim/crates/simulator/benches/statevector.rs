use criterion::{black_box, criterion_group, criterion_main, BenchmarkId, Criterion};
use qsim_simulator::{Circuit, ExecutionEngine, Precision};

/// 측정 큐비트 수. v0.2.0 까지는 [15, 20] 만 측정. v0.2.1 에서 25/28 추가
/// (메모리 대역폭 병목 영역에서 f32 메모리 절감 효과 관찰).
const QUBITS: &[usize] = &[15, 20, 25, 28];

/// 정밀도. 같은 회로를 양쪽으로 측정해 메모리/시간 trade 비교.
const PRECISIONS: &[(Precision, &str)] = &[(Precision::F64, "f64"), (Precision::F32, "f32")];

fn build_h_line(n: usize) -> Circuit {
    let mut qc = Circuit::new(n);
    for i in 0..n {
        qc.h(i);
    }
    qc
}

fn build_cnot_chain(n: usize) -> Circuit {
    let mut qc = Circuit::new(n);
    for i in 0..n - 1 {
        qc.cx(i, i + 1);
    }
    qc
}

fn build_ghz(n: usize) -> Circuit {
    let mut qc = Circuit::new(n);
    qc.h(0);
    for i in 1..n {
        qc.cx(0, i);
    }
    qc
}

/// QFT-like circuit: H + controlled-Rz decomposition + final SWAPs.
/// CRz(theta) decomposed as: Rz(theta/2) target, CNOT, Rz(-theta/2) target, CNOT.
fn build_qft(n: usize) -> Circuit {
    let mut qc = Circuit::new(n);
    for j in 0..n {
        qc.h(j);
        for k in (j + 1)..n {
            let theta = std::f64::consts::PI / (1u64 << (k - j)) as f64;
            qc.rz(theta / 2.0, k);
            qc.cx(j, k);
            qc.rz(-theta / 2.0, k);
            qc.cx(j, k);
        }
    }
    for i in 0..n / 2 {
        qc.swap(i, n - 1 - i);
    }
    qc
}

fn bench_with_builder(c: &mut Criterion, name: &str, build: fn(usize) -> Circuit) {
    let mut group = c.benchmark_group(name);
    // 28 큐비트 + QFT 등은 single-iter 만으로도 오래 걸림 — sample size 축소.
    group.sample_size(10);
    group.measurement_time(std::time::Duration::from_secs(15));
    for &n in QUBITS {
        // 28 큐비트는 메모리 8GB(f64) / 4GB(f32) 라 CI 환경에 따라 OOM 가능.
        // 환경변수 PANTA_BENCH_MAX_QUBITS 로 상한 제한 가능.
        if let Ok(s) = std::env::var("PANTA_BENCH_MAX_QUBITS") {
            if let Ok(max_n) = s.parse::<usize>() {
                if n > max_n {
                    continue;
                }
            }
        }
        for &(prec, label) in PRECISIONS {
            let id = format!("{}/{}", label, n);
            group.bench_with_input(BenchmarkId::from_parameter(&id), &n, |b, &n| {
                let qc = build(n);
                let engine = ExecutionEngine::new().with_precision(prec);
                b.iter(|| {
                    black_box(engine.run(black_box(&qc), 0));
                });
            });
        }
    }
    group.finish();
}

fn bench_h_line(c: &mut Criterion) {
    bench_with_builder(c, "H-line", build_h_line);
}
fn bench_cnot_chain(c: &mut Criterion) {
    bench_with_builder(c, "CNOT-chain", build_cnot_chain);
}
fn bench_ghz(c: &mut Criterion) {
    bench_with_builder(c, "GHZ", build_ghz);
}
fn bench_qft(c: &mut Criterion) {
    bench_with_builder(c, "QFT", build_qft);
}

criterion_group!(
    benches,
    bench_h_line,
    bench_cnot_chain,
    bench_ghz,
    bench_qft
);
criterion_main!(benches);

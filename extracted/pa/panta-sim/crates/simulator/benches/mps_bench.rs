//! v0.6.3: criterion benchmarks for the MPS backend.
//!
//! Coverage:
//! - GHZ-50 / GHZ-100 at chi=4 — minimal Schmidt rank (2) so chi=4 is
//!   lossless; the v0.6.3 Vec<bool> outcome refactor lifts the previous
//!   N<=64 cap so GHZ-100 is a real datapoint here.
//! - HEA depth=5 N=30 with chi sweep (4, 8, 16, 32, 64) — random
//!   parameter ansatz, exercises the SVD-truncation path with non-trivial
//!   bond dimensions.  The sweep makes the perf-vs-fidelity trade-off
//!   measurable and surfaces regressions in the SVD/sampling kernels.
//! - GHZ-14 vs statevector cross-check — small-N where both backends
//!   are cheap; ensures the MPS runtime cost is in the same order of
//!   magnitude as statevector for tiny circuits (sanity baseline).
//!
//! CI / sandbox notes: criterion's perf measurements are noisy in
//! containers; the benches are configured with low sample sizes so they
//! finish quickly.  The primary CI guard is "runs without panic" —
//! accuracy regressions are guarded by the unit tests in `lib.rs` and
//! `tests/`.

use criterion::{black_box, criterion_group, criterion_main, BenchmarkId, Criterion};
use qsim_simulator::{Backend, Circuit, ExecutionEngine, Precision};

fn build_ghz(n: usize) -> Circuit {
    let mut qc = Circuit::new(n);
    qc.h(0);
    for i in 0..n - 1 {
        qc.cx(i, i + 1);
    }
    qc.measure_all();
    qc
}

/// Hardware-Efficient Ansatz: layer = Ry(θ_q) on every qubit then
/// CNOT chain.  Parameters are drawn from a fixed deterministic
/// schedule (no rand dep in benches — golden-ratio LCG-ish).
fn build_hea(n: usize, depth: usize) -> Circuit {
    let mut qc = Circuit::new(n);
    let mut k = 0u64;
    for _ in 0..depth {
        for q in 0..n {
            // Deterministic angle in (-π, π).
            let theta = ((k as f64 * 0.61803398875) % 1.0 - 0.5) * std::f64::consts::TAU;
            qc.ry(theta, q);
            k += 1;
        }
        for i in 0..n - 1 {
            qc.cx(i, i + 1);
        }
    }
    qc.measure_all();
    qc
}

fn bench_mps_ghz(c: &mut Criterion) {
    let mut group = c.benchmark_group("mps_ghz");
    group.sample_size(10);
    group.measurement_time(std::time::Duration::from_secs(8));
    for &n in &[50usize, 100usize] {
        let qc = build_ghz(n);
        let engine = ExecutionEngine::with_seed(42)
            .with_backend(Backend::CpuMps)
            .with_mps_bond_dim(4);
        group.bench_with_input(BenchmarkId::from_parameter(n), &n, |b, _| {
            b.iter(|| {
                black_box(engine.run(black_box(&qc), 1000));
            });
        });
    }
    group.finish();
}

/// HEA at fixed (N=30, depth=5) with χ sweep — perf vs fidelity proxy.
fn bench_mps_hea_chi_sweep(c: &mut Criterion) {
    let mut group = c.benchmark_group("mps_hea_n30_d5");
    group.sample_size(10);
    group.measurement_time(std::time::Duration::from_secs(15));
    let n = 30usize;
    let depth = 5usize;
    let qc = build_hea(n, depth);
    for &chi in &[4usize, 8, 16, 32, 64] {
        let engine = ExecutionEngine::with_seed(42)
            .with_backend(Backend::CpuMps)
            .with_mps_bond_dim(chi);
        group.bench_with_input(BenchmarkId::new("chi", chi), &chi, |b, _| {
            b.iter(|| {
                black_box(engine.run(black_box(&qc), 200));
            });
        });
    }
    group.finish();
}

/// Side-by-side parity: GHZ-14 with statevector vs MPS at chi=4
/// (lossless).  The two backends should produce equivalent counts; the
/// bench measures wall-clock so users can see the cross-over point.
fn bench_mps_vs_statevector(c: &mut Criterion) {
    let mut group = c.benchmark_group("mps_vs_statevector_n14");
    group.sample_size(10);
    group.measurement_time(std::time::Duration::from_secs(8));
    let n = 14usize;
    let qc = build_ghz(n);

    let sv_engine = ExecutionEngine::with_seed(42).with_precision(Precision::F64);
    group.bench_function("statevector_f64", |b| {
        b.iter(|| {
            black_box(sv_engine.run(black_box(&qc), 1000));
        });
    });

    let mps_engine = ExecutionEngine::with_seed(42)
        .with_backend(Backend::CpuMps)
        .with_mps_bond_dim(4);
    group.bench_function("mps_chi4", |b| {
        b.iter(|| {
            black_box(mps_engine.run(black_box(&qc), 1000));
        });
    });

    group.finish();
}

criterion_group!(
    benches,
    bench_mps_ghz,
    bench_mps_hea_chi_sweep,
    bench_mps_vs_statevector
);
criterion_main!(benches);

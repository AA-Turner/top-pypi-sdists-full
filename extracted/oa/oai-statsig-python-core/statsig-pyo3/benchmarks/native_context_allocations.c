// Linux/glibc allocation-request counter and optional sampled allocation stacks.
// CPU timings from preload runs are intentionally not used; instrumentation
// perturbs cost. Python small-object allocator calls are not individually counted.
#include <stdatomic.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <execinfo.h>
#include <sched.h>
extern void *__libc_malloc(size_t);
extern void *__libc_calloc(size_t, size_t);
extern void *__libc_realloc(void *, size_t);
static _Atomic int enabled;
static _Atomic int capture_stacks;
static _Atomic uint64_t requests;
static _Atomic uint64_t requested_bytes;
static _Atomic uint64_t sample_count;
static _Atomic uint64_t active_writers;
static _Thread_local int inside;
#define MAX_SAMPLES 16384
#define STACK_DEPTH 28
struct Sample { size_t bytes; int depth; void *frames[STACK_DEPTH]; };
static struct Sample samples[MAX_SAMPLES];
static inline void count(size_t size) {
    if (!inside && atomic_load_explicit(&enabled, memory_order_relaxed)) {
        // Register before rechecking the capture state. Stop may have disabled
        // capture after the fast check; only registered writers may touch data.
        atomic_fetch_add(&active_writers, 1);
        if (!atomic_load(&enabled)) {
            atomic_fetch_sub(&active_writers, 1);
            return;
        }
        uint64_t n = atomic_fetch_add_explicit(&requests, 1, memory_order_relaxed);
        atomic_fetch_add_explicit(&requested_bytes, size, memory_order_relaxed);
        if ((n % 1024) == 0 && atomic_load_explicit(&capture_stacks, memory_order_relaxed)) {
            uint64_t index = atomic_fetch_add_explicit(&sample_count, 1, memory_order_relaxed);
            if (index < MAX_SAMPLES) {
                inside = 1;
                samples[index].bytes = size;
                samples[index].depth = backtrace(samples[index].frames, STACK_DEPTH);
                inside = 0;
            }
        }
        atomic_fetch_sub(&active_writers, 1);
    }
}
void *malloc(size_t size) { count(size); return __libc_malloc(size); }
void *calloc(size_t n, size_t size) { count(n * size); return __libc_calloc(n, size); }
void *realloc(void *ptr, size_t size) { count(size); return __libc_realloc(ptr, size); }
// Start/stop/dump have one controlling thread, as in the Python harness. Writers
// arriving after stop observes zero cannot write while disabled; if a new start
// enables them, its resets have already completed before their state recheck.
void probe_stop(void) {
    atomic_store(&enabled, 0);
    while (atomic_load(&active_writers) != 0) sched_yield();
}
void probe_start(void) {
    probe_stop();
    atomic_store(&requests, 0);
    atomic_store(&requested_bytes, 0);
    atomic_store(&sample_count, 0);
    atomic_store(&enabled, 1);
}
uint64_t probe_count(void) { return atomic_load(&requests); }
uint64_t probe_bytes(void) { return atomic_load(&requested_bytes); }
void probe_stacks(int enabled) { atomic_store(&capture_stacks, enabled); }
void probe_dump(const char *path) {
    probe_stop();
    FILE *out = fopen(path, "w");
    if (!out) return;
    uint64_t n = atomic_load(&sample_count);
    if (n > MAX_SAMPLES) n = MAX_SAMPLES;
    for (uint64_t i = 0; i < n; i++) {
        fprintf(out, "%zu", samples[i].bytes);
        for (int j = 0; j < samples[i].depth; j++) fprintf(out, " %p", samples[i].frames[j]);
        fputc('\n', out);
    }
    fclose(out);
}

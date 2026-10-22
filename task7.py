"""Task 7 - Arithmetic Intensity vs. Memory Bottlenecks.

Kernel A (memory-bound):  B[i] = A[i]                             (vector copy)
Kernel B (compute-bound): B[i] = sin(A[i]) * cos(A[i]) + tan(A[i])
30,000,000 float64 elements, run with 1, 2 and max cores (thread pool;
NumPy releases the GIL inside these ufuncs/copies, so threads run in parallel).
Efficiency = Speedup / Cores, Speedup = T(1) / T(p).
"""
import os
import platform
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np

STUDENT_ID = 230103129
N = 30_000_000
REPEATS = 5
BLOCK = 16_384          # Kernel B works in cache-sized blocks so temporaries stay in cache
MAX_CORES = os.cpu_count() or 1
CORE_COUNTS = sorted({1, 2, MAX_CORES})
BYTES_COPIED = 2 * N * 8   # read A + write B


def kernel_a(A, B, s, e):
    np.copyto(B[s:e], A[s:e])


def kernel_b(A, B, s, e):
    for i in range(s, e, BLOCK):
        j = min(i + BLOCK, e)
        a = A[i:j]
        np.multiply(np.sin(a), np.cos(a), out=B[i:j])
        np.add(B[i:j], np.tan(a), out=B[i:j])


def run_parallel(kernel, A, B, workers, pool):
    step = -(-N // workers)
    futures = [pool.submit(kernel, A, B, s, min(s + step, N)) for s in range(0, N, step)]
    for f in futures:
        f.result()


def best_time_ms(kernel, A, B, workers, pool):
    run_parallel(kernel, A, B, workers, pool)  # warm-up (page faults, caches)
    best = float("inf")
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        run_parallel(kernel, A, B, workers, pool)
        best = min(best, (time.perf_counter() - t0) * 1000.0)
    return best


def check(kernel_name, A, B):
    idx = slice(0, 1_000_000)
    if kernel_name == "A":
        assert np.array_equal(B[idx], A[idx])
    else:
        a = A[idx]
        assert np.allclose(B[idx], np.sin(a) * np.cos(a) + np.tan(a))


def bench(name, kernel, A, B, pool_cache):
    rows = []
    for p in CORE_COUNTS:
        t = best_time_ms(kernel, A, B, p, pool_cache[p])
        check(name, A, B)
        rows.append((p, t))
    t1 = rows[0][1]
    return [(p, t, t1 / t, (t1 / t) / p) for p, t in rows]


def print_table(title, rows, show_bw):
    print(title)
    head = f"{'Cores':>5} | {'Time (ms)':>10} | {'Speedup':>8} | {'Efficiency':>10}"
    if show_bw:
        head += f" | {'Bandwidth (GB/s)':>16}"
    print(head)
    print("-" * len(head))
    for p, t, s, e in rows:
        line = f"{p:>5} | {t:>10.2f} | {s:>8.2f} | {e:>10.2f}"
        if show_bw:
            line += f" | {BYTES_COPIED / (t / 1000.0) / 1e9:>16.2f}"
        print(line)
    print()


def main() -> None:
    print(f"Student ID    : {STUDENT_ID}")
    print(f"Platform      : {platform.platform()} / {platform.machine()}")
    print(f"Python        : {platform.python_version()}  NumPy {np.__version__}")
    print(f"Logical cores : {MAX_CORES}")
    print(f"Array size    : {N:,} float64 ({N * 8 / 1e6:.0f} MB per array)")
    print(f"Core counts   : {CORE_COUNTS}  (best of {REPEATS} runs, thread pool)")
    print()

    rng = np.random.default_rng(STUDENT_ID)
    A = rng.random(N, dtype=np.float64)
    B = np.empty_like(A)

    pools = {p: ThreadPoolExecutor(max_workers=p) for p in CORE_COUNTS}
    try:
        rows_a = bench("A", kernel_a, A, B, pools)
        rows_b = bench("B", kernel_b, A, B, pools)
    finally:
        for pool in pools.values():
            pool.shutdown()

    print_table("Kernel A (memory-bound): B[i] = A[i]", rows_a, show_bw=True)
    print_table("Kernel B (compute-bound): B[i] = sin(A[i])*cos(A[i]) + tan(A[i])", rows_b, show_bw=False)

    pmax = CORE_COUNTS[-1]
    eff_a = rows_a[-1][3]
    eff_b = rows_b[-1][3]
    print(f"Efficiency at {pmax} cores:  Kernel A = {eff_a:.2f}   Kernel B = {eff_b:.2f}")
    print()
    if pmax == 1:
        print("CONCLUSION: only 1 core available - scaling cannot be assessed.")
    elif eff_a < 0.80 and eff_b - eff_a >= 0.10:
        print(f"CONCLUSION: Kernel A (memory-bound vector copy) STALLED in scaling due to "
              f"memory channel saturation (efficiency {eff_a:.2f} at {pmax} cores),")
        print(f"            while Kernel B (compute-bound sin/cos/tan) kept scaling "
              f"(efficiency {eff_b:.2f}).")
    elif eff_b < 0.80 and eff_a - eff_b >= 0.10:
        print(f"CONCLUSION: Kernel B scaled worse than Kernel A (efficiency {eff_b:.2f} vs {eff_a:.2f}); "
              f"memory saturation is NOT the dominant limit here - check CPU load / thermal / core sharing.")
    else:
        print(f"CONCLUSION: no clear memory-channel stall between the kernels on this run "
              f"(A {eff_a:.2f}, B {eff_b:.2f}); rerun on an idle machine.")


if __name__ == "__main__":
    main()
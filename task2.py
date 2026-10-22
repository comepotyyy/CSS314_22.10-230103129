"""Task 2 - Multi-Core Scaling vs. Amdahl's Law.

Parallel summation of 20,000,000 float64 values using a thread pool.
NumPy releases the GIL inside np.sum on large chunks, so threads run in
true parallel here.
"""
import math
import os
import platform
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np

# >>> SET YOUR STUDENT ID HERE (digits only, used as the RNG seed) <<<
STUDENT_ID = 230103129

N = 20_000_000
P = 0.95          # parallelizable fraction for Amdahl's Law
REPEATS = 5       # each configuration is run this many times; best time is kept


def amdahl(p_workers: int, parallel_fraction: float = P) -> float:
    """Theoretical maximum speedup: S(p) = 1 / ((1 - P) + P / p)."""
    return 1.0 / ((1.0 - parallel_fraction) + parallel_fraction / p_workers)


def parallel_sum(data: np.ndarray, workers: int, pool: ThreadPoolExecutor) -> float:
    """Split data into `workers` chunks, sum each in a thread, combine."""
    chunks = np.array_split(data, workers)
    partials = pool.map(np.sum, chunks)
    return float(sum(partials))


def benchmark(data: np.ndarray, workers: int) -> tuple[float, float]:
    """Return (best wall time in ms, computed sum) for a worker count."""
    best = float("inf")
    result = 0.0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        parallel_sum(data, workers, pool)  # warm-up (thread start, cache)
        for _ in range(REPEATS):
            start = time.perf_counter()
            result = parallel_sum(data, workers, pool)
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            best = min(best, elapsed_ms)
    return best, result


def main() -> None:
    max_cores = os.cpu_count() or 1
    worker_counts = sorted({1, 2, 4, max_cores, max_cores * 2})

    print(f"Student ID    : {STUDENT_ID}")
    print(f"Platform      : {platform.platform()} / {platform.machine()}")
    print(f"Logical cores : {max_cores}")
    print(f"Array size    : {N:,} float64 (seed={STUDENT_ID})")
    print(f"Amdahl P      : {P}")
    print(f"Method        : ThreadPoolExecutor + np.sum per chunk, best of {REPEATS}")
    print()

    rng = np.random.default_rng(STUDENT_ID)
    data = rng.random(N, dtype=np.float64)

    reference = float(np.sum(data))

    results = []
    for w in worker_counts:
        t_ms, total = benchmark(data, w)
        # sanity check: parallel result must match serial result
        assert math.isclose(total, reference, rel_tol=1e-9), \
            f"sum mismatch for {w} workers: {total} vs {reference}"
        results.append((w, t_ms))

    t1 = results[0][1]  # T(1): single-worker time

    header = f"{'Cores':>6} | {'Wall Time (ms)':>14} | {'Speedup':>8} | {'Amdahl Upper Bound':>18}"
    print(header)
    print("-" * len(header))
    for w, t_ms in results:
        speedup = t1 / t_ms
        print(f"{w:>6} | {t_ms:>14.3f} | {speedup:>8.2f} | {amdahl(w):>18.2f}")

    print()
    print(f"Amdahl limit as p -> infinity: {1.0 / (1.0 - P):.1f}x")
    print(f"Reference serial sum: {reference:.6f}")


if __name__ == "__main__":
    main()
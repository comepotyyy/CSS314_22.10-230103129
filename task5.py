"""Task 5 - The Overhead Crossover Point.

Benchmark y[i] = a * x[i] + b, serial vs multi-threaded (all cores),
and programmatically locate the N range where parallel becomes faster.

Threads are used because NumPy releases the GIL in ufuncs, so chunks
run in true parallel with no data copying between workers.
"""
import os
import platform
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np

STUDENT_ID = 230103129
SIZES = [100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000]
A, B = 2.5, 1.0
WORKERS = os.cpu_count() or 1
REPEATS = 7            # best-of-N timing repeats per measurement
TARGET_S = 0.02        # each repeat loops until it takes at least ~20 ms


def serial(x, y):
    np.multiply(x, A, out=y)
    np.add(y, B, out=y)


def make_parallel(pool, workers):
    def work(args):
        x, y, s, e = args
        ys = y[s:e]
        np.multiply(x[s:e], A, out=ys)
        np.add(ys, B, out=ys)

    def parallel(x, y):
        n = x.size
        step = -(-n // workers)  # ceil division
        jobs = [(x, y, s, min(s + step, n)) for s in range(0, n, step)]
        list(pool.map(work, jobs))

    return parallel


def per_call_us(fn, x, y) -> float:
    """Best per-call time in microseconds (loops many calls for small N)."""
    fn(x, y)  # warm-up
    t0 = time.perf_counter()
    fn(x, y)
    once = max(time.perf_counter() - t0, 1e-7)
    loops = max(1, min(200_000, int(TARGET_S / once)))
    best = float("inf")
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        for _ in range(loops):
            fn(x, y)
        best = min(best, (time.perf_counter() - t0) / loops)
    return best * 1e6


TRIALS = 3             # serial/parallel measured alternately, median kept


def measure(n, par, rng):
    x = rng.random(n, dtype=np.float64)
    y = np.empty_like(x)
    s_list, p_list = [], []
    for _ in range(TRIALS):
        s_list.append(per_call_us(serial, x, y))
        p_list.append(per_call_us(par, x, y))
    ts = float(np.median(s_list))
    tp = float(np.median(p_list))
    ref = A * x + B
    serial(x, y)
    assert np.allclose(y, ref)
    par(x, y)
    assert np.allclose(y, ref), "parallel result mismatch"
    return ts, tp


def find_crossover(rows):
    """rows: [(n, ts, tp)] sorted by n. Return (last_slower_n, first_faster_n, status).

    first_faster_n = smallest N from which parallel stays faster for all larger N.
    """
    faster = [tp < ts for _, ts, tp in rows]
    if all(faster):
        return None, rows[0][0], "always_faster"
    if not faster[-1]:
        return rows[-1][0], None, "never_faster"
    k = len(rows) - 1
    while k > 0 and faster[k - 1]:
        k -= 1
    return rows[k - 1][0], rows[k][0], "crossover"


def print_table(rows):
    header = (f"{'N':>12} | {'Serial (us)':>12} | {'Parallel (us)':>13} | "
              f"{'Speedup':>8} | {'Winner':<8}")
    print(header)
    print("-" * len(header))
    for n, ts, tp in rows:
        print(f"{n:>12,} | {ts:>12.2f} | {tp:>13.2f} | {ts / tp:>8.2f} | "
              f"{'PARALLEL' if tp < ts else 'serial':<8}")


def main() -> None:
    print(f"Student ID    : {STUDENT_ID}")
    print(f"Platform      : {platform.platform()} / {platform.machine()}")
    print(f"Python        : {platform.python_version()}  NumPy {np.__version__}")
    print(f"Logical cores : {WORKERS}  (parallel version uses {WORKERS} threads)")
    print(f"Operation     : y[i] = {A} * x[i] + {B}  (float64)")
    print(f"Timing        : best of {REPEATS} repeats, per-call average, "
          f"median of {TRIALS} trials, pool created once")
    print()

    rng = np.random.default_rng(STUDENT_ID)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        par = make_parallel(pool, WORKERS)

        rows = []
        for n in SIZES:
            ts, tp = measure(n, par, rng)
            rows.append((n, ts, tp))
        print_table(rows)

        lo, hi, status = find_crossover(rows)
        print()
        if status == "crossover":
            print(f"Coarse crossover: parallel SLOWER at N={lo:,}, FASTER at N={hi:,}")
            # scan one decade below the coarse bracket up to its upper end,
            # so a noisy bracket edge cannot hide the true tipping point
            scan_lo = max(10, lo // 10)
            fine_ns = sorted({int(v) for v in np.geomspace(scan_lo, hi, 28)})
            fine_rows = [(n, *measure(n, par, rng)) for n in fine_ns]
            print()
            print(f"Refinement scan N={scan_lo:,} .. {hi:,} (median of {TRIALS} trials):")
            print_table(fine_rows)
            flo, fhi, fstatus = find_crossover(fine_rows)
            print()
            if fstatus == "crossover":
                print(f"RESULT: multi-threading shifts from SLOWER to FASTER "
                      f"for N in ({flo:,}, {fhi:,}]")
                print(f"        i.e. serial wins up to N={flo:,}; "
                      f"parallel wins from N={fhi:,} upward on this CPU.")
            else:
                print(f"RESULT: refinement was noisy ({fstatus}); "
                      f"crossover lies within ({lo:,}, {hi:,}]")
        elif status == "always_faster":
            print(f"RESULT: parallel was faster at every tested N (from N={hi:,}).")
        else:
            print(f"RESULT: parallel never beat serial up to N={rows[-1][0]:,} "
                  f"on this CPU (memory-bound operation).")


if __name__ == "__main__":
    main()
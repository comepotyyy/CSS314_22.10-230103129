"""Task 4 - Work Stealing & Scheduling Under Skew.

1,000 items; item i costs sleep(0.0001 * (i % 20)).
Run with 4 workers using:
  A) static contiguous blocks (250 items per worker)
  B) dynamic scheduling from a shared queue (chunk size 1 and 5)
Measure total wall time and the delta between the first and last
worker finishing. time.sleep releases the GIL, so threads overlap.
"""
import platform
import queue
import statistics
import threading
import time

STUDENT_ID = 230103129
N_ITEMS = 1000
WORKERS = 4
REPEATS = 5


def cost(i: int) -> float:
    return 0.0001 * (i % 20)


def process(items) -> int:
    n = 0
    for i in items:
        time.sleep(cost(i))
        n += 1
    return n


def run(strategy: str, chunk: int = 1):
    """Return (total_ms, finish_times_ms[list per worker], items_done)."""
    finish = [0.0] * WORKERS
    done = [0] * WORKERS
    barrier = threading.Barrier(WORKERS + 1)
    t0 = [0.0]

    if strategy == "static":
        block = N_ITEMS // WORKERS
        ranges = [range(w * block, (w + 1) * block if w < WORKERS - 1 else N_ITEMS)
                  for w in range(WORKERS)]

        def worker(w):
            barrier.wait()
            done[w] = process(ranges[w])
            finish[w] = (time.perf_counter() - t0[0]) * 1000.0
    else:
        q = queue.Queue()
        for start in range(0, N_ITEMS, chunk):
            q.put(range(start, min(start + chunk, N_ITEMS)))

        def worker(w):
            barrier.wait()
            while True:
                try:
                    items = q.get_nowait()
                except queue.Empty:
                    break
                done[w] += process(items)
            finish[w] = (time.perf_counter() - t0[0]) * 1000.0

    threads = [threading.Thread(target=worker, args=(w,)) for w in range(WORKERS)]
    for t in threads:
        t.start()
    t0[0] = time.perf_counter()
    barrier.wait()
    for t in threads:
        t.join()
    total_ms = (time.perf_counter() - t0[0]) * 1000.0
    assert sum(done) == N_ITEMS, f"items processed {sum(done)} != {N_ITEMS}"
    return total_ms, finish, done


def main() -> None:
    total_work_ms = sum(cost(i) for i in range(N_ITEMS)) * 1000.0
    print(f"Student ID     : {STUDENT_ID}")
    print(f"Platform       : {platform.platform()} / {platform.machine()}")
    print(f"Python         : {platform.python_version()}")
    print(f"Items          : {N_ITEMS}, cost(i) = 0.0001 * (i % 20) seconds")
    print(f"Workers        : {WORKERS} threads")
    print(f"Repeats        : {REPEATS} runs per strategy (mean reported)")
    print(f"Total sleep    : {total_work_ms:.1f} ms  ->  ideal per worker {total_work_ms / WORKERS:.1f} ms")
    print()

    configs = [
        ("A: Static blocks (250/worker)", "static", 1),
        ("B: Dynamic queue, chunk=1", "dynamic", 1),
        ("B: Dynamic queue, chunk=5", "dynamic", 5),
    ]

    header = (f"{'Strategy':<30} | {'Total (ms)':>10} | {'First done':>10} | "
              f"{'Last done':>10} | {'Delta (ms)':>10}")
    print(header)
    print("-" * len(header))

    for label, strat, chunk in configs:
        run(strat, chunk)  # warm-up
        totals, firsts, lasts, deltas = [], [], [], []
        for _ in range(REPEATS):
            total, finish, _ = run(strat, chunk)
            totals.append(total)
            firsts.append(min(finish))
            lasts.append(max(finish))
            deltas.append(max(finish) - min(finish))
        print(f"{label:<30} | {statistics.mean(totals):>10.2f} | "
              f"{statistics.mean(firsts):>10.2f} | {statistics.mean(lasts):>10.2f} | "
              f"{statistics.mean(deltas):>10.2f}")

    print()
    print("Delta = time between the first and the last worker finishing "
          "(lower = better load balance).")
    print("Note: time.sleep has a minimum granularity, so absolute times exceed the ideal.")


if __name__ == "__main__":
    main()
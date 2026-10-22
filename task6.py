"""Task 6 - Synchronization Cost & Data Loss.

4 threads each increment a shared counter 2,000,000 times.
  1. Unsynchronized  -> lost updates (race condition)
  2. Lock-protected  -> correct, but slower

CPython's GIL makes a plain `c[0] += 1` almost race-free, so the
read-modify-write is split into read / call / write: the Python function
call is a point where the interpreter may switch threads, which exposes
the race exactly like a non-atomic increment in Java or C.
"""
import platform
import sys
import threading
import time

STUDENT_ID = 230103129
THREADS = 4
INCREMENTS = 2_000_000
EXPECTED = THREADS * INCREMENTS
UNSAFE_RUNS = 5
SAFE_RUNS = 3


def bump(v):
    return v + 1


def run(worker_factory):
    counter = [0]
    threads = [threading.Thread(target=worker_factory(counter)) for _ in range(THREADS)]
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return counter[0], (time.perf_counter() - start) * 1000.0


def unsafe_worker(counter):
    def work():
        for _ in range(INCREMENTS):
            v = counter[0]      # read
            v = bump(v)         # modify (thread switch can happen here)
            counter[0] = v      # write back (may overwrite another thread's update)
    return work


def plain_worker(counter):
    def work():
        for _ in range(INCREMENTS):
            counter[0] += 1
    return work


LOCK = threading.Lock()


def safe_worker(counter):
    def work():
        for _ in range(INCREMENTS):
            with LOCK:
                v = counter[0]
                v = bump(v)
                counter[0] = v
    return work


def lost_pct(actual):
    return (EXPECTED - actual) / EXPECTED * 100.0


def main() -> None:
    print(f"Student ID    : {STUDENT_ID}")
    print(f"Platform      : {platform.platform()} / {platform.machine()}")
    print(f"Python        : {platform.python_version()}")
    print(f"Threads       : {THREADS} x {INCREMENTS:,} increments")
    print(f"Switch interval: {sys.getswitchinterval()} s (default)")
    print(f"Expected final: {EXPECTED:,}")
    print()

    print("== Unsynchronized (read / call / write, no lock) ==")
    print(f"{'Run':>3} | {'Actual final':>13} | {'Lost updates':>13} | {'Lost %':>7} | {'Time (ms)':>10}")
    unsafe_times, unsafe_lost = [], []
    for r in range(1, UNSAFE_RUNS + 1):
        actual, ms = run(unsafe_worker)
        unsafe_times.append(ms)
        unsafe_lost.append(lost_pct(actual))
        print(f"{r:>3} | {actual:>13,} | {EXPECTED - actual:>13,} | {lost_pct(actual):>6.2f}% | {ms:>10.1f}")
    mean_unsafe = sum(unsafe_times) / len(unsafe_times)
    print(f"Mean lost updates: {sum(unsafe_lost) / len(unsafe_lost):.2f}%   "
          f"(min {min(unsafe_lost):.2f}%, max {max(unsafe_lost):.2f}%)")
    print()

    print("== Synchronized (threading.Lock around the whole increment) ==")
    print(f"{'Run':>3} | {'Actual final':>13} | {'Lost %':>7} | {'Time (ms)':>10}")
    safe_times = []
    for r in range(1, SAFE_RUNS + 1):
        actual, ms = run(safe_worker)
        assert actual == EXPECTED, f"lock version lost updates: {actual}"
        safe_times.append(ms)
        print(f"{r:>3} | {actual:>13,} | {lost_pct(actual):>6.2f}% | {ms:>10.1f}")
    mean_safe = sum(safe_times) / len(safe_times)
    print()

    print("== Synchronization cost ==")
    print(f"Mean time, no lock : {mean_unsafe:>10.1f} ms")
    print(f"Mean time, Lock    : {mean_safe:>10.1f} ms")
    print(f"Time penalty       : {mean_safe - mean_unsafe:>10.1f} ms "
          f"({mean_safe / mean_unsafe:.2f}x slower, +{(mean_safe / mean_unsafe - 1) * 100:.0f}%)")
    print()

    plain_actual, _ = run(plain_worker)
    print(f"Extra check: plain `counter[0] += 1` without lock -> final {plain_actual:,} "
          f"(lost {lost_pct(plain_actual):.2f}%)")
    print("The GIL makes a single-statement increment hard to interrupt in CPython;")
    print("the read/call/write version above is the equivalent of a non-atomic increment.")


if __name__ == "__main__":
    main()
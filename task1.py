"""Task 1 - Hardware Probe & Serial Baseline."""
import os
import platform
import time

import numpy as np

# >>> SET YOUR STUDENT ID HERE (digits only, used as the RNG seed) <<<
STUDENT_ID = 230103129

N = 20_000_000


def cpu_model() -> str:
    """Best-effort CPU model string across Linux / macOS / Windows."""
    try:
        if platform.system() == "Linux":
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if line.lower().startswith("model name"):
                        return line.split(":", 1)[1].strip()
        elif platform.system() == "Darwin":
            import subprocess
            return subprocess.check_output(
                ["sysctl", "-n", "machdep.cpu.brand_string"], text=True
            ).strip()
    except Exception:
        pass
    return platform.processor() or platform.machine()


def main() -> None:
    print(f"Student ID       : {STUDENT_ID}")
    print(f"OS               : {platform.system()} {platform.release()} ({platform.version()})")
    print(f"CPU model        : {cpu_model()}")
    print(f"Platform         : {platform.platform()} / {platform.machine()}")
    print(f"Python           : {platform.python_version()}")
    print(f"Logical cores    : {os.cpu_count()}")

    # Generate 20,000,000 float64 values, seeded by Student ID
    rng = np.random.default_rng(STUDENT_ID)
    data = rng.random(N, dtype=np.float64)
    print(f"Array            : {data.size:,} elements, dtype={data.dtype}, seed={STUDENT_ID}")

    # Serial computation (single thread): sum, then population std dev
    start = time.perf_counter()
    total = float(np.sum(data))
    mean = total / N
    variance = float(np.sum((data - mean) ** 2)) / N
    std = variance ** 0.5
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    print(f"Sum              : {total:.6f}")
    print(f"Std deviation    : {std:.9f}")
    print(f"Serial time (ms) : {elapsed_ms:.3f}")


if __name__ == "__main__":
    main()

# Task 05: Deconstructing the "Amdahl's Pessimism" Fallacy

## 1. Introduction

In 1988, John L. Gustafson, Gary R. Montry, and Robert E. Benner published research demonstrating the capabilities of a 1024-processor hypercube computer at Sandia National Laboratories.

Their work challenged the common interpretation of Amdahl's Law, which suggests that even a small serial fraction can severely limit the benefits of massively parallel computing.

The researchers demonstrated speedups exceeding 1000 times for scaled scientific workloads. Their findings showed that the fixed-size assumption behind traditional speedup measurements does not always represent how scientific computing is performed in practice.

The main historical sources are:

- Gustafson, J. L. (1988). *Reevaluating Amdahl's Law*. Communications of the ACM, 31(5), 532–533. https://doi.org/10.1145/42411.42415
- Gustafson, J. L., Montry, G. R., & Benner, R. E. (1988). *Development of Parallel Methods for a 1024-Processor Hypercube*. SIAM Journal on Scientific and Statistical Computing, 9(4), 609–638. https://doi.org/10.1137/0909041

## 2. Historical Experimental Environment

The experiment was conducted at Sandia National Laboratories using the NCUBE/ten parallel computer, configured as a 1024-processor MIMD hypercube.

Important hardware characteristics included:

- 1024 autonomous processor nodes.
- 512 KB of memory per node.
- Distributed-memory architecture.
- Explicit communication through interprocessor channels.
- Support for 32-bit and 64-bit floating-point operations.

Unlike a shared-memory computer, the hypercube required processors to exchange information explicitly. Therefore, communication overhead and synchronization were important parts of the experiment.

The research focused on three practical scientific applications:

1. Wave mechanics using explicit finite differences.
2. Unstable fluid dynamics using Flux Corrected Transport (FCT).
3. Beam strain analysis using finite elements and the conjugate gradient method.

These were full-scale scientific applications rather than artificial tests designed only to demonstrate processor speed.

## 3. The Apparent Conflict with Amdahl's Law

Amdahl's Law assumes a fixed problem size. Its speedup equation is:

\[
S_A(P)=\frac{1}{s+\frac{1-s}{P}}
\]

For illustration, assume a serial fraction of 0.4%:

\[
s=0.004
\]

With 1024 processors:

\[
S_A(1024)=\frac{1}{0.004+\frac{0.996}{1024}}
\]

\[
S_A(1024)=\frac{1}{0.00497265625}
\]

\[
\boxed{S_A(1024)\approx201.10}
\]

This theoretical result is far below 1000 times speedup.

However, the calculation assumes that the original workload remains unchanged when additional processors are introduced.

The researchers argued that this assumption was not always suitable for scientific computing. When more computing resources become available, scientists often increase the size or resolution of their simulations rather than simply completing the same small problem faster.

## 4. Problem Expansion and Scaled Speedup

The researchers considered a different performance measurement: keeping the parallel execution time approximately constant while increasing the problem size with the number of processors.

Gustafson's scaled speedup formula is:

\[
S_G(P)=P-\alpha(P-1)
\]

where:

- \(P\) is the number of processors.
- \(\alpha\) is the serial fraction measured on the parallel machine.

The 1988 paper reported that the 1024-processor ensemble achieved:

- 502 to 637 times speedup for fixed-size problems.
- 1009 to 1020 times speedup for scaled problems.

This comparison demonstrated that the choice of workload model significantly affects the measured performance of a parallel system.

## 5. Detailed Example: The WAVE Application

One particularly useful example in the original research is the WAVE program, which simulated a two-dimensional wave mechanics problem.

The scaled problem contained a grid of:

\[
6144\times6144
\]

With 1024 processors, each processor handled a subdomain of:

\[
192\times192
\]

The full problem required approximately 340 MB for its data structures alone, making it impractical to execute on a single processor in that configuration.

The researchers measured a total parallel execution time of approximately 10,000 seconds. Of this time, approximately 40 seconds represented work that would not be required by a serial processor.

The parallel fraction was therefore:

\[
p=1-\frac{40}{10000}
\]

\[
p=0.996
\]

The scaled speedup was calculated as:

\[
S_G(1024)=1024(0.996)
\]

\[
\boxed{S_G(1024)=1019.904\approx1020}
\]

This example shows how a large scientific workload can achieve speedup exceeding 1000 times when its size is scaled to use the available processors.

## 6. Important Experimental Techniques

Achieving high speedup required more than simply adding processors. The researchers used several techniques to reduce parallel overhead.

### 6.1 Communication Overlap

Communication was organized so that data transfers could overlap with computation. This reduced the amount of time processors spent waiting for messages.

### 6.2 Efficient Message Handling

The researchers carefully organized message transfers and synchronization to reduce communication delays and message startup costs.

### 6.3 Load Balancing

Work was distributed among processors to reduce situations where some processors remained idle while others continued computing.

### 6.4 Reduction of Sequential Dependencies

The algorithms were designed to minimize operations that had to be performed sequentially.

### 6.5 Operation Efficiency

The researchers introduced operation efficiency to measure the relationship between the work performed by the parallel algorithm and the operation count of the best serial algorithm.

This was important because parallel algorithms can perform additional operations to reduce communication or improve coordination.

## 7. Historical Results and Their Interpretation

The original SIAM paper reported the following results:

| Measurement | Reported speedup |
|---|---:|
| Fixed-size problems | 502–637× |
| Scaled problems | 1009–1020× |
| Processor count | 1024 |

The researchers also reported sustained performance between 70 and 130 MFLOPS across the applications.

These results demonstrated that massively parallel computing could be practical for real scientific applications.

An important qualification is that the original paper reported different serial-component measurements for fixed and scaled workloads. It reported 0.0006–0.001 for the fixed-size measurements and 3–10 parts per million for the scaled measurements. These figures should not be confused with the simplified 0.4% illustration used in this practice task.

## 8. Why Problem Expansion Changes the Conclusion

The main difference between the two approaches is the behavior of the workload.

Amdahl's Law evaluates how much faster the same problem can be completed when more processors are added. Its fixed-size assumption means that the serial portion eventually limits speedup.

Gustafson's approach evaluates how much larger a problem can be solved in approximately the same amount of time. The parallel workload increases as additional processors become available.

Therefore, the scaled speedup can grow substantially without requiring the serial fraction to dominate the overall execution time.

The experiment did not invalidate Amdahl's mathematical result. Instead, it demonstrated that fixed-size speedup is not the only meaningful way to evaluate parallel computing performance.

## 9. Conclusion

The 1988 Sandia experiment was an important demonstration of the potential of massively parallel computing.

Using a 1024-processor NCUBE/ten hypercube, Gustafson, Montry, and Benner achieved scaled speedups between 1009 and 1020 times for three practical scientific applications.

The central lesson is that parallel performance must be evaluated in relation to the problem being solved. When the workload grows with the available processing capacity, fixed-size speedup alone may underestimate the practical value of a parallel system.

Gustafson's Law therefore provides a useful framework for understanding weak scaling and the performance potential of large parallel systems.

## 10. References

1. Gustafson, J. L. (1988). Reevaluating Amdahl's Law. *Communications of the ACM, 31*(5), 532–533. https://doi.org/10.1145/42411.42415

2. Gustafson, J. L., Montry, G. R., & Benner, R. E. (1988). Development of parallel methods for a 1024-processor hypercube. *SIAM Journal on Scientific and Statistical Computing, 9*(4), 609–638. https://doi.org/10.1137/0909041
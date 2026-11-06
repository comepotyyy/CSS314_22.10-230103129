# Task 01: Strong Scaling vs. Weak Scaling Foundations

## 1. Introduction

Parallel computing allows a computational problem to be divided among multiple processors to improve performance. Two important theoretical models used to understand parallel performance are Amdahl's Law and Gustafson's Law.

Although both models examine the relationship between processor count and speedup, they use different assumptions about problem size and execution time.

## 2. Amdahl's Law (1967)

Gene Amdahl introduced Amdahl's Law in 1967. This model focuses on improving the execution time of a fixed-size problem by increasing the number of processors.

The main assumption is that the total workload remains constant. A program consists of two parts:

- Serial portion (s): operations that cannot be executed simultaneously.
- Parallel portion (1-s): operations that can be distributed across multiple processors.

The mathematical formulation is:

\[
S_A(P)=\frac{1}{s+\frac{1-s}{P}}
\]

Where P represents the number of processors and s represents the serial fraction.

As the number of processors increases, the parallel portion becomes faster. However, the serial portion remains unchanged and limits the maximum possible speedup.

When P approaches infinity:

\[
\lim_{P\to\infty}S_A(P)=\frac{1}{s}
\]

Therefore, Amdahl's Law demonstrates that adding processors cannot eliminate the limitations caused by serial execution.

Under this model, the problem dimension remains constant:

\[
N(P)=N_0
\]

This approach is called **strong scaling or fixed-size scaling**, because the same computational problem is distributed across an increasing number of processors.

## 3. Gustafson's Law (1988)

John Gustafson introduced Gustafson's Law in 1988 as an alternative perspective on parallel computing performance.

Instead of keeping the problem size constant, Gustafson proposed increasing the workload as more processors become available.

The main objective is to solve larger computational problems while maintaining approximately constant execution time.

Its mathematical formulation is:

\[
S_G(P)=P-\alpha(P-1)
\]

Where:
- P is the number of processors.
- α is the serial fraction measured during parallel execution.

The model assumes that the serial portion remains relatively small while the parallel workload expands with the number of processors.

Rearranging the equation:

\[
S_G(P)=\alpha+(1-\alpha)P
\]

As P approaches infinity:

\[
\lim_{P\to\infty}S_G(P)=\infty
\]

For a fixed α smaller than 1, the theoretical scaled speedup increases approximately linearly with the number of processors.

The total workload can be represented as:

\[
W(P)=P\cdot W(1)
\]

This is called **weak scaling or fixed-time scaling**, because the workload increases while the execution time is approximately maintained.

For a uniformly scaled d-dimensional problem, the dimension of each side can grow as:

\[
N(P)=N_0P^{1/d}
\]

## 4. Comparison of Both Models

| Characteristic | Amdahl's Law | Gustafson's Law |
|---|---|---|
| Year | 1967 | 1988 |
| Scaling approach | Strong scaling | Weak scaling |
| Problem size | Fixed | Increasing |
| Execution time | Decreases | Approximately constant |
| Main objective | Execute the same task faster | Execute a larger task |
| Serial fraction | Fixed-size reference | Observed parallel execution |
| Speedup limitation | Limited by serial fraction | Can grow approximately linearly |

## 5. Philosophical and Physical Differences

The fundamental difference between these models is how they interpret the benefits of additional processing resources.

Amdahl's Law considers additional processors as a way to accelerate an existing computational task. Its main concern is the portion of the program that cannot be parallelized. Even if thousands of processors are available, serial operations remain a limiting factor.

Gustafson's Law considers additional processors an opportunity to solve more complex and larger problems. Instead of expecting the same workload to finish significantly faster, it assumes that computational requirements can increase alongside available processing resources.

From a practical perspective, Amdahl's model is relevant when the problem size cannot be changed, such as processing a fixed dataset. Gustafson's model is particularly useful in scientific simulations, weather forecasting, and large-scale data processing, where researchers can increase the problem size to benefit from additional computational power.

## 6. Conclusion

Amdahl's Law and Gustafson's Law provide two different perspectives on parallel computing performance.

Amdahl's Law demonstrates the limitations of parallelization when the problem size remains constant. Gustafson's Law demonstrates the potential of parallel systems when computational workloads increase with processor count.

Understanding both models is important when designing parallel applications because the appropriate scaling strategy depends on the nature of the computational problem and the available hardware resources.SS
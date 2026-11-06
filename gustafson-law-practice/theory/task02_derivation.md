# Task 02: Formal Derivation of Gustafson's Scaled Speedup

## 1. Introduction

Gustafson's Law describes the potential performance improvement of parallel computing systems when the problem size increases with the number of available processors.

Unlike fixed-size scaling, this model assumes that the parallel execution time remains normalized while the total computational workload grows.

The objective of this derivation is to obtain the formula:

\[
S(P)=P-\alpha(P-1)
\]

from the basic principles of parallel execution.

## 2. Normalization of Parallel Execution Time

Let a parallel program consist of two components:

- s: serial execution time.
- p: parallel execution time.

The total parallel execution time is normalized to one:

\[
s+p=1
\]

Therefore, the parallel execution time on P processors is:

\[
T_P=s+p=1
\]

The serial and parallel fractions can also be expressed as:

\[
p=1-s
\]

This normalization provides a convenient reference for comparing parallel and equivalent serial execution.

## 3. Determining the Equivalent Serial Workload

To calculate scaled speedup, we first determine how long the equivalent expanded workload would take on a single processor.

The serial portion requires time s and cannot be distributed across multiple processors.

However, the parallel portion represents work distributed across P processors. Assuming equal workload distribution and ideal parallel execution, the total equivalent serial time of this portion is P multiplied by p.

Therefore, the equivalent serial execution time is:

\[
T_1=s+Pp
\]

This represents the total computational work performed by the parallel system, expressed as equivalent single-processor execution time.

## 4. Derivation of the Scaled Speedup Formula

Speedup is defined as the ratio of serial execution time to parallel execution time:

\[
S(P)=\frac{T_1}{T_P}
\]

Substituting the previously derived expressions:

\[
S(P)=\frac{s+Pp}{1}
\]

Since the normalized parallel execution time equals one:

\[
\boxed{S(P)=s+Pp}
\]

This is the first form of Gustafson's scaled speedup equation.

## 5. Mathematical Proof of the Equivalent Formula

From the normalization condition:

\[
s+p=1
\]

We obtain:

\[
p=1-s
\]

Substituting this expression into the scaled speedup formula:

\[
S(P)=s+P(1-s)
\]

Expanding the equation:

\[
S(P)=s+P-Ps
\]

Rearranging:

\[
S(P)=P-s(P-1)
\]

If the serial fraction is represented by α, where α = s, the final expression becomes:

\[
\boxed{S(P)=P-\alpha(P-1)}
\]

Thus, both expressions are mathematically equivalent:

\[
\boxed{S(P)=s+pP=P-\alpha(P-1)}
\]

## 6. Numerical Verification

Consider a parallel application with the following parameters:

- Number of processors: P = 8.
- Serial fraction: s = 0.1.
- Parallel fraction: p = 0.9.

Using the first expression:

\[
S(8)=s+pP
\]

\[
S(8)=0.1+(0.9\times8)
\]

\[
S(8)=7.3
\]

Using the second expression:

\[
S(8)=P-\alpha(P-1)
\]

\[
S(8)=8-0.1(8-1)
\]

\[
S(8)=8-0.7=7.3
\]

Both calculations produce the same result, confirming the mathematical equivalence of the two formulations.

## 7. Conclusion

The derivation demonstrates that Gustafson's scaled speedup formula can be obtained by comparing the equivalent serial execution time of an expanded workload with its normalized parallel execution time.

The key idea is that increasing the number of processors allows the parallel portion of the workload to grow while maintaining approximately constant parallel execution time.

The final equation is:

\[
\boxed{S(P)=P-\alpha(P-1)}
\]

This formula provides a theoretical foundation for understanding weak scaling and the performance potential of large parallel computing systems.

The derivation assumes ideal workload distribution and does not explicitly include additional communication, synchronization, or processor-management overhead.
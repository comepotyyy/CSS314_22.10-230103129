# Task 04: Asymptotic Analysis of Parallel Efficiency

## 1. Introduction

Parallel efficiency measures how effectively a parallel system uses its available processors. It is calculated by dividing speedup by the number of processors.

\[
E(P)=\frac{S(P)}{P}
\]

This task analyzes the asymptotic behavior of efficiency under Gustafson's Law and compares it with Amdahl's Law as the processor count approaches infinity.

## 2. Efficiency Under Gustafson's Law

Gustafson's scaled speedup is:

\[
S_G(P)=P-\alpha(P-1)
\]

Parallel efficiency is:

\[
E_G(P)=\frac{S_G(P)}{P}
\]

Substituting the speedup equation:

\[
E_G(P)=\frac{P-\alpha(P-1)}{P}
\]

Expanding the numerator:

\[
E_G(P)=\frac{P-\alpha P+\alpha}{P}
\]

Dividing each term by \(P\):

\[
\boxed{E_G(P)=1-\alpha+\frac{\alpha}{P}}
\]

### 2.1 Asymptotic Limit

To determine the limiting efficiency, consider:

\[
\lim_{P\to\infty}E_G(P)
=
\lim_{P\to\infty}\left(1-\alpha+\frac{\alpha}{P}\right)
\]

For a constant serial fraction \(\alpha\):

\[
\lim_{P\to\infty}\frac{\alpha}{P}=0
\]

Therefore:

\[
\boxed{\lim_{P\to\infty}E_G(P)=1-\alpha}
\]

This means that efficiency approaches the parallel fraction of the workload. Under Gustafson's assumptions, efficiency does not necessarily approach zero as more processors are added.

## 3. Efficiency Under Amdahl's Law

Amdahl's speedup formula is:

\[
S_A(P)=\frac{1}{s+\frac{1-s}{P}}
\]

Efficiency is calculated as:

\[
E_A(P)=\frac{S_A(P)}{P}
\]

Substituting:

\[
E_A(P)=\frac{1}{P\left(s+\frac{1-s}{P}\right)}
\]

Simplifying:

\[
\boxed{E_A(P)=\frac{1}{sP+1-s}}
\]

### 3.1 Asymptotic Limit

Consider the limit:

\[
\lim_{P\to\infty}E_A(P)
=
\lim_{P\to\infty}\frac{1}{sP+1-s}
\]

For any positive serial fraction \(s>0\), the denominator increases without bound.

Consequently:

\[
\boxed{\lim_{P\to\infty}E_A(P)=0}
\]

This demonstrates that efficiency approaches zero under Amdahl's fixed-size model when the serial fraction is nonzero.

A special case occurs when \(s=0\). In that situation, the entire workload is parallelizable and efficiency remains equal to 1.

## 4. Comparative Analysis

| Metric | Gustafson's Law | Amdahl's Law |
|---|---|---|
| Efficiency equation | \(1-\alpha+\alpha/P\) | \(1/(sP+1-s)\) |
| Limiting efficiency | \(1-\alpha\) | 0, for \(s>0\) |
| Workload assumption | Scaled problem size | Fixed problem size |
| Main interpretation | Efficiency approaches the parallel fraction | Efficiency decreases as processor count grows |

The two models produce different asymptotic results because they describe different workload conditions.

Gustafson's Law assumes that the problem size increases with the number of processors. The parallel portion therefore continues to provide enough work to utilize the additional processing capacity.

Amdahl's Law assumes that the total problem size remains unchanged. As the number of processors increases, the parallel portion becomes faster, but the serial portion cannot be divided among processors. Eventually, adding processors provides progressively smaller benefits.

## 5. Numerical Illustration

Consider a serial fraction of 4%:

\[
\alpha=s=0.04
\]

Under Gustafson's Law:

\[
\lim_{P\to\infty}E_G(P)=1-0.04
\]

\[
\boxed{E_G(\infty)=0.96=96\%}
\]

Under Amdahl's Law:

\[
\boxed{E_A(\infty)=0\%}
\]

The results illustrate the difference between scaled and fixed-size workloads. The 96% result is an ideal theoretical limit and does not guarantee that a real parallel system will achieve this efficiency.

## 6. Conclusion

The asymptotic analysis demonstrates that Gustafson's Law and Amdahl's Law predict different efficiency limits.

Under Gustafson's formulation, efficiency approaches \(1-\alpha\), where \(\alpha\) is the serial fraction measured on the parallel machine. Under Amdahl's formulation, efficiency approaches zero for a fixed-size workload with a nonzero serial fraction.

The main lesson is that processor efficiency cannot be evaluated independently of workload behavior. Scaled workloads can maintain high theoretical efficiency, while fixed workloads experience decreasing efficiency as processor counts become very large.
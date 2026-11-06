# Task 03: The Serial Fraction Invariance Paradox

## 1. Introduction

Amdahl's Law and Gustafson-Barsis's Law describe parallel speedup using different assumptions about workload size and the measurement of serial execution time.

The apparent contradiction occurs because Amdahl's Law measures the serial fraction on a single processor, while Gustafson's Law measures it on the parallel machine. Understanding this difference is essential for explaining why Gustafson's model predicts substantial speedup even when the number of processors becomes very large.

## 2. Amdahl's Law: Serial Fraction on a Uniprocessor

Amdahl's Law considers a fixed-size problem. The serial fraction is measured using the total execution time on one processor.

Let:

- \(T_s\) = serial execution time.
- \(T_p\) = parallelizable execution time on one processor.
- \(T_1=T_s+T_p\) = total single-processor execution time.
- \(P\) = number of processors.

The serial fraction is:

\[
s=\frac{T_s}{T_s+T_p}
\]

Assuming ideal parallelization, the execution time on \(P\) processors is:

\[
T_P=T_s+\frac{T_p}{P}
\]

Therefore, Amdahl's speedup is:

\[
S_A(P)=\frac{1}{s+\frac{1-s}{P}}
\]

When the processor count approaches infinity:

\[
\lim_{P\to\infty}S_A(P)=\frac{1}{s}
\]

This demonstrates that the original serial fraction places an upper limit on speedup for a fixed-size workload.

## 3. Gustafson-Barsis's Law: Serial Fraction on the Parallel Machine

Gustafson's approach considers a scaled workload. Instead of keeping the total problem size fixed, the amount of parallel work increases as more processors become available.

The serial fraction is measured using the actual execution time on the parallel machine:

\[
\alpha=\frac{T_s}{T_s+T_{parallel}(P)}
\]

For a normalized parallel execution time of 1:

\[
T_s=\alpha
\]

\[
T_{parallel}(P)=1-\alpha
\]

The equivalent serial execution time for the scaled workload is:

\[
T_1^{scaled}=\alpha+P(1-\alpha)
\]

Consequently, Gustafson's scaled speedup is:

\[
S_G(P)=\alpha+P(1-\alpha)
\]

or equivalently:

\[
S_G(P)=P-\alpha(P-1)
\]

The serial fraction is not eliminated. However, the workload is expanded so that the parallel portion can make effective use of the additional processors.

## 4. Analytical Relationship Between the Two Models

The distinction can be demonstrated mathematically by considering a fixed workload and measuring its serial fraction on \(P\) processors.

For ideal parallel execution:

\[
\alpha(P)=\frac{T_s}{T_s+\frac{T_p}{P}}
\]

Since:

\[
s=\frac{T_s}{T_s+T_p}
\]

the serial fraction measured on the parallel machine becomes:

\[
\alpha(P)=\frac{sP}{1-s+sP}
\]

Substituting this expression into Gustafson's speedup equation:

\[
S_G(P)=\alpha(P)+P(1-\alpha(P))
\]

\[
S_G(P)=\frac{sP}{1-s+sP}
+\frac{P(1-s)}{1-s+sP}
\]

Combining the terms:

\[
S_G(P)=\frac{sP+P(1-s)}{1-s+sP}
\]

Therefore:

\[
\boxed{S_G(P)=\frac{P}{1-s+sP}}
\]

Amdahl's speedup can also be written as:

\[
S_A(P)=\frac{1}{s+\frac{1-s}{P}}
\]

Multiplying the numerator and denominator by \(P\):

\[
\boxed{S_A(P)=\frac{P}{sP+1-s}}
\]

Both expressions are identical because:

\[
1-s+sP=sP+1-s
\]

Thus, when the workload and measurement reference are consistent, the two formulations produce the same speedup for this idealized fixed-size case.

## 5. Why the Apparent Contradiction Is Resolved

The apparent contradiction is caused by comparing two different scaling scenarios.

Amdahl's Law assumes that the total problem size remains fixed. As processors are added, the parallel portion becomes smaller in execution time, but the serial portion remains unchanged. Consequently, the serial fraction measured against the original single-processor execution time limits the maximum speedup.

Gustafson's Law assumes that the workload grows with the number of processors while parallel execution time remains approximately constant. Its serial fraction is measured relative to the parallel machine's execution time for this larger workload.

Therefore, a relatively small serial fraction can remain compatible with substantial scaled speedup. This does not mean serial work disappears or that every application can scale indefinitely. It means that the parallel workload grows enough to keep the serial portion relatively small under the model's assumptions.

## 6. Conclusion

The Serial Fraction Invariance Paradox is resolved by distinguishing the measurement reference and workload assumptions of the two laws.

Amdahl's serial fraction is measured on a uniprocessor system and applies to a fixed-size workload. Gustafson's serial fraction is measured on a parallel machine executing a scaled workload.

The mathematical relationship also shows that the two laws are not inherently contradictory: with consistent workload assumptions and an appropriately measured serial fraction, their speedup expressions agree.

The practical lesson is that parallel performance should be evaluated in relation to the workload being executed. A fixed-size problem and a scaled-size problem can produce very different conclusions about the benefits of additional processors.
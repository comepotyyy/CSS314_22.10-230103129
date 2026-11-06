# Task 08: Cross-Over Point Determination (Amdahl vs. Gustafson)

## 1. Objective

The purpose of this task is to compare the theoretical speedup predicted by Amdahl's Law and Gustafson's Law for the same serial fraction and processor count.

The comparison helps explain how different workload assumptions influence the expected performance of parallel systems.

## 2. Given Parameters

- Amdahl's serial fraction: s = 0.08
- Gustafson's parallel-machine serial fraction: α = 0.08
- Number of processors: P = 128

## 3. Amdahl's Law Calculation

Amdahl's Law is used for strong scaling, where the total problem size remains fixed.

The formula is:

SA(P) = 1 / [s + (1 − s) / P]

Substituting the given values:

SA(128) = 1 / [0.08 + (1 − 0.08) / 128]

SA(128) = 1 / [0.08 + 0.92 / 128]

SA(128) = 1 / [0.08 + 0.0071875]

SA(128) = 1 / 0.0871875

**SA(128) ≈ 11.469**

## 4. Gustafson's Law Calculation

Gustafson's Law is used for weak scaling, where the workload increases with the number of processors.

The formula is:

SG(P) = P − α(P − 1)

Substituting the values:

SG(128) = 128 − 0.08(128 − 1)

SG(128) = 128 − 0.08 × 127

SG(128) = 128 − 10.16

**SG(128) = 117.84**

## 5. Percentage Discrepancy

To compare the two predictions, Amdahl's speedup is used as the reference value.

The percentage discrepancy is:

D = [(SG − SA) / SA] × 100

Substituting the calculated results:

D = [(117.84 − 11.469) / 11.469] × 100

**D ≈ 927.4%**

The ratio between the two predicted speedups is:

SG / SA = 117.84 / 11.469

**SG / SA ≈ 10.274**

Therefore, Gustafson's predicted speedup is approximately 10.27 times the speedup predicted by Amdahl's Law.

## 6. Comparative Analysis

The difference between the results comes mainly from the workload assumptions of the two models.

Amdahl's Law assumes that the total problem size is fixed. Increasing the number of processors reduces the parallel execution time, but the serial portion remains a limitation. For a serial fraction of 8%, the theoretical maximum speedup is:

SA(max) = 1 / 0.08 = **12.5**

Gustafson's Law considers a different situation. The workload grows with the number of processors, while the parallel execution time is assumed to remain approximately constant. This allows the system to perform more work as additional processing resources become available.

For the given configuration, Gustafson's Law predicts a speedup of 117.84, which is considerably higher than Amdahl's prediction of approximately 11.469.

These results do not mean that one law is universally more accurate than the other. They describe different scaling scenarios.

## 7. Conclusion

For 128 processors and a serial fraction of 8%, Amdahl's Law predicts a speedup of approximately 11.469, while Gustafson's Law predicts a scaled speedup of 117.84.

The percentage discrepancy, using Amdahl's result as the reference, is approximately 927.4%.

The comparison demonstrates why workload assumptions are important when evaluating parallel systems. Amdahl's Law is useful when the problem size remains fixed, while Gustafson's Law is more suitable when the workload expands with available processing resources.
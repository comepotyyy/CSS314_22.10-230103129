# Task 06: Parametric Speedup Across Processor Densities

## 1. Objective

The purpose of this task is to calculate the theoretical scaled speedup and parallel efficiency of an application with a serial execution fraction of 4%.

The calculations are performed for six processor configurations: 16, 64, 256, 1,024, 4,096, and 16,384 processors.

The analysis uses Gustafson's Law, which assumes that the workload increases with the number of processors while parallel execution time remains approximately constant.

## 2. Given Parameters

- Serial fraction: α = 0.04
- Parallel fraction: 1 − α = 0.96
- Processor counts: P = 16, 64, 256, 1,024, 4,096, 16,384

## 3. Mathematical Formulation

Gustafson's scaled speedup formula is:

S(P) = P − α(P − 1)

Substituting α = 0.04:

S(P) = P − 0.04(P − 1)

Simplifying:

**S(P) = 0.96P + 0.04**

Parallel efficiency is calculated as:

E(P) = S(P) / P

Therefore:

**E(P) = 0.96 + 0.04/P**

Efficiency is expressed as a percentage by multiplying the result by 100.

## 4. Worked Calculations

### Example 1: P = 16

Scaled speedup:

S(16) = 16 − 0.04(16 − 1)

S(16) = 16 − 0.60

S(16) = **15.40**

Parallel efficiency:

E(16) = 15.40 / 16

E(16) = 0.9625

E(16) = **96.25%**

### Example 2: P = 64

S(64) = 64 − 0.04(63)

S(64) = 64 − 2.52

S(64) = **61.48**

E(64) = 61.48 / 64

E(64) = **96.0625%**

### Remaining Calculations

For P = 256:

S(256) = 256 − 0.04(255) = **245.80**

E(256) = 245.80 / 256 = **96.015625%**

For P = 1,024:

S(1,024) = 1,024 − 0.04(1,023) = **983.08**

E(1,024) = 983.08 / 1,024 = **96.00390625%**

For P = 4,096:

S(4,096) = 4,096 − 0.04(4,095) = **3,932.20**

E(4,096) = 3,932.20 / 4,096 = **96.0009765625%**

For P = 16,384:

S(16,384) = 16,384 − 0.04(16,383) = **15,728.68**

E(16,384) = 15,728.68 / 16,384 = **96.000244140625%**

## 5. Complete Calculation Table

| Processor count (P) | Scaled speedup S(P) | Efficiency E(P) |
|---:|---:|---:|
| 16 | 15.40 | 96.2500% |
| 64 | 61.48 | 96.0625% |
| 256 | 245.80 | 96.0156% |
| 1,024 | 983.08 | 96.0039% |
| 4,096 | 3,932.20 | 96.0010% |
| 16,384 | 15,728.68 | 96.0002% |

## 6. Numerical Observations

The results show that scaled speedup increases as the processor count increases. For example, increasing the processor count from 16 to 16,384 increases the theoretical speedup from 15.40 to 15,728.68.

Parallel efficiency behaves differently. It starts at 96.25% with 16 processors and gradually approaches 96% as the processor count grows.

This happens because the efficiency formula can be written as:

E(P) = 0.96 + 0.04/P

As P becomes larger, the term 0.04/P approaches zero. Consequently:

lim E(P) = 0.96, as P → ∞

This means that the theoretical efficiency approaches 96%, rather than falling toward zero.

The small reduction in efficiency does not indicate a major performance problem. It is the mathematical consequence of distributing the fixed 4% serial component across an increasingly large processor configuration.

## 7. Conclusion

The calculations demonstrate the main advantage of Gustafson's Law under weak-scaling conditions. When the workload grows with the available processing resources, high parallel efficiency can be maintained even at very large processor counts.

For the given application, theoretical efficiency remains close to 96% across all six configurations. Meanwhile, scaled speedup increases almost proportionally to the number of processors.

However, these values are theoretical. Real distributed systems may experience communication overhead, synchronization delays, memory limitations, and load imbalance, which can reduce actual efficiency.

Therefore, the results represent an idealized weak-scaling model rather than measured hardware performance.
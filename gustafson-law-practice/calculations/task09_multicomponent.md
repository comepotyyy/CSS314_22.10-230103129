# Task 09: Multi-Component Workload Partitioning

## 1. Objective

The objective of this task is to analyze a scientific simulation consisting of three computational phases. The goal is to identify the aggregate serial fraction and calculate the theoretical scaled speedup for two different processor configurations using Gustafson's Law.

## 2. Given Parameters

The simulation contains the following phases:

| Phase | Description | Execution time |
|---|---|---:|
| A | Initial disk I/O and parameter broadcast | 2% |
| B | Boundary message-passing synchronization | 6% |
| C | Core domain flux computation | 92% |
| **Total** | | **100%** |

The required processor configurations are:

- P = 512
- P = 2,048

For this simplified calculation, phases A and B are treated as serial overhead, while phase C represents parallel computation.

## 3. Aggregate Serial Fraction

The aggregate serial fraction is obtained by adding the two overhead components:

α = A + B

α = 0.02 + 0.06

**α = 0.08 = 8%**

The parallel fraction is:

p = 1 − α

p = 1 − 0.08

**p = 0.92 = 92%**

Therefore, 8% of the normalized execution time is treated as serial overhead, while 92% is available for parallel computation.

## 4. Gustafson's Law

The scaled speedup formula is:

S(P) = P − α(P − 1)

Substituting the aggregate serial fraction:

**S(P) = P − 0.08(P − 1)**

### 4.1. Speedup with 512 processors

S(512) = 512 − 0.08(512 − 1)

S(512) = 512 − 0.08 × 511

S(512) = 512 − 40.88

**S(512) = 471.12**

### 4.2. Speedup with 2,048 processors

S(2,048) = 2,048 − 0.08(2,048 − 1)

S(2,048) = 2,048 − 0.08 × 2,047

S(2,048) = 2,048 − 163.76

**S(2,048) = 1,884.24**

## 5. Parallel Efficiency

Parallel efficiency is calculated as:

E(P) = S(P) / P

For 512 processors:

E(512) = 471.12 / 512

**E(512) ≈ 92.0156%**

For 2,048 processors:

E(2,048) = 1,884.24 / 2,048

**E(2,048) ≈ 92.0039%**

## 6. Results Table

| Metric | 512 processors | 2,048 processors |
|---|---:|---:|
| Serial fraction | 8% | 8% |
| Parallel fraction | 92% | 92% |
| Scaled speedup | 471.12 | 1,884.24 |
| Parallel efficiency | 92.0156% | 92.0039% |

## 7. Analysis

The calculations show that the aggregate serial fraction is 8%, consisting of the initial I/O and parameter broadcast phase (2%) and boundary message-passing synchronization (6%).

When the processor count increases from 512 to 2,048, the theoretical scaled speedup increases from 471.12 to 1,884.24. This is approximately a fourfold increase in speedup for a fourfold increase in processor count.

Parallel efficiency remains close to 92% in both configurations. The slight decrease occurs because the serial fraction is distributed across a larger processor count in the efficiency formula.

The results illustrate how Gustafson's Law predicts effective scaling when the workload grows with available processing resources.

One limitation is that the assignment provides normalized phase percentages but does not specify whether all synchronization and communication costs remain constant as the system grows. In a real distributed simulation, these costs may increase with processor count and reduce actual performance.

## 8. Conclusion

The aggregate serial fraction of the simulation is **8%**, and its parallel fraction is **92%**.

Using Gustafson's Law, the theoretical scaled speedup is **471.12** with 512 processors and **1,884.24** with 2,048 processors.

The results demonstrate that a workload with a relatively small serial fraction can maintain high theoretical parallel efficiency under weak-scaling assumptions.
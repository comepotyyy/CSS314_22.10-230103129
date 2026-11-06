# Task 11: Sun–Ni Memory-Bounded Speedup Model

## 1. Introduction

Amdahl's Law and Gustafson's Law describe parallel performance under different assumptions about workload size. Amdahl's Law considers a fixed problem size, while Gustafson's Law assumes that the workload increases with the number of processors so that execution time remains approximately constant.

However, in real parallel systems, the amount of work that can be processed is also influenced by available memory. Adding processors often means adding memory capacity, allowing larger datasets and problems to be processed.

To account for this relationship, Xian-He Sun and Lionel Ni introduced the memory-bounded speedup model. Their work was first presented in 1990 and developed further in their 1993 paper, *Scalable Problems and Memory-Bounded Speedup*.

The main idea is that workload growth should depend on how the problem's memory requirements change when system memory increases.

## 2. Mathematical formulation

The simplified Sun–Ni memory-bounded speedup model is:

\[
S_{SN}(P)=
\frac{\alpha+(1-\alpha)G(P)}
{\alpha+\frac{(1-\alpha)G(P)}{P}}
\]

Where:

- \(P\) is the number of processors.
- \(\alpha\) is the sequential fraction of the original workload.
- \(1-\alpha\) is the parallel fraction.
- \(G(P)\) represents the growth factor of the parallel workload when the system's memory capacity increases.

The function \(G(P)\) is important because it connects memory growth with problem-size growth. It is application-dependent and cannot always be assumed to equal the number of processors.

The numerator represents the time required by one processor to solve the scaled workload. The denominator represents the time required by \(P\) processors, assuming ideal division of the parallel work.

This simplified formulation assumes ideal workload distribution and does not explicitly include communication, synchronization, or other additional overheads.

## 3. Relationship with Amdahl's and Gustafson's Laws

The Sun–Ni model includes the other two models as special cases.

### Case 1: Fixed workload — Amdahl's Law

If the workload does not increase when more memory and processors are added, then:

\[
G(P)=1
\]

Substituting this into the Sun–Ni formula:

\[
S_{SN}(P)=
\frac{\alpha+(1-\alpha)}
{\alpha+\frac{1-\alpha}{P}}
\]

Since \(\alpha+(1-\alpha)=1\):

\[
S_{SN}(P)=
\frac{1}{\alpha+\frac{1-\alpha}{P}}
\]

This is Amdahl's Law. Therefore, Amdahl's model is the fixed-workload case of the Sun–Ni model.

### Case 2: Workload grows proportionally with processors — Gustafson's Law

If the parallel workload grows at the same rate as the number of processors:

\[
G(P)=P
\]

Then:

\[
S_{SN}(P)=
\frac{\alpha+(1-\alpha)P}
{\alpha+\frac{(1-\alpha)P}{P}}
\]

Simplifying the denominator:

\[
S_{SN}(P)=
\frac{\alpha+(1-\alpha)P}
{\alpha+(1-\alpha)}
\]

Therefore:

\[
S_{SN}(P)=\alpha+(1-\alpha)P
\]

This is equivalent to Gustafson's scaled speedup:

\[
S_G(P)=P-\alpha(P-1)
\]

Thus, Gustafson's Law is another special case of the Sun–Ni model.

## 4. Comparing the three models

| Model | Workload assumption | Main constraint |
|---|---|---|
| Amdahl's Law | Workload remains fixed | Fixed problem size |
| Gustafson's Law | Workload grows proportionally with processors | Approximately fixed execution time |
| Sun–Ni model | Workload grows according to memory capacity | Available memory |

The main advantage of the Sun–Ni model is its flexibility. It does not require the workload to remain constant or to grow exactly in proportion to the number of processors. Instead, it allows the workload growth factor to reflect the memory requirements of a particular application.

## 5. When Gustafson's Law overestimates or underestimates performance

Gustafson's Law assumes that the parallel workload grows proportionally with the number of processors. In the Sun–Ni model, this corresponds to \(G(P)=P\).

However, actual workload growth may differ from this assumption.

**When Gustafson's Law overestimates performance**

If:

\[
G(P)<P
\]

the workload grows more slowly than the processor count. In this situation, the Sun–Ni speedup is lower than the Gustafson speedup under the same idealized assumptions.

For example, an application may not have enough memory-intensive data or sufficiently large datasets to use all additional memory effectively. The workload therefore cannot increase proportionally with the number of processors.

Gustafson's Law may then predict a higher speedup than the memory-bounded model.

**When Gustafson's Law underestimates performance**

If:

\[
G(P)>P
\]

the workload grows faster than the processor count. Under the simplified Sun–Ni model, this can produce a higher speedup than Gustafson's prediction.

This situation may occur when the relationship between memory capacity and computational workload allows a disproportionately large increase in useful work.

These comparisons concern the idealized speedup equations. In an actual system, communication, synchronization, memory access delays, and load imbalance may reduce the achievable performance.

## 6. Critical evaluation

The Sun–Ni model provides a broader perspective on parallel scalability because it considers the relationship between memory capacity and workload size.

Gustafson's Law is useful when a larger system can process a proportionally larger problem within approximately the same execution time. However, this assumption may not represent every application. Some problems require memory that grows at a different rate from the number of processors.

The Sun–Ni model addresses this limitation through the function \(G(P)\). It allows different workload-growth patterns to be represented within one mathematical framework.

Nevertheless, the model is not an exact performance predictor by itself. The memory-growth function must be understood for the particular application, and real communication and synchronization costs must also be considered when estimating actual execution time.

Overall, the Sun–Ni model demonstrates that parallel scalability depends not only on the sequential and parallel portions of a program, but also on how the workload changes with available system resources.

## 7. Conclusion

Amdahl's Law, Gustafson's Law, and the Sun–Ni model describe different workload-scaling assumptions. Amdahl considers a fixed workload, Gustafson considers workload growth proportional to the number of processors, and Sun–Ni provides a more general memory-bounded formulation.

The most important conclusion is that Gustafson's Law should not automatically be treated as the expected performance of every parallel system. Its prediction depends on whether the workload can actually grow at the assumed rate. The Sun–Ni model makes this dependency explicit through \(G(P)\), providing a more flexible framework for evaluating parallel performance.

## References

1. Sun, X.-H., and Ni, L. M. (1990). *Another View on Parallel Speedup*. Proceedings of the 1990 ACM/IEEE Conference on Supercomputing, pp. 324–333. https://doi.org/10.1109/SUPERC.1990.130037

2. Sun, X.-H., and Ni, L. M. (1993). *Scalable Problems and Memory-Bounded Speedup*. Journal of Parallel and Distributed Computing, 19(1), 27–37. https://doi.org/10.1006/jpdc.1993.1087
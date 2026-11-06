# Task 10: Memory Growth Rate vs. Scaled Speedup

## 1. Objective

The purpose of this task is to examine the relationship between available memory and problem dimension under weak-scaling conditions.

The assignment considers a grid-based solver with a three-dimensional problem domain. Since the memory requirement of a 3D grid grows proportionally to the cube of its dimension, increasing the number of nodes allows the system to process larger grids.

## 2. Given Parameters

- Memory per node: 32 GB
- First configuration: 64 nodes
- Second configuration: 512 nodes
- Total memory model: M(P) = c × P
- Three-dimensional grid memory complexity: O(N³)

Here, P represents the number of nodes, N is the dimension of one side of the cubic grid, and c represents the memory capacity per node.

Since each node has a memory limit of 32 GB:

c = 32 GB

Therefore:

**M(P) = 32P GB**

## 3. Total Memory Capacity

### 3.1. Configuration with 64 nodes

M(64) = 32 × 64

**M(64) = 2,048 GB**

### 3.2. Configuration with 512 nodes

M(512) = 32 × 512

**M(512) = 16,384 GB**

The second configuration provides eight times more total memory than the first configuration.

## 4. Mathematical Formulation of the 3D Grid

For a cubic grid with dimension N × N × N, the total number of grid cells is:

Number of cells = N × N × N

**Number of cells = N³**

Assuming that each grid cell requires k units of memory, the total memory requirement is:

M(N) = kN³

The memory constraint is:

kN³ ≤ 32P

Rearranging:

N³ ≤ 32P / k

Taking the cube root:

**Nmax(P) = ∛(32P / k)**

This expression determines the maximum grid dimension that can fit within the available memory.

## 5. Maximum Grid Dimension for Each Configuration

### 5.1. 64 nodes

The total memory capacity is 2,048 GB.

Therefore:

N64 = ∛(2,048 / k)

### 5.2. 512 nodes

The total memory capacity is 16,384 GB.

Therefore:

N512 = ∛(16,384 / k)

The assignment does not provide the value of k, which represents the memory required per grid cell. Consequently, an exact numerical grid dimension cannot be determined without additional information.

However, the relative dimensions can be calculated.

## 6. Comparison of Grid Dimensions

The ratio between the two grid dimensions is:

N512 / N64 = ∛(16,384 / 2,048)

N512 / N64 = ∛8

**N512 / N64 = 2**

Therefore:

**N512 = 2N64**

The results are summarized below:

| Metric | 64 nodes | 512 nodes |
|---|---:|---:|
| Memory per node | 32 GB | 32 GB |
| Total memory | 2,048 GB | 16,384 GB |
| Memory capacity relative to 64 nodes | 1× | 8× |
| Relative grid dimension | 1× | 2× |

## 7. Analysis

The results demonstrate the relationship between memory capacity and problem dimension in a three-dimensional grid-based solver.

Increasing the number of nodes from 64 to 512 increases the total memory capacity by a factor of eight. However, because memory requirements grow proportionally to N³, the maximum grid dimension increases only by a factor of two.

This illustrates an important property of three-dimensional scientific simulations: increasing available memory does not produce an equal proportional increase in the dimension of the computational domain.

Under ideal weak-scaling conditions, each node maintains a fixed memory allocation and processes a corresponding portion of the larger problem. In practice, memory consumed by communication buffers, ghost cells, operating systems, and other data structures can reduce the memory available for the main computational grid.

## 8. Conclusion

With 32 GB of memory per node, a 64-node configuration provides 2,048 GB of total memory, while a 512-node configuration provides 16,384 GB.

For a three-dimensional grid, the maximum dimension is proportional to the cube root of the available memory. Consequently, increasing the node count from 64 to 512 doubles the maximum grid dimension under the same memory-per-cell assumption.

An exact numerical value of N requires the memory consumption per grid cell, which is not specified in the assignment. The symbolic formulation and relative comparison provide the result without introducing unsupported assumptions.
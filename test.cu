#include <iostream>
#include <cuda_runtime.h>

__global__ void testDependency(int *start, int *results, int n)
{
  int index = threadIdx.x + blockIdx.x * blockDim.x;

  int dependency_var = 0;

  // # pragma unroll
  for (int i = index; i < n; ++i)
  {
    // if (start[i] < n && i == start[i])
    // {
      dependency_var = start[i];
    // }
  }
  results[index] = dependency_var;
}

int main()
{
  unsigned n = 1024*1024;
  int results[n];

  int *d_results;
  cudaMalloc(&d_results, n * sizeof(int));

  int *start, *d_start;
  cudaMalloc(&d_start, n * sizeof(int));
  cudaMallocHost(&start, n * sizeof(int));

  for (int i = 0; i < n; ++i)
  {
    start[i] = i;
  }

  cudaMemcpy(d_start, start, n * sizeof(unsigned), cudaMemcpyHostToDevice);

  testDependency<<<1, 1>>>(d_start, d_results, n);

  cudaMemcpy(results, d_results, n * sizeof(int), cudaMemcpyDeviceToHost);

  cudaFree(d_results);

  for (int i = 0; i < n / 1024; ++i)
  {
    std::cout << "Result[" << i << "]: " << results[i] << std::endl;
  }

  return 0;
}

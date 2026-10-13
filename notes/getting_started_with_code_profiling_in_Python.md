# Getting started with code profiling in Python and cProfile


## Outline
 - Start with motivation
 - time tool
 - Python cProfile with multiple examples
 - Python libraries and some Python programs including
 	+ python multiprocessing
 	+ Numpy
 	+ Numba
 	+ dask
 - Profile these programs and try to understand each of them.
 - Introduce other tools including,
 	+ Pyinstrument
 	+ Eliot
 	+ py-spy
 	+ memory_profiler
 	+ line_profiler
 	+ Linux perf
 - Once I have all the examples and technical content mention about why profiling is important and why we need this?
 - Homework to myself, implement KNN with scikit-learn and profile this with the appropriate profilers to understand different things

## Abou Matrix Multiplication with Python

For starters, you design your code to multiply two list of lists as the data structure of matrix in Python for matrix multiplication. Result, it takes a lot of time and resource to complete this process. Of course there are some optimizations, however they may not work as expected. For instance, vectorize the list of lists into a 1D list and multiply them as multiplying matrices. Result, almost the same performance. Another way would be employing the tuples as a data structure for multpilication. There may be some performance gain but not as expected. With this motivation, engineers, researchers spend a lot of time to optimize this problem for a very long time. We have a lot of opportunities to optimize Python matrix multiplication process. Numpy, scipy, numba, taichi, TensorFlow, PyTorch, Jax and more. There are number of alternative techniques and libraries that you can use for your purpose. The latest one is Mojo which is a kind of combination all available techniques and populated all these techniques under one language.

Anyways, since you have a lot of opportunities to use for a specific cases, this also shows that you're doing something wrong with your choice of language. If you really want to build something that lasts for a long time and do not think of optimization or using resources appropriately, the best alternative would be C language. You'll see that C language is the fastest of all and you don't need to worry about such things. For this reason, you don't need much of profiling or understanding your code. Of course that code design is important and can save you ton of time, energy, resource, and man power. However, in some cases, instead of spending time on profiling or any other steps, you just need to employ certain operations to your code. Thats all!

On the next step, you're going to see that Julia and R languages are also used for profiling and  
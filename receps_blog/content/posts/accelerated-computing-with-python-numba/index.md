+++
title = 'Accelerated Computing With Python Numba'
date = 2025-08-13T22:24:25-05:00
draft = true
tags = ["Python", "Numba", "GPU Computing", "CUDA", "Accelerated Computing", "Optimization"]
categories = ["High Performance Computing", "Python"]
+++

Python JIT Compiler --> Just in time compiler
Python is an interpreted language and not like C language which is ahead of time compiled.
C extension can be used with Python to accelerate some operations.
With Numba:
 - Loops
 - aritmethic operations
 - ...
Numba is a Python library that is used to compile the Python code into CPU or GPU optimized version of it.
The thing is that Numba is a decorator-oriented library which means when you write Python code, you just need to add decorator.
More detailed explanation will come below.

To learn the details of Numba on CPU and especially on GPU computation, I took a course from NVIDIA DLI called "Fundamentals of Accelerated Computing CUDA with Python".

Topics that are covered in the course:
 - ...

Besides the course, here are my list of resources that I used to learn the fundamentals and then details are listed below:
 - ...

Some of the scenarios where Numba would be very useful. We know that scientific computing is really important and resources, time, and some other parameters become more important with
very large dataset or long process of computation.

CUDA C is important and can be difficult for some. Or if your tech stack is depend on Python language and Python scientific computing ecosystem libraries, difficult to merge with CUDA C.
CUDA C may require some set of low-level information you need to consider while designing the code structure. With Numba this experience simplified. Below both flow of executions were given.
Compare and analyze that Numba makes the process a lot siplified and encapsulates and hides some steps for the sake of Python developers.

We know that C is difficult to develop with however the power of computation with C is unique and remarkable.

I share some code examples and scenarios that Numba flies the computation and completes the fraction of the time compared to the Python version of it.

I should mention that NumPy is kind of the backbone of the some of the operations. And we know that even with NumPy, some of the computations become really really fast.
Here are the some scenarions that Python vs NumPy vs Numba CPU vs Numba GPU computation comparison. For this purpose, I prefer convolution operation for the benchmark to see how performance matters 
based on the different environment of computation. In addition to this bencmark entities, I also added C only, and CUDA C computations.

In these examples, I would like to explain some of the concepts including memory management, data move between host and device, building kernels or custom kernels for CUDA computation,
and other stuff.

I should also mention about the memory management. This topic is important and I need to learn with details!

With all these explanations, I conclude the post. The code is shared at my GitHub account and profiling results are also shared in the README.md of the repo.
\_ CPU and GPU sides profiling is important to see the performance thruought RAM, CPU, GPU, and disk access.

With this content, I wanted to build a skill set to use on my daily computations. A lot of researchers prefer to use Python for their tech stack and usually it's difficult to leave it and start learning a new 
tech stack for their task. With Numba, there is a simpler solution. No need to learn another stuff, just practice some of the concepts from NumPy and other stuff then immediately accelereate the computation.
I believe that this is huge and it's going save a lot of researchers time and energy. Moreover, hardware acceleration is a super important concept in scientific computing and with Numba decorators, we can easily
utilize NVIDIA GPU's for computation.





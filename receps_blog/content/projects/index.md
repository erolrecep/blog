+++
title = 'Projects'
date = 2026-11-08T12:15:00-06:00
draft = false
+++

A curated collection of open-source projects, technical workshops, and high-performance computing experiments:

---

- **[RCRE — Recep's Code Run Everywhere](/rcre-docs/)** *(v0.2.5 — in-development)*  
  A single-header, zero-dependency C23 engine unifying modern Computer Vision, Reverse-Mode Autograd, Classical Machine Learning, and Generative Transformers across Edge, HPC, and WebAssembly with **zero heap allocations in inner inference loops**. Features 15-bit fixed-point color kernels with 0 LSB discrepancy vs. OpenCV, subpixel continuous resizing, Harris corners, DLT/RANSAC homography, Lucas-Kanade optical flow, scalar DAG & tensor tape autograd, decoder-only generative transformers with $\mathcal{O}(1)$ KV-caching, tabular GBDT inference (7.86M preds/sec), and embedded HNSW vector search (44k QPS).
  - 🌐 **[Project Home & Showcase Portal](/rcre-docs/)**
  - 📖 **[Interactive Documentation & C23 API Reference](/rcre-docs/docs/)**
  - 📚 **[Academic Textbook Monograph (PDF)](/rcre-docs/rcre-book.pdf)**
  - 🚀 **[In-Browser Live Webcam Playground](/rcre-docs/playground.html)**
  - 🧊 **[3D Tensor Strides & Memory Layout Visualizer](/rcre-docs/learn/strides.html)**
  - ⚡ **[Cache-Tiled GEMM Hierarchy Simulator](/rcre-docs/learn/gemm_cache.html)**
  - 🎯 **[Sliding Convolution SIMD Stencil Visualizer](/rcre-docs/learn/stencils.html)**

<br>

- **[Best Practices for Using HPC: Scaling Up to Cluster-Native Workflows](https://github.com/erolrecep/best_practices_for_hpc)** *(November 2026)*  
  Comprehensive workshop curriculum, interactive slide deck, and practical guides presented at the Rice University Center for Research Computing (CRC) Research Computing Day. Designed to bridge the gap between running code on personal laptops and scaling compute jobs across large-scale supercomputing clusters. Covers login node etiquette, memory over-allocation traps, multi-core CPU and GPU resource sizing, high-speed shared file systems (Lustre/NFS), Slurm batch script templates, job monitoring with `seff`, and reproducible cluster-native workflows.
  - 🖥️ **[Interactive Presentation Slides](https://erolrecep.github.io/best-practices-hpc/)**
  - 📝 **[Technical Companion Article](/posts/best-practices-for-hpc/)**
  - 💻 **[GitHub Repository](https://github.com/erolrecep/best_practices_for_hpc)**

<br>

- **[Profiling Hardware Accelerated Computations for CPU & GPU](https://github.com/erolrecep/profiling_hardware_accelerated_computations)** *(November 2026)*  
  A practical, diagnostic guide and hands-on workshop focused on making computational science and AI workloads run 10x to 1,000x faster across modern hardware architectures (NVIDIA GPUs, Apple Silicon MPS, and multi-core x86/ARM CPUs). Teaches a simple 3-step triage workflow (Run &rarr; Spot &rarr; Fix) using system-wide macro timeline profiling (nsys), kernel micro-architecture inspection (ncu), deep learning operator tracing (torch.profiler), line-by-line profiling (Scalene), and heap allocation flamegraphs (Memray). Demonstrates how cache-friendly loop reordering, eliminating Python scalar synchronizations (aten::_local_scalar_dense), and 1D grid-stride loops eliminate warp divergence and unlock peak silicon throughput.
  - 🖥️ **[Interactive Presentation Slides](https://erolrecep.github.io/profiling_hardware_accelerated_computations/)**
  - 📓 **[Google Colab Interactive Cloud Lab](https://colab.research.google.com/github/erolrecep/profiling_hardware_accelerated_computations/blob/main/notebooks/cuda_profiling_colab_workshop.ipynb)**
  - 💻 **[GitHub Repository](https://github.com/erolrecep/profiling_hardware_accelerated_computations)**

<br>

- **[Data Science: From Yesterday to Tomorrow](https://github.com/erolrecep/datascience_from_yesterday_to_tomorrow)** *(November 2026)*  
  A structured retrospective curriculum and interactive keynote delivered at Alparslan Türkeş Science and Technology University (ATU Adana, TR) tracing the 25-year evolution of Data Science—from early Web 2.0 clickstream analytics in 2000 to modern Foundation Models, physics-informed synthetic simulation, and counterfactual causal reasoning. Features an end-to-end physics simulation and telemetry analysis of a Formula 1 Grand Prix at Monza (53 laps, 1,060 telemetry records), dual-panel real-time circuit race animations, feature dominance modeling, and "what-if rain" scenario counterfactuals verified by an automated test suite.
  - 🖥️ **[Interactive Presentation Slides](https://erolrecep.github.io/datascience_from_yesterday_to_tomorrow/)**
  - 📝 **[Article Part 1: Foundations & Evolution](/posts/data-science-yesterday-tomorrow/)**
  - 📝 **[Article Part 2: Retrospective & Future Frontiers](/posts/data-science-yesterday-tomorrow-part-2/)**
  - 💻 **[GitHub Repository](https://github.com/erolrecep/datascience_from_yesterday_to_tomorrow)**

<br>

- **[Scientific Python Environments & Workflows on HPC](https://github.com/erolrecep/scientific_python_workflow_hpc)** *(October 2026)*  
  Comprehensive workshop curriculum and hands-on laboratory for transitioning scientific Python workflows from local development environments (macOS/Linux) and Google Colab to multi-core CPUs and GPU-accelerated HPC clusters (Rocky Linux, SLURM, and Lmod). Demonstrates zero-overhead virtual environment management (uv), automated reproducible DAG pipelines (make), CPU/GPU benchmarks, memory profiling with flamegraphs (memray, scalene), and container-free cluster deployments.
  - 🖥️ **[Interactive Presentation Slides](https://erolrecep.github.io/scientific_python_workflow_hpc/)**
  - 📓 **[Google Colab Hands-On Notebook](https://github.com/erolrecep/scientific_python_workflow_hpc/blob/main/notebooks/scientific_python_workflow_colab.ipynb)**
  - 💻 **[GitHub Repository](https://github.com/erolrecep/scientific_python_workflow_hpc)**

<br>

- **[VibeCoding-Workshop](https://github.com/erolrecep/VibeCoding-Workshop)** *(October 2026)*  
  Full workshop curriculum on AI-assisted software development: prompt engineering anatomy, iterative model guidance, and full-stack interactive web application development.

- **[Python_dev_w_uv](https://github.com/erolrecep/Python_dev_w_uv)** *(September 2026)*  
  A modern Python development workflow blueprint demonstrating zero-overhead virtual environment management and package resolution using Astral's ultra-fast `uv` tool.

- **[dev_env_automation](https://github.com/erolrecep/dev_env_automation)** *(August 2026)*  
  Automated shell scripts and setup tooling for configuring reproducible, streamlined development environments on modern macOS and Linux systems.

- **[convolution_ops_hpc](https://github.com/erolrecep/convolution_ops_hpc)** *(August 2026)*  
  A benchmarking study exploring different programming languages (C, Python), optimization techniques, and libraries for accelerating 2D image convolution algorithms on HPC hardware.

- **[GettingStartedwithAHPCC](https://github.com/erolrecep/GettingStartedwithAHPCC)** *(September 2024)*  
  Comprehensive training materials, SLURM batch scripts, and step-by-step guides for users learning cluster computing at the Arkansas High Performance Computing Center (AHPCC).

- **[image_processing_workshop](https://github.com/erolrecep/image_processing_workshop)** *(August 2023)*  
  A hands-on mini-workshop designed to introduce audiences to the fundamentals, mathematics, and practical implementations of 2D image processing and computer vision algorithms.

---

For more open-source experiments and repositories, visit my **[GitHub Profile](https://github.com/erolrecep)**.

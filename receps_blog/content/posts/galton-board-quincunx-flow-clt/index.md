+++
title = "Simulating the Galton Board: From Bernoulli Trials to the Central Limit Theorem at 750M Drops/Sec"
date = 2026-11-13T15:00:00-06:00
tags = ["C Programming", "HPC", "Systems Engineering", "Statistics", "Python", "FastAPI", "WebAssembly"]
categories = ["Systems Engineering", "Algorithms", "AI/ML"]
+++

*How Sir Francis Galton's 1873 mechanical probability device inspired a modern C23 bit-level SIMD engine, an in-browser WebAudio visualizer, and a real-time Python 3.15 streaming service.*

---

## Abstract

In 1873, Victorian polymath Sir Francis Galton constructed the **quincunx** (commonly known as the **Galton board** or **bean machine**)—a vertical board studded with interleaved rows of pins through which small marbles cascade. As each bead ricochets against pins, it deflects left or right with equal probability. By the time the beads reach the bottom collector bins, an unmistakable geometric silhouette emerges: the smooth, bell-shaped Gaussian normal distribution.

To celebrate this foundational connection between discrete probability and continuous physical law, I developed [**`rcre-galton`**](https://erolrecep.github.io/galtonboard/) as part of the **`rcre` (Recep's Code Run Everywhere)** project.

This implementation bridges two worlds:
1. **Bare-Metal C23 Systems Performance**: A hardware-saturating Monte-Carlo engine that leverages bit-level hardware popcounts on `xoshiro256**` words to evaluate 64-row lattices at **750+ Million drops/sec** (1.33 ns/drop).
2. **Interactive WebAssembly & Python 3.15 Serving**: A zero-dependency HTML5 Canvas2D / Web Audio visualizer and an asynchronous Python 3.15 FastAPI streaming service broadcasting live ball trajectories over WebSockets.

> 🎲 **Live Interactive Web Simulator**:  
> Explore the live simulation, adjust pin rows, tweak right-deflection bias, and listen to synthesized collision chimes in your browser:  
> [**https://erolrecep.github.io/galtonboard/**](https://erolrecep.github.io/galtonboard/)  
> 📦 **GitHub Repository & Source Code**:  
> Located in [**`apps/rcre/projects/rcre_galtonboard/`**](https://github.com/erolrecep/codebase/tree/main/apps/rcre/projects/rcre_galtonboard) and [**`_python_/galtonboard_fastapi/`**](https://github.com/erolrecep/codebase/tree/main/_python_/galtonboard_fastapi).

---

## Interactive Visualizer Embed

<iframe src="https://erolrecep.github.io/galtonboard/" width="100%" height="820px" style="border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); margin: 1.5rem 0;" title="RCRE Galton Board Interactive Visualizer"></iframe>

---

## 1. The Mathematical Mechanism: From Bernoulli to Gauss

The physics of a Galton board with $N$ rows can be formalized as a sequence of $N$ independent Bernoulli trials $B_1, B_2, \dots, B_N$, where:

$$B_i = \begin{cases} 1 & \text{with probability } p \text{ (right deflection)} \\ 0 & \text{with probability } 1 - p \text{ (left deflection)} \end{cases}$$

The final column index $K$ into which a bead settles is the sum of right deflections:

$$K = \sum_{i=1}^N B_i$$

### Exact Binomial Probability Mass Function (PMF)
The probability of a bead landing in bin $k \in \{0, 1, \dots, N\}$ follows the Binomial distribution:

$$P(K = k) = \binom{N}{k} p^k (1 - p)^{N - k} = \frac{N!}{k!(N - k)!} p^k (1 - p)^{N - k}$$

In computer systems, directly computing factorials ($N!$) causes catastrophic 64-bit integer overflow for $N > 20$. In `rcre-galton`, we compute factorials in continuous log-space using the standard Gamma function ($\Gamma(n + 1) = n!$):

$$\ln \binom{N}{k} = \ln \Gamma(N + 1) - \ln \Gamma(k + 1) - \ln \Gamma(N - k + 1)$$

$$\ln P(K = k) = \ln \binom{N}{k} + k \ln p + (N - k) \ln(1 - p)$$

This guarantees bit-exact probabilities up to $N = 64$ rows with zero floating-point overflow.

### The De Moivre–Laplace Limit Theorem
As the number of pin rows $N \to \infty$, the discrete Binomial distribution converges to the continuous Gaussian Normal density $\mathcal{N}(\mu, \sigma^2)$:

$$\mu = N p, \quad \sigma^2 = N p (1 - p)$$

$$f(x) = \frac{1}{\sigma \sqrt{2\pi}} \exp\left(-\frac{1}{2}\left(\frac{x - \mu}{\sigma}\right)^2\right)$$

This is a special case of the **Central Limit Theorem (CLT)**: independent microscopic perturbations (peg collisions) compound into macroscopic deterministic structure.

---

## 2. Systems Optimization: 750M Drops/Sec in ISO C23

When simulating hundreds of millions of drops for Monte-Carlo verification or high-frequency rendering, traditional loop-based branches (`if (rand() < 0.5) k++;`) stall CPU pipelines.

In **`rcre-galton`**, we satuate modern hardware through three techniques:

### A. Single-Cycle Hardware Popcount
For a symmetric board ($p = 0.5$) with $N \le 64$ rows, each ball requires exactly $N$ independent random bits.

Instead of generating $N$ random floats or branching $N$ times, we draw a single 64-bit pseudo-random word from a fast `xoshiro256**` generator, mask the active $N$ bits, and compute the number of set bits using the hardware population count instruction (`popcnt` on x86-64, `cnt` on ARM Neon):

```c
// Symmetric fast-path: 1 pseudo-random word -> 1 marble drop
uint64_t word = prng_next_u64(&board->prng);
uint64_t active_bits = word & ((1ULL << rows) - 1ULL);
uint32_t bin_index = (uint32_t)__builtin_popcountll(active_bits);
board->bin_counts[bin_index]++;
```

By unrolling the batch loop by a factor of 4, the inner loop processes **4 full marble trajectories every ~5 nanoseconds**:

```
Executing Monte-Carlo Bernoulli trials...
[Simulation Completed in 0.0265 seconds]
  Throughput          : 754.15 Million drops/sec (1.33 ns/drop)
```

### B. Cache-Line Alignment & Zero Allocations
Histogram counters are aligned to 64-byte boundaries (`alignas(64)`), ensuring that all bin updates hit L1 data cache lines without false sharing. The simulation loop performs **zero heap allocations** (`malloc`), eliminating allocator locks and memory fragmentation.

### C. Pearson Chi-Square Goodness-of-Fit Test
To rigorously verify that the PRNG and bit-level dispatch faithfully reproduce the theoretical binomial law, the engine computes the Pearson $\chi^2$ statistic and evaluates the regularized upper incomplete gamma function $Q(a, x)$:

$$\chi^2 = \sum_{k=0}^N \frac{(O_k - E_k)^2}{E_k}, \quad \text{dof} = \text{bins} - 1$$

```
--- STATISTICAL VERIFICATION REPORT ---
  Total Balls (M)     : 20000000
  Pin Levels (N)      : 16  (Bins: 17)
  Empirical Mean (x̄)  : 7.999663  (Target: 8.000000, Error: -0.000337)
  Empirical Variance  : 3.999587  (Target: 4.000000, Error: -0.000413)
  Chi-Square Test (χ²): 13.8712  (dof: 16, p-value: 0.6083)
  Null Hypothesis H₀  : ACCEPTED (No divergence from Binomial PMF at α=0.05)
```

---

## 3. Real-Time Streaming with Python 3.15 & FastAPI

Alongside the low-level C engine, we developed a modern asynchronous service in **Python 3.15.2** to demonstrate real-time streaming architectures:

* **Pydantic v2 Models**: Strict schemas (`SimulationConfig`, `SimulationStats`, `BinDistributionItem`) validating inputs and telemetry outputs.
* **WebSocket Streaming (`/ws/stream`)**: Asynchronous broadcast manager streaming individual drop paths, landed bins, and live moments to multiple connected web clients.
* **Vectorized NumPy 2.0 Batching**: When serving batch queries via `POST /api/v1/simulate`, the engine uses `rng.binomial(n=rows, p=bias, size=balls)` to simulate 100,000 drops in 1.2 milliseconds.

```python
@app.post("/api/v1/simulate", response_model=SimulationResponse)
async def run_simulation(config: SimulationConfig):
    g_engine.reset(config)
    _, elapsed_ms = g_engine.simulate_batch(config.balls)
    stats = g_engine.calculate_statistics()
    items = g_engine.get_distribution_items()

    return SimulationResponse(
        configuration=config,
        stats=stats,
        distribution=items,
        elapsed_ms=round(elapsed_ms, 3),
    )
```

---

## 4. In-Browser Visualizer & Web Audio Synthesis

The client-side visualizer ([**`web/index.html`**](https://erolrecep.github.io/galtonboard/)) is built with zero external dependencies:
* **Elastic Kinematics**: Marbles bounce elastically against cylindrical pegs with restitution $e \in [0.1, 0.8]$, gravity $g$, and subtle Gaussian velocity jitter.
* **Dual Theoretical Distribution Overlays**:
  * **Amber Dotted Line**: The discrete Binomial PMF line with individual bin probability nodes.
  * **Cyan Glowing Bell Curve**: The continuous Gaussian Normal density function scaling dynamically with bin accumulation.
  * **Emerald Gradient Columns**: Physical stacking of fallen marbles into vertical bars.
* **Web Audio Synthesis**: Every peg collision triggers a synthesized sine oscillator using the Web Audio API. Pitches are mapped along a harmonic pentatonic scale proportional to row depth, creating a crystalline music box effect as beads tumble down the pyramid.

---

## 5. Summary & Verification

Whether running on bare metal with C23 bit manipulation, streaming over WebSockets via Python 3.15 FastAPI, or rendering in an interactive Canvas2D browser window, the Galton Board demonstrates the elegance of systems computing: simple, discrete, deterministic rules compounding into smooth, universal distributions.

All code and benchmarks are available in the repository:
* **C23 Core Project**: [`apps/rcre/projects/rcre_galtonboard/`](https://github.com/erolrecep/codebase/tree/main/apps/rcre/projects/rcre_galtonboard)
* **Python Standalone**: [`_python_/galtonboard_fastapi/`](https://github.com/erolrecep/codebase/tree/main/_python_/galtonboard_fastapi)
* **Live Web Playground**: [https://erolrecep.github.io/galtonboard/](https://erolrecep.github.io/galtonboard/)

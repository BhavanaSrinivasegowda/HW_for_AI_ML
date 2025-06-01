
# SPI Interface Benchmark Simulation

This project demonstrates a combined simulation of an SPI interface between a Python testbench (using cocotb) and a Verilog SPI slave module. It benchmarks latency and throughput for varying packet sizes.

---

## Overview

- **Verilog module**: SPI slave
- **Python testbench**: cocotb-based SPI master
- **Goal**: Measure and report SPI throughput and latency
- **Toolchain**: Icarus Verilog, cocotb, Python 3

---

## Files

- `spi_slave.v`: Verilog implementation of SPI slave
- `test_spi_benchmark.py`: cocotb testbench with benchmark logic
- `Makefile`: Integration with cocotb using Icarus Verilog

---

##  Test Setup & Key Features

- Simulates SPI transactions for various packet sizes (1 to 1024 bytes)
- Measures latency (in microseconds)
- Measures throughput (in kbps)
- Computes protocol efficiency
- Saves results in CSV for further analysis

---

##  Execution Steps

1. **Install dependencies**:
    ```bash
    pip install cocotb
    sudo apt install iverilog
    ```

2. **Make sure file structure is correct**:
    ```
    spi_benchmark/
    ├── spi_slave.v
    ├── test_spi_benchmark.py
    ├── Makefile
    ```

3. **Run the benchmark**:
    ```bash
    make
    ```

4. **Output**:
    ```
   SPI BENCHMARK SUMMARY
============================================================
Average Latency: 382.22 µs
Maximum Throughput: 4848.48 kbps
SPI Clock Frequency: 5.00 MHz
Protocol Overhead: 1.65 µs

Performance by Packet Size:
Size (bytes)   Throughput (kbps)        Efficiency (%)
------------------------------------------------------------
1              4848.48                  96.97
8              4845.55                  96.91
16             4842.62                  96.85
32             4836.76                  96.74
64             4825.09                  96.50
128            4801.92                  96.04
256            4756.24                  95.12
512            4733.73                  94.67
1024           4733.73                  94.67

CSV saved as: spi_benchmark_results.csv
3447400.00ns INFO     cocotb.regression                  spi_benchmark passed
3447400.00ns INFO     cocotb.regression                  ******************************************************************************************
                                                         ** TEST                              STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
                                                         ******************************************************************************************
                                                         ** test_spi_benchmark.spi_benchmark   PASS     3447400.00          30.09     114565.27  **
                                                         ******************************************************************************************
                                                         ** TESTS=1 PASS=1 FAIL=0 SKIP=0                3447400.00          30.12     114452.86  **
                                                         ******************************************************************************************


## Notes

- Simulation uses realistic timing: setup/hold, inter-byte gaps, logic delays.
- Efficient SPI simulation reaches ~94–97% efficiency at 5 MHz clock.

---


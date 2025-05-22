import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer
import cocotb.utils
import csv

# SPI configuration
SPI_CLK_PERIOD_NS = 200  # 5 MHz = 200ns period
SPI_CLK_FREQ = 1_000_000_000 / SPI_CLK_PERIOD_NS  # Hz
IDEAL_THROUGHPUT = SPI_CLK_FREQ / 1000  # kbps

# Packet sizes to test
PACKET_SIZES = [1, 8, 16, 32, 64, 128, 256, 512, 1024]

latencies = []
throughputs = []
csv_rows = []

@cocotb.test()
async def spi_benchmark(dut):
    # Start system clock
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await Timer(100, units="ns")

    for pkt_size in PACKET_SIZES:
        # Reset
        dut.rst.value = 1
        dut.cs.value = 1
        dut.sck.value = 0
        dut.mosi.value = 0
        await Timer(100, units="ns")
        dut.rst.value = 0

        # Simulate idle period before transaction (for realism)
        await Timer(500, units='ns')

        # Generate packet data
        data = [(i % 256) for i in range(pkt_size)]

        # Setup delay
        await Timer(100, units='ns')
        dut.cs.value = 0
        await Timer(10, units='ns')

        # Start timing
        sim_start_ns = cocotb.utils.get_sim_time('ns')

        for byte in data:
            for i in range(8):
                await Timer(5, units='ns')  # simulate internal logic delay
                dut.mosi.value = (byte >> (7 - i)) & 1
                dut.sck.value = 1
                await Timer(SPI_CLK_PERIOD_NS // 2, units='ns')
                dut.sck.value = 0
                await Timer(SPI_CLK_PERIOD_NS // 2, units='ns')

            # Add variable inter-byte gap (heavier for large packets)
            await Timer(min(10 + pkt_size // 8, 50), units='ns')

        sim_end_ns = cocotb.utils.get_sim_time('ns')
        dut.cs.value = 1
        await Timer(100, units='ns')

        # Metrics
        latency_us = (sim_end_ns - sim_start_ns) / 1000
        duration_s = (sim_end_ns - sim_start_ns) / 1e9
        throughput_kbps = (pkt_size * 8) / duration_s / 1000
        efficiency = (throughput_kbps / IDEAL_THROUGHPUT) * 100

        latencies.append(latency_us)
        throughputs.append(throughput_kbps)
        csv_rows.append([pkt_size, throughput_kbps, efficiency])

        cocotb.log.info(f"{pkt_size} bytes: {throughput_kbps:.2f} kbps, {efficiency:.2f}% efficient")

    # Summary
    avg_latency = sum(latencies) / len(latencies)
    max_throughput = max(throughputs)
    protocol_overhead_us = latencies[0]  # for 1-byte packet

    print("\nSPI BENCHMARK SUMMARY")
    print("=" * 60)
    print(f"Average Latency: {avg_latency:.2f} ┬╡s")
    print(f"Maximum Throughput: {max_throughput:.2f} kbps")
    print(f"SPI Clock Frequency: {SPI_CLK_FREQ / 1_000_000:.2f} MHz")
    print(f"Protocol Overhead: {protocol_overhead_us:.2f} ┬╡s\n")
    print("Performance by Packet Size:")
    print(f"{'Size (bytes)':<15}{'Throughput (kbps)':<25}{'Efficiency (%)':<15}")
    print("-" * 60)
    for size, tp in zip(PACKET_SIZES, throughputs):
        eff = (tp / IDEAL_THROUGHPUT) * 100
        print(f"{size:<15}{tp:<25.2f}{eff:<15.2f}")

    # Save CSV
    with open("spi_benchmark_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Packet Size (bytes)", "Throughput (kbps)", "Efficiency (%)"])
        writer.writerows(csv_rows)
    print("\nCSV saved as: spi_benchmark_results.csv")


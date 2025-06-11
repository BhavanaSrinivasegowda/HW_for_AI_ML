# test_mutation_sv.py
import cocotb
from cocotb.triggers import Timer, RisingEdge
import random

@cocotb.test()
async def test_mutation_sv(dut):
    GENE_LEN = 12
    mutation_rate = 0.2
    mutation_thresh = int(mutation_rate * 255)

    # Create input gene (e.g., "Hello World!")
    gene = [ord(c) for c in "Hello World!"]
    rand_mask = [random.randint(0, 255) for _ in range(GENE_LEN)]
    rand_ascii = [random.randint(32, 125) for _ in range(GENE_LEN)]

    # Flatten values
    gene_in = sum(c << (i * 8) for i, c in enumerate(gene))
    rand_mask_in = sum(c << (i * 8) for i, c in enumerate(rand_mask))
    rand_ascii_in = sum(c << (i * 8) for i, c in enumerate(rand_ascii))

    # Clock generator
    async def clk_gen():
        while True:
            dut.clk.value = 0
            await Timer(5, units="ns")
            dut.clk.value = 1
            await Timer(5, units="ns")

    cocotb.start_soon(clk_gen())

    # Apply inputs
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    dut.child_in.value = gene_in
    dut.rand_mask.value = rand_mask_in
    dut.rand_ascii.value = rand_ascii_in
    dut.mutation_thresh.value = mutation_thresh
    dut.start.value = 1

    await RisingEdge(dut.clk)
    dut.start.value = 0

    for _ in range(100):
        await RisingEdge(dut.clk)
        if dut.done.value:
            break

    result = dut.mutant_out.value.integer
    result_chars = [(result >> (i * 8)) & 0xFF for i in range(GENE_LEN)]
    print("Original gene :", ''.join(chr(c) for c in gene))
    print("Mutated gene  :", ''.join(chr(c) for c in result_chars))


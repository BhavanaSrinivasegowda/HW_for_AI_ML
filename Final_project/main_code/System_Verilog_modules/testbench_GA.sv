`timescale 1ns/1ps

module genetic_algorithm_tb;

    parameter MAX_POP = 10;
    parameter LEN = 12;

    logic clk = 0;
    logic rst;
    logic done;
    logic [7:0] best_gen[LEN];
    logic [6:0] fitness_percent;

    // Clock
    always #5 clk = ~clk;

    // DUT
    genetic_algorithm #(MAX_POP, LEN) dut (
        .clk(clk),
        .rst(rst),
        .done(done),
        .best_gen(best_gen),
        .fitness_percent(fitness_percent)
    );

    // Internal
    bit coverage_hit[0:100];
    integer cycles;
    integer coverage_count;
    integer reset_cycles;

    // Functional coverage group
    covergroup GA_CG @(posedge clk);
        option.per_instance = 1;

        coverpoint dut.state {
            bins init_stage    = {0};
            bins select_stage  = {1};
            bins cross_stage   = {2};
            bins mutate_stage  = {3};
            bins update_stage  = {4};
            bins done_stage    = {5};
        }

        coverpoint fitness_percent {
            bins low_fitness     = {[0:30]};
            bins mid_fitness     = {[31:70]};
            bins high_fitness    = {[71:99]};
            bins perfect_fitness = {100};
        }

        coverpoint done;
    endgroup

    GA_CG ga_coverage = new();

    // Repeat the test multiple times to increase variation
    initial begin
        int repeat_count = 10;
        $display("Starting Genetic Algorithm Testbench...\n");

        for (int run = 0; run < repeat_count; run++) begin
            $display("\n--- Run %0d ---", run + 1);
            cycles = 0;

            reset_cycles = $urandom_range(5, 15);
            rst = 1;
            repeat (reset_cycles) @(posedge clk);
            rst = 0;

            // Wait for algorithm to finish
            while (!done) begin
                @(posedge clk);
                cycles++;

                // Sample functional coverage
                ga_coverage.sample();

                // Track fitness histogram
                if (dut.current_best.fitness <= 100)
                    coverage_hit[dut.current_best.fitness] = 1;

                if (dut.current_best.fitness > 100)
                    $fatal(1, "Fitness exceeded 100 at cycle %0d", cycles);
            end

            // Report for each run
            $write("Best Generation: ");
            foreach (best_gen[i]) $write("%s", best_gen[i]);
            $display("\nFinal Fitness: %0d%%", fitness_percent);
            $display("Run completed in %0d cycles.", cycles);

            // Wait a few cycles before restarting
            repeat (10) @(posedge clk);
        end

        // Final global stats
        coverage_count = 0;
        for (integer i = 0; i <= 100; i++) begin
            if (coverage_hit[i]) coverage_count++;
        end

        $display("\n======== Coverage Summary ========");
        $display("Fitness Distribution Coverage: %0d of 101 levels hit (%.2f%%)",
                 coverage_count, 100.0 * coverage_count / 101.0);
        $display("[✔] Functional coverage = %0.2f%%", ga_coverage.get_coverage());
        $finish;
    end

endmodule

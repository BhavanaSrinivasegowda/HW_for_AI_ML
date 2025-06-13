module genetic_algorithm #(parameter MAX_POP = 10, LEN = 12)(
    input  logic clk,
    input  logic rst,
    output logic done,
    output logic [7:0] best_gen[LEN],
    output logic [6:0] fitness_percent
);

    // ----------------------------------------
    // Typedefs
    // ----------------------------------------
    typedef logic [7:0] gene_t;
    typedef gene_t chromosome_t[LEN];

    typedef struct {
        chromosome_t data;
        logic [6:0] fitness;
    } individual_t;

    // ----------------------------------------
    // Internal Variables
    // ----------------------------------------
    individual_t population[MAX_POP];
    individual_t parent[2];
    individual_t child[2];
    individual_t mutant[2];
    individual_t current_best;

    logic [3:0] state;
    logic [31:0] cycle_count;
    logic [6:0] prev_best_fitness;

    chromosome_t target = {"H","e","l","l","o"," ","W","o","r","l","d","!"};

    localparam INIT   = 0,
               SELECT = 1,
               CROSS  = 2,
               MUTATE = 3,
               UPDATE = 4,
               DONE   = 5;

    // ----------------------------------------
    // Random gene generator
    // ----------------------------------------
    function automatic gene_t rand_gene();
        rand_gene = $urandom_range(32, 125);
    endfunction

    // ----------------------------------------
    // Fitness calculation
    // ----------------------------------------
    function automatic logic [6:0] calc_fitness(input chromosome_t gen);
        logic [3:0] score = 0;
        for (int i = 0; i < LEN; i++)
            if (gen[i] == target[i])
                score++;
        calc_fitness = (score * 100) / LEN;
    endfunction

    // ----------------------------------------
    // Main FSM
    // ----------------------------------------
    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            state <= INIT;
            done <= 0;
            cycle_count <= 0;
            prev_best_fitness <= 0;
        end else begin
            cycle_count <= cycle_count + 1;

            case (state)
                INIT: begin
                    for (int i = 0; i < MAX_POP; i++) begin
                        for (int j = 0; j < LEN; j++)
                            population[i].data[j] = rand_gene();
                        population[i].fitness = calc_fitness(population[i].data);
                    end
                    state <= SELECT;
                end

                SELECT: begin
                    parent[0] = population[0];
                    parent[1] = population[1];
                    for (int i = 1; i < MAX_POP; i++) begin
                        if (population[i].fitness > parent[0].fitness) begin
                            parent[1] = parent[0];
                            parent[0] = population[i];
                        end else if (population[i].fitness > parent[1].fitness) begin
                            parent[1] = population[i];
                        end
                    end
                    state <= CROSS;
                end

                CROSS: begin
                    for (int i = 0; i < 2; i++) begin
                        for (int j = 0; j < LEN / 2; j++)
                            child[i].data[j] = parent[i].data[j];
                        for (int j = LEN / 2; j < LEN; j++)
                            child[i].data[j] = parent[1 - i].data[j];
                        child[i].fitness = calc_fitness(child[i].data);
                    end
                    state <= MUTATE;
                end

                MUTATE: begin
                    for (int i = 0; i < 2; i++) begin
                        for (int j = 0; j < LEN; j++) begin
                            if ($urandom_range(0, 99) < 20)
                                child[i].data[j] = rand_gene();
                        end
                        mutant[i].data = child[i].data;
                        mutant[i].fitness = calc_fitness(mutant[i].data);
                    end
                    state <= UPDATE;
                end

                UPDATE: begin
                    for (int i = 0; i < 2; i++) begin
                        int worst_idx = 0;
                        for (int j = 1; j < MAX_POP; j++)
                            if (population[j].fitness < population[worst_idx].fitness)
                                worst_idx = j;
                        if (mutant[i].fitness > population[worst_idx].fitness)
                            population[worst_idx] = mutant[i];
                    end

                    // Manually copy population[0] to current_best
                    for (int k = 0; k < LEN; k++)
                        current_best.data[k] = population[0].data[k];
                    current_best.fitness = population[0].fitness;

                    // Find fittest
                    for (int i = 1; i < MAX_POP; i++) begin
                        if (population[i].fitness > current_best.fitness) begin
                            for (int k = 0; k < LEN; k++)
                                current_best.data[k] = population[i].data[k];
                            current_best.fitness = population[i].fitness;
                        end
                    end

                    if (current_best.fitness > prev_best_fitness) begin
                        prev_best_fitness <= current_best.fitness;
                        for (int k = 0; k < LEN; k++)
                            $write("%s", current_best.data[k]);
                        $write("\t%0.2f%%\t", real'(current_best.fitness));
                        $display("Cycle: %0d", cycle_count);
                    end

                    if (current_best.fitness == 100) begin
                        for (int k = 0; k < LEN; k++)
                            best_gen[k] <= current_best.data[k];
                        fitness_percent <= 100;
                        done <= 1;
                        state <= DONE;
                    end else begin
                        state <= SELECT;
                    end
                end

                DONE: begin
                    // No-op
                end
            endcase
        end
    end

endmodule

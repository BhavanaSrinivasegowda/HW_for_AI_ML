// mutation_sv.sv
module mutation_sv #(
    parameter GENE_LEN = 12,
    parameter CHAR_WIDTH = 8
)(
    input  logic clk,
    input  logic rst,
    input  logic start,
    input  logic [GENE_LEN*CHAR_WIDTH-1:0] child_in,    // Flattened child gene
    input  logic [GENE_LEN*8-1:0] rand_mask,            // One random float (0-255) per char
    input  logic [GENE_LEN*8-1:0] rand_ascii,           // One random ASCII per char
    input  logic [7:0] mutation_thresh,                // Mutation rate * 255 (e.g. 0.2*255)

    output logic [GENE_LEN*CHAR_WIDTH-1:0] mutant_out,
    output logic done
);

    typedef enum logic [1:0] {
        IDLE, PROCESS, FINISH
    } state_t;

    state_t state;
    logic [3:0] idx;

    logic [CHAR_WIDTH-1:0] child [GENE_LEN-1:0];
    logic [CHAR_WIDTH-1:0] mutant [GENE_LEN-1:0];
    logic [7:0] rand_thresh [GENE_LEN-1:0];
    logic [7:0] rand_val [GENE_LEN-1:0];

    always_comb begin
        for (int i = 0; i < GENE_LEN; i++) begin
            child[i] = child_in[i*CHAR_WIDTH +: CHAR_WIDTH];
            rand_thresh[i] = rand_mask[i*8 +: 8];
            rand_val[i] = rand_ascii[i*8 +: 8];
        end
    end

    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            idx <= 0;
            state <= IDLE;
            done <= 0;
        end else begin
            case (state)
                IDLE: begin
                    done <= 0;
                    if (start) begin
                        idx <= 0;
                        state <= PROCESS;
                    end
                end
                PROCESS: begin
                    if (rand_thresh[idx] <= mutation_thresh)
                        mutant[idx] <= rand_val[idx];
                    else
                        mutant[idx] <= child[idx];

                    if (idx == GENE_LEN - 1)
                        state <= FINISH;
                    else
                        idx <= idx + 1;
                end
                FINISH: begin
                    done <= 1;
                    state <= IDLE;
                end
		default: begin
			state <= IDLE;
		end
            endcase
        end
    end

    always_comb begin
        for (int i = 0; i < GENE_LEN; i++) begin
            mutant_out[i*CHAR_WIDTH +: CHAR_WIDTH] = mutant[i];
        end
    end
endmodule


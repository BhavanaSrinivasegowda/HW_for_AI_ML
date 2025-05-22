module spi_slave (
    input wire clk,          // System clock
    input wire rst,
    input wire sck,          // SPI clock from master
    input wire mosi,         // Master Out Slave In
    input wire cs,           // Chip select (active low)
    output wire miso,        // Master In Slave Out
    output reg [7:0] data_out
);

    reg [7:0] shift_reg;
    reg [2:0] bit_cnt;
    reg miso_reg;

    assign miso = miso_reg;

    always @(posedge sck or posedge rst) begin
        if (rst) begin
            shift_reg <= 0;
            bit_cnt <= 0;
            miso_reg <= 0;
        end else if (~cs) begin
            shift_reg <= {shift_reg[6:0], mosi};
            bit_cnt <= bit_cnt + 1;
            if (bit_cnt == 3'd7) begin
                data_out <= {shift_reg[6:0], mosi};
            end
        end
    end
endmodule


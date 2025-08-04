module nand_gate_tb;
    reg a, b;
    wire y;

    // Instantiate the module under test
    nand_gate dut (
        .a(a),
        .b(b),
        .y(y)
    );

    initial begin
        // Test case 1: a=0, b=0 -> y=1
        a = 0; b = 0; #10;
        $display("a=%b, b=%b, y=%b", a, b, y);
        
        // Test case 2: a=0, b=1 -> y=1
        a = 0; b = 1; #10;
        $display("a=%b, b=%b, y=%b", a, b, y);
        
        // Test case 3: a=1, b=0 -> y=1
        a = 1; b = 0; #10;
        $display("a=%b, b=%b, y=%b", a, b, y);
        
        // Test case 4: a=1, b=1 -> y=0
        a = 1; b = 1; #10;
        $display("a=%b, b=%b, y=%b", a, b, y);
        
        $finish;
    end
endmodule
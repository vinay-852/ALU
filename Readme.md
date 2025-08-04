# NAND Gate on an iCE40 FPGA

This project demonstrates a complete Verilog design flow for a simple **NAND gate**, targeting an **iCE40 FPGA** using open-source tools. It guides you through simulation, synthesis, place and route, bitstream generation, and device programming.

## 1. Project Files

* `nand_gate.v`: The Verilog HDL code for the 2-input NAND gate.

* `nand_gate_tb.v`: A Verilog testbench for simulating and verifying the `nand_gate` module.

* `synth.ys`: A Yosys script to synthesize the Verilog design into a gate-level netlist.

* `nand_gate.pcf`: An example Physical Constraints File (PCF) to map the design's I/O signals to specific pins on an iCE40 FPGA board. **You'll need to adjust this for your specific board.**

* `README.md`: This documentation file.

---

## 2. Prerequisites

Before you begin, ensure you have the necessary open-source FPGA toolchain installed on your system.

* **Icarus Verilog (`iverilog`)**: A Verilog compiler for simulation.

* **GTKWave**: A waveform viewer for analyzing simulation results.

* **Yosys**: A Verilog synthesis tool.

* **nextpnr-ice40**: A place and route tool for iCE40 FPGAs.

* **icepack**: A tool to convert the place and route output into a bitstream.

* **iceprog**: A tool to program the iCE40 FPGA.

### Installation (Debian/Ubuntu)

If you're on a Debian or Ubuntu-based system, you can install all these tools using `apt`:

```bash
sudo apt-get update
sudo apt-get install iverilog gtkwave fpga-icestorm
````

-----

## 3\. Design Files

Here are the contents of the core design files:

### `nand_gate.v` (NAND Gate Module)

```verilog
// nand_gate.v
// This module implements a simple two-input NAND gate.
module nand_gate (
    input a,
    input b,
    output y
);

    assign y = ~(a & b);

endmodule
```

### `nand_gate_tb.v` (NAND Gate Testbench)

```verilog
`timescale 1ns / 1ps
module nand_gate_tb;

    // Declare signals for the testbench
    reg a_in;
    reg b_in;
    wire y_out;

    // Instantiate the Device Under Test (DUT)
    nand_gate dut (
        .a(a_in),
        .b(b_in),
        .y(y_out)
    );

    // Initial block to apply stimulus
    initial begin
        // Open VCD file for waveform viewing
        $dumpfile("nand_gate.vcd");
        $dumpvars(0, nand_gate_tb); // Dump all variables in the testbench

        $display("Time | A | B | Y");
        $monitor("%t | %d | %d | %d", $time, a_in, b_in, y_out);

        // Test Case 1: a=0, b=0 -> y=1
        a_in = 0; b_in = 0;
        #10; // Wait 10ns

        // Test Case 2: a=0, b=1 -> y=1
        a_in = 0; b_in = 1;
        #10;

        // Test Case 3: a=1, b=0 -> y=1
        a_in = 1; b_in = 0;
        #10;

        // Test Case 4: a=1, b=1 -> y=0
        a_in = 1; b_in = 1;
        #10;

        // End simulation
        $display("Simulation finished.");
        $finish; // Terminate simulation
    end

endmodule
```

### `synth.ys` (Yosys Synthesis Script)

```ys
# synth.ys
# Read in the Verilog source file
read_verilog nand_gate.v

# Select the top-level module for synthesis
hierarchy -top nand_gate

# Perform synthesis for the iCE40 FPGA family
# Output the netlist in JSON format for nextpnr
synth_ice40 -json nand_gate.json
```

### `nand_gate.pcf` (Physical Constraints File Example)

**IMPORTANT**: This PCF is an example. You **MUST** modify the pin numbers (`34`, `35`, `13`) to match the actual physical pins on your specific iCE40 FPGA development board. Consult your board's documentation for the correct pinout.

```pcf
# nand_gate.pcf
# Example Physical Constraints File for iCE40UP5K (e.g., TinyFPGA BX, iCEstick)

# Map the 'a' input to a physical pin (e.g., a button or header pin)
set_io a 34

# Map the 'b' input to another physical pin
set_io b 35

# Map the 'y' output to a physical pin (e.g., an LED)
set_io y 13
```

-----

## 4\. Build and Program Instructions

Follow these steps in your terminal to build the bitstream and program your FPGA.

### Step 1: Simulate the Design

First, simulate your Verilog design to ensure it behaves as expected.

```bash
iverilog -o nand_gate.vvp nand_gate.v nand_gate_tb.v
vvp nand_gate.vvp
gtkwave nand_gate.vcd
```

After running `gtkwave nand_gate.vcd`, you'll see the waveforms of your inputs and output, confirming the NAND gate's truth table.

### Step 2: Synthesize the Design

Use Yosys to synthesize your Verilog code into a gate-level netlist.

```bash
yosys synth.ys
```

This command will execute the `synth.ys` script, reading `nand_gate.v` and producing `nand_gate.json`.

### Step 3: Place & Route

Use `nextpnr` to map the synthesized netlist to the physical resources of your iCE40 FPGA, considering your pin constraints.

```bash
nextpnr-ice40 --up5k --package sg48 --json nand_gate.json --pcf nand_gate.pcf --asc nand_gate.asc
```

  * `--up5k`: Specifies the target FPGA as iCE40UP5K.

  * `--package sg48`: Specifies the SG48 package (common for many iCE40 boards). Adjust if your board uses a different package.

  * `--json nand_gate.json`: The input netlist from Yosys.

  * `--pcf nand_gate.pcf`: Your physical constraints file.

  * `--asc nand_gate.asc`: The output ASCII file describing the placed and routed design.

### Step 4: Generate the Bitstream

Convert the `.asc` file into a binary bitstream (`.bin`) that can be loaded onto the FPGA.

```bash
icepack nand_gate.asc nand_gate.bin
```

This command generates the `nand_gate.bin` file.

### Step 5: Program the FPGA

Finally, program your iCE40 FPGA board with the generated bitstream.

```bash
iceprog nand_gate.bin
```

Once programmed, your FPGA will now function as a hardware NAND gate\! You can test it by connecting inputs `a` and `b` (e.g., to switches or jumper wires) and observing the output `y` (e.g., connected to an LED).

## 5\. Troubleshooting

  * **`command not found`**: If you encounter errors like `yosys: command not found` or `icepack: command not found`, it means the tools are not installed or not in your system's PATH. Revisit the [Prerequisites](https://www.google.com/search?q=%232-prerequisites) section.

  * **`failed to open PCF file`**: Ensure your `nand_gate.pcf` file exists in the same directory where you run the `nextpnr` command and that its name is spelled correctly.

  * **`Loading PCF failed`**: Double-check the contents of your `nand_gate.pcf`. Make sure the pin numbers and signal names are correct and that there are no syntax errors.

  * **FPGA not programming**: Ensure your FPGA board is correctly connected to your computer via USB and that you have the necessary drivers installed. You might need `sudo` for `iceprog` depending on your system's USB permissions.
  
  * **Simulation issues**: If the simulation does not produce expected results, check your testbench for errors. Ensure that the input signals are being toggled correctly and that the DUT is instantiated properly.
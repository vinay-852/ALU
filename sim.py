import matplotlib.pyplot as plt
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# Create circuit
circuit = Circuit('CMOS Inverter')

# Power supply
circuit.V('dd', 'vdd', circuit.gnd, 5@u_V)

# Input pulse: 0V to 5V square wave
circuit.PulseVoltageSource('input', 'vin', circuit.gnd,
                           initial_value=0@u_V, pulsed_value=5@u_V,
                           pulse_width=5@u_ns, period=10@u_ns,
                           rise_time=1@u_ns, fall_time=1@u_ns)

# CMOS Inverter (PMOS on top, NMOS on bottom)
circuit.MOSFET(1, 'out', 'vin', 'vdd', 'vdd', model='PMOS', length=180@u_nm, width=10@u_um)
circuit.MOSFET(2, 'out', 'vin', circuit.gnd, circuit.gnd, model='NMOS', length=180@u_nm, width=10@u_um)

# Load capacitance
circuit.C(1, 'out', circuit.gnd, 1@u_pF)

# Transistor models
circuit.model('NMOS', 'NMOS')
circuit.model('PMOS', 'PMOS', pmos=True)

# Simulate
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=0.1@u_ns, end_time=50@u_ns)

# Plot
plt.figure(figsize=(10, 5))
plt.plot(analysis.time, analysis['vin'], label='Input (vin)')
plt.plot(analysis.time, analysis['out'], label='Output (out)')
plt.title('CMOS Inverter Simulation')
plt.xlabel('Time [s]')
plt.ylabel('Voltage [V]')
plt.grid(True)
plt.legend()
plt.savefig('inverter_output.png', dpi=300)
plt.show()

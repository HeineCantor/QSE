import numpy as np

import matplotlib.pyplot as plt

from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, transpile

from qiskit.visualization import plot_histogram

# CONSTANTS AND DEFINITIONS

INPUT_REGISTER_SIZE = 3

constantOracle = QuantumCircuit(INPUT_REGISTER_SIZE + 1) # + 1 because it's a boolean operator


balancedOracle = QuantumCircuit(INPUT_REGISTER_SIZE + 1)

stringControlsToWrap = "101"

# X GATES WRAPPING

for i in range(len(stringControlsToWrap)):
    if stringControlsToWrap[i] == '1':
        balancedOracle.x(i)

balancedOracle.barrier()

# CNOTs GENERATION

for qubit in range(INPUT_REGISTER_SIZE):
    balancedOracle.cx(qubit, INPUT_REGISTER_SIZE)

balancedOracle.barrier()

# X GATES FOR UNCOMPUTING

for i in range(len(stringControlsToWrap)):
    if stringControlsToWrap[i] == '1':
        balancedOracle.x(i)

# Building Deutsch-Jozsa ;)

djCircuit = QuantumCircuit(INPUT_REGISTER_SIZE + 1, INPUT_REGISTER_SIZE)

# Hadamard Gates for the input qubits
for qubit in range(INPUT_REGISTER_SIZE):
    djCircuit.h(qubit)

# X to put output qubit in |1> and an Hadamard to put it in |->
djCircuit.x(INPUT_REGISTER_SIZE)
djCircuit.h(INPUT_REGISTER_SIZE)

djCircuit.barrier()

# Adding the oracle

djCircuit.compose(balancedOracle, inplace=True)
#djCircuit.compose(constantOracle, inplace=True)

# Final Layer of Hadamards
for qubit in range(INPUT_REGISTER_SIZE):
    djCircuit.h(qubit)

djCircuit.barrier()

# Measuring!
for i in range(INPUT_REGISTER_SIZE):
    djCircuit.measure(i, i) # put qubit[i] in classical bit[i]

# Simulation time
aerSimulator = Aer.get_backend("aer_simulator")
results = aerSimulator.run(djCircuit).result()
answer = results.get_counts()

djCircuit.draw("mpl")

plot_histogram(answer)

plt.show()

import numpy as np

import matplotlib.pyplot as plt

from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, transpile

from qiskit.visualization import plot_histogram

# PARAMETERS

SHOTS_TO_SIMULATE = 10000

INPUT_SIZE = 3

b = '000'

# function simonsOracle: from a string 'b', get an oracle two-to-one or one-to-one (b = '000') for Simon's Problem
def simonsOracle(b):
    inputLength = len(b)
    simonsOracleCircuit = QuantumCircuit(inputLength * 2)

    # Copying the qubits from first register to second register
    for qubit in range(inputLength):
        simonsOracleCircuit.cx(qubit, qubit + inputLength)

    # If string is not all zeros (aka if not all characters in the string are zeros)
    if not all(character == '0' for character in b):
        for j in range(len(b)):
            if b[j] == '1':
                simonsOracleCircuit.cx(j, inputLength + j)

    return simonsOracleCircuit

# Building Simon's Circuit

simonsCircuit = QuantumCircuit(INPUT_SIZE * 2, INPUT_SIZE)

simonsCircuit.h(range(INPUT_SIZE))

simonsCircuit.barrier()

simonsCircuit.compose(simonsOracle(b), inplace=True)

simonsCircuit.barrier()

simonsCircuit.h(range(INPUT_SIZE))

simonsCircuit.measure(range(INPUT_SIZE), range(INPUT_SIZE))

simonsCircuit.draw("mpl")

# Simulation time
aerSimulator = Aer.get_backend("aer_simulator")
results = aerSimulator.run(simonsCircuit, shots=SHOTS_TO_SIMULATE).result()
answer = results.get_counts()

plot_histogram(answer)

plt.show()

# Then you should solve the linear system obtained


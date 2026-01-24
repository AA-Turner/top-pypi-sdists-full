##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import pytest
from qiskit import QuantumCircuit


@pytest.fixture()
def while_loop():
    circuit = QuantumCircuit(1, 1)
    circuit.name = "Simple while-loop circuit"
    with circuit.while_loop((circuit.clbits[0], 0)):
        circuit.h(0)
        circuit.measure(0, 0)
    return circuit


@pytest.fixture()
def for_loop():
    circuit = QuantumCircuit(4, 0)
    circuit.name = "Simple for-loop circuit"
    circuit.h(3)
    with circuit.for_loop(range(3)):
        # Qiskit doesn't (yet) support cnot(3, i)
        circuit.cx(3, 0)
    return circuit


cf_fixtures = ["while_loop", "for_loop"]

##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from typing import Iterable, List

import pytest
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.circuit import Qubit

from qiskit_qir.capability import (
    Capability,
    ConditionalBranchingOnResultError,
    QubitUseAfterMeasurementError,
)
from qiskit_qir.elements import QiskitModule
from qiskit_qir.visitor import BasicQisVisitor

# test circuits


def use_after_measure():
    qq = QuantumRegister(2, name="qq")
    cr = ClassicalRegister(2, name="cr")
    circuit = QuantumCircuit(qq, cr)

    circuit.h(1)
    circuit.measure(1, 1)
    circuit.h(1)

    return circuit


def use_another_after_measure():
    circuit = QuantumCircuit(3, 2)

    circuit.h(0)
    circuit.measure(0, 0)
    circuit.h(1)
    circuit.cx(1, 2)
    circuit.measure(1, 1)

    return circuit


# Utility using new visitor
def circuit_to_qir(circuit, profile: str = "AdaptiveExecution"):
    module = QiskitModule.from_quantum_circuit(circuit=circuit)
    visitor = BasicQisVisitor(profile)
    module.accept(visitor)
    return visitor.ir()


def test_reuse_after_measurement_fails_without_required_capability():
    circuit = use_after_measure()
    with pytest.raises(QubitUseAfterMeasurementError) as exc_info:
        _ = circuit_to_qir(circuit, "BasicExecution")

    exception_raised = exc_info.value
    assert (
        str(exception_raised.instruction)
        == "Instruction(name='h', num_qubits=1, num_clbits=0, params=[])"
    )
    if hasattr(exception_raised.instruction, "condition"):
        assert exception_raised.instruction.condition is None
    _check_qubits(exception_raised.qargs, [(2, "qq", 1)])
    assert len(exception_raised.cargs) == 0
    assert str(exception_raised.profile) == "BasicExecution"
    assert exception_raised.instruction_string == "h qq[1]"


def _check_qubits(qargs: Iterable[Qubit], expected: List[tuple[int, str, int]]):
    for q in qargs:
        assert isinstance(q, Qubit)
        assert (q._register.size, q._register.name, q._index) in expected


def test_reuse_after_measurement_passes_with_required_capability():
    circuit = use_after_measure()
    _ = circuit_to_qir(circuit)


def test_using_an_unread_qubit_after_measuring_passes_without_required_capability():
    circuit = use_another_after_measure()
    _ = circuit_to_qir(circuit, "BasicExecution")

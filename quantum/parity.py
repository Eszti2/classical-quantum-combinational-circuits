"""
quantum/parity.py
Kvantum paritásgenerátor implementáció.
Bemenet:  n db qubit (q0..qn-1)
Kimenet:  paritásbit (ancilla qubit: qn)
  - Páros paritás (even):   CNOT lánc
  - Páratlan paritás (odd): CNOT lánc + X kapu a végén
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from quantum.utils import get_metrics


def build_circuit(inputs: list[int], mode: str = 'even') -> QuantumCircuit:
    assert len(inputs) >= 2, "Legalább 2 bemenet szükséges"
    assert mode in ('even', 'odd'), "Mode csak 'even' vagy 'odd' lehet"

    n  = len(inputs)
    qr = QuantumRegister(n + 1, 'q')
    cr = ClassicalRegister(1, 'c')
    qc = QuantumCircuit(qr, cr)

    for i, bit in enumerate(inputs):
        if bit == 1:
            qc.x(qr[i])

    qc.barrier()

    for i in range(n):
        qc.cx(qr[i], qr[n])

    if mode == 'odd':
        qc.x(qr[n])

    qc.barrier()

    qc.measure(qr[n], cr[0])

    return qc


def run(inputs: list[int], mode: str = 'even', shots: int = 1024) -> dict:
    qc      = build_circuit(inputs, mode)
    metrics = get_metrics(qc)

    sim    = AerSimulator()
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()

    top    = max(counts, key=counts.get)
    parity = int(top[0])

    return {
        "outputs":    [parity],
        "gate_count": metrics["gate_count"],
        "depth":      metrics["depth"],
        "ancilla":    1,
        "mode":       mode,
    }


def truth_table(n: int = 4, mode: str = 'even', shots: int = 1024) -> list[dict]:
    from itertools import product
    return [
        {"inputs": list(bits), **run(list(bits), mode, shots)}
        for bits in product([0, 1], repeat=n)
    ]
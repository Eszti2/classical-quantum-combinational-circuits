"""
quantum/majority.py
Kvantum majority gate implementáció.
Bemenet:  A (q0), B (q1), C (q2)
Kimenet:  M (q3) = 1 ha legalább 2 bemenet értéke 1
Ancilla:  q3 = kimenet tárolásához

Megjegyzés: a majority gate kvantum megvalósítása strukturálisan azonos
a teljes összeadó Cout blokkjával — mindkettő három CCX kapuból áll.
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from quantum.utils import get_metrics


def build_circuit(inputs: list[int]) -> QuantumCircuit:
    assert len(inputs) == 3, "Majority gate 3 bemenetet vár"

    qr = QuantumRegister(4, 'q')
    cr = ClassicalRegister(1, 'c')
    qc = QuantumCircuit(qr, cr)

    if inputs[0] == 1: qc.x(qr[0])
    if inputs[1] == 1: qc.x(qr[1])
    if inputs[2] == 1: qc.x(qr[2])

    qc.barrier()

    qc.ccx(qr[0], qr[1], qr[3])
    qc.ccx(qr[1], qr[2], qr[3])
    qc.ccx(qr[0], qr[2], qr[3])

    qc.barrier()

    qc.measure(qr[3], cr[0])

    return qc


def run(inputs: list[int], shots: int = 1024) -> dict:
    qc      = build_circuit(inputs)
    metrics = get_metrics(qc)

    sim    = AerSimulator()
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()

    top = max(counts, key=counts.get)
    m   = int(top[0])

    return {
        "outputs":    [m],
        "gate_count": metrics["gate_count"],
        "depth":      metrics["depth"],
        "ancilla":    1,
    }


def truth_table(shots: int = 1024) -> list[dict]:
    return [
        {"inputs": [A, B, C], **run([A, B, C], shots)}
        for A in range(2)
        for B in range(2)
        for C in range(2)
    ]
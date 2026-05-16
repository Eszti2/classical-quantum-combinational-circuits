"""
quantum/full_adder.py
Kvantum teljes összeadó (Full Adder) implementáció.
Bemenet:  A (q0), B (q1), Cin (q2)
Kimenet:  Sum (q1) = A XOR B XOR Cin
          Cout (q3) = (A AND B) OR (B AND Cin) OR (A AND Cin)
Ancilla:  q3 = Cout tárolásához

Megjegyzés: A Cout kiszámításához 3 CCX kaput alkalmazunk, amely közvetlenül
tükrözi a logikai kifejezést: Cout = (A·B) + (A·Cin) + (B·Cin).
Létezik 2 CCX + 2 CX kapuval megvalósítható optimalizált verzió (Cuccaro et al., 2004),
amely a közbülső A⊕B jelet újrafelhasználja — azonban ez a pedagógiai
átláthatóságot csökkenti, ezért a referencia implementáció a 3 CCX struktúrát alkalmazza.
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from quantum.utils import get_metrics


def build_circuit(inputs: list[int]) -> QuantumCircuit:
    assert len(inputs) == 3, "Full Adder 3 bemenetet vár"

    qr = QuantumRegister(4, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr)

    if inputs[0] == 1: qc.x(qr[0])
    if inputs[1] == 1: qc.x(qr[1])
    if inputs[2] == 1: qc.x(qr[2])

    qc.barrier()

    qc.ccx(qr[0], qr[1], qr[3])
    qc.ccx(qr[0], qr[2], qr[3])
    qc.ccx(qr[1], qr[2], qr[3])
    qc.cx(qr[0], qr[1])
    qc.cx(qr[2], qr[1])

    qc.barrier()

    qc.measure(qr[1], cr[0])
    qc.measure(qr[3], cr[1])

    return qc


def run(inputs: list[int], shots: int = 1024) -> dict:
    qc         = build_circuit(inputs)
    init_gates = sum(inputs)
    metrics    = get_metrics(qc, init_gate_count=init_gates)

    sim    = AerSimulator()
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()

    top      = max(counts, key=counts.get)
    cout_bit = int(top[0])
    sum_bit  = int(top[1])

    return {
        "outputs":    [sum_bit, cout_bit],
        "gate_count": metrics["gate_count"],
        "depth":      metrics["depth"],
        "ancilla":    1,
    }


def truth_table(shots: int = 1024) -> list[dict]:
    return [
        {"inputs": [A, B, Cin], **run([A, B, Cin], shots)}
        for A in range(2)
        for B in range(2)
        for Cin in range(2)
    ]

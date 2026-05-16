"""
quantum/comparator.py
Kvantum komparátor implementáció.
Bemenet:  A és B – n bites bináris számok (qubitek)
Kimenet:  gt (A>B), eq (A=B), lt (A<B)

Megvalósítás:
- eq: CNOT lánc + X (XNOR) + MCX → egyenlőség detektálás
- gt: MSB-től bitenkénti összehasonlítás, prev_eq ancillával
- lt: NOT(gt) AND NOT(eq) → CCX kapuval

Ancilla qubitek: xnor (n db) + prev_eq (n db) = 2n db
Kimenet qubitek: gt, eq, lt (3 db) — ezek nem ancillák
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from quantum.utils import get_metrics


def build_circuit(a: list[int], b: list[int]) -> QuantumCircuit:
    assert len(a) == len(b), "A és B ugyanolyan hosszú kell legyen"
    n = len(a)

    qr_a       = QuantumRegister(n, 'a')
    qr_b       = QuantumRegister(n, 'b')
    qr_gt      = QuantumRegister(1, 'gt')
    qr_eq      = QuantumRegister(1, 'eq')
    qr_lt      = QuantumRegister(1, 'lt')
    qr_xnor    = QuantumRegister(n, 'xnor')
    qr_prev_eq = QuantumRegister(n, 'peq')
    cr         = ClassicalRegister(3, 'c')

    qc = QuantumCircuit(qr_a, qr_b, qr_gt, qr_eq, qr_lt,
                        qr_xnor, qr_prev_eq, cr)

    for i, bit in enumerate(a):
        if bit == 1: qc.x(qr_a[i])
    for i, bit in enumerate(b):
        if bit == 1: qc.x(qr_b[i])

    qc.barrier()

    for i in range(n):
        qc.cx(qr_a[i], qr_xnor[i])
        qc.cx(qr_b[i], qr_xnor[i])
        qc.x(qr_xnor[i])

    qc.mcx(list(qr_xnor), qr_eq[0])

    for i in range(n):
        qc.x(qr_xnor[i])
        qc.cx(qr_b[i], qr_xnor[i])
        qc.cx(qr_a[i], qr_xnor[i])

    qc.barrier()

    qc.x(qr_b[0])
    qc.ccx(qr_a[0], qr_b[0], qr_gt[0])
    qc.x(qr_b[0])

    qc.cx(qr_a[0], qr_xnor[0])
    qc.cx(qr_b[0], qr_xnor[0])
    qc.x(qr_xnor[0])
    qc.cx(qr_xnor[0], qr_prev_eq[0])
    qc.x(qr_xnor[0])
    qc.cx(qr_b[0], qr_xnor[0])
    qc.cx(qr_a[0], qr_xnor[0])

    for i in range(1, n):
        qc.cx(qr_a[i], qr_xnor[i])
        qc.cx(qr_b[i], qr_xnor[i])
        qc.x(qr_xnor[i])
        qc.ccx(qr_prev_eq[i-1], qr_xnor[i], qr_prev_eq[i])
        qc.x(qr_b[i])
        qc.mcx([qr_prev_eq[i-1], qr_a[i], qr_b[i]], qr_gt[0])
        qc.x(qr_b[i])
        qc.x(qr_xnor[i])
        qc.cx(qr_b[i], qr_xnor[i])
        qc.cx(qr_a[i], qr_xnor[i])

    for i in range(n - 1, 0, -1):
        qc.cx(qr_a[i], qr_xnor[i])
        qc.cx(qr_b[i], qr_xnor[i])
        qc.x(qr_xnor[i])
        qc.ccx(qr_prev_eq[i-1], qr_xnor[i], qr_prev_eq[i])
        qc.x(qr_xnor[i])
        qc.cx(qr_b[i], qr_xnor[i])
        qc.cx(qr_a[i], qr_xnor[i])

    qc.cx(qr_a[0], qr_xnor[0])
    qc.cx(qr_b[0], qr_xnor[0])
    qc.x(qr_xnor[0])
    qc.cx(qr_xnor[0], qr_prev_eq[0])
    qc.x(qr_xnor[0])
    qc.cx(qr_b[0], qr_xnor[0])
    qc.cx(qr_a[0], qr_xnor[0])

    qc.barrier()

    qc.x(qr_gt[0])
    qc.x(qr_eq[0])
    qc.ccx(qr_gt[0], qr_eq[0], qr_lt[0])
    qc.x(qr_gt[0])
    qc.x(qr_eq[0])

    qc.barrier()

    qc.measure(qr_gt[0], cr[0])
    qc.measure(qr_eq[0], cr[1])
    qc.measure(qr_lt[0], cr[2])

    return qc


def run(a: list[int], b: list[int], shots: int = 1024) -> dict:
    qc         = build_circuit(a, b)
    init_gates = sum(a) + sum(b)
    metrics    = get_metrics(qc, init_gate_count=init_gates)

    sim    = AerSimulator()
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()

    top = max(counts, key=counts.get)
    lt  = int(top[0])
    eq  = int(top[1])
    gt  = int(top[2])

    n     = len(a)
    a_val = sum(bit * (2 ** (n - 1 - i)) for i, bit in enumerate(a))
    b_val = sum(bit * (2 ** (n - 1 - i)) for i, bit in enumerate(b))

    return {
        "outputs":       [gt, eq, lt],
        "gate_count":    metrics["gate_count"],
        "depth":         metrics["depth"],
        "ancilla":       2 * n,
        "output_qubits": 3,
        "a_val":         a_val,
        "b_val":         b_val
    }


def truth_table(n: int = 2, shots: int = 1024) -> list[dict]:
    from itertools import product
    return [
        {"a": list(a), "b": list(b), **run(list(a), list(b), shots)}
        for a in product([0, 1], repeat=n)
        for b in product([0, 1], repeat=n)
    ]

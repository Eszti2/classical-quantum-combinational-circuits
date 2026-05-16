"""
quantum/multiplexer.py
Kvantum multiplexer (MUX) implementáció.
Bemenet:  n select qubit + 2^n adat qubit
Kimenet:  Y qubit = a select qubitek által kiválasztott adat qubit értéke
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from quantum.utils import get_metrics


def build_circuit(select: list[int], data: list[int]) -> QuantumCircuit:
    n        = len(select)
    num_data = 2 ** n

    assert len(data) == num_data, f"2^{n} = {num_data} adatbemenet szükséges"

    qr_sel  = QuantumRegister(n, 'sel')
    qr_data = QuantumRegister(num_data, 'dat')
    qr_out  = QuantumRegister(1, 'out')
    cr      = ClassicalRegister(1, 'c')
    qc      = QuantumCircuit(qr_sel, qr_data, qr_out, cr)

    for i, bit in enumerate(select):
        if bit == 1:
            qc.x(qr_sel[i])

    for i, bit in enumerate(data):
        if bit == 1:
            qc.x(qr_data[i])

    qc.barrier()

    for i in range(num_data):
        flipped = []
        for bit_pos in range(n):
            if not ((i >> (n - 1 - bit_pos)) & 1):
                qc.x(qr_sel[bit_pos])
                flipped.append(bit_pos)

        controls = list(qr_sel) + [qr_data[i]]
        qc.mcx(controls, qr_out[0])

        for bit_pos in flipped:
            qc.x(qr_sel[bit_pos])

    qc.barrier()

    qc.measure(qr_out[0], cr[0])

    return qc


def run(select: list[int], data: list[int], shots: int = 1024) -> dict:
    qc         = build_circuit(select, data)
    init_gates = sum(select) + sum(data)
    metrics    = get_metrics(qc, init_gate_count=init_gates)

    sim    = AerSimulator()
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()

    top = max(counts, key=counts.get)
    y   = int(top[0])

    n        = len(select)
    selected = sum(bit * (2 ** (n - 1 - i)) for i, bit in enumerate(select))

    return {
        "outputs":    [y],
        "gate_count": metrics["gate_count"],
        "depth":      metrics["depth"],
        "ancilla":    1,
        "selected":   selected,
    }


def truth_table(n: int = 2, shots: int = 1024) -> list[dict]:
    from itertools import product
    num_data = 2 ** n
    data     = [i % 2 for i in range(num_data)]

    return [
        {"select": list(sel), "data": data, **run(list(sel), data, shots)}
        for sel in product([0, 1], repeat=n)
    ]

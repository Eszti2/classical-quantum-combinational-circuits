"""
quantum/half_adder.py
Kvantum féladder implementáció.
Bemenet:  A (q0), B (q1)
Kimenet:  Sum (q1) = A XOR B,  Carry (q2) = A AND B
Ancilla:  q2 = Carry tárolásához
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from quantum.utils import get_metrics


def build_circuit(inputs: list[int]) -> QuantumCircuit:
    """
    Felépíti a kvantum féladder áramkört.

    Args:
        inputs: [A, B] – mindkettő 0 vagy 1

    Returns:
        Mérésre kész QuantumCircuit
    """
    assert len(inputs) == 2, "Féladder 2 bemenetet vár"

    qr = QuantumRegister(3, 'q')   # q0=A, q1=B, q2=Carry (ancilla)
    cr = ClassicalRegister(2, 'c') # c0=Sum, c1=Carry
    qc = QuantumCircuit(qr, cr)

    # Bemenet inicializálása
    if inputs[0] == 1:
        qc.x(qr[0])
    if inputs[1] == 1:
        qc.x(qr[1])

    qc.barrier()

    # Carry = A AND B → CCX (Toffoli)
    qc.ccx(qr[0], qr[1], qr[2])

    # Sum = A XOR B → CNOT
    qc.cx(qr[0], qr[1])

    qc.barrier()

    # Mérés
    qc.measure(qr[1], cr[0])  # Sum → c0
    qc.measure(qr[2], cr[1])  # Carry → c1

    return qc


def run(inputs: list[int], shots: int = 1024) -> dict:
    """
    Futtatja a kvantum féladder áramkört szimulátorban.

    Args:
        inputs: [A, B]
        shots:  mérések száma

    Returns:
        {
          "outputs":    [Sum, Carry],
          "gate_count": int,
          "depth":      int,
          "ancilla":    int,
        }
    """
    qc         = build_circuit(inputs)
    init_gates = sum(inputs)
    metrics    = get_metrics(qc, init_gate_count=init_gates)

    # Szimuláció
    sim    = AerSimulator()
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()

    # Qiskit fordított bitsorrend: "carry sum"
    top       = max(counts, key=counts.get)
    carry_bit = int(top[0])
    sum_bit   = int(top[1])

    return {
        "outputs":    [sum_bit, carry_bit],
        "gate_count": metrics["gate_count"],
        "depth":      metrics["depth"],
        "ancilla":    1,
    }


def truth_table(shots: int = 1024) -> list[dict]:
    """Visszaadja a teljes igazságtáblát."""
    return [
        {"inputs": [A, B], **run([A, B], shots)}
        for A in range(2)
        for B in range(2)
    ]

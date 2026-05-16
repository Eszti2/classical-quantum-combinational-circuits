"""
quantum/utils.py
Közös segédfüggvények a kvantum implementációkhoz.
"""

from qiskit import QuantumCircuit


def get_metrics(qc: QuantumCircuit, init_gate_count: int = 0) -> dict:
    """
    Kiszámítja az áramkör metrikáit — barrier és inicializáló kapuk nélkül.

    Args:
        qc:              mérésre kész QuantumCircuit
        init_gate_count: inicializáló X kapuk száma (ezek nem logikai kapuk)

    Returns:
        {
          "gate_count": int,  # logikai kapuk száma
          "depth":      int,  # áramköri mélység
        }
    """
    qc_copy = qc.copy()
    qc_copy.remove_final_measurements(inplace=True)
    ops = {k: v for k, v in qc_copy.count_ops().items() if k != 'barrier'}
    return {
        "gate_count": sum(ops.values()) - init_gate_count,
        "depth":      qc_copy.depth()
    }

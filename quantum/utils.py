"""
quantum/utils.py
Közös segédfüggvények a kvantum implementációkhoz.
"""

from qiskit import QuantumCircuit


def get_metrics(qc: QuantumCircuit) -> dict:
    """
    Kiszámítja az áramkör metrikáit — barrier nélkül.

    Args:
        qc: mérésre kész QuantumCircuit

    Returns:
        {
          "gate_count": int,  # kapuk száma barrier nélkül
          "depth":      int,  # áramköri mélység
        }
    """
    qc_copy = qc.copy()
    qc_copy.remove_final_measurements(inplace=True)
    ops = {k: v for k, v in qc_copy.count_ops().items() if k != 'barrier'}
    return {
        "gate_count": sum(ops.values()),
        "depth":      qc_copy.depth()
    }
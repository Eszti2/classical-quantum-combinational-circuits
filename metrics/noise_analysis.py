"""
metrics/noise_analysis.py
Zajérzékenység mérés depolarizációs zajmodellel.
Minden hálózatra megméri a pontosságot különböző hibaarányok mellett.
"""

from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit import QuantumCircuit
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quantum.half_adder  import build_circuit as ha_circuit
from quantum.full_adder  import build_circuit as fa_circuit
from quantum.parity      import build_circuit as par_circuit
from quantum.majority    import build_circuit as maj_circuit
from quantum.multiplexer import build_circuit as mux_circuit
from quantum.comparator  import build_circuit as cmp_circuit


# ── Zajmodell építése ────────────────────────────────────────────────────────

def build_noise_model(error_rate: float) -> NoiseModel:
    """
    Depolarizációs zajmodellt épít a megadott hibaaránnyal.
    """
    noise_model = NoiseModel()
    error_1q = depolarizing_error(error_rate, 1)
    error_2q = depolarizing_error(error_rate, 2)
    error_3q = depolarizing_error(error_rate, 3)

    noise_model.add_all_qubit_quantum_error(error_1q, ['x', 'h', 't', 's', 'id'])
    noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])
    noise_model.add_all_qubit_quantum_error(error_3q, ['ccx'])

    return noise_model


# ── Pontosság mérése ─────────────────────────────────────────────────────────

def measure_accuracy(qc: QuantumCircuit,
                     expected: str,
                     error_rate: float,
                     shots: int = 1024) -> float:
    """
    Megméri hogy az áramkör helyes eredményt ad-e zajos szimulátorban.
    """
    noise_model = build_noise_model(error_rate)
    sim = AerSimulator(noise_model=noise_model)
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()
    correct = counts.get(expected, 0)
    return correct / shots


# ── Hálózatonkénti tesztek ───────────────────────────────────────────────────

def test_half_adder(error_rates: list[float], shots: int = 1024) -> dict:
    """Féladder zajérzékenység: A=1, B=1 → Sum=0, Carry=1 → '10'"""
    results = []
    qc = ha_circuit([1, 1])
    for rate in error_rates:
        acc = measure_accuracy(qc, "10", rate, shots)
        results.append(acc)
    return {"name": "Féladder", "accuracies": results}


def test_full_adder(error_rates: list[float], shots: int = 1024) -> dict:
    """Teljes összeadó zajérzékenység: A=1, B=1, Cin=1 → Sum=1, Cout=1 → '11'"""
    results = []
    qc = fa_circuit([1, 1, 1])
    for rate in error_rates:
        acc = measure_accuracy(qc, "11", rate, shots)
        results.append(acc)
    return {"name": "Teljes összeadó", "accuracies": results}


def test_parity(error_rates: list[float], shots: int = 1024) -> dict:
    """Paritásgenerátor zajérzékenység: [1,0,1,0] → páros paritás → '0'"""
    results = []
    qc = par_circuit([1, 0, 1, 0], mode='even')
    for rate in error_rates:
        acc = measure_accuracy(qc, "0", rate, shots)
        results.append(acc)
    return {"name": "Paritásgenerátor", "accuracies": results}


def test_majority(error_rates: list[float], shots: int = 1024) -> dict:
    """Majority gate zajérzékenység: A=1, B=1, C=0 → M=1 → '1'"""
    results = []
    qc = maj_circuit([1, 1, 0])
    for rate in error_rates:
        acc = measure_accuracy(qc, "1", rate, shots)
        results.append(acc)
    return {"name": "Majority gate", "accuracies": results}


def test_multiplexer(error_rates: list[float], shots: int = 1024) -> dict:
    """Multiplexer zajérzékenység: S=[1,0], D=[0,1,0,1] → Y=0 → '0'"""
    results = []
    qc = mux_circuit([1, 0], [0, 1, 0, 1])
    for rate in error_rates:
        acc = measure_accuracy(qc, "0", rate, shots)
        results.append(acc)
    return {"name": "Multiplexer", "accuracies": results}


def test_comparator(error_rates: list[float], shots: int = 1024) -> dict:
    """Komparátor zajérzékenység: A=[1,0], B=[0,1] → gt=1,eq=0,lt=0 → '001'"""
    results = []
    qc = cmp_circuit([1, 0], [0, 1])
    for rate in error_rates:
        acc = measure_accuracy(qc, "001", rate, shots)
        results.append(acc)
    return {"name": "Komparátor", "accuracies": results}


# ── Főprogram ────────────────────────────────────────────────────────────────

def run_all(shots: int = 1024) -> dict:
    """
    Lefuttatja az összes hálózat zajérzékenység mérését.
    """
    error_rates = [0.0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2]

    print("Zajérzékenység mérés indítása...")
    results = []

    tests = [
        test_half_adder,
        test_full_adder,
        test_parity,
        test_majority,
        test_multiplexer,
        test_comparator,
    ]

    for test_fn in tests:
        print(f"  {test_fn.__name__}...")
        result = test_fn(error_rates, shots)
        results.append(result)
        print(f"    → {[f'{a:.2f}' for a in result['accuracies']]}")

    return {
        "error_rates": error_rates,
        "results": results
    }


if __name__ == "__main__":
    data = run_all(shots=1024)

    print("\n=== EREDMÉNYEK ===")
    print(f"Hibaarányok: {data['error_rates']}")
    for r in data['results']:
        print(f"\n{r['name']}:")
        for rate, acc in zip(data['error_rates'], r['accuracies']):
            print(f"  p={rate:.3f} → {acc:.3f}")
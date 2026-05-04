"""
classical/half_adder.py
Klasszikus féladder implementáció.
Bemenet:  A, B  (1 bit)
Kimenet:  Sum = A XOR B,  Carry = A AND B
"""


def run(inputs: list[int]) -> dict:
    """
    Klasszikus féladder futtatása.

    Args:
        inputs: [A, B] – mindkettő 0 vagy 1

    Returns:
        {
          "outputs":    [Sum, Carry],
          "gate_count": int,   # XOR + AND = 2
        }
    """
    assert len(inputs) == 2, "Féladder 2 bemenetet vár"
    assert all(b in (0, 1) for b in inputs), "Bitek csak 0 vagy 1 lehetnek"

    A, B = inputs
    s = A ^ B    # XOR → Sum
    c = A & B    # AND → Carry

    return {
        "outputs":    [s, c],
        "gate_count": 2,      # 1 XOR + 1 AND
    }


def truth_table() -> list[dict]:
    """Visszaadja a teljes igazságtáblát."""
    return [
        {"inputs": [A, B], **run([A, B])}
        for A in range(2)
        for B in range(2)
    ]


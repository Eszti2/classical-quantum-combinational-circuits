"""
classical/majority.py
Klasszikus majority gate (többségi kapu) implementáció.
Bemenet:  A, B, C (1-1 bit)
Kimenet:  M = 1 ha legalább 2 bemenet értéke 1
          M = (A AND B) OR (B AND C) OR (A AND C)
"""


def run(inputs: list[int]) -> dict:
    """
    Klasszikus majority gate futtatása.

    Args:
        inputs: [A, B, C] – mindhárom 0 vagy 1

    Returns:
        {
          "outputs":    [M],
          "gate_count": int,   # 3 AND + 2 OR = 5
        }
    """
    assert len(inputs) == 3, "Majority gate 3 bemenetet vár"
    assert all(b in (0, 1) for b in inputs), "Bitek csak 0 vagy 1 lehetnek"

    A, B, C = inputs

    m = (A & B) | (B & C) | (A & C)   # 3 AND + 2 OR

    return {
        "outputs":    [m],
        "gate_count": 5,    # 3 AND + 2 OR
    }


def truth_table() -> list[dict]:
    """Visszaadja a teljes igazságtáblát."""
    return [
        {"inputs": [A, B, C], **run([A, B, C])}
        for A in range(2)
        for B in range(2)
        for C in range(2)
    ]
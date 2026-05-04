"""
classical/full_adder.py
Klasszikus teljes összeadó (Full Adder) implementáció.
Bemenet:  A, B, Cin
Kimenet:  Sum = A XOR B XOR Cin
          Cout = (A AND B) OR ((A XOR B) AND Cin)

Megvalósítás (Mano, Digital Design):
  w    = A XOR B          # közbülső jel
  Sum  = w XOR Cin        # 2 XOR
  Cout = (A AND B) OR (w AND Cin)  # 2 AND + 1 OR
  Összesen: 2 XOR + 2 AND + 1 OR = 5 kapu
"""


def run(inputs: list[int]) -> dict:
    """
    Klasszikus Full Adder futtatása.

    Args:
        inputs: [A, B, Cin] – mindhárom 0 vagy 1

    Returns:
        {
          "outputs":    [Sum, Cout],
          "gate_count": int
        }
    """
    assert len(inputs) == 3, "Full Adder 3 bemenetet vár"
    assert all(b in (0, 1) for b in inputs), "Bitek csak 0 vagy 1 lehetnek"

    A, B, Cin = inputs

    w    = A ^ B                  # XOR → közbülső jel
    s    = w ^ Cin                # XOR → Sum
    c    = (A & B) | (w & Cin)   # AND + OR → Cout

    return {
        "outputs":    [s, c],
        "gate_count": 5,          # 2 XOR + 2 AND + 1 OR
    }


def truth_table() -> list[dict]:
    """Visszaadja a teljes igazságtáblát."""
    return [
        {"inputs": [A, B, Cin], **run([A, B, Cin])}
        for A in range(2)
        for B in range(2)
        for Cin in range(2)
    ]
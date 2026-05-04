"""
classical/parity.py
Klasszikus paritásgenerátor implementáció.
Bemenet:  n db bit (tetszőleges hossz)
Kimenet:  paritásbit
  - Páros paritás (even):   XOR lánc
  - Páratlan paritás (odd): XOR lánc + inverz (XNOR)
"""


def run(inputs: list[int], mode: str = 'even') -> dict:
    """
    Klasszikus paritásgenerátor futtatása.

    Args:
        inputs: tetszőleges hosszú bitlista, pl. [1, 0, 1, 0]
        mode:   'even' = páros paritás, 'odd' = páratlan paritás

    Returns:
        {
          "outputs":    [paritásbit],
          "gate_count": int,
          "mode":       str
        }
    """
    assert len(inputs) >= 2, "Legalább 2 bemenet szükséges"
    assert all(b in (0, 1) for b in inputs), "Bitek csak 0 vagy 1 lehetnek"
    assert mode in ('even', 'odd'), "Mode csak 'even' vagy 'odd' lehet"

    # XOR lánc: n-1 XOR kapu
    parity = 0
    for b in inputs:
        parity ^= b

    # Páratlan paritásnál invertáljuk a kimenetet (XNOR)
    if mode == 'odd':
        parity ^= 1

    return {
        "outputs":    [parity],
        "gate_count": len(inputs) - 1 if mode == 'even' else len(inputs),
        "mode":       mode
    }


def truth_table(n: int = 4, mode: str = 'even') -> list[dict]:
    """
    Visszaadja az igazságtáblát n bites bemenetre.

    Args:
        n:    bemeneti bitek száma
        mode: 'even' vagy 'odd'
    """
    from itertools import product
    return [
        {"inputs": list(bits), **run(list(bits), mode)}
        for bits in product([0, 1], repeat=n)
    ]
"""
classical/comparator.py
Klasszikus komparátor implementáció.
Bemenet:  A és B – n bites bináris számok
Kimenet:  A>B, A=B, A<B

Megvalósítás (Mano, Digital Design):
- eq: n XOR + n NOT + (n-1) AND = 3n-1 kapu
      (minden bitpárra XOR → NOT → AND lánc)
- gt: MSB-től bitenkénti összehasonlítás
      A_i=1, B_i=0 és minden előző bit egyenlő
- lt: szimmetrikusan gt-vel
"""


def run(a: list[int], b: list[int]) -> dict:
    """
    Klasszikus komparátor futtatása.

    Args:
        a: [A0, A1, ..., An-1] – első szám bitjei (A0 = MSB)
        b: [B0, B1, ..., Bn-1] – második szám bitjei (B0 = MSB)

    Returns:
        {
          "outputs":    [gt, eq, lt],  # A>B, A=B, A<B
          "gate_count": int,
          "a_val":      int,
          "b_val":      int
        }
    """
    assert len(a) == len(b), "A és B ugyanolyan hosszú kell legyen"
    assert all(bit in (0, 1) for bit in a + b), "Bitek csak 0 vagy 1 lehetnek"

    n = len(a)

    # Decimális értékek
    a_val = sum(bit * (2 ** (n - 1 - i)) for i, bit in enumerate(a))
    b_val = sum(bit * (2 ** (n - 1 - i)) for i, bit in enumerate(b))

    gt = 1 if a_val > b_val else 0
    eq = 1 if a_val == b_val else 0
    lt = 1 if a_val < b_val else 0

    # Kapuszám (Mano alapján):
    # eq:  n XOR + n NOT + (n-1) AND = 3n-1 kapu
    # gt:  n NOT(B) + n AND(A, NOT_B) + (n-1) AND(prev_eq, ...) + (n-1) OR = 4n-2 kapu
    # lt:  szimmetrikusan gt-vel = 4n-2 kapu
    # Összesen: (3n-1) + (4n-2) + (4n-2) = 11n-5 kapu
    gate_count = 11 * n - 5

    return {
        "outputs":    [gt, eq, lt],
        "gate_count": gate_count,
        "a_val":      a_val,
        "b_val":      b_val
    }


def truth_table(n: int = 2) -> list[dict]:
    """Visszaadja a teljes igazságtáblát n bites bemenetekre."""
    from itertools import product
    return [
        {"a": list(a), "b": list(b), **run(list(a), list(b))}
        for a in product([0, 1], repeat=n)
        for b in product([0, 1], repeat=n)
    ]
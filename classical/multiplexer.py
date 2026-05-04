"""
classical/multiplexer.py
Klasszikus multiplexer (MUX) implementáció.
Bemenet:  n select bit + 2^n adatbemenet
Kimenet:  Y = a select bitek által kiválasztott adatbemenet értéke

Például 2 select bittel (4-to-1 MUX):
Y = (S̄₁·S̄₀·D0) + (S̄₁·S₀·D1) + (S₁·S̄₀·D2) + (S₁·S₀·D3)

Jelölés: select[0] = MSB = S_{n-1}, select[n-1] = LSB = S0
"""


def run(select: list[int], data: list[int]) -> dict:
    """
    Klasszikus multiplexer futtatása.

    Args:
        select: [S_{n-1}, ..., S0] – select bitek (select[0] = MSB)
        data:   [D0, D1, ..., D2^n-1] – adatbemenetek

    Returns:
        {
          "outputs":    [Y],
          "gate_count": int,
          "selected":   int  – melyik adatbemenet lett kiválasztva
        }
    """
    n = len(select)
    assert len(data) == 2 ** n, f"2^{n} = {2**n} adatbemenet szükséges"
    assert all(b in (0, 1) for b in select), "Select bitek csak 0 vagy 1 lehetnek"
    assert all(b in (0, 1) for b in data),   "Adatbitek csak 0 vagy 1 lehetnek"

    # A kiválasztott adatbemenet indexe
    selected = sum(bit * (2 ** (n - 1 - i)) for i, bit in enumerate(select))

    y = data[selected]

    # Kapuszám (kétbemenetes kapukkal):
    # n NOT + 2^n AND (mindegyik n+1 bemenetű, de n NOT + 1 AND lánccal)
    # + (2^n - 1) OR a termek összefűzéséhez
    # Összesen: n + 2^n + (2^n - 1) = n + 2^(n+1) - 1
    gate_count = n + 2 ** (n + 1) - 1

    return {
        "outputs":    [y],
        "gate_count": gate_count,
        "selected":   selected
    }


def truth_table(n: int = 2) -> list[dict]:
    """
    Visszaadja az igazságtáblát n select bites MUX-ra.
    Az adatbemenetek értékeit rögzítjük: D0=0, D1=1, D2=0, D3=1...

    Args:
        n: select bitek száma (pl. n=2 → 4-to-1 MUX)
    """
    from itertools import product
    num_data = 2 ** n
    data = [i % 2 for i in range(num_data)]

    return [
        {"select": list(sel), "data": data, **run(list(sel), data)}
        for sel in product([0, 1], repeat=n)
    ]
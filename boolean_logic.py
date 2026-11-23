"""Operaciones y utilidades de evaluación para lógica booleana."""

from itertools import product
from typing import Callable, Iterable, Mapping, TypedDict


class GateSpec(TypedDict):
    kind: str
    inputs: list[str]
    output: str


def NOT(a: int) -> int:
    return 1 - int(bool(a))


def AND(*values: int) -> int:
    return int(all(values))


def OR(*values: int) -> int:
    return int(any(values))


def XOR(*values: int) -> int:
    return sum(values) % 2


def XNOR(a: int, b: int) -> int:
    return int(a == b)


GATE_FUNCTIONS: dict[str, Callable[..., int]] = {
    "NOT": NOT,
    "AND": AND,
    "OR": OR,
    "NAND": lambda *values: NOT(AND(*values)),
    "NOR": lambda *values: NOT(OR(*values)),
    "XOR": XOR,
    "XNOR": XNOR,
}


def evaluate_gates(
    inputs: Mapping[str, int], gates: Iterable[GateSpec]
) -> dict[str, int]:
    """Evalúa un circuito acíclico ordenado y devuelve todos sus cables."""
    signals = {name: int(bool(value)) for name, value in inputs.items()}
    for gate in gates:
        gate_inputs = [signals[name] for name in gate["inputs"]]
        signals[gate["output"]] = GATE_FUNCTIONS[gate["kind"]](*gate_inputs)
    return signals


def truth_table(
    variables: tuple[str, ...], expressions: Mapping[str, Callable[..., int]]
) -> list[dict[str, int]]:
    """Genera filas en orden binario descendente, empezando por todos los ceros."""
    rows = []
    for bits in product((0, 1), repeat=len(variables)):
        row = dict(zip(variables, bits))
        for label, expression in expressions.items():
            row[label] = int(bool(expression(*bits)))
        rows.append(row)
    return rows


LAWS = [
    (
        "Identidad",
        r"A + 0 = A,\qquad A\cdot 1 = A",
        "Sumar 0 o multiplicar por 1 no cambia la señal. Sirve para reconocer operaciones que no alteran una función.",
    ),
    (
        "Elemento nulo",
        r"A + 1 = 1,\qquad A\cdot 0 = 0",
        "En una OR, una entrada en 1 fuerza la salida a 1; en una AND, una entrada en 0 fuerza la salida a 0.",
    ),
    (
        "Idempotencia",
        r"A + A = A,\qquad A\cdot A = A",
        "Repetir la misma señal en una operación no añade información ni cambia el resultado.",
    ),
    (
        "Complemento",
        r"A + A' = 1,\qquad A\cdot A' = 0",
        "Una señal y su complemento siempre son opuestos: una de las dos vale 1 y nunca valen 1 a la vez.",
    ),
    (
        "Doble negación",
        r"(A')' = A",
        "Invertir dos veces recupera el valor original, igual que pasar por dos inversores en serie.",
    ),
    (
        "Absorción",
        r"A + A\cdot B = A,\qquad A\cdot(A+B)=A",
        "Cuando A ya determina el resultado, agregar un término que depende de A y de otra señal es redundante.",
    ),
    (
        "Combinación",
        r"A\cdot B + A\cdot B' = A",
        "Los dos casos posibles de B quedan cubiertos; por eso el resultado depende solamente de A.",
    ),
    (
        "Distributividad",
        r"A\cdot(B+C)=A\cdot B+A\cdot C",
        "Permite pasar de producto de una suma a suma de productos, una forma útil para diseñar circuitos.",
    ),
    (
        "Teorema del consenso",
        r"A\cdot B+A'\cdot C+B\cdot C=A\cdot B+A'\cdot C",
        "El término que combina B y C es redundante porque queda cubierto por los otros dos términos.",
    ),
    (
        "Leyes de De Morgan",
        r"(A\cdot B)'=A'+B',\qquad (A+B)'=A'\cdot B'",
        "Al negar una expresión, se niega cada entrada y se intercambia AND por OR, o OR por AND.",
    ),
    (
        "Dualidad",
        r"+\leftrightarrow\cdot,\qquad 0\leftrightarrow 1",
        "Al intercambiar suma por producto y 0 por 1 en una identidad, se obtiene su identidad dual.",
    ),
]

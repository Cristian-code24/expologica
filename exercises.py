"""Expresiones, pasos y circuitos de los ejercicios del Tema 5."""

from typing import Callable

from boolean_logic import truth_table


EXERCISE_511A = lambda a, b, c: (a and not b) or ((not a) and (not c)) or b
EXERCISE_511A_SIMPLE = lambda a, b, c: a or b or (not c)
EXERCISE_511B = lambda a, b, c: (not (a or b)) or ((b or (not c)) and a)
EXERCISE_511B_SOP = lambda a, b, c: ((not a) and (not b)) or (a and b) or (a and (not c))
EXERCISE_512 = lambda a, b, c, d: (a and (b or (not c))) or ((not a) and d)
EXERCISE_513 = lambda a, b, c, d: (a or (not b) or c) and (b or (not c) or d)


EXERCISES = {
    "5.11a": {
        "variables": ("A", "B", "C"),
        "expression": r"F = A\cdot B' + A'\cdot C' + B",
        "steps": [
            ("Reordenamos", r"F = A\cdot B' + B + A'\cdot C'"),
            ("Combinación", r"A\cdot B' + B = A + B"),
            ("Absorción", r"A + A'\cdot C' = A + C'"),
            ("Resultado", r"F = A + B + C'"),
        ],
        "expression_fn": EXERCISE_511A,
    },
    "5.11b": {
        "variables": ("A", "B", "C"),
        "expression": r"F = (A+B)' + (B+C')\cdot A",
        "steps": [
            ("De Morgan", r"(A+B)' = A'\cdot B'"),
            ("Distribución", r"(B+C')\cdot A = A\cdot B + A\cdot C'"),
            ("Forma suma de productos", r"F = A'\cdot B' + A\cdot B + A\cdot C'"),
        ],
        "expression_fn": EXERCISE_511B,
    },
    "5.12": {
        "variables": ("A", "B", "C", "D"),
        "expression": r"F = A\cdot(B+C') + A'\cdot D",
        "expression_fn": EXERCISE_512,
        "steps": [
            ("Distribuimos", r"F = A\cdot B + A\cdot C' + A'\cdot D"),
            ("Complementos con NAND", r"C'=\operatorname{NAND}(C,C),\qquad A'=\operatorname{NAND}(A,A)"),
            (
                "Términos negados",
                r"X_1=\operatorname{NAND}(A,B),\quad X_2=\operatorname{NAND}(A,C'),\quad X_3=\operatorname{NAND}(A',D)",
            ),
            (
                "Salida",
                r"F=\operatorname{NAND}(X_1,X_2,X_3),\qquad 6\ \text{compuertas NAND}",
            ),
        ],
    },
    "5.13": {
        "variables": ("A", "B", "C", "D"),
        "expression": r"F = (A+B'+C)\cdot(B+C'+D)",
        "expression_fn": EXERCISE_513,
        "steps": [
            ("Complementos con NOR", r"B'=\operatorname{NOR}(B,B),\qquad C'=\operatorname{NOR}(C,C)"),
            (
                "Negamos cada suma",
                r"P'=\operatorname{NOR}(A,B',C),\qquad Q'=\operatorname{NOR}(B,C',D)",
            ),
            ("Salida", r"F=\operatorname{NOR}(P',Q'),\qquad 5\ \text{compuertas NOR}"),
        ],
    },
}


CIRCUITS = {
    "NOT": {
        "variables": ["A"],
        "expression": "A'",
        "gates": [{"id": "not", "kind": "NOT", "label": "NOT", "x": 520, "y": 260, "inputs": ["A"], "output": "n"}],
        "output": "n",
    },
    "AND": {
        "variables": ["A", "B"],
        "expression": "A·B",
        "gates": [{"id": "and", "kind": "AND", "label": "AND", "x": 520, "y": 260, "inputs": ["A", "B"], "output": "f"}],
        "output": "f",
    },
    "OR": {
        "variables": ["A", "B"],
        "expression": "A+B",
        "gates": [{"id": "or", "kind": "OR", "label": "OR", "x": 520, "y": 260, "inputs": ["A", "B"], "output": "f"}],
        "output": "f",
    },
    "NAND": {
        "variables": ["A", "B"],
        "expression": "(A·B)'",
        "gates": [{"id": "nand", "kind": "NAND", "label": "NAND", "x": 520, "y": 260, "inputs": ["A", "B"], "output": "f"}],
        "output": "f",
    },
    "NOR": {
        "variables": ["A", "B"],
        "expression": "(A+B)'",
        "gates": [{"id": "nor", "kind": "NOR", "label": "NOR", "x": 520, "y": 260, "inputs": ["A", "B"], "output": "f"}],
        "output": "f",
    },
    "XOR": {
        "variables": ["A", "B"],
        "expression": "A⊕B",
        "gates": [{"id": "xor", "kind": "XOR", "label": "XOR", "x": 520, "y": 260, "inputs": ["A", "B"], "output": "f"}],
        "output": "f",
    },
    "XNOR": {
        "variables": ["A", "B"],
        "expression": "(A⊕B)'",
        "gates": [{"id": "xnor", "kind": "XNOR", "label": "XNOR", "x": 520, "y": 260, "inputs": ["A", "B"], "output": "f"}],
        "output": "f",
    },
    "5.11a": {
        "variables": ["A", "B", "C"],
        "expression": "AB' + A'C' + B",
        "gates": [
            {"id": "nb", "kind": "NOT", "label": "NOT", "x": 225, "y": 250, "inputs": ["B"], "output": "nb"},
            {"id": "na", "kind": "NOT", "label": "NOT", "x": 225, "y": 330, "inputs": ["A"], "output": "na"},
            {"id": "nc", "kind": "NOT", "label": "NOT", "x": 225, "y": 410, "inputs": ["C"], "output": "nc"},
            {"id": "t1", "kind": "AND", "label": "AND", "x": 445, "y": 200, "inputs": ["A", "nb"], "output": "t1"},
            {"id": "t2", "kind": "AND", "label": "AND", "x": 445, "y": 360, "inputs": ["na", "nc"], "output": "t2"},
            {"id": "out", "kind": "OR", "label": "OR", "x": 720, "y": 280, "inputs": ["t1", "t2", "B"], "output": "f"},
        ],
        "output": "f",
    },
    "5.11a-simplified": {
        "variables": ["A", "B", "C"],
        "expression": "A + B + C'",
        "gates": [
            {"id": "nc", "kind": "NOT", "label": "NOT", "x": 260, "y": 390, "inputs": ["C"], "output": "nc"},
            {"id": "out", "kind": "OR", "label": "OR", "x": 640, "y": 270, "inputs": ["A", "B", "nc"], "output": "f"},
        ],
        "output": "f",
    },
    "5.11b": {
        "variables": ["A", "B", "C"],
        "expression": "(A+B)' + (B+C')A",
        "gates": [
            {"id": "nor1", "kind": "NOR", "label": "NOR", "x": 230, "y": 180, "inputs": ["A", "B"], "output": "n_ab"},
            {"id": "notc", "kind": "NOT", "label": "NOT", "x": 230, "y": 410, "inputs": ["C"], "output": "nc"},
            {"id": "or1", "kind": "OR", "label": "OR", "x": 460, "y": 330, "inputs": ["B", "nc"], "output": "b_nc"},
            {"id": "and1", "kind": "AND", "label": "AND", "x": 665, "y": 275, "inputs": ["A", "b_nc"], "output": "term"},
            {"id": "or2", "kind": "OR", "label": "OR", "x": 830, "y": 245, "inputs": ["n_ab", "term"], "output": "f"},
        ],
        "output": "f",
    },
    "5.12": {
        "variables": ["A", "B", "C", "D"],
        "expression": "A(B+C') + A'D",
        "gates": [
            {"id": "a_bar", "kind": "NAND", "label": "NAND", "x": 220, "y": 115, "inputs": ["A", "A"], "output": "na"},
            {"id": "c_bar", "kind": "NAND", "label": "NAND", "x": 220, "y": 320, "inputs": ["C", "C"], "output": "nc"},
            {"id": "ab_bar", "kind": "NAND", "label": "NAND", "x": 440, "y": 180, "inputs": ["A", "B"], "output": "nab"},
            {"id": "ac_bar", "kind": "NAND", "label": "NAND", "x": 440, "y": 275, "inputs": ["A", "nc"], "output": "nac"},
            {"id": "ad_bar", "kind": "NAND", "label": "NAND", "x": 440, "y": 370, "inputs": ["na", "D"], "output": "nad"},
            {"id": "out", "kind": "NAND", "label": "NAND ×3", "x": 715, "y": 275, "inputs": ["nab", "nac", "nad"], "output": "f"},
        ],
        "output": "f",
    },
    "5.13": {
        "variables": ["A", "B", "C", "D"],
        "expression": "(A+B'+C)(B+C'+D)",
        "gates": [
            {"id": "b_bar", "kind": "NOR", "label": "NOR", "x": 225, "y": 220, "inputs": ["B", "B"], "output": "nb"},
            {"id": "c_bar", "kind": "NOR", "label": "NOR", "x": 225, "y": 320, "inputs": ["C", "C"], "output": "nc"},
            {"id": "p_bar", "kind": "NOR", "label": "NOR ×3", "x": 490, "y": 205, "inputs": ["A", "nb", "C"], "output": "np"},
            {"id": "q_bar", "kind": "NOR", "label": "NOR ×3", "x": 490, "y": 355, "inputs": ["B", "nc", "D"], "output": "nq"},
            {"id": "out", "kind": "NOR", "label": "NOR", "x": 740, "y": 280, "inputs": ["np", "nq"], "output": "f"},
        ],
        "output": "f",
    },
}


def exercise_tables() -> dict[str, list[dict[str, int]]]:
    tables: dict[str, list[dict[str, int]]] = {}
    for key in ("5.11a", "5.11b", "5.12", "5.13"):
        exercise = EXERCISES[key]
        expression: Callable[..., int] = exercise["expression_fn"]
        tables[key] = truth_table(exercise["variables"], {"F": expression})
    return tables

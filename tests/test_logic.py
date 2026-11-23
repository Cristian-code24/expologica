import itertools
import unittest

from boolean_logic import evaluate_gates
from exercises import (
    CIRCUITS,
    EXERCISE_511A,
    EXERCISE_511A_SIMPLE,
    EXERCISE_511B,
    EXERCISE_511B_SOP,
    EXERCISE_512,
    EXERCISE_513,
)


class ExerciseCircuitTests(unittest.TestCase):
    def test_511a_original_and_simplified_are_equivalent(self):
        for a, b, c in itertools.product((0, 1), repeat=3):
            self.assertEqual(EXERCISE_511A(a, b, c), EXERCISE_511A_SIMPLE(a, b, c))
            inputs = dict(A=a, B=b, C=c)
            for key, expression in (("5.11a", EXERCISE_511A), ("5.11a-simplified", EXERCISE_511A_SIMPLE)):
                self.assertEqual(evaluate_gates(inputs, CIRCUITS[key]["gates"])[CIRCUITS[key]["output"]], expression(a, b, c))

    def test_511b_expansion_and_circuit_match(self):
        for a, b, c in itertools.product((0, 1), repeat=3):
            self.assertEqual(EXERCISE_511B(a, b, c), EXERCISE_511B_SOP(a, b, c))
            actual = evaluate_gates(dict(A=a, B=b, C=c), CIRCUITS["5.11b"]["gates"])["f"]
            self.assertEqual(actual, EXERCISE_511B(a, b, c))

    def test_universal_gate_exercises_match_and_have_expected_counts(self):
        self.assertEqual(len(CIRCUITS["5.12"]["gates"]), 6)
        self.assertEqual(len(CIRCUITS["5.13"]["gates"]), 5)
        for values in itertools.product((0, 1), repeat=4):
            inputs = dict(zip(("A", "B", "C", "D"), values))
            self.assertEqual(evaluate_gates(inputs, CIRCUITS["5.12"]["gates"])["f"], EXERCISE_512(*values))
            self.assertEqual(evaluate_gates(inputs, CIRCUITS["5.13"]["gates"])["f"], EXERCISE_513(*values))


if __name__ == "__main__":
    unittest.main()

from math import log

import pytest

from hurdle_solver.utils import entropy


@pytest.mark.parametrize("guess, solutions, expected", [
    ("abcde", ["abcde", "fghij"], -log(0.5)),
    ("abcde", ["axxxx", "abxxx", "abcxx", "abcdx"], 2 * -log(0.5)),
    ("aaaaa", ["abcde", "fghij", "klmno", "pqrst"], 0.25 * -log(0.25) + 0.75 * -log(0.75))
])
def test_entropy(guess, solutions, expected):
    assert entropy(guess, solutions) == expected


@pytest.mark.parametrize("better, worse, words", [
    ("axxxx", "xxxxx", ["abcde", "fghij", "klmno", "pqrst"]),
    ("axxxx", "xafkp", ["abcde", "fghij", "klmno", "pqrst"]),
    ("xafxx", "xafkx", ["abcde", "fghij", "klmno", "pqrst"])
])
def test_better_entropy(better, worse, words):
    assert entropy(better, words) > entropy(worse, words)

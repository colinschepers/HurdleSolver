import pytest

from hurdle_solver.evaluator import Evaluator


@pytest.mark.parametrize("guess, solution, num_green, num_yellow", [
    ("cones", "moose", 1, 2),
    ("bleep", "moose", 0, 1),
    ("bingo", "moose", 0, 1),
    ("mince", "moose", 2, 0),
    ("mouse", "moose", 4, 0),
    ("moose", "moose", 5, 0)
])
def test_evaluate(guess, solution, num_green, num_yellow):
    actual_num_green, actual_num_yellow = Evaluator().evaluate(guess, solution)
    assert actual_num_green == num_green, "number of greens do not match"
    assert actual_num_yellow == num_yellow, "number of yellows do not match"

from pytest import fixture

from hurdle_solver.solver import Solver
from hurdle_solver.utils import evaluate


@fixture
def vocab() -> set[str]:
    return {"chose", "crane", "cones", "close", "comes",
         "coles", "bones", "cores", "cheer", "trail"}


@fixture
def solution() -> str:
    return "cones"


@fixture
def solver(vocab: set[str]) -> Solver:
    return Solver(vocab)


def test_get_suggestions(solver: Solver, vocab: set[str], solution: str):
    suggestions = solver.get_suggestions()
    assert len(suggestions) == len(vocab)
    assert solution in suggestions


def test_add_information(solver: Solver, vocab: set[str], solution: str):
    guess = "slice"
    num_green, num_yellow = evaluate(guess, solution)
    solver.add_information(guess, num_green, num_yellow)
    assert len(solver.possible_words) < len(vocab)
    assert solution in solver.possible_words


def test_solver(solver: Solver, vocab: set[str], solution: str):
    suggestions = solver.get_suggestions()
    while len(suggestions) > 1:
        guess = suggestions[0]
        num_green, num_yellow = evaluate(guess, solution)
        solver.add_information(guess, num_green, num_yellow)
        suggestions = solver.get_suggestions()
    assert len(suggestions) == 1
    assert suggestions[0] == solution


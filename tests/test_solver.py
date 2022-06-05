from hurdle_solver.solver import Solver
from hurdle_solver.utils import evaluate

words = ["chose", "crane", "cones", "close", "comes",
         "coles", "bones", "cores", "cheer", "trail"]
solution = "cones"


def test_get_suggestions():
    solver = Solver(set(words))
    suggestions = solver.get_suggestions()
    assert len(suggestions) == len(words)
    assert solution in suggestions


def test_add_information():
    solver = Solver(set(words))
    guess = "slice"
    num_green, num_yellow = evaluate(guess, solution)
    solver.add_information(guess, num_green, num_yellow)
    assert len(solver.possible_words) < len(words)
    assert solution in solver.possible_words


def test_solver():
    solver = Solver(set(words))
    suggestions = solver.get_suggestions()
    while len(suggestions) > 1:
        guess = suggestions[0]
        num_green, num_yellow = evaluate(guess, solution)
        solver.add_information(guess, num_green, num_yellow)
        suggestions = solver.get_suggestions()
    assert len(suggestions) == 1
    assert suggestions[0] == solution


from hurdle_solver.evaluator import Evaluator
from hurdle_solver.solver import Solver

words = ["chose", "crane", "cones", "close", "comes",
         "coles", "bones", "cores", "cheer", "trail"]
solution = "cones"
evaluator = Evaluator()


def test_get_suggestions():
    solver = Solver(set(words), evaluator)
    suggestions = solver.get_suggestions()
    assert len(suggestions) == len(words)
    assert solution in suggestions


def test_add_information():
    solver = Solver(set(words), evaluator)
    guess = "slice"
    num_green, num_yellow = evaluator.evaluate(guess, solution)
    solver.add_information(guess, num_green, num_yellow)
    assert len(solver.possible_words) < len(words)
    assert solution in solver.possible_words


def test_solver():
    solver = Solver(set(words), evaluator)
    suggestions = solver.get_suggestions()
    while len(suggestions) > 1:
        guess = suggestions[0]
        num_green, num_yellow = evaluator.evaluate(guess, solution)
        solver.add_information(guess, num_green, num_yellow)
        suggestions = solver.get_suggestions()
    assert len(suggestions) == 1
    assert suggestions[0] == solution


from random import Random

from pytest import fixture

from hurdle_solver.solver import Solver
from hurdle_solver.utils import evaluate, get_all_words


@fixture
def vocab() -> set[str]:
    return set(get_all_words())


@fixture()
def num_games() -> int:
    return 25


@fixture()
def random() -> Random:
    return Random(123456)


def _play_game(vocab: set[str], solution: str) -> int:
    solver = Solver(vocab)

    num_green = 0
    num_guesses = 0
    while num_green < 5:
        suggestions = solver.get_suggestions()
        guess = suggestions[0]
        num_green, num_yellow = evaluate(guess, solution)
        solver.add_information(guess, num_green, num_yellow)
        num_guesses += 1

    return num_guesses


def test_accuracy(vocab: set[str], num_games: int, random: Random):
    _MAX_NUM_GUESSES_PER_GAME = 8
    _MAX_MEAN_NUM_GUESSES = 6

    total_guesses = 0
    for sample_word in random.sample(sorted(vocab), num_games):
        num_guesses = _play_game(vocab, sample_word)
        total_guesses += num_guesses
        assert num_guesses <= _MAX_NUM_GUESSES_PER_GAME, f"Failed game with solution '{sample_word}'"

    print(f"Mean: {total_guesses / num_games}")
    assert total_guesses / num_games <= _MAX_MEAN_NUM_GUESSES

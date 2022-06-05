import argparse
import sys
from typing import List

from hurdle_solver.evaluator import Evaluator
from hurdle_solver.solver import Solver
from hurdle_solver.utils import get_all_words

CACHE_PATH = "evaluator.cache"
SUGGESTION_LIMIT = 50


def main(guesses: List[str], num_greens: List[int], num_yellows: List[int]):
    vocab = set(get_all_words())
    evaluator = Evaluator.load(CACHE_PATH)
    solver = Solver(vocab, evaluator)

    for guess, num_green, num_yellow in zip(guesses, num_greens, num_yellows):
        solver.add_information(guess, num_green, num_yellow)

    suggestions = solver.get_suggestions()[:SUGGESTION_LIMIT]
    print(f"Suggestions: {suggestions}")

    while len(suggestions) > 0:
        try:
            print(f"Input guess: ")
            guess = ask_word()
            print(f"Input number of green: ")
            num_green = ask_digit()
            print(f"Input number of yellow: ")
            num_yellow = ask_digit()
        except ValueError as e:
            print(e, file=sys.stderr)
            continue

        solver.add_information(guess, num_green, num_yellow)
        suggestions = solver.get_suggestions()[:SUGGESTION_LIMIT]
        print(f"Suggestions: {suggestions}")


def ask_word():
    word = input().strip()
    if len(word) == 5:
        return word
    raise ValueError("Word length should be 5")


def ask_digit():
    digit = input().strip()
    if digit.isdigit():
        digit = int(digit)
        if 0 <= digit <= 5:
            return digit
        raise ValueError("Value not between 0 and 5")
    raise ValueError("Input is not a digit")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('information', nargs='*', default=[],
                        help='the known information in triplets (guess, num_green, num_yellow)')
    args = parser.parse_args()

    if len(args.information) % 3 != 0:
        raise ValueError("the information is not provided in triplets")

    guesses = args.information[::3]
    num_greens = list(map(int, args.information[1::3]))
    num_yellows = list(map(int, args.information[2::3]))
    main(guesses, num_greens, num_yellows)

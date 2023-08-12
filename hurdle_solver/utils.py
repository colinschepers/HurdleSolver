from collections import defaultdict
from functools import lru_cache
from math import log
from typing import List, Tuple
from urllib import request


@lru_cache(maxsize=10000000)
def evaluate(guess: str, solution: str) -> Tuple[int, int]:
    """
    Evaluates a guess with the known solution.
    :param guess: the guessed word
    :param solution: the solution
    :return: tuple of the number of green and the number of yellow characters
    """
    num_green = 0
    num_yellow = 0

    n = len(guess)
    used = [False] * n

    for i in range(n):
        if guess[i] == solution[i]:
            num_green += 1
            continue
        for j in range(n):
            if guess[i] == solution[j] and guess[j] != solution[j] and not used[j]:
                num_yellow += 1
                used[j] = True
                break

    return num_green, num_yellow


def entropy(guess: str, solutions: List[str]) -> float:
    """
    Calculates the entropy of a guess given a list of possible solutions.
    :param guess: the guessed word
    :param solutions: a list of remaining words, i.e. possible solutions of a game
    :return: the entropy, a measure of how random something is
    """
    counts = defaultdict(int)
    for solution in solutions:
        key = evaluate(guess, solution)
        counts[key] += 1

    result = 0
    for count in counts.values():
        p = count / len(solutions)
        result += -p * log(p)

    return result


def get_top_words() -> List[str]:
    """
    Get a predefined list of good words to start with.
    :return: a list of good words
    """
    with open("top_words.txt", "r") as f:
        return f.read().splitlines()


def get_all_words() -> List[str]:
    """
    Get a predefined list of five-letter words.
    :return: a list of five-letter words
    """
    url = "https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt"
    text = request.urlopen(url).read()
    return [line.decode() for line in text.splitlines() if len(line) == 5]

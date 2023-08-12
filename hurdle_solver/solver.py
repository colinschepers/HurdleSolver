from random import Random
from typing import Set, List, Tuple, Iterable

from hurdle_solver.utils import entropy, evaluate, get_top_words


class Solver:
    MAX_CALCULATIONS = 1000000

    def __init__(self, vocab: Set[str]):
        self.round_nr = 1
        self.vocab = set(vocab)
        self.possible_words = list(vocab)
        Random(123456).shuffle(self.possible_words)

    def add_information(self, guess: str, num_green: int, num_yellow: int):
        """
        Add information to the state of the game.
        :param guess: the guessed word
        :param num_green: the number of green characters of the guess
        :param num_yellow: the number of yellow characters of the guess
        """
        self.possible_words = list(filter(
            lambda w: (num_green, num_yellow) == evaluate(guess, w),
            self.possible_words
        ))
        self.round_nr += 1

    def get_suggestions(self) -> List[str]:
        """
        Get a list of suggestions, given the current state of the game.
        :return: an ordered list of suggestions, with the best word first
        """
        return [word for word, _ in self.get_scored_suggestions()]

    def get_scored_suggestions(self) -> List[Tuple[str, float]]:
        """
        Get a list of scored suggestions, given the current state of the game.
        :return: an ordered list of suggestions and its score, the best word first
        """
        scored_suggestions = ((score, word) for word, score in self._stream_scored_suggestions())
        return [(word, score) for score, word in sorted(scored_suggestions, reverse=True)]

    def _stream_scored_suggestions(self) -> Iterable[Tuple[str, float]]:
        """
        Get a list of scored suggestions, given the current state of the game.
        :return: an unordered iterable of suggestions and its score
        """
        if not self.possible_words:
            return

        possible_word_sample = get_top_words() if self.round_nr == 1 else self.possible_words
        sample_size = int(self.MAX_CALCULATIONS / len(self.possible_words))
        possible_solutions_sample = self.possible_words[:sample_size]

        for word in possible_word_sample:
            yield word, entropy(word, possible_solutions_sample)

    @staticmethod
    def _get_word_dist(guess: str, num_green: int, num_yellow: int, word: str):
        ng, ny = evaluate(guess, word)
        return 2 * abs(num_green - ng) + abs(num_yellow - ny)

from itertools import islice
from typing import Set, List, Tuple, Iterable

from hurdle_solver.utils import entropy, evaluate, get_top_words


class Solver:
    MAX_POSSIBLE_WORDS: int = 1000
    LIMIT_POSSIBLE_WORDS: int = 100
    TOP_WORDS: Set[str] = set(get_top_words())

    def __init__(self, vocab: Set[str]):
        self.vocab = set(vocab)
        self.word_distances = [(word, 0) for word in sorted(vocab, key=lambda w: (w not in self.TOP_WORDS, w))]
        self.possible_words = list(vocab)

    def add_information(self, guess: str, num_green: int, num_yellow: int):
        """
        Add information to the state of the game.
        :param guess: the guessed word
        :param num_green: the number of green characters of the guess
        :param num_yellow: the number of yellow characters of the guess
        """
        self.word_distances = sorted((
            (word, distance + self._get_word_dist(guess, num_green, num_yellow, word))
            for word, distance in self.word_distances
        ), key=lambda x: (x[1], x[0] not in self.TOP_WORDS))
        self.possible_words = list(filter(
            lambda w: (num_green, num_yellow) == evaluate(guess, w),
            self.possible_words
        ))

    def get_suggestions(self, limit: int = 100) -> List[str]:
        """
        Get a list of suggestions, given the current state of the game.
        :param limit: maximum number of items to return
        :return: an ordered list of suggestions, with the best word first
        """
        return [word for word, _ in self.get_scored_suggestions(limit)]

    def get_scored_suggestions(self, limit: int = 100) -> Iterable[Tuple[str, float]]:
        """
        Get a list of scored suggestions, given the current state of the game.
        :param limit: maximum number of items to return
        :return: an ordered list of suggestions and its score, the best word first
        """
        scored_suggestions = [(score, word) for word, score in islice(self.stream_scored_suggestions(), limit)]
        return [(word, score) for score, word in sorted(scored_suggestions, reverse=True)]

    def stream_scored_suggestions(self) -> Iterable[Tuple[str, float]]:
        """
        Get a list of scored suggestions, given the current state of the game.
        :return: an unordered iterable of suggestions and its score
        """
        if len(self.possible_words) <= 2:
            words = self.possible_words
        else:
            words = [w for w, _ in self.word_distances]

        for word in words:
            yield word, entropy(word, self.possible_words)

    @staticmethod
    def _get_word_dist(guess: str, num_green: int, num_yellow: int, word: str):
        ng, ny = evaluate(guess, word)
        return 2 * abs(num_green - ng) + abs(num_yellow - ny)

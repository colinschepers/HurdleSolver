from typing import Set, List

from hurdle_solver.utils import entropy, evaluate, get_top_words


class Solver:
    MAX_POSSIBLE_WORDS: int = 1000
    MAX_SUGGESTIONS: int = 100
    TOP_WORDS: List[str] = get_top_words()

    def __init__(self, vocab: Set[str]):
        self.vocab = set(vocab)
        self.word_distances = [(0, word) for word in vocab]
        self.possible_words = list(vocab)

    def add_information(self, guess: str, num_green: int, num_yellow: int):
        """
        Add information to the state of the game.
        :param guess: the guessed word
        :param num_green: the number of green characters of the guess
        :param num_yellow: the number of yellow characters of the guess
        """
        self.word_distances = sorted(
            (dist + self._get_word_dist(guess, num_green, num_yellow, word), word)
            for dist, word in self.word_distances
        )
        self.possible_words = list(filter(
            lambda w: (num_green, num_yellow) == evaluate(guess, w),
            self.possible_words
        ))

    def get_suggestions(self) -> List[str]:
        """
        Get a list of suggestions, given the current state of the game.
        :return: a list of ordered suggestions, with the best word first
        """
        if len(self.possible_words) > self.MAX_POSSIBLE_WORDS:
            lookup = set(self.possible_words)
            words = [word for word in self.TOP_WORDS if word in lookup]
        elif len(self.possible_words) > 2:
            words = list(word for _, word in self.word_distances)[:self.MAX_SUGGESTIONS]
        else:
            words = self.possible_words

        scored_words = [(entropy(w, self.possible_words), w) for w in words]
        return [word for _, word in sorted(scored_words, reverse=True)]

    @staticmethod
    def _get_word_dist(guess: str, num_green: int, num_yellow: int, word: str):
        ng, ny = evaluate(guess, word)
        return 2 * abs(num_green - ng) + abs(num_yellow - ny)

import struct
from typing import Tuple, Dict


class Evaluator:
    PATH = "evaluator.cache"

    def __init__(self):
        self.word_to_idx: Dict[str, int] = {}
        self.cache: Dict[Tuple[int, int], Tuple[int, int]] = {}

    def evaluate(self, guess: str, solution: str) -> Tuple[int, int]:
        if guess not in self.word_to_idx:
            self.word_to_idx[guess] = len(self.word_to_idx)
        if solution not in self.word_to_idx:
            self.word_to_idx[solution] = len(self.word_to_idx)
        key = (self.word_to_idx[guess], self.word_to_idx[solution])
        if key not in self.cache:
            self.cache[key] = self._evaluate(guess, solution)
        return self.cache[key]

    @staticmethod
    def _evaluate(guess: str, solution: str) -> Tuple[int, int]:
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

    @staticmethod
    def load(path: str) -> "Evaluator":
        evaluator = Evaluator()
        with open(path, "rb") as f:
            num_words = struct.unpack('>H', f.read(2))[0]
            for i in range(num_words):
                word = struct.unpack('>5s', f.read(5))[0]
                evaluator.word_to_idx[word.decode()] = i
            cache_size = struct.unpack('>I', f.read(4))[0]
            for i in range(cache_size):
                idx1 = struct.unpack('>H', f.read(2))[0]
                idx2 = struct.unpack('>H', f.read(2))[0]
                num_green = struct.unpack('>H', f.read(2))[0]
                num_yellow = struct.unpack('>H', f.read(2))[0]
                evaluator.cache[(idx1, idx2)] = (num_green, num_yellow)
        return evaluator

    def save(self, path: str):
        with open(path, "wb") as f:
            f.write(struct.pack('>H', len(self.word_to_idx)))
            words = sorted((w for w in self.word_to_idx), key=lambda w: self.word_to_idx[w])
            for word in words:
                f.write(struct.pack('>5s', word.encode()))
            f.write(struct.pack('>I', len(self.cache)))
            for (idx1, idx2), (num_green, num_yellow) in self.cache.items():
                f.write(struct.pack('>H', idx1))
                f.write(struct.pack('>H', idx2))
                f.write(struct.pack('>H', num_green))
                f.write(struct.pack('>H', num_yellow))

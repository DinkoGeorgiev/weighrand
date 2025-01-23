import random
from typing import List


class RandomGen:
    """Random number generator with probabilities."""

    def __init__(self, random_nums: List[int] = None, probabilities: [List[float]] = None):
        """Inits RandomGen

        :param random_nums: A list of random numbers to pick from when generating.
        :param probabilities: A list of selection probabilities for the specified numbers
        """
        # The type of random_nums values is not validated as it is irrelevant for the implementation.
        if len(random_nums) == 0 or len(probabilities) != len(random_nums):
            raise ValueError("random_nums and probabilities must have the same non-zero length")
        if min(probabilities) <= 0 or max(probabilities) > 1:
            raise ValueError("probabilities must have values between 0 and 1")
        if len(random_nums) != len(set(random_nums)):
            raise ValueError("random_nums must have unique values")
        # The type of random_nums values is not validated as it is irrelevant for the implementation.

        # Values that may be returned by next_num()
        self._random_nums = random_nums
        # Probability of the occurrence of random_nums
        self._probabilities = probabilities
        self._total_probabilities = sum(probabilities)

    def __iter__(self):
        return self

    def __next__(self) -> int:
        return self.next_num()

    def next_num(self) -> int:
        """
        Returns one of the items in self._random_nums. When this method is called multiple
        times over a long period, it should return the numbers roughly with
        the initialized probabilities.
        """
        return self._get_num_for_threshold(random.random() * self._total_probabilities)

    def _get_num_for_threshold(self, threshold: float) -> int:
        position = 0
        for i, probability in enumerate(self._probabilities):
            position += probability
            if position > threshold:
                return self._random_nums[i]
        return self._random_nums[-1]

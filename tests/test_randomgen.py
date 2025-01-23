"""randomgen module unit tests"""

from collections import Counter
from random import random

import pytest
from flaky import flaky

from weighrand.randomgen import RandomGen

# pylint: disable=missing-function-docstring


def test_init_arguments_length_mismatch():
    with pytest.raises(ValueError, match="length"):
        RandomGen(random_nums=[1], probabilities=[0.5, 0.5])


def test_init_arguments_length_zero():
    with pytest.raises(ValueError, match="length"):
        RandomGen(random_nums=[], probabilities=[])


def test_init_probability_too_large():
    with pytest.raises(ValueError, match="values between"):
        RandomGen(random_nums=[1], probabilities=[1.1])


def test_init_probability_too_small():
    with pytest.raises(ValueError, match="values between"):
        RandomGen(random_nums=[1], probabilities=[0])


def test_init_duplicate_nums():
    with pytest.raises(ValueError, match="unique values"):
        RandomGen(random_nums=[1, 1], probabilities=[0.5, 0.3])


def test_get_num_for_threshold():
    """Test item selection based on specified threshold."""
    random_gen = RandomGen(random_nums=[1, 2, 3, 4], probabilities=[0.1, 0.2, 0.3, 0.35])
    # pylint: disable=protected-access
    assert random_gen._get_num_for_threshold(-1) == 1
    assert random_gen._get_num_for_threshold(0) == 1
    assert random_gen._get_num_for_threshold(0.09) == 1
    assert random_gen._get_num_for_threshold(0.1) == 2
    assert random_gen._get_num_for_threshold(0.25) == 2
    assert random_gen._get_num_for_threshold(0.35) == 3
    assert random_gen._get_num_for_threshold(0.94) == 4
    assert random_gen._get_num_for_threshold(1) == 4
    assert random_gen._get_num_for_threshold(99) == 4


def test_randomgen_iterator():
    random_nums = [1, 2, 3, 4]
    random_gen = RandomGen(random_nums=random_nums, probabilities=[0.1, 0.2, 0.3, 0.35])
    for random_num in iter(random_gen):
        assert random_num in random_nums
        break


@flaky(max_runs=5, min_passes=3, rerun_filter=lambda err, *args: not issubclass(err[0], ValueError))
@pytest.mark.parametrize(
    "n_iterations,deviation_tolerance_soft,deviation_tolerance_hard,probabilities",
    [
        # 100% chance, 1 item
        (1000, 0, 0, [0.0001]),
        # Increasing probabilities
        (1_000_000, 0.001, 0.005, [0.1, 0.2, 0.3, 0.4]),
        # Decreasing probabilities
        (1_000_000, 0.001, 0.005, [0.4, 0.3, 0.2, 0.1]),
        # Duplicate probabilities
        (1_000_000, 0.001, 0.005, [0.2, 0.3, 0.3, 0.2]),
        # Large probability difference
        (1_000_000, 0.001, 0.005, [0.9, 0.001]),
        # 1000 close probabilities - sorted
        (100_000, 0.001, 0.005, [i / 1000 for i in range(1, 1001)]),
        # 1000 close probabilities - shuffled
        (100_000, 0.001, 0.005, sorted([i / 1000 for i in range(1, 1001)], key=lambda x: random())),
    ],
)
def test_get_next_num_distribution(n_iterations, deviation_tolerance_soft, deviation_tolerance_hard, probabilities):
    """Test the random numbers distribution deviation from the probabilities is within specified tolerances.

    :param n_iterations: Number of random numbers to generate
    :param deviation_tolerance_soft: If exceeded, the test will be retried based on flaky settings above
    :param deviation_tolerance_hard: If exceeded, the test is considered as failed without retries
    :param probabilities: List of probabilities to use for the test.
    """
    # For this test the actual items are not important, so we just populate them automatically.
    random_nums = list(range(len(probabilities)))
    random_gen = RandomGen(random_nums=random_nums, probabilities=probabilities)
    counter = Counter((random_gen.next_num() for _ in range(n_iterations)))
    probabilities_total = sum(probabilities)
    for i, num in enumerate(random_nums):
        num = random_nums[i]
        concentration = counter.get(num, 0) / n_iterations
        probability = probabilities[i]
        normalized_probability = probability / probabilities_total
        deviation = abs(concentration - normalized_probability)
        assert deviation <= deviation_tolerance_soft, (
            f"{probability=}, {normalized_probability=}, "
            f"{concentration=}, {deviation=}, {deviation_tolerance_soft=}"
        )
        if deviation > deviation_tolerance_hard:
            raise ValueError(
                f"Deviation too high! "
                f"{probability=}, {normalized_probability=}, {concentration=}, "
                f"{deviation=}, {deviation_tolerance_hard=}"
            )

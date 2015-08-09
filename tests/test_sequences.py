from misc.sequences import ArithmeticSequence

import pytest
from hypothesis import given, assume
from hypothesis import strategies as st


def arithmetic_sequences():
    return st.builds(ArithmeticSequence, st.integers(), st.integers())


@given(st.integers(), st.integers())
def test_arithmetic_sequence_first_element(first, difference):
    assert ArithmeticSequence(first, difference)[0] == first


@given(arithmetic_sequences(), st.integers(min_value=0))
def test_arithmetic_sequence_difference(sequence, index):
    assert sequence[index+1] - sequence[index] == sequence.difference


@given(arithmetic_sequences(), st.integers())
def test_arithmetic_sequence_equality(sequence, n):
    from itertools import islice

    assume(n != 0)

    assert sequence == ArithmeticSequence(sequence[0], sequence.difference)
    assert list(islice(sequence, 1000)) == list(islice(
            ArithmeticSequence(sequence[0], sequence.difference), 1000))
    assert sequence != ArithmeticSequence(sequence[0] + n, sequence.difference)
    assert sequence != ArithmeticSequence(sequence[0], sequence.difference + n)


@given(st.integers(), st.integers())
def test_arithmetic_sequence_iteration(first, difference):
    s = ArithmeticSequence(first, difference)

    it = iter(s)
    previous = next(it)

    for i in range(50):
        current = next(it)
        assert current - previous == difference, i
        previous = current


@given(arithmetic_sequences())
def test_arithmetic_sequence_trivial_slicing(s):
    assert s == s[:]
    assert s == s[0:]
    assert s == s[0::1]
    assert s == s[::1]


@given(arithmetic_sequences(),
       st.integers(min_value=0),
       st.integers(min_value=1))
def test_arithmetic_sequence_positive_step_slicing(sequence, start, step):
    from itertools import islice

    assert list(islice(sequence[start::step], 10)) == list(
            islice(islice(sequence, start, None, step), 10))

from misc.sequences import ArithmeticSequence

from itertools import islice
try:
    from itertools import imap as map
except ImportError:
    # assume python 3
    pass

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
    assert list(islice(sequence, 1000)) == \
        list(islice(ArithmeticSequence(sequence[0],
                                       sequence.difference),
                    1000))
    assert sequence != ArithmeticSequence(sequence[0] + n, sequence.difference)
    assert sequence != ArithmeticSequence(sequence[0], sequence.difference + n)


@given(arithmetic_sequences())
def test_arithmetic_sequence_iteration(sequence):
    n_elems = 50
    assert list(map(lambda i: sequence[i], range(n_elems))) == \
        list(islice(sequence, n_elems))


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

    assert list(islice(sequence[start::step], 10)) == \
        list(islice(islice(sequence, start, None, step), 10))

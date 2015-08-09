try:
    import itertools.imap as map
except ImportError:
    # assume python3
    pass


class ArithmeticSequence(object):
    __slots__ = ['_impl']

    def __init__(self, first, difference):
        self._impl = (first, difference)

    def __getitem__(self, key):
        if isinstance(key, slice):
            start = key.start or 0
            step = key.step or 1

            if key.stop is None:
                return ArithmeticSequence(self[start], step * self.difference)
            else:
                return map(lambda i: self[i],
                           xrange(*key.indices(key.stop - start)))

        return self._impl[0] + key * self.difference

    @property
    def difference(self):
        return self._impl[1]


    def __iter__(self):
        current = self[0]

        while True:
            yield current
            current += self.difference

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._impl == other._impl

    def __hash__(self):
        return hash(self._impl)

    def __repr__(self):
        return "{}{}".format(
                self.__class__.__name__,
                (self[0], self.difference))

    def __str__(self):
        return "[{}, {}, ...]".format(*self[:2])

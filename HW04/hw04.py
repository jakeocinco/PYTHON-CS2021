#Homework 04 - CS2021

def every_other(s):
    """Mutates a linked list so that all the odd-indiced elements are removed
    (using 0-based indexing).

    >>> s = Link(1, Link(2, Link(3, Link(4))))
    >>> every_other(s)
    >>> s
    Link(1, Link(3))
    >>> odd_length = Link(5, Link(3, Link(1)))
    >>> every_other(odd_length)
    >>> odd_length
    Link(5, Link(1))
    >>> singleton = Link(4)
    >>> every_other(singleton)
    >>> singleton
    Link(4)
    """
    "*** YOUR CODE HERE ***"
    def break_up(s,i):
        if s.rest is not ():
            if i % 2 == 0:
                return Link(s.first,break_up(s.rest, i + 1))
            else:
                return break_up(s.rest, i + 1)
        else:
            return Link(s.first)

    return break_up(s,0)

def has_cycle(s):
    """Return whether Link s contains a cycle.

    >>> s = Link(1, Link(2, Link(3)))
    >>> s.rest.rest.rest = s
    >>> has_cycle(s)
    True
    >>> t = Link(1, Link(2, Link(3)))
    >>> has_cycle(t)
    False
    """
    "*** YOUR CODE HERE ***"
    i = 1
    tortise = s.rest
    hair = s.rest.rest

    while True:
        if tortise is hair:
            return True

        if hair.rest is not ():
            if hair.rest.rest is not():
                hair = hair.rest.rest
            else:
                return False
        else:
            return False

        if tortise.rest is not ():
            tortise = tortise.rest
        else:
            return False

def has_cycle_constant(s):
    """Return whether Link s contains a cycle.

    >>> s = Link(1, Link(2, Link(3)))
    >>> s.rest.rest.rest = s
    >>> has_cycle_constant(s)
    True
    >>> t = Link(1, Link(2, Link(3)))
    >>> has_cycle_constant(t)
    False
    """
    "*** YOUR CODE HERE ***"
    setOfObjects = set()
    t = True;
    i = 0

    while t:
        setOfObjects.add(s.first)
        i += 1

        if i != len(setOfObjects):
            return True
        if s.rest is ():
            return False
        s = s.rest




##############################
# Linked List implementation #
##############################

class Link:

    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __len__(self):
        return 1 + len(self.rest)

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_str = ', ' + repr(self.rest)
        else:
            rest_str = ''
        return 'Link({0}{1})'.format(repr(self.first), rest_str)

    def __contains__(self, value):
        setOfObjects = set()
        s = self
        i = 0

        while True:
            if s.first is value:
                return True

            setOfObjects.add(s.first)
            i += 1

            if i != len(setOfObjects):
                return False
            if s.rest is ():
                return False
            s = s.rest


    def __iadd__(self, other):
        def copyLink(o):
            if o.rest is ():
                return Link(o.first)
            else:
                return Link(o.first, copyLink(o.rest))

        q = copyLink(other)

        s = self
        while True:
            if s.rest is ():
                s.rest = q
                return self
            else:
                s = s.rest






class ScaleIterator:
    """An iterator the scales elements of the iterable s by a number k.

    >>> s = ScaleIterator([1, 5, 2], 5)
    >>> list(s)
    [5, 25, 10]

    >>> m = ScaleIterator(naturals(), 2)
    >>> [next(m) for _ in range(5)]
    [2, 4, 6, 8, 10]
    """
    def __init__(self, s, k):
        self.s = s
        self.k = k
        self.i = -1



    def __iter__(self):
        return self

    def __next__(self):
        self.i += 1
        try:
            return self.s[self.i] * self.k
        except:
            try:
                return next(self.s) * self.k
            except:
                raise StopIteration


def scale(s, k):
    """Yield elements of the iterable s scaled by a number k.

    >>> s = scale([1, 5, 2], 5)
    >>> type(s)
    <class 'generator'>
    >>> list(s)
    [5, 25, 10]

    >>> m = scale(naturals(), 2)
    >>> [next(m) for _ in range(5)]
    [2, 4, 6, 8, 10]
    """
    "*** YOUR CODE HERE ***"
    for i in s:
        yield (i) * k

def merge(s0, s1):
    """Yield the elements of strictly increasing iterables s0 and s1, removing
    repeats. Assume that s0 and s1 have no repeats. You can also assume that s0
    and s1 represent infinite sequences.

    >>> twos = scale(naturals(), 2)
    >>> threes = scale(naturals(), 3)
    >>> m = merge(twos, threes)
    >>> type(m)
    <class 'generator'>
    >>> [next(m) for _ in range(10)]
    [2, 3, 4, 6, 8, 9, 10, 12, 14, 15]
    """
    i0, i1 = iter(s0), iter(s1)
    e0, e1 = next(i0), next(i1)
    "*** YOUR CODE HERE ***"
    while True:
        if e0 < e1:
            yield e0
            e0 = next(i0)
        elif e0 > e1:
            yield e1
            e1 = next(i1)
        else:
            yield e1
            e0 = next(i0)
            e1 = next(i1)


def make_s():
    """A generator function that yields all positive integers with only factors
    2, 3, and 5.

    >>> s = make_s()
    >>> type(s)
    <class 'generator'>
    >>> [next(s) for _ in range(20)]
    [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30, 32, 36]
    """
    "*** YOUR CODE HERE ***"

    while True:
        yield 1
        s2 = scale(make_s(),2);
        s3 = scale(make_s(),3);
        s5 = scale(make_s(),5);

        m = merge(s2,merge(s3,s5))
        while True:
            yield next(m)

def naturals():
    """A generator function that yields the infinite sequence of natural
    numbers, starting at 1.

    >>> m = naturals()
    >>> type(m)
    <class 'generator'>
    >>> [next(m) for _ in range(10)]
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    i = 1
    while True:
        yield i
        i += 1

twos = scale(naturals(), 2)
threes = scale(naturals(), 3)
m = merge(twos, threes)
print(type(m))
# <class 'generator'>
# [next(m) for _ in range(10)]
# [2, 3, 4, 6, 8, 9, 10, 12, 14, 15]
# def _test():
#     import doctest
#     doctest.testmod()
#
# if __name__ == "__main__":
#     _test()

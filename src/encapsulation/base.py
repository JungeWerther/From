from typing import Callable, TypeVar, Generic

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


class From(Generic[T]):
    """Base class"""

    def __init__(self, val: T):
        self.val = val

    def __eq__(self, other):
        return self.val == other.val

    def __repr__(self):
        return f"<{self.__class__.__name__} val=({self.val})>"

    def __bool__(self):
        return True if self.val else False

    def __call__(self, func):
        return self.effect(func)

    def __mul__(self, other):
        return self.bind(lambda a: a * other)

    def __add__(self, other):
        return self.bind(lambda a: a + other)

    def __div__(self, other):
        return self.bind(lambda a: a / other) if other != 0 else Nothing()

    def effect(self, func):
        """Return self while applying `func` to self.val"""
        func(self.val)
        return self

    @classmethod
    def unit(cls, val):
        """Return a new instance of the same encapsulating class, wrapping `val`"""
        return cls(val)

    def bind(self, func):
        """Return a new wrapped instance with `func` applied to self.val"""
        return self.unit(func(self.val))


class Nothing(From[T]):
    def __init__(self, val: None = None):
        self.val = None


class Just(From[T]):
    def __init__(self, val: T):
        assert val is not None
        self.val = val


class Maybe(From[T]):
    def __init__(self, val):
        self.val = val

    def bind(self, func):
        if self.val:
            return Just(func(self.val))
        return Nothing()


M = TypeVar("M", bound=From)


def to(cls: type[From[T]]):
    def outer(func: Callable[[U], T]) -> Callable[[U], From[T]]:
        return lambda *args, **kwargs: cls(*args, **kwargs).bind(func)

    return outer


def compose(f: From[T], g: Callable[[T], From[U]] = Nothing(), *hs) -> From[U]:
    return compose(g(f.val), *hs) if g else f


if __name__ == "__main__":
    m = Maybe(2)
    assert m.bind(lambda x: 3 * x) == Maybe(6)
    assert m
    assert not Maybe(None).bind(lambda x: 3 * x)
    assert Maybe(None) == Nothing()

    f = From(2)
    (f * 3 + 2).effect(print)

    @to(From[str])
    def test(s: str):
        return f"[{s}]"

    assert test("hi").effect(print) == Just("[hi]")
    a = "b"
    assert test("a").bind(eval) == Just(["b"])
    assert test("a") != Nothing()

    @to(From)
    def id(val):
        return val

    def add1(val: int):
        return val + 1

    @to(Just[int])
    def just_add1(val: int):
        return add1(val)

    just_add1(1).effect(print)
    assert id(1).bind(add1) == Just(2)
    assert compose(id(1), just_add1, test, test) == Just("[[2]]")

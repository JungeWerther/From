from base import Maybe, Just, Nothing, From, to, Result, Success, Error, Generic
from typing import Callable, Iterable, TypeVar, TypeVarTuple

T = TypeVar("T", bound="Array")
U = TypeVar("U")
V = TypeVar("V")


class Head(Just[T]):
    pass


class Nil(Nothing):
    pass


class Array(tuple[*From[T]]):
    # def __new__(cls, *args: "From[T]") -> "Array[T]":
    #     return super().__new__(cls, args)
    def apply(self, func: Callable[[T], U]) -> "Array":
        return Array((func(val) for val in self))

    def filter(self, condition: Callable[[T], bool]) -> "Array":
        return Array((val for val in self if condition(val)))

    # def reduce(self, func: Callable[[V, T], V], accumulator: V) -> V:
    #     result = accumulator
    #     for val in self:
    #         result = Array((func(accumulator, val))).reduce(func, result)
    #     return result

    def effect(self, func: Callable[[T], None]) -> "Array":
        for val in self:
            func(val)
        return self


class Parser(From[str]):
    pass


if __name__ == "__main__":
    input = "Hello, World! This is a test. The quick brown fox jumps over the lazy dog."

    Array(input).apply(Head).effect(print)
    Array(input).filter(lambda x: x != " ").effect(print)
    pass

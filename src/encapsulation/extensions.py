from base import From
from typing import TypeVar

T = TypeVar("T")

class SideEffect(From[T]):
    """To add a side-effect, all you need to do is implement the `Fn` method """
    def Fn(self, func, *args):
        print("hi there")
        func(*args) 

@SideEffect().apply
def some_action(val: str):
    print("[doing something]")

if __name__ == "__main__":
    some_action("hiho").to("me").to("now", print)
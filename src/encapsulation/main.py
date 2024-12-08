from typing import TypeVar, Generic, Callable
from functools import wraps

T = TypeVar("T")

class Nothing(): 
    """Base class"""

    def __init__(self):
        self.val = None

    def __eq__(self, other):
        return self.val == other.val

    def __repr__(self):
        return f"<{self.__class__.__name__} val=({self.val})>"

    def __bool__(self): 
        return True if self.val else False
        
    def __call__(self, func):
        return self.effect(func)
   
    def effect(self, func)
        """Return self while applying `func` to self.val"""
        func(self.val)
        return self

    @classmethod
    def unit(cls, val=None):
        """Return a new instance of the same encapsulating class, wrapping `val`"""
        return cls(val)

    def bind(self, func):
        """Return a new wrapped instance with `func` applied to self.val"""
        return self.unit(func(self.val))

class Just(Nothing, Generic[T]):
    def __init__(self, val: T):
        assert(val is not None)
        self.val = val
    

class Maybe(Just[T]):
    def __init__(self, val):
        self.val = val

    def bind(self, func):
        if self.val: return self.unit(func(self.val))
        return Nothing()



class Writer(Maybe[str]):
    def write(self, text=""):
        return self.bind(
            lambda s: s + text
            )   

class Reader(Maybe[str]):  
    def read(self, func=id):
        return self.bind(input)(func)

# incomplete
class IO(Reader, Writer):
    def __iter__(self):
        while self.val:
            yield self.bind(input)
    
    def repl(self, func=id):
        for val in self(func): val

class From(Maybe):
    def __getattr__(self, attr):
        assert(hasattr(self.val, attr))
        return self.val.__getattr__(attr)
    
    def __add__(self, other):
        return self.bind(lambda a: a + other)
    
    def __mul__(self, val):
        return self.bind(lambda a: a * val)
    
    def __div__(self, other):
        return self.bind(lambda a: a / val) if val != 0 else Nothing()

def to(cls: type):
    def outer(func):
       return lambda *args, **kwargs: cls(*args, **kwargs).bind(func)
    return outer
    
    


if __name__ == "__main__":
    m = Maybe(2)
    assert(m.bind(lambda x: 3*x) == Maybe(6))
    assert(m)
    assert(not Maybe(None).bind(lambda x: 3*x))
    assert(Maybe(None) == Nothing())

    f = From(2)
    (f * 3 + 2)(print) 

    @to(From)
    def test(s):
        return f"[{s}]" 

    assert(test("hi")(print) == Just("[hi]"))
    a = "b"
    assert(test("a").bind(eval) == Just(["b"]))


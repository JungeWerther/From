from typing import Any, Callable, TypeVar, Generic, Tuple
from dataclasses import dataclass
from copy import copy

T = TypeVar("T")
F = Callable[[T], Any] 

def ID[T](x: T) -> T: return x

class From(Generic[T]):
    """`From` monad. Nice! 

        Usage: From[<type T>](<type U>) -> From[<type U>]
        Hint: Try adding the 'print' function as second argument of your .to() method
    """

    def __init__(self, *args: F[T] | T, **kwargs):   
        self.args = args
        self.kwargs = self.__parse_kwargs(**kwargs)
    
    def __parse_kwargs(self, **kwargs):
        for k,v in kwargs.items():
            match k:
                case "Fn":
                    self.Fn = lambda func, *x: v(func, *x)

    def __call__(self, *args, **kwargs):
        """This one also needs work / validation"""
        assert callable(self.args[0]) 
        return self.args[0](*args, **kwargs)

    def __name__(self):
        return "[coalescing __name__]", self.__doc__

    def __repr__(self):
        return "[obfuscated]"

    @classmethod
    def _next(cls, *args, **kwargs):
        """Instantiate next object with *args"""
        return cls(*args, **kwargs)

    def _ext(self, func: F[T], *args):
        """Instantiate next object with *args, while executing self.Fn as a side effect."""
        self.Fn(func, *args)
        return self._next(*args, Fn=copy(self.Fn))

    def Fn(self, func, *args) -> None:
        """Optional functor to modify side-effect. Default: function application."""
        func(*args) 

    def apply(self, func: F[T] = ID):
        """Needs work..."""
        return lambda *f: self._next(self._ext(func, *f), *self.args)

    def to(self, to: F[T] | T, Fn: F[T | F[T]] = ID):
        """Return the value of to as From(value), while optionally applying Fn as side-effect."""
        return self._ext(Fn, to) 

    def first(self, Fn: F[T]):
        """Simply apply Fn on the current object"""
        return self._ext(Fn, *self.args)

    # def on(self, *Fn: F[T]):
    #     """on (snd) - returns 'on' applied to args, while applying 'first' to 'on' as side effect. Not quite working as expected"""
    #     return self._ext(*self.args, *Fn)

    def compose(self, Fn: F[T]):
        assert callable(self.args[0]) 
        return self._ext(ID, lambda *x: Fn(*self.args[0](*x))) # type: ignore - type is fine, just using __index__ vs * is not covariant

    def back(self):
        return self.__getstate__()



if __name__ == "__main__":
    

    
    # define any type...
    @dataclass
    class MyType():
        str: str

    
    # Just does what you want..
    t = (

        # T gets applied to the From[T] once %self.to is called
        From[MyType](
            str="ho" 
        ).to(
            MyType(str="hi")
        ).to(
            MyType(str="ho")
        ).apply(

            # state can be observed by making application explicit
            lambda x: print(x)
        )(
            MyType(str="hype-machine")
        )
        )

    q = From[MyType]        (       
        a="1"               ).to(   
        MyType(str="hi")    ).apply(
        lambda x: 
            From(print)
            .to(x)          )(      
                "right"     )
    
    assert isinstance(q, From)
    
    
    
    
    # turn w into a wrapped function 

    @From().apply
    def w(*args, **kwargs): 
        print("[w][could be obfuscated]", *args)
    # how natural is this result!
    # this is how easy it is to define a decorator!!
    

    # @
    def g(func: Callable, *args):
        """You are an agent"""

        print("[g function]", func)
        print("[g]", func.__doc__)
        print("[g][args]", *args)

    
    agent = From(Fn=g).apply

    # Automatic task scheduling. If g is an agent, it can solve [task]
    @agent
    def task(z: str, *args):
        """This is the task you must fulfill"""
        
        print("[this gets handled inside the task]", z)


    # Observe that this won't work:
    # @From[MyType].to
    # def h(i):
    #     print("h func", i)
    # 
    # that's because *to* is an 'output function'
    # i.e. I do not want to expose variables
    # the program doesn't compute any further,
    #  

    @agent
    def pog(msg: str, *args):
        print("[deeper logging]", msg)

    # Exercise: run the following command and compare.
    #               Do you understand the ouput?

    obj = w(
        10                      ).to(# handled in w (obfuscated)
        "[secret password]"     ).to(# handled in w (obfuscated)
        "[yeye]", print         ).to(# handled in __main__
        40, task,               ).to(# handled in ?
        MyType(str="100"), w    ).to(# handled in ?

        pog("zarathustra"), print
        ) # handled in ?

    
    # notice how obj is obfuscated untill called:
    print(
        obj.to(any), 
        obj.to(

            lambda x, y: 2*x + y
        )(y=3, x=50) * 2 # type:ignore - From[int] ~ int 
        )

    funny: F[Tuple[int, int]] = lambda x, y: (3*x, 99*y)
    
    def unit_test(func):
        print(func(1, 2) == (9, 19602))

    # product types:
    # first - returns 'first' applied to args, while applying 'on' to 'first' as side effect
    # on (snd) - returns 'on' applied to args, while applying 'first' to 'on' as side effect. 
    #   -> THIS ONLY WORKS if your object is unary!
    # again, frist, second and compose can be interchanged freely, as long as the types match up!

    print(
        From[Tuple[int, int]](
            funny       ).compose(
            funny       ).first(
            print       ).first(
            unit_test   ).compose(
            funny       )(
            2, 2        )
    )

    task("hi")
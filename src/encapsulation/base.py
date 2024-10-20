from typing import Any, Callable, TypeVar, Generic, Tuple
from dataclasses import dataclass

T = TypeVar("T")
    
class From(Generic[T]):
    """`From` monad. Nice! 'From' has to only show 'to'. Easy, right?
    Inductive type...

        Usage: From[<type T>](<type U>) -> From[<type U>]
        Hint: Try adding the 'print' function as second argument of your .to() method
    """

    def __init__(self, *args: Callable[..., T], **kwargs):   
        self.args = args
        self.kwargs = kwargs
        
    def __call__(self, *_, **kwargs):
        """This one also needs work / validation"""
        assert(isinstance(arg, Callable) for arg in self.args)
        return self.args[0](*_, **kwargs) 

    def __name__(self):
        return "[coalescing __name__]", self.__doc__

    def __repr__(self):
        return "[obfuscated]"

    @classmethod
    def _next(cls, *args):
        return cls(*args)

    def _ext(self, func: Callable, *args):
        self.Fn(func, args)
        return self._next(*args)

    def Fn(self, func, *args):
        func(*args) 

    def apply(self, func: Callable = id):
        return lambda *args: self._ext(func, *args)

    def to(self, to: Callable[[T], Any] | T, Fn: Callable[[T], Any] = id):
        return self._ext(Fn, to) 

    def first(self, Fn: Callable):
        return self._ext(Fn, *self.args)

    def on(self, *Fn: Callable):
        """on (snd) - returns 'on' applied to args, while applying 'first' to 'on' as side effect. Not quite working as expected"""
        return self._ext(*self.args, *Fn)

    def compose(self, Fn: Callable):
        return self._ext(id, lambda *x: Fn(*self.args[0](*x)))

    def back(self):
        return self.__getstate__()



if __name__ == "__main__":
    
    # how natural is this result!
    # this is how easy it is to define a decorator!!
    agent = From(str).apply
    
    # define any type...
    @dataclass
    class MyType():
        str: str

    
    # Just does what you want..
    t = (

        # T gets applied to the From[T] once %self.to is called
        From[MyType](
            lambda x: 2*x
        ).to(
            MyType(str="hi")
        ).to(
            MyType(str="ho")
        ).apply(

            # state can be observed by making application explicit
            lambda x: print(x)
        )(
            MyType(str="hype-machine")
        ).to(
            MyType(str="hahaha")
            )
        )

    # You can order apply and to statements in arbitrary fashion here. 
    q = From[MyType]        (       
        a="1"               ).to(   
        MyType(str="hi")    ).apply(
        lambda x: 
            From(print)
            .to(x)          )(      
                "right"     ).to(
        MyType(str="R")     )


    # Decorators were never so easy...
    @From().apply
    def w(*args, **kwargs): 
        print("[w][could be obfuscated]", *args)

    # Equivalent notation:
    @agent
    def g(z: Callable):
        """You are an agent"""

        print("[g function]", z.__name__)
        print("[g]", z.__doc__)


    # Automatic task scheduling. If g is an agent, it can solve [task]
    @g
    def task(z: str):
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
    def pog(msg: str):
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
        )(y=3, x=50) * 2
        )

    id = lambda v: print(v)
    funny = lambda x, y: (3*x, 99*y) 
    test = lambda v: print(v(*[1, 1]))

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
            test        )(
            2, 2        )
    )
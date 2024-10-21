# The encapsulation library 

Introducing: the `From` class.

Decorators made easy, piece-wise oprations on product types, controlling evaluation order.

For maintainable data pipelines.

It's a monad (sorry 🍪).

## Installation

`pip install -e encapsulation`

## Getting started

Get started by 

```
from encapsulation.base import From

obj = From(
    lambda x: "hi " + x        
    )("there")

print(obj)
```

*Easy* decorator superpowers:

```python
from encapsulation.base import From

def inspect(x: str): 
    """some function you want to call each time"""
    print(x)

def compose(func, *args):
    func(*args)

# you can also turn inspect into a proper decorator using
agent = From(Fn=compose).apply

@agent
def task(val: str):
    """Some task"""
    print("[this is a task]")

task("hiho")
```

The above will both evaluate `task("hiho")` and leave its return type untouched, while also
executing `agent(task)` each time the `task` function gets called.

Congratulations! You can now stop writing convoluted wrappers each time you want to implement a decorator, and use `From` instead 😎
# The encapsulation library

![image](https://github.com/user-attachments/assets/16f602f0-5718-468c-9114-3e3e673ca02f)

Introducing: the `From` class.
For maintainable data pipelines.

- Adds new syntactic sugar to python!
- Cleanly abstract side-effects without interrupting control flow
- Elegant decorators included
- Decorate any function with `@to(From)` to make it monadic
- Explicit function composition
- Currently implemented: Maybe
- Coming soon: Result, IO

## Installation

`pip install -e encapsulation`

## Getting started

Get started by

```python
from encapsulation.base import Maybe

Maybe("a") + "b" # outputs <Maybe val=(ab)>
Maybe(None) * 2 # outputs <Nothing val=(None)>
```

_Easy to use_ decorators that elevate functions to return wrapped values instead:

```python
from encapsulation.base import Maybe, to

def add1(n: int):
    return n + 1

@to(Maybe)
def test(s: int):
    return s

test(1) << add1 & print << add1 # prints '2', while returning Maybe(3)
```

You can chain computations using compose(). For example

```python
from encapsulation.base import Just, compose

@to(Just[int])
def add2(s: int):
    return s + 2

compose(Just(1), add2, add2) # equals Just(5)
```

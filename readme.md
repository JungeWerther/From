# The encapsulation library

Introducing: the `From` class.
For maintainable data pipelines.

Adds new syntactic sugar to python!

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

test(1).bind(add1).effect(print) # prints '2'
```

You can chain computations using compose(). For example

```python
from encapsulation.base import Just, compose

@to(Just[int])
def add2(s: int):
    return s + 2

compose(Just(1), add2, add2) # equals Just(5)
```

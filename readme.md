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
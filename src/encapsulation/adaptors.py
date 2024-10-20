from base import From
from typing import Callable, Any

# Adding an agent to a function will let the function do exactly what it was going to.
# However, it can also be used as a decorator to add tasks that must be completed exactly once
# before anything else.
# 
# for example, if you want to check whether a user is authenticated only once,
#   with an token_expiry > max_function_timeout 
#   on which a set of functions depend,
#   you can decorate each function without changing their input  
# 
# So it is a check to see if 'requirements are met'

check = From[str]().apply

@check
def inspect(v: Any):
    """Inspect any object."""

    print("\n[bot] ~> |", v)
    print(" [description]", v.__doc__)
    print("  [callable]", isinstance(v, Callable))
    print("===\n")

    return v

if __name__ == "__main__":
    
    @inspect
    def good(val):
        """[Good...]"""
        print("[good]", val)
 
    # the type of `good` becomes `From`!
    # assert type(inspect(good)) == type(inspect(inspect(good))) 

    good("morning") # always runs without any change (input and output types remain the same) 
    print("============")


    #will evaluate (in order):
    # - inspect(good)
    # - print(good)
    # - good("morning") 
    inspect(good).first(print)("morning") 

    #use `to` to reset the evaluation order. Evaluates
    # - 
    inspect(
        "morning?"      ).to(
        "morning to you too.", print).to(
        "hello", good 
        )

    # you can also turn inspect into a proper decorator using
    agent = From().apply(inspect)

    @agent
    def task(val: str):
        """Some task"""
        print("[this is a task]")
        return "hohoho"

    print(task("hiho"))


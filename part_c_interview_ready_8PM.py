# Part C — Interview Questions

## Q1 — LEGB Rule
# LEGB stands for:
# L: Local
# E: Enclosing
# G: Global
# B: Built-in

# Python searches variables in this order.

x = "global"

def outer():

    x = "enclosing"

    def inner():
        x = "local"
        print(x)

    inner()

# Global keyword: global x
# This allows modifying global variables inside a function.
# Why it is a code smell:
# - makes debugging harder
# - breaks modular design
# - functions depend on external state
# Better alternative: pass variables as parameters, return values.


## Q2 — Memoize Function

def memoize(func):

    cache = {}

    def wrapper(*args):

        if args in cache:
            return cache[args]

        result = func(*args)
        cache[args] = result

        return result

    return wrapper


@memoize
def fibonacci(n):

    if n <= 1:
        return n

    return fibonacci(n-1) + fibonacci(n-2)


## Q3 — Debug Code

# Original buggy code and fix details:
# Bug 1 — Mutable Default: cart=[] is shared.
# Bug 2 — Scope Problem: total += len(cart) needs global declaration or better parameter passing.

def add_to_cart(item, cart=None, total=0):

    if cart is None:
        cart = []

    cart.append(item)

    total += len(cart)

    return cart

if __name__ == "__main__":
    outer() # Result: local
    print("Fibonacci(10):", fibonacci(10))
    print("Cart:", add_to_cart('apple'))

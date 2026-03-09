import time
from functools import wraps


def timer(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print("Execution time:", end - start)

        return result

    return wrapper


def logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        print("Function:", func.__name__)
        print("Arguments:", args, kwargs)

        result = func(*args, **kwargs)

        print("Return:", result)

        return result

    return wrapper


def retry(max_attempts=3):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            attempts = 0

            while attempts < max_attempts:

                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    attempts += 1
                    print("Retrying...", attempts)

            raise Exception("Max attempts reached")

        return wrapper

    return decorator

if __name__ == "__main__":
    # Example usage
    @timer
    @logger
    def demo_function(n):
        time.sleep(n)
        return f"Slept for {n}s"

    print(demo_function(0.1))

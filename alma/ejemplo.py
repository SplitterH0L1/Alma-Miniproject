def a_decorator(func):
    def wrapper(*args, **kwargs):
        """A wrapper function"""
        # Extend some capabilities of func
        func()
    return wrapper
  
@a_decorator
def first_function():
    """This is docstring for first function"""
    print("first function")
  
@a_decorator
def second_function(a):
    """This is docstring for second function"""
    print("second function")
  
print(first_function.__name__)
print(first_function.__doc__)
print(second_function.__name__)
print(second_function.__doc__)
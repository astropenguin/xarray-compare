__all__ = ["dataarray_method"]


# standard library
from functools import wraps
from typing import Callable


# dependencies
from xarray import register_dataarray_accessor


# main features
def dataarray_method(func: Callable) -> Callable:
    """Decorator to make a DataArray function available as a method."""

    class Accessor:
        def __init__(self, dataarray):
            self.dataarray = dataarray

        @wraps(func)
        def __call__(self, *args, **kwargs):
            return func(self.dataarray, *args, **kwargs)

    register_dataarray_accessor(func.__name__)(Accessor)
    return func

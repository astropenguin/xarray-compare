__all__ = [
    "isbetween",
    "isin",
    "ismatch",
    "isnotbetween",
    "isnotin",
    "isnotmatch",
]


# standard library
import re
from enum import Enum
from typing import Any, Optional, Pattern, Union
from operator import ge, gt, le, lt


# dependencies
import numpy as np
import xarray as xr
from .utils import dataarray_method


# constants
class Intervals(Enum):
    LORO = "()"  # left-open, right-open
    LCRO = "[)"  # left-closed, right-open
    LORC = "(]"  # left-open, right-closed
    LCRC = "[]"  # left-closed, right-closed


OPERATORS = {
    Intervals.LORO: (gt, lt),
    Intervals.LCRO: (ge, lt),
    Intervals.LORC: (gt, le),
    Intervals.LCRC: (ge, le),
}


# main features
@dataarray_method
def isbetween(
    dataarray: xr.DataArray,
    lower: Optional[Any] = None,
    upper: Optional[Any] = None,
    interval: str = "[]",
) -> xr.DataArray:
    operators = OPERATORS[Intervals(interval)]

    if np.issubsctype(dataarray, np.datetime64):
        if lower is not None:
            lower = np.asarray(lower, np.datetime64)

        if upper is not None:
            upper = np.asarray(upper, np.datetime64)

    if lower is None:
        lower_index = xr.ones_like(dataarray, bool)
    else:
        lower_index = operators[0](dataarray, lower)

    if upper is None:
        upper_index = xr.ones_like(dataarray, bool)
    else:
        upper_index = operators[1](dataarray, upper)

    return lower_index & upper_index


def isin(dataarray: xr.DataArray, values: Any) -> xr.DataArray:
    return dataarray.isin(values)


@dataarray_method
def ismatch(dataarray: xr.DataArray, pattern: Union[Pattern, str]) -> xr.DataArray:
    if not np.issubdtype(dataarray.dtype, np.str_):
        raise TypeError("Can only be used for string DataArray.")

    pattern = re.compile(pattern)
    search = np.vectorize(lambda string: pattern.search(string))

    index = xr.zeros_like(dataarray, bool)
    index.values = search(dataarray.values).astype(bool)

    return index


@dataarray_method
def isnotbetween(
    dataarray: xr.DataArray,
    lower: Optional[Any] = None,
    upper: Optional[Any] = None,
    interval: str = "[]",
) -> xr.DataArray:
    return ~isbetween(dataarray, lower, upper, interval)


@dataarray_method
def isnotin(dataarray: xr.DataArray, values: Any) -> xr.DataArray:
    return ~isin(dataarray, values)


@dataarray_method
def isnotmatch(dataarray: xr.DataArray, pattern: Union[Pattern, str]) -> xr.DataArray:
    return ~ismatch(dataarray, pattern)

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
from typing import Any, Pattern, Union
from operator import ge, gt, le, lt


# dependencies
import numpy as np
import xarray as xr
from .utils import dataarray_method


# constants
class Intervals(Enum):
    """Definitions of mathematical intervals."""

    LORO = "()"  #: left-open, right-open
    LCRO = "[)"  #: left-closed, right-open
    LORC = "(]"  #: left-open, right-closed
    LCRC = "[]"  #: left-closed, right-closed


OPERATORS = {
    Intervals.LORO: (gt, lt),
    Intervals.LCRO: (ge, lt),
    Intervals.LORC: (gt, le),
    Intervals.LCRC: (ge, le),
}


# main features
@dataarray_method
def isbetween(
    dataarray: xr.DataArray, lower: Any, upper: Any, interval: str = "[]",
) -> xr.DataArray:
    """Test whether each value in a DataArray falls within an interval.

    An interval is defined by ``lower``, ``upper``, and ``interval``.
    For example, if ``interval`` is given as ``'[)'``, the interval of
    [lower, upper) will be used for the evaluation. Then the function
    returns ``(dataarray >= lower) & (dataarray < upper)``.

    Args:
        dataarray: DataArray to be compared.
        lower: Lower endpoint of the interval.
            If ``None`` is given, then the lower end is not evaluated.
        upper: Upper endpoint of the interval.
            If ``None`` is given, then the upper end is not evaluated.
        interval: String which determine the type of the interval.
            Either ``'[]'`` (closed; default), ``'[)'`` (L-closed, R-open),
            ``'(]'`` (L-open, R-closed), or ``'()'`` (open) is accepted.

    Returns:
        Boolean DataArray each value of which is ``True``
        where it falls within the interval and ``False`` otherwise.

    Raises:
        ValueError: Raised if ``interval`` is not correct.

    """
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
    """Equivalent to dataarray.isin().

    Args:
        dataarray: DataArray to be compared.
        values: Scalar value or sequence of values.

    Returns:
        Boolean DataArray each value of which is ``True`` where it is
        equivalent to ``values`` or in ``values`` and ``False`` otherwise.

    """
    return dataarray.isin(values)


@dataarray_method
def ismatch(dataarray: xr.DataArray, pattern: Union[Pattern, str]) -> xr.DataArray:
    """Test whether each string in a DataArray matches a regex pattern.

    Args:
        dataarray: String DataArray to be compared.
        pattern: String or compiled regex pattern.

    Returns:
        Boolean DataArray each value of which is ``True``
        where it matches the pattern and ``False`` otherwise.

    Raises:
        TypeError: Raised if ``dataarray.dtype`` is not string-like.

    """
    if not np.issubdtype(dataarray.dtype, np.str_):
        raise TypeError("Can only be used for string DataArray.")

    pattern = re.compile(pattern)
    search = np.vectorize(lambda string: pattern.search(string))

    index = xr.zeros_like(dataarray, bool)
    index.values = search(dataarray.values).astype(bool)

    return index


@dataarray_method
def isnotbetween(
    dataarray: xr.DataArray, lower: Any, upper: Any, interval: str = "[]",
) -> xr.DataArray:
    """Equivalent to ~isbetween().

    Args:
        dataarray: DataArray to be compared.
        lower: Lower endpoint of the interval.
            If ``None`` is given, then the lower end is not evaluated.
        upper: Upper endpoint of the interval.
            If ``None`` is given, then the upper end is not evaluated.
        interval: String which determine the type of the interval.
            Either ``'[]'`` (closed; default), ``'[)'`` (L-closed, R-open),
            ``'(]'`` (L-open, R-closed), or ``'()'`` (open) is accepted.

    Returns:
        Boolean DataArray each value of which is ``True`` where
        it does **not** fall within the interval and ``True`` otherwise.

    Raises:
        ValueError: Raised if ``interval`` is not correct.

    """
    return ~isbetween(dataarray, lower, upper, interval)


@dataarray_method
def isnotin(dataarray: xr.DataArray, values: Any) -> xr.DataArray:
    """Equivalent to ~isin().

    Args:
        dataarray: DataArray to be compared.
        values: Scalar value or sequence of values.

    Returns:
        Boolean DataArray each value of which is ``True`` where it is **not**
        equivalent to ``values`` or **not** in ``values`` and ``False`` otherwise.

    """
    return ~isin(dataarray, values)


@dataarray_method
def isnotmatch(dataarray: xr.DataArray, pattern: Union[Pattern, str]) -> xr.DataArray:
    """Equivalent to ~ismatch().

    Args:
        dataarray: String DataArray to be compared.
        pattern: String or compiled regex pattern.

    Returns:
        Boolean DataArray each value of which is ``True`` where
        it does **not** match the pattern and ``False`` otherwise.

    Raises:
        TypeError: Raised if ``dataarray.dtype`` is not string-like.

    """
    return ~ismatch(dataarray, pattern)

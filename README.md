# xarray-compare

[![PyPI](https://img.shields.io/pypi/v/xarray-compare.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/xarray-compare/)
[![Python](https://img.shields.io/pypi/pyversions/xarray-compare.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/xarray-compare/)
[![Test](https://img.shields.io/github/workflow/status/astropenguin/xarray-compare/Test?logo=github&label=Test&style=flat-square)](https://github.com/astropenguin/xarray-compare/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)
[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.3988924-blue?style=flat-square)](https://doi.org/10.5281/zenodo.3988924)

xarray extension for data comparison

## TL;DR

xarray-compare is a third-party Python package which provides extra data-comparison features.
After importing the package, several DataArray methods (`dataarray.is*()`) will be available.

## Requirements

- **Python:** 3.6, 3.7, or 3.8 (tested by the author)
- **Dependencies:** See [pyproject.toml](https://github.com/astropenguin/xarray-compare/blob/master/pyproject.toml)

## Installation

```shell
$ pip install xarray-compare
```

## List of available methods

- `.isbetween(lower, upper)`: Test whether each value in a DataArray falls within an interval
- `.ismatch(pattern)`: Test whether each string in a DataArray matches a regex pattern

Methods of "not-in" version are also provided for readability.

- `.isnotin(values)`: Equivalent to `~dataarray.isin(values)` (`.isin()` is an xarray's builtin)
- `.isnotbetween(lower, upper)`: Equivalent to `~dataarray.isbetween(lower, upper)`
- `.isnotmatch(pattern)`: Equivalent to `~dataarray.ismatch(pattern)`

## Examples

xarray-compare is a just-import package.
After importing it, methods become available from normal DataArray instances.

```python
import xarray as xr
import xarray_compare
```

A method returns a boolean DataArray each value of which is `True` where that of the input DataArray fulfills the condition and `False` otherwise.
This is why it works well with the `dataarray.where()` method.

```python
da = xr.DataArray([0, 1, 1, 2, 3, 5, 8, 13])
da.where(da.isbetween(1, 4), drop=True)

# <xarray.DataArray (dim_0: 4)>
# array([1., 1., 2., 3.])
# Dimensions without coordinates: dim_0
```

```python
da = xr.DataArray(['a', 'aa', 'ab', 'bc'])
da.where(da.ismatch("^a+$"), drop=True)

# <xarray.DataArray (dim_0: 2)>
# array(['a', 'aa'], dtype=object)
# Dimensions without coordinates: dim_0
```
